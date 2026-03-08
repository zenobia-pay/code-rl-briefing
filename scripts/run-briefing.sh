#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DATE="${1:-$(date +%F)}"
TOPIC="${2:-What is the latest in code RL environments and human data?}"

# Load env automatically so Browser-Use key is available in cron/manual runs
if [[ -f "$ROOT/.env" ]]; then
  set -a; source "$ROOT/.env"; set +a
elif [[ -f "$HOME/.openclaw/workspace/twitter-briefing/.env" ]]; then
  set -a; source "$HOME/.openclaw/workspace/twitter-briefing/.env"; set +a
fi

python3 "$ROOT/scripts/run_briefing.py" --repo "$ROOT" --date "$DATE" --topic "$TOPIC"

echo "\nRun complete for $DATE"
echo "Raw: $ROOT/data/runs/$DATE/raw"
echo "One-pager: $ROOT/data/runs/$DATE/one-pager.md"
