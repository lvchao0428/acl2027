> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

首页标题与 `01-text-to-sql/SUQL_NAACL2024_Findings.pdf` 相同。以下只依据本目录的 SUQL_NAACL2024.pdf。

- 原文件名：SUQL_NAACL2024.pdf
- 原文标题：SUQL: Conversational Search over Structured and Unstructured Data with Large Language Models
- 作者：Shicheng Liu、Jialiang Xu、Wesley Tjangnaka、Sina J. Semnani、Chen Jie Yu、Monica S. Lam（Computer Science Department, Stanford University）
- 场合：Findings of the Association for Computational Linguistics: NAACL 2024，页 4535–4555，2024 年 6 月 16–21 日

## 摘要

对话代理的外部知识通常只接自由文本，或只接结构化记录。作者认为病历、金融库和点评网站往往是混合语料，因此提出 SUQL（Structured and Unstructured Query Language），并据此做第一个能在大型混合语料上做完整混合访问的对话代理。SUQL 在 SQL 上增加自由文本原语 SUMMARY 和 ANSWER，使检索能以形式化、简短、精确、可解释的写法任意嵌进结构化访问。配套语义解析器是做 in-context learning 的 LLM，作者称它是第一个能处理混合数据源的语义解析器。

在 HybridQA 上，这套少样本方法与在 62K 样本上训练的 SOTA 相差不超过 8.9% Exact Match 和 7.1% F1；和先前方法不同，它面向大型数据库和自由文本语料。作者另外在 Yelp 这家真实大型餐厅知识库上收集众包问题与对话。基于 SUQL 的少样本代理在 90.3% 的情况下找到满足用户全部要求的实体，线性化基线为 63.4%。代码与数据见 https://github.com/stanford-oval/suql 。

## 1 Introduction

第 1 节先把缺口放在同一张表里。已有事实性工作分别把 LLM 接到结构化数据（Hu et al., 2022; An et al., 2023; Nan et al., 2023; Poesia et al., 2022; Arora et al., 2023; Xu et al., 2020, 2023）或自由文本（Khattab et al., 2023; Jiang et al., 2023; Semnani et al., 2023; Gao et al., 2023）。附录 Figure 2 的餐馆例子里，名称、菜系、评分是结构化列，热门菜和顾客评论是自由文本。问 “Can you find me an Italian restaurant with a romantic atmosphere?” 时，必须同时用 cuisines 和 reviews。

两条现成路线都接不住这种组合。分类器把话语分给结构化模块、非结构化模块或闲聊（Jin et al., 2021; Chi et al., 2022; Zhao et al., 2023），跨两类字段的问题没有去处。把结构化记录线性化成自由文本再做向量检索（Oguz et al., 2022）则放弃 SQL。Figure 1 上半画出这条路：库中条目变成向量，用户请求也变成向量，取最近邻后再交给 LLM；图中的失败例子是菜系不对，评论里也没有浪漫氛围。HybridQA（Chen et al., 2020）专门收集答案同时依赖两类信息的自然语言问题。此前混合问答（Lei et al., 2023; Wu et al., 2023; Kumar et al., 2023; Lee et al., 2023a）要么数据小，要么放弃结构化查询的表达力，要么只能做有限组合。

本文要让对话代理同时用上结构化查询和自由文本检索。SUQL 被定义成精确、简短、可组合、可执行的形式语言：非结构化一侧用现成检索模型和 LLM，结构化一侧保留 SQL 的语义与算子。Figure 1 下半是系统：少样本 LLM 根据 schema 和示例把话语解析成 SUQL，编译器执行后把结果交回 LLM。图中查询对 restaurants 使用 `'italian' = ANY(cuisines)`、`answer(reviews, 'is this restaurant romantic?') = 'Yes'` 和 `summary(reviews)`，并 `LIMIT 1`。经验主张有三处数字：众包餐馆问题里，超过 49% 同时需要两类知识；HybridQA 上，少样本系统与在超过 62K 样本上训练的 SOTA 相差不超过 8.9% Exact Match 和 7.1% F1；在大型真实语料 Yelp 上新建的单轮问题集和对话集中，SUQL 代理满足全部用户条件的比例是 90.3%，线性化基线是 63.4%。

## 2 Related Work

第 2 节用三条既有路线说明，它们都到不了“结构化列和自由文本列放进同一次查询”。

Text-to-SQL 覆盖单轮问答（Guo and Gao, 2020; Wang et al., 2020a; Scholak et al., 2021; Zhong et al., 2017）和多轮对话（Yu et al., 2019a,b; Wang et al., 2020b; Liu et al., 2022）。LLM 经由 in-context learning（Brown et al., 2020）及多种提示策略（Hu et al., 2022; Poesia et al., 2022; An et al., 2023; Nan et al., 2023; Arora et al., 2023; Guo et al., 2023; Sun et al., 2023; Zhang et al., 2023b）在纯结构化库上已有结果。这条线没有自由文本：SQL 对字符串只做基本模式匹配，需要更深的文本理解时用不上。

另一类对话界面用分类器把每一轮交给专用模块。Chirpy（Chi et al., 2022）按问题类型分模块；Jin et al. (2021) 与 Zhao et al. (2023) 用 Turn Detection 判断该走非结构化访问，还是交给 API 或数据库。真实问题经常同时跨结构化列和自由文本列，分开的模块答不了。

第三类把表按行线性化，送进 Tabular Language Model（Herzig et al., 2020; Yin et al., 2020; Eisenschlos et al., 2021; Deng et al., 2022; Iida et al., 2021; Sun et al., 2022）。Oguz et al. (2022) 把 Wikidata、Wikipedia 表格与 Wikipedia 正文一起线性化，再用检索模型做开放域问答。作者认为这条路本身有限：统计纽约 2020 年 8 月与 9 月的 Covid 死亡人数，用结构化查询做比较和计算更直接；线性化也让数据库的不同部分更难放进同一次查询。
