# Arctic-Text2SQL-R1: Simple Rewards, Strong Reasoning in Text-to-SQL

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`Arctic-Text2SQL-R1_ACL2026-Findings.pdf`。

## Abstract 摘要

将自然语言翻译为 SQL（Text2SQL）是自然语言理解与结构化数据访问交汇处的一个长期挑战。尽管大语言模型（large language models, LLMs）已显著提高 SQL 生成的流畅性，但产出正确且可执行的 SQL——尤其是复杂查询——仍然是瓶颈。本文提出 Arctic-Text2SQL-R1，一个强化学习（reinforcement learning, RL）框架及相应的模型家族，仅依靠基于执行正确性的轻量奖励信号来生成准确、可执行的 SQL。该方法避免脆弱的中间监督和复杂的奖励塑形（reward shaping），从而有利于训练稳定，并与最终任务对齐。结合精心整理的数据、强监督初始化以及有效的训练实践，Arctic-Text2SQL-R1 在六个不同的 Text2SQL 基准上取得了最先进的执行准确率（execution accuracy），并位列 BIRD 排行榜前列。值得注意的是，我们的 7B 模型超过了此前的 70B 量级系统，体现了该框架的可扩展性与效率。我们进一步通过值检索（value retrieval）和多数投票（majority voting）等简单扩展，展示了推理阶段的稳健性。大量实验与消融研究同时给出正面与负面的认识，为后续 Text2SQL 研究提供了可操作的指导。

## 1 Introduction 引言

把自然语言问题翻译成 SQL 查询，通常称为 Text2SQL，是自然语言理解与人机交互中的核心挑战。一个稳健的解决方案将使非技术用户能够用自然语言查询结构化数据库，从而让数据分析更加普及。大语言模型的最新进展显著提高了 Text2SQL 系统的流畅性与表层覆盖（Ma et al., 2025; Pourreza et al., 2025; Zhai et al., 2025; Papicchio et al., 2025）。然而，生成正确且可执行的 SQL 仍然困难，尤其是涉及多表连接、嵌套逻辑以及对数据库模式（schema）作细致理解的复杂查询。现有方法大多在（问题, SQL）对上进行监督微调（Li et al., 2025; Gao et al., 2024），往往无法促进对可靠、可泛化的 SQL 生成至关重要的中间推理步骤。

本文提出 Arctic-Text2SQL-R1，一个用于从自然语言生成高质量可执行 SQL 的强化学习框架及模型家族。它只使用基于执行正确性的轻量奖励，避免脆弱的部分奖励，同时促进训练稳定并与最终目标对齐。结合数据过滤、合成生成和基于模型的筛选等方面的最佳实践，Arctic-Text2SQL-R1 表明：高质量数据、强监督初始化与简单的奖励信号共同作用，可以得到准确、可扩展且稳健的 Text2SQL 模型。我们的主要贡献如下：

- **面向 Text2SQL 的简单且可扩展的 RL。** 我们提出一种只使用执行奖励的轻量 RL 形式化。它在不同模型规模和基准上都能较好泛化，无需复杂的奖励设计即可稳定训练并取得强性能。
- **全面的基准领先。** 在六个不同的 Text2SQL 基准上，Arctic-Text2SQL-R1 持续优于面向 SQL 的专用模型与通用 LLM，包括 GPT-4o（OpenAI, 2023）和 DeepSeek-V3（Liu et al., 2024），显示出跨领域的稳健泛化。在 BIRD 排行榜上，我们的模型位居前列：32B 模型的执行准确率为 71.83%，使用自洽性（self-consistency）后进一步提升到 73.84%。在公开了细节的模型中，Arctic-Text2SQL-R1 排名第一，从而保证透明、可复现与可获取。值得注意的是，我们的 7B 模型甚至超过了此前的 70B 量级系统（Zhai et al., 2025），体现了该方法的可扩展性与效率。
- **真正起作用的数据与训练策略。** 我们给出数据过滤、合成数据生成和基于模型的筛选的最佳实践。此外，我们展示了在线 RL 训练（online RL training）的价值：它利用强监督检查点与精心设计的提示进一步提升性能。这些实践与高质量数据、简单的执行驱动奖励相结合，产生准确、可扩展且稳健的 Text2SQL 模型。
- **广泛而严格的评测。** 我们在六个 Text2SQL 数据集上评测 Arctic-Text2SQL-R1，覆盖不同的模式复杂度与查询难度。这为泛化提供了有力证据，并避免过拟合到单一数据集或单一评测形式。
- **推理时的稳健性与可延伸性。** Arctic-Text2SQL-R1 支持值检索和多数投票等简单的推理时技术，能以很小的系统开销进一步提高准确率，表明其适合实际部署。
- **面向社区的经验认识。** 我们同时报告成功的发现与负面的发现，提供透明、可操作的认识，以指导未来基于 RL 的 Text2SQL 研究与开发。

## 2 Related Work 相关工作

Arctic-Text2SQL-R1 的研究从两个方向获得启发，并试图推进它们：稳健 Text2SQL 系统的构建，以及面向复杂语言模型推理的强化学习技术改进。

**面向 LLM 推理的强化学习。** 近期研究表明，RL 技术有潜力显著增强大语言模型的推理能力（OpenAI et al., 2025; Lambert et al., 2024; OpenAI et al., 2024; Guo et al., 2019）。通过对逻辑正确性与逐步推理给予显式奖励，RL 使模型能够自主发现有效的解题策略，这些策略常常类似于结构化的人类推理（Xu et al., 2025; Wang et al., 2025; Yang et al., 2025b）。应用涵盖数学问题求解——在逐步正确性或最终答案准确率上做 RL 微调能带来显著提升（Shao et al., 2024; OpenAI et al., 2024）——以及代码生成：偏好优化与基于人类反馈的 RL 提高了代码的有效性与效率（Wang et al., 2025; Yang et al., 2025b）。此前多数方法建立在策略梯度算法之上，例如近端策略优化（Proximal Policy Optimization, PPO）（Schulman et al., 2017），以及更新的组相对策略优化（Group Relative Policy Optimization, GRPO）（Guo et al., 2025; Yang et al., 2024b; Dang and Ngo, 2025）。GRPO 比较一组生成回复，而不是孤立地评估单条回复。对于存在多个合理解的推理任务，这种方法尤其有效，使模型能更深入地理解何为高质量推理（Kumar et al., 2025）。例如，GRPO 使 DeepSeek-R1-Zero 等模型仅凭“最终答案正确”这一奖励，就发展出多步思维链（chain-of-thought）与自我验证等复杂推理技能（Guo et al., 2025）。这些 RL 框架的效果往往取决于精心设计的偏好数据集，以及能够准确反映逻辑推理细微差别的奖励模型。我们的工作借鉴这些认识，将 GRPO 适配到 Text2SQL，并把奖励信号集中在最终的可执行正确性上，鼓励模型对查询的完整组合结构进行推理。

**Text-to-SQL。** Text2SQL 任务多年来取得了显著进展（Zhu et al., 2024b）。早期系统基于规则与手工语法，但面对语言歧义或复杂的模式变化时很脆弱（Androutsopoulos et al., 1995; Li and Jagadish, 2014）。神经序列到序列模型的出现，帮助自动化了语义解析的一部分，不过这类模型往往需要精细的模式编码器与强监督（Guo et al., 2019; Wang et al., 2021）。更近一些，LLM 的泛化能力革新了该领域，许多工作利用预训练 LLM 进行无模板的 SQL 生成，即是证明（Singh et al., 2025; Gao et al., 2023; Li et al., 2024）。LLM 在“开箱即用”的评测中常常表现出基本的 SQL 能力，但除非显式鼓励组合推理，它们在复杂多表查询上的表现仍然有限（Wei et al., 2023; Shao et al., 2024; Guo et al., 2025; OpenAI et al., 2024）。这推动了思维链提示（Chain-of-Thought prompting）（Tai et al., 2023）、查询分解（Eyal et al., 2023）以及基于执行的反馈（Hong et al., 2024; Deng et al., 2025）等技术。在这一图景中，基于 RL 的 Text2SQL 方法日益受到关注。它们常常建立在结构化的多成分奖励函数上，把执行反馈、句法有效性、部分字符串重叠、模式一致性等聚合在一起（Pourreza et al., 2025; Ma et al., 2025; Papicchio et al., 2025）。然而，如此复杂的奖励工程有鼓励表面性奖励投机（reward hacking）的风险；语义解析中的 RL 已观察到这一现象（Skalse et al., 2022）。相比之下，我们主张更简单、以执行为中心的奖励设计，其灵感来自更早的基于 RL 的语义解析方法，如 Seq2SQL（Zhong et al., 2017），并表明这种最小奖励方案在实践中可以更稳定，也更有效。与最近的推理工作（Pourreza et al., 2025; Ma et al., 2025; He et al., 2025）或成对偏好优化（Zhai et al., 2025）相比，我们的方法的独特之处在于：把精简的数据过滤流水线、基于组的相对策略优化，以及严格基于执行的奖励统一起来（表 1）。

表 1：Arctic-Text2SQL-R1 与现有推理模型的奖励设计比较。

| 框架（Framework） | 优化（奖励） |
| --- | --- |
| Reasoning-SQL (Pourreza et al., 2025) | GRPO (EX, syntax, n-gram, LLM, schema, format) |
| SQL-R1 (Ma et al., 2025) | GRPO (EX, length, syntax, format) |
| Think2SQL (Papicchio et al., 2025) | GRPO (precision, recall, cardinality, 2×format) |
| ExCoT (Zhai et al., 2025) | DPO (EX) |
| Arctic-Text2SQL-R1 | GRPO (EX, syntax) |
