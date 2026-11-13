> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

首页标题与 `01-text-to-sql/TAG_arXiv2408.14717.pdf` 相同。以下只依据本目录的 TAG_CIDR2025.pdf。

- 原文件名：TAG_CIDR2025.pdf
- 原文标题：Text2SQL is Not Enough: Unifying AI and Databases with TAG
- 作者：Asim Biswal、Liana Patel（同等贡献）、Siddharth Jha、Amog Kamsetty、Shu Liu、Joseph E. Gonzalez、Carlos Guestrin、Matei Zaharia。标注 1 的作者属 UC Berkeley，标注 2 的 Carlos Guestrin 与 Liana Patel 属 Stanford University
- 场合：CIDR 2025（CIDR’25），2025 年 1 月 19–22 日，阿姆斯特丹

## 摘要

能用自然语言问数据库的系统，本可以同时用上语言模型的推理与世界知识，以及数据管理系统的可扩展计算，从而对用户自己的数据发问。现有方法和评测没有覆盖这个设定。Text2SQL 只处理能写成关系代数的问题，只是真实问题的一小部分。RAG 只处理对库中一条或少数几条记录做 point lookup 就能回答的查询。作者提出 Table-Augmented Generation（TAG），作为一种统一、通用的数据库自然语言问答范式，用来表示此前没被充分研究的 LM 与数据库交互，并利用 LM 的世界知识和推理。

他们系统性地做了 TAG 评测。标准方法正确回答的查询不超过 20%。代码在 https://github.com/TAG-Research/TAG-Bench 。

## 1 Introduction

第 1 节的出发点是：Text2SQL 和 RAG 的研究很多，但作者在 Databricks 的内部负载和客户里看到，真实问题经常超出这两种范式。业务问题往往要同时用领域知识、世界知识、精确计算和语义推理。数据库提供的是最新数据和可扩展的精确计算，而 LM 不擅长后者。LM 补上两样东西。一是对文本的语义推理。Databricks 客户调查里的例子包括：产品 X 的哪些评论是正面的，以及为什么某段时间销售额下降。情感分析和趋势总结无法写成传统数据库的精确计算或关系原语。二是训练进权重里的世界知识。内部用户问 “retail” 垂直领域的 QoQ 趋势，表里只有账户名、产品和收入。系统还得知道企业如何定义 QoQ（上一季度到本季度，或去年同季到今年同季），以及哪些公司算零售。这适合预训练或微调过的 LM。

因此 Text2SQL [26, 28, 31, 32] 只覆盖有直接关系等价物的自然语言问题。判断评论正负需要按行做 LM 推理；解释销售额下降则要跨许多行聚合。RAG 则是按相关性做少量记录的 point lookup，再调用一次 LM。它既做不了更丰富的数据库执行，又把计数、数学和过滤交给一次容易出错的 LM 调用。LM 在长上下文上表现差，也限制了 RAG 生成阶段处理大规模数据的能力。

TAG 把回答过程收成 Figure 1 的三步，并用三个式子定义：query synthesis 为 syn(R) → Q（式 1），query execution 为 exec(Q) → T（式 2），answer generation 为 gen(R, T) → A（式 3）。R 是任意自然语言请求，Q 是可执行数据库查询，T 是算出来的相关数据，A 是最终自然语言答案。生成阶段可以按迭代或递归方式编排 LM。Text2SQL 和 RAG 被看成 TAG 的特例，只服务一部分问题。作者给出第一个端到端 TAG 评测，查询需要 LM 的推理和知识。比较对象包括原始 Text2SQL 与 RAG，以及两个更强基线：带 LM 生成的 Text2SQL，和带 LM 重排的检索。各类查询上，每个基线的 exact match 都不超过 20%。他们在 LOTUS [21] 上写的手工 TAG 流水线，准确率比基线高出至多 20–65%。这个差距被用来说明高效 TAG 系统值得做。

## 2 THE TAG MODEL

第 2 节把模型定义成：输入自然语言请求 R，输出以数据为依据的自然语言答案 A。三步按一次迭代来定义，以便讨论；也可以扩展成 multi-hop。

2.1 的 syn 负责两件事：根据表 schema 判断哪些数据与请求相关，再把请求语义解析成数据库能执行的查询。查询语言不限定，例子用 SQL。Figure 1 的请求是 “Summarize the reviews of the highest grossing romance movie considered a ‘classic’.” 表里有 movie_title、revenue、genre 和 review。这一步用 LM 的语义推理生成涉及这些属性的 SQL。文中特别指出，若数据库 API 能在 SQL 里执行 LM UDF，syn 还会为每一行插入 LM 调用，用来判断影片是否算 classic。2.2 的 exec 在数据库引擎上执行 Q，得到表 T，利用引擎在大量数据上的效率。具体 API 留到第 3 节讨论；有的 API 允许 LM 算子 [18–21]，于是世界知识和推理可以发生在执行过程内部。Figure 1 的查询同时做选择和排序：用 LM 按 movie_title 判断是否 classic，用普通谓词筛 Romance，再按 revenue 取最高。图中 Shang-Chi 是 Action、收入 432.2，被筛掉；留下的是 Titanic，类型 Romance，收入 2257.8，并带有 “still best…” 和 “a guilty…” 两条评论。

2.3 的 gen 对应 RAG 里的生成：用 LM 根据 R 和 T 写出 A。Figure 1 的最终答案概括 Titanic 的评论，原文示例是 “The reviews of Titanic discuss the on screen chemistry…”。相关表被编码成字符串，和原始请求一起送给模型，由模型对 review 列做语义总结。
