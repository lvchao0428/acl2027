# ReRec: 通过强化微调实现推理增强的 LLM 推荐助手

**原标题**: ReRec: Reasoning-Augmented LLM-based Recommendation Assistant via Reinforcement Fine-tuning

**作者**: Jiani Huang, Shijie Wang, Liangbo Ning 等

**单位**: The Hong Kong Polytechnic University (PolyU)

## 摘要

随着 LLM 的兴起，人们越来越需要能够处理复杂查询并提供个性化、推理驱动推荐的智能推荐助手。基于 LLM 的推荐器展现出潜力，但在多步推理方面面临挑战，凸显了推理增强系统的必要性。为解决这一差距，我们提出 ReRec，一个旨在提升 LLM 在复杂推荐任务中推理能力的新型强化微调（RFT）框架。该框架引入三个关键组件：(1) **双图增强奖励塑造（Dual-Graph Enhanced Reward Shaping）**：将推荐指标（如 NDCG@K）与查询对齐分数和偏好对齐分数相结合，为 LLM 优化提供细粒度奖励信号；(2) **推理感知优势估计（Reasoning-aware Advantage Estimation）**：将 LLM 输出分解为推理片段，对错误步骤进行惩罚，以增强推荐推理能力；(3) **在线课程调度器（Online Curriculum Scheduler）**：动态评估查询难度并组织训练课程，确保 RFT 训练过程中的稳定学习。实验表明 ReRec 超越了最先进的基线方法，同时保持了指令遵循和通用知识等核心能力。
