# HARPO: Hierarchical Agentic Reasoning for User-Aligned Conversational

> 来源文件：04_HARPO.pdf
> 发表年份：2026
> 单位：Indian Institute of Technology, Patna

## 英文原文摘要（Original Abstract）

Conversational recommender systems (CRSs) operate under incremental preference revelation, requiring recommendation decisions under uncertainty. While recent LLM-based approaches achieve strong performance on proxy metrics such as Recall@K and BLEU, they often fail to deliver high-quality, user-aligned recommendations in practice, as they optimize intermediate objectives like retrieval accuracy or fluent generation rather than recommendation quality itself. We propose HARPO (Hierarchical Agentic Reasoning with Preference Optimization), an agentic framework that reframes conversational recommendation as a structured decision-making process optimized for multi-dimensional recommendation quality. HARPO integrates (i) hierarchical preference learning that decomposes recommendation quality into interpretable dimensions (relevance, diversity, satisfaction, and engagement) with context-dependent weighting; (ii) deliberative tree-search reasoning guided by a learned value network evaluating candidate paths on predicted quality; and (iii) domain-agnostic reasoning abstractions through Virtual Tool Operations and multi-agent refinement. We evaluate HARPO on ReDial, INSPIRED, and MUSE, demonstrating consistent improvements over strong baselines on recommendation-centric metrics while maintaining competitive response quality. Our code is available at https://harpo-bench.github.io.

## 中文翻译（Chinese Translation）

对话式推荐系统（CRS）运行在增量偏好揭示（incremental preference revelation）的场景下，需要在不确定性中做出推荐决策。尽管近期基于 LLM 的方法在 Recall@K、BLEU 等代理指标上表现优异，但它们在实际中往往无法交付高质量、与用户对齐的推荐，因为它们优化的是检索准确率或流畅生成等中间目标，而非推荐质量本身。我们提出 HARPO（Hierarchical Agentic Reasoning with Preference Optimization），一个智能体框架，将对话式推荐重新建模为面向多维推荐质量优化的结构化决策过程。HARPO 整合了：（i）层次化偏好学习，将推荐质量分解为可解释的维度（相关性、多样性、满意度、参与度），并结合上下文相关的权重；（ii）由学习到的价值网络引导的审慎树搜索推理，对候选路径按预测质量进行评估；（iii）通过虚拟工具操作（Virtual Tool Operations）和多智能体精炼实现领域无关的推理抽象。我们在 ReDial、INSPIRED 和 MUSE 数据集上对 HARPO 进行了评测，结果表明它在以推荐为中心的指标上一致优于强基线，同时保持了有竞争力的回复质量。代码：https://harpo-bench.github.io。
