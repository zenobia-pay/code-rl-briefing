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

## Deploy

```bash
pnpm run deploy
```
