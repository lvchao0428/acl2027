> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名**：MoR_arXiv2502.20317.pdf

**原文标题**：Mixture of Structural-and-Textual Retrieval over Text-rich Graph Knowledge Bases

**作者**：Yongjia Lei、Yu Wang（University of Oregon）；Haoyu Han、Jiliang Tang（Michigan State University）；Ryan A. Rossi、Franck Dernoncourt、Nedim Lipka（Adobe Research）；Mahantesh M Halappanavar（Pacific Northwest National Laboratory）。

**场合**：arXiv:2502.20317v4 [cs.LG]，2025 年 6 月 1 日。

## 摘要

Text-rich Graph Knowledge Bases（TG-KBs）同时提供文本知识和结构知识，用来回答查询。现有检索常常把这两种知识分开取，没有利用它们彼此加强；有些混合方法在把邻居聚合进文本之后，干脆不再做结构检索。

MoR（Mixture of Structural-and-Textual Retrieval）用 Planning–Reasoning–Organizing 把两种知识一起取回来。Planning 生成 textual planning graphs，把答题所需的逻辑画出来。Reasoning 沿着这些图，把结构遍历和文本匹配交织起来，从 TG-KB 里取候选。Organizing 再按候选的 structural trajectory 排序。实验表明这种结构检索与文本检索的配合更好，并看到两点：不同查询逻辑上的检索表现并不均匀；把结构轨迹用于候选重排有好处。代码在 https://github.com/Yoega/MoR。摘要没有给出具体指标数字。

## 1 Introduction

TG-KB 用图把文本文档组织起来，因此同时存着文本和结构（Jin et al., 2024b）。论文管理就是一个例子：节点是论文，边是引用（Lu et al., 2024）。大模型已经很会理解和生成语言，但要答对问题，仍需要从 TG-KB 里取出能约束生成的证据（Gao et al., 2023b; Ni et al., 2025）。这些证据两种形态都有（Kolomiyets and Moens, 2011; Jin et al., 2024b），检索就得两边都照顾，如图 1(a)。文本检索按与查询的相似度取文档，词法上如 BM25，语义上如 Contriever（Karpukhin et al., 2020; Izacard et al., 2022）。结构检索取邻居实体一类的结构知识（Jiang et al., 2023; Edge et al., 2024; Wang et al., 2024），手段是图遍历和图机器学习（Yasunaga et al., 2021; Tian et al., 2024）。两边各自进步，却常常单独使用，不能互相补强。

图 1 用查询 “Publications by Point Park University authors on stellar populations in tidal tails” 说明这种分家。图 1(b) 的 Hit@1（%）在两个 TG-KB 上方向相反：Amazon 上 Textual Retriever 43.05、Structural Retriever 34.04、Mixture-of-Retrievers 51.27；MAG 上分别是 31.05、51.81、58.57。正文据此说，沿查询逻辑做结构检索，或做 Top-K BM25，都不能在 Amazon 和 MAG 上同时占优。图 1(c) 再看同一个 MAG：能被文本检索答上的查询集 \(Q^{\text{Text}}\) 和能被结构检索答上的 \(Q^{\text{Struct}}\) 既有重叠也有差别，图中写明 \(Q^{\text{Text}} \neq Q^{\text{Struct}}\)，以及 \(|Q^{\text{MoR}}| > |Q^{\text{Text}} \cup Q^{\text{Struct}}|\)。三圆上印出的计数包括 306（\(Q^{\text{MoR}}\) 一侧的非重叠区）、552（\(Q^{\text{MoR}}\) 与 \(Q^{\text{Struct}}\) 的重叠）、74（靠近 \(Q^{\text{Struct}}\) 的非重叠一侧）、23（\(Q^{\text{Text}}\) 的非重叠区），另有 653、102、50 印在 \(Q^{\text{Text}}\) 与另外两圆挤在一起的相交带上。

近期混合方法（Xia et al., 2024; Li et al., 2024）先把邻居文档聚合成一段文本叙述，再做文本检索：Xia et al. 按关系滤掉无关邻居，Li et al. 按字段对邻居做加权聚合。作者认为还剩三个问题。第一，把聚合后的邻居改写成文本要反复调用大模型，文档一长、邻居指数增长，代价过高。第二，人用来形成逻辑计划的结构信号，在邻居聚合之后被丢掉。第三，固定的邻居聚合不顾不同查询、不同 TG-KB 对两种知识的需求不一样；即便在同一个 MAG 里，\(Q^{\text{Text}}\) 和 \(Q^{\text{Struct}}\) 也不是同一批查询。MoR 把 mixture-of-expert 的想法放进检索。planning module 生成 planning graph，勾出查询逻辑并保留结构信号，且不必改写聚合邻居，对应前两个问题。reasoning module 交织结构遍历和文本匹配，让两种检索互相加强。organization module 里的 structure-aware reranker 再按情况调节文本知识与结构知识的分量，对应第三个问题。贡献也按这三步写：把检索规划定义成生成勾勒逻辑结构的文本图；用文本匹配和结构遍历交织的 mixed traversal，按计划取知识；再用 Structure-aware Rerank，按遍历轨迹选 Top-K。

## 2 Preliminary

TG-KB 记为 \(\mathcal{B}\)：图上有相连节点集 \(V\)，每个节点 \(v\) 带文档 \(D_v \in \mathcal{D}\) 和类别 \(E_v \in \mathcal{E}\)。为查询 \(Q\) 检索带证据文档的节点时，通常要遵循一条概括该查询逻辑的依据（Xu et al., 2024; Xue et al., 2024），文中用一个带文本属性的 planning graph \(G\) 来表示。沿用已有写法（Jin et al., 2024a; Wu et al.），\(G\) 可以拆成若干 reasoning path：\(G=\{P_i\}_{i=1}^{|G|}\)，第 \(i\) 条 \(P_i=(p_{i1}\rightarrow p_{i2}\rightarrow\cdots\rightarrow p_{iL_i})\) 是长度为 \(L_i\) 的一条逻辑链；第 \(j\) 个节点 \(p_{ij}\) 对应 \(\mathcal{B}\) 中的实体，并带有类别 \(E_{p_{ij}}\) 和从查询抽出的文本限制 \(T_{p_{ij}}\)。图 1(a) 那条 “Publications by Point…” 查询就有两条路径：\(P_1=(\text{Institution}\rightarrow\text{Author}\rightarrow\text{Paper})\)，\(P_2=(\text{Field-of-Study}\rightarrow\text{Paper})\)；\(P_1\) 第一个节点的类别是 Institution，文本限制是 Point Park University。符号表收在附录 Table 6。要解决的问题是：给定查询 \(Q\)，检索出能回答它的实体集 \(C\subseteq V\)。

文本检索看查询和文档两边的文本信号。常见做法是在全部文档 \(\mathcal{D}\) 里取与 \(Q\) 文本相似度最高的 Top-K，相似度可以是词法的或语义的（Vijaymeena and Kavitha, 2016）。MoR 里的文本检索，是用查询中的文字描述去对文档，例如图 1 里的 “stellar populations in tidal tails”。结构检索则是对知识图谱、SQL 这类结构化库施加预定规则（Guo et al., 2023），常见的是图遍历（如 BFS、DFS）和按规则抓取（Jiang et al., 2023）。MoR 的结构检索沿着生成的 planning graph，去走特定类别的邻居；图 1(a) 的例子是，Author 的邻居里只有类型为 Paper 的才能被走到。第 3 节起才是三阶段框架，此处不展开。
