# ReRec: Reasoning-Augmented LLM-based Recommendation Assistant via

> 来源文件：03_ReRec.pdf

## 英文原文摘要（Original Abstract）

With the rise of LLMs, there is an increasing need for intelligent recommendation assistants that can handle complex queries and provide personalized, reasoning-driven recommendations. LLM-based recommenders show potential but face challenges in multi-step reasoning, underscoring the need for reasoning-augmented systems. To address this gap, we propose ReRec, a novel reinforcement fine-tuning (RFT) framework designed to improve LLM reasoning in complex recommendation tasks. Our framework introduces three key components: (1) Dual-Graph Enhanced Reward Shaping, integrating recommendation metrics like NDCG@K with Query Alignment and Preference Alignment Scores to provide fine-grained reward signals for LLM optimization; (2) Reasoning-aware Advantage Estimation, which decomposes LLM outputs into reasoning segments and penalizes incorrect steps to enhance reasoning of recommendation; and (3) Online Curriculum Scheduler, dynamically assess query difficulty and organize training curriculum to ensure stable learning during RFT. Experiments demonstrate that ReRec outperforms state-of-the-art baselines and preserves core abilities like instruction-following and general knowledge. Our codes are available at https://github.com/jiani-huang/ReRec.

## 中文翻译（Chinese Translation）

随着 LLM 的兴起，人们日益需要能够处理复杂查询、并提供个性化、推理驱动推荐的智能推荐助手。基于 LLM 的推荐器虽展现出潜力，但在多步推理方面仍面临挑战，凸显了构建推理增强系统的必要性。为此，我们提出了 ReRec，一种新颖的强化微调（Reinforcement Fine-Tuning, RFT）框架，旨在提升 LLM 在复杂推荐任务中的推理能力。该框架包含三个关键组件：（1）双图增强奖励塑形（Dual-Graph Enhanced Reward Shaping），将 NDCG@K 等推荐指标与查询对齐（Query Alignment）、偏好对齐（Preference Alignment）分数相结合，为 LLM 优化提供细粒度奖励信号；（2）推理感知的优势估计（Reasoning-aware Advantage Estimation），将 LLM 输出分解为推理片段，并对错误步骤施加惩罚，以增强推荐推理能力；（3）在线课程调度器（Online Curriculum Scheduler），动态评估查询难度并组织训练课程，以保证 RFT 过程中的稳定学习。实验表明，ReRec 优于现有 SOTA 基线，并保留了指令遵循与通用知识等核心能力。代码已开源：https://github.com/jiani-huang/ReRec。
