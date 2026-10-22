# Optimizing User Profiles via Contextual Bandits for Retrieval-Augmented

> 来源文件：10_PURPLE.pdf

## 英文原文摘要（Original Abstract）

Large language models (LLMs) excel at general-purpose tasks, yet adapting their responses to individual users remains challenging. Retrieval augmentation provides a lightweight alternative to fine-tuning by conditioning LLMs on user history records, and existing approaches typically select these records based on semantic relevance. We argue that relevance serves as an unreliable proxy for utility: a record may be semantically similar to a query yet fail to improve generation quality or even degrade it due to redundancy or conflicting information. To bridge this gap, we propose PURPLE, a contextual bandit framework that oPtimizes UseR Profiles for LLM pErsonalization. In contrast to a greedy selection of the most relevant records, PURPLE treats profile construction as an order-sensitive generation process and utilizes a Plackett-Luce ranking model to capture complex inter-record dependencies. By training with semantically rich feedback provided by the likelihood of the reference response, our method aligns retrieval directly with generation quality. Extensive experiments on nine personalization tasks demonstrate that PURPLE consistently outperforms strong heuristic and retrieval-augmented baselines in both effectiveness and efficiency, establishing a principled and scalable solution for optimizing user profiles.

## 中文翻译（Chinese Translation）

大语言模型（LLM）擅长通用任务，但让其响应适配个体用户仍具挑战。检索增强（retrieval augmentation）提供了一种轻量级替代微调的方案——通过将用户历史记录作为条件注入 LLM——但现有方法通常基于语义相关性选择这些记录。我们认为，相关性并不能可靠代理效用（utility）：一条记录可能与查询在语义上相似，却因冗余或冲突信息而无法提升生成质量，甚至可能降低质量。为弥合这一差距，我们提出 PURPLE，一个上下文赌博机（contextual bandit）框架，用于优化 LLM 个性化的用户画像（oPtimizes UseR Profiles for LLM pErsonalization）。与贪婪地选择最相关记录不同，PURPLE 将画像构建视为一个顺序敏感的生成过程，采用 Plackett-Luce 排序模型刻画记录之间的复杂依赖。通过参考回复的似然（likelihood）所提供的语义丰富反馈进行训练，该方法将检索与生成质量直接对齐。在九项个性化任务上的大量实验表明，PURPLE 在效果与效率上都一致优于强启发式与检索增强基线，为用户画像优化提供了一种有原则且可扩展的方案。
