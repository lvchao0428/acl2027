# SUQL：基于大语言模型在结构化与非结构化数据上的对话式搜索

- 原文件名：SUQL_NAACL2024.pdf
- 原标题：SUQL: Conversational Search over Structured and Unstructured Data with Large Language Models
- 中文标题：SUQL：基于大语言模型在结构化与非结构化数据上的对话式搜索
- 作者：Shicheng Liu, Jialiang Xu, Wesley Tjangnaka, Sina J. Semnani, Chen Jie Yu, Monica S. Lam
- 会议：Findings of the Association for Computational Linguistics: NAACL 2024（pages 4535–4555，June 16–21, 2024）

作者单位：Computer Science Department, Stanford University, Stanford, CA

邮箱：{shicheng, xjl, wesleytj, sinaj, jyu01, lam}@cs.stanford.edu

©2024 Association for Computational Linguistics

<!-- 原 PDF 第 1 页 -->

## 摘要

尽管大多数对话智能体要么锚定于自由文本，要么锚定于结构化知识，许多知识语料却由混合来源构成。本文提出首个面向大规模知识语料、支持混合数据访问之完全一般性的对话智能体，其所借助的语言是我们开发的 SUQL（Structured and Unstructured Query Language，结构化与非结构化查询语言）。具体而言，SUQL 用自由文本原语（SUMMARY 与 ANSWER）扩展 SQL，从而使信息检索能够以一种形式化、简洁、精确且可解释的记号，与结构化数据访问任意组合。借助 SUQL，我们提出首个能够处理混合数据源的语义解析器：一个使用上下文学习的大语言模型。

把这一基于上下文学习的方法用到 HybridQA 数据集上时，其 Exact Match 与 F1 分别落在 SOTA 的 8.9% 与 7.1% 以内，而该 SOTA 是在 6.2 万条数据样本上训练得到的。更重要的是，与先前方法不同，我们的技术适用于大型数据库和自由文本语料。

我们引入一个由众包问题与对话构成的数据集，其对象是 Yelp，一个同时包含结构化与非结构化数据的大型真实餐馆知识库。我们表明，基于 SUQL 的少样本对话智能体在 90.3% 的情况下能找到满足用户全部要求的实体，而基于线性化的基线为 63.4%。[^1]

[^1]: 代码与数据见 https://github.com/stanford-oval/suql

## 1 引言

大语言模型（LLM）已在众多下游任务上表现出色。近期一批工作致力于把回答锚定到外部资源上，以改善其事实性。这些资源包括结构化数据（Hu et al., 2022; An et al., 2023; Nan et al., 2023; Poesia et al., 2022; Arora et al., 2023; Xu et al., 2020, 2023）和自由文本（Khattab et al., 2023; Jiang et al., 2023; Semnani et al., 2023; Gao et al., 2023）。

然而，许多数据源同时包含结构化数据与自由文本：病历、金融数据库、评论网站，仅举数例。附录中的图 2 给出了本文所用应用的贯穿示例。该表中每一行代表一家独特的餐馆，其名称、菜系类型、评分等信息是结构化数据。此外，每一行还以自由文本包含招牌菜与顾客评论。要回答“能帮我找一家有浪漫氛围的意大利餐馆吗？”这类问题，智能体需要把结构化属性 cuisines 与自由文本属性 reviews 结合起来。

为处理结构化与非结构化数据的组合，许多以往的聊天系统使用分类器，把查询分配给专门处理结构化数据、非结构化数据或闲聊的模块之一（Jin et al., 2021; Chi et al., 2022; Zhao et al., 2023）。可惜，这一做法不足以回答同时需要自由文本与结构化数据的问题。

另一种常见做法是把结构化数据转换或线性化成自由文本（Oguz et al., 2022），如图 1 所示。采用这种做法后，我们便无法再运用 SQL 查询数据库的能力，而自由文本检索器也不擅长处理复杂问题。

混合数据源查询需要加以组合，这一点由 HybridQA 数据集所突出。该数据集收集了许多自然问题，其答案同时包含来自结构化数据与自由文本的信息（Chen et al., 2020）。先前试图把问答系统锚定在混合数据上的工作（Lei et al., 2023; Wu et al., 2023; Kumar et al., 2023; Lee et al., 2023a）或者只在小数据集上有效，或者放弃了结构化数据查询的表达力，或者只支持结构化与非结构化知识查询的有限组合。

<!-- 原 PDF 第 2 页 -->

**图 1：传统做法（线性化）与我们的做法（结合 SUQL 的语义解析）之比较。**

图中文字如下。

上半部分为线性化（向量数据库）。数据库条目经 linearize 后变成文本，例如：

- Name, Hummus Mediterranean Kitchen, cuisine, mediterranean, ..., reviews, | t l ; d r | This is your place ...
- Name, Penny Roma, cuisine, italian, ..., reviews, My girlfriend was craving pasta on a Monday night ...

这些文本送入 Embedding model，并与用户话语的嵌入做余弦相似度（Cos Sim）。文本层可见的嵌入分量包括：0.076、0.865、…、-0.732；-0.746；-0.301、…、0.495；0.376、-0.265；…、-0.922。

用户：Hey! Can you recommend me an Italian restaurant with a romantic atmosphere?（嘿！你能推荐一家有浪漫氛围的意大利餐馆吗？）

系统回答：I found Hummus Mediterranean Kitchen. It is a 4 star Mediterranean restaurant in San Francisco with a clean and welcoming atmosphere.（我找到了 Hummus Mediterranean Kitchen。它是旧金山一家 4 星地中海餐馆，氛围干净、令人感到受欢迎。）旁注标明该回答错误：wrong cuisine; no mention of romantic atmosphere in review（菜系错误；评论中未提及浪漫氛围）。

下半部分为结合 SUQL 的语义解析。同一用户话语连同 DB schema 与 Few-shot examples 送入 Semantic Parser，得到：

```sql
SELECT *, summary(reviews) FROM restaurants
WHERE 'italian' = ANY (cuisines)
AND answer(reviews, 'is this restaurant romantic?') = 'Yes'
LIMIT 1;
```

该查询由 SUQL Compiler 在数据库上执行。系统回答：I found Penny Roma, which has a 4.0 rating on our database and offers a variety of Italian dishes. Overall, the atmosphere is described as delightful, authentic, and perfect for a date spot.（我找到了 Penny Roma，它在我们的数据库中评分为 4.0，提供多种意大利菜。总体而言，氛围被描述为令人愉快、地道，并且 perfect for a date spot。）

图注：上：在线性化做法中，数据库条目被线性化并转换成嵌入向量。运行时，用户请求被转换成嵌入向量，用以从已存储的向量中找出最接近的嵌入。结果再提供给 LLM 以生成回复。下：在我们的做法（结合 SUQL 的语义解析）中，用户话语由经过少样本提示的 LLM 解析为形式化的 SUQL，再由 SUQL 编译器执行，从数据库取回结果。结果再提供给 LLM 以生成回复。

本文提出一种把对话智能体锚定于混合数据源的方法，以充分运用结构化数据查询与自由文本检索技术。

我们的第一项贡献是从经验上表明：在真实对话中，用户自然会提出同时跨越结构化与非结构化数据的问题。通过众包，我们获得用户会提出的问题，以及他们与餐馆聊天机器人的对话。结果显示，这些问题中超过 49% 需要同时来自结构化知识与非结构化知识的信息。

为利用形式查询语言的表达力与精确性，我们提出 SUQL，一种精确、简洁、可组合、富有表达力且可执行的形式语言。SUQL 为 SQL 增加了若干处理自由文本的原语。在高层上，SUQL 把现成的检索模型与 LLM（用于非结构化数据）同 SQL 的语义与算子（用于结构化数据）结合在一起。

我们用 HybridQA 数据集验证该方法。HybridQA 上的实验表明，一个少样本、基于 SUQL 的问答系统，其 Exact Match 与 F1 分别落在 SOTA 的 8.9% 与 7.1% 以内，而该 SOTA 模型是在超过 6.2 万条数据样本上训练的。

我们开发了一个完全可运行的对话智能体，其中包含一个基于少样本 LLM、使用 SUQL 的语义解析器，如图 1 下半部分所示。我们在 Yelp 这一大型真实知识语料上创建了新的单轮用户问题数据集和对话数据集。使用 SUQL 的聊天机器人在 90.3% 的情况下能找到满足用户全部要求的实体，而基于线性化的基线为 63.4%。

## 2 相关工作

**Text-to-SQL 语义解析。** Text-to-SQL 系统既被构建用于单轮问答任务（Guo and Gao, 2020; Wang et al., 2020a; Scholak et al., 2021; Zhong et al., 2017），也被用于多轮对话任务（Yu et al., 2019a,b; Wang et al., 2020b; Liu et al., 2022）。近来，LLM 经由上下文学习（Brown et al., 2020）在 text-to-SQL 语义解析问题上显示出有希望的结果，一系列工作聚焦于各种提示策略

<!-- 原 PDF 第 3 页 -->

（Hu et al., 2022; Poesia et al., 2022; An et al., 2023; Nan et al., 2023; Arora et al., 2023; Guo et al., 2023; Sun et al., 2023; Zhang et al., 2023b）。

这一路线只适用于不含任何自由文本的结构化数据源。面对自由文本时，SQL 仅限于对字符串做基本的模式匹配，从而妨碍了在需要更深支持之处应用 text-to-SQL。

**使用分类器的专用模块。** 为混合来源构建对话界面的一种做法，是对每个问题分类，并把它分配给某个专用模块。例如，Chirpy（Chi et al., 2022）实现不同模块来处理不同种类的问题。Jin et al. (2021) 与 Zhao et al. (2023) 实现了一个“Turn Detection”（轮次检测）模块，用来判断某一用户轮次是涉及非结构化数据访问，还是应由 API/数据库处理。然而，真实用户问题自然会同时跨越结构化列与自由文本列，由彼此分离的模块建成的系统无法回答这类问题。

**线性化结构化数据。** 另一种常见做法是把结构化数据变成线性形式，再直接交给语言模型使用。常见做法是按行线性化原始表格，并把线性化内容送入表格语言模型（TaLM）（Herzig et al., 2020; Yin et al., 2020; Eisenschlos et al., 2021; Deng et al., 2022; Iida et al., 2021; Sun et al., 2022）。具体而言，Oguz et al. (2022) 线性化 Wikidata 与 Wikipedia 表格，把它们与 Wikipedia 文本结合起来，并把检索模型用于开放域问答。然而，这一做法有其固有限制。许多查询很难仅靠自由文本回答，例如“2020 年 8 月和 9 月纽约因 Covid 死亡的人数是多少？”。这类询问用结构化数据很容易处理，因为结构化数据支持在大型数据库上进行比较与计算。此外，线性化使数据库不同部分的统一变得复杂。

## 3 SUQL 的设计与理据

本节给出 SUQL 语言的设计及其理据。该表示的设计目标是表达力、准确性与效率。

### 3.1 设计理据

**表达力。** 设计必须具有表达力，支持对混合知识语料的查询的完全一般性。它必须能处理（1）数据库中的关系算子与（2）对自由文本文档的查询之任意组合。注意，这样的设计自动涵盖自然语言处理文献中的多跳检索：一次检索得到的答案被用来进行另一次检索。

SQL 等形式语言已被证明相对于关系代数是完备的（Codd et al., 1972）。凭借其文法规则，它可以处理任意组合；例如，这些规则可以产生无界数量的嵌套子查询。

我们提出的不是把全部结构化数据变成文本的线性化，而是相反的方向。SUQL 是 SQL 的扩展，增加了两个 NLP 算子 SUMMARY 与 ANSWER：SUMMARY 产生给定文本的摘要，ANSWER 返回针对给定文本的答案。这两个算子可以用在文法中任何出现文本值的位置，这与数值算子作用于数值并无不同。这一设计的优点在于，SUQL 是一种简洁的形式表示，相对于关系代数与 NLP 运算是完备的。

**从自然语言翻译的准确性。** LLM 已被证明能够把复杂文本从一种自然语言翻译成另一种。它们可以把复杂句子翻译成 SQL 查询，尽管数据库较小，并且涉及 group-by、排序与子查询等复合运算。

我们认为，SUQL 将为 LLM 提供一种简洁记号，用以表达涉及混合数据源的复杂查询。借助 LLM 对 SQL 的熟悉，我们假设可以通过上下文学习，用 LLM 构造一个语义解析器，把对话中的用户查询翻译成 SUQL 查询。

**效率。** SUQL 查询可以由 SQL 编译器执行而无需修改，因为 SUMMARY 与 ANSWER 原语可以简单地作为用户定义函数提供。然而，这样的 SQL 编译器会表现得很差。这些文本原语的朴素实现需要逐条记录检索并施加 NLP 运算，对大表而言代价高得不可行。对

<!-- 原 PDF 第 4 页 -->

ANSWER 函数的朴素执行不会有效。

注意，与检索式语义解析等先前方法不同——那些方法随着结果被检索而构造查询（Cao et al., 2022; Gu and Su, 2022）——SUQL 把查询完整地表达出来。这使我们有可能开发一个优化编译器，如第 5 节所述。

### 3.2 SUQL 的设计

我们为 SQL 中的文本值引入两种运算。本文用 text 表示 SQL 中的任一文本类型（CHAR、VARCHAR、TEXT 等）。

我们定义 ANSWER(t, q) 返回针对文本输入 t 上问题 q 的答案。例如，

```text
ANSWER(reviews, 'is this restaurant family-friendly?')
```

若评论表明该餐馆适合家庭，则返回 yes，否则返回 no。结果是一个文本值，可以用在任何允许文本值的位置。例如，

```text
ANSWER(reviews, 'is this restaurant family-friendly?') = 'Yes'
```

可以用作过滤器，以选出适合家庭的餐馆。

ANSWER 是一个通用函数，只要提供合适的问题，就可以从文本值中导出任何信息。不过，为方便起见，我们引入 SUMMARY(t)，作为

```text
ANSWER(t, 'what is the summary of this document?')
```

的语法糖。我们认为语义解析器可以很容易学会使用 SUMMARY。ANSWER 与 SUMMARY 的形式定义见表 1。

**表 1：SUQL 中的自由文本原语**

| 算子 | 描述 | 示例 |
| --- | --- | --- |
| ANSWER(t : text \| text[], q : text) → text | 返回针对值 t 上问题 q 的答案 | ANSWER(reviews, "is this restaurant family-friendly?") |
| SUMMARY(t : text \| text[]) → Text | 返回 t 的摘要 | SUMMARY(reviews) |

ANSWER 与 SUMMARY 运算可以作用于任何文本实参，其结果可以用在期望文本值的位置，从而形成混合数据访问的组合。自由文本原语与其他 SQL 算子的复杂组合，由 HybridQA 数据集中的问题所突出。在 HybridQA 中，列 C 的每个单元格都可能链接到某些段落，我们把这些段落存放在名为 C_Info 的单独一列中。该数据集中的全部问题都可以用 SUQL 表示。我们在表 2 中给出 6 个有代表性的例子，说明每一类问题如何用 SUQL 表示。

## 4 对话智能体

以 SUQL 作为形式表示，带有混合知识语料的对话智能体的架构相对直接。

给定模式 S 的、基于 SUQL 的对话智能体，其对话状态跟踪问题（Cheng et al., 2020; Andreas et al., 2020; Campagna et al., 2022）定义如下。我们把对话历史定义为用户与智能体之间的一串话语 $A_1, U_1, \cdots, A_n, U_n$，其中 $A_i$ 与 $U_i$ 分别表示第 $i$ 轮的智能体话语与用户输入。每个 $U_i = (t_i, q_i)$，其中 $t_i$ 是自然语言文本输入；若 $t_i$ 携带查询，则 $q_i$ 是针对模式 $S$ 的一条 SUQL 查询。给定模式 $S$、所有先前轮次 $1 \leq i < n$ 的 $(A_i, U_i)$，以及最新的用户话语 $t_n$，若 $t_n$ 携带查询，对话状态跟踪预测 $q_n$。

对话状态跟踪的语义解析器由两个阶段组成，二者都用 LLM 通过上下文学习实现。第一阶段判断是否需要查阅知识语料。对于问候或一般性问题之类的用户话语，它跳过对知识语料的访问。若需要查阅，第二阶段预测 $q_n$。提示词包含模式定义，以及展示 SUQL 自由文本原语的少样本示例。

若用户话语对应一条查询，则执行预测出的 SUQL 查询。由于语义解析器可能把用户查询翻译错，系统通过提示词指示智能体根据本轮预测出的 SUQL，向用户明确说明它搜索了什么（例如：“我搜索了有浪漫氛围的意大利餐馆。”）。若搜索返回了结果，我们

<!-- 原 PDF 第 5 页 -->

**表 2：HybridQA 中的问题类型，以及与示例问题（Chen et al. (2020) 的图 3）对应的 SUQL 查询。**

| 问题类型 | 示例问题 | SUQL 查询 |
| --- | --- | --- |
| Type I | 第 XXXI 届奥运会在哪里举办？ | `SELECT answer("Event year Info", 'where is this event held?') FROM table WHERE "Name" = 'XXXI';` |
| Type II | 在里约举办的奥运赛事名称是什么？ | `SELECT "Name" FROM table WHERE answer("Event year Info", 'is this event held in Rio?') = 'Yes';` |
| Type III | 里约奥运会的旗手出生于何时？ | `SELECT answer("Flag Bearer Info", 'when is this person born?') FROM table WHERE answer("Event year Info", 'is this event held in Rio?') = 'Yes';` |
| Type IV | 哪位男性旗手参加了奥运会男子 100 公斤项目？ | `SELECT "Flag Bearer" FROM table WHERE "Gender" = 'Male' AND answer("Flag Bearer Info", 'did this person participate in Men''s 100kg event?') = 'Yes';` |
| Type V | 对于 2012 与 2016 奥运赛事，较年轻的那位旗手出生于何时？ | `SELECT MAX(answer("Flag Bearer Info", 'when is this person born?')::date) FROM table WHERE "Event year" IN ('2016', '2012');` |
| Type VI | 最年轻的缅甸旗手于何时参加奥运会开幕式？ | `SELECT "Event year" FROM table ORDER BY answer("Flag Bearer Info", 'when is this person born?')::date DESC LIMIT 1;` |

请 LLM 根据结果组织回复；否则，我们明确要求它表明没有找到结果。后者很重要，因为只要没有向 LLM 提供用户问题的答案，它就倾向于产生幻觉。

## 5 一个做优化的 SUQL 编译器

这里描述我们在 SUQL 编译器中实现的关键优化。

### 5.1 搜索与过滤优化

当 ANSWER 在查询中用作过滤器时，朴素实现需要对数据库中的每一条记录调用一次 LLM，这不可行。与用数据库索引优化查询类似，我们使用稠密检索模型快速找出相关记录，而不是逐条处理。此外，若只需要少数结果，就没有必要在全部记录上评估过滤器。

首先，我们的 SUQL 优化编译器识别使用 ANSWER 函数的过滤器。它使用稠密检索模型预先计算的嵌入，与问题做相似度匹配，以找出靠前的候选。注意，检索到的答案是相关的，但它们未必满足过滤约束。我们在整个子句上调用 LLM，以判断过滤器是否成功。例如，若用户要找停车方便的餐馆，而某条评论恰好说“停车很难”。如果没有其他评论提到“parking”，这条评论的相似度分数可能最高。因此，我们需要用 LLM 施加原始过滤器 `ANSWER(reviews, 'is parking easy?') = 'Yes'`，以确保检索到的评论确实说停车方便（提示词 8）。

若存在多个自由文本约束，SUQL 编译器使用基于每个约束的聚合相似度分数，检索最有可能满足全部约束的结果。形式上，每一行 $r$ 的聚合相似度分数计算为：

\[
\sum_{c} \max_{t} \mathrm{sim}(c, t)
\]

其中 $c$ 是一个文本约束，$t$ 是行 $r$ 中的一段文本，$\mathrm{sim}(\cdot, \cdot)$ 表示两段文本之间的相似度分数。

### 5.2 枚举类型

枚举类型（ENUM）广泛用于结构化属性，把文本类型的取值限制为预定义许可值集合中的一个或多个。ENUM 标准化属性的取值，因此基于该变量的过滤可以做成属性值与许可字面量之间的简单字符串匹配。

挑战在于如何确保语义解析器会把 ENUM 属性值映射到某个许可值。对于许可值个数不大于 $N = 10$ 的所有 ENUM 类型声明，我们把全部许可值放进提供给 LLM 的模式声明提示中。可以观察到，LLM 能够自动生成 ENUM 值。对于更大的 ENUM 类型，我们不放入许可值，解析器可能生成意料之外的值。例如，用户话语“Where can I find coffee”（我在哪里能找到咖啡）很可能被翻译成过滤子句 `'coffee' = ANY(cuisines)`。然而，Yelp 数据库只有 `'coffee & tea'` 或 `'cafe'` 菜系，而没有 `'coffee'`。

我们的解决办法是重新定义枚举类型上 `=` 算子的语义。这在编译器文献中称为重载（overloading）。我们首先定义 CLASSIFY 函数：

<!-- 原 PDF 第 6 页 -->

**定义 5.1.**

\[
\begin{aligned}
&\mathrm{CLASSIFY}(t : \mathrm{text},\; S : v_1, \ldots, v_n) \\
&\quad = \{v_{i_1}, \ldots, v_{i_m}\}, \quad \forall v_{i_k} \in S \text{ 且与 } t \text{ 相似。}
\end{aligned}
\]

这里，若两个字符串含义相近，我们称它们相似。有可能感兴趣的值并不在许可值集合之中，此时 CLASSIFY 返回 $\emptyset$。我们用一个零样本 LLM 实现 CLASSIFY（提示词 6）。

**定义 5.2.** 相等算子 `=` 被重载，使得

\[
t_1 = t_2 \iff t_2 \in \mathrm{CLASSIFY}(t_1, E),
\]

其中 $t_1 : \mathrm{text}$，$t_2 : \mathrm{ENUM}(E)$。

例如，给定子句 `'coffee' = ANY(cuisines)`，其中 $\mathrm{CLASSIFY}(\text{‘coffee’}, \mathrm{cuisines}) = \{\text{‘coffee \& tea’}, \text{‘cafe’}\}$，则该子句将匹配 cuisine 属性包含 `'coffee & tea'` 或 `'cafe'` 的任何记录。

### 5.3 查询顺序优化

由于 ANSWER 与 SUMMARY 涉及 LLM 调用，尽量减少这类函数的执行很重要。

**谓词排序。** 如上所述，过滤器中的 ANSWER 函数比其他谓词昂贵。因此，只要可能，SUQL 编译器会优先执行其他谓词，从而使 ANSWER 作用到更少的记录上。

具体而言，SUQL 编译器把带有过滤谓词的 SELECT 子句转换成析取范式（DNF），即若干 AND 的 OR。对每个 AND 子句，它优先处理不使用 ANSWER 函数的过滤器，从而只对过滤后的记录调用 ANSWER。

**惰性求值。** 惰性求值，即只在需要结果时才求值，是编程语言中一个由来已久的概念（Hudak, 1989）。SUQL 编译器采用这一概念以尽量降低执行代价。具体而言，当存在 LIMIT 子句时，一旦填满所需行数，它就停止求值。

## 6 实验

为评估 SUQL，我们进行两项实验。第一项在 HybridQA 上，这是上文讨论过的一个常用学术问答数据集。HybridQA 中的表小到足以作为输入提供给神经模型。为了在与大型真实数据库的对话上做更全面的实验，我们基于 Yelp.com 的真实餐馆数据语料引入一个新基准。

### 6.1 HybridQA 实验

HybridQA 数据集由大约 7 万个问答对组成，与 1.3 万张 Wikipedia 表格对齐，表中实体链接到多个自由形式语料。每个问题只有同时参照结构化与非结构化数据才能正确回答。为检验 SUQL，我们构建如下系统：

1. 使用带上下文学习的 LLM（示例少于 10 个）把自然语言和给定的数据库模式解析成 SUQL 查询（提示词 9）。
2. 执行生成的 SUQL，从数据库检索结果。若没有返回结果，则生成另一条 SUQL 查询并重复这一过程，最多尝试 2 次（提示词 10）。
3. 使用 LLM 把检索到的数据库结果转换成简短答案（提示词 11），因为 HybridQA 的黄金标签很短。由于黄金标签只有一个实体，尽管完整答案可能包含多个实体，我们只从 SUQL 返回的可能很多的结果中挑出一个。

除第 3 步使用 GPT-3.5-turbo-0613 外，所有步骤都使用 GPT-4-1106-preview。

我们基于上下文学习的问答系统在 HybridQA 开发集上达到 59.3% Exact Match 与 68.3% F1，在留出测试集上达到 59.0% EM 与 68.4% F1，如表 3 所示。我们的方法只用 3 个简单提示词，在测试集上与 SOTA 的差距在 8.9% EM 与 7.1% F1 以内，而该 SOTA 是在超过 6.2 万个样本的 HybridQA 训练集上训练的。

最重要的是，与我们的方法不同，这些模型不能推广到小表之外。把整张表送入 Transformer 的技术（DocHopper、Mate、MITQA、DEHG 与 MAFID）无法用于超出其输入词元上限的大型数据语料。基于检索整列并送入阅读器模型的技术（MuGER2）同样不行。SOTA 模型 S3HQA 分别检索表中的行与段落，再把靠前结果

<!-- 原 PDF 第 7 页 -->

**表 3：少样本 SUQL 及相关工作在 HybridQA 数据集上的表现。† 表示在开发集的 200 个抽样案例上运行（Shi et al., 2024）。** 表中纵向合并的单元格按所跨行重复写出；单次默认 `find_tables` 未检出该表，下列数字来自文本层与表线位置，未另补数字。

| 方法 | 模型 | 训练数据（规模） | 开发集 EM | 开发集 F1 | 测试集 EM | 测试集 F1 |
| --- | --- | --- | --- | --- | --- | --- |
| DocHopper (Sun et al., 2022) | ETC | HybridQA (62k) | 47.7 | 55.0 | 46.3 | 53.3 |
| HYBRIDER (Chen et al., 2020) | BERT | HybridQA (62k) | 44.0 | 50.7 | 43.8 | 50.6 |
| MuGER2 (Wang et al., 2022) | BERT | HybridQA (62k) | 57.1 | 67.3 | 56.3 | 66.2 |
| Mate (Eisenschlos et al., 2021) | BERT | HybridQA (62k) | 63.4 | 71.0 | 62.8 | 70.2 |
| DEHG (Feng et al., 2022) | BERT | HybridQA (62k) | 65.2 | 76.3 | 63.9 | 75.5 |
| MITQA (Kumar et al., 2023) | BERT | HybridQA (62k) | 65.5 | 72.7 | 64.3 | 71.9 |
| MAFiD (Lee et al., 2023b) | T5 | HybridQA (62k) | 66.2 | 74.1 | 65.4 | 73.6 |
| S3HQA (Lei et al., 2023) | BERT/BART/DeBERTa | HybridQA (62k) | 68.4 | 75.3 | 67.9 | 75.5 |
| LLaMA2 (7B) (Zhang et al., 2023a) | LLaMA2 (7B) | Zero-shot | 20.7 | - | - | - |
| TableLlama (Zhang et al., 2023a) | LLaMA2 (7B) | TableInstruct (2.6M) | 27.6 | - | - | - |
| End-to-End QA w/ retriever (Shi et al., 2024) | GPT-4 | Zero-shot | 24.5† | 30.0† | - | - |
| HPROPRO (Shi et al., 2024) | GPT-4 | Few-shot | 48.0† | 54.6† | 48.7 | 57.7 |
| SUQL (Ours) | GPT-4 | Few-shot | 59.3 | 68.3 | 59.0 | 68.4 |

中的每一类送入最终阅读器。若查询涉及排序，它需要把整列送入阅读器。相比之下，我们的方法具有完全的组合一般性，并能处理任意大的数据集。我们是最先把语义解析技术用于 HybridQA 数据集的，因为此前没有形式表示能够准确捕捉混合查询。

近来，Zhang et al. (2023a) 把基于 LLaMA 的技术用于 HybridQA。他们在自己超过 260 万个样本的 TableInstruct 数据集上微调 LLaMA2（7B），在 HybridQA 上只达到 27.6 EM。他们还报告了把 LLaMA2（7B）直接用于 HybridQA 的基线，结果只有 20.7 Exact Match。

Shi et al. (2024) 报告了在 HybridQA 数据集上使用 GPT-4 的两项实验。（1）他们的 GPT-4 End-to-End QA w/ retriever 使用零样本 GPT-4，直接根据 Chen et al. (2020) 的检索器检索到的表格与文本部分回答问题。（2）HPROPRO w/ GPT-4 使用基于程序的少样本提示，在 GPT-4 的帮助下迭代生成并执行 Python 代码。在开发集的 200 个样本上，他们的两个系统分别达到 24.5 与 48.0 EM，以及 30.0 与 54.6 F1。HPROPRO 系统在测试集上达到 48.7 EM 与 47.7 F1。我们基于 SUQL 的方法优于这两个系统，在测试集上 EM 与 F1 都比 HPROPRO 高出 10.0% 以上。

Sui et al. (2023) 也在 HybridQA 上用 GPT-4 做了上下文学习实验。不过，他们只报告了从开发集随机抽取的 1,000 个问题的结果。对每个问题，他们试验把整张表和问题以不同格式（JSON、HTML、Markdown 等）送入 GPT-4。若预测是黄金答案的子串，或反之亦然，则认为预测正确。[^2] 他们报告的最好结果是使用 HTML 格式的 GPT-4，按该指标为 56.68%。用他们的指标在完整开发集上评估，我们基于 SUQL 的系统得分为 72.5%。

这些结果相对其他上下文学习技术，表明了 SUQL 在混合问答任务上的有效性。

**错误分析。** 分析 100 个随机抽取的错误案例后，我们发现：

- 44% 是格式不匹配，例如 “Johnson City, Tenessee” 与 “Johnson City”。Kamalloo et al. (2023) 已指出评估 LLM 生成回复时的类似问题。
- 20% 是因为黄金标签错误或不完整。不完整的情况之所以存在，是因为 HybridQA 只允许一个黄金答案，而事实上在某些情形下可以找到多个可能正确的答案。
- 24% 是语义解析错误。
- 10% 是 SUQL 执行错误，涉及基于 LLM 的 ANSWER 函数与 ENUM 分类器。
- 其余 2% 是类型相关的转换错误，因为 HybridQA 的表没有

[^2]: 根据与作者之一的通信。

<!-- 原 PDF 第 8 页 -->

标注类型，而 SUQL 期望有类型的模式。

总之，尽管 SUQL 在开发集上的 EM 为 59.3%，在 100 个非 Exact Match 案例中只有 36% 是真正的错误。因此，SUQL 的真实准确率可能达到 85.3%。

### 6.2 餐馆上的对话智能体

为了用真实数据集做实验，我们从 Yelp.com 收集了 4 个城市共 1828 家餐馆，以及每家餐馆排名前 20 的评论和前 20 的招牌菜。数据库的列有 name、cuisines、price、rating、num_reviews、address、phone_number、opening_hours、location、reviews 和 popular_dishes。

我们使用一个现成的稠密检索模型（Yu et al., 2022）作为 SUQL 中的检索器。本节所有系统的 LLM 都使用 gpt-3.5-turbo-0613。

#### 6.2.1 收集用户查询

我们通过 Prolific（Prolific, 2023）众包征集用户查询。我们不向工作者透露数据库中有哪些字段，以免偏置他们的查询。我们请他们想出 100 个关于餐馆的问题。另外，我们也请众包工作者与我们的对话智能体（第 4 节所述）交互，并收集了 20 段对话中的 96 个轮次。

**表 4：关于搜索问题只需要结构化数据还是需要组合数据的统计。**

|  | 单轮 | 对话 |
| --- | --- | --- |
| 仅结构化 | 45 | 37 |
| 组合 | 55 | 25 |
| 合计 | 100 | 62 |

**表 5：线性化系统与 SUQL 系统的轮次准确率。**

|  | 单轮 | 对话 |
| --- | --- | --- |
| Linearization @ 1 | 57.0% | 63.4% |
| Linearization @ 3 | 49.7% | 61.9% |
| SUQL | 93.8% | 90.3% |

真实使用场景中的餐馆设定要求用户首先指定地点，这是数据库中的一个结构化列。我们在表 4 中标注用户问题是只涉及结构化信息，还是与自由文本组合。在单轮中，收集到的用户查询全部涉及搜索餐馆。在 96 个对话轮次中，有 62 个涉及搜索餐馆。总计超过 49% 的用户查询需要同时来自结构化列与非结构化列的知识。

#### 6.2.2 轮次准确率

我们试验 Oguz et al. (2022) 针对关系表提出的线性化技术，再次使用同一个稠密检索模型（Yu et al., 2022）。具体而言，我们把同一行上的单元格值拼接起来，并用逗号分隔。这些系统根据对话历史，用少样本 LLM 为检索器抽出一条简短的搜索查询。

对每个用户输入，我们人工检查系统检索到的餐馆是否满足用户指定的全部标准，并以正确且相关的信息作出回应。具体而言，给定用户话语 $u$ 与返回的餐馆列表 $\mathcal{R} = \{r_1, r_2, \cdots, r_m\}$，我们评估每个 $r_i$ 是真阳性还是假阳性。轮次准确率计算为：数据集中所有查询的真阳性数量，除以真阳性与假阳性数量之和。

对于 SUQL 系统，查询最多返回 3 个结果。如表 5 所示，单轮问题的准确率为 93.8%，对话查询的准确率为 90.3%。

我们与两个基于线性化的系统比较，其中 $m = 1$（“Linearization 1”）与 $m = 3$（“Linearization 3”）。SUQL 提高了答案准确率，在单轮设定中最多提高 36.8%，在对话中最多提高 26.9%。这表明带有 SUQL 的对话智能体能提供准确得多的结果。

我们的系统对 100 个用户问题中的 21 个、以及对话中 62 个查询中的 8 个没有返回答案。人工检查表明，这 21 个中有 7 个、这 8 个中有 2 个确实没有答案。因此，我们的系统对用户问题和对话轮次的假阴性率分别为 14% 与 9%。

#### 6.2.3 用户反馈

我们在众包用户与餐馆聊天机器人交谈之后，用图 5 所示的三个开放问题征求反馈。总体而言，反馈是正面的：“这个聊天机器人其实没有什么我不喜欢的地方。如果它向公众开放，我真的会经常使用它”，“我喜欢这个聊天机器人回复很快，而且回复非常详细，在给出选项之后，我几乎不再有关于某家餐馆的问题

<!-- 原 PDF 第 9 页 -->

了”，以及“餐馆推荐好得让人吃惊。我甚至还要求价格更合适的，它也做到了。现在我饿了。我请它定义一种菜系风格，它也能做到”。

负面意见包括：聊天机器人偶尔较慢；“它没有提供任何链接或图片”；“它听起来并不友好，有时回复太长。分点输出会有帮助得多。”

## 7 结论

我们引入 SUQL，这是面向由结构化与非结构化数据构成的混合知识语料的第一种形式查询语言。SUQL 的关键新颖之处，是把自由文本原语纳入一种精确、简洁、富有表达力且可解释的查询语言。

把基于上下文学习的方法用于 HybridQA 数据集时，其在测试集上的 Exact Match 与 F1 分别落在以 6.2 万条数据样本训练的 SOTA 的 8.9% 与 7.1% 以内。更重要的是，与先前方法不同，我们的技术适用于大型数据库和自由文本语料。

我们在真实的 Yelp 知识库上、用众包问题与对话所做的实验表明：基于 SUQL 的上下文学习对话智能体在 90.3% 的情况下能找到满足用户全部要求的实体，而基于线性化的基线为 63.4%。这些经验结果突出了 SUQL 的适用性，以及它在生物医学、法律和金融等特定领域应用等未来研究方向上的潜力。

## 伦理考量

LLM 以及 SQL 等形式语言已被越来越多的技术开发者和日常用户使用。我们提议把二者结合起来，希望取双方之长，创造出一种有表达力、准确且高效的语言，以便在结构化与非结构化数据上进行对话式搜索。我们预计这项工作不会导致任何形式的伤害或恶意误用。

**数据。** 本工作使用的数据是一个开源研究数据集（HybridQA），以及一个基于 Yelp 的餐馆对话数据集（Restaurant）。在整理 Restaurant 数据集的过程中，我们使用经过认证的在线研究众包平台 Prolific，以确保尊重工作者的隐私并按公平标准付酬。我们的流程已获得本机构 IRB 的批准。

**计算。** 本文使用的模型是已有的预训练检索模型，以及 OpenAI 提供的 LLM API 服务。我们没有额外预训练或微调任何计算密集的模型，因此避免了这些实验中显著的碳足迹。

**许可。** 我们的代码将公开发布，并采用 Apache License, Version 2.0。我们的数据将向社区提供。

## 局限

由于基于 LLM，SUQL 可能受到 LLM 固有脆弱性的影响。这些固有弱点会负面影响 SUQL 的有效性，从而限制整个流程的表现。我们强调当前版本 SUQL 方法的两个方面的局限。

**性能局限。** 在本工作中，LLM 的语义理解能力为所解析 SUQL 查询的语义与句法正确性给出了上界。SUQL 中的 ANSWER 与 SUMMARY 功能也会受底层 LLM 影响，从而在执行 SUQL 查询时可能导致错误的过滤评估。

**可靠性局限。** 该方法的适用性也会受底层 LLM 可靠性的影响。在我们的流程中，即使被明确指示不要这样做，语义解析器仍可能以不可解释的方式幻觉出数据库内容。其他需要注意之处包括 LLM API 调用之间的非确定性行为，以及针对面向 LLM 的对抗攻击的潜在脆弱性。

## 致谢

本工作部分得到 National Science Foundation、Alfred P. Sloan Foundation、Verdant Foundation、Microsoft Azure AI credit、KDDI、JPMorgan Chase 以及 Stanford Human-Centered Artificial Intelligence (HAI) Institute 的支持。我们感谢 Gui Dávid 在项目早期对餐馆数据集所做的实验。我们也感谢 Stanford OVAL（Open Virtual Assistant Lab）的成员以及 ACL ARR 审稿人提出的宝贵意见与建议。

<!-- 原 PDF 第 10 页 -->

## 参考文献

Shengnan An, Bo Zhou, Zeqi Lin, Qiang Fu, Bei Chen, Nanning Zheng, Weizhu Chen, and Jian-Guang Lou. 2023. 面向上下文学习的基于技能的少样本选择. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pages 13472–13492, Singapore. Association for Computational Linguistics.

Jacob Andreas, John Bufe, David Burkett, Charles Chen, Josh Clausman, Jean Crawford, Kate Crim, Jordan DeLoach, Leah Dorner, Jason Eisner, Hao Fang, Alan Guo, David Hall, Kristin Hayes, Kellie Hill, Diana Ho, Wendy Iwaszuk, Smriti Jha, Dan Klein, Jayant Krishnamurthy, Theo Lanman, Percy Liang, Christopher H. Lin, Ilya Lintsbakh, Andy McGovern, Aleksandr Nisnevich, Adam Pauls, Dmitrij Petters, Brent Read, Dan Roth, Subhro Roy, Jesse Rusak, Beth Short, Div Slomin, Ben Snyder, Stephon Striplin, Yu Su, Zachary Tellman, Sam Thomson, Andrei Vorobev, Izabela Witoszko, Jason Wolfe, Abby Wray, Yuchen Zhang, and Alexander Zotov. 2020. 作为数据流合成的任务型对话. Transactions of the Association for Computational Linguistics, 8:556–571.

Aseem Arora, Shabbirhussain Bhaisaheb, Harshit Nigam, Manasi Patwardhan, Lovekesh Vig, and Gautam Shroff. 2023. 适应与分解：经由领域适应的 least-to-most 提示实现 text-to-SQL 的高效泛化. In Proceedings of the 1st GenBench Workshop on (Benchmarking) Generalisation in NLP, pages 25–47, Singapore. Association for Computational Linguistics.

Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel Ziegler, Jeffrey Wu, Clemens Winter, Chris Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. 2020. 语言模型是少样本学习者. In Advances in Neural Information Processing Systems, volume 33, pages 1877–1901. Curran Associates, Inc.

Giovanni Campagna, Sina Semnani, Ryan Kearns, Lucas Jun Koba Sato, Silei Xu, and Monica Lam. 2022. 使用精确 ThingTalk 表示的、面向 Wizard-of-Oz 对话的少样本语义解析器. In Findings of the Association for Computational Linguistics: ACL 2022, pages 4021–4034, Dublin, Ireland. Association for Computational Linguistics.

Shulin Cao, Jiaxin Shi, Zijun Yao, Xin Lv, Jifan Yu, Lei Hou, Juanzi Li, Zhiyuan Liu, and Jinghui Xiao. 2022. 用于在知识库上回答复杂问题的程序迁移. In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 8128–8140, Dublin, Ireland. Association for Computational Linguistics.

Wenhu Chen, Hanwen Zha, Zhiyu Chen, Wenhan Xiong, Hong Wang, and William Yang Wang. 2020. HybridQA：表格与文本数据上的多跳问答数据集. In Findings of the Association for Computational Linguistics: EMNLP 2020, pages 1026–1036, Online. Association for Computational Linguistics.

Jianpeng Cheng, Devang Agrawal, Héctor Martínez Alonso, Shruti Bhargava, Joris Driesen, Federico Flego, Dain Kaplan, Dimitri Kartsaklis, Lin Li, Dhivya Piraviperumal, Jason D. Williams, Hong Yu, Diarmuid Ó Séaghdha, and Anders Johannsen. 2020. 面向对话状态跟踪的对话式语义解析. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP), pages 8107–8117, Online. Association for Computational Linguistics.

Ethan A. Chi, Ashwin Paranjape, Abigail See, Caleb Chiam, Trenton Chang, Kathleen Kenealy, Swee Kiat Lim, Amelia Hardy, Chetanya Rastogi, Haojun Li, Alexander Iyabor, Yutong He, Hari Sowrirajan, Peng Qi, Kaushik Ram Sadagopan, Nguyet Minh Phu, Dilara Soylu, Jillian Tang, Avanika Narayan, Giovanni Campagna, and Christopher Manning. 2022. 神经生成遇见真人：构建一个社交的、能提供信息的开放域对话智能体. In Proceedings of the 23rd Annual Meeting of the Special Interest Group on Discourse and Dialogue, pages 376–395, Edinburgh, UK. Association for Computational Linguistics.

Edgar F Codd et al. 1972. 数据库子语言的关系完备性. IBM Corporation.

Xiang Deng, Huan Sun, Alyssa Lees, You Wu, and Cong Yu. 2022. TURL：通过表示学习进行表格理解. ACM SIGMOD Record, 51(1):33–40.

Julian Eisenschlos, Maharshi Gor, Thomas Müller, and William Cohen. 2021. MATE：提升表格 Transformer 效率的多视图注意力. In Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, pages 7606–7619, Online and Punta Cana, Dominican Republic. Association for Computational Linguistics.

Yue Feng, Zhen Han, Mingming Sun, and Ping Li. 2022. 结构化与非结构化知识上的多跳开放域问答. In Findings of the Association for Computational Linguistics: NAACL 2022, pages 151–156, Seattle, United States. Association for Computational Linguistics.

Tianyu Gao, Howard Yen, Jiatong Yu, and Danqi Chen. 2023. 使大语言模型能够生成带引用的文本. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pages 6465–6488, Singapore. Association for Computational Linguistics.

<!-- 原 PDF 第 11 页 -->

Yu Gu and Yu Su. 2022. ArcaneQA：面向知识库问答的动态程序归纳与上下文化编码. In Proceedings of the 29th International Conference on Computational Linguistics, pages 1718–1731, Gyeongju, Republic of Korea. International Committee on Computational Linguistics.

Chunxi Guo, Zhiliang Tian, Jintao Tang, Pancheng Wang, Zhihua Wen, Kang Yang, and Ting Wang. 2023. 用去语义化与骨架检索提示 GPT-3.5 做 text-to-SQL. In Pacific Rim International Conference on Artificial Intelligence, pages 262–274. Springer.

Tong Guo and Huilin Gao. 2020. 内容增强的、基于 BERT 的 text-to-SQL 生成.

Jonathan Herzig, Pawel Krzysztof Nowak, Thomas Müller, Francesco Piccinno, and Julian Eisenschlos. 2020. TaPas：通过预训练进行弱监督表格解析. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, pages 4320–4333, Online. Association for Computational Linguistics.

Yushi Hu, Chia-Hsuan Lee, Tianbao Xie, Tao Yu, Noah A. Smith, and Mari Ostendorf. 2022. 用于少样本对话状态跟踪的上下文学习. In Findings of the Association for Computational Linguistics: EMNLP 2022, pages 2627–2643, Abu Dhabi, United Arab Emirates. Association for Computational Linguistics.

Paul Hudak. 1989. 函数式程序设计语言的构想、演化与应用. ACM Comput. Surv., 21(3):359–411.

Hiroshi Iida, Dung Thai, Varun Manjunatha, and Mohit Iyyer. 2021. TABBIE：表格数据的预训练表示. In Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, pages 3446–3456, Online. Association for Computational Linguistics.

Zhengbao Jiang, Frank Xu, Luyu Gao, Zhiqing Sun, Qian Liu, Jane Dwivedi-Yu, Yiming Yang, Jamie Callan, and Graham Neubig. 2023. 主动检索增强生成. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pages 7969–7992, Singapore. Association for Computational Linguistics.

Di Jin, Seokhwan Kim, and Dilek Hakkani-Tur. 2021. 还需要进一步帮忙吗？利用非结构化知识访问改进任务型对话建模. In Proceedings of the 1st Workshop on Document-grounded Dialogue and Conversational Question Answering (DialDoc 2021), pages 119–127, Online. Association for Computational Linguistics.

Ehsan Kamalloo, Nouha Dziri, Charles Clarke, and Davood Rafiei. 2023. 大语言模型时代的开放域问答评估. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 5591–5606, Toronto, Canada. Association for Computational Linguistics.

Omar Khattab, Keshav Santhanam, Xiang Lisa Li, David Hall, Percy Liang, Christopher Potts, and Matei Zaharia. 2023. 演示—搜索—预测：为知识密集型 NLP 组合检索与语言模型.

Vishwajeet Kumar, Yash Gupta, Saneem Chemmengath, Jaydeep Sen, Soumen Chakrabarti, Samarth Bharadwaj, and Feifei Pan. 2023. 面向表格加文本问答的多行、多跨度远程监督. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 8080–8094, Toronto, Canada. Association for Computational Linguistics.

Sung-Min Lee, Eunhwan Park, Daeryong Seo, Donghyeon Jeon, Inho Kang, and Seung-Hoon Na. 2023a. MAFiD：配备移动平均的 fusion-in-decoder，用于表格与文本数据上的问答. In Findings of the Association for Computational Linguistics: EACL 2023, pages 2337–2344, Dubrovnik, Croatia. Association for Computational Linguistics.

Sung-Min Lee, Eunhwan Park, Daeryong Seo, Donghyeon Jeon, Inho Kang, and Seung-Hoon Na. 2023b. MAFiD：配备移动平均的 fusion-in-decoder，用于表格与文本数据上的问答. In Findings of the Association for Computational Linguistics: EACL 2023, pages 2337–2344, Dubrovnik, Croatia. Association for Computational Linguistics.

Fangyu Lei, Xiang Li, Yifan Wei, Shizhu He, Yiming Huang, Jun Zhao, and Kang Liu. 2023. S3HQA：面向多跳文本—表格混合问答的三阶段方法. In Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers), pages 1731–1740, Toronto, Canada. Association for Computational Linguistics.

Qi Liu, Zihuiwen Ye, Tao Yu, Linfeng Song, and Phil Blunsom. 2022. 用自对弈扩充多轮 text-to-SQL 数据集. In Findings of the Association for Computational Linguistics: EMNLP 2022, pages 5608–5620, Abu Dhabi, United Arab Emirates. Association for Computational Linguistics.

Linyong Nan, Yilun Zhao, Weijin Zou, Narutatsu Ri, Jaesung Tae, Ellen Zhang, Arman Cohan, and Dragomir Radev. 2023. 增强大语言模型的 text-to-SQL 能力：一项关于提示设计策略的研究. In Findings of the Association for Computational Linguistics: EMNLP 2023, pages 14935–14956, Singapore. Association for Computational Linguistics.

Barlas Oguz, Xilun Chen, Vladimir Karpukhin, Stan Peshterliev, Dmytro Okhonko, Michael Schlichtkrull,

<!-- 原 PDF 第 12 页 -->

Sonal Gupta, Yashar Mehdad, and Scott Yih. 2022. UniK-QA：面向开放域问答的结构化与非结构化知识之统一表示. In Findings of the Association for Computational Linguistics: NAACL 2022, pages 1535–1546, Seattle, United States. Association for Computational Linguistics.

Gabriel Poesia, Oleksandr Polozov, Vu Le, Ashish Tiwari, Gustavo Soares, Christopher Meek, and Sumit Gulwani. 2022. Synchromesh：由预训练语言模型进行可靠的代码生成.

Prolific. 2023. https://www.prolific.com. Acessed: June 2023.

Torsten Scholak, Raymond Li, Dzmitry Bahdanau, Harm de Vries, and Chris Pal. 2021. DuoRAT：走向更简单的 text-to-SQL 模型. In Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, pages 1313–1321, Online. Association for Computational Linguistics.

Sina Semnani, Violet Yao, Heidi Zhang, and Monica Lam. 2023. WikiChat：通过在 Wikipedia 上做少样本锚定来制止大语言模型聊天机器人的幻觉. In Findings of the Association for Computational Linguistics: EMNLP 2023, pages 2387–2413, Singapore. Association for Computational Linguistics.

Qi Shi, Han Cui, Haofeng Wang, Qingfu Zhu, Wanxiang Che, and Ting Liu. 2024. 通过基于程序的提示探索混合问答.

Yuan Sui, Mengyu Zhou, Mingjie Zhou, Shi Han, and Dongmei Zhang. 2023. GPT4Table：大语言模型能否理解结构化表格数据？一项基准与实证研究. Proceedings of WSDM 2024.

Haitian Sun, William W. Cohen, and Ruslan Salakhutdinov. 2022. 用于在长文档上回答复杂问题的迭代层次注意力.

Ruoxi Sun, Sercan Arik, Rajarishi Sinha, Hootan Nakhost, Hanjun Dai, Pengcheng Yin, and Tomas Pfister. 2023. SQLPrompt：用极少标注数据做上下文 text-to-SQL. In Findings of the Association for Computational Linguistics: EMNLP 2023, pages 542–550, Singapore. Association for Computational Linguistics.

Bailin Wang, Richard Shin, Xiaodong Liu, Oleksandr Polozov, and Matthew Richardson. 2020a. RAT-SQL：面向 text-to-SQL 解析器的关系感知模式编码与链接. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, pages 7567–7578, Online. Association for Computational Linguistics.

Runze Wang, Zhenhua Ling, Jing-Bo Zhou, and Yu Hu. 2020b. 跟踪多轮 text-to-SQL 语义解析中的交互状态. ArXiv, abs/2012.04995.

Yingyao Wang, Junwei Bao, Chaoqun Duan, Youzheng Wu, Xiaodong He, and Tiejun Zhao. 2022. MuGER2：面向混合问答的多粒度证据检索与推理. In Findings of the Association for Computational Linguistics: EMNLP 2022, pages 6687–6697, Abu Dhabi, United Arab Emirates. Association for Computational Linguistics.

Jian Wu, Yicheng Xu, Yan Gao, Jian-Guang Lou, Börje Karlsson, and Manabu Okumura. 2023. TACR：一种基于表格对齐的单元格选择方法，用于 HybridQA. In Findings of the Association for Computational Linguistics: ACL 2023, pages 6535–6549, Toronto, Canada. Association for Computational Linguistics.

Silei Xu, Shicheng Liu, Theo Culhane, Elizaveta Pertseva, Meng-Hsi Wu, Sina Semnani, and Monica Lam. 2023. 微调后的 LLM 知道得更多、幻觉更少：在 Wikidata 上做少样本序列到序列语义解析. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pages 5778–5791, Singapore. Association for Computational Linguistics.

Silei Xu, Sina Semnani, Giovanni Campagna, and Monica Lam. 2020. AutoQA：仅用合成训练数据，从数据库到问答语义解析器. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP), pages 422–434, Online. Association for Computational Linguistics.

Pengcheng Yin, Graham Neubig, Wen-tau Yih, and Sebastian Riedel. 2020. TaBERT：面向文本与表格数据联合理解的预训练. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, pages 8413–8426, Online. Association for Computational Linguistics.

Tao Yu, Rui Zhang, Heyang Er, Suyi Li, Eric Xue, Bo Pang, Xi Victoria Lin, Yi Chern Tan, Tianze Shi, Zihan Li, Youxuan Jiang, Michihiro Yasunaga, Sungrok Shim, Tao Chen, Alexander Fabbri, Zifan Li, Luyao Chen, Yuwen Zhang, Shreya Dixit, Vincent Zhang, Caiming Xiong, Richard Socher, Walter Lasecki, and Dragomir Radev. 2019a. CoSQL：走向跨领域数据库自然语言接口的对话式 text-to-SQL 挑战. In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP), pages 1962–1979, Hong Kong, China. Association for Computational Linguistics.

Tao Yu, Rui Zhang, Michihiro Yasunaga, Yi Chern Tan, Xi Victoria Lin, Suyi Li, Heyang Er, Irene Li, Bo Pang, Tao Chen, Emily Ji, Shreya Dixit, David Proctor, Sungrok Shim, Jonathan Kraft, Vincent Zhang, Caiming Xiong, Richard Socher, and Dragomir Radev. 2019b. SParC：上下文中的跨领域语义解析. In Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics, pages 4511–4523, Florence, Italy. Association for Computational Linguistics.

<!-- 原 PDF 第 13 页 -->

Yue Yu, Chenyan Xiong, Si Sun, Chao Zhang, and Arnold Overwijk. 2022. COCO-DR：用对比学习与分布鲁棒学习对抗零样本稠密检索中的分布偏移. In Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing, pages 1462–1479, Abu Dhabi, United Arab Emirates. Association for Computational Linguistics.

Tianshu Zhang, Xiang Yue, Yifei Li, and Huan Sun. 2023a. TableLlama：走向开放的大型表格通才模型.

Yunjia Zhang, Jordan Henkel, Avrilia Floratou, Joyce Cahoon, Shaleen Deep, and Jignesh M. Patel. 2023b. ReAcTable：增强 ReAct 以做表格问答.

Chao Zhao, Spandana Gella, Seokhwan Kim, Di Jin, Devamanyu Hazarika, Alexandros Papangelis, Behnam Hedayatnia, Mahdi Namazifar, Yang Liu, and Dilek Hakkani-Tur. 2023. “别人怎么想？”：带有主观知识的任务型对话建模. In Proceedings of the 24th Annual Meeting of the Special Interest Group on Discourse and Dialogue, pages 309–323, Prague, Czechia. Association for Computational Linguistics.

Victor Zhong, Caiming Xiong, and Richard Socher. 2017. Seq2SQL：用强化学习从自然语言生成结构化查询.

## 附录

### A.1 超参数

在我们的全部实验中，调用 OpenAI 的 LLM 时温度设为 0，并直接使用 Yu et al. (2022) 提供的检索器及其默认参数。

### A.2 实验中的提示词

我们给出本文提到的提示词。所用语法是 Jinja2 模板语言，它支持类 Python 的循环（`{% for %}{% endfor %}`）、条件（`{% if %}{% endif %}`）、变量（`{{ var }}`）和注释（`{# #}`）。

### A.3 我们在 Prolific 上的众包流程

我们利用 Prolific（Prolific, 2023）整理 Restaurant 数据集。众包界面见图 3。开始众包任务后，众包工作者会看到图 4 所示的问题。他们与聊天机器人交谈结束后，会看到图 5 所示的三个问题。

在同意透露人口统计信息的 50 名众包工作者中，33 名女性、17 名男性。全部 50 名众包工作者居住在美国。我们按每小时 12.30 美元向众包工作者付酬。预期平均时长为 8 分钟。该报酬高于美国联邦最低工资，即每小时 7.25 美元。我们的众包流程征求了用户同意，将其与聊天机器人的对话用于研究。没有收集个人可识别信息。

<!-- 原 PDF 第 14 页 -->

**图 2：同时含有结构化与非结构化数据的 restaurants 表。**

| Name（Text） | Cuisines（Enum[]） | Rating（Num(2,1)） | … | Popular_dishes（Free Text[]） | Reviews（Free Text[]） |
| --- | --- | --- | --- | --- | --- |
| Hummus Mediterranean Kitchen | mediterranean, halal, salad | 4.0 | … | Chicken Kebab Plate, Lamb Beef Gyro, Marinated Chicken Gyros, ... | \| t l ; d r \| This is your place if you're looking for a healthy and filling meal whether it's a quick pick-me-up or casual dining, ...（如果你在找一顿健康又管饱的饭，无论是快速补能量还是休闲用餐，这里就是你的地方，……） |
| Penny Roma | italian, venues & event spaces | 4.0 | … | Cacio E Pepe, Agnolotti Dal Plin, Albacore Tartare, ... | My girlfriend was craving pasta on a Monday night. ... We were not expecting such an intimate and romantic dining experience. The restaurant was candle lit, modern, and perfect for a date night. ...（我女朋友在一个周一晚上很想吃意大利面。……我们没料到用餐体验会如此亲密而浪漫。餐馆点着蜡烛，风格现代，非常适合约会之夜。……） |

**表 6：SUQL 编译器中使用的 ENUM 分类器提示词。这是一个零样本提示词。**

在数据库中，`{{ field_name }}` 字段有下面这一组选项，以换行分隔。“`{{ predicted_field_value }}`”不是可能的选项之一。你需要把“`{{ predicted_field_value }}`”分类到下面的一个或多个取值之中：

```text
{% for choice in field_value_choices %}
{{ choice }}
{% endfor %}
```

你只能从上述选项中选择。你的回答应当是一个由逗号分隔的索引数字列表。

你的答案：

**表 7：SUQL 编译器中使用的 ANSWER 函数提示词。这是一个零样本提示词。**

根据下列文本回答一个问题。`{{ type_prompt }}`

问题：`{{ question }}`。如果没有信息，就说 “no info”。

文档：

```text
{% for review in reviews %}
{{ review }}
{% endfor %}
```

用几个词给出简洁答案：

**表 8：SUQL 编译器中把 ANSWER 函数用作过滤器时的提示词。这是一个零样本提示词。**

`answer(document, query)` 接收一个文档和一个查询。它针对 `document` 询问 `query`，并输出答案。

现在来看这个用例。你的任务是判断输出是否正确。

```text
answer({{ field }}, "{{ query }}") {{ operator }} {{ value }}
{{ field }} = ["{{ document }}"]
```

从下列选项中选择一个：

- 输出是正确的。
- 输出是不正确的。

<!-- 原 PDF 第 15 页 -->

**表 9：HybridQA 语义解析器提示词。该提示词包含 10 个示例，每个示例有（1）简短的表描述，（2）以 CREATE 命令给出的表模式，（3）输入查询，以及（4）目标 SUQL。**

你是一个语义解析器。为具有给定签名的数据库生成一条查询。不要生成给定字段之外的字段。

——

`1929_International_Cross_Country_Championships_0`

```sql
CREATE TABLE validation_table_7 ("Rank" INT, "Athlete" TEXT, "Athlete_Info" TEXT[], "Nationality" TEXT, "Nationality_Info" TEXT[], "Time" TEXT);
```

用户：西班牙的 José Reliegos 与出生于 1892 年 9 月 5 日、参加了 1928 年奥运会的那个人，两人的时间差是多少？

目标：

```sql
SELECT a."Time"::INTERVAL - b."Time"::INTERVAL FROM "validation_table_7" a, "validation_table_7" b WHERE a."Athlete" = 'José Reliegos' AND a."Nationality" = 'Spain' AND answer(b."Athlete_Info", 'is this athlete born 5 September 1892?') = 'Yes';
```

——

`List_of_cities_in_Somalia_by_population_0`

```sql
CREATE TABLE validation_table_8 ("Rank" INT, "City" TEXT, "City_Info" TEXT[], "Region" TEXT, "Region_Info" TEXT[], "Population" INT);
```

用户：拥有 55 万居民的那座索马里人的城市北面是哪个海湾？

目标：

```sql
SELECT answer("City_Info", 'Which gulf is north of this Somalian''s city ?') FROM "validation_table_8" WHERE "Population" = '550,000';
```

——

`List_of_the_mothers_of_the_Ottoman_Sultans_0`

```sql
CREATE TABLE validation_table_14 ("Name" TEXT, "Name_Info" TEXT[], "Titles" TEXT, "Titles_Info" TEXT[], "Maiden Name" TEXT, "Origin" TEXT, "Origin_Info" TEXT[], "Death" DATE, "Son ( s )" TEXT, "Son ( s )_Info" TEXT[]);
```

用户：奥斯曼苏丹 Suleiman I 的母亲的丈夫是谁？

目标：

```sql
SELECT answer("Name_Info", 'Who is her husband?') FROM "validation_table_14" WHERE "Son ( s )" = 'Suleiman I';
```

——

`List_of_Mohun_Bagan_A.C._managers_0`

```sql
CREATE TABLE validation_table_10 ("Name" TEXT, "Name_Info" TEXT[], "Nationality" TEXT, "Nationality_Info" TEXT[], "FROM" DATE, "TO" DATE);
```

用户：出生于 1968 年 2 月 15 日的那位主教练是什么国籍？

目标：

```sql
SELECT "Nationality" FROM "validation_table_10" WHERE answer("Name_Info", 'is this manager born on 15 February 1968?') = 'Yes';
```

——

`Grammy_Award_for_Best_Jazz_Vocal_Performance,_Male_0`

```sql
CREATE TABLE "validation_table_2615" ("Year" INT, "Year_Info" TEXT[], "Performing artist ( s )" TEXT, "Performing artist ( s )_Info" TEXT[], "Work" TEXT, "Work_Info" TEXT[], "Nominees" TEXT, "Nominees_Info" TEXT[])
```

用户：最近一首获奖歌曲上有多少人表演？

目标：

```sql
SELECT answer("Work_Info", 'how many people performed on this song?') FROM "validation_table_2615" ORDER BY "Year" DESC LIMIT 1;
```

——

`List_of_flag_bearers_for_Myanmar_at_the_Olympics_0`

```sql
CREATE TABLE validation_table_67 ("Name" TEXT, "Event Year" INT, "Year_Info" TEXT[], "Season" TEXT, "Flag Bearer" TEXT, "Flag Bearer_Info" TEXT[]);
```

用户：最年轻的缅甸旗手于何时参加奥运会开幕式？

目标：

```sql
SELECT "Event Year" FROM validation_table_67 ORDER BY answer("Flag Bearer_Info", 'when is this person born?')::date DESC LIMIT 1;
```

——

`List_of_museums_in_Atlanta_0`

```sql
CREATE TABLE validation_table_3 ("Name" TEXT, "Name_Info" TEXT[], "Area" TEXT, "Area_Info" TEXT[], "Type" TEXT, "Summary" TEXT, "Summary_Info" TEXT[]);
```

用户：位于一座维多利亚式房屋中的那座博物馆的地址是什么？其所在地区区域内的建筑风格包括 Craftsman Bungalow、Queen Anne、Stick style、Folk Victorian、Colonial Revival、American Foursquare 和 Neoclassical Revival。

目标：

```sql
SELECT answer("Name_Info", 'what is the address?') FROM "validation_table_19" WHERE answer("Area_Info", 'is this an area whose Architectural styles within the district include Craftsman Bungalow , Queen Anne , Stick style , Folk Victorian , Colonial Revival , American Foursquare and Neoclassical Revival ?') = 'Yes';
```

——

`2007_in_Canadian_music_0`

```sql
CREATE TABLE "validation_table_26" ("Rank" INT, "Artist" TEXT, "Artist_Info" TEXT[], "Album" TEXT, "Album_Info" TEXT[], "Peak position" INT, "Sales" INT, "Certification" TEXT)
```

用户：拥有专辑 *Call Me Irresponsible* 的那位音乐人，其专辑购买量有多少？

目标：

```sql
SELECT answer("Artist_Info", 'How many albums has this artist sold?') FROM "validation_table_26" WHERE answer("Album_Info", 'is this record Call Me Irresponsible?') = 'Yes';
```

——

`List_of_Indian_state_flowers_0`

```sql
CREATE TABLE "validation_table_74" ("State" TEXT, "State_Info" TEXT[], "Common name" TEXT, "Common name_Info" TEXT[], "Binomial name" TEXT, "Binomial name_Info" TEXT[])
```

用户：按面积最小的那个邦的邦花是什么？

目标：

```sql
SELECT "Common name" FROM "validation_table_74" WHERE answer("State_Info", 'is this the smallest state by area?') = 'Yes';
```

——

`List_of_Turner_Prize_winners_and_nominees_0`

```sql
CREATE TABLE "validation_table_78" ("Year" INT, "Winner" TEXT, "Winner_Info" TEXT[], "Format" TEXT, "Nominees" TEXT, "Nominees_Info" TEXT[], "Notes" TEXT, "Notes_Info" TEXT[])
```

用户：1999 年 Turner Prize 得主因其电影 *12 Years a Slave* 在哪一年获得 Academy Award？

目标：

```sql
SELECT answer("Winner_Info", 'in what year did he win the Academy Award for his film, 12 Years a Slave?') FROM "validation_table_78" WHERE answer("Winner_Info", 'did he win the Academy Award for his film, 12 Years a Slave?') = 'Yes' AND "Year" = '1999';
```

——

```text
{{ table_original_name }}
{{ create_cmd }}
用户：{{ query }}
目标：
```

<!-- 原 PDF 第 16 页 -->

**表 10：HybridQA 无结果恢复提示词。该提示词包含 5 个示例，每个示例有（1）简短的表描述，（2）以 CREATE 命令给出的表模式，（3）输入查询，（4）一条此前生成、但没有返回结果的 SUQL，以及（5）目标 SUQL。**

你是一个 SQL 语义解析器。在先前一轮中，你预测了一条 SQL，它没有返回结果。你现在的工作是生成一条新的 SQL 再试一次。

除标准 SQL 语法外，你可以使用 `answer` 函数。

一般而言，你应当尝试放宽（RELAX）约束。

——

表描述：`Doping_at_the_Olympic_Games_15`

模式：

```sql
CREATE TABLE "validation_table_56" ("Name" TEXT, "Name_Info" TEXT[], "Country" TEXT, "Country_Info" TEXT[], "Sport" TEXT, "Sport_Info" TEXT[], "Banned substance" TEXT, "Banned substance_Info" TEXT[])
```

问题：出生于 Bugulma、在 2002 年被禁赛的那位运动员，是因为使用什么物质？

此前生成的 SQL：

```sql
SELECT "Banned substance" FROM "validation_table_56" WHERE answer("Name_Info", 'is this athlete born in Bugulma?') = 'Yes' AND "Country_Info" @> ARRAY['2002'];
```

这条 SQL 没有返回结果。

新 SQL：

```sql
SELECT "Banned substance" FROM "validation_table_56" WHERE answer("Name_Info", 'is this athlete born in Bugulma and banned in 2002?') = 'Yes';
```

——

表描述：`Sweden_at_the_1932_Summer_Olympics_0`

模式：

```sql
CREATE TABLE "validation_table_1" ("Medal" TEXT, "Name" TEXT, "Name_Info" TEXT[], "Sport" TEXT, "Sport_Info" TEXT[], "Event" TEXT, "Event_Info" TEXT[])
```

问题：1932 年夏季奥运会男子重量级古典式摔跤项目金牌得主的绰号是什么？

此前生成的 SQL：

```sql
SELECT answer("Name_Info", 'What was his nickname?') FROM "validation_table_1" WHERE "Medal" = 'Gold' AND "Event" = 'Men''s heavyweight Greco-Roman wrestling';
```

这条 SQL 没有返回结果。

新 SQL：

```sql
SELECT answer("Name_Info", 'What was his nickname?') FROM "validation_table_1" WHERE "Medal" = 'Gold' AND "Event" = 'Men''s heavyweight' AND "Sport" = 'Greco-Roman wrestling';
```

——

表描述：`2011_Berlin_Marathon_0`

模式：

```sql
CREATE TABLE "validation_table_4" ("Position" INT, "Athlete" TEXT, "Athlete_Info" TEXT[], "Nationality" TEXT, "Nationality_Info" TEXT[], "Time" TIME)
```

问题：2011 年以 2:13.32 完成柏林马拉松、且那是他第一次参加马拉松的人取得了第几名？

此前生成的 SQL：

```sql
SELECT "Position" FROM "validation_table_4" WHERE "Time" = '2:13:32' AND answer("Athlete_Info", 'is this the first time this person competed in a marathon?') = 'Yes';
```

这条 SQL 没有返回结果。

新 SQL：

```sql
SELECT "Position" FROM "validation_table_4" WHERE "Time" = '2:13:32';
```

——

表描述：`List_of_Pi_Kappa_Alpha_brothers_5`

模式：

```sql
CREATE TABLE "validation_table_37" ("Name" TEXT, "Name_Info" TEXT[], "Original chapter" TEXT, "Original chapter_Info" TEXT[], "Notability" TEXT, "Notability_Info" TEXT[])
```

问题：来自 Beta Omicron 的那位兄弟出生于哪一年？

此前生成的 SQL：

```sql
SELECT answer("Name_Info", 'what year was this brother born?') FROM "validation_table_37" WHERE "Original chapter" = 'Beta Omicron';
```

这条 SQL 没有返回结果。

新 SQL：

```sql
SELECT answer("Name_Info", 'what year was this person born?') FROM "validation_table_37" WHERE "Original chapter" = 'Beta Omicron';
```

——

表描述：`List_of_radio_stations_in_the_United_Kingdom_15`

模式：

```sql
CREATE TABLE "validation_table_55" ("Name" TEXT, "Name_Info" TEXT[], "Licence area" TEXT, "Licence area_Info" TEXT[], "Analogue frequencies" FLOAT, "Notes" TEXT)"
```

问题：哪家电台向坐落于 River Yeo 河畔、位于多塞特西北部的一个民政教区广播？

此前生成的 SQL：

```sql
SELECT "Name" FROM "validation_table_55" WHERE answer("Licence area_Info", 'does this station broadcast to a civil parish in north west Dorset sited on the River Yeo?') = 'Yes';
```

这条 SQL 没有返回结果。

新 SQL：

```sql
SELECT "Name" FROM "validation_table_55" WHERE answer("Licence area_Info", 'is this a civil parish in north west Dorset sited on the River Yeo?') = 'Yes';
```

——

```text
表描述：{{ description }}
模式：{{ schema }}
问题：{{ question }}
此前生成的 SQL：{{ previous_sql }}
这条 SQL 没有返回结果。
{% if second_previous_sql is not none %}
你还生成了：{{ second_previous_sql }}
这条 SQL 也没有返回结果。
{% endif %}
新 SQL：
```

<!-- 原 PDF 第 17 页 -->

**表 11：HybridQA 格式抽取提示词。该提示词包含 6 个示例，每个示例有（1）输入查询，（2）来自 SUQL 的详细答案，以及（3）目标简短答案。**

你是一个好的答案抽取器。给定某个问题的详细答案，你总是抽出一个简短答案。如果抽不出有效答案，就回答 “No Info”。不要生成并非来自原始详细答案的答案。简短答案应当是文段中不加修改的最小片段。抄写答案时，不要使用半个词。

——

问题：在 2004 年 United States Grand Prix 中以第 4 名完赛的车手是什么国籍？

详细答案：这位车手 Jenson Alexander Lyons Button 是英国人。

简短答案：British

——

问题：位于一座维多利亚式房屋中的那座博物馆的地址是什么？其所在地区区域内的建筑风格包括 Craftsman Bungalow、Queen Anne、Stick style、Folk Victorian、Colonial Revival、American Foursquare 和 Neoclassical Revival。

详细答案：Hammonds House Museum 的地址是佐治亚州亚特兰大 West End 街区的 503 Peeples Street SW。

简短答案：503 Peeples Street SW

——

问题：地形极其崎岖、由砂岩峰、狭窄峡谷、沟壑和密林构成的那座国家公园，面积是多少公里？

详细答案：524 km

简短答案：524

——

问题：拥有 55 万居民的那座索马里城市北面是哪个海湾？

详细答案：亚丁湾位于这座城市的北面。

简短答案：Gulf of Aden

——

问题：奥斯曼苏丹 Suleiman I 的母亲的丈夫是谁？

详细答案：她的丈夫是 Selim I。

简短答案：Selim I

——

问题：他 2009 年那部电影里，片名所指综合征的症状是什么？

详细答案：文本没有提供任何综合征的症状信息。

简短答案：No Info

——

```text
问题：{{ query }}
详细答案：{{ detailed_answer }}
简短答案：
```

<!-- 原 PDF 第 18 页 -->

**表 12：餐馆实验的输入分类器提示词。该提示词包含 8 个示例。**

你是一个正在与用户聊天的餐馆虚拟助手。

你可以访问一个餐馆数据库，检索餐馆的菜系、价格（cheap、moderate、expensive、luxury）、评分（1–5）、num_reviews、location、popular_dishes、reviews、phone_number 和 opening_hours。

=====

`{# basic #}`

你：你好！我能帮你什么？

对方：芝加哥哪里适合吃早午餐？

[要查数据库吗？是]

=====

`{# ask for rating #}`

对方：给我看纽约上东区的一家中餐馆

你：我找到了 4.5 星的 Calle Dao Chelsea。它是一家中餐与亚洲融合餐馆，供应早午餐，菜单反映了华人迁往古巴的历史。

对方：它比 Panda Express 更好吗？

[要查数据库吗？是]

=====

`{# follow up on phone number #}`

对方：西雅图有什么好的海鲜餐馆？

你：我找到了 The Pink Door，西雅图一家 4.5 星海鲜餐馆。评论提到那里供应烤全鱼和蛤蜊意面等海鲜菜。

对方：你能找到他们的电话号码吗？

[要查数据库吗？是]

=====

`{# have you heard? #}`

对方：你听说过芝加哥的 Girl and the Goat 吗？

[要查数据库吗？是]

=====

`{# do not check db when asking about general knowledge #}`

对方：我想在堪萨斯城找一家西班牙餐馆

你：我找到了 4 星的 La Bodega。它有城里最好的欢乐时光之一，氛围舒适，让人觉得置身西班牙乡村。

对方：你会说西班牙语吗？

[要查数据库吗？否]

=====

`{# do not check db when asking about general knowledge about dishes #}`

对方：能帮我找一家供应北京烤鸭的地方吗？

你：抱歉，我没有这个信息。

对方：那橙汁鸡呢？

你：抱歉，我没有这个信息。

对方：那鸡肉呢？

你：我找到了 4 星的 Roost & Roast。它是一家外带店，没有室内用餐，但外面有桌子。菜单简单，通过 iPad 自助点餐机下单。他们提供受泰国启发的菜，例如 Hat Yai Fried Chicken、Pad Thai，以及其他几种炒菜。

对方：什么是 Hat Yai fried chicken？

[要查数据库吗？否]

=====

`{# show another one #}`

对方：嘿！给我看华盛顿特区的某家店。

你：我找到了 4 星的 Old Ebbitt Grill。它是位于华盛顿特区的一家历史餐馆，自 1856 年起为本地人和游客供餐。食物很好，服务很棒，员工友好且了解情况。

对方：还有另一家吗？

[要查数据库吗？是]

=====

`{# keep on checking database even if there are errors #}`

对方：你听说过芝加哥的 Girl and the Goat 吗？

你：抱歉。我没有这个信息

对方：你听说过芝加哥的 Girl and the Goat 吗？

[要查数据库吗？是]

=====

你：你好！我能帮你什么？

```text
{% for dlg_turn in dlg %}
对方：{{ dlg_turn.user_utterance }}
{% if dlg_turn.agent_utterance is not none %}
你：{{ dlg_turn.agent_utterance }}
{% endif %}
{% endfor %}
[要查数据库吗？
```

<!-- 原 PDF 第 19 页 -->

**表 13：餐馆实验的语义解析器提示词。该提示词包含 8 个示例。**

你是一个语义解析器。为具有如下签名的餐馆数据库生成一条查询：

```sql
CREATE TABLE restaurants (
name TEXT,
cuisines TEXT[],
price ENUM ('cheap', 'moderate', 'expensive', 'luxury'),
rating NUMERIC(2,1),
num_reviews NUMBER,
address TEXT,
popular_dishes FREE_TEXT,
phone_number TEXT,
reviews FREE_TEXT,
opening_hours TEXT,
location TEXT
);
```

不要生成给定字段之外的字段。`answer` 函数可以用在 FREE_TEXT 字段上。

`{# Basic example #}`

用户：Burguer King 在哪里？

目标：

```sql
SELECT address, summary(reviews) FROM restaurants WHERE name ILIKE '%Burguer King%' LIMIT 1;
```

——

`{# Basic example for cuisine, and follow up with restaurant names #}`

用户：堪萨斯城有哪些评价不错的日本餐馆？

目标：

```sql
SELECT *, summary(reviews) FROM restaurants WHERE 'japanese' = ANY (cuisines) AND location = 'Kansas City' AND rating >= 4.0 LIMIT 3;
```

智能体：我找到了 Sakura Sushi、Nami Ramen 和 Kaze Teppanyaki。

用户：它们的价格是多少？

目标：

```sql
SELECT name, price FROM restaurants WHERE (name ILIKE 'Sakura Sushi' OR name ILIKE 'Nami Ramen' OR name ILIKE 'Kaze Teppanyaki') AND location = 'Kansas City';
```

——

`{# Usage of ‘answer‘ function on FREE TEXT field in both projection and filter #}`

用户：给我看华盛顿特区一家适合家庭、并且有汉堡的餐馆。

目标：

```sql
SELECT *, summary(reviews), answer(reviews, 'is this restaurant family-friendly?') FROM restaurants WHERE answer(reviews, 'do you find this restaurant to be family-friendly?') = 'Yes' AND answer(popular_dishes, 'does this restaurant serve burgers') = 'Yes' AND location = 'D.C.' LIMIT 1;
```

智能体：我找到了 Jason's steakhouse。评论提到孩子们喜欢和父母一起去那里。它应当很适合你和家人的周末晚餐。

用户：评论怎么说这家餐馆的氛围？

目标：

```sql
SELECT answer(reviews, 'What is the atmosphere?') FROM restaurants WHERE name ILIKE 'Jason''s steakhouse' AND location = 'D.C.' LIMIT 1;
```

——

`{# Usage of ‘answer‘ function on popular_dishes #}`

用户：在纳什维尔给我找一家有意大利面的地方。

目标：

```sql
SELECT *, summary(reviews) FROM restaurants WHERE answer(popular_dishes, 'does this restaurant serve pasta') = 'Yes' AND location = 'Nashville' LIMIT 1;
```

——

`{# Usage of ‘answer‘ function on reviews #}`

用户：我喜欢中国菜。给我找一家等待时间不长的餐馆。

目标：

```sql
SELECT *, summary(reviews), answer(reviews, 'what is the wait time?') FROM restaurants WHERE 'chinese' = ANY (cuisines) AND answer(reviews, 'does this restaurant have short wait time?') = 'Yes' LIMIT 1;
```

——

`{# Meaning of the word "popular", and follow up on fetching reviews #}`

用户：我想在加州纳帕找一家受欢迎的餐馆。

目标：

```sql
SELECT *, summary(reviews) FROM restaurants WHERE rating >= 4.5 AND location = 'Napa, CA' ORDER BY num_reviews DESC LIMIT 1;
```

智能体：我找到了 5.0 星的 Gui's vegan house。它有 2,654 条评论，评论提到氛围很好、服务又快又好，以及食物质量好。

用户：把谈到食物质量好的那条评论给我。

目标：

```sql
SELECT single_review FROM restaurants AS r, unnest(reviews) AS single_review WHERE name ILIKE 'Gui''s vegan house' AND answer(single_review, 'does this review mention good food quality?') = 'Yes' AND r.location = 'Napa, CA' LIMIT 1;
```

——

`{# Usage of ‘answer‘ function on reviews #}`

用户：贝克斯菲尔德哪些餐馆有欢乐时光？

目标：

```sql
SELECT *, summary(reviews), answer(reviews, 'what is the happy hour here?') FROM restaurants WHERE location = 'Bakersfield' AND answer(reviews, 'does this restaurant have a happy hour?') = 'Yes' LIMIT 1;
```

——

`{# Usage of ‘answer‘ function on reviews #}`

用户：我饿了，午饭吃什么？我想在芝加哥找三文鱼。

目标：

```sql
SELECT *, summary(reviews) FROM restaurants WHERE answer(popular_dishes, 'does this restaurant serve salmon?') = 'Yes' AND location = 'Chicago' LIMIT 1;
```

智能体：我找到了 4.5 星的 Daigo。它是一家家族经营的店，供应传统日本料理。

用户：再给我看一家。

目标：

```sql
SELECT *, summary(reviews) FROM restaurants WHERE NOT(name = 'Daigo') AND answer(popular_dishes, 'does this restaurant serve salmon?') = 'Yes' AND location = 'Chicago' LIMIT 1;
```

——

```text
{% for dlg_turn in dlg[:-1] %}
{% if dlg_turn.genie_utterance is not none %}
用户：{{ dlg_turn.user_utterance }}
目标：{{ dlg_turn.user_target }}
智能体：{{ dlg_turn.agent_utterance }}
{% endif %}
{% endfor %}
用户：{{ query }}
目标：
```

<!-- 原 PDF 第 20 页 -->

**图 3：用户看到的众包界面**

界面标题：与一个餐馆聊天机器人交谈并评价它。

报酬与时长标记：$1.64–$12.30/hr，8 分钟，5 个名额。

设想你正在访问 Palo Alto，并且在找餐馆。在这项研究中，你将与一个聊天机器人交谈，以便在那里找餐馆。对话结束后，你需要回答 3 个关于你与该聊天机器人总体体验的问题。

你可以用来参加这项研究的设备：Desktop、Mobile、Tablet。

按钮：在新窗口中打开研究链接。

**图 4：我们在众包工作者开始与聊天机器人交谈之前给他们的提示。**

标题：与一个餐馆聊天机器人交谈并评价它。

设想你正在访问 Palo Alto，并且在找餐馆。在这项研究中，你将与一个聊天机器人交谈，以便在那里找餐馆。对话结束后，你需要回答 3 个关于你与该聊天机器人总体体验的问题。

例如，下面是一些你可以怎样开始这段对话的例子：

1. 嘿！我要带家人去 Palo Alto，我们可以去哪些中餐馆？
2. 给我推荐 Palo Alto 一家浪漫的意大利餐馆。我想带女朋友去那里。
3. 请帮我在 Palo Alto 找一家方便残障人士的餐馆。
4. 嗨！请帮我在 Palo Alto 找一家卖汉堡的四星餐馆。
5. Palo Alto 有没有评价不错、并且有午餐特价的韩国餐馆？他们有什么菜？

未分享。

\* 表示必答题。

请在这里复制粘贴你的 Prolific ID \*

你的答案

现在，与聊天机器人交谈，以便在 Palo Alto 找一家餐馆，至少 5 个轮次。\*

记住在对话中包含 “Palo Alto”。

开始时，点击这个链接。完成后，请输入 “FINISHED”（全部大写）以收到一个对话 ID，并把它粘贴到这里。

<!-- 原 PDF 第 21 页 -->

**图 5：众包工作者与聊天机器人交谈结束后被问到的问题。**

未命名部分（Untitled Section）

用几句话写下你喜欢这个聊天机器人的哪些地方。\*

你的答案

用几句话写下你不喜欢这个聊天机器人的哪些地方。\*

你的答案

使用这个聊天机器人时你是否遇到任何问题？如果有，请详细说明。\*

你的答案

<!-- 译完 -->
