# EHRSQL: A Practical Text-to-SQL Benchmark for Electronic Health Records

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`EHRSQL_NeurIPS2022.pdf`。

## Abstract 摘要

我们提出一个面向电子健康记录（electronic health records, EHRs）的新 text-to-SQL 数据集。语句收集自 222 名医院工作人员，包括医生、护士、保险审核与病案团队等。为了在结构化 EHR 数据上构建 QA 数据集，我们在一家大学医院进行了调查，并把回答模板化以创建种子问题。然后，我们手工把它们链接到两个开源 EHR 数据库——MIMIC-III 和 eICU——并把它们与各种时间表达式，以及留出的不可回答问题一起纳入数据集；这些内容都来自该调查。我们的数据集提出一组独特挑战：模型需要 1）生成反映医院中广泛需求的 SQL 查询，包括简单检索以及计算生存率等复杂操作；2）理解各种时间表达式，以回答医疗中对时间敏感的问题；3）根据预测置信度区分给定问题是可回答还是不可回答。我们相信，数据集 EHRSQL 可以作为在结构化 EHR 数据上开发与评估 QA 模型的实用基准，并朝弥合 text-to-SQL 研究与其在医疗中的真实部署之间的差距再进一步。EHRSQL 公开于 https://github.com/glee4810/EHRSQL 。

## 1 Introduction 引言

电子健康记录（EHRs）是关系数据库，存储患者在医院中的全部病史。从入院到患者治疗与出院，医院中发生的所有医疗事件都被记录并存储在 EHR 中。这些记录以表格、文本和图像等多种形式，覆盖从个体层面信息到群体层面认识的广泛临床知识 [16, 17, 11, 15]。作为一个庞大而全面的知识库，包括医生、护士和行政人员在内的医院工作人员不断与 EHR 交互，以存储和检索患者信息，从而做出更好的临床决策 [32, 3]。与此同时，大多数医院工作人员使用预定义的规则转换系统与 EHR 数据库交互。要寻找规则之外的信息，就需要接受专门训练来修改和扩展该系统 [32]。因此，用户要充分利用 EHR 中存储的信息，存在巨大瓶颈。

解决这一问题的另一种方式，是构建一个能够自动把问题直接翻译成相应 SQL 查询的系统。然后，用户只需键入或口头向系统提问，系统就会返回答案，而无需经过任何复杂过程。这样的系统将释放 EHR 数据的潜力，并极大加快任何涉及从数据库检索数据的任务。

现有针对结构化 EHR 数据问答（QA）的数据集是 MIMICSQL [32] 和 emrKBQA [27]。MIMICSQL 是 MIMIC-III [16] 上第一个医疗 QA 数据集，其中的问题由预定义模板自动生成。emrKBQA 是另一个基于 MIMIC-III 的数据集，派生自临床阅读理解数据集 emrQA [23]。然而，通过在一家大学医院的调查，我们发现现有数据集在若干方面远未满足医院工作场所的实际需求。

我们提出 EHRSQL，一个链接到两个开源 EHR 数据库——MIMIC-III [16] 和 eICU [25]——的新的大规模 text-to-SQL 数据集。该数据集以 CC BY-SA 4.0 许可分发。据我们所知，我们的工作是第一个既反映医院工作人员多样需求、又引入部署医疗 QA 系统时实际问题的 EHR QA 数据集。该数据集提出的独特挑战有三方面：

- **问题范围广。** 我们在一家大学医院进行调查，收集针对结构化 EHR 数据的常见问题。受访者共 222 人，其职业经验年限各不相同（见图 1）。在过滤并把回答模板化之后，所得模板覆盖广泛的问题，包括检索患者记录（例如所测生命体征和住院费用），以及进行复杂的群体层面操作（例如检索确诊某种疾病后开具次数最多的 top N 药物，以及计算 N 年生存率）。更多例子见表 1。
- **对时间敏感的问题。** 基于该调查，我们了解到医院工作场所中的真实问题富含时间表达式，因为时间是医疗中最关键的方面之一。为了在数据集中反映这一点，我们系统地把时间分成多种表达式类型（例如绝对、相对和混合）、单位（例如就诊、月和日）以及区间类型（例如 since、until 和 in）。然后，我们把分类后的时间与问题模板组合，以模拟医院中提出的对时间敏感的问题。更多细节在第 3.1.2 节讨论。
- **可信的 QA 系统。** 开发可信系统对在医疗中采用 AI 至关重要。同样，QA 系统需要只返回准确答案，并拒绝回答超出其能力的问题。为检验这一点，我们把不可回答的问题纳入数据集，利用调查结果中剩余的语句。这些语句不可回答，是因为与数据库模式不兼容，或需要外部领域知识。

## 2 Related Works 相关工作

**EHR QA。** Pampari et al. [23] 提出 emrQA，基于医生的常见问题，在临床笔记上做问答。后来，Raghavan et al. [27] 提出 emrKBQA，把 emrQA 适配到 MIMIC-III 中的结构化患者记录。在本文工作时，emrKBQA 尚未公开。由于原数据集针对门诊患者，emrKBQA 中问题的范围大多限于询问患者的检验结果 [27]。最近，Wang et al. [32] 提出 MIMICSQL，首次以 text-to-SQL 生成任务处理 EHR QA。为构建该数据集，他们基于预定义规则自动生成问题，并通过众包加以过滤。然而，MIMICSQL 的问题范围有限，SQL 查询也简单，且限制在五张表上，这与医院中的实际用例相去甚远 [24]。另一方面，EHRSQL 源自实际调查结果，覆盖在结构化 EHR 数据上经常被问到的多种真实世界问题（平均跨越 13.5 张表）（见表 1）。

**语义解析数据集。** 在过去几十年中，语义解析一直是自然语言处理中最活跃的研究领域之一 [13, 37, 34, 9]。它把自然语言语句转换为逻辑形式表示，这些表示常常是可执行程序，例如 Python 脚本和 SQL 查询。WikiSQL [40] 和 Spider [35] 是在未见数据库上评估语义解析模型的领先数据集。WikiSQL 提供从维基百科 HTML 表格中抽取的广泛数据库领域，但它只包含简单 SQL 查询和单表。Spider 旨在处理多个数据库领域中多张表上的复杂查询，包括连接和集合操作。最近，已提出更真实的数据集，以弥合语义解析中学术设定与实际设定之间的差距。KaggleDBQA [19] 利用来自 Kaggle 的真实世界数据库，并构建领域特定问题，而不依赖数据库模式。SEDE [12] 处理 Stack Exchange 用户在现实生活中提出的复杂 SQL 查询。我们的动机与他们一致：真实世界的医疗 QA 系统会带来额外挑战。

**QA 中的不可回答问题。** 在问答的早期，不可回答问题通过远距离监督 [18, 4]、基于规则的编辑 [14]，或由众包工作者对抗式创建 [28] 来生成。然而，在语义解析中，大多数工作假设所有输入问题都有效且可以回答；这在实践中并不成立 [38]。为确保系统可靠性，对模型而言，检索所有输入问题的答案并不总是可取的。为此，Zhang et al. [38] 利用其他 text-to-SQL 和闲聊数据集来构造不可回答问题，并把该问题作为检测不可回答问题的分类任务提出。另一方面，我们的工作同时处理系统可靠性与语义解析，并且不可回答问题是通过调查自然收集的。在任务型对话系统中，同一任务以域外（Out-of-Domain, OOD）检测的名义被研究；出于实际原因，若干近期工作在训练期间不向模型显式展示 OOD 样本来处理这一问题。遵循他们的设定，我们的不可回答问题只包含在验证集和测试集中。

表 1：EHRSQL 中的示例语句（SQL 查询按 MIMIC-III 与 eICU 模式分别标注）。抽取文本中词间空格大量丢失，下表按可辨认的词边界还原；科室列与问句在版面中粘连，对应关系依抽取顺序整理。

| 类型（Type） | 子类 | 示例问题（Sample question） | 科室（Department） |
| --- | --- | --- | --- |
| 问题多样性（Question diversity） | Demographics | Tell me the birthdate of patient 92721? | Nursing |
| 问题多样性 | Prescription | When was the first prescription time of patient 20000? | Nursing |
| 问题多样性 | Vital sign | What was the last arterial bp [systolic] for patient 23042? | Physician, Nursing, Health records, Other |
| 问题多样性 | Cost | What is the average total hospital cost that involves non-invasive mech vent? | Insurance review |
| 问题多样性 | Survival rate | What is the five diagnoses which have the lowest four year survival rate? | Nursing |
| 问题多样性 | Longitudinal statistics | What are the five most commonly prescribed drugs for patients who have been diagnosed with hypotension no earlier since 2104 within 2 months? | Physician, Nursing |
| 对时间敏感的问题（Time-sensitive question） | Absolute | Is the heart rate of patient 2518 measured at 2105-12-31 12:00:00 less than the value measured at 2105-12-31 09:00:00? | Physician |
| 对时间敏感的问题 | Absolute | Tell me the last specimen test given to patient 51177 in 10/2105? | Nursing |
| 对时间敏感的问题 | Relative | Tell me patient 6990’s daily average gastric meds intake on the last ICU visit. | - |
| 对时间敏感的问题 | Mixed | Tell me the medication that patient 3929 has been prescribed for the first time in 05/this year. | Nursing |
| 不可回答问题（Unanswerable question） | Requiring external knowledge | What is the name of the medication which should not be administered during the contrast arteriogram-leg treatment? | Nursing |
| 不可回答问题 | Beyond DB schema | When is the next earliest hospital visit of patient 73652? | Nursing |
