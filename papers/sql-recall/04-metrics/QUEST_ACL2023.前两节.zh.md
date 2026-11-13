> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

- 原文件名：QUEST_ACL2023.pdf
- 原文标题：QUEST: A Retrieval Dataset of Entity-Seeking Queries with Implicit Set Operations
- 作者：Chaitanya Malaviya（University of Pennsylvania；该工作在 Google 实习期间完成）、Peter Shaw、Ming-Wei Chang、Kenton Lee、Kristina Toutanova（Google DeepMind）
- 场合：Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (ACL 2023), Volume 1: Long Papers，页 14032–14047，2023 年 7 月 9–14 日

## 摘要

QUEST 要测的是检索系统能不能处理“有选择的信息需求”：查询表面上是自然语言，里面却隐含 intersection、union、difference。摘要里的例子是 “shorebirds that are not sandpipers” 和 “science-fiction films shot in England”。数据集共 3357 条查询，每条落到一组实体，实体再对应 Wikipedia 文档。难点不在单条关键词匹配，而在同时对上多条约束的文档证据，并做对集合运算。

构造是半自动的。查询由 Wikipedia category 名称自动组合，再经众包改写，并另做自然度与流畅度核验。众包还根据实体文档标相关性，并把约束归因到正文片段。作者用若干现代检索系统做了分析：这类查询经常失败；negation 与 conjunction 尤其难，多种运算叠在一起时更难。数据发布在 https://github.com/google-research/language/tree/master/language/quest 。

## 1 Introduction

第 1 节先把问题从知识库问答里挪出来。用户常同时给出多条偏好，查询因此隐含 intersection、difference、union：90 年代且没有外星人的科幻片、设定在法国的历史小说、巴拿马的常绿灌木。答案不多时，读者要的是穷尽列表，并且希望看到可信来源上的证据（Lamm et al., 2021）。结构化知识库可以把约束落到谓词上再符号执行，但知识库不完整，维护也贵。信息检索有机会直接把约束对到正文，可 MSMarco（Nguyen et al., 2016）和 Natural Questions（Kwiatkowski et al., 2019）既很少收录这种查询，标注也停在基线系统的前几条，而不是穷尽文档集。

QUEST 的做法是：四个领域的自然语言查询，各自映射到相对完整的 Wikipedia 实体页集合。category 及其成员只在构造时使用，推理时不开放，以免变成半结构化检索。category 名称往往像真实搜索需求，但名称和正文的对应经常不直白，判断相关性带有自然语言推理的难度。Figure 1 把流程收成四步：抽样 category 与实体、用模板合成集合运算（文中例子是 A ∩ B \ C）并请众包改写、另一批众包按流畅度和自然度筛选、再做相关性与 attribution 标注。对数据中的很大一部分，标注包括基于文档的标量相关性，以及约束到文本片段的细粒度归因。

评测要求在大规模实体集合上取回多篇文档，而不是单答案。Figure 2 用 “Supernatural horror films set in Nevada” 和实体 Willy’s Wonderland 说明：不同约束的证据可以散落在同一篇文档的不同位置。作者把预训练模型微调成多文档集合检索器。到 T5-Large（Raffel et al., 2020）为止，dual encoder 和 cross-attention 对带集合运算的查询大体无效。conjunction 与 negation 最难，运算组合更难。错误分析把不相关的假阳性主要归到两类疏忽：忽略否定约束，或忽略合取约束。

## 2 Related Work

第 2 节用三条既有线路说明 QUEST 补的空缺，而不是再做一种知识库问答。

知识库问答（Berant et al., 2013; Yih et al., 2016; Talmor and Berant, 2018; Keysers et al., 2020; Gu et al., 2021 等）取回的是库中的节点或关系，问题有时附带逻辑形式；Lan et al. (2021) 综述了复杂 KBQA。作者强调大型人工知识库并不完整（Watanabe et al., 2017），答案 schema 又限制了查询类型，且 schema 本身昂贵，所以本文不假设推理时能访问知识库。把 KBQA 改到残缺或无库设定的工作（Watanabe et al., 2017; Sun et al., 2019）是删掉一部分库或完全不用库。QUEST 与它们的另一处分界是：不做跨多文档的 multi-hop，一个实体是否相关只由它自己的文档决定。

开放域检索这边，TREC（Craswell et al., 2020）、MSMarco、Natural Questions 来自搜索日志一类 “found data”；Thakur et al. (2021) 把多份既有数据收成统一评测。HotpotQA（Yang et al., 2018）和 MultiRC（Khashabi et al., 2018）关注 multi-hop；Kong et al. (2022) 一类电商数据没有公开。这些集合很少覆盖“隐含集合运算、且答案要穷尽”的查询，因为它们落在查询分布的尾部。多答案检索（Min et al., 2021; Amouyal et al., 2022）要求一条查询对应多个不同答案；Min et al. (2021) 改编 WebQuestionsSP（Yih et al., 2016），并用 MRecall@K 衡量穷尽召回。QUEST 同样是多答案集合检索，但查询还带隐含的集合约束。同期 RomQA（Zhong et al., 2022）从 Wikidata 抽约束组合，动机同为多约束、答案集可能很大。为免人工归因，RomQA 把每条约束限制在 Wikipedia 摘要中可核验的单句上，关系靠 distant supervision，精度高、召回可能偏低（T-Rex）。QUEST 把匹配放到文档级推断；为了让人工归因可做，它限制答案集规模，且每个答案只对应单篇文档。
