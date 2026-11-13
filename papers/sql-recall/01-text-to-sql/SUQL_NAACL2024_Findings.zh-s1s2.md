# SUQL: Conversational Search over Structured and Unstructured Data with Large Language Models

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`SUQL_NAACL2024_Findings.pdf`。

## Abstract 摘要

大多数对话代理要么基于自由文本，要么基于结构化知识，但许多知识语料由混合来源构成。本文提出首个对话代理，它通过我们开发的语言 SUQL（Structured and Unstructured Query Language，结构化与非结构化查询语言），为大型知识语料支持混合数据访问的完全一般性。具体而言，SUQL 用自由文本原语（SUMMARY 与 ANSWER）扩展 SQL，使信息检索能够以形式化、简洁、精确且可解释的记号，与结构化数据访问任意组合。借助 SUQL，我们提出首个能够处理混合数据源的语义解析器（semantic parser）：一个使用上下文学习（in-context learning）的大语言模型（large language model, LLM）。

我们基于上下文学习的方法应用于 HybridQA 数据集时，在精确匹配（Exact Match）上与当前最优（SOTA）相差 8.9%，在 F1 上相差 7.1%；该 SOTA 是在 62K 条数据样本上训练的。更重要的是，与先前方法不同，我们的技术适用于大型数据库与自由文本语料。

我们引入一个数据集，包含在 Yelp 上众包得到的问题与对话。Yelp 是一个大型、真实的餐馆知识库，同时含有结构化与非结构化数据。我们表明，基于 SUQL 的少样本对话代理在 90.3% 的情况下找到满足用户全部要求的实体，而基于线性化（linearization）的基线为 63.4%。代码与数据见 https://github.com/stanford-oval/suql。

## 1 Introduction 引言

大语言模型（Large Language Models, LLMs）在众多下游任务上表现出色。近期一系列工作通过把回答锚定在外部资源上来提高其事实性，这些资源包括结构化数据（Hu et al., 2022; An et al., 2023; Nan et al., 2023; Poesia et al., 2022; Arora et al., 2023; Xu et al., 2020, 2023）与自由文本（Khattab et al., 2023; Jiang et al., 2023; Semnani et al., 2023; Gao et al., 2023）。

然而，许多数据源同时包含结构化数据与自由文本：患者记录、金融数据库以及评论网站，仅举数例。附录中的图 2 展示了本文所用应用的运行示例。表中每一行代表一家独特的餐馆，其名称、菜系类型与评分等信息作为结构化数据。此外，每一行还以自由文本包含热门菜品与顾客评论。要回答诸如 “Can you find me an Italian restaurant with a romantic atmosphere?” 这样的问题，代理需要把结构化属性 cuisines 与自由文本属性 reviews 结合起来。

为处理结构化与非结构化数据的组合，许多先前的聊天系统使用分类器，把查询分配给专门处理结构化数据、非结构化数据或闲聊的模块之一（Jin et al., 2021; Chi et al., 2022; Zhao et al., 2023）。遗憾的是，这一做法不足以应对同时需要自由文本与结构化数据的问题。

另一种流行做法是把结构化数据转换或线性化为自由文本（Oguz et al., 2022），如图 1 所示。采用这一做法后，我们不再能运用 SQL 查询数据库的能力，而自由文本检索器也不擅长处理复杂问题。

组合混合数据源查询的需要，由 HybridQA 数据集所突出。该数据集收集了许多自然问题，其答案同时包含来自结构化数据与自由文本的信息（Chen et al., 2020）。先前试图把问答系统锚定在混合数据上的工作（Lei et al., 2023; Wu et al., 2023; Kumar et al., 2023; Lee et al., 2023a），或者只在小数据集上工作，或者放弃结构化数据查询的表达力，或者只支持结构化与非结构化知识查询的有限组合。

图 1：传统方法（线性化）与我们的方法（使用 SUQL 的语义解析）的比较。上：在线性化方法中，数据库条目被线性化并转换为嵌入向量。运行时，用户请求被转换为嵌入向量，用以从已存储向量中找到最接近的嵌入。结果随后被提供给 LLM 以生成回复。下：在我们的方法（使用 SUQL 的语义解析）中，用户话语由经过少样本提示的 LLM 解析为形式化 SUQL，再由 SUQL 编译器执行，从数据库取回结果。结果随后被提供给 LLM 以生成回复。图中示例单元格在 PDF 抽取中交错：可见餐馆名 Hummus Mediterranean Kitchen（cuisine 为 mediterranean）与 Penny Roma（cuisine 为 italian），评论片段分别为 “This is your place ...” 与 “My girlfriend was craving pasta on a Monday night ...”；嵌入向量数值【抽取不清】。用户话轮被拆开，可见 “Hey! Can you recommend me an restaurant with a ?”，并另有 Italian 与 romantic atmosphere。SUQL 一侧可见 `SELECT *, summary(reviews) FROM restaurants WHERE AND LIMIT 1;`，以及条件片段 `'italian' = ANY(cuisines)` 与 `answer(reviews, 'is this restaurant romantic?') = 'Yes'`；WHERE 与 AND 之间的完整连接【抽取不清】。一侧回复提到 Hummus Mediterranean Kitchen，并标注 wrong cuisine、no mention of romantic atmosphere in review；另一侧回复提到 Penny Roma，评分为 4.0，并称氛围 delightful, authentic，且 perfect for a date spot。其余单元格文字【抽取不清】。

本文提出一种把对话代理锚定在混合数据源上的方法，以充分利用结构化数据查询与自由文本检索技术。

我们的第一项贡献是从经验上表明：在真实对话中，用户自然会提出同时跨越结构化与非结构化数据的问题。通过众包，我们获得用户提出的问题，以及他们与餐馆聊天机器人的对话。结果显示，这些问题中超过 49% 需要同时来自结构化知识与非结构化知识的信息。

为利用形式查询语言的表达力与精确性，我们提出 SUQL，一种精确、简洁、可组合、富有表达力且可执行的形式语言。SUQL 用若干处理自由文本的原语来增强 SQL。在高层面上，SUQL 把现成的检索模型与 LLM（用于非结构化数据）与 SQL 的语义及算子（用于结构化数据）结合起来。

我们使用 HybridQA 数据集验证该方法。HybridQA 上的实验表明，一个基于 SUQL 的少样本问答系统，在 Exact Match 上与在超过 62K 条数据样本上训练的 SOTA 模型相差 8.9%，在 F1 上相差 7.1%。

我们开发了一个完全可运行的对话代理，带有基于少样本 LLM 的 SUQL 语义解析器，如图 1 下半部分所示。我们在 Yelp 这一大型真实知识语料上创建了新的单轮用户问题数据集与对话数据集。使用 SUQL 的聊天机器人在 90.3% 的情况下找到满足用户全部要求的实体，而基于线性化的基线为 63.4%。

## 2 Related Work 相关工作

Text-to-SQL 语义解析。Text-to-SQL 系统既被构建用于单轮问答任务（Guo and Gao, 2020; Wang et al., 2020a; Scholak et al., 2021; Zhong et al., 2017），也被用于多轮对话任务（Yu et al., 2019a,b; Wang et al., 2020b; Liu et al., 2022）。近期，LLM 通过上下文学习（Brown et al., 2020）在 text-to-SQL 语义解析问题上显示出有希望的结果，一系列工作聚焦各种提示策略（Hu et al., 2022; Poesia et al., 2022; An et al., 2023; Nan et al., 2023; Arora et al., 2023; Guo et al., 2023; Sun et al., 2023; Zhang et al., 2023b）。

这一路线只适用于不含自由文本的结构化数据源。面对自由文本时，SQL 仅限于对字符串做基本模式匹配，从而妨碍了在需要更深支持的场合应用 text-to-SQL。

使用分类器的专门模块。为混合来源构建对话界面的一种做法，是对每个问题分类，并把它分配给专门模块之一。例如，Chirpy（Chi et al., 2022）实现不同模块来处理不同种类的问题。Jin et al. (2021) 与 Zhao et al. (2023) 实现一个 “Turn Detection” 模块，以判断某一用户轮次是涉及非结构化数据访问，还是应由 API/数据库处理。然而，真实用户问题自然地同时跨越结构化列与自由文本列，用分离模块构建的系统无法回答这类问题。

线性化结构化数据。另一种流行做法是把结构化数据变成线性形式，从而可以直接被语言模型使用。一种常见做法是逐行线性化原始表，并把线性化内容送入表格语言模型（Tabular Language Model, TaLM）（Herzig et al., 2020; Yin et al., 2020; Eisenschlos et al., 2021; Deng et al., 2022; Iida et al., 2021; Sun et al., 2022）。特别地，Oguz et al. (2022) 线性化 Wikidata 与 Wikipedia 表格，把它们与 Wikipedia 文本结合起来，并把检索模型应用于开放域问答。然而，这一做法本质上有局限。许多查询仅靠自由文本很难回答，例如 “What are the number of deaths due to Covid in August and September 2020 in New York?”。这类询问可以用结构化数据轻松处理，因为结构化数据支持在大型数据库上进行比较与计算。此外，线性化使数据库不同部分的统一变得复杂。
