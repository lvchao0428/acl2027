> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名：** `Arctic-Text2SQL-R1_ACL2026-Findings.pdf`

**原文标题：** Arctic-Text2SQL-R1: Simple Rewards, Strong Reasoning in Text-to-SQL

**作者：** Zhewei Yao、Guoheng Sun、Lukasz Borchmann、Zheyu Shen、Minghang Deng、Bohan Zhai、Hao Zhang、Ang Li、Yuxiong He（Snowflake AI Research；University of Maryland, College Park；University of California, San Diego）。首页注明 Yao 与 Sun 同等贡献，Yao 为项目负责人。

**场合：** Findings of the Association for Computational Linguistics: ACL 2026，页 26966–26995，2026 年 7 月 2–7 日。

## 摘要

这篇工作把 Text2SQL 的剩余难点收成一件事：复杂问句上，模型要交出能跑、而且跑出来的结果是对的 SQL。Arctic-Text2SQL-R1 既是一套强化学习做法，也是一组模型。奖励被压得很轻，只看执行对不对，不用容易碎掉的中间标注，也不做层层叠叠的 reward shaping，目的是让训练更稳，并且和最终任务对齐。

作者强调，单靠这个奖励不够，还要配上筛选过的数据、较强的监督起点和一套训练习惯。摘要给出的成绩是：六个差异较大的 Text2SQL 基准上执行准确率处于当时领先，并进入 BIRD 排行榜靠前位置；其中 7B 模型胜过此前 70B 这一档的系统。推理时还可以加上 value retrieval 和 majority voting。实验和消融既写成功也写失败，作为后续研究的经验。摘要没有点出表号。

## 1 Introduction

开篇把 Text2SQL 放在“非专业用户用自然语言查库”这一用途上，并把它看成自然语言理解与人机交互里的核心问题。近作已经让 SQL 写得更顺、覆盖更广（Ma et al., 2025; Pourreza et al., 2025; Zhai et al., 2025; Papicchio et al., 2025），可是多表连接、嵌套和细微的 schema 理解仍然容易错。作者把常见路线概括成对 (question, SQL) 对做监督微调（Li et al., 2025; Gao et al., 2024），并认为这种训练往往带不出可靠、可泛化生成所依赖的中间推理。

Arctic-Text2SQL-R1 的主张因此很窄：强化学习的奖励只看执行是否正确，避免部分奖励；同时用数据过滤、合成数据和基于模型的挑选。节末的判断是，数据质量、强监督初始化和简单奖励必须一起出现，模型才会又准、又能放大、又稳。

六条贡献里，第 1 节真正写出数字的是基准成绩：六个基准上同时超过专用 SQL 模型和通用大模型，点名 GPT-4o（OpenAI, 2023）和 DeepSeek-V3（Liu et al., 2024）。BIRD 上 32B 的 execution accuracy 是 71.83%，再用 self-consistency 升到 73.84%；在公开了细节的模型中排第一。7B 已经超过此前的 70B 级系统（Zhai et al., 2025）。其余几条没有新数字：执行奖励的 RL 要能跨规模、跨基准；数据侧包括过滤、合成、模型筛选，以及利用强监督检查点和提示设计的 online RL training；评测故意铺开六个数据集，以免只拟合单一基准；推理侧用 value retrieval 和 majority voting，开销很小；正负结果都公开。本节没有表。摘要说奖励 “solely on execution correctness”，第 2 节表 1 却把 syntax 也列进奖励，这个差别要到下一节才看得到。方法从第 3 节才开始。

## 2 Related Work

第 2 节只铺两条相关工作：把 Text2SQL 做稳，以及用 RL 提升语言模型的推理。写法是先借 RL 文献里“奖励最终正确就能长出推理”的结论，再批评 Text2SQL 里奖励成分越加越多，最后用表 1 把自己和几篇近作对齐。

**Reinforcement Learning for LLM Reasoning。** 这一小节的论点是：只要对逻辑正确和分步推理给明确奖励，模型会自己摸出解题策略，样子接近有结构的人类推理。例子分成数学（按步骤对错或最终答案做 RL 微调）和代码（偏好优化、以及来自人类反馈的 RL，用来提高代码是否有效、是否高效）。算法上，从 Proximal Policy Optimization（PPO, Schulman et al., 2017）写到更近的 Group Relative Policy Optimization（GRPO, Guo et al., 2025; Yang et al., 2024b; Dang and Ngo, 2025）。GRPO 在这里被定义成：一次比较一组生成，而不是给单条回答单独打分；作者认为这对“合理答案不止一个”的推理任务更合适。DeepSeek-R1-Zero 被当作例证：只奖最终答案正确，就会出现多步 chain-of-thought 和自我验证。小节末尾留了一句限制：这些框架常常还要靠精心做的偏好数据和奖励模型。本文的用法是把 GRPO 挪到 Text2SQL，奖励盯住最终能否执行正确，从而逼模型把查询的组合结构想完整。

**Text-to-SQL。** 任务史被收成三段。规则和手工语法碰到歧义或 schema 一变就脆（Androutsopoulos et al., 1995; Li and Jagadish, 2014）。神经序列到序列少做了一些手工语义解析，但往往要复杂的 schema 编码器和强监督（Guo et al., 2019; Wang et al., 2021）。LLM 让无模板 SQL 成为常态，开箱就有基本 SQL 能力，复杂多表查询则仍然有限，除非明确推动组合推理。因此才有 Chain-of-Thought prompting、query decomposition 和基于执行的反馈。作者接着把近期 Text2SQL 的 RL 概括成多成分奖励：执行反馈、句法是否合法、部分字符串重叠、schema 是否一致等绑在一起（Pourreza et al., 2025; Ma et al., 2025; Papicchio et al., 2025）。他们用语义解析里的观察（Skalse et al., 2022）指出，复杂奖励容易诱发表层 reward hacking。正面对照是更早的 Seq2SQL（Zhong et al., 2017）：更简单、以执行为中心的奖励可以更稳也更有效。和第 1 节相比，这里把本文的独特之处写成三件事合在一起：精简的数据过滤流水线、基于组的相对策略优化、严格基于执行的奖励，并指向表 1。

表 1 的列是 Framework 与 Optimization (Reward)：

| 框架 | 优化（奖励） |
| --- | --- |
| Reasoning-SQL (Pourreza et al., 2025) | GRPO（EX, syntax, n-gram, LLM, schema, format） |
| SQL-R1 (Ma et al., 2025) | GRPO（EX, length, syntax, format） |
| Think2SQL (Papicchio et al., 2025) | GRPO（precision, recall, cardinality, 2×format） |
| ExCoT (Zhai et al., 2025) | DPO（EX） |
| Arctic-Text2SQL-R1 | GRPO（EX, syntax） |

表里 Arctic 的奖励是 EX 加 syntax，不是只有 EX；正文仍把它说成比其他框架更精简、而且是 “strictly execution-based”。第 2 节到表 1 为止。奖励公式和实验从第 3 节 Methodology 起，这里不展开。
