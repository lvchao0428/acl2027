> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文标题：** Relational Deep Learning: Graph Representation Learning on Relational Databases

**作者：** Matthias Fey、Weihua Hu（Kumo.AI），Kexin Huang、Rishabh Ranjan、Joshua Robinson、Jure Leskovec（Stanford），Jan Eric Lenssen（Kumo.AI；Max Planck Institute for Informatics），Rex Ying（Kumo.AI；Yale），Jiaxuan You（Kumo.AI；UIUC）。同等贡献，按字母序。

**场合：** 预印本，arXiv:2312.04615。这份 PDF 没有会议页眉。

**PDF：** `rdl-fey-arxiv-2312.04615.pdf`

## Abstract

摘要指出有价值的数据大多在关系数据库和数据仓库里，表与表靠主键–外键相连。现有机器学习方法只能学一张表，所以要先把多表手工连接、聚合成一张训练表，也就是特征工程。作者认为这一步慢、容易错，而且模型因此不是最优的。他们提出端到端的深度表示学习，直接在由主键–外键连起来的多表上学，而不是先压成一张表。

## 1 Introduction

第 1 节用图 1 把流程画成三步：给定多表数据库；用一张训练表定义预测任务；把关系数据变成关系实体图，再在图上训练 GNN，监督来自训练表。任务可以是节点级、链接级或更高阶。

动机用决策场景说明：医院预测出院风险，电商预测销量，电信预测流失，音乐平台决定推哪首歌。这些任务背后都是多表模式。表格学习不能直接用在互相链接的表上。数据科学家要靠领域知识做连接和聚合，例如为了预测客户未来 k 天是否零交易，从交易表造出「过去 30 天购买次数」「过去 30 天金额」「周日购买次数」这类特征，再送进表格模型。作者把这种手工特征写成瓶颈：空间大、依赖人、而且一旦时间窗口或聚合方式选错，信号就丢了。关系深度学习的主张是让 GNN 在实体图上自己学这些聚合。RELBENCH 的网址写在首页，基准本身的任务列表不在这一节展开。
