- 原文件名：HybGRAG_ACL2025.pdf
- 原标题：HYBGRAG: Hybrid Retrieval-Augmented Generation on Textual and Relational Knowledge Bases
- 中文标题：HYBGRAG：面向文本知识库与关系知识库的混合检索增强生成
- 作者：Meng-Chieh Lee, Qi Zhu, Costas Mavromatis, Zhen Han, Soji Adeshina, Vassilis N. Ioannidis, Huzefa Rangwala, Christos Faloutsos
- 会议：Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL 2025, Volume 1: Long Papers), pages 879–893, July 27 – August 1, 2025

<!-- 原 PDF 第 1 页 -->

Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 879–893。2025 年 7 月 27 日至 8 月 1 日。©2025 Association for Computational Linguistics。

# HYBGRAG：面向文本知识库与关系知识库的混合检索增强生成

Meng-Chieh Lee^1,*，Qi Zhu^2,†，Costas Mavromatis^2，Zhen Han^2，Soji Adeshina^2，Vassilis N. Ioannidis^2,†，Huzefa Rangwala^2，Christos Faloutsos^1,2,†

^1 Carnegie Mellon University，^2 Amazon

{mengchil,christos}@cs.cmu.edu，{qzhuamzn,mavrok,zhenhz,adesojia,ivasilei,rhuzefa}@amazon.com

## 摘要

给定一个半结构化知识库（semi-structured knowledge base, SKB），其中文本文档由关系相互连接，我们如何有效检索相关信息来回答用户问题？检索增强生成（Retrieval-Augmented Generation, RAG）检索文档，以辅助大语言模型（large language model, LLM）进行问答；而图 RAG（Graph RAG, GRAG）则以结构化知识库作为知识来源。然而，许多问题同时需要来自 SKB 的文本信息与关系信息——这类问题称为“混合”问题——这使检索过程更为复杂，也凸显了同时利用两类信息的混合检索方法的必要性。本文通过实证分析，识别出若干关键洞见，说明现有方法为何难以在 SKB 上完成混合问答（hybrid question answering, HQA）。基于这些洞见，我们提出用于 HQA 的 HYBGRAG，它由检索器库（retriever bank）和批评模块（critic module）组成，并具有以下优点：（1）智能体式（Agentic），它通过纳入批评模块的反馈，自动改进输出；（2）自适应（Adaptive），它借助检索器库解决同时需要文本信息与关系信息的混合问题；（3）可解释（Interpretable），它以直观的改进路径为决策提供依据；（4）有效（Effective），它在 HQA 基准上超过全部基线。在 STaRK 基准上的实验中，HYBGRAG 取得显著性能提升，Hit@1 的平均相对改进为 51%。

## 1 引言

检索增强生成（RAG）（Lewis et al., 2020; Guu et al., 2020）使大语言模型能够访问非结构化文档数据库中的信息。这使得 LLM 能够处理未知事实，并借助额外的文本信息解决开放域问答（Open-Domain Question Answering, ODQA）。图 RAG（GRAG）扩展了这一思路，从结构化知识库中检索信息，在这类知识库中，文档由关系相互连接。现有 GRAG 方法主要沿两个方向展开：一是从知识图谱（knowledge graph, KG）中抽取关系信息，并利用 LLM 进行知识库问答（Knowledge Base Question Answering, KBQA）（Yasunaga et al., 2021; Sun et al., 2024; Jin et al., 2024; Mavromatis and Karypis, 2024）；二是在数据库中的文档之间建立关系，以提升 ODQA 性能（Li et al., 2024a; Dong et al., 2024; Edge et al., 2024）。

最近，一个新兴问题集中于“混合”问答（HQA）：在给定半结构化知识库（SKB）的条件下，一个问题需要同时使用关系信息与文本信息才能被正确回答（Wu et al., 2024b）。SKB 由结构化知识库（即知识图谱 KG）和非结构化文本文档组成，其中文本文档与 KG 中的实体相关联。图 1 上方给出一个混合问题的例子，它同时涉及文本方面（论文主题）和关系方面（论文作者），而 SKB 被画成圆柱体。

尽管如此，通过实证分析，我们发现两个关键洞见，表明只做 RAG 或只做 GRAG 的现有方法无法有效应对 HQA，而 HQA 需要两种检索方法协同。第一，它们只专注于检索文本信息或关系信息中的一种。如图 1(a) 和 (b) 所示，当需要两种模态协同工作时，这一局限降低了它们的适用性。第二，在混合问题中，检索不同类型信息所需的方面可能并不容易区分。图 1(c) 中执行了问题路由（question routing）（Li et al., 2024b），以识别问题的各个方面。然而，在一次不成功的路由中，文本方面“nanofluid heat transfer papers”（纳米流体传热论文）与关系方面“by John Smith”（由 John Smith 发表）发生混淆，导致检索错误。

\* 该工作完成于作者在 Amazon 实习期间。

† 通讯作者。

<!-- 原 PDF 第 2 页 -->

**图 1：** HYBGRAG 解决 SKB 中的混合问题。SKB 是半结构化的，同时涉及文本方面与关系方面。(a) RAG 忽略文档之间的相互连接，因而不能满足关系方面所规定的要求。(b) GRAG 只依赖关系方面，并把文本方面误识为关系方面的一部分。(c) HYBGRAG 通过自我反思改进问题路由，并成功检索到 SKB 中的目标文档，同时覆盖文本方面与关系方面。

图中文字：

- 混合问题：What nanofluid heat transfer papers have been published by John Smith?（John Smith 发表过哪些纳米流体传热论文？）
- (a) RAG
  - 检索
  - 文本方面：What nanofluid heat transfer papers have been published by John Smith.
  - 关系方面：无（None）
- (b) GRAG
  - 检索
  - 关系方面：nanofluid heat transfer papers, by John Smith
  - 文本方面：无（None）
- (c) HybGRAG（本文方法）
  - 改进（Refine）
  - 检索
  - 关系方面：by John Smith
  - 文本方面：nanofluid heat transfer papers
  - 另一处关系方面标注：nanofluid heat transfer papers, by John Smith

**表 1：** HYBGRAG 符合全部性质，而各基线均缺少不止一项性质。

表抽取失败，见原 PDF 第 2 页。

文本层能读到的表头与行标签如下，但勾选符号与列的对应关系在抽取结果中无法对齐，因此不列出勾选，以免把符号编到错误的方法上。

- 列名：Property（性质）、Regular RAG、Think-on-Graph、AVATAR、HYBGRAG
- 1. Agentic（智能体式）
- 2. Adaptive（自适应）
  - 2.1. Questions in ODQA（ODQA 中的问题）
  - 2.2. Questions in KBQA（KBQA 中的问题）
  - 2.3. Questions in HQA（HQA 中的问题）
- 3. Interpretable（可解释）

抽取文本中还出现符号 ✔ 与 ?，以及图中标注 “21% Higher”（高 21%）、“10% Higher”（高 10%），但它们与单元格的对应关系未能可靠还原。

**图 2：** HYBGRAG 在 STaRK 上获胜，Hit@1 最多超出基线 21%。

为解决 SKB 上的 HQA，我们提出 HYBGRAG。HYBGRAG 用检索器库处理混合问题，该检索器库同时利用文本信息与关系信息。为提高检索准确率，HYBGRAG 执行自我反思（self-reflection）（Renze and Guven, 2024），根据精心设计的批评模块所给反馈，迭代改进其问题路由。与被广泛视为可解释的思维链（chain-of-thought, CoT）（Wei et al., 2022）类似，HYBGRAG 的改进路径为性能提升提供直观解释。最后，HYBGRAG 的框架被设计为灵活的，可以方便地适配不同问题。我们将 HYBGRAG 的贡献总结如下：

1. 智能体式：它通过自我反思自动改进问题路由；
2. 自适应：它用统一框架解决文本问题、关系问题与混合问题；
3. 可解释：它以直观的改进路径为决策提供依据；
4. 有效：它在真实世界的 HQA 基准上优于全部基线。

如表 1 所示，HYBGRAG 是唯一满足全部性质并解决 SKB 上 HQA 的工作。如图 2 所示，在 HQA 基准 STaRK 上评估时，HYBGRAG 优于次优基线，在 STaRK-MAG 和 STaRK-PRIME 上的 Hit@1 相对改进分别为 47% 和 55%。

<!-- 原 PDF 第 3 页 -->

## 2 所提出的洞见：HQA 中的挑战

在 SKB 上的 HQA 中，还有哪些现有方法尚未解决的新挑战？本节首先定义 HQA 问题，然后通过实验揭示两个关键洞见，为设计我们的 HQA 方法奠定基础。

### 2.1 问题定义

半结构化知识库（SKB）包含一个知识图谱 $G = (E, R)$，其中 $E$ 与 $R$ 分别表示实体集合与关系集合。它还包含一组文本文档 $D = \text{S}_{i \in E} D_i$，其中 $D_i$ 是与实体 $i$ 相关联的文档。公式抽取不完整，见原 PDF 第 3 页。实体类型与关系类型分别记为 $T_E$ 与 $T_R$。SKB 中的每个混合问题 $q$ 都涉及半结构化信息，即文本信息与关系信息。我们将混合问答（HQA）定义如下：

- 给定由 $G = (E, R)$ 和 $D$ 组成的 SKB，以及一个混合问题 $q$。
- 检索一组文档 $X \subseteq E$，其中每个文档都满足 $q$ 的关系方面与文本方面所规定的要求。

### 2.2 挑战 1：混合来源问题

为考察回答混合问题是否必须同时利用文本信息与关系信息，我们进行实验，表明文本文档与 KG 包含有用但互不重叠的信息。作为只使用文本信息的检索器，向量相似度搜索（vector similarity search, VSS）（Karpukhin et al., 2020）通过在嵌入空间（“ada-002”）中比较问题与文档来完成检索和排序；作为只使用关系信息的检索器，个性化 PageRank（Personalized PageRank, PPR）（Andersen et al., 2006）从由 LLM（Claude 3 Sonnet）识别出的主题实体出发进行随机游走，并根据 KG 中的连通性对邻近实体排序。

在表 2 中，文本检索器与图检索器具有相近的性能。有趣的是，如果一种最优路由总能选中给出正确结果的那个检索器，性能会显著更高，这表明文本检索器与图检索器的优势之间重叠很少。这凸显了通过协同这两个检索器、同时利用文本信息与关系信息的解决方案的重要性。在图 1(c) 中，我们展示了一个需要同时使用文本信息与关系信息才能回答的混合问题。基于这一观察，我们揭示第一个挑战：

**表 2：** 文本信息与关系信息对于回答 STaRK-MAG 中的混合问题都有用。

| 方法 | Hit@1 | Hit@5 |
| --- | --- | --- |
| 文本检索器：VSS | 0.2908 | 0.4961 |
| 图检索器：PPR | 0.2533 | 0.5523 |
| 最优路由（Optimal Routing） | 0.4522 | 0.7463 |

**挑战 1（混合来源问题，Hybrid-Sourcing Question）。** 在 HQA 中，存在必须同时使用文本信息与关系信息才能回答的问题。

### 2.3 挑战 2：需要改进的问题

KBQA 的成功往往依赖于如下假设：目标实体位于从 KG 中抽取的子图之内（Lan et al., 2022）。类似地，回答 HQA 中的问题也需要从 SKB 的 KG 中抽取子图。由于混合问题同时涉及文本方面与关系方面，LLM 可能难以理解它们。

为研究这一点，我们测试 LLM 能否抽取出包含目标实体的 KG 子图（命中，hit）。更具体地说，提示 LLM（Claude 3 Sonnet）识别问题中的关系方面，即用于抽取子图的主题实体和有用关系。若目标实体不在子图中，则使用一个预言机（oracle）指示 LLM 根据反馈再进行一轮迭代。

在表 3 中，如果结果不正确，仅仅提示 LLM 重新抽取，就能得到高得多的命中率。此外，如果 LLM 收到指出抽取错误部分的反馈（例如，抽取出的主题实体是错的），结果会显著改善。这是因为在同时包含文本方面与关系方面的混合问题中，LLM 可能把文本方面错误地识别为关系方面。在图 1(c) 中，LLM 在检索正确参照时出现错误，因为它在第一次尝试中把文本方面混淆为类型为“field of study”（研究领域）的实体。基于这一观察，我们揭示第二个挑战：

**表 3：** 在 STaRK-MAG 中，LLM 经常从 SKB 的 KG 中抽取出不含目标实体的子图。

| 迭代次数 | 反馈类型 | 命中率（Hit Rate） |
| --- | --- | --- |
| 1 | N/A | 0.6769 |
| 2 | Simple（简单） | 0.7914 |
| 2 | Corrective（纠正性） | 0.9231 |

**挑战 2（需要改进的问题，Refinement-Required Question）。** 在 HQA 中，LLM 在第一次尝试时难以区分问题的文本方面与关系方面，因此需要进一步改进。

<!-- 原 PDF 第 4 页 -->

## 3 所提出的方法：HYBGRAG

为解决 HQA，我们提出 HYBGRAG。它由检索器库和批评模块组成，分别应对挑战 1 与挑战 2。

### 3.1 检索器库（针对挑战 1）

为解决挑战 1，我们提出检索器库，它由多个检索模块和一个路由器组成。给定问题 $q$，路由器决定检索模块的选择与用法，这一过程称为问题路由。随后，被选中的检索模块检索前 $K$ 个参照 $X$，如下一段所述。

**检索模块。** 我们设计两个检索模块，即文本检索模块与混合检索模块，分别从文本文档和 SKB 中检索信息。每个检索模块都包含一个检索器（retriever）和一个排序器（ranker），从而可以灵活覆盖广泛的问题。

文本检索模块针对给定问题 $q$，使用相似度搜索检索文档，例如稠密检索。它被设计为直接在文本文档中寻找答案。我们使用问题 $q$ 与文档 $D$ 在嵌入空间中的 VSS，同时作为检索器和排序器。当混合检索模块什么也抽取不出来时，通常使用这一模块。

混合检索模块以识别出的主题实体 $\hat{E}$ 和有用关系 $\hat{R}$ 作为输入。它使用图检索器抽取 $\hat{E}$ 的 ego-graph（自我中心子图）中、由 $\hat{R}$ 连接的实体。例如，在图 1 中，$\{\hat{E} = \{\text{John Smith}\},\ \hat{R} = \{\text{author writes paper}\}\}$，图检索器抽取由路径 “John Smith -> author writes paper -> {paper(s)}” 连接的实体/论文。如果抽取出多于一个 ego-graph，则使用它们的交集作为最终结果。最后，为解决混合问题，我们提出用问题 $q$ 与文档 $D$ 之间的 VSS 排序器，对与抽取出的实体相关联的文档进行排序。这保证了关系信息与文本信息之间的协同。

**路由器。** 给定问题 $q$，LLM 路由器执行问题路由，以决定检索模块的选择与用法。更具体地说，路由器首先根据实体类型 $T_E$ 和关系类型 $T_R$，利用少样本示例（Brown, 2020）识别关系方面，即主题实体 $\hat{E}$ 和有用关系 $\hat{R}$。随后路由器做出选择 $s_t$，决定使用文本检索模块还是混合检索模块。在确定 $s_t$ 之前先识别 $\hat{E}$ 和 $\hat{R}$，可以提高 $s_t$ 的质量。例如，如果没有抽取出实体，$\hat{E} = \emptyset$，则文本检索模块是更好的选择。

### 3.2 批评模块（针对挑战 2）

给定混合问题 $q$，路由器被要求执行问题路由，包括识别主题实体 $\hat{E}$ 和有用关系 $\hat{R}$。然而，如挑战 2 所述，它们在第一次迭代中可能被错误识别。

为解决这一问题，我们提出批评模块，它提供反馈，帮助路由器执行更好的问题路由。我们并不使用单一 LLM 来完成这一复杂任务，而是把批评者分为两部分：LLM 验证器 $C_{\mathrm{val}}$ 用于验证检索结果 $X$ 是否正确，LLM 评论器 $C_{\mathrm{com}}$ 在检索不正确时提供反馈 $f_t$。这一分而治之的步骤与先前工作类似（Gao et al., 2022; Asai et al., 2024），对我们的批评模块至关重要，并带来两个关键优点：（1）把一个困难任务拆成两个更容易的任务后，我们就可以利用预训练 LLM 来解决它们，同时保持良好性能。这解决了在没有标签、因而无法微调 LLM 批评者时的问题。（2）由于 $C_{\mathrm{val}}$ 与 $C_{\mathrm{com}}$ 的任务相互独立，它们可以各自拥有专属上下文，从而避免纳入无关信息，也避免“迷失在中间”（lost in the middle）现象（Shi et al., 2023; Liu et al., 2024）。

**验证器。** LLM 验证器 $C_{\mathrm{val}}$ 旨在验证检索到的顶部参照 $X$ 是否满足问题 $q$ 所规定的要求，这是一个二分类任务。为提高准确率，我们为验证器提供额外的验证上下文。我们使用主题实体与所抽取 ego-graph 中实体之间的推理路径作为验证上下文，用以核实输出是否满足问题中的某些要求。推理路径被表述为 “{topic entity} → {useful relation} → ... → {useful relation} → {neighboring entity}”。例如，如果混合问题询问某位特定作者的一篇论文（即一份文档），那么包含推理路径 “{author} → {writes} → {paper}” 的上下文对于验证是必不可少的。

**评论器。** LLM 评论器 $C_{\mathrm{com}}$ 旨在提供反馈 $f$，帮助路由器改进问题路由。为有效引导路由器，我们构造它容易理解的纠正性反馈。更具体地说，它指出

<!-- 原 PDF 第 5 页 -->

每一个动作中的错误，例如错误识别主题实体，如表 4 所示。与自然语言反馈不同——自然语言反馈可能因所用 LLM 不同而带来不确定性或不一致性——我们的纠正性反馈对如何改进问题路由给出明确指导。此外，它利用上下文学习（in-context learning, ICL）来提供精细的反馈。我们在训练集中收集少量成功经验（约 30 条）作为示例，每条经验 $\{s_t, \hat{E}_t, \hat{R}_t, f_{t+1}\}$ 由一对路由动作与反馈组成，并由真实标签（ground truth）核验。推理时，评论器根据多条预先收集的示例给出高质量反馈。

**表 4：** HYBGRAG 中批评模块针对 STaRK 的纠正性反馈。

| 错误来源 | 错误类型 | 反馈 |
| --- | --- | --- |
| 识别（Identification） | 实体/关系不正确（Incorrect Entity/Relation） | 实体/关系 {name} 不正确。请移除或替换该实体/关系。 |
|  | 缺少实体（Missing Entity） | 目前只有一个实体，但可能还有更多。请再抽取一个实体和一条关系。 |
|  | 无实体（No Entity） | 没有抽取出实体。请至少抽取一个实体和一条关系。 |
|  | 无交集（No Intersection） | 实体之间没有交集。请移除或替换一个实体和一条关系。 |
|  | 错误交集（Incorrect Intersection） | 实体之间存在交集，但答案不在该交集内。请移除或替换一个实体和一条关系。 |
| 选择（Selection） | 检索模块不正确（Incorrect Retrieval Module） | 检索到的文档不正确。当前检索模块可能无助于缩小搜索空间。 |

### 3.3 总体算法

HYBGRAG 的算法见算法 1。给定问题 $q$，在第 $t$ 次迭代中，路由器确定 $s_t$、$\hat{E}_t$ 和 $\hat{R}_t$，并用被选中的检索模块从 SKB 的 $G$ 与 $D$ 中、或仅从 $D$ 中检索参照 $X_t$。批评模块中的验证器 $C_{\mathrm{val}}$ 随后决定接受 $X_t$ 作为最终答案，还是拒绝它。如果 $X_t$ 被拒绝，评论器 $C_{\mathrm{com}}$ 生成反馈 $f_{t+1}$，供路由器在第 $t+1$ 次迭代中改进其动作。

**算法 1：HYBGRAG**

输入：问题 $q$，带有 $G$ 与 $D$ 的 SKB，实体类型 $T_E$，关系类型 $T_R$，以及最大迭代次数 $T$

```
1  f_1 = "";
2  for t = 1, ..., T do
3      /* 检索器库 */
4      s_t, Ê_t, R̂_t = Router(q, T_E, T_R, f_t);
5      if s_t 是混合检索模块 then
6          X_t = HybridRM(q, G, D, Ê_t, R̂_t);
7      else
8          X_t = TextRM(q, D);
9      /* 验证器 */
10     if C_val(q, X_t) = True then
11         Return X_t;
12     else
13         /* 评论器 */
14         f_{t+1} = C_com(q, s_t, Ê_t, R̂_t);
15 Return X_t;
```

## 4 实验

我们进行实验，以回答下列研究问题（research question, RQ）：

- RQ1. 有效性：HYBGRAG 在真实世界基准上表现如何？
- RQ2. 消融研究：HYBGRAG 中的全部设计选择是否都有必要？
- RQ3. 可解释性：HYBGRAG 如何根据反馈改进其问题路由？

**基准。** 我们在两个问答基准上进行实验：STaRK^1（Wu et al., 2024b），它是主要评测基准，并且聚焦于检索；以及 CRAG（Yang et al., 2024），它是用于评测端到端 RAG 性能的补充基准。STaRK 聚焦于 HQA，而 CRAG 把 ODQA 和 KBQA 都作为子问题涵盖在内。基准的详细描述见附录 A。

^1 由于法律问题，本文只使用 STaRK-MAG 与 STaRK-PRIME。

### 4.1 在 STaRK 上的检索评测

我们使用 STaRK 提供的默认评测指标，即 Hit@1、Hit@5、Recall@20 和平均倒数排名（mean reciprocal rank, MRR），来评测检索任务的性能。我们将 HYBGRAG 与多种基线比较，包括最近的 GRAG 方法（QAGNN（Yasunaga et al., 2021）和 Think-on-Graph（Sun et al., 2024））、传统 RAG 方法，以及自我反思式 LLM（ReAct（Yao et al., 2023）、Reflexion（Shinn et al., 2023）和 AVATAR（Wu et al., 2024a））。实现细节见附录 C。

<!-- 原 PDF 第 6 页 -->

**表 5：** 在 STaRK 上的检索评测：HYBGRAG 获胜。“*”表示由于这些方法的延迟和成本很高，只评测了 10% 的测试问题。原文在 “denotes our proposed method”（表示本文提出的方法）之前有一个标记符号，文本抽取时该符号丢失，见原 PDF 第 6 页。表中带 “(Ours)” 的行是本文方法。find_tables 把个别小数拆开（例如把 0.5820 拆成 0.5 与 820），下表数字按 `get_text` 中连续读出的数值填写，未另补未见过的数字。

| 方法 | STaRK-MAG Hit@1 | Hit@5 | Recall@20 | MRR | STaRK-PRIME Hit@1 | Hit@5 | Recall@20 | MRR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| QAGNN | 0.1288 | 0.3901 | 0.4697 | 0.2912 | 0.0885 | 0.2123 | 0.2963 | 0.1473 |
| Think-on-Graph* | 0.1316 | 0.1617 | 0.1130 | 0.1418 | 0.0607 | 0.1571 | 0.1307 | 0.1017 |
| Dense Retriever | 0.1051 | 0.3523 | 0.4211 | 0.2134 | 0.0446 | 0.2185 | 0.3013 | 0.1238 |
| VSS（文本检索模块） | 0.2908 | 0.4961 | 0.4836 | 0.3862 | 0.1263 | 0.3149 | 0.3600 | 0.2141 |
| Multi-VSS | 0.2592 | 0.5043 | 0.5080 | 0.3694 | 0.1510 | 0.3356 | 0.3805 | 0.2349 |
| VSS w/ LLM Reranker* | 0.3654 | 0.5317 | 0.4836 | 0.4415 | 0.1779 | 0.3690 | 0.3557 | 0.2627 |
| ReAct | 0.3107 | 0.4949 | 0.4703 | 0.3925 | 0.1528 | 0.3195 | 0.3363 | 0.2276 |
| Reflexion | 0.4071 | 0.5444 | 0.4955 | 0.4706 | 0.1428 | 0.3499 | 0.3852 | 0.2482 |
| AVATAR | 0.4436 | 0.5966 | 0.5063 | 0.5115 | 0.1844 | 0.3673 | 0.3931 | 0.2673 |
| 混合检索模块（本文） | 0.5028 | 0.5820 | 0.5031 | 0.5373 | 0.2492 | 0.3274 | 0.3366 | 0.2842 |
| HYBGRAG（本文） | 0.6540 | 0.7531 | 0.6570 | 0.6980 | 0.2856 | 0.4138 | 0.4358 | 0.3449 |
| 相对改进 | 47.4% | 26.2% | 29.3% | 36.5% | 54.9% | 12.7% | 10.9% | 29.0% |

**图 3：** HYBGRAG 在 STaRK 中的设计选择是必要的。我们将 HYBGRAG 与两个变体比较：没有验证上下文的验证器（Val. w/o Context），以及只有 5-shot 的评论器（Com. w/ 5-Shot）。Oracle 在推理时使用真实标签。图例还包括 HybGRAG 与 Oracle。横轴指标为 Hit@1、Hit@5、Recall@20、MRR。STaRK-MAG 一侧可见的纵轴刻度包括 0.5、0.6、0.7、0.8、0.9、1.0；STaRK-Prime 一侧可见的纵轴刻度包括 0.1、0.2、0.3、0.4、0.5、0.6。各柱的精确高度未被抽取为数据表，此处不编造。

**图 4：** 由于批评模块，HYBGRAG 改进了其问题路由。横轴为迭代次数（# of Iterations）1、2、3、4，纵轴为 Hit@1。图中同时画出 STaRK-Prime 与 STaRK-MAG。可见刻度包括 0.50、0.55、0.60、0.65，以及 0.26、0.28。各数据点的精确取值未被抽取为数据表，此处不编造。

**表 6：** 在 STaRK-MAG 上，HYBGRAG 在较弱的 LLM 上仍保持较强性能。

| 基座模型 | Hit@1 | Hit@5 | Recall@20 | MRR | 加速比（Speedup） |
| --- | --- | --- | --- | --- | --- |
| Claude 3 Haiku | 0.6019 | 0.7084 | 0.6067 | 0.6483 | 1.96× |
| Claude 3 Sonnet | 0.6540 | 0.7531 | 0.6570 | 0.6980 | 1.00× |

#### 4.1.1 有效性（RQ1）

在表 5 中，HYBGRAG 在 STaRK 的两个数据集上都显著优于全部基线。大多数基线被设计来处理 ODQA 和 KBQA，结果显示它们无法有效处理 HQA（挑战 1）。我们的混合检索模块是表现第二好的方法，这凸显了设计一个同时使用文本信息与关系信息的协同检索模块的重要性。此外，HYBGRAG 显著优于混合检索模块，表明在第一次迭代中抽取出的实体和关系经常是不正确的（挑战 2）。通过分别用检索器库和批评模块应对挑战 1 与挑战 2，HYBGRAG 的性能有显著提升。

#### 4.1.2 消融研究（RQ2）

**批评模块。** 我们将 HYBGRAG 的变体与以下设置比较：没有验证上下文的验证器、只有五条示例的评论器，以及带有预言机的设置。预言机可以访问真实标签，从而对输出是否正确、以及问题路由的错误类型（如果存在）给出最优判断。在图 3 中，我们表明 HYBGRAG

**表 7：** 在 STaRK-MAG 上，HYBGRAG 在多智能体设计下表现最好。“Router for SR”基线使用单一 LLM 路由器进行自我反思。

| 方法 | 设置 | Hit@1 | Hit@5 | Recall@20 | MRR |
| --- | --- | --- | --- | --- | --- |
| Hybrid RM | No-Agent（无智能体） | 0.5028 | 0.5820 | 0.5031 | 0.5373 |
| Router for SR | Single-Agent（单智能体） | 0.6206 | 0.7069 | 0.6187 | 0.6587 |
| HYBGRAG | Multi-Agent（多智能体） | 0.6540 | 0.7531 | 0.6570 | 0.6980 |

<!-- 原 PDF 第 7 页 -->

在我们的全部设计选择下表现最好，并接近预言机的性能。

**自我反思。** 在图 4 中，我们表明随着自我反思迭代次数增加，HYBGRAG 的性能进一步提升。当迭代次数从 1 增加到 2 时，性能提升显著；第 1 次迭代中不执行自我反思。图中还表明，少数几次迭代就足够了，因为改进幅度随迭代次数增加而减小。

**模型规模。** 尽管我们无法使用 Claude 3 Opus，我们用 Claude 3 Haiku 进行了实验。它比 Claude 3 Sonnet 更省成本，但能力更弱^2。在表 6 中，即使使用 Claude 3 Haiku，HYBGRAG 仍保持较强性能。结果也符合 LLM 的缩放定律（Kaplan et al., 2020）。

^2 https://www.anthropic.com/news/claude-3-family

**多智能体视角。** 由于 HYBGRAG 可以被理解为一个多智能体系统，我们增加一个单智能体基线，它依赖路由器做决策，并为自我反思提供反馈。在表 7 中，HYBGRAG 同时优于单智能体基线和无智能体基线。这凸显了自我反思对于在 HQA 中取得强性能是必要的，正如挑战 2 所指出的那样。此外，与单智能体基线生成的纯文本反馈不同，HYBGRAG 生成的反馈能更有效地引导路由器改进其决策，这得益于我们精心设计的批评模块。

#### 4.1.3 可解释性（RQ3）

图 5 展示了在 STaRK-MAG 中，检索器库里的路由器与批评模块之间交互的例子。在图 5(a) 的第一次迭代中，路由器把 “optical TALU implementations in electronic circuits” 误识别为代表研究领域（关系方面）的主题实体。由于基于该实体抽取出的 ego-graph 与基于 “Netaji Subhash Engineering College” 抽取出的 ego-graph 没有交集，批评模块识别出前一个实体更有可能是文本方面。因此，它把反馈给予路由器，并且

**图 5：** HYBGRAG 是可解释的。在来自 STaRK-MAG 的例子中，HYBGRAG 根据批评模块的纠正性反馈，成功改进了实体与关系抽取。

**(a) 错误类型：实体/关系不正确（Incorrect Entity/Relation）**

问：Netaji Subhash Engineering College 在 2012 年是否发表过关于电子电路中 optical TALU 实现的论文？（原文：Any 2012 publications from Netaji Subhash Engineering College on optical TALU implementations in electronic circuits?）

动作 1：

- 选择：混合检索模块
- 实体：Netaji Subhash Engineering College（institution，机构），optical TALU implementations in electronic circuits（field of study，研究领域）
- 关系：author affiliated with institution，author writes paper，paper has topic field of study

反馈 1：检索到的文档不正确。实体 “optical TALU implementations in electronic circuits” 和关系 “paper has topic field of study” 不正确。请移除或替换一个实体和一条关系。

动作 2：

- 选择：混合检索模块
- 实体：Netaji Subhash Engineering College（institution）
- 关系（原文标签为 Relational）：author affiliated with institution，author writes paper

反馈 2：接受。✅

**(b) 错误类型：缺少实体（Missing Entity）**

问：是否存在 “A Low Abundance of 135Cs in the Early Solar System from Barium Isotopic Signatures” 的共同作者在 2016 年发表的、讨论地球化学成分与球粒陨石（chondrites）化学成分比较的论文？（原文：Are there any 2016 publications by co-authors of "A Low Abundance of 135Cs in the Early Solar System from Barium Isotopic Signatures" which discuss the comparison of Earth's chemical composition with that of chondrites?）

动作 1：

- 选择：混合检索模块
- 实体：A Low Abundance of 135Cs in the Early Solar System from Barium Isotopic Signatures（paper，论文）
- 关系：author writes paper

反馈 1：检索到的文档不正确。目前只有一个实体，但可能还有更多。请再抽取一个实体和一条关系。

动作 2：

- 选择：混合检索模块
- 实体：A Low Abundance of 135Cs in the Early Solar System from Barium Isotopic Signatures（paper），chondrites（field of study）
- 关系（原文标签为 Relational）：author writes paper，paper has topic field of study

反馈 2：接受。✅

**表 8：** 在 CRAG 上的端到端 RAG 评测：HYBGRAG 获胜。除 CoT LLM 外，所有基线都共用我们的检索器库，但使用不同的批评者来提供反馈。原文在 “denotes our proposed method” 之前有一个标记符号，文本抽取时该符号丢失，见原 PDF 第 7 页。HYBGRAG (Ours) 是本文方法。Score$_a$ 的上标在抽取文本中写作 Scorea。

| 方法 | Llama 3.1 70B Accuracy ↑ | Halluc. ↓ | Missing | Score$_a$ ↑ | Claude 3 Sonnet Accuracy ↑ | Halluc. ↓ | Missing | Score$_a$ ↑ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CoT LLM | 0.4607 | 0.5026 | 0.0367 | -0.0419 | 0.3910 | 0.4052 | 0.2038 | -0.0142 |
| Text-Only RAG | 0.4105 | 0.3685 | 0.2210 | 0.0420 | 0.5034 | 0.3955 | 0.1011 | 0.1079 |
| Graph-Only RAG | 0.4861 | 0.4442 | 0.0697 | 0.0419 | 0.5303 | 0.2974 | 0.1723 | 0.2329 |
| Text & Graph RAG | 0.4120 | 0.3790 | 0.2090 | 0.0330 | 0.5820 | 0.3416 | 0.0764 | 0.2404 |
| ReAct | 0.1745 | 0.2360 | 0.5895 | -0.0615 | 0.4352 | 0.4075 | 0.1573 | 0.0277 |
| Corrective RAG | 0.4509 | 0.4652 | 0.0839 | -0.0143 | 0.4674 | 0.3333 | 0.1993 | 0.1341 |
| HYBGRAG（本文） | 0.5206 | 0.3588 | 0.1206 | 0.1618 | 0.6322 | 0.2959 | 0.0719 | 0.3363 |

<!-- 原 PDF 第 8 页 -->

路由器据此做出相应处理。HYBGRAG 的这一改进路径类似于 CoT，因而可解释，并且便于用户理解。STaRK-Prime 中的例子见附录 B.1。

### 4.2 在 CRAG 上的端到端 RAG 评测

我们对 HYBGRAG 做了修改，以适配 CRAG（细节见附录 C）。我们使用默认评测指标，由一个 LLM 评测器把答案标为准确（1）、不正确/幻觉（−1）或缺失（0），从而得到 Score$_a$。我们将 HYBGRAG 与 CoT LLM、仅文本 RAG、仅图 RAG，以及把文本参照与图参照拼接起来的 RAG 进行比较。我们还纳入一个智能体式 LLM（ReAct）和一个自我反思式 LLM（Corrective RAG），二者都共用我们的检索器库，但使用不同的批评者。

在表 8 中，HYBGRAG 在 CRAG 上优于全部基线。只带单一检索模块的 RAG 无法同时处理两类问题。使用拼接参照的 RAG 也会被长参照中的无关内容干扰。尽管已经提供我们的检索器库，智能体式基线和自我反思式基线仍然难以改进其动作。由于 ReAct 依赖 LLM 进行思考并提供自然语言反馈的能力，它往往缺乏明确指导。在没有经过微调的检索评测器时，Corrective RAG 无法有效识别一条参照是否有用。

### 4.3 模型成本分析

我们在表 9 和表 14 中分别报告 HYBGRAG 在 STaRK 与 CRAG 上、一次迭代中每一步的 API 调用次数和词元消耗（不含参照）。虽然大部分词元消耗来自用于 ICL 的示例，提示本身只需要很少的词元。此外，由于 HYBGRAG 使用对话式 LLM 作为路由器，用于 ICL 的示例只需要给出一次。与 STaRK 上的最先进基线 AVATAR 相比——AVATAR 在训练期间至少需要 500 次 API 调用——我们的混合检索模块只用 2 次 API 调用就在 Hit@1 上取得 24% 的相对改进，而 HYBGRAG 最多用 14 次 API 调用取得 51% 的相对改进，二者都不需要训练。

**表 9：** STaRK 的 API 调用次数与词元数。

| HYBGRAG 组件 | 每次迭代的 API 调用次数 | 提示的词元数 | MAG 中示例的词元数 | Prime 中示例的词元数 |
| --- | --- | --- | --- | --- |
| Router（路由器） | 2 | 159 | 2709 | 3018 |
| Validator（验证器） | 1 | 39 | 1383 | 2107 |
| Commenter（评论器） | 1 | 52 | 1215 | 1583 |

## 5 相关工作

**图 RAG（GRAG）。** GRAG 已经探索了多种设定（Peng et al., 2024），大致可以分为三个方向。第一个方向聚焦于 KBQA，利用 LLM 的能力（Yasunaga et al., 2021; Sun et al., 2024; Jin et al., 2024; Mavromatis and Karypis, 2024）。第二个方向聚焦于 ODQA，在文档之间建立关系以改进检索（Li et al., 2024a; Dong et al., 2024; Edge et al., 2024）。最后一个方向假设在回答问题时已经给定一个子图（He et al., 2024; Hu et al., 2024）。相比之下，本文聚焦于解决 SKB 上的 HQA，而先前的 GRAG 方法不容易推广到 HQA。

**智能体式与自我反思式 LLM。** LLM 智能体（Yao et al., 2023; Wu et al., 2024a）促进复杂推理任务中的规划。其中，AVATAR 是最新的工作，它通过对比较推理进行迭代式提示优化。然而，它们仍可能在第一次尝试时难以生成正确输出。自我反思通过根据反馈迭代优化输出来应对这一局限；反馈通常由批评者提供，而批评者可以用多种方法实现：预训练 LLM（Shinn et al., 2023; Madaan et al., 2023）、外部工具（Gou et al., 2024; Qiao et al., 2024），或经过微调的 LLM（Paul et al., 2024; Asai et al., 2024; Yan et al., 2024）。尽管如此，它们由于两个原因而不能推广到 HQA。第一，它们缺少合适的检索工具，也缺少关于如何有效改进检索的指导。第二，在没有外部工具或微调标签时，若不经仔细设计就把预训练 LLM 用作批评者，会导致不理想的自我评测，以及过于含蓄的反馈。

## 6 结论

为解决混合问答（HQA），我们提出 HYBGRAG。它由我们实证分析中的洞见所推动，并具有下列优点：

1. 智能体式：它通过我们的批评模块，用自我反思改进问题路由；
2. 自适应：它通过我们的检索器库解决文本问题、关系问题与混合问题；
3. 可解释：它以直观的改进路径为决策提供依据；
4. 有效：它在 HQA 基准上显著优于全部基线。

应用于 STaRK 时，HYBGRAG 在 Hit@1 上取得 51% 的平均相对改进。

<!-- 原 PDF 第 9 页 -->

## 局限性

虽然 HYBGRAG 能够在 HQA 上优于现有的 RAG 与 GRAG 方法，它仍有一些局限：（1）HYBGRAG 只使用了最简单的检索模块，多种替代方案尚未探索。例如，检索模块中的排序器可以替换为交叉编码器排序器，混合检索模块中的检索器也可以改用 PPR 的前 $K$ 个实体。（2）HYBGRAG 在领域适配方面没有显著优势。实验中，尽管 HYBGRAG 优于基线，它在 STaRK-Prime 上的性能差于 STaRK-MAG；学术界通常认为学术领域的复杂程度低于医学领域。（3）HYBGRAG 中的评论器（原文此处写作 commentor）在执行 ICL 时随机选择经验。例如，选择与当前问题最相关的经验，可能会带来更好的性能。这些局限指出了可能改进的地方，同时也给出了未来进一步增强 HYBGRAG 能力的方向。

## 参考文献

Reid Andersen, Fan Chung, and Kevin Lang. 2006. 使用 PageRank 向量进行局部图划分（Local graph partitioning using pagerank vectors）. In 2006 47th Annual IEEE Symposium on Foundations of Computer Science (FOCS’06), pages 475–486. IEEE.

Akari Asai, Zeqiu Wu, Yizhong Wang, Avirup Sil, and Hannaneh Hajishirzi. 2024. Self-RAG：通过自我反思学习检索、生成与批评（Self-RAG: Learning to retrieve, generate, and critique through self-reflection）. In The Twelfth International Conference on Learning Representations.

Tom B Brown. 2020. 语言模型是少样本学习者（Language models are few-shot learners）. arXiv preprint arXiv:2005.14165.

Jianlv Chen, Shitao Xiao, Peitian Zhang, Kun Luo, Defu Lian, and Zheng Liu. 2024. BGE M3-Embedding：借助自知识蒸馏得到的多语言、多功能、多粒度文本嵌入（Bge m3-embedding: Multi-lingual, multi-functionality, multi-granularity text embeddings through self-knowledge distillation）. arXiv preprint arXiv:2402.03216.

Jialin Dong, Bahare Fatemi, Bryan Perozzi, Lin F Yang, and Anton Tsitsulin. 2024. 别忘了把它们连起来！用基于图的重排序改进 RAG（Don’t forget to connect! improving rag with graph-based reranking）. arXiv preprint arXiv:2405.18414.

Darren Edge, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao, Apurva Mody, Steven Truitt, and Jonathan Larson. 2024. 从局部到全局：一种面向查询聚焦摘要的图 RAG 方法（From local to global: A graph rag approach to query-focused summarization）. arXiv preprint arXiv:2404.16130.

Luyu Gao, Zhuyun Dai, Panupong Pasupat, Anthony Chen, Arun Tejasvi Chaganty, Yicheng Fan, Vincent Y Zhao, Ni Lao, Hongrae Lee, Da-Cheng Juan, et al. 2022. RARR：用语言模型研究并修订语言模型所说的内容（Rarr: Researching and revising what language models say, using language models）. arXiv preprint arXiv:2210.08726.

Zhibin Gou, Zhihong Shao, Yeyun Gong, yelong shen, Yujiu Yang, Nan Duan, and Weizhu Chen. 2024. CRITIC：大语言模型可以借助与工具交互的批评进行自我纠正（CRITIC: Large language models can self-correct with tool-interactive critiquing）. In The Twelfth International Conference on Learning Representations.

Kelvin Guu, Kenton Lee, Zora Tung, Panupong Pasupat, and Mingwei Chang. 2020. 检索增强的语言模型预训练（Retrieval augmented language model pre-training）. In International conference on machine learning, pages 3929–3938. PMLR.

Xiaoxin He, Yijun Tian, Yifei Sun, Nitesh V Chawla, Thomas Laurent, Yann LeCun, Xavier Bresson, and Bryan Hooi. 2024. G-Retriever：面向文本图理解与问答的检索增强生成（G-retriever: Retrieval-augmented generation for textual graph understanding and question answering）. arXiv preprint arXiv:2402.07630.

Yuntong Hu, Zhihan Lei, Zheng Zhang, Bo Pan, Chen Ling, and Liang Zhao. 2024. GRAG：图检索增强生成（Grag: Graph retrieval-augmented generation）. arXiv preprint arXiv:2405.16506.

Bowen Jin, Chulin Xie, Jiawei Zhang, Kashob Kumar Roy, Yu Zhang, Suhang Wang, Yu Meng, and Jiawei Han. 2024. 图思维链：通过在图上推理来增强大语言模型（Graph chain-of-thought: Augmenting large language models by reasoning on graphs）. arXiv preprint arXiv:2404.07103.

Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei. 2020. 神经语言模型的缩放定律（Scaling laws for neural language models）. arXiv preprint arXiv:2001.08361.

Vladimir Karpukhin, Barlas Oğuz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, and Wen-tau Yih. 2020. 面向开放域问答的稠密段落检索（Dense passage retrieval for open-domain question answering）. arXiv preprint arXiv:2004.04906. 作者名在 PDF 文本抽取中写作 Barlas O˘guz。

Yunshi Lan, Gaole He, Jinhao Jiang, Jing Jiang, Wayne Xin Zhao, and Ji-Rong Wen. 2022. 复杂知识库问答：一篇综述（Complex knowledge base question answering: A survey）. IEEE Transactions on Knowledge and Data Engineering, 35(11):11196–11215.

Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, et al. 2020. 面向知识密集型 NLP 任务的检索增强生成（Retrieval-augmented generation for knowledge-intensive nlp tasks）. Advances in Neural Information Processing Systems, 33:9459–9474.

Shilong Li, Yancheng He, Hangyu Guo, Xingyuan Bu, Ge Bai, Jie Liu, Jiaheng Liu, Xingwei Qu, Yangguang Li, Wanli Ouyang, et al. 2024a. GraphReader：构建基于图的智能体，以增强大语言模型的长上下文能力（Graphreader: Building graph-based agent to enhance long-context abilities of large language models）. arXiv preprint arXiv:2406.14550.

<!-- 原 PDF 第 10 页 -->

Zhuowan Li, Cheng Li, Mingyang Zhang, Qiaozhu Mei, and Michael Bendersky. 2024b. 检索增强生成，还是长上下文大语言模型？一项综合研究与一种混合方法（Retrieval augmented generation or long-context llms? a comprehensive study and hybrid approach）. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing: Industry Track, pages 881–893.

Nelson F Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang. 2024. 迷失在中间：语言模型如何使用长上下文（Lost in the middle: How language models use long contexts）. Transactions of the Association for Computational Linguistics, 12:157–173.

Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, Shashank Gupta, Bodhisattwa Prasad Majumder, Katherine Hermann, Sean Welleck, Amir Yazdanbakhsh, and Peter Clark. 2023. Self-Refine：借助自我反馈进行迭代改进（Self-refine: Iterative refinement with self-feedback）. In Thirty-seventh Conference on Neural Information Processing Systems.

Costas Mavromatis and George Karypis. 2024. GNN-RAG：面向大语言模型推理的图神经检索（Gnn-rag: Graph neural retrieval for large language model reasoning）. arXiv preprint arXiv:2405.20139.

Debjit Paul, Mete Ismayilzada, Maxime Peyrard, Beatriz Borges, Antoine Bosselut, Robert West, and Boi Faltings. 2024. REFINER：关于中间表示的推理反馈（Refiner: Reasoning feedback on intermediate representations）. In Proceedings of the 18th Conference of the European Chapter of the Association for Computational Linguistics (Volume 1: Long Papers), pages 1100–1126.

Boci Peng, Yun Zhu, Yongchao Liu, Xiaohe Bo, Haizhou Shi, Chuntao Hong, Yan Zhang, and Siliang Tang. 2024. 图检索增强生成：一篇综述（Graph retrieval-augmented generation: A survey）. arXiv preprint arXiv:2408.08921.

Shuofei Qiao, Ningyu Zhang, Runnan Fang, Yujie Luo, Wangchunshu Zhou, Yuchen Eleanor Jiang, Chengfei Lv, and Huajun Chen. 2024. AutoAct：通过自我规划从零开始自动学习智能体（Autoact: Automatic agent learning from scratch via self-planning）. arXiv preprint arXiv:2401.05268.

Matthew Renze and Erhan Guven. 2024. 大语言模型智能体中的自我反思：对解题表现的影响（Self-reflection in llm agents: Effects on problem-solving performance）. arXiv preprint arXiv:2405.06682.

Freda Shi, Xinyun Chen, Kanishka Misra, Nathan Scales, David Dohan, Ed H. Chi, Nathanael Schärli, and Denny Zhou. 2023. 大语言模型很容易被无关上下文分散注意力（Large language models can be easily distracted by irrelevant context）. In Proceedings of the 40th International Conference on Machine Learning, volume 202 of Proceedings of Machine Learning Research, pages 31210–31227. PMLR.

Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik R Narasimhan, and Shunyu Yao. 2023. Reflexion：带有言语强化学习的语言智能体（Reflexion: language agents with verbal reinforcement learning）. In Thirty-seventh Conference on Neural Information Processing Systems.

Jiashuo Sun, Chengjin Xu, Lumingyuan Tang, Saizhuo Wang, Chen Lin, Yeyun Gong, Lionel Ni, Heung-Yeung Shum, and Jian Guo. 2024. Think-on-Graph：大语言模型在知识图谱上的深度且负责任的推理（Think-on-graph: Deep and responsible reasoning of large language model on knowledge graph）. In The Twelfth International Conference on Learning Representations.

Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al. 2022. 思维链提示激发大语言模型中的推理（Chain-of-thought prompting elicits reasoning in large language models）. Advances in neural information processing systems, 35:24824–24837.

Shirley Wu, Shiyu Zhao, Qian Huang, Kexin Huang, Michihiro Yasunaga, Kaidi Cao, Vassilis N Ioannidis, Karthik Subbian, Jure Leskovec, and James Zou. 2024a. AVATAR：为工具辅助的知识检索优化大语言模型智能体（Avatar: Optimizing llm agents for tool-assisted knowledge retrieval）. arXiv preprint arXiv:2406.11200.

Shirley Wu, Shiyu Zhao, Michihiro Yasunaga, Kexin Huang, Kaidi Cao, Qian Huang, Vassilis N Ioannidis, Karthik Subbian, James Zou, and Jure Leskovec. 2024b. STaRK：在文本知识库与关系知识库上为大语言模型检索建立基准（Stark: Benchmarking llm retrieval on textual and relational knowledge bases）. arXiv preprint arXiv:2404.13207.

Shi-Qi Yan, Jia-Chen Gu, Yun Zhu, and Zhen-Hua Ling. 2024. 纠正性检索增强生成（Corrective retrieval augmented generation）. arXiv preprint arXiv:2401.15884.

Xiao Yang, Kai Sun, Hao Xin, Yushi Sun, Nikita Bhalla, Xiangsen Chen, Sajal Choudhary, Rongze Daniel Gui, Ziran Will Jiang, Ziyu Jiang, et al. 2024. CRAG：综合性 RAG 基准（Crag–comprehensive rag benchmark）. arXiv preprint arXiv:2406.04744.

Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik R Narasimhan, and Yuan Cao. 2023. ReAct：在语言模型中协同推理与行动（React: Synergizing reasoning and acting in language models）. In The Eleventh International Conference on Learning Representations.

Michihiro Yasunaga, Hongyu Ren, Antoine Bosselut, Percy Liang, and Jure Leskovec. 2021. QA-GNN：用语言模型与知识图谱进行问答推理（Qa-gnn: Reasoning with language models and knowledge graphs for question answering）. In North American Chapter of the Association for Computational Linguistics (NAACL).

<!-- 原 PDF 第 11 页 -->

## A 附录：基准

### A.1 STaRK

我们使用 STaRK 基准中的两个数据集：STaRK-MAG 与 STaRK-PRIME。每个数据集都包含一个知识图谱（KG），以及与某些类型的实体相关联的非结构化文档。任务是从数据库中检索一组满足问题所规定要求的文档。需要注意的是，大多数问题是混合问题，文本问题非常少。我们使用 STaRK 的测试集进行评测，其中 STaRK-MAG 与 STaRK-PRIME 分别包含 2665 和 2801 个问题。STaRK-MAG 的 KG 是学术知识图谱，STaRK-PRIME 的 KG 是精准医学知识图谱。它们的实体类型与关系类型由该基准提供。

### A.2 CRAG

在 CRAG 基准中，有来自 5 个不同领域的 KG，可用于检索有用参照。对每个问题，给定一个数据库，其中包含 50 个已检索的网页以及全部 5 个 KG，但并不保证答案位于网页、KG 或二者之上。任务是生成该问题的答案，无论是否借助检索到的参照。其中既有文本问题，也有关系问题，覆盖多种问题类型，例如简单（simple）、带条件的简单（simple with condition）、比较（comparison）和多跳（multi-hop）。我们使用 CRAG 的测试集进行评测。共有 1335 个文本问题与关系问题，覆盖多种问题类型，例如简单、比较和多跳。

## B 附录：实验

### B.1 STaRK-Prime 中的可解释性（RQ3）

图 6 给出两个例子，说明 HYBGRAG 在 STaRK-Prime 中改进其问题路由。在图 6(a) 的例子中，HYBGRAG 在第一次迭代选择使用文本检索模块，检索到的文档被验证器拒绝。HYBGRAG 随后采纳评论器（原文写作 commentor）的反馈，转而使用混合检索模块，并在接下来的两次迭代中改进主题实体与有用关系的抽取。

### B.2 关于批评模块的消融研究

我们将 HYBGRAG 的变体与下列设置比较：没有验证器上下文的验证器、只有少量示例或零示例的评论器（原文写作 commentors），以及带有预言机的设置。预言机可以访问真实标签，从而对输出是否正确、以及动作的错误类型（如果存在）给出最优判断。在表 10 和表 11 中，我们表明 HYBGRAG 在我们的全部设计选择下表现最好，并接近预言机的性能。

## C 附录：可复现性

### C.1 实验细节

全部实验在带有 NVIDIA A100 GPU 的 AWS EC2 P4 实例上进行。大多数 LLM 通过 Amazon Bedrock^3 实现，Llama 3.1 通过 Ollama^4 实现。

^3 https://aws.amazon.com/bedrock/

^4 https://github.com/ollama/ollama

#### C.1.1 HYBGRAG 的实现

**STaRK。** 提示中的示例收集自 STaRK 提供的训练集。我们使用 STaRK 提供的默认实体类型与关系类型。所抽取 ego-graph 的半径不超过二。已完成四轮自我反思迭代。从问题中抽取实体名称时，知识库中可能有多个实体的名称完全相同。在这些情况下，我们选择其一跳邻域中包含答案的那个实体来消歧，因为这不是本文的重点。而且这些情况很少发生：在 STaRK-MAG 与 STaRK-PRIME 中，分别只有 3.83% 和 0.07% 的问题存在这一问题。

**CRAG。** 在文本检索模块中，基于问题的网页搜索被用作检索器，该搜索由 CRAG 事先完成。VSS 排序器根据网页与问题在嵌入空间中的相似度对网页排序。在这一模块中，我们为路由器提供一个额外选择。如果基于当前一批已检索网页生成的输出被验证器拒绝，路由器可以选择转到排序列表中的下一批。在 CRAG 中，由于没有混合问题，混合检索模块被替换为图检索模块，以便应对关系问题。在图检索模块中，检索器为每个主题实体抽取由有用关系连接的 ego-graph。由于没有与实体相关联的文档，检索器检索从主题实体到所抽取 ego-graph 中实体的推理路径。推理路径被表述为 “{topic

<!-- 原 PDF 第 12 页 -->

entity} → {useful relation} → ... → {useful relation} → {neighboring entity}”，并用 VSS 排序。本页文本抽取在正文之前还出现数字 0.4358 与 0.3932，它们与表 10 中 Oracle 一行在 STaRK-PRIME 上的 Recall@20 与 MRR 相同，此处不另作独立结果。

检索到的参照被用作验证上下文，以检查它是否可靠到足以回答问题。验证器把生成器的输出和验证上下文作为输入。由于生成器与验证器的提示针对不同任务专门设计，验证器因而能够给出有意义的验证。尽管 CRAG 中没有检索的真实标签，我们仍根据路由器的动作和评测结果构造纠正性反馈，如表 12 所示。如果使用了图检索模块且评测结果不正确，那么要么检索输入（抽取出的实体和关系，或领域）不正确，要么选择图检索模块这一决定不正确；如果使用了文本检索模块且评测结果不正确，则认为当前这一批文档中的信息无助于回答问题。

提示中的示例收集自 CRAG 提供的验证集。由于 CRAG 没有给出实体类型与关系类型，而且 KG 只能通过所提供的 API 访问，我们从验证集的问题中收集它们，如表 13 所示。所抽取 ego-graph 的半径不超过二。已完成四轮自我反思迭代。一批包含五个网页。

#### C.1.2 基线实现

**STaRK。** 我们使用 “ada-002” 作为稠密检索与排序的嵌入模型，与原论文中的用法一致。HYBGRAG 使用 Claude 3 Sonnet 作为基座模型，而 ReAct、Reflexion、AVATAR 以及带 LLM 重排序器的 VSS 使用 Claude 3 Opus，后者被设计为比 Claude 3 Sonnet 更强^5。对于 QAGNN 和 Dense Retriever，由于需要训练，使用 RoBERTa 作为基座模型。在没有指定基座 LLM 的实验中，我们默认使用 Claude 3

^5 https://www.anthropic.com/news/claude-3-family

**图 6：** HYBGRAG 是可解释的。在来自 STaRK-PRIME 的例子中，HYBGRAG 根据批评模块的纠正性反馈，成功改进了实体与关系抽取。

**(a) 错误类型：模块不正确且缺少实体（Incorrect Module & Missing Entity）**

问：哪些常染色体显性遗传病与多余乳腺组织（supernumerary breast tissue）的发育有关？（原文：Which autosomal dominant diseases are linked to the development of supernumerary breast tissue?）

动作 1：

- 选择：文本检索模块

反馈 1：检索到的文档不正确。当前检索模块可能无助于缩小搜索空间。

动作 2：

- 选择：混合检索模块
- 实体：autosomal dominant diseases（disease，疾病）
- 关系（原文标签为 Relational）：phenotype present

反馈 2：检索到的文档不正确。目前只有一个实体，但可能还有更多。请再抽取一个实体和一条关系。

动作 3：

- 选择：混合检索模块
- 实体：autosomal dominant diseases（disease），supernumerary breast tissue（effect/phenotype，效应/表型）
- 关系（原文标签为 Relational）：phenotype present，associated with

反馈 3：接受。✅

**(b) 错误类型：实体/关系不正确（Incorrect Entity/Relation）**

问：请为我找出与儿童肝癌相关、与 PAXIP1 相互作用、在肺腺癌中高表达、具有核信号且与 GAGE/PAGE 蛋白相似的基因或蛋白质。（原文：Please find me genes or proteins linked to pediatric liver cancer, interacting with PAXIP1, highly expressed in lung adenocarcinoma, with a nuclear signal and similarity to GAGE/PAGE proteins.）

动作 1：

- 选择：混合检索模块
- 实体：PAXIP1（gene/protein，基因/蛋白质），pediatric liver cancer（disease），lung adenocarcinoma（disease）
- 关系（原文标签为 Relational）：ppi，associated with，expression present

反馈 1：检索到的文档不正确。实体 “pediatric liver cancer” 和 “lung adenocarcinoma” 不正确。请移除或替换这些实体。关系 “associated with” 和 “expression present” 不正确。请移除或替换这些关系。

动作 2：

- 选择：混合检索模块
- 实体：PAXIP1（gene/protein）
- 关系（原文标签为 Relational）：ppi

反馈 2：接受。✅

**表 10：** HYBGRAG 在 STaRK 中的设计选择是必要的。原文用标记分别表示 HYBGRAG 的设置，以及在推理时使用真实标签的基线；这些标记在文本抽取中丢失，见原 PDF 第 12 页。表头中的 Commentor 按原文拼写保留。

| 验证器（Validator） | 评论器（Commentor） | STaRK-MAG Hit@1 | Hit@5 | Recall@20 | MRR | STaRK-PRIME Hit@1 | Hit@5 | Recall@20 | MRR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 无上下文（w/o Context） | ICL | 0.6105 | 0.7073 | 0.6245 | 0.6541 | 0.1946 | 0.2592 | 0.2685 | 0.2251 |
| 有上下文（w/ Context） | 5-Shot | 0.6465 | 0.7407 | 0.6458 | 0.6884 | 0.2406 | 0.3006 | 0.3038 | 0.2676 |
| 有上下文（w/ Context） | ICL | 0.6540 | 0.7531 | 0.6570 | 0.6980 | 0.2856 | 0.4138 | 0.4358 | 0.3449 |
| Oracle | Oracle | 0.7193 | 0.7824 | 0.6840 | 0.7479 | 0.3606 | 0.4320 | 0.4358 | 0.3932 |

<!-- 原 PDF 第 13 页 -->

Sonnet。我们用他们提供的代码^6 实现 Think-on-Graph，并以 Claude 3 Sonnet 作为基座模型。由于跑完全部实验需要一周以上，我们只在 10% 的测试数据上评测它，这与 STaRK 论文中对 LLM 重排序器的做法一致。

^6 https://github.com/GasolSun36/ToG

**CRAG。** 我们使用 Claude 3 Sonnet 作为 LLM 评测器，并对所有生成器 LLM 使用 CoT 提示（Wei et al., 2022）。我们使用 “BAAI/bge-m3”（Chen et al., 2024）作为稠密检索与排序的嵌入模型。ReAct 和 Corrective RAG 与 HYBGRAG 共用同一骨干，但批评者不同。ReAct 有三个动作：“search web”（搜索网页）、“search KG”（搜索知识图谱）和 “extract entity relation domain”（抽取实体、关系与领域），并被给予一些示例。该过程像 HYBGRAG 一样，在动作、观察和思考之间迭代四轮。虽然 Corrective RAG 需要一个经过微调的检索评测器，我们实现的是一个只使用预训练 LLM 的版本。它从文本检索模块开始，并验证检索到的参照是正确、含糊还是不正确。如果不正确，它改用图检索模块。最终答案基于参照、用 CoT 提示生成。

**表 11：** HYBGRAG 在 CRAG 中的设计选择是必要的。原文用标记分别表示 HYBGRAG 的设置，以及在推理时使用真实标签的基线；这些标记在文本抽取中丢失，见原 PDF 第 13 页。表头中的 Commentor 按原文拼写保留。Score$_a$ 在抽取文本中写作 Score a。

| 验证器（Validator） | 评论器（Commentor） | Accuracy ↑ | Halluc. ↓ | Missing | Score$_a$ ↑ |
| --- | --- | --- | --- | --- | --- |
| 无上下文（w/o Context） | ICL | 0.5581 | 0.3461 | 0.0958 | 0.2120 |
| 有上下文（w/ Context） | 0-Shot | 0.6277 | 0.3004 | 0.0719 | 0.3273 |
| 有上下文（w/ Context） | ICL | 0.6322 | 0.2959 | 0.0719 | 0.3363 |
| Oracle | Oracle | 0.7813 | 0.1640 | 0.0547 | 0.6173 |

**表 12：** HYBGRAG 中面向 CRAG 的批评模块设计。

| 错误来源 | 错误类型 | 反馈 |
| --- | --- | --- |
| 输入（Input） | 问题类型不正确（Incorrect Question Type） | 预测的问题类型是错的。请重新回答。这个问题是哪种类型？ |
|  | 问题动态性不正确（Incorrect Question Dynamism） | 预测的问题动态性是错的。请重新回答。这个问题是哪种动态性？ |
|  | 问题领域不正确（Incorrect Question Domain） | 预测的问题领域是错的。请重新回答。这个问题来自哪个领域？ |
|  | 实体与关系不正确（Incorrect Entity and Relation） | 从问题中抽取出的主题实体和有用信息不正确。请重新抽取。 |
| 选择（Selection） | 检索模块不正确（Incorrect Retrieval Module） | 该参照不包含对解决问题有用的信息。我们应当根据新抽取出的实体和关系，把知识图谱用作参照来源，还是把下一批文本文档用作参照来源？ |

### C.2 提示

**STaRK。** 路由器第一次决策的提示是：

> 你是一个乐于助人、遵循模式的助手。给定下列问题，按要求从问题中抽取信息。规则：1. 关系信息必须来自给定的关系类型。2. 每个实体在括号中必须恰好有一个类别。
>
> <<<{10 examples for entity and relation extraction}>>>
>
> 给定下列问题，根据实体类型和关系类型，从问题中抽取主题实体和有用关系。
>
> 实体类型：<<<{entity types}>>>
>
> 关系类型：<<<{relation types}>>>
>
> 问题：<<<{question}>>>
>
> 回答给定问题需要文档，目标是搜索有用的文档。知识图谱中的每个实体都与一份文档相关联。根据抽取出的实体和关系，知识图谱还是文本文档有助于缩小搜索空间？你必须用二者之一作答，且不超过两个词。

路由器进行反思的提示是：

<!-- 原 PDF 第 14 页 -->

**表 13：** CRAG 基准中的实体类型与关系类型。Content 一列是原文中的类型字符串，保持英文。

| 领域（Domain） | 类型（Type） | 内容（Content） |
| --- | --- | --- |
| Finance（金融） | Entity（实体） | company_name, ticker_symbol, market_capitalization, earnings_per_share, price_to_earnings_ratio, datetime |
|  | Relation（关系） | get_company_ticker, get_ticker_dividends, get_ticker_market_capitalization, get_ticker_earnings_per_share, get_ticker_price_to_earnings_ratio, get_ticker_history_last_year_per_day, get_ticker_history_last_week_per_minute, get_ticker_open_price, get_ticker_close_price, get_ticker_high_price, get_ticker_low_price, get_ticker_volume, get_ticker_financial_information |
| Sports（体育） | Entity（实体） | nba_team_name, nba_player, soccer_team_name, datetime_day, datetime_month, datetime_year |
|  | Relation（关系） | get_nba_game_on_date, get_soccer_previous_games_on_date, get_soccer_future_games_on_date, get_nba_team_win_by_year |
| Music（音乐） | Entity（实体） | artist, lifespan, song, release_date, release_country, birth_place, birth_date, grammy_award_count, grammy_year |
|  | Relation（关系） | grammy_get_best_artist_by_year, grammy_get_award_count_by_artist, grammy_get_award_count_by_song, grammy_get_best_song_by_year, grammy_get_award_date_by_artist, grammy_get_best_album_by_year, get_artist_birth_place, get_artist_birth_date, get_members, get_lifespan, get_song_author, get_song_release_country, get_song_release_date, get_artist_all_works |
| Movie（电影） | Entity（实体） | actor, movie, release_date, original_title, original_language, revenue, award_category |
|  | Relation（关系） | act_movie, has_birthday, has_character, has_release_date, has_original_title, has_original_language, has_revenue, has_crew, has_job, has_award_winner, has_award_category |
| Encyclopedia（百科） | Entity（实体） | encyclopedia_entity |
|  | Relation（关系） | get_entity_information |

> 检索到的文档不正确。
>
> 反馈：<<<{feedback on extracted entity and relation}>>>
>
> 问题：<<<{question}>>>
>
> 检索到的文档不正确。请根据新抽取出的主题实体和有用关系重新回答。知识图谱还是文本文档有助于缩小搜索空间？你必须用二者之一作答，且不超过两个词。

验证器的提示是：

> 你是一个乐于助人、遵循模式的助手。
>
> <<<{examples for retrieval validation, 2 for each type of entity}>>>
>
> ### 问题：<<<{question}>>>
>
> ### 文档：<<<{content of document and reasoning paths}>>>
>
> ### 任务：
>
> 该文档是否与问题的要求一致？只回答 yes 或 no。

评论器（原文写作 commentor）的提示是：

> 你是一个乐于助人、遵循模式的助手。
>
> <<<{30 examples of action and feedback pair}>>>
>
> 问题：<<<{question}>>>
>
> 主题实体：<<<{extracted entities}>>>
>
> 有用关系：<<<{extracted relations}>>>
>
> 请指出从问题中抽取出的错误实体或关系，如果存在的话。

**CRAG。** 路由器第一次决策的提示是：

> 你是一个乐于助人、遵循模式的助手。给定下列问题，按要求从问题中抽取信息。规则：1. 每个实体在括号中必须恰好有一个类别。2. 严格遵循示例。
>
> <<<{examples of entity and relation extraction, 5 for each domain}>>>
>
> ### 问题类型：simple, simple_w_condition, set, comparison, aggregation, multi_hop, post_processing, false_premise。
>
> ### 问题：<<<{question}>>>
>
> ### 任务：这个问题是哪种类型？答案必须是其中之一。
>
> ### 动态性（Dynamism）：real-time, fast-changing, slow-changing, static。
>
> ### 问题：<<<{question}>>>
>
> ### 任务：这个问题属于哪一类动态性？用一个词回答，且答案必须是其中之一。
>
> ### 领域：music, movie, finance, sports, encyclopedia。
>
> ### 问题：<<<{question}>>>
>
> ### 任务：这个问题来自哪个领域？用一个词回答，且答案必须是其中之一。
>
> 给定下列问题，根据实体类型和关系类型，从问题中抽取主题实体和有用关系。
>
> 实体类型：<<<{entity types}>>>
>
> 关系类型：<<<{relation types}>>>
>
> 问题：<<<{question}>>>
>
> ### 参照来源：knowledge graph, text documents。
>
> ### 问题：<<<{question}>>>
>
> ### 任务：根据抽取出的实体，哪种参照来源有助于回答问题？你必须选择其中之一，并用不超过两个词作答。

<!-- 原 PDF 第 15 页 -->

路由器进行反思的提示是：

> ### 问题类型：simple, simple_w_condition, set, comparison, aggregation, multi_hop, post_processing, false_premise。
>
> ### 问题：<<<{question}>>>
>
> ### 任务：预测的问题类型是错的。请重新回答。这个问题是哪种类型？用一个词回答，且答案必须是其中之一。
>
> ### 动态性：real-time, fast-changing, slow-changing, static。
>
> ### 问题：<<<{question}>>>
>
> ### 任务：预测的问题动态性是错的。请重新回答。这个问题是哪种动态性？用一个词回答，且答案必须是其中之一。
>
> ### 领域：music, movie, finance, sports, encyclopedia。
>
> ### 问题：<<<{question}>>>
>
> ### 任务：预测的问题领域是错的。请重新回答。这个问题来自哪个领域？用一个词回答，且答案必须是其中之一。
>
> 从问题中抽取出的主题实体和有用信息不正确。请重新抽取。给定下列问题，根据实体类型和关系类型，从问题中抽取主题实体和有用关系。
>
> 实体类型：<<<{entity types}>>>
>
> 关系类型：<<<{relation types}>>>
>
> 问题：<<<{question}>>>
>
> ### 参照来源：knowledge graph, text documents。
>
> ### 问题：<<<{question}>>>
>
> ### 任务：答案不正确。该参照不包含对解决问题有用的信息。请重新回答：我们应当根据新抽取出的实体和关系，把知识图谱用作参照来源，还是把下一批文本文档用作参照来源？你必须选择其中之一，并用不超过两个词作答。

验证器的提示是：

> ### 参照：<<<{reference}>>>
>
> ### 预测：<<<{output of generator}>>>
>
> ### 问题：<<<{question}>>>
>
> ### 查询时间：<<<{question time}>>>
>
> ### 任务：该预测是根据参照生成的。这个预测回答了问题吗？用一个词回答，yes 或 no。

评论器（原文写作 commentor）的提示是：

> 你是一个乐于助人、遵循模式的助手。
>
> <<<{5 examples of action and feedback pair}>>>
>
> ### 参照来源：<<<{source}>>>
>
> ### 问题：<<<{question}>>>
>
> ### 查询时间：<<<{question time}>>>
>
> ### 查询类型：<<<{question type}>>>
>
> ### 查询动态性：<<<{dynamism}>>>
>
> ### 查询领域：<<<{domain}>>>
>
> ### 任务：请指出关于该问题的错误信息（Reference Source、Query Type、Query Dynamism、Query Domain），如果存在的话。答案必须是其中之一。

生成器的提示是：

> 你是一个乐于助人、遵循模式的助手。
>
> <<<{1 chain-of-though prompt example}>>>
>
> 原文写作 chain-of-though。
>
> ### 参照：<<<{reference}>>>
>
> ### 参照来源：<<<{source}>>>
>
> ### 问题：<<<{question}>>>
>
> ### 查询时间：<<<{question time}>>>
>
> ### 查询类型：<<<{question type}>>>
>
> ### 查询动态性：<<<{dynamism}>>>
>
> ### 查询领域：<<<{domain}>>>
>
> ### 任务：给你一个问题（Question）、若干参照（References），以及它在太平洋时区（Pacific Time Zone, PT）被提出的时间，称为查询时间（Query Time）。查询时间的格式为 mm/dd/yyyy, hh:mm:ss PT。参照可能有助于回答问题。如果问题包含错误的前提或假设，请回答 “invalid question”。首先，系统而详细地列出这个问题中、在我们得出正确答案之前需要解决的全部子问题。然后，利用前面子问题的答案解决每一个子问题，并得到最终解答。
>
> 最终答案是什么？

评测器的提示是：

> ### 问题：<<<{question}>>>
>
> ### 真实答案：<<<{ground truth answer}>>>
>
> ### 预测答案：<<<{output of generator}>>>
>
> ### 任务：根据问题和真实答案，预测答案是准确（accurate）、不正确（incorrect），还是缺失（missing）？答案必须是其中之一，并且是一个词。

**表 14：** CRAG 的 API 调用次数与词元数。

| HYBGRAG 组件 | 每次迭代的 API 调用次数 | 提示的词元数 | 示例的词元数 |
| --- | --- | --- | --- |
| Router（路由器） | 4 | 266 | 5752 |
| Validator（验证器） | 1 | 56 | 0 |
| Commenter（评论器） | 1 | 78 | 598 |
| Generator（生成器） | 2 | 168 | 553 |

<!-- 译完 -->
