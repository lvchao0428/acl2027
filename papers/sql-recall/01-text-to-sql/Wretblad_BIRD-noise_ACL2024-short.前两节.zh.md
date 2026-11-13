> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

- 原文件名：Wretblad_BIRD-noise_ACL2024-short.pdf
- 原文标题：Understanding the Effects of Noise in Text-to-SQL: An Examination of the BIRD-Bench Benchmark
- 作者：Niklas Wretblad、Fredrik Gordh Riseby（同等贡献）、Oskar Holmström（Linköping University）；Rahul Biswas、Amin Ahmadi（Silo AI）
- 场合：Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers)，页 356–369，2024 年 8 月 11–16 日。数据、标注与代码：https://github.com/niklaswretblad/the-effects-of-noise-in-text-to-SQL

## 摘要

Text-to-SQL 把自然语言译成 SQL，让不懂数据库的人也能访问结构化数据。建模很难，原因之一是噪声，例如含糊的问题和语法错误。本文细看广泛使用的 BIRD-Bench 里噪声的分布与类型，以及噪声对模型的影响。BIRD-Bench 的设计目标是脏的、有噪声的数据库取值，并不是要在问题和金标 SQL 里放进噪声与错误。作者发现问题和金标查询里的噪声很普遍，各领域多少不一，噪声类型的分布也不均匀。错误的金标 SQL 会生成错误的金标答案，明显影响基准是否可靠。出乎意料的是，在改对的 SQL 上评测时，zero-shot 基线超过了当时领先的提示方法。结论是：要发展能应付不同噪声的 Text-to-SQL，需要有信息量的噪声标签，也需要可靠的基准。

## 1 Introduction

用大语言模型做 Text-to-SQL，可以不靠专家知识访问结构化数据库，因此高质量的开放数据和基准很重要。早期 WikiSQL 多是简单、常常只涉及单表的情形。随后的数据更接近真实使用：跨多表、带 JOIN 的复杂查询（Yu et al., 2018），未见过的领域数据（Gan et al., 2021b; Lee et al., 2021），以及带噪声的问题（Gan et al., 2021a）。较新的 BIRD-Bench 想进一步缩小研究和应用的差距，例如放入大而脏的数据库取值，并要求外部知识（Li et al., 2023）。

BIRD-Bench 没有故意往问题里加噪声，但人工建库时仍可能无意引进。真实使用里，人的输入也常常含糊并带语法错误。基准若要用来判断模型处理噪声的能力，数据本身必须有效，并能指出模型该改进的地方。本文延续对开放数据和基准适用性与局限的检查，专门看 BIRD 的问题和查询如何表现噪声。Figure 1 给了一个金标 SQL 写错、因而金标答案也错的例子。问题是男性借款人的平均贷款额。错误查询把 client 和 account 按 district_id 连接，再连到 loan，并用客户性别 `'M'` 过滤。同一地区可以有多个客户和账户，账户就会对到错误的人。改正后的查询从 loan 出发，经 account 和 disp 连到 client，再按客户性别过滤。

后文要做的是：定性分析数据里有哪些噪声、噪声在各领域如何分布，再用强基线和当时领先的方法看噪声对不同模型与提示技术的影响。引言先给出结论：问题和金标 SQL 里的噪声很常见，领域之间不均匀，噪声类别的数量也不相等；金标 SQL 的错误很常见，并降低 BIRD-Bench 的可靠性。把金标查询改正后再评，zero-shot 基线与领先提示技术之间的差距被抹平，因此在 BIRD-Bench 上读模型成绩需要重新考虑。Figure 2 画的是开发集各领域的问题难度构成（simple、moderate、challenging）以及 DIN-SQL 的执行准确率，横轴领域包括 california_schools、codebase_community、superhero、formula_1、european_football_2、thrombosis_prediction、student_club、financial、toxicology 和 card_games。各柱没有逐项标出数字，柱高无法从正文可靠读出。

## 2 Related Work

数据集方面，WikiSQL 规模大，但只有简单的 SELECT 和 WHERE，没有嵌套查询或 JOIN。SPIDER 更接近真实场景，要求模型写出复杂查询并理解数据库模式。后来的变体分别加入噪声问题（Gan et al., 2021a）和领域专用问题（Gan et al., 2021b）。BIRD-Bench 则用大而脏的数据库取值、需要外部知识的问题，以及 SQL 执行效率，来缩小学术研究与真实应用的差距（Li et al., 2023）。

方法方面，自动系统与人类专家的准确率仍有明显差距：截至 2024-02-16，BIRD-Bench 网站上分别是 65.45% 和 92.96%（https://bird-bench.github.io）。一条路线是在 Text-to-SQL 例子上微调大语言模型。这些模型有结果，但仍落后于用提示工程适配到该任务的指令微调模型，尤其是 GPT-4（Li et al., 2023）。提示常常串成链，每一步处理子问题，例如模式链接、查询分解和生成结果的修正（Pourreza and Rafiei, 2023a; Wang et al., 2023）。

噪声方面，同期的 Wang et al. (2023) 和 Sun et al. (2024) 已经指出 BIRD-Bench 里有含糊问题和错误 SQL，但没有研究噪声如何随领域变化，也没有研究这些噪声和错误如何影响模型表现。Pourreza and Rafiei (2023b) 对错误 SQL 做了更细的分析，并提到本文也覆盖的噪声类别，例如自然语言问题与数据库模式对不上。与他们相比，本文把自然语言问题里的噪声分得更细，例如语法错误、同义词和含糊问题。Katsogiannis-Meimarakis and Koutrika (2023) 则指出数据库模式经常与数据实体错位，从而造成词汇或句法歧义，影响 Text-to-SQL 模型。

下一页页首印有 Table 1 和 Table 2，统计的是后文标注出的噪声，不属于这两节的正文。
