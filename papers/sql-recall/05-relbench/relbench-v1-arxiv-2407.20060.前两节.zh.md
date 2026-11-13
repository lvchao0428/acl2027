> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名：** `relbench-v1-arxiv-2407.20060.pdf`

**原文标题：** RELBENCH: A Benchmark for Deep Learning on Relational Databases

**作者：** Joshua Robinson、Rishabh Ranjan、Weihua Hu、Kexin Huang（同等贡献，顺序随机）、Jiaqi Han、Alejandro Dobles、Matthias Fey、Jan E. Lenssen、Yiwen Yuan、Zecheng Zhang、Xinwei He、Jure Leskovec。单位：Stanford、Kumo.AI、Max Planck Institute for Informatics。

**场合：** arXiv:2407.20060v1，2024-07-29，首页写 Preprint, under review。网站 https://relbench.stanford.edu

同一篇的会议版见同目录 `relbench-v1-neurips2024.pdf`（NeurIPS 2024 Datasets and Benchmarks）。就前两节而言，会议版与这份预印本的主张和表 1 一致。

## 摘要（Abstract）

RELBENCH 是用图神经网络做关系数据库预测任务的公开基准，库和任务覆盖多个领域和规模，定位是后续研究的基础设施。作者用它做 Relational Deep Learning（RDL, Fey et al., 2024）的第一次系统研究：GNN 负责预测，深度表格模型负责从原始表抽出实体初始表示。端到端模型直接用主键–外键里的信号，而不是手工特征加表格模型。对照是一位有经验的数据科学家为每个任务手工做特征。摘要的结论是：RDL 模型更好，人力减少一个数量级以上。

## 1 Introduction

关系库流行是因为表好维护、SQL 好查，电商、社交、银行、医疗、制造和科学库都建在上面。没有能直接处理不同库结构的模型时，常见做法是把数据压成一张表再交给表格模型，预测信号丢失，抽取流水线也容易出错。

RDL 的图是一一对应的：每个实体一个节点，主键–外键是边，节点特征来自深度表格模型，预测用 GNN。作者认为这是第一个能碰到库里全部预测信号的端到端神经网络。缺的是基准、把数据变成图并训练 GNN 的实现，以及 RDL 是否有效的初步研究。RELBENCH 用来补这三块。

规模写在第 1 节：实体数从 7.4 万到 4100 万，训练时间跨度从 2 周到 55 年，表数 3 到 15，列数 15 到 140，一共 30 个任务，类型是实体分类、回归和推荐。发布物包括 Python 包、第一份开源 RDL 实现和排行榜。数据科学家基线的结果也在这一节：准确率上 RDL 持平或更好，人工工时平均减少 96%，代码行数平均减少 94%。

## 2 Overview and Design

基准提供两类东西。数据库：多表，主键–外键相连，列多样，部分表有实体创建时间。预测任务：一张 training table，列包括实体 ID、seed time 和标签；seed time 用来滤掉未来数据。

设计原则四块。

**数据选择。** 要有丰富的关系结构和列特征；领域要散（电商、社交、医疗、体育）；任务类型要盖住实体分类、实体回归和推荐。表 1 只统计测试时间切点及以前、可供测试推理的行。七个库是 rel-amazon、rel-avito、rel-event、rel-f1、rel-hm、rel-stack、rel-trial。合计 30 个任务、51 张表、103,466,370 行、489 列。任务例子包括顾客流失、临床试验不良事件数量、给用户推荐帖子。各库的行数、列数和时间切点以表 1 为准，这里不逐格复述。

**划分。** 按时间切：训练到 VAL_TIMESTAMP，验证在 VAL 与 TEST 之间，测试在 TEST_TIMESTAMP 之后。推理时藏起测试切点之后的数据；训练和验证用 Fey et al. (2024) 的时间邻居采样避免泄漏。作者强调防泄漏是设计者的责任，并建议用他们测过的实现。

**研究自由度。** 同一库上的任务共用同一对时间切点，便于多任务和预训练。库如何变成图的逻辑是公开的，方便改图的构造。

**开源 RDL。** 在与数据库一一对应的异构时间图上学习：实体分类和回归预测节点，推荐预测链接。初始嵌入用 PyTorch Frame，GNN 用 PyTorch Geometric。实现细节指向第 3 节；各库和任务的正文从第 4、5 节开始，与数据科学家的对照实验在第 6 节。
