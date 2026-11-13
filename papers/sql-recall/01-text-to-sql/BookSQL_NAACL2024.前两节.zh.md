> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名：** `BookSQL_NAACL2024.pdf`

**原文标题：** BookSQL: A Large Scale Text-to-SQL Dataset for Accounting Domain

**作者：** Rahul Kumar、Amar Raja Dibbu、Shrutendra Harsola、Vignesh Subrahmaniam、Ashutosh Modi。Kumar、Dibbu、Modi 来自 Indian Institute of Technology Kanpur；Harsola、Subrahmaniam 来自 Intuit。

**场合：** Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)，页 497–516，2024 年 6 月 16–21 日。

## 摘要

这是一篇资源论文。作者认为 WikiSQL、Spider 这类大规模 text-to-SQL 数据覆盖的领域很广，但财务和会计这种全球都在用、而且使用者往往不懂 SQL 的领域没有被好好覆盖。BookSQL 就是为会计和金融域补的大规模数据集：10 万条自然语言查询–SQL 对，会计库共 100 万条记录。

他们在 BookSQL 上跑了现有最优模型，包括 GPT-4，并做了分析。摘要的结论句是：性能差距很大，说明这个领域需要更专门的模型。摘要没有给出 GPT-4 的具体分数，也没有指向表号。

## 1 Introduction

第 1 节从使用场景写起：关系数据库到处都有，但 SQL 把没有技术背景的人挡在外面，财务会计就是例子。研究问题被收成：能不能用自然语言查关系数据库，尤其是会计库。作者承认 Spider（Yu et al., 2018）和 WikiSQL（Zhong et al., 2017）已经是大规模通用数据，可是跨领域不等于能做真实业务。原因是这些数据领域种类很多，却要么缺会计，要么在金融、销售、营销上的数据和查询类型很有限。BookSQL 由和财务专家合作做成，目标是反映业界实际在用的会计库。据作者所知，此前没有大规模会计数据把企业账簿的细粒度记录收进来。

规模用美国约 3300 万家小企业来衬托：这些企业用会计软件记 money-in（如 invoice、sales receipt）和 money-out（如 expense、purchase order、bill payment），报税还要遵守复式记账、分层的 chart of accounts 和权责发生制。一笔交易跨多张表，SQL 会用到聚合、distinct count 和嵌套查询，新手很难写。表 1 把这个缺口落成数字：在 Spider 上预训练的模型，Exact Match Accuracy（定义见第 5 节）换到 BookSQL 上掉得很厉害。

| 模型 | Spider | BookSQL |
| --- | --- | --- |
| UniSAr | 70% | 3.8% |
| SEDE | 63.2% | 0.0% |
| RESDSQL | 80.5% | 10.8% |

贡献有两条。一是 BookSQL 本身：100 万条记录的财务账户库，查询按会计实务来设计；10 万条 Query-SQL 对，大约是当时最大的 text-to-SQL 数据集 WikiSQL 的 1.25 倍；查询设计咨询了财务专家。二是把包括 GPT-4 在内的现有模型拿到 BookSQL 上，看在 Spider 这类数据上训练的模型缺在哪里，并放出数据和代码：`https://github.com/Exploration-Lab/BookSQL`。第 1 节没有印出 GPT-4 的分数。文中对术语的界定是：text-to-SQL 系统把自然语言查询转成 SQL 再取数；text-to-SQL 数据集则同时包含自然语言、对应 SQL、正确答案和被查询的库。

同一节还放了表 2，把 BookSQL 和常见基准对齐。列依次是 query-SQL 对数量、数据库数、领域数、平均每个领域的表数、领域类型（Cross 或 Single），以及 ORDER BY、GROUP BY、NESTED 三类查询的数量。#D 为 “-” 表示领域数未知。

| 数据集 | #Size | #DB | #D | #T/DB | Domain | ORDER BY | GROUP BY | NESTED |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Spider | 10,181 | 200 | 138 | 5.1 | Cross | 1335 | 1491 | 844 |
| WikiSQL | 80,654 | 26,521 | - | 1 | Cross | 0 | 0 | 0 |
| Advising | 3,898 | 208 | 1 | 10 | Single | 15 | 9 | 22 |
| BIRD | 12,751 | 95 | 37 | 7.3 | Cross | 2576 | 881 | 0 |
| IMDB | 131 | 1 | 1 | 16 | Single | 10 | 6 | 1 |
| Yelp | 128 | 1 | 1 | 7 | Single | 18 | 21 | 0 |
| BookSQL | 100k | 1 | 1 | 7 | Single | 17,529 | 11,508 | 4,456 |

## 2 Related Work

第 2 节不打算覆盖全部自然语言数据库接口研究，总述指向 Deng et al. (2022) 的综述，然后把数据集和模型分开写。数据集一侧，Spider 覆盖 138 个领域；WikiSQL 由 24,241 张维基表构成。Squall（Shi et al., 2020b）、KaggleDBQA（Lee et al., 2021）和 BIRD-SQL（Li et al., 2023b）用来测模型在没见过的领域上能否泛化。领域专用数据则包括基于 Yelp 和 IMDB 的数据（Yaghmazadeh et al., 2017）、Advising（Finegan-Dollak et al., 2018）、MIMICSQL（Wang et al., 2020）、SEDE（Hazoom et al., 2021a）、Restaurants（Tang and Mooney, 2001）和 Academic（Li and Jagadish, 2014）。作者对这一类的定位是：追求在特定领域上的精度，并不把泛化当目标。

**Comparison。** 对照就用表 2。BookSQL 的 Query-SQL 对更多，SQL 子句更多样（文中点名 ORDER BY），嵌套也更复杂。Spider 虽然横跨 138 个领域，但每个领域的查询很少，平均每个领域 74 条，所以在单一领域上的表现有限，并回指表 1。作者还说 BookSQL 可以并进 Spider，补上商业领域的覆盖。

**Models。** 模型只点了两个后来要拿来比的系统。UniSAr（Dou et al., 2022）是基于 Seq2Seq 的 non-invasive 模型，在多领域、多表的 Spider 上准确率高。RESDSQL（Li et al., 2023a）把 schema linking 和 skeleton parsing 拆开：前者找出问题要用的表和列，后者先生成 SQL 骨架再生成最终 SQL，并在 Spider 上达到当时最优。第 2 节到此结束。库的表结构和标注从第 3 节 BookSQL Dataset 起，此处不展开。
