# Reasoning Over Space: Enabling Geographic Reasoning for LLM-Based

> 来源文件：06_ROS.pdf

## 英文原文摘要（Original Abstract）

Generative recommendation with large language models (LLMs) reframes prediction as sequence generation, yet existing LLM-based recommenders remain limited in leveraging geographic signals that are crucial in mobility and local-services scenarios. Here, we present REASONING OVER SPACE (ROS), a framework that utilizes geography as a vital decision variable within the reasoning process. ROS introduces a Hierarchical Spatial Semantic ID (SID) that discretizes coarse-to-fine locality and POI semantics into compositional tokens, and endows LLM with a three-stage Mobility Chain-of-Thought (CoT) paradigm that models user personality, constructs an intent-aligned candidate space, and performs locality informed pruning. We further align the model with real world geography via spatial-guided Reinforcement Learning (RL). Experiments on three widely used location-based social network (LBSN) datasets show that ROS achieves over 10% relative gains in hit rate over strongest LLM-based baselines and improves cross-city transfer, despite using a smaller backbone model.

## 中文翻译（Chinese Translation）

基于大语言模型（LLM）的生成式推荐将预测重新建模为序列生成任务，但现有基于 LLM 的推荐器在利用地理信号方面仍然受限，而这些信号在移动（mobility）与本地服务场景中至关重要。为此，我们提出 REASONING OVER SPACE（ROS）框架，将地理信息作为推理过程中的关键决策变量。ROS 引入了层次化空间语义 ID（Hierarchical Spatial Semantic ID, SID），将由粗到细的位置（locality）与 POI 语义离散化为可组合的 token，并赋予 LLM 一种三阶段的"移动思维链"（Mobility Chain-of-Thought, CoT）范式：建模用户个性、构建与意图对齐的候选空间、并执行基于位置的剪枝。我们进一步通过空间引导的强化学习（RL）将模型与真实地理对齐。在三个广泛使用的位置社交网络（LBSN）数据集上的实验表明，ROS 即使在使用更小骨干模型的情况下，命中率也比最强的 LLM 基线提升超过 10%，并改善了跨城市迁移能力。
