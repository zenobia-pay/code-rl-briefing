# Raw briefing input (verbatim-style ingest)

## Prompt header
What is the latest in code RL environments and human data?

## Key Trends in Code RL Environments
Recent research emphasizes moving beyond simple code generation to terminal interaction and hardware-aware optimization. Instead of just predicting a code snippet, models are being trained as agents that can execute commands, observe errors, and iterate in a loop.

### Terminal Capability Scaling
New work explores data engineering specifically for “terminal capabilities,” treating the command-line interface as a structured RL environment. This allows agents to handle complex file systems and system-level tasks.

### GPU Kernel Optimization
K-Search: LLM Kernel Generation via Co-Evolving Intrinsic World Model treats CUDA kernel generation as a search problem. It uses an internal “world model” to predict performance, allowing the agent to optimize hardware-level code without requiring constant, expensive physical hardware execution.

### Mathematical Research Agents
Aletheia tackles FirstProof autonomously demonstrates agents powered by Deep Think models (like Gemini 3) solving autonomous math challenges, where the “environment” is a rigorous formal proof system that provides verifiable rewards.

## Advancements in Human Data & Feedback
Human data strategies are shifting from simple preference labeling (RLHF) to Human-in-the-loop (HITL) orchestration and Long-horizon trajectory collection.

### Extremely Long-horizon Tasks
KLong: Training LLM Agent for Extremely Long-horizon Tasks introduces a method to cold-start agents using “trajectory-splitting” SFT before scaling via progressive RL. This addresses the scarcity of human data for tasks that span thousands of steps.

### Agents of Chaos
Agents of Chaos reports on a massive “red-teaming” study where agents were deployed in live laboratory environments (with email, Discord, and file access). This generates a new kind of human-interaction data centered on “chaos” and edge-case behavior in persistent environments.

### Verifiable Reward Foundries
There is a growing trend of building “foundries”—environments where rewards are automatically verified by code tests or physical simulators—to reduce the reliance on expensive human feedback for every step of training.

## Recent Papers (Feb 19 - Feb 25, 2026)
- On Data Engineering for Scaling LLM Terminal Capabilities — Focuses on training strategies for agents to master terminal/shell environments. — Feb 24, 2026
- KLong: Training LLM Agent for Extremely Long-horizon Tasks — Solves the data bottleneck for long-horizon tasks using trajectory splitting. — Feb 19, 2026
- K-Search: LLM Kernel Generation via Co-Evolving Intrinsic World Model — RL-based GPU kernel optimization using a learned world model. — Feb 22, 2026
- Agents of Chaos — Explores agent behavior in live human environments with persistent tools. — Feb 23, 2026
- Aletheia tackles FirstProof autonomously — Autonomous agents solving math research problems in verifiable environments. — Feb 24, 2026

## Priority accounts
@karpathy, @natolambert, @willccbb

## 1) Hermes Agent launch by Nous Research (Feb 25)
Main announcement thread by @NousResearch (ID: 2026758996107898954, 579 likes, 224k+ views):
- “Meet Hermes Agent, the open source agent that grows with you.
Hermes Agent remembers what it learns and gets more capable over time, with a multi-level memory system and persistent dedicated machine access.”
- “Hermes Agent runs in your CLI and through messaging platforms like Telegram, WhatsApp, Slack, and Discord - picking up and transferring sessions wherever you go.
https://nousresearch.com/hermes-agent/
It has advanced agentic capabilities: command over subagents, programmatic tool calling, advanced filesystem/terminal control, agent-managed skills, browser use, scheduled tasks, and more.”
- “Hermes Agent is open source and built in Python, so it’s easy for developers to extend. It sits between a Claude Code style CLI and an OpenClaw style messaging platform agent...
It also powers our agentic RL pipeline, expanding Atropos so you can run RL with Hermes Agent primitives, and it supports mass-scale data generation out of the box.”
@Teknium (same day): “Hope everyone enjoys! Join our discord to discuss...”

## 2) Prime Intellect RL residents breakthrough (@willccbb, Feb 25)
Main post by @willccbb (ID: 2026743565699936376, 160 likes, 6k views):
- “god the prime intellect RL residents have been cooking so hard  a major bottleneck in continual learning is that we don’t have a general way to compare and evaluate methods across task domains  i think @carnot_cyclist may have solved this”
Follow-up:
- “i won’t spoil it because i want him to write a banger blog post about it. but wow it’s just a really really clean formalism that can be used for so many different things, and he’s got some nice early experimental results to show it off”

## 3) Rubric-based RL thread (@cwolferesearch, Feb 24)
Full key post (ID: 2026151598523625626, 76 likes, 3.6k views + 4 images/screenshots):
- “Rubric-based RL is a really popular topic right now, but it’s not new. Rubrics have a relatively long (and successful) history of use in safety / alignment research…
... Today, rubric-based RL looks pretty similar to these systems. The main differences are:
• We go beyond preference data and usually generate a direct assessment reward.
• Rubrics are oftentimes prompt-specific…
• The output of the reasoning model / LLM judge is directly used as the reward signal.
• However, fundamental concepts remain the same: detailed rubrics provide a reliable reward signal for RL… and provide granular control over the training process, even on very open-ended tasks.”

## 4) RLVR vs RLHF debate (Feb 24–25)
Representative post by @saen_dev (Feb 25):
- “RLVR over RLHF is a genuine paradigm shift — training on verifiable outcomes rather than human preference labels removes a whole class of reward hacking problems. The challenge is defining what ‘verifiable’ means for open-ended tasks. Code and math are easy; reasoning is harder.”
Other noted:
- @Shekswess (Feb 23): alpha and rollout diversity findings.
- @fourierproject (Feb 25): caution on short time scales and RL diversity.
- @agitbackprop (Feb 24): RLVR can bypass HHH circuits (coding-agent sabotage examples).

## 5) RL env infrastructure & moats (@sachpatro97, Feb 25)
Post ID: 2026773868233343072
- “... Everybody wants high quality tasks, rubrics and verifiers  but some want just that, others want the full harness and TVRs ... from a product standpoint, it feels like you are skating to where the puck is, vs where it’s going ...”

## Additional KLong data dump (raw)
Yes, people are talking about the KLong paper (arXiv 2602.17547, dropped Feb 19, 2026). It’s getting targeted discussion in long-horizon/agentic RL circles.

Paper mechanism details called out:
- trajectory-splitting SFT (cold-start: preserves early context; progressively truncates later parts with overlap)
- progressive RL (multi-stage training with gradually longer timeouts)
- Research-Factory distillation pipeline from Claude 4.5 Sonnet trajectories
- Result claim: 106B KLong beats Kimi K2 Thinking (1T) by 11.28% on PaperBench, with generalization to SWE-bench Verified and MLE-bench.

Recent mentions:
- @dair_ai (Feb 20, 158 likes, 8.6k+ views) detailed summary post
- @guifav (Feb 20) parameter efficiency framing
- @SciFi (Feb 21) arXiv bot mention
- Replies in @dair_ai thread emphasize human-data scarcity and synthetic distillation

Canonical paper link: https://arxiv.org/abs/2602.17547
