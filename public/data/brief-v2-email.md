Code RL is becoming an environment-design race, not a model-size race. The winning stack is executable settings + hard verifiers + long-horizon training loops.

Tweets

- @JoshPurtell "i have an agentic RL task idea, create a dataset + build the environment for it, run some basic evals + sanity checks, then kick off an RL run and monitor the logs" is now one-shottable by 5.3-codex for me with a short prompt and a couple skill f → [willccbb thread](https://x.com/willccbb/status/2027183031950458961)

- @markatgradient @swyx @harborframework @modal verifiers is focused on being a domain-agnostic layer for converting any eval into a trainable RL environment, including all of the token-level plumbing harbor is the correct way to express tasksets for terminal ag → [willccbb thread](https://x.com/willccbb/status/2027251231878697316)

- If people are working on open research for scaling RL in llms i'd love to talk to you. → [natolambert thread](https://x.com/natolambert/status/2027451823981031550)

- @HeMuyu0327 we also did this (skipping the double ratio) for async RL in intellect-3 :) https://t.co/FExkj2R04a https://t.co/Mb14oZZIU6 → [willccbb thread](https://x.com/willccbb/status/2027912957175468357)

- to get an answer, we have to decide what “optimal” is — minmax expected judge? → [willccbb thread](https://x.com/willccbb/status/2027621849723768933)

- Dario Amodei just revealed that the AI training bottleneck everyone is worried about doesn’t exist anymore. → [r0ck3t23 thread](https://x.com/r0ck3t23/status/2027498827243016298)

- @mermachine rl environments are responsible for this. → [elliotarledge thread](https://x.com/elliotarledge/status/2028260383103008911)

- A Reinforcement Learning Environment for Automatic Code Optimization in MLIR https://t.co/BGHTK7yc4w → [mhatta thread](https://x.com/mhatta/status/2028155809994023289)

- @herbiebradley @SeanZCai when we do RL runs for other people it’s in a collaborative capacity where we’re acting as an extension of their own team, sharing envs/prompts/configs/commands etc, to then allow them to go further themselves → [willccbb thread](https://x.com/willccbb/status/2027627415401599290)

- I had the same thought so I've been playing with it in nanochat. → [karpathy thread](https://x.com/karpathy/status/2027521323275325622)

Papers

- Despite rapid recent progress in the terminal capabilities of large language models, the training data strategies behind state-of-the-art terminal agents remain largely undisclosed. → [On Data Engineering for Scaling LLM Terminal Capabilities](https://www.alphaxiv.org/abs/2602.21193)

- This paper introduces KLong, an open-source LLM agent trained to solve extremely long-horizon tasks. → [KLong](https://www.alphaxiv.org/abs/2602.17547)

- Optimizing GPU kernels is critical for efficient modern machine learning systems yet remains challenging due to the complex interplay of design factors and rapid hardware evolution. → [K-Search](https://www.alphaxiv.org/abs/2602.19128)

- We report an exploratory red-teaming study of autonomous language-model-powered agents deployed in a live laboratory environment with persistent memory, email accounts, Discord access, file systems, and shell execution. → [Agents of Chaos](https://www.alphaxiv.org/abs/2602.20021)

- We report the performance of Aletheia (Feng et al., 2026b), a mathematics research agent powered by Gemini 3 Deep Think, on the inaugural FirstProof challenge. → [Aletheia tackles FirstProof autonomously](https://www.alphaxiv.org/abs/2602.21201)
