The center of gravity has moved: code RL is no longer about prettier completions, it’s about agents surviving real environments with verifiable feedback. My take is blunt — teams still obsessing over preference-only tuning are going to get outcompeted by teams building better environments, verifiers, and long-horizon data loops.

Tweets (primary-source first):
- https://x.com/NousResearch/status/2026758996107898954 — “Meet Hermes Agent, the open source agent that grows with you.”
- https://x.com/NousResearch/status/2026758996107898954 — “Hermes Agent remembers what it learns and gets more capable over time, with a multi-level memory system and persistent dedicated machine access.”
- https://x.com/willccbb/status/2026743565699936376 — “a major bottleneck in continual learning is that we don’t have a general way to compare and evaluate methods across task domains.”
- https://x.com/cwolferesearch/status/2026151598523625626 — “Rubric-based RL is a really popular topic right now, but it’s not new.”
- https://x.com/sachpatro97/status/2026773868233343072 — “Everybody wants high quality tasks, rubrics and verifiers but some want just that, others want the full harness and TVRs.”
- https://x.com/saen_dev — “RLVR over RLHF is a genuine paradigm shift — training on verifiable outcomes rather than human preference labels removes a whole class of reward hacking problems.”

Papers (one sentence extracted):
- https://arxiv.org/abs/2602.21193 — “Despite rapid recent progress in the terminal capabilities of large language models, the training data strategies behind state-of-the-art terminal agents remain largely undisclosed.”
- https://arxiv.org/abs/2602.17547 — “KLong tackles this with a two-phase approach: trajectory-splitting supervised fine-tuning that preserves early context while progressively truncating later context, followed by progressive RL that schedules training into stages with extended timeouts.”
- https://arxiv.org/abs/2602.19128 — “Optimizing GPU kernels is critical for efficient modern machine learning systems yet remains challenging due to the complex interplay of design factors and rapid hardware evolution.”
- https://arxiv.org/abs/2602.20021 — “We report an exploratory red-teaming study of autonomous language-model-powered agents deployed in a live laboratory environment with persistent memory, email accounts, Discord access, file systems, and shell execution.”
- https://arxiv.org/abs/2602.21201 — “Within the allowed timeframe of the challenge, Aletheia autonomously solved 6 problems out of 10 according to majority expert assessments.”
- https://github.com/google-deepmind/superhuman/tree/main/aletheia — “Raw prompts and outputs are available at https://github.com/google-deepmind/superhuman/tree/main/aletheia.”
