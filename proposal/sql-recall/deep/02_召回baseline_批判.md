# 召回 baseline 批判

> 2026-11-11。对照 [02_召回baseline](../02_召回baseline.md)。数字只来自当天打开的 PDF，页码是 PDF 页。没有横比不同协议的格子。没有 git 提交。

这一路要回答的不是「SQL 能不能生成」，而是：无约束的下一物品上，一条协同自连接有没有资格宣称打不过调好的 SASRec / EASE；带谓词时，过滤近似搜索的召回塌陷是不是推荐约束上的证据；GPT4Rec 和 Bing 的 Q′ 是不是最近的前作。

## 获取

PDF 在 `papers/sql-recall/02-recall/`。KDD 2025 档案版没有开放 PDF，没有去下第三方仓库里的转载。

| 论文 | 本地文件 | 打开的 URL | 失败 |
|---|---|---|---|
| STAR | `STAR-2410.16458.pdf`（16 页） | https://arxiv.org/pdf/2410.16458 | 首页未印会议名 |
| NoteLLM | `NoteLLM-2403.01744.pdf`（10 页） | https://arxiv.org/pdf/2403.01744 | WWW ’24 Companion |
| NoteLLM-2 | `NoteLLM-2-2405.16789.pdf`（12 页） | https://arxiv.org/pdf/2405.16789 | KDD ’25 |
| LLM2Rec | `LLM2Rec-2506.21579.pdf`（12 页） | https://arxiv.org/pdf/2506.21579 | KDD ’25 |
| LEARN | `LEARN-2405.03988.pdf`（9 页） | https://arxiv.org/pdf/2405.03988 | AAAI，版权年为 2025 |
| HLLM | `HLLM-2409.12740.pdf`（12 页） | https://arxiv.org/pdf/2409.12740 | 首页未印会议名 |
| TIGER | `TIGER-2305.05065.pdf`（17 页） | https://arxiv.org/pdf/2305.05065 | NeurIPS 2023 |
| LC-Rec | `LC-Rec-2311.09049.pdf`（14 页） | https://arxiv.org/pdf/2311.09049 | 首页未印会议名 |
| LETTER | `LETTER-2405.07314.pdf`（10 页） | https://arxiv.org/pdf/2405.07314 | CIKM ’24 |
| EAGER | `EAGER-2406.14017.pdf`（10 页） | https://arxiv.org/pdf/2406.14017 | KDD ’24 |
| IDGenRec | `IDGenRec-2403.19021.pdf`（11 页） | https://arxiv.org/pdf/2403.19021 | SIGIR ’24 |
| OneRec-Think | `OneRec-Think-2510.11639.pdf`（17 页） | https://arxiv.org/pdf/2510.11639 | 首页未印会议名 |
| GPT4Rec | `GPT4Rec-2304.03879.pdf`（5 页） | https://arxiv.org/pdf/2304.03879 | ACM 模板未填会议名，`Conference acronym ’XX ... Woodstock` |
| Xu 等 | `Xu-SASRec-CE-2408.14238.pdf`（18 页） | https://arxiv.org/pdf/2408.14238 | arXiv v1，首页无会议 |
| Ferrari Dacrema RecSys 2019 | `FerrariDacrema-RecSys2019-1907.06902.pdf`（10 页） | https://arxiv.org/pdf/1907.06902 | 作者稿，对应 RecSys ’19 |
| Ferrari Dacrema TOIS 2021 | `FerrariDacrema-TOIS2021-1911.07698.pdf`（49 页） | https://arxiv.org/pdf/1911.07698 | 学校库 `re.public.polimi.it` 返回 403。这份 arXiv 带 TOIS 39(2) 的 ACM 引用格式 |
| Shevchenko 等 | `Shevchenko-2505.09364.pdf`（71 页） | https://arxiv.org/pdf/2505.09364 | 正文刊头是 TORS 4(1) Article 46，出版日期印为 2026-03。作者是 Benigni、Ferrari Dacrema、Jannach，不是 Shevchenko |
| SIEVE | `SIEVE-PVLDB18-li.pdf`（14 页，引用用这份）；另存 arXiv `SIEVE-2507.11907.pdf` | https://www.vldb.org/pvldb/vol18/p4723-li.pdf ；https://arxiv.org/pdf/2507.11907 | PVLDB 18(11):4723–4736, 2025 |
| Lim 等 | `Lim-PVLDB19-filtered-ANN.pdf`（14 页） | https://www.vldb.org/pvldb/vol19/p2763-lim.pdf | PVLDB 19(10):2763–2776, 2026 |
| RepeatNet | `RepeatNet-1812.02646.pdf`（9 页） | https://arxiv.org/pdf/1812.02646 | AAAI OJS `ojs.aaai.org/.../4408/4286` 下下来不是 PDF，已删。arXiv v1 带 AAAI 2019 版权行 |
| RecGPT | `RecGPT-2507.22879.pdf`（42 页） | https://arxiv.org/pdf/2507.22879 | 技术报告，无公开库 Recall@K |
| InteRecAgent | `InteRecAgent-2308.16505.pdf`（18 页） | https://arxiv.org/pdf/2308.16505 | 首页标题是 *Recommender AI Agent*；系统名 InteRecAgent 在正文 |
| Bing Q′ 档案版 | 未下载 | https://doi.org/10.1145/3690624.3709413 | ACM DL 只有付费 PDF。GitHub 上有转载，未取 |
| WebReco | `WebReco-IRS2024-not-archival.pdf`（11 页） | https://irsworkshop.github.io/2024/publications/paper_webreco.pdf | **不是** KDD 2025 档案版。CIKM 2024 IRS 研讨会 |
| Q′ 的另一份开放稿 | `Bing-Qprime-EARL2024-not-KDD.pdf`（10 页） | https://earl-workshop.github.io/pdf/recsys2024-workshops_paper_29.pdf | **不是** 档案版。RecSys 2024 EARL 研讨会。表 5 的 CTR / RecoDCG 与 WebReco 表 2 相同 |

## 四个判断

### 1. 「SQL 自连接就是 ItemKNN/Swing，所以无约束下一物品上打不过调好的 SASRec/EASE」是过度声称

前半句是定义，后半句没有被这批 PDF 测过。

自连接能写出的是物品共现：余弦或 Jaccard 的 ItemKNN，加上用户活跃度惩罚就是 Swing。EASE 是带 L2 闭式解的线性模型，SASRec 吃序列顺序。一条 `item, item, count` 的自连接实现不了这两样。这批论文里没有一篇把 SQL 自连接和 SASRec、EASE 放在同一张全库排序表里。

能引用的事实，方向还彼此打架：

- 矩阵补全式的 top-n 上，近邻和线性模型经常赢过 2015–2018 的神经协同过滤。RecSys 2019 摘要：18 篇里 7 篇可复现，其中 6 篇经常输给近邻一类的简单方法；剩下的 Mult-VAE 明显好于他们的简单基线，但没有稳定好于调好的线性模型 SLIM。Netflix 上 Mult-VAE 的 Recall@20 是 0.2626，ItemKNN 是 0.2088，SLIM 是 0.2551；NDCG@100 是 0.3756 对 SLIM 的 0.3745；把截断换到 NDCG@20，SLIM 0.2473，Mult-VAE 0.2448（表 8、表 9，第 7 页）。TOIS 2021 引言写得更死：26 篇里复现 12 篇；12 篇里有 8 篇输给近邻一类的老方法；算上矩阵分解等线性模型之后，12 篇里只有 1 篇明确好于非神经基线，而且只在其中一个数据集上（第 3 页）。摘要的另一句是 12 篇里 11 篇可以被近邻或线性模型超过。这些论文的时间窗口止于 2018，里面没有全量交叉熵 SASRec。
- Shevchenko 这条线（实际作者 Benigni、Ferrari Dacrema、Jannach）把四篇 SIGIR 2023–2024 的扩散推荐放到调过的近邻和线性模型上。Amazon-Books（clean）表 2（第 21 页）：ItemKNN 的 Recall@10 / NDCG@10 是 0.1133 / 0.0743，SLIM 的 Recall@20 是 0.1561，高于表内所有 DiffRec 变体（论文报告的最好一档 LT-DiffRec Recall@10 是 0.0838，他们自己重跑是 0.0835±0.0018）。EASE 在这张表上是空的，因为 64 GB 内存不够。所以在这个协议上，自连接那一家是领先的一方，不是输家。
- 序列下一物品上，Xu 等只比了损失函数，没有 ItemKNN，也没有 EASE。Beauty 与 Yelp 都是留一，按目标物品在全体物品中的名次算 NDCG 和 MRR，也就是全库排序（第 3–4 页）。用户数和物品数对齐：Xu 附录、STAR 表 1、IDGenRec 表 3 都是 22,363 用户、12,101 物品、198,502 次交互。TIGER 附录表 6 只印了用户、物品和平均长度 8.87，没有印交互次数。EAGER 表 1 的交互次数是 198,360。差大约一百次交互，所以下面的 NDCG 对照只说明方向。表 3：全量交叉熵 SASRec 的 NDCG@10，Beauty 0.0597，Yelp 0.0415。同表 LlamaRec 是 0.0492 和 0.0367。改回 BPR，SASRec 的 Beauty NDCG@10 掉到 0.0374，低于 LlamaRec。BCE 是 0.0353。Yelp 上 FMLP-Rec 的全量交叉熵 NDCG@10 是 0.0444，还高于 SASRec 的 0.0415。结论只支持「BPR/BCE 的 SASRec 是弱基线，全量 softmax 之后传统序列模型超过同表的 LLM 推荐器」。它不支持「ItemKNN 打不过 SASRec」。

可以写进论文的句子是：无约束共现 SQL 与调好的 ItemKNN 是同一类方法，先导里它的对照就是它自己；它会不会输给全量交叉熵 SASRec 或 EASE，这批文献没有测。EASE 在内存够的数据集上可以高于 ItemKNN。GiffCF 一节的表 7 是 MovieLens-1M（clean），第 28 页：归一化 Recall@10 上 EASE 是 0.1186，ItemKNN 是 0.1092。这列是归一化 Recall，不是 Amazon-Books 表 2 的普通 Recall，也不是 Beauty 的留一序列任务，不能拿来填 Beauty 的格子。

### 2. 换掉弱基线之后，哪些涨幅会消失

这批生成式检索的主表是留一，绝对 Recall@10 在 0.06 附近，不是早期 SASRec 那种 100 个采样负例的 Hit@10。把「全库」写死的是 LC-Rec（全体物品，不用 sample-based evaluation）和 IDGenRec（评估不用负采样，对全体物品排序）。TIGER、EAGER、LETTER、OneRec-Think 没有这句，只引用 SASRec 或 TIGER 的协议；它们和 IDGenRec 抄的是同一行 SASRec，尺度才按全库理解。会翻盘的是训练目标，不是把采样 Hit 换成全库 NDCG。TIGER 写明，除 P5 外的基线数字来自 Zhou 等 S3-Rec 公开结果（第 7 页）。同一行 SASRec 被 EAGER、IDGenRec 原样抄走。Beauty 上这行是 Recall@10 0.0605、NDCG@10 0.0318。Xu 在同一用户数、同一物品数的 Beauty 上把损失函数换成全量交叉熵，NDCG@10 是 0.0597。两边序列截断不同（TIGER 训练历史限 20，Xu 的 SASRec 最大长度 50），所以下面是方向性的对照，不是配对实验。

| 论文 | 它声称打败的 SASRec | 它自己的 Beauty NDCG@10 | 相对 Xu 的 0.0597 |
|---|---|---|---|
| TIGER 表 1，第 7 页 | Recall@10 0.0605，NDCG@10 0.0318 | 0.0384 | 低于 |
| EAGER 表 2，第 6 页 | 同上，原样 | 0.0525 | 低于 |
| IDGenRec 表 4，第 7 页 | 同上，原样；正文写明评估不做负采样，对全体物品排序 | 0.0541 | 低于 |
| OneRec-Think 表 1，第 6 页 | Recall@10 0.0607，NDCG@10 0.0320；他们重做的 TIGER 是 0.0623 / 0.0337 | 0.0471 | 低于 |
| STAR 表 2，第 7 页 | Hits@10 0.061，NDCG@10 0.032 | 成对排序 0.060 | 和 0.0597 粘在一起 |

分论文：

- **TIGER。** Beauty 上相对最好基线，Recall@10 只从 S3-Rec 的 0.0647 到 0.0648，表底写 +0.15%。大的百分比在 NDCG@5：0.0321 对 SASRec 的 0.0249，+29.04%。附录表 9 三次种子的均值更低：Recall@10 0.0642±0.00092，NDCG@10 0.0374±0.00061，主表的 0.0648 / 0.0384 是单次报告。换成全量交叉熵之后，这个 NDCG 故事对不上。Recall@10 的「超过 SASRec」本来就几乎是和 S3-Rec 打平。
- **EAGER。** Beauty Recall@10 0.0836，相对表内最好基线 Recforest 0.0664 是 +25.90%。Toys 的 Recall@10 只从 TIGER 的 0.0712 到 0.0714（+0.28%），Recall@20 的改进栏是 −3.85%（S3-Rec 0.1065，EAGER 0.1024）。「全面超过」在自己的表里已经不成立。NDCG@10 0.0525 仍低于 Xu 的 0.0597。
- **IDGenRec。** Beauty HR@10 0.0814，NDCG@10 0.0541。相对提升是对着抄来的 SASRec / S3-Rec 算的。NDCG 仍低于 0.0597。
- **OneRec-Think。** Beauty R@10 0.0791，对照 SASRec 0.0607、TIGER 0.0623。N@10 0.0471。线上是快手 App 停留时长 +0.159%（表 3，第 7 页），不能当公开库 Recall。
- **STAR。** 成对排序 Hits@10：Beauty 0.101，Toys 0.120，Sports 0.056。只检索：0.098 / 0.118 / 0.054。同表 KNN 的 Hits@10 是 0.007 / 0.007 / 0.002。正文写的是「找 10 个最相似用户再平均打分」的 UserKNN（第 5 页），不是语义近邻，也不是调过邻域大小和收缩的 ItemKNN。拿 0.007 证明近邻很弱，不成立。成对排序的 NDCG@10 0.060 与 Xu 的 0.0597 不能写成谁赢谁。
- **Xu 自己。** 这是「换掉弱基线，LLM 的优势消失」的直接实验。评估一直是全库。变的是 BPR（每个正例一个负例）对全量 softmax。Beauty 上 LlamaRec 从「超过 BPR-SASRec」变成「落后全量交叉熵 SASRec 约 21% 的 NDCG@10」（表 3 的 ▲% over LLM 在 CE 块是 +21.3%）。
- **NoteLLM。** 离线主表（表 2，百分数）Recall@100：NoteLLM 84.02，RepLLaMA 83.63，PromptEOL+CSE 83.28，线上 SentenceBERT 70.72。相对强嵌入基线，Recall@100 只高 0.39 个点；Recall@1k 是 95.23，低于 PromptEOL+CSE 的 95.26。大的差距只相对 SentenceBERT。
- **LLM2Rec、LC-Rec、LETTER、LEARN、HLLM** 的数据集或基线套装和上面这份 Beauty 不同，不能用 0.0597 直接判死。它们的问题写在各篇里：要么没放 ID 版全量交叉熵 SASRec，要么 SASRec 来自上一篇的公开数字。

Shevchenko 是另一类消失：扩散模型相对原论文弱基线的优势，在 ItemKNN / SLIM / RP3β 放进来之后消失。四篇都至少有一个更简单的基线打平或超过。这不是采样指标的问题。

### 3. 过滤近似搜索的召回塌陷，谓词长什么样

两篇都在说向量近邻的 recall：找回的是不是真正的 top-k 近邻。都不是推荐系统的 Recall@K，都没有 NDCG，都没有下一物品标签。

**SIEVE**（PVLDB 第 2–3 页，§2.2）写的是机制。后过滤对选择率 \(sel\) 的查询去取 top-\(k/sel\)，不够再翻倍。hnswlib 在结果集上过滤，时间大致随 \(1/sel\) 变差。ACORN 在邻居扩展时过滤，诱导子图丢掉小世界连通性，搜索会提前停、recall 变低。引言里的「儿童向视频」「价格区间里的戏服」是动机句。实验（表 4、图 9，第 8–9 页）是 YFCC-10M 的 `A or A∧B`、Paper 和 UQV 上按他们的规则生成的合取或析取、GIST 和 SIFT 上的数值区间、MSONG 上的均匀过滤。图 9 是 QPS 对 recall@10 的曲线。正文给出的退化幅度是：低选择率的 YFCC、Paper、UQV 上，ACORN-γ 的 recall 停在大约 0.95，SIEVE 可以到 0.99 以上。这是索引没撑满，不是推荐命中率掉到 0.2。

**Lim 等**（第 11 页，§5.3）有「经常低于 0.2」这句，原文是：高难度负载上，多数策略的 recall 急剧下降，often below 0.2，并说这与选择率大约 0.1% 或更低的已知困难一致。0.2 是对图 6 的概括，不是表里的一个格子。同页写 ACORN 的更密 HNSW 在选择率低于大约 0.1% 时连通性不够，搜索提前结束。负载是 SIFT1M 和 GIST1M 上合成的属性：每个数据集 3 个属性、基数 12、Zipf 1.5、缺失概率 0.5、属性与向量的相关设为 0，再分成 Low / High 难度（§5.1）。半真实数据是 YFCC 一类的混合检索负载，用来拟合难度分布。这些谓词是数据库微基准里的标签和区间，不是「这个品牌、这个价格、排除已买」。

能拿来用的只有机制：图上的过滤近邻在选择率很低时要多取，而且多取也不保证找回真正的近邻；SQL 的 `WHERE` 在同一谓词上是精确的。不能写成「推荐约束下向量召回的 NDCG 会塌」。品类、品牌、价格、排除已买要在先导里自己测。选择率若在百分之几以上，Lim 的 0.1% 区间套不上。

### 4. GPT4Rec 和 Bing Q′ 是不是最近的前作

是「模型写查询、另一个引擎执行」这一类里最近的公开系统。审稿人会说抄的是这条管线，不会说抄了协同 SQL，因为两边都没有协同 SQL。

**GPT4Rec**（第 2–3 页）用 GPT-2 从用户历史标题生成多条查询，BM25 执行，再按生成分数把每条查询的 top-\(K/m\) 拼起来。训练时把目标标题本身当成最细的查询，去微调 GPT-2，然后网格搜索 BM25 的 \(k_1\) 和 \(b\)。表 1 的划分是用户序列 0.8/0.1/0.1，序列去重后截到 15，不是每个用户留一。Beauty 的规模是 22,254 用户、11,778 物品，和标准 5-core Beauty 不是同一预处理。75.7% 和 22.2% 是 Recall@40、相对 BERT4Rec：Beauty 0.2040 对 0.1161，Electronics 0.0918 对 0.0751。同表没有 SASRec、ItemKNN、EASE。Beauty 的 Recall@10 上，BERT4Rec 是 0.0513；5 条查询的 GPT4Rec 是 0.0810，10 条查询是 0.1036。0.0810 不是 40 条查询的格子。审稿人会说：你们把 BM25 换成了 SQL，查询从标题扩展换成了连接。若主表只报 SQL 执行成功，贡献停在 GPT4Rec 已经做过的「生成查询再取回」。

**Bing。** KDD 2025 档案版没打开。下面两个数字来自非档案稿，两份一致。WebReco 表 2 和 EARL 表 5：Q′ Recall（GPT-4）线上 CTR +0.89%、RecoDCG@5 +0.760；Mistral-7B 是 +1.71% 和 +0.762。做法是用 URL、标题、正文生成平均约 6 条互补查询，Bing 搜索每条取 top 10，每个 URL1 存最多 30 个 URL2。任务是网页到网页。协同点击是另一条召回。没有用户–物品自连接，没有属性谓词的精确过滤实验，没有公开库的 Recall@K。

更近、而且已经在写 SQL 的是 **InteRecAgent**。工具链是 SQL 查询、SQL 检索、排序器，外加单独的 ItemCF 工具（第 4 页附近的例子，附录里的工具说明）。附录把 SQL 限制死了：只能出现一张物品信息表；不能用 SQL 找相似物品；标题不能当条件。排序任务是 1 个正例加 19 个随机负例上的 NDCG@20（第 9 页，表 5 说明）。表 5 的检索 Recall@5（百分数）在 Beauty 上是 30.28，对照 GPT-4 的 12.80。这和全库 0.06 不是一个协议。审稿人若说「SQL 召回已经有了」，指的就是这种属性过滤 SQL。还没做的是让模型写出 I2I / U2U 自连接，并且用全库或可行集上的 Recall 对 SASRec、ItemKNN 打分。

RecGPT 技术报告写的是兴趣句和物品标签，注进用户–物品–标签的三塔，解释模型在检索之后另训。摘要里的线上数字是 CTR +6.33%、IPV +9.47%、DCAU +3.72%。没有公开库 Recall@K，没有 SQL。

## 逐篇

协议栏里的「全库」指评估时对全体物品排序，或论文写明不用采样负例。「留一」指最后一次交互做测试。结论三档：站得住；只在该协议下成立；不成立。

### STAR

路径 `STAR-2410.16458.pdf`。Dong-Ho Lee 等。arXiv:2410.16458。首页无会议。

声称的创新：

- 免训练。检索分是语义相似度与共现的加权和，再乘时效和评分（第 4–5 页的打分式）。
- 排序阶段把候选和共现次数写进 Gemini 的提示，做 point-wise / pair-wise / list-wise。
- 共现、流行度、评分都是管线算好再填进提示，不是模型现写的查询。

主表是表 2，第 7 页。Amazon 2014 的 Beauty、Toys、Sports，留一，Hits@5/10 与 NDCG@5/10。表 1 的 Beauty 是 22,363 / 12,101 / 198,502，和 Xu、IDGenRec 相同。TIGER 附录表 6 只印到平均长度 8.87。正文没写采样负例；同表 SASRec 的 Hits@10 0.061 与 TIGER 表 1 的 Recall@10 0.0605 对齐。

数字：成对排序 Hits@10 为 0.101 / 0.120 / 0.056，NDCG@10 为 0.060 / 0.073 / 0.034。只检索 Hits@10 为 0.098 / 0.118 / 0.054。SASRec 的 Hits@10 为 0.061 / 0.068 / 0.035。KNN 为 0.007 / 0.007 / 0.002。IDGenRec 在同表是 0.081 / 0.087 / 0.057，高于 STAR 的 Sports。

对照是弱的。KNN 是 top-10 UserKNN。SASRec 是生成式检索那一串里的弱行，不是 Xu 的全量交叉熵。不能和别的论文的 Recall 横比到小数点后四位以外的协议；和 TIGER、IDGenRec、Xu 的 Beauty 是同一份数据，NDCG 可以谨慎对照。

结论：只在该协议下成立。对选题：共现项是脚本算的，SQL 自连接没有新意；0.007 的 KNN 不能当「近邻很弱」的证据。免训练和「SQL 即解释」不是一回事，这里的解释是提示里的共现句。

### NoteLLM

路径 `NoteLLM-2403.01744.pdf`。Zhang 等。WWW ’24 Companion。https://arxiv.org/pdf/2403.01744

声称的创新：

- 用压缩提示把笔记压成一个特殊 token，再做对比学习，得到可检索的笔记向量（摘要）。
- 指令微调同时生成话题标签或类目，并说这会反过来加强嵌入。
- 面向小红书的 I2I 笔记召回，不是用户序列的下一物品。

离线主表是表 2，第 6 页，数字是百分数。测试池是下个月的笔记，训练笔记排除在外。对一对笔记，拿第一条当查询，在池子里排第二条。指标是 Recall@100 / 1k / 10k / 100k。NoteLLM 7B：84.02 / 95.23 / 99.23 / 99.96。RepLLaMA：83.63 / 95.10 / 99.27 / 99.94。SentenceBERT（线上）：70.72 / 87.88 / 96.29 / 99.62。

线上（§5.8，第 8 页）：相对 SentenceBERT，CTR +16.20%，评论数 +1.10%，周均发布者 +0.41%。新笔记一天内的评论数 +3.58%。这是内容嵌入对冷启动笔记的线上评论，分母是新笔记的评论，不是全体 CTR，也不是协同边。

不能和 Amazon 的 Recall@10 横比。结论：相对 SentenceBERT 站得住；相对 RepLLaMA，Recall@100 的差距可以忽略，Recall@1k 还略低，所以「LLM 笔记编码器大幅优于强嵌入」只在对着线上旧模型时成立。对选题：冷启动没有交互边，自连接帮不上；不要把 +3.58% 写成协同 SQL 失败或成功的证据。

### NoteLLM-2

路径 `NoteLLM-2-2405.16789.pdf`。Zhang 等。KDD ’25。https://arxiv.org/pdf/2405.16789

声称的创新：任意 LLM 加视觉编码器做端到端多模态表示；mICL 把图文分开以免微调时丢掉图像；late fusion 把视觉向量直接加进最终表示（摘要）。

主表是表 4，第 8 页附近，仍是小红书笔记对，百分数 Recall。MQwen-Base 上，basic 的 All-Pair R@100 是 74.02，NoteLLM-2 是 76.49。短查询对上 R@100 从 48.15 到 55.73。线上（第 10 页）：10% 流量、一周；基线是用 NoteLLM 训练过的同一个 LLM。前一千次曝光的点击 +6.35%，发布后 24 小时互动 +8.08%，24 小时内且 100 次曝光内出现首次互动的笔记 +9.83%。

没有公开下一物品表，没有 SASRec。结论只在该私有 I2I 协议下成立。对选题：多模态向量召回，SQL 自连接不覆盖图像。

### LLM2Rec

路径 `LLM2Rec-2506.21579.pdf`。He 等。KDD ’25。https://arxiv.org/pdf/2506.21579

声称的创新：两阶段把 LLM 变成物品编码器。先做协同监督微调，让模型根据历史推断物品关系；再做物品级嵌入，使向量同时带语义和协同（摘要）。下游仍是 GRU4Rec 或 SASRec，损失是交叉熵。

主表是表 3，第 7 页。评估写明 full ranking，全体物品为候选，Recall 与 NDCG 的 10 和 20，三次种子平均（§4.1.1）。数据是 Amazon 的 Games、Arts、Movies，以及域外的 Sports、Baby、Goodreads。切分与预训练相同，表 2 的 Train / Val&Test 是计数，不是 TIGER 那份 Beauty。

SASRec 行的 R@10：Games 上 LLM2Rec 0.0865，最强嵌入基线 LLMEmb 0.0813（+6.42%）；Arts 0.0925 对 0.0865（+6.95%）；Movies 0.0705 对 LLM2Vec 的 0.0662（+6.49%）；Sports 0.1170 对 LLMEmb 0.1131（+3.51%）；Baby 0.0708 对 0.0659（+7.39%）；Goodreads 0.1530 对 BLAIR 0.1508（+1.45%）。全部行都是「文本嵌入初始化的 SASRec」。表里没有从零训练的 ID SASRec，没有 ItemKNN，没有 EASE。

不能和 Beauty 0.06 横比。结论只在「嵌入初始化、全库、交叉熵 SASRec」这个协议下成立，而且 Goodreads 的相对增益只剩 1.45%。对选题：模型产出的是向量，召回仍是内积。协同信号进了编码器，没有进一条可执行的连接。

### LEARN

路径 `LEARN-2405.03988.pdf`。Jia 等（快手）。AAAI，版权页 2025。https://arxiv.org/pdf/2405.03988

声称的创新：CEX 用冻结的 LLM 抽物品文本向量，PAL 把开放世界向量投到推荐空间，用用户–物品对比损失对齐；避免把推荐域硬塞回 LLM 造成遗忘（贡献列表，第 2 页）。

公开主表是表 3，第 5 页。六个 Amazon 类目：Scientific、Instruments、Arts、Office、Games、Pet。协议跟 RecFormer：留一，NDCG@10、Recall@10、MRR。正文写 Amazon 上训练不采样。SASRec 等 ID 模型的数字与 RecFormer 设置对齐，不是在本表里用全量交叉熵重新搜过的。

LEARN 相对 RecFormer 的 Recall@10：Scientific 0.1594 对 0.1448（+10.08%），Instruments 0.1240 对 0.1052（+17.87%），Arts 0.1701 对 0.1614（+5.39%），Office 0.1549 对 0.1403（+10.41%），Games 0.1345 对 0.1039（+29.45%），Pet 0.1284 对 0.1162（+10.50%）。平均 13.95% 与这六个数的算术平均一致。Arts 的 NDCG@10 是 0.1225，RecFormer 是 0.1252，改进栏为「–」。Games 上同表 SASRec 的 Recall@10 只有 0.0953。

工业表是排序不是召回：UAUC +0.84 个点，WUAUC +0.76 个点（表 8 的正文，第 7 页）。表 9 冷启动物品收入 +8.77%。线上 20% 流量、9 天，图 6 没有印出 CVR 的终点数字，正文只说收入约在千万量级时 2% 就算显著。

不能和 TIGER Beauty 横比。结论：Recall@10 相对 RecFormer 在六个数上成立，NDCG 在 Arts 上不成立；ID SASRec 是否弱，取决于 RecFormer 当年怎么训的，本 PDF 没有换成 Xu 的损失。对选题：LLM 在这里是冻结的文本编码器，下游是对比学习排序，不是 SQL。

### HLLM

路径 `HLLM-2409.12740.pdf`。Chen 等（字节）。首页无会议。https://arxiv.org/pdf/2409.12740

声称的创新：物品 LLM 和用户 LLM 分层；预训练知识要迁到推荐，但必须用推荐目标微调；参数和数据变大时还在涨；物品向量可以缓存，使训练和服务接近 ID 模型（贡献列表，第 2 页）。

主表是表 7，第 7 页。Pixel8M 和 Amazon Books，留一，R@10/50/200 与 N@10/50/200。表内 R@10 写成 6.129 这种大于 1 的数，只能是百分数口径，不能和 0–1 的 TIGER 横比。训练使用大量负例：Books 上默认 512 个负例、batch 128；带 † 的行把负例和 batch 加到 28k 和 512。评估是留一的 Recall，不是 100 负例打分。

Books 上，他们重跑的 SASRec∗ R@10 是 5.35，HLLM-1B 是 6.97，HLLM-7B† 是 9.39。相对表底的 SASRec (2018) 3.06，7B 的平均改进栏写 +169.58%。Pixel8M 上 HLLM-1B 的 R@10 是 6.129，SASRec∗ 是 5.083。线上 A/B 是排序任务，「关键指标」+0.705%（第 7 页），没写是哪一个指标。

SASRec∗ 是他们自己重跑的，比表里的 SASRec (2018) 高一截，这一点比 TIGER 抄表老实。仍然没有 ItemKNN / EASE，也没有写明是不是全量 softmax。结论只在 PixelRec / Books 的留一协议下成立。对选题：分层 LLM 产出的是缓存向量，服务路径是现有排序模型。贵，不适合当先导主对照。

### TIGER

路径 `TIGER-2305.05065.pdf`。Rajput 等。NeurIPS 2023。https://arxiv.org/pdf/2305.05065

声称的创新：用 RQ-VAE 把文本嵌入收成语义 ID；序列模型直接生成下一个物品的 ID，而不是做最大内积；语义 ID 有层级，可做冷启动（第 5–8 页）。

主表是表 1，第 7 页。Amazon 2014 Beauty、Sports、Toys。留一写在附录 C。Recall@5/10、NDCG@5/10。基线除 P5 外取自 S3-Rec 的公开结果。Beauty：TIGER 0.0454 / 0.0321 / 0.0648 / 0.0384，SASRec 0.0387 / 0.0249 / 0.0605 / 0.0318，S3-Rec 的 Recall@10 是 0.0647。表底 Beauty Recall@10 的相对提升是 +0.15%，NDCG@5 是 +29.04%。附录表 9 的三次均值是 Recall@10 0.0642±0.00092、NDCG@10 0.0374±0.00061。正文没有写「对全部物品打分」，绝对值才是全库尺度。

同一数据上 Xu 的全量交叉熵 SASRec NDCG@10 为 0.0597。TIGER 的 0.0384 低于它。结论：相对这份抄来的 SASRec，NDCG 的提升站得住；「生成式检索在这个数据集上打败了调好的序列模型」不成立。对选题：模型生成的是离散 ID，不是 SQL。官方代码文中写明未放出。先导里最多留一条，不能当主对照，也不能把表 1 的 SASRec 当成强基线。

### LC-Rec

路径 `LC-Rec-2311.09049.pdf`。Zheng 等。首页无会议名。https://arxiv.org/pdf/2311.09049

声称的创新：语义 ID 之外，用对齐任务把语言语义和协同语义一起放进 LLaMA-7B；索引唯一且词表小（第 2 页贡献，表 I）。

主表是表 III，第 9 页。Amazon 2018 的 Instruments、Arts、Games，不是 2014 Beauty。留一，全体物品上的 HR 和 NDCG，K=1、5、10。正文写明是 full ranking，不用 sample-based evaluation。生成式方法的 beam 为 20。

Games 的 HR@10：LC-Rec 0.1174，SASRec 0.0940，FDSA 0.1041，TIGER 0.0939，相对最好基线 +12.78%。Instruments 的 HR@10：0.1220 对 S3-Rec 0.1136（+7.39%）。Arts 的 HR@10：0.1266 对 S3-Rec 0.1051（+20.46%）。SASRec 在 Games 上不是最强基线，FDSA 和 S3-Rec 更高，但没有全量交叉熵的消融。

不能和 TIGER Beauty 横比，类目和年份都不同。TIGER 是作者自己按论文重做的。结论只在这三份 2018 数据的全库留一上成立。对选题：7B 微调，先导里是贵的那一臂。查询是语义 ID 的生成，执行器是 beam search，不是数据库。

### LETTER

路径 `LETTER-2405.07314.pdf`。Wang 等。CIKM ’24。https://arxiv.org/pdf/2405.07314

声称的创新：量化时加协同正则和多样性正则，让语义 ID 对齐 SASRec 的物品向量，并减轻码字分配偏置（第 2 页贡献）。

主表是表 1，第 6 页。Instruments、Beauty、Yelp。留一，历史截到 20，R@5/10、N@5/10，跟 TIGER。TIGER 官方代码未放出，他们按论文重做。Beauty 上 TIGER 的 R@10 是 0.0610，LETTER-TIGER 是 0.0672；LC-Rec 0.0642，LETTER-LC-Rec 0.0703。SASRec 的 Beauty R@10 是 0.0588，N@10 是 0.0313，仍是弱行。和原 TIGER 论文的 0.0648 差一截，说明重实现或预处理不完全相同，两篇的 Beauty 格子不要横比。

结论只在他们的重实现上成立，绝对提升大约 0.006 的 Recall@10。对选题：改的是 ID 怎么学，不是召回引擎。

### EAGER

路径 `EAGER-2406.14017.pdf`。Wang 等。KDD ’24。https://arxiv.org/pdf/2406.14017

声称的创新：行为码和语义码两条解码流；全局对比和语义引导的迁移任务，让两套码协作（第 2 页贡献）。

主表是表 2，第 6 页。Beauty、Sports、Toys 用的 SASRec 与 TIGER 数字和 TIGER 表 1 一致，Yelp 上 TIGER 标了星号，表示他们自己跑的。留一，历史截到 20，Recall 与 NDCG 的 5/10/20。Beauty Recall@10：EAGER 0.0836，最好基线 Recforest 0.0664，+25.90%；TIGER 0.0648；SASRec 0.0605。Toys Recall@20 的改进是 −3.85%。NDCG@10 Beauty 0.0525，低于 Xu 的 0.0597。表 1 的 Beauty 交互次数是 198,360，不是 198,502。正文把 Beauty Recall@5 的 +31.49% 写成相对 TIGER；表末的对照定义是该行最优基线，0.0618 相对的是 Recforest 的 0.0470，不是 TIGER 的 0.0454。

结论：Beauty 上相对表内基线的 Recall 提升在该协议下成立；「超过调好的 SASRec」不成立，Toys 的 Recall@20 在表内已经为负。对选题：双流生成 ID，与 SQL 无关。

### IDGenRec

路径 `IDGenRec-2403.19021.pdf`。Tan 等。SIGIR ’24。https://arxiv.org/pdf/2403.19021

声称的创新：用文本词而不是整数码当物品 ID，生成器和推荐器交替训练，使 ID 对齐推荐（摘要与 §3）。

主表是表 4，第 7 页。Sports、Beauty、Toys、Yelp。留一。第 6 页写明评估不用负采样，对全体物品排序。Beauty 统计是 22,363 / 12,101 / 198,502，与 Xu、STAR 相同。TIGER 附录没有印交互次数。HR@10 0.0814，NDCG@10 0.0541；SASRec 仍是 0.0605 / 0.0318。作者写的平均相对提升，Beauty 是 23.55%，对着每行最好的基线。

NDCG 仍低于 Xu 的 0.0597。结论只在「抄来的弱 SASRec + 全库留一」下成立。对选题：文本 ID 是给语言模型生成的，不是给数据库执行的。

### OneRec-Think

路径 `OneRec-Think-2510.11639.pdf`。Liu、Wang 等。首页无会议。https://arxiv.org/pdf/2510.11639

声称的创新：物品 token 对齐到 LLM 词空间；用推荐里的多步推理激活再增强；推理用推荐奖励，允许多个都算对的下一物品；线上用 Think-Ahead 把推理挪到离线（第 2 页）。

公开主表是表 1，第 6 页。Amazon Beauty、Toys、Sports，预处理引用 TIGER。留一，历史截到 50，beam 10。Beauty R@10：OneRec-Think 0.0791，ReaRec 0.0704，SASRec 0.0607，TIGER 0.0623。N@10 是 0.0471，SASRec 是 0.0320。消融表 2：Base 的 R@10 0.0654，加对齐 0.0735，加推理 0.0791。线上表 3：停留时长 +0.159%，观看时长 +0.169%，1.29% 流量、一周。

他们的 Beauty TIGER 是 R@10 0.0623，原论文是 0.0648。Toys 上他们的 TIGER R@10 是 0.0547，原论文是 0.0712，而且低于他们自己的 SASRec 0.0626。N@10 0.0471 低于 Xu 的 0.0597。结论只在他们这套弱 SASRec 上成立。对选题：推理文本不是 SQL，也不是约束谓词。工业数字不能复现。

### GPT4Rec

路径 `GPT4Rec-2304.03879.pdf`。Li 等。5 页。https://arxiv.org/pdf/2304.03879 。PDF 仍是 ACM 模板占位会议名，不当档案版引用。

声称的创新：

- 把下一物品写成「生成查询 + 搜索」。
- beam search 出多条查询，每条取 \(K/m\) 个不重复物品。
- 用目标标题当查询来微调 GPT-2，再单独调 BM25。

表 1，第 3 页。Beauty 与 Electronics，用户级 8:1:1，序列截断 15。Recall@K 是单个目标是否落在 top-K，文中没写采样负例。Beauty Recall@40：40 条查询 0.2040，BERT4Rec 0.1161，相对 75.7%。Electronics 0.0918 对 0.0751，相对 22.2%。基线是 FM-BPR、ContentRec、YouTubeDNN、BERT4Rec。没有 SASRec。

不能和留一全库的 Beauty 横比，物品数已经不同。结论只在这张表的协议下成立，而且强基线缺失。对选题：这是最近的「写查询、引擎执行」。抄的是管线。差在引擎是 BM25、查询是标题扩展、没有协同自连接、没有硬谓词的满足率。

### Xu 等，全量交叉熵 SASRec

路径 `Xu-SASRec-CE-2408.14238.pdf`。标题是 *Are LLM-based Recommenders Already the Best? Simple Scaled Cross-entropy Unleashes the Potential of Traditional Sequential Recommenders*。arXiv:2408.14238v1。

声称的创新：

- LLM 推荐器超过传统模型，是因为传统模型用了 BCE 或 BPR。换成全体物品上的交叉熵之后，SASRec 和 FMLP-Rec 反过来超过 LlamaRec、P5、E4SRec。
- 用归一化项的紧度和覆盖解释交叉熵为何更贴排序指标。
- 采样 softmax 配一个放大系数，可以用很少的负例接近全量 softmax。

主表是表 3，第 4 页。Beauty、Yelp，交互少于 5 次的去掉，留一。NDCG 和 MRR 由目标物品在全体物品中的名次算出。Beauty：22,363 / 12,101 / 198,502。

全量交叉熵 SASRec：Beauty NDCG@5/10 0.0510 / 0.0597，Yelp 0.0345 / 0.0415。LlamaRec：Beauty 0.0405 / 0.0492，Yelp 0.0306 / 0.0367。BPR SASRec 的 Beauty NDCG@10 是 0.0374。BCE 是 0.0353。Yelp 上全量交叉熵 FMLP-Rec 的 NDCG@10 是 0.0444，高于 SASRec。没有 ItemKNN，没有 EASE。

和 TIGER 的 Beauty 是同一用户数、同一物品数，可以比 NDCG 的方向，不能把 Xu 的 NDCG 当成 TIGER 的 Recall。结论站得住：在全库留一、全量 softmax 可算的目录上，微调 LLM 没有超过传统序列模型。对选题：先导里的序列基线必须是这一档，不能是 BPR-SASRec。它没有回答自连接能不能打过这一档。

### Ferrari Dacrema，RecSys 2019

路径 `FerrariDacrema-RecSys2019-1907.06902.pdf`。https://arxiv.org/pdf/1907.06902 。会议版是 RecSys ’19。

声称的创新：不是新模型。18 个顶会神经 top-n 方法里 7 个能以合理代价复现；这 7 个里 6 个经常输给近邻或基于图的简单方法；剩下的 Mult-VAE 明显好于简单基线，但没有稳定好于调好的非神经线性模型（摘要）。

协议是各原论文的 top-n 切分，他们再调 ItemKNN、P3α、RP3β，以及事后加的 SLIM。不是序列留一，不是采样 Hit。Netflix 上的数字见上一节表 8、表 9。

结论站得住，范围是 2015–2018 的矩阵式 top-n。对选题：支持「近邻和 SLIM 是强基线」，不支持「SASRec 全量交叉熵已经赢了 ItemKNN」。Mult-VAE 对 ItemKNN 的 Recall@20 是 0.2626 对 0.2088，神经方法并非一律输给近邻。

### Ferrari Dacrema，TOIS 2021

路径 `FerrariDacrema-TOIS2021-1911.07698.pdf`。学校库 403，用的是 arXiv:1911.07698，49 页，文首即 TOIS 引用。

声称的创新：把 2019 的复现扩到 2015–2018 的 SIGIR、KDD、WWW、IJCAI、WSDM、RecSys。26 篇相关，12 篇可复现（46%）。8 篇输给近邻一类方法。计入线性模型后，12 篇里只有 1 篇明确好于非神经基线，且只在一个数据集上（第 2–3 页）。摘要的口径是 11/12 可以被近邻或线性模型超过，没有一个复杂神经方法稳定好于已有的学习型方法（矩阵分解或线性模型）。

后来的讨论里他们把 EASE 放进来：EASE 比 NeuMF 更准，而且在其中一个数据集上和 Mult-VAE 同一档（附录对 Mult-VAE 的讨论）。这是 2021 年的追加，不是 2018 年那些论文自己的表。

结论站得住，任务仍是评分矩阵上的 top-n，不含会话推荐和今天的 SASRec。对选题：引用时要带上「8/12 输给近邻，1/12 在一个数据集上赢过非神经方法」这两句，不要收成「神经方法都不行」。EASE 在这里是强线性基线，但不是用自连接写出来的。

### Shevchenko 这条线（Benigni 等）

路径 `Shevchenko-2505.09364.pdf`。标题 *Diffusion Recommender Models and the Illusion of Progress*。arXiv:2505.09364。刊头 TORS 2026。

声称的创新：复现 SIGIR 2023–2024 的九个扩散推荐模型，来自四篇论文：DiffRec（SIGIR ’23）、CF-Diff、GiffCF、DDRM（均 SIGIR ’24）。检查方差、弱基线，并讨论扩散生成分布和离线「几乎确定性的推荐列表」不匹配。

协议跟着原论文的数据和划分，再系统调 TopPop、UserKNN、ItemKNN、RP3β、GF-CF、EASE、SLIM、MF-BPR、iALS、MultVAE。指标是 Recall 和 NDCG 的 10 和 20，全库 top-n 的口径，不是序列留一。

Amazon-Books（clean）表 2，第 21 页：ItemKNN Recall@10 0.1133、NDCG@10 0.0743、Recall@20 0.1525。DiffRec 论文数字 Recall@10 0.0695，他们重跑 0.0692±0.0007。LT-DiffRec 论文 0.0838，重跑 0.0835±0.0018。SLIM Recall@20 0.1561，略高于 ItemKNN 的 0.1525，但 NDCG@10 是 0.0707，低于 ItemKNN 的 0.0743。EASE 缺席。正文写：所有简单的近邻和图方法都超过 DiffRec 及其变体；ItemKNN 几乎一直领先。Yelp 上 DiffRec 大约打平 ItemKNN，仍低于 RP3β、iALS 或 GF-CF。MovieLens-1M（clean）上，论文里的 DiffRec 数字看起来有竞争力，但方差大，而且 EASE 更高；EASE 因内存没有出现在 Amazon-Books 这张表上。

有的配置他们判为不可复现或只部分可复现，方差最大到约 18%（引言）。GiffCF 的论文还写了在测试集上调超参。表 7（MovieLens-1M clean，归一化 Recall@10）：论文值 0.1251，高于同表 EASE 的 0.1186；改到验证集调参后，GiffCF (hyperopt) 是 0.0936±0.0269，低于 ItemKNN 的 0.1092 和 EASE。结论站得住：这四篇的「超过强基线」在换上调过的近邻和线性模型、并且不在测试集上调参之后不成立。对选题：ItemKNN 在清洗后的 Amazon-Books 上领先，正是自连接那一类。用这篇证明「SQL 版 ItemKNN 没前途」，方向反了。用这篇证明「新模型必须打过调好的 ItemKNN」，方向对。

### SIEVE

路径 `SIEVE-PVLDB18-li.pdf`。Li 等。PVLDB 2025。https://www.vldb.org/pvldb/vol18/p4723-li.pdf

声称的创新：不为每个谓词改遍历，而是按负载建一堆子索引；用索引大小、搜索时间、recall 的三维模型决定建哪些、查询时用哪个。相对其他索引，加速最高 8.06 倍，建索引时间可低到对方的 1%，内存小于一份 HNSW 的 2.15 倍（摘要）。

实验是向量检索的 recall@10 对 QPS，数据集见 §3。后过滤要取 \(k/sel\) 写在 §2.2。儿童向和价格区间只出现在引言。ACORN 在低选择率数据上 recall 大约停在 0.95，不是 0.2。

结论在「过滤向量搜索的吞吐和 recall」上站得住。对选题：只能支持「谓词下图索引会退化、精确过滤不会漏」。不能支持推荐 NDCG。先导里若做后过滤向量臂，多取倍数按这里的 \(1/sel\) 写清楚。

### Lim 等

路径 `Lim-PVLDB19-filtered-ANN.pdf`。Lim、Kim、Kim、Do。PVLDB 2026。https://www.vldb.org/pvldb/vol19/p2763-lim.pdf

声称的创新：过滤近似搜索的难度不该用选择率或属性–向量相关来代表；他们定义 α-Hardness，并用它生成可控负载 HCBGen。现有基准偏容易，所以各方法的排序在更难的负载上会变（摘要）。

§5.3 的「often below 0.2」和「around or below 0.1%」见上一节。谓词是 SIFT/GIST 上的合成标签，以及用来对齐难度分布的半真实负载。recall 是近邻召回率。

结论站得住，对象是索引评测，不是推荐。对选题：引用这句时必须写明是向量近邻 recall、合成谓词、高难度档。不要写成「推荐约束下 Hit 低于 0.2」。

### RepeatNet

路径 `RepeatNet-1812.02646.pdf`。Ren 等。arXiv 版带 AAAI 2019 版权；OJS PDF 没下到。

声称的创新：会话推荐里显式建重复模式和解锁模式，用模式开关决定何时从历史里再推同一个物品（摘要）。

主表是表 3，第 6 页，单位是百分数。会话内下一物品，MRR 和 Recall 的 10 与 20。不是全库留一的 Amazon 协议，绝对数字高，是因为会话推荐的常规尺度。

DIGINETICA 的 Recall@20：RepeatNet（去掉重复机制）42.56，RepeatNet 47.79，NARM 49.70，Improved-GRU4REC 46.16。47.79 没有显著性标记。LASTFM 的 Recall@20：去掉重复机制 29.96，RepeatNet 32.38（有显著性标记），NARM 29.94。YOOCHOOSE 的 Recall@20：RepeatNet 70.71，GRU4REC-TOPK 70.30，70.71 无显著性标记。

「从 42.56 到 47.79」只是自己的消融，而且仍低于 NARM。结论：重复头相对自己的探索支路，在 DIGINETICA 和 LASTFM 上提高了 Recall@20；「打赢当时的会话模型」在 DIGINETICA 的 Recall@20 上不成立。对选题：历史过滤或重复连接可以把买过的物品精确取回，这是机制，不是这张表的胜负。先导里报重复物品的命中时，对照应包括「只做集合过滤」的 SQL，而不是把 47.79 当成要超越的 SOTA。

### RecGPT

路径 `RecGPT-2507.22879.pdf`。RecGPT Team。42 页技术报告。https://arxiv.org/pdf/2507.22879

声称的创新：LLM 先写用户兴趣，再写物品标签，标签注进双塔，变成用户–物品–标签三塔；另有一个模型在检索之后写解释；多阶段训练以适应线上（摘要与 §2）。

没有公开数据集，没有 Recall@K 或 NDCG。线上相对他们的基线系统：CTR +6.33%，IPV +9.47%，DCAU +3.72%，CICD +6.96%，停留相关的 DT +4.82%（摘要和第 1 页的指标列举）。图里的 CTR 做了归一化。

结论只在该工业系统的线上协议下成立，外部无法复核。对选题：标签注入不是 SQL。解释是另一个模型，不是查询文本。不要把 +6.33% 放进和 Recall 同一张表。

### InteRecAgent

路径 `InteRecAgent-2308.16505.pdf`。Huang、Lian 等。首页无会议名。https://arxiv.org/pdf/2308.16505

声称的创新：LLM 做规划，推荐模型当工具；候选集在工具之间用共享内存传递；SQL 工具负责硬条件，ItemCF 负责相似，排序器负责打分；为了让小模型学会调工具，做了模仿数据（第 2 页贡献）。

SQL 的边界写在附录的工具说明里：只能查一张物品信息表；不许用 SQL 找相似物品；标题不能当条件。相似物品走 ItemCF 工具。

表 5（第 9 页）是一轮推荐，单位百分数。检索 Recall@5：InteRecAgent 在 Steam / Movie / Beauty 上是 65.05 / 52.02 / 30.28，GPT-4 是 56.77 / 47.78 / 12.80。排序是用户给出的 20 个候选：1 个正例加 19 个随机负例，NDCG@20。Beauty 上是 40.05 对 GPT-4 的 33.28。没有 SASRec，没有 EASE，没有全库 Recall。

结论只在「对话式工具调用 + 这套采样排序」下成立。对选题：这是已经发表的「LLM 写推荐 SQL」。审稿人会拿它当最近的系统前作。差异必须写清：对方禁止自连接，协同召回仍是 ItemCF 工具；本文若只做属性 `WHERE`，就是在复现他们的 SQL 工具。

### Bing Q′：两份非档案稿

WebReco：`WebReco-IRS2024-not-archival.pdf`，IRS ’24（挂在 CIKM 2024 下）。https://irsworkshop.github.io/2024/publications/paper_webreco.pdf

EARL：`Bing-Qprime-EARL2024-not-KDD.pdf`，EARL ’24（RecSys 2024 研讨会）。https://earl-workshop.github.io/pdf/recsys2024-workshops_paper_29.pdf

档案版 *Towards Web-scale Recommendations with LLMs*（KDD ’25，DOI 10.1145/3690624.3709413）未打开。下面不把它的摘要当成表内数字。

两份开放稿里，Q′ 的创新是同一句：LLM 从网页的 URL、标题、正文写平均约 6 条互补查询，Bing 取每条的 top 10，去重后每个触发页最多存 30 个候选。为了扩到数亿 URL，用 GPT-4 的查询蒸馏 Mistral-7B。

WebReco 表 2 与 EARL 表 5：GPT-4 的 CTR +0.89%、RecoDCG@5 +0.760；Mistral-7B 的 CTR +1.71%、RecoDCG@5 +0.762。RecoDCG 是用 LLM 打的相关性做 DCG，不是公开库的 NDCG。EARL 还写了质量感知排序与 Q′ 叠在一起时，CTR 净 +0.52%、RecoDCG@5 +5.862，那是另一行处理，不要和 Q′ 单独的 +0.760 加在一起理解。

结论只在 Bing 网页推荐的线上协议下成立，而且来源不是档案版。对选题：审稿人会说管线相同。不同点是引擎、查询语言、有没有协同自连接、评价是 CTR 还是可行集上的 Recall。引用时标题要写成研讨会名，并注明不是 KDD 2025。

## 对先导实验

无约束的下一物品不要当主表。主表放带谓词的召回：品类、品牌、价格、排除已买，候选必须落在可行集里。同时报可行集上的 Recall@K、NDCG、约束满足率、调用次数和连接时间。无约束格子只用来说明「把 ItemKNN 写成 SQL」没有额外增益，而且序列基线要用全量交叉熵。

必须进先导、并且要出数字的三个对照：

1. **全量交叉熵 SASRec**（Xu 等的训练目标，全库排序）。带约束的实验里，先用它排出候选，再套同一组谓词做后过滤。BPR-SASRec 可以放在附录，用来展示弱基线会把 SQL 衬得过好。
2. **调好的 ItemKNN，用 SQL 自连接实现**（余弦或 Jaccard，加收缩；不要用 STAR 那种 top-10 UserKNN）。这是平凡对照。内存放得下的切分上再加 **EASE** 的后过滤。Shevchenko 在 Amazon-Books 上没跑成 EASE，先导若用 Beauty 或 STaRK 的子集，要单独确认内存，缺了就写明，不要把 ItemKNN 的结果说成 EASE 的结果。
3. **后过滤的向量检索**，多取倍数按大约 \(1/sel\)（SIEVE §2.2）。报它在谓词下的近邻 recall 或可行集 Recall，以及约束满足率。没有这一臂，「精确 SQL 胜过向量召回」没有对照。

GPT4Rec 和 Q′ 写进相关工作，不进这张数字主表。它们的切分、目录和指标都对不上。InteRecAgent 用来划界：属性 SQL 已经有人做了，自连接才是空的。

## 不要当成证据的三篇

1. **STAR 表 2 的 KNN。** Hits@10 为 0.007 的是 top-10 UserKNN。不能用来说明 ItemKNN 或 Swing 很弱，也不能用来说明 SQL 自连接没有竞争力。
2. **TIGER 表 1，以及原样抄走这行 SASRec 的 EAGER、IDGenRec。** 「超过 SASRec」的参照是 NDCG@10 约 0.032 的那一档。同一份 Beauty 上，全量交叉熵 SASRec 的 NDCG@10 是 0.0597，高于 TIGER 的 0.0384、EAGER 的 0.0525、IDGenRec 的 0.0541。这三篇不能作为「生成式检索已经打赢调好的序列模型」的证据。OneRec-Think 的 N@10 0.0471 同样不要写成打赢了这一档。
3. **RepeatNet 的 42.56 到 47.79。** 这是去掉自身重复头之后的消融。同表 DIGINETICA 上 NARM 的 Recall@20 是 49.70，高于 RepeatNet 的 47.79。不能写成「显式重复模式打赢了会话推荐」。历史过滤能精确取回重复物品，这是另一句话，不需要这个数字撑着。

另外两处容易误引，但不占上面的三个名额：NoteLLM 的新笔记评论 +3.58% 是内容嵌入对 SentenceBERT 的线上结果；SIEVE 引言里的「儿童向 / 价格」没有对应的推荐 NDCG 实验。
