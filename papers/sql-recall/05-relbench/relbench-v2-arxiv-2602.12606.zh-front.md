> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文标题：** RELBENCH V2: A Large-Scale Benchmark and Repository for Relational Data

**作者：** Justin Gu、Rishabh Ranjan、Charilaos Kanatsoulis、Pranshu Chaturvedi、Parth Shroff、Fengyu Li、Jure Leskovec（Stanford），Haiming Tang（National University of Singapore），Martin Jurkovic（University of Ljubljana），Valter Hudovernik（Kumo AI），Mark Znidar（University of Oxford）。

**场合：** 3rd DATA-FM workshop @ ICLR 2026。arXiv:2602.12606v2，2026-05-09。这是研讨会论文，不是 ICLR 主会。

**PDF：** `relbench-v2-arxiv-2602.12606.pdf`

## Abstract

摘要认为关系深度学习已经能直接在多表上学习实体和关系，而且这一方向正在走向更大的模型和关系基础模型，因此需要可扩展、贴近真实的基准。RELBENCH v2 在 v1 上扩展：新增四个大规模关系数据集，领域包括学术出版、企业资源计划、消费平台和临床记录，新增超过 2,200 万行、29 张表，基准库数增到 11。新任务类型是 autocomplete：在给定时间戳上预测表中已有列的值。摘要还说会把若干外部基准和诊断框架接进这个仓库。

## 1 Introduction

第 1 节先说明关系库上的预测为什么重要：流失、销量、推荐、系统或病人结局，都依赖主键–外键带出来的结构和时间。RDL 把库看成异构图，用 GNN 或其他关系表示模型直接学，用来减少「把多表摊成一张表」的手工特征工程。作者把这一路线的已有结果写成：在关系数据的预测任务上达到了当时的高水平。

转折是基础模型。语言、视觉和单表表格上都出现了在多样数据上预训练、再迁移的模型，但单表模型看不到多表结构。近期工作开始做关系库的基础模型。v1 被写成第一个 RDL 基准，任务是预测未来结果，例如实体流失、销量或推荐。v2 的新增内容在节末点名：rel-arxiv（论文、作者、类别、引用），rel-salt（销售订单和业务流程），rel-ratebeer（用户、产品和评论），rel-mimic（来自电子健康记录的临床数据）。四库合计超过 2,200 万行、29 张表。除了 autocomplete，还接入 Temporal Graph Benchmark 的时间交互数据、ReDeLEx 在 70 个以上关系库上的评测，以及 4DBInfer 的四维设计空间。关系基础模型的更多讨论放在附录 A。

## 2 Overview and Design

第 2 节沿用 v1 的两个部件，并把时间切分写死。库是主键–外键相连的表，部分表有行创建时间。每个库有固定的 VAL_TIMESTAMP 和 TEST_TIMESTAMP：训练只用到验证切分之前的数据，验证用两道切分之间的行，测试用测试切分之后的行。测试切分之后的数据在推理时隐藏，采用 Fey 等人的时间邻居采样，避免测试泄漏。

任务仍由训练表定义，列是实体 ID、种子时间和标签。种子时间决定预测时刻并滤掉未来信息。同一库上的任务共用这两道时间切分，因此可以在同一库的多个任务上做多任务学习或预训练。

Autocomplete 是这一节引入的新任务：预测表里已经存在的列在某个时间戳上的值，模型要从关系和时间上下文补缺失值，同时不能看到不该看到的信息。表 1 开始给新库的统计，包括表数、行数、列数和切分日期；rel-mimic 的日期因患者隐私做了平移。各任务的指标不在第 2 节开头。
