# SUQL: Conversational Search over Structured and Unstructured Data with Large Language Models

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`SUQL_NAACL2024.pdf`。

## Abstract 摘要

尽管大多数对话智能体要么锚定于自由文本，要么锚定于结构化知识，许多知识语料却由混合来源构成。本文提出首个对话智能体，它借助我们开发的语言 SUQL（Structured and Unstructured Query Language，结构化与非结构化查询语言），对大规模知识语料支持混合数据访问的完整一般性。具体而言，SUQL 用自由文本原语（SUMMARY 与 ANSWER）扩展 SQL，从而使信息检索能够以形式化、简洁、精确且可解释的记法，与结构化数据访问任意组合。基于 SUQL，我们提出首个能够处理混合数据源的语义解析器：一个使用上下文学习（in-context learning）的大语言模型（large language model, LLM）。

把这一基于上下文学习的方法用于 HybridQA 数据集时，其 Exact Match 与 F1 同在 62K 条样本上训练得到的 SOTA 分别只相差 8.9% 与 7.1%。更重要的是，与先前方法不同，我们的技术适用于大规模数据库与自由文本语料。

我们引入一个由众包问题与对话构成的数据集，其对象是 Yelp，一个同时含有结构化与非结构化数据的大型真实餐馆知识库。我们表明，基于 SUQL 的少样本对话智能体在 90.3% 的情况下能找到满足用户全部要求的实体，而基于线性化（linearization）的基线为 63.4%。¹

¹ 代码与数据见 https://github.com/stanford-oval/suql。

## 1 Introduction 引言

大语言模型（Large Language Models, LLMs）在众多下游任务上表现突出。近期一系列工作着眼于把回答锚定在外部资源上，以改进其事实性；这些资源包括结构化数据（Hu et al., 2022; An et al., 2023; Nan et al., 2023; Poesia et al., 2022; Arora et al., 2023; Xu et al., 2020, 2023）以及自由文本（Khattab et al., 2023; Jiang et al., 2023; Semnani et al., 2023; Gao et al., 2023）。

然而，许多数据源同时包含结构化数据与自由文本，例如病历、金融数据库和点评网站。附录中的图 2 给出了本文所使用应用的贯穿示例。该表的每一行代表一家独一无二的餐馆，名称、菜系类型和评分等信息属于结构化数据。此外，每一行还以自由文本包含热门菜品与顾客评论。要回答诸如 “Can you find me an Italian restaurant with a romantic atmosphere?” 这样的问题，智能体需要把结构化属性 cuisines 与自由文本属性 reviews 结合起来。

为处理结构化数据与非结构化数据的组合，许多先前的聊天系统使用分类器，把查询分配到专门处理结构化数据、非结构化数据或闲聊的模块之一（Jin et al., 2021; Chi et al., 2022; Zhao et al., 2023）。这一做法不足以回答同时需要自由文本与结构化数据的问题。

另一种流行做法是把结构化数据转换或线性化（linearize）为自由文本（Oguz et al., 2022），如图 1 所示。采用这一做法之后，我们不再能运用 SQL 来查询数据库，而自由文本检索器并不擅长处理复杂问题。

HybridQA 数据集突出了组合混合数据源查询的需要。该数据集收集了许多自然问题，其答案同时包含来自结构化数据与自由文本的信息（Chen et al., 2020）。先前试图把问答系统锚定在混合数据上的工作（Lei et al., 2023; Wu et al., 2023; Kumar et al., 2023; Lee et al., 2023a），或者只适用于小数据集，或者放弃了结构化数据查询的表达能力，或者只支持结构化知识查询与非结构化知识查询的有限组合。

图 1：传统方法（线性化）与我们的方法（使用 SUQL 的语义解析）的比较。上方：在线性化方法中，数据库条目被线性化并转换为嵌入向量。运行时，用户请求被转换为一个嵌入向量，用来在已存储的向量中寻找最接近的嵌入。结果随后提供给 LLM 以生成回复。下方：在我们的方法（使用 SUQL 的语义解析）中，用户话语由经过少样本提示的 LLM 解析为形式化 SUQL，再由 SUQL 编译器执行，从数据库取回结果。结果随后提供给 LLM 以生成回复。

图中两侧的用户请求均为 “Hey! Can you recommend me an Italian restaurant with a romantic atmosphere?”。线性化一侧给出被线性化的条目，其中包括 Name, Hummus Mediterranean Kitchen, cuisine, mediterranean，以及评论片段 “This is your place ...”；另有 Name, Penny Roma, cuisine, italian，以及评论片段 “My girlfriend was craving pasta on a Monday night ...”。评论开头有一处抽取为 “| t l ; d r |”【抽取不清】。这些条目被转换成嵌入向量；图中可辨认的数值包括 0.076、0.865、…、-0.732、0.376、-0.265、-0.746、…、-0.922、-0.301、…、0.495，其余向量分量【抽取不清】。该路径的回复是 “I found Hummus Mediterranean Kitchen. It is a 4 star Mediterranean restaurant in San Francisco with a clean and welcoming atmosphere.”，并标注 wrong cuisine; no mention of romantic atmosphere in review。SUQL 一侧由带有 DB schema 与 few-shot examples 的 Semantic Parser 生成查询；图中可辨认的片段为：

```
SELECT *, summary(reviews) FROM restaurants
WHERE AND
LIMIT 1;
'italian' = ANY(cuisines)
answer(reviews, 'is this restaurant romantic?') = 'Yes'
```

WHERE 与两个谓词在图中被拆开排布，AND 单独出现。该查询经 SUQL Compiler 与 Embedding model 执行，图中还标有 Cos Sim 与 linearize。回复为 “I found Penny Roma, which has a 4.0 rating on our database and offers a variety of Italian dishes. Overall, the atmosphere is described as delightful, authentic, and perfect for a date spot.”。图中 “4.0”“database”“described”“Yes”“Embedding”“Italian” 等词被空格拆开，此处按词内空格还原。

本文提出一种把对话智能体锚定在混合数据源上的方法，以同时充分利用结构化数据查询与自由文本检索技术。

我们的第一项贡献，是从经验上表明：在真实对话中，用户会自然地提出同时跨越结构化数据与非结构化数据的问题。通过众包，我们收集用户提出的问题，以及他们与餐馆聊天机器人进行的对话。结果显示，这些问题中超过 49% 需要同时来自结构化知识与非结构化知识的信息。

为利用形式查询语言的表达能力与精确性，我们提出 SUQL。它是一种精确、简洁、可组合、富有表达力且可执行的形式语言。SUQL 为 SQL 增加了若干处理自由文本的原语。在较高层面上，SUQL 把现成的检索模型以及用于非结构化数据的 LLM，与用于结构化数据的 SQL 语义和算子结合起来。

我们使用 HybridQA 数据集验证这一方法。HybridQA 上的实验表明，一个基于少样本和 SUQL 的问答系统，其 Exact Match 与 F1 同在超过 62K 条样本上训练的 SOTA 模型分别只相差 8.9% 与 7.1%。

我们开发了一个完全可运行的对话智能体，其中包含基于少样本 LLM 的 SUQL 语义解析器，如图 1 下方所示。我们在 Yelp 这一大型真实知识语料上新建了单轮用户问题数据集和对话数据集。使用 SUQL 的聊天机器人在 90.3% 的情况下找到满足用户全部要求的实体，而基于线性化的基线为 63.4%。

## 2 Related Work 相关工作

### Text-to-SQL Semantic Parsing 文本到 SQL 的语义解析

Text-to-SQL 系统既被用于单轮问答任务（Guo and Gao, 2020; Wang et al., 2020a; Scholak et al., 2021; Zhong et al., 2017），也被用于多轮对话任务（Yu et al., 2019a,b; Wang et al., 2020b; Liu et al., 2022）。近期，LLM 经由上下文学习（Brown et al., 2020）在 text-to-SQL 语义解析问题上取得了有前景的结果，一系列工作关注各种提示策略（Hu et al., 2022; Poesia et al., 2022; An et al., 2023; Nan et al., 2023; Arora et al., 2023; Guo et al., 2023; Sun et al., 2023; Zhang et al., 2023b）。

这一路线只适用于不含自由文本的结构化数据源。面对自由文本时，SQL 仅限于对字符串做基本的模式匹配，因此在需要更深层支持的场合，text-to-SQL 难以应用。

### Specialized Modules Using a Classifier 使用分类器的专用模块

为混合来源构建对话接口的一种做法，是对每个问题进行分类，并把它分配给某个专用模块。例如，Chirpy（Chi et al., 2022）实现了不同模块来处理不同种类的问题。Jin et al. (2021) 与 Zhao et al. (2023) 实现了一个 “Turn Detection” 模块，用来判断某个用户轮次是涉及非结构化数据访问，还是应当由 API 或数据库处理。然而，真实的用户问题会自然地同时跨越结构化列与自由文本列，由彼此分离的模块搭建而成的系统无法回答这类问题。

### Linearize structured data 将结构化数据线性化

另一种流行做法是把结构化数据变成线性形式，从而可以直接交给语言模型使用。常见做法是把原始表格逐行线性化，再把线性化后的内容送入表格语言模型（Tabular Language Model, TaLM）（Herzig et al., 2020; Yin et al., 2020; Eisenschlos et al., 2021; Deng et al., 2022; Iida et al., 2021; Sun et al., 2022）。特别地，Oguz et al. (2022) 线性化了 Wikidata 与 Wikipedia 的表格，把它们与 Wikipedia 文本结合起来，并把检索模型用于开放域问答。然而，这一做法本身是有限的。许多查询很难只靠自由文本回答，例如 “What are the number of deaths due to Covid in August and September 2020 in New York?”。这类询问可以很容易地用结构化数据处理，因为结构化数据支持在大型数据库上进行比较与计算。此外，线性化也使数据库中不同部分难以统一。
