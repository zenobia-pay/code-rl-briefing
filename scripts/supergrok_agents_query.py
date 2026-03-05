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
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode("utf-8"))


def run_task(api_key: str, prompt: str, profile_id: str, timeout_s: int):
    session = browseruse_req(api_key, "POST", "/sessions", {
        "profileId": profile_id,
        "persistMemory": True,
        "keepAlive": False,
    })
    task = browseruse_req(api_key, "POST", "/tasks", {
        "task": prompt,
        "sessionId": session["id"],
    })

    task_id = task["id"]
    start = time.time()
    status = None
    while time.time() - start < timeout_s:
        status = browseruse_req(api_key, "GET", f"/tasks/{task_id}/status")
        if status.get("status") in ("finished", "failed", "stopped"):
            break
        time.sleep(8)

    return {"session": session, "task": task, "status": status}


def main():
    parser = argparse.ArgumentParser(description="Run a SuperGrok query through Browser Use")
    parser.add_argument("--query", default=DEFAULT_QUERY, help="Prompt/query to run")
    parser.add_argument("--profile-id", default=DEFAULT_PROFILE_ID)
    parser.add_argument("--timeout", type=int, default=1200)
    parser.add_argument("--out", default="data/supergrok-autonomous-agents-latest.json")
    args = parser.parse_args()

    api_key = os.environ.get("BROWSER_USE_API_KEY")
    if not api_key:
        raise SystemExit("Missing BROWSER_USE_API_KEY")

    payload = run_task(api_key, args.query, args.profile_id, args.timeout)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps({
        "query": args.query,
        "ranAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        **payload,
    }, indent=2))

    print(f"Wrote {out_path}")
    print(f"Task status: {(payload.get('status') or {}).get('status')}")


if __name__ == "__main__":
    main()
