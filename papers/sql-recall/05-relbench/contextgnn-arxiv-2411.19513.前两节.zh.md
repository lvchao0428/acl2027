> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名：** `contextgnn-arxiv-2411.19513.pdf`

**原文标题：** ContextGNN: Beyond Two-Tower Recommendation Systems

**作者：** Yiwen Yuan、Zecheng Zhang、Xinwei He、Akihiro Nitta、Weihua Hu、Dong Wang、Manan Shah、Shenyang Huang、Blaž Stojanovič、Alan Krumholz、Jan Eric Lenssen、Jure Leskovec、Matthias Fey（Kumo.AI）

**场合：** arXiv:2411.19513v1，2024-11-29

## 摘要（Abstract）

文章针对推荐里主流的 two-tower：用户和物品各自一个向量，用内积排序。这种表示与具体的用户–物品对无关。真正的 pair-wise 表示要么复杂度随候选对二次增长，要么必须先把候选对筛得很窄。ContextGNN 把两种表示放进同一个链接预测模型：用户局部子图里的熟悉物品用 pair-wise 表示，探索性物品退回 two-tower，再由一个网络决定怎么把两路分数合成一个排序。摘要的总结果是：在一组实际推荐任务上，相对已有传统方法和 GNN 方法平均提高 20%。

## 1 Introduction

第 1 节先说明 two-tower 为什么能扩展：用户和物品向量可以预先算好，推理时用近似最大内积搜索排序。代价是表示不看当前这对用户和物品。化妆品定期补货被用来说明：熟悉购买需要这对交互的细粒度上下文，单靠两个独立向量分不出来；探索新物品则是另一种行为。全量 pair-wise 不可行；先用内容或协同过滤筛候选，模型又被召回率卡住。

ContextGNN 被定义成单阶段、做时间推荐的 GNN，图是异构且带时间的。局部：对用户 k-hop 交互图里的物品做 pair-wise 表示，能记下重复购买、点击、收藏、加购，以及朋友是否买过同一物品。远处或不在局部子图里的物品，用基于浅层物品嵌入的 two-tower GNN 当退路，开销要能嵌进 pair-wise 架构。最后学一个随用户变化的融合分，决定这个人更吃熟悉物品还是探索。

部署场景是关系数据库上的 relational deep learning（Fey et al., 2024）：多表、多模态特征、多种行为、带时间。第 1 节末给出的对比是：相对最好的 pair-wise 基线平均提高 20%，相对最好的 two-tower 基线平均提高 344%。实验细节不在这两节。

## 2 Related Work

第 2 节把推荐写成用户–物品二部图上的链接预测：历史交互是边，要预测未来的边。传统路线是矩阵分解和协同过滤，用内积比较嵌入。深度学习之后包括非线性打分网络、图嵌入、变分自编码器，以及用大模型做生成式推荐。作者把自己放在两条线上：序列推荐，以及用 GNN 做推荐。

序列一侧从马尔可夫链写到 RNN、时间注意力和 Transformer，并提到有人把序列模型和 GNN 合起来以带上协同信号。GNN 一侧强调：只在交互图上传播不够，因为 GNN 是局部的，浅层用户/物品嵌入要一起传，才能保住协同信号；LightGCN、UltraGCN 把消息传递简化了；对比学习一类自监督是正交的，底下仍是 two-tower。

最接近的是让 GNN 带上身份和位置、从而能谈论具体用户–物品对的工作。局部子图加位置编码缺少高效推理。NBFNet 从用户节点出发建子图，在物品节点读出表示，于是物品表示条件于这个用户，又不必给所有对都算一遍；限制是候选只能落在用户子图里，探索和冷启动物品做不好。ContextGNN 的局部模型沿这条线改到异构、多行为、带时间的设定，并用 two-tower 退路去掉「只能看局部」这一限制。时间推荐的评测被指向 Temporal Graph Benchmark 和 RelBench；本文采用时间推荐的任务定义，主要在 RelBench 上评。
