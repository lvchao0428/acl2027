原文件名：SPARK_arXiv2602.16964.pdf

原标题：SAGE: Structure Aware Graph Expansion for Retrieval of Heterogeneous Data

中文标题：SAGE：面向异构数据检索的结构感知图扩展

作者：Prasham Titiya^{1∗}、Rohit Khoja^{1∗}、Tomer Wolfson^{2†}、Vivek Gupta^{1†}、Dan Roth^{2}

单位：^{1} Arizona State University；^{2} University of Pennsylvania

∗同等贡献（共同第一作者）；†同等贡献（共同第二作者）

arXiv:2602.16964v1 [cs.IR] 18 Feb 2026

<!-- 原 PDF 第 1 页 -->

# SAGE：面向异构数据检索的结构感知图扩展

## 摘要

异构语料上的检索增强问答，需要把文本、表格和图节点中的证据连起来。实体级知识图谱能够支持结构化访问，但构建和维护代价高，查询时遍历也不高效。相比之下，标准的检索器–阅读器流水线对各自独立切分的文本做扁平相似度搜索，会错过跨模态的多跳证据链。我们提出 SAGE（Structure Aware Graph Expansion，结构感知图扩展）框架：（i）离线阶段用元数据驱动的相似度，并按分位数剪枝，构建块级图；（ii）在线阶段先运行初始基线检索器，得到 \(k\) 个种子块，扩展其一跳邻居，再用稠密+稀疏检索过滤这些邻居，选出额外的 \(k'\) 个块。对于隐式跨模态语料，初始检索器实例化为混合稠密+稀疏检索；对于显式模式图，则使用智能体检索器 SPARK（Structure Aware Planning Agent for Retrieval over Knowledge Graphs，面向知识图谱检索的结构感知规划智能体）。在 OTT-QA 和 STaRK 上，SAGE 相对基线将检索召回率分别提高 5.7 和 8.5 个百分点。^1

^1 代码见 https://github.com/CoRAL-ASU/sage

## 1 引言

检索增强生成（retrieval-augmented generation, RAG）（Lewis et al., 2020）把大语言模型锚定在外部知识上，已成为面向领域语料的问答标准范式。多数 RAG 系统依赖扁平检索：对独立建索引的文本块，用稀疏、稠密或混合相似度搜索进行检索（Mandikal and Mooney, 2024; Arabzadeh et al., 2021; Zhang et al., 2024; Chen et al., 2022）。这种设计对简单的以文本为中心的查询有效，但难以处理同时包含文档、表格和结构化元数据的异构数据上的复杂推理。

**图 1：** SAGE 的种子→扩展检索示意：从一块初始相关文本出发，图扩展找回一块相连的邻居，其中包含扁平检索未能露出的缺失电影/导演证据。（图题原文抽取为 “SAGE â ˘A´Zs seed→expand retrieval”，撇号乱码，此处按 SAGE 的种子→扩展检索理解。）

扁平检索把每个块当作彼此独立，忽略了常常把相关证据跨文档或跨模态连在一起的结构依赖。因此，那些在嵌入空间里与查询关系较弱、但在结构上与相关内容相连的中间证据，经常被漏掉。例如，要回答一部由 Trevor Eyster 主演的电视剧及其原著的问题，就需要把演员信息、改编元数据和作者细节连起来；这些连接单靠相似度搜索很难找回。

为应对这些局限，近期工作用基于图的表示增强 RAG，以刻画异构数据之间的关系并支持多跳检索（Edge et al., 2024a; Jimenez Gutierrez et al., 2024; Mavromatis and Karypis, 2024）。已有方法大致分为两类：知识图谱（knowledge graph, KG）和相似度图。知识图谱把结构化知识编码为带类型的实体–关系三元组，并可通过遍历或 Cypher（Francis et al., 2018）、SPARQL（201, 2013）等查询语言做精确的符号推理，但需要昂贵的实体抽取和模式对齐，因而更适合模式稳定的领域。相似度图则把文本块、表格片段或半结构化节点表示为节点，边由嵌入相似度诱导，天然支持异构数据，而不必显式抽取实体。

<!-- 原 PDF 第 2 页 -->

**图 2：** SAGE 总览。离线：把文档和表格按语义切成节点，并用元数据驱动的相似度（例如标题、主题、内容、实体）连边，再按分位数剪枝。在线：基线检索器返回 \(k\) 个种子节点，在离线图上扩展到 \(n\) 个一跳邻居，再重排序选出额外的 \(k'\) 个节点，最终上下文为 \(k+k'\)。

然而，其效果关键取决于边如何构建：图过密会引入虚假邻居，图过稀则妨碍多跳推理。节点粒度也会影响表达能力、连通性和计算成本。实体级图能抓住细粒度实体，适合事实型查询，但难以应对需要上下文或聚合的问题。社区级图把实体或文档聚成簇，可扩展性更好，但细节更少。这些权衡促使我们采用介于二者之间的表示，以平衡粒度、可扩展性和检索效果。

我们用块级图填补这一空缺：在语义连贯的单元上做结构感知扩展，从而提高召回。我们不是一次检索许多彼此独立的块，而是先选出一小集种子节点，再经图遍历扩展，把那些与查询相似度可能较弱、但通过文档结构、元数据或共享上下文紧密相连的证据找出来。每个节点是一段文本或表格，既保留局部连贯性，又不需要显式实体抽取。图在离线构建，与具体检索器无关，运行时开销很小。紧凑的邻域遍历使多跳推理更高效，也能在异构语料上可靠地聚合证据。我们的贡献如下：

- 我们提出 SAGE，一种结构感知检索框架。它用块级图扩展增强扁平检索，从而支持邻居感知的推理，并仍与现有检索器兼容。
- 通过相似度诱导的图扩展，在固定预算下，SAGE 相对强扁平混合基线稳定提高召回（OTT-QA 上 +5.7，STaRK 上 +8.5），在隐式多跳和跨模态查询上增益最大。
- 针对显式模式图，我们进一步提出 SPARK，一种检索智能体。它做受模式约束的扩展，在遍历时强制结构合法，并优于朴素的稠密扩展。

## 2 SAGE 方法

给定表示为图 \(G = (V, E)\) 的语料，节点内容为 \(\mathrm{text}(v)\)，可选元数据为 \(\mathrm{meta}(v)\)。对查询 \(q\) 的检索目标，是返回一个证据节点的排序列表 \(R_k(q)\)，使相关证据出现在前 \(k\) 个位置。

### 2.1 离线图构建

我们在文档块和表格片段上构建异构图 \(G\)（文档图），或者保留原生的实体–关系模式（知识图谱）。图构建过程与具体数据集无关，并在查询之前离线完成。

**A. 数据处理与节点创建**

**1. 文档的语义分块。** 我们把每篇文档切成句子序列，并用句子编码器（Reimers and Gurevych, 2019）嵌入重叠的上下文窗口（边界处截断）：

\[
w_i = [s_{i-1}, s_i, s_{i+1}]
\]

记 \(h_i\) 为 \(w_i\) 的嵌入。我们计算相邻窗口的余弦相似度

<!-- 原 PDF 第 3 页 -->

\[
s_i = \cos(h_i, h_{i+1}).
\]

在局部连贯性下降的下标处引入边界。规则基于 \(\{s_i\}\) 的分位数：令 \(\theta = \mathrm{Percentile}_{20}(\{s_i\})\)（等价于选取跌幅最大的前 80% 位置），在所有满足 \(s_i \le \theta\) 的 \(i\) 处切开。分块之后，我们用大语言模型为每个块生成元数据（主题、标题和实体），供后续建图使用。

**2. 表格切分。** 我们用大语言模型生成简短的表格描述和列描述，这些成为表格块元数据的一部分。对每张表，我们保留表标题/描述、列名和列描述，并且每个片段保留 5–10 行，以便在片段上下文大小有界的前提下保留纵向上下文。

**3. 半结构化节点。** 对半结构化节点，我们把每个对象当作一个“块”，并从其文本字段（例如名称/标题和长描述）构造元数据。这些元数据字段用于建立下游的图连接。

**B. 建边**

**经由元数据相似度的图构建。** 我们用 Sentence-Transformer 编码器嵌入这些元数据字段，并按模态特定的相似度信号连接节点：（1）文档–文档边捕捉主题–主题相似度、内容–内容相似度以及实体重叠；（2）表–表边捕捉列–列相似度、标题–标题相似度以及实体重叠；（3）表–文档边捕捉内容–列相似度、主题–标题相似度以及实体重叠；（4）半结构化块的边，通过对象描述性元数据上的相似度把对象连起来。

仅当某条相似度边的元数据相似度超过经验分布的第 95 百分位时，我们才保留它。这样可以保持稀疏，并减少稠密邻域中的噪声。我们还保留父子/结构链接（例如来自同一来源的块），并在可用时保留显式模式边。图 2 展示了所得的图结构。

**供遍历使用的边元数据。** 边存储轻量元数据，以引导受控的图遍历。表–表边记录可连接的列名；文档–文档边记录共享实体和置信度；表–文档边记录共享实体，并在可用时记录行或列引用。这些元数据使多跳推理能够优先选择与查询实体对齐、或满足结构约束的邻居。

### 2.2 在线检索

查询时，我们采用两阶段检索：（i）初始基线检索，得到 \(k\) 个种子节点；（ii）基于图的邻居扩展与剪枝，选出额外的 \(k'\) 个节点。由于文档图和知识图谱的结构性质不同，基线检索方法也不同：混合稀疏–稠密检索适合 OTT-QA 的文本/表格数据，而 STaRK 上模式丰富的知识图谱需要 SPARK（混合检索在 STaRK 上表现较差，见表 6）。

**A. 初始基线检索。**

**1. 相似度图。** 对文档图（表格和文本块），我们使用混合稀疏–稠密检索基线。我们计算 BM25（Robertson et al., 2009）分数做词汇匹配，并在稠密嵌入上计算余弦相似度做语义匹配，再把这些分数合并，选出前 \(k\) 个种子节点。当块含有足够的文本内容、且相关性可以由表层语义相似度判定时，这一方法效果良好。

**2. 半结构化知识库（semi-structured knowledge base, SKB）。** 对带显式模式的半结构化知识库（即节点带有文本字段的图），BM25 和余弦相似度能力有限。它们忽略边类型和带类型的关系，不能在多跳路径上推理，并且存在类型偏差：往往检索到同一类型的节点，而不是查询所要求的正确实体。

**图 3：** SKB 基线检索：问题和模式元数据引导大语言模型智能体生成检索计划，把 HNSW 语义搜索与 Cypher 符号查询交织在一起。

<!-- 原 PDF 第 4 页 -->

为此，我们提出 SPARK，一种面向 SKB 检索的基于大语言模型的智能体。给定问题，智能体可以访问实体模式、关系以及两种检索工具。它生成一个多步计划，在下列步骤之间交替：（1）**语义候选生成**：基于文本相似度和描述属性，用层次化可导航小世界图（Hierarchical Navigable Small World, HNSW）（Malkov and Yashunin, 2018）搜索检索节点。这样可以灵活匹配，即使查询关键词并未显式出现，智能体仍能识别语义相关的节点。（2）**结构扩展**：在 Neo4j（Neo4j, Inc., 2026）中用 Cypher 查询遍历边，并受实体类型和关系约束，以保证多跳结构正确。这保证检索到的节点满足显式的关系和类型约束，而简单的关键词或基于相似度的方法无法强制这些约束。

我们执行生成的计划，并把检索到的前 \(k\) 个节点作为种子返回。当计划没有返回结果时，回退到 BM25 和余弦相似度，以保证稳健性，因为智能体可能对某些问题生成不正确的多步查询，或遇到文本内容稀疏的节点。这一组合在模式感知遍历的精度与传统检索方法的覆盖之间取得平衡。

**B. 基于图的邻居扩展与剪枝。** 无论基线如何，我们对文档和知识图谱都使用统一的图扩展策略。SPARK 只是面向模式丰富知识图谱的一种可能的种子检索器；SAGE 扩展算子本身在所有数据集和种子检索器上保持不变。给定初始检索得到的 \(k\) 个种子节点：（1）**邻居扩展**：从预先构建的图 \(G\) 中收集 \(k\) 个种子的全部一跳邻居，得到 \(n\) 个候选节点；（2）**邻居剪枝**：用相对于查询的 BM25 和稠密嵌入相似度对 \(n\) 个候选重排序，选出前 \(k'\) 个邻居；（3）**最终上下文**：返回原来的 \(k\) 个种子与 \(k'\) 个邻居的并集，共 \(k+k'\) 个节点。

**代码清单 1：** 统一的 \(k+k'\) 检索（伪代码）

```
输入：查询 q，预算 k、k'，基线检索器 BL，图 G
S = TopK(BL(q), k)
N = OneHopNeighbors(G, S)
R = TopK(BM25DenseRank(q, N), k')
返回 Union(S, R)
```

这一做法比在运行时计算全部节点对相似度更高效。预先计算的连接能抓住桥接证据，通过聚焦相关邻居来降低噪声，保留多跳上下文，并且可以扩展到大图，而不必做穷尽的两两比较。

## 3 实验

**数据集。** 我们在 OTT-QA 和 STaRK（Wu et al., 2024b）上评估。OTT-QA 源自 Wikipedia，同时包含文本段落和表格，每张表原本链接到一组文档。我们用开发集构建图，并从头重建全部连接，而不使用预定义链接。STaRK 包含三个领域的半结构化知识图谱：AMAZON（产品推荐，节点类型有限，但文本内容丰富）、MAG（关于论文和作者的学术引用，含一跳和两跳推理）以及 PRIME（生物医学知识，关系结构稠密，所有节点都可作为答案）。我们只在文本描述丰富的节点之间添加相似度边（例如产品、论文和生物医学实体），文本极少的原子实体则通过词汇 Cypher 匹配处理。表 1 汇总了所得的图统计。

每个 STaRK 子集都提供合成与人工评估划分。合成查询由四步流水线生成：把关系模板与大语言模型抽取的属性结合起来，产生多样的多跳问题，并带有经过核验的标准答案；人工查询则反映真实的风格、歧义和语言变异。

| 数据集 | 节点数 | 节点类型数 | 边数 | 边类型数 |
| --- | ---: | ---: | ---: | ---: |
| OTT-QA | 22,886 | 2 | 751,836 | 3 |
| STaRK AMAZON | 13,920,204 | 2 | 40,876,246 | 4 |
| MAG | 1,872,968 | 4 | 36,853,636 | 5 |
| PRIME | 129,375 | 10 | 9,825,282 | 19 |

**表 1：** 实验所用数据集概览。节点数和边数是图中的总数。节点类型数和边类型数表示模式的多样性。

这些数据集代表异构数据的两种互补情形。在我们的 OTT-QA 设定中，结构是隐式的：文本块与表格块之间的链接由内容相似度和元数据重叠诱导，而不是预定义关系。相比之下，STaRK 提供显式结构，带类型的实体和关系遵循固定模式。这一对照使我们能够评估 SAGE 是否会按底层拓扑调整其检索算子。

<!-- 原 PDF 第 5 页 -->

节点类型与边类型的更多细节见附录 A。

**OTT-QA 的基线。** 先前的 OTT-QA 工作主要针对表级检索，例如 CRAFT（Singh et al., 2025）和 OTTeR（Huang et al., 2022），而不是块级检索。许多方法还依赖预定义的表–文档链接，包括 COS（Ma et al., 2023）、RINK（Park et al., 2023）、CARP（Zhong et al., 2022）以及 Dual Reader-Parser（Chen et al., 2020）。忽略这些链接的方法采用了不同设定：ARM（Chen et al., 2025b）采用黄金集评估，而 CORE（Ma et al., 2022）试图重建这些链接，因而无法直接比较。扩展基线（Extended Baseline, BL）在不做基于图的扩展的情况下，直接检索同样数量的块。

**STaRK 的基线。** 在 STaRK 上，我们与稠密检索器（ada-002、multi-ada-002、DPR（Karpukhin et al., 2020））、稀疏词汇基线（BM25），以及基于图的推理方法 QA-GNN（Yasunaga et al., 2021）比较。混合检索方法包括 4StepFocus（Boer et al., 2024）和 FocusedR（Boer et al., 2025），它们把向量搜索与基于大语言模型的三元组抽取及迭代细化结合起来。查询扩展方法（HyDE（Gao et al., 2023）、AGR（Chen et al., 2024）、RAR（Shen et al., 2024）、KAR（Xia et al., 2024））利用知识图谱或大语言模型得到的信号改写查询。智能体系统包括 ReACT（Yao et al., 2022），它把推理与检索交织在一起；以及 Reflexion（Shinn et al., 2023），它加入情景记忆以便迭代改进。经过微调的半结构化检索器，如 mFAR（Li et al., 2024a）和 MoR（Lei et al., 2025），会调整字段权重，或把规划与图遍历结合起来；AvaTaR（Wu et al., 2024a）则通过基于对比比较器的细化，以及对过往失败的记忆，来优化会使用工具的智能体。我们将 AvaTaR 归为微调方法。

**评估指标。** 对 OTT-QA，检索用 Recall@\(k\) 衡量，即检索到多少相关段落。对 STaRK，我们虽然聚焦召回，仍报告原论文的标准指标：Hit@1、Hit@5、Recall@20 和 MRR，以同时刻画排序质量与所检索知识的覆盖。

### 3.1 OTT-QA：混合文本–表格结果

**基于图的检索在所有检索规模上都提高 Recall@\(k\)。** 基于图的检索在所有检索规模上都稳定提高 Recall@\(k\)（图 4）。从块级图加入一跳邻居后，每一个 \(k\) 上检索到的相关项都增加，从很小的检索集（\(k \approx 2\)）到更大的集合（\(k = 100\)）。这说明该图能有效露出仅靠扁平相似度检索无法抓住的额外相关节点。

**图 4：** OTT-QA 检索的 Recall@\(k\)（%，越高越好）。BL（Baseline，基线）是结合 BM25 与稠密嵌入的扁平混合检索器。BL+Graph 用 BL 检索 \(k_1\) 个种子，并从诱导图加入 \(k_2\) 个一跳邻居（\(k = k_1 + k_2\)）；扩展 BL 则直接用 BL 检索 \(k\) 个项。箭头标注每个 \(k\) 处的绝对增益。

**图的影响在较小检索集上更大。** 图的影响在较小检索集上尤其明显。例如，\(k = 20\) 时召回提高 5.7 个百分点，而 \(k = 100\) 时为 2.8 个百分点，说明检索项越少，相对改进越大。这突出表明：检索受约束时，图中的结构连接最为有益，使系统能高效识别否则会被漏掉的相关邻居。

**元数据对建图的影响。** 我们分析元数据相似度以指导建图。表–表对的标题相似度与描述相似度强相关（0.846，表 17），文档–文档对在主题相似度与内容相似度上对齐（0.650，表 18）。跨模态的文档–表相关介于 0.517 到 0.691（表 19）。这些模式表明，沿某一元数据维度的相似度往往能预测其他维度的相似度，有助于形成连贯的图邻域。

相似度分布大体呈钟形，并带有高端尾部，因而覆盖面广，同时强调强相关的块。因为大多数块只含一个实体，实体重叠成为关键桥梁：共享同一实体的块可以把原本不同的主题连起来。保留相似度最高 5% 的分位数剪枝，能保住这些有意义的链接，又不会使图过密。更多分布

<!-- 原 PDF 第 6 页 -->

与相关分析见附录 B。

**表 2：** 全部 STaRK 数据集（AMAZON、MAG、PRIME）上，人工查询与合成查询的 Recall@20。非微调方法中的最高值加粗，次高值加下划线。注：FocusedR、4StepFocus、mFAR 和 MoR 只报告合成划分上的结果；其论文或发布产物中没有人工划分的结果。样本量：AMAZON 人工 \(n = 81\)、合成 \(n = 1638\)；MAG 人工 \(n = 84\)、合成 \(n = 2664\)；PRIME 人工 \(n = 98\)、合成 \(n = 2801\)。

| 类别 | 方法 | AMAZON 人工 | AMAZON 合成 | MAG 人工 | MAG 合成 | PRIME 人工 | PRIME 合成 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 稠密 | ada-002 | 35.46 | 53.29 | 35.95 | 48.36 | 41.09 | 36.00 |
| 稠密 | multi-ada-002 | 40.22 | 55.12 | 39.85 | 50.80 | 47.21 | 38.05 |
| 稠密 | DPR | 15.23 | 44.49 | 25.00 | 42.11 | 10.69 | 30.13 |
| 稀疏 | BM25 | 15.23 | 53.77 | 32.46 | 45.69 | 42.32 | 31.25 |
| 结构 | QAGNN | 21.54 | 52.05 | 28.76 | 46.97 | 17.62 | 29.63 |
| 混合 | 4StepFocus | – | 56.20 | – | 65.80 | – | 55.90 |
| 混合 | FocusedR | – | 56.00 | – | 78.80 | – | 65.50 |
| 混合 | Dense+BM25 | 24.30 | 51.49 | 46.64 | 51.49 | 52.65 | 39.11 |
| 查询扩展 | HyDE | 39.25 | 53.71 | 37.23 | 50.02 | 47.70 | 43.55 |
| 查询扩展 | RAR | 36.15 | 54.63 | 35.19 | 50.87 | 49.01 | 44.50 |
| 查询扩展 | AGR | 37.27 | 53.38 | 37.23 | 51.89 | 49.65 | 46.63 |
| 查询扩展 | KAR | 40.62 | 57.29 | 46.60 | 60.28 | 59.90 | 50.81 |
| 智能体 | ReACT | 35.95 | 50.81 | 35.95 | 47.03 | 41.09 | 33.63 |
| 智能体 | Reflexion | 35.95 | 54.70 | 35.95 | 49.55 | 41.09 | 38.52 |
| 微调 | AvaTaR | 42.43 | 60.57 | 35.94 | 49.70 | 53.34 | 42.23 |
| 微调 | mFAR | – | 58.50 | – | 71.70 | – | 68.30 |
| 微调 | MoR | – | 59.90 | – | 75.00 | – | 63.50 |
| SAGE（本文） | SPARK | 33.56 | 53.95 | 53.51 | 66.40 | 63.56 | 57.64 |
| SAGE（本文） | SPARK +SAGE +Edge | 36.93 | 54.12 | 55.90 | 68.60 | 65.85 | 58.42 |
| SAGE（本文） | SPARK +SAGE-Edge | 42.05 | 58.28 | 56.40 | 70.10 | 66.37 | 60.98 |

**表 3：** OTT-QA 中文档对与表对的跨模态相似度统计。

| 相似度指标 | 文档–文档 | 文档–表 | 表–表 |
| --- | ---: | ---: | ---: |
| topic_similarity | 0.350 | 0.247 | 0.263 |
| content_similarity | 0.389 | 0.350 | 0.404 |
| column_similarity | 0.000 | 0.242 | 0.409 |
| entity_relationship_overlap | 0.013 | 0.000 | 0.000 |
| entity_count | 0.682 | 0.477 | 0.849 |
| topic_title_similarity | 0.000 | 0.221 | 0.000 |
| topic_summary_similarity | 0.000 | 0.236 | 0.000 |
| title_similarity | 0.000 | 0.000 | 0.239 |
| description_similarity | 0.000 | 0.000 | 0.262 |

表 3 进一步揭示三种跨模态结构效应。以实体为中心的连通性占主导，但依赖于模态。共享实体构成图的骨干，但其影响随节点类型而变。表格形成稠密的实体枢纽，文本区域则支持语义上更为混合的邻域，从而得到一种混合拓扑，既能做事实链接，也能做主题遍历。不同模态编码根本不同的结构信号。文本捕捉叙述和关系结构，表格则提供散文中没有的模式级对齐。因此相似度是不对称的，有效的建图必须把各模态视为互补，而不是可互换。跨模态对齐来自信号的组合，而不是某一信号占优。文档–表链接产生于多个虽弱但一致的信号的聚合，而不是单一主导指标。可靠的跨模态桥梁需要多信号融合，稳定性来自各维度上的一致。

### 3.2 STaRK：半结构化数据结果

**图对智能体检索器的影响。** 与我们在 OTT-QA 上的观察类似，基于图的检索也提高了智能体检索器在全部 STaRK 数据集上的 Recall@20（表 2）。把检索集合扩展到包含相连节点后，图露出基座智能体遗漏的额外相关节点，从而在人工查询和合成查询上都得到更高召回。

**是否存在图增强帮助更大的、依数据集而异的模式？** 当节点含有更丰富的文本内容时，图增强的增益更大。我们评估两种扩展策略。SPARK +SAGE-Edge 在 Cypher 查询包含显式边时跳过邻居扩展，以保留查询中指定的语义关系。相比之下，SPARK +SAGE +Edge 总是扩展邻居。在 AMAZON 上，产品元数据提供详细的节点描述，SPARK +SAGE-Edge 使人工查询的 R@20 提高 +8.49，合成查询提高 +4.33。节点信息更稀疏的数据集，如 MAG 和 PRIME，改进较小，大约 1 到 2 个百分点。这一模式表明，块级图在

<!-- 原 PDF 第 7 页 -->

节点含有足够上下文、足以支撑有意义的多跳证据链时最为有效，从而能检索到扁平检索方法未能抓住的连接。

**这一基线+图的组合与其他最先进方法相比如何。** SPARK +SAGE-Edge 在所有数据集上都大幅优于传统基线，包括稠密、稀疏和查询扩展方法（表 2），同时达到 AvaTaR、mFAR 和 MoR 等微调方法的性能水平。FocusedR 在 MAG 和 PRIME 上得分更高，那里结构化的知识图谱三元组提供了强信号；但 SPARK +SAGE-Edge 在 AMAZON 上最好，因为它利用丰富的节点内容做块级扩展。重要的是，SPARK +SAGE-Edge 只需要一次大语言模型调用和一步检索，因而比多轮迭代的替代方法显著更快，也更适合大规模部署。

**我们的智能体方法与其他最先进方法相比效率如何。** 表 4 揭示现有检索方法共有的三个主要效率瓶颈。第一，反复调用大语言模型大幅增加推理成本。第二，迭代检索循环带来可能任意变长的执行路径。第三，符号集合连接运算增加可观的计算开销。ReAct、Reflexion 和 AvaTaR 依赖逐步检索，每一步动作都发出一次大语言模型调用，步数增加时延迟和成本都急剧上升。相比之下，4StepFocus 和 FocusedR 在多轮中反复做带集合交集的符号剪枝，查询变复杂时运行时间大幅增长。KAR 把大语言模型的使用减到两次调用，但仍需要对整个数据集做多次检索，因而限制了可扩展性。

**表 4：** 根据方法描述得到的理论上的运行时间分解。#Retr. 统计检索操作次数；\(n\) 是依方法而定的推理步数。\(n_1\)、\(n_2\) 表示外层/内层迭代。\(e\) 是抽取出的实体数。\(E\) 和 \(R\) 表示回合数与调用次数。Set Join 表示显式的候选–邻域交集。

| 方法 | #Retr. | #LLM | #Iter. | Set Join |
| --- | --- | --- | --- | --- |
| 4StepFocus | \(1 + n\) | 2 | \(n\) | Triplet cand. |
| FocusedR | \(\ge 3+n\) | 3 | \(n_1 \times n_2\) | Sym. cand |
| AvaTaR | \(n\) | \(n+1\) | \(n\) | – |
| KAR | \(e+3\) | 2 | 1 | – |
| ReACT | \(n\) | \(n+1\) | \(n\) | – |
| Reflexion | \(n\) | \((n+1)E+R\) | \(nE+R\) | – |
| SAGE | 2 | 1 | 1 | – |

**表 5：** 剪枝分位数与逻辑选边对图稀疏性的影响。

| 分位数 | 逻辑 | 总边数 | 候选占比 | 平均度 | 密度 |
| ---: | --- | ---: | ---: | ---: | ---: |
| 80 | OR | 1,240,504 | 39.5% | 109.2 | 0.0048 |
| 85 | OR | 969,911 | 30.9% | 85.4 | 0.0038 |
| 90 | OR | 669,992 | 21.3% | 59.0 | 0.0026 |
| 95 | OR | 344,955 | 11.0% | 30.4 | 0.0013 |
| 97 | OR | 206,461 | 6.6% | 18.2 | 0.0008 |
| 99 | OR | 60,371 | 1.9% | 5.3 | 0.0002 |
| 80 | AND | 150,973 | 4.8% | 13.3 | 0.0006 |
| 85 | AND | 101,963 | 3.2% | 9.0 | 0.0004 |
| 90 | AND | 63,042 | 2.0% | 5.6 | 0.0002 |
| 95 | AND | 30,920 | 1.0% | 2.7 | 0.0001 |
| 97 | AND | 21,553 | 0.7% | 1.9 | 0.0001 |
| 99 | AND | 13,434 | 0.4% | 1.2 | 0.0001 |

SPARK 消除了全部三个瓶颈。它一次大语言模型调用、一次检索、一次图扩展即可完成。没有迭代循环，也没有符号集合连接。由此得到一条固定、轻量的执行路径，速度快得多，同时召回仍有竞争力。在延迟和成本至关重要的真实部署中，SPARK 给出更好的单位计算精度权衡。阶复杂度的计算细节见附录 C。

### 3.3 消融研究

**敏感性分析：建边时分位数的影响。** 我们研究基于分位数的剪枝如何塑造 OTT-QA 设定中的图连通性。剪枝通过限制每个块的相似度边，控制连通性与噪声之间的权衡。

我们比较两种选边策略。OR 逻辑保留满足任一相似度准则的边，鼓励跨异构信号的连通；AND 逻辑要求全部准则都满足，从而大幅剪枝。

表 5 显示，AND 逻辑稳定地产生极低的平均度（1.2–2.7），连通性弱，连通分量破碎。这使可靠的多跳遍历无法进行，也没有实际收益。因此我们采用 OR 逻辑。

在 OR 逻辑下，第 95 百分位平衡最好。更严的阈值会拆碎邻域、降低扩展覆盖；更松的剪枝则使度与噪声急剧上升。第 95 百分位保持稳定连通，同时使候选扩展和重排序仍然可行。

第 95 百分位的目标是：在扩展和下游过滤之后，每个块大约有 5–25 个有效邻居，既保持连通，又使重排序可行。

<!-- 原 PDF 第 8 页 -->

**表 6：** STaRK 各数据集上，不同基线检索器在图增强前后的 Recall@20。Hybrid 指 BM25+余弦相似度。A.、M.、P. 分别表示 AMAZON、MAG 和 PRIME。

| 方法 | 人工 A. | 人工 M. | 人工 P. | 合成 A. | 合成 M. | 合成 P. |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Hybrid | 24.3 | 46.6 | 52.7 | 51.5 | 51.5 | 39.1 |
| Hybrid+Graph | 31.1 | 46.4 | 53.4 | 53.8 | 52.9 | 38.4 |
| 变化（\(\Delta\)） | +6.8 | −0.2 | +0.7 | +2.3 | +1.4 | −0.7 |
| SPARK | 33.6 | 53.5 | 63.6 | 54.1 | 66.4 | 58.4 |
| SPARK +SAGE | 42.1 | 56.4 | 66.4 | 58.3 | 70.1 | 61.0 |
| 变化（\(\Delta\)） | +8.5 | +2.9 | +2.8 | +4.2 | +3.7 | +2.6 |

**性能增益有多少来自图结构本身，有多少来自图扩展策略？** 两种变体都优于基础 SPARK 模型（表 2），但 SPARK +SAGE-Edge 的增益稳定地更大。例如，在 AMAZON 人工查询上，它使 R@20 提高 +8.49，而 SPARK +SAGE +Edge 为 +6.21；在 MAG 人工查询上，它增加 +1.31，后者为 +0.84。这一趋势在各数据集上成立。对带边意识的查询有选择地跳过扩展，可以避免无关邻居稀释语义上有根据的候选；而对没有结构约束的查询，扩展仍然有益。这些结果表明，改进来自图与扩展策略的相互作用：图提供有用的连通性，而按查询语义决定是否扩展，则保证只引入有意义的邻居。

**初始检索器对基于图的扩展有何影响？** 如表 6 所示，图增强的效果强烈依赖于初始检索器的质量。对稠密与稀疏混合基线，Recall@20 明显低于智能体检索器，图扩展带来的改进也有限。在某些情形，尤其是 PRIME 和 MAG 子集在较低检索深度上，差值可以忽略，甚至为负，例如 Hybrid 的人工 MAG 从 46.6 降到 46.4。部分原因是混合检索器不考虑节点类型，而图扩展倾向于偏向与种子节点嵌入相似的节点，这些节点往往类型相同。若没有较强的初始候选集和对节点类型的引导，扩展可能引入无关节点，从而限制增益。

相比之下，智能体检索器提供更高的初始 Recall@20，并确定节点类型。与智能体结合的图扩展在所有数据集和查询类型上都稳定提高性能，例如 AMAZON 人工查询从 33.6 提高到 42.1。更强的初始候选与类型感知检索相结合，使图能够加入相关节点，放大扩展的收益。展示这些趋势的完整 Recall@\(k\) 曲线见附录 D。

### 3.4 STaRK 人工集上的错误分析

我们人工分析 STaRK 人工集上的检索失败，并把错误分为三类：

- **数据错误**反映数据集本身的局限，包括：（1）结构错误，即知识图谱中缺失边或边的方向错误；（2）欠指定，即查询缺少足够约束来确定正确实体；（3）评估伪影，即黄金标注不完整，只标出有效答案的一个子集。
- **Cypher 生成错误**出现在把自然语言翻译成图查询时：（1）约束错误，即数值、时间或逻辑过滤没有正确施加；（2）结构错误，即系统未能为图遍历选择正确的节点或边类型。
- **运行时错误**发生在查询执行期间，尽管 Cypher 在句法上正确：（1）语义错误，即单位、术语或缩写不匹配，导致无法正确检索；（2）过度检索，即过滤不足，查询返回过多候选。

**表 7：** STaRK 各数据集上的错误分布（%）。

| 类别 | 子类 | Amazon | MAG | Prime |
| --- | --- | ---: | ---: | ---: |
| 数据 | 结构 | 5 | 6 | 4 |
| 数据 | 欠指定 | 4 | 5 | 3 |
| 数据 | 评估伪影 | 7 | 4 | 4 |
| Cypher | 约束 | 36 | 30 | 31 |
| Cypher | 结构 | 0 | 0 | 22 |
| 运行时 | 语义 | 25 | 37 | 12 |
| 运行时 | 过度检索 | 23 | 18 | 22 |
| 合计 |  | 100 | 100 | 100 |

约束抽取失败在 AMAZON 和 PRIME 上占主导，反映出把复杂的产品属性或生物医学谓词翻译成精确图查询的困难。MAG 主要受语义不匹配影响，原因是技术摘要很密，查询与图实体之间的术语和措辞不同。当过滤不足时，所有数据集都会出现过度检索。PRIME 独有大量图结构错误，这与其更丰富的模式需要正确选择边和节点相一致。数据错误总体上较小，但仍占一定比例，尤其在 MAG 上黄金标注不完整（表 7）。

总体而言，这些模式突出了一种权衡，它介于

<!-- 原 PDF 第 9 页 -->

查询翻译、数据质量与语义对齐之间。AMAZON 的查询因术语和单位多样而失败，MAG 的查询因内容复杂、结构化图遍历难以捕捉而失败，PRIME 的查询因需要在其丰富模式中导航而失败。

## 4 相关工作

异构语料上的检索增强问答，不仅要处理文本相关性，还要处理结构：表格有模式和连接约束，文档有潜在的主题链接，许多真实集合还显式给出关系。下面概述不同技术：

**以表格为中心的检索与数据集发现。** 对表格仓库而言，一个主要主题是按可合并性、可连接性等结构准则检索相关表。Starmie（Fan et al., 2022）、DeepJoin（Dong et al., 2022）和 WarpGate（Cong et al., 2022）学习或编码列/表表示，以便高效搜索连接或合并，通常借助 ANN 索引加速。其他工作针对专门的关系增强信号，例如通过基于略图的索引搜索相关数据集（Santos et al., 2022）。对端到端表格问答，系统用级联流水线提高实际检索质量，把稀疏过滤、稠密检索和重排序结合起来（Singh et al., 2025）；而基于大语言模型的稠密检索技术（例如 HyDE）可以在没有标注相关性数据时改善零样本检索。

**面向检索与 RAG 的基于图的索引。** 基于图的 RAG 方法把信息组织成图，以检索相连上下文并聚合证据。Microsoft GraphRAG（Edge et al., 2024b）构建带社区摘要的实体图，用于语料级问题；GRAG（Peng et al., 2024）检索文本子图，并把拓扑注入生成；PathRAG（Chen et al., 2025a）聚焦冗余剪枝和基于路径的提示。GNN-Ret（Li et al., 2024b）用结构边（同一节/同一文档）和关键词边构建段落图，再用图神经网络重排序，而不做语义分块或元数据剪枝。ATLANTIC（Munikoti et al., 2023）用预定义结构关系构建文档级图，并用图神经网络编码，其操作粒度是文档而不是块。在多文档问答中，知识图谱提示通过段落图遍历组装支持上下文（Wang et al., 2023）。一篇更广的综述（Han et al., 2024）指出，图的形式和领域约束会强烈塑造设计空间。

**语言模型+知识图谱推理，以及带工具的智能体检索。** 当有显式知识图谱时，QA-GNN 等模型（Wang et al., 2024; Sun et al., 2018, 2019; Yasunaga et al., 2021; Pan et al., 2024）把基于语言模型的相关性估计与图神经推理结合起来。与此并行，智能体框架把检索当作在外部工具上的规划–执行过程：ReAct 交织推理与动作，Reflexion 通过反馈和自我反思改进智能体，AvaTaR 通过对比较推理优化工具使用。

先前工作常常只针对单一结构类型（表格仓库、显式知识图谱，或文本语料的图索引）。我们的框架以检索为中心且结构感知：关系隐式时离线构建块图，图显式时保留原生关系，并用简单的种子 → 扩展 → 重排序算子，在固定预算下选择证据。

## 5 结论

我们提出 SAGE，一种结构感知的图检索框架。它把离线图构建与在线的、以查询为条件的遍历分开，从而使检索算子适应数据拓扑。元数据驱动的相似度与剪枝为隐式语料建图，显式知识图谱则保留原生模式边，并在查询时根据图密度和模式是否可用选择算子。

在 OTT-QA 上，相似度驱动的扩展相对强混合基线将 Recall@\(k\) 提高 2.8–5.7 个百分点，用紧凑上下文检索到更连贯的多跳证据。在 STaRK 上，带选择性扩展的智能体检索在不训练的情况下接近微调性能：用符号 Cypher 查询在稠密图中导航，同时限制邻居噪声。总体而言，利用图连通性的结构感知检索，可以在没有任务特定训练的情况下，达到或超过强混合基线。

未来工作可以包括指令微调或微调智能体，以生成更准确、更高效的 Cypher 查询，并把框架扩展到通过跨模态链接纳入图像和其他媒体的多模态图。

<!-- 原 PDF 第 10 页 -->

## 局限

本研究聚焦两种有代表性的情形，并在 STaRK 上依赖基于大语言模型的智能体，相对传统检索会引入延迟和计算成本。这一权衡换来免训练的符号 Cypher 生成，从而在稠密图中提供精确的模式感知遍历，同时避免邻居噪声。该框架依赖初始种子的质量，因为图扩展是放大而不是取代基座检索。错误分析表明，约束抽取与过滤（占错误的 30% 到 36%）是主要失败模式，反映出在没有任务特定训练时，把非正式查询映射到结构化谓词的困难。尽管有这些局限，我们擅长露出扁平检索会漏掉的、结构上相连的多跳证据：在 OTT-QA 上获得 2.8 到 5.7 个百分点的增益，并在不训练的情况下接近 STaRK 上的微调基线；在图拓扑提供判别性结构的复杂查询上，表现尤其强。

## 伦理声明

我们在公开基准（OTT-QA 和 STaRK）上评估，这些基准按其各自许可发布，供研究使用。我们的框架在图结构上运行，不收集任何新的用户数据，也不推断个人或人口统计属性。

重要的是，我们的智能体方法在查询规划期间只访问图拓扑和模式信息，而不访问实际节点内容，这提供了额外的隐私保护，并减少对敏感信息的暴露。我们希望通过在异构信息源上实现更高效的结构感知检索，使研究社区受益。

与任何检索系统一样，我们的方法在真实部署中可能被滥用，以在未经授权的情况下露出或组合信息。然而，本工作仅用于学术研究，并非为监控、决策或其他高风险场景的部署而设计。任何实际使用都应遵循标准的数据治理实践（访问控制、审计和隐私保障），并接受适当监督。为支持可复现性，我们记录了数据划分、提示和解码设置。

我们使用了人工智能工具协助写作并改进表述。

## 致谢

本研究部分得到 ONR Contract N00014-23-1-2364 的支持，并由 Arizona State University 与 University of Pennsylvania 合作开展。我们感谢 Arizona State University School of Augmented Intelligence 的 Complex Data Analysis and Reasoning Lab，以及 University of Pennsylvania 的 Cognitive Computation Group 提供计算资源与机构支持。

## 参考文献

2013. SPARQL 1.1 查询语言. Technical report, W3C.

Negar Arabzadeh, Xinyi Yan, and Charles LA Clarke. 2021. 预测稠密与稀疏检索策略选择中的效率/效果权衡. In Proceedings of the 30th ACM International Conference on Information & Knowledge Management, pages 2862–2866.

Derian Boer, Fabian Koch, and Stefan Kramer. 2024. 借助基于三元组的预过滤，利用半结构化知识与大语言模型进行问答. arXiv preprint arXiv:2409.00861.

Derian Boer, Stephen Roth, and Stefan Kramer. 2025. 聚焦、合并、排序：基于半结构化知识库的改进问答. arXiv preprint arXiv:2505.09246.

Boyu Chen, Zirui Guo, Zidan Yang, Yuluo Chen, Junze Chen, Zhenghao Liu, Chuan Shi, and Cheng Yang. 2025a. PathRAG：用关系路径剪枝基于图的检索增强生成. arXiv preprint arXiv:2502.14902.

Peter Baile Chen, Yi Zhang, Mike Cafarella, and Dan Roth. 2025b. 我们能一次把一切都检索出来吗？ARM：一种面向对齐的、基于大语言模型的检索方法. In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 30298–30317, Vienna, Austria. Association for Computational Linguistics.

Wenhu Chen, Ming-Wei Chang, Eva Schlinger, William Wang, and William W Cohen. 2020. 面向表格与文本的开放问答. arXiv preprint arXiv:2010.10439.

Xilun Chen, Kushal Lakhotia, Barlas Oguz, Anchit Gupta, Patrick Lewis, Stan Peshterliev, Yashar Mehdad, Sonal Gupta, and Wen-tau Yih. 2022. 显著短语感知的稠密检索：稠密检索器能否模仿稀疏检索器？ In Findings of the Association for Computational Linguistics: EMNLP 2022, pages 250–262.

<!-- 原 PDF 第 11 页 -->

Xinran Chen, Xuanang Chen, Ben He, Tengfei Wen, and Le Sun. 2024. 分析、生成与细化：用大语言模型为零样本开放域问答做查询扩展. In Findings of the Association for Computational Linguistics: ACL 2024, pages 11908–11922, Bangkok, Thailand. Association for Computational Linguistics.

Tianji Cong, James Gale, Jason Frantz, HV Jagadish, and Ça˘gatay Demiralp. 2022. WarpGate：面向云数据仓库的语义连接发现系统. arXiv preprint arXiv:2212.14155.

Yuyang Dong, Chuan Xiao, Takuma Nozawa, Masafumi Enomoto, and Masafumi Oyamada. 2022. DeepJoin：用预训练语言模型发现可连接的表. arXiv preprint arXiv:2212.07588.

Darren Edge, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao, Apurva Mody, Steven Truitt, Dasha Metropolitansky, Robert Osazuwa Ness, and Jonathan Larson. 2024a. 从局部到全局：面向查询聚焦摘要的图 RAG 方法. arXiv preprint arXiv:2404.16130.

Darren Edge, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao, Apurva Mody, Steven Truitt, Dasha Metropolitansky, Robert Osazuwa Ness, and Jonathan Larson. 2024b. 从局部到全局：面向查询聚焦摘要的图 RAG 方法. arXiv preprint arXiv:2404.16130.

Grace Fan, Jin Wang, Yuliang Li, Dan Zhang, and Renée Miller. 2022. 用上下文化的基于列的表示学习，从数据湖中做语义感知的数据集发现. arXiv preprint arXiv:2210.01922.

Nadime Francis, Alastair Green, Paolo Guagliardo, Leonid Libkin, Tobias Lindaaker, Victor Marsault, Stefan Plantikow, Mats Rydberg, Petra Selmer, and Andrés Taylor. 2018. Cypher：一种面向属性图、仍在演进的查询语言. In Proceedings of the 2018 international conference on management of data, pages 1433–1445.

Luyu Gao, Xueguang Ma, Jimmy Lin, and Jamie Callan. 2023. 无需相关性标签的精确零样本稠密检索. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 1762–1777.

Haoyu Han, Yu Wang, Harry Shomer, Kai Guo, Jiayuan Ding, Yongjia Lei, Mahantesh Halappanavar, Ryan A Rossi, Subhabrata Mukherjee, Xianfeng Tang, et al. 2024. 带图的检索增强生成（GraphRAG）. arXiv preprint arXiv:2501.00309.

Junjie Huang, Wanjun Zhong, Qian Liu, Ming Gong, Daxin Jiang, and Nan Duan. 2022. 面向开放问答中表格与文本联合检索的混合模态表示学习与预训练. In Findings of the Association for Computational Linguistics: EMNLP 2022, pages 4117–4129, Abu Dhabi, United Arab Emirates. Association for Computational Linguistics.

Bernal Jimenez Gutierrez, Yiheng Shu, Yu Gu, Michihiro Yasunaga, and Yu Su. 2024. HippoRAG：受神经生物学启发的、面向大语言模型的长期记忆. Advances in Neural Information Processing Systems, 37:59532–59569.

Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick SH Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, and Wen-tau Yih. 2020. 面向开放域问答的稠密段落检索. In EMNLP (1), pages 6769–6781.

Yongjia Lei, Haoyu Han, Ryan A Rossi, Franck Dernoncourt, Nedim Lipka, Mahantesh M Halappanavar, Jiliang Tang, and Yu Wang. 2025. 面向文本丰富图知识库的结构与文本混合检索. arXiv preprint arXiv:2502.20317.

Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, et al. 2020. 面向知识密集型自然语言处理任务的检索增强生成. Advances in neural information processing systems, 33:9459–9474.

Yihao Li, Ru Zhang, and Jianyi Liu. 2024a. 经由与知识图谱集成的协作而增强的、基于提示的大语言模型推理方案. In International Conference on Artificial Neural Networks, pages 251–265.

Zijian Li, Qingyan Guo, Jiawei Shao, Lei Song, Jiang Bian, Jun Zhang, and Rui Wang. 2024b. 面向大语言模型问答的、图神经网络增强的检索.

Kaixin Ma, Hao Cheng, Xiaodong Liu, Eric Nyberg, and Jianfeng Gao. 2022. 经由异构知识上的推理链进行开放域问答. In Findings of the Association for Computational Linguistics: EMNLP 2022, pages 5360–5374, Abu Dhabi, United Arab Emirates. Association for Computational Linguistics.

Kaixin Ma, Hao Cheng, Yu Zhang, Xiaodong Liu, Eric Nyberg, and Jianfeng Gao. 2023. 技能链：一种可配置的开放域问答模型. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 1599–1618, Toronto, Canada. Association for Computational Linguistics.

Yu A Malkov and Dmitry A Yashunin. 2018. 用层次化可导航小世界图进行高效且稳健的近似最近邻搜索. IEEE transactions on pattern analysis and machine intelligence, 42(4):824–836.

Priyanka Mandikal and Raymond Mooney. 2024. 稀疏遇上稠密：一种增强科学文献检索的混合方法. arXiv preprint arXiv:2401.04055.

Costas Mavromatis and George Karypis. 2024. GNN-RAG：面向大语言模型推理的图神经检索. arXiv preprint arXiv:2405.20139.

<!-- 原 PDF 第 12 页 -->

Sai Munikoti, Anurag Acharya, Sridevi Wagle, and Sameera Horawalavithana. 2023. ATLANTIC：面向交叉学科科学的结构感知检索增强语言模型.

Neo4j, Inc. 2026. Neo4j 图数据库.

OpenAI, :, Aaron Hurst, Adam Lerer, Adam P. Goucher, Adam Perelman, Aditya Ramesh, Aidan Clark, AJ Ostrow, Akila Welihinda, and et al. 2024. GPT-4o 系统卡.

Shirui Pan, Linhao Luo, Yufei Wang, Chen Chen, Jiapu Wang, and Xindong Wu. 2024. 统一大语言模型与知识图谱：一份路线图. IEEE Transactions on Knowledge and Data Engineering, 36(7):3580–3599.

Eunhwan Park, Sung min Lee, Dearyong Seo, Seon-hoon Kim, Inho Kang, and Seung-Hoon Na. 2023. RINK：面向表格与文本开放域问答的、由阅读器继承的证据重排序器. In AAAI Conference on Artificial Intelligence.

Boci Peng, Yun Zhu, Yongchao Liu, Xiaohe Bo, Haizhou Shi, Chuntao Hong, Yan Zhang, and Siliang Tang. 2024. 图检索增强生成：综述. ACM Transactions on Information Systems.

Nils Reimers and Iryna Gurevych. 2019. Sentence-BERT：用孪生 BERT 网络做句子嵌入. arXiv preprint arXiv:1908.10084.

Stephen Robertson, Hugo Zaragoza, et al. 2009. 概率相关性框架：BM25 及其延伸. Foundations and Trends® in Information Retrieval, 3(4):333–389.

AÃl’cio Santos, Aline Bessa, Christopher Musco, and Juliana Freire. 2022. 面向相关数据集搜索的基于略图的索引. In 2022 IEEE 38th International Conference on Data Engineering (ICDE), pages 2928–2941.

Tao Shen, Guodong Long, Xiubo Geng, Chongyang Tao, Yibin Lei, Tianyi Zhou, Michael Blumenstein, and Daxin Jiang. 2024. 检索增强的检索：大语言模型是强零样本检索器. In Findings of the Association for Computational Linguistics: ACL 2024, pages 15933–15946, Bangkok, Thailand. Association for Computational Linguistics.

Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. 2023. Reflexion：带言语强化学习的语言智能体. Advances in Neural Information Processing Systems, 36:8634–8652.

Adarsh Singh, Kushal Raj Bhandari, Jianxi Gao, Soham Dan, and Vivek Gupta. 2025. CRAFT：面向表格问答的免训练级联检索. arXiv preprint arXiv:2505.14984.

Haitian Sun, Tania Bedrax-Weiss, and William Cohen. 2019. 题目抽取不完整，见原 PDF 第 12 页. In Proceedings of the 2019 conference on empirical methods in natural language processing and the 9th international joint conference on natural language processing (EMNLP-IJCNLP), pages 2380–2390.

Haitian Sun, Bhuwan Dhingra, Manzil Zaheer, Kathryn Mazaitis, Ruslan Salakhutdinov, and William Cohen. 2018. 用知识库与文本的早期融合进行开放域问答. In Proceedings of the 2018 conference on empirical methods in natural language processing, pages 4231–4242.

Wenhui Wang, Furu Wei, Li Dong, Hangbo Bao, Nan Yang, and Ming Zhou. 2020. MiniLM：面向预训练 Transformer 的任务无关压缩的深度自注意力蒸馏. Advances in neural information processing systems, 33:5776–5788.

Yu Wang, Nedim Lipka, Ryan A. Rossi, Alexa Siu, Ruiyi Zhang, and Tyler Derr. 2023. 面向多文档问答的知识图谱提示.

Yu Wang, Nedim Lipka, Ryan A Rossi, Alexa Siu, Ruiyi Zhang, and Tyler Derr. 2024. 面向多文档问答的知识图谱提示. In Proceedings of the AAAI conference on artificial intelligence, volume 38, pages 19206–19214.

Shirley Wu, Shiyu Zhao, Qian Huang, Kexin Huang, Michihiro Yasunaga, Kaidi Cao, Vassilis Ioannidis, Karthik Subbian, Jure Leskovec, and James Y Zou. 2024a. AvaTaR：通过对比较推理优化大语言模型智能体的工具使用. Advances in Neural Information Processing Systems, 37:25981–26010.

Shirley Wu, Shiyu Zhao, Michihiro Yasunaga, Kexin Huang, Kaidi Cao, Qian Huang, Vassilis N. Ioannidis, Karthik Subbian, James Zou, and Jure Leskovec. 2024b. STaRK：在文本与关系知识库上对大语言模型检索进行基准评测. In NeurIPS Datasets and Benchmarks Track.

Yu Xia, Junda Wu, Sungchul Kim, Tong Yu, Ryan A Rossi, Haoliang Wang, and Julian McAuley. 2024. 面向文本与关系检索的、借助大语言模型的知识感知查询扩展. arXiv preprint arXiv:2410.13765.

Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik R Narasimhan, and Yuan Cao. 2022. ReAct：在语言模型中协同推理与行动. In The eleventh international conference on learning representations.

Michihiro Yasunaga, Hongyu Ren, Antoine Bosselut, Percy Liang, and Jure Leskovec. 2021. QA-GNN：用语言模型与知识图谱进行问答推理. arXiv preprint arXiv:2104.06378.

Haoyu Zhang, Jun Liu, Zhenhua Zhu, Shulin Zeng, Maojia Sheng, Tao Yang, Guohao Dai, and Yu Wang.

<!-- 原 PDF 第 13 页 -->

2024. 用基于图的近似最近邻搜索，高效且有效地检索稠密–稀疏混合向量. arXiv preprint arXiv:2410.20381.

Wanjun Zhong, Junjie Huang, Qian Liu, Ming Zhou, Jiahai Wang, Jian Yin, and Nan Duan. 2022. 面向表格与文本开放域问答、在混合链上的推理. arXiv preprint arXiv:2201.05880.

## 附录 A 数据集统计

### A.1 OTT-QA

OTT-QA 由连接文档块与表格块的异构图构成（表 8）。表格块数量相对较少，但与文档连接稠密，因而能在结构化来源与非结构化来源之间做跨模态检索。文档–文档边数量很大，反映出文档之间强烈的主题重叠，这对基于图的上下文传播特别有用。

**表 8：** OTT-QA 数据集统计，给出节点类型、边类型及其数量。

| 组成部分 | 数量 |
| --- | ---: |
| 文档块 | 21,912 |
| 表格块 | 974 |
| 节点合计 | 22,886 |
| 表–表边 | 66,003 |
| 文档–表边 | 162,374 |
| 文档–文档边 | 523,459 |
| 边合计 | 751,836 |

### A.2 STaRK

#### A.2.1 AMAZON

AMAZON 数据集原本包含四种节点类型：review、brand、color 和 category。后三种（brand、color、category）也可以表示为元数据属性，而不是单独的节点。我们观察到，所有产品节点都包含一个 reviews 键，其中存放表格形式的评论数据。

对稠密+稀疏（混合）检索，我们把这些评论数据当作表来检索和扩展（表 9）。由于 Neo4j 是图数据库，并不像 SQL 数据库那样原生支持表格结构，我们把每条评论转换成一个单独的节点，并连接到对应的产品节点（表 10）。这种图原生表示便于在需要跨同一产品的多条评论聚合数据（例如星级评分）时高效查询。

**表 9：** 来自 STaRK 数据集、用于混合检索的 AMAZON 节点类型分布。

| 节点类型 | 数量 |
| --- | ---: |
| Review | 957,192 |
| Product | 957,192 |
| 合计 | 1,914,384 |

**表 10：** 来自 STaRK 数据集、用于 Neo4j 查询的 AMAZON 节点类型分布。

| 节点类型 | 数量 |
| --- | ---: |
| Review | 12,963,012 |
| Product | 957,192 |
| 合计 | 13,920,204 |

**表 11：** 来自 STaRK 数据集的 AMAZON 边类型分布。

| 边类型 | 数量 |
| --- | ---: |
| HAS_REVIEW | 12,963,012 |
| ALSO_BUY | 1,663,562 |
| ALSO_VIEW | 1,362,680 |
| IS_SIMILAR | 24,886,992 |
| 合计 | 40,876,246 |

#### A.2.2 MAG

MAG 是一个大型学术图，实体类型多样，但每个节点的文本丰富程度相对有限（表 12 和表 13）。引用边和作者边提供强结构信号，但较短的文本描述限制了语义图扩展的效果。

**表 12：** 来自 STaRK 数据集的 MAG 节点类型分布。

| 节点类型 | 数量 |
| --- | ---: |
| Author | 1,104,554 |
| Paper | 700,244 |
| Field | 59,469 |
| Institution | 8,701 |
| 合计 | 1,872,968 |

**表 13：** 来自 STaRK 数据集的 MAG 边类型分布。

| 边类型 | 数量 |
| --- | ---: |
| CITES | 9,719,488 |
| HAS_FIELD | 7,243,269 |
| AUTHORED | 6,768,883 |
| ASSOCIATED_WITH | 167,482 |
| IS_SIMILAR | 12,954,514 |
| 合计 | 36,853,636 |

<!-- 原 PDF 第 14 页 -->

#### A.2.3 PRIME

PRIME 是高度结构化的生物医学图，实体类型和关系类型都很细（表 14 和表 15）。尽管图的关系语义丰富，节点级文本内容往往稀疏，因此有效的图扩展对初始检索的质量更为敏感。

**表 14：** 来自 STaRK 数据集的 PRIME 节点类型分布。

| 节点类型 | 数量 |
| --- | ---: |
| BiologicalProcess | 28,642 |
| Gene | 27,671 |
| Disease | 17,080 |
| Phenotype | 15,311 |
| Anatomy | 14,035 |
| MolecularFunction | 11,169 |
| Drug | 7,957 |
| CellularComponent | 4,176 |
| Pathway | 2,516 |
| Exposure | 818 |
| 合计 | 129,375 |

**表 15：** 来自 STaRK 数据集的 PRIME 边类型分布。下列数字按原文抽取列出；各项相加与表中合计 9,825,282 不一致，见原 PDF 第 14 页。

| 边类型 | 数量 |
| --- | ---: |
| EXPRESSED_IN | 3,036,406 |
| SYNERGISTIC_WITH | 2,672,628 |
| AFFILIATED_WITH | 1,029,162 |
| INTERACTS_WITH | 686,550 |
| INTERACTS_WITH_PROTEIN | 642,150 |
| PHENOTYPE_PRESENT | 300,634 |
| PARENT_OF | 281,744 |
| HAS_SIDE_EFFECT | 129,568 |
| CONTRAINDICATED_FOR | 61,350 |
| NOT_EXPRESSED_IN | 39,774 |
| TARGETS | 32,760 |
| INDICATED_FOR | 18,776 |
| INHIBITS_ENZYME | 10,634 |
| TRANSPORTED_BY | 6,184 |
| OFF_LABEL_USE | 5,136 |
| LINKED_TO | 4,608 |
| PHENOTYPE_ABSENT | 2,386 |
| ACTS_AS_CARRIER | 1,728 |
| IS_SIMILAR | 963,104 |
| 合计 | 9,825,282 |

## 附录 B OTT-QA 建图统计

### B.1 元数据抽取的成本分析

**表 16：** OTT-QA 元数据抽取按模态统计的词元用量。

| 模态 | 输入 | 输出 | 合计 |
| --- | ---: | ---: | ---: |
| 表格 | 1,625,516 | 3,989,504 | 5,615,020 |
| 文本 | 53,501,851 | 21,960,752 | 75,462,603 |
| 总计 | 55,127,367 | 25,950,256 | 81,077,623 |

如表 16 所示，文本元数据抽取主导了总词元用量，占所处理的 8110 万词元中的大部分。按 gpt-4o-mini 的定价，表格元数据抽取约花费 2.64 美元，文本元数据抽取花费 21.20 美元，合计 23.84 美元；若采用批处理则为 11.92 美元。尽管总量很大，逐项处理成本仍然极低，说明大规模元数据生成的成本效率很高。也可以使用开源模型。

### B.2 表–表相似度分析

我们分析 OTT-QA 中表格块之间的相似度统计，以评估建图是否必须使用大语言模型。

**列相似度与实体分布。** 图 5 给出列相似度以及每个块的实体数量的分布。列相似度大致呈钟形（正态分布），实体数量则强烈左偏——大多数块只含一个实体。这些图表明，即使是单实体块，也存在很高的语义相似度。

**图 5：** 左：列相似度分布。右：每个表格块的实体数量（左偏）。

**描述相似度与标题相似度。** 图 6 给出描述相似度与标题相似度的分布。二者都呈钟形，并在高端有轻微尾部，说明有些表在标题或描述上高度相似。

**图 6：** 左：描述相似度。右：标题相似度。两种分布相似，在高相似度处略有上升。

<!-- 原 PDF 第 15 页 -->

**列–标题、列–描述、标题–描述散点图。** 图 7 分别给出列–标题、列–描述和标题–描述相似度的散点图。明显的对角线趋势表明，相似的列往往与相似的标题和描述一起出现。

**图 7：** 列–标题（左）、列–描述（中）和标题–描述（右）相似度的散点图。对角线趋势表示强对齐。

**相关矩阵。** 表 17 给出全部表级相似度指标的相关矩阵。列、标题和描述相似度强相关，其中标题相似度与描述相似度的相关为 0.846。

**表 17：** 表–表相关矩阵。缩写：（1）column_similarity，（2）entity_count，（3）title_similarity，（4）description_similarity。

|  | (1) | (2) | (3) | (4) |
| --- | ---: | ---: | ---: | ---: |
| (1) Col Sim | 1.000 | 0.165 | 0.577 | 0.696 |
| (2) Ent Cnt | 0.165 | 1.000 | 0.179 | 0.189 |
| (3) Titl Sim | 0.577 | 0.179 | 1.000 | 0.846 |
| (4) Desc Sim | 0.696 | 0.189 | 0.846 | 1.000 |

### B.3 文档–文档相似度分析

我们分析 OTT-QA 中文档块之间的相似度统计，以评估语义内容，以及是否需要基于大语言模型的处理。

**每个块的实体数与事件数。** 图 8 给出每个文档块的实体数和事件数。两种分布都强烈左偏，大多数块只含一个实体或一个事件。这表明文档块小而聚焦，额外的基于大语言模型的抽取或摘要收益很小。

**图 8：** 每个文档块的实体与事件分布。大多数块只含一个实体，因而对基于大语言模型的抽取需求较低。

**主题相似度与内容相似度的分布。** 图 9 给出文档块之间主题相似度与内容相似度的直方图。两种分布大致呈钟形，并在 1 附近有一个小尖峰，说明大多数文档对中等相似，少数几乎相同。

**图 9：** 文档块之间主题相似度（左）与内容相似度（右）的直方图。可见钟形分布以及高相似度处的尖峰。

**主题–内容散点图。** 图 10 给出每个文档对的内容相似度相对主题相似度的散点图。大多数点落在对角线上，确认内容相似度与主题相似度强对齐。

**图 10：** 内容相似度相对主题相似度的散点图。对角线上的集中表明两个指标强对齐。

**相关矩阵。** 表 19 给出文档–表相似度指标的相关矩阵。列相似度、标题相似度和摘要相似度中等相关，确认跨模态语义对齐可以用简单嵌入捕捉。

<!-- 原 PDF 第 16 页 -->

**表 18：** 文档–文档相关矩阵。缩写：（1）topic_similarity，（2）content_similarity，（3）entity_relationship_overlap，（4）entity_count，（5）event_count。

|  | (1) | (2) | (3) | (4) | (5) |
| --- | ---: | ---: | ---: | ---: | ---: |
| (1) Top Sim | 1.000 | 0.650 | 0.250 | 0.253 | 0.153 |
| (2) Cont Sim | 0.650 | 1.000 | 0.357 | 0.339 | 0.251 |
| (3) Ent Rel | 0.250 | 0.357 | 1.000 | 0.530 | 0.230 |
| (4) Ent Cnt | 0.253 | 0.339 | 0.530 | 1.000 | 0.235 |
| (5) Evt Cnt | 0.153 | 0.251 | 0.230 | 0.235 | 1.000 |

### B.4 文档–表相似度分析

我们分析 OTT-QA 中文档块与表格块之间的语义对齐，以评估是否必须使用基于大语言模型的处理。

**主题–标题与主题–摘要相似度。** 图 11 分别给出主题–标题相似度与主题–摘要相似度的分布。两条曲线都呈钟形，说明大多数文档–表对中等相似，极端情形很少。这两个直方图并排放置，以便直接比较。

**图 11：** 左：主题–标题相似度分布。右：主题–摘要相似度分布。二者都呈钟形。

**列相似度与实体数量。** 图 12 给出列相似度以及每个表格块的实体数量。列相似度呈钟形分布，实体数量左偏，与文档–文档的观察一致。并排放置可以突出结构特征与语义特征上的分布模式。

**图 12：** 左：列相似度分布。右：每个表格块的实体数量（左偏）。

**主题、标题、摘要和列相似度的散点图。** 图 13 给出主题、标题、摘要和列相似度各种组合的散点图。对角线趋势表明，文档块与表格块在多个语义维度上强对齐。

**图 13：** 展示文档块与表格块对齐的散点图：主题–标题相对主题–摘要（左），列相对主题–摘要（中），列相对主题–标题（右）。对角线趋势表示强对齐。

**相关矩阵。** 表 19 给出文档–表相似度指标的相关矩阵。列相似度、标题相似度和摘要相似度中等相关，确认跨模态语义对齐可以用简单嵌入捕捉，而不需要基于大语言模型的处理。

**表 19：** 文档–表相关矩阵。缩写：（1）column_similarity，（2）entity_count，（3）topic_title_similarity，（4）topic_summary_similarity。

|  | (1) | (2) | (3) | (4) |
| --- | ---: | ---: | ---: | ---: |
| (1) Col Sim | 1.000 | 0.078 | 0.517 | 0.535 |
| (2) Ent Count | 0.078 | 1.000 | 0.107 | 0.107 |
| (3) Title Sim | 0.517 | 0.107 | 1.000 | 0.691 |
| (4) Summ Sim | 0.535 | 0.107 | 0.691 | 1.000 |

## 附录 C STaRK 上全部最先进基线的运行时间分析

### C.1 4StepFocus

4StepFocus 通过符号预过滤，再接向量相似度搜索和基于大语言模型的重排序，在半结构化知识库（SKB）上处理查询。

**流水线：**

1. **大语言模型抽取：** 大语言模型从查询 \(q\) 中抽取三元组 \(T\) 和目标变量 \(x_{\mathrm{target}}\)。
2. **符号预过滤（SUBSTITUTE）：** 迭代地把候选集与知识图谱邻居求交，直到收敛，得到过滤后的候选集 \(C_{\mathrm{filtered}}\)。
3. **向量相似度评分（VSS）：** 用非结构化数据为 \(C_{\mathrm{filtered}}\) 评分，返回

<!-- 原 PDF 第 17 页 -->

前 \(k_{\max}\) 个候选，以及额外的相关候选。

4. **大语言模型重排序：** 用 SKB 上下文对候选重排序。

**SUBSTITUTE 算法：**

**算法 1：** SUBSTITUTE：面向候选选择的符号预过滤

```
输入：候选集 C，三元组 T = {(h_i, e_i, t_i)}，目标变量 x_target
输出：过滤后的候选集 C_filtered
对每个变量 x 执行
    substitute[x] ← {c ∈ C | type(c) = type(x)}
结束
重复
    对每个 (h_i, e_i, t_i) ∈ T 执行
        substitute[h_i] ← substitute[h_i] ∩ neighbors(h_i, e_i, −)
        substitute[t_i] ← substitute[t_i] ∩ neighbors(t_i, e_i, +)
    结束
直到任何一个 substitute[x] 都不再变化
C_filtered ← substitute[x_target]
返回 C_filtered
```

**运行时间分析：**

- 步骤 1：\(O(1)\)，单次大语言模型调用。
- 步骤 2：\(O(n \cdot |T| \cdot \mathrm{deg})\)，对 \(|T|\) 个三元组做 \(n\) 次迭代，\(\mathrm{deg}\) 为平均节点度。
- 步骤 3：\(O(|C_{\mathrm{filtered}}|)\)，对过滤后的候选做 VSS。
- 步骤 4：\(O(1)\)，一次用于重排序的大语言模型调用。

**总复杂度：**

\[
O(n \cdot |T| \cdot \mathrm{deg} + |C_{\mathrm{filtered}}|)
\]

### C.2 FocusedR

FocusedR 把 Cypher 查询生成、符号落地，以及混合检索（受 Cypher 约束的检索，加上回退的向量相似度搜索 VSS）结合起来，然后再用大语言模型重排序。

**流水线：**

1. **大语言模型生成 Cypher：** 大语言模型利用节点类型和边类型，从 \(q\) 生成 Cypher 查询 \(q_{\mathrm{cypher}}\)。
2. **正则解析：** 把 \(q_{\mathrm{cypher}}\) 解析为目标 \(y\)、三元组 \(T\) 和符号约束 \(S_{\mathrm{raw}}\)。
3. **符号落地：**
   - SYMBOL_CANDIDATES：对符号常量做 VSS。
   - GROUND_TRIPLETS：通过邻居交集迭代剪枝候选集。
4. **自适应候选扩展：** 当 \(|C_{\mathrm{cypher}}| < k\) 时，按指数增大 \(\hat{k}\) 并重复步骤 3。
5. **混合 VSS 检索：** 做两次 VSS 调用：
   - \(Y_{\mathrm{cypher}}\)：受 Cypher 约束的候选
   - \(Y_{\mathrm{vss}}\)：回退的非结构化候选
6. **大语言模型重排序：** 对拼接后的候选 \(Y = Y_{\mathrm{cypher}} + Y_{\mathrm{vss}}\) 重排序。

**GROUND_TRIPLETS 算法：**

**算法 2：** GROUND_TRIPLETS：迭代候选剪枝

```
输入：三元组 T = {(h_i, e_i, t_i)}，符号候选集 S
输出：剪枝后的符号候选集 S
重复
    对每个 (h_i, e_i, t_i) ∈ T 执行
        S(h_i) ← S(h_i) ∩ neighbors(h_i, e_i, −)
        S(t_i) ← S(t_i) ∩ neighbors(t_i, e_i, +)
    结束
直到任何一个 S(x) 都不再变化
返回 S
```

**运行时间分析：**

- 步骤 1：\(O(1)\)，单次大语言模型调用。
- 步骤 2–4：\(O(n_1 \cdot n_2 \cdot |T| \cdot \mathrm{deg})\)。\(n_1\) 为外层 \(\hat{k}\) 扩展次数，\(n_2\) 为内层收敛迭代次数，\(|T|\) 为三元组数，\(\mathrm{deg}\) 为平均度。
- 步骤 5：\(O(|C_{\mathrm{cypher}}| + |C(y'.\mathrm{type})|)\)，两次 VSS 调用。

<!-- 原 PDF 第 18 页 -->

- 步骤 6：\(O(1)\)，一次用于重排序的大语言模型调用。

**总复杂度：**

\[
O(n_1 \cdot n_2 \cdot |T| \cdot \mathrm{deg} + |C_{\mathrm{cypher}}|)
\]

### C.3 AvaTaR

AvaTaR 是一个智能体优化框架，通过对比较推理改进会调用工具的大语言模型。它通常被实例化为在检索工具上运行的 ReAct 风格智能体。

**流水线：**

1. **智能体初始化：** 用查询 \(q\) 和一套工具（例如面向 SKB 的检索 API）初始化智能体。
2. **智能体循环：** 重复 \(m\) 步：
   - 大语言模型生成一个想法（thought）和一个动作（工具调用）。
   - 执行该动作，并把得到的观察追加到轨迹中。
3. **终止：** 一直继续，直到达到最大步数、满足成功条件，或生成最终答案。
4. **AvaTaR 优化（训练时）：** 用成功轨迹相对失败轨迹做对比微调，以改进以后的表现。

**运行时间分析：**

- 每条轨迹：\(O(m)\) 次大语言模型调用，以及 \(O(m_r)\) 次检索（\(m\) 为总步数，\(m_r \le m\) 为检索动作的次数）。
- 没有显式集合运算；推理隐含在大语言模型中。
- 没有专门的重排序器；检索结果直接送入智能体提示。
- 推理成本可以通过训练得到的策略，在多个查询上摊销。

**总复杂度（每个查询）：**

\[
O(m)\ \text{次大语言模型调用} + O(m_r)\ \text{次检索}
\]

其中 \(m\) 是直到停止条件为止的轨迹长度。

### C.4 KAR

KAR 通过实体抽取、邻居检索、文档关系过滤、三元组构造和最终检索，做知识感知的查询扩展。

**流水线：**

1. **实体抽取：** 大语言模型从查询 \(q\) 中抽取实体 \(E = \{e_1, \ldots, e_e\}\)。
2. **邻居与文档检索：** 对每个实体 \(e_i\)，检索邻居 \(N(e_i)\) 和相关联的文档 \(D_i\)（共 \(e + 1\) 次检索）。
3. **文档关系过滤：** 在这 \(e + 1\) 个邻居集合上，按余弦相似度过滤检索到的文档。
4. **三元组构造：** 从过滤后的邻居集合构造三元组 \((e_i, r_j, d_k)\)。
5. **查询扩展：** 把全部三元组送给大语言模型，生成扩展查询 \(q_{\mathrm{exp}}\)。
6. **最终检索：** 对扩展查询 \(q_{\mathrm{exp}}\) 执行一次检索。

**运行时间分析：**

- 步骤 1：\(O(1)\)，一次用于实体抽取的大语言模型调用。
- 步骤 2：\(O(e)\)，\(e\) 次实体邻居检索，外加 1 次文档检索。
- 步骤 3：\(O((e + 1) \cdot \mathrm{deg}_D)\)，在邻居文档上计算余弦相似度，\(\mathrm{deg}_D\) 为平均文档邻居数。
- 步骤 4：\(O(|T|)\)，构造三元组，\(|T|\) 为三元组总数。
- 步骤 5：\(O(1)\)，一次用于查询扩展的大语言模型调用。
- 步骤 6：\(O(1)\)，一次最终检索。

**总复杂度：**

\[
O(e \cdot \mathrm{deg}_D + |T|)
\]

恰好两次大语言模型调用。

<!-- 原 PDF 第 19 页 -->

### C.5 ReAct

ReAct 把大语言模型推理与工具调用（通常是检索）交织在思考–行动–观察循环中，直到任务完成或达到步数上限。

**流水线：**

1. **初始大语言模型推理：** 大语言模型生成初始想法和第一个动作（检索工具调用）。
2. **执行动作：** 执行检索动作，并把结果作为观察追加到轨迹中。
3. **后续推理：** 大语言模型根据观察进行推理，并生成下一个想法和动作。
4. **迭代：** 重复步骤 2–3，共 \(m\) 次迭代，直到得到最终答案或达到最大步数。

**运行时间分析：**

- 每条轨迹：\(O(m)\) 次大语言模型调用，以及 \(O(m_r)\) 次检索。
- \(m\)：直到停止条件（最大步数、成功或最终答案）的总步数。
- \(m_r \le m\)：检索动作的次数（全部动作的一个子集）。
- 没有显式集合运算；推理隐含在大语言模型中。
- 没有专门的重排序器；检索结果直接送入智能体提示。

**总复杂度（每个查询）：**

\[
O(m)\ \text{次大语言模型调用} + O(m_r)\ \text{次检索}
\]

其中 \(m\) 是直到停止为止的轨迹长度。

### C.6 Reflexion

Reflexion 用自我反思扩展 ReAct 智能体：每个失败回合之后，大语言模型分析轨迹，为下一回合生成言语反馈。

**流水线：**

- 步骤 1：运行一个 ReAct 回合：\(m\) 次迭代，每次为大语言模型调用 → 检索 → 观察。
- 步骤 2：评估回合结果（成功/失败）。
- 步骤 3：若失败，大语言模型生成反思 \(r_i\)，分析轨迹和错误。
- 步骤 4：把反思追加到提示中，重复步骤 1–3，总共 \(E\) 个回合。

**运行时间分析：**

- 每个回合：\(O(m)\) 次大语言模型调用 \(+\) \(O(m_r)\) 次检索（\(m\) 为步数，\(m_r\) 为检索次数）。
- 每次反思：\(O(1)\) 次大语言模型调用（自我批评）。
- \(E\)：直到成功或达到上限的总回合数。
- \(R\)：反思次数（\(R \le E - 1\)，每个失败回合一次）。
- 合计：\(O(E \cdot m + R)\) 次大语言模型调用 \(+\) \(O(E \cdot m_r)\) 次检索。

总计：\(O(E \cdot m + R)\) 次大语言模型调用 \(+\) \(O(E \cdot m_r)\) 次检索，其中 \(E\) 为回合数，\(m\) 为每个回合的步数，\(R\) 为反思次数。

### C.7 使用 SPARK 的 SAGE

使用 SPARK 的 SAGE 通过单遍智能体检索流水线进行查询，并带有混合稠密+稀疏扩展。

**流水线：**

1. **查询生成：** 智能体大语言模型根据自然语言输入 \(q\) 生成 Cypher/HNSW 查询。
2. **初始检索：** 用生成的查询检索前 \(k\) 个节点 \(N_k\)。
3. **图扩展：** 检索前 \(k\) 个节点的一跳邻居 \(N(N_k)\)。
4. **混合检索：** 在 \(N(N_k)\) 上做稠密+稀疏检索，得到最终的 \(k + k'\) 候选集。

**运行时间分析：**

- 步骤 1：\(O(1)\)，一次智能体大语言模型调用。
- 步骤 2：\(O(k)\)，初始检索（HNSW/Cypher）。
- 步骤 3：\(O(k \cdot \mathrm{deg})\)，邻居扩展（\(\mathrm{deg}\) 为平均节点度）。
- 步骤 4：\(O(k \cdot \mathrm{deg})\)，在邻居上做混合稠密+稀疏检索。

**总复杂度：**

\[
O(k \cdot \mathrm{deg})
\]

恰好一次大语言模型调用，且没有迭代循环。

<!-- 原 PDF 第 20 页 -->

## 附录 D 稠密+稀疏检索器 + 图扩展在 STaRK 数据集上的效果

### D.1 AMAZON

图 14 和图 15 给出 AMAZON 子集上合成查询与人工查询的 Recall@\(k\)。图扩展在所有 \(k\) 上都稳定提高召回。这与我们的观察一致：AMAZON 中的节点含有丰富的产品描述和特征丰富的元数据，为传播提供了充足的语义内容。一跳扩展策略可靠地提高相关节点的覆盖，又不引入噪声，相对稠密+稀疏基线有稳定增益。

**图 14：** AMAZON 上合成查询的 Recall@\(k\)。图扩展在所有 \(k\) 上都提高召回。

**图 15：** AMAZON 上人工查询的 Recall@\(k\)。图扩展稳定提高召回。

### D.2 MAG

图 16 和图 17 给出 MAG 的 Recall@\(k\)。这里图扩展主要在较大的 \(k\)（\(k \gtrsim 10\)）上有帮助，而在较小的 \(k\) 上召回可能下降。MAG 节点的标题和摘要较短，因此在小 \(k\) 上扩展图会引入弱相关邻居，损害靠前位置的检索。不过在更大的 \(k\) 上，图增强仍然提供额外的相关节点，提高召回，说明当可用候选更多时它是有用的。

**图 16：** MAG 上合成查询的 Recall@\(k\)。图扩展在较大 \(k\) 上提高召回，但在低 \(k\) 上有害。

**图 17：** MAG 上人工查询的 Recall@\(k\)。图扩展只在较大 \(k\) 上表现出增益。

### D.3 PRIME

图 18 和图 19 给出 PRIME 的 Recall@\(k\)。与 MAG 类似，图扩展的收益主要出现在较大的 \(k\)（\(k \gtrsim 20\)），而较低的 \(k\) 上召回略有下降。PRIME 节点含有简短的药物、通路和疾病描述，限制了语义传播。这些趋势强化了我们的发现：当节点具有丰富文本内容时，基于图的扩展最为有效。

**图 18：** PRIME 上合成查询的 Recall@\(k\)。图扩展只在较大 \(k\) 上有效。

<!-- 原 PDF 第 21 页 -->

**图 19：** PRIME 上人工查询的 Recall@\(k\)。图扩展主要在较大 \(k\) 上有帮助。

## 附录 E 实现细节

本系统采用两阶段设计：离线预处理与在线查询处理。离线阶段，我们使用 all-MiniLM-L6-v2 嵌入模型（384 维）（Wang et al., 2020）做语义分块和建图，并用 HNSW（\(M = 64\)）构建 ANN 索引；预处理在单块 NVIDIA A100 GPU 上执行一次。对显式模式图，我们把结构化数据存入 Neo4j 并在其中查询，同时从节点/字段抽取标题、实体等轻量元数据，以支持链接和检索。在线阶段，我们用线性融合结合稀疏与稠密信号（BM25 的 \(\alpha = 0.6\)，嵌入的 \(\beta = 0.4\)）来回答每个查询；在需要基于大语言模型的抽取或规划时，使用 GPT-4o-mini-2024-07-18（OpenAI et al., 2024）。

## 附录 F STaRK 的附加指标

表 20 给出所有方法在 AMAZON、MAG 和 PRIME 数据集上的 Hits@1、Hits@5 和 MRR。

## 附录 G 大语言模型元数据抽取的提示词

提示词中的省略号在 PDF 文本抽取里显示为「âĂę」，下文照录，不补写被省略的字段。

### G.1 表格块的实体抽取

**代码清单 2：** 表格元数据抽取提示词

你是一个表格元数据抽取引擎。给定带表头和行的表格数据，把它解析成一个合法的 JSON 对象，严格遵循下面的模式：

```
{{
"table_title": "<逐字使用的表标题；若没有则推断标题>",
"table_description": "<用一句话解释表格内容>",
"table_summary": "<由数据得出的简洁解释或洞见>",
"col_desc": {{
"<ColumnName1>": "<对该列所表示的内容、用途的上下文描述>",
âĂę
}},
"col_format": {{
"<ColumnName1>": "<数据格式说明：string、number、date（格式）等>",
âĂę
}},
"entities": {{
"<EntityName1>": {{
"type": "<person/place/organization/event/concept/thing>",
"category": "<named/non-named>",
"description": "<对该实体的简短描述>"
}},
âĂę
}}
}}
```

说明：

1. table_title：若有来源名称则使用它；否则根据数据推断一个描述性标题。
2. table_description：用一句话说明这张表包含的信息。
3. table_summary：对整体数据模式给出简短洞见或解释。
4. col_desc：对每个列名，提供该列表示什么、其用途和重要性的上下文描述。
5. col_format：对每个列名，说明数据格式（例如 string 表示姓名，number 表示分数，date（Month Day）表示日期）。
6. entities：抽取表中提到的全部唯一实体，并给出详细信息：

<!-- 原 PDF 第 22 页 -->

**表 20：** STaRK 数据集上的 Hits@1（H@1）、Hits@5（H@5）和平均倒数排名（MRR）。A = SPARK，G = SAGE，E = Edge。原 PDF 为一张宽表，这里按数据集拆开，数字不改。DPR 在 MAG 合成上的 10.51、35.23、21.34，以及在 PRIME 人工上的 2.04、9.18、7.05，在按行文本中因换行缺失，取自同页一次默认 find_tables 的对应列；该列分组与本表其余已对齐的行一致。若干 MAG 合成三元组与 AMAZON 合成三元组在抽取结果中相同，按原样保留。

**表 20（AMAZON）**

| 类别 | 方法 | 人工 H@1 | 人工 H@5 | 人工 MRR | 合成 H@1 | 合成 H@5 | 合成 MRR |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 稠密 | ada-002 | 39.50 | 64.19 | 52.65 | 29.08 | 49.61 | 38.62 |
| 稠密 | m-ada | 46.91 | 72.84 | 58.74 | 40.07 | 64.98 | 51.55 |
| 稠密 | DPR | 16.05 | 39.51 | 27.21 | 15.29 | 47.93 | 30.20 |
| 稀疏 | BM25 | 27.16 | 51.85 | 18.79 | 25.85 | 45.25 | 34.91 |
| 结构 | QAGNN | 22.22 | 49.38 | 31.33 | 12.88 | 39.01 | 29.12 |
| 混合 | 4Step | – | – | – | 47.60 | 67.60 | 56.50 |
| 混合 | FocusR | – | – | – | 64.00 | 76.20 | 69.30 |
| 混合 | D+B | 32.14 | 44.05 | 38.46 | 29.72 | 49.64 | 38.71 |
| 查询扩展 | HyDe | 45.68 | 72.84 | 57.56 | 28.98 | 50.10 | 39.58 |
| 查询扩展 | RAR | 55.56 | 71.60 | 62.15 | 39.02 | 52.87 | 39.58 |
| 查询扩展 | AGR | 55.56 | 71.60 | 63.54 | 39.29 | 53.66 | 46.20 |
| 查询扩展 | KAR | 61.73 | 72.84 | 66.32 | 50.47 | 65.37 | 57.51 |
| 智能体 | AvaTaR | 58.32 | 76.54 | 65.91 | 49.97 | 69.16 | 52.01 |
| 智能体 | ReACT | 45.65 | 71.73 | 58.81 | 42.14 | 64.56 | 52.30 |
| 智能体 | Reflex | 49.38 | 64.19 | 52.91 | 42.79 | 65.05 | 52.91 |
| 微调 | mFAR | – | – | – | 41.20 | 70.00 | 54.20 |
| 微调 | MoR | – | – | – | 52.20 | 74.60 | 62.20 |
| 本文 | SPARK | 22.22 | 58.03 | 39.93 | 26.72 | 54.27 | 36.24 |
| 本文 | A+G+E | 25.18 | 55.13 | 37.75 | 25.18 | 53.45 | 36.18 |
| 本文 | A+G-E | 28.41 | 63.84 | 42.48 | 28.41 | 55.13 | 42.48 |

**表 20（MAG）**

| 类别 | 方法 | 人工 H@1 | 人工 H@5 | 人工 MRR | 合成 H@1 | 合成 H@5 | 合成 MRR |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 稠密 | ada-002 | 28.57 | 41.67 | 35.81 | 29.08 | 49.61 | 38.62 |
| 稠密 | m-ada | 23.81 | 41.67 | 31.43 | 25.92 | 50.43 | 36.94 |
| 稠密 | DPR | 4.72 | 9.52 | 7.90 | 10.51 | 35.23 | 21.34 |
| 稀疏 | BM25 | 32.14 | 41.67 | 37.42 | 25.85 | 45.25 | 34.91 |
| 结构 | QAGNN | 20.24 | 26.19 | 25.53 | 12.88 | 39.01 | 29.12 |
| 混合 | 4Step | – | – | – | 53.80 | 69.20 | 61.40 |
| 混合 | FocusR | – | – | – | 74.10 | 84.20 | 78.80 |
| 混合 | D+B | 32.14 | 44.05 | 38.46 | 29.72 | 49.64 | 38.71 |
| 查询扩展 | HyDe | 33.33 | 44.05 | 38.95 | 28.98 | 50.10 | 39.58 |
| 查询扩展 | RAR | 38.10 | 45.24 | 42.04 | 39.02 | 52.87 | 39.58 |
| 查询扩展 | AGR | 33.33 | 44.05 | 38.95 | 39.29 | 53.66 | 46.20 |
| 查询扩展 | KAR | 51.20 | 58.30 | 54.20 | 50.47 | 65.37 | 57.51 |
| 智能体 | AvaTaR | 33.33 | 42.86 | 38.62 | 46.08 | 59.32 | 52.01 |
| 智能体 | ReACT | 27.27 | 40.00 | 33.94 | 31.07 | 49.49 | 39.25 |
| 智能体 | Reflex | 28.57 | 39.29 | 36.53 | 40.71 | 54.44 | 47.06 |
| 微调 | mFAR | – | – | – | 49.00 | 69.60 | 58.20 |
| 微调 | MoR | – | – | – | 58.20 | 78.30 | 67.10 |
| 本文 | SPARK | 44.40 | 54.80 | 49.40 | 41.00 | 56.41 | 49.30 |
| 本文 | A+G+E | 45.10 | 55.60 | 48.90 | 41.70 | 57.20 | 48.80 |
| 本文 | A+G-E | 43.20 | 58.70 | 49.40 | 43.20 | 60.00 | 49.30 |

**表 20（PRIME）**

| 类别 | 方法 | 人工 H@1 | 人工 H@5 | 人工 MRR | 合成 H@1 | 合成 H@5 | 合成 MRR |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 稠密 | ada-002 | 17.35 | 34.69 | 26.35 | 12.63 | 31.49 | 21.41 |
| 稠密 | m-ada | 24.49 | 39.80 | 32.98 | 15.10 | 33.56 | 23.49 |
| 稠密 | DPR | 2.04 | 9.18 | 7.05 | 4.46 | 21.85 | 12.38 |
| 稀疏 | BM25 | 22.45 | 41.84 | 30.37 | 12.75 | 27.92 | 19.84 |
| 结构 | QAGNN | 6.12 | 13.27 | 26.35 | 8.85 | 21.35 | 14.73 |
| 混合 | 4Step | – | – | – | 39.30 | 53.20 | 45.80 |
| 混合 | FocusR | – | – | – | 46.40 | 63.90 | 53.70 |
| 混合 | D+B | 24.77 | 43.12 | 33.25 | 13.71 | 31.13 | 21.39 |
| 查询扩展 | HyDe | 24.77 | 42.20 | 33.65 | 16.85 | 37.59 | 26.56 |
| 查询扩展 | RAR | 31.19 | 43.12 | 37.72 | 22.23 | 40.84 | 30.93 |
| 查询扩展 | AGR | 32.11 | 49.54 | 39.27 | 25.85 | 44.41 | 35.04 |
| 查询扩展 | KAR | 44.95 | 60.55 | 44.51 | 30.35 | 49.30 | 39.22 |
| 智能体 | AvaTaR | 33.03 | 51.37 | 41.00 | 20.10 | 39.89 | 29.18 |
| 智能体 | ReACT | 21.73 | 33.33 | 28.20 | 15.28 | 31.95 | 22.76 |
| 智能体 | Reflex | 16.52 | 33.03 | 23.99 | 14.28 | 34.99 | 24.82 |
| 微调 | mFAR | – | – | – | 40.90 | 62.80 | 51.20 |
| 微调 | MoR | – | – | – | 36.40 | 60.00 | 46.90 |
| 本文 | SPARK | 41.66 | 61.14 | 52.53 | 29.12 | 48.31 | 41.94 |
| 本文 | A+G+E | 42.20 | 61.60 | 51.53 | 30.14 | 49.56 | 42.79 |
| 本文 | A+G-E | 40.23 | 65.40 | 52.53 | 30.86 | 51.48 | 43.20 |

（续代码清单 2）

- type：person、place、organization、event、concept、thing 等。
- category：named（专有名词）或 non-named（普通名词/概念）。
- description：简要说明该实体表示什么。

输出：只要纯 JSON。不要 Markdown，也不要注释。

单样本示例（原文抽取为 “OneâĂŘShot Example”）：

表来源名称："1911 Notre Dame Fighting Irish football team - Schedule"

表数据：

```
[
{{
"Date": "October 7",
"Opponent": "Ohio Northern",
"Site": "Cartier Field South Bend, IN",
"Result": "W 32-6"
}},
{{
"Date": "October 14",
"Opponent": "St. Viator",
"Site": "Cartier Field South Bend, IN",
"Result": "W 43-0"
}},
{{
"Date": "October 21",
"Opponent": "Butler",
"Site": "Cartier Field South Bend, IN",
"Result": "W 27-0"
}}
]
```

期望输出：

```
{{
"table_title": "1911 Notre Dame Fighting Irish football team - Schedule",
"table_description": "本表给出 1911 年 Notre Dame Fighting Irish 橄榄球队的赛程和结果。",
"table_summary": "Notre Dame 赛季表现强劲，在主场多次获胜，对各个对手都稳定地得到高分。",
"col_desc": {{
"Date": "1911 赛季每场橄榄球比赛的预定日期",
"Opponent": "Notre Dame 在每场比赛中对阵的对方橄榄球队
```

<!-- 原 PDF 第 23 页 -->

```
",
"Site": "每场比赛的场馆和地点，包括主场和客场",
"Result": "每场比赛的最终结果和比分，显示 Notre Dame 的表现"
}},
"col_format": {{
"Date": "string - date（Month Day 格式）",
"Opponent": "string - 队名",
"Site": "string - 带场馆细节的地点",
"Result": "string - 比赛结果（W/T/L 后接比分）"
}},
"entities": {{
"Notre Dame Fighting Irish": {{
"type": "organization",
"category": "named",
"description": "University of Notre Dame 的大学橄榄球队"
}},
"Ohio Northern": {{
"type": "organization",
"category": "named",
"description": "对阵的大学橄榄球队"
}},
"St. Viator": {{
"type": "organization",
"category": "named",
"description": "对阵的大学橄榄球队"
}},
"Butler": {{
"type": "organization",
"category": "named",
"description": "对阵的大学橄榄球队"
}},
"Cartier Field": {{
"type": "place",
"category": "named",
"description": "Notre Dame 的主场橄榄球场"
}},
"South Bend": {{
"type": "place",
"category": "named",
"description": "Indiana 州 Notre Dame 所在的城市"
}},
"IN": {{
"type": "place",
"category": "named",
"description": "Indiana 州的缩写"
}}
}}
}}
```

现在，分析这份表格数据：

表来源名称："{source_name}"

表数据：

{table_content}

### G.2 文档块的实体抽取

**代码清单 3：** 文档元数据抽取提示词

你是一个元数据抽取引擎。给定一块文本，把它解析成一个合法的 JSON 对象，严格遵循下面的模式：

```
{
"entities": {
"<EntityName1>": {
"details": [
"<详细属性或描述句>",
âĂę
]
},
âĂę
},
"events": {
"<EventName1>": {
"date": "<YYYY-MM-DD 或 null>",
"details": "<一句话说明其上下文或重要性>"
},
âĂę
},
"timeline": [
"<ISO 日期 - 描述>",
âĂę
],
"topic": "<用一句话描述整体内容>"
}
```

说明：

1. entities：每个唯一的命名实体一个键（不是名词短语）。昵称和缩写算作单独的实体，但必须在 details 中提到原名（例如 ORIGINAL: ...）。
   - details：以该实体为主语的、有区分度的描述句或属性。
2. events：每个命名事件一个键。
   - date：ISO 日期或 null。
   - details：用一句话概括其重要性。
3. timeline：按时间顺序排列的数组，对所有带日期的提及写成 “<日期> - <简短描述>”。
4. topic：用一句话概括整体主题。

输出：只要纯 JSON。不要 Markdown，也不要注释。

注意：每个对象的键必须唯一。

单样本示例

输入文本

Bixente Jean Michel Lizarazu（巴斯克语发音：[biËĹÊČente liËĹsÌłaraËŇsÌłu]，1969 年 12 月 9 日出生）是一名法国前

<!-- 原 PDF 第 24 页 -->

职业足球运动员，司职左后卫。

他在 Bordeaux 逐级升上，并在 1989–1990 赛季的法国甲级联赛中获得第二名。球队随后降级，但在 1991–92 赛季从乙级联赛升级。他所在的 Bordeaux 队在 1995–96 赛季的 UEFA Cup 中获得亚军。

1997 年，他加盟 Bayern Munich，赢得六次 Bundesliga 冠军以及 2000–01 赛季的 UEFA Champions League，并在决赛点球大战中取得进球。

期望输出

```
{
"entities": {
"Bixente Jean Michel Lizarazu": {
"details": [
"巴斯克语发音：[biËĹÊČente liËĹsÌłaraËŇsÌłu]",
"前职业足球运动员",
"代表法国参加国际比赛",
"1969 年 12 月 9 日出生",
"司职左后卫"
]
},
"Bordeaux FC": {
"details": [
"法国足球俱乐部",
"Lizarazu 开始职业生涯的俱乐部"
]
},
"Bayern Munich": {
"details": [
"Lizarazu 于 1997 年加盟的德国俱乐部",
"Bundesliga 的顶级俱乐部"
]
},
"Bundesliga": {
"details": [
"德国足球的顶级联赛"
]
},
"France": {
"details": [
"Lizarazu 出生并开始足球生涯的国家"
]
},
"French First Division": {
"details": [
"法国顶级足球联赛（现为 Ligue 1）"
]
},
"French Second Division": {
"details": [
"法国第二级足球联赛（现为 Ligue 2）"
]
}
},
"events": {
"1989-1990 French First Division season": {
"date": "1989-1990",
"details": "在法国顶级联赛中的早期成功"
},
"1991-1992 French Second Division promotion": {
"date": "1991-1992",
"details": "降级后重返法国甲级联赛"
},
"1995-1996 UEFA Cup Final": {
"date": "1996-05-08",
"details": "一家法国俱乐部的重要欧洲决赛"
},
"1997 Transfer to Bayern Munich": {
"date": "1997-07-01",
"details": "从法国足球转会到德国足球"
},
"2001 UEFA Champions League Final": {
"date": "2001-05-23",
"details": "Lizarazu 随德国俱乐部获得欧洲冠军"
}
},
"timeline": [
"1969-12-09 - Bixente Jean Michel Lizarazu 在法国出生",
"1989-08-xx - 1989-1990 法国甲级联赛赛季开始",
"1991-08-xx - 1991-1992 法国乙级联赛赛季开始",
"1996-05-08 - 1995-1996 UEFA Cup 决赛",
"1997-07-01 - Lizarazu 加盟 Bundesliga 中的 Bayern Munich",
"2001-05-23 - 2001 UEFA Champions League 决赛"
],
"topic": "Bixente Lizarazu 在法国和德国的俱乐部生涯进程与主要成就，包括法国和德国的国内联赛"
}
```

关键要求：

- 纳入文本中直接或间接提到的每一个实体或事件。
- 确保所有分隔符和引号位置正确。
- 核实你的输出是合法的 JSON。
