# ScienceBenchmark: A Complex Real-World Benchmark for Evaluating Natural Language to SQL Systems

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`ScienceBenchmark_PVLDB2024_Stockinger.pdf`。

## Abstract 摘要

自然语言到 SQL 系统（Natural Language to SQL systems, NL-to-SQL）近期在把自然语言翻译为 SQL 查询方面的准确率有所提高（超过 80%），这得益于基于 transformer 的语言模型的出现，以及 Spider 基准的流行。然而，Spider 主要包含表、列与条目都很少的简单数据库，并不能反映真实设定。此外，带有领域特定内容的复杂真实世界数据库，几乎没有以 NL/SQL 对（NL/SQL-pairs）形式可用的训练数据，导致现有 NL-to-SQL 系统表现不佳。

本文引入 ScienceBenchmark，一个面向三个真实世界、高度领域特定数据库的新的复杂 NL-to-SQL 基准。针对这一新基准，SQL 专家与领域专家为每个领域创建了高质量的 NL/SQL 对。为收集更多数据，我们用 GPT-3 生成的合成数据扩展了少量人工生成的数据。我们表明，该基准极具挑战性：在 Spider 上表现最好的系统，在我们的基准上性能很低。因此，挑战是多方面的：要为高度复杂的领域创建 NL-to-SQL 系统，而可用的只有少量手工训练数据，并以合成数据加以扩充。据我们所知，ScienceBenchmark 是首个面向复杂真实世界科学数据库设计的 NL-to-SQL 基准，其中包含由领域专家仔细验证的、具有挑战性的训练与测试数据。

## 1 INTRODUCTION 引言

使用自然语言查询结构化数据，被视为实现数据民主化（data democratization）的关键。面向数据库的自然语言接口（Natural Language Interfaces for Databases，即 NL-to-SQL 系统）出现于 1970 年代 [1, 4]。早期系统依赖数据库模式，从自然语言（natural language, NL）查询构建 SQL 查询（例如 SODA [5]、Precis [40]），或聚焦于理解自然语言查询的结构，以将其映射到 SQL（例如 ATHENA [37]、NaLIR [24]）。早在 1995 年，基准的缺乏就已显而易见：“尚未制定标准基准 [...], 对该领域现状的任何评价都只能是印象式的” [4]。这一状况在近期发生了变化：首批大规模基准 WikiSQL [53] 与 Spider [51] 出现。它们使得神经机器翻译（neural machine translation, NMT）方法得以训练与评测（例如 [44, 48, 53]）。这些方法把 NL-to-SQL 问题表述为语言翻译问题，并用大量 NL/SQL 对训练神经网络。

第一批深度学习方法 [48, 53] 只能处理单表，无法生成跨越多表的复杂 SQL 查询（例如包含嵌套查询与复杂子句）；近期系统 [7, 8, 38, 44] 则能在完整数据库上工作，并在 Spider 基准 [51] 上取得高分。顶尖 NL-to-SQL 系统在 Spider 上的准确率高达 85%。然而，Spider 中的大多数数据库是专为该基准创建的，并不能代表为真实世界数据库创建自然语言接口时所面临的困难。在 Spider 上当前表现最好的开源系统中，T5-Large [32]（配合 Picard [38] 做约束解码（constrained decoding））、SmBoP [36]，以及带 NatSQL 的 RESDSQL [25]，性能已经超过 70%。把在 Spider 数据集上训练的系统应用到天体物理或癌症研究等新领域，结果很差，使这类系统走向真实应用显得极为不切实际。

问题在于：尽管 WikiSQL 与 Spider 提供了共同的训练与评测工具，对 NL-to-SQL 系统的发展具有变革意义，它们仍有严重局限。每条 WikiSQL 问题都指向单张表，而不是关系数据库。WikiSQL 查询复杂度低，使其对真实应用的价值实际上很有限。Spider 包含来自 138 个不同领域的 200 个关系数据库，以及超过 10,000 个自然语言问题和超过 5,000 条复杂 SQL 查询，因此它针对的是查询复杂度问题。同时，它也试图通过提供带有新数据库的开发集（dev set）来解决迁移学习（transfer learning）问题。

然而，Spider 基准中的大多数数据库相当简单，即复杂度低，且只包含被视为常识的内容。因此，我们需要专门的、领域特定的基准，以便在科学领域中训练和评测 NL-to-SQL 系统。由于所需的数据量以及科学领域所需的专业知识，手工打造这样的基准代价过高。数据增强（data augmentation），即自动生成基准，是唯一可行的解决方案。

**Our Approach. 我们的方法。** 本文引入 ScienceBenchmark，一个用于评测 NL-to-SQL 系统的复杂真实世界基准。它是首个与 SQL 专家以及研究政策制定（research policy making）、天体物理和癌症研究领域的研究者协作开发的此类基准。我们把来自人工收集训练数据的知识，与一套自动训练数据生成系统结合起来。该系统使那些训练时需要大量数据的 NL-to-SQL 系统，能够在原本训练数据稀缺或不可得的复杂科学数据库上起步。

数据增强系统的主要架构如图 1 所示。该系统输入一小批人工生成的 NL/SQL 对，以提供关于新领域的准确且在语义上高度相关的信息。从这些种子查询（seed queries）中抽取 SQL 模板，随后在考虑数据库模式与内容的前提下，用它们针对特定数据库生成 SQL 查询。这些 SQL 查询再借助大语言模型（large language model, LLM）GPT-3 [6] 回译（back-translated）为自然语言。对于本工作使用的 SQL-to-NL 组件，我们试验了当前最优的、基于 transformer 的预训练模型；它们在多个相关任务上取得当前最优分数，已展现出自然语言生成能力。我们的评测表明，GPT-3 [6] 模型性能最好，并且能够用极少样本泛化到新领域（在我们的情形中，这些样本就是种子 NL/SQL 对），因此被集成到我们的架构中。随后，用一个评判模型（critic model）过滤所得到的自然语言问题，为相应的 SQL 查询选出最相关的 NL 问题。由此得到的扩充 NL/SQL 对数据集，可以送入任何 NL-to-SQL 系统进行训练。我们的方法是通用的，并且能够提升任何 NL-to-SQL 系统的准确率，如表 5 中的实验所示。

图 1：自动训练数据生成的端到端架构，由四个阶段组成，即 (1) Seeding Phase（种子阶段）、(2) SQL Query Generation Phase（SQL 查询生成阶段）、(3) SQL-to-NL Translation Phase（SQL 到自然语言翻译阶段）与 (4) Discriminative Phase（判别阶段）。该方法用于产生我们称为 ScienceBenchmark 的新基准数据集。这些阶段的细节在第 3.3 节中描述。图中连线与各框的版面位置抽取不全，【抽取不清】。抽出的文字与示例如下。

种子问题（Seed Question）：Find all Starburst galaxies.（找出所有 Starburst 星系。）

种子 SQL（Seed SQL）：

```sql
SELECT specobjid
FROM specobj AS s
WHERE s.subclass = ' STARBURST'
```

种子 AST（Seed AST）：

```text
Select T(4) C(32)
Filter(2) T(4) C(49) V(0)
```

抽取的 AST 模板（Extracted AST Template）：

```text
Select T(*) C(*)
Filter(2) T(*) C(*) V(*)
```

生成的 AST (1)（Generated AST (1)）：

```text
Select T(0) C(1)
Filter(2) T(0) C(7) V(3)
```

生成的 SQL (1)（Generated SQL (1)）：

```sql
SELECT T1.objid
  FROM neighbors AS T1
WHERE T1.neighbormode = 2
```

生成的问题 (1)（Generated Questions (1)）：

- Find the center object which has nearest neighbor with neighbor mode 2（找出具有 neighbor mode 为 2 的最近邻的中心天体）
- Find the center id of nearest neighbor object with neighbor mode smaller than 2（找出 neighbor mode 小于 2 的最近邻天体的中心 id）

已验证问题 (1)（Validated Question (1)）：

- ✓ Find the center object of nearest neighbor with neighbor mode 2（找出 neighbor mode 为 2 的最近邻的中心天体）
- ⨯ Find the center id of nearest neighbor object with neighbor mode smaller than 2（找出 neighbor mode 小于 2 的最近邻天体的中心 id）

生成的 AST (2)（Generated AST (2)）：

```text
Select T(4) C(45)
Filter(2) T(4) C(37) V(0)
```

生成的 SQL (2)（Generated SQL (2)）：

```sql
SELECT T1.z
  FROM specobj AS T1
WHERE T1.survey = " eboss"
```

生成的问题 (2)（Generated Questions (2)）：

- Find redshift of spectroscopic objects with survey equal to 'eboss'（找出 survey 等于 'eboss' 的光谱天体（spectroscopic objects）的 redshift）
- What is the redshift of objects with survey not equal to ‘eboss’（survey 不等于 ‘eboss’ 的天体的 redshift 是什么）

已验证问题 (2)（Validated Question (2)）：

- ✓ Find redshift of spectroscopic objects with survey equal to 'eboss'（找出 survey 等于 'eboss' 的光谱天体的 redshift）
- ⨯ What is the redshift of objects with survey not equal to ‘eboss’（survey 不等于 ‘eboss’ 的天体的 redshift 是什么）

抽出的模式图例（取值缺失处标明）：

```text
T(0): neighbors
    C(7) - neighbormode
    C(1) - objid
    C(5) - neighbortype
V(0): 2
V(3): 3
T(4): specobj
    C(32): specobjid
    C(44): ancillary_target1
    C(48): class
V(0): ‘QSO’
V(1): …
V(2): …
V(3):18014398509481984
T(4): specobj
    C(37): survey
    C(45): z
    C(48): class
V(0) 【抽取不清】
V(1) 【抽取不清】
```

**Contributions. 贡献。** 本工作的主要贡献如下：

- 我们贡献 ScienceBenchmark——一个针对复杂科学数据库评测 NL-to-SQL 系统的新基准。ScienceBenchmark 包含超过 6,000 个 NL/SQL 对，帮助研究者应对真实世界数据库中那些被流行基准所忽视的复杂挑战。
- 我们用一种新方法构建 ScienceBenchmark，为几乎没有训练数据的数据库自动生成训练数据。与先前聚焦于相当简单的数据库的工作不同，我们专注于复杂的真实世界科学数据库；在这一领域，流行的 NL-to-SQL 系统通常因缺乏领域知识与训练数据而表现不佳。
- 我们在该基准上评测了三个当前最优的 NL-to-SQL 系统以及两个 LLM。尽管这些系统在 Spider 排行榜上取得顶尖分数（准确率高于 82%），没有一个在我们的基准上取得令人满意的分数（依领域不同，仅在 25-60% 准确率范围内），这展示了 ScienceBenchmark 的难度。

## 2 THE NEED FOR A NEW BENCHMARK - MOTIVATING EXAMPLE: ASTROPHYSICS 对新基准的需求——动机示例：天体物理学

NL-to-SQL 系统需要应对许多挑战 [1, 3, 18, 20]。一方面，自然语言问题可能含糊，包含即使对人类也难以理解的指称，并且使用与数据库中不同的词汇。另一方面，相应的 SQL 查询必须遵守严格的语法以及底层数据库模式，才能在语法和语义上正确。把 NL-to-SQL 系统应用于真实世界的科学数据库时，还会出现源于这些数据库的性质与领域的额外挑战。尽管 Spider 基准是首个带有复杂 SQL 查询的大规模数据集，其数据库并不能算复杂。它们的主题非常泛化，涵盖宠物以及娱乐（音乐会、管弦乐队、音乐剧等）。这些数据库大多由学生专为 Spider 创建，并不能代表真实世界数据库。

下文说明，为何需要针对复杂的科学数据库，对 NL-to-SQL 系统进行新的设计与训练。我们将讨论聚焦于天体物理学：这是一个数据密集、高度复杂，并且长期使用关系数据库的科学学科 [41]。这里描述的挑战不仅与天体物理有关，也与其他科学学科有关，例如同样纳入我们实验评测的癌症研究。

作为贯穿示例，我们使用名为 Sloan Digital Sky Survey（SDSS）¹ 的天体物理数据库。该数据库存储天空特定位置上的恒星与星系信息。该数据库复杂度的进一步细节在第 3 节说明。考虑三条有代表性的天体物理查询，作为本文的贯穿示例。

- Q1: Find all Starburst galaxies.（找出所有 Starburst 星系。）
- Q2: What is the object id, right ascension, declination and redshift from spectroscopically observed galaxies with redshift greater than 0.5 but less than 1?（在光谱观测的星系中，redshift（红移）大于 0.5 且小于 1 的那些星系的 object id、right ascension（赤经）、declination（赤纬）与 redshift 是什么？）
- Q3: Find the photometric objects with object ids and spectroscopic object id whose spectroscopic class is ’GALAXY’, with the difference of magnitude u and magnitude r less than 2.22 and the difference of magnitude u and magnitude r greater than 1.（找出 photometric objects（测光天体）的 object id 与 spectroscopic object id（光谱天体 id），其 spectroscopic class（光谱类别）为 ’GALAXY’，且 magnitude u 与 magnitude r 之差小于 2.22、并大于 1。）

对应的 SQL 查询如下：

Q1:（Spider hardness: Easy）

```sql
SELECT s.specobjid
FROM specobj AS s
WHERE s.subclass = 'STARBURST'
```

Q2:（Spider hardness: Medium）

```sql
SELECT s.bestobjid, s.ra, s.dec, s.z
FROM specobj AS s
WHERE s.class = 'GALAXY' AND s.z > 0.5 AND s.z < 1
```

Q3:（Spider hardness: Extra hard）

```sql
SELECT p.objid, s.specobjid
FROM photoobj AS p
JOIN specobj AS s ON s.bestobjid = p.objid
WHERE s.class = 'GALAXY'
AND p.u - p.r < 2.22 AND p.u - p.r > 1
```

如这些查询所示，面向复杂科学数据库的 NL-to-SQL 系统的主要挑战如下：

- **Unseen domains. 未见领域。** 要理解天体物理这样有挑战的领域，并写出有意义的查询——无论是自然语言还是 SQL——都需要广泛的领域知识。因此，在常识数据集（如 Spider）上预训练的神经机器翻译系统，通常会因主题差异巨大而在复杂领域失败。
- **Complex, often cryptic, database schemas. 复杂且常常晦涩的数据库模式。** 科学数据库常常存储大量数据，属性可达数百个。此外，属性名可能极短，例如 ra 或 z（在天体物理中分别指 right ascension 与 redshift），或存储数值测量。因此，需要额外的本体（ontologies）来描述这些属性的含义或科学解释——这些解释可以是包含数学方程与自然语言文本的复杂天体物理描述。最后，把自然语言问题中的词元映射到相关数据库属性，并非平凡的任务。
- **Sophisticated queries. 精细的查询。** 领域特定查询可能比 Spider 中的查询更为精细。例如，天体物理分析需要在属性之间使用函数与数学运算符，例如紫外（ultraviolet, u）与红外滤光片（infrared filters, r）之间的星等差，例如 u - r < 2.22。

这些观察表明，需要专门的基准来捕捉当前领域的特殊性与语义，以及 NL-to-SQL 系统需要理解的查询类型。这些要求，再加上这样的基准所必需的规模，使其无法手工构建。

既然庞大而复杂的模式即使对专家也难以理解与查询，自然出现的问题就是：如何构建这样的基准？答案是数据增强，而这又带来它自己的挑战：如何为新数据库构建有代表性的 SQL 查询？如何给出它们的自然语言描述？如何在极少、乃至没有任何人工参与的情况下完成这件事？

¹ https://www.sdss.org/
