> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文标题：** RELBENCH: A Benchmark for Deep Learning on Relational Databases

**作者：** Joshua Robinson、Rishabh Ranjan、Kexin Huang、Jiaqi Han、Alejandro Dobles（Stanford），Weihua Hu、Matthias Fey、Yiwen Yuan、Zecheng Zhang、Xinwei He（Kumo.AI），Jan E. Lenssen（Kumo.AI；Max Planck Institute for Informatics），Jure Leskovec（Stanford；Kumo.AI）。Robinson、Ranjan、Hu、Huang 为同等贡献。

**场合：** NeurIPS 2024 Datasets and Benchmarks，12 页会议版。

**PDF：** `relbench-v1-neurips2024.pdf`

## Abstract

摘要把 RELBENCH 定义成用图神经网络做关系库预测任务的公开基准，库和任务覆盖多个域和规模，打算当后续研究的基础设施。作者用它做关系深度学习（RDL）的第一次系统研究：GNN 负责预测，深度表格模型从原始表抽出实体的初始表示。端到端的 RDL 直接用主键–外键里的预测信号，用来替换「手工特征工程加表格模型」这一主流做法。为了和这个金标准比，一位有经验的数据科学家为每个任务手工做特征。摘要给出的用户研究结果是：RDL 学到更好的模型，同时把所需人力减少一个数量级以上。

## 1 Introduction

第 1 节把缺口写成三件缺失的基础设施：标准化的库和任务、把数据变成图并训练 GNN 的初始实现、以及一份关于 RDL 是否有效的先导研究。RELBENCH 因此同时发布数据和代码。

库的范围写在这一节：电商、问答、医疗和体育；实体规模从 7.4 万到 4,100 万；训练时间跨度从 2 周到 55 年；表数从 3 到 15，列数从 15 到 140。每个库带多个预测任务，合计 30 个，包括实体分类、回归和推荐。软件有三块：加载库和任务的 Python 包、一份便于修改的 RDL 开源实现，以及公开排行榜。

和数据科学家基线的对比也在第 1 节给出总结：RDL 在准确率上打平或超过手工特征加表格模型，人力时间平均减少 96%，代码行数平均减少 94%。这被写成 RDL「端到端深度模型可以代替手工特征」的第一次实证。网站同时提供库、任务、代码和添加新任务的教程。

## 2 Overview and Design

第 2 节把基准拆成库和任务两件东西。库是用主键–外键相连的表，列里存放实体信息，有的表还有时间列，表示实体或记录何时产生，例如交易日期。任务由一张训练表定义，列包括实体 ID、种子时间和目标标签。种子时间表示在哪个时刻做预测，并用来滤掉未来数据。设计原则的其余部分（如何划分、如何防止泄漏）从这一节往后写，第 2 节开头先把这两个对象定下来。实体分类、回归和推荐共用这套训练表，差别在标签，不在输入是不是自然语言问句。
