# 只有 Text2SQL 不够：用 TAG 统一人工智能与数据库

- 原文件名：TAG_CIDR2025.pdf
- 原标题：Text2SQL is Not Enough: Unifying AI and Databases with TAG
- 中文标题：只有 Text2SQL 不够：用 TAG 统一人工智能与数据库
- 作者：Asim Biswal1,*，Liana Patel2,*，Siddharth Jha1，Amog Kamsetty1，Shu Liu1，Joseph E. Gonzalez1，Carlos Guestrin2，Matei Zaharia1（1UC Berkeley，2Stanford University）。*两位作者对本研究贡献相同。
- 会议或 arXiv：页眉为 CIDR’25, January 19-22, 2025, Amsterdam, The Netherlands。ACM ISBN 978-x-xxxx-xxxx-x/YY/MM，https://doi.org/10.1145/nnnnnnn.nnnnnnn

<!-- 原 PDF 第 1 页 -->

## 摘要

在数据库上用自然语言问题提供服务的 AI 系统，有望释放巨大价值。这类系统将允许用户把语言模型（LM）强大的推理与知识能力，和数据管理系统可扩展的计算能力一起使用。这些组合能力将使用户能够对自定义数据源提出任意自然语言问题。然而，现有方法和基准对这一设定探索不足。Text2SQL 方法只关注能够用关系代数表达的自然语言问题，这只是真实用户希望提问的一小部分。同样，检索增强生成（RAG）只考虑能用对数据库中一条或少数几条记录的点查找来回答的有限查询子集。我们提出表增强生成（Table-Augmented Generation, TAG），一种统一且通用的范式，用于回答数据库上的自然语言问题。TAG 模型表示 LM 与数据库之间广泛的、此前未被探索的交互，并为在数据上利用 LM 的世界知识与推理能力创造了令人兴奋的研究机会。我们系统地开发基准来研究 TAG 问题，并发现标准方法正确回答的查询不超过 20%，证实这一领域需要进一步研究。我们在 https://github.com/TAG-Research/TAG-Bench 发布基准代码。

## 1 引言

语言模型有望通过让用户用自然语言对数据提问来革新数据管理，这带来了大量关于 Text2SQL 和检索增强生成（RAG）方法的研究。然而根据我们的经验（包括 Databricks 的内部工作负载和客户），用户的问题常常超出这些范式的能力，要求对新系统投入研究：把数据库系统的逻辑推理能力与现代语言模型的自然语言推理能力结合起来。

具体而言，我们发现真实商业用户的问题常常需要领域知识、世界知识、精确计算和语义推理的复杂组合。数据库系统显然通过它们存储的最新数据提供领域知识来源，也提供规模化的精确计算（而这正是 LM 不擅长的）。

LM 以两种关键方式扩展数据库的现有能力。第一，LM 拥有对文本数据的语义推理能力，而这是许多自然语言用户查询的核心要素。例如，一项 Databricks 客户调查表明，用户希望问这样的问题：产品 X 的哪些客户评论是正面的？或者为什么我的销售额在这段时间下降了？这些问题呈现基于复杂推理的任务，例如对自由文本字段做情感分析，或对趋势做摘要。LM 很适合这些任务，而传统数据库系统中的精确计算或关系原语无法对它们建模。

第二，LM 利用模型训练期间学到的、并由模型权重隐式存储的知识，可以用数据库表模式没有显式捕获的世界知识来增强用户的数据。例如，一位 Databricks 内部 AI 用户在一张包含账户名、产品和收入属性的表上问：零售（retail）垂直领域的 QoQ 趋势是什么？要回答这个查询，系统必须理解业务如何定义 QoQ（例如从上一季度到本季度的环比趋势，或从去年本季度到今年本季度），以及哪些公司被认为属于零售垂直领域。这一任务很适合利用预训练或微调 LM 所持有的知识。

能够高效地一起利用数据库和 LM、以充分的一般性来服务自然语言查询的系统，有潜力改变用户理解其数据的方式。不幸的是，这些问

<!-- 原 PDF 第 2 页 -->

题今天不能被 Text2SQL 和 RAG 等常见方法回答。虽然 Text2SQL 方法 [26, 28, 31, 32] 适合那些有直接关系等价物的自然语言查询子集，它们无法处理需要语义推理或世界知识的大量用户查询。例如，前面那个询问哪些客户评论是正面的用户查询，可能需要对评论做按行的逻辑 LM 推理，把每条分类为正面或负面。类似地，询问销售额为何下降的问题需要一个必须跨许多表项聚合信息的推理问题。

另一方面，RAG 模型限于基于相关性的、对少数数据记录的简单点查找，随后是单次 LM 调用。这一模型只服务能用点查找回答的查询子集，也未能利用许多数据库系统更丰富的查询执行能力，从而把计算任务（例如计数、数学和过滤）留给一次容易出错的 LM 调用。除了在计算任务上容易出错且低效之外，LM 也被表明在长上下文提示上表现差，这限制了它们在 RAG 生成阶段对规模化数据进行推理的能力。

我们转而提出表增强生成（TAG），作为在数据库上回答自然语言问题的系统的统一范式。具体而言，TAG 定义三个关键步骤，如图 1 所示。首先，查询合成步骤 $\mathrm{syn}$ 把用户的任意自然语言请求 $R$ 翻译成可执行的数据库查询 $Q$。然后，查询执行步骤 $\mathrm{exec}$ 在数据库系统上高效计算相关数据 $T$。最后，答案生成步骤 $\mathrm{gen}$ 利用 $R$ 和 $T$，其中 LM 被编排，可能以迭代或递归模式作用在数据上，以生成最终的自然语言答案 $A$。TAG 模型简单但有力：它由下面三个方程定义，但捕获了 LM 与数据库之间广泛的、此前研究不足的交互。

$$
\mathrm{syn}(R) \rightarrow Q \tag{查询合成}
$$

$$
\mathrm{exec}(Q) \rightarrow T \tag{查询执行}
$$

$$
\mathrm{gen}(R, T) \rightarrow A \tag{答案生成}
$$

值得注意的是，TAG 模型统一了先前方法，包括 Text2SQL 和 RAG，它们是 TAG 的特例，并且只服务有限的用户问题子集。

虽然若干先前工作处理 TAG 的这些特例，我们提供第一个端到端的 TAG 基准，由一组广泛的、需要 LM 推理和知识能力的现实查询组成。我们表明这类问题带来显著的研究挑战，以及高效 TAG 实现的前景。我们的评测分析了朴素 Text2SQL 和 RAG 基线，以及两个更强的基线：带 LM 生成的 Text2SQL，以及带基于 LM 重排序的检索。在多种查询类型上，我们发现每种基线方法都持续无法达到高准确率，在基准上从未超过 20% 的精确匹配。另一方面，我们在近期的 LOTUS 运行时 [21] 之上实现手写的 TAG 流水线，发现它们相对基线达到最多高 20–65% 的准确率。这一显著的性能差距表明构建高效 TAG 系统的前景。

## 2 TAG 模型

我们现在描述 TAG 模型。它接受自然语言请求 $R$，并返回锚定在数据源上的自然语言答案 $A$。我们概述 TAG 系统实现的三个主要步骤：查询合成、查询执行和答案生成。我们把 TAG 可处理地定义为这些步骤的单次迭代，但也可以考虑以多跳方式扩展 TAG。

### 2.1 查询合成

$\mathrm{syn}$ 函数接受自然语言请求 $R$，以及一个将由数据库系统执行的查询 $Q$。给定用户请求，这一步负责（a）推断哪些数据与回答该请求相关（例如使用表模式），以及（b）执行语义解析，把用户请求翻译成数据库系统可以执行的查询。这个查询可以是任何查询语言，但在我们的例子中使用 SQL。

图 1 给出用户查询的一个 TAG 实例，该查询问：“Summarize the reviews of the highest grossing romance movie considered a ‘classic’”（总结被看作“经典”的票房最高爱情电影的评论）。这里，数据源包含每部电影的标题、收入、体裁，以及一条相关评论的信息。

**图 1 见原 PDF。** 图中示例表包含列 movie_title、revenue、review、genre。可见行包括 Shang-Chi 432.2、体裁 Action、评论 “solid film…”；以及 Titanic 2257.8、体裁 Romance、评论 “still best…” 与 “a guilty…”。查询合成后执行 SQL，答案生成输出类似 “The reviews of Titanic discuss the on screen chemistry…”。

图 1：一个 TAG 实现的例子，用于在一张关于电影的表上回答用户的自然语言问题。TAG 流水线分三个阶段进行：查询合成、查询执行和答案生成。

在这一步，系统利用 LM 的语义推理能力生成一条 SQL 查询，该查询使用数据源中 movie_title、review、revenue 和 genre 上的属性。注意，在这个例子中，数据库 API 能够在 SQL 查询内执行 LM 用户定义函数，因此这一步也为每一行引入对 LM 的调用，以在查询中识别经典电影。

### 2.2 查询执行

在查询执行步骤中，$\mathrm{exec}$ 函数执行查询，以从数据库系统获得表 $T$。这一步利用数据库查询引擎，在大量存储数据上高效执行查询。数据库 API 可以由多种多样的系统提供，我们在第 3 节探讨。一些 API 可能允许基于 LM 的算子 [18–21]，使数据库引擎能够在 $\mathrm{exec}$ 内部利用 LM 的世界知识和推理能力。

在图 1 所示的例子中，数据库查询是用 SQL 写成的选择与排序查询，返回包含相关行的表。查询使用 LM 做选择，根据 movie_title 评估哪些电影是经典，并对 genre 做标准过滤以找到爱情电影。查询也根据收入对结果排序，以找到票房最高的电影。如图所示，所得表包含电影 “Titanic” 的评论。

### 2.3 答案生成

TAG 中的答案生成步骤对应 RAG 中的生成步骤。在这一步，$\mathrm{gen}$ 函数使用 LM 生成

<!-- 原 PDF 第 3 页 -->

对用户自然语言请求 $R$ 的答案 $A$，并使用计算出的数据 $T$。

图 1 展示示例 TAG 流水线的最后阶段，输出对 “Titanic” 评论的摘要，作为对原始用户请求的答案。在该例子中，相关数据 $T$ 被编码成字符串供模型处理。编码后的表与原始用户请求 $R$ 一起被传给 LM。为得到答案，这一步利用模型对 review 列的语义推理能力来总结评论。

## 3 TAG 设计空间

在本节中，我们探讨 TAG 模型的一般性，并描述它产生的丰富设计空间，突出若干研究不足、值得进一步研究的机会。

**查询类型。** TAG 模型的表达能力足以服务广泛的自然语言用户查询。我们考虑两种重要的查询分类，依据（a）回答查询所需的数据聚合层次，以及（b）回答查询所需的知识与能力。首先，TAG 模型既捕获点查询，例如基于检索的问题 [3, 9, 15, 16, 25, 30]，它们需要对数据库中一行或少数几行做查找；也捕获聚合查询，例如基于摘要或排序的问题，它们需要跨数据库许多行的逻辑推理。其次，TAG 模型使自然语言查询对系统提出不同程度的数据或基于推理的能力要求，包括情感分析和分类等任务。

**数据模型。** 底层数据模型可以采取许多形式。我们的实现使用关系数据库来存储和检索结构化属性，以便在下游问答任务中做知识锚定。其他系统可以在更非结构化的数据（例如自由文本、图像、视频和音频）或半结构化数据上操作，这些数据可以用多种数据模型存储，例如键值、图、向量、文档或对象存储。

**数据库执行引擎与 API。** 用于存储数据的底层系统可以使用许多可能的数据库执行引擎。Text2SQL 考虑的是基于 SQL 的查询引擎设定，为用户查询检索关系数据。在这一设定中，$\mathrm{syn}$ 将利用数据源的知识，例如表模式，并返回一条 SQL 查询来执行检索步骤。在另一种常见设定中，即向量嵌入上的检索系统，$\mathrm{syn}$ 把自然语言查询变换成嵌入，$\mathrm{exec}$ 在向量存储上执行基于相似度的检索。

虽然这两种设定已被广泛研究，若干研究不足的替代设定为高效实现 TAG 系统、以服务更广泛的查询提供了有趣机会。例如，近期工作用语义算子增强关系模型 [21]，它们提供一组基于 AI 的声明式算子（例如用自然语言说明符做过滤、排序、聚合和搜索），或 LM 用户定义函数 [19]，它们提供通用的 LM 函数。此外，MADLib [10]、Google 的 BigQuery ML [1] 和 Microsoft 的 Predictive SQL [24] 等查询语言用原生的基于 ML 的函数增强基于 SQL 的 API。利用这些系统，为执行优化的、基于推理的检索模式提供了独特机会。例如，在图 1 所示的例子中，用语义算子 [21] 实现的 TAG 流水线可以使用 $\mathrm{sem\_filter}$ 算子，在查询执行步骤中根据它们是否为 “classic” 来过滤行。

**LM 生成模式。** 给定相关数据表 $T$，$\mathrm{gen}$ 可以由大量实现决策组成，以产生对用户请求 $R$ 的最终自然语言答案 $A$。Text2SQL 省略最后的生成步骤，在查询执行后即停止；RAG 流水线通常利用单次 LM 调用的生成实现，把相关数据放进上下文。在这一设定中，若干工作研究与表编码 [8]、提示压缩 [5] 和提示调优 [13] 相关的子问题，以优化上下文学习结果。

更新近的研究，例如 LOTUS [21]，突出了组合迭代或递归 LM 生成模式的潜力，用于回答涉及跨多个数据行的、基于推理的变换、聚合或排序的查询。早期工作表明这些基于 LM 的算法所呈现的丰富设计空间，以及在若干下游任务上有前景的结果。

## 4 评测

在本节中，我们引入第一个 TAG 基准并评测一组基线，旨在处理如下问题：

（1）现有的表问答方法在需要语义推理或世界知识的查询上表现如何？

（2）TAG 模型的手写实现——把计算步骤和推理步骤划分到 DBMS 与 LM 操作上——在这些查询上表现如何？

### 4.1 基准方法

现有基准探索了模型在完全可以由数据源中的数据回答的基本查询上的表现。我们在先前工作的基础上修改查询，使它们需要数据源中没有直接提供的知识，或需要语义推理才能回答。我们选择 BIRD [17]，一个被广泛使用、且 LM 已在其上被评测的 Text2SQL 基准，因为它有大规模的表，以及多样的领域和查询类型。

**数据集。** 我们的查询跨越从 BIRD 选出的 5 个领域，每个领域的查询类型都有多样性。我们选择 california_schools、debit_card_specializing、formula_1、codebase_community 和 european_football_2 作为查询的数据库来源。

**查询。** BIRD 基准定义了基本查询类型，包括基于匹配、比较、排序和聚合的查询。我们从 BIRD 基准中在这些类型里选择查询，并修改它们，使模型需要世界知识或语义推理才能回答。作为一个需要世界知识的修改查询的例子，在 california_schools 数据库中，一条修改后的查询增加了一个附加子句，只询问湾区（Bay Area）的学校。这一信息不在表中，需要模型的世界知识才能回答。接下来，一条修改后的查询

<!-- 原 PDF 第 4 页 -->

需要 LM 推理，它询问 codebase_community 数据库中某篇帖子上最讽刺的前 3 条评论。对于这些查询的评测，我们依赖人工标注的真实答案。我们的最终基准由 80 条修改后的查询组成，40 条需要参数知识，40 条需要推理，并在所选的 4 种 BIRD 查询类型中各有 20 条。

**评测指标。** 对基于匹配、比较和排序的查询类型，我们把准确率度量为相对标注正确答案的精确匹配百分比。对聚合查询，我们用每种基线对结果做定性分析。我们也以秒为单位测量每条查询的执行时间。

**实验设定。** 我们使用 Meta 的 Llama-3.1 模型 [2] 的指令调优变体，参数量为 70B，作为 Text2SQL 和最终输出生成的 LM。对涉及 SQL 的基线，我们使用 SQLite3 作为数据库 API，并对 RAG 基线使用 E5 base 嵌入模型 [23]。我们用 vLLM [14] 在 8 块 A100 80GB GPU 上运行 Llama-3.1-70B-Instruct。

### 4.2 基线

**Text2SQL。** 在这一基线中，LM 生成 SQL 代码并运行以得到答案。对给定的自然语言查询，我们构造一个 LM 提示，包含该查询领域中每张表的表模式，使用与 BIRD 工作相同的提示格式。我们评测这一基线：在 SQLite3 中执行生成的 SQL 代码，并测量不正确答案的数量，包括模型未能生成合法 SQL 代码的情形。

**检索增强生成（RAG）。** RAG 风格的方法已被探索用于表检索 [6, 25]，其中表格数据被嵌入到索引中以供搜索。对我们的基线，我们使用行级嵌入。给定一行在被嵌入 FAISS [7] 索引之前，被序列化为每个列的 “- col: val”。在查询时，我们执行向量相似度搜索，检索 10 个相关行，连同自然语言问题一起放进上下文喂给模型。

**检索 + LM 排序。** 我们扩展 RAG 基线，利用 LM 为检索到的行分配 0 到 1 之间的分数，以便在输入模型之前重排行，如 STaRK 工作 [25] 中所做的那样。我们使用 Llama-3.1-70B-Instruct 作为重排器。

**Text2SQL + LM。** 在这一基线中，我们的模型首先被要求生成 SQL，以检索一组相关行来回答给定的自然语言查询。这与 Text2SQL 基线有重要区别：在后者中，模型被要求直接生成 SQL 代码，这些代码在执行后单独就给出查询的答案。与 RAG 基线类似，相关行一旦被检索，就被放进上下文喂给模型。

**手写 TAG。** 我们也评测手写的 TAG 流水线，它们利用对表模式的专家知识，而不是从自然语言请求到数据库查询的自动查询合成。我们用 LOTUS [21] 实现手写 TAG 流水线。LOTUS API 允许程序员用标准关系算子以及语义算子（例如基于 LM 的过滤、排序和聚合）声明式地指定查询流水线。LOTUS 也提供优化的语义查询执行引擎，我们用它来实现手写 TAG 流水线的查询执行和答案生成步骤。

### 4.3 结果

表 1 给出每种方法的准确率（以精确匹配度量）和执行时间。如表所示，在所选的 BIRD 查询类型上，我们发现手写 TAG 基线一致地达到 40% 或更好的精确匹配准确率，而所有其他基线都未能超过 20% 准确率。

Text2SQL 基线在所有类型上表现都差，执行准确率不高于 20%，但在排序查询上尤其差，只有 10% 准确率，因为许多排序查询需要在文本上推理。Text2SQL + LM 生成基线在各类型上有类似的差表现，但在基于匹配和比较的查询上更差，只有 10% 准确率。在这些查询类型上，执行 SQL 之后试图把许多行喂给模型时，发生了若干上下文长度错误。

把注意力转向 RAG 基线，我们看到它在所有查询类型上都未能正确回答任何一条查询，突出了它对这一空间中查询的不适应。加上 LM 重排序后，检索 + LM 排序能够在比较查询中正确回答一条查询，然而该基线仍然比除 RAG 之外的所有其他基线更差。

我们的手写 TAG 基线总体上正确回答 55% 的查询，在比较查询上表现最好，精确匹配准确率为 65%。该基线在除排序查询之外的所有查询类型上一致地超过 50% 准确率，这是因为精确排序项目的难度更高。总体而言，这一方法相对标准基线给我们 20% 到 65% 的准确率提升。

此外，表 2 突出了标准方法在回答第 3 节所讨论的查询类型时的弱点。具体而言，朴素 Text2SQL 在需要 LM 推理的查询上尤其吃力，精确匹配准确率只有 10%，因为它省略了答案生成步骤。同时，RAG 基线以及检索 + LM 排序基线在所有查询类型上都吃力，只正确回答了一条查询，因为它们依赖 LM 来处理数据上的全部精确计算。与之相对，手写 TAG 基线在需要知识的查询和需要推理的查询上都达到超过 50% 的准确率，强调 TAG 模型在它所涵盖的查询上的通用性。

值得注意的是，在提供更高准确率的同时，手写 TAG 方法提供了高效实现，执行时间比其他基线低至多 $3.1\times$。手写基线对所有查询平均耗时 2.94 秒。这一相对较低的执行时间突出：可以通过利用 LM 的高效批推理来设计高效的 TAG 系统。

最后，我们定性分析每种基线在聚合查询上的结果。图 2 给出 RAG、朴素 TAG（文中亦称 Text2SQL + LM）和手写基线在示例查询 “Provide information about the races held on Sepang International Circuit.” 上的结果。RAG 基线只能提供部分比赛的信息，因为大多数相关比赛没有被检索到。另一方面，Text2SQL + LM 基线不能利用来自

<!-- 原 PDF 第 5 页 -->

表 1：TAG 基准查询的准确率与执行时间（ET），对全部查询以及每种查询类型取平均。TAG 显著提高答案质量，同时达到最快或接近最快的执行时间。脚注 1：由于不测量准确率，精确匹配排除聚合查询。列顺序为：总体，然后是基于匹配、比较、排序、聚合。每个分块含 Exact Match（越高越好）和 ET（秒，越低越好）。聚合列的 Exact Match 为 N/A。

| 方法 | 总体 Exact Match | 总体 ET (s) | 匹配 Exact Match | 匹配 ET | 比较 Exact Match | 比较 ET | 排序 Exact Match | 排序 ET | 聚合 Exact Match | 聚合 ET |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| Text2SQL | 0.17 | 5.63 | 0.20 | 4.72 | 0.20 | 4.01 | 0.10 | 7.26 | N/A | 6.53 |
| RAG | 0.00 | 3.23 | 0.00 | 3.73 | 0.00 | 2.29 | 0.00 | 2.01 | N/A | 4.89 |
| Retrieval + LM Rank | 0.02 | 4.82 | 0.00 | 6.20 | 0.05 | 4.19 | 0.00 | 3.42 | N/A | 5.46 |
| Text2SQL + LM | 0.13 | 9.08 | 0.10 | 11.25 | 0.10 | 3.89 | 0.20 | 11.80 | N/A | 9.38 |
| Hand-written TAG | 0.55 | 2.94 | 0.60 | 1.70 | 0.65 | 5.05 | 0.40 | 2.50 | N/A | 2.50 |

**图 2 见原 PDF。** 查询为 “Provide information about the races held on Sepang International Circuit”。RAG 的回答只列出部分马来西亚大奖赛年份，并给出地点 Kuala Lumpur, Malaysia。Text2SQL + LM 回答说所给数据点不包含关于该赛道比赛的具体信息，然后凭一般知识说该赛道在 1999 到 2017 年举办过马来西亚大奖赛。手写 TAG 给出 1999 至 2017 年各届日期与轮次，例如 1999: October 17 (15th round)，直到 2017: October 1 (15th round)。

图 2：聚合结果示例。RAG 基线对查询给出不完整的答案，而 Text2SQL + LM 未能使用数据库中的任何数据来回答问题。手写 TAG 基线给出最充分的答案，综合了数据库中的数据与它自己的世界知识。

表 2：在需要知识或推理的查询上取平均的 TAG 基准结果。TAG 在知识和推理两类查询上一致地表现良好，精确匹配准确率都高于 50%。

| 方法 | 知识 Exact Match | 知识 ET (s) | 推理 Exact Match | 推理 ET (s) |
| --- | ---: | ---: | ---: | ---: |
| Text2SQL | 0.20 | 5.23 | 0.10 | 5.52 |
| RAG | 0.00 | 2.73 | 0.00 | 2.58 |
| Retrieval + LM Rank | 0.03 | 4.97 | 0.00 | 3.87 |
| Text2SQL + LM | 0.10 | 10.27 | 0.20 | 6.39 |
| Hand-written TAG | 0.53 | 3.50 | 0.60 | 2.24 |

DBMS 的信息，只依赖参数知识，并且不提供进一步分析。手写基线提供了 1999 年到 2017 年在雪邦国际赛道（Sepang International Circuit）举行的全部比赛的充分摘要。我们在基准提供的其他聚合查询上观察到类似趋势，初步结果突出了 TAG 系统成功聚合大量数据以提供有信息量的答案的潜力。我们把定量分析留给未来工作。

## 5 相关工作

**Text2SQL。** 使用 LM 的 Text2SQL 在先前工作中已被广泛探索。WikiSQL [33]、Spider [29] 和 BIRD [17] 都是流行的跨领域 Text2SQL 数据集。这些数据集包含许多领域的结构化数据，并在其上评测把自然语言查询转换成 SQL 的任务。然而，这一方向并不利用超出 SQL 生成的模型能力，把需要静态数据源之外的推理或知识的查询排除在范围之外。

**检索增强生成。** 检索增强生成（RAG）[16] 使 LM 能够超出其参数知识，延伸到大规模文本集合。SQuAD [22] 和 HotpotQA [27] 分别聚焦单文档和多文档来源上的问答。稠密表检索（DTR）模型 [11] 把 RAG 扩展到表格数据，嵌入表格上下文以检索与查询相关的单元格和行。连接感知的表检索 [6] 给 DTR 模型增加一个表—表相似度分数项，以改进涉及连接表的复杂查询上的性能。与先前的 RAG 工作相对，TAG 模型通过在查询执行步骤中利用 LM 能力，并允许 DBMS 操作对大量数据做精确计算，涵盖用户对其数据所拥有的更大查询领域。

**半结构化数据上的自然语言查询。** 先前工作探索了半结构化数据源中表实体与非结构化实体字段之间的关系信息。STaRK [25] 在半结构化知识库（SKB）上评测表检索方法，包括结构性和非结构性信息。SUQL [20] 处理对话搜索任务，其中 LM 被用作语义解析器，以处理用户在混合数据上的查询中的非结构化成分。虽然这些工作主要聚焦半结构化数据上的自然语言搜索查询，我们寻求探索更广泛的查询范围，为搜索和查找之外的任务利用更多 LM 能力。

<!-- 原 PDF 第 6 页 -->

**智能体式数据助手。** 近期工作探索了把 LM 智能体作为数据助手 [12]。Spider2-V [4] 探索多模态智能体在涉及代码生成和 GUI 控制的任务中的表现。尽管我们把 TAG 模型可处理地定义为一轮 $\mathrm{syn}$、$\mathrm{exec}$ 和 $\mathrm{gen}$ 函数，未来工作可以探索在智能体循环中扩展它。

## 6 结论

在本工作中，我们提出表增强生成（TAG），作为在数据库上回答自然语言问题的统一模型。我们开发基准来研究两类重要查询：需要世界知识的查询，以及需要语义推理能力的查询。我们的系统评测确认，基线方法无法在这些任务上取得有意义的进展。然而，手写 TAG 流水线可以达到高出至多 65% 的准确率，表明构建 TAG 系统有实质性的研究机会。

## 7 致谢

本研究过去得到 Stanford DAWN 项目和 Berkeley Sky Computing Lab 的附属成员与支持者的支持，包括 Accenture、AMD、Anyscale、Cisco、Google、IBM、Intel、Meta、Microsoft、Mohamed Bin Zayed University of Artificial Intelligence、NVIDIA、Samsung SDS、SAP、VMware，以及一项 Sloan Fellowship。本材料中表达的任何意见、发现、结论或建议都属于作者，不一定反映资助方的观点。

## 参考文献

[1] [n. d.]. BigQuery 中的 AI 与 ML 介绍 | Google Cloud. https://cloud.google.com/bigquery/docs/bqml-introduction

[2] 2024. https://ai.meta.com/blog/meta-llama-3-1/

[3] Raviteja Anantha, Svitlana Vakulenko, Zhucheng Tu, Shayne Longpre, Stephen Pulman, and Srinivas Chappidi. 2021. 开放域问答经由问题改写走向对话. In Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies. Association for Computational Linguistics, Online, 520–534. https://doi.org/10.18653/v1/2021.naacl-main.44

[4] Ruisheng Cao, Fangyu Lei, Haoyuan Wu, Jixuan Chen, Yeqiao Fu, Hongcheng Gao, Xinzhuang Xiong, Hanchong Zhang, Yuchen Mao, Wenjing Hu, Tianbao Xie, Hongshen Xu, Danyang Zhang, Sida Wang, Ruoxi Sun, Pengcheng Yin, Caiming Xiong, Ansong Ni, Qian Liu, Victor Zhong, Lu Chen, Kai Yu, and Tao Yu. 2024. Spider2-V：多模态智能体距离自动化数据科学与工程工作流还有多远？ arXiv:2407.10956 [cs.AI] https://arxiv.org/abs/2407.10956

[5] Lingjiao Chen, Matei Zaharia, and James Zou. 2023. FrugalGPT：如何在降低成本并提高性能的同时使用大语言模型. http://arxiv.org/abs/2305.05176 arXiv:2305.05176 [cs].

[6] Peter Baile Chen, Yi Zhang, and Dan Roth. 2024. 表检索是已解决的问题吗？探索连接感知的多表检索. arXiv:2404.09889 [cs.IR] https://arxiv.org/abs/2404.09889

[7] Matthijs Douze, Alexandr Guzhva, Chengqi Deng, Jeff Johnson, Gergely Szilvasy, Pierre-Emmanuel Mazaré, Maria Lomeli, Lucas Hosseini, and Hervé Jégou. 2024. Faiss 库. (2024). arXiv:2401.08281 [cs.LG]

[8] Xi Fang, Weijie Xu, Fiona Anting Tan, Jiani Zhang, Ziqing Hu, Yanjun Qi, Scott Nickleach, Diego Socolinsky, Srinivasan Sengamedu, and Christos Faloutsos. 2024. 表格数据上的大语言模型：预测、生成与理解——一项综述. https://doi.org/10.48550/arXiv.2402.17944 arXiv:2402.17944 [cs].

[9] Luyu Gao, Zhuyun Dai, Panupong Pasupat, Anthony Chen, Arun Tejasvi Chaganty, Yicheng Fan, Vincent Y. Zhao, Ni Lao, Hongrae Lee, Da-Cheng Juan, and Kelvin Guu. 2023. RARR：用语言模型研究并修订语言模型所说的话. https://doi.org/10.48550/arXiv.2210.08726 arXiv:2210.08726 [cs].

[10] Joe Hellerstein, Christopher Ré, Florian Schoppmann, Daisy Zhe Wang, Eugene Fratkin, Aleksander Gorajek, Kee Siong Ng, Caleb Welton, Xixuan Feng, Kun Li, and Arun Kumar. 2012. MADlib 分析库，或 MAD 技能，即 SQL. https://doi.org/10.48550/arXiv.1208.4165 arXiv:1208.4165 [cs].

[11] Jonathan Herzig, Thomas Müller, Syrine Krichene, and Julian Martin Eisenschlos. 2021. 通过稠密检索在表上做开放域问答. arXiv:2103.12011 [cs.CL] https://arxiv.org/abs/2103.12011

[12] Xueyu Hu, Ziyu Zhao, Shuang Wei, Ziwei Chai, Qianli Ma, Guoyin Wang, Xuwu Wang, Jing Su, Jingjing Xu, Ming Zhu, Yao Cheng, Jianbo Yuan, Jiwei Li, Kun Kuang, Yang Yang, Hongxia Yang, and Fei Wu. 2024. InfiAgent-DABench：在数据分析任务上评测智能体. arXiv:2401.05507 [cs.CL] https://arxiv.org/abs/2401.05507

[13] Omar Khattab, Arnav Singhvi, Paridhi Maheshwari, Zhiyuan Zhang, Keshav Santhanam, Sri Vardhamanan, Saiful Haq, Ashutosh Sharma, Thomas T. Joshi, Hanna Moazam, Heather Miller, Matei Zaharia, and Christopher Potts. 2023. DSPy：把声明式语言模型调用编译成自我改进的流水线. https://doi.org/10.48550/arXiv.2310.03714 arXiv:2310.03714 [cs].

[14] Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E. Gonzalez, Hao Zhang, and Ion Stoica. 2023. 用 PagedAttention 为大语言模型服务做高效内存管理. arXiv:2309.06180 [cs.LG] https://arxiv.org/abs/2309.06180

[15] Kenton Lee, Ming-Wei Chang, and Kristina Toutanova. 2019. 面向弱监督开放域问答的潜在检索. In Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics. Association for Computational Linguistics, Florence, Italy, 6086–6096. https://doi.org/10.18653/v1/P19-1612

[16] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, and Douwe Kiela. 2021. 面向知识密集型 NLP 任务的检索增强生成. http://arxiv.org/abs/2005.11401 arXiv:2005.11401 [cs].

[17] Jinyang Li, Binyuan Hui, Ge Qu, Jiaxi Yang, Binhua Li, Bowen Li, Bailin Wang, Bowen Qin, Rongyu Cao, Ruiying Geng, Nan Huo, Xuanhe Zhou, Chenhao Ma, Guoliang Li, Kevin C. C. Chang, Fei Huang, Reynold Cheng, and Yongbin Li. 2023. LLM 已经能充当数据库接口了吗？一个面向大规模数据库锚定 Text-to-SQL 的大基准. http://arxiv.org/abs/2305.03111 arXiv:2305.03111 [cs].

[18] Chunwei Liu, Matthew Russo, Michael Cafarella, Lei Cao, Peter Baille Chen, Zui Chen, Michael Franklin, Tim Kraska, Samuel Madden, and Gerardo Vitagliano. 2024. 一个用于优化 AI 工作负载的声明式系统. http://arxiv.org/abs/2405.14696 arXiv:2405.14696 [cs].

[19] Shu Liu, Asim Biswal, Audrey Cheng, Xiangxi Mo, Shiyi Cao, Joseph E. Gonzalez, Ion Stoica, and Matei Zaharia. 2024. 在关系工作负载中优化 LLM 查询. https://doi.org/10.48550/arXiv.2403.05821 arXiv:2403.05821 [cs].

[20] Shicheng Liu, Jialiang Xu, Wesley Tjangnaka, Sina J. Semnani, Chen Jie Yu, and Monica S. Lam. 2024. SUQL：用大语言模型在结构化与非结构化数据上做对话搜索. https://doi.org/10.48550/arXiv.2311.09818 arXiv:2311.09818 [cs].

[21] Liana Patel, Siddharth Jha, Carlos Guestrin, and Matei Zaharia. 2024. LOTUS：用 LLM 在非结构化与结构化数据表上启用语义查询. https://doi.org/10.48550/arXiv.2407.11418 arXiv:2407.11418 [cs].

[22] Pranav Rajpurkar, Jian Zhang, Konstantin Lopyrev, and Percy Liang. 2016. SQuAD：用于文本机器理解的 10 万以上问题. arXiv:1606.05250 [cs.CL] https://arxiv.org/abs/1606.05250

[23] Liang Wang, Nan Yang, Xiaolong Huang, Binxing Jiao, Linjun Yang, Daxin Jiang, Rangan Majumder, and Furu Wei. 2024. 通过弱监督对比预训练得到的文本嵌入. arXiv:2212.03533 [cs.CL] https://arxiv.org/abs/2212.03533

[24] WilliamDAssafMSFT. 2023. PREDICT (Transact-SQL) - SQL 机器学习. https://learn.microsoft.com/en-us/sql/t-sql/queries/predict-transact-sql?view=sql-server-ver16

[25] Shirley Wu, Shiyu Zhao, Michihiro Yasunaga, Kexin Huang, Kaidi Cao, Qian Huang, Vassilis N. Ioannidis, Karthik Subbian, James Zou, and Jure Leskovec. 2024. STaRK：在文本与关系知识库上对 LLM 检索做基准测试. https://doi.org/10.48550/arXiv.2404.13207 arXiv:2404.13207 [cs].

[26] Navid Yaghmazadeh, Yuepeng Wang, Isil Dillig, and Thomas Dillig. 2017. SQLizer：从自然语言合成查询. Proc. ACM Program. Lang. 1, OOPSLA (Oct. 2017), 63:1–63:26. https://doi.org/10.1145/3133887

<!-- 原 PDF 第 7 页 -->

[27] Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W. Cohen, Ruslan Salakhutdinov, and Christopher D. Manning. 2018. HotpotQA：面向多样、可解释的多跳问答的数据集. arXiv:1809.09600 [cs.CL] https://arxiv.org/abs/1809.09600

[28] Tao Yu, Zifan Li, Zilin Zhang, Rui Zhang, and Dragomir Radev. 2018. TypeSQL：基于知识、类型感知的神经 Text-to-SQL 生成. https://doi.org/10.48550/arXiv.1804.09769 arXiv:1804.09769 [cs].

[29] Tao Yu, Rui Zhang, Kai Yang, Michihiro Yasunaga, Dongxu Wang, Zifan Li, James Ma, Irene Li, Qingning Yao, Shanelle Roman, Zilin Zhang, and Dragomir Radev. 2019. Spider：一个用于复杂与跨领域语义解析及 Text-to-SQL 任务的大规模人工标注数据集. arXiv:1809.08887 [cs.CL] https://arxiv.org/abs/1809.08887

[30] Eric Zelikman, Yuhuai Wu, Jesse Mu, and Noah D. Goodman. 2022. STaR：用推理来自举推理. https://doi.org/10.48550/arXiv.2203.14465 arXiv:2203.14465 [cs].

[31] John M. Zelle and Raymond J. Mooney. 1996. 用归纳逻辑编程学习解析数据库查询. In Proceedings of the thirteenth national conference on Artificial intelligence - Volume 2 (AAAI’96). AAAI Press, Portland, Oregon, 1050–1055.

[32] Bin Zhang, Yuxiao Ye, Guoqing Du, Xiaoru Hu, Zhishuai Li, Sun Yang, Chi Harold Liu, Rui Zhao, Ziyue Li, and Hangyu Mao. 2024. 对大语言模型 Text-to-SQL 能力做基准测试：一项综合评测. http://arxiv.org/abs/2403.02951 arXiv:2403.02951 [cs].

[33] Victor Zhong, Caiming Xiong, and Richard Socher. 2017. Seq2SQL：用强化学习从自然语言生成结构化查询. CoRR abs/1709.00103 (2017).

<!-- 原 PDF 第 8 页 -->

## 附录 A 示例查询

我们详细说明为本基准对 BIRD 查询所做的修改。每条查询都被修改成需要 LM 知识或推理才能回答。示例查询如下。

**基于匹配**

原始 BIRD 查询：经度最高的那所学校提供的年级跨度是什么？（What is the grade span offered in the school with the highest longitude?）

修改后的查询：在属于 “Silicon Valley” 地区的城市中，经度最高的那所学校提供的年级跨度是什么？（What is the grade span offered in the school with the highest longitude in cities in that are part of the ’Silicon Valley’ region?）

分析：这条查询被修改成需要 LM 知道哪些城市位于加利福尼亚的硅谷地区，这一信息在数据源中不可得。

**比较**

原始 BIRD 查询：在身高超过 180 的球员中，有多少人的凌空抽射（volley）分数超过 70？（Among the players whose height is over 180, how many of them have a volley score of over 70?）

修改后的查询：在身高超过 180 的球员中，有多少人的凌空抽射分数超过 70，并且比 Stephen Curry 更高？（Among the players whose height is over 180, how many of them have a volley score of over 70 and are taller than Stephen Curry?）

分析：这条查询被修改成需要 LM 知道 Stephen Curry 有多高。

**排序**

原始 BIRD 查询：人气最高的前 5 篇帖子的标题是什么？（What are the titles of the top 5 posts with the highest popularity?）

修改后的查询：在人气最高的 5 篇帖子中，按从最技术性到最不技术性的顺序列出它们的标题。（Of the 5 posts wih highest popularity, list their titles in order of most technical to least technical. 原文 “wih” 按 PDF 保留。）

分析：这条查询被修改成需要 LM 对文本字段（帖子标题）进行推理。

**聚合**

原始 BIRD 查询：写出标题为 “How does gentle boosting differ from AdaBoost?” 的帖子上的全部评论。

修改后的查询：总结标题为 “How does gentle boosting differ from AdaBoost?” 的帖子上的评论，以回答原始问题。

分析：这条查询被修改成依赖 LM 对文本评论字段的推理来提供摘要。

## 附录 B LM 提示

我们总结与指令调优的 Llama-3.1 80B 一起用于查询合成和答案生成的提示。（附录此处写 80B；正文实验设定写的是 Llama-3.1-70B-Instruct。）

### B.1 查询合成

对查询合成步骤，在我们的情形中是 Text2SQL 步骤，我们使用与原始 BIRD 基准相同的表模式编码和 LM 提示。下面给出查询合成的一个示例提示。

```
-- Example Prompt for Query Synthesis
CREATE TABLE frpm
(
CDSCode TEXT not null primary key ,
Academic Year TEXT null ,
...
)

CREATE TABLE satscores
(
...
AvgScrRead INTEGER null ,
AvgScrMath INTEGER null ,
...
)
```

<!-- 原 PDF 第 9 页 -->

```
CREATE TABLE schools
(
...
District TEXT not null ,
School TEXT null ,
...
)

-- External Knowledge: None
-- Using valid SQLite and understading External Knowledge , answer the following questions for the tables provided above.
-- Among the schools with the average score in Math over 560 in the SAT test , how many schools are in the bay area?
SELECT
```

提示中的英文问题译为：在 SAT 考试中数学平均分超过 560 的学校里，有多少所位于湾区？注释行中的 “understading” 按 PDF 原文保留。

### B.2 答案生成

在 Text2SQL + LM 和 RAG 基线上，答案生成步骤要求 LM 用上下文中提供的行来回答用户问题。我们对聚合查询使用单独的提示，而基于匹配、比较和排序共享同一提示。两种提示如下。

面向基于匹配、比较和排序查询的答案生成示例提示，大意是：你将得到一组数据点和一个问题。用这些数据点回答问题。你的答案必须是一个可以在 Python 中求值的值列表。以 `[value1, value2, ..., valueN]` 的格式回答。如果你无法回答，回答 `[]`。只回答值的列表，不要其他内容。如果值是字符串，必须用双引号括起来。随后是 Data Point 1、Data Point 2，字段包括 School 与 AvgScrMath，问题为：Among the schools with the average score in Math over 560 in the SAT test, how many schools are in the bay area?

面向聚合查询的答案生成示例提示，大意是：你将得到一组数据点和一个问题。用这些数据点回答问题。如果值是字符串，必须用双引号括起来。数据点字段包括 PostId 与 Text。问题为：Summarize the comments made on the post titled "How does gentle boosting differ from AdaBoost?" to answer the original question.

## 附录 C 手写流水线

我们使用 LOTUS 包来构造手写 TAG 流水线。对基准中的每条查询，用 Python 写了一条流水线，由一系列 dataframe 变换与过滤以及 LOTUS 语义 LM 算子组成。示例流水线如下。

基于匹配：查询为硅谷地区城市中经度最高学校的年级跨度。代码读取 `california_schools/schools.csv`，对唯一城市调用 `sem_filter("{City} is a city in the Silicon Valley region")`，再按经度绝对值降序取第一行，返回 `GSoffered`。

<!-- 原 PDF 第 10 页 -->

排序：查询为人气最高的 5 篇帖子，按从最技术性到最不技术性列出标题。代码读取 `codebase_community/posts.csv`，按 `ViewCount` 降序取前 5，再调用 `sem_topk("What {Title} is most technical ?", 5)`，返回标题列表。

聚合：查询为总结标题为 “How does gentle boosting differ from AdaBoost?” 的帖子上的评论。代码读取帖子与评论，按标题过滤后在 `Id` 与 `PostId` 上合并，再调用 `sem_agg("Summarize the comments", all_cols=True)`，返回 `_output[0]`。

<!-- 译完 -->
