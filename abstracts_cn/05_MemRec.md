# MemRec: 协作记忆增强的智能体推荐系统

**原标题**: MemRec: Collaborative Memory-Augmented Agentic Recommender System

**作者**: Weixin Chen, Yuhan Zhao, Jingyuan Huang 等

**单位**: Hong Kong Baptist University (HKBU); Rutgers University; Snap Inc.

## 摘要

推荐系统的演进已从传统协同过滤转向基于 LLM 的智能体系统，后者依赖语义化的用户和物品记忆来做出预测。然而，现有智能体以孤立的方式维护这些记忆。这忽视了关键的协作信号，例如用户-物品共同参与和社区内的同伴关系，显著限制了它们发现隐藏偏好和准确推断用户需求的能力，尤其对数据稀疏用户而言。为弥合这一差距，我们引入**协作记忆**范式，将孤立的语义记忆连接起来以实现关系洞察的共享。然而，朴素地利用协作记忆会导致严重的上下文过载和对下游 LLM 引入噪声，且计算成本过高。为解决这些问题，我们提出 MemRec，一个在架构上将记忆管理与推理解耦的框架。MemRec 引入一个专用的轻量级语言模型（LM_Mem）在后台高效管理和合成动态协作记忆图，仅向下游的重量级大语言模型（LLM_Rec）提供蒸馏后的高信号上下文用于最终推荐。在四个基准上的大量实验表明 MemRec 达到了最先进的性能。
