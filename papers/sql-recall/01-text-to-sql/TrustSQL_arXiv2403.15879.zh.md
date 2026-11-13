原文件名：TrustSQL_arXiv2403.15879.pdf

原标题：TrustSQL: Benchmarking Text-to-SQL Reliability with Penalty-Based Scoring

中文标题：TrustSQL：用基于惩罚的评分评测 Text-to-SQL 可靠性

作者：Gyubok Lee, Woosog Chay, Seonhee Cho, Edward Choi（KAIST AI；{gyubok.lee, benchay, seonhee.cho, edwardchoi}@kaist.ac.kr）

会议或 arXiv：arXiv:2403.15879v6 [cs.AI] 2 Jul 2024（Preprint. Under review.）

<!-- 原 PDF 第 1 页 -->

# TrustSQL：用基于惩罚的评分评测 Text-to-SQL 可靠性

Gyubok Lee  
Woosog Chay  
Seonhee Cho  
Edward Choi  

KAIST AI  
{gyubok.lee, benchay, seonhee.cho, edwardchoi}@kaist.ac.kr

## 摘要

Text-to-SQL 让用户用自然语言与数据库交互，从而简化信息的检索与综合。尽管大语言模型（LLM）在把自然语言问题翻译成 SQL 查询方面取得了显著成功，广泛部署仍然受限于两个主要挑战。第一，有效使用 text-to-SQL 模型，取决于用户是否了解模型的能力，也就是模型能够正确回答的问题范围。第二，缺少弃答机制时，错误的 SQL 生成可能不被察觉，从而削弱对模型输出的信任。要想更广泛地部署，就必须在模型设计中应对这些挑战，并改进模型评测，以建立对模型输出的信任。为此，我们提出 TrustSQL，一个新的综合基准，用来评测 text-to-SQL 可靠性。可靠性定义为：模型能够正确处理任意类型的输入问题，对可行问题生成正确的 SQL 查询，并对不可行问题弃答（例如由于模式不兼容，或所需功能超出 SQL）。我们用一种新的基于惩罚的评分指标评测现有方法，并采用两种建模途径：（1）流水线方法，把 SQL 生成器与不可行问题检测器、SQL 错误检测器组合起来以实现弃答；（2）统一方法，用单一模型完成整个任务。实验结果表明，在严厉惩罚下取得高分需要付出大量努力，并为开发可供更安全部署的 text-to-SQL 模型提供了新的视角。TrustSQL 发布于 https://github.com/glee4810/TrustSQL。

## 1 引言

Text-to-SQL 是从自然语言（NL）问题生成 SQL 查询的任务，这一挑战已经持续了数十年 [17]。由于数据库在医学、金融、零售和电信等许多领域无处不在，这项任务无论在机器学习与自然语言处理（NLP）之内还是之外都十分关键。通过自然语言访问这些数据库中存储的结构化数据，可以释放大数据的真正潜力，使领域专家发现新的定量洞见 [21]。

要有效使用这些模型，用户需要熟悉它们的能力。这包括每个具体模型能够准确回答的问题类型、它能访问哪些信息，以及哪些操作可以通过 SQL 完成、哪些不能。然而，许多本可以大大受益于模型的潜在用户并不熟悉这些能力，使用起来可能很困难，因为他们的问题经常落在模型能力范围之外（超出图 1(b) 中的正确 SQL）。在真实部署中，这一挑战更为尖锐：用户问题不仅包括模型可以处理的可行问题，也包括不可行问题，例如需要数据库内容之外的知识、或超出 SQL 功能的请求（如图 1(a) 所示）。此外，

预印本。审稿中。

arXiv:2403.15879v6 [cs.AI] 2 Jul 2024

<!-- 原 PDF 第 2 页 -->

图 1 中的文字标签包括：部署场景（Deployment Scenarios）、不可行区域（Infeasible Region）、可行区域（Feasible Region）、正确 SQL（Correct SQL）、模型输出（Model Output）、标准 Text-to-SQL（Standard Text-to-SQL）、弃答（Abstention）、可靠 Text-to-SQL（Reliable Text-to-SQL），以及区域 I、II、III、IV、V。默认 `find_tables` 在本页只抽出一行残片「Model | Outpu」，不是完整表格。

**图 1：**（a）部署场景同时包含与 text-to-SQL 任务相关的可行与不可行用户问题（例如超出数据库模式或 SQL 功能的请求）。（b）标准 Text-to-SQL 旨在最大化正确 SQL 查询的生成。这种侧重可能使错误的模型输出不被察觉，从而增加部署风险。绿色区域和红色区域分别表示正确与不正确的 SQL 生成。要有效使用 text-to-SQL 模型，用户必须熟悉其能力，而这些能力因模型而异，即每个模型能够正确回答的问题类型，这给潜在用户设置了很高的门槛。（c）可靠 Text-to-SQL 消除这一门槛，目标是通过弃答（红色箭头）尽量减少不正确输出（III）和（IV），同时在可行区域内最大化正确输出（I）（绿色箭头），从而增强对模型的信任。随着红色区域（III）和（IV）缩小，随后黄色区域（II）也会缩小，用户就会开始信任模型的输出。各区域的进一步说明见脚注 1。

当前 text-to-SQL 建模缺少弃答机制，可能使可行问题与不可行问题上的错误模型输出都不被察觉，其代价甚至可能超过使用模型所带来的收益。如果模型在设计上能够有选择地回答正确的 SQL 查询，并对其余情况弃答，就会显著提升用户信心，从而增强对模型的信任并鼓励使用 [25, 16]。

为应对上述挑战，我们提出 TrustSQL，一个用于评估 text-to-SQL 可靠性的新基准。我们将 text-to-SQL 可靠性定义为：模型通过准确的 SQL 生成与弃答，正确处理任意输入问题的能力，从而缩小红色区域和黄色区域，使整个区域被绿色覆盖，如图 1(c) 所示。与定义在可行区域之内的标准 text-to-SQL 任务（图 1(b)）不同，真实用户问题横跨可行与不可行任务区域，包括超出数据库内容和 SQL 功能的请求（图 1(a)）。我们用三个领域数据集——ATIS [3]、Advising [4] 和 EHRSQL [9]——以及一个跨领域数据集——Spider [27]——构造了这一新的综合设定。构造 TrustSQL 时，我们通过仔细的数据划分，并纳入多种不可行问题，反映了那些会损害 text-to-SQL 可靠性的常见错误情形，做法类似于红队测试。随后，我们用一种专门用来衡量 text-to-SQL 可靠性的、基于惩罚的新评分指标评测现有方法（细节见第 3.2 节）。实验结果表明，在无惩罚设定下，多数先进方法看起来表现不错，但在严厉惩罚设定下取得高分仍然非常困难。从高惩罚的角度看，精确知道何时弃答，比贸然尝试生成 SQL 查询更为重要，这突出表明：要让模型输出赢得信任，还需要付出大量努力。

## 2 数据集构建

在本节中，我们首先识别部署期间会损害 text-to-SQL 可靠性、使答案落在图 1(c) 红色区域中的常见错误情形。然后，我们介绍把每种情形纳入数据集构建过程的策略。

脚注 1：图 1(c) 中的五个关键区域是：（I）对可行问题生成正确 SQL（对 text-to-SQL 可靠性而言是可取的）；（II）对可行问题弃答（既非严格可取也非严格不可取，因此是中性的）；（III）对可行问题生成不正确的 SQL（不可取）；（IV）对不可行问题生成不正确的 SQL（不可取）；（V）对不可行问题正确弃答（可取）。这五种互不相同的情形全部纳入第 3.2 节介绍的基于惩罚的评分指标，其实例见补充材料 E。

<!-- 原 PDF 第 3 页 -->

**表 1：** Spider 中 orchestra 数据库上各类不可行问题的样例。该库含 4 张表、23 列。领域数据库的样例为求简略未在此展示。「注释」表示现有表中的假设列（即我们用于 text-to-SQL 的数据库里并不存在的列），或用于问题标注的任务名。

| 类型 | 问题 | 注释 |
| --- | --- | --- |
| column-surface | What is the average attendance capacity for all the shows? | show.attendance_capacity |
| column-related | Which orchestra has the most members? | orchestra.number_of_member |
| column-unrelated | What aircraft does Charles Dutoit own? | conductor.aircraft |
| non-sql | Identify the top three significant features that influence attendance. | feature importance |
| ext-know | What advantages does diversity bring to an orchestra? | - |

中文对照：column-surface「所有演出的平均容纳人数是多少？」；column-related「哪个乐团成员最多？」；column-unrelated「Charles Dutoit 拥有什么飞行器？」；non-sql「找出影响上座率的三个最重要特征。」；ext-know「多样性给乐团带来什么好处？」

以下是 text-to-SQL 部署中的常见错误情形：

- **SQL 生成的复杂度：** 用户问题，尤其是领域专家提出的问题，对模型来说往往过于复杂，难以准确回答。这种复杂度来自查询本身的固有难度 [27, 11, 5, 9]，如补充材料 B 的表 7，或来自模型遇到数据库特有的、不熟悉的说法和实体 [19, 8]。如果模型生成 SQL 时不能对这类情形弃答，就有损害其输出可信度的风险。我们在可行数据构建中纳入查询难度 [P1] 和熟悉度 [P2] 这两个维度。
- **用户查询中的歧义：** 用户问题常常含糊，尤其是在指称列或取值（即数据库记录）时没有精确说明。澄清用户的真实意图需要多轮交互，这超出本文范围。
- **模式不兼容：** 不熟悉确切数据库模式的用户，可能无意中提出无法处理的问题，因为他们想要的信息不存在于现有列中。先前工作通过删除和扰动现有列来构造这类情形 [29, 22]。我们则在该情形中纳入三种不同类型 [P3]，以便更细粒度地观察模型行为。
- **SQL 功能的范围：** 用户并不总是熟悉 SQL 功能的范围，因而会提出需要复杂数值运算、数据分析或预约安排的请求，这些超出标准 SQL 执行。我们在不可行数据构建中纳入这类问题 [P4]。
- **对外部知识的需求：** 用户可能提出涉及远超数据库内容的事实性世界知识的问题，要么完全超出（例如「Wilder, KY 有什么机场？」），要么部分超出（例如「找出二战后出生的患者」）。构造不可行问题时，我们考虑前一种情形 [P5]，而排除后一种。

### 2.1 可行数据构建

**数据集选择。** 为建立覆盖综合设定的基准数据，我们选择了三个复杂的领域 text-to-SQL 数据集，即 ATIS（航班信息）[3]、Advising（教育）[4] 和 EHRSQL（医疗）[9]。此外，我们还纳入一个跨领域数据集 Spider。领域设定与跨领域 text-to-SQL 设定的区别，以及各数据集的复杂度，详见补充材料 B。

**数据预处理。** 初步数据分析表明，ATIS 和 Advising 需要大量预处理，问题包括大量查询重复、不一致，以及自然语言（NL）问题质量差（各项问题在补充材料 G 中讨论）。我们采取若干策略纠正这些问题，包括用 GPT-4 为全部输入 NL 问题创建新的释义，再由作者人工复核。更多细节请参阅补充材料 G。预处理之后，四个数据集的数据库及其对应的问题–SQL 对，被纳入可行任务区域中的问题（图 1(a) 中的浅蓝色区域）。为反映查询难度 [P1]，我们在所有数据集上采用遵循 [14] 的 SQL hardness 标准。各难度等级的详细统计见补充材料 B 的表 7。查询熟悉度 [P2] 稍后在数据划分过程中引入（第 2.3 节）。

<!-- 原 PDF 第 4 页 -->

**表 2：** TrustSQL 的数据集统计。TrustSQL 的测试集中，不可回答问题与可回答问题数量相等。对于 Q，用「/」分开的三个数字分别表示训练、验证和测试集的规模。表头抽取中该列写作 EHRQSL，正文其余处均为 EHRSQL，下表按 EHRSQL 列出。默认 `find_tables` 未抽出本表；下列数字来自按页 `get_text('text')`，且各行可与正文合计互相核对。

| | ATIS | Advising | EHRSQL | Spider |
| --- | --- | --- | --- | --- |
| 全部问题（Q ∪ Qc） | 2555 | 2769 | 7473 | 8561 |
| 可行问题（Q） | 1114 / 489 / 476 | 1170 / 533 / 533 | 4674 / 931 / 934 | 7000 / 507 / 527 |
| 不可行问题（Qc） | 476 | 533 | 934 | 527 |
| ⌞non-sql | 99 | 110 | 191 | 100 |
| ⌞surface | 93 | 102 | 185 | 100 |
| ⌞unrelated | 94 | 110 | 187 | 100 |
| ⌞related | 98 | 107 | 189 | 100 |
| ⌞ext-know | 92 | 104 | 182 | 127 |

### 2.2 不可行数据构建

部署在真实场景中的 text-to-SQL 模型，经常遇到落入不可行任务区域（图 1(a) 中的灰色区域）的用户请求，原因是超出数据库内容或 SQL 功能，因此没有对应的 SQL 查询。为了在更现实的环境中评测模型，我们手工标注 NL 问题，纳入如下三种常见的不可行错误情形：

**模式不兼容 [P3]：** 我们不随机删除数据库中的现有列 [29, 22]，而是引入假设列这一概念，作为不可行问题的目标列。这些问题被问得好像存在对应的 SQL 查询，但实际上并不存在，因为数据库中没有这样的列。我们将它们分为三类：column-surface、column-related 和 column-unrelated，分别表示基于表面形式以及语义上的列相似与不相似所做的攻击。

- **column-surface：** 问题指称的假设列与其他表中的现有列相似，或表面形式相近（例如在 dog_kennels 数据库中，Professionals 表里一个假设的 age 列，与 Dogs 表中的 age 列相似）。
- **column-related：** 问题指称的假设列可以自然地融入现有数据库模式（例如 song 表中一个名为 duration 的假设列）。这类问题可以看作 ADVETA [13] 中 ADD 扰动的手工版本。
- **column-unrelated：** 问题指称的假设列是从其他数据库随机抽取的，多数很不自然（例如 battles 数据库中一个假设的 product_category 列）。

**超出 SQL 功能 [P4]：** 为捕捉超出 SQL 执行的多样用户请求（non-sql），我们整理了一份 NLP 与数据分析任务清单，并用 GPT-4 识别：若给定数据库内容且可以使用任意工具，作为 AI 助手还能做什么。基于一份包含 27 项任务的清单（例如异常检测、可视化和网页搜索），我们手工标注与每个数据库中现有列相关、或指称这些列的 NL 问题（因此是由上下文驱动的标注），以模拟用户期望模型完成不能仅靠 SQL 处理的任务。

**对外部知识的需求 [P5]：** 为构造涉及外部知识的 NL 问题（ext-know），我们提示 GPT-4 生成需要领域专长、定性洞见或因果理解的问题。我们持续这一过程，直到样本数量与其他类型的不可行问题大致均衡。

在手工标注不可行 NL 问题之后，作者使用 GPT-4 反复复查，以确保它们确实不可行。标注问题的样例见表 1。

### 2.3 数据划分

数据划分的核心原则是：为可行数据制造不同的查询熟悉度 [P2]，并为模型评测引入不可行数据的意外性。表 2 汇总了 TrustSQL 的总体数据统计。

**可行数据。** 我们定义「seen SQL」和「unseen SQL」，以引入查询熟悉度 [P2]（只适用于可行数据内部）。当样本对应的 SQL

<!-- 原 PDF 第 5 页 -->

结构²出现在训练集中，但验证集和测试集中的 NL 问题是不同释义时，这些样本视为「seen SQL」。「Unseen SQL」样本的 SQL 结构未出现在训练集中。我们用纳入验证集和测试集的这些不同查询熟悉度 [P2] 来分析模型表现。领域数据集的划分过程如下：1）按 NL 问题把可行数据以 6:2:2 分成训练集、验证集和测试集（各划分的 SQL 结构相同，但 NL 问题不同）；2）从验证集和测试集中去掉 20% 互不重叠的 SQL 结构；3）再把这合计 40% 的 SQL 结构从训练集中去掉。于是所有划分中有 60% 为「seen SQL」，而验证集和测试集包含 80% 的 SQL 结构（其中 60% 为「seen SQL」，20% 为「unseen SQL」）。对于 Spider，我们把开发集对半切开，作为新的验证集和测试集（各 10 个数据库），全部是「unseen SQL」，与训练集没有重叠。

**不可行数据。** 我们把五类已标注的不可行 NL 问题（column-surface、column-related、column-unrelated、non-sql 和 ext-know）全部以大致均衡的比例加入测试集，以反映部署中意外遇到它们的情形。

## 3 评测 Text-to-SQL 可靠性

### 3.1 任务

可靠 text-to-SQL 旨在开发这样的模型：只生成正确的 SQL 查询，并在任何其他情形下弃答，包括可行问题（Q）和不可行问题（Qc），从而增强 text-to-SQL 可靠性。在这一原则下优化之后，用户无需广泛了解模型能力，就能有效使用这些模型。他们也可以较少担心模型产生错误输出，因为模型会对其能力之外的问题弃答。可靠性的提高将促使 text-to-SQL 模型被更广泛地采用，使领域专家能够借助自然语言界面访问并分析数据库中存储的大量数据。

### 3.2 评价指标

评测可靠 text-to-SQL 的表现时，我们把模型输出分为三类：可取（绿色）、不可取（红色）和中性（黄色），如图 1(c) 所示。这些类别反映模型输出带来的不同后果。可取输出提供效用，包括正确的 SQL 生成（I）和弃答（V）。然而，不可取输出的后果严重程度会随部署情境而变化。在不太关键的设定中（例如实验场景），我们可以对不可取输出较为宽容，只关注模型的效用。相反，在高风险环境中（例如医院），不可取输出可能造成严重后果，其代价可能超过模型提供的任何效用。因此，我们把负面影响相对于正面影响的相对幅度定义为风险。这一风险包括不正确的 SQL 生成（III）和弃答（IV），并由惩罚因子 c 加权，c 即负面影响与正面影响之比。中性（黄色）情形（II）既非严格可取，也非严格不可取，因此我们既不把它算作效用，也不把它算作风险。各类实例见附录 E。

总之，text-to-SQL 可靠性可以量化为效用与风险之差。为把这一概念在数学上形式化，我们将这一针对 text-to-SQL 的基于惩罚的评分——可靠性分数（RS）——定义如下。分段花括号在抽取中为乱码符号（、、 及若干 ）。公式抽取不完整，见原 PDF 第 5 页。按可读的取值与条件整理为：

$$
\phi_c(x)=
\begin{cases}
1 & \text{if } x \in Q;\ g(x)=1;\ \mathrm{Acc}(x)=1, \\
0 & \text{if } x \in Q;\ g(x)=0, \\
-c & \text{if } x \in Q;\ g(x)=1;\ \mathrm{Acc}(x)=0, \\
-c & \text{if } x \in Q_c;\ g(x)=1, \\
1 & \text{if } x \in Q_c;\ g(x)=0,
\end{cases}
\tag{1}
$$

其中 Acc(x) 是 text-to-SQL 中的执行准确率，g(x)=1 与 g(x)=0 分别表示模型决定回答或弃答。

脚注 2：SQL 结构指 SQL 成分与特定表、列的特定组合，不含实际数据取值。

<!-- 原 PDF 第 6 页 -->

**表 3：** 在同时包含可行问题与不可行问题的 TrustSQL 上比较模型，评测 ϕ0、ϕ10 和 ϕN。AT、AD、EH、SP 分别指 ATIS、Advising、EHRSQL 和 Spider。ABSTAIN-ALL 对全部输入问题盲目弃答，其分数反映不可行问题所占比例。为便于阅读，数值均为百分数。默认 `find_tables` 只抽出残行；下表按 `get_text('text')` 中每个方法名之后连续的 12 个数填写，顺序为 ϕ0 的 AT、AD、EH、SP，然后是 ϕ10 的四列，然后是 ϕN 的四列。`find_tables` 抽出的 CLSM → T5 与 CLSP → SQLPROMPT、CLSP → DIN-SQL 残行与这一顺序一致。

| 方法 | ϕ0 AT | ϕ0 AD | ϕ0 EH | ϕ0 SP | ϕ10 AT | ϕ10 AD | ϕ10 EH | ϕ10 SP | ϕN AT | ϕN AD | ϕN EH | ϕN SP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ABSTAIN-ALL | 50.0 | 50.0 | 50.0 | 50.0 | 50.0 | 50.0 | 50.0 | 50.0 | 50.0 | 50.0 | 50.0 | 50.0 |
| 开源 / 流水线 CLSM → T5 | 55.7 | 48.1 | 62.7 | 61.1 | -160.7 | -154.5 | -60.4 | -304.2 | -20.5K | -21.6K | -22.9K | -38.4K |
| 开源 / 流水线 T5 → ERRORM | 73.0 | 73.8 | 75.5 | 60.3 | -59.3 | -133.5 | -115.6 | -121.8 | -12.5K | -22.0K | -35.6K | -19.1K |
| 开源 / 流水线 CLSM → T5 → ERRORM | 64.3 | 58.9 | 66.5 | 64.3 | 13.9 | -21.8 | 14.6 | -66.6 | -4.7K | -8.5K | -9.6K | -13.7K |
| 开源 / 统一 T5[MAXENT] | 63.8 | 74.6 | 85.3 | 58.3 | 6.0 | 28.6 | 36.1 | -71.7 | -5.4K | -4.8K | -9.1K | -13.6K |
| 开源 / 统一 T5[MAXPROB] | 61.6 | 74.4 | 85.3 | 56.7 | 15.3 | 18.1 | 36.6 | -18.2 | -4.3K | -5.9K | -9.0K | -7.8K |
| 开源 / 统一 T5[FEATMD] | 67.5 | 57.1 | 67.6 | 50.1 | -9.1 | -315.3 | 14.1 | 50.1 | -7.2K | -39.6K | -9.9K | 50.1 |
| 开源 / 统一 T5[FEATRMD] | 72.8 | 55.8 | 76.4 | 49.9 | -48.0 | -352.3 | -153.2 | -296.4 | -11.4K | -43.4K | -42.8K | -36.5K |
| API / 流水线 CLSP → SQLPROMPT | 88.9 | 88.7 | 85.3 | 67.1 | -2.5 | -3.2 | -48.0 | -126.5 | -8.6K | -9.7K | -24.8K | -20.3K |
| API / 流水线 CLSP → DIN-SQL | 61.4 | 75.7 | 61.5 | 75.0 | -304.1 | -146.6 | -310.6 | -39.8 | -34.7K | -23.6K | -69.4K | -12.0K |
| API / 流水线 CLSP → MAC-SQL | 73.2 | 71.0 | 66.1 | 74.4 | -169.4 | -198.2 | -260.0 | -46.1 | -23.0K | -28.6K | -60.8K | -12.6K |
| API / 流水线 SQLPROMPT → ERRORP | 52.4 | 55.8 | 54.3 | 72.1 | 24.1 | 5.2 | 9.4 | -107.2 | -2.6K | -5.3K | -8.3K | -18.8K |
| API / 流水线 CLSP → SQLPROMPT → ERRORP | 54.5 | 58.9 | 57.4 | 67.6 | 51.4 | 45.8 | 46.7 | -41.5 | -245.5 | -1.3K | -1.9K | -11.4K |
| API / 统一 SQLPROMPT[DEMO] | 73.4 | 70.4 | 68.6 | 66.8 | -190.2 | -226.1 | -241.3 | -265.3 | -25.0K | -31.5K | -57.8K | -34.9K |
| API / 统一 SQLPROMPT[VOTING] | 66.2 | 67.4 | 73.4 | 50.7 | 41.0 | 40.2 | 45.0 | 29.8 | -2.3K | -2.8K | -5.2K | -2.1K |

对每个样本：当 x ∈ Q 且 SQL 生成正确（I），或模型对 x ∈ Qc 弃答（V）时，记 1 分，表示效用；当模型决定不对 x ∈ Q 生成 SQL（II）时，记 0 分，表示既无风险也无效用；当生成的 SQL 不正确（III），或模型试图对 x ∈ Qc 生成 SQL（IV）时，记惩罚 −c，表示风险。各类的实际例子见补充材料 E。

算出每个样本级分数之后，汇总 RS 取均值。该均值在抽取中断成四行：「1」「N」「P」「x ϕc(x)」，求和号呈「P」。公式抽取不完整，见原 PDF 第 6 页。正文写明是取均值，整理为 ϕc，即

$$
\phi_c=\frac{1}{N}\sum_x \phi_c(x).
$$

实验中，惩罚值 c 考虑三个选项：0、10 和 N，其中 N 是待评测的样本总数。

- c = 0：最宽松的情形。不惩罚模型所犯的任何错误。如果只处理可行问题，该分数等价于标准 text-to-SQL 准确率。
- c = 10：中等严格的情形。每 10 个正确答案与 1 个错误答案的权重相同。
- c = N：最严格的情形。哪怕其余答案全部正确，只要出现一个错误，分数就为负。

RS(c) 为 100% 表示完美的 text-to-SQL 可靠性，即模型能正确处理全部输入（用绿色覆盖图 1(c) 的所有区域）。RS(c) > 0 表示效用大于风险，因而在 text-to-SQL 可靠性的语境下可以部署。

## 4 实验

### 4.1 建模

本节描述多种用来增强 text-to-SQL 可靠性的建模方法。我们把方法分成两大途径：基于流水线的方法和统一方法。对每种途径，我们都开发开源模型和商业 API 模型，因为部署时往往依预算约束、技术专长和隐私顾虑等因素，选用其中之一。

#### 4.1.1 基于流水线的方法

在传统 NLP 任务表述中，增强 text-to-SQL 可靠性可以通过组合三项不同任务来处理：不可行问题检测 [29, 22]、SQL 生成 [14, 23]，以及 SQL 错误检测 [2]。

**开源。** SQL 生成使用 T5（T5-3B），输入是问题，后面接上列出全部表和列的序列化模式 [19]。为加入弃答机制，我们用 SQLCoder（sqlcoder-7b-2）做不可行问题检测（在 SQL 生成之前）和错误检测（在 SQL 生成之后）。不可行问题检测是在 TriageSQL [29] 上微调 SQLCoder，

<!-- 原 PDF 第 7 页 -->

**表 4：** 只用可行数据时，TrustSQL 上的模型比较。本表中 ϕ0 等价于标准 text-to-SQL 的执行准确率。阴影单元格中的分数表示没有弃答时的 SQL 表现。文本抽取无法定位哪些单元格带阴影，阴影位置见原 PDF 第 7 页。默认 `find_tables` 只抽出 T5、SQLPROMPT、DIN-SQL、MAC-SQL 的部分行；下表仍按 `get_text('text')` 中每个方法之后连续的 12 个数填写，列顺序与表 3 相同。其中 CLSP → MAC-SQL 的 ϕ10 AT 在抽取中为「-425」，没有小数位。

| 方法 | ϕ0 AT | ϕ0 AD | ϕ0 EH | ϕ0 SP | ϕ10 AT | ϕ10 AD | ϕ10 EH | ϕ10 SP | ϕN AT | ϕN AD | ϕN EH | ϕN SP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 开源 / 流水线 T5 | 57.8 | 72.6 | 86.8 | 50.9 | -364.5 | -201.3 | -44.9 | -440.6 | -20.0K | -14.5K | -12.2K | -25.8K |
| 开源 / 流水线 CLSM → T5 | 32.6 | 28.3 | 42.6 | 49.0 | -188.0 | -56.1 | -32.3 | -414.0 | -10.5K | -4.5K | -7.0K | -24.4K |
| 开源 / 流水线 T5 → ERRORM | 57.6 | 70.5 | 79.0 | 41.4 | -91.6 | -115.2 | -22.7 | -116.1 | -7.0K | -9.8K | -9.4K | -8.3K |
| 开源 / 流水线 CLSM → T5 → ERRORM | 32.4 | 28.3 | 38.2 | 39.8 | -30.7 | -28.0 | -14.2 | -110.1 | -3.0K | -3.0K | -4.9K | -7.9K |
| 开源 / 统一 T5[MAXENT] | 31.7 | 52.7 | 77.6 | 32.1 | -41.8 | -3.6 | 48.7 | -72.3 | -3.5K | -2.9K | -2.6K | -5.5K |
| 开源 / 统一 T5[MAXPROB] | 27.7 | 53.7 | 77.6 | 22.2 | -18.5 | -10.1 | 49.8 | -40.4 | -2.2K | -3.3K | -2.5K | -3.3K |
| 开源 / 统一 T5[FEATMD] | 35.5 | 64.7 | 41.4 | 0.2 | -113.7 | -175.4 | -3.5 | 0.2 | -7.1K | -12.7K | -4.2K | 0.2 |
| 开源 / 统一 T5[FEATRMD] | 45.8 | 67.7 | 86.5 | 37.4 | -193.7 | -187.4 | -36.6 | -279.5 | -11.4K | -13.5K | -11.4K | -16.7K |
| API / 流水线 SQLPROMPT | 81.5 | 82.2 | 82.3 | 54.5 | -103.4 | -96.1 | -93.3 | -400.9 | -8.7K | -9.4K | -16.3K | -23.9K |
| API / 流水线 DIN-SQL | 26.5 | 56.7 | 34.9 | 75.0 | -708.8 | -376.6 | -616.1 | -175.5 | -35.0K | -23.0K | -60.8K | -13.1K |
| API / 流水线 MAC-SQL | 49.2 | 46.3 | 44.4 | 73.6 | -448.7 | -490.2 | -511.2 | -190.1 | -23.7K | -28.6K | -51.9K | -13.8K |
| API / 流水线 CLSP → SQLPROMPT | 79.0 | 80.1 | 81.8 | 38.0 | -91.2 | -77.5 | -73.4 | -311.2 | -8.0K | -8.3K | -14.4K | -18.4K |
| API / 流水线 CLSP → DIN-SQL | 24.2 | 54.0 | 34.4 | 55.8 | -694.3 | -364.4 | -595.2 | -115.0 | -34.2K | -22.2K | -58.8K | -8.9K |
| API / 流水线 CLSP → MAC-SQL | 47.7 | 44.7 | 43.4 | 54.5 | -425 | -467.5 | -496.3 | -129.6 | -22.5K | -27.3K | -50.4K | -9.6K |
| API / 流水线 SQLPROMPT → ERRORP | 9.9 | 19.3 | 16.2 | 50.7 | 3.6 | -5.1 | 1.2 | -243.5 | -290.1 | -1.3K | -1.4K | -15.4K |
| API / 流水线 CLSP → SQLPROMPT → ERRORP | 9.0 | 18.2 | 16.1 | 35.5 | 2.7 | -4.3 | 7.5 | -180.8 | -290.1 | -1.2K | -783.9 | -11.4K |
| API / 统一 SQLPROMPT[DEMO] | 79.4 | 81.1 | 82.2 | 74.6 | -122.3 | -108.4 | -88.0 | -179.7 | -9.5K | -10.0K | -15.8K | -13.3K |
| API / 统一 SQLPROMPT[VOTING] | 34.5 | 37.9 | 49.6 | 4.7 | 5.0 | 13.5 | 20.7 | -2.8 | -1.4K | -1.3K | -2.7K | -395.3 |

记为 CLSM。对于错误检测，我们根据已训练的 T5 在 TrustSQL 验证集上生成的 SQL 及其样本级准确率，再加上 TriageSQL 中的不可行问题样本，来训练 SQLCoder，记为 ERRORM。这些模型的训练细节见补充材料 C。表示组合方法时，用箭头表示模型之间的数据流，例如 CLSM → T5 表示先做问题检测，再做 SQL 生成。

**基于 API。** SQL 生成采用 GPT-3.5（gpt-3.5-turbo-0125）的三种方法：SQLPROMPT，即少样本提示下的 SQL 生成 [1]；DIN-SQL [14]，Spider 上最先进的任务分解框架；以及 MAC-SQL [23]，BIRD [11] 上最先进的多智能体框架。我们为领域数据集调整了 DIN-SQL 和 MAC-SQL 的文本提示。弃答方面，不可行问题检测和错误检测都使用 GPT-4o。建模细节见补充材料 D。

#### 4.1.2 统一方法

要用单一模型实现 text-to-SQL 可靠性，我们探索多种带有弃答机制的 text-to-SQL 提示。此外，我们利用多种不确定性估计方法，使用 SQL 生成器的隐藏表示和概率来实现弃答。

**开源。** SQL 生成使用 T5（T5-3B），因为它在 NLP 的选择性生成 [16] 和校准 [18] 中使用广泛。弃答方面，我们利用输入的隐藏表示和输出概率，用不确定性估计检测分布外（OOD）样本并据此弃答。所用方法如下：

- **基于熵：** 每个样本取所生成 SQL 词元中的最大熵，记为 MAXENT [9]。
- **基于概率：** 每个样本取词元序列里各最高词元概率中的最小值，记为 MAXPROB [18]。
- **基于距离：** 按训练数据表示的分布计算马氏距离，记为 FEATMD [10, 16]；再用 TriageSQL 数据集作为背景分布计算相对马氏距离，记为 FEATRMD [15, 16]。

这些方法需要校准阈值，以便在分布内与分布外之间画出决策边界。我们提出的启发式方法见补充材料 C.2。

**基于 API。** 我们使用 GPT-3.5 的两种提示方法，说明如下：

- **SQLPROMPT[DEMO]：** 用相似的可行问题及其对应 SQL 查询，以及相似的不可行问题做少样本演示，不可行问题都标成 “not_answerable” [20]。演示顺序随机选取。

<!-- 原 PDF 第 8 页 -->

- **SQLPROMPT[VOTING]：** 提示与 SQLPROMPT 相同。我们将答案采样五次 [24]，只有全部样本一致同意时才采纳这次 SQL 生成；否则弃答。

## 5 结果

### 5.1 模型比较

**全量数据。** 表 3 给出各方法在 TrustSQL 基准上的表现。对开源模型而言，统一途径中基于概率的方法（即 T5[MAXENT]）和基于熵的方法（即 T5[MAXPROB]）在不同惩罚设定下始终优于其他方法。对基于 API 的模型而言，CLSP → SQLPROMPT 在 RS(0) 上最好，而 CLSP → SQLPROMPT → ERRORP 在更严格的设定（即 RS(10) 和 RS(N)）上更为出色。这表明，问题检测和错误检测对于增强 text-to-SQL 可靠性都至关重要。SQLPROMPT[VOTING] 在全部惩罚下都有值得注意的表现，尤其考虑到它很简单。

**仅可行数据。** 在可行数据上评测模型，衡量的是不必要的弃答以及错误检测器的影响，具体表现为：没有弃答时的 SQL 表现（阴影单元格）与带弃答的模型在 RS(0) 上的表现之间的下降。与全量数据设定类似，开源模型 T5[MAXENT] 和 T5[MAXPROB] 往往随着惩罚加重而表现最好。采用统一途径的 API 模型，尤其是 SQLPROMPT[VOTING]，随着惩罚增加而优于 SQLPROMPT[DEMO]。RS(0) 上的高表现意味着弃答频繁，因而在更高惩罚下表现更低。流水线方法中各组件的更详细分析见补充材料 F。

### 5.2 讨论

**问 1：为什么在 text-to-SQL 可靠性中，ALL-ABSTAIN 被视为可以部署？** 在标准 text-to-SQL 的语境里，表 3 的 ALL-ABSTAIN 不能算可以部署，因为它与该任务的根本目的相矛盾。然而，在 text-to-SQL 可靠性的语境里，ALL-ABSTAIN 在所有 c 上都得到 RS 为 50，因为它有把握地正确处理了全部输入问题的 50%（即 TrustSQL 中不可行问题所占的比例）。这种做法可能比一个为标准 text-to-SQL 优化的模型更可靠（在所有设定下绝对没有风险）；后者总是生成可能不正确的 SQL 查询，风险有可能高于效用。

**问 2：增强 text-to-SQL 可靠性的简便做法是什么？** 在严格设定下，要把 RS 至少提升到可部署水平（即大于 0），一个简便做法是：只生成模型具有高置信度的 SQL 查询，不确定时一律不生成。实验结果表明，在错误生成会受到高惩罚的设定中，这种做法尤其有效。例如，如表 3 所示，由于我们严格的启发式阈值（见补充材料 C.2），Spider 上的 T5[FEATMD] 只生成一条正确的 SQL 查询，其余全部弃答。降低风险所能增加的 RS，可以多于提高效用所能增加的分数。然而，靠这种谨慎的 SQL 生成达到更高的 RS（即大于 50%），还需要另一条尚未被充分探索的努力路线。

**问 3：为什么需要把 TrustSQL 作为 text-to-SQL 基准？** 现有基准没有基于惩罚的评分，也没有考虑不可行问题。TrustSQL 通过把 SQL 生成与弃答放在一起建模，并处理不可行问题检测中的错误情形来填补这些空白；这些错误随后会传递到 SQL 生成和错误检测。这种综合途径鼓励新的建模角度，以增强可靠性。例如，表 1 中的 column-surface 和 non-sql 就是基于 GPT-4o 的不可行问题检测与错误检测方法（即 CLSP → SQLPROMPT → ERRORP）未能处理好的例子。传统任务设定探索不到这类情形，也就无法展示这些模型如何回应不可行问题。例如，对问题 “What is the average attendance capacity for all the shows?”（库中只有 attendance 列，没有 capacity），模型生成查询 “SELECT avg(attendance) FROM show”，并从数据库返回结果 1326.4。TrustSQL 的综合途径为 text-to-SQL 生成中的错误情形提供了新的视角，并鼓励开发更可靠的模型。

<!-- 原 PDF 第 9 页 -->

## 6 相关工作

**Text-to-SQL 中的模型可靠性。** Text-to-SQL 因其实际应用而受到大量关注。主要的单领域数据集包括 ATIS [3]、GeoQuery [28]、Advising [4]、SEDE [5] 和 EHRSQL [9]。跨领域任务方面，Spider [27] 和 BIRD [11] 是 SQL 生成的重要基准。然而，这些基准假定所有输入问题都应当生成 SQL，因而缺少开发弃答模型的激励。缺少这类安全措施，会损害可靠部署。有些工作关注在给定数据库模式的情况下检测不可行问题 [29, 22]，但它们没有把 SQL 生成整合进来，也没有考虑 text-to-SQL 模型处理错误的能力。我们的工作旨在整合综合性的可靠性度量，使基准更接近对模型的信任。

**NLP 中的不确定性估计。** 不确定性估计对人工智能的可靠性至关重要 [6]。相关方法包括基于概率的方法（计算熵或模型所赋予的概率）[12, 26, 7, 18]，以及基于距离的方法（使用马氏距离等度量，把新输入与训练数据相比较）[10, 30, 15, 16]。基于概率的方法衡量模型置信度，从而增强输出的可靠性。基于距离的方法识别那些可能产生低质量输出的离群点，促进更安全的人工智能部署。我们的工作同时采用这两类方法，为 text-to-SQL 模型开发弃答机制。

## 7 结论与未来方向

本文提出 TrustSQL，一个用于评估 text-to-SQL 可靠性的新基准。可靠性定义为模型正确处理任意类型输入问题的能力：对可行问题生成正确的 SQL 查询，并对不可行问题弃答。为此，我们依据不熟悉模型能力的用户可能遇到的常见错误情形构造了该基准。我们采用现有建模策略，开发并评估了两种途径：基于流水线的方法和统一方法。使用基于惩罚的评分指标后，实验结果表明，完成这一任务需要多种建模途径，也为模型开发打开了新的路径。

尽管我们仔细设计了该基准，仍有若干局限。第一，尽管我们努力覆盖范围广泛的不可行问题，基准仍然不能涵盖真实场景中出现的全部此类问题。第二，本文聚焦单轮 text-to-SQL 任务，没有处理实体链接与模式链接中的不确定性消歧，也没有处理用户意图的消歧。最后，若商业 API 模型发生任何更新，实验中这些模型的结果可能无法复现。

未来研究方向包括：开发能够预先规划、从而在 RS(N) 上取得高表现的基于智能体的方法，从而绕过对提示工程和领域适配等策略的大量需求，加速 text-to-SQL 在不同领域中更广泛的采用。

## 参考文献

[1] Shuaichen Chang and Eric Fosler-Lussier. 如何为 text-to-SQL 提示大语言模型：零样本、单领域与跨领域设定中的一项研究. arXiv preprint arXiv:2305.11853, 2023.

[2] Xinyun Chen, Maxwell Lin, Nathanael Schaerli, and Denny Zhou. 教大语言模型自我调试. In The 61st Annual Meeting Of The Association For Computational Linguistics, 2023.

[3] Deborah A Dahl, Madeleine Bates, Michael K Brown, William M Fisher, Kate Hunicke-Smith, David S Pallett, Christine Pao, Alexander Rudnicky, and Elizabeth Shriberg. 扩展 ATIS 任务的范围：ATIS-3 语料库. In Human Language Technology: Proceedings of a Workshop held at Plainsboro, New Jersey, March 8-11, 1994, 1994.

[4] Catherine Finegan-Dollak, Jonathan K Kummerfeld, Li Zhang, Karthik Ramanathan, Sesh Sadasivam, Rui Zhang, and Dragomir Radev. 改进 text-to-SQL 的评测方法. In Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 351–360, 2018.

[5] Moshe Hazoom, Vibhor Malik, and Ben Bogin. 真实环境中的 text-to-SQL：一个基于 Stack Exchange 数据、自然出现的数据集. In Proceedings of the 1st Workshop on Natural Language Processing for Programming (NLP4Prog 2021), pages 77–87, 2021.

<!-- 原 PDF 第 10 页 -->

[6] Dan Hendrycks, Nicholas Carlini, John Schulman, and Jacob Steinhardt. 机器学习安全中尚未解决的问题. arXiv preprint arXiv:2109.13916, 2021.

[7] Daeyoung Kim, Seongsu Bae, Seungho Kim, and Edward Choi. 面向结构化电子健康记录问答的、带不确定性意识的 text-to-program. In Conference on Health, Inference, and Learning, pages 138–151. PMLR, 2022.

[8] Chia-Hsuan Lee, Oleksandr Polozov, and Matthew Richardson. KaggleDBQA：对 text-to-SQL 解析器的现实评测. In Chengqing Zong, Fei Xia, Wenjie Li, and Roberto Navigli, editors, Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers), pages 2261–2273, Online, August 2021. Association for Computational Linguistics.

[9] Gyubok Lee, Hyeonji Hwang, Seongsu Bae, Yeonsu Kwon, Woncheol Shin, Seongjun Yang, Minjoon Seo, Jong-Yeup Kim, and Edward Choi. EHRSQL：面向电子健康记录的实用 text-to-SQL 基准. Advances in Neural Information Processing Systems, 35:15589–15601, 2022.

[10] Kimin Lee, Kibok Lee, Honglak Lee, and Jinwoo Shin. 一个用于检测分布外样本与对抗攻击的简单统一框架. Advances in neural information processing systems, 31, 2018.

[11] Jinyang Li, Binyuan Hui, GE QU, Jiaxi Yang, Binhua Li, Bowen Li, Bailin Wang, Bowen Qin, Ruiying Geng, Nan Huo, et al. 大语言模型是否已经能够充当数据库接口？一个面向大规模、以数据库为根据的 text-to-SQL 的大型基准. In Thirty-seventh Conference on Neural Information Processing Systems Datasets and Benchmarks Track, 2023.

[12] Petr Marek, Vishal Ishwar Naik, Anuj Goyal, and Vincent Auvray. OODGAN：用于生成域外数据的生成对抗网络. In Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies: Industry Papers, pages 238–245, 2021.

[13] Xinyu Pi, Bing Wang, Yan Gao, Jiaqi Guo, Zhoujun Li, and Jian-Guang Lou. 走向 text-to-SQL 模型面对自然且现实的对抗性表格扰动时的稳健性. In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 2007–2022, Dublin, Ireland, May 2022. Association for Computational Linguistics.

[14] Mohammadreza Pourreza and Davood Rafiei. DIN-SQL：带自我修正的 text-to-SQL 分解式上下文学习. In Thirty-seventh Conference on Neural Information Processing Systems, 2023.

[15] Jie Ren, Stanislav Fort, Jeremiah Liu, Abhijit Guha Roy, Shreyas Padhy, and Balaji Lakshminarayanan. 为改进近分布外检测而对马氏距离所作的一项简单修正. Dimension, 2:0.

[16] Jie Ren, Jiaming Luo, Yao Zhao, Kundan Krishna, Mohammad Saleh, Balaji Lakshminarayanan, and Peter J Liu. 条件语言模型的分布外检测与选择性生成. In The Eleventh International Conference on Learning Representations, 2022.

[17] Ravid Shwartz-Ziv and Amitai Armon. 表格数据：深度学习并非你所需要的全部. Information Fusion, 81:84–90, 2022.

[18] Elias Stengel-Eskin and Benjamin Van Durme. 经过校准的解释：语义解析中的置信度估计. Transactions of the Association for Computational Linguistics, 11:1213–1231, 2023.

[19] Alane Suhr, Ming-Wei Chang, Peter Shaw, and Kenton Lee. 探索跨数据库语义解析中尚未被探索的泛化挑战. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, pages 8372–8388, Online, July 2020. Association for Computational Linguistics.

[20] Haitian Sun, William W Cohen, and Ruslan Salakhutdinov. ConditionalQA：一个带有条件式答案的复杂阅读理解数据集. arXiv preprint arXiv:2110.06884, 2021.

[21] Boris van Breugel and Mihaela van der Schaar. 为什么表格基础模型应当成为研究优先事项. arXiv preprint arXiv:2405.01147, 2024.

[22] Bing Wang, Yan Gao, Zhoujun Li, and Jian-Guang Lou. 知道我所不知道的：为 text-to-SQL 处理歧义问题与未知问题. In Anna Rogers, Jordan Boyd-Graber, and Naoaki Okazaki, editors, Findings of the Association for Computational Linguistics: ACL 2023, pages 5701–5714, Toronto, Canada, July 2023. Association for Computational Linguistics.

<!-- 原 PDF 第 11 页 -->

[23] Bing Wang, Changyu Ren, Jian Yang, Xinnian Liang, Jiaqi Bai, Qian-Wen Zhang, Zhao Yan, and Zhoujun Li. MAC-SQL：面向 text-to-SQL 的多智能体协作. arXiv preprint arXiv:2312.11242, 2023.

[24] Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V Le, Ed H Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou. 自一致性改进语言模型中的思维链推理. In The Eleventh International Conference on Learning Representations, 2022.

[25] Spencer Whitehead, Suzanne Petryk, Vedaad Shakib, Joseph Gonzalez, Trevor Darrell, Anna Rohrbach, and Marcus Rohrbach. 可靠的视觉问答：与其答错，不如弃答. In European Conference on Computer Vision, pages 148–166. Springer, 2022.

[26] Yijun Xiao and William Yang Wang. 论条件语言生成中的幻觉与预测不确定性. In Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics: Main Volume, pages 2734–2744, 2021.

[27] Tao Yu, Rui Zhang, Kai Yang, Michihiro Yasunaga, Dongxu Wang, Zifan Li, James Ma, Irene Li, Qingning Yao, Shanelle Roman, et al. Spider：一个用于复杂且跨领域的语义解析与 text-to-SQL 任务的大规模人工标注数据集. In Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing, pages 3911–3921, 2018.

[28] John M. Zelle and Raymond J. Mooney. 用归纳逻辑编程学习解析数据库查询. In Proceedings of the Thirteenth National Conference on Artificial Intelligence - Volume 2, pages 1050–1055, 1996.

[29] Yusen Zhang, Xiangyu Dong, Shuaichen Chang, Tao Yu, Peng Shi, and Rui Zhang. 你问了一个好问题吗？一个面向 text-to-SQL 的跨领域问题意图分类基准. arXiv preprint arXiv:2010.12634, 2020.

[30] Yinhe Zheng, Guanyi Chen, and Minlie Huang. 对话系统中自然语言理解的域外检测. IEEE/ACM Transactions on Audio, Speech, and Language Processing, 28:1198–1209, 2020.

<!-- 原 PDF 第 12 页 -->

## 补充材料目录

下列页码是原文自带的页码。

- A 数据集数据说明（Datasheet for Datasets），第 13 页
- B Text-to-SQL 数据集的复杂度，第 17 页
  - B.1 为种子可行问题选择数据集，第 17 页
  - B.2 TrustSQL 中的查询难度，第 17 页
- C 开源模型的建模细节，第 19 页
  - C.1 基于流水线的方法，第 19 页
  - C.2 统一方法，第 19 页
- D 商业 API 模型的建模细节，第 21 页
  - D.1 基于流水线的方法，第 21 页
  - D.2 统一方法，第 21 页
- E 可靠性分数的定性分析，第 22 页
- F 详细的模型表现，第 24 页
  - F.1 在全部模型输出中正确 SQL 所占的表现，第 24 页
  - F.2 流水线方法的不可行问题检测表现，第 25 页
  - F.3 流水线方法的 SQL 生成表现，第 25 页
  - F.4 流水线方法的错误检测表现，第 26 页
- G 数据预处理，第 27 页
- H GitHub 链接与 Croissant 元数据记录，第 28 页
- I 作者声明，第 28 页

<!-- 原 PDF 第 13 页 -->

## A 数据集数据说明

### A.1 动机

- **创建该数据集的目的是什么？**  
  TrustSQL 用来评测 text-to-SQL 可靠性。可靠性定义为：模型能够正确处理任意类型的输入问题，对可行问题生成正确的 SQL 查询，并对不可行问题弃答（例如由于模式不兼容，或所需功能超出 SQL）。基准同时纳入可行问题与不可行问题这两个方面，目的是评估现有模型能否通过恰当弃答来赢得对其输出的信任，并鼓励 text-to-SQL 模型在实验设定之外的各个领域被更广泛地采用。

- **谁创建了该数据集（例如哪个团队、研究组），代表哪个实体（例如公司、机构、组织）？**  
  本文作者。

- **谁资助了该数据集的创建？如果有相关资助，请提供资助方名称以及项目名称和编号。**  
  本工作得到韩国政府（MSIT）资助的 Institute for Information & communications Technology Promotion（IITP）项目（No.RS-2019-II190075），以及 National Research Foundation of Korea（NRF）项目（NRF-2020H1D3A2A03100945）的支持。

### A.2 构成

- **构成数据集的实例代表什么（例如文档、照片、人物、国家）？**  
  TrustSQL 包含自然语言问题及其对应的 SQL 查询（若可行）；不可行问题没有对应的 SQL。

- **总共有多少实例（如适用，请按类型分别说明）？**  
  约有 21.4K 条数据实例（18.9K 条可行；2.5K 条不可行）。

- **数据集是否包含全部可能的实例，还是来自更大集合的一个样本（不一定是随机样本）？**  
  这是 TrustSQL 的完整数据。

- **每个实例由什么数据组成？**  
  TrustSQL 包含两组数据：可行问题的问题–SQL 对，以及不可行问题的仅问题数据。

- **每个实例是否关联有标签或目标？**  
  标签是 SQL 查询。

- **单个实例是否缺少任何信息？如果是，请说明缺少什么，并解释原因（例如因为当时无法获得）。这里不包括有意删除的信息，但可能包括例如经过涂黑的文本。**  
  不适用。

- **个体实例之间的关系是否被明确给出（例如用户的电影评分、社交网络链接）？**  
  不适用。

- **是否有推荐的数据划分（例如训练、开发/验证、测试）？**  
  我们提供已经划分好的数据集。

- **数据集中是否存在错误、噪声来源或冗余？**  
  我们已尽最大努力确保每条数据实例都能最好地服务于其目的，而不含错误或噪声。将来仍可能出现意料之外的错误或噪声；一旦发现，我们愿意予以纠正。

- **数据集是自包含的，还是链接到外部资源，或以其他方式依赖外部资源（例如网站、推文、其他数据集）？**  
  如果用户遵守下载链接中的许可，该数据集是自包含的。

<!-- 原 PDF 第 14 页 -->

- **数据集是否包含可能被视为机密的数据（例如受法律特权或医患保密保护的数据，或包含个人非公开通信内容的数据）？**  
  不适用。

- **数据集是否包含直接查看时可能具有冒犯性、侮辱性、威胁性，或可能以其他方式引起焦虑的数据？**  
  不适用。

- **数据集是否与人有关？**  
  EHRSQL 部分与人有关。

- **数据集是否标识任何亚群体（例如按年龄、性别）？**  
  否。

- **是否可能从数据集中直接或间接（即与其他数据结合）识别出个人（即一个或多个自然人）？**  
  否。

- **数据集是否包含在任何意义上可能被视为敏感的数据（例如揭示种族或民族出身、性取向、宗教信仰、政治观点或工会成员身份，或所在地点的数据；财务或健康数据；生物特征或遗传数据；政府身份证件，如社会安全号码；犯罪史）？**  
  EHRSQL 部分的问题–SQL 对链接到 MIMIC-IV Demo。该数据已按 HIPAA 标准去标识，并且对任何遵守其许可的人完全公开。

### A.3 收集过程

- **与每个实例关联的数据是如何获得的？**  
  我们基于现有 text-to-SQL 数据集及其数据库，整理并修改了 TrustSQL 中的问题–SQL 对（可行问题）。不可行问题由作者根据现有数据库手工标注。

- **收集数据使用了哪些机制或程序（例如硬件装置或传感器、人工整理、软件程序、软件 API）？**  
  我们主要使用 Excel、Google Sheets 和 Python 来收集、处理并标注数据。此外，我们使用 OpenAI 的 GPT-4 为每个问题模板生成释义。

- **如果数据集是来自更大集合的样本，抽样策略是什么（例如确定性抽样，或具有特定抽样概率的概率抽样）？**  
  不适用。

- **谁参与了数据收集过程（例如学生、众包人员、承包商），他们如何获得报酬（例如众包人员的报酬是多少）？**  
  数据收集过程中有三个部分需要人工参与：问题–SQL 数据的预处理、问题释义，以及针对每个数据库的不可行问题标注。在所有情况下，这些过程都由作者完成，必要时借助 GPT-4。如果使用了 GPT-4，作者会人工复查全部数据，以保持高质量。

- **数据是在什么时间范围内收集的？**  
  不适用。

- **是否进行过任何伦理审查程序（例如由机构审查委员会进行）？**  
  不适用。

- **数据集是否与人有关？**  
  EHRSQL 部分与人有关。

- **你是直接从相关个人那里收集数据，还是通过第三方或其他来源（例如网站）获得？**  
  不适用。

- **相关个人是否被告知数据收集一事？**  
  不适用。

<!-- 原 PDF 第 15 页 -->

- **相关个人是否同意收集并使用其数据？**  
  不适用。

- **如果已获得同意，是否向同意的个人提供了在将来或针对某些用途撤回同意的机制？**  
  不适用。

- **是否分析过该数据集及其使用对数据主体的潜在影响（例如数据保护影响分析）？**  
  我们使用的 EHRSQL 数据库已经去标识。

### A.4 预处理 / 清洗 / 标注

- **是否对数据做过任何预处理、清洗或标注（例如离散化或分桶、分词、词性标注、SIFT 特征提取、删除实例、处理缺失值）？**  
  为构造 TrustSQL 做了大量预处理。细节见第 G 节。

- **除预处理、清洗、标注后的数据之外，是否保存了「原始」数据（例如为了支持事先未预料到的未来用途）？**  
  不适用。

- **用于预处理、清洗、标注数据的软件是否可以获得？**  
  预处理、清洗和标注使用 Excel、Google Sheets 和 Python 完成。

### A.5 用途

- **该数据集是否已经用于某些任务？**  
  原始数据集被用于 text-to-SQL 建模。

- **是否有仓库链接到使用该数据集的任何或全部论文或系统？**  
  ATIS 和 Advising 的原始版本见 https://github.com/jkkummerfeld/text2sql-data。  
  EHRSQL 见 https://github.com/glee4810/ehrsql-2024。  
  Spider 见 https://github.com/taoyds/spider。

- **该数据集还可以用于哪些（其他）任务？**  
  不适用。

- **数据集的构成，或它被收集、预处理、清洗、标注的方式，是否有任何可能影响未来用途的地方？**  
  不适用。

- **是否有不应当使用该数据集的任务？**  
  不适用。

### A.6 分发

- **数据集是否会分发给创建它所代表的实体（例如公司、机构、组织）之外的第三方？**  
  否。

- **数据集将如何分发（例如网站上的压缩包、API、GitHub）？**  
  数据集发布于 https://github.com/glee4810/TrustSQL。

- **数据集将于何时分发？**  
  现在。

- **数据集是否会在版权或其他知识产权（IP）许可下，和/或在适用的使用条款（ToU）下分发？**  
  数据集在 CC-BY-4.0 许可下发布。

- **是否有任何第三方对与实例关联的数据施加了基于知识产权的限制或其他限制？**  
  否。

- **是否有任何出口管制或其他监管限制适用于该数据集或单个实例？**  
  否。

<!-- 原 PDF 第 16 页 -->

### A.7 维护

- **谁将支持、托管并维护该数据集？**  
  本文作者。

- **如何联系数据集的所有者、管理者或管理人员（例如电子邮件地址）？**  
  联系第一作者（gyubok.lee@kaist.ac.kr）或其他作者。

- **是否有勘误？**  
  否。

- **数据集是否会更新（例如纠正标注错误、增加新实例、删除实例）？**  
  如果需要任何纠正，我们计划上传新版本。

- **如果数据集与人有关，对与实例关联的数据的保留是否有适用的限制（例如，相关个人是否被告知其数据将保留一段固定时间然后删除）？**  
  不适用。

- **数据集的旧版本是否会继续得到支持、托管和维护？**  
  我们计划只维护最新版本。

- **如果其他人想扩展、增补、在其基础上构建或向该数据集贡献，是否有相应机制？**  
  联系本文作者。



