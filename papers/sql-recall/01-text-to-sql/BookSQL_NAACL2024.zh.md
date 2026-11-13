原文件名：BookSQL_NAACL2024.pdf

原标题：BookSQL: A Large Scale Text-to-SQL Dataset for Accounting Domain

中文标题：BookSQL：面向会计领域的大规模 Text-to-SQL 数据集

作者：Rahul Kumar†，Amar Raja Dibbu†，Shrutendra Harsola∗，Vignesh Subrahmaniam∗，Ashutosh Modi†

单位：† Indian Institute of Technology Kanpur (IIT Kanpur)；∗Intuit

邮箱：{rahulkumar21, amard21}@iitk.ac.in；{shrutendra_harsola, vignesh_subrahmaniam}@intuit.com；{ashutoshm}@cse.iitk.ac.in

会议：Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)，页 497–516，2024 年 6 月 16–21 日。©2024 Association for Computational Linguistics

<!-- 原 PDF 第 1 页 -->

## 摘要

近来已有若干大规模数据集（例如 WikiSQL、Spider）被提出，用于开发面向数据库的自然语言接口。这些数据集的领域覆盖面很宽，但在金融、会计等关键领域上仍然不足。会计数据库在世界各地被使用，使用者中有很多并非技术人员，因此迫切需要能够借助自然语言查询、从会计数据库中抽取信息的模型。作为一篇资源论文，我们提出面向会计与金融领域的新大规模 Text-to-SQL 数据集 BookSQL，用以填补这一空白。该数据集包含 10 万条自然语言查询–SQL 对，以及合计 100 万条记录的会计数据库。我们在 BookSQL 上实验并分析了现有最先进模型（包括 GPT-4）完成 Text-to-SQL 任务的表现，发现存在显著的性能差距，从而表明需要为该领域开发更有针对性的模型。

## 1 引言

关系数据库遍及当今各类组织，从金融机构到教育机构都在使用。通常要用 SQL 这类查询语言，才能从关系数据库中取出所需数据。然而，用 SQL 写查询需要掌握这门语言本身；因此，不会 SQL 的人（尤其是没有技术背景的人，例如财务会计）就被排除在数据库使用者之外。必须发展相应技术，来回答这样一个研究问题：能否用自然语言查询关系数据库？本文朝这一目标迈出一步；具体而言，我们探讨能否为会计数据库开发自然语言接口。近年来，已有若干大规模通用数据集（Deng 等人，2022）被提出，用于开发 Text-to-SQL 系统¹，例如 Spider（Yu 等人，2018）和 WikiSQL（Zhong 等人，2017）。这类数据集²虽然跨领域，仍不适合用来开发能够应对真实商业用例的系统，例如通过自然语言接口访问会计数据库。主要原因是：这些大规模数据集在领域类型上覆盖很宽，但要么缺少某些领域（例如会计），要么在特定领域（例如金融、销售和营销）上的数据和查询类型很有限。本文试图填补这一空白，提出一个面向会计与商业领域的大规模 Text-to-SQL 数据集（称为 BookSQL）。我们与财务专家合作，使所建数据集反映业界实际使用的会计数据库。

据我们所知，此前没有会计领域的大规模数据集，能够包含企业所用账簿的细粒度记录。为了说明会计数据库的使用规模：仅美国就有大约 33

**表 1：** 预训练的最先进 Text-to-SQL 模型在 Spider 与本文提出的 BookSQL 上的表现（精确匹配准确率，参见第 5 节）。可以看到，现有模型在 BookSQL 上的表现很差，说明领域泛化不足。

默认 `find_tables` 未检出该表。下表按该页文本顺序整理，数字均来自文本抽取。

| 模型 | Spider | BookSQL |
| --- | --- | --- |
| UniSAr | 70% | 3.8% |
| SEDE | 63.2% | 0.0% |
| RESDSQL | 80.5% | 10.8% |

¹ 所谓 Text-to-SQL 系统，是指这样一个系统：给定一条自然语言查询，它把自然语言查询转换成 SQL 查询，作为中间表示，从而自动从一个数据库或多个数据库中检索出所需信息。

² 所谓 Text-to-SQL 数据集，是指同时包含自然语言查询、对应的 SQL 写法、正确答案，以及实际执行这些查询所针对的数据库的数据集。

<!-- 原 PDF 第 2 页 -->

**表 2：** BookSQL 与各基准数据集的比较。#Size、#DB、#D 和 #T/DB 分别表示查询–SQL 对的数量、数据库数量、领域数量，以及每个领域的平均表数。“#D”列中的“-”表示领域数量未知。最后 3 列表示查询类型。Yelp 数据集基于 Yelp 网站，IMDB 基于电影领域，Advising 数据集基于大学课程领域。

默认 `find_tables` 未检出该表。下表按该页文本顺序整理，数字均来自文本抽取。

| 数据集 | #Size | #DB | #D | #T/DB | 领域 | ORDER BY | GROUP BY | NESTED |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Spider | 10,181 | 200 | 138 | 5.1 | Cross | 1335 | 1491 | 844 |
| WikiSQL | 80,654 | 26,521 | - | 1 | Cross | 0 | 0 | 0 |
| Advising | 3,898 | 208 | 1 | 10 | Single | 15 | 9 | 22 |
| BIRD | 12,751 | 95 | 37 | 7.3 | Cross | 2576 | 881 | 0 |
| IMDB | 131 | 1 | 1 | 16 | Single | 10 | 6 | 1 |
| Yelp | 128 | 1 | 1 | 7 | Single | 18 | 21 | 0 |
| BookSQL | 100k | 1 | 1 | 7 | Single | 17,529 | 11,508 | 4,456 |

百万家小型企业³。这些企业大多使用会计软件来记账，以掌握自身财务，也就是资金流入交易（例如发票和销售收据）和资金流出交易（例如费用、采购订单和账单支付）。此外，出于税务目的，这些账簿需要遵循标准会计原则，例如复式记账⁴、层级化的会计科目表结构⁵，以及权责发生制⁶。会计数据库中的交易横跨多张表。对应的 SQL 查询可能涉及复杂运算，例如聚合、计算去重计数，以及用嵌套查询来从中抽取信息。对新手用户来说，这并不是一件容易的事。而且，正如我们在初步实验（表 1）中所观察到的，在 Spider 上训练的现有最先进 Text-to-SQL 模型，在领域专用的 BookSQL 数据集上表现很差，这说明需要一个会计领域专用的数据集，并进而促成最先进模型的开发。简而言之，在这篇资源论文中，我们做出如下贡献：

1. 我们创建了一个新的大规模金融 Text-to-SQL 数据集，称为 BookSQL。该数据集包含一个有 100 万条记录的财务账户数据库。相应的自然语言查询旨在应对会计领域的各种实际细节。BookSQL 有 10 万条查询–SQL 对，大约是现有最大 Text-to-SQL 数据集 WikiSQL 的 1.25 倍。具体而言，在设计查询时，我们咨询了财务专家，以理解各种实际用例。
2. 我们在 BookSQL 上运行现有最先进模型（包括 GPT-4）来完成 Text-to-SQL 任务，查看其表现，并分析在 Spider 这类现有大规模数据集上训练的模型有哪些不足，从而指向为该领域开发专门模型。我们通过 GitHub 发布数据集和模型代码：https://github.com/Exploration-Lab/BookSQL 。

³ https://tinyurl.com/mr3vrptj

⁴ https://en.wikipedia.org/wiki/Double-entry_bookkeeping

⁵ https://en.wikipedia.org/wiki/Chart_of_accounts

⁶ https://en.wikipedia.org/wiki/Basis_of_accounting

## 2 相关工作

由于在实际应用中很重要，开发面向数据库的自然语言接口一直是活跃的研究方向。限于篇幅，我们无法覆盖全部研究，请读者参阅 Deng 等人（2022）的综述。本节概述该领域的一些主要工作。近年来已有若干数据集被提出用于 Text-to-SQL 任务。例如，Spider（Yu 等人，2018）数据集覆盖 138 个不同领域。大规模数据集 WikiSQL（Zhong 等人，2017）由 24,241 张维基百科表格构成。类似地，Squall（Shi 等人，2020b）、KaggleDBQA（Lee 等人，2021）和 BIRD-SQL（Li 等人，2023b）被构建出来，用于评估模型在未见领域上的泛化性质。也已有领域专用数据集被提出，例如基于 Yelp 和 IMDB 的数据集（Yaghmazadeh 等人，2017）、Advising 领域（Finegan-Dollak 等人，2018）、MIMICSQL（Wang 等人，2020）、SEDE（Hazoom 等人，2021a）、

<!-- 原 PDF 第 3 页 -->

餐馆领域（Tang 与 Mooney，2001）以及学术领域（Li 与 Jagadish，2014）。这些数据集的目的，是在很高的精度下评估模型表现，而不考虑模型的泛化特性。

**比较。** 我们在表 2 中把 BookSQL 与其他常用数据集作比较。可以看到，BookSQL 的查询–SQL 对数量大得多，在 SQL 子句方面的查询也更多样（例如 ORDER BY），并且包含更复杂的（以及嵌套的）查询。Spider 这类基准数据集对各个领域的覆盖非常宽（138 个），但每个领域的查询很少（例如 Spider 每个领域的平均查询数是 74），这限制了它在特定领域上的表现（另见表 1）。此外，可以把 BookSQL 与现有的 Spider 数据集合并，以增加后者在商业领域的覆盖。

**模型。** 已有多种模型被提出用于 Text-to-SQL 任务（Deng 等人，2022）。一些最先进模型包括基于 Seq2Seq 架构的非侵入式 UniSAr 模型（Dou 等人，2022）。该模型在多领域、多表的 Spider 数据集上显示出高准确率。RESDSQL（Li 等人，2023a）把模式链接与骨架解析解耦，用于 Text-to-SQL 生成。模式链接识别回答给定问题所需的表和列。骨架解析先生成 SQL 骨架，再生成最终 SQL。它在 Spider 基准上取得了最先进的表现。

## 3 BookSQL 数据集

鉴于商业数据库在世界各地的重要性和广泛存在，本文提出的数据集 BookSQL 聚焦金融与会计领域。会计数据库被用于很宽的行业谱系，例如建筑、医疗、零售、教育服务、保险、餐馆、房地产等。这些行业中的企业把财务交易归入各自不同的一套类别（在会计术语中称为会计科目表⁷）。例如，餐馆企业可能有广告、执照费等类别，房地产经纪企业可能有佣金、办公用品等类别。考虑到泛化，BookSQL 数据集纳入了来自不同行业的多种企业。因此，在 BookSQL 上开发的 Text-to-SQL 系统，在处理各类会计数据库时会更稳健。数据集的总规模为 100 万。数据集在财务专家监督下制备，其统计量见表 3。数据集包含 27 家企业，每家企业大约有 35k–40k 笔交易。全部企业及其产品的分布见附录图 3 和图 4。

**表 3：** BookSQL 的统计量。

默认 `find_tables` 未检出该表。下表按该页文本顺序整理，数字均来自文本抽取。

| 统计项 | 数值 |
| --- | --- |
| 数据库规模 | 100 万 |
| 企业总数 | 27 |
| 问题–SQL 对规模 | 100k |
| Easy SQL 的数量 | 10,000 |
| Medium SQL 的数量 | 45,000 |
| Hard SQL 的数量 | 45,000 |

### 3.1 BookSQL 的表

图 1 给出详细的数据库模式。该模式反映金融与会计领域中真实使用的数据库。BookSQL 中有七张表，分别是 Master Transactions、Customer、Employees、Product Service、Vendor、Chart of Account 和 Payment Method。我们是在检查若干企业的数据库（并与财务专家作了相应讨论）之后，才确定这七张表的清单。鉴于会计领域的性质，全球企业所使用的数据库，大多数主要就限制在这七张表之内。主表是 “Master Transaction” 表（例如附录表 8），它记录资金流入交易（发票、销售收据等）和资金流出交易（费用、采购订单、账单支付等）。该表还记录相应的其他交易细节，例如客户、供应商、产品/服务、贷方科目、借方科目和金额。“Chart of accounts” 表（例如附录表 9）包含全部科目名称和类型的信息。“Customer” 表（例如附录表 10）包含全部客户的细节，即姓名、账单地址和收货地址。“Vendors” 表（例如附录表 11）包含所有企业的全部供应商细节，即供应商名称和账单地址。“Employees” 表（例如附录

⁷ https://www.investopedia.com/terms/c/chart-accounts.asp

<!-- 原 PDF 第 4 页 -->

**图 1：** BookSQL 数据库模式

图 1 为多栏模式图。默认 `find_tables` 未把七张表的字段对齐抽全。下列字段按该页文本抽取，并吸收该次 `find_tables` 已对齐到表名上的 `business_id`；文本末尾另有 6 处未能挂到表名上的 `business_id`（int），见原 PDF 第 4 页。类型按抽出的原文保留。

`accounting.chart_of_accounts`

- business_id，int
- account_name，text
- account_type，text

`accounting.customers`

- customer_name，text
- billing_address，text
- billing_state，text
- billing_city，text
- billing_zip_code，int
- shipping_address，text
- shipping_state，text
- shipping_city，text
- shipping_zip_code，int

`accounting.vendors`

- vendor_name，text
- billing_address，text
- billing_state，text
- billing_city，text
- billing_zip_code，int

`accounting.Master_Trx`（`business_id int` 来自该次 `find_tables`）

- business_id，int
- transaction_id，int
- transaction_date，datetime
- transaction_type，text
- amount，double
- created_date，datetime
- created_user，text
- due_date，datetime
- open_balance，int
- product_service_name，text
- account，text
- account_receivable，double
- account_payable，double
- customer_name，text
- vendor_name，text
- quantity，int
- rate，double
- credit，double
- debit，double
- payment_method，text
- misc，text

`accounting.product_service`（`business_id int` 来自该次 `find_tables`）

- business_id，int
- product_service，text
- product_service_type，text

`accounting.payment_method`

- payment_method_type，text
- credit_card，text

`accounting.employees`

- employee_name，text
- employee_id，text
- hire_date，datetime
- billing_rate，double

表 12）包含关于该企业全部员工的信息。“Product service” 表（例如附录表 13）包含全部产品和服务的细节。“Payment method” 表（例如附录表 14）包含该企业使用的不同付款方式。

### 3.2 财务约束

为创建该数据集，我们取用以上述模式为基础的现有会计数据库，并对表中的名称和条目作匿名化，也就是把真实姓名、企业和数字替换成虚构的，同时遵守财务约束（下文说明）。这样做是为了维护个人和企业的隐私。所得数据库真实反映现实世界的会计设置。会计数据库遵循某些会计规则和财务约束，匿名化时也遵循了这些规则和约束。具体而言，遵循标准复式记账，即对一个科目的每一笔分录，都需要在另一个科目上有对应且相反的分录，也就是借方和贷方。因此，对每一笔交易，借方合计应当始终等于贷方合计。全部七张表都按 `business_id` 划分。对给定的 `transaction_id`，贷方列的合计应当等于借方列的合计，并且二者都应当等于 Master Transactions 表中的金额列。Master Transaction 表中的贷方（Credit）应当等于数量（Quantity）与单价（Rate）的乘积。会计科目表使用一家知名注册会计师（CPA）公布的分行业清单进行匿名化。⁸ 企业特有的自定义字段，使用各会计软件帮助文章中提供的示例进行匿名化。创建出的数据库交由财务专家交叉核对，以确保它看起来像真实世界的账户数据库。

### 3.3 数据集创建与标注

BookSQL 数据集包含 10 万个自然语言问题及其对应的 SQL，这些 SQL 作用在

⁸ https://hectorgarcia.com/resources/

<!-- 原 PDF 第 5 页 -->

多张表上，覆盖 27 家不同的企业。我们让财务专家参与查询创建过程。我们与两位财务专家合作，他们此前参与过会计软件的创建。此外，这些专家具备处理涉及账簿的客户交互的知识与经验。财务专家以无偿方式帮助我们，因为为会计领域创建 Text-to-SQL 系统，将对他们及其客户有帮助。

问题–SQL 对的形成过程如下。在财务专家的帮助下，我们首先列出客户（或企业人员）通常会问的、基于账簿的典型问题，或者客户有兴趣了解的信息。我们尽量让问题（查询）保持自然，以捕捉真实场景。我们依靠财务专家的经验，使这份清单尽可能穷尽。我们也为清单中的每条自然语言查询写了对应的 SQL 查询。清单中的查询随后通过模板化过程用来生成更多查询。图 2 用一个例子说明这一过程。

**图 2：** 创建 BookSQL 数据集的流程示例。这里可以把 aggregation_entity 替换为 max、min、total 和 average，customer_name 可以替换为任一可能的姓名，从而得到问题–SQL 对。类似地，date/period 可以替换为 last quarter、this quarter、last month。

图中文字：

- 自然语言查询：What were the total sales for John in the last quarter?
- 模板：What was the [aggregation_entity] sales for [customer_name] in the [date/period]?
- 流程标签：Templatization（模板化）、SQL Creation（SQL 创建）、NL Query（自然语言查询）、SQL、Template（模板）

SQL 模板按该页文本保留如下。`transaction_date` 与 `"[date_filter]"` 之间未见比较运算符。公式抽取不完整，见原 PDF 第 5 页。

```sql
select [aggregation_entity](credit) from master_txn_table as T1 join chart_of_accounts as T2 on T1.account = T2.account_name where account_type in ('Income','Other Income') and customers = "[customer_name]" and transaction_date "[date_filter]"
```

为了尽可能穷尽，在专家帮助下，我们得到 183 个客户在与会计数据库交互时通常会问的、互不重复的自然语言问题。这些自然语言问题被用来创建查询模板，并进一步用来在 BookSQL 中生成多样的问题–SQL 对。此外，我们对 BookSQL 语料和查询模板与财务专家做了第二轮核对，以验证一致性、真实性，并确保数据集反映真实场景。需要说明的是，现有的通用 Text-to-SQL 数据集（例如 Spider 和 WikiSQL）由多个领域的数据库组成，而 BookSQL 聚焦金融领域，因此模板数量看起来可能较少。不过，若按单一领域来比较，模板数量仍然很多。举一个粗略估计：Spider 数据集使用 5693 个模板，跨越 138 个领域，因此每个领域的模板数粗略约为 41（$\sim 5693/138$）。Spider 并没有给出每个领域的模板细节，所以这只是粗略估计。此外，现有 Text-to-SQL 数据集（如 Spider）中的问题由学生创建（Yu 等人，2018），而 BookSQL 中的问题由财务专家创建；这些专家定期使用会计系统，并且非常熟悉。虽然我们的数据集（就模板总数而言）较小，但质量高、也更复杂，因此有助于学到能够较好泛化的模型。另外，在用模型做实验时，测试集中的查询基于训练期间未使用的模板（见第 5 节）。

据我们所知，BookSQL 是第一个包含多步问题的 Text-to-SQL 数据集；这类问题需要嵌套 SQL 查询才能得到答案。例如：“What products are selling less than last month/week?”（哪些产品的销量低于上个月/上周？）它首先需要计算月度/周度的产品级销售额，然后把每个产品的当前销售额与上个月/上周的销售额作比较。BookSQL 的数据库模式也包含复杂的列类型。此外，BookSQL 是第一个带有大量基于时间的过滤条件的 Text-to-SQL 数据集，例如上个月、本季度至今、上一财年、7 月到 8 月之间、本周、昨天等。

### 3.4 BookSQL 中 SQL 的复杂度

BookSQL 中的 SQL 查询是多样的，覆盖各个复杂度级别，也就是覆盖下列运算：带多列和聚合的 SELECT、WHERE、GROUP BY、HAVING、ORDER BY、LIMIT、JOIN、INTERSECT、UNION、NOT IN、OR、AND、EXISTS、CONTAINS，以及嵌套查询。表 2 给出全部 Text-to-SQL 数据集的比较。就复杂度而言，BookSQL 包含复杂 SQL 查询，其中有 17,529 条 ORDER BY、11,508 条 GROUP BY 和 4,456 条 NESTED 查询。我们进一步按 SQL 的复杂度，把全部查询–SQL 对分成三类：Easy、Medium 和 Hard。表 4 给出每一类的例子。表 3 给出 BookSQL 的主要统计量。BookSQL 包含 7,193 条 Hard SQL 查询，使它成为一个更复杂、规模更大、也更具挑战的数据集。我们用下列标准决定一条查询的复杂度。

<!-- 原 PDF 第 6 页 -->

- EASY：带单一 WHERE 条件的简单查询
- MEDIUM：WHERE 子句中有多个条件，并且 SELECT 子句中有多列
- HARD：Join、Group by、内层查询、Union、Except，因为这些很难从自然语言问题中预测出来

**表 4：** 按查询复杂度给出的 BookSQL 问题–SQL 对示例。

默认 `find_tables` 未检出该表。问句与 SQL 按该页文本转写；仅把行末连字符拼接回原词，未改数字，也未补运算符。

Easy。问题：What is the balance owned by John?（John 拥有的余额是多少？）

```sql
SELECT balance from Customers where customer_name = 'John'
```

Medium。问题：What is the maximum sales for John in the last month?（John 上个月的最高销售额是多少？）

```sql
SELECT MAX(credit) FROM master_txn_table where account_type in ('Income', 'Other Income') AND customer = 'John' AND month(transaction_date) = month(current_timestamp) - 1
```

Hard。问题：What products are selling less than last month?（哪些产品的销量低于上个月？）

```sql
SELECT A.product_service, revenue_this_month, revenue_last_month
FROM (SELECT product_service, SUM(credit) as revenue_this_month FROM master_txn_table
WHERE account_type in ('Income', 'Other Income') AND month(transaction_date) = month(current_timestamp) GROUP BY 1) AS A
INNER JOIN (SELECT product_service, SUM(credit) as revenue_last_month FROM master_txn_table
WHERE account_type in ('Income', 'Other Income') AND month(transaction_date) = month(current_timestamp) - 1 GROUP BY 1) AS B
ON A.product_service = B.product_service WHERE revenue_this_month < revenue_last_month
```

## 4 基线模型

我们在 BookSQL 数据集上对现有最先进的 Text-to-SQL 模型做基准测试。

**SEDE：** 我们在 BookSQL 数据集上微调了 SEDE 模型（Hazoom 等人，2021b）。SEDE 是基于 T5 的序列到序列模型（Raffel 等人，2020）。它把无序的模式项（表名和列名）与问题一起作为输入，并生成对应的 SQL 查询作为输出。

**UniSAr：** 我们在 BookSQL 训练集上微调了 UniSAr 模型（Dou 等人，2022），以 T5-large 作为基础语言模型。UniSAr 用三项非侵入式扩展，把任意序列到序列语言模型变成 text2sql 模型：（1）Structure Mark（结构标记），用于在模型输入中编码数据库模式；（2）Constrained Decoding（约束解码），用于生成结构良好的 SQL。对 BookSQL 数据集，我们去掉了 UniSAr 的约束解码模块，因为它不支持 BookSQL 数据集中带有复杂语法的 SQL 查询。（3）SQL Completion（SQL 补全），用于补全可能缺失的 JOIN 关系。

**RESDSQL：** RESDSQL（Li 等人，2023a）把模式链接与骨架感知解码解耦，用于 SQL 生成。训练一个交叉编码器，为模式链接对给定查询所需的表和列进行排序。对于 SQL 生成，使用带骨架感知解码的序列到序列模型：它先生成一个 SQL 骨架，然后模型据此预测实际的 SQL 查询。解码器中的掩码自注意力方法，使首先生成的骨架能够隐式指导后续的 SQL 解析。

**DIN-SQL + GPT4：** 我们使用 Pourreza 与 Rafiei（2023）所提出的提示链技术。

<!-- 原 PDF 第 7 页 -->

它把 Text-to-SQL 任务分解为多个子任务，然后用针对子任务的提示去提示 GPT4（Achiam 等人，2023），逐个求解每个子任务。它使用下列子任务：

1. 模式链接（Schema Linking）：该模块识别回答自然语言问题所需的、对数据库表和列的指称。
2. 分类与分解（Classification and Decomposition）：该模块把每个问题分成 easy、非嵌套复杂（non-nested complex）和嵌套复杂（nested complex）。这表示给定问题所需的 SQL 查询类型。
3. SQL 生成（SQL Generation）：该模块用前面各模块的输出生成 SQL。
4. 自校正模块（Self Correction）：该模块负责改正前一模块所生成 SQL 中的任何小错误。

每个子任务的提示样本见附录 C。

**动态少样本提示 + GPT4（DFew+GPT4）：** 我们采用与 Sun 等人（2023）类似的动态少样本提示技术。首先，用 SentenceTransformers 的 all-MiniLM-L6-v2 模型⁹对训练集问题做嵌入，从而创建一个向量数据库。该模型在 10 亿句对数据集¹⁰上训练，最适合用来生成句子嵌入。这样创建的嵌入数据库称为 trainDB。然后在推理时，用同一个 SentenceTransformers 模型为测试问题创建嵌入，并用该嵌入在 trainDB 中做 ANN（近似最近邻，Approximate Nearest Neighbor）搜索，从训练集中取出十个例子。这十个例子和数据库模式被用来为 GPT4 创建少样本 SQL 生成提示。伪代码和提示样本见附录 B。我们使用 ChromaDB¹¹作为底层向量数据库，并用于 ANN 搜索。

⁹ https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

¹⁰ https://huggingface.co/blog/1b-sentence-embeddings

¹¹ https://github.com/chroma-core/chroma

## 5 实验、结果与分析

### 5.1 评价指标

我们使用标准评价指标（细节见附录 D）：精确匹配准确率 EMA（Exact Match Accuracy）（Yu 等人，2018）、执行准确率 EA（Execution Accuracy）（Yu 等人，2018）、部分组件匹配 F1，即 PCM-F1（Partial Component Match F1）（Hazoom 等人，2021a）、BLEU-4（Papineni 等人，2002）和 ROUGE-L（Lin，2004）。

### 5.2 实验设置

我们按查询模板把数据集划分为 70% 训练集、10% 验证集和 20% 测试集。测试集包含 14.37% 的 easy、78.43% 的 medium 和 7.2% 的 hard SQL 查询。为了检验泛化表现，测试集中的查询基于训练期间未使用的模板。鉴于对 OpenAI GPT4 API 的调用次数有限，对基于 GPT4 的方法，我们使用 BookSQL 测试集中随机抽取的 10%。训练和超参数的细节见附录 E。

### 5.3 结果

表 5 和表 6 给出基线模型的表现。表 5 给出

**表 5：** Spider 与 BookSQL 数据集上的结果。EMA 指精确匹配准确率，EA 指执行准确率，PCM-F1 指部分组件匹配 F1。DFew+GPT4 指动态少样本提示 + GPT4。

默认 `find_tables` 未检出该表。下表按该页文本顺序整理。Spider 下为 EMA、EA 两列，BookSQL 下为 EMA、PCM-F1、EA、BLEU-4、ROUGE-L。“-”按原文保留。

| 模型 | Spider EMA | Spider EA | BookSQL EMA | PCM-F1 | EA | BLEU-4 | ROUGE-L |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SEDE | 63.2% | - | 43.4% | 0.82 | 44.3% | 0.69 | 0.83 |
| UniSAr | 70% | - | 43.0% | 0.78 | 47.6% | 0.72 | 0.80 |
| RESDSQL | 80.5% | 84.1% | 51.5% | 0.81 | 54.4% | 0.74 | 0.81 |
| DIN-SQL+GPT4 | 60% | 85.3% | 9.3% | 0.63 | 7.6% | 0.43 | 0.68 |
| DFew+GPT4 | - | - | 47.5% | 0.89 | 67.2% | 0.86 | 0.90 |

<!-- 原 PDF 第 8 页 -->

在 BookSQL 数据集上微调的最先进 Text-to-SQL 模型的表现。就精确匹配准确率和执行准确率而言，可以看到 RESDSQL 表现最好。SEDE 和 UniSAr 的精确匹配准确率和执行准确率较差。虽然 BookSQL 与 Spider 不能直接比较，我们也列入这些模型在 Spider 数据集上的结果，以提供一个对照参照。可以看到，在 Spider 上表现好的模型，在 BookSQL 上并没有好的表现，这说明该数据集的复杂度。表 5 给出 GPT4 在 BookSQL 测试集上的上下文学习表现。DIN-SQL+GPT4 的精确匹配准确率只有 9.3%，而动态少样本提示 + GPT4 接近微调最好的模型，精确匹配准确率为 47.5%，执行准确率为 67.2%。表 6 给出在 easy、medium 和 hard 查询上的表现。所有模型在 easy 查询上都有完美表现（执行准确率 100%），但在 medium 和 hard 查询上较为吃力。

**表 6：** 各模型在不同复杂度 SQL 查询上的执行准确率（%）。E 表示 Easy 查询，M 表示 Medium 查询，H 表示复杂度为 Hard 的查询。

默认 `find_tables` 未检出该表。下表按该页文本顺序整理，数字均来自文本抽取。表头中的 GPT4 按原文保留。

| 查询 | SEDE | UniSAr | RESDSQL | GPT4 |
| --- | --- | --- | --- | --- |
| E | 100 | 100 | 100 | 100 |
| M | 43.08 | 46.49 | 62.12 | 71.35 |
| H | 15.00 | 12.34 | 15.00 | 22.08 |

### 5.4 错误分析

我们观察到，最先进模型在带日期过滤、嵌套查询、去重聚合和领域专用过滤条件的查询上会失败。表 7 给出这些模型在测试集若干例子上的输出。DIN-SQL + GPT4 表现很差，执行准确率为 7.6%。性能差的原因或许是：不论测试问题是什么，它都使用同一条静态的思维链提示。BookSQL 的问题非常多样，并且需要领域知识。不可能仅靠提示中的少数例子就捕捉这种多样性和领域知识。因此，只要测试问题与提示中提供的例子完全不同，DIN-SQL 就会失败。动态少样本提示 + GPT4 模型针对测试问题动态选择少样本例子，从而应对 DIN-SQL 的这一局限。它把执行准确率显著提高到 67.2%。表现较差的原因可能是：1）在不同列之间发生混淆（例如 WHERE 子句用在 product_service 上还是 account 列上，见表 7）；2）把 credit、debit 和 amount 列混用，并在聚合中使用不正确的列；3）即使正确回答测试问题需要嵌套 SQL，也生成不出来；4）当正确生成 SQL 需要领域专用信息时失败。例如，invoice、sales receipt 和 purchase order 这些 transaction_type 过滤条件，或者 expense、income、account receivable 和 account payable 这些 account_type 过滤条件，会被错误地应用。

SEDE 未能生成正确的 SQL，原因可能是输入到 T5 模型时缺少问题与模式的链接。因此，它会把 customer、vendor、product_service 和 account 等不同列混在一起。UniSAr 表现较差，原因可能是 BookSQL 引入了复杂查询，例如日期过滤、嵌套查询、去重聚合等。UniSAr 引入了基于约束语法的解码，这对简单查询效果好，但在这类复杂查询上会失败。RESDSQL 是表现最好的模型。其表现不佳的原因可能是：1）在复杂的基于时间的问题上失败，例如 “What is average revenue for customer X in last 6 years”（客户 X 过去 6 年的平均收入是多少，见表 7）；2）把 credit 列和 debit 列混用；3）在需要去重聚合时失败，例如 `COUNT(DISTINCT transaction_id)`；4）在嵌套查询很多时失败。

## 6 未来方向

结果表明，最先进模型在 BookSQL 上表现较差。我们概述若干未来可能用来改进表现的方向。

**多任务学习：** 可以采用多任务学习设置，也就是除了优化 SQL 生成目标之外，再加入其他多任务目标，这可能有助于提高在困难 SQL 查询上的表现。这些目标可以包括：（1）嵌套与非嵌套 SQL 的分类；（2）distinct 关键词分类；（3）日期格式分类。

**预训练：** 对于大型数据库，当问题可能指的是某个表单元格的值时，任何模型都很难把问题中的词元与列名关联起来。在 Text-to-SQL 任务之前，

<!-- 原 PDF 第 9 页 -->

**表 7：** 不同模型在 BookSQL 测试集上的错误分析。

默认 `find_tables` 未检出该表。问句译成中文，SQL 按该页文本转写；仅拼接行末连字符。✓ 表示该行在原文中标为正确，✗ 表示标为错误。引号按 SQL 惯用的直引号转写。

**1. 问题：** 生物源城市垃圾燃料发电（Biogenic municipal waste-fueled power generation）的平均发票金额是多少？

标准 SQL（Gold SQL）：

```sql
SELECT avg(credit) FROM master_txn_table WHERE transaction_type = 'invoice' AND instr(account, 'Biogenic municipal waste-fueled power generation')
```

Few-shot GPT4：

```sql
SELECT avg(amount) FROM master_txn_table WHERE transaction_type = 'invoice' AND product_service = 'Biogenic municipal waste-fueled power generation'
```

✗

SEDE：

```sql
SELECT avg(credit) FROM master_txn_table WHERE transaction_type = 'invoice' AND instr(account, 'biogenic municipal waste-fueled power generation')
```

✓

UniSAr：

```sql
SELECT avg(credit) FROM master_txn_table WHERE transaction_type = 'invoice' AND product_service = 'Biogenic municipal waste-fueled power generation'
```

✗

RESDSQL：

```sql
SELECT avg(credit) FROM master_txn_table WHERE transaction_type = 'invoice' AND instr(account, 'biogenic municipal waste-fueled power generation')
```

✓

**2. 问题：** 在本周至今（This week to date）这一范围内，Drain cleaning 的最后一笔发票金额是多少？

标准 SQL：

```sql
SELECT max(credit) FROM master_txn_table WHERE transaction_type = 'invoice' AND instr(account,'Drain cleaning') AND transaction_date BETWEEN date( current_date, 'weekday 0', '-7 days') AND date( current_date)
```

Few-shot GPT4：

```sql
SELECT credit FROM master_txn_table WHERE transaction_type = 'invoice' AND product_service = 'Drain cleaning' AND transaction_date BETWEEN date(current_date, 'weekday 0', '-7 days') AND date(current_date) ORDER BY transaction_date DESC LIMIT 1
```

✗

SEDE：

```sql
SELECT max(credit) FROM master_txn_table WHERE transaction_type = 'invoice' AND customers = 'drain cleaning' AND transaction_date BETWEEN date( current_date, 'weekday 0', '-7 days') AND date( current_date)
```

✗

UniSAr：

```sql
SELECT max(credit) FROM master_txn_table WHERE transaction_date BETWEEN date ( current_date , 'weekday 0' , '-7 days' ) AND date ( current_date )
```

✗

RESDSQL：

```sql
SELECT max ( credit ) FROM master_txn_table WHERE transaction_type = 'invoice' AND instr ( account , 'Drain cleaning' ) AND transaction_date BETWEEN date ( current_date , 'weekday 0' , '-7 days' ) AND date ( current_date )
```

✓

**3. 问题：** 客户 Nathan Hernandez 过去 6 年的平均收入是多少？

标准 SQL：

```sql
SELECT sum(credit)/6 FROM master_txn_table WHERE customers = 'Nathan Hernandez' AND strftime('%Y', transaction_date) >= strftime('%Y', current_date)-6-1
```

Few-shot GPT4：

```sql
SELECT sum(credit)/6 FROM master_txn_table WHERE customers = 'Nathan Hernandez' AND strftime('%Y', transaction_date) >= strftime('%Y', current_date)-6-1
```

✓

SEDE：

```sql
SELECT avg(credit) FROM master_txn_table AS t1 JOIN chart_of_accounts AS t2 ON t1.account = t2.account_name WHERE account_type IN ('income','other income') AND customers = 'nathan hernandez' AND transaction_date BETWEEN date(current_date,'start of year','-6 year') AND date(current_date,'start of year','-1 day')
```

✗

UniSAr：

```sql
SELECT avg(credit) FROM master_txn_table as T1 JOIN chart_of_accounts as T2 on T1.account = T2.account_name WHERE account_type in ( 'Income' , 'Other Income' ) AND customers = 'Nathan Hernandez' AND transaction_date BETWEEN date ( current_date ,'start of year' , '-6 year' ) AND date ( current_date ,'start of year' , '-1 day')
```

✗

RESDSQL：

```sql
SELECT sum (credit) / 6 FROM master_txn_table WHERE customers = 'Nathan Hernandez' AND strftime ( '%Y' , transaction_date ) >= strftime ( '%Y' , current_date ) - 1 GROUP BY strftime ( '%Y' , transaction_date )
```

✗

可以进行预训练，以便更好地理解问题与表之间的关系。这可以用掩码建模来做：定义列恢复、列预测之类的任务，把少数词元掩掉，让模型尝试恢复并预测被掩掉的词元；Shi 等人（2020a）经由 GAP 模型提出了类似做法。

**多步少样本提示：** 也可以用动态少样本提示分多步生成 SQL，而不是一步生成。

**值编码：** 上下文学习模型（GPT4）会把不同的列混在一起，原因是缺少关于表内容的知识。把相关的表行加进提示，可能缓解这一问题。

## 7 结论

本文提出 BookSQL，这是一个将在金融与会计领域有广泛应用的 Text-to-SQL 数据集。若干 Text-to-SQL 模型的实验结果说明，仍有相当大的改进空间。未来我们打算构建一个更稳健的模型，使之能够处理困难查询并提高表现。

<!-- 原 PDF 第 10 页 -->

## 局限

由于这是一篇资源论文，我们发布一个大规模数据集，因而对 Text-to-SQL 系统的建模着墨较少。我们测试了现有的 Text-to-SQL 系统，看它们在这个新数据集上表现如何。结果说明仍有相当大的改进余地。未来我们将专注于开发在 BookSQL 上表现更好的新模型。此外，我们希望数据集发布之后，能促进该领域的更多研究，从而产生更有意思的模型。

## 伦理声明

考虑到隐私，我们在数据集中创建的是匿名化条目。此外，数据集由财务专家核对，以确保条目遵守会计原则，并反映真实场景。我们将公开发布该数据集，供研究使用。据我们所知，我们没有发现所提出数据集的其他可能伦理后果。

## 参考文献

Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. 2023. GPT-4 技术报告. arXiv preprint arXiv:2303.08774.

Naihao Deng, Yulong Chen, and Yue Zhang. 2022. Text-to-SQL 的最新进展：关于我们已有什么、以及我们期待什么的综述. In COLING, Gyeongju, Republic of Korea. International Committee on Computational Linguistics.

Longxu Dou, Yan Gao, Mingyang Pan, Dingzirui Wang, Wanxiang Che, Dechen Zhan, and Jian-Guang Lou. 2022. UniSAr：面向 Text-to-SQL 的统一结构感知自回归语言模型.

Catherine Finegan-Dollak, Jonathan K. Kummerfeld, Li Zhang, Karthik Ramanathan, Sesh Sadasivam, Rui Zhang, and Dragomir Radev. 2018. 改进 Text-to-SQL 评估方法. In Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 351–360, Melbourne, Australia. Association for Computational Linguistics.

Moshe Hazoom, Vibhor Malik, and Ben Bogin. 2021a. 真实环境中的 Text-to-SQL：一个基于 Stack Exchange 数据、自然出现的数据集. In Proceedings of the 1st Workshop on Natural Language Processing for Programming (NLP4Prog 2021), pages 77–87, Online. Association for Computational Linguistics.

Moshe Hazoom, Vibhor Malik, and Ben Bogin. 2021b. 真实环境中的 Text-to-SQL：一个基于 Stack Exchange 数据、自然出现的数据集. arXiv preprint arXiv:2106.05006.

Chia-Hsuan Lee, Oleksandr Polozov, and Matthew Richardson. 2021. KaggleDBQA：对 Text-to-SQL 解析器的真实评估. In Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers), pages 2261–2273, Online. Association for Computational Linguistics.

Fei Li and H. V. Jagadish. 2014. 为关系数据库构建交互式自然语言接口. Proc. VLDB Endow., 8(1):73–84.

Haoyang Li, Jing Zhang, Cuiping Li, and Hong Chen. 2023a. RESDSQL：为 Text-to-SQL 解耦模式链接与骨架解析. In Proceedings of the Thirty-Seventh AAAI Conference on Artificial Intelligence (AAAI).

Jinyang Li, Binyuan Hui, Ge Qu, Binhua Li, Jiaxi Yang, Bowen Li, Bailin Wang, Bowen Qin, Rongyu Cao, Ruiying Geng, Nan Huo, Chenhao Ma, Kevin C. C. Chang, Fei Huang, Reynold Cheng, and Yongbin Li. 2023b. 大语言模型是否已经能够充当数据库接口？一个面向大规模、以数据库为根据的 Text-to-SQL 的大型基准.

Chin-Yew Lin. 2004. ROUGE：一个自动评估摘要的工具包. In Text Summarization Branches Out, pages 74–81, Barcelona, Spain. Association for Computational Linguistics.

Kishore Papineni, Salim Roukos, Todd Ward, and Wei jing Zhu. 2002. BLEU：一种自动评估机器翻译的方法. pages 311–318.

Mohammadreza Pourreza and Davood Rafiei. 2023. DIN-SQL：带自校正的、对 Text-to-SQL 的分解式上下文学习. arXiv preprint arXiv:2304.11015.

Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, and Peter J Liu. 2020. 用统一的文本到文本 Transformer 探索迁移学习的极限. The Journal of Machine Learning Research, 21(1):5485–5551.

Peng Shi, Patrick Ng, Zhiguo Wang, Henghui Zhu, Alexander Hanbo Li, Jun Wang, Cicero Nogueira dos Santos, and Bing Xiang. 2020a. 借助生成增强预训练来学习语义解析的上下文表示.

Tianze Shi, Chen Zhao, Jordan Boyd-Graber, Hal Daumé III, and Lillian Lee. 2020b. 词汇–逻辑对齐对于把语义解析为 SQL 查询的潜力. In Findings of the Association for Computational Linguistics: EMNLP 2020, pages 1849–1864, Online. Association for Computational Linguistics.

<!-- 原 PDF 第 11 页 -->

Ruoxi Sun, Sercan O Arik, Hootan Nakhost, Hanjun Dai, Rajarishi Sinha, Pengcheng Yin, and Tomas Pfister. 2023. SQL-PaLM：改进大语言模型对 Text-to-SQL 的适配. arXiv preprint arXiv:2306.00739.

Lappoon R. Tang and Raymond J. Mooney. 2001. 在归纳逻辑程序设计中使用多个子句构造器进行语义解析. In Proceedings of the 12th European Conference on Machine Learning, pages 466–477, Freiburg, Germany.

Ping Wang, Tian Shi, and Chandan K. Reddy. 2020. 面向电子病历问答的 Text-to-SQL 生成. In Proceedings of The Web Conference 2020, WWW ’20, page 350–361, New York, NY, USA. Association for Computing Machinery.

Navid Yaghmazadeh, Yuepeng Wang, Isil Dillig, and Thomas Dillig. 2017. SQLizer：从自然语言合成查询. Proc. ACM Program. Lang., 1(OOPSLA).

Tao Yu, Rui Zhang, Kai Yang, Michihiro Yasunaga, Dongxu Wang, Zifan Li, James Ma, Irene Li, Qingning Yao, Shanelle Roman, Zilin Zhang, and Dragomir Radev. 2018. Spider：一个面向复杂且跨领域的语义解析与 Text-to-SQL 任务的大规模人工标注数据集.

Victor Zhong, Caiming Xiong, and Richard Socher. 2017. Seq2SQL：用强化学习从自然语言生成结构化查询. CoRR, abs/1709.00103.

<!-- 原 PDF 第 12 页 -->

## 附录

### A 数据集细节

- 表 8 给出主交易表。
- 表 9 给出会计科目表。
- 表 10 给出客户表。
- 表 11 给出供应商表。
- 表 12 给出员工表。
- 表 13 给出产品与服务表。
- 表 14 给出付款方式表。

**BookSQL 中的企业分布。** 全部企业及其产品的分布见图 4。每个行业表示在内圈层，其后是该行业的企业（在中圈），其产品在外圈。每个行业包含多家企业，每家企业包含多种产品和服务。

<!-- 原 PDF 第 13 页 -->

**图 3：** BookSQL 企业分布示例。中间部分给出企业的样本集合，内层给出与相应企业关联的行业，最外层给出该企业的相应产品。此图根据 https://www.ibisworld.com/united-states/list-of-industries/ 上的信息制作。

默认 `find_tables` 未检出表格。文本层没有标出下列字符串属于内圈、中圈还是外圈，因此只按阅读顺序转写，不自行归层。

- Industry（行业）
- Accommodation and Food Services（住宿与餐饮服务）
- Hotels and motel services（旅馆与汽车旅馆服务）
- Casino Hotels（赌场酒店）
- Camping and Parking（露营与停车）
- Traveller accommodation（旅客住宿）
- Golf Courses & Country Clubs（高尔夫球场与乡村俱乐部）
- Golf Equipment Rental Services（高尔夫器材租赁服务）
- Golf Equipment（高尔夫器材）
- Golf Courses（高尔夫球场）
- Tournaments and Matches（锦标赛与比赛）
- Adoption & Child Welfare Services（收养与儿童福利服务）
- Children and youth recreational programs（儿童与青少年娱乐项目）
- Youth guidance（青少年指导）
- Child abuse prevention（虐待儿童预防）
- Self-help programs（自助项目）
- Aircraft, Marine & Railroad Transportation Equipment Wholesaling（飞机、船舶与铁路运输设备批发）
- Wholesaling aircraft engines and parts（飞机发动机及零件批发）
- Aeronautical Equipment（航空设备）
- Aircraft Engines（飞机发动机）
- Marine Supplies（船舶用品）

<!-- 原 PDF 第 14 页 -->

**图 4：** BookSQL 企业分布。这里，内圈表示行业，中圈表示与相应行业关联的企业集合，最外圈表示该企业的相应产品。此图根据 https://www.ibisworld.com/united-states/list-of-industries/ 上的信息制作。

该环形图中的行业、企业与产品名称未进入文本层，见原 PDF 第 14 页。

<!-- 原 PDF 第 15 页 -->

### B 动态少样本提示 + GPT4

给定一个测试问题，为其动态选择少样本训练示例的伪代码如下。文本层在部分标识符的字母之间插入了空格，下面去掉这些空格；导入路径、类名和参数按抽出的词符还原，未改逻辑。

```python
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.prompts.example_selector import MaxMarginalRelevanceExampleSelector
from langchain.vectorstores import Chroma
example_selector = MaxMarginalRelevanceExampleSelector.from_examples(
    examples,
    HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
    Chroma,
    k=10,
    input_keys=["input"]
)
```

#### B.1 示例提示

数据库模式：

```text
Table master_txn_table, columns = [*, Transaction_ID, Transaction_DATE, Transaction_TYPE, Amount, CreatedDATE, CreatedUSER, Account, AR_paid, AP_paid, Due_DATE, Open_balance, Customers, Vendor, Product_Service, Quantity, Rate, Credit, Debit, payment_method, Misc]
Table chart_of_accounts, columns = [*, Account_name, Account_type]
Table customers, columns = [*, customer_name, customer_full_name, Billing_address, Billing_city, Billing_state, Billing_ZIP_code, Shipping_address, Shipping_city, Shipping_state, Shipping_ZIP_code, Balance]
Table employees, columns = [*, Employee_name, Employee_ID, Hire_date, Billing_rate, Deleted]
Table products, columns = [*, Product_Service, Product_Service_type]
Table vendors, columns = [*, Vendor_name, Billing_address, Billing_city, Billing_state, Billing_ZIP_code, Balance]
Table payment_method, columns = [*, Payment_method, Credit_card]
Foreign_keys = [master_txn_table.Account = chart_of_accounts.Account_name, master_txn_table.Customers = customers.customer_name, master_txn_table.Vendor = vendors.Vendor_name, master_txn_table.Product_Service = products.Product_Service, master_txn_table.payment_method = payment_method.payment_method]
```

下面是问题及其对应 SQL 查询的示例。

«来自训练集的 10 个少样本示例»

把下面的问题翻译成 SQL 查询。

输入：客户 Ronald Bailey 有多少未结信用额度（open credit）？

输出：SELECT

原文的输出在 “SELECT” 处截断，其后即为附录 C 的标题，未见后续 SQL。公式抽取不完整，见原 PDF 第 15 页。

### C DIN-SQL+GPT4 的提示

下面一节给出 DIN-SQL 各个模块所用的提示样本。为求简短，这些提示样本里我们只放入了 1 个少样本示例。不过在实际使用中会用 5–10 个少样本示例，并在提示末尾用 « » 标出。

#### C.1 模式链接提示

该提示再次列出数据库模式。本页文本在 `customers` 的列清单处截断，后续列见下一页。

```text
Table master_txn_table, columns = [*, Transaction_ID, Transaction_DATE, Transaction_TYPE, Amount, CreatedDATE, CreatedUSER, Account, AR_paid, AP_paid, Due_DATE, Open_balance, Customers, Vendor, Product_Service, Quantity, Rate, Credit, Debit, payment_method, Misc]
Table chart_of_accounts, columns = [*, Account_name, Account_type]
Table customers, columns = [*, customer_name, customer_full_name, Billing_address, Billing_city,
```

<!-- 原 PDF 第 16 页 -->

```text
Billing_state, Billing_ZIP_code, Shipping_address, Shipping_city, Shipping_state, Shipping_ZIP_code, Balance]
Table employees, columns = [*, Employee_name, Employee_ID, Hire_date, Billing_rate, Deleted]
Table products, columns = [*, Product_Service, Product_Service_type]
Table vendors, columns = [*, Vendor_name, Billing_address, Billing_city, Billing_state, Billing_ZIP_code, Balance]
Table payment_method, columns = [*, Payment_method, Credit_card]
Foreign_keys = [master_txn_table.Account = chart_of_accounts.Account_name, master_txn_table.Customers = customers.customer_name, master_txn_table.Vendor = vendors.Vendor_name, master_txn_table.Product_Service = products.Product_Service, master_txn_table.payment_method = payment_method.payment_method]
```

问：客户 Ronald Bailey 有多少未结信用额度？

S：

```sql
select sum(open_balance) from ( select distinct transaction_id, open_balance from master_txn_table where customers = 'Ronald Bailey')
```

答：让我们逐步思考。在问题「客户 Ronald Bailey 有多少未结信用额度？」中，我们被问到的是「有多少未结信用额度」，因此需要的列 = [master_txn_table.open_balance]。「未结信用额度，客户 Ronald Bailey」，因此需要的列 = [master_txn_table.transaction_id, master_txn_table.customers]。基于这些列和表，我们需要的外键 Foreign_keys = []。基于这些表、列和外键，可能的单元格值集合 = [Ronald Bailey]。因此模式链接为：Schema_links: [master_txn_table.open_balance, master_txn_table.customers, master_txn_table.transaction_id, Ronald Bailey]

«另有 9 个少样本示例»

#### C.2 分类提示

问：我的月初至今（MTD）交易有哪些？

schema_links: [master_txn_table.transaction_id, master_txn_table.amount, master_txn_table.transaction_date]

答：让我们逐步思考。问题「我的月初至今交易有哪些？」的 SQL 查询需要这些表 = [master_txn_table]，因此不需要 JOIN。另外，它不需要带有（INTERSECT、UNION、EXCEPT、IN、NOT IN）的嵌套查询，并且我们需要这些问题的答案 = [""]。因此，不需要 JOIN，也不需要嵌套查询，于是该 SQL 查询可以归类为 "EASY"。

标签："EASY"

问：有多少产品从未以高于 5 的总价值售出？

schema_links: [Product_Service.transaction_id, master_txn_table.transaction_type]

答：让我们逐步思考。问题「有多少产品从未以高于 5 的总价值售出？」的 SQL 查询需要这些表 = [Product_Service, master_txn_table]，因此需要 JOIN。另外，它需要带有（INTERSECT、UNION、EXCEPT、IN、NOT IN）的嵌套查询，或者 FROM 子句内部的内层查询，并且我们需要这些问题的答案 = ["以高于 5 的总价值售出的产品"]。因此，需要 JOIN，也需要嵌套查询，于是该 SQL 查询可以归类为 "NESTED"。

标签："NESTED"

问：年初至今（YTD），我们最小的费用是多少？

schema_links = [master_txn_table.account = chart_of_accounts.account_name, master_txn_table.credit, master_txn_table.transaction_date, master_txn_table.account_type, master_txn_table.debit]

答：让我们逐步思考。问题「年初至今，我们最小的费用是多少？」的 SQL 查询需要这些表 = [master_txn_table, chart_of_accounts]，因此需要 JOIN。另外，它不需要带有（INTERSECT、UNION、EXCEPT、IN、NOT IN）的嵌套查询，并且我们需要这些问题的答案 = [""]。因此，需要 JOIN，不需要嵌套查询，于是该 SQL 查询可以归类为 "NON-NESTED"。

标签："NON-NESTED"

<!-- 原 PDF 第 17 页 -->

«另有 7 个少样本示例»

#### C.3 SQL 生成

##### C.3.1 简单提示

问："客户 Ronald Bailey 有多少未结信用额度？"

Schema_links: [master_txn_table.open_balance, master_txn_table.transaction_id, master_txn_table.customers,Ronald Bailey]

SQL：

```sql
select sum(open_balance) from ( select distinct transaction_id, open_balance from master_txn_table where customers = 'Ronald Bailey')
```

«另有 4 个少样本示例»

##### C.3.2 非嵌套复杂提示

问："今天我们向 Ethan Walker 卖出了多少 Traveller accomodation？"（原文产品名拼作 accomodation）

Schema_links: [master_txn_table.quantity ,master_txn_table.customers, master_txn_table.product_service, master_txn_table.transaction_type, master_txn_table.transaction_date]

答：让我们逐步思考。为给定问题创建 SQL 时，我们需要连接这些表 = []。首先创建一个中间表示，再用它构造 SQL 查询。

中间表示：

```sql
select sum(master_txn_table.quantity) from master_txn_table where master_txn_table.customers = 'Ethan Walker' and master_txn_table.product_service = 'Traveller accomodation' and master_txn_table.trasaction_type in ('invoice','sales receipt') and master_txn_table.transaction_date BETWEEN date(current_date) AND date(current_date)
```

原文把 `transaction_type` 写成 `trasaction_type`，此处照录。

紧接着的 SQL 在人名和产品名的引号处乱码。原串保留如下。公式抽取不完整，见原 PDF 第 17 页。

```text
select sum(quantity) from master_txn_table where customers = Ëthan Walkeränd product_service = ¨Traveller accomodationänd trasaction_type in ('invoice','sales receipt') and transaction_date BETWEEN date(current_date) AND date(current_date)
```

«另有 9 个少样本示例»

##### C.3.3 嵌套复杂提示

问："有多少产品从未以高于 5 的总价值售出？"

Schema_links: [master_txn_table.product_service, master_txn_table.transaction_type, master_txn_table.credit, product_service.*]

答：让我们逐步思考。「有多少产品从未以高于 5 的总价值售出？」可以通过知道下面这个子问题的答案来求解：「把从未以高于 5 的总信用额售出的全部产品给我看」。子问题「把从未以高于 5 的总信用额售出的全部产品给我看」的 SQL 查询是：

```sql
SELECT count(*) FROM Product_Service WHERE product_service NOT IN ( SELECT product_service FROM master_txn_table WHERE transaction_type in ('invoice','sales receipt') group by product_service having sum(credit)>5)
```

因此，问题「有多少产品从未以高于 5 的总价值售出？」的答案 = 中间表示：

```sql
SELECT count(Product_Service.*) FROM Product_Service WHERE Product_Service.product_service NOT IN ( SELECT master_txn_table.product_service FROM master_txn_table WHERE master_txn_table.transaction_type in ('invoice','sales receipt') group by master_txn_table.product_service having sum(master_txn_table.credit) > 5)
```

SQL：

```sql
SELECT count(*) FROM Product_Service WHERE product_service NOT IN ( SELECT product_service FROM master_txn_table WHERE transaction_type in ('invoice','sales receipt') group by product_service having sum(credit) > 5)
```

«另有 9 个少样本示例»

#### C.4 自校正提示

对给定问题，使用所提供的表、列、外键和主键，修正给定的 SQLite SQL QUERY 中的任何问题。如果有问题，就修正它们。如果没有问题，就按原样返回该 SQLite SQL QUERY。

修正 SQL QUERY 时使用下列说明：

1）使用问题中明确提到的数据库值。

<!-- 原 PDF 第 18 页 -->

2）借助 Foreign_keys，注意用于 JOIN 的列。

3）在需要时使用 DESC 和 DISTINCT。

4）注意用于 GROUP BY 语句的列。

5）注意用于 SELECT 语句的列。

6）只在必要时修改 GROUP BY 子句（避免 GROUP BY 中的冗余列）。

7）只对一列使用 GROUP BY。

### D 评价指标

使用下列标准指标：

- 精确匹配准确率（Exact Match Accuracy）（Yu 等人，2018）：把预测 SQL 和标准 SQL（Gold SQL）都分解成不同的 SQL 组件，例如 SELECT、WHERE、GROUP BY 等。若全部 SQL 组件都与标准 SQL 精确匹配，则把预测 SQL 标为正确。
- 执行准确率（Execution Accuracy）（Yu 等人，2018）：预测 SQL 在数据库上执行的输出，与标准 SQL 的执行输出相同。
- 部分组件匹配 F1（Partial Component Match F1）（Hazoom 等人，2021a）：用 JSqlParser¹² 把预测查询和标准查询都解析成树。比较这两棵解析树，并根据匹配子树的数量计算一个汇总分数。原文把 trees 拼作 tress。
- BLEU-4（Papineni 等人，2002）：度量预测 SQL 与标准 SQL 之间匹配的 n-gram 数量。
- ROUGE-L（Lin，2004）：基于预测 SQL 与标准 SQL 之间的最长公共子序列（LCS）。共享序列越长，表示预测 SQL 与标准 SQL 越相似。

¹² https://github.com/JSQLParser/JSqlParser

### E 训练细节与超参数

全部实验在一块 NVIDIA A10G Tensor Core GPU 上完成。

对于 SEDE，我们用 T5-Large 作为基础的序列到序列模型，学习率为 $5 \times 10^{-5}$，训练 15 个 epoch，批大小为 6。解码使用束宽 6，最大解码步数为 250。

对于 UniSAr，我们用 T5-Large 作为基础语言模型，学习率为 $1 \times 10^{-5}$，最大词元数为 1024。我们采用 polynomial_decay，预热更新 5,000 次。dropout 率为 0.1。优化器为 Adam，使用默认参数。max-update 设为 10,000。根据经验，该模型在 BookSQL 上大约于 $10 \sim 15$ 个 epoch 取得最好表现。Fairseq 会动态调整批大小，以提高 GPU 利用率。

对于 RESDSQL，我们使用原论文和代码所建议的设置。Schema Item Classifier 模块使用 RoBERTa-large 模型，学习率为 $1 \times 10^{-5}$，有效批大小为 32（使用梯度累积）。topk_table_num 取 4，topk_column_num 取 8。对于 text2sql 模块，使用 T5-large 模型，学习率为 $5 \times 10^{-5}$，有效批大小为 32（使用梯度累积）。解码使用束搜索，num_beams 设为 8，num_return_sequences 设为 8。

对于 DIN-SQL+GPT4 和动态少样本提示 + GPT4，我们使用 OpenAI GPT4 API，设置为：n = 1，temperature = 0.0，max_tokens = 600，top_p = 1.0，frequency_penalty = 0.0，presence_penalty = 0.0。鉴于对 OpenAI GPT4 API 的调用次数有限，对基于 GPT4 的方法，我们使用 BookSQL 测试集中随机抽取的 10%。

<!-- 原 PDF 第 19 页 -->

**表 8：** 主交易表。

表抽取失败，见原 PDF 第 19 页。

**表 9：** 会计科目表。

默认 `find_tables` 未检出该表。下面按该页文本中重复的四元组（企业编号、科目名称、科目全称、科目类型）转写，未改数字，也未补行。

| 企业 Id | 科目名称 | 科目全称 | 科目类型 |
| --- | --- | --- | --- |
| 2 | Accumulated Depreciation | Accumulated Depreciation | Fixed Asset |
| 2 | Furniture and Equipment | Furniture and Equipment | Fixed Asset |
| 2 | Payroll Liabilities | Payroll Liabilities | Other Current Liability |
| 2 | Opening Balance Equity | Opening Balance Equity | Equity |
| 2 | Owners Draw | Owners Draw | Equity |
| 2 | Owners Equity | Owners Equity | Equity |
| 2 | Accounting Service Income | Accounting Service Income | Income |
| 2 | Consulting Income | Consulting Income | Income |
| 2 | Tax Preparation Services Income | Tax Preparation Services Income | Income |

**表 10：** 客户表。

表抽取失败，见原 PDF 第 19 页。

<!-- 原 PDF 第 20 页 -->

**表 11：** 供应商表。

默认 `find_tables` 未检出该表。下面按该页文本顺序整理。地址按换行拼回，未改数字。

| 企业 Id | 供应商名称 | 账单地址 | 账单城市 | 账单州 | 账单邮政编码 | 余额 |
| --- | --- | --- | --- | --- | --- | --- |
| 2 | Shelly Ramos | 82768 Dawn Crescent | West Cynthia | WY | 39877 | 4042.15 |
| 2 | Jade Barnett | 782 Mitchell Camp Suite 676 | Grahambury | KS | 80370 | 12949.89 |
| 2 | Nicole Jordan | 14959 Mccullough Green Suite 029 | East Kevinfurt | WI | 42930 | 5294.89 |
| 2 | Adam Pena | 192 Brenda Gardens | Erinmouth | IA | 93008 | 6949.89 |
| 2 | Jeffrey Roman | 784 Cameron Parks Apt. 902 | North Gloriafurt | AR | 48141 | 7299.89 |
| 2 | Zachary Butler | 61717 Christopher Cliffs Apt. 122 | Port Joshua | MT | 44164 | 465.09 |
| 2 | Taylor Moses | 19368 Jenny Courts Apt. 094 | Kerristad | OR | 25430 | 65.09 |
| 2 | John Russo | Unit 6387 Box 0856 | DPO | AA | 73133 | 1538.8 |
| 2 | Robert Phillips | USCGC Steele | FPO | AA | 91533 | 55388.8 |

**表 12：** 员工表。

默认 `find_tables` 未检出该表。计费费率在原文中为破折号，未改成数字。

| 企业 Id | 员工姓名 | 员工 Id | 入职日期 | 计费费率 | 已删除 |
| --- | --- | --- | --- | --- | --- |
| 2 | Stephanie Baker | STE123 | 07/17/2022 | – | No |
| 2 | Julia Rivera | JUL456 | 07/31/2002 | – | No |
| 2 | Valerie Kline | VAL232 | 04/15/2012 | – | Yes |
| 2 | Greg Cardenas | GRE443 | 08/27/2013 | – | No |
| 2 | Mr. Zachary Levy | ZAC998 | 01/28/2000 | – | Yes |
| 2 | Taylor Hughes | TAY009 | 07/17/2022 | – | Yes |
| 2 | Jodi Bishop | JOD778 | 12/27/2016 | – | Yes |
| 2 | Andrew Flores | AND667 | 05/20/2018 | – | No |
| 2 | Earl Lee | EAR221 | 08/19/2002 | – | No |

**表 13：** 产品与服务表。

默认 `find_tables` 未检出该表。下列按该页文本顺序整理。

| 企业 Id | Product_service | Product_Service_type |
| --- | --- | --- |
| 2 | Hours | Service |
| 2 | Services | Service |
| 2 | Design | Service |
| 2 | Installation | Service |
| 2 | Lighting | Service |
| 2 | Maintenance & Repair | Service |
| 2 | Refunds & Allowances | Service |

**表 14：** 付款方式。

默认 `find_tables` 未检出该表。下列按该页文本顺序整理。

| 企业 Id | 付款方式 | 信用卡 |
| --- | --- | --- |
| 1 | Cash | No |
| 1 | Check | No |
| 1 | Visa | Yes |
| 1 | MasterCard | Yes |
| 1 | Discover | Yes |
| 1 | American Express | Yes |
| 1 | Diners Club | Yes |

<!-- 译完 -->
