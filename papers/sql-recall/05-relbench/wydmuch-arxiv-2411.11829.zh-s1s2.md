# Tackling prediction tasks in relational databases with LLMs

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`wydmuch-arxiv-2411.11829.pdf`。

## Abstract / 摘要

尽管大语言模型（large language models, LLMs）已在众多问题上表现出色，将其用于关系数据库上的预测任务仍大体未被探索。本文针对这样一种看法：由于表彼此相连、关系复杂、数据类型异构，LLM 无法在关系数据库上得到令人满意的结果。我们使用最近提出的 RelBench 基准表明，即便直接应用 LLM，也能在这些任务上取得有竞争力的表现。这些发现把 LLM 确立为关系数据库上机器学习（machine learning, ML）的一种有前景的新基线，并鼓励沿此方向继续研究。

## 1 Introduction / 引言

把大语言模型以及更一般的基础模型（foundational models）用到关系数据库上，在很大程度上仍是尚未探明的领域。面向表格数据与结构化数据的资源近来增长很快，无监督与监督学习任务都已有可用资源（例如 GitTables（Hulsebos et al., 2023）、TabLib（Eggert et al., 2023）），评测数据集也在增加（见 Gardner et al. (2024) 的列表）——但关系数据库尚未得到可比的关注，在 LLM 这一背景下尤其如此。

关系数据库本质上比单张表更复杂：它们是由主键与外键连在一起的一组表，包含一对多与多对多关系，以及异构的数据类型。涉及这类数据库的机器学习基准并不多。例子大多是 Text-to-SQL 数据集，如 Spider（Yu et al., 2018）、Bird（Li et al., 2024a）；迄今以预测任务为中心、值得注意的基准只有少数几个：CTU Prague Relational Learning Repository（Motl and Schulte, 2024）、SJTUTable（Li et al., 2024b），以及 RelBench（Robinson et al., 2024）。

本文聚焦 RelBench。它是最近发表的、现实且易于获取的基准，用于关系数据上的分类与回归。它汇集了来自不同领域的 7 个关系数据库，每个库带有一组预测任务，共计 30 个任务。RelBench 的难点来自关系数据本身。在使用经典机器学习模型之前，必须把复杂的关系结构“展平”成一张表，作为实例的表示。此前在 RelBench 上的工作报告了标准机器学习方法（例如梯度提升树（gradient-boosted trees）（Friedman, 2001））以及关系深度学习（relational deep learning）方法（Fey et al., 2023; Robinson et al., 2024）的结果。到目前为止，还没有在该基准上报告使用 LLM 的结果，无论这些 LLM 是按常规方式训练，还是用表格数据训练。本文给出一系列在 RelBench 上使用预训练 LLM 得到的结果。重要的是，我们表明：顺着表与表之间的链接走，可以构造信息丰富的文档，使 LLM 的预测能够与关系深度学习方法相比。我们的结果建立了一条新的简单基线，并促使这一方向的进一步研究。

## 2 Relational data and RelBench / 关系数据与 RelBench

表 \(T\) 定义为由 \(n\) 行组成的集合 \(T = \{R, \ldots, R_n\}\)【抽取不清：花括号内第一项在抽取文本中写作 “R”，下标没有读出】。同一张表里的所有行具有同一组属性，属性也称为列。沿用 Robinson et al. (2024) 的用语，我们把某一张表中的一行也称为实体（entity）。每一列对应一种数据类型，例如数值、时间、文本、图像等。关系数据库可以表示为一组表 \(T = \{T_1, \ldots, T_t\}\) 以及这些表之间的链接 \(L = \{L_1, \ldots, L_l\}\)。一条链接 \(L = (T_{\mathrm{fkey}}, T_{\mathrm{pkey}})\) 由 \(T_{\mathrm{fkey}}\) 中的一个外键列构成，该列指向 \(T_{\mathrm{pkey}}\) 的主键列。主键是表中一行的唯一标识；外键是对另一张表中某个主键的引用。此外，表中每一行都可以带一个时间戳 \(t\)，表示该行创建的时间。带时间戳列的表称为事实表（fact tables）；没有时间戳、存放静态信息的表称为维度表（dimension tables）（Garcia-Molina et al., 2008）。

在 RelBench 中，每个预测任务由一张任务表定义。任务表含有指向数据库主表的外键、预测时间（也称种子时间，seed time），以及待预测的目标变量 \(y\)。任务表按预测时间 \(t_p\) 分成训练表、验证表和测试表（同一实体可以带着不同的时间戳，在训练、验证和测试表中出现多次）。预测时间表示应当在哪一时刻预测目标。它会滤掉数据库中的未来数据，以保证时间一致性，并防止信息泄漏。形式上，当为预测时间等于 \(t_p\) 的实体做预测时，模型只能使用另一实体 \(v\) 中满足 \(t_v < t_p\) 的信息作为输入。

RelBench 提供 3 类预测任务：（1）实体级二分类，其中 \(y \in \{0, 1\}\)（例如流失预测，churn prediction），用 ROC 曲线下面积（area under the ROC curve, AUROC）（McNeil and Hanley, 1984）评估；（2）实体级回归，其中 \(y \in \mathbb{R}\)（例如预测售出物品的总量），用平均绝对误差（mean absolute error, MAE）评估；（3）预测两个实体之间链接的任务（例如用户–物品推荐），用平均精度均值（mean average precision, MAP）评估。总之，RelBench 要代表真实关系数据库中典型的预测与预报任务。
