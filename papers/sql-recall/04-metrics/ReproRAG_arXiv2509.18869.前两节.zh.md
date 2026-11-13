> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

- 原文件名：ReproRAG_arXiv2509.18869.pdf
- 原文标题：On The Reproducibility Limitations of RAG Systems
- 作者：Baiqiang Wang、Dongfang Zhao（University of Washington, Seattle）；Nathan R Tallent、Luanzheng Guo（Pacific Northwest National Laboratory, Richland）
- 场合：arXiv:2509.18869v1 [cs.DC]，2025 年 9 月 23 日。PDF 页眉写作 Workshop ’25，会议名与页码仍是占位符

## 摘要

这篇论文把 RAG 的可靠性问题收束到检索阶段的非确定性。生成式科学工作流要用 RAG 接上快速变化的知识库，但同一套输入多次运行，检索结果可以不一样。ReproRAG 是一套评测框架，用来系统测量向量检索的可复现性。它覆盖整条流水线里的不确定来源：embedding 模型、数值精度、检索算法、硬件配置，以及分布式执行环境。

度量上，摘要点名 Exact Match Rate、Jaccard Similarity 和 Kendall’s Tau，用来刻画可复现性与性能之间的取舍。作者给出的主要观察是：不同 embedding 模型对 RAG 可复现性的影响很大。框架开源，定位是给研究和工程人员做部署核验、可复现性对比和设计取舍，服务于更可信的 scientific AI。

## 1 Introduction

第 1 节的论证从用途推到测量缺口。RAG [12] 已是知识密集型系统、尤其是科学研究 [20] 的基本架构：用大规模语料里检索到的证据约束 LLM，减轻事实性幻觉 [8]，并提供领域内、较新的信息。系统一旦从原型进入科学工作流，可靠性和一致性就变成 Trustworthy AI [17] 的核心问题。威胁来自非确定性。这在并行和深度学习系统里已有记录 [16]：输入相同，多次运行结果仍可能不同，而且不一致经常出在向量检索，不是出在生成本身。向量检索已有性能评测 [1]，但不管可复现性，研究者只好靠轶事或临时测试。没有严格测量，就谈不清性能和一致性怎么换，也没法核验生产部署，或放心沿用先前的计算结果。

ReproRAG 被定义成填这个缺口的测试框架，贡献分成四条。第一，开源实现，用一组指标量化 RAG 检索流水线多个维度的不确定性。第二，大规模实验建立一种 uncertainty hierarchy：embedding 模型的选择和动态插入数据，是结果波动最主要的来源。第三，挑战常见假设：核心 ANN 检索算法和分布式协议可以做到运行之间完全可复现；常见的软件层 determinism 开关，对现代 embedding 模型可能看不出效果。第四，给实践者的可操作结论，包括对精度引起的 “embedding drift” 的量化，以及某些模型上，偏性能的设置可以加速、同时不损害可复现性。这些是引言里的主张，具体实验数字不在前两节。

## 2 Background and Related Work

2.1 先解释向量检索为什么会不确定。现代 RAG 靠 Approximate Nearest Neighbor（ANN）在高维空间里找文档。FAISS（Facebook AI Similarity Search）[9] 一类库用速度换精确最近邻，这个交换本身就能引入非确定性。HNSW [13] 建的是概率图，构图时的选择可以带随机性。IVF 先用 k-means 划分空间，随机初始化会使索引结构不同 [7]。LSH [5] 用随机投影把相近项分到一起，投影的选取本身是随机的。算法随机性之外，多核 CPU 或 GPU 上浮点运算的重排，也会让并行执行不可复现。

2.2 把工作放在三个交叉点上。科学工作流里，LLM 被用来加速发现 [20]，RAG 负责把模型锚到专门、更新的文献，服务假设生成和文献综述；SciTrust [6] 评的是 LLM 本身是否可信，并假设送给它的检索输入稳定可复现，本文则补检索这一段。计算可复现性危机在计算科学里已有讨论 [4]；高性能计算社区用 Artifact Description and Evaluation 等机制推动可重复性 [3]，ReproRAG 是把这套测量原则用到大规模向量检索。评测传统方面，MLPerf [15] 测训练和推理性能，ann-benchmarks [1] 比较不同 ANN 算法的性能；既有评测看速度和准确率，作者主张 ReproRAG 是第一套系统量化这类系统一致性与确定性行为的框架。
