#!/usr/bin/env python3
from __future__ import annotations
import argparse, datetime as dt, json, re, shutil, time, urllib.parse, urllib.request
from pathlib import Path

BROWSERUSE_BASE = "https://api.browser-use.com/api/v2"
DEFAULT_PROFILE_ID = "9e0f01a3-5227-4424-bc58-b9b226110020"


def read_prompt(repo: Path, name: str) -> str:
    return (repo / "prompts" / name).read_text()


def ensure(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def save_step(run_dir: Path, step: str, prompt: str, story: str, raw_name: str, raw_obj, normalized):
    d = run_dir / "steps" / step
    ensure(d)
    (d / "prompt.txt").write_text(prompt)
    (d / "story.md").write_text(story)
    if isinstance(raw_obj, str):
        (d / raw_name).write_text(raw_obj)
    else:
        (d / raw_name).write_text(json.dumps(raw_obj, indent=2))
    (d / "normalized.json").write_text(json.dumps(normalized, indent=2))


def browseruse_req(api_key: str, method: str, path: str, payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        BROWSERUSE_BASE + path,
        data=data,
        method=method,
        headers={"Content-Type": "application/json", "X-Browser-Use-API-Key": api_key},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))


def browseruse_run(api_key: str, profile_id: str, task_prompt: str, timeout_s: int = 1200):
    session = browseruse_req(api_key, "POST", "/sessions", {"profileId": profile_id, "persistMemory": True, "keepAlive": False})
    task = browseruse_req(api_key, "POST", "/tasks", {"task": task_prompt, "sessionId": session["id"]})
    tid = task["id"]
    start = time.time()
    status = None
    while time.time() - start < timeout_s:
        status = browseruse_req(api_key, "GET", f"/tasks/{tid}/status")
        if status.get("status") in ("finished", "failed", "stopped"):
            break
        time.sleep(12)
    return {"session": session, "task": task, "status": status}


def parse_jsonish(s: str):
    if not s:
        return {}
    m = re.search(r"```(?:json)?\s*([\s\S]*?)```", s)
    if m:
        s = m.group(1)
    try:
        return json.loads(s)
    except Exception:
        return json.loads(s.replace("\\'", "'"))


def alphaxiv_papers(topic: str, target_date: str):
    # alphaXiv first (explicitly hits alphaxiv.org)
    q = urllib.parse.quote(topic)
    url = f"https://www.alphaxiv.org/search?q={q}"
    html = urllib.request.urlopen(url, timeout=40).read().decode("utf-8", errors="ignore")
    ids = list(dict.fromkeys(re.findall(r"/abs/(\d{4}\.\d{4,5})", html)))[:8]

    papers = []
    for aid in ids:
        api = f"https://export.arxiv.org/api/query?id_list={aid}"
        x = urllib.request.urlopen(api, timeout=40).read().decode("utf-8", errors="ignore")
        t = re.search(r"<title>([\s\S]*?)</title>", x)
        # first title is feed title; get entry title
        titles = re.findall(r"<title>([\s\S]*?)</title>", x)
        title = re.sub(r"\s+", " ", titles[1]).strip() if len(titles) > 1 else f"arXiv {aid}"
        summs = re.findall(r"<summary>([\s\S]*?)</summary>", x)
        summary = re.sub(r"\s+", " ", summs[0]).strip() if summs else ""
        papers.append({
            "title": title,
            "alphaXivUrl": f"https://www.alphaxiv.org/abs/{aid}",
            "arxivUrl": f"https://arxiv.org/abs/{aid}",
            "insight": (summary[:220] + "...") if len(summary) > 220 else summary,
        })
    return {"queryUrl": url, "paperIds": ids, "papers": papers}


def exa_people(api_key: str, queries: list[str]):
    out = []
    for q in queries:
        payload = {"query": q, "type": "deep", "category": "people", "numResults": 10, "contents": {"text": True}}
        req = urllib.request.Request(
            "https://api.exa.ai/search",
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers={"x-api-key": api_key, "Content-Type": "application/json", "User-Agent": "code-rl-briefing/1.0"},
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                resp = json.loads(r.read().decode("utf-8"))
        except Exception as e:
            resp = {"error": str(e)}
        out.append({"payload": payload, "response": resp})
    return out




def youtube_search(api_key: str, query: str, date: str):
    start = f"{date}T00:00:00Z"
    end = f"{date}T23:59:59Z"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "order": "date",
        "maxResults": 15,
        "publishedAfter": start,
        "publishedBefore": end,
        "key": api_key,
    }
    url = "https://www.googleapis.com/youtube/v3/search?" + urllib.parse.urlencode(params)
    try:
        raw = json.loads(urllib.request.urlopen(url, timeout=60).read().decode("utf-8"))
    except Exception as e:
        raw = {"error": str(e), "url": url}

    transcript_error = None
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
    except Exception as e:
        YouTubeTranscriptApi = None
        transcript_error = f"youtube-transcript-api unavailable: {e}"

    items = []
    for it in raw.get("items", []) if isinstance(raw, dict) else []:
        vid = (((it.get("id") or {}).get("videoId")) or "")
        sn = it.get("snippet") or {}
        transcript = None
        if vid and YouTubeTranscriptApi is not None:
            try:
                segs = YouTubeTranscriptApi.get_transcript(vid)
                transcript = " ".join((x.get("text", "") for x in segs))[:4000]
            except Exception as e:
                transcript = f"[transcript unavailable: {e}]"
        items.append({
            "videoId": vid,
            "title": sn.get("title", ""),
            "channelTitle": sn.get("channelTitle", ""),
            "publishedAt": sn.get("publishedAt", ""),
            "description": sn.get("description", "")[:400],
            "url": f"https://www.youtube.com/watch?v={vid}" if vid else "",
            "transcript": transcript,
        })
    return {"requestUrl": url, "raw": raw, "videos": items, "transcriptLibrary": "youtube-transcript-api", "transcriptLibraryError": transcript_error}


def publish_run(repo: Path, date: str):
    src = repo / "data" / "runs" / date
    dst = repo / "public" / "data" / "runs" / date
    ensure(dst)
    for p in src.rglob("*"):
        t = dst / p.relative_to(src)
        if p.is_dir():
            ensure(t)
        else:
            ensure(t.parent)
            shutil.copy2(p, t)
    files = [{"path": "/" + str(p.relative_to(repo / "public")).replace("\\", "/"), "bytes": p.stat().st_size}
             for p in sorted(dst.rglob("*")) if p.is_file()]
    (dst / "raw-index.json").write_text(json.dumps({"date": date, "files": files}, indent=2))


def run(repo: Path, topic: str, date: str, browseruse_key: str, exa_key: str | None, youtube_key: str | None):
    run_dir = repo / "data" / "runs" / date
    ensure(run_dir)

    # Step 01: AlphaXiv papers
    p01 = read_prompt(repo, "step01_alphaxiv_query.txt").format(topic=topic, window="last 24 hours")
    raw01 = alphaxiv_papers(topic, date)
    save_step(
        run_dir,
        "step-01-papers-alphaxiv",
        p01,
        "Visited alphaxiv.org search first, extracted paper IDs from AlphaXiv results, then enriched with arXiv metadata.",
        "raw.json",
        raw01,
        raw01["papers"],
    )

    # Step 02: SuperGrok topic pass
    p02 = read_prompt(repo, "step02_supergrok_topic.txt").format(topic=topic)
    r02 = browseruse_run(browseruse_key, DEFAULT_PROFILE_ID, p02)
    n02 = parse_jsonish((r02.get("status") or {}).get("output") or "{}")
    save_step(
        run_dir,
        "step-02-supergrok-topic",
        p02,
        "Called browser-use API with saved profile, opened X + SuperGrok, ran the exact topic query.",
        "raw.json",
        r02,
        n02,
    )

    # Step 03: per-paper SuperGrok discussion
    per = []
    for paper in raw01["papers"][:6]:
        p03 = read_prompt(repo, "step03_supergrok_paper_discussion.txt").format(paper_title=paper["title"])
        r03 = browseruse_run(browseruse_key, DEFAULT_PROFILE_ID, p03)
        n03 = parse_jsonish((r03.get("status") or {}).get("output") or "{}")
        per.append({"paper": paper["title"], "prompt": p03, "raw": r03, "normalized": n03})
    save_step(
        run_dir,
        "step-03-supergrok-paper-discussion",
        "Per-paper prompts are stored in normalized.json per item.",
        "For each AlphaXiv paper title, asked SuperGrok EXACTLY: what are people saying about this exact paper title?",
        "raw.json",
        per,
        per,
    )

    # Step 04: signals pass
    handles = ["karpathy", "natolambert", "willccbb", "HamelHusain", "LangChain"]
    p04 = read_prompt(repo, "step04_supergrok_signals.txt").format(handles_csv=",".join(handles), topic=topic)
    r04 = browseruse_run(browseruse_key, DEFAULT_PROFILE_ID, p04)
    n04 = parse_jsonish((r04.get("status") or {}).get("output") or "{}")
    save_step(run_dir, "step-04-supergrok-signals", p04, "Asked SuperGrok account-by-account what each tracked signal discussed today.", "raw.json", r04, n04)

    # Step 05: history pass
    p05 = read_prompt(repo, "step05_supergrok_history_updates.txt")
    r05 = browseruse_run(browseruse_key, DEFAULT_PROFILE_ID, p05)
    n05 = parse_jsonish((r05.get("status") or {}).get("output") or "{}")
    save_step(run_dir, "step-05-supergrok-history-updates", p05, "Asked SuperGrok for 1/3/7/14-day update signals tied to prior claims.", "raw.json", r05, n05)

    # Step 06: Exa people
    q_lines = [x.strip() for x in read_prompt(repo, "step06_exa_people_queries.txt").format(topic=topic).splitlines() if x.strip()]
    r06 = exa_people(exa_key, q_lines) if exa_key else [{"error": "EXA_API_KEY missing"}]
    save_step(run_dir, "step-06-exa-people", "Queries in prompts/step06_exa_people_queries.txt", "Called Exa API with type=deep category=people using exact query payloads.", "raw.json", r06, r06)

    # Step 07: YouTube search
    p07 = read_prompt(repo, "step07_youtube_search.txt").format(topic=topic, date=date)
    r07 = youtube_search(youtube_key, topic, date) if youtube_key else {"error": "YOUTUBE_DATA_API_KEY missing"}
    save_step(run_dir, "step-07-youtube-search", p07, "Called YouTube Data API search endpoint for same-day topic videos, then attempted transcript fetch via youtube-transcript-api for each videoId; persisted request + response + transcript results.", "raw.json", r07, r07.get("videos", []) if isinstance(r07, dict) else r07)

    # Step 08: synthesis (file-backed)
    one = run_dir / "one-pager.md"
    one.write_text(
        f"# One-Pager — {topic} ({date})\n\n"
        f"Built from step outputs under data/runs/{date}/steps/.\n\n"
        "- Check step-01 for AlphaXiv paper discovery.\n"
        "- Check step-02/03/04/05 for SuperGrok passes.\n"
        "- Check step-06 for Exa deep people payloads and responses.\n"
        "- Check step-07 for YouTube same-day search artifacts.\n"
    )

    # Convenience rollup
    rollup = {
        "topic": topic,
        "date": date,
        "papers": raw01["papers"],
        "supergrokTopic": n02,
        "paperDiscussion": [x["normalized"] for x in per],
        "signals": n04,
        "history": n05,
        "exa": r06,
        "youtube": r07,
    }
    (run_dir / "briefing-rollup.json").write_text(json.dumps(rollup, indent=2))
    (run_dir / "run-story.md").write_text(
        "# Run Story\n\n"
        "This run executed scripted steps in order.\n\n"
        "1. AlphaXiv paper discovery (step-01)\n"
        "2. SuperGrok topic pass (step-02)\n"
        "3. SuperGrok per-paper discussion (step-03)\n"
        "4. SuperGrok signals account pass (step-04)\n"
        "5. SuperGrok historical updates pass (step-05)\n"
        "6. Exa deep people pass (step-06)\n"
        "7. YouTube search pass (step-07)\n"
        "8. File-backed synthesis (step-08)\n"
    )

    publish_run(repo, date)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--topic", default="What is the latest in code RL environments and human data?")
    ap.add_argument("--date", default=dt.date.today().isoformat())
    ap.add_argument("--browseruse-api-key", default=None)
    ap.add_argument("--exa-api-key", default=None)
    ap.add_argument("--youtube-api-key", default=None)
    args = ap.parse_args()

    import os
    bkey = args.browseruse_api_key or os.environ.get("BROWSER_USE_API_KEY")
    ekey = args.exa_api_key or os.environ.get("EXA_API_KEY")
    ykey = args.youtube_api_key or os.environ.get("YOUTUBE_DATA_API_KEY")
    if not bkey:
        raise SystemExit("Missing BROWSER_USE_API_KEY")

    repo = Path(args.repo).resolve()
    run(repo, args.topic, args.date, bkey, ekey, ykey)
    print(json.dumps({"ok": True, "date": args.date, "runDir": str(repo / 'data' / 'runs' / args.date)}, indent=2))


if __name__ == "__main__":
    main()
