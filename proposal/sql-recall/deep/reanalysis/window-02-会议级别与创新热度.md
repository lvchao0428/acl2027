# SQL 召回：已读论文的会议档次与创新点热度

日期：2026-11-11。对象是「大模型写 SQL、当作推荐召回」这一选题已经读过的目标论文。数字和会议名只来自本仓库笔记：`00_总览.md`、`07_继续调研.md`、`大纲/` 五份清单、`deep/reanalysis/` 的五步与 `window-02.md`、`00_五步之后的网格.md`、`deep/06_创新点总表.md`、`deep/00_批判后的决定.md`。笔记没有投稿数，也没有录用率。下面的篇数是这批已读论文的场合分布，不能写成全领域统计，也不能写成某会的中稿率。

分档是便于选题的口径，不是 CCF 官方目录，也不补 CCF 等级。

- **档案顶会**：笔记点名 NeurIPS（含 Datasets and Benchmarks）、KDD、SIGIR、WWW（含短文）、AAAI、CIKM 且笔记没有写研讨会或「不是档案」、RecSys 且笔记没有写研讨会、ACL / NAACL / EMNLP 的档案长文、短文或 Findings。
- **档案期刊**：笔记点名 PVLDB、TOIS、TORS。
- **研讨会**：笔记写明 IRS、EARL、Companion、workshop、Workshop、DATA-FM workshop，或写明不是档案。
- **仅预印本**：首页未印会议名、页眉没有会议名、页眉是占位会议名、笔记写「不是档案版」。这一档不进入档案顶会的篇数。
- **技术报告**：笔记写明技术报告的，单独一档。本批只有 RecGPT。
- **名单外已点名**：笔记印了会议名，但该名字不在上面的档案名单里。按原句保留，不升格，也不改叫研讨会。ICLR、SIGMOD、CIDR、COLM、WSDM、ClinicalNLP、BDMA、IJCNLP-AACL、EMNLP Industry Track 都在这一档。
- **场合未统一或未核实**：两边说法冲突，或打开的页面没有印出会议全称。不升格。

同一篇只计一次。SIEVE 的 arXiv 与 PVLDB 是一篇，档次按笔记写明的 PVLDB。RelBench v1 的长预印本不另计。WebReco 与 EARL 是两篇；Q′ 那一组线上数字在后文只算一次观察。RecSys 2019 与 TOIS 2021 是两篇。SUQL、TAG 只归大纲 01。InteRecAgent 只归大纲 02。QUEST 只归大纲 04。RecBench+ 只归大纲 03。

不收入、也不把会议名写成已核实的：GenFacet（`07` 写 DOI 和 ISBN 仍是占位符，自称 SIGIR 2026 不能用）；只读摘要且没有核成可引用会议名的 K-RagRec、Zamani 2018、2009 年分面检索；Amazon-M2 只出现在数据表里，不是大纲清单中的论文。

年份规则：笔记给了会议年，就用会议年。没有会议名时，用笔记写出的日期；只有 arXiv 号时，用号段的年份。ScienceBenchmark 的文件名写 2024，笔记写 PDF 自署 2023，计入 2023。TalkPlay-Tools 的号段是 2510，窗口 03 写 v4 日期 2026-06-02，计入 2026。

---

## 1. 结论

这批已读论文共 **94** 篇：大纲五份清单 **79** 篇，`07_继续调研.md` 里已经核过场合的近邻 **15** 篇。档次如下。

| 档次 | 篇数 | 其中大纲清单 | 其中 07 近邻 |
|---|---:|---:|---:|
| 档案顶会 | 31 | 25 | 6 |
| 档案期刊 | 5 | 5 | 0 |
| 研讨会 | 5 | 5 | 0 |
| 仅预印本 | 36 | 29 | 7 |
| 技术报告 | 1 | 1 | 0 |
| 名单外已点名（不升格） | 14 | 14 | 0 |
| 场合未统一或未核实 | 2 | 0 | 2 |
| 合计 | 94 | 79 | 15 |

档案顶会 31 篇里，有 2 篇没有把全文结果表纳入下面的中稿原因：Hidasi 的 RecSys 2023 只读了 ACM HTML 的问题界定；Zhang 的 RecSys 2026 短文只打开了 ACM 摘要页。其余 29 篇的场合来自大纲或 `07` 里已经打开的正文。

能对上这批笔记的中稿档次是：

- 档案顶会里反复出现的，是弱序列基线上的语义 ID、把 LLM 当成物品编码器或笔记编码器、域内执行准确率或拒答、没有用户问句的关系库预测，以及仍然带着 BM25 或稠密检索器的半结构化检索。CIKM 2024 的商品过滤接口占的是过滤 schema 的 Exact Match，没有候选召回，也没有 SQL。
- 档案期刊占住的是过滤近似搜索的近邻 recall（PVLDB），以及「新模型至少要打过调过的近邻」（RecSys 2019 是顶会，TOIS 2021 与 TORS 2026 是期刊）。
- 「模型写查询、搜索引擎执行」的线上 CTR 在这批笔记里停在 CIKM 2024 IRS 和 RecSys 2024 EARL，两篇都写明不是档案。Q′ 只算一次观察。
- 「LLM 写推荐 SQL 并用 Recall 打分」的 InteRecAgent，笔记写首页未印会议名。HyST、ProRetrieval、MACS 也是未印会议。这三篇加上 InteRecAgent 把「第一次做结构化商品过滤 / 第一次让模型写 SQL 再打 Hit」堵上了，但它们不进入档案顶会的篇数。

对 ACL 2027，档案顶会已经吃满的是上面四块：领域模板加域内执行准确率，拒答和可靠性分，无约束下一物品上的语义 ID 与全量交叉熵这一档序列模型，以及仍然带着检索器的半结构化混合系统。还能投的一句，按 `window-02.md` 和网格已经定下的那句，是**带谓词的召回测量**。原句是：自然语言里同时有硬谓词和协同意图时，模型写出带谓词的协同 SQL，数据库执行，在同一组谓词下同时报可行集上的 Recall、NDCG 和约束满足率。无约束下一物品上把 ItemKNN 写成 SQL，这一格写出来就是 SQL 版近邻，空本身不是 ACL 贡献。

这一句值得做，是因为同一组谓词下的三臂对照表在这 24 篇召回笔记里不存在，不是因为已经知道 SQL 会赢。三臂是：Xu 等的全量交叉熵 SASRec 再套同一组谓词；同一条 SQL 写出的、余弦加收缩的 ItemKNN；按 SIEVE 大约 \(1/\mathrm{sel}\) 多取的后过滤向量。STaRK-Amazon 上「关系片段写成 SQL、文档上另排」是另一张表，网格写明不要收成「SQL 替换向量检索」。`07` 要求点名 HyST、ProRetrieval、MACS、Malik 等 CIKM 2024，以及仓库里已有的 InteRecAgent、TalkPlay-Tools、SUQL。

---

## 2. 分档表

一篇一行。创新点类型用网格和总表里已经有的叫法。一篇只标主类型；跨格的在第 3 节说明。

### 2.1 大纲 01：Text-to-SQL（22）

| 论文 | 笔记里的场合 | 档次 | 创新点类型 | 计入年份 |
|---|---|---|---|---|
| ScienceBenchmark | PVLDB 17(4): 685–698, 2023。文件名写 2024，PDF 自署 2023 | 档案期刊 | 文本转 SQL：域内执行准确率 | 2023 |
| SM3-Text-to-Query | NeurIPS 2024 Datasets and Benchmarks | 档案顶会 | 文本转 SQL：域内执行准确率 | 2024 |
| BiomedSQL | COLM 2026 | 名单外已点名 | 文本转 SQL：域内执行准确率 | 2026 |
| BookSQL | NAACL 2024 长文，页 497–516 | 档案顶会 | 文本转 SQL：域内执行准确率 | 2024 |
| FinSQL / BULL | arXiv:2401.10506。页眉是 Conference’17 占位，笔记写不要当成已出版会议 | 仅预印本 | 文本转 SQL：域内执行准确率 | 2024 |
| FINCH | arXiv:2510.01887，2025-10-02。没有会议页眉 | 仅预印本 | 文本转 SQL：域内执行准确率 | 2025 |
| EHRSQL | NeurIPS 2022 Datasets and Benchmarks | 档案顶会 | 文本转 SQL：拒答 | 2022 |
| EHRSQL 2024 共享任务 | ClinicalNLP 2024，页 644–654 | 名单外已点名 | 文本转 SQL：拒答 / 可靠性分 | 2024 |
| TrustSQL | arXiv:2403.15879，2024-07-02。页眉没有会议名 | 仅预印本 | 文本转 SQL：拒答 | 2024 |
| OMOP text-to-SQL | ClinicalNLP @ LREC 2026，页 381–393 | 名单外已点名 | 文本转 SQL：拒答；域内高执行分 | 2026 |
| Query Carefully | arXiv:2512.21345，2025-12-19。没有会议页眉 | 仅预印本 | 文本转 SQL：拒答 | 2025 |
| Binder | ICLR 2023 | 名单外已点名 | 文本转 SQL：SQL 当中间表示 | 2023 |
| SUQL | NAACL 2024 Findings，页 4535–4555 | 档案顶会 | 文本转 SQL：自由文本谓词；人工集合精度 | 2024 |
| TAG | CIDR 2025 | 名单外已点名 | 文本转 SQL：SQL 当中间表示 | 2025 |
| H-STAR | NAACL 2025 长文，页 8841–8863 | 档案顶会 | 文本转 SQL：表问答路由 | 2025 |
| BlendSQL | arXiv:2402.17882。没有会议页眉 | 仅预印本 | 文本转 SQL：SQL 当中间表示 | 2024 |
| FLEX | NAACL 2025 长文，页 4448–4475 | 档案顶会 | 文本转 SQL：执行对错会改名次 | 2025 |
| Jin 等，标注错误审计 | arXiv:2601.08778。没有会议页眉 | 仅预印本 | 文本转 SQL：金 SQL 会改名次 | 2026 |
| Wretblad 等 | ACL 2024 短文，页 356–369 | 档案顶会 | 文本转 SQL：噪声与金 SQL | 2024 |
| Spider 2.0 | ICLR 2025 | 名单外已点名 | 文本转 SQL：企业库上的执行 | 2025 |
| Arctic-Text2SQL-R1 | ACL 2026 Findings，页 26966–26995 | 档案顶会 | 文本转 SQL：奖励只看执行 | 2026 |
| OmniSQL | arXiv:2503.02240。没有会议页眉 | 仅预印本 | 文本转 SQL：域内执行准确率 | 2025 |

### 2.2 大纲 02：召回（24）

| 论文 | 笔记里的场合 | 档次 | 创新点类型 | 计入年份 |
|---|---|---|---|---|
| TIGER | NeurIPS 2023 | 档案顶会 | 语义 ID 生成式检索 | 2023 |
| EAGER | KDD 2024 | 档案顶会 | 语义 ID 生成式检索 | 2024 |
| LETTER | CIKM 2024 | 档案顶会 | 语义 ID 生成式检索 | 2024 |
| LC-Rec | 首页未印会议名。arXiv:2311.09049 | 仅预印本 | 语义 ID 生成式检索 | 2023 |
| IDGenRec | SIGIR 2024 | 档案顶会 | 语义 ID 生成式检索 | 2024 |
| OneRec-Think | 首页未印会议名。arXiv:2510.11639 | 仅预印本 | 语义 ID 生成式检索 | 2025 |
| LLM2Rec | KDD 2025 | 档案顶会 | LLM 做物品编码器或对齐 | 2025 |
| LEARN | AAAI，版权页 2025 | 档案顶会 | LLM 做物品编码器或对齐 | 2025 |
| HLLM | 首页未印会议名。arXiv:2409.12740 | 仅预印本 | LLM 做物品编码器或对齐 | 2024 |
| NoteLLM | WWW 2024 Companion | 研讨会 | LLM 做物品编码器或对齐（笔记对笔记） | 2024 |
| NoteLLM-2 | KDD 2025 | 档案顶会 | LLM 做物品编码器或对齐（笔记对笔记） | 2025 |
| STAR | 首页未印会议名。arXiv:2410.16458 | 仅预印本 | 网格列：向量（语义加事先算好的共现） | 2024 |
| GPT4Rec | arXiv:2304.03879。笔记写 PDF 不是档案版，页眉是占位会议名 | 仅预印本 | 生成查询再搜索（BM25） | 2023 |
| InteRecAgent | arXiv:2308.16505。首页未印会议名 | 仅预印本 | 属性 SQL / 工具调用 | 2023 |
| WebReco | CIKM 2024 的 IRS 研讨会，不是档案 | 研讨会 | 生成查询再搜索（Bing） | 2024 |
| EARL 上的 Q′ | RecSys 2024 的 EARL 研讨会。笔记写不是 KDD 2025 | 研讨会 | 生成查询再搜索（Bing） | 2024 |
| RecGPT | arXiv:2507.22879。42 页技术报告 | 技术报告 | LLM 写标签注入三塔（不是 SQL） | 2025 |
| Xu 等，全量交叉熵 | arXiv:2408.14238。首页无会议 | 仅预印本 | 全量交叉熵序列模型 | 2024 |
| Ferrari Dacrema 等 | RecSys 2019 | 档案顶会 | 复现与强基线批判 | 2019 |
| Ferrari Dacrema 等 | TOIS 39(2) Article 20，2021 年 1 月 | 档案期刊 | 复现与强基线批判 | 2021 |
| Benigni、Ferrari Dacrema、Jannach | TORS 4(1) Article 46，出版日期印为 2026 年 3 月 | 档案期刊 | 复现与强基线批判 | 2026 |
| SIEVE | 会议版 PVLDB 18(11)，2025。分析用 arXiv，不另计 | 档案期刊 | 过滤向量搜索 | 2025 |
| Lim 等 | PVLDB 19(10):2763–2776, 2026 | 档案期刊 | 过滤向量搜索 | 2026 |
| RepeatNet | arXiv:1812.02646，带 AAAI 2019 版权行 | 档案顶会 | 会话重复头（笔记用来挡住横比） | 2019 |

### 2.3 大纲 03：benchmark（7）

| 论文 | 笔记里的场合 | 档次 | 创新点类型 | 计入年份 |
|---|---|---|---|---|
| STaRK | NeurIPS 2024 Datasets and Benchmarks | 档案顶会 | 混合检索与指标（半结构化全库检索） | 2024 |
| RecBench+ | 页眉 WSDM ’26 | 名单外已点名 | 网格列：LLM 凭记忆生成标题 | 2026 |
| BLaIR / Amazon-C4 | ACL 2026 长文 | 档案顶会 | 混合检索与指标（稠密检索；论文无 SQL 行） | 2026 |
| EComAgentBench | EMNLP 2026 Industry Track，页 1012–1027 | 名单外已点名 | 属性过滤（最多 10 个 id 上的子串） | 2026 |
| REGEN | 重析未印会议名。页眉是 ACM 占位 | 仅预印本 | 网格列：LLM 凭记忆生成标题（下一物品叙事） | 2025 |
| TalkPlay-Tools | 页眉 Preprint。arXiv:2510.01698，v4 日期 2026-06-02 | 仅预印本 | 属性 SQL / 工具调用（单表布尔 SQL） | 2026 |
| AgentRecBench | 页眉 Preprint。arXiv:2505.19623，2025-05-28 | 仅预印本 | 无约束下一物品的 20 选 1（没有全库召回） | 2025 |

### 2.4 大纲 04：指标与混合检索（19）

| 论文 | 笔记里的场合 | 档次 | 创新点类型 | 计入年份 |
|---|---|---|---|---|
| LIMIT | ICLR 2026 | 名单外已点名 | 混合检索与指标 | 2026 |
| Text2VectorSQL | arXiv:2506.23071。大纲未印会议名 | 仅预印本 | 混合检索与指标（SQL 与向量的两种顺序） | 2025 |
| NevIR | arXiv:2305.07614。大纲未印会议名 | 仅预印本 | 混合检索与指标（自由文本里的否定） | 2023 |
| ExcluIR | arXiv:2404.17288。大纲未印会议名 | 仅预印本 | 混合检索与指标（自由文本里的排除） | 2024 |
| NumConQ | BDMA 2026 | 名单外已点名 | 混合检索与指标（问句里的数值） | 2026 |
| QUEST | ACL 2023 | 档案顶会 | 混合检索与指标 | 2023 |
| FollowIR | NAACL 2025 | 档案顶会 | 混合检索与指标（叙事指令） | 2025 |
| BRIGHT | ICLR 2025 | 名单外已点名 | 混合检索与指标（推理型检索） | 2025 |
| ACORN | SIGMOD 2024 | 名单外已点名 | 过滤向量搜索 | 2024 |
| AvaTaR | arXiv:2406.11200。大纲未印会议名 | 仅预印本 | 混合检索与指标 | 2024 |
| KAR | arXiv:2410.13765。大纲未印会议名 | 仅预印本 | 生成查询再搜索（扩展后引擎仍是 BM25） | 2024 |
| MoR | arXiv:2502.20317。大纲未印会议名 | 仅预印本 | 混合检索与指标（文本臂仍是 BM25） | 2025 |
| mFAR | ICLR 2025 | 名单外已点名 | 混合检索与指标（多字段词法） | 2025 |
| HybGRAG | ACL 2025 | 档案顶会 | 混合检索与指标（检索器银行；没有 Amazon） | 2025 |
| SAGE / SPARK | arXiv:2602.16964，2026-02-18。大纲未印会议名 | 仅预印本 | 混合检索与指标（HNSW、Cypher、BM25 回退） | 2026 |
| PCN-Rec | arXiv:2601.09771。大纲未印会议名 | 仅预印本 | 约束校验（候选来自 MF/CF，不是 SQL） | 2026 |
| Faithful Chain-of-Thought | IJCNLP-AACL 2023 | 名单外已点名 | 指标：忠实等于求解器执行符号链 | 2023 |
| Atil 等 | arXiv:2408.04667。大纲未印会议名 | 仅预印本 | 指标：字符串一致（TARr） | 2024 |
| ReproRAG | 页眉 Workshop ’25。具体研讨会名未印 | 研讨会 | 指标：结果集 Jaccard | 2025 |

### 2.5 大纲 05：RelBench（7）

| 论文 | 笔记里的场合 | 档次 | 创新点类型 | 计入年份 |
|---|---|---|---|---|
| RelBench v1 会议版 | NeurIPS 2024 Datasets and Benchmarks。12 页 | 档案顶会 | 关系库推荐（输入是实体和种子时间） | 2024 |
| RelBench v2 | ICLR 2026 DATA-FM workshop | 研讨会 | 关系库推荐 | 2026 |
| ContextGNN | arXiv:2411.19513。这份 PDF 没有会议页眉 | 仅预印本 | 关系库推荐 | 2024 |
| Fey 等 | arXiv:2312.04615。这份 PDF 没有会议页眉。RelBench 会议版把它引成 ICML 2024 position paper | 仅预印本 | 关系库推荐（框架；无 MAP 实验） | 2023 |
| Wydmuch 等 | arXiv:2411.11829。大纲未印会议名 | 仅预印本 | 关系库上的分类与回归（链接 MAP 没测） | 2024 |
| RelAgent | NeurIPS 2026 | 档案顶会 | 关系库：SQL 出特征，再接树模型 | 2026 |
| ReFuGe | WWW 2026 短文 | 档案顶会 | 关系库：SQL 出特征，再接 LightGBM | 2026 |

Fey 的 ICML 2024 是另一篇论文的转引，本 PDF 无页眉，且 ICML 不在本分档的档案名单里。不把这一篇计入 2024 的档案顶会。

### 2.6 `07` 里核过场合的近邻（15）

| 论文 | 笔记里的场合 | 档次 | 创新点类型 | 计入年份 |
|---|---|---|---|---|
| HyST | arXiv:2508.18048，2025-08-25。打开的 arXiv 页没有会议名 | 仅预印本 | 硬属性过滤后再做向量检索（JSON，不是 SQL） | 2025 |
| ProRetrieval | arXiv HTML `2608.27017`。首页没有会议名 | 仅预印本 | 属性 SQL / 工具调用（SQL 加检索占位符） | 2026 |
| MACS | arXiv HTML `2608.14068`。首页没有会议名 | 仅预印本 | 属性 SQL / 工具调用（槽位映射成 WHERE） | 2026 |
| Malik 等，自然语言到商品过滤接口 | CIKM 2024 | 档案顶会 | 属性过滤 schema（没有 SQL，没有候选召回） | 2024 |
| Pandey | 预印本，首页日期 2026-02-03，arXiv:2602.00899。没有会议页眉 | 仅预印本 | 稠密检索的失败类型（过滤臂没有 Recall） | 2026 |
| BEATS | SIGIR 2026 | 档案顶会 | 属性写进商品文本，再训双塔（不经过 SQL） | 2026 |
| RecoAtlas | arXiv HTML `2605.18805`。首页没有会议名 | 仅预印本 | 购物代理的工具调用（工具不是 SQL） | 2026 |
| SQLForge | ACL 2025 Findings，页 8441–8452 | 档案顶会 | 文本转 SQL：域内执行准确率 | 2025 |
| Jannach 与 Liegl | 打开的前两页没有再印会议全称。年份只记到文件名 `Conference_IEA_2006` | 场合未核实 | 约束放松的最小定义（没有 LLM，没有把 SQL 当 top-K） | 2006 |
| DAIL-SQL | arXiv:2308.15363。打开的 arXiv 页没有印期刊名 | 仅预印本 | 文本转 SQL：提示和例选 | 2023 |
| DIN-SQL | NeurIPS 2023 | 档案顶会 | 文本转 SQL：分解提示。总览已排除出强基线 | 2023 |
| MAC-SQL | arXiv:2312.11242。打开的 arXiv 页没有印会议名 | 仅预印本 | 文本转 SQL：分解后用工具改 SQL | 2023 |
| CHESS | arXiv:2405.16755。作者主页写成 ICML 2025 的 MAS workshop；实验室页面的 bib 仍标预印本 | 场合未统一 | 文本转 SQL：schema 裁剪 | 2024 |
| Zhang | RecSys 2026 短文。只打开了 ACM 摘要页，没有全文 | 档案顶会 | 评测协议：固定候选和各自召回 | 2026 |
| Hidasi 与 Czapp | RecSys 2023。读了 ACM HTML 的问题界定 | 档案顶会 | 复现与强基线批判（离线评测的四类缺陷） | 2023 |

CHESS 只在 2024 计一次。2025 的 workshop 说法和预印本说法没有合成一个场合，所以不另计入 2025，也不计入档案顶会或研讨会。

---

## 3. 按创新点：中稿形态与投 ACL 的退稿风险

笔记没有收录审稿意见原文。这一节的「能出现在那一档」只复述笔记已经写明的贡献形态和证据范围。「投 ACL 会被打回」只复述仓库写死的禁区：弱基线、指标横比、把 ItemKNN 换个 SQL 写法、执行准确率当主指标、研讨会 CTR 当公开库证据。笔记里已经写过「审稿人会把它叫成……」的句子，也只复述那些句子。

### 3.1 语义 ID 生成式检索

代表论文和已核实场合：TIGER 在 NeurIPS 2023，EAGER 在 KDD 2024，LETTER 在 CIKM 2024，IDGenRec 在 SIGIR 2024。LC-Rec 与 OneRec-Think 首页未印会议名，不把这一路的最高场合抬高。

笔记里能对上的贡献形态是：用离散码或文本词当物品 ID，自回归生成下一个物品，在他们自己的表里高于那一行 SASRec。TIGER 写明那一行来自 S3-Rec 公开结果。Beauty 上这行 SASRec 的 NDCG@10 是 0.0318；TIGER 自己是 0.0384，Recall@10 相对最好基线 +0.15%。EAGER 的 Beauty NDCG@10 是 0.0525，Toys 的 Recall@20 改进栏是 −3.85%。IDGenRec 的 Beauty NDCG@10 是 0.0541，用户数和物品数与 Xu 相同。这些顶会论文卖的是「在这张留一表、这套抄来或重做的弱序列行上，生成式 ID 更高」。协同在码本或参数里。自回归生成离散码不是自连接。

同类做法若投 ACL，退稿风险是弱基线和指标横比。Xu 等在同一用户数、同一物品数上，全量交叉熵 SASRec 的 Beauty NDCG@10 是 0.0597，高于 TIGER 0.0384、EAGER 0.0525、IDGenRec 0.0541、OneRec-Think 0.0471。笔记写不能把「超过表内 SASRec」写成超过调好的序列模型。原 TIGER 的 Recall@10 0.0648 和 LETTER 重做的 0.0610 不要横比。历史截断（20 与 50）不对齐时，只保留方向。这一路也写不出「LLM 生成 ID 等于 LLM 写 SQL」。

### 3.2 LLM 做物品编码器或对齐

代表论文和已核实场合：LLM2Rec 与 NoteLLM-2 在 KDD 2025，LEARN 的版权页是 AAAI 2025。NoteLLM 是 WWW 2024 Companion，按研讨会，不升成 WWW 档案。HLLM 首页未印会议名。RecGPT 是技术报告。BEATS 在 SIGIR 2026，做法是把 LLM 生成的属性拼进商品文本再训双塔，笔记写检索结构没变。

笔记里能对上的贡献形态是：下游仍是 SASRec 或双塔，涨幅来自文本向量或文本里多出来的属性。LLM2Rec 写明检验的是高于同表最好的嵌入基线；Goodreads 上相对增益 1.45%；没有从零训练的纯 ID SASRec，没有 ItemKNN，没有 EASE。LEARN 在 Arts 上 Recall@10 高于 RecFormer，NDCG@10 的改进栏是「–」。NoteLLM-2 仍是笔记对笔记。BEATS 的对照失败应是「列上有值、稠密检索仍违反该列」，不是「目录里根本没有这一列」。

同类做法若投 ACL：用 2018 年那一档 SASRec 或线上旧 SentenceBERT 当强基线，就是弱基线。HLLM 的格子按百分数口径读，不能和 TIGER 的 0–1 Recall 横比；线上「关键指标」+0.705% 没有指标名。NoteLLM 相对 SentenceBERT 的点击率 +16.20%，相对 RepLLaMA 的 Recall@100 只高 0.39 个点；NoteLLM-2 的线上对照已经是 NoteLLM，两篇的线上百分数不能相加，也不能用来证明该用或不该用 SQL。产出是向量，召回仍是内积，SQL 表达不了这步投影。

### 3.3 属性 SQL / 工具调用

代表论文和已核实场合：InteRecAgent 首页未印会议名，已经让 LLM 写 SQL，表 5 用全库检索的 Recall@5 打分（Beauty 30.28，单位是百分数），提示禁止用 SQL 找相似物品，只许一张物品信息表，不许 `LIMIT`。TalkPlay-Tools 页眉是 Preprint，SQL 是单表布尔过滤。`07` 里 ProRetrieval、MACS 首页没有会议名。Malik 等在 CIKM 2024，任务是过滤 API 的 Exact Match，笔记写没有候选召回，也没有 SQL。EComAgentBench 是 EMNLP 2026 Industry Track，属性过滤只在调用者给的最多 10 个 id 里做子串，不计入档案顶会。

所以「模型写 SQL、执行后用推荐指标打分」在这批笔记里的最高已核实场合是未印会议，不是档案顶会。CIKM 2024 吃掉的是另一件事：自然语言落到品牌、内存、价格的过滤 schema。

笔记里能对上的形态是工具分工，不是新的协同算子。InteRecAgent 的协同走 ItemCF，排序 NDCG 是 1 个正例加 19 个随机负例。ProRetrieval 在 3,000 件自建商品上有 Hit@1，金标准是构造出来的单篇文档，只执行 SQL 的 Hit@1 0.650 低于 SQL 加文本的 0.752。MACS 的 LLM 写的是槽位，SQL 是确定性映射；140 条上的通过率不是公开全库 Recall。HyST 在 STaRK 的 76 条、3,335 件子集上做了 JSON 过滤后再向量检索，关系边被删掉。

同类做法若投 ACL：只做属性 `WHERE`，笔记写就是在复现 InteRecAgent 的工具。把 ItemKNN 或 Swing 写成自连接，审稿人会把它叫成 SQL 版近邻；空本身不是贡献。主指标若改成 Exact Match，就是在跟 Malik 等的 CIKM 2024 比，召回论文要另报执行后的候选集。执行准确率当主指标，对不上留出交互。HyST 的 Precision@1 0.9211 不能当成打过 STaRK 官方全库 BM25（Hit@1 44.94，Recall@20 53.77）。ProRetrieval 的 Hit 不能写成留出购买上的收益。

### 3.4 生成查询再搜索（BM25 或 Bing）

代表论文和已核实场合：GPT4Rec 的 PDF 不是档案版，查询是标题，引擎是 BM25，基线有 BERT4Rec，没有 SASRec。WebReco 是 CIKM 2024 IRS，EARL 是 RecSys 2024 EARL，笔记都写明不是档案；KDD 2025 档案版不在目录里，不用它的摘要填表。KAR 没有会议名，扩展后的引擎仍是 BM25。

笔记里能对上的形态是：模型写多条查询，另一个引擎执行。GPT4Rec 在它自己的用户级划分、序列截到 15 的表里，40 条查询的 Recall@40 是 0.2040，高于 BERT4Rec 的 0.1161。Q′ 两行相同：GPT-4 的线上 CTR +0.89%、RecoDCG@5 +0.760；Mistral-7B 是 +1.71% 和 +0.762。只算一次观察。查询是网页，不是用户–物品自连接。

同类做法若投 ACL：研讨会 CTR 不能当公开库上某个召回算子的证据，也不能和 Recall@K 横比。GPT4Rec 的 Beauty 规模是 22,254 / 11,778，不是 22,363 / 12,101，Recall@K 不能和留一全库的 0.06 横比。SQL 的全文检索可以模仿 BM25，那不是协同自连接，也没有硬谓词满足率。网格把这一格标成假空。

### 3.5 过滤向量搜索

代表论文和已核实场合：SIEVE 的会议版是 PVLDB 2025，Lim 等是 PVLDB 2026，都算档案期刊。ACORN 是 SIGMOD 2024，不在本分档档案名单，不升格。HyST 未印会议名。

笔记里能对上的形态是索引：带谓词时如何找回真正的 top-k 向量近邻，以及吞吐。SIEVE 的后检索过滤先搜大约 \(k/\mathrm{sel}\)，不够再翻倍。低选择率上 SIEVE 的近邻 recall 可以到 0.99 以上，ACORN-γ 大约停在 0.95。Lim 等的原句是高难度负载上多数策略的 recall 急剧下降，often below 0.2，并与选择率大约 0.1% 或更低一致。0.2 是对图的概括。ACORN 的方向与「向量约束失败」相反：谓词可以留在向量搜索里面。

同类做法若投 ACL：把近邻 recall 写成推荐 Hit 或 NDCG，就是指标横比。把 Lim 的 0.2 写成「推荐约束下 Hit 低于 0.2，所以该换成 SQL」，笔记写不成立；数据集是 SIFT、GIST 上的合成或半真实属性。SQL 的 `WHERE` 在同一谓词上精确，这是机制。这批 PDF 没有测过它在留出交互上的推荐涨幅。

### 3.6 复现与强基线批判

代表论文和已核实场合：Ferrari Dacrema 等的会议稿是 RecSys 2019，期刊扩展是 TOIS 2021，两篇不并。Benigni 等是 TORS 2026。Hidasi 与 Czapp 是 RecSys 2023，本报告只采用问题界定，不把未打开的实验表写成中稿论据。Zhang 的 RecSys 2026 短文同样只到摘要页。

笔记里能对上的形态是：多数当时的神经方法在可复现的矩阵式 top-n 上没有稳定胜过调过的近邻或线性模型。RecSys 2019 的 Netflix 表里，ItemKNN CF 的 REC@20 / REC@50 / NDCG@100 是 0.2088 / 0.3386 / 0.3086，SLIM 更高，Mult-VAE 的 Recall@20 仍高于 ItemKNN。TOIS 要同时引用 11/12 和 1/12。Benigni 等在 Amazon-Books（clean）上，余弦加收缩的 ItemKNN 高于表内 DiffRec 变体；EASE 整行是空的，因为内存超过 64 GB。Hidasi 写的四类缺陷是数据与任务不配、在重度预处理的数据上作一般结论、时间泄漏、负采样。Zhang 的摘要写固定候选和各自召回会选出不同的第一名。

这些论文能进 RecSys 档案和 TOIS / TORS，对得上的论点是「进步声明要打过调过的简单基线」，协议是评分矩阵 top-n，不是 Beauty 留一，也没有自然语言。

同类做法若投 ACL：主表若只放一个没调收缩的近邻，或把 STAR 表里 Hits@10 为 0.007 的 top-10 UserKNN 当成 ItemKNN 很弱，就是弱基线。把 EASE 或 SLIM 的胜负说成 SQL 自连接的胜负，笔记写不成立：自连接写得出共现、余弦和收缩，写不出 EASE，也写不出 SLIM。用 Benigni 等证明「SQL 版 ItemKNN 没前途」，方向反了。无约束下一物品上缺少对照表，既不能宣称 SQL 赢，也不能把「第一篇」当贡献。

### 3.7 全量交叉熵序列模型

代表论文：Xu 等，arXiv:2408.14238，首页无会议。档次是仅预印本。不进入档案顶会的篇数。

笔记里能对上的论点是损失，不是会议身份：传统模型多用 BCE 或 BPR，LLM 推荐器用全体物品上的交叉熵。两边都用交叉熵时，SASRec 反过来超过表内的 LLM 推荐器。Beauty 的 NDCG@10：BPR 0.0374，BCE 0.0353，全量交叉熵 0.0597。Yelp 的全量交叉熵 NDCG@10 是 0.0415。表里没有 ItemKNN，没有 EASE。

这一档没有「中在顶会」的句子可以写。它在选题里的用处是先导的序列臂必须用这一档。不能引用 ItemKNN 或 SQL 自连接打不过它，因为这张全库排序表不在这批 PDF 里。

同类做法若投 ACL：把 TIGER 表里 NDCG@10 为 0.0318 的 SASRec 写成调好的序列模型，就是弱基线。把不同论文的 NDCG 横比成配对实验，笔记只允许写成方向。SQL 表达不了自注意力。无约束下一物品不要当主表。

### 3.8 关系库推荐

代表论文和已核实场合：RelBench v1 会议版是 NeurIPS 2024 Datasets and Benchmarks。RelAgent 是 NeurIPS 2026。ReFuGe 是 WWW 2026 短文。RelBench v2 是 ICLR 2026 DATA-FM workshop，按研讨会。ContextGNN、Fey、Wydmuch 的 PDF 没有会议页眉。Fey 被会议版引成 ICML 2024 position paper，不据此升格。

笔记里能对上的形态是：输入是实体和种子时间，标签是未来窗口里的实体，评测用 MAP。H&M 购买上，会议版测试的历史访问是 0.89（百分数刻度），两层 GraphSAGE 0.80，ID-GNN 2.81。高于历史访问的是 ID-GNN、NBFNet 和 ContextGNN，不是任意一个 GNN。MultiVAE 0.28、NGCF 0.75、两层 GraphSAGE 0.80 都没有超过 0.89。RelAgent 和 ReFuGe 的 SQL 写出的是特征，再接树模型；实验是分类和回归，H&M 列是 churn，不是 `user-item-purchase`。没有一篇把用户问句解析成 SQL，再把结果集当成购买 top-K。

v1 能出现在 NeurIPS 的 Datasets and Benchmarks，对得上的是关系库上的任务定义和基线表，不是语言贡献。RelAgent、ReFuGe 能出现在 NeurIPS 2026 和 WWW 2026 短文，对得上的是智能体搜索特征，对不上推荐 top-K。

同类做法若投 ACL：14 个任务各一句模板、没有词汇变化，笔记写 ACL 审稿人会同意把它逐出语言主实验。手写共现是漏掉的经典基线，审稿人会把它叫成 SQL 版近邻，所以只做健全性检查：先对照历史访问 0.89，超过历史访问不等于接近 ContextGNN 的 2.93。历史访问数的是历史标签列表，不是交易表对自身的连接，不能和 02 的 ItemKNN 横比。把「GNN 打败 SQL」写成结论，笔记已经杀掉。

### 3.9 文本转 SQL 的域内执行准确率或拒答

代表论文和已核实场合：执行准确率这一路里，BookSQL、SUQL 在 NAACL 2024，Wretblad 在 ACL 2024 短文，H-STAR 与 FLEX 在 NAACL 2025，SQLForge 在 ACL 2025 Findings，Arctic-Text2SQL-R1 在 ACL 2026 Findings，SM3 在 NeurIPS 2024 Datasets and Benchmarks，EHRSQL 在 NeurIPS 2022 Datasets and Benchmarks，DIN-SQL 在 NeurIPS 2023，ScienceBenchmark 在 PVLDB 2023。拒答这一路里，EHRSQL 与 TrustSQL、Query Carefully 分占 NeurIPS 2022 和未印会议；EHRSQL 2024 是 ClinicalNLP 2024；OMOP 是 ClinicalNLP @ LREC 2026。ClinicalNLP、ICLR、CIDR、COLM 不计入档案顶会。FinSQL、FINCH、OmniSQL、BlendSQL、Jin 等、DAIL-SQL、MAC-SQL 是仅预印本。CHESS 场合未统一。

`06_创新点总表.md` 写明：被接收的文章另外卖的是换库之后系统变差、第二种查询语言、schema 里没有的统计惯例、拒答加惩罚，或者执行准确率本身会把名次排错。窗口 01 写明这 22 篇全文检索不到推荐的 NDCG、Hit、Recall；FinSQL 表 7 的 recall 是表和列。OMOP 上 LoRA 的测试执行准确率 93.55 可以和很差的可靠性分同时出现，高分不构成新贡献。SUQL 的 93.8% / 90.3% 是最多返回 3 家的人工精度。TAG 的 0.55 是 80 道改写题上的手写精确匹配，不是 Recall。

同类做法若投 ACL：再报一个域内执行准确率，或把拒答、不可答令牌、错答更贵的可靠性分写成主创新，窗口 01 写这两格已经挤满。执行准确率、作者判定的约束满足、可靠性分，不能写成 Recall、NDCG 或 Hit。审稿人会当成已经做过的三件事，笔记写的是：模板填槽加一张相对 Spider 或 BIRD 的下跌表、拒答可靠性分、把主指标改成作者看约束满不满足。标签若由一条 SQL 算出，Recall 会退回执行匹配。生成器可以借用 Arctic-7B 或 OmniSQL-7B，借用的是检查点；Arctic 表里的 68.9 是 BIRD 开发集，不是测试集。

### 3.10 混合检索与指标

代表论文和已核实场合：QUEST 在 ACL 2023，FollowIR 在 NAACL 2025，HybGRAG 在 ACL 2025，STaRK 在 NeurIPS 2024 Datasets and Benchmarks，BLaIR 在 ACL 2026 长文。BRIGHT、mFAR、LIMIT 在 ICLR，不升格。ReproRAG 的页眉是 Workshop ’25，按研讨会。AvaTaR、MoR、Text2VectorSQL、NevIR、ExcluIR、SPARK、Atil、PCN-Rec 未印会议名。

笔记里能对上的形态是检索指标和分工，不是用 SQL 换掉向量。QUEST 的双编码器平均 Recall@100 是 0.476，高于 BM25 的 0.197；0.142 是 MRecall@100，不是宏召回。STaRK 表 6 的 BM25 是 Hit@1 44.94、Hit@5 67.42、Recall@20 53.77、MRR 55.30。SPARK 的合成 Amazon Recall@20 是 53.95，和 BM25 的 53.77 打平，工具仍是 HNSW 加 Cypher，空结果回退 BM25。HybGRAG 没有 Amazon 分割。BLaIR 的 Amazon-C4 有嵌入的 NDCG@100 0.1856，论文没有 SQL 行。FollowIR 的失败被作者写成不习惯长指令。Faithful CoT 的忠实等于答案由求解器执行符号链，翻译阶段不在保证里。

窗口 04 写：没有任何一篇是「只执行 Cypher 或 SQL、不再做向量或 BM25」，并且在 STaRK-Amazon 上打过 BM25。还能写、但这批 PDF 没测过的，是关系片段写成 SQL、数据库取超集、BM25 或小编码器在超集里排序。

同类做法若投 ACL：指标横比会被打回。mFAR 表 1 的 BM25（0.483 / 0.584 / 0.589）不是 STaRK 表 6。NevIR、ExcluIR、NumConQ、LIMIT 的失败发生在自由文本、改写句，或 46 篇文档的两两组合，不是已经落到列上的谓词；小集合上 BM25 的 Recall@2 是 97.8，不能写成嵌入搞不定推荐式查询。Text2VectorSQL 只有 ClickHouse 上 UniVectorSQL-7B 从 0.6 到 0.4 这一对，WHERE 没有「丢掉 30%」这个数。把「返回行等于 SQL 结果」写成忠实解释，笔记写审稿人会要用户研究。Atil 的 15% 和 70% 不是这篇 SQL 生成器已经测过的晃动。PCN-Rec 一次生成的 PassRate 0.000 不能写成大模型在约束推荐上的普遍通过率。

### 3.11 网格里另有、但不单独立成热度的几格

- **LLM 凭记忆生成标题**：RecBench+ 页眉是 WSDM ’26，不在档案名单里。表 2 的 Precision 0.308、CMR 0.714 是没看目录的生成分数，不进检索主表。REGEN 未印会议名，叙事生成时看过目标。这一格不能当成 ACL 上已经中稿的检索贡献。
- **会话重复**：RepeatNet 带 AAAI 2019 版权行。DIGINETICA 上 RepeatNet 的 Recall@20 是 47.79，同表 NARM 是 49.70。绝对 Recall 是会话尺度，不能和 Amazon 留一横比。先导里若报重复物品，对照包括「只做集合过滤」的 SQL。
- **约束放松的定义**：Jannach 与 Liegl 的会议全称未在打开的前两页印出，不升格。MACS 的放松是另一套产品规则。两篇不要写成同一个算法。
- **评测协议**：Zhang 的摘要支持「比较整条流水线时报告各自候选上的效用」。这和总览「不要用固定候选掩盖第一阶段」同向。摘要没有讨论 SQL，不提供新的主指标。

---

## 4. 年份趋势

趋势只描述这 94 篇已读论文。某一年没有的类型，就写这批笔记里没有。不补「当年全领域最热」。2023 年以前的 5 篇不写进四年热度，单列在表下，避免把 2019–2022 的复现文献说成 2023 年的热度。CHESS 只计在 2024 的「场合未统一」，不在 2025 再计一篇。

| 年份 | 篇数 | 档案顶会 | 档案期刊 | 研讨会 | 仅预印本 | 名单外已点名 | 技术报告 | 未统一 | 这批笔记里实际出现的创新点 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 2023 | 14 | 4 | 1 | 0 | 7 | 2 | 0 | 0 | 语义 ID 同时出现在 NeurIPS（TIGER）和未印会议（LC-Rec）。文本转 SQL 出现在 NeurIPS（DIN-SQL）、PVLDB（ScienceBenchmark）、ICLR（Binder，不升格）和未印会议（DAIL-SQL、MAC-SQL）。混合检索的 QUEST 在 ACL；自由文本否定的 NevIR 未印会议。属性 SQL 的 InteRecAgent、BM25 多查询的 GPT4Rec 都未印成档案。关系库框架 Fey 的 PDF 无页眉。RecSys 上有离线评测缺陷的问题界定（Hidasi，未读全文表） |
| 2024 | 28 | 10 | 0 | 3 | 12 | 2 | 0 | 1 | 语义 ID 出现在 KDD、SIGIR、CIKM 档案（EAGER、IDGenRec、LETTER）。域内 text-to-SQL 出现在 NAACL、ACL 短文、NeurIPS Datasets and Benchmarks；FinSQL、TrustSQL、BlendSQL 仍是未印会议。STaRK 与 RelBench v1 同在 NeurIPS Datasets and Benchmarks。CIKM 档案上的 Malik 是过滤 schema，不是召回。生成查询的线上 CTR 只在 IRS 与 EARL 两个研讨会。全量交叉熵（Xu）、HLLM、STAR、ContextGNN、Wydmuch 都是未印会议。ACORN 在 SIGMOD，不升格。CHESS 场合未统一 |
| 2025 | 24 | 8 | 1 | 1 | 9 | 4 | 1 | 0 | LLM 物品编码器出现在 KDD 和 AAAI（LLM2Rec、LEARN）；笔记对笔记的多模态出现在 KDD（NoteLLM-2），上一篇仍是 2024 Companion。文本转 SQL 的执行判断出现在 NAACL（H-STAR、FLEX），合成配方出现在 ACL Findings（SQLForge）；OmniSQL、FINCH、Query Carefully 未印会议。过滤向量的近邻 recall 出现在 PVLDB（SIEVE）。混合检索出现在 ACL、NAACL；ICLR 上的 BRIGHT、mFAR 不升格。HyST、OneRec-Think、MoR、Text2VectorSQL 未印会议。RecGPT 是技术报告。这批笔记里 2025 没有新的档案顶会协同 SQL |
| 2026 | 23 | 6 | 2 | 1 | 8 | 6 | 0 | 0 | 最接近「模型写 SQL、用 Hit 打分」的 ProRetrieval，以及槽位到 SQL 的 MACS，首页都没有会议名。属性写进双塔的 BEATS 在 SIGIR，不经过 SQL。关系库智能体出现在 NeurIPS（RelAgent）和 WWW 短文（ReFuGe），实验不是购买 top-K；v2 是 DATA-FM workshop。强基线复现出现在 TORS（Benigni）。过滤 ANN 的难度句子出现在 PVLDB（Lim）。ACL 档案上有 Arctic 的 Findings（奖励只看执行）和 BLaIR 长文（稠密检索，无 SQL 行）。RecBench+ 的页眉是 WSDM，EComAgentBench 是 EMNLP Industry Track，LIMIT 是 ICLR，都不升格 |

四年合计 14 + 28 + 24 + 23 = 89。另有 5 篇在 2023 年以前：RepeatNet（AAAI 2019 版权行）、Ferrari 等 RecSys 2019、Ferrari 等 TOIS 2021、EHRSQL（NeurIPS 2022 Datasets and Benchmarks）、Jannach 与 Liegl（会议全称未核实，文件名记到 2006）。5 + 89 = 94。

这批已读论文里，四年都没有的情况：

- 2023：没有研讨会稿，没有档案期刊上的过滤向量论文，没有技术报告。
- 2024：没有档案期刊。过滤向量这一年只看到 SIGMOD 上的 ACORN，不计入档案期刊或档案顶会。
- 2025：没有「模型写出协同自连接并用推荐 Recall 打分」的档案顶会论文。
- 2026：没有技术报告。ProRetrieval 与 MACS 没有会议名。

跨年能看出来的，只限这批论文：语义 ID 的档案顶会论文集中在 2023–2024；LLM 物品编码器的档案顶会论文出现在 2025，属性拼进双塔的一篇在 2026 的 SIGIR；域内执行准确率和拒答从 2022 的 EHRSQL 一直写到 2026 的 ACL Findings，档次里既有档案顶会，也有大量未印会议；「写 SQL 当推荐召回」的近邻在 2023（InteRecAgent）、2025（HyST）、2026（ProRetrieval、MACS）都停在未印会议。不能把这个时间顺序写成全领域的热度排名。

---

## 5. 四个维度

### 5.1 场合档次 × 论文数

口径见文首。名单外和未核实单列，避免把 ICLR、SIGMOD、WSDM、Industry Track 算进档案顶会，也避免把它们涂成「没有发表」。

| 档次 | 论文数 | 占这 94 篇 | 读法 |
|---|---:|---:|---|
| 档案顶会 | 31 | 31/94 | 含 NeurIPS Datasets and Benchmarks、ACL/NAACL Findings、ACL 与 WWW 与 RecSys 短文。其中 2 篇只核到摘要或问题界定 |
| 档案期刊 | 5 | 5/94 | PVLDB 3、TOIS 1、TORS 1 |
| 研讨会 | 5 | 5/94 | Companion 1、IRS 1、EARL 1、Workshop ’25 1、DATA-FM workshop 1 |
| 仅预印本 | 36 | 36/94 | 含首页未印、占位页眉、笔记写不是档案版。不进入顶会篇数 |
| 技术报告 | 1 | 1/94 | RecGPT |
| 名单外已点名 | 14 | 14/94 | 有会议名，不在本分档档案名单 |
| 场合未统一或未核实 | 2 | 2/94 | CHESS、Jannach 与 Liegl |

31 + 5 + 5 + 36 + 1 + 14 + 2 = 94。

大纲清单单独看：档案顶会 25，档案期刊 5，研讨会 5，仅预印本 29，技术报告 1，名单外已点名 14。这 25 篇档案顶会里，没有一篇是「大模型写出协同 SQL 自连接，数据库执行，再用留出交互的 Recall 或 NDCG 打分」。

### 5.2 创新点类型 × 最高已核实场合

「最高」指本分档里更高的一档，同一档里的会议不排先后。未印会议即使论点更近，也不把它写成顶会。

| 创新点类型 | 这批笔记里的最高已核实场合 | 没有升上去的近邻 |
|---|---|---|
| 语义 ID 生成式检索 | 档案顶会并列：NeurIPS 2023、KDD 2024、SIGIR 2024、CIKM 2024 | LC-Rec、OneRec-Think 首页未印 |
| LLM 做物品编码器或对齐 | 档案顶会并列：KDD 2025、AAAI 2025、SIGIR 2026（BEATS，属性拼进文本） | NoteLLM 只到 WWW 2024 Companion；HLLM 未印；RecGPT 是技术报告 |
| 属性 SQL / 工具调用 | 未印会议（InteRecAgent、TalkPlay-Tools、ProRetrieval、MACS）。CIKM 2024 是过滤 schema，不是 SQL 召回 | 不要把 CIKM 2024 的 Exact Match 写成 SQL 召回已经中了档案顶会 |
| 生成查询再搜索（BM25 或 Bing） | 研讨会：IRS 2024、EARL 2024。KAR 未印会议，引擎仍是 BM25 | GPT4Rec 笔记写不是档案版。KDD 2025 档案版不在目录 |
| 过滤向量搜索 | 档案期刊：PVLDB 2025（SIEVE）、PVLDB 2026（Lim） | ACORN 是 SIGMOD 2024，不升格。HyST 未印会议 |
| 复现与强基线批判 | 档案顶会 RecSys 2019；档案期刊 TOIS 2021、TORS 2026 | 协议是矩阵式 top-n。Xu 的全量交叉熵不在这些表里 |
| 全量交叉熵序列模型 | 仅预印本（Xu，首页无会议） | 不能把 TIGER 一系「超过 SASRec」写成这一档已经在顶会被打赢 |
| 关系库推荐 | 档案顶会：NeurIPS 2024 Datasets and Benchmarks；NeurIPS 2026 与 WWW 2026 短文的实验不是购买 top-K | v2 是 workshop。ContextGNN 未印会议。Fey 的 ICML 说法是转引 |
| 文本转 SQL 的域内执行准确率或拒答 | 档案顶会：NAACL、ACL 短文与 Findings、NeurIPS 及 NeurIPS Datasets and Benchmarks。档案期刊：PVLDB 2023 | 挤满的是执行准确率和拒答。22 篇窗口没有推荐 Recall。ClinicalNLP、ICLR、CIDR、COLM 不升格 |
| 混合检索与指标 | 档案顶会：ACL 2023、NAACL 2025、ACL 2025、NeurIPS 2024（STaRK）、ACL 2026（BLaIR，无 SQL 行） | ICLR 上的 BRIGHT、mFAR、LIMIT 不升格。没有任何一篇只执行 SQL 打过 STaRK 的 BM25 |

### 5.3 任务 × 是否和 ACL 语言贡献同一条路

「同一条路」按总览和窗口 02：语言主实验要有自然语言，主指标是留出交互或可核验属性上的召回，而且不是再报域内执行准确率。协同自连接若没有问句里的硬谓词，笔记把它逐出语言主贡献。

| 任务 | 和 ACL 语言贡献是否同一条路 | 笔记依据 |
|---|---|---|
| 无约束下一物品 | 否。移出主表 | 写出来的自连接是 ItemKNN 或 Swing。全量交叉熵 SASRec、EASE 与 SQL 的同表不存在。AgentRecBench 的名单已经切成 20 选 1 |
| 对话工具 | 否。问句在，但只做属性 WHERE 是已有工具 | InteRecAgent 禁止用 SQL 找相似物品。MACS 写的是槽位。TalkPlay 的单表布尔 SQL 不替换 STaRK |
| 笔记对笔记 | 否 | NoteLLM / NoteLLM-2 的测试池是笔记，没有用户–物品自连接。线上点击不能证明协同 SQL 没有空间 |
| 过滤向量 | 否 | SIEVE 与 Lim 的 recall 是向量近邻。没有用户问句上的语言贡献，也没有推荐 NDCG |
| 矩阵 top-n 复现 | 否 | 评分矩阵，没有自然语言。近邻是强基线，这条证据用来规定平凡臂，本身不是语言论文 |
| 关系库 | 否 | 输入是实体和种子时间。14 句模板不是语言贡献。RelAgent、ReFuGe 的 SQL 不出购买 top-K |
| 文本转 SQL | 只在一格上接得上 | 再报域内执行准确率或拒答，窗口 01 写已经挤满。接得上的是：在用户、物品、交互表上写 SQL，执行结果当候选，用留出交互的 Recall 或 NDCG 打分，并单列错误 SQL 被执行的代价。相关集不能是这条 SQL 自己的结果 |

### 5.4 对本选题的含义

| 已经吃到的档次 | 吃满的创新点 | 这批笔记留给 ACL 主会的空格 |
|---|---|---|
| 档案顶会 | 弱 SASRec 上的语义 ID；LLM 物品编码器；域内执行准确率与拒答；无问句的关系库任务形状；过滤 schema 的 Exact Match（CIKM 2024）；仍带 BM25 或稠密检索器的半结构化检索 | 这些格子再投一篇同类主创新，对得上的退稿理由就是弱基线、执行准确率当主指标、或把表内涨幅写成打赢 Xu 的 0.0597 |
| 档案期刊 | 过滤向量的近邻 recall；调过的 ItemKNN / 线性模型是强基线 | 近邻 recall 不能写成推荐 Hit。平凡臂必须是余弦加收缩的 ItemKNN，否则就是这批复现论文已经打过的弱基线 |
| 研讨会 | 网页查询交给 Bing 的线上 CTR | 研讨会 CTR 不能当公开库证据。Q′ 只算一次，而且不是协同 SQL |
| 仅预印本 | InteRecAgent 的属性 SQL；Xu 的全量交叉熵；HyST 的子集 JSON 过滤；ProRetrieval 的自建商品 SQL+Hit；MACS 的槽位 SQL | 不计入顶会篇数，但选题不能写成「还没有人做」。官方全库、留出交互、带谓词的三臂，这些预印本没有占住 |

直接建议：ACL 2027 这一选题若还要投主会，贡献句用 `window-02.md` 已经定下的那句，也就是网格里「主表放带谓词的召回」。同一组已经落到列或边上的谓词下，比较精确 SQL、后过滤的全量交叉熵 SASRec、以及大约按 \(1/\mathrm{sel}\) 多取的向量，看谁改变可行集上的 Recall、NDCG 和约束满足率。模型写 SQL 放在手写查询已经改变可行集之后。无约束下一物品上的 SQL ItemKNN 不作为主句。

STaRK 上的关系片段加文档排序仍是另一张表，要打的全库数字仍是表 6 的 BM25：Hit@1 44.94，Hit@5 67.42，Recall@20 53.77，MRR 55.30。`07` 已经把「第一次做结构化商品过滤」划掉。两张表不要合成「SQL 替换向量检索」。手写共现对 H&M 历史访问只做健全性检查。再报一个 Spider 或 BIRD 上的执行准确率，不作为这篇的主创新。
