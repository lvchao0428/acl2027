> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名：** QueryCarefully_arXiv2512.21345.pdf

**原文标题：** Query Carefully: Detecting the Unanswerables in Text-to-SQL Tasks

**作者：** Jasmin Saxer、Andreas Weiler、Kurt Stockinger（Institute of Computer Science, Zurich University of Applied Sciences，Winterthur）；Isabella Maria Aigner（Institute of Medical Virology, University of Zurich）；Luise Linzmeier（Department of Gastroenterology and Hepatology, University Hospital Zurich / University of Zurich）。

**arXiv：** arXiv:2512.21345v1 [cs.DB]，2025 年 12 月 19 日。DOI：https://doi.org/10.48550/arXiv.2512.21345 。

## 摘要 Abstract

Text-to-SQL 让不懂 SQL 的人用自然语言查关系数据库，但系统会给含糊、超出范围或根本无法回答的问题也生成可执行 SQL，输出容易被当成正确答案。生物医学场景里这种风险尤其大。本文提出 Query Carefully：把基于大语言模型的 SQL 生成和不可回答输入的显式检测、处理放在一条管道里。数据在 ScienceBenchmark 的 OncoMX 部分上扩展出 OncoMX-NAQ（No-Answer Questions），共 80 道无答案问题，覆盖 8 类，包括非 SQL、schema 或领域之外，以及多种歧义。模型用 llama3.3:70b，提示里带 schema、显式的 No-Answer Rules（NAR），以及同时来自可回答题和不可回答题的少样本例子。评测看 SQL exact match、结果准确率和不可回答检测准确率。界面会展示中间 SQL、执行结果和弃答。

摘要所报的后文主结果是一句：在 OncoMX 开发集上，用来自可回答题的少样本能提高结果准确率，再加入不可回答例子也不会把成绩拉低；在 OncoMX-NAQ 上，平衡提示的不可回答检测准确率最高，为 0.8，其中 non-SQL、missing columns、out-of-domain 这些结构清楚的类别接近完美，missing-value 查询为 0.5，column ambiguity 为 0.3。摘要未标表号。关键词为 text-to-SQL、Unanswerable Question Detection、OncoMX。

## 1 Introduction

关系数据库是管理结构化数据的基本工具，医疗和科研也靠它，但使用者通常得写 SQL，库里的知识因此主要留给数据库专家。Text-to-SQL 把自然语言问题译成可执行 SQL，让人用日常语言查库 [5]。深度学习和大语言模型已经把 Spider 这类配有问题–SQL 标注的简单基准上的成绩明显拉高 [6, 9]。

在医疗这类出错可能影响患者的领域，任务仍然难。作者列出三件事：为大型领域库里的复杂问题生成语义正确的查询；避免输出误导或错误的 SQL；处理含糊、不完整或无法回答的用户问题。本文聚焦第三件。真实用户通常不是数据库专家，问题可能有歧义、指向不存在的 schema 元素，或落在库的领域之外。基于大语言模型的系统仍可能硬生成 SQL，得到错误或误导性的结果。因此系统应能认出无法回答的问题，并给出“不可回答”或请求澄清。这样做既能挡住错误结果，也能暴露系统边界，提高真实应用里的稳健性 [1, 8, 11, 12]。

具体做法是扩展已有的 ScienceBenchmark [10]：围绕含癌症生物标志物信息的生物医学库 OncoMX 增加不可回答问题，再提出一条管道，把 SQL 生成和不可回答输入的检测、处理接到一个对话式界面上。

## 2 Related Work

本工作以 ScienceBenchmark 为底。该数据集为三个复杂的领域库提供了问题–SQL 标注：科研政策（CORDIS）、天体物理（SDSS）和癌症研究（OncoMX）[10]。作者选用 OncoMX，是因为其生物医学信息和术语领域性很强；库的公开站点为 https://www.oncomx.org/ 。ScienceBenchmark 所用版本有 25 张表，每表 2 到 14 列，共 106 列，每表平均 2,636,771 行。该库由美国 National Institutes of Health (NIH) 资助，汇集癌症生物标志物、癌症样本中的差异基因表达，以及来自多个来源的已知癌症突变，适合和 ScienceBenchmark 的问题–SQL 对一起做真实生物医学 text-to-SQL 测试。

多数 text-to-SQL 研究默认用户问题在给定 schema 内有效且可回答，专门检测不可回答或含糊问题的工作很少。Zhang 等人的 TriageSQL [11] 把用户问题分成五种意图，其中四类不可回答，例如 ambiguous、improper、需要外部知识，以及 non-SQL；他们用问题和 schema 训练 RoBERTa 分类器，主张在生成 SQL 之前先做意图分类。Wang 等人 [8] 观察一个商用 text-to-SQL 产品的真实使用，发现用户提交的问题里有 20% 有问题，说明只含可回答题的精选数据集会漏掉这一块。他们收集了 3,000 条以上失败查询，手工分成六类不可回答问题；其中歧义、超出范围和 schema 不匹配构成了本文分类框架的基础，细节留在方法部分。他们认为这类问题频繁，来自三件事：用户不熟悉 schema、自然语言本身含糊且说法多变、库里存在语义相近的概念。Wang 等人进一步只盯 column ambiguity 和 column unanswerable 两类，提出用修改已有表来制造不可回答问题，而不是新写问题；这样更可控，也更不真实。

生物医学方面，EHRSQL 2024 Shared Task 面向电子病历上可靠的 text-to-SQL，有意放入不可回答问题 [3]。系统既要为可回答输入写出正确 SQL，也要在很可能无法回答时弃答。评测奖励对不可回答题不产出 SQL，并同时惩罚错误 SQL 和在不该回答时仍然作答。本文把这一思路用到 OncoMX，并给不可回答问题分类，以便按不可回答的类型分析系统表现，目标是提高医疗和生物医学研究这类敏感领域里 text-to-SQL 的可靠性与安全性。
