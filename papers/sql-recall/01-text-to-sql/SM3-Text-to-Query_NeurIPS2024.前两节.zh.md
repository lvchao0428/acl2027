> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名：** SM3-Text-to-Query_NeurIPS2024.pdf

**原文标题：** SM3-Text-to-Query: Synthetic Multi-Model Medical Text-to-Query Benchmark

**作者：** Sithursan Sivasubramaniam 与 Cedric Osei-Akoto（同等贡献）、Yi Zhang、Kurt Stockinger、Jonathan Fürst（通讯作者）。单位均为 Zurich University of Applied Sciences，瑞士。

**场合：** NeurIPS 2024，38th Conference on Neural Information Processing Systems，Track on Datasets and Benchmarks。

## 摘要 Abstract

电子病历会落在不同的数据库模型和异构存储上，例如关系数据库、文档库或图数据库。模型不同，查询的复杂度和性能就不同。数据库领域早就知道这一点，但越来越多的 Text-to-Query 系统还没有被从这个角度考察。本文提出 SM3-Text-to-Query，称其为第一个多模型的医学 Text-to-Query 基准：病人数据由 Synthea 合成，并遵循广泛使用的医学术语知识图谱本体 SNOMED-CT。同一批数据做成四种表示，对应 PostgreSQL、MongoDB、Neo4j 和 GraphDB（RDF），从而可以评 SQL、MQL、Cypher 和 SPARQL。作者手工系统地写了 408 个模板问题，再扩充成每种查询语言 10K 条自然语言问题/查询对，四种语言合计 40K 对。基准也可以再加查询语言，或换上符合标准的真实病人库。

摘要所报的后文主结果是一句：在该数据上比较若干常见的 in-context learning 做法和一组有代表性的闭源、开源大语言模型，用来看数据库模型、查询语言、提示策略和模型之间的取舍。摘要未标表号。

## 1 Introduction

医疗数字化之后，电子病历的存放方式并不统一。关系库如 PostgreSQL 或 Oracle 把数据放进表和行，用 SQL 访问；文档库如 MongoDB 把数据看成文档集合，用 MongoDB Query Language（MQL）；图数据库则要么是属性图（如 Neo4j，查询语言 Cypher），要么是 RDF 语义图（如 Ontotext GraphDB，查询语言 SPARQL）。关系模型和 SQL 仍是病历的主要选择，但文档模型和图模型因为 schema 灵活、便于把数据孤岛连起来而受到更多关注。欧洲的数字医院试点 AICCELERATE 就用图模型连接传统病历、其他医院数据、可穿戴设备和物联网设备。使用 SPARQL 的 RDF 图数据库在生命科学里已经很常见，医学也在跟上。底层模型会明显改变读写性能和查询复杂度：患者、医生、治疗和病情之间的多对多关系，图模型可以直接表示，关系库则可能要昂贵的连接和复杂查询；文档库对多对多只有初步支持，更适合互联不多、schema 灵活的文档集合。Figure 1 用同一句请求对照四种语言：“Provide me the names of patients that are linked with the organization Royal of Fairhaven Nursing Center.” 图中给出的复杂度是：SQL 为 25 个 token、8 个关键词、2 次连接/遍历、嵌套深度 0；Cypher 为 12、3、3、1；SPARQL 为 49、8、4、1；MongoDB 为 60、8、1、5。作者认为，这些差异在数据库研究和工业界是已知事实，但对 Text-to-Query 的影响还没有被研究。

Text-to-Query 近来方法变多、分数变高，主要靠 Transformer 和大语言模型：用户用自然语言表达意图，系统根据底层库把它译成合法查询，例如 SQL 或 SPARQL。这在数字医疗里尤其要紧，因为护士、医生或行政人员不能被指望去写复杂查询，目前多依赖预先写好的规则转换，能问的问题因此受限。已有数据和基准通常只覆盖一种数据库模型和一种查询语言。Text-to-SQL 一侧有 Spider、WikiSQL、BIRD、ScienceBenchmark、Statbot.swiss 和 EHRSQL；Text-to-SPARQL（也称 Knowledge Graph Question Answering）一侧有 LC-Quad 2 和 Spider4SPARQL。FootballDB 开始在同一个数据库系统内部、用不同 schema 看数据模型的影响。另有工作基于 MIMICSQL 比较 SQL 和 SPARQL，准确率相差 34 个点。医学领域内外都还没有一项工作能跨多种核心数据库模型和查询语言来评 Text-to-Query。SM3-Text-to-Query 就是为这个空档做的多模型医学基准，基于合成病人数据。

基准有三个设计要点。其一，遵循标准且保护隐私：数据来自合成病人模拟器 Synthea，发布的数据没有隐私问题；schema 遵循 SNOMED-CT，这是跨机构、跨国家常用的医学知识图谱本体，便于健康数据互操作。其二，三种数据库模型、四个系统和四种查询语言：在数据库专家参与下，为 PostgreSQL、MongoDB、Neo4j 和 RDF（GraphDB）设计表示，并从 Synthea 的输出做转换；内容相同，分别用 SQL、MQL、Cypher 和 SPARQL 访问。所选系统按 DB-Engines Ranking 覆盖常见系统。其三，问题生成系统化且可扩展：手工覆盖 Synthea 数据的主要实体和属性，写成 408 个模板，再用可调参数的抽样自动充实，例如从库里取患者姓名或过敏原，每种查询语言得到 10K 对自然语言/查询。以后可以加模板（不同语言、不同问题、改写），也可以接入按 SNOMED-CT 建模的真实病人库。

## 2 Related Work

医学方向的相关数据都围绕真实或准真实病历，但只服务一种查询语言。MIMICSQL 从 MIMIC-III 派生，有 10K 条不重复问题，面向医疗质量保证；为避免问题结构过于固定，专家自由职业者做了过滤和改写。MIMIC-SPARQL 沿用 MIMICSQL 的框架，把问题模板改到一个用 SPARQL 查询的修改版 schema 上，结构相近，同样是 10K 条面向医疗问答的不重复问题。EHRSQL 做的是电子病历上的 text-to-SQL，底库是 MIMIC-III 和 eICU；230 个问题模板来自用户调查，据此生成 24K 条 SQL 问题/查询对。

通用基准则用来说明现有资源要么跨领域、要么仍停在 SQL。WikiSQL 有超过 80K 条文本/SQL 对，查询分布在 24,241 张表上。Spider 是常用的跨领域 text-to-SQL 数据，含 10,181 个问题、5,693 条不重复 SQL，覆盖 200 个数据库。KaggleDBQA 在 Spider、WikiSQL 这类大规模数据上做跨领域集合，并带有领域特定的数据类型。BIRD 有 12,751 条不重复问题，来源包括 Kaggle、CTU Prague 和 Open Tables，覆盖 37 个主题；它面向真实应用，从 95 个大库中取复杂例子，总量 33.4 GB。ScienceBenchmark 给出三个真实、领域特定的 text-to-SQL 数据集，用来强调领域基准对真实任务的重要性。FootballDB 在单个数据库内部比较不同 schema 对 Text-to-SQL 的影响，问题来自有真实用户的部署。

相对这些工作，SM3-Text-to-Query 的新意是：据作者所知，它是第一个能跨三种核心数据库模型（关系、图、文档）和四种查询语言（SQL、SPARQL、Cypher、MQL）评测 Text-to-Query 的数据集和基准。FootballDB 同样关心 schema 依赖，但只在一个数据库内部、只针对 SQL。模板式构造受到 EHRSQL 启发，并用遵循 SNOMED 命名体系的合成数据补上，使基准能对应世界各地按这一医学命名法建库的数字健康场景。
