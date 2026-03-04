# Specificity-aware reinforcement learning for fine-grained open-world classification

Published: 2026-03-03T17:52:39Z

ArXiv: https://arxiv.org/abs/2603.03197v1

alphaXiv: https://www.alphaxiv.org/abs/2603.03197

Authors: Samuele Angheben, Davide Berasi, Alessandro Conti, Elisa Ricci, Yiming Wang

Abstract:
Classifying fine-grained visual concepts under open-world settings, i.e., without a predefined label set, demands models to be both accurate and specific. Recent reasoning Large Multimodal Models (LMMs) exhibit strong visual understanding capability but tend to produce overly generic predictions when performing fine-grained image classification. Our preliminary analysis reveals that models do possess the intrinsic fine-grained domain knowledge. However, promoting more specific predictions (specificity) without compromising correct ones (correctness) remains a non-trivial and understudied challenge. In this work, we investigate how to steer reasoning LMMs toward predictions that are both correct and specific. We propose a novel specificity-aware reinforcement learning framework, SpeciaRL, to fine-tune reasoning LMMs on fine-grained image classification under the open-world setting. SpeciaRL introduces a dynamic, verifier-based reward signal anchored to the best predictions within online rollouts, promoting specificity while respecting the model's capabilities to prevent incorrect predictions. Our out-of-domain experiments show that SpeciaRL delivers the best trade-off between correctness and specificity across extensive fine-grained benchmarks, surpassing existing methods and advancing open-world fine-grained image classification. Code and model are publicly available at https://github.com/s-angheben/SpeciaRL.
