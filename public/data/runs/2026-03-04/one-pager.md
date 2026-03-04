# One-Pager — Code RL Environments + Human Data (2026-03-04)

Code-RL discourse in the last 24 hours is concentrating on verifier-backed training loops and harness-level gains, while human data is shifting toward narrower, high-value supervision and privacy-preserving alignment rather than blanket preference labeling.

## Top Tweets (highest-signal)
- $LOD Agent Update 🤖 After some deep dives + dev calls… we found a gem. There’s already an open-source RL environment (PyLoL) that enabled AI to play League via a modified GameServer. It exposes a Python ML API → agents g → [league0fdegens update](https://x.com/league0fdegens/status/2028985356570304601)
- 𝗪𝗵𝘆 𝗔𝗜 𝗶𝘀 𝗮 𝗖𝗼𝗱𝗶𝗻𝗴 𝗚𝗲𝗻𝗶𝘂𝘀 𝗯𝘂𝘁 𝗮 𝗠𝗲𝗱𝗶𝗼𝗰𝗿𝗲 𝗪𝗿𝗶𝘁𝗲𝗿 Ask an LLM to build a complex web scraper, and it gives you flawless Python. Ask it to write a heartfelt email, and it sounds like a corporate HR manual. Why is AI accelera → [Arjunjain update](https://x.com/Arjunjain/status/2028649120593055890)
- @anecdotal @DAcemogluMIT Technically: you're proposing a Grandmother Agent (so not RLHF, but RLAI?) "whose action space is the knowledge base itself." I think I don't really understand what this looks like. Specialized m → [joaneleanor_ update](https://x.com/joaneleanor_/status/2028996681874747490)
- midnight coding sessions with only my cat as a critic Who needs human feedback when you have a 3am meow? https://t.co/xScz8YxuOO → [ChristyPug64727 update](https://x.com/ChristyPug64727/status/2028840618689224727)

## Top Papers (papers-first pass)
- Modern machine learning (ML) workloads increasingly rely on GPUs, yet achieving high end-to-end performance remains challenging due to dependencies on both GPU kernel efficiency and host-side settings. Although LLM-based. → [StitchCUDA: An Automated Multi-Agents End-to-End GPU Programing Framework with Rubric-based Agentic Reinforcement Learning](https://arxiv.org/abs/2603.02637v1)
- Leveraging the priors of 2D diffusion models for 3D editing has emerged as a promising paradigm. However, maintaining multi-view consistency in edited results remains challenging, and the extreme scarcity of 3D-consisten. → [Geometry-Guided Reinforcement Learning for Multi-view Consistent 3D Scene Editing](https://arxiv.org/abs/2603.03143v1)
- Agentic language models operate in a fundamentally different safety regime than chat models: they must plan, call tools, and execute long-horizon actions where a single misstep, such as accessing files or entering creden. → [Learning When to Act or Refuse: Guarding Agentic Reasoning Models for Safe Multi-Step Tool Use](https://arxiv.org/abs/2603.03205v1)
- Classifying fine-grained visual concepts under open-world settings, i.e., without a predefined label set, demands models to be both accurate and specific. Recent reasoning Large Multimodal Models (LMMs) exhibit strong vi. → [Specificity-aware reinforcement learning for fine-grained open-world classification](https://arxiv.org/abs/2603.03197v1)
- Agentic Reinforcement Learning (Agentic RL) has shown remarkable potential in large language model-based (LLM) agents. These works can empower LLM agents to tackle complex tasks via multi-step, tool-integrated reasoning. → [RAPO: Expanding Exploration for LLM Agents via Retrieval-Augmented Policy Optimization](https://arxiv.org/abs/2603.03078v1)

## Signal Movement (tracked accounts)
- @HamelHusain: Evals Skills for Coding Agents → https://x.com/HamelHusain/status/2028894099483578872
- @LangChain: What? LangChain is evolving!  Meet our final form ➡️ https://t.co/f6eGVFchtB https://t.co/MWLFt7Awpd → https://x.com/LangChain/status/2028522092774199731
- @_reachsumit: Super Research: Answering Highly Complex Questions with Large Language Models through Super Deep and Super Wide Research → https://x.com/_reachsumit/status/2028734391569260873

## Notable Changes vs Prior Runs
- Historical update pass covered available dates: 2026-02-25.
- Missing run files for requested dates: 2026-03-03, 2026-03-01, 2026-02-18 (no local briefing artifact found).
- More references are now persisted as raw files first, then synthesized (prevents signal loss from short summaries).

## What to Watch (next 24h)
- Whether tool-verification style methods (T³RL-like) start appearing in code-agent eval threads, not just math benchmarks.
- Whether RAPO-style retrieval-augmented exploration is replicated on SWE/terminal benchmarks by independent teams.
- Whether rubric+execution reward designs (StitchCUDA pattern) spread into general software-engineering agent pipelines.