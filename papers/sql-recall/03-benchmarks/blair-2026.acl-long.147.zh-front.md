> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文标题：** Bridging Language and Items for Retrieval and Recommendation: Benchmarking LLMs as Semantic Encoders

**作者：** Yupeng Hou、Jiacheng Li、Xiangjun Fu、Zhankui He、An Yan（UC San Diego），Xiusi Chen（UC Los Angeles），Julian McAuley（UC San Diego）。前三人同等贡献。

**场合：** ACL 2026 长文，Proceedings of the 64th Annual Meeting of the ACL (Volume 1: Long Papers)，页 3251–3265，2026 年 7 月 2–7 日。

**PDF：** `blair-2026.acl-long.147.pdf`

## Abstract

摘要认为推荐系统长期依赖特征工程，但物品文本一直难用好。LLM 已经可以被当成语义编码器，可是选模型时人们常看通用嵌入基准 MTEB，忽略推荐任务自己的特点。作者因此提出 BLAIR，用来评测 LLM 在推荐场景里当语义编码器的表现。三件贡献写在摘要里：Amazon Reviews 2023，超过 5.7 亿条评论、4,800 万件物品；一套覆盖序列推荐、协同过滤和商品搜索的统一基准；以及新的复杂查询商品搜索任务，同时有半合成数据和真实数据。实验比较 11 个领先的 LLM 编码器。摘要给出的判断是：MTEB 上的名次不能预测推荐里的编码器名次；简单任务上，更大的编码器通常更好，任务变复杂后这个效应变弱；复杂查询上，半合成数据和真实数据的结果高度相关，所以半合成数据可以当便宜的评测代理。

## 1 Introduction

第 1 节把问题从「文本特征有用」推到「缺一个推荐专用的编码器基准」。物品标题、描述、评论被说成推荐里最常见的文本。早期内容推荐靠关键词，后来用预训练模型直接编码文本，但预训练域和推荐域之间有缝。LLM 的泛化能力让人开始把它们冻住，当成语义编码器，再接到下游推荐模型上。作者指出，这一步的模型选择仍借用 MTEB 一类通用榜，那些榜覆盖分类、聚类、检索，并不对应「编码之后还要做序列推荐、协同过滤或商品搜索」。

贡献在节末收成三条，与摘要一致，并补上实验层面的三点观察，仍放在第 1 节的预告里，细节留给后文：编码器名次与 MTEB 脱节；规模效应随任务变复杂而减弱；半合成复杂查询与真实复杂查询同向。这一节没有展开具体 NDCG 表。

## 2 Related Work

第 2 节用三条并列的文献线，把 BLAIR 和已有基准分开。

**Semantic Encoders in Recommendation。** 内容推荐从抽关键词、学用户与物品的协同关系，走到用预训练模型直接编码标题和描述。作者指出这些编码器常有域差。近期工作开始用 LLM 当推荐里的语义编码器，但「换一个 LLM 会怎样改变下游」仍不清楚。这一句是后文实验的动机，不是实验结果。

**Benchmarking Text Embeddings。** BEIR 评信息检索，MTEB 与 MMTEB 把评测扩到分类和聚类，BRIGHT 关注需要推理才能找出相关文档的检索。作者把自己的目标和这些榜分开：要评的是嵌入模型当推荐语义编码器，不是把通用检索榜换一个域再跑一遍。他们认为编码器在推荐里需要的能力不同。

**Benchmarking LLMs for Recommendation。** 已有 LLM 推荐基准被收成三类：当购物代理在网页上行动；测购物知识和用户意图理解；把 LLM 自己当成推荐模型。作者声称，把 LLM 专门用来编码推荐里的文本特征，就他们所知还没有这样的基准。第 3 节才开始写 Amazon Reviews 2023 的数据本身。
