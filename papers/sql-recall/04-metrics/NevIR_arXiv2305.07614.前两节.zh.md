> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名**：NevIR_arXiv2305.07614.pdf

**原文标题**：NevIR: Negation in Neural Information Retrieval

**作者**：Orion Weller、Dawn Lawrie、Benjamin Van Durme（Johns Hopkins University）。

**场合**：arXiv:2305.07614v2 [cs.IR]，2024 年 2 月 26 日。

## 摘要

否定在日常语言里很常见，也一直是语言模型的弱项。信息检索已经把语言模型当成现代架构的骨干，但否定如何影响神经检索，几乎还没有人专门看。作者因此做了一个直接的基准：让检索模型给两篇只差否定的文档排序。

结果随架构差得很远：cross-encoder 最好，其次是 late-interaction，bi-encoder 和稀疏神经架构垫底。包括当时前沿模型在内的大多数检索模型并不理会否定，表现与随机排序相同，或者更差。在含否定的对比文档上继续微调能提高成绩，模型变大也有帮助，但机器和人之间仍有很大差距。代码和数据在 https://github.com/orionw/NevIR。摘要没有给出具体分数。

## 1 Introduction

自然语言处理里已有工作表明，语言模型读含否定的文本很吃力（Ravichander et al., 2022; McKenzie et al., 2022），也远不如人。检索模型既然以语言模型为起点，这个问题就会传到下游。可检索文献里谈否定的，主要还是神经网络出现之前的系统（Kim and Kim, 1990; McQuire and Eastman, 1998; Averbuch et al., 2004; Kim et al., 2019），现代神经检索几乎是空白。漏掉否定会在高风险场景出事：图 1 是 Google Search 在癫痫急救上的截图，网页原文在列“不要做”的事项（如 “do not ...”），搜索结果却把 “Hold the person down”“Put something in the person's mouth”“Administer CPR”“Give the person food or water” 这些条目当成该做的建议。法律、教育、政治里不难想象类似失败。日常查询也同样整类被忽略，例如某度假地不该住哪里、2023 年谁没拿 Oscar、OpenAI 有哪些关于 GPT-4 的信息没公布。

NevIR（读作 “never”）用来补这个空缺，材料来自已有的否定研究（Ravichander et al., 2022）：2,556 对对比文档，每对只在一处关键否定上不同。再众包为每对里的两篇文档各写查询，使每条查询只与其中一篇相关、与另一篇无关（图 2）。这样就能检查模型排序时有没有把否定算进去。图 2 的例子改自 CondaQA：两段都谈镍在 20 世纪被不锈钢（铁合金）取代，一篇写 “except in the United States and Canada”，另一篇写 “throughout the United States, Canada, and elsewhere in the Americas”。对应的两条查询分别问哪些国家没有替换、哪些国家替换了。图中的模型两次都把 Doc #1 排在 Doc #2 前面，成对准确率为零。

作者发现，几乎所有检索系统都忽略否定，往往对两条查询都把同一篇文档打得更高。前沿模型与随机排列文档对相比，接近持平，或者差得更多。进一步的分析是：尽管有否定词，bi-encoder 给两篇文档的表示几乎一样；ColBERT 这类 late-interaction 模型则在 MaxSim 里忽略否定词。在否定数据上继续微调能在 NevIR 上有所提升，但余地仍然很大，而且会让 MSMarco 这类传统基准略降。引言希望由此把注意力引向检索中的否定，并给出一份可用于训练和评测的数据。引言没有印出各模型的具体准确率。

## 2 Background

**2.1 Motivation** 与 **2.2 Neural IR。** 信息检索是按自然语言查询找相关信息，语言、领域（如法律）和目的（反论、列表、一般事实）都可以差很远。列表、反论，以及法律、医学这类领域语言，都会因更懂否定而受益。神经检索进步的同时，检索增强语言模型迅速增多，如 RAG（Lewis et al., 2020）、FiD（Izacard and Grave, 2021）、SeeKeR（Shuster et al., 2022）；生成式检索也已产品化，文中点名 Google 的 Bard、Bing Chat 和 You.com。语言模型和检索绑在一起、进入线上系统之后，否定这类失败就同时关系到公司和用户。自 2020 年以来，神经检索在多数情形下已经超过 BM25 一类传统稀疏方法（Karpukhin et al., 2020; Khattab and Zaharia, 2020）：给定大量训练数据，用对比损失学习文档与查询的关系，从而越过词面匹配、编码语义相似。近期工作关心零样本换领域；BEIR（Thakur et al., 2021）就是在多种检索数据上测泛化。本文同时提供不做微调的零样本设定，以及常规的训练/测试划分。

**2.3 Negation in NLP** 与 **2.4 Negation in IR。** 否定也是语言模型通常低于平均的地方（Li and Huang, 2009; He et al., 2017; Hartmann et al., 2021; Ettinger, 2020）。模型变大、提示方法改进后会好一些（McKenzie et al., 2022; Wei et al., 2022），但后续工作仍表明它们对付否定很吃力，需要新数据和新方法（Ravichander et al., 2022; Hossain et al., 2022）。检索模型以语言模型为骨干，否定会同样成为问题；而且检索要实时处理大量文档，受效率和延迟约束，不能像纯语言模型那样轻易换到更大的骨干。检索里否定长期是弱点。早期工作已说明，TF-IDF（Sparck Jones, 1972）和 BM25（Robertson et al., 1995）拿来即用时很难处理否定（Kim and Kim, 1990; Strzalkowski et al., 1995）。作者认为，针对神经模型的否定研究几乎没有发表。最接近的是论证检索（Wachsmuth et al., 2018; Bondarenko et al., 2022），BEIR 里也有：目标是为查询找反论，但“找反论”是任务设计隐含的，查询里刻意不含否定。这类数据里的否定比 MSMarco（Nguyen et al., 2016）多，却不是文档或查询的有意设计，还和隐含任务定义缠在一起。本文则明确在文档和查询两侧提供否定，并测量其影响。Opitz and Frank (2022) 把 AMR 解析特征（否定只是其中之一）用于改进 SBERT 训练，但他们只在 AMR 数据上评否定；本文关注的是检索排序，并为此建基准。

**2.5 Contrastive Evaluation。** 对比评测的做法是构造差别很小、但差别恰好卡在关键区分上的数据（Gardner et al., 2020; Kaushik et al., 2019）。检索里已有人用它看句子顺序（Rau and Kamps, 2022）、词汇结构（Nikolaev and Padó, 2023）、公理（Völske et al., 2021）、释义、拼写和语序（Penha et al., 2022）、基于大模型的查询与文档扩展（Weller et al., 2023a），以及事实性、正式程度、流畅度等（MacAvaney et al., 2022）。本文沿这条线，评测对象是成对的查询和文档，而不是一份经典的检索评测语料。第 3 节起才是 NevIR 的构造，此处不展开。
