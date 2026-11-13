> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名**：HybGRAG_ACL2025.pdf

**原文标题**：HYBGRAG: Hybrid Retrieval-Augmented Generation on Textual and Relational Knowledge Bases

**作者**：Meng-Chieh Lee（Carnegie Mellon University；该工作在 Amazon 实习期间完成）、Qi Zhu、Costas Mavromatis、Zhen Han、Soji Adeshina、Vassilis N. Ioannidis、Huzefa Rangwala（以上 Amazon）、Christos Faloutsos（Carnegie Mellon University 与 Amazon）。通讯作者为 Qi Zhu、Vassilis N. Ioannidis、Christos Faloutsos。

**场合**：Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)，第 879–893 页，2025 年 7 月 27 日–8 月 1 日。

## 摘要

半结构化知识库（semi-structured knowledge base, SKB）把文本文档用关系连在一起。普通 RAG 从文档里取证据给大模型答题，Graph RAG（GRAG）则从结构化知识库取证据。许多问题同时依赖文本内容和实体之间的关系，论文称之为 hybrid questions；只走一条检索路径就不够。

作者先用经验分析说明现有方法为什么做不好 SKB 上的 hybrid question answering（HQA），再提出 HYBGRAG。系统由 retriever bank 和 critic module 组成，并被概括成四点：能根据 critic 的反馈自动改输出（Agentic）；用同一套检索库处理既要文本又要关系的问题（Adaptive）；用可看懂的 refinement path 解释决策（Interpretable）；在 HQA 基准上超过全部基线（Effective）。在 STARK 上，Hit@1 的平均相对提升为 51%。

## 1 Introduction

RAG（Lewis et al., 2020; Guu et al., 2020）让大模型能查阅非结构化文档，从而做开放域问答。GRAG 把检索对象换成文档之间有关系的结构化知识库，现有工作大致分两路：从知识图谱抽关系、用大模型做 KBQA；或在文档库上补关系以改善开放域问答。更新的问题是 HQA（Wu et al., 2024b）：给定 SKB——即知识图谱加上挂在实体上的文本文档——问题同时要文本侧面和关系侧面。图 1 用“John Smith 发表过哪些 nanofluid heat transfer 论文”说明这一点：主题在文本里，作者关系在图里。

经验分析给出两个原因，说明单独的 RAG 或 GRAG 不够。第一，它们各自只取一种信息：RAG 看不见文档之间的连接，GRAG 又容易把文本侧面误当成关系侧面（图 1(a)(b)）。第二，两种侧面并不总是分得开。question routing（Li et al., 2024b）一旦把 “nanofluid heat transfer papers” 和 “by John Smith” 搞混，检索就会偏掉（图 1(c)）。

HYBGRAG 用 retriever bank 同时使用文本和关系信息，并用 self-reflection（Renze and Guven, 2024）按 critic 的反馈反复修正路由；这条修正路径被比作 chain-of-thought，用来解释性能从何而来。框架本身也可以换到别的问题上。贡献按 Agentic、Adaptive（文本、关系、混合问题共用一套框架）、Interpretable、Effective 四条列出。表 1 比较 Regular RAG、Think-on-Graph、AVATAR 与 HYBGRAG：在 Agentic、Adaptive（ODQA / KBQA / HQA）和 Interpretable 上，只有 HYBGRAG 被标成全部满足，基线各自缺不只一项。图 2 称其在 STARK 上 Hit@1 最多高出基线 21%。正文给出的相对提升是：相对次优基线，STARK-MAG 的 Hit@1 提高 47%，STARK-PRIME 提高 55%。

## 2 Proposed Insights: Challenges in HQA

这一节先定义 HQA，再用两个实验提出尚未被现有方法解决的挑战，作为后面方法设计的依据。

**2.1 Problem Definition。** SKB 包含知识图谱 \(G=(E,R)\)（实体集与关系集），以及文档集 \(D=\bigcup_{i\in E} D_i\)，其中 \(D_i\) 是挂在实体 \(i\) 上的文档；实体类型、关系类型分别记为 \(T_E\)、\(T_R\)。每道 hybrid question 同时涉及文本信息和关系信息。HQA 的任务是：给定这样的 SKB 和问题 \(q\)，检索文档集合 \(X\subseteq E\)，使其中每篇文档同时满足 \(q\) 的关系侧面和文本侧面。

**2.2 C1: Hybrid-Sourcing Question。** 作者要验证：答题是否必须同时用到文档和图谱，以及两边的有用信息是否重叠。文本检索用 vector similarity search（VSS; Karpukhin et al., 2020），在 “ada-002” 嵌入空间里比较问题和文档。关系检索用 Personalized PageRank（PPR; Andersen et al., 2006）：由 Claude 3 Sonnet 标出主题实体后做随机游走，再按图谱连通性给邻居排序。表 2 在 STARK-MAG 上报告：文本检索 VSS 的 Hit@1 / Hit@5 为 0.2908 / 0.4961，图检索 PPR 为 0.2533 / 0.5523；若有一个总能选对检索器的 Optimal Routing，则升到 0.4522 / 0.7463。两边单独看旗鼓相当，但最优路由明显更高，说明各自擅长的题目重叠不多，需要把两种检索合在一起。由此得到 Challenge 1（Hybrid-Sourcing Question）：HQA 里存在必须同时依靠文本信息和关系信息才能答对的问题。

**2.3 C2: Refinement-Required Question。** KBQA 常常默认目标实体已经落在抽出的子图里（Lan et al., 2022）。HQA 同样要从 SKB 的图谱里抽子图，但混合问题同时含文本侧面和关系侧面，大模型第一次往往读不准。实验让 Claude 3 Sonnet 从问题里抽出关系侧面，也就是主题实体和用来抽子图的有用关系；若子图没盖住目标实体，再由 oracle 要求它带反馈多做一轮。表 3 在 STARK-MAG 上的 hit rate 为：1 轮、无反馈 0.6769；2 轮、Simple 反馈 0.7914；2 轮、Corrective 反馈（指出抽错的部分，例如主题实体不对）0.9231。简单重做已经明显变好，指出错误后更好。原因是模型会把文本侧面误认成关系侧面；图 1(c) 的例子里，它第一次把文本侧面当成类型为 “field of study” 的实体。由此得到 Challenge 2（Refinement-Required Question）：在 HQA 中，大模型第一次尝试往往分不清文本侧面和关系侧面，需要后续修正。
