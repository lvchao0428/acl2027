# PURPLE: 通过上下文赌博机优化用户画像实现检索增强 LLM 个性化

**原标题**: Optimizing User Profiles via Contextual Bandits for Retrieval-Augmented LLM Personalization

**作者**: Linfeng Du, Ye Yuan, Zichen Zhao 等

**单位**: McGill University; Mila; MBZUAI; Salesforce

## 摘要

大语言模型（LLMs）擅长通用任务，但将其回复适配到个体用户仍然充满挑战。检索增强提供了一种轻量级的微调替代方案，通过在用户历史记录上条件化 LLM 来实现个性化，现有方法通常基于语义相关性来选择这些记录。我们认为**相关性是效用的不可靠代理**：一条记录可能在语义上与查询相似，但未能提升生成质量，甚至由于冗余或冲突信息而降低质量。为弥合这一差距，我们提出 PURPLE，一个通过上下文赌博机框架**优化用户画像以实现 LLM 个性化**的方法。与贪婪地选择最相关记录不同，PURPLE 将画像构建视为顺序敏感的生成过程，利用 Plackett-Luce 排序模型来捕获复杂的记录间依赖关系。通过使用参考回复似然提供的语义丰富反馈进行训练，我们的方法将检索与生成质量直接对齐。在九个个性化任务上的广泛实验表明，PURPLE 在有效性和效率上均持续优于强启发式和检索增强基线，为优化用户画像建立了一个原理性且可扩展的解决方案。
