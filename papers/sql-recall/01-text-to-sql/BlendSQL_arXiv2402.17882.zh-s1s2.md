# BlendSQL: A Scalable Dialect for Unifying Hybrid Question Answering in Relational Algebra

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`BlendSQL_arXiv2402.17882.pdf`。

## Abstract 摘要

许多现有的混合问答端到端系统，可以归结为一种“提示然后祈祷”（prompt-and-pray）的范式：用户对达成最终结果所用的中间推理步骤，控制有限，也缺乏洞察。此外，由于许多基于 Transformer 的 LLM 存在上下文长度限制，在零样本设定下，往往不能合理地期望把完整的结构化与非结构化上下文都放进给定提示，少样本设定就更是如此。我们提出 BLENDSQL，它是 SQLite 的超集，作为一种统一方言，用来编排跨越非结构化数据与结构化数据的推理。对于涉及多跳推理的混合问答任务，我们把完整的分解推理路线图编码为一条可解释的 BLENDSQL 查询。值得注意的是，我们表明 BLENDSQL 可以扩展到大规模数据集，并在少用 35% 提示词元的同时提升端到端系统的性能。代码已公开，并可按包安装：github.com/parkervg/blendsql 。

## 1 Introduction 引言

**问题分解。** 在微调和上下文学习两种设定中，已有研究表明：为复杂问题生成显式的中间步骤可以提高准确率。在题为 “Scratchpad” 的框架中，Nye et al. (2021) 揭示：在微调语言模型以生成执行输出时，预测完整的执行轨迹会带来更好的结果。更近的工作表明，提示 LLM 在生成最终答案之前，把复杂问题分解为更小的推理步骤，可以改善结果（Wei et al., 2022; Yao et al., 2023; Wang et al., 2022）。然而，这些方法在核心上使用自然语言作为中间推理表示。借助 BLENDSQL，我们认为自然语言本身作为中间推理表示天生是有损且有歧义的。图 1 给出一个 OTT-QA 开发集示例的 BLENDSQL 表示。相反，把问题分解为类似 SQL 的语法，我们就可以利用关系代数的组合性（Codd, 1970），获得更确定的推理能力，以及更好的中间步骤可解释性。

**智能体。** 先前工作探索了智能体（agents）：一种基于专家的框架，主任务被拆成若干部分，由各个智能体或专家分别完成（Parisi et al., 2022; Liang et al., 2022; Schick et al., 2023; Shen et al., 2023; Liang et al., 2023; Lu et al., 2023）。此外，这些工作依赖于“路由器”或“规划器”的存在，它们理解给定任务并将其拆成更小的任务。尽管基于规则的路由器已被广泛使用，LLM 对复杂文本的泛化能力使其可以被用作规划器。作为规划器的 LLM 处理输入，并生成包含下列内容的文本：子任务列表（Shen et al., 2023）、从给定集合中选用哪些智能体、这些智能体的输入是什么（Schick et al., 2023; Qin et al., 2023; Cheng et al., 2023），以及期望从智能体得到何种响应（Parisi et al., 2022）。由于智能体所执行任务的范围很窄，近期工作主要聚焦该框架的规划器组件。为此，利用 LLM 的上下文学习能力（Shen et al., 2023; Qin et al., 2023），或微调规划器 LLM（Parisi et al., 2022; Schick et al., 2023; Patil et al., 2023; Tang et al., 2023; Wang et al., 2023; Lu et al., 2023），是两种主要方法。此外，已有工作使用 LLM 的上下文学习能力来创建数据集（Patil et al., 2023; Tang et al., 2023）。BLENDSQL 中的解析器充当规划器，并生成用于回答输入问题的 API 或 Ingredients。然而，它与先前工作不同：它不止生成复杂问题分解的单一字符串表示，而是用稳健且复杂的抽象语法树（abstract syntax tree, AST）结构来简化智能体框架，并把这些结构编码进单个字符串。还需要指出，BLENDSQL 不只是用形式构造重写输入陈述（Lu et al., 2021; Wu et al., 2022），它还利用参考数据库、输入提示以及语言模型的内部知识来补充信息。此处，一个智能体或专家可以是 Python 脚本、API 调用、工具或语言模型中的任何一种。

**Text-to-SQL。** 在广泛使用的 text-to-SQL 数据集 Spider（Yu et al., 2018）上，许多工作在少样本或零样本设定下展示了令人印象深刻的性能（Gao et al., 2023; Pourreza and Rafiei, 2023; Dong et al., 2023; Liu et al., 2023）。即便在不以 text-to-SQL 为重点的设定中，现有工作也详述了 SQL 这类常见且被充分理解的中间表示对其他推理任务的有效性。Hu et al. (2022) 把对话状态跟踪（dialogue state tracking, DST）框定为 text-to-SQL 任务：把 MultiWOZ（Budzianowski et al., 2018）中的领域和槽位编码为序列化的数据库格式，并以 SQL 作为中间表示，相对“传统的”键值式预测格式显示出显著改进。

**混合问答。** 与 text-to-SQL 不同，混合问答涉及一个隐式决策：访问表格数据、非结构化数据，或二者兼有（Chen et al., 2020; Zhu et al., 2021; Chen et al., 2021）。Li et al. (2021) 通过在端到端模型与生成中间 SQL 表示的解析器之间做路由，使这一决策更加显式。他们的实现把二者框定为相互隔离的专用系统，无法彼此传递信息。就本文范围而言，我们把混合问答（Hybrid Question Answering）定义为：使用表格与非结构化多模态内容的语料来回答问题。尽管这种多模态内容可以涵盖文本、图像、音频和视频，本文的主要焦点是非结构化文本与表格数据的结合。把这一过程适配到图像等其他格式的可能性，也在附录 C 中讨论。一项先前工作 UniK-QA（Oguz et al., 2022）提议把结构化表格数据转换成非结构化文本数据。我们的工作方向相反，而是把所有非结构化文本数据转换成表格数据。经验上，UniK-QA 使用一个知识库到文本（KB-to-text）的预处理模型，在若干知识库问答基准上有所改进。例如，对于 UniK-QA 论文中提到的 KB-to-text 模型，不同实体之间的关系被假定具有简单的三元组表示 `<subj, pred, obj>`，其中 pred（谓词）由表名定义该关系。然而，`<subj>` 与 `<obj>` 之间的关系常常复杂地嵌入在异质信息源中（例如音频、文档或表的列名），这就会要求投入更多努力去开发专门的 KB-to-text 模型。

**神经–符号框架。** 与我们的工作最相似的是 Cheng et al. (2023) 提出的 BINDER 方法，它把 LLM 推理集成到 SQL 和 Python 等符号语言中。虽然我们从其用于推理的神经–符号框架获得启发，BLENDSQL 在以下方面有所不同。（1）我们创建了专门面向 SQL 的 API，能够在包含非结构化内容的多表数据库上推理，并能够执行和优化含有 JOIN 语句、别名、条件表表达式以及大多数其他 SQLite 操作的查询。（2）我们支持按照数据库模式进行约束解码。（3）我们这样设计 API，使用户能够自己轻松创建任意数量的自定义函数，并在 BLENDSQL 脚本中使用。

### 1.1 Main Contributions 主要贡献

概括而言，我们做出如下贡献。

- 据我们所知，我们首次提议把混合问答的上下文框定为一个关系数据库。
- 我们引入一种新的开源查询语言 BLENDSQL，用以编排并优化跨越 SQL 逻辑与 LLM 推理的混合函数。
- 我们表明，仅凭少量上下文示例，BLENDSQL 就可以在少用 35% 词元、且不直接访问非结构化上下文的情况下，优于端到端方法。

## 2 BLENDSQL: Overview BLENDSQL 概述

我们把 BLENDSQL 实现为 SQLite 关系数据库管理系统（RDBMS）的超集。一条执行后的 BLENDSQL 脚本返回一个 smoothie 对象作为输出，其中包含最终结果以及所采取的中间推理步骤。要制作 smoothie，需要一些 ingredients 和一个 blender。我们在下文描述这些组件。

### 2.1 Blender vs. Parser Blender 与解析器

我们用 “blender” 一词指称那个 LLM：它接收提示，用以执行 BLENDSQL 脚本中的每个 ingredient 函数。在执行之前，“parser”（解析器）接收一组少样本示例，并在给定问题和数据库上下文时生成一条 BLENDSQL 查询。在核心实验中，我们使用 GPT-4-0613（Achiam et al., 2023）同时作为 blender 和解析器。

### 2.2 Ingredients 成分

Ingredients 是 BLENDSQL 脚本的核心。它们是子程序，用来把某些逻辑操作交给基于 LLM 的函数，并用双花括号（“{{” 和 “}}”）表示。BLENDSQL 语法被表示为一套解析表达式文法，通过 PyParsing（McGuire, 2007）实现。与普通 SQL 一样，ingredient 调用是完全递归的，传给某个调用的上下文可以包含调用其他 BLENDSQL ingredient 的操作。

**LLMMap。** LLMMap 这一 ingredient 是一元标量函数，很像标准 SQLite 中的 LENGTH 或 ABS。该操作的输出随后被设为临时表中的一个新列，供更宽的查询稍后使用。具体而言，它以字符串格式 “table::column” 接受表和列参数。然后它创建一个新列 `c′`，其映射值 `v′` 是该标量函数的输出。以 `n_c` 作为目标列 `c` 中的值的个数，我们有：

`V = {v_i, ∀i ∈ {1, ..., n_c}}`

`f_map(V) → {v′_1, ..., v′_{n_c}}`

例如，图 2 描绘了正在起作用的 LLMMap。对每个值，都会提示一个 LLM 回答问题：“Is this a team event?” 鉴于该列中团队项目的记法多种多样（“team event”、“4x100 medley relay” 等），很难通过纯字符串解析为整张表写出通用的 SQLite 逻辑。LLMMap 则实现一种通用解法，根据值的语义所指来变换这些值。

**LLMQA。** LLMQA 这一 ingredient 是一个聚合函数，把表子集 T 变换为单个标量值 `v′`：

`f_qa(T) → v′`

如图 1 所示，该 ingredient 可以用 options 参数加以限制，从而保证函数输出是特定列 `c` 中的一个已有值，`v′ ∈ {v_i, ∀i ∈ {1, ..., n_c}}`。这种约束解码使用 guidance 实现，它操纵 OpenAI API 中的 `logit_bias` 参数。在图 2 中，LLMQA 函数接收一段非结构化文档上下文，以及问题：“Which NBA season was suspended due to COVID-19?” 此外，它还接收一组列值，用来约束语言模型的生成。对于事实验证任务，我们实现了该 ingredient 的一个修改版本 LLMValidate，它始终返回 true 或 false 布尔值。

**LLMJoin。** LLMJoin 这一 ingredient 在一对值集合 `V_1` 与 `V_2` 之间创建自定义映射。该映射随后被用来创建一张辅助表，以执行 SQL 的 INNER JOIN 操作：

`f_join(V_1, V_2) → {(v1′_1, v2′_1), ..., (v1′_{n_{v1}}, v2′_{n_{v2}})}`

当不存在适当的外键、但仍可能有某种语义对齐时，这一 ingredient 尤其有用。在图 2 中，“joshua fields” 与 “josh fields (pitcher)” 指向同一所指。我们用 LLMJoin 对齐这两个不同的指称，实际上执行一种实体链接。

表 1：来自一个 HybridQA 示例的数据库配置示例，与 3 对齐【抽取不清：“aligned with 3” 的指代在本节抽取中未写全】。上方的表 `w` 包含与维基百科页面中某张表相对应的结构化数据；下方的表 `documents` 包含维基百科页面文章内容中的非结构化数据，并用 FTS5 建立索引。抽取到的单元格如下，列与单元格边界有粘连：

| name | position | school |
| --- | --- | --- |
| joshua fields | right-handed pitcher | university of georgia |
| dennis raben | outfielder | university of miami |
| matt jensen | second basemen | clovis east high school |

| title | content |
| --- | --- |
| kenn kasparek | kenn anthony kasparek ( born 1985-9-23 ) is... |
| pitcher in baseball | the pitcher is the player who throws the baseball from... |
| josh fields (pitcher) | joshua david fields ( born 1985-8-19 ) is an american professional baseball pitcher... |

### 2.3 Query Optimizations 查询优化

在可能的情况下，我们先在子查询中执行全部 SQL 谓词，并把它们的输出赋给一张临时会话表。由于原生 SQLite 操作相对便宜，我们确保昂贵的、基于 LLM 的 ingredient 函数所接收的数据不多于、也不少于生成忠实执行输出所需的子集。如下文所示，我们只把 `w` 中满足 `w.school = 'university of georgia'` 的行子集传给基于 LLM 的 ingredient（原文写 “in 3”）。我们用一套广泛的测试套件验证这些优化。

原文称该优化 “as demonstrated below”，但对应示例查询未出现在本节抽取文本中。后页图注 Figure 3 与同一 University of Georgia / Seattle Mariners（2008）示例及表 1 对齐，图中的 BLENDSQL 程序本身未被抽出。抽取在此截断。
