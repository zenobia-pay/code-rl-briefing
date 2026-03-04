# One-Pager — What is the latest in code RL environments and human data? (2026-03-04)

Code-RL discussion is concentrating around verifier-backed training loops and harness-level gains, while human data is becoming narrower and higher-value (targeted supervision, safety checks, privacy-preserving alignment).

## Tweets
- $LOD Agent Update 🤖 After some deep dives + dev calls… we found a gem. There’s already an open-source RL environment (PyLoL) that enabled AI to play League via a modified GameServer. It exposes a Python ML API → agents g → [league0fdegens](https://x.com/league0fdegens/status/2028985356570304601)
- @anecdotal @DAcemogluMIT Technically: you're proposing a Grandmother Agent (so not RLHF, but RLAI?) "whose action space is the knowledge base itself." I think I don't really understand what this looks like. Specialized m → [joaneleanor_](https://x.com/joaneleanor_/status/2028996681874747490)

## Papers
- Modern machine learning (ML) workloads increasingly rely on GPUs, yet achieving high end-to-end performance remains challenging due to dependencies on both GPU kernel efficiency and host-side settings. Although LLM-based. → [StitchCUDA: An Automated Multi-Agents End-to-End GPU Programing Framework with Rubric-based Agentic Reinforcement Learning](https://arxiv.org/abs/2603.02637v1)
- Leveraging the priors of 2D diffusion models for 3D editing has emerged as a promising paradigm. However, maintaining multi-view consistency in edited results remains challenging, and the extreme scarcity of 3D-consisten. → [Geometry-Guided Reinforcement Learning for Multi-view Consistent 3D Scene Editing](https://arxiv.org/abs/2603.03143v1)
- Large language models are increasingly used for patient-facing medical assistance and clinical decision support, but adapting them to clinical dialogue often requires supervision derived from doctor-patient conversations. → [PrivMedChat: End-to-End Differentially Private RLHF for Medical Dialogue Systems](https://arxiv.org/abs/2603.03054v1)
- Agentic language models operate in a fundamentally different safety regime than chat models: they must plan, call tools, and execute long-horizon actions where a single misstep, such as accessing files or entering creden. → [Learning When to Act or Refuse: Guarding Agentic Reasoning Models for Safe Multi-Step Tool Use](https://arxiv.org/abs/2603.03205v1)
- Classifying fine-grained visual concepts under open-world settings, i.e., without a predefined label set, demands models to be both accurate and specific. Recent reasoning Large Multimodal Models (LMMs) exhibit strong vi. → [Specificity-aware reinforcement learning for fine-grained open-world classification](https://arxiv.org/abs/2603.03197v1)

## Signal Movement
- @HamelHusain: Evals Skills for Coding Agents → https://x.com/HamelHusain/status/2028894099483578872
- @LangChain: What? LangChain is evolving! Meet our final form ➡️ https://t.co/f6eGVFchtB https://t.co/MWLFt7Awpd → https://x.com/LangChain/status/2028522092774199731
- @_reachsumit: Super Research: Answering Highly Complex Questions with Large Language Models through Super Deep and Super Wide Research → https://x.com/_reachsumit/status/2028734391569260873

## Changes vs prior
- Historical update pass found local briefing artifacts for: 2026-02-25.
- Missing local artifacts for requested offsets: 2026-03-03, 2026-03-01, 2026-02-18.

## Watch next 24h
- Replications of tool-verification and retrieval-augmented exploration on SWE/terminal benchmarks.
- More concrete evidence that rubric+execution rewards transfer from narrow domains to broad code-agent tasks.