# code-rl-briefing

Primary-source-driven briefing site for:

**“What is the latest in code RL environments and human data?”**

## Dataset files

- `public/data/accounts.json` — seed + secondary account links
- `public/data/papers.json` — paper list + source links
- `public/data/tweets.json` — thread/post records with post/account links and quoted excerpts
- `public/data/signals.json` — structured trend synthesis from supplied notes

## Site

- `public/index.html` renders all dataset files directly (link-driven view)

## Run

```bash
pnpm install
pnpm dev
```

## Run briefing pipeline (wired process)

```bash
# default: today + default topic
npm run run:briefing

# explicit date/topic
./scripts/run-briefing.sh 2026-03-04 "What is the latest in code RL environments and human data?"
```

This pipeline now does, in order (scripted step prompts):
1. step-01-papers-alphaxiv (AlphaXiv-first paper discovery)
2. step-02-supergrok-topic
3. step-03-supergrok-paper-discussion (exact query: "what are people saying about this exact paper title?")
4. step-04-supergrok-signals
5. step-05-supergrok-history-updates
6. step-06-exa-people (deep, category=people)
7. step-07-youtube-search (YouTube Data API)
8. step-08-synthesis

Step-07 uses `youtube-transcript-api` when available to attach per-video transcripts.

### Separate YouTube channel-search workflow

```bash
python3 scripts/youtube_channel_search.py --query "RL and human data" --min-subs 5000
```

Outputs ranked channels with stats to a JSON file (supports `--out`).

Definition of "run briefing" is stored in `briefing-process.md`.
Per-step prompts are stored in `prompts/`.
Per-run artifacts are stored in `data/runs/YYYY-MM-DD/steps/step-XX-*` with prompt + story + raw + normalized outputs.

## Deploy

```bash
pnpm run deploy
```
