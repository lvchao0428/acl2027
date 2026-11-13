> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名**：LIMIT_arXiv2508.21038.pdf

**原文标题**：On the Theoretical Limitations of Embedding-Based Retrieval

**作者**：Orion Weller（Google DeepMind 与 Johns Hopkins University）、Michael Boratko、Iftekhar Naim、Jinhyuk Lee（Google DeepMind）。

**场合**：ICLR 2026 会议论文；arXiv:2508.21038v2 [cs.IR]，2026 年 3 月 12 日。

## 摘要

向量嵌入承担的检索任务越来越多，已经扩到推理、指令跟随、编程等。新基准默认它们要应付任意查询、任意相关性定义。此前已有人指出向量嵌入的理论限制，但常见看法是：困难只来自不现实的查询，现实查询可以用更好的数据和更大的模型绕过去。

本文要说明，这些限制会在很现实、而且查询极简单的设定里出现。论证接到学习理论中已有的结果：某个查询能够作为结果返回的文档 top-k 子集，其数目受嵌入维度限制。即便用可自由参数化的嵌入、直接在测试集上优化，这一限制仍然成立。作者据此构造了贴近真实用语、但按该理论加压的数据集 LIMIT。任务本身很简单，当时的前沿嵌入模型仍然失败。结论指向现有单向量范式的上限，并呼吁后续工作发展能越过这一基本限制的技术。摘要没有给出具体分数。

## 1 Introduction

近二十年信息检索从以 BM25（Robertson et al., 1995）为代表的稀疏模型，转到以神经语言模型为骨干的模型（Lee et al., 2019; Craswell et al., 2020; Izacard et al., 2021; Wang et al., 2022）。主流用法是单向量，也就是 dense retrieval：整个输入压成一个嵌入。这些模型能泛化到新数据集，任务也越来越难（Thakur et al., 2021; Enevoldsen et al., 2025; Lee et al., 2025）。指令跟随检索又把要求推到“任意相关性定义、任意查询”（Weller et al., 2025a;c; Song et al., 2025; Xiao et al., 2024; Su et al., 2024）。QUEST（Malaviya et al., 2023）用逻辑算子组合概念，例如 “Moths or Insects or Arthropods of Guadeloupe”；BRIGHT（Su et al., 2024）则把相关性定义成需要推理，例如给定一道 Leetcode 题，去找共用同一子任务（如 dynamic programming）的其他题。社区提出这些基准，实际上是在把 dense retriever 推向“任何可定义的任务”。

本文不再加一个经验基准来探上限，而是问几何表示本身的限制。嵌入落在向量空间里，可以借用已有的数学结果（Papadimitriou & Sipser, 1982）。作者把线性代数里的已知结论接到神经检索上：对一组相关文档与查询的组合，给出表示它所需嵌入维度的下界。具体地说，给定维度 \(d\)，总存在一些 top-k 文档组合，无论查询怎么写都无法被返回。为表明这与具体模型或训练集无关，他们直接用测试数据优化向量本身，观察每个维度 \(d\) 都有一个临界点：文档数一大，就装不下全部组合。把不同 \(d\) 的临界点收起来，这种关系可以用一个多项式经验地拟合。

再往前一步，他们按这些理论限制做成一个简单但贴近自然语言的数据集 LIMIT（数据与代码在 https://github.com/google-deepmind/limit）。图 1 示意其构造：对 \(N\) 篇文档测试相关性的全部组合（图中是三篇文档、每个查询两篇相关），再用直白的对应关系落到句子上，例如 “Who likes Quokkas?”，以及 “Jon Durben likes Quokkas and Apples.” 这类文档。尽管问法像 “who likes Apples?” 一样简单，在 MTEB（Enevoldsen et al., 2025）上的前沿嵌入模型（Lee et al., 2025; Zhang et al., 2025）仍然很难，小维度模型用常规优化几乎做不到。贡献有三：嵌入模型基本限制的理论根据；用自由嵌入优化做的最好情形分析，说明该证明不依赖某种数据集写法；以及一个连前沿模型也解不开的自然语言实例 LIMIT。引言据此提醒：神经嵌入已经很成功，但学术评测只覆盖很少的查询，而且常常被过拟合，于是把限制藏住了。一旦任务要求返回越来越多的 top-k 组合（例如用指令和逻辑算子把原先无关的文档连进同一个相关集），就会碰到可表示组合数的上限。做评测时应意识到这一点；若要覆盖任意查询和任意相关性定义，应考虑 cross-encoder、多向量或表达力更强的相似度函数。引言没有印出具体的维度临界值或检索分数。

## 2 Related Work

**2.1 Neural Embedding Models。** 嵌入模型近年进步很快（Lee et al., 2019; Craswell et al., 2020; BehnamGhader et al., 2024），从纯文本网页搜索走到指令跟随和多模态表示，步伐大体跟着语言模型：预训练语言模型（Hoffmann et al., 2022）、多模态语言模型（Li et al., 2024; Team, 2024）、指令跟随（Zhou et al., 2023; Ouyang et al., 2022）。检索里被点名的例子包括多模态的 CoPali（Faysse et al., 2024）和 DSE（Ma et al., 2024），指令跟随的 Instructor（Su et al., 2022）和 FollowIR（Weller et al., 2024a），以及把预训练语言模型改成嵌入器的 GritLM（Muennighoff et al., 2024）和 Gemini Embeddings（Lee et al., 2025）。本文为简化只写文本，但结论针对任何领域、任何模态的单向量嵌入：要表示的空间一旦因指令或多模态变大，就会撞上这些理论限制。

**2.2 Empirical Tasks Pushing the Limits of Dense Retrieval。** 检索模型已被推出最初用途：覆盖很多领域（Thakur et al., 2021; Lee et al., 2024）、很多指令（Weller et al., 2024a; Zhou et al., 2024; Oh et al., 2024; Weller et al., 2025b），以及在查询上做推理（Xiao et al., 2024; Su et al., 2024）。焦点从关键词匹配转到要表示语言的完整语义。于是，把原先互不相关的文档放进同一个 top-k 相关集变得常见，模型必须能表示的组合数随之增加；脚注指出，用逻辑算子（如 X and Y）就能轻易把任意两篇文档连起来。经验上已有人碰过模型上限：Reimers & Gurevych (2020) 发现更小的嵌入维度会带来更多假阳性，语料越大越明显；Ormazabal et al. (2019) 讨论跨语言设定；Yin & Shen (2018) 把维度和偏差–方差权衡联系起来。本文的差别是：把嵌入维度和它能检索的 top-k 集合从理论上连起来，并同时给出经验上的限制。

**2.3 Theoretical Limits of Vectors in Geometric Space。** 语义空间里找最近邻在数学中由来已久。Voronoi 图可追溯到 1644 年，1908 年被形式化（Voronoi, 1908）。order-k Voronoi 图按最近的 \(k\) 个点划分空间（Clarkson, 1988），区域数等于大小为 \(k\) 的不同检索集数目，但这个量很难给出紧的界（Bohler et al., 2015; Lee, 1982; Chen et al., 2023）。本文换一个问题：不问某个构型能实现多少个 \(k\)-子集，而问要在带分数间隔的前提下实现全部 \(k\)-子集，嵌入维度至少要多大。用经典的球体装填体积论证（Vershynin, 2018; Conway et al., 1999），得到用文档数 \(n\)、\(k\) 和间隔 \(\gamma\) 表示的维度下界。它和 Johnson–Lindenstrauss 引理（Johnson et al., 1984）相关但方向不同：后者给出保持 \(n\) 个点两两距离的充分维度，本文给出实现全部检索集并留出间隔的必要维度。间隔如何控制可实现构型的复杂度，也平行于统计学习里的 fat-shattering dimension（Kearns & Schapire, 1994）以及线性分类器的间隔泛化界（Bartlett, 2002; Vapnik, 1998）：更大的间隔同样限制假设类的容量。本节没有给出具体的维度数值表。第 3 节起是形式化结果，此处不展开。
