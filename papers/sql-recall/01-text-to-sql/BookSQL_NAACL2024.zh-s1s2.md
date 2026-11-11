# BookSQL: A Large Scale Text-to-SQL Dataset for Accounting Domain

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`BookSQL_NAACL2024.pdf`。

## Abstract 摘要

近来已提出若干大规模数据集（例如 WikiSQL、Spider），用于开发面向数据库的自然语言接口。这些数据集覆盖了很宽的领域范围，但在金融和会计等一些关键领域上有所不足。鉴于会计数据库在世界范围内被使用，尤其是被非技术人士使用，迫切需要开发能够借助自然语言查询从会计数据库中抽取信息的模型。在这篇资源论文中，我们旨在填补这一空白，为会计与金融领域提出一个新的大规模 Text-to-SQL 数据集：BookSQL。该数据集包含 100k 条自然语言查询–SQL 对，以及 1 million 条记录的会计数据库。我们在 BookSQL 上对现有最先进模型（包括 GPT-4）做 Text-to-SQL 实验并加以分析。我们发现显著的性能差距，从而指向为该领域开发更有针对性的模型。

## 1 Introduction 引言

关系数据库遍布所有现代组织，从金融机构到教育机构。通常使用 SQL 等查询语言从关系数据库中抽取所需数据。然而，用 SQL 表述查询需要掌握这门语言本身；因此，这把不懂 SQL 的人（尤其是没有技术背景的人，例如财务会计）排除在数据库使用者之外。必须发展技术来回答这一研究问题：能否用自然语言查询关系数据库？本文朝这一目标迈出一步；具体而言，我们探讨能否为会计数据库开发自然语言接口。

近年来，已提出若干大规模通用数据集（Deng et al., 2022），用于开发 Text-to-SQL 系统，例如 Spider（Yu et al., 2018）和 WikiSQL（Zhong et al., 2017）。所谓 Text-to-SQL 系统，是指给定自然语言查询后，通过把自然语言查询转换为作为中间表示的 SQL 查询，自动从一个或多个数据库中检索所需信息的系统。所谓 Text-to-SQL 数据集，是指同时包含自然语言查询及其对应 SQL 表述、正确答案，以及查询所针对的相应数据库的数据集。这类数据集虽然跨领域，仍不适合开发能够应对真实商业用例的系统，例如通过自然语言接口访问会计数据库。主要原因是，这些大规模数据集在领域类型上有相当的广度，但它们或者缺少某些领域（例如会计），或者对特定领域（例如金融、销售和市场营销）只有有限的数据和查询类型。

本文试图通过为会计与商业领域提出一个大规模 Text-to-SQL 数据集（称为 BookSQL）来填补这一空白。我们与金融专家合作，创建反映业界实际使用的会计数据库的数据集。据我们所知，会计领域还没有大规模数据集包含企业所用会计账簿的细粒度记录。为了给出会计数据库使用规模的概念：仅在美国就有大约 33 million 家小型企业。这些企业大多使用会计软件来维护账簿、跟踪财务，即资金流入交易（例如发票和销售收据）和资金流出交易（例如费用、采购订单和账单支付）。此外，出于税务目的，这些账簿需要遵循标准会计原则，如复式记账（double-entry accounting）、层级化的会计科目表结构（hierarchical chart of account structure），以及权责发生制会计（accrual accounting）。会计数据库中的交易跨越多张表。相应的 SQL 查询可能涉及聚合、计算去重计数，以及嵌套查询等复杂操作，才能从中抽取信息。对新手用户来说，这并非易事。此外，正如我们的初步实验（表 1）所观察到的，在 Spider 上训练的现有最先进（state-of-the-art, SOTA）Text-to-SQL 模型在领域特定的 BookSQL 数据集上表现很差，这指向需要一个会计领域专用数据集，并进一步导向 SOTA 模型的开发。

表 1：预训练 SOTA Text-to-SQL 模型在 Spider 与本文提出的 BookSQL 数据集上的性能（精确匹配准确率 Exact Match Accuracy，参见 §5）。可以看到，现有模型在 BookSQL 上表现很差，表明领域泛化不佳。

| 模型（Model） | Spider | BookSQL |
| --- | --- | --- |
| UniSAr | 70% | 3.8% |
| SEDE | 63.2% | 0.0% |
| RESDSQL | 80.5% | 10.8% |

表 2：BookSQL 与基准数据集的比较。#Size、#DB、#D 和 #T/DB 分别表示查询–SQL 对的数量、数据库数、领域数，以及每个领域的平均表数。“#D” 列中的 “-” 表示领域数未知。最后 3 列表示查询类型。Yelp 数据集基于 Yelp 网站，IMDB 基于电影领域，Advising 数据集基于大学课程领域。

| 数据集（Dataset） | #Size | #DB | #D | #T/DB | 领域（Domain） | ORDER BY | GROUP BY | NESTED |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Spider | 10,181 | 200 | 138 | 5.1 | Cross | 1335 | 1491 | 844 |
| WikiSQL | 80,654 | 26,521 | - | 1 | Cross | 0 | 0 | 0 |
| Advising | 3,898 | 208 | 1 | 10 | Single | 15 | 9 | 22 |
| BIRD | 12,751 | 95 | 37 | 7.3 | Cross | 2576 | 881 | 0 |
| IMDB | 131 | 1 | 1 | 16 | Single | 10 | 6 | 1 |
| Yelp | 128 | 1 | 1 | 7 | Single | 18 | 21 | 0 |
| BookSQL | 100k | 1 | 1 | 7 | Single | 17,529 | 11,508 | 4,456 |

简而言之，在这篇资源论文中，我们做出如下贡献：

1. 我们创建一个新的大规模 Text-to-SQL 金融数据集，称为 BookSQL。该数据集包含一个 1 million 条记录的财务账户数据库。相应的自然语言查询被设计来应对会计领域的各种实际细节。BookSQL 有 100k 条查询–SQL 对，约为现有最大 Text-to-SQL 数据集 WikiSQL 的 1.25 倍。特别是，在设计查询时，我们咨询了金融专家，以理解各种实际用例。
2. 我们在 BookSQL 上运行现有最先进模型（包括 GPT-4）来做 Text-to-SQL 任务，观察其性能，并分析在 Spider 等现有大规模数据集上训练的模型的不足，从而指向为该领域开发专门模型。我们通过 GitHub 发布数据集和模型代码：https://github.com/Exploration-Lab/BookSQL 。

## 2 Related Work 相关工作

由于在实际应用中的重要性，开发面向数据库的自然语言接口一直是活跃的研究领域。由于篇幅限制，我们无法覆盖全部研究，请读者参阅 Deng et al. (2022) 的综述。本节概述该领域的一些主要工作。近年来已为 Text-to-SQL 任务提出若干数据集。例如，已提出 Spider（Yu et al., 2018）数据集，它覆盖 138 个不同领域。已创建大规模数据集 WikiSQL（Zhong et al., 2017），包含 24241 张维基百科表。类似地，已生成 Squall（Shi et al., 2020b）、KaggleDBQA（Lee et al., 2021）和 BIRD-SQL（Li et al., 2023b）等数据集，以评测模型在未见领域上的泛化性质。也已提出领域特定数据集，例如基于 Yelp 和 IMDB 的数据集（Yaghmazadeh et al., 2017）、Advising 领域（Finegan-Dollak et al., 2018）、MIMICSQL（Wang et al., 2020）、SEDE（Hazoom et al., 2021a）、餐馆领域（Tang and Mooney, 2001）以及学术领域（Li and Jagadish, 2014）。这些数据集的目的是在忽略模型泛化特性的同时，以很高的精度评测模型性能。

**比较。** 我们在表 2 中把 BookSQL 与其他流行数据集进行比较。可以看到，BookSQL 的查询–SQL 对数量大得多，在 SQL 子句方面的查询更为多样（例如 ORDER BY），并且涉及更复杂（以及嵌套）的查询。Spider 等基准数据集对各个领域的覆盖非常宽（138），但每个领域的查询很少（例如 Spider 每个领域的平均查询数为 74），限制了它在特定领域中的表现（另见表 1）。此外，BookSQL 可以与现有 Spider 数据集合并，以增加其在商业领域的覆盖。

**模型。** 已为 Text-to-SQL 任务提出多种模型（Deng et al., 2022）。一些最先进模型包括基于 Seq2Seq 架构的非侵入式 UniSAr 模型（Dou et al., 2022）。该模型在多领域、多表的 Spider 数据集上显示出高准确率。RESDSQL（Li et al., 2023a）把模式链接与骨架解析解耦，用于 Text-to-SQL 生成。模式链接识别给定问题所需的表和列。骨架解析先生成 SQL 骨架，再生成最终 SQL。它在 Spider 基准上取得 SOTA 性能。

表 3 出现在本节抽取文本中（其讨论见后文，此处仅译所抽出的表）。表 3：BookSQL 的统计。

| BookSQL 统计（BookSQL Stats） | 数值 |
| --- | --- |
| 数据库规模（Size of the database） | 1 million |
| 企业总数（Total Businesses） | 27 |
| 问题–SQL 对规模（Size of Question-SQL Pair） | 100k |
| 简单 SQL 数量（Number of Easy SQL） | 10,000 |
| 中等 SQL 数量（Number of Medium SQL） | 45,000 |
| 困难 SQL 数量（Number of Hard SQL） | 45,000 |
