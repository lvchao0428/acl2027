# 候选 benchmark

> 2026-11-11 核对。数字来自当天打开的论文、榜单或官方代码。
> 总览和先导实验在 [00_总览](00_总览.md)。

没有一个公开集同时具备自然语言推荐请求、用户到用户图、物品到物品图，以及官方的全库 Recall@K。下面按「SQL 能替换哪一步」排。协议分三种：全库检索、给定短名单后重排、模型凭记忆生成标题。

| 数据 | 场合 | 协议 | 规模 | 能装进表的 | 要打过的数字 | SQL 能换的那一步 |
|---|---|---|---|---|---|---|
| [STaRK-Amazon](https://arxiv.org/html/2404.13207) | NeurIPS 2024 D&B | 全库 | 合成查询 9,100，其中 7,082 条多答案；人工查询 81。约 90 万商品、940 万边 | `also_bought` 280 万、`also_viewed` 190 万、品牌、颜色、品类。HF `snap-stanford/stark` | 合成全测试：ColBERTv2 Hit@1 46.10；BM25 44.94 / 67.42 / 53.77 / 55.30（Hit@1 / Hit@5 / R@20 / MRR）；ada-002 Hit@1 39.16。人工 81 条：Claude3 重排 Hit@1 53.09 | 稠密检索。没有用户表，做不了 U2U |
| [RecBench+](https://github.com/jiani-huang/RecBenchPlus) | arXiv 2503.09382；DOI 10.1145/3773966.3777954 | 生成标题 | 电影 19,529 题、3,247 物品；图书 14,965 题 | 电影：`movies.dat`、`ratings.dat`、`users.dat`，以及 21,797 条维基 infobox。`KG.dump` 只有 6.4KB，不是可用的图 | 电影显式条件，GPT-4o：Precision 0.308，Recall 0.408，CMR 0.714。这些系统没看过目录 | 改成检索之后，过滤和共看连接才有意义。官方分数不能直接比 |
| [Amazon-C4 / BLaIR](https://aclanthology.org/2026.acl-long.147/) | ACL 2026 | 全库 | 21,223 条查询，池子 1,058,417 件。查询由 5 星评论改写 | 只有品类字符串，加标题和描述拼在一起。HF `McAuley-Lab/Amazon-C4` | NDCG@100：text-embedding-3-large 0.1856，GritLM-7B 0.1845 | 嵌入检索。精确 SQL 在这里应该输 |
| [EComAgentBench](https://github.com/Morizeyao/EComAgentBench_) | EMNLP 2026 Industry | 智能体选一件 | 662 个任务；约 370 万商品、2,140 万评论。库文件 26.9GB | 已经是 SQLite：`brand, price, average_rating, main_category`。`bought_together` 被丢掉了 | Claude Opus 4.6 准确率 57.1% | 替换 FTS 搜索工具。没有 I2I 或 U2U 边 |
| [REGEN](https://arxiv.org/abs/2503.11924) | arXiv | 序列下一个物品 | Office 89,489 条序列、27,887 件物品 | 品类、描述、价格，以及部分相邻物品之间的短评 | 历史加短评，Recall@10 0.1402，NDCG@10 0.113 | SQL 只适合放在排序器前面，把短评里的属性变成过滤 |

另外核对过、但不作主实验的：iAgent 的 InstructRec 和 AgentRecBench 都是 10 或 20 个候选上的重排，名单已经切好，没有全库召回可换。POINTREC 只有 112 条人工叙事。APeB 是给定名单。QUEST 是维基实体的集合运算，不是推荐。KuaiSAR、Qilin、RecFlow、Yambda 是交互日志，没有自然语言推荐请求。TREC 2023 的推荐轨从 ASIN 出发，搜索轨只有 186 条查询。

RecBench+ 的发布文件需要单独记住。查询 JSON 里有 `sharedRelationships`、`movieSubset` 和电影 id，条件标签可以重建。评分文件是真实的 MovieLens。维基 infobox 按标题索引，没有 MovieLens id，标题对齐会有噪声，这一步还没量过覆盖率。论文里式 (7) 把标准答案定义成知识图谱上所有满足条件的物品，发布的评测脚本用的却是该用户历史里满足条件的子集。两个标签故意不一样：论文发现历史会抬高 Precision、压低 CMR。SQL 系统如果返回所有符合条件的电影，会被历史子集的 Precision 罚到。两个数都要报。

### 6.1 先导实验就用这三个

1. **STaRK-Amazon，主实验。** 输入是自然语言，池子约 90 万，指标是 Hit@k、Recall@20、MRR 和延迟。`also_bought` 就是 I2I 连接。BM25 已经打过 ada-002，结构化检索有空间；每条查询还有文本半边，纯 SQL 吃不满标签。合成查询先抽关系模板，再让模型按文本筛候选，所以只执行模板的 SQL 是最终答案的超集。关系片段和整句要分开报。81 条人工查询是模板解析器背不下来的那一组。公平的系统是：SQL 取出关系超集，再用 BM25 或小编码器在商品文本上排序。只报合成集上的 SQL-only Hit@1，会比系统实际的能力好看。单张 A100 上 ada-002 是 5.71 秒，GPT-4 重排是 24.76 秒，延迟就跟这两个比。商品文本约 5.92 亿 token，编码是贵的那一步；SQL 本身是 CPU。
2. **RecBench+ 电影，显式和隐式，改成检索协议。** 最贴近「精确过滤加用户历史」。官方任务是凭记忆生成标题，不能把 0.308 和 0.714 当成检索基线，论文里要写明那些系统没看过目录。新协议：用情景问句，对 `movies`、`ratings`、`movie_info` 建的表做检索；约束满足按全目录上的 `sharedRelationships` 算，Precision、Recall、NDCG 按 `movieSubset` 算，并且放在排序之后。图书没有作者和品类表，不进第一轮。
3. **Amazon-C4，负对照。** 要替换的就是 1,058,417 件上的嵌入点积，NDCG@100 的 0.1856。发布的物品记录是品类加一段标题描述，查询是评论改写（「给孩子洗澡时解闷」），精确 SQL 应该输。这个负结果用来说明 STaRK 或 RecBench+ 上的正结果不是「SQL 什么都能赢」。同一张表里的 Reddit-Movie 是 1,627 条真实帖子、51,203 部电影，GritLM-7B 的 NDCG@100 是 0.0734，编码字段只有标题和年份。

EComAgentBench 留作备份：已经是一个 SQL 文件加购物请求。662 条撑不起一篇。很多要求藏在人设和澄清里，只对可见问句做 Text-to-SQL 是错的系统。
