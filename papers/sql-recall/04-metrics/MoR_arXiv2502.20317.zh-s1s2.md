# Mixture of Structural-and-Textual Retrieval over Text-rich Graph Knowledge Bases

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`MoR_arXiv2502.20317.pdf`。

## Abstract 摘要

文本丰富的图知识库（Text-rich Graph Knowledge Bases, TG-KBs）通过同时提供文本知识与结构知识，对回答查询日益关键。然而，当前检索方法往往孤立地检索这两类知识，不考虑它们的相互强化；一些混合方法甚至在邻居聚合之后完全绕过结构检索。为填补这一空白，我们提出结构与文本混合检索（Mixture of Structural-and-Textual Retrieval, MoR），经由 Planning–Reasoning–Organizing 框架检索这两类知识。在 Planning 阶段，MoR 生成文本规划图，勾勒回答查询的逻辑。沿着规划图，在 Reasoning 阶段，MoR 交织结构遍历与文本匹配，从 TG-KB 中获得候选。在 Organizing 阶段，MoR 进一步按结构轨迹对取回的候选排序。大量实验表明 MoR 在协调结构检索与文本检索上的优势，并得到若干发现，包括不同查询逻辑上检索表现不均衡，以及把结构轨迹整合进候选重排序的益处。代码见 https://github.com/Yoega/MoR 。

## 1 Introduction 引言

文本丰富的图知识库（TG-KBs）以结构化方式表示文本文档，因而普遍存储文本知识与结构知识（Jin et al., 2024b）。例如，学者从论文管理系统中检索相关研究以推进科学发现，其中节点表示论文、边表示引用（Lu et al., 2024）。随着由大语言模型（LLM）驱动的生成器在语言理解与生成上接近人类智能，从 TG-KB 中检索支持性知识以提供上下文并约束生成，对正确回答查询日益关键（Gao et al., 2023b; Ni et al., 2025）。

图 1 的框内数字标签【抽取不清】。图注如下。（a）文本检索与结构检索。（b）检索方法的有效性在不同 TG-KB 上有差异。（c）在同一 TG-KB 内，由文本检索处理的查询（即 QText）与由结构检索处理的查询（即 QStruct）既有重叠也有区别。图中可读的查询示例为：Publications by Point Park University authors on stellar populations in tidal tails。

由于 TG-KB 中的支持性知识通常同时以文本与结构两种形式出现（Kolomiyets and Moens, 2011; Jin et al., 2024b），检索方法应如图 1(a) 所示针对两种形式分别有效设计。文本检索方法根据与给定查询的相似度检索文本知识，例如已索引的文档，可大致分为词法方法（例如 BM25）与语义方法（例如 Contriever）（Karpukhin et al., 2020; Izacard et al., 2022）。结构检索方法通过图遍历与图机器学习检索结构知识，例如邻居实体（Jiang et al., 2023; Edge et al., 2024; Wang et al., 2024）（Yasunaga et al., 2021; Tian et al., 2024）。尽管文本检索与结构检索都有进展，它们往往被独立应用，未能相互强化。如图 1(b) 所示，无论是沿查询逻辑结构进行的结构检索，还是做 Top-K BM25 匹配的文本检索，都不能同时在 Amazon 与 MAG 两个数据集上取得更好表现。

为从 TG-KB 中有效检索文本与结构知识，近期工作（Xia et al., 2024; Li et al., 2024）聚合邻居文档，把结构知识融入文本叙述，再做文本检索：Xia et al. (2024) 按关系过滤无关邻居，Li et al. (2024) 按字段对邻居做加权聚合。然而仍有三个挑战。第一，改写聚合后的邻居需要频繁调用 LLM，对邻居数量指数增长的长文档而言资源代价过高。第二，人类用来形成逻辑计划的结构信号在邻居聚合之后被完全丢弃。第三，僵硬的邻居聚合忽视了不同查询与不同 TG-KB 对结构知识与文本知识的不同需求。即使在同一 TG-KB 内，例如图 1(c) 中的 MAG，由文本检索回答的查询（即 QText）也不同于由结构检索回答的查询（即 QStruct）。

为应对上述三个挑战，我们把混合专家的思想注入检索设计，并提出图 2 中的结构与文本混合检索（MoR）。MoR 从一个规划模块开始，生成规划图以勾勒查询逻辑，并在不改写聚合邻居的情况下保留结构信号，从而克服第一与第二个挑战。接下来，MoR 在推理模块中交错结构遍历与文本匹配，使两种检索相互强化。最后，MoR 在组织模块中设计结构感知的重排序器，自适应调整所检索文本/结构知识的重要性，从而应对第三个挑战。经由 Planning–Reasoning–Organizing，MoR 根据查询的逻辑结构智能地检索结构知识与文本知识。我们的主要贡献是：

- 经由文本图生成进行规划：我们把检索规划定义为生成文本图，这些图勾勒逻辑结构，即用于识别与查询相关实体的计划。
- 经由结构与文本混合遍历进行推理：我们设计混合遍历，交织文本匹配与结构遍历，按照所生成计划描绘的查询逻辑结构检索知识。
- 经由结构感知重排序进行组织：对混合遍历得到的候选，我们提出 Structure-aware Rerank，根据其遍历轨迹选择 Top-K 候选。

## 2 Preliminary 预备知识

**记号。** 文本丰富的图知识库（TG-KB）\(B\) 一般由一组相连节点 \(V\) 组成，每个节点 \(v\in V\) 关联其对应文档 \(D_v\in D\) 与类别 \(E_v\in E\)。当为回答给定查询 \(Q\in\mathcal{Q}\) 而从 \(B\) 中检索带支持文档的节点时，我们通常遵循某种理由，它封装该查询的底层逻辑（Xu et al., 2024; Xue et al., 2024），可由一个带文本属性的规划图 \(G\) 刻画。在许多现有工作中（Jin et al., 2024a; Wu et al.），该规划图通常可分解为多条推理路径 \(G=\{P_i\}_{i=1}^{|G|}\)，其中第 \(i\) 条推理路径 \(P_i=(p_{i1}\rightarrow p_{i2}\rightarrow,\ldots,\rightarrow p_{iL_i})\) 是长度为 \(L_i\) 的一条独特推理链，编码一种独特逻辑，第 \(j\) 个节点 \(p_{ij}\) 对应 \(B\) 中的一个实体，具有自身类别 \(E_{p_{ij}}\) 以及从查询中抽取的文本限制 \(T_{p_{ij}}\)。例如，在图 1(a) 中，查询 Publications by Point... 有一个含两条路径的规划图，即 \(P_1=(\mathrm{Institution}\rightarrow\mathrm{Author}\rightarrow\mathrm{Paper})\) 与 \(P_2=(\mathrm{Field\text{-}of\text{-}Study}\rightarrow\mathrm{Paper})\)，其中 \(P_1\) 上第一个节点的类别与文本限制分别为 \(E_{p_{11}}=\mathrm{Institution}\) 与 \(T_{p_{11}}=\langle\) Point Park Univerisity \(\rangle\)。完整记号汇总于附录 A 的表 6。

**问题设定。** 在上述记号下，所研究的问题是检索实体 \(C\subseteq V\) 以回答给定查询 \(Q\)。

**文本检索**根据查询与文档双方的文本信号检索候选。一种常见策略是从全部文档 \(D\) 中检索与查询 \(Q\) 具有 Top-K 文本相似度的候选 \(\tilde{C}\)，相似度由词法或语义相似度衡量（Vijaymeena and Kavitha, 2016）。MoR 中使用的文本检索通过把文档与查询中的文本描述相匹配来为给定查询检索文档，例如匹配图 1 中所示的 stellar populations in tidal tails。

**结构检索**通过对知识图谱与 SQL 等结构化数据库施加规定规则来检索候选（Guo et al., 2023）。常见策略包括基于图的遍历（例如 BFS、DFS）与规则获取（Jiang et al., 2023）。具体而言，MoR 通过遍历所生成规划图中某些类别的邻居来做结构检索。例如，在图 1(a) 中，我们的结构检索只能遍历 Author 的类型为 “Paper” 的邻居。

图 2 内部流程标签【抽取不清】。图注：我们的 MoR 框架由一个生成规划图的规划模块、一个执行混合遍历的推理模块，以及一个对检索候选重排序的组织模块组成。
