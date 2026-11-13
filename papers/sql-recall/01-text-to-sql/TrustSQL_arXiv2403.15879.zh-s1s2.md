# TrustSQL: Benchmarking Text-to-SQL Reliability with Penalty-Based Scoring

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`TrustSQL_arXiv2403.15879.pdf`。

## Abstract 摘要

Text-to-SQL 让用户用自然语言与数据库交互，从而简化信息的检索与综合。尽管大语言模型（large language models, LLMs）在把自然语言问题翻译成 SQL 查询方面取得了显著成功，广泛部署仍然受限，主要有两个挑战。第一，有效使用 text-to-SQL 模型取决于用户对模型能力的理解，也就是模型能够正确回答的问题范围。第二，缺少弃答机制（abstention mechanisms）时，错误的 SQL 生成可能不被察觉，从而削弱对模型输出的信任。要扩大部署，就必须在模型设计中应对这些挑战，并改进模型评测，以建立对模型输出的信任。为此，我们提出 TrustSQL，一个新的综合基准，用于评测 text-to-SQL 可靠性（text-to-SQL reliability）。可靠性定义为：模型正确处理任何类型输入问题的能力，即对可行问题生成正确 SQL，并对不可行问题放弃生成（例如由于模式不兼容，或所需功能超出 SQL）。我们用一种新的基于惩罚的评分指标评测现有方法，并采用两种建模途径：（1）流水线方法（pipeline-based methods），把 SQL 生成器与不可行问题检测器、SQL 错误检测器组合起来以实现弃答；（2）统一方法（unified methods），用单一模型完成整个任务。实验结果表明，要在严厉惩罚下取得高分需要付出很大努力，并为开发更安全部署的 text-to-SQL 模型提供了新的视角。TrustSQL 见 https://github.com/glee4810/TrustSQL。

## 1 Introduction 引言

Text-to-SQL 是从自然语言（natural language, NL）问题生成 SQL 查询的任务，这一挑战已经持续了数十年 [17]。由于数据库在医学、金融、零售和电信等诸多领域无处不在，该任务在机器学习与自然语言处理（natural language processing, NLP）之内和之外都很关键。通过自然语言访问这些数据库中存储的结构化数据，可以释放大数据的真正潜力，使领域专家发现新的定量洞见 [21]。

要有效使用这些模型，用户需要熟悉它们的能力。这包括每个模型能够准确回答的问题类型、它能访问的信息，以及哪些操作可以通过 SQL 完成、哪些不能。然而，许多原本能从模型中大大受益的潜在用户并不熟悉这些能力，使用起来可能很困难，因为他们的问题经常落在模型能力范围之外（超出图 1(b) 中的正确 SQL）。在真实部署场景中，挑战更加突出：用户问题不仅包括模型能够处理的可行问题，也包括不可行问题，例如需要数据库内容之外的知识或超出 SQL 功能的请求（如图 1(a) 所示）。此外，当前 text-to-SQL 建模缺少弃答机制，会使可行问题与不可行问题上的错误模型输出都不被察觉，其代价可能超过使用模型的收益。如果模型在设计上能够有选择地回答正确的 SQL 查询，并对其余情况弃答，就会显著增强用户信心，从而提高对模型的信任并鼓励使用 [25, 16]。

图 1：（a）部署场景（Deployment Scenarios）同时包含与 text-to-SQL 任务相关的可行与不可行用户问题（例如超出数据库模式或 SQL 功能的请求）。（b）标准 Text-to-SQL 旨在最大化正确 SQL 查询的生成。这种关注可能导致错误的模型输出不被察觉，从而增加部署风险。绿色与红色区域分别表示正确与错误的 SQL 生成。要有效使用 text-to-SQL 模型，用户必须熟悉其能力，而这些能力因模型而异——即每个模型能够正确回答的问题类型——这对潜在用户构成了很高的门槛。（c）可靠 Text-to-SQL 移除这一门槛，并通过弃答（红色箭头）尽量减少错误输出 (III) 和 (IV)，同时在可行区域内最大化正确输出 (I)（绿色箭头），以增强对模型的信任。随着红色区域 (III) 和 (IV) 缩小，随后黄色区域 (II) 也会缩小，用户就会开始信任模型的输出。各区域的进一步说明见脚注 1。图中区域分界的版面细节【抽取不清】。

脚注 1：图 1(c) 中的五个关键区域是：(I) 对可行问题生成正确 SQL（对 text-to-SQL 可靠性是可取的）；(II) 对可行问题弃答（既非严格可取也非严格不可取，因而是中性的）；(III) 对可行问题生成错误 SQL（不可取）；(IV) 对不可行问题生成错误 SQL（不可取）；(V) 对不可行问题正确弃答（可取）。这五种不同情形都被纳入第 3.2 节介绍的基于惩罚的评分指标，实例见 Supplementary E。

为应对上述挑战，我们提出 TrustSQL，一个用于评估 text-to-SQL 可靠性的新基准。我们将 text-to-SQL 可靠性定义为：模型通过准确的 SQL 生成与弃答来正确处理任何输入问题的能力，从而缩小红色和黄色区域，并用绿色覆盖整个区域，如图 1(c) 所示。标准 text-to-SQL 任务定义在可行区域之内（图 1(b)），而真实用户问题同时跨越可行与不可行任务区域，包括超出数据库内容和 SQL 功能的请求（图 1(a)）。我们用三个领域专用数据集——ATIS [3]、Advising [4] 和 EHRSQL [9]——以及一个跨领域数据集 Spider [27]，构建了这一新的综合设定。在构建 TrustSQL 时，我们通过仔细的数据划分，并纳入各类不可行问题（类似于红队测试，red teaming），反映了那些削弱 text-to-SQL 可靠性的常见错误情形。随后，我们用一种专门用于度量 text-to-SQL 可靠性的新型基于惩罚的评分指标评测现有方法（细节见 Section 3.2）。实验结果表明，大多数先进方法在无惩罚设定下看似表现良好，但在严厉惩罚设定下取得高分仍然非常困难。从高惩罚的视角看，准确知道何时弃答，比贸然尝试生成 SQL 查询更为重要，这突出表明：要赢得对模型输出的信任，仍需付出大量努力。

## 2 Dataset Construction 数据集构建

本节首先识别部署过程中削弱 text-to-SQL 可靠性、并使答案落在图 1(c) 红色区域中的常见错误情形，然后介绍把每种情形纳入数据集构建过程的策略。text-to-SQL 部署中的常见错误情形如下：

- **SQL 生成的复杂性（Complexity of SQL generation）。** 用户问题，尤其是领域专家提出的问题，往往过于复杂，模型难以准确回答。这种复杂性来自查询本身的难度 [27, 11, 5, 9]（如 Supplementary B 的 Table 7），或来自模型遇到数据库特有的、不熟悉的短语和实体 [19, 8]。如果模型生成 SQL 时不能对此类情形弃答，就有损害其输出可信度的风险。我们在可行数据的构建中纳入查询难度 [P1] 和熟悉度 [P2] 这两个维度。
- **用户查询中的歧义（Ambiguity in user queries）。** 用户问题常常有歧义，尤其是在指称列或值（即数据库记录）时缺少精确说明。弄清用户的真实意图需要多轮交互来澄清，这超出了本工作的范围。
- **模式不兼容（Schema incompatibility）。** 不熟悉确切数据库模式（schema）的用户，可能无意中提出无法处理的问题，因为他们寻求的信息不存在于现有列中。以往工作通过删除和扰动现有列来构造这类情形 [29, 22]。我们则在这一情形中纳入三种不同类型 [P3]，以便更细粒度地观察模型行为。
- **SQL 功能的范围（Scope of SQL functionalities）。** 用户并不总是熟悉 SQL 功能的范围，因而可能提出需要复杂数值运算、数据分析或预约安排等超出标准 SQL 执行的请求。我们在不可行数据的构建中纳入这类问题 [P4]。
- **对外部知识的需求（Need for external knowledge）。** 用户可能提出涉及事实性世界知识、且远远超出数据库内容的问题，要么完全超出（例如 “What airport is in Wilder, KY?”），要么部分超出（例如 “Find me patients born after WWII”）。构造不可行问题时，我们考虑前一类情形 [P5]，而排除后一类。

### 2.1 Feasible Data Construction 可行数据构建

**数据集选择（Dataset selection）。** 为建立覆盖综合设定的基准数据，我们选择了三个复杂的领域专用 text-to-SQL 数据集，即 ATIS（航班信息）[3]、Advising（教育）[4] 和 EHRSQL（医疗）[9]。此外，我们还纳入一个跨领域数据集 Spider。领域专用与跨领域 text-to-SQL 设定的区别，以及各数据集的复杂度，详见 Supplementary B。

**数据预处理（Data preprocessing）。** 我们的初步数据分析表明，ATIS 和 Advising 需要大量预处理，原因包括大量查询重复、不一致，以及质量较差的自然语言问题（每个问题在 Supplementary G 中讨论）。我们实施了若干策略来修正这些问题，包括用 GPT-4 为所有输入 NL 问题创建新的问题复述，再由作者人工审阅。更多细节见 Supplementary G。预处理之后，四个数据集的数据库及其对应的问题–SQL 对被纳入可行任务区域中的问题（图 1(a) 中的浅蓝色区域）。为反映查询难度 [P1]，我们在所有数据集上采用遵循 [14] 的 SQL 难度（SQL hardness）标准。各难度级别的详细统计见 Supplementary B 的 Table 7。查询熟悉度 [P2] 稍后在数据划分过程中引入（§2.3）。

### 2.2 Infeasible Data Construction 不可行数据构建

部署在真实场景中的 text-to-SQL 模型经常遇到落入不可行任务区域（图 1(a) 中的灰色区域）的用户请求，因为这些请求超出了数据库内容或 SQL 功能，因而没有对应的 SQL 查询。为了在更真实的环境中评测模型，我们手工标注 NL 问题，并纳入以下三种常见的不可行错误情形：

**模式不兼容 [P3]。** 我们没有随机丢弃数据库中的现有列 [29, 22]，而是引入假设列（hypothetical columns）的概念，作为不可行问题的目标列。这些问题被提出时，仿佛存在对应的 SQL 查询，但实际上并不存在，因为数据库中没有这样的列。我们将它们分为三类：column-surface、column-related 和 column-unrelated，分别表示基于表层形式的列相似、语义上的列相似，以及不相似的攻击。

- **column-surface：** 问题所指的假设列与其他表中的现有列相似，或具有相似的表层形式（例如在 dog_kennels 数据库中，Professionals 表里一个假设的 age 列，类似于 Dogs 表中的 age 列）。
- **column-related：** 问题所指的假设列可以自然地融入现有数据库模式（例如 song 表中一个名为 duration 的假设列）。这类问题可以看作 ADVETA [13] 中 ADD 扰动的人工版本。
- **column-unrelated：** 问题所指的假设列是从其他数据库中随机抽取的，大多不自然（例如 battles 数据库中一个假设的 product_category 列）。

**超出 SQL 功能 [P4]。** 为覆盖超出 SQL 执行的多样用户请求（non-sql），我们整理了一份 NLP 与数据分析任务清单，并使用 GPT-4 识别：在给定数据库内容的情况下，如果可以使用任何工具，作为 AI 助手可以做什么。基于一份包含 27 项任务的清单（例如异常检测 anomaly detection、可视化 visualization 和网页搜索 web search），我们手工标注了与每个数据库中现有列相关或指称这些列的 NL 问题（因而是上下文驱动的标注），以模拟期望模型完成并非仅靠 SQL 就能处理的任务的用户。

**对外部知识的需求 [P5]。** 为构造涉及外部知识的 NL 问题（ext-know），我们提示 GPT-4 生成需要领域专长、定性洞见或因果理解的问题。我们持续这一过程，直到得到与其他类型不可行问题规模相当的均衡样本集。

在手工标注不可行 NL 问题之后，作者使用 GPT-4 迭代审阅，以确保它们确实不可行。标注问题的样例见表 1。

表 1：Spider 中 orchestra 数据库的各类不可行问题样例。该库含 4 张表、23 列。为简洁起见，此处不展示领域专用数据库的样例。“Note”表示现有表中的假设列（即我们用于 text-to-SQL 的数据库里并不存在的列），或问题标注所用的任务名称。

| Type | Question | Note |
| --- | --- | --- |
| column-surface | 所有演出的平均上座容量是多少？（What is the average attendance capacity for all the shows?） | show.attendance_capacity |
| column-related | 哪个乐团的成员最多？（Which orchestra has the most members?） | orchestra.number_of_member |
| column-unrelated | Charles Dutoit 拥有什么飞机？（What aircraft does Charles Dutoit own?） | conductor.aircraft |
| non-sql | 找出影响上座情况的三个最显著特征。（Identify the top three significant features that influence attendance.） | feature importance |
| ext-know | 多样性给乐团带来哪些优势？（What advantages does diversity bring to an orchestra?） | - |

### 2.3 Data Splitting 数据划分

数据划分的核心原则是：为可行数据制造不同程度的查询熟悉度 [P2]，并在模型评测中引入不可行数据的意外性。表 2 汇总了 TrustSQL 的总体数据统计。

表 2：TrustSQL 的数据集统计。TrustSQL 的测试集中，不可回答问题与可回答问题数量相等。对于 Q，由 “/” 分隔的三个数字分别表示训练集、验证集和测试集的规模。表头一列在抽取中记为 EHRQSL，与正文中的 EHRSQL 对应，此处按 EHRSQL 列出。

|  | ATIS | Advising | EHRSQL | Spider |
| --- | --- | --- | --- | --- |
| All Questions (\(Q \cup Q_c\)) | 2555 | 2769 | 7473 | 8561 |
| Feasible Question (\(Q\)) | 1114 / 489 / 476 | 1170 / 533 / 533 | 4674 / 931 / 934 | 7000 / 507 / 527 |
| Infeasible Question (\(Q_c\)) | 476 | 533 | 934 | 527 |
| non-sql | 99 | 110 | 191 | 100 |
| surface | 93 | 102 | 185 | 100 |
| unrelated | 94 | 110 | 187 | 100 |
| related | 98 | 107 | 189 | 100 |
| ext-know | 92 | 104 | 182 | 127 |

**可行数据（Feasible data）。** 我们定义 “seen SQL” 与 “unseen SQL”，以引入查询熟悉度 [P2]（只适用于可行数据）。若样本对应的 SQL 结构出现在训练集中，但在验证集和测试集中配有不同的复述 NL 问题，则视为 “seen SQL”。“Unseen SQL” 样本的 SQL 结构不出现在训练集中。我们利用验证集和测试集中这些不同的查询熟悉度 [P2] 来分析模型性能。领域专用数据集的划分过程如下：1）按 NL 问题以 6:2:2 的比例把可行数据划分为训练集、验证集和测试集（各划分中的 SQL 结构相同，但 NL 问题不同）；2）从验证集和测试集中移除 20% 互不重叠的 SQL 结构；3）从训练集中移除这些 SQL 结构的共计 40%，从而使所有划分中有 60% 的 “seen SQL”，而验证集和测试集包含 80% 的 SQL 结构（60% 为 “seen SQL”，20% 为 “unseen SQL”）。对 Spider，我们把开发集划分对半，构成新的验证集和测试集（各 10 个数据库），全部为 “unseen SQL”，并且与训练集没有重叠。

脚注 2：SQL 结构指 SQL 成分与特定表、列的一种特定组合，不包括实际数据值。

**不可行数据（Infeasible data）。** 我们把五种类型（column-surface、column-related、column-unrelated、non-sql 和 ext-know）的已标注不可行 NL 问题全部加入测试集，并保持比例均衡，以反映部署中对它们的意外遭遇。
