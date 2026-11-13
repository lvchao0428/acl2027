# SAGE: Structure Aware Graph Expansion for Retrieval of Heterogeneous Data

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`SPARK_arXiv2602.16964.pdf`。

## Abstract 摘要

面向异构语料的检索增强问答，需要贯通文本、表格与图节点的相连证据。实体级知识图谱（knowledge graphs）能够支持结构化访问，但构建与维护成本高，而且在查询时遍历效率低。相比之下，标准的检索器–阅读器（retriever-reader）流水线对各自独立切分的文本做扁平相似度搜索，会错过跨模态的多跳证据链。我们提出 SAGE（Structure Aware Graph Expansion）框架。它 (i) 离线利用元数据驱动的相似度，并配合基于百分位的剪枝，构建块级（chunk-level）图；(ii) 在线检索时，先运行初始基线检索器得到 k 个种子块，扩展其一跳邻居，再用 dense+sparse 检索过滤这些邻居，选出额外的 k′ 个块。对于隐式的跨模态语料，我们用混合 dense+sparse 检索来实例化初始检索器；对于显式模式图，则使用 SPARK（Structure Aware Planning Agent for Retrieval over Knowledge Graphs）这一智能体检索器。在 OTT-QA 与 STaRK 上，SAGE 相对基线将检索召回分别提高 5.7 与 8.5 个百分点。¹

¹ 代码见 https://github.com/CoRAL-ASU/sage。

## 1 Introduction 引言

检索增强生成（retrieval-augmented generation, RAG）（Lewis et al., 2020）把大语言模型（large language models）锚定在外部知识上，已成为面向领域特定语料进行问答的标准范式。大多数 RAG 系统依赖扁平检索（flat retrieval）：用稀疏、稠密或混合相似度搜索，检索各自独立索引的文本块（Mandikal and Mooney, 2024; Arabzadeh et al., 2021; Zhang et al., 2024; Chen et al., 2022）。这一设计对简单的、以文本为中心的查询是有效的，但难以对包含文档、表格与结构化元数据的异构数据进行复杂推理。

图 1：SAGE【抽取不清】的 seed→expand 检索示意图：从一块初始相关块出发，图扩展检索到一个相连邻居，其中包含扁平检索未能浮现的、缺失的电影/导演证据。

扁平检索把每个块独立对待，忽略了常常把相关证据跨文档或跨模态连接起来的结构依赖。因此，那些在嵌入空间中与查询仅弱相关、但在结构上与相关内容相连的中间证据经常被遗漏。例如，要回答关于一部由 Trevor Eyster 主演的电视剧及其原著的问题，就需要把演职员信息、改编元数据与作者细节连接起来；这些连接不太可能仅靠相似度搜索恢复。

为应对这些局限，近期工作用基于图的表示来增强 RAG，以建模异构数据之间的关系，并支持多跳检索（Edge et al., 2024a; Jimenez Gutierrez et al., 2024; Mavromatis and Karypis, 2024）。先前方法分为两类：知识图谱（knowledge graphs, KGs）与相似度图（similarity graphs）。知识图谱把结构化知识编码为带类型的实体–关系三元组，并通过遍历或查询语言进行精确的符号推理，例如 Cypher（Francis et al., 2018）与 SPARQL（201, 2013）；但它们需要代价高昂的实体抽取与模式对齐，因而适用于模式稳定的领域。相似度图用由嵌入相似度诱导的边来表示文本块、表格片段或半结构化节点，无需显式实体抽取，就能自然地支持异构数据。

图 2：SAGE 概览。Offline：我们把文档与表格按语义切分为节点，并用元数据驱动的相似度（例如 title、topic、content、entities）配合基于百分位的剪枝来建边。Online：基线检索器返回 k 个种子节点；我们在离线图上扩展到 n 个一跳邻居，再重排序以选出额外的 k′ 个节点，得到规模为 k+k′ 的最终上下文。

然而，其有效性关键取决于边如何构建：过密的图会引入虚假邻居，过稀的图则会妨碍多跳推理。节点粒度也会影响表达能力、连通性与计算成本。实体级图（entity-level graphs）捕捉细粒度实体，能支持事实型查询，但难以处理上下文型或聚合型问题。社区级图（community-level graphs）把实体或文档聚成簇，提高了可扩展性，但降低了细节。这些权衡促使我们采用在粒度、可扩展性与检索效果之间取得平衡的中间表示。

我们引入块级图来填补这一空白：在语义连贯的单元上做结构感知扩展，从而提高召回。我们并非检索许多彼此独立的块，而是先选出一小批种子节点，再经由图遍历加以扩展，从而浮现那些与查询的相似度可能较弱、但通过文档结构、元数据或共享上下文而紧密相连的证据。每个节点表示一段文本或表格片段，在不要求显式实体抽取的情况下保持局部连贯。该图离线构建，并且与具体检索器无关，只增加极少的运行时开销。其紧凑的邻域遍历，使异构语料上的高效多跳推理与可靠证据聚合成为可能。我们的贡献如下：

- 我们提出 SAGE，一种结构感知检索框架（structure-aware retrieval framework）。它用块级图扩展增强扁平检索，从而在与现有检索器保持兼容的同时，支持邻域感知推理。
- 通过相似度诱导的图扩展（similarity-induced graph expansion），SAGE 在固定预算下相对强扁平混合基线持续提高召回（OTT-QA 上 +5.7，STaRK 上 +8.5），在隐式多跳查询与跨模态查询上增益最大。
- 对于显式模式图，我们进一步提出 SPARK，一种执行模式约束扩展（schema-constrained expansion）的检索智能体。它在遍历时强制结构有效性，并优于朴素的稠密扩展。

## 2 SAGE Approach SAGE 方法

给定表示为图 G = (V, E) 的语料，节点内容为 text(v)，可选元数据为 meta(v)。对查询 q，检索目标是返回证据节点的排序列表 Rk(q)，使相关证据出现在 top-k 位置。

### 2.1 Offline Graph Construction 离线图构建

我们在文档块与表格片段之上构建异构图 G（用于文档图），或者保留原生的实体–关系模式（用于知识图谱）。图构建过程与具体数据集无关，并在查询时刻之前离线进行。

#### A. Data Processing and Node Creation 数据处理与节点创建

1. Semantic chunking of documents 文档的语义切块。我们把每篇文档切分为句子序列，并用句子编码器（Reimers and Gurevych, 2019）对重叠的上下文窗口 wi = [si−1, si, si+1]（边界处截断）进行嵌入。令 hi 表示 wi 的嵌入。相邻窗口之间的余弦相似度计算为 si = cos(hi, hi+1)。我们在局部连贯性下降的下标处引入边界，对 {si} 使用基于百分位的规则：令 θ = Percentile20({si})（等价于选出前 80% 的 “drop” 位置），并在所有满足 si ≤ θ 的 i 处切分。切块之后，我们使用大语言模型（large language model, LLM）为每个块生成元数据（topic、title 与 entities），供下游图构建使用。

2. Table segmentation 表格切分。我们使用 LLM 生成简短的表格描述与列描述；它们成为表格块元数据的一部分。对每张表，我们保留表题/描述、列标题与列描述，并且每个片段保留 5–10 行，以便在把片段控制在有界上下文规模内的同时保留纵向上下文。

3. Semi-structured nodes 半结构化节点。对于半结构化节点，我们把每个对象视为一个 “chunk”，并从其文本字段（例如 name/title 以及长文本描述）构造元数据。这些元数据字段用于建立下游的图连通性。

#### B. Edge creation 建边

经由元数据相似度构建图。我们使用 Sentence-Transformer 编码器嵌入这些元数据字段，并依据特定于模态的相似度信号连接节点：(1) Document–Document 边捕捉 topic–topic 相似度、content–content 相似度以及实体重叠；(2) Table–Table 边捕捉 column–column 相似度、title–title 相似度以及实体重叠；(3) Table–Document 边捕捉 content–column 相似度、topic–title 相似度以及实体重叠；(4) Semi-Structured Chunk 边经由对象描述性元数据上的相似度把对象连接起来。

仅当一条相似度边的元数据相似度超过经验分布的第 95 百分位时，我们才保留该边；这样做维持了稀疏性，并减少稠密邻域中的噪声。我们还保留父子链接与结构链接（例如来自同一来源的块），并在可得时保留显式的模式边。图 2 展示了由此得到的图结构。

用于遍历的边元数据。边存储轻量元数据，用以引导受控的图遍历。Table–table 边记录可连接的列名，document–document 边记录共享实体与置信度分数，table–document 边记录共享实体，并在可得时记录行或列引用。这些元数据使多跳推理能够优先考虑与查询实体一致、或满足结构约束的邻居。

### 2.2 Online Retrieval 在线检索

在查询时，我们采用两阶段检索策略：(i) 初始基线检索，以获得 k 个种子节点；(ii) 基于图的邻居扩展与剪枝，以选出额外的 k′ 个节点。由于结构性质不同，文档图与知识图谱所使用的基线检索方法并不相同：混合稀疏–稠密检索适用于 OTT-QA 的文本/表格数据，而 STaRK 中模式丰富的知识图谱则需要 SPARK（如表 6 所示，混合检索在 STaRK 上表现较差）。

#### A. Initial baseline retrieval 初始基线检索

1. Similarity graphs 相似度图。对于文档图（表格与文本块），我们使用混合稀疏–稠密检索基线。我们计算 BM25（Robertson et al., 2009）分数以做词法匹配，并在稠密嵌入上计算余弦相似度以做语义匹配，然后合并这些分数，选出 top-k 种子节点。当块含有足够的文本内容、且相关性可以由表层语义相似度判定时，该方法效果良好。

2. Semi-Structured Knowledge Bases (SKBs) 半结构化知识库。对于带有显式模式的半结构化知识库（semi-structured knowledge bases, SKBs，即节点关联有文本字段的图），BM25 与余弦相似度作用有限。它们忽略边类型与带类型的关系，无法沿多跳路径进行推理，并且表现出类型偏差（type bias），常常检索到同一类型的节点，而不是查询所要求的正确实体。

图 3：SKB 基线检索：问题与模式元数据引导一个 LLM 智能体生成检索计划，将 HNSW 语义搜索与 Cypher 符号查询交错执行。

为此，我们提出 SPARK，一种面向 SKB 检索的、基于 LLM 的智能体。给定一个问题，该智能体可以访问实体模式、关系以及两种检索工具。它生成一个多步计划，在以下两者之间交替：(1) Semantic Candidate Generation（语义候选生成）：基于文本相似度与描述属性，通过 Hierarchical Navigable Small World（HNSW）（Malkov and Yashunin, 2018）搜索来检索节点。这使得匹配更加灵活，即使查询关键词并未显式出现，智能体也能够识别语义上相关的节点。(2) Structural Expansion（结构扩展）：在 Neo4j（Neo4j, Inc., 2026）中用 Cypher 查询遍历边，并受实体类型与关系约束，以确保多跳结构的正确性。这保证被检索到的节点满足显式的关系约束与类型约束，而简单的关键词方法或基于相似度的方法无法强制这些约束。

我们执行所生成的计划，并把检索到的 top-k 节点作为种子返回。当该计划没有返回结果时，回退到 BM25 与余弦相似度，以保证稳健性；因为对某些问题，智能体可能无法生成正确的多步查询，或者会遇到文本内容稀疏的节点。这一组合在模式感知遍历的精度与传统检索方法的覆盖范围之间取得平衡。

#### B. Graph-based neighbor expansion and pruning 基于图的邻居扩展与剪枝

无论采用哪种基线，我们对文档与知识图谱都应用统一的图扩展策略。SPARK 只是一种专用于模式丰富知识图谱的可能种子检索器；SAGE 扩展算子本身在所有数据集与所有种子检索器上保持不变。给定初始检索得到的 k 个种子节点：(1) Neighbor Expansion（邻居扩展）：从预先构建的图 G 中收集这 k 个种子的全部一跳邻居，得到 n 个候选节点；(2) Neighbor Pruning（邻居剪枝）：依据与查询的 BM25 以及稠密嵌入相似度，对这 n 个候选重新排序，并选出 top-k′ 个邻居；(3) Final Context（最终上下文）：返回原来的 k 个种子与这 k′ 个邻居的并集，共计 k+k′ 个节点。

Listing 1：统一的 k+k′ 检索（伪代码）

```
Input : query q , budgets k , k’ , baseline retriever BL , graph G
S = TopK ( BL ( q ) , k )
N = OneHopNeighbors (G , S )
R = TopK ( BM25DenseRank (q , N ) , k’ )
Return Union (S , R )
```

该方法比在运行时计算完整的节点到节点相似度更加高效。预先计算的连接能够捕捉起桥接作用的证据，通过聚焦相关邻居来降低噪声，保留多跳上下文，并且可以扩展到大规模图，而无需穷尽的两两比较。
