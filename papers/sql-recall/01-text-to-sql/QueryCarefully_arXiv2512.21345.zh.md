原文件名：QueryCarefully_arXiv2512.21345.pdf

原标题：Query Carefully: Detecting the Unanswerables in Text-to-SQL Tasks

中文标题：谨慎查询：检测 Text-to-SQL 任务中的不可回答问题

作者：Jasmin Saxer；Isabella Maria Aigner；Luise Linzmeier；Andreas Weiler；Kurt Stockinger

arXiv:2512.21345v1 [cs.DB] 19 Dec 2025

<!-- 原 PDF 第 1 页 -->

Query Carefully: Detecting the Unanswerables in Text-to-SQL Tasks

Jasmin Saxer¹，Isabella Maria Aigner²，Luise Linzmeier³，Andreas Weiler¹，Kurt Stockinger¹

¹ 计算机科学研究所，苏黎世应用科学大学（Zurich University of Applied Sciences），Technikumstrasse 9, 8401 Winterthur, Switzerland

² 医学病毒学研究所，苏黎世大学（University of Zurich），8057 Zurich, Switzerland

³ 胃肠病学与肝病学系，苏黎世大学医院（University Hospital Zurich），苏黎世大学（University of Zurich），8091 Zurich, Switzerland

**摘要。** Text-to-SQL 系统使并非 SQL 专家的人也能用自然语言与关系数据库交互。然而，这类系统倾向于为含糊、超出范围或不可回答的查询生成可执行的 SQL。由此带来一种隐蔽风险：输出可能被误认为是正确的。这一风险在生物医学场景中尤为严重，因为精度至关重要。因此，我们提出 Query Carefully。这是一条流水线，把基于大语言模型的 SQL 生成，与对不可回答输入的显式检测和处理结合在一起。我们在 ScienceBenchmark 的 OncoMX 部分之上，构建了 OncoMX-NAQ（No-Answer Questions，无答案问题）。其中包含 80 个无答案问题，覆盖 8 个类别（非 SQL、模式外/领域外，以及多种歧义类型）。我们的方法使用 llama3.3:70b，配合模式感知的提示、显式的无答案规则（No-Answer Rules, NAR），以及同时取自可回答问题与不可回答问题的少样本示例。我们评估 SQL 精确匹配、结果准确率，以及不可回答检测准确率。在 OncoMX 的 dev 划分上，使用可回答示例的少样本提示提高了结果准确率；再加入不可回答示例，性能并未下降。在 OncoMX-NAQ 上，平衡提示取得最高的不可回答检测准确率（0.8）：对结构上可界定的类别（非 SQL、缺失列、领域外）接近完美，但对缺失值查询（0.5）和列歧义（0.3）仍然困难。一个轻量的用户界面会呈现中间 SQL、执行结果和弃权，从而支持生物医学应用中透明、可靠的 text-to-SQL。

**关键词：** text-to-SQL · 不可回答问题检测 · OncoMX。

## 1 引言

关系数据库是在众多领域中管理并查询结构化数据的基本工具，医疗与科学研究都包括在内。这些系统通常要求用户使用领域特定的编程语言来表述查询，例如 SQL（Structured Query Language）。这会

arXiv:2512.21345v1 [cs.DB] 19 Dec 2025

<!-- 原 PDF 第 2 页 -->

构成显著障碍，并使存储在关系数据库中的知识只限于数据库专家能够获取。

自然语言到 SQL（text-to-SQL）系统试图弥合这一差距：把自然语言问题翻译成可执行的 SQL 查询，使用户能够用日常语言与数据库交互，而不必具备查询语言方面的专门知识 [5]。深度学习模型的进展，尤其是基于大语言模型（Large Language Models, LLM）的方法，已经使 text-to-SQL 在 Spider 这类简单基准数据集上有了显著提升。这类数据集提供成对标注的自然语言问题及其对应的 SQL 查询 [6, 9]。

尽管具有潜力，text-to-SQL 仍然是一项困难的任务，在医疗这类敏感领域中尤其如此，因为错误可能给患者带来严重后果。三个关键挑战包括：

- 在大规模、领域专一的关系数据库上，为复杂问题生成准确且语义正确的查询。[7]
- 避免输出具有误导性或不正确的 SQL 语句。[7]
- 处理含糊、不完整或不可回答的用户查询 [11]。

本文聚焦第三个挑战：识别不可回答的问题。text-to-SQL 系统的真实用户通常并不是数据库专家。因此，他们可能会提出含糊的问题，提及模式中并不存在的元素，或者提出落在数据库领域之外的问题。面对这类问题，基于 LLM 的 text-to-SQL 系统仍可能尝试生成 SQL 查询，从而产生不正确的输出或误导性的结果。因此，text-to-SQL 系统必须能够检测不可回答的问题，并作出恰当回应，例如返回“不可回答”的信息，或请求澄清。检测不可回答的问题，不仅有助于防止错误结果，也能揭示系统的局限，从而提升真实应用中 text-to-SQL 界面的稳健性与可靠性 [1, 8, 11, 12]。

在本文中，我们应对这一挑战的方式是：扩展已有的 text-to-SQL 数据集（ScienceBenchmark [10]），基于收录癌症生物标志物信息的生物医学数据库 OncoMX，补充不可回答的问题。随后，我们提出一条流水线，把基于 LLM 的 SQL 生成，与检测并处理不可回答输入的机制结合起来，并通过直观的对话式界面来实现。

## 2 相关工作

本项目基于 ScienceBenchmark 数据集。该数据集为三个复杂、领域专一的数据库提供了已标注的问题–SQL 对：科研政策制定（CORDIS）、天体物理学（SDSS），以及癌症研究（OncoMX）[10]。我们特别关注 OncoMX 数据库⁴，因为它的生物医学信息与术语高度专域。本文使用的 OncoMX 版本

⁴ https://www.oncomx.org/

<!-- 原 PDF 第 3 页 -->

在 ScienceBenchmark 中包含 25 张表，每张表有 2 至 14 列，共计 106 列，平均每张表 2,636,771 行。OncoMX 由美国国立卫生研究院（U.S. National Institutes of Health, NIH）资助，整合了多个来源关于癌症生物标志物、癌症样本中差异基因表达以及已知癌症突变的数据。因此，它与 ScienceBenchmark 中的问题–SQL 对相结合，成为面向真实生物医学 text-to-SQL 应用的理想测试数据库。

现有的 text-to-SQL 研究大多假定：用户查询在给定模式之内是有效且可回答的。很少有研究处理检测不可回答或含糊的用户问题这一关键问题。

Zhang 等人 [11] 提出了 TriageSQL。这是一个基准，把用户问题分为五种意图类型，其中包含四类不可回答查询（例如含糊、不恰当、需要外部知识，以及非 SQL）。他们训练了一个基于 RoBERTa 的分类器，依据输入问题和数据库模式来预测问题类型，并指出：在生成 SQL 之前，需要有一个意图分类步骤。Wang 等人 [8] 研究了一款商业 text-to-SQL 产品的真实使用情况，发现用户提交的问题中有 20% 是有问题的。这说明，只依赖仅仅收录可回答问题的精选数据集是有局限的。他们收集了 3,000 余条失败的用户查询，并手工归入六类不可回答问题。这些类别关注歧义、超出范围的查询以及模式不匹配等问题，构成了本研究分类框架的基础；方法部分将进一步说明。Wang 等人 [8] 认为，不可回答查询出现频率高，源于三个关键因素：（1）用户不熟悉数据库模式；（2）自然语言固有的含糊性与表达上的多变；（3）数据库中存在语义相近的概念，因而容易造成混淆。Wang 等人进一步聚焦于两个类别——列歧义与列不可回答——并提出：通过修改已有的表来生成不可回答问题，而不是另造新的不可回答问题。这样做使过程更可控，但也更不贴近真实情况。

在生物医学领域，EHRSQL 2024 共享任务针对的是：为电子健康记录（electronic health records, EHR）构建可靠的 text-to-SQL 系统 [3]。这项任务的独特之处在于，它有意纳入了不可回答的问题，促使系统不仅要为可回答的输入生成正确的 SQL 查询，还要在查询很可能无法回答时放弃作答。评价指标奖励系统对不可回答问题不产出 SQL，并同时惩罚不正确的 SQL，以及在问题不可回答时仍然尝试作答。在这一做法之上，我们把它用到一个生物医学数据集（OncoMx）上，并引入了对不可回答问题的分类。这样，我们就可以按不同的不可回答类型分析系统表现，目标是进一步提升 text-to-SQL 系统在医疗和生物医学研究等敏感领域中的可靠

<!-- 原 PDF 第 4 页 -->

性与安全性。

## 3 数据集

### 3.1 OncoMX（ScienceBenchmark）

为评估可回答的问题，我们使用 ScienceBenchmark 套件所提供的 OncoMX 数据集 [10]。具体而言，我们在该数据集的开发集（dev）划分上评估模型性能。这一划分共有 99 个自然语言问题，并配有对应的 SQL 查询。除金标准 SQL 查询之外，我们还从 OncoMX 数据库中取回了相应的结果。这些输出用来与模型生成的查询及其取回的结果进行比较。少样本提示所用的示例，取自 ScienceBenchmark 的 Seed 数据集。

### 3.2 OncoMX-NAQ（无答案问题，No-answer Questions）

为评估发现不可回答问题的性能，我们新建了一个数据集，包含 8 个类别、共 80 个问题。

**类别。** 我们依据文献 [8, 11]，选择了下列不可回答问题类别。

**1. 非 SQL 问题（Non-SQL Questions）。** 这一类别包括任何 SQL 查询都无法回答的问题。它们可能真实，也与领域相关，但超出了结构化查询生成的范围，通常需要的是解释性或程序性的回应。例如：“为什么 TP53 基因在一些患者中会致癌，在另一些患者中却不会？”（原文：Why does the TP53 gene cause cancer in some patients but not in others?）

**2. 模式外问题（Out of Schema Questions）。** 这些问题所依赖的信息，在模式中是结构上缺失的，或者在数据库内从逻辑上无法访问。我们区分两个子类型：

- **列缺失（Columns Missing）：** 问题所指的信息，并不出现在模式的任何一列中。例如：“EGFR 基因产物的三维蛋白质结构是什么？”（原文：What is the 3D protein structure of the EGFR gene product?）
- **值缺失（Values Missing）：** 问题依赖于数据库中并不存在的特定数据值，尽管相关的列可能存在。例如：“列出在火星癌症组织中过表达的全部基因。”（原文：List all genes overexpressed in Martian cancer tissues.）

**3. 领域外问题（Out of Domain Questions）。** 这一类别中的问题，需要数据库或应用领域（本文中为 OncoMX）之外的知识。没有额外的外部信息，这些问题就无法解答。例如：“2023 年诺贝尔奖研究中提到了哪些生物标志物？”（原文：Which biomarkers are mentioned in the 2023 Nobel Prize research?）

<!-- 原 PDF 第 5 页 -->

**4. 含糊问题（Ambiguous Questions）。** 这一组问题在句法上是有效的，看上去也落在模式范围之内，但说得不够具体，或者意思不清楚，因此存在多种说得通的解释。子类包括：

- **列含糊（Column Ambiguous）：** 有多个列都可以合理地满足查询中的请求。例如：“肺癌中 EGFR 的分数是多少？”（原文：What is the score for EGFR in lung cancer?）
- **值含糊（Value Ambiguous）：** 问题所引用的数据值，可能对应多个实体或多种含义。例如：“找出与生长有关的全部基因。”（原文：Find all genes linked to growth.）
- **上下文含糊（Contextual Ambiguous）：** 问题的本意在很大程度上取决于上下文，而查询里并没有明确给出这些上下文。例如：“导致它的基因有哪些？”（原文：What are the genes that cause it?）
- **算子含糊（Operator Ambiguous）：** 查询暗示了某种比较或条件，但没有清楚指定应当使用哪一个算子（例如“略微过表达”，原文：slightly overexpressed）。例如：“哪些生物标志物更可靠？”（原文：Which biomarkers are more reliable?）

**生成。** 为构建不可回答问题数据集，我们在给定数据库模式的条件下，用两套不同的提示、借助 GPT-4o 生成候选问题。作者对生成结果做了手工审阅和筛选，最终得到 80 个不可回答问题；每个类别选取 10 个有代表性的例子。

完整的问题集和提示见我们的 GitHub 仓库⁵。

## 4 方法

我们提出 Query Carefully，一条用自然语言查询 OncoMX 数据库的流水线。该方法包括流水线、提示设计和指标三个部分。完整代码见 GitHub⁵。

### 4.1 流水线

完整流水线（包括用户界面）见图 1。我们的 text-to-SQL 流水线使用大语言模型 llama3.3:70b，把自然语言问题翻译成可执行的 SQL。对每一个输入问题，我们构造一条针对该任务的提示，并提交给模型。随后解析返回的文本，从中抽出候选 SQL 语句。如果没有产出 SQL，而且输出也没有明确表示该问题不可回答，我们就发出一次标准化的再提示：“请返回一条 SQL 查询；如果该问题无法用数据库上的 SQL 查询来回答，则返回 ‘unanswerable question’。”（原文：Please return a SQL query or ‘unanswerable question’ if the question cannot be answered with an SQL query on the database.）若得到一条有效的 SQL 查询，就在目标数据库上执行它。在一种设定中，我们加入一个可选的后处理步骤，用来验证 SQL。

⁵ https://github.com/JasminSaxer/QueryCarefully.git

<!-- 原 PDF 第 6 页 -->

如果查询在执行过程中出错，我们把错误信息再次交给 LLM，提示为：“请根据下列错误信息修正 SQL 查询：<error>。”（原文：Please correct the SQL query based on the following error message: <error>.）这一修正循环最多允许三次重试。

**图 1.** 带用户界面的 Query Carefully 流水线。NAQ：无答案问题（No-Answer-Questions）。

表抽取失败，见原 PDF 第 6 页。`find_tables` 把该图误识别为一张表，抽出的单元格与正文混杂，不能当作表中数字或结构使用。下面只列出文本层抽出的图中标签，顺序为抽取顺序，不表示方框之间的连线：

- OncoMX Database（OncoMX 数据库）
- User Query（用户查询）
- Text-to-SQL
- Schema for LLM Prompt（供 LLM 提示使用的模式）
- NL2SQL Prompt（NL2SQL 提示）
- No SQL Clarification Prompt（无 SQL 时的澄清提示）
- Debug SQL with Error Prompt（根据错误调试 SQL 的提示）
- Interim Results（中间结果）
- Result Explanation Prompt（结果解释提示）
- Few-Shot Examples（少样本示例）
- SQL Execution（SQL 执行）
- SQL, None or NAQ（SQL、空，或 NAQ）
- Result or Error（结果或错误）
- Schema（模式）
- processed Schema（处理后的模式）
- Examples（示例）
- Query（查询）
- Response（回应）
- SQL Extraction（SQL 抽取）
- None（空）
- Response（回应）
- SQL
- Error（错误）
- Response（回应）
- SQL Extraction（SQL 抽取）
- SQL
- Result（结果）
- SQL-to-Result（由 SQL 得到结果）
- User Interface（用户界面）
- OncoMX-NAQ
- OncoMX Dev
- NAQ

### 4.2 提示设计

为了在我们的 text-to-SQL 设定中生成高质量的 SQL，我们针对 OncoMX 关系数据库模式，仔细设计了提示模板。基础提示包含一条系统消息，要求 LLM 充当自然语言到 SQL 翻译的专家，并生成句法正确的 PostgreSQL 查询。模型被要求只返回 SQL 查询，不附加解释或评论。此外，提示中还包括经过重新排版、便于人阅读的数据库模式。

**模式表示。** 我们用 GPT-4o 把数据库模式重新排版，使之更适合 LLM，确保表名和列名可读，并且语义清楚。完整模式以结构化、便于人阅读的格式交给模型：列出每一张表及其列、数据类型、外键关系，以及列级注释，以便保留语义上下文。

**处理不可回答问题。** 为确保模型不会尝试为那些无法可靠地从

<!-- 原 PDF 第 7 页 -->

数据库中得到回答的问题生成 SQL 查询，我们在系统提示里加入了显式指令，做法与 [2] 相近。这些规则用来引导模型：当问题不应当被回答时，返回 “unanswerable question”。

**用户提示。** 用户提示由一条自然语言查询构成，前面加上一句简短指令。例如：

```
# 返回下列问题的 SQL
[Q]：请给出 ref_aa 为 E 的全部疾病突变
[SQL]：
```

原文为：

```
# Return the SQL for the following Question
[Q]: Show me all disease mutations with ref_aa E
[SQL]:
```

**少样本示例。** 为评估上下文学习的效果，我们比较了四种提示配置：零样本、1-shot、3-shot 和 5-shot。在少样本设定中，提示用可回答问题与不可回答问题这两类示例加以扩充。可回答示例包含正确落地的 SQL 语句；不可回答示例则是自然语言问题，后面跟着回应 unanswerable question。

为了动态选择相关的少样本示例，我们使用 Alibaba-NLP/gte-Qwen2-1.5B-instruct 模型，对自然语言问题做嵌入。最相似的可回答问题，从 OncoMX 的 ScienceBenchmark seed 数据集中检索；最相似的不可回答问题，从我们的新数据集中检索，并去掉当前待回答的那个问题。相似度用余弦相似度来衡量。

完整的提示示例见 GitHub。

### 4.3 指标

为全面评估我们的 text-to-SQL 系统，我们报告三项不同指标上的表现。每一项对应系统行为的一个方面：句法正确性、语义准确性，以及对不可回答查询的稳健性。每项指标都在可回答问题数据集或不可回答问题数据集上计算，并报告为准确率，即正确预测的数量除以被评估查询的总数。

**SQL 精确匹配准确率（SQL Exact Match Accuracy）。** 该指标检查：预测的 SQL 字符串在规范化之后（转为小写，并去掉多余空白），是否与金标准（参考）SQL 查询完全一致。这是一种严格比较，不容忍语义等价但句法不同的查询。

**结果准确率（Result Accuracy）。** 该指标把预测 SQL 查询的执行结果，与金标准（参考）查询的执行结果相比较，以此评估预测 SQL 的语义正确性。它支持多层比较，以便容纳格式差异或轻微的结构差异：

- **精确匹配（Exact Match）：** 结果表在内容和结构上都相同，包括行的顺序和列名。

<!-- 原 PDF 第 8 页 -->

- **软正确（Soft Correct）：** 预测结果与金标准结果包含相同的数据，但允许行顺序不同、列名不同，也允许标识列（例如 id）是否出现有所不同。软正确分数的思路来自 [4]。
- **数据库错误（DB Error）：** 预测的 SQL 查询未能成功执行，原因是数据库错误（例如语法错误或无效引用）。

**不可回答问题检测（Unanswerable Question Detection）。** 该指标评估系统正确识别无法回答的问题的能力。它检查：对于金标准数据中标注为不可回答的查询，模型是否返回指示 “unanswerable question”。此外，我们也核验：对于可回答的查询，模型不会返回 “unanswerable question”。

## 5 结果

我们在 OncoMX Dev 数据集上，以及在 OncoMX-NAQ 上，评估了不同的提示设计。OncoMX-NAQ 是对 OncoMX Dev 的扩展，每个类别另有 10 个不可回答问题（图 2）。在 OncoMX Dev 上，单独加入“无答案规则”（No-Answer Rules, NAR）对准确率没有影响（原文括注为 “accuracy” 换行后接 “0.5”，中间的关系符号未抽出：`(accuracy 0.5)`。公式抽取不完整，见原 PDF 第 8 页）。加入可回答示例后，准确率适度提高到 0.6，其中 5-shot 提示表现最好。同时加入可回答示例与不可回答示例，得到的准确率与此相近。这表明：正例提升了可回答性检测，而不可回答示例不会影响那些本身不含不可回答问题的数据集上的性能。在我们的 OncoMX-NAQ 数据集上，单独使用 NAR 的准确率为 0.37。加入可回答示例后性能有所提高；不论上下文学习的设定如何，都是如此，不过仍低于 OncoMX dev 的水平。继续增加不可回答示例会进一步提高准确率，并在 5-shot 时超过 OncoMX dev。最高准确率（接近 0.8）是在同时使用可回答示例与不可回答示例时取得的。这说明，对于含有不可回答问题的数据集，平衡的提示是有价值的。

### 5.1 OncoMX dev

图 3 比较了 OncoMX dev 集上、不同提示变体的准确率指标。只有在使用上下文学习（in-context learning, ICL）、并且示例是来自 OncoMX Seed 划分的可回答示例时，才观察到 SQL 精确匹配。这表明，严格的 SQL 精确匹配并不足以单独作为 text-to-SQL 的评价指标。在所有提示中，软正确这一类都很少出现；在多数情况下，系统要么精确复现金标准结果集，要么与之大幅偏离。引入错误检查循环之后，数据库执行错误消失了，但不正确的结果增多了。这说明，仅做句法验证并不能保证事实上的正确，而且许多查询对模型来说本质上仍然困难。

<!-- 原 PDF 第 9 页 -->

**图 2.** 不同提示在 OncoMX Dev 与 OncoMX-NAQ 数据集上的准确率。图中给出了 OncoMX Dev 的软正确准确率。

该图为图像，文本层只抽出图题。图中未在正文写出的数值见原 PDF 第 9 页。

### 5.2 按无答案问题类型划分的准确率

接下来，我们分析不可回答的问题是如何被检出的。为了进一步拆开 NAR 对不同类别不可回答问题的作用，我们按不可回答问题的类别做了更细的分析（图 4）。结果发现，不同类型的不可回答问题，可检出的程度并不一样：

- 结构上可界定的类别，例如非 SQL（Non-SQL）、列缺失（Columns Missing）和领域外（Out of Domain），在只使用 NAR 时具有中等的基线准确率（0.6–0.65）。无论加入可回答示例还是不可回答示例，准确率都有明显提高；同时包含两类示例的提示，在这些类别上达到接近完美的检测。
- 在值缺失（Values Missing）类别中，基线准确率较低（0.3），而且只有在同时纳入可回答示例与不可回答示例时才有改善，最高达到 0.5。这反映出：仅凭模式信息很难检出缺失的值。缺失的列可以直接从模式细节推断出来，缺失的值则不能。
- 含糊类别（列含糊 Column Ambiguous、值含糊 Value Ambiguous、上下文含糊 Contextual Ambiguous、算子含糊 Operator Ambiguous）的表现更为多样。值得注意的是，列含糊问题分类得很差（最高准确率 0.3）。text-to-SQL 常常生成引用某一个合适列的 SQL，却没有识别出这里存在歧义。相比之下，值含糊问题取得了更高的

<!-- 原 PDF 第 10 页 -->

**图 3.** 按提示类型给出的 ScienceBenchmark（OncoMX dev）各项度量。AQ：可回答问题（Answerable Questions）；NAQ：无答案问题（No-Answer Questions）。

该图为图像，文本层只抽出图题。图中未在正文写出的数值见原 PDF 第 10 页。

准确率，尤其是在纳入不可回答示例的时候。这表明，模型处理值上的歧义，要好于处理列上的歧义。

- 对于上下文含糊的问题，只使用 NAR 时大约检出一半；只有同时提供可回答示例与不可回答示例，才达到完全准确。与此类似，算子含糊的问题也需要两类示例，才能达到较高的准确率（0.9）。有一个被误分类的问题，最终因为存在一个相关的数据库列，而被认定为可回答。

有意思的是，在几乎所有类别中，只加入可回答示例对不可回答问题检测的提升，大于只加入不可回答示例（平均准确率 0.49 对 0.43；仅使用 NAR 时为 0.35）。不过，把两类示例结合起来，在所有类别上都稳定地得到最高准确率。

### 5.3 Text-to-SQL 用户界面

我们提供一个轻量的网页界面，用来与 Query Carefully 流水线交互（见图 5）。用户从下拉菜单中选择大语言模型（默认是 llama3.3:70b），输入一个关于 OncoMX 数据库的自然语言问题，然后得到生成的 SQL、相应的结果表，以及对这个问题的简短回答。界面会把中间步骤展示出来，包括 SQL 预览、执行状态，以及任何错误信息。

<!-- 原 PDF 第 11 页 -->

**图 4.** 按类别和提示划分的、不可回答问题检测准确率。AQ：可回答问题（Answerable Questions）；NAQ：无答案问题（No-Answer Questions）。

该图为图像，文本层只抽出图题。图中未在正文写出的数值见原 PDF 第 11 页。

由于 SQL 和输出都被明确展示出来，这个界面有助于保持透明，便于领域专家核验，也便于快速迭代问法。当模型检出一个不可回答的问题时，它会返回说明，解释为什么不能回答这个问题，并给出改进的办法。

## 6 结论

Text-to-SQL 系统应当考虑到用户的专业程度，以及可能出现的不可回答查询。这是当前基准数据集的一项局限，在医学等领域尤其如此，因为并非 SQL 专家的人可能会误读结果。PRACTIQ [1] 等已有数据集依据 SQL 语句把查询分成若干类，例如含糊的或不存在的列、过滤条件和连接。与此相对，我们的工作在这一做法之上，还纳入了非 SQL 问题和领域外问题，从而覆盖更广的一类真实用户查询。PRACTIQ 和 Sphinteract [12] 这类对话式方法，通过为不可回答查询提供解释，来增强与用户的交互。尽管如此，要有效地使用，仍要求用户自己识别出相关的列，或者向用户提供显式的模式标注，引导他们找到匹配的查询。“先消歧，再解析”（Disambiguate First, Parse Later）（Saparina & Lapata, 2025）以及“是不是只要长上下文就够了”（Is Long Context All You Need）（Chung, 2025）等方法表明：生成多种解释，或者利用扩展的上下文窗口，都有助于消解歧义，不过计算代价更高。我们的结果与先前的发现一致，即基于示例的提示能够改善 text-to-SQL 的问题分类 [12, 1]；同时，本文特有地表明，可回答示例对检测不可回答查询的贡献可以大于负例，从而凸显平衡地纳入示例的重

<!-- 原 PDF 第 12 页 -->

**图 5.** 用户界面上一个不可回答问题的示例。

该图为界面截图，文本层只抽出图题。界面中的具体问答见原 PDF 第 12 页。

要性。

本研究的局限包括：检测某些特定类别的不可回答查询仍然困难，尤其是那些涉及缺失值，或者涉及列歧义与值歧义的查询。此外，识别出不可回答的查询只是一个初始阶段。如果纳入能够提出可能解决办法的机制，如 PRACTIQ 或 Sphinteract 所建议的那样，就可以进一步增强 text-to-SQL 系统的稳健性。

**利益披露。** 作者声明，没有需要披露的、与本文内容相关的竞争性利益。

## 参考文献

1. Dong, M., Kumar, N.A., Hu, Y., Chauhan, A., Hang, C.W., Chang, S., Pan, L., Lan, W., Zhu, H., Jiang, J., Ng, P., Wang, Z.: PRACTIQ：一个实用的对话式

<!-- 原 PDF 第 13 页 -->

Text-to-SQL 数据集，包含含糊查询与不可回答查询（2024 年 10 月）. https://doi.org/10.48550/arXiv.2410.11076

2. Jo, Y., Lee, S., Seo, M., Hwang, S.J., Lee, M.: LG AI Research 与 KAIST 在 EHRSQL 2024：用伪标注的不可回答问题对大语言模型做自训练，以构建电子健康记录上可靠的 Text-to-SQL 系统（2024 年 5 月）. https://doi.org/10.48550/arXiv.2405.11162

3. Lee, G., Kweon, S., Bae, S., Choi, E.: EHRSQL 2024 共享任务综述：电子健康记录上的可靠 Text-to-SQL 建模. In: Naumann, T., Ben Abacha, A., Bethard, S., Roberts, K., Bitterman, D. (eds.) Proceedings of the 6th Clinical Natural Language Processing Workshop. pp. 644–654. Association for Computational Linguistics, Mexico City, Mexico（2024 年 6 月）. https://doi.org/10.18653/v1/2024.clinicalnlp-1.62

4. Nooralahzadeh, F., Zhang, Y., Smith, E., Maennel, S., Matthey-Doret, C., De Fondeville, R., Stockinger, K.: StatBot.Swiss：用自然语言探索双语开放数据. In: Findings of ACL (2024). https://doi.org/10.18653/v1/2024.findings-acl.326

5. Popescu, A.M., Etzioni, O., Kautz, H.: 迈向数据库自然语言界面的理论. In: Proceedings of the 8th international conference on Intelligent user interfaces. pp. 149–157. ACM, Miami Florida USA（2003 年 1 月）. https://doi.org/10.1145/604045.604070

6. Sala, L., Sullutrone, G., Bergamaschi, S.: 基于大语言模型的 Text-to-SQL：前景与陷阱. https://ceur-ws.org/Vol-3741/paper65.pdf

7. Singh, A., Shetty, A., Ehtesham, A., Kumar, S., Khoei, T.T.: 基于大语言模型的生成式人工智能用于 Text-to-SQL 综述：基准、应用、用例与挑战. In: 2025 IEEE 15th Annual Computing and Communication Workshop and Conference (CCWC). pp. 00015–00021（2025 年 1 月）. https://doi.org/10.1109/CCWC62904.2025.10903689

8. Wang, B., Gao, Y., Li, Z., Lou, J.G.: 知道我所不知道的：处理 Text-to-SQL 中的含糊问题与未知问题. In: Rogers, A., Boyd-Graber, J., Okazaki, N. (eds.) Findings of the Association for Computational Linguistics: ACL 2023. pp. 5701–5714. Association for Computational Linguistics, Toronto, Canada（2023 年 7 月）. https://doi.org/10.18653/v1/2023.findings-acl.352

9. Yu, T., Zhang, R., Yang, K., Yasunaga, M., Wang, D., Li, Z., Ma, J., Li, I., Yao, Q., Roman, S., Zhang, Z., Radev, D.: Spider：面向复杂、跨领域语义解析与 Text-to-SQL 任务的大规模人工标注数据集. In: Riloff, E., Chiang, D., Hockenmaier, J., Tsujii, J. (eds.) Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing. pp. 3911–3921. Association for Computational Linguistics, Brussels, Belgium（2018 年 10 月）. https://doi.org/10.18653/v1/D18-1425

10. Zhang, Y., Deriu, J., Katsogiannis-Meimarakis, G., Kosten, C., Koutrika, G., Stockinger, K.: ScienceBenchmark：评估自然语言到 SQL 系统的复杂真实世界基准. Proceedings of the VLDB Endowment 17(4), 685–698（2023 年 12 月）. https://doi.org/10.14778/3636218.3636225

11. Zhang, Y., Dong, X., Chang, S., Yu, T., Shi, P., Zhang, R.: 你问了一个好问题吗？面向 Text-to-SQL 的跨领域问题意图分类基准（2020 年 10 月）. https://doi.org/10.48550/arXiv.2010.12634

12. Zhao, F., Deep, S., Psallidas, F., Floratou, A., Agrawal, D., Abbadi, A.E.: Sphinteract：通过用户交互消解 NL2SQL 中的歧义. Proceedings of the VLDB Endowment 18(4), 1145–1158（2024 年 12 月）. https://doi.org/10.14778/3717755.3717772, publisher: Association for Computing Machinery (ACM)

<!-- 译完 -->
