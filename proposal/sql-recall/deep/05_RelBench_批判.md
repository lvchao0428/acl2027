# RelBench 批判

> 2026-11-11。只新增这一份。PDF 在 `papers/sql-recall/05-relbench/`。标签 SQL 和指标来自 GitHub `stanford-star/relbench` 的 tag `v1.1.0`（`snap-stanford/relbench` 会跳到这里）。没有下载 parquet，没有装包后跑数据。
>
> 现行 `main`（v3）已经不再带 `relbench/tasks/*.py`。`main` 上的 `relbench/metrics.py` 仍然返回 0 到 1 的 MAP。论文表格用的是 v1 那套任务定义。

读过的全文：RelBench v1 arXiv 2407.20060（33 页，含附录；NeurIPS 会议版 PDF 只有 12 页，表格文字抽不出来，数字以 arXiv 为准）、RelBench v2 arXiv 2602.12606、ContextGNN arXiv 2411.19513、Fey 等 arXiv 2312.04615、Wydmuch 等 arXiv 2411.11829、RelAgent arXiv 2605.07840、ReFuGe arXiv 2601.17735（WWW 2026 短文，下载到的 PDF 是 4 页，文中说提示词在附录，这份 PDF 里没有）。Kumo 的 PQL 是产品文档，不是论文；当天打开的页面写在文末。

## 五个问题

### 1. 调查里的 MAP 就是论文测试格，而且是百分数

是。两行都是测试集，列顺序是全局流行、历史访问、LightGBM、GraphSAGE、ID-GNN、ContextGNN。前五列是 RelBench v1 表 5，最后一列是 ContextGNN 表 2。没有抄错格，也没有把验证集当成测试集。

v1 表 5 的表题是：“Recommendation results (MAP, higher is better) on RELBENCH. Best values are in bold. See Table 8 in Appendix B for standard deviations.” 表题本身没写 percent。ContextGNN 表 2 的表题写了：“Recommendation results (MAP, higher is better, in %) on RELBENCH.”

它们必须是百分数。MAP 的定义在 0 和 1 之间，而表里 Stack 评论的 ID-GNN 是 12.72，trial 的 site-sponsor-run 是 19.00。v1.1.0 的 `link_prediction_map` 返回的是这个 0 到 1 的均值。2026-08-25 的线上榜也存小数。历史访问在 `rel-hm/user-item-purchase` 上是 0.008909512329806949，乘 100 是 0.89095，四舍五入就是表里的 0.89。Amazon 购买的历史访问是 0.0006272245094988528，乘 100 后对上 0.06。全局流行同样对得上：H&M 0.0030455769442783946 → 0.30，Amazon 购买 0.0024395144913499944 → 0.24。

所以调查里的 0.89 和 2.93 是百分点。代码里的 MAP 大约是 0.00891 和 0.0293。两行的 ContextGNN 测试格都印成 2.93，不是抄重了：Amazon 购买的验证集是 2.71，H&M 的验证集是 3.00。

| 任务（测试） | 调查 | v1 表 5 | ContextGNN 表 2 | 判定 |
|---|---|---|---|---|
| Amazon 购买 | 0.24 / 0.06 / 0.16 / 0.74 / 0.10 / 2.93 | 0.24 / 0.06 / 0.16 / 0.74 / 0.10 | LightGBM 0.16，GraphSAGE 0.74，ContextGNN 2.93 | 对 |
| H&M 购买 | 0.30 / 0.89 / 0.38 / 0.80 / 2.81 / 2.93 | 0.30 / 0.89 / 0.38 / 0.80 / 2.81 | LightGBM 0.38，GraphSAGE 0.80，ContextGNN 2.93 | 对 |

ContextGNN 表 2 没有历史访问、全局流行和名为 ID-GNN 的列。H&M 测试集上它的 NBFNet 格也是 2.81，和 v1 的 ID-GNN 相同。调查把 2.81 标成 ID-GNN，跟的是 v1 表 5 的列名。两篇论文的 LightGBM 和 GraphSAGE 在这两行上一致，所以把 2.93 接到同一行是合法的拼接，不是把不同协议的数字横着比。

v2 表 20 把同一批 v1 任务又跑了一遍，列顺序改成了历史访问、全局流行。确定性的两列没变：H&M 测试仍是历史访问 0.89、全局流行 0.30；Amazon 购买仍是 0.06 和 0.24。LightGBM 的点估计动了：H&M 测试 0.37±0.03，Amazon 购买测试 0.14±0.01。两层 ID-GNN 的 H&M 测试是 2.80±0.01。调查写的 0.38、0.16、2.81 是 v1 表 5 的点估计，不是 v2 的重跑。引用时要写明是哪一张表。

调查里另外两行也核过，测试格同样对得上：Amazon 打 5 星是 0.15 / 0.07 / 0.17 / 0.87 / 0.12，ContextGNN 2.25；Stack 评论是 0.02 / 1.42 / 0.04 / 0.11 / 12.72，ContextGNN 13.34。

榜上有一格不能拿来改论文。2026-08-25 榜的 ID-GNN，`rel-trial/condition-sponsor-run` 是 0.003319897518235944，`rel-trial/site-sponsor-run` 是 0.0013654002629684414。v1 表 5 的测试格是 11.36 和 19.00。除以 100 也不是这两格。同一份榜上，H&M 和 Amazon 购买的 ID-GNN 乘 100 后仍是 2.81 和 0.10。GraphSAGE 那一列已经漂了：榜上 Amazon 购买是 0.008221787606968074，乘 100 约 0.82，论文是 0.74。比较时用论文表格。

K 不是 10。v1.1.0 里：Amazon 三个推荐任务 `eval_k = 10`，H&M 和 Avito 是 12，Stack 两个任务是 100，trial 两个任务是 10。v1 没有 F1 推荐任务。调查里「F1 也是 10」对不上 v1。v2 附录 E.3 写 “the official MAP@10 used in the RELBENCH evaluation code”，这句不成立：评测代码用的是每个任务自己的 `eval_k`。v2 表 25 把 H&M 的冒烟结果标成 MAP@10，数值是 0.0006649 这种小数，和表 5 的 0.92 不是同一次实验，不能拿来改表。

### 2. 历史访问不是最强的平凡 SQL；手写共现是漏掉的基线，不是新系统

历史访问和全局流行是两条聚合，都可以写成 SQL。它们不是协同自连接。

v1.1.0 的 `examples/baseline_link.py` 把历史访问定义成：对每个源实体，把它在过去任务表里的目标列表摊平，用 `Counter.most_common(eval_k)` 取前 K。测试时把训练表和验证表拼在一起。任务表里的列表是每个历史种子之后那个窗口的 `LIST(DISTINCT …)`，所以计的是「出现在多少个历史窗口里」，不是原始交易次数，也没有时间衰减。全局流行是同一批列表的全局计数。H&M 上这条历史访问已经是 0.89，全局流行是 0.30。Amazon 购买上反过来：全局流行 0.24，历史访问 0.06。

LightGBM 也不是共现连接。`examples/lightgbm_link.py` 的 `prepare_for_link_pred_eval` 把该用户的历史前 K 和全局前 `2K` 交错，再截到最多 `eval_k * 2` 个候选，然后在这个小集合上重排。H&M 的 K 是 12，候选最多 24 个。它打不到目录里其余的物品。训练指标的注释写明，训练集指标会虚高，因为正例被放进了候选集。这就是为什么 H&M 上 LightGBM 测试只有 0.38，低于历史访问 0.89：它是在给一条已经不错的历史名单重新排序，排坏了就掉分。Amazon 购买上它是 0.16，落在历史访问 0.06 和全局流行 0.24 之间，同样出不了这两张名单。

论文没有跑 ItemKNN、Swing，也没有跑一条时间衰减的物品–物品自连接。附近的东西是学习过的近邻模型，都在 ContextGNN 表 2 里，单位同样是百分数：

| 测试 | 历史访问 | 全局流行 | MultiVAE | GraphSAGE | NGCF | NBFNet | ContextGNN |
|---|---:|---:|---:|---:|---:|---:|---:|
| H&M 购买 | 0.89 | 0.30 | 0.28 | 0.80 | 0.75 | 2.81 | 2.93 |
| Amazon 购买 | 0.06 | 0.24 | 0.23 | 0.74 | 0.88 | 2.06 | 2.93 |

H&M 上，MultiVAE、NGCF、两层 GraphSAGE 都没有超过历史访问。Amazon 购买上，GraphSAGE 和 NGCF 超过了全局流行，但离 NBFNet 和 ContextGNN 还远。ContextGNN 自己的局部性分数说明这两边的信号不一样。表 1 里，测试集 1 跳局部性（未来正例里有多少已经在该用户自己的历史上）H&M 是 0.048，Amazon 购买是 0.001。3 跳局部性 H&M 是 0.417，Amazon 购买是 0.168。H&M 的重复购买覆盖率只有 4.8%，但历史访问的 MAP 已经不低；能把 MAP 从 0.80 抬到 2.81 的是 ID-GNN / NBFNet 这种按用户条件化的成对表示，不是对称的共现计数。

因此：手写的时间衰减共现 SQL 是 RelBench 没报过的经典基线，是一次复现意义上的补实验，不是一个新系统。它更接近表里已经输给历史访问的近邻模型，而不是 ContextGNN。H&M 上它有可能超过 0.89，因为现有近邻模型做了 128 邻居采样，并不是精确的 ItemKNN；现有数字只说明先验不利。Amazon 上超过 0.06 几乎没有信息量，要看的是能不能超过全局流行 0.24，以及离 GraphSAGE 的 0.74 还有多远。先导如果只把「超过 H&M 历史访问 0.89」当成协同假设的生死线，H&M 失败只能说明这条 SQL 没有打过重复购买，不能说明 Amazon 上没有协同空间。

人类基线和后来的智能体也不是「SQL 的执行结果就是 top-K」。v1 第 6 节的数据科学家给 15 个实体分类和回归任务写特征 SQL，再接 LightGBM。平均 12.3 小时，标准差 1.6 小时。图 3 只有分类和回归。推荐任务不在这 15 个里面。

### 3. 怎样的泄漏会让手写 SQL 看起来打过 ContextGNN

合法的切分是：特征用种子时间及其之前的行，标签用种子之后、窗口右端闭区间里的行。几份文献的写法不完全一样，先导要按模型实际用的那条，而不是按最严的那句英文。

- Wydmuch 等把 RelBench 的规则写成严格小于。原文：“when predicting for an entity with prediction time \(t_p\), the model can get as input only information from another entity \(v\) with timestamp \(t_v < t_p\).”
- Fey 等的公式（4）是小于等于。邻域是 \(\tau(w) \le t\) 的邻居。正文又说 “only aggregating messages from nodes that were available before the given seed time”。算法 1 把条件写成了中心节点的 \(\tau(v) \le t\)，和公式（4）的邻居时间不是同一件事。以公式（4）为准。
- ContextGNN 第 3 节：图是 \(G_{(-\infty,T]}\)，标签在 \((T, T+i]\)。“the model only has access to historical information up to timestamp \(T\).”
- PyG 2.6.1 的负采样注释写 “we can only sample nodes for which `node_time <= seed_time`”，非法样本是 `node_time > seed_time`。pyg-lib 的文档写 “earlier or equal timestamp than the seed node”。
- v1 正文用的是 “before the seed time”，同时写明避免泄漏是设计者的责任，并建议用他们测过的采样实现。

标签 SQL 和这个闭开区间一致。H&M 是 `t_dat > t.timestamp AND t_dat <= t.timestamp + 窗口`。窗口在种子处是开的，所以恰好落在种子时间上的交易不是标签。GNN 的 \(\le T\) 会把它们当特征。手写 SQL 用 `t_dat <= 种子` 是在对齐 GNN；用 `t_dat < 种子` 更严，只会使分变低或持平。H&M 的 `t_dat` 如果只精确到日期，相等的那一天就是整天。这不是把 SQL 做成假胜利的那种错误。

会把 MAP 做成假结果的，是把种子之后的行算进特征。具体有四条：

1. 目标用户自己在 \((T, T+7]\) 里的购买进了历史或候选。正例被塞进前 12，MAP 会跳。LightGBM 训练注释里的虚高就是这一种。这是唯一一种不需要任何协同信号、也能稳定超过 ContextGNN 的错误。
2. 共现表用了全表，包括测试周里其他用户的购买。目标物品和用户历史物品的共现次数里含有标签周。H&M 测试窗只有 7 天，行数占比不大，但这 7 天就是标签的来源。验证集如果用测试截止日之前的整张共现表来调衰减系数，验证窗 \((2020\text{-}09\text{-}07,\ 2020\text{-}09\text{-}14]\) 已经漏进验证分。
3. 测试和验证共用一张在全历史上算的矩阵。v1 的历史访问没有这么做：测试用训练表加验证表，验证只用训练表。
4. 候选集里放入真实标签，再在这个集合里排序。全库 MAP 和「正例已经在候选里」的 MAP 不是同一个数。

先导里先复现官方历史访问，测试 MAP 要对上榜上的 0.008909512329806949（表里的 0.89）。对不上就不要解释共现 SQL。官方历史访问读的是任务表，不是原始交易；用原始次数重写一条「历史访问」不会得到 0.89，那个差距不是协同信号。

H&M 的种子只有一个。`num_eval_timestamps` 默认是 1，购买任务没有改。表 1 的验证截止是 2020-09-07，测试截止是 2020-09-14。测试的 67,144 行共享这一个测试时间。共现表按这一个截止日算一次是合法的。训练表有 3,878,451 行，那是许多个历史种子，不能把每个训练行的未来列表当成该行的历史。

数据库侧还有一道闸。`BaseTask._get_table` 对训练和验证调用 `get_db(upto_test_timestamp=True)`，构造这两份标签时看不到测试截止之后的行。测试标签用完整库。特征侧的闸不在这里，而在采样器的 `input_time`。SQL 必须自己写时间谓词。

### 4. 「14 个任务各一句英文模板，不是 ACL 的语言论文」这个理由成立

成立，而且只够把 RelBench 留在健全性检查里。两篇 RelBench 都没有自然语言查询。任务表的列是实体、种子时间和标签。v1 第 2 节写的是 Entity ID、seed time、target labels。输入不是一句用户话。

14 这个数对得上推荐任务的个数：v1 有 9 个（Amazon 3，Avito 1，H&M 1，Stack 2，trial 2），v2 表 10 新加 5 个（arXiv 共引、F1 车手–赛道、RateBeer 三个）。9 加 5 是 14。v1 单独看是 9，不是 14。这些任务的英文只出现在文档字符串和附录 A 的任务说明里，例如 “Predict the list of articles each customer will purchase in the next seven days.” 那是任务定义，不是待解析的问句。给 14 个任务各套一句模板，语言侧没有词汇变化、没有组合、没有歧义，也没有用户真的说过的话。

ACL 审稿人会同意把它逐出语言主实验。他还会追问两件和语言无关的事：H&M 上没超过 0.89，能不能就写成「协同自连接没有空间」；主实验如果在 STaRK 上，RelBench 的负结果要不要写进正文。以目前的停点，负结果应当留下，但范围只写成「这条手写 SQL 在 H&M 购买上没有超过历史访问」。

KDD 审稿人不会接受「没有语言」作为把结果降级的理由。对他来说 RelBench 就是实验，STaRK 是另一个问题。他会要求时间协议和全库排序，也会要求 ItemKNN 或时间衰减共现本来就在表里。他还会说：Amazon 上超过历史访问 0.06 太容易，H&M 上和历史访问比又被重复购买缠住；ContextGNN 不是这条 SQL 的直接对照，NGCF 和 MultiVAE 已经在论文里。两边的意见可以同时成立：ACL 主实验不放在 RelBench，KDD 也不会把一条补上的经典基线当成新模型。

Wydmuch 等确实给实体任务写了短的任务说明，再把相关行序列化成 JSON，用 Llama 3.2 的下一个 token 概率或一个小 MLP 做分类和回归。那仍然不是用户问句，而且他们没有跑推荐。不能把那篇当成「RelBench 已经是语言实验」的反例。

### 5. H&M 的手写 SQL 在一台 CPU 上可以跑；13.4M 不是目录大小

可以跑，但不要对交易表做无聚合的自连接，也不要物化稠密的物品–物品矩阵。四层 GNN 不用跑。v2 写的 80GB A100 显存错误是真的，范围主要是 RateBeer：表 10 里这些任务的四层 GraphSAGE 是空的，附录 D.4 写明即使 batch size 降到 64，RateBeer 的四层 GraphSAGE 仍然放不进显存。同一份表 20 里，H&M 的四层 GraphSAGE 有数字，测试 MAP 是 0.68±0.06，低于两层的 0.80±0.07，也低于历史访问 0.89。Amazon 购买的四层是 0.91±0.09，高于两层的 0.74±0.06。所以「H&M 上四层会 OOM」并不成立；「H&M 上不值得为四层去租 A100」成立，因为论文里的那一格已经输给历史访问。5090 用不上。SQL 是 CPU。

目录不是 1,340 万。表 2 最后一列的表头是 “#Dst Entities”，H&M 购买是 13,428,473，Amazon 购买是 12,562,384。它等于训练正例边加验证正例边：

- H&M：表 15 的训练边 13,191,321，验证边 237,152，和是 13,428,473。
- Amazon 购买：训练边 11,759,844，验证边 802,540，和是 12,562,384。

物品表的大小在 item-sales 上。唯一实体 105,542，训练行 5,488,184，等于 52 乘 105,542。验证和测试各 105,542 行，训练/测试实体重叠 100%。文章目录就是 105,542。数据库在测试截止之前一共 16,664,809 行、3 张表、37 列（表 1）。购买任务的测试表是 67,144 行，一个种子时间，K=12，标签窗 7 天。测试正例边 207,996，平均每个源实体 3.10 条。

GNN 的评测代码本来就给目录里每个目标节点打分：`examples/gnn_link.py` 对整个目标表做 `NeighborLoader`，再 `topk(emb @ dst_emb.T, k=eval_k)`。`num_dst_nodes` 是目标表的行数。H&M 上这个行数是 105,542，不是 1,340 万。67,144 乘 105,542 的稠密分数矩阵大约是 71 亿个标量，不必落盘；SQL 也不该落盘。

论文没有给每个用户的终身购买度数，所以不能从论文推出无上限自连接的中间行数。仍然是 SQL 的预聚合是：

1. `WHERE t_dat <= 测试种子`，全测试集共用这一刀。
2. `GROUP BY customer_id, article_id`，得到次数和最近时间。衰减如果是写死的函数，例如固定 \(\lambda\) 的指数，`SUM` 里可以带上它。
3. 窗口函数只留每个用户最近或次数最高的前 N 个物品，再按 `customer_id` 自连接，得到稀疏的物品–物品计数。N 是写死的或在验证集上选的常数。
4. 用测试用户的历史连接这张稀疏表，聚合成物品分，`ROW_NUMBER` 取 12。流行度惩罚如果是计数的闭式，例如除以物品出现次数，仍然是 SQL。

变成学习模型的地方：GraphSAGE、ID-GNN、ContextGNN、NGCF、MultiVAE 的嵌入；在成对特征上训练 LightGBM；用梯度去拟合衰减系数或融合权重。在验证集上网格搜索一个 \(\lambda\)，并且验证矩阵按验证种子另算一张，这仍是基线的超参，不是 GNN。用测试矩阵去选 \(\lambda\) 就是第 3 节的泄漏。

Amazon 购买不能沿用「1,260 万个目标、所以连接不可做」这个理由，因为 12,562,384 同样是训练边加验证边。论文没有给出 product 表的行数。表 1 只说三张表在测试截止前一共 15,000,713 行。item-churn 的唯一实体 416,352 是进了那个任务的产品，不是目录上界。Amazon 的标签窗以代码为准：`timedelta = pd.Timedelta(days=365 // 4)`，即 91 天，`eval_k = 10`。附录 A 写 “next 3 months”。类文档字符串写 “next two years”。当天用 DuckDB 算过，`INTERVAL '91 days 00:00:00 days'` 和少写一个单位的写法都是加 91 天，f-string 里多出来的 `days` 没有把窗口加长。Stack 的两个推荐任务有同一个错位：附录和文档字符串都写两年，`timedelta` 仍是 `365 // 4`。H&M 的文档、附录和 `Timedelta(days=7)` 三者一致。验证截止 2015-10-01 到测试截止 2016-01-01 差 92 天，91 天的窗口能通过代码里「窗口不能长于验证到测试的间隔」那道检查。

先导的数据量级就是这 1,666 万行和 10.6 万篇文章。代码本身不用下载数据就能读。真要跑查询，才需要 H&M 的 parquet；论文给出的规模是上面这几个行数，不是 1,340 万个目的地。

## 每篇里和「SQL 能不能排序」有关的主张

### RelBench v1（Robinson 等，NeurIPS 2024 D&B，arXiv 2407.20060）

- 推荐是给定源实体和种子时间，对目标实体排 top-K，指标是 MAP@K。站得住。K 按任务，不是统一的 10。
- 表 5 的测试格就是调查引用的那几列，打印刻度是百分数。数字站得住。表题没写 “in %”，刻度要靠「表内有大于 1 的数 + 代码返回 0 到 1 + ContextGNN 表题写了 in % + 榜上小数乘 100」一起才站得住。
- 历史访问和全局流行是强的平凡基线，RDL 经常大胜。只在该设置下成立。Amazon 购买上两层 GraphSAGE 的 0.74 确实高于 0.24 和 0.06；H&M 上两层 GraphSAGE 的 0.80 低于历史访问 0.89。赢的是 ID-GNN 那一列的 2.81，不是任意一个 GNN。
- 数据科学家写 SQL 特征再接 LightGBM，是推荐系统里「SQL 出 top-K」的对照。不成立。15 个任务全是实体分类和回归，平均 12.3±1.6 小时，SQL 产出的是特征列。
- 时间采样系统性地避免泄漏。只在该设置下成立。他们自己写了设计者有责任，而且正文的 “before” 和 Fey 公式的 \(\le\) 并不相同。
- 库里没有自然语言查询，所以不能当 ACL 的语言实验。站得住。这是任务定义的事实，不是我们追加的解释。

### RelBench v2（arXiv 2602.12606，ICLR 2026 DATA-FM workshop）

- 推荐仍然报 MAP@K，基线仍然是历史访问、全局流行、带这两种秩特征的 LightGBM。站得住。表 10 和表 20 的刻度和 v1 一样是百分数风格。表 10 里新任务的测试均值：历史访问 7.45，全局流行 10.61，LightGBM 13.96，四层 ID-GNN 23.35。这些是新任务，不能和 H&M 的 0.89 放进一张表比高低。
- 四层 GraphSAGE 在 80GB A100 上显存失败，所以推荐是多跳的。只在该设置下成立。失败写在 RateBeer 上。H&M 的四层有结果，而且更差。多跳这个解释不能从 H&M 的四层格读出来。
- 现有 RelBench 推荐任务的官方指标是 MAP@10。不成立。见上面的 `eval_k`。表 25 的冒烟小数也不能改表 5。
- 附录 E.3 的 TGB 移植写 “only use historical events up to the validation cutoff”。那是移植实验的协议，比主榜更严：测试也不能用验证截止之后的边。不要把这句话误当成 H&M 主协议。H&M 测试的官方历史访问使用了验证窗。

### ContextGNN（ICLR 2025，arXiv 2411.19513）

- 表 2 是百分数，H&M 和 Amazon 购买的测试格是 2.93。站得住。
- 双塔模型抓不到成对信号，ContextGNN 平均比最好的双塔高 344%，比 NBFNet 高 20%。只在该设置下成立。测试集平均 NBFNet 7.71、ContextGNN 9.23，相对差大约两成，和正文一致。H&M 上相对 NBFNet 只从 2.81 到 2.93，他们也写了高局部性任务上的增益大约 3% 到 5%。344% 是对双塔的平均相对数，不能单独拿来形容 H&M。
- H&M 用户会频繁重复购买衣服。只在该设置下成立，而且用词强于数字。1 跳局部性是 0.048，也就是测试正例里 4.8% 落在用户自己的历史上。相对 Amazon 的 0.001 它更高；作为绝对覆盖率它不高。历史访问仍能到 0.89 个百分点，是因为这 4.8% 被排得很靠前，再加上 MAP 只在有正例的源实体上平均。
- 局部成对模型的候选出不了子图，所以需要双塔兜底。站得住，这是他们相对 NBFNet 的结构论点。它同时说明：一条只在用户子图里取共现邻居的 SQL，和 ContextGNN 的全目录双塔不是同一个候选集。H&M 上 3 跳也只盖住 41.7% 的正例。
- Amazon-Book 的 Recall@20 是 0.0451，IJCAI 的 HR@1 是 0.411。只在该设置下成立。前者是静态、无时间的小图；后者是每个实体 99 个抽样负例。两格都不能换算成 RelBench 的 MAP。
- 训练时类别可以到大约 100 万、15GB 显存。只在该设置下成立，说的是他们的采样训练，不是允许特征看到未来。

### Fey 等，关系深度学习框架（arXiv 2312.04615）

- 消息传递就是 SQL 的 `JOIN` 加 `AGGREGATE` 的可学习版本，GNN 是它的神经网络形式。只在该设置下成立。他们说的是一层聚合的函数形式可以写成对邻居的聚合。这不推出一条手写连接的 MAP 等于训练后的 GNN，也不推出没训练的连接会输。H&M 上没训练的历史访问已经高于两层 GraphSAGE，这个事实在 v1 里，不在这篇里。
- 第一版 RelBench 只有节点级任务。站得住，而且因此这篇没有推荐数字。推荐是后来的 v1 基准论文加上去的。
- 时间一致的计算图只用种子时间之前的邻居。公式站得住，正文的 “before” 比公式宽。采用 \(\tau(w) \le t\)。

### Wydmuch 等（arXiv 2411.11829）

- 预测时间 \(t_p\) 只能使用 \(t_v < t_p\) 的其他实体。这是他们对 RelBench 的转述，转述本身站得住。它比 Fey 的 \(\le\) 和 ContextGNN 的 \((-\infty, T]\) 更严。先导若写「严格早于」，引用的是这篇，不是 GNN 的采样实现。
- 把关系行写成 JSON，Llama 3.2 1B/3B 加一个小 MLP，就能在实体任务上接近或超过 RDL。只在该设置下成立。表 1 和表 2 只有分类 AUROC 和回归 MAE。测试点超过 10 万的任务被抽成 1 万。没有 MAP，没有推荐，模型也不输出 SQL。
- 由此得到「LLM 已经会做 RelBench 推荐」或「LLM 写的 SQL 就是排序」。不成立。这篇没有做这两件事。

### Kumo PQL（产品文档，不是论文）

当天直接请求 `https://docs.nvidia.com/sdgm/reference/rank` 返回 404。打开并读到的是跳转后的 Kumo Engine 页面：[Personalized Email Recommendations](https://docs.nvidia.com/sdgm/kumo-engine/get-started-with-kumo-engine/workflows-and-solutions/personalization/personalized-email-recommendations)。上面的查询是：

```text
PREDICT LIST_DISTINCT(transactions.item_id, 0, 14, days) RANK TOP 12 FOR EACH users.user_id
```

同一页写 `query.get_task_type()` 的结果是 `temporal_link_prediction`，排序来自已经拟合的 `trainer.predict(...)`。返回列是 `ENTITY`、`CLASS`、`SCORE`。页面明确分数不是购买概率，邮件资格和商品是否可推荐是预测之后的 pandas 过滤。

另一份当天打开的客户端文档 [Query Kumo Relational](https://docs.nvidia.com/sdgm/client/kumo-relational/user-guide/make-predictions/querying-rfm) 写：当前校验器里 `RANK TOP K` 必须用 `materialize(..., candidates=...)` 显式给出候选，不会默认有一个候选集，而且每个候选一次调用。这和「一条 SQL 在库里执行完就得到 top-K」不是同一个执行器。

主张「PQL 证明 SQL 可以做推荐」。不成立。语法长得像带时间窗的 `LIST_DISTINCT` 加 `RANK`，执行器仍是关系模型。主张「RelBench 推荐任务的形状和这种预测查询相同」。站得住：未来窗口里的去重目标列表，再取 top-K。这只说明任务形式，不说明我们的手写连接已经有人试过。

搜索索引里还留着旧参考页的句子：`PREDICT LIST_DISTINCT(transaction.article_id, 0, 30) RANK TOP 12`，以及排序最多 1,000 个目标、实体规模到 10,000,000。那一页当天没有打开成功，不当成已核对的产品限制。

### RelAgent（arXiv 2605.07840，NeurIPS 2026）

- 智能体写 SQL 特征程序，在 LightGBM、XGBoost、CatBoost 等七个树模型里选择，推理时不再调用模型。站得住，范围是实体分类和回归。他们评的是 RelBench v1、v2（不含 MIMIC）和 4DBInfer，指标是 AUROC 和标准化 MAE。
- SQL 的执行结果就是推荐列表。不成立。预测器是「SQL 特征图加上经典模型」。推荐任务不在实验里。

### ReFuGe（arXiv 2601.17735，WWW 2026）

- 模式选择、特征生成、特征过滤三个智能体写出关系特征，接 LightGBM，在 11 个实体分类任务上比 AUROC。站得住，表 1 就是这些任务，其中包括 H&M 的 user-churn，不是 user-item-purchase。
- 这覆盖了 RelBench 的推荐，或产出了 top-K。不成立。下载到的 4 页 PDF 没有 MAP，也没有推荐任务。文中指向的提示词附录不在这份 PDF 里。

## 对两周先导的直接后果

H&M 购买仍然是该跑的那一个：一个种子、7 天、K=12、10.6 万篇文章、1,666 万行，CPU 上的 DuckDB 够用。先复现历史访问的 0.89。共现 SQL 使用 `t_dat <= 2020-09-14` 的预聚合，验证用另一张切在 2020-09-07 的表。不要把没超过 0.89 写成「协同连接没有信息」；表里的近邻模型已经给了这个不利先验，而 3 跳局部性 0.417 说明子图里仍有正例。超过 0.89 之后，对照依次是全局流行 0.30、两层 GraphSAGE 0.80、ID-GNN 2.81、ContextGNN 2.93。超过历史访问不等于接近 ContextGNN。

Amazon 购买留作第二次，而且第二次的线不是 0.06。全局流行 0.24 和 GraphSAGE 0.74 才是这条 SQL 该面对的数。标签窗按 91 天写进查询，不按文档字符串里的两年。product 表的行数在开查之前从 parquet 的元数据读出来，不沿用 12,562,384。

14 个任务不改写成语言实验。PQL 的 `RANK TOP` 可以在相关工作里出现，并写明执行器是模型、文档是产品文档。RelAgent 和 ReFuGe 只说明「模型写特征 SQL，树模型出分类或回归分」，不能用来声称已经有人用 SQL 的结果集交了 MAP。
