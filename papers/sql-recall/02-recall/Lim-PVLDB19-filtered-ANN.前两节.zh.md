> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名**：Lim-PVLDB19-filtered-ANN.pdf

**原文标题**：Revisiting Filtered ANN Benchmarks: A Hardness-Controlled Benchmark Generator for Realistic Evaluation

**作者**：Mintaek Lim、Dogeun Kim、Minwoo Kim、Jaeyoung Do。四人均署 Seoul National University。Jaeyoung Do 为通讯作者。

**场合**：PVLDB, 19(10): 2763–2776, 2026。Proceedings of the VLDB Endowment, Vol. 19, No. 10，ISSN 2150-8097。doi:10.14778/3828612.3828630。许可为 Creative Commons BY-NC-ND 4.0。代码与数据：https://github.com/AIDASLab/FANN_Benchmark.git 。首页未见 arXiv 号。

## 摘要

Filtered approximate nearest neighbor（FANN）搜索要同时满足向量相似度和结构化谓词，但评测很脆：真实混合负载很少能公开，现有基准又靠临时拼出来的合成或半真实数据。作者认为真实程度取决于执行过程里的查询难度：早期过滤失败会触发额外候选的 over-fetching，从而改变延迟、吞吐和 recall。据此提出 α-Hardness，用 over-fetch factor 刻画条件执行链，并可延伸到随策略变化的设定。在多种数据和混合策略上，α-Hardness 与实测性能有强单调对齐；selectivity、属性–向量 correlation 这类常用代理则常常不稳，或随策略不一致。他们再给出硬度受控的基准生成器 HCBGen，用 α-Hardness 当显式控制信号，按粗粒度偏差模式合成负载，或去匹配目标硬度分布。实验结论是：常用基准只占硬度谱里偏窄、相对容易的一段，更难的查询才会露出稳健性缺口；匹配硬度分布还能做出隐私友好的代理负载，复现性能趋势，把研究基准和真实评测接起来。

## 1 INTRODUCTION

向量搜索已被写成现代数据管理的基本操作，用在 RAG、推荐、电商搜索和多模态分析里。生产环境里只比相似度不够，查询还要强制类别、时间或商品属性这类结构化谓词，否则正确性和安全过不了关。学术搜索被当作例子：自然语言先嵌成向量，再按相似度找论文，同时用户可能还要求特定会议或年份，谓词例子是 `year = 2026 and venue = VLDB`。系统因此要同时索引结构化属性和非结构化 embedding，返回的点既要通过过滤，又要离查询向量最近。

算法进展快，混合索引怎么可靠地做基准却是瓶颈。结果常常换数据集、换查询模式、换部署就对不上，从业者难以决定用哪种方法，研究者也难得出能站住的结论。原因被归到真实混合负载很少能共享：隐私、专有数据和公开覆盖有限。于是多数工作用合成或半真实负载，通常拿一个纯向量数据集，再合成标签、属性和带过滤的查询。

作者认为“混合负载”并不由底层向量集唯一决定，而取决于属性怎么赋给向量、过滤怎么组合、查询怎么生成；这些选择常常含糊，研究之间也不一致。同一批基向量上，很小的设计改动就能改变有效难度，从而改变方法排名。Fig. 1 用 RWalks 说明这种敏感：同一纯向量数据集 SIFT1M 上，按不同标签合成策略做出六条合成混合负载，recall–QPS 曲线差得很开。图例六条为 RWalks、ACORN、NHQ、UNG，以及 HCBGen (Ours, High-Car.)、HCBGen (Ours, High-Sel.)。纵轴 Recall@10 标到 0.0–1.0，横轴 QPS 标有 10^3、10^4、10^5。图注说明四条负载来自已有研究的设定，两条（High Cardinality 与 Highly Selective）来自本文的硬度控制框架；红色曲线是 RWalks 论文所用配置，在高吞吐下达到接近完美的 Recall@10，其余设计的权衡明显不同。曲线上各点的精确读数正文没有逐一给出。没有办法刻画并控制难度时，混合基准可能无意中偏向某种策略。现有合成基准既不显式建模、也不充分控制查询难度，差异常被平均指标盖住。真实负载的难度跨度很大，一小部分难查询就能主导尾延迟并暴露系统失败。这妨碍可靠评估，也挡住 FANN 在商业向量数据库里的采用。

缺口被说成缺少查询级硬度的原则性定义。selectivity 和 correlation 只覆盖难度的一部分，解释不了代理值相近的查询之间很大的性能差（后文 Section 3.1，本导读不展开）。以往主要控制基数、偏斜、相关和缺失等数据性质，查询则用随机属性组合或 selectivity 目标这类简单启发式生成。

α-Hardness 把混合搜索的查询级硬度定义成来自执行过程，而不是孤立的静态属性。FANN 执行被建模成一条条件链：向量检索、over-fetching 和条件过滤如何相互作用、代价如何沿路径累积。这个执行驱动的度量要对齐实测搜索性能，并且对新因素保持稳健：新影响表现为同一执行结构里的变化，而不必另造代理。硬度还可以当控制旋钮。HCBGen 用它规定硬度剖面来系统合成负载，而不是只盯 selectivity 或随机抽过滤组合。它能构造 Random-、Low-、High-hardness 几档，也能靠匹配目标硬度分布去逼近真实负载。由此有三件事：在可比难度下比较方法，降低负载构造暗中偏向某一策略的风险；故意做出高硬度负载，看失败模式和尾延迟，而不只看平均情况；机构可以分享硬度说明（例如硬度分布）来代替原始查询日志或敏感属性，仍支持可复现、可预测的性能刻画。实验还表明常用合成混合基准只落在硬度谱中偏窄且相对容易的一段。贡献被收成三条：定义与实测对齐的执行驱动度量 α-Hardness；重看常见混合基准实践，指出许多评测偏向容易查询、掩盖尾部行为并限制泛化；给出 HCBGen，用于受控构造、与索引无关的公平比较、按目标硬度做压力测试，以及用硬度说明对真实负载做隐私友好的近似。

## 2 PRELIMINARY

### 2.1 Filtered ANNs

FANN 在语义搜索上再加结构化过滤。标准 ANN 只按向量距离找近邻；FANN 还要对类别标签、数值范围或其他元数据加谓词。基数据写成

\[\mathcal{D} = \{(\mathbf{v}_i, \mathbf{a}_i) \mid i = 1, \ldots, N\}\]

其中 \(\mathbf{v}_i \in \mathbb{R}^d\) 是第 \(i\) 个点的 \(d\) 维 embedding，\(\mathbf{a}_i\) 是它的结构化属性集合。混合查询 \(q\) 由向量谓词 \(q_v \in \mathbb{R}^d\) 和一组过滤谓词 \(q_f\) 组成。目标是在满足 \(q_f\) 的点里，取离 \(q_v\) 最近的 top-\(K\)：

\[\mathrm{FANN}(q_{\mathrm{hybrid}}) = \arg\min_{\substack{S \subseteq \{i \mid q_f \subseteq \mathbf{a}_i\} \\ |S|=K}} \sum_{i \in S} d(q_v, \mathbf{v}_i)\]

\(d(\cdot,\cdot)\) 是 embedding 空间上的距离。多出来的过滤使 FANN 成为二维检索：剪枝时要决定先顾哪一边，索引必须同时处理非结构化向量相似度和结构化判断。

### 2.2 Filtered ANN Approaches

常见基线是 Post-Filtering 和 Pre-Filtering。Post-Filtering 先只按与 \(q_v\) 的向量相似度取候选，再套过滤；满足过滤的比例事先未知，所以通常在 HNSW 这类纯向量索引上 over-fetch。Pre-Filtering 先用谓词筛点，再在通过过滤的子集里做向量搜索；它避免 over-fetch，并能保证完整 recall，但没有查询专用索引时，往往退化成对过滤子集的暴力扫描，扩展性和吞吐受限。混合原生索引把相似度和过滤缠在搜索过程里，点到的有 NHQ、ACORN、UNG、RWalks 和 Filtered-DiskANN（FDANN）。NHQ 把基于属性的距离加进向量距离，以便在向量空间和属性空间上联合导航。ACORN 在建图时把 HNSW 图加密，遍历时只走满足过滤的节点，用来近似一个查询专用的 oracle 索引。UNG 按共享属性值分组，建一张同时有组内和组间连接的统一图。RWalks 在图上传播属性信息，做法被比作图神经网络的传播，再用得到的属性矩阵把搜索引向合法候选。FDANN 从感知标签的入口点出发，搜索时只探索满足过滤的节点。本节没有表格。
