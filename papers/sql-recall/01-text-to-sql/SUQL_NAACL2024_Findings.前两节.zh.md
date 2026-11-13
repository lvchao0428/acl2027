> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

- 原文件名：SUQL_NAACL2024_Findings.pdf
- 原文标题：SUQL: Conversational Search over Structured and Unstructured Data with Large Language Models
- 作者：Shicheng Liu, Jialiang Xu, Wesley Tjangnaka, Sina J. Semnani, Chen Jie Yu, Monica S. Lam（Stanford University, Computer Science Department）
- 场合：Findings of the Association for Computational Linguistics: NAACL 2024，页 4535–4555，2024 年 6 月 16–21 日

## 摘要

对话代理通常只接地于自由文本，或只接地于结构化知识，而病历、金融库、点评网站这类语料往往两者并存。本文提出 SUQL（Structured and Unstructured Query Language）：在 SQL 上增加自由文本原语 SUMMARY 与 ANSWER，使检索可以和结构化访问以形式化、简短、精确、可解释的方式任意组合。作者据此给出一个基于 LLM in-context learning 的语义解析器，并称这是第一个能处理混合数据源的语义解析器。

在 HybridQA 上，该少样本系统与在 62K 样本上训练的当时最优结果相差 8.9 个 Exact Match 百分点和 7.1 个 F1 百分点；与先前方法不同，它面向大型数据库和自由文本语料。作者另在 Yelp 餐厅知识库上收集众包问题与对话。基于 SUQL 的少样本对话代理在 90.3% 的情况下找到满足全部用户要求的实体，基于线性化的基线为 63.4%。

## 1 Introduction

大型语言模型的事实性工作，分别把回答锚定到外部结构化数据或自由文本。同一张表里却常常两种字段都有。文中的餐厅例子里，名称、菜系、评分是结构化列，热门菜和顾客评论是自由文本。问“找一家有浪漫氛围的意大利餐厅”，就要同时用 cuisines 和 reviews。

已有系统大致走两条路。一条用分类器把问题分给结构化模块、非结构化模块或闲聊（Jin et al., 2021; Chi et al., 2022; Zhao et al., 2023），跨两类字段的问题接不住。另一条把结构化记录线性化成自由文本再做向量检索（Figure 1 上半），SQL 的过滤与计算用不上，自由文本检索器也不擅长复杂条件。HybridQA（Chen et al., 2020）把这种混合需求做成评测；此前混合问答（Lei et al., 2023; Wu et al., 2023; Kumar et al., 2023; Lee et al., 2023a）要么只覆盖小数据，要么放弃结构化查询的表达力，要么只支持有限组合。

Figure 1 下半是本文路线：少样本 LLM 把用户话语解析成完整 SUQL，由 SUQL 编译器执行，结果再交给 LLM 生成回复。示例在 restaurants 上用 `'italian' = ANY(cuisines)` 过滤菜系，并用 `answer(reviews, 'is this restaurant romantic?') = 'Yes'` 判断评论，同时取出 `summary(reviews)`。作者把 SUQL 定位为精确、简短、可组合、可执行的形式语言：非结构化一侧用现成检索模型和 LLM，结构化一侧沿用 SQL 的语义与算子。众包结果显示，超过 49% 的问题同时需要两类知识。HybridQA 上，少样本系统与在超过 62K 样本上训练的最优模型相差 8.9% Exact Match、7.1% F1。在大型真实语料 Yelp 上，SUQL 代理找到完全满足条件实体的比例为 90.3%，线性化基线为 63.4%。

## 2 Related Work

Text-to-SQL 语义解析覆盖单轮问答（Guo and Gao, 2020; Wang et al., 2020a; Scholak et al., 2021; Zhong et al., 2017）和多轮对话（Yu et al., 2019a,b; Wang et al., 2020b; Liu et al., 2022）。LLM 经由 in-context learning（Brown et al., 2020）及多种提示策略（Hu et al., 2022; Poesia et al., 2022; An et al., 2023; Nan et al., 2023; Arora et al., 2023; Guo et al., 2023; Sun et al., 2023; Zhang et al., 2023b）在纯结构化库上已有结果。这条线到不了自由文本：SQL 对字符串只有基本模式匹配。

另一类对话界面用分类器把每一轮交给专用模块。Chirpy（Chi et al., 2022）按问题类型分模块；Jin et al. (2021) 与 Zhao et al. (2023) 用 Turn Detection 判断该走非结构化访问还是 API 或数据库。真实问题经常同时跨结构化列和自由文本列，分开的模块答不了。

第三类把表按行线性化，送进 Tabular Language Model（Herzig et al., 2020; Yin et al., 2020; Eisenschlos et al., 2021; Deng et al., 2022; Iida et al., 2021; Sun et al., 2022）。Oguz et al. (2022) 把 Wikidata、Wikipedia 表格与 Wikipedia 正文一起线性化，再用检索模型做开放域问答。作者认为这条路本身有限：需要跨库比较和计算的问题，例如统计纽约 2020 年 8 月与 9 月的 Covid 死亡人数，用结构化查询更直接；线性化也让数据库不同部分更难放在同一次查询里。
