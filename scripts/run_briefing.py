#!/usr/bin/env python3
"""
Run the Code-RL daily briefing pipeline end-to-end.

Pipeline (wired to Ryan's requested process):
1) Papers first (arXiv/alphaXiv)
2) Initial X pass
3) "People talking about <paper title>" pass
4) Signals-account pass
5) Historical (1/3/7/14 day) bullet update pass
6) exa.ai blog query pass
7) Persist ALL raw files, then synthesize one-pager
8) Publish raw files under public/data/runs/<date>/
"""

from __future__ import annotations
import argparse
import datetime as dt
import email.utils
import json
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


def sh(cmd: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, shell=True, cwd=str(cwd) if cwd else None, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def bird_search(repo: Path, query: str, count: int = 30) -> dict:
    cmd = f"bird search --json -n {count} {subprocess.list2cmdline([query])}"
    p = sh(cmd, cwd=repo)
    if p.returncode != 0:
        return {"query": query, "error": p.stderr.strip(), "items": []}
    try:
        obj = json.loads(p.stdout)
        items = obj if isinstance(obj, list) else obj.get("tweets") or obj.get("data") or []
        return {"query": query, "items": items}
    except Exception:
        return {"query": query, "error": "json_parse", "items": []}


def bird_user_tweets(repo: Path, handle: str, count: int = 25) -> list:
    cmd = f"bird user-tweets --json -n {count} {subprocess.list2cmdline([handle])}"
    p = sh(cmd, cwd=repo)
    if p.returncode != 0:
        return []
    try:
        obj = json.loads(p.stdout)
        return obj if isinstance(obj, list) else obj.get("tweets") or obj.get("data") or []
    except Exception:
        return []


def fetch_papers_for_window(target_date: str, max_results: int = 80) -> list[dict]:
    q = 'all:("reinforcement learning" AND (code OR coding OR software OR terminal OR agent)) OR all:(RLHF OR RLVR OR "human feedback" OR "verifiable reward")'
    url = "https://export.arxiv.org/api/query?search_query=" + urllib.parse.quote(q) + f"&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
    xml = urllib.request.urlopen(url, timeout=40).read()
    root = ET.fromstring(xml)
    ns = {"a": "http://www.w3.org/2005/Atom"}

    d = dt.date.fromisoformat(target_date)
    keep_dates = {d.isoformat(), (d - dt.timedelta(days=1)).isoformat()}

    papers: list[dict] = []
    for e in root.findall("a:entry", ns):
        pub = (e.find("a:published", ns).text or "")[:10]
        if pub not in keep_dates:
            continue
        title = " ".join((e.find("a:title", ns).text or "").split())
        summary = " ".join((e.find("a:summary", ns).text or "").split())
        arx = (e.find("a:id", ns).text or "").replace("http://", "https://")
        m = re.search(r"abs/(\d+\.\d+)", arx)
        alphaxiv = f"https://www.alphaxiv.org/abs/{m.group(1)}" if m else None
        authors = [a.find("a:name", ns).text for a in e.findall("a:author", ns)]
        papers.append({
            "title": title,
            "published": e.find("a:published", ns).text,
            "arxiv": arx,
            "alphaxiv": alphaxiv,
            "summary": summary,
            "authors": authors,
        })

    # rough ranking for this topic
    kw = ["agent", "tool", "terminal", "code", "coding", "reinforcement", "rlhf", "rlvr", "verif", "reward", "swe", "gui", "human"]
    papers.sort(key=lambda x: sum(k in (x["title"] + " " + x["summary"]).lower() for k in kw), reverse=True)
    return papers[:8]


def status_url(t: dict) -> str:
    u = (t.get("author", {}) or {}).get("username", "unknown")
    i = t.get("id")
    return f"https://x.com/{u}/status/{i}" if i else ""


def synthesize_onepager(run_dir: Path, topic: str, date: str) -> None:
    x = run_dir / "raw" / "x"
    papers = json.loads((run_dir / "papers_selected.json").read_text())[:5]
    init = json.loads((x / "initial_prompt_search.json").read_text()).get("items", [])
    noise = ["konnex", "wallet", "airdrop", "crypto"]

    clean = []
    for t in init:
        tx = (t.get("text") or "").lower()
        u = ((t.get("author") or {}).get("username") or "").lower()
        if any(n in tx for n in noise) or u == "grok":
            continue
        clean.append(t)
    clean = sorted(clean, key=lambda t: t.get("likeCount", 0) + t.get("retweetCount", 0) + t.get("replyCount", 0), reverse=True)[:10]

    acct_roll = json.loads((run_dir / "signals_account_rollup.json").read_text())
    hist_roll = json.loads((run_dir / "history_updates_rollup.json").read_text())
    present = [h["date"] for h in hist_roll if not h.get("missing") and not h.get("missing_file")]
    missing = [h["date"] for h in hist_roll if h.get("missing") or h.get("missing_file")]

    lines: list[str] = []
    lines.append(f"# One-Pager — {topic} ({date})")
    lines.append("")
    lines.append("Code-RL discussion is concentrating around verifier-backed training loops and harness-level gains, while human data is becoming narrower and higher-value (targeted supervision, safety checks, privacy-preserving alignment).")
    lines.append("")
    lines.append("## Tweets")
    for t in clean:
        txt = re.sub(r"\s+", " ", (t.get("text") or "").replace("\n", " ")).strip()
        # no quote marks around tweet sentence
        lines.append(f"- {txt[:220]} → [{(t.get('author',{}) or {}).get('username','account')}]({status_url(t)})")

    lines.append("")
    lines.append("## Papers")
    for p in papers:
        insight = p["summary"][:220].rstrip(". ") + "."
        lines.append(f"- {insight} → [{p['title']}]({p['arxiv']})")

    lines.append("")
    lines.append("## Signal Movement")
    for a in acct_roll:
        tw = sorted(a.get("tweets", []), key=lambda t: t.get("likeCount", 0) + t.get("retweetCount", 0), reverse=True)
        top = tw[0] if tw else None
        if top:
            txt = re.sub(r"\s+", " ", (top.get("text") or "").replace("\n", " ")).strip()
            lines.append(f"- @{a['handle']}: {txt[:120]} → https://x.com/{a['handle']}/status/{top.get('id')}")
        else:
            lines.append(f"- @{a['handle']}: no strong same-day RL/code signal found.")

    lines.append("")
    lines.append("## Changes vs prior")
    lines.append(f"- Historical update pass found local briefing artifacts for: {', '.join(present) if present else 'none'}." )
    if missing:
        lines.append(f"- Missing local artifacts for requested offsets: {', '.join(missing)}.")

    lines.append("")
    lines.append("## Watch next 24h")
    lines.append("- Replications of tool-verification and retrieval-augmented exploration on SWE/terminal benchmarks.")
    lines.append("- More concrete evidence that rubric+execution rewards transfer from narrow domains to broad code-agent tasks.")

    (run_dir / "one-pager.md").write_text("\n".join(lines))


def publish_run_to_public(repo: Path, date: str) -> None:
    src = repo / "data" / "runs" / date
    dst = repo / "public" / "data" / "runs" / date
    ensure_dir(dst)

    for p in src.rglob("*"):
        rel = p.relative_to(src)
        t = dst / rel
        if p.is_dir():
            ensure_dir(t)
        else:
            ensure_dir(t.parent)
            shutil.copy2(p, t)

    files = []
    for p in sorted(dst.rglob("*")):
        if p.is_file():
            rel = p.relative_to(repo / "public")
            files.append({"path": "/" + str(rel).replace("\\", "/"), "bytes": p.stat().st_size})

    (dst / "raw-index.json").write_text(json.dumps({"date": date, "files": files}, indent=2))


def update_signal_file(signals_root: Path, signal_name: str, handle: str, date: str, source_file_rel: str) -> None:
    f = signals_root / f"{handle}.json"
    cur = {"name": signal_name, "role": "account", "handle": handle, "days": {}}
    if f.exists():
        try:
            cur = json.loads(f.read_text())
        except Exception:
            pass
    cur.setdefault("days", {})[date] = {"source_file": source_file_rel}
    f.write_text(json.dumps(cur, indent=2))


def extract_bullets_from_markdown(md: str) -> list[str]:
    out = []
    for ln in md.splitlines():
        s = ln.strip()
        if s.startswith("- "):
            out.append(s[2:].strip())
    return out


def exa_deep_people_search(api_key: str, query: str, num_results: int = 10) -> dict:
    req = urllib.request.Request(
        "https://api.exa.ai/search",
        data=json.dumps({
            "query": query,
            "type": "deep",
            "category": "people",
            "numResults": num_results,
            "contents": {"text": True}
        }).encode("utf-8"),
        headers={
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "User-Agent": "code-rl-briefing/1.0 (+https://github.com/zenobia-pay/code-rl-briefing)",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e), "query": query}


def run(topic: str, date: str, repo: Path, exa_api_key: str | None = None) -> Path:
    run_dir = repo / "data" / "runs" / date
    raw = run_dir / "raw"
    papers_dir = raw / "papers"
    x_dir = raw / "x"
    signals_root = repo / "data" / "signals"

    for p in [run_dir, raw, papers_dir, x_dir, signals_root]:
        ensure_dir(p)

    # 1) papers first
    papers = fetch_papers_for_window(date)
    (run_dir / "papers_selected.json").write_text(json.dumps(papers, indent=2))
    for i, p in enumerate(papers, 1):
        safe = re.sub(r"[^a-zA-Z0-9]+", "_", p["title"])[:90]
        (papers_dir / f"{i:02d}_{safe}.md").write_text(
            f"# {p['title']}\n\nPublished: {p['published']}\n\nArXiv: {p['arxiv']}\n\nalphaXiv: {p['alphaxiv']}\n\nAuthors: {', '.join(p['authors'])}\n\nAbstract:\n{p['summary']}\n"
        )

    # 2) initial X pass
    init_query = '("code RL" OR "RL environment" OR RLVR OR RLHF OR "human feedback") (coding OR agent OR terminal OR verifier)'
    init = bird_search(repo, f"{init_query} since:{date} until:{(dt.date.fromisoformat(date)+dt.timedelta(days=1)).isoformat()}", 100)
    (x_dir / "initial_prompt_search.json").write_text(json.dumps(init, indent=2))

    # 3) per-paper people talking pass
    paper_people = []
    for p in papers:
        q = f'"{p["title"]}" since:{date} until:{(dt.date.fromisoformat(date)+dt.timedelta(days=1)).isoformat()}'
        r = bird_search(repo, q, 40)
        out = {"paper": p["title"], "query": q, "results": r.get("items", [])}
        paper_people.append(out)
        safe = re.sub(r"[^a-zA-Z0-9]+", "_", p["title"])[:90]
        (x_dir / f"paper_people_{safe}.json").write_text(json.dumps(out, indent=2))
    (run_dir / "paper_people_rollup.json").write_text(json.dumps(paper_people, indent=2))

    # 4) signals account pass
    sig_src = repo / "public" / "data" / "signals-global.json"
    sigs = json.loads(sig_src.read_text()) if sig_src.exists() else []
    accounts = [s for s in sigs if s.get("role") == "account" and (s.get("links") or {}).get("x")]

    acct_roll = []
    for s in accounts:
        handle = s["links"]["x"].rstrip("/").split("/")[-1]
        tweets = bird_user_tweets(repo, handle, 25)
        out = {"signal": s, "handle": handle, "tweets": tweets}
        acct_roll.append(out)
        f = x_dir / f"signal_account_{handle}.json"
        f.write_text(json.dumps(out, indent=2))
        update_signal_file(signals_root, s.get("name", handle), handle, date, str(f.relative_to(repo)))
    (run_dir / "signals_account_rollup.json").write_text(json.dumps(acct_roll, indent=2))

    # 5) historical update pass (1,3,7,14)
    wanted = [(dt.date.fromisoformat(date) - dt.timedelta(days=d)).isoformat() for d in (1, 3, 7, 14)]
    briefings = json.loads((repo / "public" / "data" / "briefings.json").read_text())
    by_date = {b.get("date"): b for b in briefings}
    history = []

    for d in wanted:
        b = by_date.get(d)
        if not b:
            history.append({"date": d, "missing": True})
            continue
        f = repo / "public" / b["file"].lstrip("/")
        if not f.exists():
            history.append({"date": d, "missing_file": str(f)})
            continue
        bullets = extract_bullets_from_markdown(f.read_text())
        updates = []
        for bt in bullets[:20]:
            q = (bt[:150].replace("→", " ") + f" since:{date} until:{(dt.date.fromisoformat(date)+dt.timedelta(days=1)).isoformat()}")
            r = bird_search(repo, q, 12)
            updates.append({"bullet": bt, "query": q, "updates": r.get("items", [])})
        out = {"date": d, "briefing_id": b.get("id"), "file": str(f.relative_to(repo)), "bullet_updates": updates}
        history.append(out)
        (x_dir / f"history_updates_{d}.json").write_text(json.dumps(out, indent=2))
    (run_dir / "history_updates_rollup.json").write_text(json.dumps(history, indent=2))

    # 6) exa query pass (deep + people category) + saved outputs
    exa_queries = [
        "people talking about code RL environments and human data",
        "people discussing RLVR coding agents",
        "people discussing terminal bench harness engineering",
        "people discussing tool verification test-time reinforcement learning",
    ]
    exa = [{"query": q, "url": "https://exa.ai/search?query=" + urllib.parse.quote(q)} for q in exa_queries]
    (run_dir / "exa_queries.json").write_text(json.dumps(exa, indent=2))

    exa_deep_people_results = []
    key = exa_api_key
    if key:
        for q in exa_queries:
            exa_deep_people_results.append({
                "query": q,
                "request": {"type": "deep", "category": "people"},
                "response": exa_deep_people_search(key, q, num_results=10),
            })
    else:
        exa_deep_people_results = [{
            "warning": "EXA_API_KEY not set; deep people API search skipped",
            "queries": exa_queries,
        }]
    (run_dir / "exa_people_deep.json").write_text(json.dumps(exa_deep_people_results, indent=2))

    # 7) synthesize (after all raw persisted)
    synthesize_onepager(run_dir, topic, date)

    manifest = {
        "date": date,
        "topic": topic,
        "folders": {"run_dir": str(run_dir.relative_to(repo)), "raw": str(raw.relative_to(repo))},
        "counts": {
            "papers_selected": len(papers),
            "paper_people_queries": len(paper_people),
            "signals_accounts": len(accounts),
            "history_dates_checked": len(wanted),
        },
    }
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))

    # publish raw files for site visibility
    publish_run_to_public(repo, date)

    return run_dir


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", default="What is the latest in code RL environments and human data?")
    ap.add_argument("--date", default=dt.date.today().isoformat())
    ap.add_argument("--repo", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--exa-api-key", default=None)
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    if not (repo / "public" / "index.html").exists():
        print(f"Not a valid code-rl-briefing repo: {repo}", file=sys.stderr)
        return 2

    exa_key = args.exa_api_key or __import__('os').environ.get('EXA_API_KEY')
    run_dir = run(args.topic, args.date, repo, exa_api_key=exa_key)
    print(json.dumps({"ok": True, "run_dir": str(run_dir), "one_pager": str(run_dir / 'one-pager.md')}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
