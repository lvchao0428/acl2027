# Text2VectorSQL: Towards a Unified Interface for Vector Search and SQL Queries

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`Text2VectorSQL_arXiv2506.23071.pdf`。

## Abstract 摘要

非结构化数据的激增，对传统数据库接口构成了根本挑战。Text-to-SQL 虽已使结构化数据的获取得以普及，却仍无法解释语义查询或多模态查询。与此同时，向量搜索（vector search）已成为查询非结构化数据的事实标准，但它与 SQL 的结合——称为 VectorSQL——仍依赖人工编写查询，并且缺乏标准化的评测方法，从而在其潜力与实际应用之间留下显著缺口。为弥合这一根本缺口，我们提出并形式化 Text2VectorSQL，这是一项新任务，旨在建立统一的自然语言接口，以便无缝查询结构化数据与非结构化数据。为推动这一新方向的研究，我们给出一套完整的基础生态（foundational ecosystem），包括：（1）一条可扩展且稳健的流水线，用于合成高质量的 Text-to-VectorSQL 训练数据。（2）VectorSQLBench，该任务上首个大规模、多面向的基准，覆盖 3 种数据库后端（SQLite、PostgreSQL、ClickHouse）与 4 种数据源（BIRD、Spider、arXiv、Wikipedia）的 12 种不同组合。（3）若干为更细致的性能分析而设计的新评测指标。大量实验不仅证实了我们所训练模型具有较强的基线表现，也揭示了召回退化（recall degradation）挑战：把 SQL 过滤与向量搜索结合，可能比传统的过滤向量搜索造成更明显的结果遗漏。通过定义核心任务、交付必要的数据与评测基础设施，并指出关键研究挑战，本文为构建下一代统一且智能的数据接口奠定了必要基础。代码仓库见 https://github.com/OpenDCAI/Text2VectorSQL。

索引词（Index Terms）：Text-to-SQL、Vector Search、Vector Database、Relational Database、Data Synthesis。

## I. INTRODUCTION 引言

现代数据版图的根本特征是一种二分：一边是由 SQL 的精确逻辑所导航的关系数据库这一结构化世界，另一边是庞大的非结构化数据——据估计占全部企业数据的 90% 以上 [1]——并越来越多地通过语义向量搜索来查询。这种分离对统一数据接口构成关键障碍，迫使用户在基于 SQL 的分析与基于向量的语义搜索之间来回切换不同接口。

一方面，Text-to-SQL 系统在把自然语言（natural language, NL）翻译为结构化查询方面取得了显著进展，使表格数据的获取得以普及。然而，它们天生看不见嵌入在文本、图像及其他模态等非结构化内容中的丰富语义。因此，它们无法回答诸如 “Find scientific papers discussing learned index structures published after 2020” 这类混合问题。

与此同时，向量搜索已成为基于相似度检索的事实标准，而将其集成进关系数据库——即 VectorSQL——有望弥合这一缺口 [2], [3]。不过，这一集成仍处于初期。编写有效的 VectorSQL 查询是一个人工且易错的过程，要求同时具备向量搜索与 SQL 查询两方面的专门知识。更关键的是，把自然语言翻译为 VectorSQL 的学术研究完全缺位。

为弥合这一根本缺口，并为新一类数据交互范式铺路，我们提出 Text2VectorSQL。然而，实现这一设想并非易事，并面临三项核心挑战：

- 训练数据极度稀缺：不存在把自然语言与 VectorSQL 查询配对的公开数据集，可供模型训练或微调。
- 评测空白：没有既定的基准或指标来衡量 Text2VectorSQL 模型的性能，从而阻碍可复现研究。
- VectorSQL 翻译与执行中准确率与效率的权衡：向量搜索与 SQL 过滤之间的相互作用，可能导致大量却悄无声息的召回失败。

为应对这些基础障碍，我们构建了一套基础生态。首先，为克服数据稀缺，我们开发一条可扩展且稳健的流水线，用以合成高质量、多样化的 Text-to-VectorSQL 训练数据。其次，为填补评测空白，我们构建 VectorSQLBench，该任务上首个大规模、多面向的基准，覆盖数据库后端（SQLite、PostgreSQL、ClickHouse）与数据源（BIRD、Spider、arXiv、Wikipedia）的 12 种不同组合。VectorSQLBench 还配有一套新评测指标，例如基于排序的分数（rank-based score）与分解准确率（decomposed accuracy），以便在执行准确率之外做更全面、更细粒度的评测。

最后，借助这一生态，我们的大量实验得到了关键认识。尽管所训练的模型达到了最先进的性能，分析揭示了一个此前考察不足的关键挑战，我们称之为 recall degradation。我们发现，流行的后过滤（post-filtering）做法——先得到向量搜索结果，再用 SQL 谓词加以过滤——可能比传统的过滤向量搜索更明显地遗漏正确结果。例如，在涉及 ‘JOIN’ 操作的复杂查询中，post-filtering 可能悄无声息地丢弃超过 30% 的正确结果。这一发现把 Text2VectorSQL 从单纯的翻译问题，提升为与查询优化及执行策略深度交织的复杂挑战。

图 1：Text2VectorSQL 任务示意图。下方场景说明，把 SQL 查询与向量搜索结合，如何实现语义过滤（semantic filtering）、多模态匹配（multi-modal matching）与检索加速（retrieval acceleration）。这些能力对通用自然语言接口不可或缺。图内文字因版面抽取交错，可辨认的标签包括 “Find Papers on “Learned Indexes” after 2020”、“User Input”、“Natural Language Question”、“Text2VectorSQL”、“Title”、“Year”，以及 “… 2021”、“… 2023”、“… 2025”、“SELECT ...”、“WHERE year > 2020”、“ORDER BY”、“embedding <->...”、“Semantic Filtering”、“Multimodal Matching”、“Retrieval Acceleration”、“Abstract”、“Year”、“B+-Tree 2019”、“Crowdsourcing 2021”、“AI-based Index 2023”、“Learned Bloom Filter 2024”、“Beach in the evening”、“Fuzzy Matching”、“Scan”、“O(N)”、“Title (%LLM%)”、“... LLM as DBA ...”、“... language model ...”、“HNSW”、“O(logN)”、“Unified Querying”、“SQL & Vector”、“Execution Results”、“0.5”、“0.4”、“0.8”、“Vector Search”。各标签之间的连线与版面关系【抽取不清】。

本文的主要贡献概括如下：

- 任务形式化（Task Formalization）。我们首次形式化定义 Text2VectorSQL 任务，为统一自然语言与结构化及非结构化数据的交互确立清晰目标，从而克服传统 Text-to-SQL 的固有局限。
- 基础生态（A Foundational Ecosystem）。我们提供一套完整生态，以推动这一新兴方向的研究。其中包括一条用于合成高质量训练数据的可扩展流水线，以及 VectorSQLBench，即首个用于 Text2VectorSQL 评测的综合基准。VectorSQLBench 的广度（12 种数据集组合）与深度（所提出的指标）为整体评估提供了稳健基础。
- 实证分析与关键发现（Empirical Analysis and Key Findings）。通过在多个数据集与多个数据库上的大量实验，我们为该任务建立了较强的基线性能。更重要的是，分析揭示了 VectorSQL 执行中 recall degradation 这一关键挑战。这一认识指出了未来研究的一个关键方向：协同优化查询生成与执行。

我们的数据、模型与评测脚本公开于 https://github.com/OpenDCAI/Text2VectorSQL。

## II. PRELIMINARIES 预备知识

本节介绍支撑本文工作的基础概念：向量搜索，以及 VectorSQL 范式。

### A. Vector Search 向量搜索

向量搜索从集合中检索那些高维向量表示与给定查询向量最相似的条目。这是现代语义信息检索与多模态信息检索的基石 [4]–[6]。

**Definition 2.2 (Vector Search Task) 定义 2.2（向量搜索任务）。** 设 \(D\) 为非结构化条目的集合（例如文档、图像），\(E: D \rightarrow \mathbb{R}^{d}\) 为嵌入模型，把任意条目 \(d \in D\) 映射为 \(d\) 维向量 \(\vec{v} = E(d)\)。给定查询文本 \(Q_{\mathrm{txt}}\)，其对应查询向量 \(\vec{q} = E(Q_{\mathrm{txt}})\)，相似度函数 \(\mathrm{sim}(\cdot,\cdot)\)（例如余弦相似度或点积），以及整数 \(k\)，向量搜索任务是找到一个大小为 \(k\) 的结果集 \(R_{V} \subset D\)，其中包含与查询最相似的 top-\(k\) 条目：

\[
R_{V} = \arg\max_{R \subset D,\ |R|=k} \sum_{d_{i} \in R} \mathrm{sim}(\vec{q}, E(d_{i}))
\]

为了在大规模数据集上保持效率，这通常用近似最近邻（Approximate Nearest Neighbor, ANN）搜索算法实现，以获得对数时间复杂度。在许多实际应用中，该任务被扩展为过滤向量搜索（filtered vector search）：检索到的条目不仅要在语义上与查询相似，还要满足某个过滤谓词。

### B. Text-to-VectorSQL Text-to-VectorSQL

**Definition 2.3 (VectorSQL Query) 定义 2.3（VectorSQL 查询）。** 一条 VectorSQL 查询记为 \(Q_{VSQL}\)，在概念上由结构化过滤与语义向量搜索两部分组成：

- SQL 谓词分量（SQL Predicate Component，\(Q_{S}\)）：一条标准 SQL 查询或子查询，对结构化数据列施加约束（例如 ‘WHERE’ 与 ‘JOIN’ 子句）。
- 向量搜索分量（Vector Search Component，\(Q_{V}\)）：一条语义搜索指令，由元组 \((\vec{q}, k)\) 定义，其中 \(\vec{q} \in \mathbb{R}^{d}\) 为查询向量，\(k\) 为最近邻个数。

执行一条 \(Q_{VSQL}\) 查询，通过协调 \(Q_{S}\) 与 \(Q_{V}\) 得到结果集。对过滤向量搜索这一 VectorSQL 的简化形式而言，这种协调可分为两种策略：

- 预过滤（Pre-filtering (Filter-then-Search)）。该策略优先保证准确率：先用 SQL 谓词划定数据的一个精确子集，再在该子集内做向量搜索。
  1. Filter：执行 SQL 查询 \(Q_{S}\)，选出精确的条目子集：\(D' = \{d \in D \mid d\ \mathrm{satisfies}\ Q_{S}\}\)。
  2. Search：只在过滤后的子集上做向量搜索，找出 top \(k\) 结果：\(R_{\mathrm{pre}} = \mathrm{ANN\ Search}(\vec{q}, k, D')\)。

  该方法保证所有结果都符合结构化条件，但可能低效，因为它可能使预先构建的 ANN 索引所依赖的假设不再成立，从而被迫对 \(D'\) 做代价高昂的暴力扫描。

- 后过滤（Post-filtering (Search-then-Filter)）。该策略优先保证速度：先做近似向量搜索以缩小候选范围，再施加 SQL 过滤。
  1. Search：执行一次 ANN 搜索，得到初始候选集 \(R_{V} = \mathrm{ANN\ Search}(\vec{q}, k')\)，其中 \(k'\) 可以大于最终所需的 \(k\)，以便计入将被滤掉的条目。
  2. Filter：把 SQL 谓词 \(Q_{S}\) 施加于检索到的候选：\(R_{\mathrm{post}} = \{d \in R_{V} \mid d\ \mathrm{satisfies}\ Q_{S}\}\)。

实际上，SQL 过滤与语义相似度通常分别被视为硬约束与软约束。预过滤的执行被视为高保真；后过滤虽然高效，但可能因 recall degradation 而检索不到足够多的正确结果。

最后，在确立 VectorSQL 的定义之后，我们可以定义 Text-to-VectorSQL 任务。

**Definition 2.4 (Text-to-VectorSQL Task) 定义 2.4（Text-to-VectorSQL 任务）。** 给定混合数据库模式 \(S_{\mathrm{hybrid}}\)（其中包含带向量列的关系表）以及自然语言问题 \(Q_{NL}\)，Text-to-VectorSQL 任务是学习一个映射函数 \(f_{\mathrm{T2VSQL}}\)，把该问题翻译为一条合法的 VectorSQL 查询 \(Q_{VSQL} = f_{\mathrm{T2VSQL}}(Q_{NL}, S_{\mathrm{hybrid}})\)。
