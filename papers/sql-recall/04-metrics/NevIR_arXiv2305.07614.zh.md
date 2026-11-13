原文件名：NevIR_arXiv2305.07614.pdf

原标题：NevIR: Negation in Neural Information Retrieval

中文标题：NevIR：神经信息检索中的否定

作者：Orion Weller, Dawn Lawrie, Benjamin Van Durme（Johns Hopkins University；oweller@cs.jhu.edu）

来源：arXiv:2305.07614v2 [cs.IR] 26 Feb 2024

<!-- 原 PDF 第 1 页 -->

# NevIR：神经信息检索中的否定

Orion Weller, Dawn Lawrie, Benjamin Van Durme

Johns Hopkins University

oweller@cs.jhu.edu

## 摘要

否定是日常生活中的常见现象，也一直是语言模型（LM）的薄弱环节。尽管信息检索（IR）社区已把语言模型当作现代 IR 架构的骨干，但关于否定如何影响神经 IR，几乎没有研究。因此，我们围绕这一主题构建了一个直截了当的基准：要求 IR 模型对仅在否定上有差异的两篇文档进行排序。可以看到，结果随 IR 架构类型而有很大差异：交叉编码器表现最好，其次是后期交互模型，双编码器与稀疏神经架构垫底。我们发现，大多数信息检索模型（包括当前最优模型）并不考虑否定，表现与随机排序相同，甚至更差。我们表明，尽管在包含否定的对比文档数据集上继续微调这一显而易见的做法能够提升性能（模型规模增大同样如此），机器与人类表现之间仍有很大差距。[^1]

[^1]: 代码与数据见 https://github.com/orionw/NevIR

## 1 引言

自然语言处理（NLP）的近期工作表明，语言模型难以理解包含否定的文本（Ravichander et al., 2022; McKenzie et al., 2022），表现远不如人类。这一尚未解决的问题会影响到信息检索模型，因为这些模型以语言模型作为架构的起始骨干。

然而，IR 中关于否定的工作主要集中在前神经时代（即不使用 LM）的检索（Kim and Kim, 1990; McQuire and Eastman, 1998; Averbuch et al., 2004; Kim et al., 2019），尚无研究考察否定如何影响现代神经 IR。不能理解 IR 中的否定，可能在高风险情境中造成严重后果。一个突出案例是：Google Search 在告诉用户癫痫发作时该怎么做时，把某网站专门说明“不该做什么”的要点逐条列了出来（图 1）。

**图 1 中的可见文字：**

癫痫发作了，现在怎么办？

按住患者，或试图阻止其动作。往患者嘴里塞东西（这会造成牙齿或下颌损伤）。在发作期间实施 CPR 或其他口对口呼吸。在患者再次清醒之前给予食物或水。

**图 1：** 否定是 IR 系统未能很好理解的现象。该截图显示，Google Search 因未能捕捉文章中的否定（例如 “do not ...”）而给出了致命建议。

人们很容易想象法律、教育或政治等高风险领域中的其他严重失败情形。即便在日常随意使用中，神经 IR 不理解否定，也会忽略整整一类用户查询，例如“我在［度假小镇］不该住在哪里？”“谁没有赢得 2023 年的奥斯卡？”“OpenAI 未能发布关于 GPT-4 的哪些信息？”

我们旨在填补文献中的这一空白，提出一个用于信息检索中否定评估的基准，称为 NevIR（读作 “never”）。NevIR 建立在既有否定研究（Ravichander et al., 2022）之上，使用 2,556 个对比文档对实例，这些文档对仅在一处关键否定上有所不同。随后，我们为每一对中的两篇文档众包查询标注：每条查询只与其中一篇文档相关，而与另一篇无关（图 2）。由此可以检验模型在考虑否定时是否能正确排序文档。

我们发现，几乎所有 IR 系统都忽略否定，通常对两条查询都把两篇文档中的

<!-- 原 PDF 第 2 页 -->

同一篇打出更高的分数。此外，当前最优模型的表现与随机排序文档对几乎相同，或差得多。我们对这些结果进行分析，表明尽管存在否定词，两篇文档的双编码器表示几乎相同，并且 ColBERT 等后期交互模型在 MaxSim 算子中忽略否定词。

我们还表明，在否定数据上继续微调 IR 模型，能在 NevIR 上带来一定增益，但仍有很大的改进空间（同时还会略微损害 MSMarco 等传统基准上的表现）。我们希望这一分析能促使人们更加关注信息检索中的否定问题，并提供一个用于 IR 训练与评估的数据集。

## 2 背景

### 2.1 动机

信息检索（IR）是一项定义宽泛的任务：根据自然语言查询找到相关的信息片段。IR 的具体形式在语言、领域（例如法律）和目的（例如反驳论点、列表、一般事实）上可以差别很大。请注意，其中许多专门情形都会因更好地理解否定而得到改进，例如列表、反驳论点，以及领域特定语言（例如法律或医学）。

随着神经 IR 的进步，检索增强语言模型也兴起，例如 RAG（Lewis et al., 2020）、FiD（Izacard and Grave, 2021）和 SeeKeR（Shuster et al., 2022）。就在最近几个月，生成式检索已经产品化，相关系统包括 Google 的 Bard、Bing Chat 和 You.com。[^2] 这些系统把 IR 模型与大语言模型结合起来，使其能够即时查找并生成对查询的回复。

因此，随着 LM 与 IR 系统更加交织并投入生产使用，理解并改进它们的失败情形（例如否定），对公司和用户都变得至关重要。

[^2]: https://bard.google.com/、https://www.bing.com/new 以及 https://you.com

**图 2 中的文档与查询：**

文档 1：由于镍耐腐蚀，它偶尔被用作装饰性银的替代品。1859 年之后，镍在一些国家也偶尔被用作廉价铸币金属（见上文），但在 20 世纪后期，除美国和加拿大外，它被更便宜的不锈钢（即铁）合金所取代。

文档 2：由于镍耐腐蚀，它偶尔被用作装饰性银的替代品。1859 年之后，镍在一些国家也偶尔被用作廉价铸币金属（见上文），但在 20 世纪后期，在整个美国、加拿大以及美洲其他地方，它被更便宜的不锈钢（即铁）合金所取代。

查询（对应文档 1）：20 世纪哪些国家没有用铁合金取代镍？

查询（对应文档 2）：20 世纪哪些国家用铁合金取代了镍？

图中两个排序列表示例均为：1. 文档 1；2. 文档 2。

**图 2：** 一个实例及评估过程。来自 CondaQA（Ravichander et al., 2022）的初始文档经由 Mechanical Turk 生成查询。下半部分展示成对准确率的评估过程：模型必须把两条查询都排对。在此例中，IR 模型的成对准确率为零，两条查询都把文档 1 排在文档 2 之上（未能考虑否定）。

### 2.2 神经 IR

自 2020 年以来，信息检索的神经模型在大多数情况下普遍优于传统稀疏方法（例如 BM25）（Karpukhin et al., 2020; Khattab and Zaharia, 2020）。给定大量训练数据，这些模型使用对比损失进行优化，以学习文档如何与给定查询相关。这些方法相对稀疏方法有若干优势，包括能够超越简单的词汇匹配，从而编码自然语言文本的语义相似度。

<!-- 原 PDF 第 3 页 -->

近期工作关注神经模型在没有任何领域特定训练数据的情况下泛化到新领域的能力（例如零样本）。此类工作的一个突出基准是 BEIR 数据集套件（Thakur et al., 2021），它在一系列多样化的 IR 数据集上评估模型的泛化。我们的工作同时提供零样本设定（不对模型微调）和标准的训练/测试划分，以兼顾两种范式。

### 2.3 NLP 中的否定

否定也是语言模型通常表现低于平均水平的方面（Li and Huang, 2009; He et al., 2017; Hartmann et al., 2021; Ettinger, 2020）。NLP 中关于否定的近期工作表明，尽管语言模型在否定上有困难，模型规模扩大和改进提示技术会带来提升（McKenzie et al., 2022; Wei et al., 2022）。尽管有规模上的改进，这些工作以及其他后续工作（参见 Ravichander et al. (2022); Hossain et al. (2022)）表明，语言模型仍然难以处理否定，需要新的数据集和方法来提升表现。

由于现代 IR 模型以语言模型作为架构骨干，否定也会给 IR 系统带来问题，这一点是直观的。该问题还因如下事实而加剧：由于要实时处理大量文档，存在效率与延迟约束，IR 模型不容易扩展到更大的语言模型。

### 2.4 IR 中的否定

多年来，否定一直是信息检索方法的弱点。早期信息检索工作（Kim and Kim, 1990; Strzalkowski et al., 1995）已经表明，开箱即用时，TF-IDF（Sparck Jones, 1972）和 BM25（Robertson et al., 1995）等非神经方法难以处理否定。

据我们所知，关于神经模型中否定的已发表工作很少，甚至没有。IR 中最相近的领域是论点检索（Wachsmuth et al., 2018; Bondarenko et al., 2022），它也包含在 BEIR 数据集中，目标是为给定查询找到反驳论点。然而，这些数据集通过任务设计隐式地要求模型找出查询的反驳论点，并且特意不在查询中包含否定。因此，尽管论点检索数据集相对 MSMarco（Nguyen et al., 2016）等标准 IR 数据集包含更多否定，否定并不是文档或查询设计中的有意选择，并且与隐式的任务定义相混淆。与此相对，我们显式地提供否定，并度量否定对文档和查询两者的影响。

Opitz and Frank (2022) 的另一项近期工作把抽象意义表示（AMR）解析的特征（否定是其中许多特征之一）纳入训练，以改进 SBERT。然而，他们只针对 AMR 解析、并在 AMR 数据集上评估否定，而我们关注 IR 中的否定，并创建一个用于排序的基准。

### 2.5 对比评估

对比评估已成为一种有前景的评估技术：构建由细微差异组成、但检验关键区别的数据集（Gardner et al., 2020; Kaushik et al., 2019）。具体到 IR，这包括检验句子顺序（Rau and Kamps, 2022）、词汇结构（Nikolaev and Padó, 2023）、一般公理的构建（Völske et al., 2021）、释义、拼写错误和顺序（Penha et al., 2022）、基于大语言模型的查询与文档扩展（Weller et al., 2023a），以及事实性、正式程度、流畅性等（MacAvaney et al., 2022）。我们遵循这些工作，不在经典 IR 评估语料上评估，而是使用成对的查询和文档。

## 3 构建 NevIR

我们使用对比评估框架来测试神经 IR 中的否定。该框架在理解神经模型方面已显示出很大效用（第 2.5 节）。

### 3.1 对比文档

我们首先收集差异尽可能小、但包含否定的文档对，以 CondaQA（Ravichander et al., 2022）数据集为起点。CondaQA 由“真实场景中”包含否定的自然段落，以及这些段落经人工编辑的版本组成；编辑要么是释义、改变否定的辖域，要么是取消否定。对于我们的 IR 基准，我们排除释义编辑，因为它们不提供可供比较的不同语义。因此，这使我们能够在词汇差异最小的文档对之间比较否定的影响（统计见

<!-- 原 PDF 第 4 页 -->

表 1 与图 3）。

**表 1：** NevIR 统计。长度以词计。注意，平均长度差只考虑总长度；独特词差异的分布见图 3。

| 统计量 | 训练集 | 开发集 | 测试集 |
| --- | --- | --- | --- |
| 文档对数量 | 948 | 225 | 1383 |
| 问题 1 长度 | 10.9 | 11.1 | 11.0 |
| 问题 2 长度 | 11.2 | 11.4 | 11.4 |
| 平均长度差 | 0.95 | 1.05 | 1.01 |
| 文档 1 长度 | 112.5 | 113.0 | 113.7 |
| 文档 2 长度 | 115.6 | 116.8 | 116.8 |
| 平均长度差 | 4.39 | 4.71 | 4.16 |

### 3.2 收集对比查询

为检验 IR 模型是否正确排序文档，我们通过 Amazon Mechanical Turk 上的工作者，为这些文档收集自然语言查询。我们要求工作者为两段各写一条查询，并施加四项约束：

1. 两条查询的答案对两段而言是相同的。
2. 问题由一个文本片段作答（例如不是是/否或布尔答案）。
3. 问题包含足够信息，以便从文档集合中识别相关段落（例如包含相关实体名称，而不只是“他何时出生？”）。
4. 问题只能由两段中的一段回答（从而使另一段不相关）。

注意，布尔问题会与两篇文档都相关，因此被排除。

为帮助标注者理解任务，我们允许他们用一个小型神经交叉编码器模型（Reimers and Gurevych (2019) 的 all-mpnet-base-v2）测试自己的查询，但不作要求。标注界面见附录 A。

通过一系列初始试点 HIT，我们发现标注者通常会逐字引用段落，并使用只出现在一篇文档中的词。为防止模型利用这种浅层启发式，我们加入第 5 项约束：不允许工作者在查询中使用只出现在两篇文档之一中的任何词。注意，这是一项有效但不完美的约束（如表 2 中 TF-IDF 的 2% 表现所示），因为任何非精确字符串匹配，包括子词、复数形式等，都会通过这一校验。

我们招募 HIT 接受率高于 99%、且已完成 HIT 超过 5000 的标注者。所有标注者都先参加两个付费试做 HIT，其工作经评估后才继续。每个 HIT 约六分钟，报酬为 2.5 美元，平均时薪 15 美元。总体而言，我们有 28 名不同的标注者，每人平均标注 91 对查询。

### 3.3 数据集统计

数据集统计见表 1。问题的平均词数约为 11，文档约为 113。问题对与文档对的词长平均差分别为 1 和 4，表明每一对中的条目长度几乎相同。查询之间与文档之间独特词差异的分布见图 3。该图显示，大多数查询的差异较小，为 2 到 5 个词，尽管有些只差一个否定词，有些相差超过五个词。两篇文档之间的差异变动大得多，大约相差 5 到 10 个词。

### 3.4 人类表现

为验证该数据集对人类而言很简单，我们请三名标注者对随机抽取的 10 个测试实例执行排序任务。在全部三名标注者的结果中，所有查询都被排对，说明任务很简单。

## 4 实验设置

### 4.1 指标

在早期调查中，我们观察到 IR 模型倾向于对两条查询都把同一篇文档排在另一篇之上。这促使我们使用成对准确率，以避免模型实际上并不理解否定时分数被夸大。我们首先让 IR 模型为每条查询对两篇文档排序。然后，如果模型对两条查询都正确排序了文档（在给定带否定的查询时翻转排序），我们就认为模型正确理解了否定，该对记为正确。

### 4.2 模型

我们评估多种模型，以便

<!-- 原 PDF 第 5 页 -->

**图 3：** 每一对中，查询之间（左）或文档之间（右）不同（即独特）词数量的分布。平均长度差见表 1。横轴为不同词的数量：左图刻度为 0、5、10、15，右图刻度为 0、10、20、30、40。纵轴为计数：左图刻度为 0、100、200、300、400，右图刻度为 0、25、50、75、100、125。各柱的具体计数未以文本抽出，见原 PDF 第 5 页。

对常见的神经 IR 模型类型作全面评估。需要说明的是，尽管还有我们未使用的其他模型（以及许多不同的模型训练策略），主要的检索模型类型在这里都已覆盖。我们评估以下 IR 模型类别：

**稀疏模型。** 我们评估检索时使用词袋表示的稀疏 IR 模型。这包括 TF-IDF（此处作为基线的唯一非神经 IR 方法），以及 SPLADE v2++ 的两个变体（Formal et al., 2022, 2021; Lassance and Clinchant, 2022），即集成蒸馏与自蒸馏方法。注意，SPLADE 的其他变体不如这两种方法。我们不纳入 BM25，因为在这个很小的集合上、且文档对内部词汇高度相似时，BM25 的实现表现与 TF-IDF 相近。

**后期交互。** ColBERT（Khattab and Zaharia, 2020; Santhanam et al., 2022b）等后期交互模型把文档和查询嵌入为每个子词词元一个向量。推理时，这些模型需要在查询向量与文档向量之间计算 MaxSim 运算，以确定相似度。实验中我们使用 ColBERT v1 和 v2。[^3]

**双编码器。** 另一类常见的 IR 模型是双编码器，它把文档和查询各自嵌入为单一向量表示。推理时，相似度通过简单的点积或余弦相似度计算。由于这一类模型很流行，我们纳入了较宽的范围：在 MSMarco 和/或 Natural Questions 上训练的 SentenceTransformer（Reimers and Gurevych, 2019）模型、DPR（Karpukhin et al., 2020）、CoCondenser（Gao and Callan, 2022）以及 RocketQA（Qu et al., 2021; Ren et al., 2021）。注意，这些模型涵盖多种预训练任务、基座模型，以及硬负样本挖掘和蒸馏等复杂的训练与额外微调策略。

**交叉编码器。** 交叉编码器同时编码文档和查询，在两段文本之间计算注意力。这种表示表达能力最强，但也最耗时，对更大的模型尤其如此。我们使用多种 SentenceTransformer 交叉编码器，包括在 MSMarco 以及多种 NLI 数据集上训练的模型（Demszky et al., 2018; Williams et al., 2018; Cer et al., 2017）、RocketQAv2 交叉编码器（Qu et al., 2021; Ren et al., 2021），以及 MonoT5 交叉编码器（Nogueira et al., 2020）。注意，MonoT5 模型显著更大（3B 版本最大可达其他交叉编码器的 33 倍），也更昂贵。[^4]

**随机。** 我们纳入一个随机排序两篇文档的基线。由于每个实例有两对排序，成对准确率的期望均值为 25%（$\frac{1}{2} \times \frac{1}{2}$）。

[^3]: 我们从其代码库复现 ColBERT v1 的权重。我们不使用 PLAID（Santhanam et al., 2022a）或量化，因为每条查询的集合中只有两篇文档，因而没有效率方面的要求。

[^4]: T5 模型通常也用于生成式检索（GR）（Tay et al., 2022）；因此我们不评估 GR 方法，原因是：（1）T5 已经通过 MonoT5 得到评估；（2）已有工作表明 GR 无法扩展到标准规模的集合（Pradeep et al., 2023），实践中也不使用。

## 5 结果

### 5.1 主要结果

主要结果见表 2。可以看到，表示的表达能力越强，模型总体上表现越好。

<!-- 原 PDF 第 6 页 -->

**表 2：** 使用成对准确率的成对对比评估结果。除非另有引用，所有模型均来自 sentence-transformers（Reimers and Gurevych, 2019）。Data 表示模型训练数据的主要来源，Score 表示成对准确率（见第 4.1 节）。注意，RocketQA 的两个版本都同时包含交叉编码器和双编码器。TF-IDF 的分数在任务说明中被有意设计得很低（第 3.2 节）。

| 类型 | 数据 | 参数量 | 模型名称 | 分数 |
| --- | --- | --- | --- | --- |
| 随机 | N/A | 0 | Random | 25% |
| 稀疏 | N/A | N/A | TF-IDF (Pedregosa et al., 2011) | 2.0% |
| 稀疏 | MSMarco | 110M | SPLADEv2 ensemble-distill (Formal et al., 2022) | 8.0% |
| 稀疏 | MSMarco | 110M | SPLADEv2 self-distill (Formal et al., 2022) | 8.7% |
| 后期交互 | MSMarco | 110M | ColBERTv2 (Santhanam et al., 2022b) | 13.0% |
| 后期交互 | MSMarco | 110M | ColBERTv1 (Khattab and Zaharia, 2020) | 19.7% |
| 双编码器 | NQ | 219M | DPR (Karpukhin et al., 2020) | 6.8% |
| 双编码器 | MSMarco | 110M | msmarco-bert-base-dot-v5 | 6.9% |
| 双编码器 | MSMarco | 110M | coCondenser (Gao and Callan, 2022) | 7.7% |
| 双编码器 | MSMarco | 85M | RocketQA v2 (Ren et al., 2021) | 7.8% |
| 双编码器 | NQ | 66M | nq-distilbert-base-v1 | 8.0% |
| 双编码器 | MSMarco | 110M | all-mpnet-base-v2 | 8.1% |
| 双编码器 | MSMarco | 66M | msmarco-distilbert-cos-v5 | 8.7% |
| 双编码器 | MSMarco | 170M | RocketQA v1 (Qu et al., 2021) | 9.1% |
| 双编码器 | QA Data | 110M | multi-qa-mpnet-base-dot-v1 | 11.1% |
| 交叉编码器 | MSMarco | 85M | RocketQA v2 (Ren et al., 2021) | 22.4% |
| 交叉编码器 | STSB | 355M | stsb-roberta-large | 24.9% |
| 交叉编码器 | MSMarco | 303M | RocketQA v1 (Qu et al., 2021) | 26.3% |
| 交叉编码器 | MSMarco | 61M | MonoT5 small (Nogueira et al., 2020) | 27.7% |
| 交叉编码器 | MNLI | 184M | nli-deberta-v3-base | 30.2% |
| 交叉编码器 | QNLI | 110M | qnli-electra-base | 34.1% |
| 交叉编码器 | MSMarco | 223M | MonoT5 base (default) (Nogueira et al., 2020) | 34.9% |
| 交叉编码器 | MSMarco | 737M | MonoT5 large (Nogueira et al., 2020) | 45.8% |
| 交叉编码器 | MSMarco | 2.85B | MonoT5 3B (Nogueira et al., 2020) | 50.6% |

没有任何双编码器架构的成对准确率高于 12%，无论预训练方法（例如 CoCondenser）或对比训练数据的类型（MSMarco、NQ 等）如何；大多数模型落在 5%–10% 的区间。

在稀疏类别中，TF-IDF 的成对准确率只有 2%。由于我们不允许标注者使用只出现在其中一段中的词，这是预期之中的。[^5] 对于神经稀疏模型，所有 SPLADEv2++ 模型的表现与双编码器相近，成对准确率约为 8%。

后期交互风格的模型显著优于双编码器和稀疏模型：ColBERTv1 为 19.7%，ColBERTv2 为 13.0%。由于这类模型的性质，我们可以可视化 MaxSim 算子，以理解其表现（第 5.3 节）。

交叉编码器模型表现最好。MonoT5（默认的 “base” 版本）成对准确率为 34.9%（最大版本为 50.6%）。有趣的是，在 NLI 数据集上训练的交叉编码器总体上优于在 MSMarco 上训练的交叉编码器，原因很可能是 MSMarco 几乎不含否定，而 NLI 数据集通常含有否定。

总体而言，尽管这些模型在各种标准 IR 基准上分数很高，几乎所有模型都比随机排序更差。只有少数交叉编码器模型更好，而它们是最慢、最昂贵的一类检索模型。即便这些模型，也显著低于人类，远非理想表现。

[^5]: 之所以是 2% 而不是 0%，是因为我们的标注界面并不限制部分匹配（例如 “version” 与 “versions”、“part” 与 “parting” 等）。

<!-- 原 PDF 第 7 页 -->

**图 4：** 对模型预测的错误分析，说明模型偏好的是哪一种情形（例如对两条查询都把某一篇排在第一）：带否定的文档（绿色）、编辑后的非否定文档（橙色），或对两条查询都给出相反排序（蓝色）。表现更好的模型在预测错误时通常偏好带否定的文档，而双编码器模型的错误更加均衡。纵轴为比例，刻度 0.0、0.1、0.2、0.3、0.4、0.5、0.6、0.7。横轴模型依次为：QNLI-Electra、MonoT5-base、MonoT5-3b、NLI-DeBERTa、ColBERTv2、ColBERTv1、RocketQA v2 CE、SPLADEv2、DPR、Multi-qa-mpnet、RocketQA v2 BE。图例三项为：总是把带否定的文档排在前面；总是把非否定文档排在前面；两条查询的排序都反了。各柱高度未以文本抽出，见原 PDF 第 7 页。

### 5.2 模型规模如何影响结果？

我们注意到表 2 包含不同规模的 MonoT5。可以看到，随着模型规模增大，准确率也提高（从 MonoT5-small 的约 28% 到 MonoT5-3B 的约 51%）。这与自然语言处理社区关于模型规模的结果一致（McKenzie et al., 2022; Wei et al., 2022; Ravichander et al., 2022; Weller et al., 2023b）。

然而，与 NLP 不同，IR 通常受到更强的延迟约束。因此，MonoT5-3B 这类模型只适合重排序，不适合第一阶段检索（更多讨论见第 7 节）。

### 5.3 ColBERT 分析

由于 ColBERT 模型提供词元级向量并使用 MaxSim 算子，我们可以可视化该最大算子是否关注否定词（因篇幅所限，见附录图 9 与图 10）。我们在所有抽样实例中发现，ColBERTv1 的 MaxSim 算子忽略否定词，不会把它们选为任何查询词元的最大值。因此，在默认训练下，这是处理否定时的一个关键缺陷，并导致其表现低于随机。不过，可以微调这些表示，使否定词获得更大权重，从而让 MaxSim 正确识别它们，如第 6 节所示。

### 5.4 错误分析

我们进行错误分析，以确定对于给定的一对文档，模型偏好哪一篇。模型可以偏好（例如在两条查询中都排得最高）带否定的文档、编辑后的非否定文档，或对两条查询都预测出相反的排序。图 4 显示，在 NLI 上训练的模型（以及交叉编码器）强烈偏好带否定的文档，而双编码器模型对二者的偏好大致相当。相反排序并不常见，双编码器模型的这一比例最高（例如 RocketQA 约为 20%）。

## 6 在 NevIR 上微调

表 2 表明，在标准 IR 训练数据集上训练的模型，在 NevIR 上结果并不强。然而，标准 IR 数据集的查询中都没有多少否定（这可能是因为生产系统使用户产生了偏向，参见第 7 节）。因此，本节在 NevIR 的训练集上微调 IR 模型，以考察针对否定的训练数据如何提升表现。

我们使用非稀疏类别中表现最好的模型：SentenceTransformers 的 multi-qa-mpnet-base-dot-v1、ColBERTv1，以及 PyGaggle 的 MonoT5-base。微调分别使用 SentenceTransformers、原始 ColBERTv1 代码和原始 PyGaggle 代码。我们训练 20 个 epoch，并在每个 epoch 之后于 NevIR 测试集和 MSMarco 开发集上评估。

图 5 显示，在否定数据上微调能显著提升表现，但距离完美（以及人类的）100% 成对准确率仍有很大差距。正如预期，较大的 MonoT5 模型很快学会并随即过拟合该数据（同时很快损失

<!-- 原 PDF 第 8 页 -->

**图 5：** 在 NevIR 训练集上微调如何影响 NevIR 与 MSMarco 上的结果。上图为训练至多 20 个 epoch 期间 NevIR 测试集的成对准确率，下图为 MSMarco 开发集的 MRR@10。QNLI-electra-base 见附录 E。横轴为 Epoch，刻度 0.0、2.5、5.0、7.5、10.0、12.5、15.0、17.5、20.0。上图纵轴为成对准确率，刻度 0.2、0.4、0.6；下图纵轴为 MRR@10，刻度 0.1、0.2、0.3。图例模型为 ColBERTv1、MonoT5 base、Multi-qa-mpnet。曲线读数未以文本抽出，见原 PDF 第 8 页。

在 MSMarco 上的表现）。有趣的是，ColBERT 学习所需的时间长得多（由于 MaxSim 算子），在将近 20 个 epoch 中缓慢上升，才学到双编码器模型在不到 3 个 epoch 内就迅速学到的内容。然而，我们发现 ColBERT 在 MSMarco 上的排序分数下降幅度更小、速度也更慢（图 5 下图）。我们在附录 D 中给出 NevIR 训练前后 MaxSim 算子的可视化，说明训练前 MaxSim 算子忽略否定，训练后则学会正确地把它纳入。

## 7 讨论与启示

**对当前系统的启示。** IR 模型在 NevIR 上的表现表明，第一阶段检索器在检索时并不考虑否定。因此，要用当前模型在否定上表现良好，昂贵的交叉编码器重排序器是必要的，但并不足以取得好结果。此外，我们的分析表明，为了最好地学习否定（并显著提升表现），模型应当把否定纳入训练数据。

因此，当不需要针对否定检索的高精度时（例如某些第一阶段检索设定），当前模型可能是有效的，因为无论是否有否定，它们都会检索出词汇相似的文档。然而，若要在否定条件下做高精度检索（并且带否定与不带否定的文档都有很高的词汇重叠），昂贵的交叉编码器是当前唯一表现优于随机排序的模型。NevIR 是目前唯一用于度量并改进带否定检索的数据集。

**对当前用户的启示。** 据我们的观察，大多数用户倾向于避免在 Google Search 等生产 IR 系统中使用带否定的查询。这可能是一个自我强化的问题：用户在搜索中使用否定时得到了很差的结果，因而以后避免使用否定。例如，图 1 所示 University of Utah 文章的网页此后已经更新，目前不再包含否定词。因此，尚不清楚带否定的查询较少，究竟是因为人们真实的信息需求如此，还是因为生产系统把用户（以及内容创作者）导向了回避否定。我们希望，通过引入一个 IR 评估基准，能够帮助这类查询在未来成为可能。

## 8 结论

我们提议对神经信息检索中的否定进行基准测试，并构建了名为 NevIR 的基准来探究这一问题，标注经由 Mechanical Turk 众包。我们发现，现代 IR 模型在该任务上表现很差：交叉编码器模型最好（略高于随机表现），所有其他架构（双编码器、稀疏模型以及后期

<!-- 原 PDF 第 9 页 -->

交互）都比随机更差。我们进一步表明，只要在微调中纳入否定，就能带来显著增益，尽管要达到人类表现仍有改进空间。我们希望这一基准能激发后续工作，提升信息检索模型识别否定的能力。

## 9 局限

我们的工作给出了范围较广的 IR 模型结果（包括最常见、最流行的模型），但由于篇幅和时间，并未覆盖所有可能的 IR 模型。我们欢迎未来研究探索其他方法与模型，以提升在 NevIR 上的表现。

我们的数据集遵循以往设计对比评估数据集的工作（Kaushik et al., 2019; Penha et al., 2022; MacAvaney et al., 2022）。因此需要说明：与经典 IR 数据集可能具备的设置不同，我们的工作没有提供与查询配套的大规模文档集合（从而无法在我们所度量的精度之外再分析召回）。然而，正如大量工作所示（见第 2.5 节），对比评估能够为理解并改进神经模型提供重要洞见。我们把带否定的大规模集合构建以及召回表现分析留待未来工作。

## 致谢

OW 得到 National Science Foundation Graduate Research Fellowship Program 的支持。

## 参考文献

Mordechai Averbuch, Tom H Karson, Benjamin Ben-Ami, Oded Maimon, and Lior Rokach. 2004. 情境敏感的医学信息检索. In MEDINFO 2004, pages 282–286. IOS Press.

Alexander Bondarenko, Maik Fröbe, Johannes Kiesel, Shahbaz Syed, Timon Gurcke, Meriem Beloucif, Alexander Panchenko, Chris Biemann, Benno Stein, Henning Wachsmuth, et al. 2022. Touché 2022 综述：论点检索. In Experimental IR Meets Multilinguality, Multimodality, and Interaction: 13th International Conference of the CLEF Association, CLEF 2022, Bologna, Italy, September 5–8, 2022, Proceedings, pages 311–336. Springer.

Daniel Cer, Mona Diab, Eneko Agirre, Iñigo Lopez-Gazpio, and Lucia Specia. 2017. SemEval-2017 任务 1：面向多语言与跨语言的语义文本相似度评测. In Proceedings of the 11th International Workshop on Semantic Evaluation (SemEval-2017), pages 1–14, Vancouver, Canada. Association for Computational Linguistics.

Dorottya Demszky, Kelvin Guu, and Percy Liang. 2018. 将问答数据集转换为自然语言推断数据集. ArXiv preprint, abs/1809.02922.

Allyson Ettinger. 2020. BERT 所不能：来自一套新的语言模型心理语言学诊断的教训. Transactions of the Association for Computational Linguistics, 8:34–48.

Thibault Formal, Carlos Lassance, Benjamin Piwowarski, and Stéphane Clinchant. 2022. 从蒸馏到硬负样本采样：使稀疏神经 IR 模型更有效. In Proceedings of the 45th International ACM SIGIR Conference on Research and Development in Information Retrieval, SIGIR ’22, page 2353–2359, New York, NY, USA. Association for Computing Machinery.

Thibault Formal, Carlos Lassance, Benjamin Piwowarski, and Stéphane Clinchant. 2021. SPLADE v2：用于信息检索的稀疏词汇与扩展模型.

Luyu Gao and Jamie Callan. 2022. 面向稠密段落检索的无监督、语料感知语言模型预训练. In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 2843–2853, Dublin, Ireland. Association for Computational Linguistics.

Matt Gardner, Yoav Artzi, Victoria Basmova, Jonathan Berant, Ben Bogin, Sihao Chen, Pradeep Dasigi, Dheeru Dua, Yanai Elazar, Ananth Gottumukkala, et al. 2020. 通过对比集评估模型的局部决策边界. arXiv preprint arXiv:2004.02709.

Mareike Hartmann, Miryam de Lhoneux, Daniel Hershcovich, Yova Kementchedjhieva, Lukas Nielsen, Chen Qiu, and Anders Søgaard. 2021. 用最小对探测否定意识的多语言基准. In Proceedings of the 25th Conference on Computational Natural Language Learning, pages 244–257, Online. Association for Computational Linguistics.

Hangfeng He, Federico Fancellu, and Bonnie Webber. 2017. 用于中文否定线索检测的神经网络. In Proceedings of the Workshop Computational Semantics Beyond Events and Roles, pages 59–63, Valencia, Spain. Association for Computational Linguistics.

Md Mosharaf Hossain, Dhivya Chinnappa, and Eduardo Blanco. 2022. 自然语言理解语料库中否定的分析. In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers), pages 716–723, Dublin, Ireland. Association for Computational Linguistics.

<!-- 原 PDF 第 10 页 -->

Gautier Izacard and Edouard Grave. 2021. 借助生成模型利用段落检索进行开放域问答. In Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics: Main Volume, pages 874–880, Online. Association for Computational Linguistics.

Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, and Wen-tau Yih. 2020. 面向开放域问答的稠密段落检索. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP), pages 6769–6781, Online. Association for Computational Linguistics.

Divyansh Kaushik, Eduard Hovy, and Zachary C Lipton. 2019. 用反事实增强数据学习真正造成差异的差别. arXiv preprint arXiv:1909.12434.

Omar Khattab and Matei Zaharia. 2020. ColBERT：通过 BERT 上的上下文化后期交互进行高效且有效的段落搜索. In Proceedings of the 43rd International ACM SIGIR conference on research and development in Information Retrieval, SIGIR 2020, Virtual Event, China, July 25-30, 2020, pages 39–48. ACM.

Mi-Young Kim, Juliano Rabelo, and Randy Goebel. 2019. 成文法信息检索与蕴含. In Proceedings of the Seventeenth International Conference on Artificial Intelligence and Law, pages 283–289.

Young-Whan Kim and Jin H. Kim. 1990. 基于层次概念图的知识型信息检索模型. J. Documentation, 46:113–136.

Carlos Lassance and Stéphane Clinchant. 2022. SPLADE 模型的效率研究. In Proceedings of the 45th International ACM SIGIR Conference on Research and Development in Information Retrieval, SIGIR ’22, page 2220–2226, New York, NY, USA. Association for Computing Machinery.

Patrick S. H. Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, and Douwe Kiela. 2020. 面向知识密集型 NLP 任务的检索增强生成. In Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual.

Shoushan Li and Chu-Ren Huang. 2009. 考虑否定与对比转折的情感分类. In Proceedings of the 23rd Pacific Asia Conference on Language, Information and Computation, Volume 1, pages 307–316, Hong Kong. City University of Hong Kong.

Sean MacAvaney, Sergey Feldman, Nazli Goharian, Doug Downey, and Arman Cohan. 2022. ABNIRML：分析神经 IR 模型的行为. Transactions of the Association for Computational Linguistics, 10:224–239.

Ian McKenzie, Alexander Lyzhov, Alicia Parrish, Ameya Prabhu, Aaron Mueller, Najoung Kim, Sam Bowman, and Ethan Perez. 2022. 逆缩放奖：第一轮获奖者.

April R McQuire and Caroline M Eastman. 1998. 面向信息检索系统的自然语言查询中否定的歧义. Journal of the American Society for Information Science, 49(8):686–692.

Tri Nguyen, Mir Rosenberg, Xia Song, Jianfeng Gao, Saurabh Tiwary, Rangan Majumder, and Li Deng. 2016. MS MARCO：一个由人工生成的机器阅读理解数据集. choice, 2640:660.

Dmitry Nikolaev and Sebastian Padó. 2023. 句子 Transformer 中的表示偏差. arXiv preprint arXiv:2301.13039.

Rodrigo Nogueira, Zhiying Jiang, Ronak Pradeep, and Jimmy Lin. 2020. 用预训练序列到序列模型进行文档排序. In Findings of the Association for Computational Linguistics: EMNLP 2020, pages 708–718, Online. Association for Computational Linguistics.

Juri Opitz and Anette Frank. 2022. SBERT 研究意义表示：将句子嵌入分解为可解释的语义特征. In Proceedings of the 2nd Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics and the 12th International Joint Conference on Natural Language Processing (Volume 1: Long Papers), pages 625–638, Online only. Association for Computational Linguistics.

F. Pedregosa, G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, M. Blondel, P. Prettenhofer, R. Weiss, V. Dubourg, J. Vanderplas, A. Passos, D. Cournapeau, M. Brucher, M. Perrot, and E. Duchesnay. 2011. scikit-learn：Python 中的机器学习. Journal of Machine Learning Research, 12:2825–2830.

Gustavo Penha, Arthur Câmara, and Claudia Hauff. 2022. 用查询变体生成器评估检索流水线的稳健性. In European conference on information retrieval, pages 397–412. Springer.

Ronak Pradeep, Kai Hui, Jai Gupta, Adam D Lelkes, Honglei Zhuang, Jimmy Lin, Donald Metzler, and Vinh Q Tran. 2023. 生成式检索如何扩展到数百万段落？ arXiv preprint arXiv:2305.11841.

Yingqi Qu, Yuchen Ding, Jing Liu, Kai Liu, Ruiyang Ren, Wayne Xin Zhao, Daxiang Dong, Hua Wu, and Haifeng Wang. 2021. RocketQA：面向开放域问答稠密段落检索的优化训练方法. In Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, pages 5835–5847, Online. Association for Computational Linguistics.

<!-- 原 PDF 第 11 页 -->

David Rau and Jaap Kamps. 2022. 复杂 NLP 在用于文本排序的 Transformer 中的作用. In Proceedings of the 2022 ACM SIGIR International Conference on Theory of Information Retrieval, pages 153–160.

Abhilasha Ravichander, Matt Gardner, and Ana Marasovic. 2022. CONDAQA：用于否定推理的对比阅读理解数据集. In Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing, pages 8729–8755, Abu Dhabi, United Arab Emirates. Association for Computational Linguistics.

Nils Reimers and Iryna Gurevych. 2019. Sentence-BERT：使用孪生 BERT 网络的句子嵌入. In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP), pages 3982–3992, Hong Kong, China. Association for Computational Linguistics.

Ruiyang Ren, Yingqi Qu, Jing Liu, Wayne Xin Zhao, QiaoQiao She, Hua Wu, Haifeng Wang, and Ji-Rong Wen. 2021. RocketQAv2：稠密段落检索与段落重排序的联合训练方法. In Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, pages 2825–2835, Online and Punta Cana, Dominican Republic. Association for Computational Linguistics.

Stephen E Robertson, Steve Walker, Susan Jones, Micheline M Hancock-Beaulieu, Mike Gatford, et al. 1995. TREC-3 上的 Okapi. Nist Special Publication Sp, 109:109.

Keshav Santhanam, Omar Khattab, Christopher Potts, and Matei Zaharia. 2022a. PLAID：后期交互检索的高效引擎. In Proceedings of the 31st ACM International Conference on Information & Knowledge Management, pages 1747–1756.

Keshav Santhanam, Omar Khattab, Jon Saad-Falcon, Christopher Potts, and Matei Zaharia. 2022b. ColBERTv2：通过轻量后期交互实现有效且高效的检索. In Proceedings of the 2022 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, pages 3715–3734, Seattle, United States. Association for Computational Linguistics.

Kurt Shuster, Mojtaba Komeili, Leonard Adolphs, Stephen Roller, Arthur Szlam, and Jason Weston. 2022. 寻求知识的语言模型：面向对话与提示补全的模块化搜索与生成. In Findings of the Association for Computational Linguistics: EMNLP 2022, pages 373–393, Abu Dhabi, United Arab Emirates. Association for Computational Linguistics.

Karen Sparck Jones. 1972. 词项特异性的统计解释及其在检索中的应用. Journal of documentation, 28(1):11–21.

Tomek Strzalkowski, Jose Perez Carballo, and Mihnea Marinescu. 1995. 自然语言信息检索：TREC-3 报告. NIST SPECIAL PUBLICATION SP, pages 39–39.

Yi Tay, Vinh Tran, Mostafa Dehghani, Jianmo Ni, Dara Bahri, Harsh Mehta, Zhen Qin, Kai Hui, Zhe Zhao, Jai Gupta, et al. 2022. 作为可微搜索索引的 Transformer 记忆. Advances in Neural Information Processing Systems, 35:21831–21843.

Nandan Thakur, Nils Reimers, Andreas Rücklé, Abhishek Srivastava, and Iryna Gurevych. 2021. BEIR：信息检索模型零样本评估的异构基准. ArXiv preprint, abs/2104.08663.

Michael Völske, Alexander Bondarenko, Maik Fröbe, Benno Stein, Jaspreet Singh, Matthias Hagen, and Avishek Anand. 2021. 走向神经排序模型的公理化解释. In Proceedings of the 2021 ACM SIGIR International Conference on Theory of Information Retrieval, pages 13–22.

Henning Wachsmuth, Shahbaz Syed, and Benno Stein. 2018. 在没有事先主题知识的情况下检索最佳反驳论点. In Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 241–251, Melbourne, Australia. Association for Computational Linguistics.

Jason Wei, Yi Tay, and Quoc V Le. 2022. 逆缩放可以变成 U 形. ArXiv preprint, abs/2211.02011.

Orion Weller, Kyle Lo, David Wadden, Dawn Lawrie, Benjamin Van Durme, Arman Cohan, and Luca Soldaini. 2023a. 生成式查询扩展与文档扩展何时失败？一项跨越方法、检索器与数据集的综合研究. arXiv preprint arXiv:2309.08541.

Orion Weller, Marc Marone, Nathaniel Weir, Dawn Lawrie, Daniel Khashabi, and Benjamin Van Durme. 2023b. 用 “according to...” 提示语言模型，能改进对预训练数据的引用. arXiv preprint arXiv:2305.13252.

Adina Williams, Nikita Nangia, and Samuel Bowman. 2018. 通过推断进行句子理解的广覆盖挑战语料库. In Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long Papers), pages 1112–1122, New Orleans, Louisiana. Association for Computational Linguistics.

## 附录 A 标注界面

图 6 展示了提供给 Mechanical Turk 工作者的标注界面。

<!-- 原 PDF 第 12 页 -->

**图 6：** 两条查询之间的独特词数量。

图中为标注界面（见附录 A）。界面可见文字如下。

问题对。

段落 1：由于镍耐腐蚀，它偶尔被用作装饰性银的替代品。1859 年之后，镍在一些国家也偶尔被用作廉价铸币金属（见上文），但在 20 世纪后期，除美国和加拿大外，它被更便宜的不锈钢（即铁）合金所取代。其中 “except” 被标出。

段落 2：由于镍耐腐蚀，它偶尔被用作装饰性银的替代品。1859 年之后，镍在一些国家也偶尔被用作廉价铸币金属（见上文），但在 20 世纪后期，在整个美国、加拿大以及美洲其他地方，它被更便宜的不锈钢（即铁）合金所取代。其中相应的编辑词被标出。

不要在问题 1 中使用这些独有词：'except'

不要在问题 2 中使用这些独有词：'elsewhere'、'throughout'、'americas'

与段落 1 相关、但与段落 2 不相关的问题：20 世纪哪些国家没有用铁合金取代镍？

与段落 2 相关、但与段落 1 不相关的问题：20 世纪哪些国家用铁合金取代了镍？

**图 7：** 来自 CondaQA 数据集的编辑类型及其平均成对分数。误差棒表示 95% 置信区间。横轴为编辑类型，两类为 Scope（辖域）与 Affirmation（肯定）。纵轴为分数，刻度 0.0、0.1、0.2、0.3、0.4、0.5。柱高未以文本抽出，见原 PDF 第 12 页。

## 附录 B 文档编辑类型

我们还分析原始 CondaQA 数据集中的编辑类型，看它们是否影响成对准确率。图 7 显示，对 MonoT5-3B 模型而言，两类编辑之间没有统计差异（在 95% 置信区间下）。我们注意到其他模型与此相似，因此只给出一个模型。

## 附录 C 微调后的余弦相似度

图 8 给出不同 epoch 中每一文档对之间的余弦相似度。可以看到，表示一开始几乎相同，但随着训练继续，彼此拉开距离，方差也变大。该图使用 multi-qa-mpnet 模型绘制，其他稠密模型也显示类似结果。

## 附录 D ColBERT 分析

我们给出 ColBERTv1 模型的两张热力图：第一张使用在 MSMarco 上训练的原始模型，第二张是在 NevIR 上微调 20 个 epoch 之后。图 9 中，模型未能把任何最大词元与关键词 “rather” 关联起来，而是把 “not” 与 “usually” 关联。相比之下，在 NevIR 上训练之后，模型正确地把 “rather” 与 “not” 关联起来。

## 附录 E 在 NevIR 上训练 QNLI-electra-base 的结果

图 11 也给出了 QNLI-electra-base 的结果，它与正文中的 MonoT5 类似。我们不展示 MSMarco 上的结果，因为 QNLI-electra-base 并未在 MSMarco 上训练。

## 附录 F 检索中否定的重要性

我们在图 12 中收录了推文 https://x.com/soft/status/1449406390976409600 的图片，展示不理解否定的危险。

## 附录 G 超参数与计算资源

所有实验都在一组 V100 上运行，每个实验在

<!-- 原 PDF 第 13 页 -->

一块 V100 上不到一小时。推理时，所有模型都使用默认超参数（许多模型没有任何超参数）。ColBERT 训练使用其代码，默认学习率为 $3\times 10^{-6}$；双编码器训练使用 Sentence-Transformers，默认学习率为 $2\times 10^{-5}$。

**图 8：** 对 multi-qa-mpnet 双编码器模型微调期间，文档对内两篇文档的余弦相似度。误差棒表示一个标准差。横轴为 Epoch，刻度 0.0、2.5、5.0、7.5、10.0、12.5、15.0、17.5、20.0。纵轴为文档余弦相似度，刻度 0.0、0.2、0.4、0.6、0.8、1.0。曲线读数未以文本抽出，见原 PDF 第 13 页。

**图 9：** ColBERTv1 模型上 ColBERT 的 MaxSim 算子在一个实例上的结果。红色高亮表示与否定（或缺少否定）对应的词元，蓝色高亮表示 MaxSim 算子的最大词元。该模型把 “not” 的 MaxSim 词元预测为 “usually”，并且对关键词 “rather” 没有最大值。进一步微调可以改善这一点，见图 10。色标刻度为 0.50、0.75、1.00、1.25、1.50、1.75、2.00。热力图逐格数值未以文本抽出，见原 PDF 第 13 页。

文档词元：[CLS] [unused1] ghost ##writer ##s , technical writers , and textbooks writers are usually paid differently : rather than a set fee or a rate based on word count , they are paid based on a percentage of sales . [SEP]

查询词元：[CLS] [unused0] what types of writers are not often paid by the word ? [SEP]

文档大意：代笔作者、技术写作者和教科书写作者的付酬方式通常不同：他们不是按固定费用或按字数计费，而是按销售额的一定比例获得报酬。查询大意：哪些类型的写作者通常不按字数付酬？

<!-- 原 PDF 第 14 页 -->

**图 10：** 在 NevIR 上训练 20 个 epoch 的 ColBERTv1 模型中，ColBERT 的 MaxSim 算子在同一实例上的结果。红色高亮表示与否定（或缺少否定）对应的词元，蓝色高亮表示 MaxSim 算子的最大词元。与图 9 不同，该模型正确地把 “not” 与关键词 “rather” 关联起来。色标刻度为 0.25、0.50、0.75、1.00、1.25、1.50、1.75、2.00、2.25。热力图逐格数值未以文本抽出，见原 PDF 第 14 页。

文档词元与查询词元与图 9 相同。

**图 11：** 在 NevIR 训练集上微调 IR 模型的结果，其中包括 QNLI-electra-base。该图展示训练至多 20 个 epoch 期间 NevIR 测试集的成对准确率。横轴为 Epoch，刻度 0.0、2.5、5.0、7.5、10.0、12.5、15.0、17.5、20.0。纵轴为成对准确率，刻度 0.2、0.4、0.6。图例模型为 Multi-qa-mpnet、QNLI-Electra、ColBERTv1。曲线读数未以文本抽出，见原 PDF 第 14 页。

**图 12：** 该推文的复现，显示 Google Search 给出危及生命的建议，并且未能捕捉文章中的否定。

图中可见文字：左侧搜索结果摘录题为 “Had a seizure Now what?”（癫痫发作了，现在怎么办？），列出“按住患者或试图阻止其动作；往患者嘴里塞东西（这会造成牙齿或下颌损伤）；在发作期间实施 CPR 或其他口对口呼吸；在患者再次清醒之前给予食物或水”。链接为 https://healthcare.utah.edu › seizures，标题为 “What to Do During & After a Seizure | University of Utah Health”（癫痫发作期间与之后该怎么做 | University of Utah Health），日期为 Feb 11, 2021。右侧标题为 “Do not:”（不要：），下列出同样四条，即文章中明确说不要做的事项。

<!-- 译完 -->
