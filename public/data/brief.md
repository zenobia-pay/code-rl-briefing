Code RL is becoming an environment-design race, not a model-size race. The winning stack is executable settings + hard verifiers + long-horizon training loops, and everyone still doing preference-only polish is going to lose ground.

Tweets
- Hermes Agent remembers what it learns and gets more capable over time, with a multi-level memory system and persistent dedicated machine access. → [Nous thread](https://x.com/NousResearch/status/2026758996107898954)
- A major bottleneck in continual learning is that we don’t have a general way to compare and evaluate methods across task domains. → [willccbb thread](https://x.com/willccbb/status/2026743565699936376)
- Detailed rubrics provide a reliable reward signal for RL and granular control over the training process, even on very open-ended tasks. → [cwolferesearch thread](https://x.com/cwolferesearch/status/2026151598523625626)
- Everybody wants high quality tasks, rubrics and verifiers, but some want just that while others want the full harness and TVRs. → [sachpatro97 thread](https://x.com/sachpatro97/status/2026773868233343072)
- RLVR over RLHF is a genuine paradigm shift, but the challenge is defining what verifiable means for open-ended tasks. → [saen_dev account](https://x.com/saen_dev)

Papers
- Despite rapid recent progress in terminal capabilities, the training data strategies behind state-of-the-art terminal agents remain largely undisclosed. → [On Data Engineering for Scaling LLM Terminal Capabilities](https://arxiv.org/abs/2602.21193)
- KLong uses trajectory-splitting supervised fine-tuning followed by progressive RL stages with extended timeouts. → [KLong](https://arxiv.org/abs/2602.17547)
- K-Search decouples high-level algorithmic planning from low-level program instantiation to navigate non-monotonic optimization paths. → [K-Search](https://arxiv.org/abs/2602.19128)
- We report an exploratory red-teaming study of autonomous language-model-powered agents deployed in a live laboratory environment with persistent memory, email, Discord, file systems, and shell execution. → [Agents of Chaos](https://arxiv.org/abs/2602.20021)
- Within the allowed timeframe of the challenge, Aletheia autonomously solved 6 problems out of 10 according to majority expert assessments. → [Aletheia tackles FirstProof autonomously](https://arxiv.org/abs/2602.21201)
