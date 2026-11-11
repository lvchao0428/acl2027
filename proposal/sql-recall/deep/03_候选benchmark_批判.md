# 候选 benchmark 批判

> 2026-11-11。读的是当天下载的 PDF，以及发布文件里能小规模打开的部分。PDF 在 `papers/sql-recall/03-benchmarks/`。
> 没有下载 STaRK 的 `skb/amazon/processed.zip`（3,524,776,983 字节）、Amazon-C4 的 `sampled_item_metadata_1M.jsonl` 全文（643,452,148 字节，只取了第一行）、EComAgentBench 的 `product.db`（数据集卡写 26.9GB）。
> 下面凡是我自己数出来的，都标明「发布文件」。论文表格里的数字另标表号。

## 结论

主实验仍然应该是 **STaRK-Amazon**。协议维持总览里的那条：模型只把关系片段写成 SQL，文本仍交给 BM25 或小编码器，关系片段和整句分开报。换主实验的理由不成立。RecBench+ 的官方分是生成式的，而且历史子集 Precision 会罚掉「把满足条件的电影都返回」的 SQL。Amazon-C4 继续当负对照，但「SQL 会输」是推断，论文没有测过 SQL。

三条必须改口的地方：

1. 合成查询上，只执行关系模板的 SQL 返回的是标签的超集。集合召回会被构造过程抬高。Hit@1 不会自动变高，因为 Hit@1 要有序，论文也没有公布筛选前的候选集有多大。
2. 81 条人工查询不是四个模板填出来的，解析器背模板字符串解决不了它们。它们也不是「模板解析器一定解析不了」的证明：不少句子仍然点了品牌、颜色、品类或另一件商品，同时夹着图里没有的价格、尺寸和兼容关系。
3. 论文用「所有查询的答案个数都不超过 20」来解释为什么报 Recall@20。发布的 Amazon 合成文件里，9,100 条中有 2,720 条答案多于 20 个，最长 100。这句话与文件不符。

## STaRK

- 原文：`papers/sql-recall/03-benchmarks/stark-2404.13207.pdf`（25 页，含附录 A–E）
- URL：<https://arxiv.org/pdf/2404.13207>
- 查询文件：Hugging Face `snap-stanford/stark`，`qa/amazon/stark_qa/stark_qa.csv`（2,787,755 字节，9,100 行）和 `stark_qa_human_generated_eval.csv`（22,231 字节，81 行）。两份都只有 `id, query, answer_ids`。
- 数据集卡：<https://huggingface.co/datasets/snap-stanford/stark>

### 创新点，以及证据落在哪

1. **半结构化检索**：查询同时要关系约束和文本约束，答案是图上的节点（第 2.1 节）。证据是三个 SKB 上的全库检索，不是给定 10 个或 20 个候选。合成查询由流水线生成；人工查询另有一组。Amazon 的检索池在论文里是整张 SKB，不是短名单。
2. **用关系模板加文本筛选自动造标签**（第 2.4 节，图 3，附录 A.2、E）。这是数据构造，不是系统结果。标签质量的人工核对是 63 名参与者对抽样查询打自然度、多样性和实用性（附录 D.1，表 10），不是对「SQL 能否还原模板」的实验。
3. **BM25 在合成测试上接近稠密模型**。表 6「Full Testing Dataset」、STARK-AMAZON：BM25 的 Hit@1 / Hit@5 / R@20 / MRR 是 44.94 / 67.42 / 53.77 / 55.30；ada-002 的 Hit@1 是 39.16；ColBERTv2 的 Hit@1 是 46.10（同行 Hit@5 66.02，R@20 53.44，MRR 55.51）。这是全测试集上的检索，不是重排。
4. **LLM 重排能抬高 Hit@1**。第 3.1 节写明：重排的是 ada-002 的 top-k，合成查询 k=20，人工查询 k=10；合成集上因为贵，只评了测试查询的随机 10%。表 6 里 Claude3、GPT-4 两行都在「Random 10% Sample」下面。表 7 人工 Amazon 的 Claude3 Hit@1 是 53.09，这一格是 81 条上的重排，不是从 90 万节点里检索。53.09% 与 43/81 对齐（42/81=51.85，44/81=54.32）。
5. **人工查询作为另一套参照**（第 2.6 节，附录 C）。Amazon 81 条，表 3：其中 64 条多答案，平均答案数 19.50。发布文件数出来是平均 19.49，单答案 17 条，与「64 条多答案」一致。

延迟在表 8，单张 A100-SXM4-80GB：Amazon 上 ada-002 是 5.71 秒，Claude3 重排 27.24 秒，GPT-4 重排 24.76 秒。正文写 ada-002 的耗时来自多次 API 调用，不全是这张 GPU 的计算时间。

### 关系模板和文本筛选

附录 A.1 的 Amazon SKB：约 100 万实体（商品约 90 万，品牌约 10 万，品类 1.4k，颜色 1.7k），约 940 万关系（`also_bought` 280 万，`also_viewed` 190 万，`has_brand` 170 万，`has_category` 230 万，`has_color` 60 万）。表 2 的精确总数是 1,035,542 个实体、9,443,802 条关系、592,067,882 个 token、平均度 18.2。商品节点没有精确到个位，附录用的是「0.9M」。`processed.zip` 有 3.52GB，这次没有打开，所以没有从原图里再数一遍商品节点。

附录 A.2 的基本模板只有四条，而且写明最终模板可以由多条拼起来：

| 元路径 | 模板句 |
|---|---|
| brand → product | "Can you list the products made by \<brand\>?" |
| product → product | "Which products are similar to \<product\>?" |
| color → product | "Can you provide a list of products that are available in \<color\>?" |
| category → product | "What products are available in the \<category\> category?" |

「similar」对应商品到商品的边。图里的商品—商品关系只有 `also_bought` 和 `also_viewed`，模板句没有写死是哪一种。

第 2.4 节的四步，图 3 画的是同一件事：

1. 抽一个关系模板并填上实体。这一步得到候选节点，例子是 Radio Flyer 的全部商品。
2. 从候选里随机抽一个 gold，让 LLM 从它的文档里抽文本属性。
3. 两个 LLM 把文本属性和关系要求写成自然语言。
4. 多个 LLM 检查第 1 步的候选是否满足这些文本属性。**全部验证通过的候选才进入最终标签。**

所以，合成标签是关系候选集被文本筛选之后的子集。gold 本身被验证通过的比例，论文写成 86.6%、98.9%、92.3%，「on the three datasets」，没有点名哪一个是 Amazon。附录 E 的表 11：Amazon 的文本抽取用 `gpt-3.5-turbo-16k`；三套数据的融合用 `claude-2.0` 和 `gpt-4-0125-preview`；筛选用 `claude-2.1`、`claude-2.0`、`claude-instant-1.2`。

发布的 CSV 没有模板编号，也没有筛选前的候选集。不打开那 3.52GB 的图，就不知道超集比标签大多少。

### 纯 SQL 的高 Hit 是不是虚高

分两截。

**集合召回是虚高的。** 第 4 步把标签定义成关系候选里通过文本验证的那些节点。只执行模板的 SQL 把第 1 步的候选集取回来，合成标签落在这个集合里面（gold 若没通过验证会被拿掉，所以是「筛选后的子集」，极端情况下原来的 gold 不在最终标签里）。在合成集上报告「SQL 结果覆盖了标准答案」，测的是构造过程的逆运算。第 2.3 节自己也写了：Amazon 任务把文本属性（质量、功能、款式）和单跳关系放在同一句里。关系 SQL 没有做文本那一半。

**Hit@1 不会因为这件事自动变高。** 第 3.1 节的 Hit@k 看的是有序列表的前 k 个。SQL 没有 `ORDER BY` 就没有 Hit@1。若在超集里随机排，Hit@1 的期望是 `|标签| / |关系候选|`。论文没有给筛选前的候选集大小。表 3 的合成 Amazon 平均答案数是 17.99；发布文件里 9,100 条答案列表长度之和是 166,363，平均 18.28，中位数 7，最大 100，其中 12 条刚好是 100。中位数 7 说明多数查询的标签不大，但品牌或品类的候选可以比 7 大很多：附录的 `has_category` 约 230 万条、品类实体 1.4k，品类模板的候选是千这个量级，随机 Hit@1 会很低；`also_bought` 约 280 万条、商品约 90 万，邻居模板的候选很小，随机 Hit@1 可能不低。两种模板的虚高程度不一样，发布文件区分不了每条查询用的是哪一种。

因此：合成集上只报 SQL-only Hit@1，在候选集很小、而且文本筛选几乎没删人的那些查询上，会把系统说得比「整句都做对了」更好看；在品类这种大候选集上，同样的 SQL 会很难看。两种方向论文都没有测。公平的主结果仍是「SQL 取出关系超集，再在商品文本上用 BM25 或小编码器排序」，并且关系片段和整句分开报。

另外，表 6 的 Hit@1 已经有 44.94（BM25）。表 3 写 7,082 / 9,100 条有多个答案，平均 17.99 个。多答案会抬高「任一相关物品出现在第一名」的 Hit@1。这是指标定义带来的，不只是 SQL 的问题。正文第 2.3 节另写「68% 的合成查询有多于一个答案」，与表 3 的 7,082/9,100（77.8%）对不上。以表 3 和 CSV 为准，CSV 里单答案是 2,018 条，多答案 7,082 条。

### Recall@20 的理由是错的

第 3.1 节：「For synthesized queries, k = 20 is used, as the answer length of all of the queries in our benchmarks are equal or smaller then 20.」

发布的 `stark_qa.csv`：2,720 / 9,100（29.9%）的答案个数大于 20，2,001 / 9,100（22.0%）大于 30。22% 与正文第 2.5 节「about 22% of the answers have more than 30 entities」一致。大于 20 的那 2,720 条，即使排序完美，Recall@20 也到不了 1。人工 81 条里有 28 条答案多于 20，同样的句子也不成立。先导仍然可以报官方的 Recall@20，但不要把「完美系统应接近 1」写进预期。

### 81 条人工查询，解析器背不背得下来

附录 C 的指令是：给一个随机实体，让参与者同时看文档和邻接结构，写出一个该实体能满足的查询。三条限制：不要泄露这个实体的名字；不懂可以跳过；**表达方式没有限制**（"There is NO restriction on how you express the queries."）。31 人写了三个 SKB 共 263 条，其中 22 人是英语母语者。答案由人工筛选，不是模板候选再过一遍 LLM。

因此这 81 条不是 A.2 四个模板填槽填出来的。背下那四句模板、再按字符串匹配，解不了它们。第 2.6 节的差别也是这条：人工查询有更特别的说法，例子是 "Give me a fat cross and road tire that works with my Diamondback bicycle tube"。发布文件第 77 条就是 "Give me a fat cross and road tire which works with my Diamondback bicycle tube."，与论文例子是同一条。`works with` 不是 `also_bought` 或 `also_viewed`。

「解析器一定解析不了」过了。我通读了 81 条。有的句子就是模板能接住的碎片，再加图里没有的条件，例如：

- 第 23 条："What's a good 7 foot long fishing rod made by the brand Zebco?" 品牌和品类在四条元路径里，7 英尺不在。
- 第 31 条："Could you recommend a pistol laser sight made by Sightmark?" 品牌加品类。
- 第 2 条："I just bought a Forest Byke Company Derailleur Hanger 65, please recommend me something similar from x5." 「similar」像商品—商品模板，`x5` 又像品牌。
- 第 0 条："I like playing card games. I want a box to hold my card games. I have around 1000 cards." 58 个答案。决定答案的是容量和用途，五类关系里没有这些列。

第 2.6 节同时写了另一面：人工查询的多数风格在合成集里出现过，答案个数也相近（表 3：合成平均 17.99，人工 19.50）。所以 81 条是「模板字符串背不下来、关系碎片仍可能被抽出来、文本一半和额外谓词抽不出来」的那一组。论文没有跑过模板解析器。81 条上 Hit@1 每错一条约动 1.2 个点，只能当核对，不能当主表的唯一胜负。

表 7 还有一个内部矛盾：STARK-AMAZON 的 BM25，Hit@1 27.16，MRR 18.79。第 3.1 节把 MRR 定义成第一个相关物品的秩的倒数的平均，这个定义下 MRR 不会低于 Hit@1。同表 ada-002 是 39.50 对 52.65，Claude3 是 53.09 对 62.11，都不违反。BM25 这一格，PDF 文本层和版面都是 18.79。人工集上若要比 MRR，不要把 18.79 当成可靠靶子。Hit@1 27.16 与 22/81 对齐，这一格没有同样的矛盾。

人工标签是人筛的，不是「模板候选的子集」。合成集上那种「SQL 超集覆盖标签」的构造，不能搬到这 81 条上。

## RecBench+

- 原文：`papers/sql-recall/03-benchmarks/recbenchplus-2503.09382.pdf`（10 页，页眉是 WSDM ’26）
- URL：<https://arxiv.org/pdf/2503.09382>
- 代码与数据：<https://github.com/jiani-huang/RecBenchPlus>
- 评测脚本：`eval/eval_movie.py`。模式：`eval/movie-schema.json`。

### 创新点，以及证据落在哪

1. **五类查询**（条件式三种：显式、隐式、错误信息；画像式两种：兴趣、人口统计）。条件来自用户历史里共享的知识图谱关系，查询由 GPT-4o 生成（式 (5)）。兴趣查询和人口统计查询的标签是「常见后续电影」或「该人群看过的热门电影」（第 1.3 节）。全部是合成查询。
2. **CMR**（第 2.1.2 节）：推荐列表里满足条件的比例。表 2 的数字来自模型凭记忆生成标题。附录 A 的测试提示词是「You are a movie recommender system. You are given a query from the user. … Please output the recommended movies directly」。没有把目录放进提示词。
3. **历史会改变生成结果**（观察 4，图 5）。这是提示词里加不加观影历史的消融，仍然是生成式。正文写：加历史会在各类查询上提高 Precision；CMR 不一定提高，因为历史会带进不满足条件的干扰项。图 5 没有把柱子的高度印成数字，这里不引用图上的读数。

表 1：电影查询一共 19,529，物品 3,247，用户 6,036，交互 29,459。显式条件按条件个数是 2,225（1 个）、2,346（2 个）、426（3 或 4 个），合计 4,997。发布的 `ExplicitQuery.json` 也是 4,997 条，`condition_num` 为 1/2/3/4 的条数是 2,225 / 2,346 / 334 / 92，后两个加起来 426。图书 14,965 条、50,088 个物品。这次只拆了电影显式文件。

表 2 电影、显式、GPT-4o：Precision 0.308，Recall 0.408，CMR 0.714，FTR 0.016。列顺序与表头一致：每个难度下是 P、R、CMR、FTR，最后一组平均只有 P、R、CMR。这些系统没看目录。FTR 在脚本里是输出里有没有 `[SEP]`，SQL 执行用不上。

### 式 (7) 和发布的评测脚本

式 (7) 把标准答案定义成知识图谱上满足条件的全部物品：

> G_q = { i ∈ KG | C_shared ⊆ A_i }

式 (6) 的样本是 `(q, H'_u, G_q)`，其中 `H'_u = H_u \ G_q`，也就是给模型看的历史要把这些答案拿掉。

发布文件和脚本用的是另一个集合。README 对 `movieSubset` 的注释是「movies that satisfy these conditions in user …'s interaction history」。`eval_movie.py` 的 `precision`、`recall`、`ndcg` 都拿 `movieSubset` / `movieSubsetId` 当相关集。`satisfied_ratio`（脚本里的 CMR）才去 Neo4j 上检查 `sharedRelationships`：不在历史子集里的推荐，用 `check_by_KG` 看是否满足全部条件；在历史子集里的推荐直接算满足。分母是能解析到图谱 id 的推荐个数。

两套标签都在发布物里，但不是论文写明的「故意用两个指标惩罚不同系统」。观察 4 说的是提示词里的历史，不是式 (7) 和 `movieSubset` 的差别。调研笔记把这两件事写成了一句，这里拆开。

显式文件里没有全目录答案列表，只有 `movieSubset`。`movieCount` 与 `len(movieSubset)` 在 4,997 条上全部一致。`movieCount` 最小 2，平均 2.84，中位数 2，最大 34。历史子集通常就是两三部电影。

`dataset/KG.dump` 是 6,416 字节，文件头是 `DZV1`，装不下 2 万部电影的图。README 仍写着用它在 Neo4j 里建图之后才能评测。CMR 的图谱检查无法从这个 dump 复现。

`movie_info.jsonl.zip` 解压后是 21,796 条 JSON（调研笔记写 21,797，文件里是 21,796 个对象）。主键是 `Title`，没有 MovieLens id。常见字段是 Directed by、Starring、Cinematography、Produced by、Music by、Language 等。`Genre` 这个键只出现在 2,801 条上。`movies.dat` 有 3,883 行，是 MovieLens-1M 的影片表，不是表 1 的 3,247。评分文件这次只看了表头，格式是 `UserID::MovieID::Rating::Timestamp`，GitHub 上的大小是 24,594,131 字节；没有数完全部评分行。

标题对齐，用「去掉年份、下划线变空格、把 MovieLens 的 `, The` 移回句首」之后：`movies.dat` 3,840 个不同标题里，3,204 个能对上 infobox。显式查询的 `movieSubsetId` 与 `movies.dat` 标题，14,170 对里 13,726 对对得上，444 对对不上，例子是 Dr. / Doctor、以及带 "a.k.a." 的别名。显式子集的标题字符串是维基写法（`The_Godfather`），不是 MovieLens 的 `Godfather, The`。

条件本身也不总是 infobox 的同一列。显式文件里，Rushmore (1998) 和 Four Rooms (1995) 的 `sharedRelationships` 是 `Directed_by / Mark Mothersbaugh`。infobox 里 Rushmore 的 Directed by 是 Wes Anderson，Music by 才是 Mark Mothersbaugh；Four Rooms 的导演是 Allison Anders 等四人。按 infobox 的「Directed by」执行 SQL，会错过官方历史标签；按标签里的关系名执行，又和 infobox 不一致。式 (7) 的图是作者构建的那张图，不是这份 infobox 的干净投影。

我用 infobox 对显式查询做了一次重建，只统计关系类型都能映到 infobox 列的查询（`Directed_by`、`Produced_by`、`Starring`、`Cinematography`、`Language`），跳过含 `Genre` 或其他类型的 729 条，剩下 4,268 条。人名按分号拆开、做了小写和去标点。这 4,268 条上，infobox 匹配集大小的中位数是 14，平均 18.5，最大 83；历史 `movieCount` 的中位数仍是 2。匹配集大于历史子集的有 3,194 条，相等 723 条，更小 351 条。更小的那 351 条说明重建会漏标签，中位数 14 是下限方向上的估计，不是论文的 `|G_q|`。在「历史子集包含于匹配集」时，把整个匹配集交回去，历史子集 Precision 的上界是 `movieCount / |匹配集|`，这 4,268 条的中位数是 0.20，平均数是 0.41。

`Genre` 没有拿来做这个除法。它对 `movies.dat` 的体裁做严格字符串匹配时，3,065 个（电影，体裁值）对里 1,569 个相等。不相等的里面包含 `Children` 对 MovieLens 的 `Children's`，所以不能把「不相等」直接当成错误条数。`Rock` 作为体裁值出现了，MovieLens 的体裁表里没有 Rock。

### 改成检索之后，哪个标签当主指标

主指标用式 (7) 的全目录条件集：返回的每一行是否满足 `sharedRelationships`，以及这张条件表被找回了多少。显式问句问的是条件（README 的例子是 "Can you recommend some war movies starring Tom Hanks?"）。SQL 的工作就是把满足这些谓词的电影找出来。

历史子集当 Precision，会冤枉这条 SQL。标签中位数是 2 部看过的电影。上面那次重建里，条件在 infobox 上的匹配集中位数是 14。SQL 把 14 部都返回，而且每一部都满足条件，历史子集 Precision 仍只有约 2/14。表 2 的 0.308 是生成式 Precision，和这个数不是同一种分母，不能横着比。

历史子集当 Recall，会把 SQL 说得过好。那 2 部只要在结果里，Recall 就是 1，多返回的、同样满足条件的电影不扣分。不加截断的话，返回整个影片表也能在这个 Recall 上满分，只要历史子集被包在里面。

CMR 靠近「条件精度」，不衡量式 (7) 的召回。只报 CMR，返回 1 部正确电影和返回全部正确电影可以一样高。检索实验要把条件精度和全目录条件召回一起报。排序指标（NDCG）的相关集也用这张全目录条件表。脚本里的 NDCG 用的是 `movieSubset`，表 2 没有发表 NDCG。

隐式条件和错误信息条件不适合当 SQL 的第一刀。隐式条件要先从「The Abyss 的导演」推到人名（式 (2)(3)）；错误信息条件是故意写错的（式 (4)）。人口统计和兴趣查询的标签是人群热门或常见后续，不是可执行谓词。图书没有导演、演员这种表，第一轮仍然不放进来。

官方 0.308 / 0.408 / 0.714 只作为「没看过目录的生成系统」的参照，不放进检索主表。

## Amazon-C4 / BLaIR

- 原文：`papers/sql-recall/03-benchmarks/blair-2026.acl-long.147.pdf`（ACL 2026 long，15 页）
- URL：<https://aclanthology.org/2026.acl-long.147.pdf>
- 数据卡：<https://huggingface.co/datasets/McAuley-Lab/Amazon-C4>

### 创新点，以及证据落在哪

1. **把 LLM 当语义编码器**，在序列推荐、协同过滤、短查询商品搜索、复杂查询商品搜索上比嵌入（表 6、表 8–10）。序列推荐和协同过滤要训练适配层；商品搜索是零样本点积。都不是给定 10/20 个候选的重排。
2. **复杂查询商品搜索**，两个集。Amazon-C4 是评论改写。Reddit-Movie 是论坛求推荐的帖子。评估指标是 NDCG@100（附录 C.3）。

### 查询是不是评论改写：论文里的事实

第 4.2 节和数据集卡写的是同一件事。论文：从 Amazon Reviews 2023 均匀抽取超过 20,000 条至少 100 字的 5 星评论，用 ChatGPT 改成第一人称找商品的查询；提示词要求商品名不得出现。表 4 的对照：同一商品，ESCI 的查询是 "salt gun"，Amazon-C4 的查询是一段除虫用途的长句。

数据卡把字段写成 21,223 条，`Avg.Len.q` 229.89。`test.csv` 的表头是 `qid,query,item_id,user_id,ori_rating,ori_review`。文件第一行的查询是过滤器吸尘，`ori_review` 是对应的 5 星评论，`ori_rating` 是 5。数据卡第 288 条就是「给孩子洗澡时解闷、可以涂花生酱」那句。查询是评论改写，这是论文、数据卡和文件头三处一致的事实。

### 物品有没有结构化列

发布的物品文件，第一行的键只有 `item_id`、`category`、`metadata`。这一行的 `category` 是 `Care`，`metadata` 以标题 "Supergoop! Super Power Sunscreen Mousse…" 开头，后面接 "Product Description"。数据卡写明：`metadata` 是原数据里 title 和 description 拼起来的一段；`category` 是一个字符串，用来按品类看结果。数据卡的 `Avg.Len.t` 是 538.97，对应这段拼接文本。

论文附录 C.2 写的编码方式更窄：Amazon-C4、ESCI、Beauty、Games、Baby 的主实验只用商品标题。第 5.3 节试过标题加描述，并不稳定地更好，所以主表用标题。表 3 里 Amazon-C4 的平均物品元数据长度是 99.81 个字符，查询是 229.89 个字符。99.81 对得上标题，对不上数据卡的 538.97。表 10 的 NDCG 是标题编码的结果。

「几乎没有结构化列」描述的是发布文件：没有品牌、价格、颜色这种列，只有一个品类字符串和一段文本。这是文件里的事实。论文没有说「因此 SQL 会输」。

### 池子是不是全库

表 3：Amazon-C4 物品数 1,058,417，查询数 21,223。数据卡的 `len(item_pool)` 也是 1,058,417。附录 C.1：每条 ground-truth 从同品类抽 50 个物品，排序时同时看本域和跨域的候选。这是抽样拼出来的 1,058,417，不是 Amazon Reviews 2023 论文里的约 4,800 万商品。相对「20 个候选的重排」，它仍是在这 100 万级池子上做检索。

表 10 的 NDCG@100：Amazon-C4 上 text-embedding-3-large 是 0.1856，GritLM-7B 是 0.1845。Reddit-Movies 上 GritLM-7B 是 0.0734，text-embedding-3-large 是 0.0699。正文在表 11 附近再次写了 GritLM-7B 在 Reddit-Movies 上的 NDCG@100 是 0.0734。

表 3 的 Reddit-Movies 行是 51,203 个物品、1,627、元数据平均 19.63 字符、查询平均 435.85 字符。第 4.2 节说整理出来的帖子—电影对超过 20,000，评估只用原来的测试划分。1,627 是表 3 里和 Amazon-C4 的 21,223 对齐的那个位置，也就是参与评估的测试划分，不是全部帖子。附录 C.2：Reddit-Movie 的编码字段是电影标题和上映年。这是论文里的事实。19.63 个字符也短到只容得下标题和年份。

### 负对照是否成立

「精确 SQL 应该输给 0.1856」是我们的推断，论文没有 SQL 或 BM25 的行。推断所靠的前提是事实：查询是去掉商品名之后的评论改写，说的是用途（洗澡、吸尘、固定鼻枕）；发布物品没有品牌、价格、颜色列；官方嵌入看的是标题。品类字符串还在。池子又是按 ground-truth 的品类抽了 50 个同品类负例再并起来的，所以就算猜中品类，候选里仍有同品类的难负例，品类谓词隔离不出那一件商品。

推断停在谓词 SQL。对 `metadata` 做 `LIKE` 是词法检索，论文没测，不能事先写成「一定输」。总览里那条停点仍然对：若 SQL 在这里打赢嵌入，先查是不是品类或标题泄漏。

Reddit-Movie 不适合当这个负对照的替代。它的文本更短（标题和年份），查询是真人帖，GritLM 的 NDCG@100 只有 0.0734。SQL 若输了，分不清是「结构化列不够」还是「年份和标题本来就接不住长帖」。Amazon-C4 的查询来源和字段更干净地对准「精确谓词帮不上忙」。

## EComAgentBench

- 原文：`papers/sql-recall/03-benchmarks/ecomagentbench-2026.emnlp-industry.61.pdf`
- URL：<https://aclanthology.org/2026.emnlp-industry.61.pdf>，arXiv <https://arxiv.org/abs/2606.17698>
- 代码：<https://github.com/Morizeyao/EComAgentBench_>。库本身没有下载。

### 创新点，以及证据落在哪

创新点是隐藏意图散在三处：可见问句、只能用工具读到的人设、脚本化的澄清。智能体在 100 次工具调用内提交一件商品。主指标是准确率：命中目标商品，或满足全部 rubric（第 3 节）。摘要和正文都写最强模型 57.1%。第 5 节点名 claude-opus-4-6 在准确率上领先。921 条生成候选里 662 条通过校验。

这是单件商品的智能体任务。证据不在全库 Recall@K，也不在给定 20 个候选的重排。可见问句只带一部分要求。只对可见问句做 Text-to-SQL，人设和澄清里的条件根本不在输入里。

第 4 节：目录是 370 万商品、2,140 万评论。`DATA.md` 写大约 370 万商品、2,100 万评论，四个类目（All_Beauty、Electronics、Cell_Phones_and_Accessories、Office_Products），每件商品最多 20 条评论，种子 42。

### 模式：代码里的事实，不是 PDF 里的句子

`scripts/build_product_index.py` 的 `products` 表有 `product_id, title, store, brand, price, average_rating, rating_number, main_category`，外加一个 `data` JSON。品牌来自 `details["Brand"]`。第 104 行 `p.pop("bought_together", None)`，`bought_together` 不进任何列。FTS5 只索引 `title`。`search_products` 用 BM25，每页 20 条，描述写明只搜标题。`filter_by_attribute` 只在调用者给的最多 10 个 id 里做子串匹配。

「已经是 SQLite，而且丢掉了 bought_together」是构建脚本里的事实。论文 PDF 没有写 `bought_together`。没有 I2I 或 U2U 的边，指的是这张建出来的表，不是论文的一个实验结论。

662 条、隐藏意图、一次只能交一件商品。它留在备份里是对的，撑不起主实验。

## REGEN

- 原文：`papers/sql-recall/03-benchmarks/regen-2503.11924.pdf`
- URL：<https://arxiv.org/pdf/2503.11924>

### 创新点，以及证据落在哪

创新点是在「下一个物品」旁边联合生成评论式叙事。对话元素是 Gemini 1.5 Flash 补出来的，不是用户当时说的话（第 3.2.2 节）。短评只加在相邻、且类目层级至少四级相同的物品之间（第 3.2.3 节）。

表 1 的 Office 列：用户 89,489，物品 27,887，每用户平均物品 7.86。89,489 是用户数。一人一条序列的话，序列数等于用户数，但表头不是「序列数」。Clothing 是 1,168,735 用户、376,847 物品。正文用「Office with 27k items」是约数，表 1 才是 27,887。

表 4「Hist. + Critique」一行，Flare+LLM 的 Recall@10 是 0.1402，NDCG@10 是 0.113，而且这对数在五个对话任务列上重复出现，因为推荐头不随叙事任务改变。同一行 LUMEN 的 Recall@10 是 0.123，NDCG@10 是 0.102。上面「Hist.」那一块，Flare+LLM 的 Recall@10 是 0.124，不是 0.1402。调研笔记里的 0.1402 / 0.113 对应的是历史加短评、Flare+LLM。

物品文本里有类目、描述、价格和评论（第 3.1 节，输入模板也把 Price 和 User Review 拼进序列）。SQL 最多把短评里的属性变成过滤，再交给下一个物品的排序器。官方指标是序列上的下一个物品，语言是模型补写的。不做主实验。

## InteRecAgent

- 原文：`papers/sql-recall/03-benchmarks/interecagent-2308.16505.pdf`（18 页）。仓库里原先没有这份 PDF，这次按 arXiv 下的。
- URL：<https://arxiv.org/pdf/2308.16505>

### 创新点，以及证据落在哪

创新点是对话智能体把工具分成查询、检索、排序，中间用 Candidate Bus 传递候选，而不是把候选名单写进提示词（第 3.1–3.2 节）。硬条件走 SQL，软条件走 ItemCF，排序用去掉位置编码的 SASRec（第 4.1 节）。证据是用户模拟器上的 Hit@50 和平均轮数（表 2、表 3），数据集是 Steam、MovieLens、Beauty。没有一份公开的、带自然语言查询和全库 Recall@K 的固定测试集。

SQL 的限制写在附录图 C3，不是实验结论：

- 只许一条单行 `SELECT`，只许一张物品信息表。
- 字符串列必须用 `LIKE`，不许用 `=`。
- 物品标题不许当条件。
- 这个工具不能找相似物品。
- 不许写 `LIMIT`；提示词要求把满足条件的都选出来。
- 规则第 6 条是「try to use OR instead of AND」。

实现又加了一道（第 4.1 节）：硬条件检索的候选上限是 1,000，软条件截到相似度的前 5%。Candidate Bus 每轮从全部物品开始，再被工具过滤。查询工具另外规定不能用来做推荐，也不许 `SELECT` id。

这套限制和「用 SQL 写 I2I 自连接」是反的：相似物品被明确交给 ItemCF，标题不许出现在 SQL 条件里。OR 优先也会拆掉「品牌并且颜色」这种合取。它说明有人已经把硬条件交给 SQL，同时说明他们的提示词不允许 SQL 承担协同那一步。模拟器上的 Hit@50 不能当作 STaRK 上的检索基线。

## TalkPlay-Tools

- 原文：`papers/sql-recall/03-benchmarks/talkplay-tools-2510.01698.pdf`
- URL：<https://arxiv.org/pdf/2510.01698>

### 创新点，以及证据落在哪

创新点是让 LLM 计划工具的种类、顺序和参数，把 SQL、BM25、稠密检索和 Semantic ID 串成一条检索—重排管道。SQL 是其中的布尔过滤：单表，字段包括 title、artist、album、release date、tempo、key、popularity；参数里有 `topk`，例子是 `topk=100`（第 2.2 节，表 1）。

证据在 TalkPlayData 2 的 1,000 段合成对话上，每段 8 轮，指标是 Hit@1、Hit@10、Hit@20（第 3 节）。用户和曲目来自 LFM-2b，对话是合成的。SQL 有用，是在这套音乐工具链里观察到的，不是商品全库召回，也不是给定 20 个候选。它支持「SQL 做硬过滤、文本另走检索」这个系统形状，不替换 STaRK-Amazon 做主实验。

## AgentRecBench

- 原文：`papers/sql-recall/03-benchmarks/agentrecbench-2505.19623.pdf`
- URL：<https://arxiv.org/pdf/2505.19623>

第 4.4 节写明每条测试由 20 个候选组成：1 个来自用户交互历史的正例，19 个来自未观察交互的负例。指标是 HR@1、HR@3、HR@5。第 9 页的提示词要求只给这 20 个物品排序，不许引入别的 id。正例是历史里抽出来的已交互物品。

智能体流程、冷启动、兴趣漂移上的结论，都只在这 20 个候选的重排里成立。没有全库召回可以换成 SQL。

## QUEST

- 原文：`papers/sql-recall/03-benchmarks/quest-2023.acl-long.784.pdf`
- URL：<https://aclanthology.org/2023.acl-long.784.pdf>，arXiv <https://arxiv.org/abs/2305.11694>

QUEST 是维基实体检索。3,357 条自然语言查询，带隐式的交、并、差；每条最多 20 个实体；语料 325,505 个实体。划分是 1,307 / 323 / 1,727。原子查询来自维基类目名。推理时不许使用类目标签，类目已从实体文档里去掉，系统只能看文本（第 3 节）。

电影会出现在查询里（摘要的例子是 "science-fiction films shot in England"），任务仍是返回维基文档对应的实体集合，不是给用户推荐下一步要点的物品。正文里 "recommendations" 出现在「用户要能核对系统给出的建议」这种一般说法里，不是推荐系统实验。它不能当 SQL 召回的数据集。类目在构造时已知、在推理时被禁止，和「把类目写成 SQL」也不是同一个协议。

## 主实验还是不是 STaRK-Amazon

是。公开材料里，同时有自然语言、可执行的关系边、以及官方全库 Hit / Recall / MRR 的，仍然是 STaRK-Amazon。标签被文本筛过，所以主表不能是纯 SQL 的 Hit@1；81 条人工查询正好用来看解析器是不是在背合成模板，尽管它小，而且句子里混有图外谓词。

RecBench+ 电影显式查询是第二实验，不是替代。它更接近「精确过滤加一份用户历史」，但官方分是生成式的，`KG.dump` 不能用，历史子集 Precision 会罚掉正确的全目录 SQL。要用它，就按 `sharedRelationships` 重建式 (7) 的条件表，主指标用这张表的条件精度和召回，历史子集的 Precision 和 NDCG 另报，并写明后一组会怎么冤枉 SQL。

Amazon-C4 仍然是负对照。查询是评论改写、发布物品只有品类字符串和一段文本，这两点是论文和文件里的事实。嵌入的靶子是表 10 的 NDCG@100 0.1856，池子是 1,058,417 的抽样池。SQL 会不会输，要测了才知道。

EComAgentBench、REGEN、TalkPlay-Tools、InteRecAgent 都不换到主实验的位置：前两个没有「一句自然语言、全库、关系边」的官方检索协议；TalkPlay 的 SQL 证据在合成音乐对话上；InteRecAgent 的 SQL 被限制成单表硬过滤，相似物品不许它做，评估是用户模拟器。AgentRecBench 是 20 选 1 的重排。QUEST 不是推荐。
