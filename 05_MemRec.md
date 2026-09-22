# MemRec: Collaborative Memory-Augmented Agentic Recommender System

| 项目 | 内容 |
|------|------|
| **Paper** | MemRec: Collaborative Memory-Augmented Agentic Recommender System |
| **Authors** | Weixin Chen, Yuhan Zhao, Jingyuan Huang, Zihe Ye, Clark Mingxuan Ju, Tong Zhao, Neil Shah, Li Chen, Yongfeng Zhang |
| **Affiliation** | Hong Kong Baptist University (HKBU); Rutgers University; Snap Inc. |
| **Theme** | Agentic 推荐系统 / 协作记忆 / 记忆增强推荐 |
| **Problem** | 现有 agentic 推荐系统的记忆是孤立的（仅维护单个用户/物品的语义记忆），忽略了关键的协作信号，尤其影响数据稀疏用户的推荐效果 |
| **Method** | MemRec 框架：架构性地将记忆管理与推理解耦。引入轻量级 LM_Mem 管理动态协作记忆图，通过 curate-then-synthesize 检索和 O(1) 异步标签传播更新，为重量级 LLM_Rec 提供蒸馏后的高信号上下文 |
| **Benchmark** | Amazon Books, Goodreads, MovieTV, Yelp |
| **Result** | 相比 SOTA 方法 H@1 相对提升 15%-29%；对稀疏用户相比 Vanilla LLM 提升 91.4% |
| **Question** | 协作记忆图的规模增长如何影响 LM_Mem 的效率？隐私敏感场景中跨用户协作信号的共享如何处理？ |

## 详细笔记

### 研究背景与动机

推荐系统从传统协同过滤演进到 LLM 驱动的 agentic 系统，后者依赖语义化的用户和物品记忆进行预测。但现有 agent 的记忆是孤立的——每个用户/物品独立维护记忆，缺乏跨用户的协作信号。这导致数据稀疏用户无法从社区中相似用户的行为中获益。

### 核心方法详解

**架构解耦设计**：LM_Mem（轻量级语言模型）专门负责协作记忆图的管理和上下文合成；LLM_Rec（重量级语言模型）专门负责基于蒸馏上下文的最终推荐推理。

**动态协作记忆图**：将孤立的用户/物品语义记忆通过交互边连接，边代表用户-物品交互、用户-用户相似性等协作信号。

**Curate-then-Synthesize 检索**：LM_Mem 通过 zero-shot 引导筛选高信号记忆，合成为紧凑的"协作 facets"，仅将蒸馏后的高信号上下文提供给 LLM_Rec。

**O(1) 异步标签传播**：借鉴图神经网络标签传播，每次新交互以 O(1) 复杂度异步更新相关记忆，避免对每个邻居反复调用 LLM。

### 实验设置与结果

- **数据集**：Amazon Books、Goodreads、MovieTV、Yelp
- **关键结果**：H@1 相对提升 15%-29%（vs SOTA）；稀疏用户效果尤为显著：相比 Vanilla LLM 提升 91.4%

### 个人思考

MemRec 解决了 agentic 推荐中"agent 的记忆不应是孤岛"的问题。LM_Mem + LLM_Rec 的解耦设计很务实——用小模型做记忆管理、大模型做推理。O(1) 异步传播是工程上的重要贡献。对稀疏用户 91.4% 的提升是最令人印象深刻的结果。
