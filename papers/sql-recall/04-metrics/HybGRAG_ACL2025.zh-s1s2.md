# HybGRAG: Hybrid Retrieval-Augmented Generation on Textual and Relational Knowledge Bases

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`HybGRAG_ACL2025.pdf`。

## Abstract 摘要

给定一个半结构化知识库（semi-structured knowledge base, SKB），其中文本文档由关系相互连接，我们如何有效检索相关信息来回答用户问题？检索增强生成（Retrieval-Augmented Generation, RAG）检索文档，以辅助大语言模型（large language models, LLMs）做问答；图 RAG（Graph RAG, GRAG）则以结构化知识库为知识来源。然而，许多问题需要同时用到 SKB 中的文本信息与关系信息——称为“混合”（hybrid）问题——这使检索过程变复杂，也说明需要一种同时利用两类信息的混合检索方法。本文通过实证分析识别出关键洞见，说明现有方法为何难以在 SKB 上做混合问答（hybrid question answering, HQA）。基于这些洞见，我们提出用于 HQA 的 HybGRAG，它由检索器库（retriever bank）和评论模块（critic module）组成，并具有以下优点：（1）具有智能体性（Agentic），它通过纳入评论模块的反馈自动精炼输出；（2）具有自适应性（Adaptive），它用检索器库解决同时需要文本信息与关系信息的混合问题；（3）可解释（Interpretable），它以直观的精炼路径（refinement path）为决策提供依据；（4）有效（Effective），它在 HQA 基准上超过全部基线。在 STARK 基准上的实验中，HybGRAG 取得显著性能提升，Hit@1 的平均相对改进为 51%。

## 1 Introduction 引言

检索增强生成（Lewis et al., 2020; Guu et al., 2020）使大语言模型能够访问非结构化文档数据库中的信息。这使大语言模型能够处理未知事实，并借助额外文本信息解决开放域问答（Open-Domain Question Answering, ODQA）。图 RAG（GRAG）将这一概念扩展到从结构化知识库中检索信息，其中文档由关系相互连接。现有 GRAG 方法聚焦两个方向：从知识图谱（knowledge graphs, KGs）中抽取关系信息，并利用大语言模型做知识库问答（Knowledge Base Question Answering, KBQA）（Yasunaga et al., 2021; Sun et al., 2024; Jin et al., 2024; Mavromatis and Karypis, 2024）；以及在数据库中的文档之间建立关系，以提升 ODQA 性能（Li et al., 2024a; Dong et al., 2024; Edge et al., 2024）。

最近出现的问题集中于“混合”问答（HQA）：在给定半结构化知识库（SKB）时，一个问题需要同时具备关系信息与文本信息才能被正确回答（Wu et al., 2024b）。SKB 由结构化知识库（即知识图谱）和非结构化文本文档组成，文本文档与知识图谱中的实体相关联。图 1 上方给出一个混合问题的例子，它同时涉及文本方面（论文主题）和关系方面（论文作者），SKB 在图中以圆柱表示。

尽管如此，我们的实证分析揭示了两个关键洞见，说明只做 RAG 或只做 GRAG 的现有方法不能有效处理 HQA，而 HQA 需要两种检索方法协同。第一，它们只专注于检索文本信息或关系信息中的一种。如图 1(a) 与 (b) 所示，当需要两种模态协同时，这一限制降低了它们的适用性。第二，在混合问题中，检索不同类型信息所需的方面未必容易区分。图 1(c) 使用问题路由（question routing）（Li et al., 2024b）来识别问题的各个方面。然而，一次不成功的路由会把文本方面 “nanofluid heat transfer papers” 与关系方面 “by John Smith” 混淆，从而导致错误检索。

图 1：HybGRAG 解决 SKB 中的混合问题。这类问题是半结构化的，同时涉及文本方面与关系方面。(a) RAG 忽略文档之间的相互连接，不能满足关系方面所规定的要求。(b) GRAG 只依赖关系方面，并把文本方面误识别为关系方面的一部分。(c) HybGRAG 通过自我反思精炼问题路由，并成功检索到 SKB 中的目标文档，同时处理文本方面与关系方面。图中混合问题可辨认为 “What nanofluid heat transfer papers have been published by John Smith?”。各面板内部把文本方面与关系方面拆开后的栏位交错，部分字符串粘连（如 “papershave”、“papers,by”），具体归属【抽取不清】。

表 1：HybGRAG 匹配全部性质，而基线各自缺少不止一项性质。可辨认的性质名称包括：1. Agentic；2. Adaptive，其下有 2.1. Questions in ODQA、2.2. Questions in KBQA、2.3. Questions in HQA；3. Interpretable。列名包括 Regular RAG、Think-on-Graph、AVATAR、HybGRAG。勾选符号因栏位错位【抽取不清】。

图 2：HybGRAG 在 STARK 上胜出，Hit@1 最多高出基线 21%。图中另有 “21% Higher” 与 “10% Higher” 两处标注；它们各自对应哪条基线【抽取不清】。

为解决 SKB 上的 HQA，我们提出 HybGRAG。HybGRAG 用检索器库处理混合问题，同时利用文本信息与关系信息。为提高检索准确率，HybGRAG 进行自我反思（self-reflection）（Renze and Guven, 2024），根据精心设计的评论模块所给反馈，迭代改进其问题路由。与被广泛视为可解释的思维链（chain-of-thought, CoT）（Wei et al., 2022）类似，HybGRAG 的精炼路径为性能提升提供直观解释。最后，HybGRAG 的框架被设计为灵活的，可以容易地适配不同问题。我们将 HybGRAG 的贡献总结如下：

1. 具有智能体性：它用自我反思自动精炼问题路由；
2. 具有自适应性：它用统一框架解决文本问题、关系问题与混合问题；
3. 可解释：它以直观的精炼路径为决策提供依据；
4. 有效：它在真实世界 HQA 基准上优于全部基线。

如表 1 所示，HybGRAG 是唯一满足全部性质并解决 SKB 上 HQA 的工作。如图 2 所示，在 HQA 基准 STARK 上评价时，HybGRAG 优于次优基线，Hit@1 在 STARK-MAG 与 STARK-PRIME 上的相对改进分别为 47% 与 55%。

## 2 Proposed Insights: Challenges in HQA 提出的洞见：HQA 中的挑战

SKB 上的 HQA 还有哪些现有方法未能解决的新挑战？本节先定义 HQA 问题，再通过实验揭示两个关键洞见，为设计 HQA 方法奠定基础。

### 2.1 Problem Definition 问题定义

半结构化知识库（SKB）包含一个知识图谱 G = (E, R)，其中 E 与 R 分别表示实体集合与关系集合。它还包含文本文档集合 D = ⋃_{i∈E} D_i，其中 D_i 是与实体 i 相关联的文档。实体类型与关系类型分别记为 T_E 与 T_R。SKB 中的每个混合问题 q 都涉及半结构化信息，即文本信息与关系信息。我们将混合问答（HQA）定义如下：

- 给定由 G = (E, R) 与 D 组成的 SKB，以及一个混合问题 q。
- 检索文档集合 X ⊆ E，其中每篇文档都满足 q 的关系方面与文本方面所规定的要求。

### 2.2 C1: Hybrid-Sourcing Question 挑战 1：混合来源问题

为考察回答混合问题是否必须同时利用文本信息与关系信息，我们做了一项实验，表明文本文档与知识图谱包含有用但互不重叠的信息。作为只使用文本信息的检索器，向量相似度搜索（vector similarity search, VSS）（Karpukhin et al., 2020）在嵌入空间（“ada-002”）中比较问题与文档，从而完成检索与排序；作为只使用关系信息的检索器，个性化 PageRank（Personalized PageRank, PPR）（Andersen et al., 2006）从由大语言模型（Claude 3 Sonnet）识别出的主题实体出发做随机游走，并按知识图谱中的连通性对相邻实体排序。

在表 2 中，文本检索器与图检索器的性能相当。有趣的是，如果一种最优路由总能选中给出正确结果的检索器，性能会显著更高，说明文本检索器与图检索器的优势重叠很少。这突出了一种解决方案的重要性：通过协同这两种检索器，同时利用文本信息与关系信息。在图 1(c) 中，我们展示了一个需要同时具备文本信息与关系信息才能回答的混合问题。基于这一观察，我们揭示第一个挑战：

表 2：在 STARK-MAG 上，文本信息与关系信息对回答混合问题都有用。

| Method | Hit@1 | Hit@5 |
| --- | --- | --- |
| Text Retriever: VSS | 0.2908 | 0.4961 |
| Graph Retriever: PPR | 0.2533 | 0.5523 |
| Optimal Routing | 0.4522 | 0.7463 |

挑战 1（Hybrid-Sourcing Question）。在 HQA 中，存在必须同时具备文本信息与关系信息才能回答的问题。

### 2.3 C2: Refinement-Required Question 挑战 2：需要精炼的问题

KBQA 的成功往往依赖于一个假设：目标实体位于从知识图谱中抽出的子图之内（Lan et al., 2022）。类似地，回答 HQA 中的问题也需要从 SKB 的知识图谱中抽出子图。由于混合问题同时涉及文本方面与关系方面，大语言模型可能难以理解它们。为研究这一点，我们测试大语言模型能否抽出一个包含目标实体的子图（记为命中，hit）。更具体地说，我们提示一个大语言模型（Claude 3 Sonnet）识别问题中的关系方面，即用于抽出子图的主题实体与有用关系。若子图未包含目标实体，则由一个预言机（oracle）指示大语言模型带着反馈再做一轮迭代。

表 3：在 STARK-MAG 上，大语言模型经常从 SKB 的知识图谱中抽出不含目标实体的子图。

| # of Iterations | Feedback Type | Hit Rate |
| --- | --- | --- |
| 1 | N/A | 0.6769 |
| 2 | Simple | 0.7914 |
| 2 | Corrective | 0.9231 |

在表 3 中，如果结果不正确，仅仅提示大语言模型重新抽取，就能得到高得多的命中率。此外，如果大语言模型收到指出抽取错误部分的反馈（例如抽出的主题实体是错的），结果会显著改善。这是因为在同时包含文本方面与关系方面的混合问题中，大语言模型可能把文本方面误识别为关系方面。在图 1(c) 中，大语言模型在检索正确参照时出错：它在第一次尝试中把文本方面混淆为类型 “field of study” 的实体。基于这一观察，我们揭示第二个挑战：

挑战 2（Refinement-Required Question）。在 HQA 中，大语言模型在第一次尝试时难以区分问题的文本方面与关系方面，因此需要进一步精炼。
