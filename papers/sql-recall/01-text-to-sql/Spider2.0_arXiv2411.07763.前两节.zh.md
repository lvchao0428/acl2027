> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

- 原文件名：Spider2.0_arXiv2411.07763.pdf
- 原文标题：Spider 2.0: Evaluating Language Models on Real-World Enterprise Text-to-SQL Workflows
- 作者：Fangyu Lei、Jixuan Chen（同等贡献）、Yuxiao Ye、Ruisheng Cao、Dongchan Shin、Hongjin Su、Zhaoqing Suo、Hongcheng Gao、Wenjing Hu、Pengcheng Yin、Victor Zhong、Caiming Xiong、Ruoxi Sun、Qian Liu、Sida I. Wang、Tao Yu。首页标注的单位包括 University of Hong Kong、Salesforce Research、Sea AI Lab、Google Deepmind、Google Cloud AI Research、University of Waterloo
- 场合：ICLR 2025 会议论文；arXiv:2411.07763v2 [cs.CL]，2025 年 3 月 17 日。代码、基线与数据见 spider2-sql.github.io

## 摘要

真实企业里的 text-to-SQL 往往跨云端或本地多种数据库、多种 SQL 方言和多条查询，操作从数据变换做到分析。Spider 2.0 是一套评测框架，包含 632 个来自企业级数据库场景的真实工作流问题。库来自真实数据应用，常常超过 1,000 列，放在 BigQuery、Snowflake 等本地或云系统里。解题经常要检索库元数据、方言文档，甚至项目级代码库；模型要在复杂环境里交互、处理极长上下文、做多步推理，并生成多种操作的多条 SQL，长度常常超过 100 行。

评测上，基于 o1-preview 的 code agent 框架只成功解决 21.3% 的任务，对照 Spider 1.0 的 91.2% 和 BIRD 的 73.0%。作者认为，语言模型在以往 text-to-SQL 基准的代码生成上已经很强，但离企业场景够用还差一截；Spider 2.0 上的进展，被他们看成走向真实企业自主代码代理的步骤。

## 1 Introduction

自动写代码被看成人和数据之间的桥梁。大量数据在关系数据库里，SQL 是分析师做日常查询、编排工作流和商业智能的接口，因此语义解析或 text-to-SQL 能减少重复劳动。LLM 已经很会把自然语言写成 SQL：基于 GPT-4 的方法在 Spider 1.0（Yu et al., 2018）和 BIRD（Li et al., 2024b）上的执行准确率分别是 91.2% 和 73.0%。这些数据集多用非工业库，表和列都少，SQL 和问题偏简单，也盖不住多种方言。

企业数据则散落在各自方言的系统里，模式可以有数千列和复杂嵌套，工作流还要项目代码、外部知识和多步上下文，覆盖清洗、变换和分析。Spider 2.0 据此收了 632 个真实的数据整理、变换和分析任务。Figure 1 把每个任务画成要同时看元数据、方言文档、复杂工作流，再写出多样 SQL。库来自 Google Analytics、Salesforce 一类工业应用，模式项平均 812 列，并有嵌套列、多 schema 和 TB 级数据量；系统包括 SQLite、DuckDB，以及 BigQuery、Snowflake。方言材料来自技术教程、社区论坛和开源项目。标准 SQL 平均 144 个 token，并使用高级函数，例如 `ST_DISTANCE(x1, x2)` 计算两点最短距离。任务都配有项目代码库、文档和数据库接口。

与旧数据集不同，Spider 2.0 的代理设定不预先给好问题和模式、也不把输出限定为一条预测 SQL。输入是真实项目代码库和数据库接口；模型要在项目里导航，用 SQL 以及 Python 或 Shell 命令行动态交互，目标是完成库内的复杂变换，或从数据中抽出分析结果。为了方便和旧方法比较、也加快开发，作者另做了 Spider 2.0-lite 和 Spider 2.0-snow：模式和文档已预处理，输出只许是 SQL，因此不必预测最终答案或改库。lite 托管在 BigQuery、Snowflake 和 SQLite，snow 全部在 Snowflake。两者与完整版同源，但作者认为并不更简单，因为这种 text-to-SQL 设定能看到的信息更少，例如没有执行反馈。完整版被定位成要和多种信息源交互的真实数据工作流。

引言中的评测留出很大差距：最好的、基于 o1-preview 的 code agent 只有 21.3%，句末指向 Tab. 2；在 lite 设定下，最强的 text-to-SQL 解析器也只做出 5.7% 的问题，对照仍是 Spider 1.0 的 91.2% 和 BIRD 的 73.0%。第 2 节后面印出的 Tab. 2 是数据集统计，表内并没有这两个成功率。引言点出的障碍包括：在极大的库上对齐模式、处理不同方言、为复杂变换和分析规划嵌套 SQL 序列，以及使用外部文档和项目级代码库。这些困难的展开在后文，这里不进入实验。

## 2 Benchmark Construction

本节定义任务、说明标注流程，并给出 Spider 2.0、Spider 2.0-snow 和 Spider 2.0-lite 的统计。具体例子指向附录。

2.1 Task Definition 用 Figure 2 并列两种设定。代码代理任务中，给定问题 Q、数据库接口 I 和带项目上下文、配置与文档的代码库 C，智能体按观察 \(O_k = \mathrm{execute}(C, I, Q)\) 反复修改 SQL 或 Python，直到得到最终结果 A（文本、表或数据库），并令 \(A = O_k\)。lite 与 snow 则是自包含的 text-to-SQL：给定模式 D、问题 Q 和辅助文档 E，解析器输出 \(S = f(Q, D, E \mid \theta)\)。lite 的库像完整版一样分散在多种系统上；snow 全部放在 Snowflake，更集中在生成 SQL。

2.2 Annotation Pipeline 由八位精通 SQL 的计算机专业作者完成，共六步。第一步从 BigQuery 公开数据、Snowflake Marketplace 等收集库，要求超过 200 列或具有嵌套模式；筛后保留 BigQuery 74 个、Snowflake 54 个、SQLite 30 个、DuckDB 40 个、PostgreSQL 10 个、ClickHouse 5 个。再从教程和论坛收集 1,021 条复杂 SQL，以及来自 Fivetran 和 DBT 的 157 个数据变换项目。SQL 须超过 50 个按空白切分的 token（文中对照 BIRD 平均 30.9），且必须来自真实项目或教程。最终留下 547 条高质量 SQL 和 78 个 DBT 项目。第二步为防泄漏改写 SQL，分表面和语义两层（Tab. 1）：表面层改参数和答案格式，语义层扩展题意，例如把页面浏览顺序改成页面转化率，或合并地理与天气相关查询。84.2% 的例子做了表面改写，42% 做了语义改写。改写后的 SQL 必须能成功执行、在可接受时间内结束并返回非空结果。其中 85.98% 使用各方言的高级函数，10.76% 还要额外的 DBT 工具。第三步为 lite 和 snow 收集方言与外部函数文档（Tab. 18），为完整版保留原始代码库、数据库接口，并在自然语言盖不住意图时补上数据模型说明或预定义答案文件。第四步按 SQL 和上下文手写两套指令：代理任务因为有上下文和预定义文件，问法可以更自然；text-to-SQL 则优先消除歧义，并写明全部 SQL 条件。DBT 项目任务只出现在完整版。标注后还核对 SQL 与指令的语义等价，并借助 LLM 改写以求清楚。第五步用执行结果做聚焦评测，结果可以是字符串、表或库文件。表评测不要求列集合与金标完全一致，因为有的问题没有规定返回哪些列；脚本只核对指令里的核心列，以减少假阴性。lite 和 snow 的输出必须是 SQL，再用这种表评测比较执行结果。第六步要求每条指令、金标 SQL 和评测脚本至少由三名标注者检查，并反复复查第三到第五步。第一轮校验发现 45% 的例子有错；与第二轮校验者迭代后，仍有错的只剩 5%，随后全部改正。作者还用一组假结果和格式正确的结果对自动评测做了 red team 检查。

2.3 Dataset Statistics 用 Tab. 2 把测试规模和复杂度与旧基准对照。Tok. 与 Func. 分别指 token 和函数；星号表示因测试集不可得而改用开发集。数值与表末三列（External Knowledge、SQL Dialect、Project Level）如下：WikiSQL 为 15,878 例、5,230 个库、每库 6.3 列、每条 SQL 12.2 个 token、0.0 个函数，三列皆无；Spider 1.0 为 2,147 例、40 库、27.1 列、18.5 token、0.0* 函数，三列皆无；KaggleDBQA 为 272 例、8 库、23.4 列、13.8 token、0.0 函数，仅有外部知识；SEDE 为 857 例、1 库、212.0 列、46.9 token、1.4 函数，三列皆无；BIRD 为 1,789 例、15 库、54.2 列、30.9 token、0.4* 函数，仅有外部知识。Spider 2.0-lite 为 547 例、158 库、803.6 列、144.5 token、6.5 函数，有外部知识与方言、无项目级代码；snow 为 547 例、152 库、812.1 列、161.8 token、6.8 函数，同样有外部知识与方言、无项目级代码；完整 Spider 2.0 为 632 例、213 库、743.5 列、148.3 token、7.1 函数，三列都有。

Figure 3 画的是这些库在系统上的分布，与采集阶段的 213 个库对应：BigQuery 34.7%，Snowflake 25.4%，DuckDB 18.8%，SQLite 14.1%，Postgres 4.7%，ClickHouse 2.3%。Tab. 3 则是 632 个 Spider 2.0 任务，不能和 Figure 3 的库占比混读。按金标 SQL 的 token 数：Easy（少于 80）160 个，占 25.32%；Medium（不少于 80 且少于 160）279 个，占 44.15%；Hard（不少于 160）193 个，占 30.54%。任务所用系统为 BigQuery 214（33.86%）、Snowflake 198（31.33%）、SQLite 135（21.36%）、DuckDB 68（10.76%）、Postgres 10（1.58%）、ClickHouse 7（1.11%）。特征计数还有：项目级 DBT 78（12.34%），需文档 82（12.97%），含函数 474（75.00%），分区表 54（8.54%），多 schema 140（22.15%），嵌套 schema 117（18.51%）。答案为字符串或数字的 162 个（25.63%），为表的 392 个（62.03%），为数据库的 78 个（12.34%）。正文写明 85.98% 的例子要用这些方言里的专用函数，金标 SQL 平均使用 7.1 个。任务来自真实教程和论坛，覆盖整理、变换和分析；相对旧基准，查询里的列、token 和函数都明显更多。完整版还给每个任务提供代码库上下文，其中 DBT 上的项目级变换要求在代码库、数据库和文档之间多步执行并生成多种查询。
