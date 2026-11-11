# 03 benchmark

日期：2026-11-11。本窗口核对基准能不能承载「模型把关系片段写成 SQL，数据库返回候选」。主实验仍是 STaRK-Amazon 的全库检索。InteRecAgent 归 02，QUEST 归 04，RecBench+ 归这里。输出写到 `proposal/sql-recall/deep/reanalysis/window-03.md`。

## 这个窗口要回答的问题

1. STaRK-Amazon 全库上，关系片段写成 SQL、文档上另排、关系片段和整句分开报、人工 81 条另表：这些数测过没有？要打的全库基线是不是表 6 的 BM25？
2. 硬属性过滤上「工程师写死的 SQL」是不是假空？合成标签落在关系候选里，只执行关系模板是构造的逆运算，没有排序就没有第一名。
3. RecBench+ 若做电影显式条件，相关集是不是式 (7)？历史子集 Precision，以及表 2 的生成式 Precision 0.308 和 CMR 0.714，为什么不能进检索主表？网格已经规定不能进。本窗口核对式 (7) 和表 2 的分母。
4. Amazon-C4 上精确 SQL 会不会输，测过没有？网格写论文没有 SQL 行，「会输」还不是结论。负对照的池子、标签和编码字段以哪张表为准？测赢了先查什么泄漏？
5. 半结构化检索留下的是关系片段加上文档排序，不是再做一个语义 ID。TalkPlay 的 Semantic ID 是不是因为上下文里已经有码，所以这一格是假空，不能替换 STaRK？

## 不要做的事

- 不要写「Amazon-C4 上精确 SQL 一定会输给嵌入」。论文没有 SQL 或 BM25 的行，「会输」必须先测再写。
- 对标题做 `LIKE` 论文没测，不能事先写成一定输。测赢了先查品类或标题泄漏，不写成主结论。
- 不要把合成集上只执行关系模板的集合召回，或纯 SQL 的 Hit@1，当主结果。Recall@20 可以照官方协议报，不能按「完美系统应接近 1」来读。
- 不要把 RecBench+ 的历史子集 Precision，以及表 2 的生成式 Precision 0.308 和 CMR 0.714，放进检索主表。
- 不要把 EComAgentBench、REGEN、TalkPlay-Tools、AgentRecBench 换到主实验的位置。
- 合成全测试集与人工 81 条不要合成一个平均数。Claude3 的 53.09 是 top-10 重排，不进主表。

## 论文清单

重析写过 8 篇。InteRecAgent 归 02，本表不列；本地另一份在 `papers/sql-recall/03-benchmarks/interecagent-2308.16505.pdf`，不要在这里重析。QUEST 以及 STaRK 的后续方法 AvaTaR、KAR、MoR、SPARK 归 04。

| 文章名称 | 场合或 arXiv | 本地 PDF 路径 | 这个窗口要核对的分析要点 |
|---|---|---|---|
| STaRK：Benchmarking LLM Retrieval on Textual and Relational Knowledge Bases | NeurIPS 2024 Datasets and Benchmarks；arXiv:2404.13207v3 | `papers/sql-recall/03-benchmarks/stark-2404.13207.pdf` | ① 表 6 合成 Amazon 的 BM25 从 PDF 重抄 Hit@1、Hit@5、Recall@20、MRR。网格写 44.94、67.42、53.77、55.30。不要改用 mFAR 表 1。② 表 3 的平均答案数、多答案条数从 PDF 重抄。笔记写平均 17.99；正文 68% 与表 3 的 7,082/9,100 不一致，引用比例用表 3。「答案都不超过 20」与第 2.5 节约 22% 多于 30 对不上。③ 表 7 人工集 BM25 的 Hit@1 与 MRR。笔记写 Hit@1 27.16、MRR 18.79，后者低于前者，和论文自己的 MRR 定义冲突。Claude3 的 53.09 是 81 条上对 ada-002 top-10 的重排。④ 隐含假设：「similar」没有规定落到 `also_bought` 还是 `also_viewed`。没有 `ORDER BY` 就没有 Hit@1。MAG、Prime 不换成主实验。 |
| RecBench+（首页标题：Towards Next-Generation Recommender Systems: a Benchmark for Personalized Recommendation Assistant with LLMs） | 页眉 WSDM ’26 | `papers/sql-recall/03-benchmarks/recbenchplus-2503.09382.pdf` | ① 式 (7) 把标准答案定义成知识图谱上属性包含 \(C_{shared}\) 的全部物品。显式条件的相关集是这张全目录条件表，不是历史子集。② 表 2 的生成式 Precision 和 CMR 从 PDF 重抄。笔记写 0.308 和 0.714，并写测试时目录不在提示里。这两格不进检索主表。③ 历史子集当 Precision 会罚掉「返回全部满足条件的电影」；当 Recall 则返回整张影片表也能满分。CMR 要和全目录条件召回一起报。④ 错误信息条件仍用原来的 \(C_{shared}\)，不用那句假话。画像式标签是历史共现或人群热门，系统却在没看目录的情况下生成标题。归本窗口。 |
| BLaIR / Amazon-C4 | ACL 2026 长文 | `papers/sql-recall/03-benchmarks/blair-2026.acl-long.147.pdf` | ① 表 3 的 Amazon-C4 物品数、测试查询数从 PDF 重抄。笔记写池子 1,058,417，不是全文的 4,800 万；同品类负例是每条正例 50 个。② 表 10 的 NDCG@100 从 PDF 重抄。笔记写 text-embedding-3-large 0.1856、GritLM-7B 0.1845。③ 主实验编码的是标题还是描述。论文有没有 SQL 或 BM25 行。④ 标签是写这条 5 星评论的那一件商品。没有品牌、价格、颜色列上的金 SQL。Reddit-Movie 的 GritLM NDCG@100 若是 0.0734，不要拿它替换这个负对照。 |
| EComAgentBench | EMNLP 2026 Industry | `papers/sql-recall/03-benchmarks/ecomagentbench-2026.emnlp-industry.61.pdf` | ① 有效划分的条数从 PDF 重抄。笔记写 662 条，一次交一件。主指标不是候选列表的 Recall 或 NDCG。② PDF 有没有可执行的模式。没有的话，不要把仓库脚本里的列当成这篇论文的句子。③ 可见问句、人设、澄清是三处。评测前把人设和澄清拼进问句，会把准确率抬高。④ `review_opinion` 仍在 SQL 外面。`entity_match` 若对标题做子串，核对这个短语是不是构造时从标题抄进去的。 |
| REGEN：A Dataset and Benchmarks with Natural Language Critiques and Narratives | arXiv:2503.11924。重析未印会议名 | `papers/sql-recall/03-benchmarks/regen-2503.11924.pdf` | ① 标签是序列上的下一个物品 id，不是用户句子里的谓词。表 1 的 Office、Clothing 规模从 PDF 重抄。② Hist. 与 Hist.+Critique 的下一物品分数从 PDF 重抄。笔记写不要拿 Hist.+Critique 的 0.1402 当主结果，因为短评生成时看过目标。③ Office 约 17.6%、Clothing 约 18.6% 的相邻对有短评。不要把这个子集说成整个目录上的约束推荐。④ 隐含假设：用短评里的标题词做过滤或 `LIKE`，再报 Recall@10，会把数字说得比系统好看。 |
| TalkPlay-Tools | arXiv:2510.01698v4。重析未印会议名 | `papers/sql-recall/03-benchmarks/talkplay-tools-2510.01698.pdf` | ① SQL 是不是单表 `tracks` 上的布尔过滤，另有 BM25。它支持工具形状，不替换 STaRK-Amazon。② 表 2 的 Hit@1、Hit@10、Hit@20 从 PDF 重抄。笔记写 BM25 为 0.017 / 0.073 / 0.107，加上工具调用为 0.022 / 0.082 / 0.111。③ 生成参数是不是 temperature=0.6、top_p=0.95，不是温度 0。④ 用户到物品的高成功率若来自把上下文里已有的用户 id 填进去，不要当成推荐质量。Semantic ID 成功率高，要核对上下文里是不是已经有码。 |
| AgentRecBench | arXiv:2505.19623v2。重析未印会议名 | `papers/sql-recall/03-benchmarks/agentrecbench-2505.19623.pdf` | ① 每条测试是不是 20 个候选：1 个正例加 19 个负例。名单已经切好，没有全库召回可以换成 SQL。② 表 2、表 3、表 4 报的是 HR@1、HR@3、HR@5 的平均，还是单独的 HR@1。从 PDF 重抄，并核对对照里的 15.0 是什么模型。③ 图 5 的输出格式是否禁止引入这 20 个以外的 id。④ 冷启动的 m 和 n，正文若没给数值，不要补。 |

## 交给这个窗口的写法

对上表每一篇按五步写完，不要跳步：（1）逐段提取核心论点和论据（2）论点之间的因果、递进、转折、并列（3）未明说的隐含假设（4）证据强度和推理漏洞（5）最终结论。数字从 PDF 抄，不从旧笔记或本大纲转写。输出写到 `proposal/sql-recall/deep/reanalysis/window-03.md`。不要重析 InteRecAgent、QUEST、AvaTaR、KAR、MoR、SPARK，也不要重析归 01、02、05 的论文。
