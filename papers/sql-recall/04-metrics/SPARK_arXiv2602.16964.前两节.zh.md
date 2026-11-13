> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

- 原文件名：SPARK_arXiv2602.16964.pdf
- 原文标题：SAGE: Structure Aware Graph Expansion for Retrieval of Heterogeneous Data
- 作者：Prasham Titiya、Rohit Khoja（共同一作）、Tomer Wolfson、Vivek Gupta（共同二作）、Dan Roth。Titiya、Khoja、Gupta 属 Arizona State University；Wolfson、Roth 属 University of Pennsylvania
- 场合：arXiv:2602.16964v1 [cs.IR]，2026 年 2 月 18 日
- 说明：PDF 文件名用的是 SPARK，首页标题是 SAGE。SPARK 是文中用于显式 schema 图的检索代理，不是论文主标题。

## 摘要

异构语料上的检索增强问答，需要把文本、表格和图节点上的证据连起来。实体级知识图谱能做结构化访问，但构建和维护贵，查询时遍历也不划算。常规 retriever-reader 则对切块做扁平相似度检索，跨模态的多跳证据链会断。SAGE（Structure Aware Graph Expansion）分成两段：离线用元数据相似度建 chunk 级图，并用分位数剪枝；在线先由基线检索器取出 k 个种子 chunk，扩展一跳邻居，再用 dense 加 sparse 检索筛出额外的 k′ 个 chunk。

初始检索器按语料类型换。隐式跨模态语料用 hybrid dense+sparse；显式 schema 图用 SPARK（Structure Aware Planning Agent for Retrieval over Knowledge Graphs），一个代理式检索器。摘要给出的结果是：在 OTT-QA 和 STaRK 上，SAGE 的检索 recall 比基线高 5.7 和 8.5 个点。代码见 https://github.com/CoRAL-ASU/sage 。

## 1 Introduction

第 1 节论证扁平 RAG 为什么接不住异构证据。RAG（Lewis et al., 2020）把 LLM 锚到外部知识，已是领域问答的常规做法。多数系统把文本切块独立索引，再用稀疏、稠密或混合相似度检索（Mandikal and Mooney, 2024; Arabzadeh et al., 2021; Zhang et al., 2024; Chen et al., 2022）。文档、表格和结构化元数据混在一起时，这种设计不够用：切块在嵌入空间里彼此无关，结构上相连、但和查询只是弱相似的中间证据经常被丢掉。文中的例子是一部由 Trevor Eyster 出演的电视剧及其原著：演员、改编关系和作者信息要串起来，单靠相似度搜不回来。Figure 1 把 SAGE 画成 seed 再 expand：从一块相关内容扩到相连邻居，补上扁平检索漏掉的电影与导演证据。

已有工作用图来做多跳（Edge et al., 2024a; Jimenez Gutierrez et al., 2024; Mavromatis and Karypis, 2024），大致两类。知识图谱把知识写成带类型的实体–关系三元组，可用 Cypher（Francis et al., 2018）或 SPARQL 做符号推理，但实体抽取和 schema 对齐成本高，适合 schema 稳定的领域。相似度图则把文本块、表片段或半结构化节点连起来，边来自嵌入相似度，不必显式抽实体。图好不好用取决于边：太密会引进假邻居，太稀则多跳走不通。粒度上也有取舍：实体级适合事实型问题，不擅长上下文或聚合问题；社区级更可扩展，细节更少。作者因此要一种居中的表示。

他们的回答是 chunk 级图。先取少量种子，再沿图扩展，把和查询弱相似、但经文档结构、元数据或共享上下文强相连的证据捞出来。节点是文本段或表段，保持局部连贯，不做显式实体抽取。图离线建成，与具体检索器解耦，查询时只做紧凑的邻域遍历。贡献有三条：SAGE 用 chunk 级扩展补扁平检索，并可接在现有检索器上；在固定预算下，相对强的扁平混合基线，OTT-QA 的 recall 提高 5.7 个点，STaRK 提高 8.5 个点，增益主要在隐式多跳和跨模态查询；对显式 schema 图另给 SPARK，在遍历时施加 schema 约束，并优于朴素的稠密扩展。Figure 2 对应这条流水线：离线按 title、topic、content、entities 等元数据建边并做分位数剪枝；在线由 k 个种子扩到 n 个一跳邻居，再重排选出 k′，最终上下文是 k+k′。

## 2 SAGE Approach

第 2 节把任务写成：语料是图 G = (V, E)，节点有正文 text(v)，可选元数据 meta(v)；对查询 q 返回排序后的证据节点 Rk(q)，相关证据应出现在 top-k。2.1 是离线建图，对文档切块加表片段建异构图，知识图谱则保留原有实体–关系 schema，过程与具体数据集无关，发生在查询之前。

节点有三种处理。文档按句切分，用重叠窗口 wi = [s_{i−1}, s_i, s_{i+1}] 送进句编码器（Reimers and Gurevych, 2019），相邻窗口的余弦相似度记为 s_i = cos(h_i, h_{i+1})；边界取这些相似度的第 20 百分位 θ = Percentile20({s_i})，文中等同于选出 top-80% 的 “drop” 位置，在 s_i ≤ θ 处切开，再用 LLM 为每块生成 topic、title 和 entities。表格由 LLM 写短描述和列描述，每段保留表题或描述、列名、列描述以及 5–10 行，兼顾纵向上下文和长度。半结构化对象各自当作一个 chunk，元数据来自名称、标题和长描述等文本字段。边由 Sentence-Transformer 对元数据编码后按模态连接：文档–文档看 topic、content 和实体重叠；表–表看列、标题和实体重叠；表–文档看 content 与列、topic 与标题、以及实体重叠；半结构化对象则按描述性元数据相连。相似度须超过经验分布的第 95 百分位才保留，以保持稀疏。同源的父子或结构链接、以及已有 schema 边另外保留。边上还存轻量元数据：表–表记下可连接的列名，文档–文档记下共享实体和置信度，表–文档记下共享实体，有的话还有行或列引用，供多跳时优先对齐查询实体或结构约束的邻居。

2.2 是在线检索，两阶段：基线取出 k 个种子，再扩展并剪枝出 k′ 个额外节点。文档图（OTT-QA 的文本和表）用 BM25（Robertson et al., 2009）加稠密余弦的混合打分，适合切块文本够长、相关性主要看表层语义的情况。半结构化知识库（SKB）上，BM25 和余弦会忽略边类型与带类型的关系，做不了多跳，还容易偏向同一节点类型。SPARK 因此让 LLM 代理看到实体 schema、关系和两种工具，交替规划：(1) Semantic Candidate Generation，用 HNSW（Malkov and Yashunin, 2018）按文本相似度和描述属性找节点，关键词未出现也能匹配；(2) Structural Expansion，在 Neo4j（Neo4j, Inc., 2026）里用受实体类型和关系约束的 Cypher 做多跳。计划执行后取 top-k 作为种子；若计划无结果，则退回 BM25 加余弦。Figure 3 画的就是问题加 schema 引导代理，把 HNSW 语义搜索和 Cypher 符号查询交织起来。文中指出混合检索在 STaRK 上表现差，并指向 Table 6；该表不在第 2 节内，此处不转写表中数字。无论种子从哪来，扩展算子相同：收集 k 个种子的全部一跳邻居，得到 n 个候选，再用 BM25 和稠密相似度相对查询重排，取 top-k′，与原种子并成 k+k′。Listing 1 把这写成 TopK(BL(q), k)、OneHopNeighbors、BM25DenseRank 再 Union。作者认为预计算的连接能抓住桥接证据、压低噪声，并避免查询时做全量节点两两比较。
