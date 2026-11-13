> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文标题：** STARK: Benchmarking LLM Retrieval on Textual and Relational Knowledge Bases

**作者：** Shirley Wu、Shiyu Zhao、Michihiro Yasunaga、Kexin Huang、Kaidi Cao、Qian Huang、James Zou、Jure Leskovec（Stanford），Vassilis N. Ioannidis、Karthik Subbian（Amazon）。Wu 与 Zhao 为同等贡献，Zou 与 Leskovec 为同等资深作者。

**场合：** NeurIPS 2024 Datasets and Benchmarks。arXiv:2404.13207v3，2024-10-20。

**PDF：** `stark-2404.13207.pdf`

## Abstract

摘要认为真实的复杂查询，例如复杂商品搜索，要从半结构化知识库里检索：库里既有自由文本，也有实体关系。已有工作把文本检索和关系检索分开做。STARK 因此做了一个大规模的半结构化检索基准，覆盖商品搜索、学术论文搜索和精准医学三类查询。构造是一条新流水线：合成同时包含多样关系信息和复杂文本属性的用户查询，并带上标准答案；再用人工评估检查合成查询的质量；另外收集一批人工查询当参照。摘要的实验判断是：现有检索系统和 LLM 在 STARK 上仍然困难，需要更能同时处理文本和关系的检索系统。

## 1 Introduction

第 1 节用商品和论文的例子把「半结构化」说具体。顾客会同时提到品牌或另一件商品，以及耐用、适配这种只能在描述或评论里判断的性质。学术查询会同时要机构、作者和主题。纯文本检索看不到图上的关系；纯 SQL 或图谱查询盖不住自由文本。作者把这个缺口写成基准，而不是一个新检索器。

三个知识库在这一节点名：Amazon 的商品、品牌、颜色、品类及购买和浏览关系；MAG 的论文、作者、机构和领域；Prime 的生物医学实体。查询分两套：大批合成查询，小批人工查询。节末预告实验会暴露检索器在文本与关系同时出现时的失败，以及百万级实体上的延迟。表 1 的例子已经显示出答案是节点，而且一条查询可以对应多件商品。具体规模和四步构造留在第 2 节。

## 2 Benchmarking Retrieval Tasks over Textual and Relational Knowledge

第 2 节先定义任务，再给库的规模，并把 Amazon 称为产品推荐。

**2.1 Problem Definition。** 半结构化知识库是一张图加每个节点上的文档。给定查询，输出一个节点集合。每个答案节点既要满足查询在图上的关系要求，也要让节点文档满足查询的文本要求。这是在整张图上检索，不是在事先给定的短名单里重排。电商例子里，关系是商品与品牌、颜色、品类，文档是描述和评论。

**2.2 Semi-structured Knowledge Bases。** 表 2 给出三库的实体数、关系数和 token 数。Amazon 一行是 4 类实体、5 类关系、平均度 18.2、1,035,542 个实体、9,443,802 条关系、592,067,882 个 token。正文说明五类关系是商品之间的 also_bought、also_viewed，以及 has_brand、has_color、has_category。商品文本来自评论和问答；品牌、颜色、品类的文本是名字。

**2.3 Retrieval Tasks。** Amazon 任务被叫做 product recommendation。正文写 68% 的合成查询有多于一个标准答案。表 3 的计数是另一套：合成 Amazon 9,100 条，其中 7,082 条多答案，平均答案数 17.99，划分 0.65 / 0.17 / 0.18。文本侧重质量、功能和款式，关系是单跳，问句是对话体。MAG 有单跳和多跳模板，Prime 有更多多跳模板。第 2 节后半的合成四步和检索实验表不在这一节的开头部分展开；任务定义本身已经说明：标签必须同时满足关系和文本，不能把多答案理解成用户的下一次购买。
