> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名**：NumConQ_BDMA2026.pdf

**原文标题**：Numerical Constraint-Aware Dense Retrieval with Two-Phase Contrastive Learning

**作者**：Meng Wang（通讯作者）、Yisong Wang（College of Design and Innovation, Tongji University）；Feifan Wu（School of Computer Science and Engineering, Southeast University）。

**场合**：Big Data Mining and Analytics，第 9 卷第 2 期，2026 年 4 月，第 341–359 页。DOI: 10.26599/BDMA.2025.9020047。稿件收到 2025-02-15，修回 2025-04-23，录用 2025-04-28。

## 摘要

RAG 用外部知识补大模型，事实准确性和任务表现都会上去。现有 dense retriever 却很难处理查询里的数值约束，尤其是要精确过滤的条件。为把这个问题摊开看，作者建了 Numerical Constraint Question（NumConQ），覆盖医疗、金融、教育、体育和电影，查询超过 6500 条。经验分析里，当时的前沿 dense retriever 在数值约束是否满足上只有 16.3% 的准确率，和它们的语义匹配能力差一截。

针对这一点，Numerical Constraint-aware Retriever（NC-Retriever）有两处设计：两阶段对比学习，把 in-batch negative sampling 和逐步加入的 hard negative 合在一起；以及一套混合数值表示，让分词更一致。实验称，相对当时的前沿方法，recall@10 相对提高 65.84%，precision@10 提高 78.28%。代码和基准在 https://github.com/Tongji-KGLLM/NumConQ。

## 1 Introduction

RAG 把大模型和外部资料库接在一起，检索先从大语料里找出相关文档，生成器再据此产出答案。dense retrieval 把查询和文档都编成高维向量，开放域任务上进步明显，但训练重心在语义匹配，用户查询里写明的数值条件经常被放过。这类查询和纯主题查询不一样：病历分析、财务审计里常有硬条件，例如 “over 65 years old”“revenue less than 10 million”“release in 2009”。模型若主要在非结构化文本上训练，会抓住 “film genre”“country” 这类概念相似，却不检查文档是否正好落在数值界限内。

图 1 把这个界限写得很具体。查询要求印度的足球联赛、球员平均薪资低于 6 183 974 美元。真正相关的文档是 NFL，平均薪资 3 810 000 美元，低于门槛。BGE-M3 却取回 Ligue 1（6 650 000 美元，高出门槛 7.54%）和 Bundesliga（10 710 000 美元，高出 73.19%）。图中 GPT-4 顺着这些错误文档，把这两支联赛答成满足条件的结果，而正确回答应是 NFL。作者把现有做法的问题收成三条：多位数字的分词不一致；注意力偏向文本特征；缺少面向数值约束的训练目标。

在此之上他们构造 NumConQ：6577 条带数值约束的查询，5362 篇自然语言文档，领域仍是医疗、金融、教育、体育、电影。每个领域把结构化条目写成文本，且每条查询至少含一个数值约束。评测五套常用 dense retriever：Contriever、TAS-B、DPR、BGE-M3、JinaAI 的 jina-embeddings-v2-base-en。其中最好的 BGE-M3，Recall@10 和 Precision@10 也只有 40.37% 和 10.45%。

改进思路是：把查询里的数值轻轻改掉，做成 hard negative；训练时同时用 in-batch negative sampling，但把 hard negative 留到中后期才引入，让模型先抓住一般语义，再去分数值上的细差别。他们还注意到高位数常被切成不一致的子词，于是采用混合数值表示：较小的数保持原来的数字形式，较大的数改成文字表达式。贡献对应三块：多领域数值基准（6577 条查询、5362 篇文档）；对现有 retriever 处理数值约束的分析，指出分词不一致和缺少针对性训练数据；以及分阶段对比学习加混合数值表示。

## 2 Related Work

**2.1 Numerical constraint query。** 语义搜索随着神经网络进步很多，数值仍然难。Qsearch 是较早的端到端系统：用深度网络从文本抽数值并转成语义结构，用 Semantic Role Labeling（SRL）把词分成实体、数量或上下文，从而抽出数值事实三元组，再用一种统计匹配来检索和排序。Faith 把这类系统扩到异构数据上的时间问答，把隐含的时间约束通过中间问题和递归调用变成显式值。Han et al. 针对大模型读不懂财务报告里的数值约束查询，提出 XBRL agent，用外部工具补上金融数值推理，并做了一份面向 XBRL 报告的数值类查询数据。Biswal et al. 的 Table-Augmented Generation（TAG）把大模型和数据库系统合在一起，处理包括数值约束在内的复杂自然语言查询。这一路工作是在结构化知识上把数值问答越做越细；在知识库上查数值，比在非结构化文档里查更容易。结构化库却更难获取和维护，非结构化文档能覆盖的数值知识更广，这也是本文方法要利用的范围。

**2.2 Dense retriever。** dense retriever 近年受关注，是因为在需要语义理解时往往强于稀疏检索。TF-IDF 和 BM25 靠精确词项匹配，语义相近但用词不同时容易失手。dense retriever 把查询和文档编进同一嵌入空间再算相似度。编码器多用预训练模型，常见两种结构：dual-encoder 用两个编码器分别编查询和文档，再算向量相似度；cross-encoder 把查询和文档拼在一起，用一个编码器直接建模细粒度交互。后者更擅细节，前者可以把文档预先编码并建索引，计算更省。朴素 RAG 文档量很大，大规模检索多用 dual-encoder，cross-encoder 则常做重排。文中点名的模型包括：DPR，用问答数据里的正例和 BM25 的难负例做判别训练，只靠稠密表示检索；ANCE（Xiong et al.）认为局部负采样是瓶颈，改为用当前的 dense retriever 在全语料上取全局负例，使训练时的负例分布靠近测试时的不相关文档；Contriever 用对比学习训练无监督 dense retriever，面向低资源；LARMOR 让大模型产生伪相关信号，用来选择和排序 dense retriever；KaLM-Embedding 把大模型的多语言知识与动态训练策略合在一起，给 RAG 提供语义基础。本节的判断是：这些模型语义上很强，但数值敏感查询要的是精确、细粒度的数值匹配，而稠密模型依赖潜空间里的语义相似，注意力更多在复杂语境和语义关系上，而不是数值是否精确。第 3 节起才是 NumConQ 的定义与构造，此处不展开。
