#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DATE="${1:-$(date +%F)}"
TOPIC="${2:-What is the latest in code RL environments and human data?}"

python3 "$ROOT/scripts/run_briefing.py" --repo "$ROOT" --date "$DATE" --topic "$TOPIC"

echo "\nRun complete for $DATE"
echo "Raw: $ROOT/data/runs/$DATE/raw"
echo "One-pager: $ROOT/data/runs/$DATE/one-pager.md"
