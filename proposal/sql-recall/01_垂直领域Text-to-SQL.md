# 垂直领域 Text-to-SQL，以及 SQL 作为下游组件

> 2026-11-11 核对。数字来自当天打开的论文、榜单或官方代码。
> 总览和先导实验在 [00_总览](00_总览.md)。

顾问说这个方向偏应用、常被当成练手。核对后的情况与此一致，但被接收的文章都多卖了一样东西。

| 论文 | 场合 | 多卖的那一点 | 规模与做法 | 结果 |
|---|---|---|---|---|
| [ScienceBenchmark](https://www.vldb.org/pvldb/vol17/p685-stockinger.pdf) | PVLDB 2024 | Spider 上 82% 以上的系统，到真实科学库掉到 25%–60% | 经费、天文、肿瘤三个库；每库 100 条专家种子。SQL 专家和领域专家写种子，GPT-3 把 SQL 翻成问句 | T5-Large 在 OncoMX 上 56%；GPT-3.5 在 CORDIS 上最高 60%，SDSS 上 33% |
| [SM3-Text-to-Query](https://proceedings.neurips.cc/paper_files/paper/2024/file/a182a8e6ebc91728b6e6b6382c9f7b1e-Paper-Datasets_and_Benchmarks_Track.pdf) | NeurIPS 2024 D&B | 同一批问题写成 SQL、MQL、Cypher、SPARQL，变量是数据模型 | 408 个人工模板扩到每种语言 1 万对。两家医院，一年以上 | 带 schema 的零样本 SQL 最高 47.05%；SPARQL 零样本最高 3.3% |
| [BiomedSQL](https://arxiv.org/html/2505.20321v6) | 仅 arXiv，未见会议版 | 答案依赖 schema 里没有的统计惯例（全基因组阈值、试验分期） | 40 条专家问题，模板扩到 6.8 万。评测用 546 条 | Gemini-3-Pro 58.1%；他们的 agent 62.6%；两位分析员在 20 条子集上平均 90% |
| [BookSQL](https://aclanthology.org/2024.naacl-long.28/) | NAACL 2024 长文 | 会计库，Spider 类数据没覆盖 | 约 7.8 万到 10 万对，单库、约 100 万行 | GPT-4 仍有明显差距 |
| [FinSQL / BULL](https://doi.org/10.1145/3626246.3653375) | SIGMOD 2024 | 金融宽表；跨库 few-shot | 恒生业务库，4,966 对、3 个库 | 跨库 few-shot 最高提升 36.64% |
| [FINCH](https://arxiv.org/abs/2510.01887) | 仅 arXiv | 把 BIRD、Spider、FinSQL、BookSQL 收成 33 个金融库 | 75,725 对 | 合并已有资源，不是新的医院式采集 |
| [EHRSQL](https://proceedings.neurips.cc/paper_files/paper/2022/file/643e347250cf9289e5a2a6c1ed5ee42e-Paper-Datasets_and_Benchmarks.pdf) | NeurIPS 2022 D&B | 222 名医务人员的真实问题；时间表达式；不可回答问题 | 1,742 条原话收成 230 个模板，约 2.44 万实例 | 后续是 ClinicalNLP 2024 共享任务和 TrustSQL |
| [OMOP text-to-SQL](https://aclanthology.org/2026.clinicalnlp-1.40/) | ClinicalNLP 2026 | 安全约定：只输出一条 SQL，否则输出拒答 | 75 个模板、6,690 条改写，合成库 | LoRA Llama-3-8B 执行准确率 93.55%。数字高，是因为库是合成的、概念已归一 |
| [Query Carefully](https://arxiv.org/html/2512.21345) | 仅 arXiv | 生物医学上的拒答 | OncoMX 上 80 条不可回答问题 | Llama-3.3-70B 检测不可回答 0.8；缺值类只有 0.5，列歧义只有 0.3 |

法律案例、法规、合同上的自然语言到 SQL 或 SPARQL 数据集，这一路没有找到。最接近的是 SBBD 2026 的审计系统：SQL 负责可审计的计数、过滤和排序，检索负责解释。结构化问题的 Answer@Exec 从纯 RAG 的 0.09 到混合系统的 0.98。数据未按 Spider 的方式公开。

被接收的文章反复用的切口：

- 一个已知强的系统换到新库上大幅下跌。只说「我们也在某领域做了 Text-to-SQL」并且域内分数很高，站不住，除非另卖拒答或安全约定。
- schema 里没有的东西：统计惯例、不可回答、歧义、第二种查询语言。
- 指标能惩罚「说得很顺但是错的」。BIRD 已到 80% 出头、Spider 2.0-Snow 已到 96% 之后，原始执行准确率不再是卖点。
- 造数据的标准工量是几十到几百个专家模板，再程序填槽或让模型改写。一年以上的采集只出现在有领域科学家参与的科学库和医院数据上。

## 2. SQL 是流水线的一段、指标是下游任务（已核对）

没有一篇用推荐的 Recall、NDCG 或 Hit 给生成的 SQL 打分。下游指标是问答准确率、对话状态准确率或抽取 F1。

| 论文 | SQL 的角色 | 下游数字 | 对这篇的用处 |
|---|---|---|---|
| [Binder](https://arxiv.org/pdf/2210.02875)，ICLR 2023 | SQL 或 Python 里嵌模型调用 | WikiTQ 测试 64.6，对比端到端 Codex 48.7 | 说明「程序加模型」能处理纯 SQL 写不出的问题 |
| [SUQL](https://aclanthology.org/2024.findings-naacl.283.pdf)，NAACL 2024 Findings | SQL 加对自由文本列的 `SUMMARY` 和 `ANSWER` | 餐馆搜索：每条约束都满足的对话轮 90.3%，对照把表线性化后塞进模型的 63.4%。单轮 93.8% | 公开文献里最接近「结构化约束下找物品」。语料是 Yelp 1,828 家餐馆，不是推荐 |
| [TAG](https://arxiv.org/html/2408.14717)，CIDR 2025 | 先合成查询并执行，再由模型作答 | 80 道改写的 BIRD 题上，手写流程约 55%；Text-to-SQL、RAG、RAG 加重排都不超过 20% | 论证执行准确率覆盖不了真问题。手写流程是上界，不是可复用系统 |
| [H-STAR](https://aclanthology.org/2025.naacl-long.445/)，NAACL 2025 | 定量和逻辑题才走 SQL | WikiTQ 68.85（GPT-3.5-turbo） | 模型按题型在文本和 SQL 之间分流 |
| [BlendSQL](https://arxiv.org/html/2402.17882)，未见会议版 | SQL 方言里的函数回调模型 | HybridQA 开发集 52.89 | 同一套代数覆盖表和文本 |
| SBBD 2026 审计系统 | 只读 SQL 与检索并列，SQL 失败就退回检索 | 见上一节 | 「硬操作走 SQL、其余走检索」有审计场景的数字 |

和召回阶段对得上的是 SUQL 和 TAG：SQL 的结果是中间表，论文报告的是用户看到的答案对不对。两篇都认为 Spider 式的执行准确率漏掉了人真正要问的问题。两篇都没有排序器。

## 3. 先导实验可以用的 SQL 生成器（2026-11-11 榜单）

榜单页面：[BIRD](https://bird-bench.github.io/)，[Spider 2.0](https://spider2-sql.github.io/)。

| 用途 | 选择 | 数字 | 备注 |
|---|---|---|---|
| 本地，单张 5090 | [Arctic-Text2SQL-R1-7B](https://huggingface.co/Snowflake/Arctic-Text2SQL-R1-7B) 或 [OmniSQL-7B](https://huggingface.co/seeklhy/OmniSQL-7B) | Arctic-7B：BIRD 测试 68.5，Spider 测试 88.8，Spider 2.0-SQLite 15.6。OmniSQL-7B：BIRD 测试 67.97 | Arctic 从 OmniSQL 出发，用执行对错做强化学习。论文是 [ACL 2026 Findings](https://aclanthology.org/2026.findings-acl.1345.pdf) |
| API 对照 | 当时的前沿模型，给 schema，允许多次执行 | BIRD 上 GPT-5.5 基线 72.55（2026-04-28，带 oracle knowledge，不是纯零样本）。Spider 2.0-Snow 上 Spider-Agent + GPT-4o 只有 12.98，DIN-SQL + GPT-4o 是 0 | 不要用 2023 年的 DIN-SQL 当强基线 |
| 不追 | BIRD 榜首 AskData 83.40（2026-10-22，闭源）；Spider 2.0-Snow 榜首 96.70 | 人类在 BIRD 上是 92.96 | 超过榜首是另一篇论文，不是这篇的先导实验 |

Spider 2.0（[ICLR 2025](https://arxiv.org/abs/2411.07763)）换成了企业库，列数平均 812，金 SQL 平均 144 个 token，智能体还要读方言文档和项目代码。当时 o1-preview 智能体 21.3%，同一类系统在 Spider 1.0 上 91.2%、BIRD 上 73.0%。Snow 子集已经接近天花板，Lite 和 DBT 还没有。

## 4. 为什么不能把「SQL 写对了」当主指标（已核对）

- [FLEX](https://aclanthology.org/2025.naacl-long.228.pdf)（NAACL 2025）：执行准确率相对专家既高估也低估，换成更接近专家的评判后系统排名会变。
- [Jin 等，arXiv 2601.08778](https://arxiv.org/html/2601.08778)：BIRD Mini-Dev 标注错误率 52.8%，Spider 2.0-Snow 公开金标 121 条里 62.8% 有错。修正一个 BIRD 开发子集后，16 个可复现系统的相对执行准确率变化在 −7% 到 +31%，排名最多动 9 位。脏子集上的排名和全开发集相关（Spearman 0.85），和修正后的子集不相关（0.32）。
- [TS-SQL](https://aclanthology.org/2025.findings-emnlp.156.pdf)（EMNLP 2025 Findings）另标出 Spider 开发集 12.67% 的金 SQL 是错的。
- [ACL 2024 短文](https://aclanthology.org/2024.acl-short.34/) 早先就报告过 BIRD 的问句和金 SQL 有噪声，修正后零样本超过了当时的提示方法。
- 一条错误 SQL 可以在某一个数据库快照上返回和金标一样的表。推荐这边的对应风险是：在一份 MovieLens 快照上「返回了正确物品」的 SQL，换一个时间切分就错，执行匹配看不出来。留出交互上的 Recall 和 NDCG 避开这个问题。
