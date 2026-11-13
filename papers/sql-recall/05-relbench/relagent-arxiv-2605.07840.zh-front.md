> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文标题：** RELAGENT: LLM Agents as Data Scientists for Relational Learning

**作者：** Xingyue Huang（Oxford），Louis Tichelman（TU Wien；AITHYRA），Jinwoo Kim（KAIST），Krzysztof Olejniczak（Oxford），İsmail İlkan Ceylan（TU Wien；AITHYRA；Oxford）。

**场合：** 首页写 40th Conference on Neural Information Processing Systems (NeurIPS 2026)，未写 Datasets and Benchmarks，也未写 workshop。arXiv:2605.07840。

**PDF：** `relagent-arxiv-2605.07840.pdf`

## Abstract

摘要把关系学习的现有路线收成三类：图模型（GNN、图 Transformer）、表格方法（表格基础模型）和序列方法（大语言模型），各自有长处也有限制。RELAGENT 让 LLM 当关系学习的自主数据科学家，分两段。搜索阶段，智能体使用数据库、验证和评估这三类工作区工具，写出 SQL 特征程序并选择预测模型。推理阶段，程序直接执行，不再调用 LLM。最终预测器由选中的 SQL 特征和下游模型组成。

## 1 Introduction

第 1 节把贡献收成五条。框架把关系学习定义成对「基于查询的特征」和「预测模型」的自主搜索，LLM 通过工具和数据库交互。学习回路靠验证反馈和评估工作区，用先前试验的结构化分析来改下一轮。搜索和推理分开，所以推理时的预测器不需要 LLM，并且快、确定、可解释。归纳偏置来自可执行查询：两条样本只要在选中的 SQL 特征上输出相同，预测就相同，而不是来自固定的图编码、序列顺序或某种网络结构。最后一条是在关系基准上与强基线比较，同时保留可解释性和可扩展性。首页还强调可以检查物化后的特征值，以及下游模型用了哪些特征。

## 2 Related work

第 2 节从表 1 开始对照。传统预测要人手把连接和聚合物化成任务专用的特征表，再做监督。表把方法按表示、访问方式、机制、归纳偏置和可解释性分开。表格方法在表上学习，访问方式是先摊平，机制是树或注意力，对行置换等变，解释在特征层。GNN 在图上学习，访问方式是局部内化。RELAGENT 的位置是：表示由 SQL 查询定义，解释对应到这些查询，而不是对应到一层消息传递。搜索算法和各基准上的数字留在后文。
