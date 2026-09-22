# RecPO: 什么使 LLM 成为有效的序列推荐器？关于偏好强度与时间上下文的研究

**原标题**: What Makes LLMs Effective Sequential Recommenders? A Study on Preference Intensity and Temporal Context

**作者**: Zhongyu Ouyang, Qianlong Wen, Chunhui Zhang 等

**单位**: Dartmouth College; ByteDance; University of Notre Dame

## 摘要

什么使大语言模型（LLMs）能够有效地建模序列推荐中的用户偏好？我们的研究揭示，现有的偏好对齐方法主要依赖二元成对比较，忽略了两个关键因素：**偏好强度**——亲和或厌恶的结构化强度——以及**时间上下文**——近期交互在多大程度上更好地反映用户当前意图。通过对照实验，我们表明利用包含结构化偏好信号的全面反馈能显著提升推荐性能，说明二元建模丢弃了关键信息。受这些发现启发，我们提出 RecPO，一个统一的偏好优化框架，将显式和隐式反馈映射到共同的偏好信号空间，并构建自适应的奖励边际（reward margin），同时考虑偏好强度和交互时效性。在五个数据集上的实验表明，RecPO 持续优于最先进的基线方法，同时展现出与人类决策一致的行为模式，包括偏好即时满足、维持偏好一致性和规避不喜欢的物品。我们的结果表明，偏好强度和时间上下文是有效的基于 LLM 推荐的基本要素。
