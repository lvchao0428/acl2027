> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名：** `rdl-fey-arxiv-2312.04615.pdf`

**原文标题：** Relational Deep Learning: Graph Representation Learning on Relational Databases

**作者：** Matthias Fey、Weihua Hu、Kexin Huang、Jan Eric Lenssen、Rishabh Ranjan、Joshua Robinson、Rex Ying、Jiaxuan You、Jure Leskovec（同等贡献，按字母序）。单位包括 Stanford、Kumo.AI、Max Planck Institute for Informatics、Yale、UIUC。

**场合：** arXiv:2312.04615v1，2023-12-07。文内给出 RelBench：https://relbench.stanford.edu

## 摘要（Abstract）

数据在多张表里，靠主键–外键相连，但机器学习方法只能吃单表，所以要先手工 join 和聚合，也就是特征工程。作者认为这一步慢、易错，而且模型次优。Relational Deep Learning（RDL）把关系数据库看成带时间的异构图：每行一个节点，主键–外键是边，再用消息传递 GNN 在整张图上学习，不必手工做特征。摘要还宣布 RelBench：一组基准数据和一份 RDL 实现，例子从 Stack Exchange 讨论到 Amazon 商品目录上的书评。目标是把图机器学习推广到这类多表预测。

## 1 Introduction

第 1 节用出院风险、销量、流失、歌曲推荐说明：任务重要，背后都是多表 schema，但表格学习不能直接用在互相关联的表上。数据科学家要按领域知识把表压成一张特征表。流失例子是 CUSTOMERS、TRANSACTIONS、PRODUCTS：从交易表聚合出「过去 30 天购买次数、金额、星期几的购买」之类特征。时间又让标签和特征天天变，重算容易引入 time travel 一类泄漏。

手工特征的五条批评是：劳动密集；特征选择随意且可能次优；只能探索特征空间的一小部分；聚合成粗粒度后丢掉细信号；分布一变就要重做特征。对照是视觉从手工滤波器走到直接在像素上端到端学习。关系数据还没发生这次转变。

RDL 的图定义与摘要一致。预测任务靠一张额外的 training table 提供监督，这张表本身不放输入特征。标签可以从历史数据自动算出来，不必外部标注；外键个数决定任务类型：1 个是实体级，2 个是推荐这类链接级，多于 2 个是多实体任务。标签可以是多类、多标签或回归。

流水线四步（图 2）：按历史数据做 training table；每行用模态网络编成节点特征；沿主键–外键做消息传递；任务头输出预测并反传。时间约束是：节点只能收到更早时间戳的消息，避免泄漏，新数据到来时表示也会在前向里更新。

当时的 RelBench 还是早期版本，模块分数据、模型、评测；数据与评测不绑死某个深度学习框架。模型用 PyTorch Frame 编码行，再用 PyTorch Geometric 做 GNN。首发两个库、各两个任务：Stack Exchange 有帖子、用户、投票等 7 张表，任务是用户是否会再贡献，以及新问题的热度；Amazon 图书子集有用户、商品、评论 3 张表，任务是用户生命周期价值和是否会离开。第 1 节列出的后续机会包括多任务、新 GNN 结构和多跳学习。方法细节留到第 3 节。

## 2 Predictive Tasks on Relational Databases

第 2 节只定义数据和任务，不讲 GNN。关系库被收成三点：多表、每行一个带主键的实体、外键指向另一实体的主键。文中引用 DB-Engines（2023），称关系库约占世界数据的 72%。形式化对象是表集合 T 和表间链接 L。每个实体有四部分：主键、外键集合、属性、可选时间戳。同一张表的列空间相同，值可以缺失。

表再分成 dimension（相对静态的上下文，行数通常少）和 fact（交互记录，通常占大多数行，带时间列）。时间被当成一等公民，因为很多任务是预测未来，例如接下来 k 天花多少钱。防止未来信息进入训练的具体采样放到第 3 节。

### 2.2 From Task to Training Table

标签用历史数据生成。例子：在时刻 t 预测「未来 90 天购买额」，就把 t 到 t+90 的消费加总；只要 t+90 仍早于库里最新时间，就不需要外部标注。沿时间轴多取几个 t，同一实体可以有很多训练标签。

training table 的每一行有外键（指向被预测的实体）、时间戳、标签，没有输入特征 xv。它并进原库的表集合和链接里。训练预测 yv 时，只允许看到时间戳不晚于 tv 的实体。因此这张表同时规定输出（监督）和输入的时间切面。

任务形态：节点级是 ENTITY ID、LABEL、TIME 三列；链接预测再加上源实体和目标实体；时间任务需要 seed time，静态填补任务可以去掉 TIME。实践上，training table 由带时间条件的 SQL 生成：把查询窗口往过去平移，收集训练、验证和测试目标，并把 t 存成时间戳。
