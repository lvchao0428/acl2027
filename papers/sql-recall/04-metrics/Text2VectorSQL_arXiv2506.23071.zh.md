原文件名：Text2VectorSQL_arXiv2506.23071.pdf

原标题：Text2VectorSQL: Towards a Unified Interface for Vector Search and SQL Queries

中文标题：Text2VectorSQL：迈向向量检索与 SQL 查询的统一接口

作者：Zhengren Wang（Peking University）；Dongwen Yao（Shanghai Jiao Tong University）；Bozhou Li（Peking University）；Dongsheng Ma（Peking University）；Bo Li（Peking University）；Zhiyu Li（Institute for Advanced Algorithms Research, Shanghai；通讯作者）；Feiyu Xiong（Institute for Advanced Algorithms Research, Shanghai）；Bin Cui（Peking University）；Linpeng Tang（OriginHub Technology；Institute for Advanced Algorithms Research, Shanghai）；Wentao Zhang（Peking University；OriginHub Technology；Zhongguancun Academy；通讯作者）。邮箱：wzr@stu.pku.edu.cn，{wentao.zhang, bin.cui}@pku.edu.cn

arXiv：arXiv:2506.23071v2 [cs.CL] 6 Nov 2025

<!-- 原 PDF 第 1 页 -->

## 摘要

非结构化数据的激增，给传统数据库接口带来根本性挑战。Text-to-SQL 已经降低了访问结构化数据的门槛，但它仍然无法解释语义查询或多模态查询。与此同时，向量检索已成为查询非结构化数据的事实标准；可它与 SQL 的结合——称为 VectorSQL——仍然依赖手工编写查询，并且缺少标准化的评测方法，因而在潜力与实际应用之间留下显著缺口。

为弥合这一根本缺口，我们提出并形式化 Text2VectorSQL。这是一项新任务，目标是为同时、无缝地查询结构化数据与非结构化数据建立统一的自然语言接口。为推动这一新方向上的研究，我们给出一套完整的基础生态，包括：（1）一条可扩展且稳健的流水线，用于合成高质量的 Text-to-VectorSQL 训练数据；（2）VectorSQLBench，该任务上第一个大规模、多面向的基准，涵盖 12 种不同组合，横跨三种数据库后端（SQLite、PostgreSQL、ClickHouse）与四种数据源（BIRD、Spider、arXiv、Wikipedia）；（3）若干新的评价指标，用于更细致的性能分析。大量实验不仅确认了我们所训练模型作为强基线的表现，也揭示了召回下降（recall degradation）这一挑战：把 SQL 过滤与向量检索结合起来，可能导致比传统过滤向量检索更明显的结果遗漏。通过定义核心任务、交付必要的数据与评测基础设施，并指出关键研究挑战，本工作为构建下一代统一、智能的数据接口奠定了必要基础。我们的仓库见 https://github.com/OpenDCAI/Text2VectorSQL 。

## 关键词

Text-to-SQL、向量检索、向量数据库、关系数据库、数据合成

## I. 引言

现代数据图景的根本特征是一种二分：一边是关系数据库构成的结构化世界，靠 SQL 的精确逻辑来导航；另一边是庞大的非结构化数据——据估计占全部企业数据的 90% 以上 [1]——越来越多地通过语义向量检索来查询。这种分离对统一数据接口构成关键障碍，并迫使用户在基于 SQL 的分析与基于向量的语义检索之间来回切换不同接口。

一方面，Text-to-SQL 系统在把自然语言翻译成结构化查询方面已取得显著进展，使表格数据更容易被使用。然而，它们本质上看不见文本、图像及其他模态等非结构化内容中蕴含的丰富语义。因此，它们无法回答这样的混合问题：“找出 2020 年之后发表的、讨论 learned index structures 的科学论文。”

与此同时，向量检索已成为基于相似度检索的事实标准，而把它集成进关系数据库——即 VectorSQL——有望弥合这一缺口 [2], [3]。不过，这种集成仍处于萌芽阶段。编写有效的 VectorSQL 查询是手工且易出错的过程，要求同时精通向量检索与 SQL。更关键的是，把自然语言翻译成 VectorSQL 的学术研究完全缺席。

为弥合这一根本缺口，并为新一类数据交互范式铺路，我们提出 Text2VectorSQL。实现这一设想并不简单，面临三项核心挑战：

- 训练数据极度稀缺：不存在把自然语言与 VectorSQL 查询配对的公开数据集，因而无法用于模型训练或微调。
- 评测空白：没有既定基准或指标来衡量 Text2VectorSQL 模型的性能，从而阻碍可复现研究。
- VectorSQL 翻译与执行中准确率与效率的权衡：向量检索与 SQL 过滤相互交织，可能导致大量却不易察觉的召回失败。

为解决这些基础障碍，我们构建了一套基础生态。首先，针对数据稀缺，我们开发一条可扩展且稳健的流水线，用于合成高质量、多样化的 Text-to-VectorSQL 训练数据。其次，为填补评测空白，我们构建 VectorSQLBench，这是该任务上第一个大规模、多面向的基准，覆盖数据库后端（SQLite、PostgreSQL、ClickHouse）与数据源（BIRD、Spider、arXiv、Wikipedia）的 12 种组合。VectorSQLBench 还配有一套新的评价指标，例如基于排序的分数与分解准确率，以便在执行准确率之外做更全面、更细粒度的评测。

最后，借助这一生态，我们的大量实验得出关键认识。我们所训练的模型达到了当时最优的性能，同时分析也揭示了一个关键、且此前考察不足的挑战，我们称之为

<!-- 原 PDF 第 2 页 -->

召回下降。我们发现，流行的“后过滤”做法——先得到向量检索结果，再用 SQL 谓词过滤——可能比传统过滤向量检索更严重地漏掉正确结果。例如，在涉及 JOIN 的复杂查询中，后过滤可能悄悄丢弃超过 30% 的正确结果。这一发现把 Text2VectorSQL 从单纯的翻译问题，提升为与查询优化和执行策略深度交织的复杂挑战。

我们的主要贡献概括如下：

- 任务形式化。我们首次形式化定义 Text2VectorSQL 任务，为用自然语言同时与结构化数据和非结构化数据交互确立明确目标，从而克服传统 Text-to-SQL 的固有局限。
- 一套基础生态。我们提供完整生态，以推动这一新兴方向的研究。其中包括一条可扩展的高质量训练数据合成流水线，以及 VectorSQLBench，即第一个用于评测 Text2VectorSQL 的综合性基准。VectorSQLBench 的广度（12 种数据集组合）与深度（所提出的指标）为整体评估提供了稳健基础。
- 实证分析与关键发现。通过在多个数据集和数据库上的大量实验，我们为该任务建立了强基线。更重要的是，分析揭示了 VectorSQL 执行中召回下降这一关键挑战。这一认识指出了未来研究的一个关键方向：共同优化查询生成与执行。

我们的数据、模型与评测脚本已公开于 https://github.com/OpenDCAI/Text2VectorSQL 。

图 1 的可见文字包括：用户输入 “Find Papers on ‘Learned Indexes’ after 2020”；自然语言问题经 Text2VectorSQL 得到 `SELECT ... WHERE year > 2020 ORDER BY embedding <-> ...`；结果年份示例为 2021、2023、2025。图下方场景包括语义过滤、多模态匹配与检索加速。语义过滤一侧可见摘要与年份示例：B+-Tree / 2019、Crowdsourcing / 2021、AI-based Index / 2023、Learned Bloom Filter / 2024。检索加速一侧对比模糊匹配与向量检索：Scan 为 \(O(N)\)，HNSW 为 \(O(\log N)\)；标题匹配示例含 “... LLM as DBA ...”“... language model ...”，以及 0.5、0.4、0.8。多模态一侧可见 “Beach in the evening”。图中还标有统一查询（SQL 与向量）及执行结果。这些是示意图标签，不是数据表。

**图 1：** Text2VectorSQL 任务示意。下方场景说明，把 SQL 查询与向量检索结合起来，可以解锁语义过滤、多模态匹配和检索加速。这些能力对于通用自然语言接口不可或缺。

## II. 预备知识

本节介绍支撑本工作的基础概念：向量检索，以及 VectorSQL 范式。

### A. 向量检索

向量检索从集合中取出那些高维向量表示与给定查询向量最相似的条目。这是现代语义检索与多模态信息检索的基石 [4]–[6]。

**定义 2.2（向量检索任务）。** 设 \(D\) 为非结构化条目的集合（例如文档、图像），\(E: D \rightarrow \mathbb{R}^d\) 为嵌入模型，把任意条目 \(d \in D\) 映射为 \(d\) 维向量 \(\vec{v} = E(d)\)。给定查询文本 \(Q_{\mathrm{txt}}\)，其对应查询向量为 \(\vec{q} = E(Q_{\mathrm{txt}})\)，相似度函数为 \(\mathrm{sim}(\cdot, \cdot)\)（例如余弦相似度或点积），以及整数 \(k\)。向量检索任务是找到大小为 \(k\) 的结果集 \(R_V \subset D\)，其中包含与查询最相似的 top-\(k\) 个条目：

\[
R_V = \arg\max_{R \subset D,\ |R|=k} \sum_{d_i \in R} \mathrm{sim}(\vec{q}, E(d_i))
\]

为了在大规模数据上保持效率，这通常用近似最近邻（Approximate Nearest Neighbor，ANN）检索算法实现，以获得对数时间复杂度。在许多实际应用中，该任务被扩展为过滤向量检索：检索到的条目既要与查询语义相似，也要满足某个过滤谓词。

<!-- 原 PDF 第 3 页 -->

### B. Text-to-VectorSQL

**定义 2.3（VectorSQL 查询）。** 一条 VectorSQL 查询记为 \(Q_{VSQL}\)，在概念上由结构化过滤与语义向量检索两部分组成：

- SQL 谓词分量（\(Q_S\)）：一条标准 SQL 查询或子查询，对结构化数据列施加约束（例如 WHERE 与 JOIN 子句）。
- 向量检索分量（\(Q_V\)）：一条语义检索指令，由二元组 \((\vec{q}, k)\) 定义，其中 \(\vec{q} \in \mathbb{R}^d\) 是查询向量，\(k\) 是最近邻个数。

执行一条 \(Q_{VSQL}\) 时，通过协调 \(Q_S\) 与 \(Q_V\) 得到结果集。对作为 VectorSQL 简化形式的过滤向量检索，这种协调可分为两种策略：

- 先过滤（Filter-then-Search）。该策略把准确率放在前面：先用 SQL 谓词划定数据的精确子集，再在该子集内做向量检索。
  1. 过滤：执行 SQL 查询 \(Q_S\)，选出精确子集 \(D' = \{d \in D \mid d \text{ 满足 } Q_S\}\)。
  2. 检索：只在过滤后的子集上做向量检索，找出 top-\(k\) 结果：\(R_{\mathrm{pre}} = \mathrm{ANN\ Search}(\vec{q}, k, D')\)。

  这种方法保证所有结果都遵守结构化条件，但可能低效，因为它可能破坏预先构建的 ANN 索引所依赖的假设，从而被迫对 \(D'\) 做代价高昂的暴力扫描。

- 后过滤（Search-then-Filter）。该策略把速度放在前面：先做近似向量检索以缩小候选，再施加 SQL 过滤。
  1. 检索：执行 ANN 检索，得到初始候选集 \(R_V = \mathrm{ANN\ Search}(\vec{q}, k')\)，其中 \(k'\) 可以大于最终想要的 \(k\)，以便为随后会被滤掉的条目留出余量。
  2. 过滤：对检索到的候选施加 SQL 谓词 \(Q_S\)：\(R_{\mathrm{post}} = \{d \in R_V \mid d \text{ 满足 } Q_S\}\)。

实际上，SQL 过滤与语义相似度通常分别被当作硬约束和软约束。先过滤的执行被视为高保真；后过滤效率较高，但可能因召回下降而检索不到足够多的正确结果。

在 VectorSQL 的定义确立之后，我们可以定义 Text-to-VectorSQL 任务。

**定义 2.4（Text-to-VectorSQL 任务）。** 给定混合数据库模式 \(S_{\mathrm{hybrid}}\)（其中包含带向量列的关系表）以及自然语言问题 \(Q_{NL}\)，Text-to-VectorSQL 任务是学习一个映射函数 \(f_{T2VSQL}\)，把问题翻译成一条合法的 VectorSQL 查询：

\[
Q_{VSQL} = f_{T2VSQL}(Q_{NL}, S_{\mathrm{hybrid}}).
\]

## III. Text2VectorSQL 的基础生态

为系统应对 Text2VectorSQL 中的数据稀缺、评测标准缺失以及稳健基线不足，我们开发了如图 2 所示的基础生态。这一生态的基石是 VectorSQLGen，一条用于合成高质量训练数据的可扩展流水线。该流水线支撑我们的 UniVectorSQL 模型。与此同时，我们构建了 VectorSQLBench，一个用于整体评测的、有原则的基准。

### A. VectorSQLGen：面向 Text2VectorSQL 训练数据的合成流水线

解决训练数据的极度稀缺，是 Text2VectorSQL 取得进展的首要前提。受 OmniSQL [7] 等数据合成范式成功的启发，我们提出 VectorSQLGen，一条显著扩展该方法、以服务 Text2VectorSQL 任务的新流水线。VectorSQLGen 自动创建高质量训练四元组：〈混合数据库，自然语言问题，VectorSQL 查询，思维链〉。流水线经过仔细设计，分四个阶段运行。

**1）混合数据库增强。** 第一项挑战是：标准 SQL 数据库纯粹是关系型的。要合成有意义的 VectorSQL，必须为这些数据库补上一层语义：

- 基础数据库来源。真实世界的数据库在互联网上很稀缺，因为企业数据库往往含有敏感信息。尽管如此，表格数据很丰富，并且同样反映真实场景。为保证来源多样并增强模型泛化，我们遵循 OmniSQL [8] 的方法，用网页表格语料合成全新的数据库。
- 目标列识别。我们把大语言模型当作“模式分析员”，让它自主识别语义丰富、适合向量化的列。提示要求模型分析模式定义（CREATE TABLE 语句）和表内容（例如样例行），找出包含自由文本的列，例如论文表中的摘要，或产品表中的描述。
- 语义内容增强。对缺少丰富文本的表，指示大语言模型以每一行已有的结构化数据为条件，生成合理的非结构化文本。例如，给定论文表的一行，列包括 title、authors 和 conference，模型可以撰写一段简短的 paper_abstract。这一步增强了与关系数据在上下文上连贯的语义内容。
- 嵌入与模式修改。我们使用一些流行的嵌入模型（例如 all-MiniLM-L6-v2），把已识别或已增强列的内容转换成稠密向量表示。随后，以程序方式修改数据库模式，加入新的向量类型列。生成的向量被插入这些新列，从而把关系数据库转变成既能支持 SQL、也能支持向量运算的混合数据库（\(S_{\mathrm{hybrid}}\)）。

<!-- 原 PDF 第 4 页 -->

**图 2：** Text2VectorSQL 生态。核心组件是 VectorSQLGen 流水线，一个大规模、自动化的数据合成引擎，产出高质量训练样本。随后，合成数据用于训练我们的 UniVectorSQL 模型家族。与此同时，经过筛选的数据子集再经历更严格的人工审核，形成 VectorSQLBench，即带有一套新的细粒度指标的金标准评测基准。

图 2 可见标签还包括：UniVectorSQL 的输入含任务说明、数据库模式、VectorSQL 语法与自然语言问题，模型规模为 7B/14B/32B；VectorSQLBench 侧列出基于集合、基于排序与分解三类指标；流水线四步为混合数据库增强（Find、Add、Embed，后端为 SQLite、PostgreSQL、ClickHouse）、复杂度感知的 VectorSQL 合成（向量复杂度与结构复杂度，后者含子查询与 CTE、混合集成深度、聚合与窗口，并执行后去重）、语义感知回译（意图翻译、候选选择、文体多样性：正式、口语、模糊、祈使等；字面说法如 “Order by distance to the embedding of …”，语义说法如 “Find papers about...”），以及思维链合成与精炼（混合意图分解、双路模式链接、SQL 与向量、多数投票）。训练策略包括 LoRA/全量微调、数据混合与思维链。示例思维链为：“We will first vector-search top 100 papers and use a WHERE clause to filter by year.” 真值生成包括先过滤执行、变体采样（约 5 个）与倒数排名融合（RRF）；人工检查包括自然语言问题润色、查询逻辑校验与参数检查。图中还标有 2,997 条高质量样本、3 种后端与 4 个数据集（Wiki、arXiv、Spider、BIRD），以及代表性取值、向量索引与元数据。图中指标公式的符号为乱码，原文抽取为：

```
퐏퐫ͳͱ. = |ͦ퐩퐫ͳͲ ∩ͦ퐠퐨͸Ͳ|
|ͦ퐩퐫ͳͲ|
ͦͳͱͯ. = |ͦ퐩퐫ͳͲ ∩ͦ퐠퐨͸Ͳ|
|ͦ퐠퐨͸Ͳ|
퐃͗͛@ͷ =
풓ίδβ
δηαΉ(β + Έ)
퐧퐃͗͛@ͷ = 퐃͗͛@ͷ
퐈퐃͗͛@ͷ
퐀͗͗퐕ͳͱ = 퐒퐈͡(ͦ퐩퐫ͳͲ, ͦ퐠퐨͸Ͳ)
퐀͗͗퐒ͥ͠ = 퐒퐄͠퐄͗ͨ⋀퐅ͦͣ͡
```

以及 `⋀퐖퐇퐄ͦ퐄⋀. . .`。公式抽取不完整，见原 PDF 第 4 页。

**2）复杂度感知的 VectorSQL 查询合成。** 这一阶段是流水线的核心，目的是生成一批 VectorSQL 查询：它们在多种数据库后端上语法正确，并且覆盖很宽的逻辑复杂度谱。我们不再把复杂度看成单一维度，而采用更细致的二维框架。

- 多后端语法适配。一个关键的实际挑战是，向量运算在不同数据库系统中的语法并不一致。我们的基准纳入 SQLite（经由 sqlite-vec，https://github.com/asg017/sqlite-vec ）、PostgreSQL（经由 pgvector，https://github.com/pgvector/pgvector ）和 ClickHouse。为此，我们设计了特定于后端的语法模板。生成查询时，把合适的模板注入大语言模型提示，引导它为目标后端产出语法合法的查询。例如，ClickHouse 使用 L2Distance 函数，PostgreSQL 使用 `<->` 运算符。具体例子见图 3。
- 二维复杂度框架。为使合成数据覆盖宽谱挑战，我们沿两条正交轴定义查询复杂度：结构复杂度与向量复杂度。
  1. 结构复杂度。这一轴刻画查询中传统 SQL 部分的难度，既包括基本数据检索，也包括高级数据分析。我们控制如下指标：
     - 子查询与 CTE 深度：子查询的嵌套层数，以及 WITH 子句的数量。
     - 连接复杂度：涉及的表的数量，以及 JOIN 的类型（INNER、LEFT 等）。
     - 聚合、分组与集合运算：是否出现 GROUP BY、HAVING 和窗口函数，以及是否使用 UNION、INTERSECT 或 EXCEPT 等集合运算。
  2. 向量复杂度。这一新轴量化查询中语义检索分量所固有的难度。它由三个子维度组成：
     - 向量运算次数：查询可以只有一次向量检索，也可以有多次向量检索，后者可能需要连接或求交来自不同语义查询的结果（例如：“找出方法与 ‘B-tree’ 相关、且应用领域与 ‘Spanner’ 相似的论文。”）。
     - 查询意图复杂度：这一项评估把用户的自然语言说法翻译成精确查询关键词时所需的认知跨度与世界知识。我们定义三层：
       （1）实体级：这是最直接的情形，查询目标是一个直接、显式的实体，例如 ‘pgvector’；（2）概念级：


<!-- 原 PDF 第 5 页 -->

用户描述的是抽象概念、类别或主题，而不是某个具体实体，例如 “extension for vector search in relational database”（关系数据库中用于向量检索的扩展）；（3）推理级：意图高度抽象、带有关系性，或者需要 Text2VectorSQL 模型去组织表述、并需要嵌入模型去理解，例如 “database with both SQL interface and vector search capability but different storage format from ClickHouse”（同时具备 SQL 接口和向量检索能力、但存储格式与 ClickHouse 不同的数据库）。

- 混合集成深度。这一关键指标衡量向量检索与 SQL 谓词耦合得有多紧，而这正是影响召回下降的关键因素。由简到繁，我们定义三个级别：（1）非集成：向量检索独立进行（例如放在 CTE 或子查询中），其结果（例如主键）再通过 WHERE IN 或 JOIN 过滤主查询；（2）WHERE 集成：向量检索在已经被 WHERE 子句过滤过的数据子集上进行；（3）JOIN 集成：向量检索发生在一张表已经与其他表连接之后，过滤条件来自相关表。这是最复杂的情形，也是后过滤策略最可能失败的地方。
- 生成与后处理。合成过程中，我们从这个二维复杂度空间里随机采样一个目标复杂度，并提示大语言模型生成对应的 VectorSQL 查询。所有生成的查询都拿到数据库上执行，以滤掉语法错误、执行超时或结果为空的查询。最后，把查询模板化以去掉字符串字面量，再去重，从而尽量提高多样性。

**3）语义感知的问题回译。** 有了高质量 VectorSQL 查询语料之后，我们用回译技术 [9] 生成对应的自然语言问题，也就是由 VectorSQL 到问题。

- 语义意图翻译。这一步的核心，是明确提示大语言模型去理解并解释向量检索分量的语义意图。对于 `ORDER BY abstract_embedding <-> EMBED("query optimization")` 这样的子句，提示要求模型生成“找出关于加快数据库查询的技术的论文”这类问题，而不是字面翻译成“按摘要嵌入到……的距离对论文排序”。
- 文体多样性。我们采用 OmniSQL 定义的九种语言风格（正式、口语、祈使、疑问、描述、简洁、模糊、隐喻和对话），为每条 VectorSQL 生成不同风格的问题。这样训练数据能反映真实用户输入的多样性，并增强模型的稳健性。例如，正式问法可以是 “Retrieve top-10 articles related to database published after 2022”（检索 2022 年之后发表的、与数据库相关的前 10 篇文章），模糊版本可以是 “Show me some recent DB papers from the last couple of years.”（给我看最近几年的一些数据库论文）。
- 语义一致性选择器。对每条 VectorSQL，我们生成多个候选问题。为自动选出质量最高的一个，我们把全部候选嵌入向量空间，并找出最接近该簇语义质心的问题。已有工作证明，这一技术能选出最有代表性的样本，并提高数据质量 [8], [10]。

**4）思维链合成与精炼。** 最后一阶段有两重目的：生成详细的逐步推理过程，用作强训练信号；并通过自我纠正做最后一轮质量保证。

- 面向混合查询的扩展思维链结构。我们设计了专为 Text2VectorSQL 定制的思维链，迫使大语言模型同时推理结构化 SQL 过滤和语义向量检索：
  1. 混合意图分解。思维链先分析自然语言问题，把结构约束（例如“2020 年之后发表”）和语义检索意图（例如“讨论关系数据库”）分开。
  2. 双路模式链接。然后把结构部分链接到具体的表和列，把语义部分链接到合适的向量列。
  3. 向量查询构造。明确说明语义意图如何翻译成向量检索子句，其中包括对查询关键词的推理。

**图 3：** SQLite（经由 sqlite-vec）、PostgreSQL（经由 pgvector）和 ClickHouse 中向量运算的不同语法。sqlite-vec 借助虚表机制和 vec0 引擎隐式生成距离列。PostgreSQL 与 ClickHouse 支持为近似最近邻检索建索引，sqlite-vec 目前还不支持。自然语言查询为：找出与查询优化技术最相关的前 5 篇论文。

ClickHouse 使用内置函数做向量运算：

```sql
SELECT title FROM papers ORDER BY
L2Distance(abstract_embedding,
EMBED('query optimization')) LIMIT 5;
```

SQLite-vec 使用 MATCH 关键字做 KNN：

```sql
SELECT title FROM papers WHERE
abstract_embedding MATCH
EMBED('query optimization') AND k=5;
```

PostgreSQL 使用中缀运算符计算距离：

```sql
SELECT title FROM papers ORDER BY
abstract_embedding <-> EMBED('query
optimization') LIMIT 5;
```

原文中 ClickHouse 示例的结束引号抽取为弯引号。以上 SQL 按可见词保留。

<!-- 原 PDF 第 6 页 -->

  4. SQL 谓词构造。说明标准 SQL 子句（WHERE、JOIN 等）如何构造。
  5. 最终组装与策略解释。关键的一步是组装出完整的 VectorSQL 查询，并明确解释所选的集成策略。例如：“我们先对前 100 篇论文做向量检索，再用 WHERE 子句按年份过滤。”这使模型的推理更透明，也更可控。

- 用多数投票做自我纠正。为尽量提高最终训练样本的正确性，我们对每个问题生成多条思维链解答。然后从每条思维链中抽出 VectorSQL 查询并执行，比较执行结果。与多数投票结果交集最大的那条思维链被选为规范、最可靠的训练实例。这一精炼纠正初始查询合成中的细微错误和次优选择。

为了做出能面向多种数据库后端的 Text2VectorSQL 模型，我们为每个后端收集约 8k 条训练样本，汇总成 SynVecSQL-24k，作为训练集。

### B. VectorSQLBench：面向整体评测 Text2VectorSQL 的基准

VectorSQLGen 解决了模型训练的数据稀缺，但这一领域仍然缺少标准化、高质量的基准。没有它，就很难比较不同方法、诊断模型弱点、衡量真正的进展。为填补这一空白，我们提出 VectorSQLBench：一个多面向、跨后端、并带有严格标注的基准。除端到端执行准确率之外，它要在一系列复杂度上给出细粒度、可用于诊断的认识。为搭一个全面的测试床，我们选取的基础数据源既包括复杂的结构化模式（来自经典基准 BIRD [11] 和 Spider [12]），也包括丰富的非结构化内容（来自 arXiv 论文，https://www.kaggle.com/datasets/Cornell-University/arxiv ；以及 Wikipedia 文章，https://www.kaggle.com/datasets/jacksoncrow/extended-wikipedia-multimodal-dataset ）。arXiv 数据集包含非结构化的标题、摘要和评论；Wikipedia 数据集提供图像、图注、段落、小标题等。

**1）VectorSQLBench 的构建流水线。** 构建过程兼有自动数据合成和人类专家审核，并遵循一条旨在保证多样性、正确性和自然度的三阶段流水线。

- 用分层采样播种候选。为得到有代表性、也有难度的基准，我们按二维复杂度框架做分层采样（见第 III-A2 节）。从“结构复杂度 × 向量复杂度”矩阵的每个格子里采样，使 VectorSQLBench 从简单的单表语义检索，覆盖到必须先连接多张表再做向量检索的高度复杂查询，从而全面考察模型能力。
- 有原则地生成真值。对评测基准来说，正确和完整是首要的。后过滤虽然高效，但因其固有的召回下降，不能用来建立真值。因此，对每个抽到的候选，我们强制采用先过滤执行，收集黄金结果集 \(R_{\mathrm{gold}}\)。此外，同一个问题可能有多种合法的 VectorSQL 写法，流水线为每个问题采样五个 VectorSQL 变体。全部分支都用先过滤执行，并把 \(R_{\mathrm{gold}}\) 定义为：列相同的执行结果经倒数排名融合（RRF）[13] 得到的有序并集。这样得到的真值不偏向某一种写法，也能承受语法变体或关键词改写。脚注：对于本文中的 VectorSQL，我们把先过滤执行的结果视为真值；不过对模糊查询而言，执行或显式声明后过滤可以是高效且可接受的。
- 专家标注与修订。人工审核是把基准提升到金标准的最后一步。每个样本都由同时熟悉数据库系统和自然语言处理的标注者彻底审核。审核主要有三项：
  1. 自然语言问题修订。标注者判断回译问题是否自然、清楚。含糊或生硬的问题会被改写，使之更接近真实用户的意图和语气。
  2. 查询逻辑校验。专家确认配套的 VectorSQL 是修订后自然语言问题的直接、合理翻译。这包括修正细微的逻辑缺陷，并保证能够执行。无法执行的样本一律丢弃。
  3. 参数检查。关键是检查那些取决于用户意图的查询参数。例如，根据说法是“找出最相似的论文”还是“给我看一些相关论文”，专家标注最合适的 top-\(k\)，作为评估模型能否推断这类差别的参考值。

**2）基准构成与统计。** 上述流水线得到综合性基准 VectorSQLBench。它的数据源多样，查询复杂度也有挑战。表 I 给出详细概览。基准包含 2,997 条高质量样本，分布在 3 种数据库后端和 4 种数据源上（BIRD-Vec、Spider-Vec、arXiv-Vec、Wikipedia-Vec），既有复杂的结构化模式，也有丰富的非结构化内容。

高复杂度查询所占比例相当大，并且基准在两个复杂度

<!-- 原 PDF 第 7 页 -->

维度上是平衡的。结构复杂度按 SQL 谓词难度评定，包括 942 个易、786 个中、624 个难、645 个极难样本。向量复杂度关注向量检索的集成深度，合计有 969 个非集成样本、1,005 个 WHERE 集成样本和 1,023 个 JOIN 集成样本。难与极难合计 1,269 条，JOIN 集成有 1,023 条，对当前和未来的 Text2VectorSQL 模型都是显著挑战。

图 4 进一步展示了为在广泛场景中压力测试模型而做的多层设计。第一层（内环）体现语言多样性，把 2,997 条查询分到九种语言风格上，以覆盖真实用户表达的范围。文中举例包括正式（348）、口语（330）、模糊（270）和描述（294）。后面的层分别拆开向量复杂度和结构 SQL 复杂度。这种层次分布使 VectorSQLBench 成为严格的评测套件。

**表 I：** VectorSQLBench 的综合统计与复杂度分布。表中给出基准的总体规模，并分解查询复杂度。结构复杂度按 SQL 谓词难度评定（E：易，M：中，H：难，EH：极难）。向量复杂度关注向量检索与 SQL 谓词的集成深度（Non：非集成，WHERE：WHERE 集成，JOIN：JOIN 集成）。表中同时给出合成训练数据 SynVecSQL-24k 的统计，供参照。`find_tables` 未返回该表；下表按页面文本中的数字顺序对齐。结构四档之和、向量三档之和都等于对应样本数，并与正文中的 942、786、624、645 以及 969、1,005、1,023 一致。

| 数据集 | 数据库数 | 表数 | 列数 | 向量列数 | 总行数 | 样本数 | E | M | H | EH | Non | WHERE | JOIN |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BIRD-Vec | 69 | 519 | 3,805 | 140 | 362,892,413 | 1,278 | 438 | 315 | 264 | 261 | 441 | 400 | 437 |
| Spider-Vec | 166 | 872 | 5,955 | 497 | 1,604,329 | 1,080 | 351 | 276 | 228 | 225 | 317 | 374 | 389 |
| arXiv-Vec | 1 | 7 | 29 | 3 | 28,475,592 | 261 | 69 | 99 | 39 | 54 | 95 | 92 | 74 |
| Wikipedia-Vec | 1 | 5 | 35 | 6 | 7,973 | 378 | 84 | 96 | 93 | 105 | 116 | 139 | 123 |
| 合计 | 237 | 1,403 | 9,824 | 646 | 392,980,307 | 2,997 | 942 | 786 | 624 | 645 | 969 | 1,005 | 1,023 |
| 训练数据 | 1,839 | 15,586 | 117,884 | 7,467 | 20,270 | 24,421 | 9,934 | 4,324 | 6,142 | 4,021 | 7,078 | 8,092 | 9,251 |

**图 4：** VectorSQLBench 的多样性。层次结构沿三个维度拆开数据集：（1）九种语言风格（内环），以承受不同的用户措辞；（2）三级向量复杂度（中环），说明向量检索如何与 SQL 集成（Non、WHERE、JOIN）；（3）四级结构 SQL 难度（外环），从易到极难。这种多面向设计有助于覆盖 Text2VectorSQL 中的挑战。

内环与风格名称相邻、可以对齐的计数为：疑问 387、祈使 366、对话 348、正式 348、隐喻 342、口语 330、简洁 312、描述 294、模糊 270，合计 2,997。中环与外环各扇区的数字在文本层里与扇区标签脱开，对应关系抽取不完整，见原 PDF 第 7 页。

**3）一套专门的评价指标。** 为了做实用、也有诊断价值的分析，我们不再只看执行准确率（EX）[11]。EX 并不适合 Text2VectorSQL：它要求执行结果精确匹配，而向量检索中近似结果本质上难以避免，也可以接受。因此我们提出一套更稳健、更能诊断问题的指标。

- 基于集合的分数。这是端到端性能的基本指标。它衡量预测 VectorSQL 的结果集 \(R_{\mathrm{pred}}\) 与黄金结果集 \(R_{\mathrm{gold}}\) 的重叠，能够抓住语义等价，并容忍语法差异。分数如下计算，其中 F1 是精确率与召回率的调和平均。

\[
\mathrm{Precision} = \frac{|R_{\mathrm{pred}} \cap R_{\mathrm{gold}}|}{|R_{\mathrm{pred}}|}, \quad
\mathrm{Recall} = \frac{|R_{\mathrm{pred}} \cap R_{\mathrm{gold}}|}{|R_{\mathrm{gold}}|}
\]

- 基于排序的分数。当语义相关性的次序重要时（例如“找出最相似的前 5 篇文章”），基于集合的指标不够用。我们因此也使用归一化折损累积增益 nDCG@\(k\) [14]，这是标准的信息检索指标。它奖励把更相关的条目排得更靠前的模型。给定预测排序，nDCG@\(k\) 的计算原文按行抽取为：

```
DCG@k =
k
X
i=1
reli
log2(i + 1),
nDCG@k = DCG@k
IDCG@k
```

求和号在文本层显示为单独一行的 `X`。按可见的上下限和分式，可写为

\[
\mathrm{DCG@}k = \sum_{i=1}^{k} \frac{\mathrm{rel}_i}{\log_2(i+1)}, \quad
\mathrm{nDCG@}k = \frac{\mathrm{DCG@}k}{\mathrm{IDCG@}k}
\]

若 `X` 并不是求和号，公式抽取不完整，见原 PDF 第 7 页。其中 \(\mathrm{rel}_i\) 是排在第 \(i\) 位的条目的相关性（若属于 \(R_{\mathrm{gold}}\) 则为 1，否则为 0），IDCG 是理想排序的 DCG。MRR、MAP 等其他信息检索指标同样适用 [15], [16]。

<!-- 原 PDF 第 8 页 -->

- 分解准确率。为了诊断模型为什么失败，我们把评测拆成两个正交部分：SQL 骨架是否正确，以及向量检索部分是否正确。
  - SQL 骨架准确率（\(\mathrm{ACC}_{\mathrm{SQL}}\)）。该指标评估查询中非向量部分的结构是否正确。我们用基于大语言模型的评估器解析查询，并分别核对核心子句：FROM（含表和 JOIN 条件）、SELECT（列与聚合）、WHERE（非向量条件）、GROUP BY，以及 ORDER BY（非向量排序）。一条查询的 \(\mathrm{ACC}_{\mathrm{SQL}}\) 为 1，当且仅当它的全部结构分量都被判为正确。
  - 向量分量准确率（\(\mathrm{ACC}_{\mathrm{Vec}}\)）。该指标单独衡量模型能否正确解释用户的非结构化语义。若预测查询选错了向量列，这项应为 0。否则，用预测关键词的嵌入与专家标注的真值关键词嵌入之间的余弦相似度来评估关键词质量（即 BertScore [17]）。这样可以承受措辞差异，例如 “AI research” 与 “papers on artificial intelligence”。

### C. UniVectorSQL：开源 Text-to-VectorSQL 大语言模型

利用 VectorSQLGen 的合成数据，我们提出 UniVectorSQL，一族开源 Text2VectorSQL 模型，规模为 7B、14B 和 32B。本节说明输入输出序列的格式，以及训练目标和策略。

**1）输入与输出的构造。** 输入序列包括任务定义、数据库模式、VectorSQL 语法与说明，以及一个自然语言问题。遵循已有工作 [8], [18]–[20]，我们把模式写成 CREATE TABLE 语句，并用注释补充四类信息：（1）列描述，帮助模型在列名有歧义（例如缩写）时找对问题所指的列；（2）代表性取值，让模型知道库存值的格式，从而会用 STRFTIME 这类函数；（3）与问题相关的取值，帮助模型在问题提到具体数据库值时写出准确谓词；（4）向量元数据，告诉模型嵌入列的内容和来源，例如 “A 384-dim semantic vector for the paper abstract from all-MiniLM-L6-v2 encoder”（由 all-MiniLM-L6-v2 编码器得到的、论文摘要的 384 维语义向量），从而理解嵌入列，并自动选择嵌入模型。提示中还放入 VectorSQL 语法，以及带少样本示例的说明，使较小的大语言模型可以靠上下文学习完成 Text2VectorSQL。输出序列是带最终 VectorSQL 的向量感知思维链，由 VectorSQLGen 生成。

**2）训练目标与策略。** UniVectorSQL 由开源模型微调而来。我们使用标准的自回归语言建模目标：在给定前文的条件下预测下一个词元。损失的原文抽取为：

```
Loss = −E(x,y)∼D [P
t log Pθ(yt | x, y<t)] ,
(1)
```

公式抽取不完整，见原 PDF 第 8 页。这里 \(x\) 是上述输入序列，\(y\) 是目标输出，即专门的向量感知思维链。为了让 UniVectorSQL 擅长混合查询，同时保持复杂标准 SQL 上的能力，我们也考虑把合成的 Text2VectorSQL 语料与 SynSQL-2.5M [8] 等已有 Text-to-SQL 数据混合后再微调。这种混合训练让模型获得向量检索能力，同时保留传统 SQL 生成能力。实现细节放在第 IV-A3 节。

## IV. 实验

本节用大量实验检验所提出的生态，并指出后续研究要面对的挑战。

### A. 实验设置

**1）基准与指标。** 主实验在 VectorSQLBench 上进行。该基准由四种数据源构成：BIRD、Spider、arXiv 和 Wikipedia。为考察稳健性和通用性，全部模型都在三种 VectorSQL 语法不同的数据库后端上评测：SQLite（配合 sqlite-vec）、PostgreSQL（配合 pgvector）和 ClickHouse。整体评测使用基于排序的分数（nDCG@10）、基于集合的分数（F1）以及用于诊断的分解准确率。训练数据混合实验还使用 BRID-dev 基准和执行准确率。

**2）基线。** 我们把 UniVectorSQL 与一批开源和闭源大语言模型比较。（1）我们的模型：UniVectorSQL-7B、UniVectorSQL-14B、UniVectorSQL-32B，以及对应的 LoRA 微调版本。（2）闭源模型：Claude-3/4、GPT-4、Gemini-2.5 和 Grok-3/4 系列，作为当时高水平结果的参照。（3）开源模型：包括领先的指令微调与代码模型，如 Meta-Llama-3.1 [21]、Qwen2.5-Coder [22]、DeepSeek-Coder [23] 和 OmniSQL [8]。开源模型再按规模分为约 7B–8B、14B–22B，以及大于 32B 的模型，例如 DeepSeek-V3.1 [24]。

**3）实现细节。** UniVectorSQL 由开源 OmniSQL 微调得到。OmniSQL 本身是在 Qwen2.5-Coder 上微调的自然语言到 SQL 模型，而 Qwen2.5-Coder 在 92 种编程语言上训练 [25]。UniVectorSQL-7B 与 UniVectorSQL-14B 做全量微调；UniVectorSQL-32B 使用低秩适配（LoRA）[26] 做参数高效微调。训练数据包括我们的 SynVecSQL 语料，以及可选的


<!-- 原 PDF 第 9 页 -->

**表 II：** 各大型语言模型在 VectorSQLBench 上、跨三种数据库后端的性能（nDCG@10）与执行成功率（%）。我们的 UniVectorSQL 在合成数据 SynVecSQL-24K 上微调后，在开源模型中达到当时最优，并与顶尖专有 API 相当。为保证公平，各模型的输入提示相同。原文称每一类中的最佳结果用粗体标出；文本层没有粗体信息，见原 PDF 第 9 页。“DSC” 是 “DeepSeek-Coder” 的缩写。单元格为 nDCG@10 / 执行成功率。`find_tables` 把同一栏中的多个模型挤进同一个单元格；下表按每个模型名之后连续出现的 13 个配对回排，列顺序为 SQLite、PostgreSQL、ClickHouse 下的 BIRD、Spider、arXiv、Wiki，最后是平均，并与 `find_tables` 的列分组一致。模型顺序为：闭源；开源（约 7B）；开源（14B–32B）；开源（≥32B）。

| 模型 | SQLite BIRD | SQLite Spider | SQLite arXiv | SQLite Wiki | PostgreSQL BIRD | PostgreSQL Spider | PostgreSQL arXiv | PostgreSQL Wiki | ClickHouse BIRD | ClickHouse Spider | ClickHouse arXiv | ClickHouse Wiki | 平均 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Claude-3.5-Haiku | 28.7/57.5 | 27.2/59.7 | 13.7/51.7 | 20.1/58.6 | 39.0/82.2 | 34.9/75.2 | 17.6/90.9 | 31.7/85.0 | 35.6/92.7 | 39.7/91.6 | 27.0/89.9 | 33.8/92.4 | 29.1/77.3 |
| Claude-3.7-Sonnet | 36.7/68.8 | 35.2/74.7 | 29.8/69.7 | 28.9/66.9 | 42.9/85.3 | 50.0/90.3 | 35.9/89.1 | 36.5/91.7 | 42.5/96.4 | 47.3/94.1 | 39.7/94.9 | 36.9/94.7 | 38.5/84.7 |
| Claude-4-Sonnet | 37.9/70.9 | 41.2/81.2 | 25.3/59.6 | 28.1/74.5 | 46.7/95.0 | 52.7/97.3 | 35.8/98.2 | 40.8/97.5 | 46.6/97.4 | 43.9/98.3 | 37.1/94.9 | 38.6/98.5 | 39.6/88.6 |
| GPT-4o-mini | 28.3/65.7 | 33.4/71.5 | 24.9/53.9 | 22.6/61.1 | 44.6/83.8 | 41.9/89.4 | 30.0/81.8 | 47.6/95.0 | 34.2/87.2 | 33.0/90.8 | 32.5/83.5 | 31.8/97.0 | 33.7/80.1 |
| GPT-4-Turbo | 30.8/50.0 | 27.9/59.1 | 21.8/44.9 | 26.7/58.6 | 47.8/90.7 | 46.0/90.3 | 38.8/92.7 | 43.5/95.0 | 34.6/90.1 | 36.8/90.8 | 32.4/92.4 | 32.5/95.5 | 35.0/79.2 |
| GPT-4o | 48.3/79.6 | 38.1/79.0 | 39.9/83.1 | 36.6/80.9 | 51.2/91.9 | 50.1/89.4 | 36.8/87.3 | 41.6/95.0 | 47.4/94.9 | 42.5/95.8 | 40.3/93.7 | 31.4/95.5 | 42.0/88.8 |
| Gemini-2.5-Flash | 34.9/62.7 | 31.8/61.8 | 21.1/52.8 | 14.7/41.4 | 39.9/75.3 | 32.6/66.4 | 37.2/96.4 | 43.0/91.7 | 40.7/86.9 | 39.5/82.4 | 33.7/89.9 | 37.9/82.6 | 33.9/74.2 |
| Gemini-2.5-Pro | 34.1/60.3 | 29.6/62.9 | 26.2/69.7 | 24.7/63.1 | 35.7/66.4 | 25.8/54.0 | 22.8/58.2 | 11.7/23.3 | 37.3/68.6 | 25.7/65.5 | 26.4/69.6 | 25.6/57.6 | 27.1/59.9 |
| Grok-3 | 47.2/92.3 | 19.1/38.2 | 38.0/89.9 | 38.9/93.6 | 44.1/96.9 | 51.3/92.0 | 39.0/96.4 | 39.0/95.8 | 41.1/96.7 | 39.1/95.8 | 37.1/96.2 | 40.9/97.0 | 39.6/90.1 |
| Grok-4 | 41.9/75.6 | 38.8/83.3 | 22.9/75.3 | 27.2/81.5 | 41.4/98.1 | 47.6/98.2 | 30.8/98.2 | 32.5/96.7 | 45.0/93.4 | 42.8/95.0 | 29.8/88.6 | 37.6/89.4 | 36.5/89.4 |
| DSC-6.7B-Instruct | 12.8/35.4 | 15.1/41.4 | 6.3/20.2 | 12.6/28.0 | 12.8/32.4 | 6.9/15.9 | 24.6/87.3 | 19.2/49.2 | 16.0/36.9 | 17.2/50.4 | 17.4/53.2 | 7.7/25.8 | 14.0/39.7 |
| Qwen2.5-Coder-7B-Instruct | 18.2/43.7 | 19.5/54.8 | 9.2/38.2 | 8.8/28.0 | 9.9/34.7 | 14.8/34.5 | 17.4/56.4 | 16.4/45.0 | 22.7/64.2 | 22.4/61.3 | 29.0/75.9 | 24.1/62.9 | 17.7/50.0 |
| Qwen2.5-7B-Instruct | 22.3/48.6 | 23.7/55.9 | 16.3/41.6 | 17.1/51.0 | 25.8/64.1 | 25.4/59.3 | 27.9/78.2 | 25.3/78.3 | 22.3/62.0 | 19.9/62.2 | 15.1/48.1 | 19.0/53.0 | 21.7/58.5 |
| OmniSQL-7B | 24.0/65.9 | 27.5/74.6 | 15.8/51.7 | 25.4/70.1 | 17.4/39.4 | 9.1/31.9 | 25.3/67.3 | 19.6/45.8 | 26.6/79.9 | 22.1/74.8 | 31.4/89.9 | 26.4/78.0 | 22.5/64.1 |
| OpenCoder-8B-Instruct | 15.9/36.9 | 21.8/52.2 | 12.7/48.3 | 17.3/46.5 | 14.0/32.0 | 10.7/24.8 | 22.2/80.0 | 16.3/50.8 | 24.9/57.3 | 23.8/60.5 | 26.5/82.3 | 15.9/37.1 | 18.5/50.7 |
| Meta-Llama-3.1-8B-Instruct | 12.7/41.1 | 14.1/44.6 | 12.5/40.4 | 9.5/35.0 | 10.4/36.7 | 12.4/35.4 | 11.0/63.6 | 10.8/28.3 | 16.6/42.3 | 20.8/55.5 | 19.4/65.8 | 15.9/39.4 | 13.8/44.0 |
| UniVectorSQL-7B-LoRA | 37.1/79.6 | 35.6/82.8 | 30.7/77.7 | 28.1/79.0 | 39.7/90.6 | 42.1/91.5 | 37.8/95.9 | 39.6/94.5 | 44.7/96.0 | 42.6/95.3 | 41.1/96.6 | 38.6/95.7 | 38.1/89.6 |
| UniVectorSQL-7B | 38.3/81.0 | 36.8/84.2 | 31.9/79.1 | 29.3/80.4 | 40.9/92.0 | 43.3/92.9 | 39.0/97.2 | 40.8/95.9 | 45.9/97.3 | 43.8/96.6 | 42.3/97.9 | 39.8/97.0 | 39.3/91.0 |
| Qwen2.5-Coder-14B-Instruct | 25.2/57.0 | 22.7/59.3 | 16.3/43.9 | 21.7/55.9 | 19.4/50.0 | 20.0/54.2 | 16.4/47.8 | 7.1/19.7 | 32.1/81.2 | 36.4/81.0 | 34.4/89.7 | 39.7/94.6 | 24.3/61.2 |
| Qwen2.5-14B-Instruct | 30.5/60.6 | 30.5/62.4 | 15.4/42.7 | 23.2/61.1 | 36.1/82.2 | 31.8/80.5 | 37.9/90.9 | 36.0/84.2 | 37.8/82.8 | 31.4/88.2 | 31.3/92.4 | 35.2/90.2 | 31.4/76.5 |
| OmniSQL-14B | 36.6/73.0 | 30.7/73.7 | 23.7/64.0 | 25.3/65.0 | 20.9/51.7 | 20.4/47.8 | 20.4/61.8 | 15.5/40.8 | 39.0/86.9 | 35.8/84.9 | 31.7/91.1 | 31.1/86.4 | 27.6/68.9 |
| StarCoder2-15B-Instruct | 16.2/41.2 | 16.2/50.0 | 14.2/38.1 | 12.6/29.4 | 10.4/22.8 | 4.1/10.0 | 19.9/61.1 | 10.7/34.5 | 25.0/59.8 | 25.2/68.1 | 25.1/66.7 | 13.3/41.3 | 16.1/43.6 |
| DSC-V2-Lite-In. (16B, MoE) | 11.9/34.9 | 13.4/40.0 | 10.0/44.9 | 9.8/44.1 | 11.5/28.9 | 11.8/26.5 | 0.0/13.5 | 15.6/49.1 | 18.6/45.3 | 24.0/58.5 | 11.2/78.5 | 16.0/55.8 | 12.8/43.3 |
| Codestral-22B | 28.4/49.1 | 25.9/55.4 | 12.7/32.6 | 26.6/56.1 | 34.9/68.3 | 28.5/59.3 | 33.1/78.2 | 43.0/89.2 | 38.4/86.1 | 36.4/79.8 | 32.6/83.5 | 37.5/86.4 | 31.5/68.7 |
| UniVectorSQL-14B-LoRA | 40.5/84.5 | 38.5/86.6 | 34.5/82.5 | 32.0/84.0 | 43.5/94.0 | 45.5/94.6 | 41.0/97.7 | 42.5/96.6 | 47.5/98.0 | 45.5/97.5 | 44.0/98.5 | 41.5/97.7 | 41.4/92.7 |
| UniVectorSQL-14B | 40.8/85.0 | 38.8/87.1 | 34.8/83.0 | 32.3/84.5 | 43.8/94.5 | 45.8/95.1 | 41.3/98.1 | 42.8/97.1 | 47.8/98.4 | 45.8/97.9 | 44.3/98.9 | 41.8/98.1 | 41.7/93.1 |
| Qwen2.5-Coder-32B-Instruct | 26.9/57.8 | 27.6/65.8 | 23.5/46.1 | 25.5/65.2 | 32.0/74.3 | 34.3/69.9 | 40.7/92.7 | 35.8/83.2 | 33.7/79.9 | 28.3/73.1 | 33.9/84.8 | 37.5/92.4 | 31.6/73.8 |
| Qwen2.5-32B-Instruct | 37.0/64.8 | 35.4/66.7 | 20.5/50.6 | 28.2/65.0 | 39.8/75.3 | 36.1/77.0 | 21.8/72.7 | 35.4/84.2 | 40.4/88.0 | 36.1/87.4 | 34.0/91.1 | 31.1/75.0 | 33.0/74.8 |
| OmniSQL-32B | 31.2/61.7 | 24.6/67.2 | 24.6/48.3 | 29.3/65.6 | 34.3/76.1 | 35.3/78.8 | 30.9/83.6 | 28.4/70.8 | 30.7/67.9 | 26.3/64.7 | 30.6/81.0 | 30.0/83.3 | 29.7/70.8 |
| DSC-33B-Instruct | 18.5/45.3 | 17.9/51.4 | 7.2/29.2 | 14.6/40.8 | 9.6/23.9 | 4.6/9.8 | 15.4/80.0 | 8.8/26.9 | 23.4/64.8 | 23.8/69.7 | 21.9/83.5 | 22.8/65.2 | 15.7/49.2 |
| Meta-Llama-3.1-70B-Instruct | 28.3/53.8 | 22.9/61.3 | 19.9/50.6 | 19.5/56.7 | 30.5/71.0 | 40.3/75.2 | 32.7/89.1 | 5.2/11.7 | 38.9/87.2 | 34.2/85.7 | 34.0/86.1 | 36.3/92.4 | 28.6/68.4 |
| Qwen2.5-72B-Instruct | 43.4/73.5 | 38.0/70.4 | 23.9/59.6 | 32.0/66.2 | 41.4/86.1 | 37.8/77.9 | 41.1/94.5 | 43.6/88.3 | 39.4/88.0 | 37.8/86.6 | 37.8/83.5 | 37.4/87.9 | 37.8/80.2 |
| DeepSeek-V3.1 (671B, MoE) | 43.7/84.3 | 42.3/84.9 | 34.4/79.8 | 29.4/83.4 | 47.6/92.7 | 50.9/92.9 | 45.4/100.0 | 38.6/93.3 | 42.6/95.6 | 44.6/97.5 | 36.1/96.2 | 37.9/95.5 | 41.1/91.3 |
| UniVectorSQL-32B | 41.8/86.1 | 39.8/88.0 | 35.8/84.1 | 33.3/85.3 | 44.8/95.5 | 46.8/96.0 | 42.3/98.5 | 43.8/97.6 | 48.8/98.9 | 46.8/98.4 | 45.3/99.3 | 42.8/98.6 | 42.7/93.9 |


上一页末句在本页续完：训练数据包括我们的 SynVecSQL 语料，以及可选的来自 OmniSQL 的 SynSQL 数据集，以便在数据混合实验中保留较强的标准 SQL 能力。LoRA 的秩 \(r = 256\)，\(\alpha = 512\)。我们使用 AdamW 优化器 [27]，参数为 \(\beta_1 = 0.9\)、\(\beta_2 = 0.95\)、\(\epsilon = 10^{-8}\)。原文把 \(\epsilon\) 写成 `10−8`。UniVectorSQL-7B、UniVectorSQL-14B 和 UniVectorSQL-32B 的峰值学习率分别设为 2e−5、4e−6 和 2e−4。学习率在前 5% 的训练步做线性预热，再按余弦衰减到峰值的 10%。批大小、轮数（带早停）、上下文长度、权重衰减和梯度裁剪统一设为 64、2、8192、0.1 和 1.0。训练时用 DeepSpeed 的 bfloat16 混合精度和 ZeRO3 [28] 以节省显存。实际中，UniVectorSQL-7B/14B/32B 在一台配有 4 块 NVIDIA A100-SXM4-80GB GPU 的机器上一天内训完。我们也提供 UniVectorSQL-7B 和 UniVectorSQL-14B 的 LoRA 版本（记为 UniVectorSQL-7B-LoRA 和 UniVectorSQL-14B-LoRA），超参数与 UniVectorSQL-32B 相同，以便直接比较全量微调与 LoRA。嵌入模型方面，BIRD、Spider、arXiv 以及训练数据合成使用 all-MiniLM-L6-v2 [29]；Wikipedia 使用 CLIP-ViT-B-32-laion2B [30]。评测后端为 SQLite 3.46（配合 SQLite-vec 0.1.6）、PostgreSQL 14.18 和 ClickHouse 25.9。为贴近真实评测，我们保留默认执行设置，但把执行超时设为 60 秒，并在 ClickHouse 和 PostgreSQL 上建立 HNSW 索引，以加速向量检索和查询评测。

### B. 总体性能

表 II 给出主要评测结果，把 UniVectorSQL 与大量开源和专有大语言模型作比较。我们的模型在 SynVecSQL-24K 上微调后，在全部开源对照中处于明显领先。UniVectorSQL-7B 的平均 nDCG@10 为 39.3，执行成功率为 91.8%，大幅优于同规模的其他模型，例如 OmniSQL-7B

<!-- 原 PDF 第 10 页 -->

（nDCG@10 为 22.5）和 Qwen2.5-Coder-7B（nDCG@10 为 17.7）。性能随规模提升：UniVectorSQL-32B 达到 42.7 的 nDCG@10，超过规模大得多的 DeepSeek-V3.1（41.1）和 Qwen2.5-72B（37.8）。正文所写的 UniVectorSQL-7B 成功率为 91.8%；表 II 中该模型平均一栏为 39.3/91.0。

与领先的闭源 API 相比，UniVectorSQL-32B 很有竞争力（42.7），并略高于 GPT-4o（42.0）、Grok-3（39.6）和 Claude-4-Sonnet（39.6）。UniVectorSQL-32B 的执行成功率（93.9%）也高于 GPT-4o（88.8%），说明它在三种数据库后端上都能较稳定地生成语法正确的查询。

结果也说明 Text2VectorSQL 本身很难：即便是 OmniSQL 和 DeepSeek-Coder 这样较强的 Text-to-SQL 模型，若没有专门微调，表现也很差。

### C. 消融与讨论

为检验关键设计并提供更深入的认识，我们做了一系列消融和讨论。我们考察四个方面：训练数据混合的影响、思维链是否有效、召回下降现象，以及直观的案例。

**a）训练数据混合的影响。** 表 III 给出训练数据构成的消融。比较的起点是原本在 SynSQL 上训练的 OmniSQL-7B。基础 OmniSQL 在标准 BIRD 基准上表现尚可（EX 为 63.9%），但做不好新的 Text2VectorSQL 任务，在 VectorSQLBench 上的 nDCG@\(k\) 只有 22.5%。分解准确率显示，它有时能生成合法的 SQL 骨架（\(\mathrm{ACC}_{\mathrm{SQL}}\) 为 83.2%），但写不出向量分量（\(\mathrm{ACC}_{\mathrm{Vec}}\) 为 41.3%）。

只在我们的 SynVecSQL 上训练的模型（比例 1:0）在 VectorSQLBench 上最高（nDCG@\(k\) 为 39.3），说明该数据对目标任务有效。代价是标准 Text-to-SQL 下降（BIRD-dev 上 EX 为 58.2），出现明显的灾难性遗忘，原先的 SQL 能力变弱。

把 SynSQL 加进训练混合可以缓解这一点。随着 SynSQL 比例提高，BIRD-dev 上的表现回升，在 1:4 时 EX 达到 63.2。与此同时，VectorSQLBench 下降到 nDCG@\(k\) 为 32.7。这说明高质量的数据准备和混合很重要。

1:1 的混合取得较好平衡：BIRD-dev 上 EX 为 61.5，VectorSQLBench 上 nDCG@\(k\) 为 37.8。模型既获得向量检索能力，又保持对复杂传统 SQL 的掌握，说明混合训练对统一查询接口是必要的。由于本文的重点是为 Text2VectorSQL 建立稳健基线，UniVectorSQL 采用了纯 SynVecSQL（1:0）。

**表 III：** 在 UniVectorSQL-7B 上对训练数据构成做消融。评测包括 BIRD-dev（执行准确率）和 VectorSQLBench（nDCG@\(k\) 与分解准确率）。混合训练的综合表现最好，说明需要混合训练策略。`find_tables` 未返回该表；数字按页面文本顺序对齐，并与正文中的 63.9、22.5、83.2、41.3、39.3、58.2、63.2、32.7、61.5、37.8 一致。

| 混合比例（SynVecSQL:SynSQL） | BIRD-dev EX（%） | VectorSQLBench nDCG@k（%） | ACCSQL（%） | ACCVec（%） |
| --- | --- | --- | --- | --- |
| OmniSQL-7B | 63.9 | 22.5 | 83.2 | 41.3 |
| 1:0 | 58.2 | 39.3 | 89.7 | 78.5 |
| 1:1 | 61.5 | 37.8 | 88.3 | 76.2 |
| 1:2 | 62.8 | 35.4 | 87.1 | 72.9 |
| 2:1 | 60.1 | 38.5 | 89.1 | 77.8 |
| 1:4 | 63.2 | 32.7 | 85.9 | 68.4 |
| 4:1 | 58.3 | 39.1 | 89.4 | 78.1 |

**b）思维链的影响。** 为量化结构化推理的收益，我们消融了微调时是否加入思维链。每个 UniVectorSQL 规模都训练两个版本：一个使用包含思维链的完整训练序列（“有思维链”），另一个直接把输入映射到最终 VectorSQL（“无思维链”）。表 IV 显示，使用思维链后，各规模都有稳定提升。

例如，带思维链的 UniVectorSQL-32B 平均 nDCG@10 为 42.7，比无思维链的 39.5 高 3.2。查询可靠性也同步提高，执行成功率从 89.7% 升到 93.9%。7B 和 14B 上有类似增益。这说明，训练模型把推理过程明确写出来，对掌握 Text2VectorSQL 这种复杂的混合任务很关键。

这种提升可以归因于思维链起到了认知支架的作用。Text2VectorSQL 特别复杂，因为模型必须同时走两条推理路径：关系数据上的结构化 SQL 谓词，以及非结构化数据上的语义向量检索。我们专门的思维链（见第 III-A4 节）迫使模型先分解混合意图，分别规划 SQL 与向量部分，再考虑如何组装。逐步过程显著降低任务难度，帮助模型避开语法错误和逻辑谬误，从而生成更准确、更稳健的查询。

**c）召回下降现象。** 混合查询执行中一个关键、且在 Text2VectorSQL 语境下很少被考察的挑战，是召回下降。实践中，PostgreSQL 和 ClickHouse 为了效率都采用后过滤，但这也有明显风险：真正满足 SQL 谓词的 top-\(k\) 结果，可能不在向量检索结果里。我们的分析表明，这一现象在复杂 VectorSQL 上更加突出，尤其是带 JOIN 的查询。也就是说，JOIN 子句会成为一种选择性很高、且依赖于数据的

<!-- 原 PDF 第 11 页 -->

过滤器，标准 ANN 索引无法预先料到它。为定量刻画这一问题，我们在 PostgreSQL 和 ClickHouse 上评测了三个有代表性的模型（Claude-4-Sonnet、OmniSQL-32B 和我们的 UniVectorSQL-7B），并按第 III-A2 节定义的向量集成复杂度分段。

图 5 给出了清楚的证据。所有模型上，平均召回（橙色柱）都随查询从简单的非集成走到 WHERE 集成而明显下降，并在最复杂的 JOIN 集成中大幅下跌。例如在 ClickHouse 上，UniVectorSQL-7B 的召回下降超过 30%（从非集成的 0.6 降到 JOIN 集成的 0.4）。PostgreSQL 也有这个问题，但下降轻得多。事实上，pgvector 引入了迭代索引扫描 [31]。该机制会自动扫描索引中更多部分，直到找到足够多的结果，从而缓解后过滤造成的召回下降。

比较 ClickHouse 与 PostgreSQL 上的召回下降，可以把问题本身的复杂度因素分离出来，并说明：后过滤这一执行策略，尤其是再叠上复杂的 SQL 连接，会取不回很大一部分正确结果。因此 Text2VectorSQL 不只是翻译问题，它和底层数据库的执行策略、查询优化能力紧紧连在一起。

**表 IV：** 思维链影响的消融。表中是 UniVectorSQL 在有、无思维链时，于 VectorSQLBench 上跨三种数据库后端的 nDCG@10 与执行成功率（%）。思维链在各规模上都带来稳定且可观的提升，小模型上尤其明显。单元格为 nDCG@10 / 执行成功率。数字按页面文本中每个设置之后的 13 个配对排列，并与 `find_tables` 的列分组一致。有思维链的行与表 II 中对应的 UniVectorSQL 全量模型一致。

| 模型 | 设置 | SQLite BIRD | SQLite Spider | SQLite arXiv | SQLite Wiki | PostgreSQL BIRD | PostgreSQL Spider | PostgreSQL arXiv | PostgreSQL Wiki | ClickHouse BIRD | ClickHouse Spider | ClickHouse arXiv | ClickHouse Wiki | 平均 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UniVectorSQL-7B | 无思维链 | 33.9/74.6 | 32.4/77.8 | 27.5/72.7 | 24.9/74.0 | 36.5/85.6 | 38.9/86.5 | 34.6/90.8 | 36.4/89.5 | 41.5/90.9 | 39.4/90.2 | 37.9/91.5 | 35.4/90.6 | 34.9/84.6 |
| UniVectorSQL-7B | 有思维链 | 38.3/81.0 | 36.8/84.2 | 31.9/79.1 | 29.3/80.4 | 40.9/92.0 | 43.3/92.9 | 39.0/97.2 | 40.8/95.9 | 45.9/97.3 | 43.8/96.6 | 42.3/97.9 | 39.8/97.0 | 39.3/91.0 |
| UniVectorSQL-14B | 无思维链 | 36.6/78.8 | 34.6/80.9 | 30.6/76.8 | 28.1/78.3 | 39.6/88.3 | 41.6/88.9 | 37.1/91.9 | 38.6/90.9 | 43.6/92.2 | 41.6/91.7 | 40.1/92.7 | 37.6/91.9 | 37.5/86.9 |
| UniVectorSQL-14B | 有思维链 | 40.8/85.0 | 38.8/87.1 | 34.8/83.0 | 32.3/84.5 | 43.8/94.5 | 45.8/95.1 | 41.3/98.1 | 42.8/97.1 | 47.8/98.4 | 45.8/97.9 | 44.3/98.9 | 41.8/98.1 | 41.7/93.1 |
| UniVectorSQL-32B | 无思维链 | 38.6/81.9 | 36.6/83.8 | 32.6/79.9 | 30.1/81.1 | 41.6/91.3 | 43.6/91.8 | 39.1/94.3 | 40.6/93.4 | 45.6/94.7 | 43.6/94.2 | 42.1/95.1 | 39.6/94.4 | 39.5/89.7 |
| UniVectorSQL-32B | 有思维链 | 41.8/86.1 | 39.8/88.0 | 35.8/84.1 | 33.3/85.3 | 44.8/95.5 | 46.8/96.0 | 42.3/98.5 | 43.8/97.6 | 48.8/98.9 | 46.8/98.4 | 45.3/99.3 | 42.8/98.6 | 42.7/93.9 |

**d）案例。** 为更直观地说明 Text2VectorSQL 的难点和我们模型的能力，表 V 给出一个对比案例。我们比较 UniVectorSQL-7B 与一个较强的开源基线 Qwen2.5-Coder-7B，看它们如何为一个典型的混合用户问题生成查询。这个例子指出一种常见而隐蔽的失败：模型分不清结构化过滤和语义检索主题的边界，从而写出逻辑有误的查询。

**表 V：** 一个复杂混合问题上的查询生成对比。UniVectorSQL 把结构化约束和语义约束分开；基线把二者混在一起，导致查询错误。

自然语言问题：“Find the 5 papers from the ICDE conference published after 2022 that are most related to query optimization techniques.”（找出 2022 年之后在 ICDE 会议上发表的、与查询优化技术最相关的 5 篇论文。）

UniVectorSQL-7B：

```sql
SELECT title, conference, publication_year
FROM papers WHERE conference = 'ICDE'
AND publication_year > 2022 ORDER BY
abstract_embedding <-> EMBED('query
optimization techniques') LIMIT 5;
```

分析：正确。模型成功分解了混合意图。它把结构化谓词（`conference = 'ICDE'`、`publication_year > 2022`）和语义检索主题（‘query optimization techniques’）分开，并组装成逻辑完整的查询。

Qwen2.5-Coder-7B：

```sql
SELECT title, conference, publication_year
FROM papers WHERE publication_year >
2022 ORDER BY abstract_embedding <->
EMBED('query optimization techniques on
ICDE') LIMIT 5;
```

分析：错误。基线正确处理了日期过滤，但没有区分结构化过滤和语义概念。它把 ICDE 会议这一约束混进检索主题，嵌入的是 “query optimization techniques on ICDE”。这从根本上改变了语义查询，更重要的是漏掉了必需的硬过滤（`WHERE conference = 'ICDE'`），结果在逻辑上不正确。

## V. 相关工作

**关系数据库与向量数据库。** 数据管理长期以关系数据库为主，它擅长用 SQL 存储和查询结构化数据。然而，随着非结构化数据爆炸式增长，预计将占全部数据的 80% 甚至 92.9% [1], [32]，一种新范式出现了。向量数据库已成为管理高维

**Text-to-SQL 框架与基准。** 把自然语言翻译成 SQL 的任务已经有很大变化：从早期用图神经网络增强的编码器–解码器来捕捉数据库模式关系 [39], [40]，到微调大规模预训练模型

<!-- 原 PDF 第 12 页 -->

嵌入的关键设施，这些嵌入来自文本和图像等非结构化来源。局部敏感哈希（LSH）[33]、乘积量化 [34]，以及 HNSW [35] 这类基于图的索引，使高效的近似最近邻检索成为可能。由此出现了 Faiss [36] 等开源库，以及 Milvus [37]、Pinecone [38] 和 MyScale [3] 等向量数据库。尽管有这些进展，关系和向量两种范式大体仍各自为政。一些系统开始集成向量运算，但通常仍依赖手工编写混合查询。要做出统一、易用的接口，缺口仍然很大。我们的任务 Text2VectorSQL 第一次在自然语言交互这一层把两边接起来。

**图 5：** 不同模型在 PostgreSQL 和 ClickHouse 上的召回下降。图中给出 VectorSQLBench 四个数据集上、按混合集成深度分组的平均精确率、平均召回和平均 F1。从非集成到 WHERE 集成，平均召回（橙色柱）严重下降，在 JOIN 集成查询中最明显，这是 Text2VectorSQL 执行中的关键挑战。除第 11 页正文已写出的数字（ClickHouse 上 UniVectorSQL-7B 从非集成的 0.6 降到 JOIN 集成的 0.4）外，各柱数值未从文本层抽出。图 5 的柱状数值抽取不完整，见原 PDF 第 12 页。

例如 T5 [41], [42]；最近则是基于大语言模型的智能体框架 [43]–[49]。这些框架把 Text-to-SQL 拆成模式链接、查询生成和自我纠正等子问题。这一进展很大程度上由一系列高质量基准推动和衡量。Spider [50] 这类开创性数据集建立了跨领域标准；后续基准引入新的复杂度，例如 BIRD [51] 中的执行效率、KaggleDBQA [52] 中的数据库文档，以及 MIMICSQL [53] 中细致的领域查询。然而，这些进展有一个共同限制：框架和基准都只处理结构化的关系数据。它们不能解释或生成涉及语义相似度或跨模态匹配的查询，而后者正是现代数据应用的核心。因此，无法评估同时做结构化和非结构化查询的能力。为填补这一空白，我们提出 VectorSQLBench，作为第一个为衡量并推动这一新的统一查询范式提供基础设施的基准，并用 UniVectorSQL 实现自动的 VectorSQL 翻译。这不只是提高 SQL 生成准确率，而是从根本上扩大能够回答的问题范围。

**过滤向量检索。** 过滤向量检索把 ANN 检索与基于属性的谓词结合起来，是 VectorSQL 一种众所周知的简化形式。两种典型策略是先过滤和后过滤 [54], [55]。先过滤先按结构化谓词缩小数据集，再在过滤后的子集上做 ANN。后过滤则先取出候选向量，再去掉不满足谓词的那些。后过滤直接且高效，但容易召回偏低，因为满足谓词的真正近邻未必在最初取出的候选里；当过滤器选择性很高时，这个问题会变得严重 [56]。为克服这些限制，已有大量工作构造同时考虑向量和属性信息的专用索引。其中包括对 DiskANN 这类基于图的索引的改造 [57], [58]，按属性对数据聚类的划分方法 [59], [60]，以及把属性直接融入向量索引结构的复合索引 [61], [62]。这些专用索引相对于朴素方法提高了效率和召回，但需要底层的程序化交互 [63], [64]，并且未必适用于复杂的 VectorSQL 场景。我们的工作第一次在 SQL 抽象层考察这些挑战，并表明 VectorSQL 的复杂度会加剧后过滤的召回问题。在追求统一查询接口时，这个关键问题被忽略了。

## VI. 结论

本文提出并形式化 Text2VectorSQL，这是一项用自然语言统一查询结构化与非结构化数据的新任务。为推动研究，我们建立了一套基础生态：可扩展的数据合成流水线 VectorSQLGen，以及该任务上第一个综合性基准 VectorSQLBench。由此得到的 UniVectorSQL 模型，作为开源方案达到了新的最优水平。关键的是，分析揭示了召回下降：把 JOIN 这类复杂 SQL 过滤与向量检索结合时，正确结果会被悄悄漏掉。这一发现把 Text2VectorSQL 从简单的翻译任务，提升为复杂的查询协同优化问题。本工作定义了任务、提供了工具并指出了关键挑战，为构建下一代统一数据接口奠定了必要基础。

## 致谢

本工作得到中国国家重点研发计划（2024YFA1014003）、国家自然科学基金（92470121、62402016）、CAAI-蚂蚁集团科研基金，以及北京大学高性能计算平台的支持。


<!-- 原 PDF 第 13 页 -->

## 人工智能生成内容致谢

我们说明，在准备本文时使用了生成式人工智能助手 Gemini-2.5-Pro [65]。该工具用于全文（第 I 节至第 VI 节），以改进语言、语法、用词和整体可读性。使用程度严格限于文字润色。所有核心科学贡献，包括 Text2VectorSQL 任务的形式化、VectorSQLGen 流水线与 VectorSQLBench 的设计、实验方法以及结果分析，都只由人类作者完成。作者仔细审阅并修改了全部人工智能建议，以保证最终内容准确，并反映他们自己的工作。

## 参考文献

[1] I. Corporate, 「非结构化数据占比超过 92.9%，IDC 发布 RAG 与向量数据库的市场展望」, 在线: https://my.idc.com/getdoc.jsp?containerId=prCHC52694924

[2] A. Kane, 「pgvector：面向 Postgres 的开源向量相似度检索」, https://github.com/pgvector/pgvector, 2024, accessed: 2024-05-24.

[3] O. Technology, 「面向可扩展人工智能的 SQL 向量数据库」, 2025. 在线: https://myscale.com/

[4] J. J. Pan, J. Wang, and G. Li, 「向量数据库管理系统综述」, The VLDB Journal, vol. 33, no. 5, pp. 1591–1615, 2024.

[5] J. J. Pan, J. Wang, and G. Li, 「向量数据库管理技术与系统」, in Companion of the 2024 International Conference on Management of Data, 2024, pp. 597–604.

[6] T. Taipalus, 「向量数据库管理系统：基本概念、用例与当前挑战」, Cognitive Systems Research, vol. 85, p. 101216, 2024.

[7] H. Li, S. Wu, X. Zhang, X. Huang, J. Zhang, F. Jiang, S. Wang, T. Zhang, J. Chen, R. Shi et al., 「OmniSQL：大规模合成高质量 Text-to-SQL 数据」, arXiv preprint arXiv:2503.02240, 2025.

[8] H. Li, S. Wu, X. Zhang, X. Huang, J. Zhang, F. Jiang, S. Wang, T. Zhang, J. Chen, R. Shi et al., 「OmniSQL：大规模合成高质量 Text-to-SQL 数据」, arXiv preprint arXiv:2503.02240, 2025.

[9] S. Edunov, M. Ott, M. Auli, and D. Grangier, 「理解大规模回译」, arXiv preprint arXiv:1808.09381, 2018.

[10] G. Rossiello, P. Basile, and G. Semeraro, 「借助词嵌入组合性的基于质心文本摘要」, in Proceedings of the Workshop on Summarization and Summary Evaluation Across Source Types and Genres, MultiLing@EACL 2017, Valencia, Spain, April 3, 2017. Association for Computational Linguistics, 2017, pp. 12–21.

[11] J. Li, B. Hui, G. Qu, B. Li, J. Yang, B. Li, B. Wang, B. Qin, R. Geng, N. Huo, X. Zhou, C. Ma, G. Li, K. C. C. Chang, F. Huang, R. Cheng, and Y. Li, 「大语言模型是否已经能充当数据库接口？面向大规模、以数据库为依据的 Text-to-SQL 的大型基准」, 2023.

[12] T. Yu, R. Zhang, K. Yang, M. Yasunaga, D. Wang, Z. Li, J. Ma, I. Li, Q. Yao, S. Roman, Z. Zhang, and D. Radev, 「Spider：面向复杂跨领域语义解析与 Text-to-SQL 任务的大规模人工标注数据集」, in Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing. Brussels, Belgium: Association for Computational Linguistics, 2018.

[13] G. V. Cormack, C. L. Clarke, and S. Buettcher, 「倒数排名融合优于 Condorcet 方法与单独的排序学习方法」, in Proceedings of the 32nd international ACM SIGIR conference on Research and development in information retrieval, 2009, pp. 758–759.

[14] K. Järvelin and J. Kekäläinen, 「基于累积增益的信息检索技术评测」, ACM Transactions on Information Systems (TOIS), vol. 20, no. 4, pp. 422–446, 2002.

[15] P. Zhao, H. Zhang, Q. Yu, Z. Wang, Y. Geng, F. Fu, L. Yang, W. Zhang, J. Jiang, and B. Cui, 「面向人工智能生成内容的检索增强生成：综述」, arXiv preprint arXiv:2402.19473, 2024.

[16] Z. Wang, Q. Yu, S. Wei, Z. Li, F. Xiong, X. Wang, S. Niu, H. Liang, and W. Zhang, 「QAEncoder：问答系统中面向对齐的表示学习」, Sep. 2024, arXiv:2409.20434 [cs]. 在线: http://arxiv.org/abs/2409.20434

[17] T. Zhang, V. Kishore, F. Wu, K. Q. Weinberger, and Y. Artzi, 「BERTScore：用 BERT 评测文本生成」, arXiv preprint arXiv:1904.09675, 2019.

[18] N. Rajkumar, R. Li, and D. Bahdanau, 「评测大语言模型的 Text-to-SQL 能力」, CoRR, vol. abs/2204.00498, 2022.

[19] H. Li, J. Zhang, H. Liu, J. Fan, X. Zhang, J. Zhu, R. Wei, H. Pan, C. Li, and H. Chen, 「Codes：构建面向 Text-to-SQL 的开源语言模型」, Proc. ACM Manag. Data, vol. 2, no. 3, p. 127, 2024.

[20] S. Talaei, M. Pourreza, Y. Chang, A. Mirhoseini, and A. Saberi, 「CHESS：为高效 SQL 合成而利用上下文」, CoRR, vol. abs/2405.16755, 2024.

[21] A. Dubey, A. Jauhri, A. Pandey, A. Kadian, A. Al-Dahle, A. Letman, A. Mathur, A. Schelten, A. Yang, A. Fan et al., 「Llama 3 模型群」, arXiv preprint arXiv:2407.21783, 2024.

[22] B. Hui, J. Yang, Z. Cui, J. Yang, D. Liu, L. Zhang, T. Liu, J. Zhang, B. Yu, K. Dang, A. Yang, and et al., 「Qwen2.5-Coder 技术报告」, CoRR, vol. abs/2409.12186, 2024.

[23] D. Guo, Q. Zhu, D. Yang, Z. Xie, K. Dong, W. Zhang, G. Chen, X. Bi, Y. Wu, and et al., 「DeepSeek-Coder：当大语言模型遇上编程——代码智能的兴起」, CoRR, vol. abs/2401.14196, 2024.

[24] DeepSeek-AI, 「DeepSeek-V3 技术报告」, CoRR, vol. abs/2412.19437, 2024.

[25] B. Hui, J. Yang, Z. Cui, J. Yang, D. Liu, L. Zhang, T. Liu, J. Zhang, B. Yu, K. Dang, A. Yang, R. Men, F. Huang, X. Ren, X. Ren, J. Zhou, and J. Lin, 「Qwen2.5-Coder 技术报告」, CoRR, vol. abs/2409.12186, 2024. 在线: https://doi.org/10.48550/arXiv.2409.12186

[26] E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, and W. Chen, 「LoRA：大语言模型的低秩适配」, in The Tenth International Conference on Learning Representations, ICLR 2022, Virtual Event, April 25-29, 2022. OpenReview.net, 2022.

[27] I. Loshchilov and F. Hutter, 「解耦的权重衰减正则」, in 7th International Conference on Learning Representations, ICLR 2019, New Orleans, LA, USA, May 6-9, 2019. OpenReview.net, 2019.

[28] S. Rajbhandari, J. Rasley, O. Ruwase, and Y. He, 「ZeRO：面向万亿参数模型训练的内存优化」, in Proceedings of the International Conference for High Performance Computing, Networking, Storage and Analysis, SC 2020, Virtual Event / Atlanta, Georgia, USA, November 9-19, 2020. IEEE/ACM, 2020, p. 20.

[29] N. Reimers and I. Gurevych, 「Sentence-BERT：用孪生 BERT 网络做句子嵌入」, in Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing. Association for Computational Linguistics, 11 2019. 在线: https://arxiv.org/abs/1908.10084

[30] A. Radford, J. W. Kim, C. Hallacy, A. Ramesh, G. Goh, S. Agarwal, G. Sastry, A. Askell, P. Mishkin, J. Clark, G. Krueger, and I. Sutskever, 「从自然语言监督中学习可迁移的视觉模型」, in ICML, 2021.

[31] J. Ni, X. Xu, Y. Wang, C. Li, J. Yao, S. Xiao, and X. Zhang, 「DiskANN++：用查询敏感的入口顶点，在同构映射的图索引上做高效的基于页检索」, arXiv preprint arXiv:2310.00402, 2023.

[32] T. King, 「五年之内，你的数据将有 80% 是非结构化的」, Data Management Solutions Review, 2019.

[33] M. S. Charikar, 「由舍入算法得到的相似度估计技术」, in Proceedings of the thiry-fourth annual ACM symposium on Theory of computing, 2002, pp. 380–388.

[34] H. Jegou, M. Douze, and C. Schmid, 「用于最近邻检索的乘积量化」, IEEE transactions on pattern analysis and machine intelligence, vol. 33, no. 1, pp. 117–128, 2010.

[35] Y. A. Malkov and D. A. Yashunin, 「用层次化可导航小世界图做高效且稳健的近似最近邻检索」, IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 42, no. 4, pp. 824–836, 2018.

[36] J. Johnson, M. Douze, and H. Jégou, 「用 GPU 做十亿规模的相似度检索」, IEEE Transactions on Big Data, vol. 7, no. 3, pp. 535–547, 2019. 在线: https://arxiv.org/abs/1702.08734

[37] J. Wang, X. Yi, R. Guo, H. Jin, P. Xu, S. Li, X. Wang, X. Guo, C. Li, X. Xu et al., 「Milvus：为向量数据管理专门构建的系统」, in Proceedings of the 2021 International Conference on Management of Data, 2021, pp. 2614–2627.

<!-- 原 PDF 第 14 页 -->

[38] S. Bruch, F. M. Nardini, A. Ingber, and E. Liberty, 「流式稀疏向量上最大内积检索的一种近似算法」, ACM Transactions on Information Systems, vol. 42, no. 2, pp. 1–43, 2023.

[39] B. Wang, R. Shin, X. Liu, O. Polozov, and M. Richardson, 「RAT-SQL：面向 Text-to-SQL 解析器的、关系感知的模式编码与链接」, in Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, ACL 2020, Online, July 5-10, 2020. Association for Computational Linguistics, 2020, pp. 7567–7578.

[40] R. Cao, L. Chen, Z. Chen, Y. Zhao, S. Zhu, and K. Yu, 「LGESQL：混合局部与非局部关系的线图增强 Text-to-SQL 模型」, in Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing, ACL/IJCNLP 2021, (Volume 1: Long Papers), Virtual Event, August 1-6, 2021. Association for Computational Linguistics, 2021, pp. 2541–2555.

[41] H. Li, J. Zhang, C. Li, and H. Chen, 「RESDSQL：为 Text-to-SQL 解耦模式链接与骨架解析」, in Thirty-Seventh AAAI Conference on Artificial Intelligence, AAAI 2023, Thirty-Fifth Conference on Innovative Applications of Artificial Intelligence, IAAI 2023, Thirteenth Symposium on Educational Advances in Artificial Intelligence, EAAI 2023, Washington, DC, USA, February 7-14, 2023. AAAI Press, 2023, pp. 13067–13075.

[42] T. Scholak, N. Schucher, and D. Bahdanau, 「PICARD：为语言模型的约束自回归解码做增量解析」, in Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, EMNLP 2021, Virtual Event / Punta Cana, Dominican Republic, 7-11 November, 2021, M. Moens, X. Huang, L. Specia, and S. W. Yih, Eds. Association for Computational Linguistics, 2021, pp. 9895–9901.

[43] M. Pourreza and D. Rafiei, 「DIN-SQL：带自我纠正的 Text-to-SQL 分解式上下文学习」, in Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023, 2023.

[44] D. Gao, H. Wang, Y. Li, X. Sun, Y. Qian, B. Ding, and J. Zhou, 「由大语言模型增强的 Text-to-SQL：一项基准评测」, Proc. VLDB Endow., vol. 17, no. 5, pp. 1132–1145, 2024.

[45] B. Wang, C. Ren, J. Yang, X. Liang, J. Bai, L. Chai, Z. Yan, Q. Zhang, D. Yin, X. Sun, and Z. Li, 「MAC-SQL：面向 Text-to-SQL 的多智能体协作框架」, in Proceedings of the 31st International Conference on Computational Linguistics, COLING 2025, Abu Dhabi, UAE, January 19-24, 2025. Association for Computational Linguistics, 2025, pp. 540–557.

[46] Y. Fan, T. Ren, C. Huang, Z. He, and X. S. Wang, 「用基于数据的自我解释，把自然语言落到 SQL 翻译上」, in 2025 IEEE 41st International Conference on Data Engineering (ICDE). IEEE, 2025, pp. 29–42.

[47] Y. Fan, Z. He, T. Ren, C. Huang, Y. Jing, K. Zhang, and X. S. Wang, 「MetaSQL：自然语言到 SQL 翻译的先生成再排序框架」, in 2024 IEEE 40th International Conference on Data Engineering (ICDE). IEEE, 2024, pp. 1765–1778.

[48] Y. Fan, T. Ren, Z. He, X. S. Wang, Y. Zhang, and X. Li, 「GenSQL：数据库系统的生成式自然语言接口」, in 2023 IEEE 39th International Conference on Data Engineering (ICDE). IEEE, 2023, pp. 3603–3606.

[49] Y. Chronis, H. Caminal, Y. Papakonstantinou, F. Özcan, and A. Ailamaki, 「过滤向量检索：现状与研究机会」, Proceedings of the VLDB Endowment, vol. 18, no. 12, pp. 5488–5492, 2025.

[50] T. Yu, R. Zhang, K. Yang, M. Yasunaga, D. Wang, Z. Li, J. Ma, I. Li, Q. Yao, S. Roman et al., 「Spider：面向复杂跨领域语义解析与 Text-to-SQL 任务的大规模人工标注数据集」, in Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing, 2018, pp. 3911–3921.

[51] J. Li, B. Hui, G. Qu, J. Yang, B. Li, B. Li, B. Wang, B. Qin, R. Geng, N. Huo et al., 「大语言模型是否已经能充当数据库接口？面向大规模、以数据库为依据的 Text-to-SQL 的大型基准」, Advances in Neural Information Processing Systems, vol. 36, 2024.

[52] C.-H. Lee, O. Polozov, and M. Richardson, 「KaggleDBQA：对 Text-to-SQL 解析器的现实评测」, in Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers), 2021, pp. 2261–2273.

[53] P. Wang, T. Shi, and C. K. Reddy, 「面向电子病历问答的 Text-to-SQL 生成」, in Proceedings of The Web Conference 2020, 2020, pp. 350–361.

[54] Q. Zhang, S. Xu, Q. Chen, G. Sui, J. Xie, Z. Cai, Y. Chen, Y. He, Y. Yang, F. Yang, M. Yang, and L. Zhou, 「VBASE：用放松的单调性统一在线向量相似度检索与关系查询」, in USENIX Symposium on Operating Systems Design and Implementation (OSDI), 2023, pp. 377–395.

[55] 「Milvus 文档：做一次混合检索」, 2022. 在线: https://github.com/milvus-io/milvus-docs/blob/v2.1.x/site/en/userGuide/search/hybridsearch.md

[56] S. Gollapudi, N. Karia, V. Sivashankar, R. Krishnaswamy, N. Begwani, S. Raz, Y. Lin, Y. Zhang, N. Mahapatro, P. Srinivasan, A. Singh, and H. V. Simhadri, 「Filtered-DiskANN：带过滤器的近似最近邻检索图算法」, in ACM Web Conference, 2023, p. 3406–3416.

[57] S. Jayaram Subramanya, F. Devvrit, H. V. Simhadri, R. Krishnawamy, and R. Kadekodi, 「DiskANN：在单节点上做快速、准确的十亿级最近邻检索」, Advances in Neural Information Processing Systems, vol. 32, 2019.

[58] S. Gollapudi, N. Karia, V. Sivashankar, R. Krishnaswamy, N. Begwani, S. Raz, Y. Lin, Y. Zhang, N. Mahapatro, P. Srinivasan et al., 「Filtered-DiskANN：带过滤器的近似最近邻检索图算法」, in Proceedings of the ACM Web Conference 2023, 2023, pp. 3406–3416.

[59] G. Gupta, J. Yi, B. Coleman, C. Luo, V. Lakshman, and A. Shrivastava, 「CAPS：面向过滤相似度检索的实用划分索引」, arXiv preprint arXiv:2308.15014, 2023.

[60] J. Mohoney, A. Pacaci, S. R. Chowdhury, A. Mousavi, I. F. Ilyas, U. F. Minhas, J. Pound, and T. Rekatsinas, 「知识图谱中的高吞吐向量相似度检索」, Proceedings of the ACM on Management of Data, vol. 1, no. 2, pp. 1–25, 2023.

[61] M. Wang, L. Lv, X. Xu, Y. Wang, Q. Yue, and J. Ni, 「由可导航邻近图驱动的、带结构化与非结构化约束的原生混合查询」, arXiv preprint arXiv:2203.13601, 2022.

[62] L. Patel, P. Kraft, C. Guestrin, and M. Zaharia, 「ACORN：在向量嵌入与结构化数据上做高性能、与谓词无关的检索」, Proc. ACM Manag. Data, vol. 2, no. 3, May 2024. 在线: https://doi.org/10.1145/3654923

[63] Z. Li, S. Huang, W. Ding, Y. Park, and J. Chen, 「Sieve：用一组索引做有效的过滤向量检索」, arXiv preprint arXiv:2507.11907, 2025.

[64] J. Engels, B. Landrum, S. Yu, L. Dhulipala, and J. Shun, 「带窗口过滤器的近似最近邻检索」, arXiv preprint arXiv:2402.00943, 2024.

[65] G. Comanici, E. Bieber, M. Schaekermann, I. Pasupat, N. Sachdeva, I. Dhillon, M. Blistein, O. Ram, D. Zhang, E. Rosen et al., 「Gemini 2.5：用高级推理、多模态、长上下文和下一代智能体能力推进前沿」, arXiv preprint arXiv:2507.06261, 2025.

<!-- 译完 -->
