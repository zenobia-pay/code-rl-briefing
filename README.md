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

This pipeline now does, in order:
1. papers-first (arXiv + alphaXiv links)
2. initial X research pass
3. per-paper "people talking about <title>" pass
4. signals-account daily pass
5. historical bullet updates (1/3/7/14 days, when present)
6. exa.ai blog query pass
7. persist all raw files, then synthesize one-pager
8. publish raw files for site browsing under `public/data/runs/YYYY-MM-DD/`

## Deploy

```bash
pnpm run deploy
```
