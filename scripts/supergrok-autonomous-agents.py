#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import time
import urllib.request
from pathlib import Path

BROWSERUSE_BASE = "https://api.browser-use.com/api/v2"
DEFAULT_PROFILE_ID = "9e0f01a3-5227-4424-bc58-b9b226110020"
DEFAULT_QUERY = "how are people actually setting up autonomous agents? find me the tweets of people actually doing this"


def browseruse_req(api_key: str, method: str, path: str, payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        BROWSERUSE_BASE + path,
        data=data,
        method=method,
        headers={"Content-Type": "application/json", "X-Browser-Use-API-Key": api_key},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
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
        time.sleep(10)
    return {"session": session, "task": task, "status": status}


def main():
    parser = argparse.ArgumentParser(description="Run a Browser Use + SuperGrok autonomous-agents query and save output.")
    parser.add_argument("--query", default=DEFAULT_QUERY)
    parser.add_argument("--profile-id", default=DEFAULT_PROFILE_ID)
    parser.add_argument("--out", default="data/supergrok-autonomous-agents-latest.json")
    parser.add_argument("--timeout", type=int, default=1200)
    args = parser.parse_args()

    api_key = os.getenv("BROWSER_USE_API_KEY")
    if not api_key:
        raise SystemExit("Missing BROWSER_USE_API_KEY")

    prompt = (
        "Use X + SuperGrok. Query exactly: \""
        + args.query
        + "\"\n\n"
        "Return strict JSON with this schema:\n"
        "{\n"
        "  \"query\": string,\n"
        "  \"oneSentenceTake\": string,\n"
        "  \"tweets\": [{\"author\": string, \"handle\": string, \"text\": string, \"url\": string, \"whyItMatters\": string}],\n"
        "  \"people\": [{\"name\": string, \"handle\": string, \"url\": string, \"evidence\": string}],\n"
        "  \"setupPatterns\": [string]\n"
        "}\n"
        "Rules: include at least 15 tweets; prioritize people showing real builds, repos, demos, or deployment details."
    )

    run = browseruse_run(api_key, args.profile_id, prompt, timeout_s=args.timeout)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({"prompt": prompt, "run": run}, indent=2))

    print(f"Saved: {out_path}")
    print("Task status:", (run.get("status") or {}).get("status"))
    print("Output preview:")
    print(((run.get("status") or {}).get("output") or "")[:1200])


if __name__ == "__main__":
    main()
