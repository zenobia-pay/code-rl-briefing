Code RL is decisively shifting from “predict code” to “operate systems”: the winners are models trained in executable environments with verifiable feedback, not chat-only reward loops. My take: the next moat is not model size but the quality of environment design (terminal depth, verifier quality, long-horizon curriculum) plus operational data flywheels from persistent agents.

The most important signal this week is convergence: terminal-capability training (Nemotron-Terminal), long-horizon curriculum design (KLong), hardware-level search (K-Search), formal-verification research agents (Aletheia), and live red-team evidence (Agents of Chaos) all point to the same bottleneck—good outcomes require structured environments and better reward instrumentation, not just more preference labels. Hermes Agent matters because it operationalizes that loop in production-style settings, while RLVR debates show the field still lacks robust verification for open-ended reasoning.

Links:
- On Data Engineering for Scaling LLM Terminal Capabilities — https://arxiv.org/abs/2602.21193
- KLong: Training LLM Agent for Extremely Long-horizon Tasks — https://arxiv.org/abs/2602.17547
- K-Search: LLM Kernel Generation via Co-Evolving Intrinsic World Model — https://arxiv.org/abs/2602.19128
- Agents of Chaos — https://arxiv.org/abs/2602.20021
- Aletheia tackles FirstProof autonomously — https://arxiv.org/abs/2602.21201
- Aletheia project repo — https://github.com/google-deepmind/superhuman/tree/main/aletheia
- Hermes Agent launch page — https://nousresearch.com/hermes-agent/
- @NousResearch thread — https://x.com/NousResearch/status/2026758996107898954
- @willccbb thread — https://x.com/willccbb/status/2026743565699936376
- @cwolferesearch thread — https://x.com/cwolferesearch/status/2026151598523625626
- @sachpatro97 thread — https://x.com/sachpatro97/status/2026773868233343072
