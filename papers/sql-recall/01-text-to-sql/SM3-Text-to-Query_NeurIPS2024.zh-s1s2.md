# SM3-Text-to-Query: Synthetic Multi-Model Medical Text-to-Query Benchmark

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`SM3-Text-to-Query_NeurIPS2024.pdf`。

## Abstract 摘要

电子健康记录（electronic health records, EHRs）存储在多种数据库系统中。这些系统采用不同的数据库模型，并运行在异构存储架构上，例如关系数据库、文档存储或图数据库。不同的数据库模型对查询复杂度与性能有很大影响。尽管这在数据库研究中已是已知事实，它对日益增多的 Text-to-Query 系统意味着什么，迄今出人意料地尚未被研究。本文提出 SM3-Text-to-Query，首个多模型医学 Text-to-Query 基准。它基于 Synthea 的合成患者数据，并遵循 SNOMED-CT 分类体系——一种广泛使用、覆盖医学术语的知识图谱本体。SM3-Text-to-Query 为关系数据库（PostgreSQL）、文档存储（MongoDB）以及图数据库（Neo4j 与 GraphDB（RDF））提供数据表示，从而可以跨四种流行查询语言评测，即 SQL、MQL、Cypher 与 SPARQL。我们系统且人工地编写 408 道模板问题，并加以扩充，为这四种查询语言构建包含 10K 对多样化自然语言问题/查询对的基准（共计 40K 对）。在该数据集上，我们针对一组有代表性的闭源与开源大语言模型（large language models, LLMs），评测若干常见的上下文学习（in-context-learning, ICL）方法。评测揭示了不同 ICL 策略与 LLM 下，数据库模型与查询语言之间的权衡。最后，SM3-Text-to-Query 易于扩展到更多查询语言，或扩展到真实的、基于标准的患者数据库。

## 1 Introduction 引言

卫生部门正在加速数字化，数据存储于电子健康记录（electronic health records, EHR）[25]。实践中，这些记录可以保存在多种形式与系统中：(i) 传统关系数据库，如 PostgreSQL 或 Oracle，实现关系数据模型：数据被组织成关系（表），而关系是元组（行）的集合。用户通过声明式查询语言 SQL 访问数据；(ii) 流行的文档数据库，如 MongoDB，把数据建模为文档数据模型中的文档集合，并通过 MongoDB 查询语言（MongoDB Query Language, MQL）等专门语言提供数据访问；(iii) 图数据库（三元组存储，triple stores）把数据建模为属性图（例如 Neo4j）或语义 RDF 图（例如 Ontotext GraphDB），分别通过查询语言 Cypher 与 SPARQL 提供接口。

尽管关系模型与 SQL 查询语言仍是 EHR 的首要选择 [22]，由于模式灵活性以及跨数据孤岛互联数据源的天然能力，文档与图数据库模型受到的关注正在增加 [37, 11, 7]。例如，AICCELERATE 是最近一项关于数字医院的大规模欧洲试点项目，它使用图模型连接多种数据源，包括传统 EHR、其他医院数据、可穿戴设备与物联网（IoT）设备 [1]。此外，以 SPARQL 为主要查询语言的 RDF 图数据库在生命科学中被广泛使用，医学领域也在迅速跟上 [34]。

数据库的选择以及底层核心数据模型（关系、文档、图）对读/写性能与查询复杂度有很大影响。例如，图模型天然表示多对多关系，如患者、医生、治疗与医疗状况之间的连接，而关系数据库则可能需要代价高昂的连接操作与复杂查询。文档数据库对多对多关系只有初步支持，面向的是数据互联程度不高、并以灵活模式存储在文档集合中的场景 [19]。图 1 展示同一用户问题及其在四种查询语言中对应查询语句的例子。尽管这些差异在数据库研究与工业界已是已知事实，它对日益增多的 Text-to-Query 系统意味着什么，迄今出人意料地尚未被研究。

图 1：同一用户请求在不同查询语言与数据库系统中的差异（Differences across query languages and database systems for the same user request）。用户请求原文为：“Provide me the names of patients that are linked with the organization Royal of Fairhaven Nursing Center.” 图中 SQL、SPARQL、Cypher 与 MongoDB 查询语句在 PDF 抽取中空格粘连，并与 #Tokens、#Keywords、#Joins/Traversals、Nesting Depth 等指标交错，【抽取不清】，此处不复原查询文本。抽取中可见的指标数值为：#Tokens 25、#Keywords 8、#Joins/Traversals 2、Nesting Depth 0；#Tokens 12、#Keywords 3、#Joins/Traversals 3、Nesting Depth 1；#Tokens 60、#Keywords 8、#Joins/Traversals 1、Nesting Depth 5；#Tokens 49、#Keywords 8、#Joins/Traversals 4、Nesting Depth 1。这些数值与具体查询语言的对应关系因版面交错无法确定。

Text-to-Query 系统在方法数量与新的高分上近期都有增长，主要得益于 Transformer 架构以及大语言模型（Large Language Models, LLMs）的进展 [17]。其想法很有吸引力：用户不必编写数据库查询，而是用自然语言表达意图，一个能够访问底层数据库的 Text-to-Query 系统把它们翻译成有效的查询语句（例如 SQL 或 SPARQL）。这在数字健康场景中尤其相关：领域专家（例如护士、医生或行政人员）不能被期望去编写复杂查询，目前依赖预定义的规则转换系统，而这限制了可以提出的问题 [22]。

现有 Text-to-Query 数据集与基准通常聚焦单一数据库模型与查询语言。例如 Spider [42]、WikiSQL [44]、BIRD [23]、ScienceBenchmark [43]、Statbot.swiss [29] 与 EHRSQL [22]（Text-to-SQL），以及 LC-Quad 2 [9] 与 Spider4SPARQL [20]（面向 Text-to-SPARQL，也称为知识图谱问答（Knowledge Graph Question Answering, KGQA））。直到最近，FootballDB [12] 才开始尝试在单一数据库系统内部（同一数据的不同模式）评测数据模型的影响。此外，已有初步工作跨越两种数据库模型与查询语言。例如，基于 MIMICSQL 数据集 [40] 对 SQL 与 SPARQL 的一项近期比较，发现了 34 个百分点的准确率差异 [31]。

然而，医学领域内外都还没有现有工作能够跨多种核心数据库模型与查询语言评测 Text-to-Query。这正是我们的数据集与基准的目标。本文提出 SM3-Text-to-Query，首个基于合成患者数据的多模型医学 Text-to-Query 基准（Multi-Model Medical Text-to-Query Benchmark）。SM3-Text-to-Query 提供以下关键特性：

- 基于标准且保护隐私。SM3-Text-to-Query 由 Synthea [39]（一种合成患者数据模拟器）精心构建。因此，所发布的数据集不涉及隐私问题。在数据模式中，我们遵循 SNOMED-CT 分类体系 [35]。这是一种常用的医学知识图谱本体，在机构与国家之间被广泛采用，使健康数据能够互操作。这保证了该基准对真实健康用例具有广泛影响。
- 三种数据库模型——四种数据库系统与查询语言。在数据库专家参与下，我们在 PostgreSQL、MongoDB、Neo4j 与 RDF（GraphDB）中设计四种数据表示（模式），并创建从 Synthea 输出到这些表示的转换。这些数据库代表三种核心数据库模型：关系、文档与图模型。内容相同的数据库可以通过四种不同查询语言访问：SQL、MQL、Cypher 与 SPARQL。据我们所知，SM3-Text-to-Query 是具备这些特性的首个基准。我们所选的数据库系统与查询语言，广泛代表了 DB-Engines Ranking [36] 中最流行的系统。
- 系统化且可扩展的问题生成。我们系统且人工地创建一组 408 道模板问题，覆盖 Synthea 数据的主要实体与属性。这些模板问题随后被自动增强与充实，从而为每种查询语言得到 10K 对自然语言/查询对。充实通过可参数化的抽样方法完成，例如从底层数据库检索患者姓名或过敏信息。我们的方法易于扩展：可以加入新模板（例如不同语言、不同问题、释义），或接入按 SNOMED-CT 建模的真实患者数据库。这保证基准面向未来，并能调整到其他使用场景。

## 2 Related Work 相关工作

本节回顾 Text-to-Query 系统的相关工作，重点是 (i) 医学数据与 (ii) 一般相关基准。

医学方向。MIMICSQL [40] 派生自 MIMIC-III 数据库 [15]，包含 10K 道面向医学质量保证任务的独特问题。为避免固定问题结构等潜在局限，MIMICSQL 经过了由专家自由职业者执行的过滤与释义过程。MIMIC-SPARQL [31] 建立在 MIMICSQL [40] 的框架上，并改写其问题模板，以便用 SPARQL 查询修改后的模式。它与 MIMICSQL 结构相似，提供 10K 道面向医学问答（QA）任务的独特问题。最后，EHRSQL [22] 提供一个聚焦电子健康记录（EHR）的 text-to-SQL 任务基准。它基于 MIMIC-III 与 eICU 数据库，而 230 道问题模板来自用户调查。基于这 230 个模板，EHRSQL 为 SQL 生成 24K 对问题/查询对。

一般基准。WikiSQL [44] 数据集是一个著名的通用 Text-to-SQL 基准，包含超过 80K 对文本/SQL 对。该数据集的特点是查询广泛分布在 24,241 张表上。Spider [42] 是最流行的跨领域 text-to-SQL 数据集之一，包含 10,181 道问题与 5,693 条独特 SQL 查询，覆盖 200 个数据库。KaggleDBQA [21] 建立在 Spider 与 WikiSQL 等大规模数据集之上，提供带有领域特定数据类型的跨领域数据集。BIRD [23] 是一个全面的问答（question answering, QA）资源，包含来自 Kaggle、CTU Prague 与 Open Tables 等多种来源的 12,751 道独特问题，覆盖 37 个主题领域。BIRD 面向真实应用，纳入来自 95 个大型数据库的复杂例子，总计 33.4 GB。ScienceBenchmark [43] 给出三个真实世界、领域特定的 text-to-SQL 数据集。与其他数据集相比，它反映出领域特定基准数据集对真实 text-to-SQL 任务的高度重要性。最后，FootballDB [12] 在单一数据库内部研究不同数据库模式及其对 Text-to-SQL 系统的影响。问题来自与终端用户的真实部署。

与这些工作相比，SM3-Text-to-Query 的主要新意在于：据我们所知，它是首个能够在三种核心数据库模型（关系、图、文档）与四种查询语言（SQL、SPARQL、Cypher、MQL）上评测 Text-to-Query 系统的数据集与基准。FootballDB [12] 在分析单一数据库内部 Text-to-SQL 系统的模式依赖性方面具有可比性。然而，它只针对 SQL、单一数据库模型（关系模型）以及查询语言 SQL。对于我们基于模板的方法，我们从 EHRSQL [22] 获得启发，并用遵循广泛使用的医学标准（SNOMED [35]）的合成数据生成来加以补充。这使我们的基准与世界各地遵循 SNOMED 医学命名分类体系的数字健康场景相关。
