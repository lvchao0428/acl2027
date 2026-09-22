# ReRec: Reasoning-Augmented LLM-based Recommendation Assistant via Reinforcement Fine-tuning

| 项目 | 内容 |
|------|------|
| **Paper** | ReRec: Reasoning-Augmented LLM-based Recommendation Assistant via Reinforcement Fine-tuning |
| **Authors** | Jiani Huang, Shijie Wang, Liangbo Ning, Wenqi Fan, Qing Li |
| **Affiliation** | The Hong Kong Polytechnic University (PolyU) |
| **Theme** | LLM 推荐助手 / 强化微调 / 推理增强推荐 |
| **Problem** | LLM 推荐助手在处理复杂查询时面临多步推理挑战，现有方法难以进行深度推理以给出个性化、reason-driven 的推荐 |
| **Method** | RFT 框架包含三个组件：(1) Dual-Graph Enhanced Reward Shaping（NDCG@K + Query Alignment + Preference Alignment 得分）；(2) Reasoning-aware Advantage Estimation（分解推理段、惩罚错误步骤）；(3) Online Curriculum Scheduler（动态评估查询难度） |
| **Benchmark** | 多个推荐数据集 |
| **Result** | 超越 SOTA 基线方法，同时保持指令遵循和通用知识能力 |
| **Question** | Dual-Graph 中的 Query Alignment 和 Preference Alignment 权重如何确定？Reasoning segment 的划分粒度对效果的影响如何？ |

## 详细笔记

### 研究背景与动机

随着 LLM 的崛起，智能推荐助手需要处理越来越复杂的用户查询，并提供个性化、基于推理的推荐。然而现有 LLM 推荐器在多步推理方面能力有限——面对需要综合多个约束条件的查询时，模型往往难以进行深度推理。

来自香港理工大学的 Huang 等人提出 ReRec，通过强化微调（Reinforcement Fine-Tuning, RFT）增强 LLM 推荐助手的推理能力。

### 核心方法详解

**Dual-Graph Enhanced Reward Shaping**：设计了融合推荐指标的多维度奖励信号：NDCG@K 衡量排序质量、Query Alignment Score 衡量语义一致性、Preference Alignment Score 衡量偏好匹配度。通过构建 query-item 和 preference-item 双图来计算细粒度奖励。

**Reasoning-aware Advantage Estimation**：将 LLM 输出分解为多个推理段（reasoning segments），对正确推理段给正向 advantage，对错误推理段施加 token 级别惩罚，使模型不仅学会"推荐什么"，还学会"如何正确推理"。

**Online Curriculum Scheduler**：动态评估每个训练样本的查询难度，按照从简到难的顺序组织训练课程，确保 RFT 训练过程的稳定性。

### 实验设置与结果

- **数据集**：多个推荐数据集
- **关键结果**：推荐准确性超越 SOTA 基线；保持了模型的指令遵循能力和通用知识

### 个人思考

ReRec 的核心洞察是"推荐推理的每一步都应该被监督"，Reasoning-aware Advantage Estimation 让模型不仅优化最终推荐结果，还优化推理过程本身。这与 OneRec-Think 的思路异曲同工但切入点不同：OneRec-Think 侧重激活推理能力，ReRec 侧重通过 RL 精细化监督推理过程。Online Curriculum Scheduler 的引入也很实用——推荐场景中的查询复杂度差异巨大。
