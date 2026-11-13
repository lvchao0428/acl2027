> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名：** `wydmuch-arxiv-2411.11829.pdf`

**原文标题：** Tackling prediction tasks in relational databases with LLMs

**作者：** Marek Wydmuch（Snowflake AI Research；波兹南工业大学）、Łukasz Borchmann（Snowflake AI Research）、Filip Graliński（Snowflake AI Research；亚当·密茨凯维奇大学）

**场合：** arXiv:2411.11829v1，2024-11-18

## 摘要（Abstract）

LLM 在很多问题上很强，但关系数据库上的预测几乎还没人做。常见说法是：表互相连接、关系复杂、类型混杂，LLM 做不好。作者用当时刚发布的 RelBench，说明哪怕很直接地使用 LLM，也能在这些任务上达到有竞争力的水平。摘要把 LLM 定位成关系库机器学习的一个新基线，并鼓励继续做。摘要没有给出具体分数。

## 1 Introduction

单表和结构化数据的资源在增加，无监督和有监督都有，例如 GitTables、TabLib，以及 Gardner et al. (2024) 列出的评测集。关系库没有得到对等的关注，尤其是和 LLM 一起看的时候。

关系库比单表复杂：多表、主键外键、一对多和多对多、类型不统一。带这种数据的机器学习基准不多。多数是 Text-to-SQL，如 Spider 和 BIRD；面向预测的少，文中点名 CTU Prague Relational Learning Repository、SJTUTable 和 RelBench。

本文只用 RelBench：7 个不同领域的关系库，一共 30 个分类和回归任务。难点是进经典模型之前，得把关系结构压成一张表示实例的表。已有 RelBench 结果来自梯度提升树和 relational deep learning（Fey et al., 2023; Robinson et al., 2024）。按标准方式或在表格数据上训练的 LLM，当时还没有结果。作者的做法是顺着表之间的链接做成信息比较密的文档，让预训练 LLM 做出能和 RDL 竞争的预测。具体做法和数字在第 3 节及以后，前两节只建立这个问题和数据定义。

## 2 Relational data and RelBench

表是行的集合，同一张表的行共享一组属性（列）。沿用 Robinson et al. (2024)，一行叫一个 entity。列有类型：数值、时间、文本、图像等。数据库是表的集合加上链接；一条链接是某表的外键列指向另一表的主键列。主键唯一标识一行，外键是对主键的引用。行还可以有创建时间。有时间列的是 fact table，没有时间列、存放静态信息的是 dimension table。

RelBench 的每个预测任务由一张 task table 定义：指向主表的外键、预测时间（seed time）、目标 y。按预测时间分成训练、验证和测试；同一实体可以带着不同时间戳多次出现。预测时间为 tp 时，只能使用时间戳严格早于 tp 的其他实体，以避免泄漏。

任务三类。（1）实体二分类，y 为 0 或 1，例如流失，指标 AUROC。（2）实体回归，y 为实数，例如销量，指标 MAE。（3）预测两个实体之间的链接，例如用户–物品推荐，指标 MAP。第 2 节到此为止，还没有描述 LLM 如何把这些表变成输入。
