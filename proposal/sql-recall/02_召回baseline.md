# 召回 baseline

> 2026-11-11 核对。数字来自当天打开的论文、榜单或官方代码。
> 总览和先导实验在 [00_总览](00_总览.md)。

这一路把 2024–2026 的大模型召回方法按「模型在召回里做什么」拆开。没有一篇是模型写出协同 SQL。工业界的 I2I 表本来就是 SQL 引擎算的，但规则是工程师写死的，不是模型按一句自然语言现写的。

### 5.1 先导实验要放进表里的对照

三组，按「审稿人会问你为什么不跟这个比」来选，不按论文里的相对提升来选。

| 组 | 方法 | 为什么放进来 | 公开数字（协议写在格子里，不能和别的格子横比） | 代码 |
|---|---|---|---|---|
| 最强，无约束 | SASRec，全量交叉熵 | 换掉 BPR 之后，超过同表里的大模型推荐器 | Beauty NDCG@10 0.0597，Yelp 0.0345；同设置 LlamaRec 是 0.0492 和 0.0306。改回 BPR 后 Beauty 掉到 0.0374，反而输给 LlamaRec（[arXiv 2408.14238](https://arxiv.org/abs/2408.14238)） | [MTandHJ/CE-SCE-LLMRec](https://github.com/MTandHJ/CE-SCE-LLMRec) |
| 最强，非序列 | EASE、ItemKNN | 闭式或免训练。2019 和 2021 的可复现性调查里，多数神经推荐器打不过近邻 | 全量排序、Recall@10 / NDCG@10：MovieLens-1M 上 EASE 0.205 / 0.314，ItemKNN 0.163 / 0.126，LightGCN 0.173 / 0.269；Amazon Books 上 EASE 0.158 / 0.157，ItemKNN 0.149 / 0.149，LightGCN 0.088 / 0.083（Anelli 等，CEUR-WS Vol-3294） | [RecBole](https://github.com/RUCAIBox/RecBole) |
| 最像 | GPT4Rec；Bing 的 Q′ 召回 | 模型写查询，另一个引擎执行。引擎不是 SQL，也没有协同自连接 | GPT4Rec 已在上一轮核对：生成检索式查询，BM25 取回，两个公开集上 Recall@K 相对提升 75.7% 和 22.2%。Bing：模型写约 6 条互补查询，搜索引擎取回；协同点击是另一条路。开放版本里 GPT-4 的 CTR +0.89%、RecoDCG@5 +0.760，Mistral-7B 的 CTR +1.71%、RecoDCG@5 +0.762。正式版是 KDD 2025，[DOI 10.1145/3690624.3709413](https://doi.org/10.1145/3690624.3709413)，PDF 未打开 | GPT4Rec 见 arXiv 2304.03879。Bing 无代码 |
| 免训练、最接近「向量加共现」 | STAR | 向量、共现、时效、评分合在一起，模型不做训练。共现项是管线算的，不是模型写成 SQL | Amazon 2014，留一。成对排序 Hit@10：Beauty 0.101，Toys 0.120，Sports 0.056。只检索：0.098 / 0.118 / 0.054。他们表里的 KNN 只有 0.007，是弱的语义近邻，不能当成调好的 ItemKNN（[arXiv 2410.16458](https://arxiv.org/abs/2410.16458)） | 非官方、只有检索：[jyouturner/STAR](https://github.com/jyouturner/STAR) |
| 大模型编码器 | LLM2Rec | 协同微调之后，解码器变成物品编码器，后面仍接 SASRec | 全量排序，SASRec+LLM2Rec 的 R@10：Games 0.0865，Arts 0.0925，Movies 0.0705，Sports 0.1170。相对同表最好的嵌入基线大约高 3.5 到 7.4 个相对点（KDD 2025，[arXiv 2506.21579](https://arxiv.org/abs/2506.21579)） | [HappyPointer/LLM2Rec](https://github.com/HappyPointer/LLM2Rec) |
| 生成式检索 | TIGER，以及后来的 LC-Rec、EAGER、OneRec-Think | 语义 ID 上做下一个物品。算力允许时留一条，不作为主对照 | TIGER 留一，R@10 / NDCG@10：Beauty 0.0648 / 0.0384，同论文 SASRec 0.0605 / 0.0318（NeurIPS 2023）。OneRec-Think：Beauty R@10 0.0791，对照 SASRec 0.0607、TIGER 0.0623。OneRec 本体只有线上数字 | TIGER 官方代码未放出。LC-Rec：[RUCAIBox/LC-Rec](https://github.com/RUCAIBox/LC-Rec) |

OneRec、RecGPT、URM、PLUM、LEADRE 是工业召回，没有公开库上的 Recall@K。RecGPT 用模型写兴趣标签再注入双塔，线上 CTR +6.33%；URM 是工业生成式检索，广告核心指标 +3%。这些只能引用，不能复现。

单卡能跑的是 SASRec、EASE、ItemKNN、TIGER 这个量级，以及 7B 编码器。LC-Rec 和 HLLM-7B 是贵的那一臂。API 预算留给 STAR 式的成对排序和 Text-to-SQL。

### 5.2 共现召回本来就很强，所以题目不能是「SQL 版 ItemKNN」

- Ferrari Dacrema 等，RecSys 2019：18 个神经推荐器里 7 个可复现，其中 6 个输给近邻。TOIS 2021 的扩展里，12 个可复现模型有 8 个输给近邻，只有 1 个明确好于调好的非神经方法。
- Shevchenko 等，[arXiv 2505.09364](https://arxiv.org/abs/2505.09364)：四篇 SIGIR 2023–2024 的扩散推荐，每篇都被更简单的基线打平或超过；Amazon-Books 清洗后 ItemKNN 领先。
- OTTO 第一名：带访问过的物品、若干共现矩阵和一个神经候选源时，本地加权 recall@20 是 0.588；去掉共现剩 0.583；只留一个神经候选源是 0.515。第二名的候选来自把会话事件连接到共现矩阵。H&M 第一名把物品协同过滤和复购、流行度并列，图像和文本特征没有帮上排序。
- Swing 是阿里系的生产 I2I。PAI 把它做成 MaxCompute 作业，输入是用户到物品列表，输出是 `item_id, similar_items`，并带流行度惩罚。公开的 Hive 复现是 [recsysgroup/i2i_recall](https://github.com/recsysgroup/i2i_recall)，在作者自己的 MovieLens-1M 切分上，item-CF 的 HR@20 / HR@100 是 0.0783 / 0.267，带用户活跃度惩罚的 Swing 是 0.0786 / 0.273。

SQL 自连接就是这个候选阶段。还没被做的是：模型按一句自然语言，写出带属性谓词的连接，而不是一张事先算好的共现表。

### 5.3 精确 SQL 有证据的失败点，和没有证据的

有数字、值得放进先导实验的：

- 过滤后的近邻搜索。SIEVE（Li 等，PVLDB 18，2025）写明，加上「儿童向」或「相似且在价格区间内」这类谓词后，图上的近似搜索退化；后过滤要按 1/选择率多取。Lim 等，PVLDB 19（2026）：高难度负载上，选择率约 0.1% 或更低时，过滤近似搜索的召回「经常低于 0.2」。`WHERE` 在这些谓词上是精确的。
- 重复消费。RepeatNet（AAAI 2019）把显式的重复模式加进去后，DIGINETICA 的 Recall@20 从 42.56 到 47.79，LASTFM 从 29.96 到 32.38。历史过滤或重复连接可以把这些物品精确取回。
- 双塔的流行度。RecSys 2025 的 logQ 修正论文里，工业消费 Recall@1000 从未修正的 0.3133 到标准修正的 0.4308。Swing 的文档用物品范数和用户活跃度惩罚处理同一件事。

不能拿来当卖点的：

- 冷启动。没有交互的物品，协同自连接没有边。NoteLLM 在新笔记上的线上评论提升（+3.58%）来自内容嵌入。
- 索引过期。一篇过滤近似搜索的维护论文里，固定插入窗口下召回从 99.44% 掉到 99.01%。这是基础设施上的一个点，不是推荐效果上的缺口。免训练是工程优点，单独写进论文不够。
- SQL 文本本身即可解释。这一路没有找到把 SQL 文本当解释的用户研究。RecGPT 是在检索之后另训一个解释模型。

自然语言控制也停在重打分，没有走到召回 SQL。RuleAgent（[arXiv 2503.23374](https://arxiv.org/abs/2503.23374)）让智能体发现隐式反馈的去噪规则。InstructAgent 和 RecBot 把用户指令变成结构化偏好，再去重排已有信息流。都没有产出 I2I 或 U2U 的连接计划。

受众圈选是邻近产品，不是召回论文。Amazon Marketing Cloud 的 SQL 生成器把「看过商品页、看过贴片广告、30 天没买」写成 AMC SQL，再投到广告平台。RudderStack、Akkio 有同类功能。都没有离线 Recall 或 NDCG。

### 5.4 这一路对实验设计的直接后果

先导实验比较的是带约束的召回：品类、品牌、价格、排除已买，候选必须落在可行集里，同时报可行集上的 Recall@K、NDCG、约束满足率，以及模型调用和连接的耗时。Amazon Beauty、Sports、Toys 小到可以在一台机器上做精确连接。OTTO 是共现召回的公开压力测试。无约束的下一个物品留给 SASRec 和 EASE，用来说明「只是把 ItemKNN 写成 SQL」没有增益。
