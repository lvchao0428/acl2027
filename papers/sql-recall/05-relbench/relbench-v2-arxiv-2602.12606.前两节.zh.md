> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名：** `relbench-v2-arxiv-2602.12606.pdf`

**原文标题：** RELBENCH V2: A Large-Scale Benchmark and Repository for Relational Data

**作者：** Justin Gu、Rishabh Ranjan、Charilaos Kanatsoulis、Haiming Tang、Martin Jurkovic、Valter Hudovernik、Mark Znidar、Pranshu Chaturvedi、Parth Shroff、Fengyu Li、Jure Leskovec。单位包括 Stanford、新加坡国立大学、卢布尔雅那大学、Kumo AI、Oxford。

**场合：** 3rd DATA-FM workshop @ ICLR 2026。arXiv:2602.12606v2，2026-05-09。网站 https://relbench.stanford.edu

## 摘要（Abstract）

RDL 把多表和表间关系直接当学习对象。模型变大、关系基础模型出现之后，需要能扩展的真实基准。RELBENCH v2 在 v1 上扩充：新增四个大规模关系数据集，领域是学术出版物、企业资源计划、消费平台和临床记录，新增超过 2200 万行、29 张表，基准里的数据集总数到 11 个。新任务类是 autocomplete：在遵守时间约束的前提下，补关系表里缺失的属性，而不是只做用 SQL 构造出来的未来预测。基准还接上外部资源：把 Temporal Graph Benchmark 的事件流翻译成关系 schema；通过 ReDeLEx 统一访问 70 个以上适合预训练的真实库；纳入 4DBInfer 的数据集和任务。摘要中的实验结论是：在 autocomplete、预测和推荐任务上，RDL 稳定超过单表基线。

## 1 Introduction

关系库是企业、科研和医疗里结构化数据的主要存法，预测任务包括流失、销量、推荐和病人或系统结果。RDL（Robinson et al., 2024; Fey et al., 2024）用异构图和 GNN 或其他关系表示架构直接建模，少做手工压平。单表基础模型已经很强，但不看多表结构；关系基础模型是把 RDL 架构拿去预训练。v1 提供真实库和预测未来结果的 forecasting 任务，并用来说明 RDL 相对传统做法有效。

v2 的增量是新数据、新任务类型和新的预测设定。四个新库：rel-arxiv（论文、作者、类别、引用）、rel-salt（销售订单和业务流程）、rel-ratebeer（用户交互、商品、评论）、rel-mimic（电子病历）。合计超过 2200 万行、29 张表。autocomplete 要在给定时间戳上预测表中已有列的缺失值，不能泄漏未来信息。外部整合三条：TGB 的时间交互、ReDeLEx 上 70 个以上关系库、4DBInfer 的四维图中心设计空间。RDL 和关系基础模型的更多讨论指向附录 A。

## 2 Overview and Design

v1 的两块被重述一遍：多表数据库，以及每库一组预测任务。时间切点仍是 VAL_TIMESTAMP 和 TEST_TIMESTAMP，测试切点之后的数据在推理时隐藏，训练用 Fey et al. (2024) 的时间邻居采样。training table 仍有实体 ID、seed time 和标签；同一数据集上的任务共用切点，以便多任务和预训练。

**Autocomplete。** 与 forecasting 的差别是：forecasting 的标签由 SQL 构造出来；autocomplete 预测的是表里已经存在的列。可以想成往库里加一行，填上一部分列，再在不能看未来的前提下预测其余列。每个任务固定一组观测列和一个目标列。动机来自 SALT 的销售订单界面：根据已填字段和 schema 上下文推荐付款类别（图 5，不在这两节展开）。

泄漏是主要设计问题，因为同表列可能高度相关。作者按领域知识和训练数据检查，手工删掉与目标高度相关的列。例子：rel-amazon 的 review-rating 任务必须丢掉 review_text，否则正文和评分缠在一起。

**RDL 实现。** 与 Robinson et al. (2024) 相同：PyTorch Frame 里的 ResNet 表格模型把行编成初始节点嵌入；在 seed time 周围做时间子图采样；异构 GraphSAGE（求和聚合邻居）更新嵌入；任务头输出预测。新库的统计在表 1，只计测试切点及以前的行。rel-mimic 为隐私平移了日期。四库合计 21 个任务、29 张表、22,615,013 行、327 列：rel-salt 8 个任务、4 表、4,257,145 行；rel-arxiv 4 个任务、6 表、2,146,112 行；rel-ratebeer 8 个任务、13 表、13,787,005 行；rel-mimic 1 个任务、6 表、2,424,751 行。各库正文从第 3 节开始。
