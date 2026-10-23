# What Makes LLMs Effective Sequential Recommenders?

> 来源文件：08_RecPO.pdf
> 发表年份：2026
> 单位：ByteDance Inc.；Dartmouth College；University of Notre Dame

## 英文原文摘要（Original Abstract）

What enables large language models (LLMs) to effectively model user preferences in sequential recommendation? Our investigation reveals that existing preference-alignment approaches largely rely on binary pairwise comparisons, overlooking two critical factors: preference intensity—the structured strength of affinity or aversion —and temporal context—the extent to which recent interactions better reflect a user's current intent. Through controlled experiments, we show that leveraging comprehensive feedback with structured preference signals substantially improves recommendation performance, indicating that binary modeling discards essential information. Motivated by these findings, we propose RecPO, a unified preference optimization framework that maps both explicit and implicit feedback into a common preference signal and constructs adaptive reward margins that jointly account for preference intensity and interaction recency. Experiments across five datasets show that RecPO consistently outperforms state-of-the-art baselines while exhibiting behavioral patterns aligned with human decision-making, including favoring immediate satisfaction, maintaining preference coherence, and avoiding dispreferred items. Our results highlight that preference intensity and temporal context are fundamental ingredients for effective LLM-based recommendation. Code: https://github.com/zyouyang/RecPO.

## 中文翻译（Chinese Translation）

是什么让大语言模型（LLM）在序列推荐中有效建模用户偏好？我们的研究揭示，现有的偏好对齐方法大多依赖二值成对比较，忽略了两个关键因素：偏好强度（preference intensity）——即亲和或厌恶的结构化强弱——以及时间上下文（temporal context）——即近期交互在多大程度上更能反映用户当前意图。通过受控实验，我们表明，利用包含结构化偏好信号的综合反馈能显著提升推荐性能，这说明二值建模丢弃了关键信息。基于这些发现，我们提出 RecPO，一个统一的偏好优化框架，将显式与隐式反馈映射到同一偏好信号，并构建自适应奖励边界（adaptive reward margins），联合考虑偏好强度与交互近因（interaction recency）。在五个数据集上的实验表明，RecPO 一致优于 SOTA 基线，同时表现出与人类决策一致的行为模式——偏好即时满足、保持偏好连贯性、回避不喜欢的物品。我们的结果凸显：偏好强度与时间上下文是基于 LLM 的推荐的基本要素。代码：https://github.com/zyouyang/RecPO。
