# 01 Text-to-SQL

日期：2026-11-11。本窗口只核对下面 22 篇。SUQL、TAG 归这里；04 里的同名五步是指针，不要另写一篇。输出写到 `proposal/sql-recall/deep/reanalysis/window-01.md`。

## 这个窗口要回答的问题

1. 这 22 篇里，有没有一篇已经在用户、物品、交互表上由模型写出 SQL，把执行结果当作候选，用留出交互的 Recall 或 NDCG 打分，并单独报告错误 SQL 被执行的代价？网格把这一格标成空着，并写这一路没有这篇。
2. 再报一个域内执行准确率，或把拒答、不可答令牌、错答更贵的可靠性分写成主创新，是不是已经挤满？网格写拒答主创新没有空位。
3. 换库会使在 Spider 上训练或成名的系统变差，但必须带配置。有没有同一系统、同一配置从 82% 掉到 25%–60%？40 个模板和专家 90.0 在 PDF 里还在不在？
4. 执行准确率会把错查询判对、把对查询判错，金 SQL 也会改名次。这些证据停在 SQL 对错。有没有一篇把主指标写成推荐的 Recall、NDCG 或 Hit？标签若由一条 SQL 算出，Recall 会不会退回执行匹配？这一点五份文件都还没测。
5. 纯 SQL 盖不住外部知识或自由文本。SUQL 占住的是餐馆表、最多返回 3 家、作者判定的集合精度。这个分数是不是 STaRK 上的检索，或交互表上的留出推荐分？

## 不要做的事

- 不要写「领域 text-to-SQL 完全不值得做」。挤满的是再报一个域内执行准确率；空位仍在。
- 不要把拒答写成主创新。EHRSQL、TrustSQL、EHRSQL 2024、OMOP、Query Carefully 已经占住「知道何时不写 SQL」。
- 不要写成同一系统从 82% 掉到 25%–60%。换库必须带配置。
- 不要把执行准确率、作者判定的约束满足或可靠性分写成 Recall、NDCG 或 Hit。
- 不要把空位写成「原文已经证明主指标必须是推荐效果」。推荐指标是把「打用户任务」落到推荐上的推论。

## 论文清单

重析实际写了下面 22 篇。Binder、H-STAR、BlendSQL 只在本目录，04 不析。

| 文章名称 | 场合或 arXiv | 本地 PDF 路径 | 这个窗口要核对的分析要点 |
|---|---|---|---|
| ScienceBenchmark | PVLDB 17(4): 685–698, 2023。文件名写 2024，PDF 自署 2023 | `papers/sql-recall/01-text-to-sql/ScienceBenchmark_PVLDB2024_Stockinger.pdf` | ① Table 5 的执行准确率从 PDF 重抄。82% 来自别的系统在 Spider 上的分数，25%–60% 不是同一批系统的同配置落差。② 脚注排除了 Picard 和 RESDSQL，核对表里实际跑通的模型。③ 隐含假设：每库 100 条 dev、裁过的 SDSS 仍代表复杂科学库。④ 指标是执行准确率；核对有没有推荐 Recall、NDCG 或 Hit。 |
| SM3-Text-to-Query | NeurIPS 2024 Datasets and Benchmarks | `papers/sql-recall/01-text-to-sql/SM3-Text-to-Query_NeurIPS2024.pdf` | ① Table 3 零样本 SQL 的最高分、Table 4 用 BM25 抽 5 个相似问句后的 SQL 分，都从 PDF 重抄。笔记写 Llama3-70b 零样本 47.05，GPT-3.5 固定五点 56.30、相似例 88.55。② 不要把 47% 写成医学 text-to-SQL 的上限。③ 隐含假设：408 个模板的填槽题等于医院原话；相似例不是同一骨架的金查询。④ 数据是 Synthea，不是医院导出。 |
| BiomedSQL | COLM 2026；arXiv:2505.20321v6 | `papers/sql-recall/01-text-to-sql/BiomedSQL_arXiv2505.20321.pdf` | ① 基线提示下的执行准确率从结果表重抄，并核对是不是笔记写的 546 条、这个 BigQuery 库。笔记写 Gemini-3-Pro 58.1、BMSQL-GPT-o3-mini 62.6。② 40 个模板和专家 90.0：笔记写这两格没有留下。核对它们属于哪个子集，不要写成科学推理已被测到差 25–30 个点。③ 隐含假设：漏掉 schema 里没有的统计阈值（如 `p < 5e-08`）是领域惯例，不是领域词表。④ 没有推荐指标。 |
| BookSQL | NAACL 2024 长文，页 497–516 | `papers/sql-recall/01-text-to-sql/BookSQL_NAACL2024.pdf` | ① Table 1 的精确匹配迁移从 PDF 重抄。笔记写 UniSAr 3.8、SEDE 0.0、RESDSQL 10.8，这是迁移，不是在 BookSQL 上微调。② 摘要的约 100k 对与第 3.4 节的 7,193 道 Hard、Table 3 的 Hard 45,000 冲突，两句都记下，不要收成一个规模。③ GPT-4 只跑了测试集随机 10%。④ 隐含假设：183 个专家模板的填槽等于会计人员的问句分布。 |
| FinSQL / BULL | arXiv:2401.10506v1。PDF 里 ACM 页眉仍是 Conference’17 占位，不要写成已出版会议 | `papers/sql-recall/01-text-to-sql/FinSQL-BULL_arXiv2401.10506.pdf` | ① BULL 的库数、对数，以及英文 FinSQL+LLaMA2 的执行准确率，从实验表重抄。笔记写三个金融库、4,966 对、执行准确率 82.2。② 10-shot 宏观迁移上 36.64 个相对点：核对是不是 LLaMA2 那一格，不要写成主表涨点。③ schema 链接的 R@k 或接近 1 的 AUC 是表/列召回，不是推荐召回，也不是跨库能力。④ 单表最大列数约 30，不要用 Spider 2.0 的难度给这个库背书。 |
| FINCH | arXiv:2510.01887v1，2025-10-02 | `papers/sql-recall/01-text-to-sql/FINCH_arXiv2510.01887.pdf` | ① 他们对 BookSQL 的执行检查从 PDF 重抄。笔记写 78,433 条里 9,526 条跑失败；保留的 BIRD 金融子集是从 1,139 里删掉 327 条。② Table 3 里 Arctic-Text2SQL-R1-7B 的执行准确率与 FINCH Score 名次可能不同。笔记写执行准确率第四、FINCH Score 第三。③ 结论若写 Arctic 胜过万亿模型，核对表里有没有万亿参数模型。④ 参考文献表里的 forthcoming 和 TrustSQL 的会议归属不要转引。 |
| EHRSQL | NeurIPS 2022 Datasets and Benchmarks | `papers/sql-recall/01-text-to-sql/EHRSQL_NeurIPS2022.pdf` | ① Table 5 的 F1exe 从 PDF 重抄。笔记写 MIMIC-III 百分位阈值下 T5 为 89.9，eICU 为 89.5。② 可回答模板是否出现在每个划分；不可回答是否只在验证和测试、约占 33%。③ Table 6 正文的 5.8% 与 5/107=4.7% 对不上，以表为准，两句都记下。④ 隐含假设：去歧义后的模板实例仍是 222 人的原话。不要把高分外推到没见过的问法。 |
| EHRSQL 2024 共享任务 | ClinicalNLP 2024，页 644–654 | `papers/sql-recall/01-text-to-sql/EHRSQL2024-shared-task_ClinicalNLP2024.pdf` | ① Table 3 从 PDF 重抄第一名的执行分、RS(0) 和严格惩罚下的 RS。笔记写第一名 RS(0) 88.17、RS(N) −711.83。② 核对高执行分和负的可靠性分是否来自同一系统。③ 不要把共享任务第一名写成医学 text-to-SQL 已解决。④ 各队工作论文不要另开。 |
| TrustSQL | arXiv:2403.15879v6，2024-07-02。页眉没有会议名 | `papers/sql-recall/01-text-to-sql/TrustSQL_arXiv2403.15879.pdf` | ① 公式 (1) 里 c=0、只看可行题时，可靠性分是否退化成执行准确率。从 PDF 抄公式，不要从笔记转写。② Table 3 的对照从 PDF 重抄。③ 隐含假设：假设列等于真实用户的含糊问法。笔记写不能这样写。④ 若主表只有推荐分、没有错误 SQL 被执行的代价，记下这篇追问的是哪一种错误被算成成功。 |
| An OMOP-Based Open-Source Text-to-SQL Benchmark Dataset | ClinicalNLP @ LREC 2026，页 381–393 | `papers/sql-recall/01-text-to-sql/OMOP-text-to-SQL_ClinicalNLP2026.pdf` | ① Table 2 从 PDF 重抄 LoRA-312 的 ExecAcc 和 RS(10)，以及未微调 Llama-3-8B-Instruct 的执行准确率。笔记写 93.55 与 RS(10) 0.373 同时出现，未微调是 10.54。② 输入是否已经换成 OMOP concept id，实体链接被拿掉。③ 划分单位是不是模板。④ 隐含假设：概念 id 已给定时的 SQL 生成等于临床 text-to-SQL。高分不构成新贡献。 |
| Query Carefully：Detecting the Unanswerables in Text-to-SQL Tasks | arXiv:2512.21345v1，2025-12-19。没有会议页眉 | `papers/sql-recall/01-text-to-sql/QueryCarefully_arXiv2512.21345.pdf` | ① 80 道题、8 类、每类 10 道，只有 llama3.3:70b。Values Missing 与 Column Ambiguous 的检测率从正文点名的数重抄。笔记写缺值基线 0.3、最高 0.5，列歧义最高 0.3。② 图 2–4 的柱高，除正文点名的数外，不要从图像上读出新的百分数。③ 可回答评测用的 OncoMX dev 是 99 对还是 100 对。④ 隐含假设：作者挑选的每类 10 题代表该类。不能写成拒答已经解决。 |
| Binder | ICLR 2023 | `papers/sql-recall/01-text-to-sql/Binder_ICLR2023.pdf` | ① WikiTQ 上相对 Codex SQL 的准确率从 Table 1 重抄。笔记写 61.1 到 64.6。② 不要把 64.6 写成 SQL 召回的上界。WikiTQ 是小维基表上的问答准确率。③ 隐含假设：需要外部知识或 SQL 语法外操作的题，纯 SQL 盖不住。④ 核对评测器说明，不要把这张表的分数和 H-STAR 表里的 BINDER 格子当成同一次复现。 |
| SUQL | NAACL 2024 Findings，页 4535–4555。归本窗口 | `papers/sql-recall/01-text-to-sql/SUQL_NAACL2024_Findings.pdf`。`papers/sql-recall/04-metrics/SUQL_NAACL2024.pdf` 字节相同，不另开 | ① Table 5 从 PDF 重抄。笔记写单轮 93.8、对话 90.3；线性化 @1 是 57.0 和 63.4。指标是返回集合的人工精度，上限 3 家。② 摘要若把 63.4 和 90.3 放在一起，核对 63.4 是不是对话的线性化 @1。③ 对话是否在他们自己的代理上收集。空返回的假阴性率从正文重抄。④ HybridQA 开发集 59.3 是原榜；抽 100 例后的 85.3% 是事后改标签。不要把 93.8% 写成排序指标，也不要写成 SQL 可以替换检索。 |
| TAG（《Text2SQL is Not Enough》） | CIDR 2025。归本窗口。分析对象是 CIDR 版 | `papers/sql-recall/04-metrics/TAG_CIDR2025.pdf`。不要把 `papers/sql-recall/01-text-to-sql/TAG_arXiv2408.14717.pdf` 写成另一篇 | ① Table 1 从 PDF 重抄。笔记写 80 道 BIRD 改写题、Llama-3.1-70B-Instruct；手写 TAG 总体精确匹配 0.55，Text2SQL 0.17，RAG 0.00。② 0.55 是手写流水线上界，不是可复用自动系统的分数。正文「其他基线不超过 20%」是精确匹配，不是 Recall。③ 聚合类是否不计精确匹配。④ 外推停在这 80 题和这个 70B。20% 不是 Recall、0.55 不是自动 Text-to-SQL，这句事实与 04 相同，论文仍归本窗口。 |
| H-STAR | NAACL 2025 长文，页 8841–8863 | `papers/sql-recall/01-text-to-sql/H-STAR_NAACL2025.pdf` | ① Table 1 从 PDF 重抄 GPT-3.5-Turbo 的 WikiTQ。笔记写 H-STAR 69.56，端到端 QA 51.84；表内 BINDER 是 56.74，低于 Binder 原文的 64.6。② 68.85 若 PDF 里没有这一格，不要补。③ 表注是否写明基线来自 Chain-of-Table 论文。④ 这是表问答路由。可以核对「不是每道题都该进 SQL」，不要把 WikiTQ 准确率写成推荐召回。 |
| BlendSQL | arXiv:2402.17882。没有会议页眉 | `papers/sql-recall/01-text-to-sql/BlendSQL_arXiv2402.17882.pdf` | ① Table 2 从 PDF 重抄 HybridQA 开发集。笔记写全文端到端 49.13、BlendSQL 52.89、回退到端到端 57.76。8.63 个点是回退，不是方言单独的涨点。② 12 个少样本对零样本端到端，例题数不同。合法子集上的 64.43 不是全开发集。③ 35% 与 45% 的 token 节省，只有同一张表算得出来才引用。④ 隐含假设：把上下文先灌进 SQLite 不改变任务难度。没有推荐留出。 |
| FLEX | NAACL 2025 长文，页 4448–4475 | `papers/sql-recall/01-text-to-sql/FLEX_NAACL2025.pdf` | ① Table 3 从 PDF 重抄 EX 对专家共识的 Cohen’s kappa，以及等价、不等价子集的准确率。笔记写 kappa 62.00，子集准确率 79 与 83。② 正文把 21 与 17 放进的子集若和表相反，两句都记下，不要择一。③ GPT-4o 版 FLEX 的 kappa 87.04 只属于他们后来选的提示。名次变化是 FLEX 对 EX 的重排，不是金标被独立改正。④ 论文要求换的是更像专家的 SQL 对错判断，没有写成 Recall 或 NDCG。 |
| Pervasive Annotation Errors Break Text-to-SQL Benchmarks and Leaderboards（Jin 等） | arXiv:2601.08778。没有会议页眉 | `papers/sql-recall/01-text-to-sql/Jin_annotation-error_arXiv2601.08778.pdf` | ① 人工复核后的错误率从 PDF 重抄，并写明子集。笔记写 BIRD Mini-Dev 498 条里 263 条（52.8%），Spider 2.0-Snow 公开金 SQL 121 条里 76 条（62.8%）。不要写成全部 BIRD 或全部 Spider 2.0。② 修正子集上 16 个系统的相对执行准确率变化和名次变化从 PDF 重抄。笔记写 −7% 到 31%，名次 −9 到 +9。CHESS 的配置是否用了 GPT-4o。③ 相对百分比不是绝对点数。④ 金 SQL 会改名次。若推荐标签也由一条 SQL 算出，同样的审计适用。这篇不把替代指标指定为 NDCG。 |
| Understanding the Effects of Noise in Text-to-SQL: An Examination of the BIRD-Bench Benchmark（Wretblad 等） | ACL 2024 短文，页 356–369 | `papers/sql-recall/01-text-to-sql/Wretblad_BIRD-noise_ACL2024-short.pdf` | ① Table 1 从 PDF 重抄。笔记写金融开发集 106 对里 52 对有噪声、22 条金 SQL 有错；另外四个域各 20 条。n 不要写成全开发集。② Table 2 的错误类型次数可以大于有错的对数，不要当成两个错误率。③ Figure 3 只有版面上印出的百分比才可引用；笔记没有从柱高抽出可靠数字。④ 只修正 SQL 之后的名次颠倒，限于这批金融域问题和他们用的模型。 |
| Spider 2.0 | ICLR 2025；arXiv:2411.07763v2 | `papers/sql-recall/01-text-to-sql/Spider2.0_arXiv2411.07763.pdf` | ① Table 2 按全体、lite、snow 分开抄列数和金 SQL token 数。不要把「812 列」和「144 token」收成同一个子集的一对平均数。② Table 3 的 21.36% 若是带 SQLite 的任务占比，不要写成做对率。Table 6 的成功率从 PDF 重抄。笔记写 o1-preview 智能体 21.36%。③ 91.2 与 73.0 的主语是不是这篇智能体。不要写成同一系统从 Spider 1.0 / BIRD 掉到 21.3。④ 物品-用户-交互若只有几张窄表，不能用这篇的企业工作流难度背书。 |
| Arctic-Text2SQL-R1 | ACL 2026 Findings，页 26966–26995 | `papers/sql-recall/01-text-to-sql/Arctic-Text2SQL-R1_ACL2026-Findings.pdf` | ① 7B 那一行从 PDF 重抄，并核对表头：BIRD 是不是 (dev)。笔记写 BIRD 68.9、Spider 88.8、Spider2.0-SQLite 15.6。同表 OmniSQL-7B 的 Spider2.0-SQLite 是 13.3，不是 OmniSQL 自己 Table 4 的 10.4。② 32B 的 BIRD 测试 71.83 是另一行。不要把 7B 的 68.9 写成测试集，也不要把同表 ExDPO-70B 的 68.5 写成 7B。③ 奖励只看执行。局限节是否写明碰巧相同的错 SQL 仍可能得分。④ 六基准平均不要写成每个库都已解决。本地用这个检查点是工程选择，不是评测结论。 |
| OmniSQL | arXiv:2503.02240。没有会议页眉 | `papers/sql-recall/01-text-to-sql/OmniSQL_arXiv2503.02240.pdf` | ① Table 4 的 OmniSQL-7B 行从 PDF 重抄，列明贪心还是多数投票、开发集还是测试集。笔记写 Spider 测试贪心 87.9，BIRD 开发集 63.9 与 66.1，Spider2.0-SQLite 10.4。这份 PDF 里若没有 BIRD 测试 67.97，不要补。② Spider2.0-SQLite 子集是不是 135 条。③ 隐含假设：一致性过滤等于人工金标；Spider 高分会转移到物品-交互库。④ 生成器可以借用，评测不要借用它的执行准确率。 |

## 交给这个窗口的写法

对上表每一篇按五步写完，不要跳步：（1）逐段提取核心论点和论据（2）论点之间的因果、递进、转折、并列（3）未明说的隐含假设（4）证据强度和推理漏洞（5）最终结论。数字从 PDF 抄，不从旧笔记或本大纲转写；旧笔记只用来知道要核对哪一格。输出写到 `proposal/sql-recall/deep/reanalysis/window-01.md`。不要重写 SUQL、TAG 以外、归 02 到 05 的论文；QUEST、InteRecAgent、SIEVE、RecBench+、RelBench v1 会议版都不在这里。
