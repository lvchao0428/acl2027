# 05 RelBench

日期：2026-11-11。本窗口只做协同假设的健全性检查：一条带时间谓词的共现 SQL，在 H&M 购买上有没有超过历史访问。这组不能当语言实验。RelBench v1 只分析 12 页会议版。输出写到 `proposal/sql-recall/deep/reanalysis/window-05.md`。

## 这个窗口要回答的问题

1. 关系库上的未来窗口 top-K、由工程师写死的 SQL：手写共现有没有出现？网格标成空着且值得做。它是漏掉的基线，不是新系统。
2. 这条共现 SQL 在 H&M 购买上有没有超过历史访问？网格写先对照历史访问；超过历史访问不等于接近 ContextGNN。这个对照测过没有？
3. 同一任务上，用 BM25 或搜索引擎改写问句，是不是假空？网格写输入是实体和种子时间，没有可供模型改写的用户问句。
4. Wydmuch 定义了链接任务的 MAP，实验有没有测？网格写没有测，不能把缺席写成 LLM 已经匹配推荐。

## 不要做的事

- 不要写「GNN 打败 SQL」。H&M 上超过历史访问的是 ID-GNN、NBFNet 和 ContextGNN，不是任意一个 GNN，也不是数据科学家的特征 SQL。
- 不要把两层 GraphSAGE、NGCF、MultiVAE 写成超过了历史访问。
- 不要把「超过历史访问」写成接近 ContextGNN。
- 不要把这组写成 ACL 的语言实验。没有一篇把用户问句解析成 SQL，再把结果集当成购买 top-K。
- 不要把这里的历史访问数成 02 的 ItemKNN。历史访问数的是历史标签列表，不是交易表对自身的连接。MAP 以本窗口的表为准。
- 不要把没做推荐实验写成 LLM 已经匹配推荐。

## 论文清单

七篇都在下表。`papers/sql-recall/05-relbench/relbench-v1-arxiv-2407.20060.pdf` 是 v1 的 33 页预印本，不另列。附录表 15 只在解释会议版 `#Dst Entities` 时打开。

| 文章名称 | 场合或 arXiv | 本地 PDF 路径 | 这个窗口要核对的分析要点 |
|---|---|---|---|
| RELBENCH: A Benchmark for Deep Learning on Relational Databases（会议版 v1，Robinson 等） | NeurIPS 2024 Datasets and Benchmarks。12 页。归本窗口 | `papers/sql-recall/05-relbench/relbench-v1-neurips2024.pdf` | ① 表 5 的 H&M 购买测试从 PDF 重抄：全局流行、历史访问、LightGBM、GraphSAGE、ID-GNN。笔记写 0.30、0.89、0.38、0.80、2.81。表题没有写百分数；大于 1 的格子、以及 ContextGNN 写明的 in %，用来确定刻度。标准差在附录 C 表 8，这 12 页没有。② `#Dst Entities` 13,428,473 是不是目录。预印本附录表 15 的训练边 13,191,321 加验证边 237,152 是否等于这个数。`item-sales` 的唯一实体 105,542 是另一列。③ 手写共现有没有出现。历史访问和全局流行数的是历史标签列表，不是自连接。④ 用户研究的 15 个任务是分类和回归，图 3 到图 5 不包含购买推荐。输入列是实体、种子时间、标签。 |
| RELBENCH V2: A Large-Scale Benchmark and Repository for Relational Data（Gu 等） | ICLR 2026 DATA-FM workshop；arXiv:2602.12606 | `papers/sql-recall/05-relbench/relbench-v2-arxiv-2602.12606.pdf` | ① 表 20 的 H&M 购买测试从 PDF 重抄，带标准差。笔记写历史访问仍是 0.89、全局流行 0.30；两层 GraphSAGE 0.80±0.07，四层 0.68±0.06，都低于历史访问；两层 ID-GNN 2.80±0.01。会议版的 0.38、2.81 是另一轮点估计。② 表 10 的新任务平均不要和 H&M 的 0.89 比高低。RateBeer 上四层 GraphSAGE 的空格是显存，不是 H&M。③ 附录 E.3 的 “official MAP@10” 和按任务设置的 K 是否冲突。表 25 的 0.0006649 是冒烟，不能用来改表 5 或表 20。④ 手写共现仍然没有。输入仍是实体、时间和标签。 |
| ContextGNN: Beyond Two-Tower Recommendation Systems（Yuan 等） | arXiv:2411.19513v1。这份 PDF 没有会议页眉 | `papers/sql-recall/05-relbench/contextgnn-arxiv-2411.19513.pdf` | ① 表 2 的 H&M 购买测试从 PDF 重抄。笔记写 LightGBM 0.38、MultiVAE 0.28、GraphSAGE 0.80、NGCF 0.75、NBFNet 2.81、ContextGNN 2.93。表题写了 MAP in %。历史访问不在这张表。② 20% 和 344% 是八个任务测试平均上的相对差，不是 H&M 这一格。③ 表 1 的局部性从 PDF 重抄。笔记写 H&M 购买测试 k=1 为 0.048、k=3 为 0.417。公式 (1) 的区间与第 3 节正文是否同一个开闭区间。④ 没有自连接，没有 ItemKNN。生成式推荐只在相关工作里一句带过。Amazon-Book 的 Recall@20、NDCG@20 是静态小图，不要填进 H&M。 |
| Relational Deep Learning: Graph Representation Learning on Relational Databases（Fey 等） | arXiv:2312.04615v1。会议版 v1 把它引成 ICML 2024 position paper；这份 PDF 没有会议页眉 | `papers/sql-recall/05-relbench/rdl-fey-arxiv-2312.04615.pdf` | ① 第一版 RelBench 是不是只有节点任务。有没有 MAP，有没有 H&M。② 第 3.5 节、第 5.3 节把一层消息传递写成 `JOIN` 再 `AGGREGATE`。核对有没有跑这条聚合，有没有跑自连接基线。③ 时间条件三处是否不一致：引言是严格早于，公式 (4) 是邻居时间小于等于种子，算法 1 滤的是中心节点自己的时间。④ 隐含假设：`JOIN+AGGREGATE` 等于已经提交了 top-K。不能把「GNN 是 SQL 的神经网络形式」写成共现 SQL 已经输了。 |
| Tackling prediction tasks in relational databases with LLMs（Wydmuch 等） | arXiv:2411.11829v1 | `papers/sql-recall/05-relbench/wydmuch-arxiv-2411.11829.pdf` | ① 表 1、表 2 是不是只有实体分类 AUROC 和实体回归 MAE，对照是 LightGBM 和 RDL。有没有 MAP 的实验格子。② 正文是否定义了链接任务用 MAP，然后实验没有做第三类。③ 时间谓词是不是严格小于 \(t_p\)。任务说明是基准作者写的固定段落，不是用户问句。④ 大测试集被抽成 10,000 条时，表上的数只在这个抽样下成立。不要把缺席写成 LLM 已经匹配推荐。 |
| RelAgent: LLM Agents as Data Scientists for Relational Learning（Huang 等） | NeurIPS 2026；arXiv:2605.07840v2 | `papers/sql-recall/05-relbench/relagent-arxiv-2605.07840.pdf` | ① 表 2 的任务范围从 PDF 核对。笔记写 v1 的 12 个分类加 9 个回归，就是 30 个任务去掉 9 个推荐。H&M 列是 churn，不是 `user-item-purchase`。② 分类平均 AUROC 和名次从 PDF 重抄。笔记写 RelAgent 78.38、名次 3.17，KumoRFM-v2 79.60。H&M 的 71.07 若是流失分类，不要和购买 MAP 的 0.89 或 2.93 比较。③ 有没有在 H&M 购买上提交 SQL 结果集。④ 语言用在搜索特征的智能体里。推理时有没有用户问句。 |
| ReFuGe: Feature Generation for Prediction Tasks on Relational Databases with LLM Agents（Kim 等） | WWW 2026 短文；arXiv:2601.17735v1。4 页 | `papers/sql-recall/05-relbench/refuge-arxiv-2601.17735.pdf` | ① 表 1 是不是全部 AUROC。H&M 这一列是 churn 还是购买。笔记写 LightGBM 55.21，与会议版表 3 的 `user-churn` 相同；ReFuGe 68.10。② 有没有 `user-item-purchase`，有没有 MAP，有没有 top-K。③ 特征生成里的连接进入的是 LightGBM，不是协同召回的结果集。提示词若不在这 4 页里，不要补具体 SQL。④ 平均迭代轮数只是他们报告的停止统计，没有推荐任务的对应实验。 |

## 交给这个窗口的写法

对上表每一篇按五步写完，不要跳步：（1）逐段提取核心论点和论据（2）论点之间的因果、递进、转折、并列（3）未明说的隐含假设（4）证据强度和推理漏洞（5）最终结论。MAP、历史访问和 `#Dst Entities` 从 PDF 抄。输出写到 `proposal/sql-recall/deep/reanalysis/window-05.md`。不要把 arXiv 预印本写成第二篇，也不要重析归 01 到 04 的论文。ItemKNN 的矩阵式 top-n 归 02。
