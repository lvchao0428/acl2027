> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名：** `FINCH_arXiv2510.01887.pdf`

**原文标题：** FINCH: Financial Intelligence using Natural language for Contextualized SQL Handling

**作者：** Avinash Kumar Singh（Domyn，Hyderabad）、Bhaskarjit Sarmah（Domyn，Gurgaon）、Stefano Pasquali（Domyn，New York）。

**场合：** arXiv:2510.01887v1 [q-fin.CP]，2025 年 10 月 2 日。首页未印会议名称。关键词为 Text-to-SQL、Large Language Models in Finance、Financial benchmark dataset，以及面向 text-to-SQL 的金融评测指标。

## 摘要

Text-to-SQL 把自然语言问题翻成 SQL，金融域尤其难：schema 复杂、术语专、写错的代价高。作者认为这个方向还没有专用的大规模金融数据。FINCH 是他们整理的金融数据集，292 张表、75,725 条自然语言–SQL 对，既可以微调也可以评测。在这上面，他们比较不同规模的推理模型和语言模型，并分析优劣。最后提出面向金融的 FINCH Score，用来抓住现有指标忽略的细微差别。摘要没有给出模型分数，也没有指向表号。

## 1 Introduction

第 1 节把通用 text-to-SQL 的进展压成一条时间线，再论证它仍接不上金融部署。早期是规则语法和符号解析；Seq2SQL（2017）用强化学习生成可执行查询，超过模板系统；SQLNet 改成 sketch-based decoding，降低复杂度。Spider（2018）是第一个大规模跨领域数据，变成默认基准。CoSQL 和 SParC（2019）把任务扩到对话和依赖上下文。模型侧，RAT-SQL（2020）用 relation-aware transformer 做 schema linking，PICARD（2021）对大预训练模型做约束解码。BIRD（2023）被写成把评测扩到十亿级查询、用来测规模上的稳健性。作者接着指出，高分系统换到和训练语料不一样的 schema 上就会掉；Spider 和 BIRD 偏百科或开放域，不是行业库。RAT-SQL 和 DCG-SQL（2025）改善对齐，但仍怕噪声描述和很宽的列空间。NL2PY2SQL（2024）走 Python 再到 SQL 的中间表示，效率和可解释性在高风险领域仍存疑。评测则仍靠 exact match 和 execution accuracy，抓不住细小但有意义的结构差别。

金融侧被分成“可执行推理”和“已经碰 SQL 的工作”两段。FinQA（2021）对公司财报做数值推理，用运算程序作监督。TAT-QA（2021）把表和文本合在一起。ConvFinQA（2022）做成多轮，模拟分析师把问题越问越深。Nye et al. 用两个模块分工：一个从文件抽关键绩效指标，一个翻成 SQL。指标也从僵硬的完全匹配转向树编辑距离和结构感知相似度。真正做金融 text-to-SQL 的工作还少：FinSQL（2024）放出宽 schema 的 BULL，面向跨库泛化，领域微调相对通用基线最多约 36% 的相对提升，但 schema 一大就掉得很陡。BookSQL（2024）在会计域提供约 75k 条自然语言–SQL 对，用来暴露大预训练模型在细微商业语义和复杂连接上的不足。方法上，NL2PY2SQL 用自然语言–Python–SQL 两步来抓住领域逻辑，DCG-SQL 用深层上下文图加强宽表上的 schema linking。Reliable Text-to-SQL（RTS, 2025）加入自适应弃权和人在回路的修正，把可靠性写成银行、审计和投资场景的核心要求。收束句是：金融库的 schema 又宽又会变，约束严，还要合规，对错误更敏感；缺的是领域数据、针对金融 schema 的结构，以及超出完全匹配、能看语义忠实和操作安全的评测。此前金融问答多半还停在文档或表–文混合，而不是直接查金融 SQL 库。

贡献三条。数据：把 BIRD、Spider、FinSQL 和 BookSQL 收成一套，SQL 都规范成 SQLite。FINCH 覆盖 33 个库，领域包括 retail、banking transactions、loans、insurance、sales、marketing、finance、e-commerce、funds、stocks 和 accounting；共 292 张表、2,233 列、177 个关系、75,725 条 NL–SQL 对，被称作最大的面向金融的基准。模型：四类里实际点名的是大规模 Qwen3-235B-A22B，中小开源 GPT-OSS-120B、GPT-OSS-20B、Qwen3-8B，以及推理向的 Phi-4-mini-reasoning 和 Arctic-Text2SQL-R1-7B。第 1 节已经给出的主结果只有这一句，没有指向表号：GPT-OSS-120B 整体最强，超过更大的 Qwen3-235B-A22B；Arctic-Text2SQL-R1-7B 参数不大，但是第三名；推理向结构经过适配后，可以赶上甚至超过大得多的通用 LLM。指标：FINCH Score 把 component matching 和 execution accuracy 合在一起，加上加权和容差，减轻浮点小误差的过重惩罚，更看重列名、表引用和条件是否正确。具体公式在第 3 节，这里不展开。

## 2 FINCH Dataset Construction

第 2 节说明 FINCH 不是把四个公开资源原样叠起来，而是先筛掉和金融无关的库，再执行、改错。Spider 和 BIRD 原本覆盖体育、教育、娱乐、地理等，和金融系统关系不大；金融场景要处理的是银行记录、卡交易、零售与销售、贷款和保险。筛保留的领域是 retail sales、card transactions、banking services、loan processing、insurance 和 e-commerce。作者用表 1 说明：相对只拼规模的 BookSQL，或只拼跨领域泛化的 Spider、BIRD，FINCH 要同时保住规模、schema 多样性和金融相关性，并用 33 个金融库、更高的平均 table-to-database 比，来评 schema linking 和组合推理。表注把 #T/DB 称为 database-to-table ratio。#DB*、#Size* 是筛进 FINCH 的库数和样本数；FINCH 一行的 #Size、#DB 印为 “-”。

| 数据集 | #Size | #DB | #DB* | #Size* | #T/DB |
| --- | --- | --- | --- | --- | --- |
| Spider | 10,181 | 200 | 22 | 1,100 | 5.1 |
| BIRD | 12,751 | 95 | 7 | 812 | 7.3 |
| BULL | 4,966 | 3 | 3 | 4,966 | 26.0 |
| BookSQL | 78,433 | 1 | 1 | 68,907 | 7.0 |
| FINCH | - | - | 33 | 75,725 | 8.85 |

**2.1 Dataset Curation。** 从 Spider 选了 22 个有明确金融相关性的库，从 BIRD 留了 7 个。BULL 和 BookSQL 本身就是金融向的，只要自然语言问题和对应 SQL 都在，就全部保留。正文在讲清洗之前给出的条数是：BIRD 1,139，Spider 1,100，BULL 4,966，BookSQL 78,433。BookSQL 的测试划分没有对应 SQL，这一部分被排除。随后每条 SQL 都在对应的 SQLite 库上执行，失败情况是：BIRD 1,139 条里 327 条失败，其中列名错误 198、非法表引用 129；BULL 4,966 条里 60 条有问题，其中语法错误 43、错表 10、列错误 1、不完整查询 4、无法识别的 token 2；BookSQL 78,433 条里 9,526 条出错，其中列名错误 7,018、非法表引用 1,494、语法错误 1,014；Spider 子集没有检出异常。作者写的是反复执行、核对 schema、按问题意图改这些错误，而不是只做机械过滤。表 1 的 #Size* 与这些数字的关系是：BIRD 的 812 等于 1,139 减 327，BookSQL 的 68,907 等于 78,433 减 9,526；BULL 的 #Size* 仍印成 4,966，没有减去那 60。四行 #Size* 相加是 75,785，与 FINCH 的 75,725 相差 60。

最终版本写成 33 个库、292 张表、2,233 列、177 个关系，以及 over 75,725 条 NL–SQL 对；第 1 节和表 1 写的是 75,725，没有 “over”。难度分布是 easy 9,358、medium 33,780、hard 32,587，三者之和等于 75,725。另外 7,035 条原先没有难度标签，按 BookSQL 的 schema 复杂度指南补标。查询大量使用 ORDER BY、GROUP BY 和嵌套。图 1 是多来源库合成一个基准的总览，并标出 schema 多样性和领域覆盖；图中的具体库名抽取不全。第 2 节的收束是：FINCH 是第一个同时有多领域广度、schema 深度和非平凡 SQL 难度的大规模金融 text-to-SQL 数据。实验设置和 FINCH Score 的公式从第 3 节起，此处不展开。
