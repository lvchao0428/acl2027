# Spider 2.0: Evaluating Language Models on Real-World Enterprise Text-to-SQL Workflows

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`Spider2.0_arXiv2411.07763.pdf`。

## Abstract 摘要

真实企业中的 text-to-SQL 工作流常常涉及分布在多种数据库系统上的复杂云端或本地数据、多种方言下的多条 SQL 查询，以及从数据变换到分析的多样操作。我们提出 Spider 2.0，一个评测框架，包含 632 个源自企业级数据库用例的真实 text-to-SQL 工作流问题。Spider 2.0 中的数据库来自真实数据应用，常常包含超过 1,000 个列，并存储在 BigQuery、Snowflake 等本地或云数据库系统中。我们表明，求解 Spider 2.0 中的问题经常需要理解并检索数据库元数据（database metadata）、方言文档（dialect documentation），乃至项目级代码库（project-level codebases）。这一挑战要求模型与复杂的 SQL 工作流环境交互、处理极长的上下文、进行精细推理，并生成包含多样操作、常常超过 100 行的多条 SQL 查询，这远远超出传统 text-to-SQL 挑战。我们的评测表明，基于 o1-preview，我们的代码智能体框架（code agent framework）仅成功求解 21.3% 的任务，相比之下在 Spider 1.0 上为 91.2%，在 BIRD 上为 73.0%。Spider 2.0 上的结果表明：尽管语言模型在代码生成上——尤其是在此前的 text-to-SQL 基准上——已展现出显著性能，但要在真实企业使用中达到足够的性能，仍需大幅改进。在 Spider 2.0 上取得进展，代表着走向面向真实企业场景的智能、自主代码智能体的关键步骤。我们的代码、基线模型与数据可在 spider2-sql.github.io 获取。

## 1 Introduction 引言

自动代码生成可以作为人与数据之间的关键桥梁，帮助个人利用复杂数据完成困难或单调的任务。现有数据中有相当一部分存储在关系数据库中，SQL 是促成人类与这些数据交互的必要接口。在这一背景下，语义解析（semantic parsing）或 text-to-SQL（Dahl et al., 1994; Zelle & Mooney, 1996; Zettlemoyer & Collins, 2005; Li & Jagadish, 2014; Zhong et al., 2017; Yu et al., 2018）是一项重要技术，协助数据分析师执行常规查询、编排数据工作流并完成高级商业智能（business intelligence），从而显著减少重复的人力劳动并减轻程序员的负担。

大语言模型（large language models, LLMs）已展现出出色的代码生成能力（Chen et al., 2021; Austin et al., 2021），尤其是把自然语言问题转换为 SQL 查询。值得注意的是，基于 GPT-4 的方法在经典基准 Spider 1.0（Yu et al., 2018）和 BIRD（Li et al., 2024b）上的执行准确率（execution accuracy）分别达到 91.2% 和 73.0%。

尽管 LLM 在这些数据集上表现优异，它们使用的往往是表和列都很少的非工业数据库，SQL 与问题较为简单，达不到真实世界的复杂度，也忽略了多样的 SQL 方言（SQL dialects）。相比之下，真实世界的数据分布在多种多样的数据库系统中，每种系统都有自己独特的 SQL 方言，从而带来广泛的 SQL 语法与函数。此外，这些企业级应用数据库具有规模庞大的模式（schema），列数以千计，并带有复杂的嵌套结构。而且，真实的 text-to-SQL 工作流需要利用项目代码库、外部知识与多种上下文，分多步构造复杂 SQL 查询、完成各种操作，并搭建完整的数据工程流水线（data engineering pipeline）。这包括为分析而清洗和组织数据的数据整理（data wrangling）、重构并增强数据的数据变换（data transformation），以及提取洞见以支持决策、推动战略举措的数据分析（data analytics）。这些复杂性表明，迫切需要一个更贴近真实情况的企业级基准。

我们提出 Spider 2.0，一个反映真实数据工作流的基准，以促进企业应用中 text-to-SQL 模型的开发，涵盖 632 个真实的复杂数据整理、变换与分析任务。如图 1 所示，Spider 2.0 中的数据库来自工业应用（例如 Google Analytics 与 Salesforce），具有规模巨大的模式项（平均 812 列）和独特结构（例如图 11 中的嵌套列、图 12 中的多个模式），以及 TB 级的数据量。它们涵盖多种数据库系统，包括本地数据库（例如 SQLite 与 DuckDB）和云数据仓库（例如 BigQuery 与 Snowflake）。这些数据库所用的复杂 SQL 方言整理自技术教程、社区论坛和开源项目。平均而言，每条标准答案 SQL（ground-truth SQL）包含 144 个 token，并包含高级函数（例如 ST DISTANCE(x1, x2) 度量两点之间的最短距离），复杂度明显超过以往基准。所有任务都基于项目代码库，并配有文档和数据库接口，以模拟真实的 text-to-SQL 编写场景。

图 1：Spider 2.0 旨在评测 LLM 在真实企业级 text-to-SQL 工作流上的表现。求解每个任务都需要理解数据库元数据、查阅 SQL 方言文档、处理复杂工作流，并进行精细推理以生成多样的 SQL 查询。图中示意界面、示例 SQL 与省略行的版面抽取不完整，细节【抽取不清】。

与以往数据集不同，Spider 2.0 的智能体式任务设定（agentic task setting）并不依赖预先准备好的输入（问题与数据库模式）或期望输出（预测的 SQL）。它纳入的是真实项目代码库和数据库接口。这种复杂性超出了仅仅预测一条 SQL 查询：模型需要在项目中导航，并通过 SQL 查询和命令行脚本（Python 或 Shell）与复杂数据库动态交互。任务目标是在数据库内执行精细的数据变换，或从数据中提取分析洞见。这一设定紧密对应真实企业 SQL 工作流，要求模型参考代码库与文档、生成多条 SQL 查询，并与环境动态交互，以完成复杂任务并得到最终结果。为简化与以往 text-to-SQL 方法及基准的性能比较，并支持更快的开发与评测，我们还引入 Spider 2.0-lite 与 Spider 2.0-snow。二者是带有预处理数据库模式和文档的自包含数据集：前者托管在 BigQuery、Snowflake 和 SQLite 上，后者完全托管在 Snowflake 上。这一设定省略代码库，并把输出限制为仅 SQL，从而无需预测最终答案或变换数据库。尽管它们与 Spider 2.0 源自同一原始数据，这些设定并不比 Spider 2.0 更容易，因为 text-to-SQL 设定能够获得的信息更少（例如执行反馈）。我们把 Spider 2.0-lite 和 Spider 2.0-snow 呈现为直接的文本输入到 SQL 输出挑战，便于使用当前先进的 text-to-SQL 解析器来处理；把 Spider 2.0 呈现为真实的数据工作流挑战，需要与多样信息源交互以完成数据变换和分析。

我们在 Spider 2.0 上的评测表明，把 LLM 部署到真实企业 text-to-SQL 工作流中仍有很大改进空间。基于 o1-preview 的最佳代码智能体框架性能仅为 21.3%，凸显 LLM 作为熟练 SQL 专家的能力存在显著不足（Tab. 2）。在 Spider 2.0-lite 设定下，即便最先进的 text-to-SQL 解析器也只能成功处理 5.7% 的问题，与 Spider 1.0 上 91.2%、BIRD 上 73.0% 的执行准确率形成鲜明对照，从而突出了实质性挑战（§3.2）。我们的详细分析进一步识别出企业 text-to-SQL 的主要障碍，包括从极大规模数据库中准确链接模式、正确处理不同 SQL 方言、规划嵌套 SQL 查询序列以完成复杂变换与分析任务，以及有效利用外部文档并理解项目级代码库（§4.1 与 §4.2）。Spider 2.0 中的这些挑战，是创建与真实场景紧密对齐的基准的关键步骤。借助 Spider 2.0，我们希望推动新一代智能自主智能体的发展，使其能够在真实企业环境中完成数据工程工作流。

## 2 Benchmark Construction 基准构建

本节介绍 Spider 2.0、Spider 2.0-snow 与 Spider 2.0-lite 的任务定义、总体标注流程和数据集统计。具体例子见 App.B。

### 2.1 Task Definition 任务定义

图 2 说明代码智能体设定与传统 text-to-SQL 设定的任务定义。

图 2：我们提供两种设定：传统的、由文本输入到 SQL 输出的 Spider 2.0-lite/snow，以及智能体式的 Spider 2.0。图内流程框、版本标记（Ver 3、Ver 4. (10.02)）与连线在抽取中交错，细节【抽取不清】。

**代码智能体任务（Code agent task）。** Spider 2.0 被定义为一个综合的代码智能体任务。给定问题 \(Q\)、数据库接口 \(I\) 和代码库 \(C\)（含项目上下文、配置与文档，如图 1 所示），任务是根据观察 \(O_k = \mathrm{execute}(C, I, Q)\) 迭代修改代码（SQL/Python）\(C\)，直到得到最终结果 \(A\)（文本/表/数据库）。换言之，我们把最终观察 \(O_k\) 用作智能体对问题的回答，即 \(A = O_k\)。

**Text-to-SQL 任务。** 与 Spider 2.0 相对，Spider 2.0-snow 和 Spider 2.0-lite 被形式化为自包含任务。给定数据库模式 \(D\)、自然语言问题 \(Q\) 和辅助文档 \(E\) 作为输入，text-to-SQL 解析器 \(f(\cdot)\) 需要输出对应的 SQL 查询 \(S = f(Q, D, E \mid \theta)\)，其中 \(\theta\) 是解析器的参数。Spider 2.0-lite 的数据库与 Spider 2.0 一样托管在多种数据库上，而 Spider 2.0-snow 完全托管在 Snowflake 上，更侧重于 text-to-SQL 生成。

### 2.2 Annotation Pipeline 标注流程

八位主修计算机科学、且都非常精通 SQL 的作者完成数据标注。标注流程包括以下六个步骤：

**1）数据库与 SQL 收集（Database and SQL collection）。** 我们从云数据仓库收集多种数据库，包括 BigQuery 公开数据、Snowflake Marketplace 数据以及其他平台，并要求它们满足特定标准：每个数据库必须包含超过 200 列，或具有嵌套模式结构。过滤后，我们选出 74 个 BigQuery、54 个 Snowflake、30 个 SQLite、40 个 DuckDB、10 个 PostgreSQL 和 5 个 ClickHouse 数据库。从相应的教程和论坛中，我们收集了 1,021 条复杂 SQL 查询，以及来自 Fivetran 和 DBT 的 157 个数据变换项目（见 App.B.2）。按我们的标准，SQL 查询必须包含超过 50 个 token（按空白分词；作为参照，BIRD（Li et al., 2024b）的平均 token 数为 30.9）。此外，查询必须来自真实项目或教程，而不能来自合成例子或极端特例。最终，我们保留 547 条高质量 SQL 查询和 78 个 DBT 项目。

**2）重写 SQL 以防止数据泄漏（SQL rewrite to prevent data leakage）。** 为避免污染并确保 Spider 2.0 评测可信，标注者必须重写每条 SQL，并验证其没有缺陷。重写在复杂度递增的两个层面上进行：表层（surface）与语义（semantic），详见 Tab. 1。84.2% 的例子做了表层重写，42% 做了语义层重写。标注者必须确保重写后的 SQL 能够成功执行、在可接受的时间内完成，并返回非空结果。这些 SQL 查询中，85.98% 使用了各方言中的高级函数（App.B.7.1），10.76% 需要额外的 DBT 工具；由于必须整合项目上下文，后者带来额外挑战。

表 1：重写类别如下。“Surface”重写调整参数和答案格式，“Semantic”重写扩展问题的含义。Example 列中的每个表引用给出对应类型的重写例子。

| Rewrite Categories | Example |
| --- | --- |
| Surface：Answer format | Tab. 13，把单一渠道替换为按会话数（sessions）排序的渠道排名。 |
| Surface：Condition parameters | Tab. 14，更复杂的过滤条件：citibike 比出租车更快。 |
| Surface：Advanced calculation | Tab. 15，基于选定出版物计算原创性分数（originality score）。 |
| Semantic：Advanced requirements | Tab. 16，把页面浏览次序（page view order）改为页面转化率（page conversion rate）。 |
| Semantic：Merge related SQLs | Tab. 17，合并与地理相关和与天气相关的查询。 |
| Semantic：SQL codebase files | App.B.2，修改原项目中的 SQL 与 YML 文件。 |

**3）代码库与上下文设置（Codebase and context setup）。** 对 Spider 2.0-lite 和 Spider 2.0-snow 中的每条复杂 SQL 查询，我们收集完成该任务所需的外部参考文档。由于任务跨越多种数据库类型，我们收集了 SQL 方言与外部函数的文档，如 Tab. 18 所示。此外，对 Spider 2.0，我们保留 SQL 相关项目的原始代码库。对 Spider 2.0，除参考文档外，标注者还收集代码库、数据库接口等资源，为每个任务建立上下文（图 1）。由于有些复杂的数据变换意图无法完全由一个自然语言问题表达，标注者会提供额外上下文，包括数据模型描述（App.B.2）或预定义的答案文件（App.B.5），以便在处理潜在歧义的同时保持清晰。

**4）自然语言任务指令标注（Natural language task instructions annotation）。** 标注者需要根据第 3 步收集的 SQL 与上下文编写问题，并为不同设定撰写两个版本。指令的设计要同时兼顾自然性（naturalness）与无歧义性（unambiguity）。由于 Spider 2.0 与 Spider 2.0-lite/snow 的差异，代码智能体任务的问题更自然，因为它提供上下文和预定义文件来引导答案；text-to-SQL 任务则优先保证无歧义，使规格更清楚、更直接（差异见 App.B.6）。标注者手工撰写指令：避免生硬描述以使其自然，消除期望结果中的歧义，并确保所有 SQL 条件都被明确写出。DBT 项目任务（见图 1 与 App.B.2）是贴近真实的数据变换编码场景，只用于 Spider 2.0。标注者根据所提供的上下文撰写任务指令。初始标注之后，他们验证 SQL 查询与指令之间的语义等价，并借助 LLM 改写以使表述更清楚。

**5）基于执行的聚焦评测（Execution-based focused evaluation）。** 在这一步，标注者需要以程序方式从数据库取得结果，并编写评测脚本（细节见 App.A）。评测脚本可以处理字符串、表和数据库文件形式的结果。需要注意的是，在基于表的评测中，预测结果可能包含很多列，未必与标准答案完全一致。这种差异常常出现，是因为有些问题没有规定应当返回哪些列。为此，评测脚本专门聚焦答案的必要组成部分，忽略非必要列，并强调指令中列出的核心要素。这种方法便于针对每个任务的关键列做有针对性的评估，从而显著减少假阴性。对 Spider 2.0-lite 和 Spider 2.0-snow，这些设定要求输出必须是 SQL，因此评测会用基于表的评估方法比较各 SQL 的执行结果。

**6）质量控制（Quality control）。** 为确保基准质量，每条指令、标准 SQL 查询和评测脚本都至少由三位标注者审阅。我们要求标注者反复检查步骤 3）、4）和 5），以保证标注的正确性、自然性和无歧义性。因此，45% 的例子被第一轮校验者发现含有错误。经过讨论和修正，在与第二轮校验者的第二轮迭代之后，只有 5% 的例子仍含错误。随后我们修正全部错误并完善全部标注，最终所有例子都被视为标注完成。此外，我们对自动评测做了“红队”（red team）评估：提供一组错误结果，检查它们是否会被正确判为假；同时提供多种格式正确的结果，验证它们会被判为真。

### 2.3 Dataset Statistics 数据集统计

我们对 Spider 2.0、Spider 2.0-snow 和 Spider 2.0-lite 的特征做了详细统计分析，并在 Tab. 2 中与多个以往数据集比较。我们的数据集在数据库、SQL 和任务场景等方面表现出很强的复杂度与真实感。

表 2：Spider 2.0、Spider 2.0-snow、Spider 2.0-lite 与其他 text-to-SQL 基准的统计比较。Tok. 与 Func. 分别指 token 与函数。\* 表示因测试集不可得而采用开发集统计。更多统计见 App.B.8。External Knowledge、SQL Dialect、Project Level 三列的单元格标记【抽取不清】。

| Dataset | # Test Examples | # Test DB | # Col / DB | # Tok. / SQL | # Func. / SQL |
| --- | --- | --- | --- | --- | --- |
| WikiSQL (Zhong et al., 2017) | 15,878 | 5,230 | 6.3 | 12.2 | 0.0 |
| Spider 1.0 (Yu et al., 2018) | 2,147 | 40 | 27.1 | 18.5 | 0.0\* |
| KaggleDBQA (Lee et al., 2021) | 272 | 8 | 23.4 | 13.8 | 0.0 |
| SEDE (Hazoom et al., 2021) | 857 | 1 | 212.0 | 46.9 | 1.4 |
| BIRD (Li et al., 2024b) | 1,789 | 15 | 54.2 | 30.9 | 0.4\* |
| Spider 2.0-lite | 547 | 158 | 803.6 | 144.5 | 6.5 |
| Spider 2.0-snow | 547 | 152 | 812.1 | 161.8 | 6.8 |
| Spider 2.0 | 632 | 213 | 743.5 | 148.3 | 7.1 |

图 3：不同数据库系统上的数据分布。抽取到的百分比包括 2.3%、4.7%、14.1%、18.8%、25.4%、34.7%，系统名包括 Postgres、DuckDB、Snowflake、BigQuery、SQLite、Clickhouse，但标签与百分比在版面中错位，对应关系【抽取不清】。

表 3：Spider 2.0 任务特征统计。

| Statistics | Number (% of Total) |
| --- | --- |
| Total（#tokens） | 632 (100%) |
| Easy（#tokens<80） | 160 (25.32%) |
| Medium（80≤#tokens<160） | 279 (44.15%) |
| Hard（#tokens≥160） | 193 (30.54%) |
| With Bigquery | 214 (33.86%) |
| With Snowflake | 198 (31.33%) |
| With SQLite | 135 (21.36%) |
| With DuckDB | 68 (10.76%) |
| With Postgres | 10 (1.58%) |
| With Clickhouse | 7 (1.11%) |
| With Project-level (DBT) | 78 (12.34%) |
| With Documentation | 82 (12.97%) |
| With Functions | 474 (75.00%) |
| With Partition Tables | 54 (8.54%) |
| With Multiple Schemas | 140 (22.15%) |
| With Nested Schemas | 117 (18.51%) |
| With String/Number Answer | 162 (25.63%) |
| With Table Answer | 392 (62.03%) |
| With Database Answer | 78 (12.34%) |

**多样的数据库系统与 SQL 方言（Diverse database systems and SQL dialects）。** 如图 3 与 Tab. 3 所示，我们的基准包含多样的数据库系统，既有 BigQuery、Snowflake 这类云数据仓库，也有 Postgres、ClickHouse 这类本地托管数据库，以及 SQLite、DuckDB 这类轻量系统。这种多样性使本基准有别于以往工作，因为它覆盖了多种 SQL 方言。值得注意的是，85.98% 的例子需要使用这些方言中的专用函数，每条标准答案 SQL 平均使用 7.1 个特殊函数。

**真实且复杂的数据库模式（Real and complex database schema）。** 如 Tab. 2 所示，Spider 2.0 中的数据库配备了大规模模式，包含大量表和列，有效反映真实企业环境。如 Tab. 3 所示，这些数据库具有复杂的模式结构（例如多个模式与嵌套模式、分区表；见图 11 与图 12），以及每日更新的动态表。此外，数据涵盖广泛的复杂类型（图 16）、巨大的数据量与多样的范围（图 15），因而比以往数据集更加多样。

**贯穿数据工程流水线的高难度任务（Challenging tasks across the data engineering pipeline）。** 我们基准中的例子收集自真实教程和论坛，覆盖数据流水线中遇到的广泛问题，包括数据整理、数据变换和数据分析（例子见 App.B.1）。这些问题的难度显著超过以往与 SQL 相关的基准，因为 Spider 2.0 中的 SQL 查询在每条查询的列数、token 数和函数数上都明显更多（见 Tab. 2 与图 18 中的例子）。

**带有代码库和文档的真实项目场景（Real projects scenarios with codebases and documents）。** 如 Tab. 2 与 Tab. 3 所示，两个数据集中的任务都需要查阅文档，例如外部知识（App.B.4）和 SQL 方言（App.B.7），因而必须深入理解这些材料。与其他以往工作相比，我们对 Spider 2.0 中的每个任务都提供代码库上下文，以模拟真实工作流（App.B.5）。更值得注意的是，一些任务引入了新的设定，例如建立在 DBT 之上的项目级数据变换工作流（App.B.2）。DBT 是广泛用于管理数据变换与分析工程（analytics engineering）的工具。要成功完成这些任务，需要在复杂的项目代码库和数据库中导航、理解文档、处理精细的上下文，并通过多步执行与推理生成多样的查询。
