#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, urllib.parse, urllib.request
from pathlib import Path


def yt_get(url: str):
    return json.loads(urllib.request.urlopen(url, timeout=60).read().decode("utf-8"))


def search_channels(api_key: str, query: str, max_results: int = 50):
    url = (
        "https://www.googleapis.com/youtube/v3/search?" +
        urllib.parse.urlencode({
            "part": "snippet",
            "q": query,
            "type": "channel",
            "maxResults": min(max_results, 50),
            "key": api_key,
        })
    )
    raw = yt_get(url)
    channels = []
    for it in raw.get("items", []):
        cid = ((it.get("id") or {}).get("channelId"))
        sn = it.get("snippet") or {}
        if not cid:
            continue
        channels.append({
            "channelId": cid,
            "title": sn.get("channelTitle") or sn.get("title") or "",
            "description": sn.get("description", ""),
            "customUrl": sn.get("customUrl"),
            "publishedAt": sn.get("publishedAt"),
            "url": f"https://www.youtube.com/channel/{cid}",
        })
    return {"requestUrl": url, "raw": raw, "channels": channels}


def enrich_stats(api_key: str, channels: list[dict]):
    ids = [c["channelId"] for c in channels if c.get("channelId")]
    enriched = {c["channelId"]: dict(c) for c in channels}
    for i in range(0, len(ids), 50):
        chunk = ids[i:i+50]
        if not chunk:
            continue
        url = (
            "https://www.googleapis.com/youtube/v3/channels?" +
            urllib.parse.urlencode({
                "part": "snippet,statistics,brandingSettings",
                "id": ",".join(chunk),
                "maxResults": 50,
                "key": api_key,
            })
        )
        raw = yt_get(url)
        for it in raw.get("items", []):
            cid = it.get("id")
            stats = it.get("statistics") or {}
            sn = it.get("snippet") or {}
            b = it.get("brandingSettings") or {}
            if cid in enriched:
                enriched[cid].update({
                    "title": sn.get("title", enriched[cid].get("title", "")),
                    "description": sn.get("description", enriched[cid].get("description", ""))[:500],
                    "subscriberCount": int(stats.get("subscriberCount", 0)) if str(stats.get("subscriberCount", "")).isdigit() else 0,
                    "videoCount": int(stats.get("videoCount", 0)) if str(stats.get("videoCount", "")).isdigit() else 0,
                    "viewCount": int(stats.get("viewCount", 0)) if str(stats.get("viewCount", "")).isdigit() else 0,
                    "country": sn.get("country"),
                    "keywords": ((b.get("channel") or {}).get("keywords") or "")[:300],
                })
    return list(enriched.values())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=True)
    ap.add_argument("--api-key", default=None)
    ap.add_argument("--min-subs", type=int, default=0)
    ap.add_argument("--max-results", type=int, default=50)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    import os
    key = args.api_key or os.environ.get("YOUTUBE_DATA_API_KEY")
    if not key:
        raise SystemExit("Missing YOUTUBE_DATA_API_KEY")

    s = search_channels(key, args.query, args.max_results)
    enriched = enrich_stats(key, s["channels"])
    filtered = [c for c in enriched if c.get("subscriberCount", 0) >= args.min_subs]
    filtered.sort(key=lambda c: c.get("subscriberCount", 0), reverse=True)

    out = {
        "query": args.query,
        "minSubscribers": args.min_subs,
        "totalFound": len(enriched),
        "totalAfterFilter": len(filtered),
        "channels": filtered,
        "searchRequestUrl": s["requestUrl"],
    }

    out_path = Path(args.out) if args.out else Path("data") / "youtube-channel-search.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(out, indent=2))
    print(json.dumps({"ok": True, "out": str(out_path), "count": len(filtered)}, indent=2))


if __name__ == "__main__":
    main()
