# code-rl-briefing

Briefing site + cleaned dataset for:

**“What is the latest in code RL environments and human data?”**

## What’s included

- `public/index.html` — briefing page with headline trend summary and papers table
- `public/data/papers.json` — normalized paper list (Feb 19–25, 2026)
- `public/data/signals.json` — trend-level synthesis
- `public/data/posts.json` — curated social posts and summaries
- `public/data/people-seeds.json` — priority accounts to monitor first
- `src/index.ts` — Cloudflare Worker entry

## Run locally

```bash
pnpm install
pnpm dev
```

## Deploy

```bash
pnpm deploy
```
