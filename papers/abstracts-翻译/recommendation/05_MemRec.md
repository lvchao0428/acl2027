# MemRec: Collaborative Memory-Augmented

> 来源文件：05_MemRec.pdf

## 英文原文摘要（Original Abstract）

The evolution of recommender systems has shifted from traditional collaborative filtering to LLM-based agentic systems, which rely on semantic user and item memories to make predictions. However, existing agents maintain these memories in isolation. This overlooks crucial collaborative signals, such as user-item co-engagements and peer relationships across the community, which significantly limits their ability to uncover hidden preferences and accurately infer user needs, particularly for data-sparse users. To bridge this gap, we introduce collaborative memory, a paradigm that connects isolated semantics to enable the sharing of relational insights. Yet, naively utilizing collaborative memory causes severe context overload and introduces noise to downstream LLMs, alongside prohibitive computational costs. To resolve this, we propose MemRec, a framework that architecturally decouples memory management from reasoning. MemRec introduces a dedicated, lightweight language model (LMMem) to efficiently manage and synthesize a dynamic collaborative memory graph in the background. It provides only distilled, high-signal contexts to a downstream, heavyweight large language model (LLMRec) for the final recommendation. Extensive experiments on four benchmarks demonstrate that MemRec achieves state-of-the-art performance. Code: https://github.com/rutgerswiselab/memrec Homepage: https://memrec.weixinchen.com.

## 中文翻译（Chinese Translation）

推荐系统的演进已从传统协同过滤转向基于 LLM 的智能体系统，后者依赖语义化的用户与物品记忆进行预测。然而，现有智能体将这些记忆彼此孤立地维护，忽略了关键的协同信号——例如用户-物品共同参与（co-engagement）以及社区中的同伴关系——这显著限制了它们挖掘隐式偏好、准确推断用户需求的能力，尤其在数据稀疏用户上表现突出。为弥合这一差距，我们提出"协同记忆"（collaborative memory）这一新范式，将孤立的语义连接起来以共享关系性洞见。然而，朴素地使用协同记忆会造成严重的上下文过载，并向后续 LLM 引入噪声，同时带来高昂的计算成本。为此，我们提出 MemRec，一个在架构上将记忆管理与推理解耦的框架。MemRec 引入了一个专用的轻量级语言模型（LMMem），在后台高效管理并合成动态的协同记忆图，仅将经过蒸馏、高信号的上下文提供给下游的重量级大语言模型（LLMRec），由后者完成最终推荐。在四个基准上的大量实验表明，MemRec 取得了 SOTA 性能。代码：https://github.com/rutgerswiselab/memrec；主页：https://memrec.weixinchen.com。
