> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名：** H-STAR_NAACL2025.pdf

**原文标题：** H-STAR: LLM-driven Hybrid SQL-Text Adaptive Reasoning on Tables

**作者：** Nikhil Abhyankar（Virginia Tech）、Vivek Gupta（Arizona State University）、Dan Roth（University of Pennsylvania）、Chandan K. Reddy（Virginia Tech）。

**场合：** NAACL 2025，*Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)*，第 8841–8863 页，2025 年 4 月 29 日–5 月 4 日。

## 摘要 Abstract

表格推理要同时做语言理解和结构化数据分析。已有路线分成两支：文本推理语义强，但数学运算弱；符号推理擅长计算，但缺少语义理解。H-STAR 把符号推理和语义（文本）推理放进一个两阶段流程。第一阶段按步骤抽表：先用 multi-view 检索列，再抽行。第二阶段按问题类型切换策略：直接查找和复杂词汇类问题走语义推理；数量和逻辑类问题则在文本推理之外加上符号推理。

摘要所报的后文主结果是：在三个表格问答和事实核查数据集上，H-STAR 明显超过当时的最优方法。摘要未给表号。代码见 https://github.com/nikhilsab/H-STAR 。

## 1 Introduction

表格是现实应用里最常见的结构化存储形式之一。表格推理要在非结构化问题和结构化表上同时做逻辑、数学和文本推理（Ye et al., 2023）。Figure 1 用同一张 NY Americans 赛季表把任务分成三类，并在每题旁标出作答所需的列和行：事实核查要判陈述真伪，示例陈述为 “NY Americans did not qualify for playoffs in 1936/37”，答案标为 False；短答案问答要给出一个值，示例问 1936 年之后何时赢得奖杯，答案为 1953/54；长答案问答要写成一句概括，示例称该队在 1936/37 和 1953/54 赢得 national cup。相关任务包括基于表的问答（Pasupat and Liang, 2015; Nan et al., 2022）和基于表的事实核查（Chen et al., 2019）。

大语言模型靠提示提升了多种任务，表格领域也试过符号路线 Program of Thought（Chen et al., 2023）和文本路线 Chain of Thought（Wei et al., 2022; Brown et al., 2020）。单独用时都会被数值、时间和文本混在一起、表结构又复杂的情况卡住（Shi et al., 2023; Liu et al., 2023; Sui et al., 2024）。文本推理理解自然语言好，却容易读错表结构，数量推理也弱；基于 SQL 的方法数量题强，但对噪声或非结构化输入表现差（Liu et al., 2023）。只走文本或只走符号的近期方法（Cheng et al., 2022; Ye et al., 2023; Wang et al., 2023; Nahid and Rafiei, 2024）带着同样的限制。Figure 2 用这张赛季表说明：符号推理会把是否类问题答成一个单元格的值；文本推理则会把一道数学题算错。

本文要回答的问题是：怎样把符号方法和文本方法合成一种混合表格推理，用上双方的长处、压低各自的短处。H-STAR 把任务拆成 Table Extraction 和 Adaptive Reasoning。抽表时走一条逐步的 multi-view 链：先用原表和转置表一起找相关列，再在滤过的表上抽行。Ye et al. (2023) 和 Nahid and Rafiei (2024) 则在原表上同时选行和选列。只把相关单元格交给模型，是为了给对上下文、减少推理时的幻觉；抽表阶段同时使用 SQL 和文本。自适应推理用少样本例子让模型判断何时用 SQL 给语义方法补一刀：语义推理始终使用，直接查找、常识和复杂词汇问题只用语义；数量、数学和逻辑问题再加一步 SQL。作者称该组合在三个表格问答与事实核查基准上超过此前全部最优方法，并且跨语言模型仍然稳。贡献有三：提出把抽表和自适应推理合在一起的混合方法；实验上混合路线超过只用符号或只用语义的最优方法，大表上尤其明显；消融表明抽表和推理两个阶段都起作用。另一处代码与资源页为 https://hstar-llm.github.io/ 。

## 2 H-STAR Approach

H-STAR 把表格推理拆成抽取和推理，把语言模型的文本理解与符号推理合在一起：把原表 T 收成与当前问题对应的表 TCR，流程见 Algorithm 1 和 Figure 3。DATER（Ye et al., 2023）靠文本推理抽表，TabQSLify（Nahid and Rafiei, 2024）靠 text-to-SQL；H-STAR 在抽表时让两种推理互补，推理阶段则只在数量问题上动态加上符号步骤。两个主阶段是 Table Extraction 和 Adaptive Reasoning。提示、输入表格式和超参数放在 Appendix C 与 D。

抽表按列、行两步走。Algorithm 1 的 Stage A：列抽取采用 multi-view，先在原表 T 上用 colsql 生成 SQL 得到列集合 C1，再在转置表 TT 上用 coltext 得到 C2，换视角是为了补上表结构导致漏掉的信息（附录 A.3 有进一步结果）。Figure 3 的例子是 “How long did it take the New York Americans to win the National Cup after 1936?”。colsql 抽出列 year；coltext 返回 year 和 national cup，补上 SQL 漏掉的 national cup。C′ 为两者并集，TC 是只留这些列之后的表，图中还会加上 row_id。TC 比 T 短，更容易落在长度限制内。行抽取在 TC 上做：rowsql 得到 R1，示例为 row 18，够相关但还答不了题；rowtext 再核对，补出 row 1 和 row 18。R′ 为并集，TCR 是按这些行滤出的最终表。

自适应推理先让模型凭语言理解判断问题要不要定量计算。Algorithm 1 的 Stage B：若 math(Q) 为真，用 fsql 在 TCR 上生成并执行 SQL，得到证据 Ev，再连同 TCR 交给 ftext 得到答案 Â；否则只用 TCR 做 ftext。仍用上面那道“多久”的题：管道优先走 fsql，SQL 在引擎上对 TCR 计算，Ev 作为额外证据进入最后的文本推理。Figure 3 把该题标成需要计算，SQL 证据为 years_after_1936，图中答案为 17。这一步是为了补上语言模型不擅长数量推理的短板。
