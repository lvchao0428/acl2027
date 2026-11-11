> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文标题：** Arctic-Text2SQL-R1: Simple Rewards, Strong Reasoning in Text-to-SQL

**作者：** Zhewei Yao、Guoheng Sun、Lukasz Borchmann、Zheyu Shen、Minghang Deng、Bohan Zhai、Hao Zhang、Ang Li、Yuxiong He（Snowflake AI Research；University of Maryland, College Park；University of California, San Diego）。Yao 与 Sun 为同等贡献，Yao 为项目负责人。

**场合：** Findings of the Association for Computational Linguistics: ACL 2026，页 26966–26995，2026 年 7 月 2–7 日。

**PDF：** `Arctic-Text2SQL-R1_ACL2026-Findings.pdf`

## 摘要

文章把 Text2SQL 的瓶颈从“能不能写出像 SQL 的句子”收回到“能不能写出可执行且结果正确的 SQL”，尤其是复杂查询。作者提出强化学习框架和模型族 Arctic-Text2SQL-R1：奖励只看执行是否正确，刻意不依赖脆弱的中间监督，也不做复杂的 reward shaping，以便训练更稳、目标和最终任务对齐。

他们把这套轻奖励和三件事绑在一起：精选数据、较强的监督初始化、以及一套训练做法。摘要里的结果主张是：六个不同 Text2SQL 基准上的执行准确率达到当时的领先水平，并排进 BIRD 排行榜前列；7B 模型超过此前 70B 量级的系统。推理阶段再用 value retrieval 和 majority voting 做简单扩展。实验与消融同时给出正面和负面结论，供后续 Text2SQL 研究参考。

## 1 Introduction

第 1 节先把任务放回使用场景：非技术人员用自然语言查结构化库，Text2SQL 是自然语言模型与人机交互的核心问题。接着指出 LLM 已经改善了流畅度和表层覆盖（Ma et al., 2025; Pourreza et al., 2025; Zhai et al., 2025; Papicchio et al., 2025），但多表连接、嵌套逻辑和细微 schema 理解仍然难。作者把现有主流做法概括为在 (question, SQL) 对上做监督微调（Li et al., 2025; Gao et al., 2024），并认为这种监督往往推不动可靠、可泛化生成所需要的中间推理。

由此引出 Arctic-Text2SQL-R1：用执行正确性这一项轻量奖励做强化学习，避开脆弱的部分奖励；再配合数据过滤、合成生成和基于模型的筛选。节内的总判断是，高质量数据、强监督初始化和简单奖励三者合在一起，才能得到准确、可扩展、稳健的模型。

贡献按六条展开，第 1 节里已经给出的数字集中在第二条：

- 简单、可扩展的 RL：只用执行奖励，跨模型规模和基准泛化，不靠复杂奖励设计。
- 基准领先：六个 Text2SQL 基准上超过专用 SQL 模型和通用 LLM，点名 GPT-4o（OpenAI, 2023）与 DeepSeek-V3（Liu et al., 2024）。BIRD 上 32B 的 execution accuracy 为 71.83%，加上 self-consistency 到 73.84%。在公开了细节的模型里排第一。7B 超过此前 70B 量级系统（Zhai et al., 2025）。
- 数据和训练：过滤、合成、基于模型的筛选，以及 online RL training（用强监督检查点和设计过的提示继续提分）。
- 评测面：六个数据集，覆盖不同 schema 复杂度与查询难度，用来防止只拟合单一基准。
- 推理时：value retrieval 与 majority voting，用很小的系统开销再提准确率。
- 经验：成功与失败都报告，给后续基于 RL 的 Text2SQL 作参考。

本节没有另列表格。摘要里的“solely on execution correctness”与后文表 1 把 syntax 也写进奖励，需要到第 2 节对照，方法细节留在第 3 节。

## 2 Related Work

第 2 节把工作放在两条线上：稳健的 Text2SQL，以及用强化学习做语言模型推理。论证方式是先借已有 RL 结论，再指出 Text2SQL 里奖励越堆越复杂，最后用一张对照表把自己和近期推理模型分开。

**Reinforcement Learning for LLM Reasoning。** 作者把近期 RL 的作用概括为：对逻辑正确和逐步推理给显式奖励后，模型会自己找出解题策略，形态接近结构化的人类推理。应用被收成两类：数学题（按逐步正确或最终答案做 RL 微调）和代码生成（偏好优化以及来自人类反馈的 RL 提高有效性与效率）。算法谱系从 Proximal Policy Optimization（PPO, Schulman et al., 2017）接到 Group Relative Policy Optimization（GRPO, Guo et al., 2025 等）。GRPO 的定义在这里说清楚：比较一组生成结果，而不是孤立打分一条；对“多个答案都说得通”的推理任务更合适。例证是 DeepSeek-R1-Zero：只奖励最终答案正确，就出现多步 chain-of-thought 和自我验证。作者同时提醒，这些框架往往还依赖精心构造的偏好数据和奖励模型。本文的接法是把 GRPO 用到 Text2SQL，并把奖励集中在最终可执行正确性上，迫使模型把查询的完整组合结构想完。

**Text-to-SQL。** 历史被压成三步。早期规则和手工语法在语言歧义或 schema 变化下很脆（Androutsopoulos et al., 1995; Li and Jagadish, 2014）。神经序列到序列减轻了部分语义解析的手工，但常要复杂的 schema 编码器和强监督（Guo et al., 2019; Wang et al., 2021）。LLM 带来无模板 SQL 生成，开箱评测已有基本 SQL 能力，可是复杂多表查询若不显式鼓励组合推理，仍然有限。由此出现 Chain-of-Thought prompting、query decomposition 和基于执行的反馈。

落到 RL 路线时，作者的批评对象是多成分奖励：把执行反馈、句法有效性、部分字符串重叠、schema 一致性等捆在一起（Pourreza et al., 2025; Ma et al., 2025; Papicchio et al., 2025）。他们引用语义解析中的 RL 观察（Skalse et al., 2022），认为复杂奖励工程会鼓励表层 reward hacking。对照的正面先例是更早的 Seq2SQL（Zhong et al., 2017）：更简单、以执行为中心的奖励可以更稳、也更有效。

和第 1 节的差别在于，这里把“独特点”写成三件套：精简的数据过滤流水线、基于组的相对策略优化、以及严格基于执行的奖励。表 1 把这句话落成可核对的奖励设计对照（Optimization / Reward）：

| 框架 | 优化（奖励） |
| --- | --- |
| Reasoning-SQL (Pourreza et al., 2025) | GRPO（EX, syntax, n-gram, LLM, schema, format） |
| SQL-R1 (Ma et al., 2025) | GRPO（EX, length, syntax, format） |
| Think2SQL (Papicchio et al., 2025) | GRPO（precision, recall, cardinality, 2×format） |
| ExCoT (Zhai et al., 2025) | DPO（EX） |
| Arctic-Text2SQL-R1 | GRPO（EX, syntax） |

表 1 印出的 Arctic 奖励是 EX 加 syntax，并不只剩 EX；正文仍称其为相对其他框架更精简、且“strictly execution-based”。第 2 节在表 1 之后结束，具体奖励公式、训练数据和实验表从第 3 节 Methodology 起，此处不展开。
