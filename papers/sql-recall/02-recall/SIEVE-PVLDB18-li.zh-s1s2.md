# SIEVE: Effective Filtered Vector Search with Collection of Indexes

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`SIEVE-PVLDB18-li.pdf`。

## Abstract 摘要

现实任务，例如推荐带有 kids 标签的视频，可以归结为寻找与硬谓词（hard predicates）相关联的相似向量。这一任务称为过滤向量搜索（filtered vector search）。它具有挑战性，因为先前最先进的、基于图的（无过滤）相似性搜索技术一旦考虑硬约束就会退化：有效的、基于图的过滤相似性搜索依赖于足够的连通性，以便在少数几跳之内到达相似物品。为了考虑谓词，近期工作提议修改图遍历，使之只访问满足谓词的物品。然而，它们无法在广泛的谓词上提供“只需几跳”（just-a-few-hops）这一性质：它们必须大幅限制谓词，否则当只有很少物品满足谓词时就会失去效率。

我们提出相反的做法：不去约束遍历，而是构建许多索引，每个索引服务于不同形式的谓词。为了有效构建，我们设计了一个三维分析模型，刻画索引大小、搜索时间与召回率（recall）之间的关系；据此，我们采用感知工作负载的方法，把尽可能多的有用索引装进一个集合。查询时再次使用该分析模型，在给定召回率下辨别出搜索最快的那一个。我们在选择率（selectivity）与形式各异的数据集上展示了更优的性能与支持：相对其他索引，我们的方法取得至多 8.06× 的加速，构建时间可低至对方的 1%，内存不到标准 HNSW 图的 2.15×，并且只需要对历史工作负载有适度了解。

## 1 INTRODUCTION 引言

寻找满足硬约束的语义相似物品是一项常见任务。妈妈们可能会搜索带有 “safe-for-kids” 标签（硬约束）的视频（语义）。网购者可能会搜索处于特定价格区间（硬约束）的戏服（costumes，语义）[74]。这一任务称为过滤向量搜索：我们查询的是编码语义、并与硬谓词相关联的相似向量。随着现代机器学习模型能够提供高质量的向量嵌入（vector embeddings）[35, 36, 43]，该问题受到越来越多的研究 [15, 16, 21, 23, 31, 39, 44, 48, 51, 61, 66, 74]。

一些工作通过约束原本用于无过滤向量搜索的、基于图的近似最近邻（approximate nearest neighbor, ANN）索引，来处理过滤向量搜索 [17, 27, 33]：FilteredVamana 把图遍历与过滤器求值交错进行；ACORN [44] 只访问通过谓词的节点，从而在查询时诱导出子图。这些工作优于预过滤（pre-filtering）这类朴素方法；预过滤使用（缓慢的）线性扫描来做相似度计算。基于图的方法经由边在物品之间导航，以少数几跳到达目标。有效的过滤向量搜索旨在用紧凑的图来服务查询；一旦小世界（small world）这一性质丢失，图遍历就会失去效率。

不幸的是，现有基于图的方法无法对低选择率谓词提供小世界性质，因而性能更差。此外，也不能简单改用预过滤，因为除非选择率过低，线性扫描仍然过于昂贵。这一选择率区间被称为 “unhappy middle” [23]。FilteredVamana 试图把共享属性的向量链接成局部的、稠密的、按过滤器划分的子图来缓解这一问题，但需要限制过滤器的形式 [21]。ACORN [44] 以一定代价支持一般谓词：若其诱导子图变得过于稀疏，则可以证明它会失去小世界性质 [4, 29, 33]。我们推测，单张图不足以处理全部谓词，这些谓词的支持集可能以复杂方式彼此重叠。我们可能需要多张图，每张图专门针对不同的谓词集合。

**Our Goal.** 我们的目标是：通过构建一个索引集合，为选择率或形式各异的几乎全部过滤查询提供紧凑的图。集合比单个索引更有表达力。借助真实世界过滤向量搜索工作负载中过滤器的稳定性 [39, 53]，我们可以按已观测的工作负载来定制索引，以最大化期望搜索质量。每个索引可以服务多个谓词：例如，为 stars=1–3 构建的图，若它对子谓词足够稠密，也可以服务 stars=1。索引集合比单个索引需要更多内存；不过，相对原始数据（即高维向量），索引相对较小。在我们的实验中，数百个（较小的）附加索引所占内存仅相当于一个覆盖全数据集的索引，同时相对只依赖一个索引，它们显著提升了性能。只要所提出的索引集合能为几乎全部查询提供高质量的过滤搜索、且每个查询都有一张紧凑的图，并同时保持内存高效，它就可以成功。

**Challenge.** 由于目标相互冲突，构建有效的索引集合具有挑战性。在构建时，图可以用召回率换取更小的尺寸（图 1a），从而允许更多索引与更大覆盖。然而，图必须足够稠密才能获得高召回率。同样，在查询时可以用搜索速度换取更高召回率（图 1b）。必须量化这一关系，才能为给定查询确定该使用哪个索引。这些独特性质使本任务区别于已有问题 [49, 52]。例如，物化视图选择（materialized view selection）面向的是精确查询，而 ANN 是近似的，并带有速度与召回率的权衡。

**Our Approach.** 我们的框架称为 SIEVE（Set of Indexes for Efficient Vector Exploration）。它构建一个针对已观测查询工作负载定制的索引集合，以便在内存预算与指定召回率下最大化期望吞吐量。每个候选索引被赋予收益——把它加入集合时的边际性能增益——以及内存代价，我们据此构建集合。这一做法本身并不新；新的是（1）如何估计收益与代价，以及（2）如何用该索引集合来服务查询。

首先，我们设计一个分析性的、与谓词形式无关的收益/代价模型，刻画索引大小、搜索时间与召回率之间的三维关系，从而能够找到满足特定召回率的最小（亦即最稀疏）图。由于每个索引更小，同一内存预算内容纳的索引更多，从而为更多谓词加速搜索。该模型基于经验观察以及已有的小世界网络理论 [4]。

其次，查询服务在给定某一召回率时动态选择搜索最快的索引。之所以需要这种查询时选择，是因为我们的索引可能相互重叠：一个查询可能可以由多个索引来服务。为做出最优选择，我们再次使用该模型来确定（1）使用哪个索引，以及（2）它的搜索参数设置。

**Difference from Existing Work.** SIEVE 与已有向量搜索工作有显著不同（表 1）。相对面向精确查询的物化视图选择（MV selection）[2, 70]、划分（partitioning）[53, 68] 与查询重写 [19, 20]，SIEVE 的优化明确把召回率纳入考虑，并执行理论驱动的索引调参（§4.2）以及动态的、感知召回率的服务（§5.2），以取得所期望的内存、速度与召回率权衡。

**Contributions.** 我们提出 SIEVE，一个用于过滤向量搜索的索引框架（§3），贡献如下：

- **Index Selection（索引选择）：** 我们引入一个三维代价模型，用于评估向量搜索策略的搜索速度、召回率与内存代价，并据此在有界内存下联合进行索引选择与参数化。（§4）
- **Query Serving（查询服务）：** 我们利用所导出的代价模型，得到一种动态搜索策略，在任意目标召回率下选择最高效的服务方法与参数设置。（§5）
- **Effective Filtered Vector Search（有效的过滤向量搜索）：** 我们通过实验表明，在多样的查询过滤器格式上，SIEVE 相对现有索引取得至多 8.06× 的加速，内存不到标准 HNSW 的 2.15×，并且只需要对历史工作负载有适度了解。（§7）

表 1 出现在本节版面中。图注原文：Comparison between SIEVE (ours) and other indexing methods for filtered vector search。译文：SIEVE（本文）与其他过滤向量搜索索引方法的比较。表头为 Approach、Query Selectivity（分 high / medium / low）、Complex Filters、Potential Weaknesses。单元格如下：

| Approach | high | medium | low | Complex Filters | Potential Weaknesses |
| --- | --- | --- | --- | --- | --- |
| Partition-Based [23, 39] | × | ✓ | ✓ | × | Restrictive filter format（过滤器格式受限） |
| Data Attr.-aware Graphs [21, 61, 66] | ✓ | ✓ | × | × | Requires limiting data attribute cardinality (<200)（需要限制数据属性基数，<200） |
| Intra-Search Filtering [44] | ✓ | ✓ | × | ✓ | Potentially excessive TTI (up to 219× of regular HNSW)（TTI 可能过高，至多达常规 HNSW 的 219×） |
| Exhaustive Indexing [31, 74] | ✓ | ✓ | ✓ | × | High memory cost, restrictive filter format（内存代价高，过滤器格式受限） |
| Index Collection (Ours, SIEVE) | ✓ | ✓ | ✓ | ✓ | Needs bounded extra memory and past workload (up to 2.15× of HNSW)（需要有界的额外内存以及历史工作负载，至多达 HNSW 的 2.15×） |

图 1 出现在本节版面中。图注原文：ANN vector search trade-offs: (Left) indexes can be built with varying recall/memory trade-offs. (Right) indexes can be over-searched to trade slower search for higher recall。译文：ANN 向量搜索的权衡：（左）索引可以按不同的召回率/内存权衡来构建；（右）可以对索引过度搜索，以更慢的搜索换取更高召回率。子图注：(a) Mem. vs. recall, 100K random vecs；(b) Time vs. recall, 100k random vecs。可读轴名包括 Recall、Index size (MB)、Search time (ms)。坐标刻度在抽取中粘连（如 0.70、1.00 与相邻数字连在一起），【抽取不清】。

## 2 MOTIVATION 动机

SIEVE 建立在 HNSW [33] 之上。HNSW 是一种高性能的无过滤向量索引 [12, 73]。我们说明 HNSW（§2.1），已有工作如何（并未有效地）把它扩展到过滤搜索（§2.2），以及我们为有效过滤搜索而构建并使用 HNSW 索引集合的想法（§2.3）。

### 2.1 HNSW Graph HNSW 图

HNSW 是一种基于图的向量索引 [33]，它结合小世界图 [4] 与跳表（skip-lists）[65] 的思想，形成多层图结构，用于在向量数据集上进行有效的相似性搜索。

**HNSW Graph Structure.** 一张 HNSW 图由多个分层的小世界图构成 [4]。最上层（入口层，entry layer）包含的向量最少，边较长，便于在向量空间中做远距离移动；最下层（基层，base layer）包含全部向量，边较短，表示局部邻域。HNSW 图通过逐个插入向量来构建：每个向量在每一层与若干邻居相连，由构建参数 \(M\) 控制。\(M\) 充当出度上限，并保证向量在每一层连接到其他相似向量。

**HNSW Search.** 给定查询向量后，各层自顶向下遍历：借助高层的长边走到含有相似数据向量的邻域，再借助低层的短边找出 top-\(k\) 的选择。算法 1 给出逐层搜索算法。

算法 1 的抽取文本把 Input / Output 也计为编号行。下列行号按正文引用对齐：正文所称第 6 行是邻居扩展（ACORN 在此过滤），第 13 行是并入 top-\(k\) 结果集之前（hnswlib 在此过滤）。

```
Algorithm 1: HNSW_SEARCH_LAYER
Input: query vector \(q\), enter points \(ep\), exploration factor \(ef\), layer \(l_c\)
Output: \(ef\) closest vectors to \(q\)
1  Initialize visited set \(V\), candidate set \(C\), top-\(ef\) set \(W\) to \(ep\);
2  while \(|C| > 0\) do
3    \(c \leftarrow\) extract nearest vector in \(C\) to \(q\)
4    \(f \leftarrow\) furthest vector in \(W\) to \(q\)
5    if \(dist(c,q) > dist(f,q)\): break
6    \(nbrs \leftarrow neighborhood(c)\) at layer \(l_c\)   // ACORN filters here
7    for each \(e \in nbrs\) do
8      if \(e \in V\): continue
9      \(V \leftarrow V \cup e\)
10     \(f \leftarrow\) furthest vector from \(W\) to \(q\)
11     if \(dist(e,q) < dist(f,q)\) or \(|W| < ef\): then
12       \(C \leftarrow C \cup e\)
13       \(W \leftarrow W \cup e\)   // hnswlib filters here
14     If \(|W| > ef\): remove furthest vector from \(W\) to \(q\)
15  Return \(W\).
```

译文：输入为查询向量 \(q\)、进入点（enter points）\(ep\)、探索因子 \(ef\)、层 \(l_c\)。输出为距离 \(q\) 最近的 \(ef\) 个向量。把已访问集合 \(V\)、候选集合 \(C\)、top-\(ef\) 集合 \(W\) 初始化为 \(ep\)。当 \(|C| > 0\) 时，取出 \(C\) 中距离 \(q\) 最近的向量 \(c\)，以及 \(W\) 中距离 \(q\) 最远的向量 \(f\)；若 \(dist(c,q) > dist(f,q)\) 则停止。取 \(c\) 在层 \(l_c\) 上的邻域为 \(nbrs\)（ACORN 在此处过滤）。对每个 \(e \in nbrs\)：若已访问则跳过，否则加入 \(V\)；再取 \(W\) 中距离 \(q\) 最远的向量 \(f\)；若 \(dist(e,q) < dist(f,q)\) 或 \(|W| < ef\)，则把 \(e\) 加入 \(C\) 与 \(W\)（hnswlib 在此处过滤）。若 \(|W| > ef\)，从 \(W\) 中移除距离 \(q\) 最远的向量。返回 \(W\)。

### 2.2 Existing Filtering Methods Underperform 现有过滤方法表现不佳

尽管最初的 HNSW 图方案并未考虑执行过滤向量搜索，已有若干基于 HNSW 的过滤搜索方法被提出。本节对这些方法作一概述。

**Post-Search Filtering.** 对于选择率为 \(sel\) 的过滤 top-\(k\) 查询，可以对图做过度搜索，以取得 top-\(k/sel\) 个向量。不匹配的结果被丢弃，并期望在 top-\(k/sel\) 的结果中仍保留 \(k\) 个：若不然，再执行一次 top-\(2k/sel\) 搜索，依此类推。

**Result-Set-Filtering.** hnswlib [40] 在 HNSW 搜索过程中、将候选加入 top-\(k\) 结果集之前评估查询过滤器（算法 1 第 13 行）。相对搜索后过滤，这样做有所改进，因为它在一次遍历中即返回 \(k\) 个满足条件的结果；然而每个候选仍有 \((1-sel)\) 的概率被过滤器拒绝、不能进入 top-\(k\) 集合。因此，召回率几乎不受影响，但搜索时间与选择率成反比（图 2a）。当 \(sel\) 较低、而预过滤搜索仍要面对很多点时（例如大规模数据集 [8]），它实际上仍然表现不佳。

脚注 1：具体而言，hnswlib、ACORN（以及我们的工作）都通过一种常用的、基于位图（bitmap）的过滤方法来实现过滤。该方法原则上可处理任意谓词：它为插入的向量分配 ID，再依据相对标量属性通过过滤器的向量 ID，计算一个二值映射 \(\mathrm{ID}\rightarrow\{0,1\}\)（例如经由外部关系数据库管理系统 RDBMS，§6）。

**Other Filter Application Methods.** ACORN [44] 在邻居扩展时施加过滤（算法 1 第 6 行），实际上是在 HNSW 图中、由满足条件的向量所诱导的子图上搜索。然而，子图诱导等价于删除边与节点。若子图过于稀疏 [41]，它可能失去有效搜索所需要的小世界性质，尤其是连通性 [67]；若仍按算法 1 原样搜索，可能导致过早停止以及低召回率。因此，ACORN 同时修改 HNSW 的构建与搜索，特别是扩展到 2 跳邻居，以避免子图稀疏。然而，即使 2 跳子图仍然稀疏，ACORN 也仍可能表现不佳。我们将通过实验表明（§7.2），结果集过滤有时优于 ACORN，有时则相反。

SIEVE 在其 HNSW 索引中采用结果集过滤，因为该方法无需专门的图构建即可适用，而专门构建可能带来过高的建索引时间（time-to-index, TTI，§7.3）。以下各节的讨论限于结果集过滤。不过，只需少量调整，SIEVE 也可以改用 ACORN 的过滤方式。

### 2.3 SIEVE’s Intuition for Faster Search SIEVE 实现更快搜索的直觉

现有基于 HNSW 的过滤方法在 “unhappy-middle” 这一档选择率上表现不佳。SIEVE 试图用由工作负载驱动的拟合来缓解这一点：在数据子集上拟合一个 HNSW（子）索引集合，使这些查询能够因其匹配点在子索引中足够稠密而得到有效服务。如 §1 所述，构建和使用 HNSW 图涉及速度、召回率与内存的权衡（图 1）；因此，SIEVE 需要同时决定构建并使用哪些索引，以及如何构建与使用。本节说明我们的直觉。

**Three-Dimensional Modeling.** 不失一般性，SIEVE 把召回率与内存视为约束，并以速度为优化目标。用户通常既有 ① 用于建索引的有界内存 [32, 53, 54]，也有 ② 目标召回率（例如服务等级目标 SLOs [49, 52]）。原文圈号抽取为 1○、2○。这不同于面向（精确）查询的物化视图选择（MV Selection），后者通常只受内存约束。SIEVE 的直觉是：借助理论驱动的建模，可以通过推理在不同目标召回率下索引应当如何构建（稍后说明），从而消掉召回率这一维。然后，SIEVE 可以使用已有方法，在有界内存下选择要构建哪些索引，以最大化服务速度。最后，在服务阶段，SIEVE 可以用类似的建模，在一个可能不同于构建时所设的新目标召回率下，确定使用哪些已构建的索引以及如何使用，从而得到最快的搜索。

**How to Build Indexes?** 每个子索引的内存大小与（1）被索引向量的数量，以及（2）控制密度的构建参数 \(M\)（§2.1）成线性关系。\(M\) 可以按不同的内存/召回率权衡来调节：更高的 \(M\) 会同时增大内存占用与召回率（因为密度提高），反之亦然（图 3a）。目标召回率实际上规定了每个索引在构建时可以使用的最低 \(M\)。

脚注 2：SIEVE 针对平均召回率进行优化；据我们所知，由于查询难度可以变化 [62]，并不存在能够保证绝对的、逐查询召回率的方法。

直观地说，更小的索引达到同一目标召回率所需的 \(M\) 更低。例如，相对 attr=D，图 2 中的 attr=C 以更低的 \(M\) 即可在平均召回率 \(x\) 下服务查询（图 3b）。我们在 §4.2 中说明这一点。

**What Indexes to Build?** SIEVE 旨在构建这样的子索引：它们能够高效服务那些已观测到的、替代方法（例如暴力最近邻，brute-force KNN）效率不高的查询，从而取得边际收益。假设我们有图 2b 中的基座 HNSW 索引：尽管构建子索引（attr=D）对其对应的过滤查询有好处，但 attr=D 的选择率很高（50%），基座索引通过结果集过滤就已经能足够快地服务它。相比之下，子索引（attr=AorB）的边际收益很高：它服务（attr=AorB）显著快于基座索引（图 2）。抽取文本写作 AorB，表示属性 A 或 B。子索引也可以服务并非精确匹配的过滤查询：例如，（attr=AorB）也可以有效服务（attr=A），而 attr=A 在该子索引中的选择率足够高（50%）。这扩展了（attr=AorB）这类子索引的效用，使其也能用于其他过滤器。我们在 §4.3 描述 SIEVE 的索引选择。

**How to Serve Queries?** 在用已构建的索引集合服务查询时，SIEVE 在索引搜索与暴力 KNN 之间做出选择。控制 HNSW 索引之搜索速度/召回率权衡的一个关键参数是搜索探索因子 \(sef\)（算法 1）：更高的 \(sef\)（对图进行过度搜索）以更低的速度换取更高的召回率（图 3c）。若服务阶段的目标召回率高于构建时所假定的召回率，SIEVE 就需要调节 \(sef\)。与 \(M\) 类似，SIEVE 希望索引搜索使用尽可能低的 \(sef\)，而更小的子索引达到同一目标所需的 \(sef\) 也更小（图 3d）。随后，在得到最佳索引与 \(sef\) 之后，SIEVE 评估回退到暴力 KNN 是否更快（例如 \(sef > 30\)，图 3c）。暴力 KNN 的召回率始终为完美。我们在 §5.2 描述 SIEVE 的服务策略。

图 2 出现在本节版面中。图注原文：SIEVE aims to build subindexes with high relative speedup and applicability to many queries (e.g., attr=AorB)。译文：SIEVE 旨在构建相对加速高、且能用于许多查询的子索引（例如 attr=AorB）。子图注：(a) QPS vs. sel. on 100K-vector dataset；(b) Example Candidate Subindexes。可读标签包括 Filter Selectivity、QPS @ 0.9+ recall、Filtered Search in base HNSW、Brute-force Pre-Filter Search、Subindex Search (our goal)，以及 attr=D、attr=C、attr=AorB。子图 (b) 可读标签包括 Vectors、attr、A、B、C、D、100K vectors、10K vecs、30K vecs、50K vecs，以及 attr=AorB、attr=C、attr=D。各框与这些规模、属性标注之间的版面连线【抽取不清】。坐标刻度在抽取中粘连，【抽取不清】。

图 3 出现在本节版面中。图注原文：\(M\) and \(sef\) respectively increase the memory size and search time (Left), but smaller graphs require smaller \(M\) and \(sef\) values to reach the same recall (Right)。译文：\(M\) 与 \(sef\) 分别增大内存占用和搜索时间（左），但更小的图达到同一召回率所需的 \(M\) 与 \(sef\) 也更小（右）。子图注：(a) Mem. vs. \(M\), 100K vectors；(b) Recall vs. \(M\), random vectors；(c) speed vs. \(sef\), 100K vecs, 0.2 sel；(d) Recall vs. \(sef\), random vectors。可读轴名与标注包括 HNSW \(M\) parameter、Memory (MB)、\(M\) to reach 0.9 average recall、Index vectors、Brute-force、HNSW \(sef\) parameter、Avg. time (ms)、\(sef\) to reach 0.9 average recall。纵轴可见 102、103、104、105，上标是否为 \(10^{2}\) 至 \(10^{5}\)【抽取不清】。其余坐标刻度在抽取中粘连，【抽取不清】。
