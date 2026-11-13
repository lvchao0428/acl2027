> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文标题：** Tackling prediction tasks in relational databases with LLMs

**作者：** Marek Wydmuch（Snowflake AI Research；Poznan University of Technology），Łukasz Borchmann（Snowflake AI Research），Filip Graliński（Snowflake AI Research；Adam Mickiewicz University）。

**场合：** 预印本，arXiv:2411.11829v1，2024-11-18。首页没有会议名。

**PDF：** `wydmuch-arxiv-2411.11829.pdf`

## Abstract

摘要认为大语言模型在很多问题上已经很强，但关系库上的预测任务几乎还没被用到。常见说法是：表互相连接、关系复杂、类型混杂，所以 LLM 得不到令人满意的结果。作者用 RelBench 检验这个说法。他们的结论是，即便很直接地使用 LLM，也能在若干关系预测任务上达到有竞争力的表现。具体任务分数不在摘要里。

## 1 Introduction

第 1 节先承认关系库比单表复杂：主键和外键、一对多和多对多、类型不统一。面向这种数据的机器学习基准不多。例子主要是 Spider、BIRD 这类 text-to-SQL，以及少数预测基准：CTU Prague Relational Learning Repository、SJTUTable 和 RelBench。

本文选定 RelBench，因为它新、真实、而且可以直接用。作者在这里写的规模是 7 个不同领域的关系库、合计 30 个预测任务，任务是分类和回归。困难来自必须先把关系结构摊成一张表，经典模型才能用。已有 RelBench 结果使用梯度提升树和关系深度学习，还没有标准训练或面向表格数据训练的 LLM 结果。本文的做法是沿着表与表的链接，把信息编成文档，再让预训练 LLM 做预测，并声称可以和关系深度学习相比。这一节把结果定位成一条简单基线，用来推动后续研究。数字表不在第 1 节。

## 2 Relational data and RelBench

第 2 节先把表、实体和链接定义清楚，再接到 RelBench 的对象。一张表是若干行，同一张表的行共享同一组列。按 Robinson 等人的用语，一行叫做一个实体。列有类型，例如数值、时间、文本、图像。一个关系库是若干张表加上表之间的链接。一条链接是外键列指向另一张表的主键列。主键唯一标识一行，外键是对主键的引用。

这一节的作用是给后文的「把链接走成文档」提供词汇，而不是报告 LLM 的准确率。RelBench 的任务仍是预测，不是自然语言问答。如何把多表走成一篇文档、以及和 RDL 的对照表，留在第 2 节后半和第 3 节。
