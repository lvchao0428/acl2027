# ExcluIR：排他性神经信息检索

- 原文件名：ExcluIR_arXiv2404.17288.pdf
- 原标题：ExcluIR: Exclusionary Neural Information Retrieval
- 中文标题：ExcluIR：排他性神经信息检索
- 作者：Wenhao Zhang1、Mengqi Zhang1、Shiguang Wu1、Jiahuan Pei2、Zhaochun Ren3、Maarten de Rijke4、Zhumin Chen1、Pengjie Ren1*（*通信作者；1 Shandong University, Qingdao, China；2 Centrum Wiskunde & Informatica, Amsterdam, The Netherlands；3 Leiden University, Leiden, The Netherlands；4 University of Amsterdam, Amsterdam, The Netherlands）
- 会议或 arXiv：arXiv:2404.17288v1 [cs.IR] 26 Apr 2024
- 邮箱：{zhangwenhao,shiguang.wu}@mail.sdu.edu.cn；{mengqi.zhang,chenzhumin,renpengjie}@sdu.edu.cn；jiahuan.pei@cwi.nl；z.ren@liacs.leidenuniv.nl；m.derijke@uva.nl

<!-- 原 PDF 第 1 页 -->

## 摘要

排他是人类用来表达自己不想要什么的一项重要而普遍的语言技能。然而，在信息检索社区中，关于排他性检索的研究很少。在排他性检索中，用户在查询里表达他们不想要什么。在本工作中，我们首次考察文档检索中的排他性检索场景。我们提出 ExcluIR，一套用于排他性检索的资源，由一个评估基准和一个训练集组成，以帮助检索模型理解排他性查询。评估基准包含 3,452 条高质量排他性查询，每一条都经过人工标注。训练集包含 70,293 条排他性查询，每条配有一篇正文档和一篇负文档。我们进行详细实验和分析，得到三个主要观察：（1）不同架构的现有检索模型难以有效理解排他性查询；（2）虽然整合我们的训练数据可以改善检索模型在排他性检索上的性能，与人类性能相比仍存在差距；（3）生成式检索模型在处理排他性查询上具有天然优势。为促进未来对排他性检索的研究，我们在 https://github.com/zwh-sdu/ExcluIR 分享基准和评估脚本。

## 1 引言

选择性注意（Treisman, 1964; LaBerge, 1990; Cherry, 2020）被定义为聚焦相关信息、同时忽略无关信息的能力，它在塑造用户搜索行为中扮演关键角色。这一原则源自认知心理学，不仅塑造人类对环境的感知，也把影响延伸到与信息检索系统的交互。在搜索信息时，用户可以表达排除某些信息的愿望。我们把这一现象称为排他性检索，即用户明确表示偏好排除特定信息。

排他性检索强调信息检索中对精确性和相关性的关键需求。它展示用户如何利用自己的知识和期望来寻找满足其特定需要的信息。因此，未能理解排他性查询可能构成一个潜在的严重问题。例如，如图 1 所示，想象一个用户在检索系统中搜索电影。他提出这样的查询：“2019 年还上映了哪些其他科幻电影（除了 Avengers: Endgame）？”如果检索系统不能正确处理这一排他性要求，检索结果就可能包含与用户兴趣无关的内容（例如电影 “Avengers: Endgame”），从而降低用户满意度。

**图 1 见原 PDF。** 图 1：非排他性查询与排他性查询的比较。排他性查询常常指定要排除的内容（例如 “Avengers: Endgame”），以表达用户省略某些信息的要求。在这种情况下，如果检索系统未能理解查询的排他性质（例如包含词语 “besides” 的查询），它就会产生用户不想要的检索结果。图中非排他查询为 “What are the American sci-fi action movies released in 2019?”，排他查询为 “What other sci-fi movies (besides Avengers: Endgame) were released in 2019?”。正例文档是 Alita: Battle Angel，负例倾向是 Avengers: Endgame。

<!-- 原 PDF 第 2 页 -->

关于排他性检索的研究仍然相对被忽视。早期研究主要聚焦于基于关键词的方法（Nakkouzi and Eastman, 1990; McQuire and Eastman, 1998; Harvey et al., 2003）。关键想法是构造包含否定项的布尔查询，这本质上是一种后处理策略。然而，这些方法由于依赖结构化查询而表现出局限，使它们不适合更多样、更复杂的自然语言查询。虽然近期工作探索了否定在现代检索模型中的影响（Rokach et al., 2008; Koopman et al., 2010; Weller et al., 2024），它们的焦点是理解文档内部的否定语义，而不是查询的排他性质。目前，没有评估数据集来评估检索模型在排他性检索上的能力。

为此，本文的第一项贡献是引入排他性检索的资源，即 ExcluIR。ExcluIR 包含一个评估基准，以评估检索模型在排他性检索上的能力，同时也提供一个包含排他性查询的训练数据集。该数据集基于 HotpotQA（Yang et al., 2018）构建。我们首先使用 ChatGPT【脚注 1】为两篇给定的相关文档生成一条排他性查询，要求只有一篇文档包含答案，同时明确拒绝来自另一篇文档的信息。随后，我们雇用 17 名工作者检查基准中的每个数据实例，以保证数据质量。训练集包含 70,293 条排他性查询，基准包含 3,452 条人工标注的排他性查询。该数据集可以评估检索模型在处理排他性查询时能否正确检索文档，为评估检索模型提供一个新视角。

我们的第二项贡献是考察不同架构的现有检索方法在排他性检索上的性能，包括稀疏检索（Robertson et al., 2009; Nogueira et al., 2019）、稠密检索（Karpukhin et al., 2020; Ni et al., 2022a）和生成式检索方法（Bevilacqua et al., 2022; Wang et al., 2022a）。我们进行广泛实验，并有如下三个主要观察：（1）不同架构的现有检索模型不能完全理解排他性查询的真实意图；（2）生成式检索模型在排他性检索上具有独特优势，而像 ColBERT 这样的后期交互模型（Khattab and Zaharia, 2020; Santhanam et al., 2022）在处理这类查询上有明显局限；（3）用 ExcluIR 的训练集微调检索模型可以改善排他性检索上的性能，但结果仍远不能令人满意。我们对这些观察提供深入分析。这些结论为未来研究应对排他性检索的挑战提供有价值的洞见。

【脚注 1】https://platform.openai.com/docs/models/gpt-3-5

## 2 数据集构造

如图 2 所示，ExcluIR 数据集的构造包含如下步骤：（1）最初，我们从 HotpotQA（Yang et al., 2018）抽取文档对，每个数据实例由两篇相互关联的文档组成；（2）对每个文档对，我们使用 ChatGPT 生成一条排他性查询；（3）为增强合成查询的多样性，我们进一步用 ChatGPT 改写它们；（4）最后，为保证数据集的高质量，我们建立标注指南并雇用工作者做人工校正。

### 2.1 收集文档对

我们从收集 HotpotQA（Yang et al., 2018）数据集中的文档开始。该数据集面向问答任务中的多跳推理。每个数据实例包含两篇相互关联的支持文档。模型需要理解它们之间的关联，并从中抽取信息来回答问题。我们从每个数据实例中抽取两篇相关文档，形成我们的文档对。总共收集了 74,293 个文档对。合并并去除重复后，我们得到一个包含 90,406 篇文档的文档集合。

### 2.2 生成排他性查询

为高效构造数据集，我们仔细设计一个提示，引导 ChatGPT 为每一对文档生成排他性查询（见附录 A）。为确保生成的查询同时覆盖正文档和负文档，我们设计一种两步构造策略。具体而言，我们首先指示 ChatGPT 生成一条与两篇文档都相关的查询，然后引导 ChatGPT 修订该查询，增加一个约束，以纳入拒绝来自负文档的信息这一语义。

<!-- 原 PDF 第 3 页 -->

**图 2 见原 PDF。** 图 2：ExcluIR 数据集构造过程概览。流程包括从 HotpotQA 收集文档对、合成查询生成、查询改写、标注指南、人工校正，得到 ExcluIR 基准和合成的 ExcluIR。每个实例含排他性查询、负文档和正文档。

### 2.3 改写合成查询

虽然提示已被仔细调整，生成的查询常常以有限的方式表达排他短语，例如 “excluding any information about”、“except for any information” 和 “without referencing any information about”。这些表达缺乏自然性，并偏离真实世界查询。为增加查询的多样性和自然性，我们进一步指示 ChatGPT 改写它们。然后，我们把在这一步得到的 ExcluIR 数据集划分为训练集和测试集。测试集再经人工校正以构造基准，将在下一节描述。

### 2.4 人工校正数据

为构建可靠的 ExcluIR 基准，我们雇用 17 名工作者做人工数据校正。我们首先从先前步骤得到的 74,293 个数据点中采样 4,000 个实例。每个实例包含两篇文档以及一条由 ChatGPT 生成的合成查询。我们要求工作者检查合成的排他性查询，以确保其自然性和正确性，并鼓励他们用多样的表达来表达查询的排他性质。详细要求见附录 B。为便于校正过程，我们构造一个在线校正系统。在该系统中，我们为工作者定义三种操作来校正每个数据实例：

（1）符合标准。如果合成查询已经符合标准，不必进一步修改。

（2）修改查询。如果合成查询未能符合标准，修改或改写查询以符合要求。

（3）丢弃数据。如果基于这两篇文档很难写出符合标准的查询，工作者可以选择丢弃该数据。

**图 3 见原 PDF。** 图 3：ExcluIR 中排他性查询长度的分布。

### 2.5 质量保证

我们采取一些措施来保证数据质量。第一，我们提供详细的文档指南，包括任务定义、校正过程，以及排他性查询的具体标准。第二，我们呈现多个排他性查询的例子，以帮助工作者理解任务和要求。第三，我们录制一段视频来演示整个校正过程，并强调需要特别注意的关键考虑。第四，我们采用实时反馈机制，允许工作者分享他们在校正过程中遇到的问题。我们讨论这些问题并相应提供解决方案。最后，我们随机采样每位工作者 10% 的数据进行质量检查。如果采样数据中有错误，我们将要求该工作者再次校正数据。

### 2.6 数据集统计

按照上述数据集构造过程，我们为基准得到 3,452 条人工标注条目，为训练集得到 70,293 条排他性查询。训练集和基准中排他性查询的平均词数分别为 22.37 和 21.64。为进一步考察数据的多样性，我们在图 3 中可视化排他性查询长度的分布。我们表明排他性查询的长度是多样的，反映了不同的复杂度和细节水平。

<!-- 原 PDF 第 4 页 -->

## 3 实验设定

### 3.1 用于比较的方法

为评估各种检索模型在排他性检索上的性能，我们选择三种不同架构的检索模型：稀疏检索、稠密检索和生成式检索。

稀疏检索方法使用词项匹配指标（如 TF-IDF，Robertson and Walker, 1997）计算文档的相关性分数。

- BM25（Robertson et al., 2009）是一种经典的概率检索方法，基于词项频率和文档长度的归一化。
- DocT5Query（Nogueira et al., 2019）在构建 BM25 索引之前，用一个微调过的 T5 模型生成伪查询来扩展文档（Raffel et al., 2020）。

稠密检索利用预训练语言模型（PLM）作为骨干，把查询和文档表示为稠密向量以计算相关性分数。

- DPR（Karpukhin et al., 2020）是基于双编码器架构的稠密检索模型，使用 BERT 的 [CLS] 词元表示（Kenton and Toutanova, 2019）。
- Sentence-T5（Ni et al., 2022a）使用微调过的 T5 编码器模型，把查询和文档编码为稠密向量。
- GTR（Ni et al., 2022b）与 Sentence-T5 架构相同，并在从网上收集的二十亿个问答对上预训练。
- ColBERT（Khattab and Zaharia, 2020）是一种后期交互模型，它为查询和文档中的每个词元学习嵌入，然后用 MaxSim 算子计算相关性分数。

生成式检索是一种端到端检索范式。

- GENRE（De Cao et al., 2020）通过序列到序列模型生成实体名称来检索实体，它可以通过直接生成文档标题应用到文档检索。原始 GENRE 基于 BART 作为骨干训练，我们用 T5 复现它。
- SEAL（Bevilacqua et al., 2022）通过生成文档内部的 n-gram 来检索文档。
- NCI（Wang et al., 2022a）提出一种前缀感知的权重自适应解码器架构，利用语义文档标识符以及查询生成等多种数据增强策略。

### 3.2 评估指标

对原始测试查询，我们报告常用指标：秩 N 处的 Recall（R@N，$N = 1,5,10$）和秩 N 处的 MRR（MRR@N，$N = 10$）。Recall 衡量在前 N 个结果中被检索到的相关文档比例。MRR 是第一篇相关文档的秩的倒数的均值。

在 ExcluIR 中，每条排他性查询 $q$ 有一篇正文档 $d^+$ 和一篇负文档 $d^-$。因此，$d^+$ 的秩与 $d^-$ 的秩之差可以反映检索模型理解排他性查询的能力。所以我们报告 $\Delta$R@N 和 $\Delta$MRR@N，可以表述为：

$$
\Delta \mathrm{R@}N = \mathrm{R@}N(d^+) - \mathrm{R@}N(d^-), \tag{1}
$$

$$
\Delta \mathrm{MRR@}N = \mathrm{MRR@}N(d^+) - \mathrm{MRR@}N(d^-). \tag{2}
$$

此外，我们也报告 Right Rank（RR），即 $d^+$ 排在 $d^-$ 之前的结果所占比例。随机排序时 RR 的期望值是 50%。

### 3.3 实现细节

在实验中，我们使用 Elasticsearch 在原始文档和用 DocT5Query 增强的文档上评估 BM25。我们用 bert-base-uncased 架构训练 DPR 和 ColBERT，用 t5-base 架构训练 Sentence-T5、GENRE 和 NCI，并用 BART-large 架构训练 SEAL。我们按其官方实现复现 NCI 和 SEAL，其他方法由我们自己的实现复现。对查询生成，我们利用预训练模型 DocT5Query（Nogueira et al., 2019）为每篇文档生成伪查询。对神经检索模型的训练，最大输入长度设为 256，批次大小设为 32。

<!-- 原 PDF 第 5 页 -->

## 4 结果与分析

在本节中，我们呈现六组实验结果和分析，以研究：（1）现有检索模型在 ExcluIR 上的性能（第 4.1 节）；（2）改善 ExcluIR 上性能的策略，包括扩展训练数据领域（第 4.2 节）、把我们的数据集纳入训练数据（第 4.3 节）以及增大模型规模（第 4.4 节）；（3）生成式检索在 ExcluIR 上优越性的解释（第 4.5 节）；（4）像 ColBERT 这样的后期交互模型在 ExcluIR 上受限的原因（第 4.6 节）。

### 4.1 现有方法在 ExcluIR 上表现如何？

为评估在现有数据集上训练的各种检索模型在 ExcluIR 上的性能，我们在两个著名的标准检索数据集上做实验：Natural Questions（NQ）（Kwiatkowski et al., 2019）和 HotpotQA（Yang et al., 2018）。NQ 是一个用于文档检索和问答的大规模数据集。我们使用的版本是 NQ320k，由 32 万个查询–文档对组成。HotpotQA 是一个聚焦多跳推理的问答数据集。我们以与 ExcluIR 数据集相同的方式划分原始 HotpotQA，得到 7 万的训练集和 3.5 千的测试集。

各种方法在 ExcluIR 基准和其他测试数据上的主要性能见表 1 和表 2。我们从结果中有如下观察。

第一，虽然这些方法在包括 HotpotQA 和 NQ320k 的标准测试数据上取得好性能，它们在 ExcluIR 基准上的性能不能令人满意。几乎所有模型在 RR 指标上的得分都只比随机排序高出不到 10%。尽管在 NQ320k 上训练的 Sentence-T5 和 GTR 模型取得最高的 $\Delta$R@1 / $\Delta$MRR / RR 分数，它们仍然远未达到理想性能。这归因于负文档被错误地检索并排在高位，表明这些模型未能理解查询的排他性质。

第二，稀疏检索方法在理解查询的排他性质上表现出显著局限，因此它们几乎没有处理 ExcluIR 的能力。如表 2 所示，BM25 和 DocT5Query 的 RR 分数只有 53.48% 和 53.85%，只略高于随机排序。它们的 $\Delta$R@1 和 $\Delta$MRR 分数低于大多数在 NQ320k 上训练的神经检索模型。这是因为这些方法基于查询与文档之间的词汇匹配。这一局限使它们不能聚焦于查询中的排他短语，反而导致负文档得到高相关性分数。

**表 1：在 HotpotQA 上训练、并在 HotpotQA 与 ExcluIR 上测试的模型性能。** 对 HotpotQA 的评估，我们报告 Recall@2 而不是 Recall@1，因为 HotpotQA 中每个查询有两篇支持文档。指标中的 R 即 Recall，MRR 保留英文。

| 类型 | 模型 | HotpotQA R@2 | R@5 | R@10 | MRR | ExcluIR R@1 | MRR | $\Delta$R@1 | $\Delta$MRR | RR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 稀疏 | BM25 | 67.16 | 76.65 | 80.98 | 92.47 | 49.68 | 65.17 | 7.82 | 4.66 | 53.48 |
| 稀疏 | DocT5Query | 69.19 | 77.88 | 81.65 | 94.10 | 50.98 | 67.50 | 7.85 | 3.81 | 53.85 |
| 稠密 | DPR | 55.53 | 67.44 | 73.49 | 81.73 | 49.63 | 65.79 | 7.34 | 5.01 | 54.02 |
| 稠密 | Sentence-T5 | 57.63 | 68.45 | 74.29 | 82.48 | 51.04 | 66.27 | 10.11 | 7.01 | 55.41 |
| 稠密 | GTR | 61.82 | 73.57 | 79.42 | 85.50 | 54.87 | 70.88 | 14.40 | 8.79 | 57.42 |
| 稠密 | ColBERT | 73.58 | 83.73 | 87.95 | 94.44 | 54.00 | 71.24 | 10.72 | 6.42 | 55.57 |
| 生成式 | GENRE | 48.87 | 51.67 | 53.24 | 75.25 | 48.03 | 63.22 | 4.35 | 0.13 | 52.10 |
| 生成式 | SEAL | 60.78 | 72.26 | 78.20 | 85.76 | 51.33 | 67.88 | 11.64 | 7.71 | 55.52 |
| 生成式 | NCI | 47.60 | 58.14 | 64.37 | 74.59 | 37.22 | 51.37 | 1.97 | 2.29 | 50.93 |

**表 2：在 NQ320k 上训练、并在 NQ320k 与 ExcluIR 上测试的模型性能。**

| 类型 | 方法 | NQ320k R@1 | R@5 | R@10 | MRR | ExcluIR R@1 | MRR | $\Delta$R@1 | $\Delta$MRR | RR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 稀疏 | BM25 | 37.96 | 61.24 | 68.86 | 47.86 | 49.68 | 65.17 | 7.82 | 4.66 | 53.48 |
| 稀疏 | DocT5Query | 42.63 | 66.18 | 73.38 | 52.69 | 50.98 | 67.50 | 7.85 | 3.81 | 53.85 |
| 稠密 | DPR | 54.81 | 79.50 | 85.52 | 65.39 | 48.55 | 60.50 | 16.45 | 13.49 | 58.76 |
| 稠密 | Sentence-T5 | 59.63 | 82.78 | 87.42 | 69.57 | 57.76 | 66.34 | 32.90 | 27.96 | 67.83 |
| 稠密 | GTR | 62.35 | 84.67 | 89.17 | 71.90 | 59.79 | 69.00 | 34.85 | 28.12 | 68.31 |
| 稠密 | ColBERT | 60.08 | 84.19 | 89.41 | 70.50 | 57.01 | 70.88 | 20.02 | 15.26 | 59.97 |
| 生成式 | GENRE | 56.25 | 71.21 | 74.00 | 62.80 | 31.63 | 37.63 | 11.44 | 10.15 | 58.65 |
| 生成式 | SEAL | 55.24 | 75.13 | 80.97 | 63.86 | 43.54 | 55.17 | 16.11 | 15.27 | 60.02 |
| 生成式 | NCI | 60.41 | 76.10 | 80.19 | 67.18 | 31.46 | 38.95 | 15.87 | 16.81 | 56.84 |

<!-- 原 PDF 第 6 页 -->

第三，训练数据的多样性影响模型理解排他性查询的能力。从表 1 和表 2 可见，在 NQ320k 上训练的模型在 ExcluIR 上的表现优于在 HotpotQA 上训练的模型。我们认为这是因为 NQ320k 中的查询更多样，并包含更多排他性查询。因此，增加训练数据的领域和多样性可能有益于排他性检索。我们将在第 4.2 节做进一步实验分析。

此外，我们也评估在不同数据集上训练的额外模型在 ExcluIR 上的性能。由于篇幅限制，这些结果见附录 C。

### 4.2 扩展训练数据如何影响性能？

为进一步理解训练数据对排他性检索性能的影响，我们从每一类中选择代表性模型做额外实验。我们通过把 NQ320k 数据集加入训练数据来扩展表 1 中的实验。我们考虑两种扩展训练数据的设定：“Mix” 表示把两个数据集混合后同时训练，“Seq” 表示先在 NQ320k 上训练，再在 HotpotQA 上持续训练。表 3 的结果表明，扩展训练数据领域对 ExcluIR 的影响因模型而异。具体而言，我们有如下观察。

对包括 DPR 和 Sentence-T5 在内的双编码器模型，“Seq” 策略导致 ExcluIR 上的性能改善。我们认为这是因为在 NQ320k 上的初始训练增强了模型的一般理解能力，HotpotQA 测试集上改善的性能也证明了这一点。

然而，扩展训练数据并不能帮助 ColBERT 和 SEAL 在 ExcluIR 上取得更好结果。虽然 ColBERT 在两个标准数据集上表现出有竞争力的性能，它在 ExcluIR 上的性能下降。这是因为 ColBERT 基于词元级匹配计算文档相关性分数，导致忽略查询中的排他短语，而这对象排他性检索至关重要。我们可视化 ColBERT 的相关性计算，以在第 4.6 节进一步理解其性能。至于 SEAL，生成式检索模型在泛化到新的或分布外文档上的固有局限，解释了为什么扩展训练数据不会导致 ExcluIR 上的性能改善（Lee et al., 2023; Mehta et al., 2023）。

总体而言，扩展训练数据并不能稳定地增强模型在 ExcluIR 上的性能。我们认为主要原因是训练数据中缺乏排他性查询。因此，在下一节中，我们将考察把由排他性查询组成的训练集纳入训练数据的影响。

**表 3：扩展训练数据领域之后的模型性能。** NQ+H(Mix) 表示把 NQ320k 和 HotpotQA 混合后同时训练。NQ+H(Seq) 表示先在 NQ320k 上训练，再在 HotpotQA 上持续训练。

| 模型 | 训练集 | HotpotQA R@2 | R@5 | R@10 | MRR | ExcluIR R@1 | MRR | $\Delta$R@1 | $\Delta$MRR | RR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DPR | HotpotQA | 55.53 | 67.44 | 73.49 | 81.73 | 49.63 | 65.79 | 7.34 | 5.01 | 54.02 |
| DPR | NQ+H(Mix) | 53.19 | 65.05 | 71.52 | 79.57 | 48.93 | 64.47 | 6.95 | 4.59 | 53.94 |
| DPR | NQ+H(Seq) | 56.91 | 69.02 | 74.59 | 82.74 | 50.87 | 67.12 | 8.66 | 5.99 | 54.66 |
| Sentence-T5 | HotpotQA | 57.63 | 68.45 | 74.29 | 82.48 | 51.04 | 66.27 | 10.11 | 7.01 | 55.41 |
| Sentence-T5 | NQ+H(Mix) | 54.32 | 65.67 | 72.02 | 79.56 | 51.45 | 66.58 | 11.27 | 8.71 | 56.10 |
| Sentence-T5 | NQ+H(Seq) | 58.40 | 69.05 | 74.72 | 82.66 | 52.49 | 67.82 | 12.92 | 9.44 | 56.82 |
| ColBERT | HotpotQA | 73.58 | 83.73 | 87.95 | 94.44 | 53.69 | 70.82 | 10.64 | 6.35 | 55.53 |
| ColBERT | NQ+H(Mix) | 71.54 | 82.46 | 86.40 | 94.58 | 52.78 | 69.91 | 8.86 | 5.21 | 54.49 |
| ColBERT | NQ+H(Seq) | 73.26 | 83.42 | 87.69 | 94.68 | 51.27 | 69.21 | 5.82 | 2.10 | 52.93 |
| SEAL | HotpotQA | 60.78 | 72.26 | 78.20 | 85.76 | 51.33 | 67.88 | 11.64 | 7.71 | 55.52 |
| SEAL | NQ+H(Mix) | 61.65 | 72.80 | 78.61 | 86.39 | 51.25 | 67.68 | 11.50 | 7.23 | 55.63 |
| SEAL | NQ+H(Seq) | 59.86 | 71.19 | 76.88 | 84.30 | 50.52 | 66.73 | 10.77 | 6.79 | 55.36 |

<!-- 原 PDF 第 7 页 -->

### 4.3 把我们的数据集纳入训练数据如何影响性能？

先前实验表明，在 HotpotQA 和 NQ320k 上训练的模型在 ExcluIR 上表现不能令人满意。我们认为这部分是由于训练数据中缺乏排他性查询。因此，在本节中，我们把 ExcluIR 训练集纳入训练数据，以评估其对性能的影响。从图 4 的结果，我们有三个主要观察。

第一，把 ExcluIR 训练集合并进训练数据，可以显著增强模型理解排他性查询的能力。例如，以 NQ320k 为原始数据集，SEAL 通过整合 ExcluIR 训练集，在 RR 上取得 18% 的提升（60.02% 对 78.02%），而原始测试数据上的性能只下降 1.08%（63.86% 对 62.78%）。这是因为 ExcluIR 训练集包含大量排他性查询，可以帮助检索模型更好地理解查询的排他性质。

第二，当训练数据包含排他性查询时，生成式检索方法比稠密检索方法更善于学习查询的排他性质。如图 4 所示，虽然在两个原始数据集上训练的稠密检索模型在 ExcluIR 上表现更好，ExcluIR 训练集的增强导致生成式检索模型有更大的改进，最终总体上超过稠密检索方法。平均而言，包括 GENRE、SEAL 和 NCI 在内的生成式检索模型取得 17.75% 的提升，而稠密检索模型观察到的平均提升是 4.77%。这是因为生成式检索模型在模型架构和训练目标上更适合捕捉查询与文档之间的复杂关系。我们在第 4.5 节给出更详细的分析。

第三，与第 4.2 节的结论一致，即便在 ExcluIR 上微调之后，ColBERT 也未能取得令人满意的性能。如图 4 所示，在用 ExcluIR 训练集训练的模型中，ColBERT 表现出最低性能，在 HotpotQA 加 ExcluIR 上的 RR 为 59.59%，在 NQ320k 加 ExcluIR 上为 59.71%。如第 4.2 节所述，ColBERT 使用的相关性分数计算方法不利于处理排他性查询。我们将在第 4.6 节提供更详细的分析。

**图 4 见原 PDF。** 图 4：不同训练数据设定下模型的性能。上图展示各种模型在 ExcluIR 基准上的 RR 分数，下图展示这些模型在 HotpotQA 和 NQ320k 上的性能。柱的不同颜色代表不同训练数据。完整结果见附录 D。

### 4.4 模型规模如何影响性能？

为分析模型规模对 ExcluIR 性能的影响，我们增大 DPR、sentence-t5、GENRE、NCI 的模型规模，并在不同数据集上训练它们。具体而言，对 DPR，我们使用两个变体：bert-base-uncased 和 bert-large-uncased。对 sentence-t5、GENRE 和 NCI，我们采用 t5-base 和 t5-large。

结果见表 4。我们注意到，当训练数据包含排他性查询时，增大模型规模会改善 ExcluIR 上的性能。这与 Ravichander 等人（2022）的观察一致，该工作表明更大的模型更善于理解文档中被否定陈述的含义。然而，当在两个原始数据集上训练时，增大模型规模并不总是导致 ExcluIR 上的性能改善。表 6 的结果支持这一观察。例如，monot5-base 的性能不如 monot5-large，但 stsb-roberta-large 相对于 stsb-roberta-base 的性能显著下降。这表明仅仅增大模型规模不能解决排他性检索的挑战，我们应当研究构建更多训练数据并提出新的训练策略。

<!-- 原 PDF 第 8 页 -->

**图 5 见原 PDF。** 图 5：分析摘要，展示稠密检索与生成式检索模型在处理 ExcluIR 上的差异。图中包括最大内积搜索、双编码器、文档、查询、交叉注意力、权重、排他短语，以及生成式检索模型解码器中的交叉注意力。图例包括查询词元向量、像 EXCEPT 这样的排他项向量，以及文档标识词元向量。

### 4.5 为什么生成式检索模型在 ExcluIR 上更优？

生成式检索模型在理解排他性查询上具有固有优势。我们试图从生成式模型的架构来分析和解释原因。

首先，作为比较，我们表明双编码器模型对排他性查询有表示瓶颈。当两篇文档相似、但有一些用户希望区分的差异时，很难保证查询的向量表示远离负文档、同时与正文档紧密对齐。这一表示瓶颈使模型不能正确理解查询的真实意图。我们在附录 E 中给出这一证明。

生成式检索模型采用序列到序列框架，例如 T5 或 BART，它用条件概率模型估计给定查询时生成文档标识的概率：$P(d \mid q)$。在生成文档标识时，解码器中的多个交叉注意力层可以捕捉查询中的词元级语义信息，Wu 等人（2024）也探索了这一现象。假设解码器由 $L$ 层组成，对第 $l$ 层（$0 \le l < L$），交叉注意力层由下式给出：

$$
S^{(l+1)} = \mathrm{softmax}\left(\frac{Q^{(l)} {K^{(l)}}^\top}{\sqrt{d_k}}\right) V^{(l)}, \tag{3}
$$

其中 $Q^{(l)} = W_q^{(l)} S^{(l)}$，$K^{(l)} = W_k^{(l)} H_q^{(l)}$，$V^{(l)} = W_v^{(l)} H_q^{(l)}$，并且 $H_q^{(l)} = [e_{q_1}, \cdots, e_{q_N}]$ 是编码器生成的查询词元向量，$S^{(l)} = [e_{d_1}, \cdots, e_{d_M}]$ 是第 $l$ 层文档标识词元的生成嵌入向量，$W_q^{(l)}$、$W_k^{(l)}$ 和 $W_v^{(l)}$ 是可学习的交叉注意力权重矩阵。我们可视化生成式模型中的交叉注意力来概括我们的分析。如图 5 所示，多层交叉注意力机制使模型能够密集聚焦于查询中的关键项，包括排他短语（以深绿色高亮）。因此，即便面对语义复杂的查询，生成式检索模型也能够有效捕捉查询意图。

### 4.6 为什么 ColBERT 在 ExcluIR 上表现不佳？

像 ColBERT 这样的后期交互模型难以理解查询的排他性质。从先前实验结果可见，ColBERT 在 ExcluIR 上比其他神经检索模型更差。由于 ColBERT 引入后期交互架构，它基于查询与文档之间词元级向量的匹配来计算文档相关性分数。因此，查询中的排他短语对与文档词元的匹配构成挑战。

如图 6 所示，查询中的词元 exclude 与负文档中每个词元的相关性都相对较低。这表明 ColBERT 几乎不理解查询的真实意图。我们也可以注意到 decemberists 同时出现在查询和负文档中，贡献了非常高的相关性分数，这对排他性检索是不利的。虽然查询中提到了 decemberists 乐队，查询的意图是避免检索关于这个乐队的信息。因此，

<!-- 原 PDF 第 9 页 -->

**表 4：ExcluIR 上不同模型规模的性能。** 对 DPR，base 版本是 bert-base-uncased，large 版本是 bert-large-uncased。对 sentence-t5、GENRE 和 NCI，base 版本是 t5-base，large 版本是 t5-large。↑ 表示增大模型规模改善性能，↓ 表示相反。

| 训练集 | 模型 | Base $\Delta$R@1 | $\Delta$MRR | RR | Large $\Delta$R@1 | $\Delta$MRR | RR | 方向 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HotpotQA | DPR | 7.34 | 5.01 | 54.02 | 8.00 | 6.22 | 54.25 | ↑ |
| HotpotQA | Sentence-T5 | 10.11 | 7.01 | 55.41 | 7.21 | 5.23 | 53.78 | ↓ |
| HotpotQA | GENRE | 4.35 | 0.13 | 52.10 | −1.71 | −3.09 | 49.01 | ↓ |
| HotpotQA | NCI | 1.97 | 2.29 | 50.93 | 1.05 | 1.41 | 50.64 | ↓ |
| HotpotQA 加 ExcluIR | DPR | 21.32 | 14.93 | 61.19 | 24.55 | 17.88 | 62.63 | ↑ |
| HotpotQA 加 ExcluIR | Sentence-T5 | 33.78 | 24.49 | 66.75 | 37.05 | 26.50 | 69.01 | ↑ |
| HotpotQA 加 ExcluIR | GENRE | 38.71 | 18.34 | 69.07 | 42.15 | 20.20 | 70.96 | ↑ |
| HotpotQA 加 ExcluIR | NCI | 42.29 | 38.38 | 73.75 | 43.74 | 38.56 | 73.61 | ↑ |
| NQ320k | DPR | 16.45 | 13.49 | 58.76 | 20.83 | 17.16 | 61.62 | ↑ |
| NQ320k | Sentence-T5 | 32.90 | 27.96 | 67.83 | 34.36 | 29.94 | 69.02 | ↑ |
| NQ320k | GENRE | 11.44 | 10.15 | 58.65 | 11.03 | 8.88 | 55.82 | ↓ |
| NQ320k | NCI | 15.87 | 16.81 | 56.84 | 21.27 | 22.86 | 62.54 | ↑ |
| NQ320k 加 ExcluIR | DPR | 21.52 | 16.38 | 61.00 | 25.52 | 19.15 | 63.47 | ↑ |
| NQ320k 加 ExcluIR | Sentence-T5 | 34.47 | 26.19 | 68.00 | 37.34 | 28.70 | 69.65 | ↑ |
| NQ320k 加 ExcluIR | GENRE | 41.19 | 20.31 | 70.48 | 46.04 | 23.24 | 72.86 | ↑ |
| NQ320k 加 ExcluIR | NCI | 41.13 | 39.92 | 72.97 | 43.13 | 41.86 | 74.45 | ↑ |

ColBERT 固有地缺乏理解具有复杂意图的查询的能力，限制了它在 ExcluIR 上的有效性。我们在附录 F 中呈现更多案例。

## 5 相关工作

排他性检索的早期研究主要聚焦于基于关键词的方法。这些方法通常把用户查询当作布尔运算的逻辑表达式（Nakkouzi and Eastman, 1990; Strzalkowski, 1995; McQuire and Eastman, 1998; Harvey et al., 2003）。然而，这些方法依赖显式且确定的规则，缺乏处理微妙和条件性排除的灵活性，并且不适合更现实的检索场景。此外，有一个相似的检索任务，称为论证检索（Wachsmuth et al., 2018）。该任务旨在为任何争议话题上的给定论证检索最佳反论证。但论证检索隐含地要求模型找到查询的反论证，排他意图并没有在查询中被明确表达。Wang 等人（2022b）首次在文本到视频检索（T2VR）中考察排他性检索。他们表明，现有视频检索模型在处理像 “find shots of kids sitting on the floor and not playing with the dog” 这样的查询时表现很差。据我们所知，文档检索中还没有关于排他性检索的研究。

Weller 等人（2024）的另一项近期工作引入 NevIR，一个用于评估神经信息检索系统处理否定的能力的基准。NevIR 要求检索模型对两篇只在否定上不同的文档排序，两篇文档除关键否定外在所有其他方面保持一致。类似地，Rokach 等人（2008）和 Koopman 等人（2010）考察文档内部否定语境对检索性能的影响。例如，搜索 “headache” 可能检索到包含 “the patient has no symptoms of headache” 的病历。与之不同，我们聚焦于排他性检索，研究检索模型能否理解排他性查询的意图。

## 6 结论

在本工作中，我们聚焦于一种常见但研究不足的检索场景，称为排他性检索，用户在其中明确表达他们不想获得的信息。我们向社区提供了一个新基准，名为 ExcluIR，它聚焦于明确表达用户不想获得的信息的排他性查询。

<!-- 原 PDF 第 10 页 -->

**图 6 见原 PDF。** 图 6：ColBERT 在查询与负文档之间的相关性计算可视化。热图中的每个值表示查询词元向量与负文档词元向量的点积结果。红色高亮表示查询中词元 excluding 与负文档中每个词元的相关性，粉色高亮表示相关性分数最高的词元。

我们进行了广泛实验，表明不同架构的现有检索方法在 ExcluIR 上表现很差。值得注意的是，ExcluIR 不能通过简单地增加训练数据领域或增大模型规模来解决。此外，我们的分析表明，与稀疏和稠密检索模型相比，生成式检索模型固有地更擅长理解排他性查询。我们希望本工作能启发未来对 ExcluIR 的研究。

## 局限与未来工作

本工作有如下局限。第一，虽然我们构建的训练数据可以显著改善各种检索模型在 ExcluIR 上的性能，与人类性能（RR 分数为 100%）相比仍有相当大的差距。在未来工作中，我们计划研究如何利用生成式检索（GR）的优势，以进一步改善检索模型在排他性检索上的能力。第二，在实际检索场景中，查询中的排除可以用不同方式表达。有些在单轮查询中被直接陈述，另一些则隐含在多轮查询的上下文中。例如，用户可能希望当前查询的结果不包含先前轮次检索到的内容，即便这一排他意图没有在查询中被直接表达。在本工作中，我们只考虑了前一种场景，需要进一步研究来探索更广范围的排他性检索场景。

## 伦理考虑

我们意识到 ExcluIR 研究中的潜在风险，因此有必要关注伦理问题。本研究收集的全部原始数据来自公开可用的数据集，伦理考虑已由出版方批准。在数据标注过程中，所有工作者都事先被告知研究目标。我们没有收集任何个人隐私信息，研究中使用的全部数据都按照法律和伦理标准获得。

## 参考文献

Michele Bevilacqua, Giuseppe Ottaviano, Patrick Lewis, Scott Yih, Sebastian Riedel, and Fabio Petroni. 2022. 自回归搜索引擎：生成子串作为文档标识符. Advances in Neural Information Processing Systems, 35:31668–31683.

Kendra Cherry. 2020. 我们如何用选择性注意来过滤信息并聚焦. Verywell Mind.

Nicola De Cao, Gautier Izacard, Sebastian Riedel, and Fabio Petroni. 2020. 自回归实体检索. In ICLR 2021. 原 PDF 第 11 页作者名抽取为 “N De Cao, G Izacard, S Riedel, and F Petroni”。

Valerie J Harvey, Jeanne M Baugh, Bruce A Johnston, Constance M Ruzich, Arthur J Grant, et al. 2003. 搜索与查询中否定的挑战. Review of Business Information Systems (RBIS), 7(4):63–76.

Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, and Wen-tau Yih. 2020. 面向开放域问答的稠密段落检索. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP), pages 6769–6781.

Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. 2019. BERT：面向语言理解的深度双向 Transformer 预训练. In Proceedings of NAACL-HLT, pages 4171–4186. 原 PDF 第 11 页作者行抽取为 “Jacob Devlin Ming-Wei Chang Kenton and Lee Kristina Toutanova”。

Omar Khattab and Matei Zaharia. 2020. ColBERT：经由 BERT 上的上下文化后期交互做高效有效的段落搜索. In Proceedings of the 43rd International ACM SIGIR conference on research and development in Information Retrieval, pages 39–48.

Bevan Koopman, Peter Bruza, Laurianne Sitbon, and Michael Lawley. 2010. 否定对医学数据信息检索之影响的分析. In Proceedings of 15th Australasian Document Computing Symposium, pages 89–92. School of Computer Science and IT, RMIT University.

Tom Kwiatkowski et al. 2019. Natural Questions：问答研究的一个基准. Transactions of the Association for Computational Linguistics, 7:453–466.

David L. LaBerge. 1990. 注意. Psychological Science, 1(3):156–162.

Hyunji Lee, Jaeyoung Kim, Hoyeon Chang, Hanseok Oh, Sohee Yang, Vladimir Karpukhin, Yi Lu, and Minjoon Seo. 2023. 生成式检索的非参数解码. In Findings of the Association for Computational Linguistics: ACL 2023, pages 12642–12661.

April R McQuire and Caroline M Eastman. 1998. 自然语言查询到信息检索系统中否定的歧义. Journal of the American Society for Information Science, 49(8):686–692.

Sanket Mehta, Jai Gupta, Yi Tay, Mostafa Dehghani, Vinh Tran, Jinfeng Rao, Marc Najork, Emma Strubell, and Donald Metzler. 2023. DSI++：用新文档更新 Transformer 记忆. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pages 8198–8213.

Ziad S Nakkouzi and Caroline M Eastman. 1990. 用于在信息检索系统中处理否定的查询构造. Journal of the American Society for Information Science, 41(3):171–182.

Jianmo Ni, Gustavo Hernandez Abrego, Noah Constant, Ji Ma, Keith Hall, Daniel Cer, and Yinfei Yang. 2022a. Sentence-T5：来自预训练文本到文本模型的可扩展句子编码器. In Findings of the Association for Computational Linguistics: ACL 2022, pages 1864–1874.

Jianmo Ni, Chen Qu, Jing Lu, Zhuyun Dai, Gustavo Hernandez Abrego, Ji Ma, Vincent Zhao, Yi Luan, Keith Hall, Ming-Wei Chang, et al. 2022b. 大型双编码器是可泛化的检索器. In Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing, pages 9844–9855.

Rodrigo Nogueira, Zhiying Jiang, Ronak Pradeep, and Jimmy Lin. 2020. 用预训练序列到序列模型做文档排序. In Findings of the Association for Computational Linguistics: EMNLP 2020, pages 708–718.

Rodrigo Nogueira, Jimmy Lin, and AI Epistemic. 2019. 从 doc2query 到 doctttttquery. Online preprint, 6:2.

Yingqi Qu, Yuchen Ding, Jing Liu, Kai Liu, Ruiyang Ren, Wayne Xin Zhao, Daxiang Dong, Hua Wu, and Haifeng Wang. 2021. RocketQA：面向开放域问答稠密段落检索的优化训练方法. In Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, pages 5835–5847.

Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, and Peter J Liu. 2020. 探索用统一的文本到文本 Transformer 做迁移学习的极限. The Journal of Machine Learning Research, 21(1):5485–5551.

Abhilasha Ravichander, Matt Gardner, and Ana Marasović. 2022. CondaQA：一个用于关于否定进行推理的对比阅读理解数据集. In Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing, pages 8729–8755. 原 PDF 第 11 页姓氏抽取为 “Marasovi´c”。

Nils Reimers and Iryna Gurevych. 2019. Sentence-BERT：用孪生 BERT 网络做句子嵌入. In Proceedings of EMNLP-IJCNLP, pages 3982–3992.

Ruiyang Ren, Yingqi Qu, Jing Liu, Wayne Xin Zhao, Qiaoqiao She, Hua Wu, Haifeng Wang, and Ji-Rong Wen. 2021. RocketQAv2：稠密段落检索与段落重排序的联合训练方法. In Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, pages 2825–2835.

<!-- 原 PDF 第 12 页 -->

Stephen Robertson, Hugo Zaragoza, et al. 2009. 概率相关性框架：BM25 及其延伸. Foundations and Trends® in Information Retrieval, 3(4):333–389.

Stephen E Robertson and Steve Walker. 1997. 关于只有很少相关性信息时的相关性权重. In Proceedings of the 20th annual international ACM SIGIR conference on Research and development in information retrieval, pages 16–24.

Lior Rokach, Roni Romano, and Oded Maimon. 2008. 医学叙述报告中的否定识别. Information Retrieval, 11:499–538.

Keshav Santhanam, Omar Khattab, Jon Saad-Falcon, Christopher Potts, and Matei Zaharia. 2022. ColBERTv2：经由轻量后期交互的有效且高效检索. In Proceedings of the 2022 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, pages 3715–3734.

Tomek Strzalkowski. 1995. 自然语言信息检索. Information Processing & Management, 31(3):397–417.

Anne M Treisman. 1964. 人的选择性注意. British medical bulletin.

Henning Wachsmuth, Shahbaz Syed, and Benno Stein. 2018. 在没有先验话题知识的情况下检索最佳反论证. In Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 241–251.

Yujing Wang, Yingyan Hou, Haonan Wang, Ziming Miao, Shibin Wu, Qi Chen, Yuqing Xia, Chengmin Chi, Guoshuai Zhao, Zheng Liu, et al. 2022a. 用于文档检索的神经语料索引器. Advances in Neural Information Processing Systems, 35:25600–25614.

Ziyue Wang, Aozhu Chen, Fan Hu, and Xirong Li. 2022b. 学习在视频检索中理解否定. In Proceedings of the 30th ACM International Conference on Multimedia, pages 434–443.

Orion Weller, Dawn Lawrie, and Benjamin Van Durme. 2024. NevIR：神经信息检索中的否定. In Proceedings of the 18th Conference of the European Chapter of the Association for Computational Linguistics (Volume 1: Long Papers), pages 2274–2287, St. Julian’s, Malta. Association for Computational Linguistics.

Shiguang Wu, Wenda Wei, Mengqi Zhang, Zhumin Chen, Jun Ma, Zhaochun Ren, Maarten de Rijke, and Pengjie Ren. 2024. 生成式检索作为多向量稠密检索. arXiv preprint arXiv:2404.00684.

Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William Cohen, Ruslan Salakhutdinov, and Christopher D Manning. 2018. HotpotQA：一个多样、可解释的多跳问答数据集. In Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing, pages 2369–2380.

<!-- 原 PDF 第 13 页 -->

## A 提示模板

我们在表 5 中给出用于引导 ChatGPT 为每一对文档生成并改写排他性查询的提示。

## B 人工校正的要求

在人工校正期间，为保证数据质量，我们向工作者提供如下要求。

1. 查询应当与正文档相关。
2. 查询应当包含一个排他性约束，以明确拒绝询问负文档中的信息。
3. 查询应当包含足够的信息，而不是只用一个人名来代表一篇文档。
4. 你应当用多样的表达来表达排他性约束，而不是重复使用像 excluding 这样的相同术语。

## C ExcluIR 上额外模型的实验结果

我们在表 6 中呈现更多结果，展示各种模型在 ExcluIR 上的性能。大多数模型来自 sentence-transformers（Reimers and Gurevych, 2019），RocketQA（Qu et al., 2021; Ren et al., 2021）和 monot5（Nogueira et al., 2020）除外。由于交叉编码器模型用于重排序，计算语料中全部文档的相关性分数非常耗时。因此，我们首先用 BM25 检索前 100 篇文档，然后再排序。我们发现 BM25 对正文档和负文档的 Recall@100 分别为 95.77% 和 94.74%，因此这一策略可以保证公平性。

## D 在 HotpotQA 和 NQ320k 上用 ExcluIR 训练的完整结果

表 7 和表 8 分别展示用 ExcluIR 训练集增强 HotpotQA 和 NQ320k 之后，检索模型性能的完整结果。

## E 当正负文档相似时，双编码器模型在 ExcluIR 上的局限

双编码器模型把查询和文档嵌入到高维空间以计算相关性分数。当查询和文档的语义直截了当且不重叠时，这些方法是有效的。然而，在 ExcluIR 中，排他性查询包含负文档的语义。我们表明，当正文档和负文档的向量表示在嵌入空间中接近时，双编码器模型难以区分它们。这一局限导致双编码器模型在 ExcluIR 上的瓶颈。下面是证明。

**定义 1。** 不失一般性，$A$、$B$ 可以被看作查询或文档。$q_{A,B} := f(A, B)$，其中 $f(A, B)$ 是查询 $A$ 与负查询 $B$ 的查询编码向量。$d_A := g(A)$，其中 $g(\cdot)$ 是文档编码向量函数。所有向量都归一化到 1。若存在 $\delta \in (0, 1/9)$ 使得 $\Pr(\langle x, y \rangle > 1 - \varepsilon) > 1 - \delta$，我们也定义 $x$、$y$ 为 $\varepsilon$-接近。

**假设 1。** 我们有若干假设。

- $d_A$ 与 $d_B$ 是 $\varepsilon$-接近的，这意味着 $A$ 和 $B$ 都是相关文档，但有一些用户希望区分的差异。
- $q_{A,B}$ 与 $d_A$ 是 $\varepsilon$-接近的，这意味着 $q_{A,B}$ 有好的表示来检索 $d_A$。对 $q_{B,A}$ 与 $d_B$ 类似成立。
- $\langle q_{B,A}, d_B \rangle - \langle q_{B,A}, d_A \rangle \ge 1 - \varepsilon$ 以高概率成立，这意味着 $q_{B,A}$ 偏好 $d_B$ 而不是 $d_A$。
- $\varepsilon < 3 - 2\sqrt{2}$。

**主张 1。** 我们想证明 $\langle q_{A,B}, d_B \rangle - \langle q_{A,B}, d_A \rangle > 0$ 以高概率成立。

证明：

$$
\langle q_{A,B}, d_B \rangle - \langle q_{A,B}, d_A \rangle
= \langle q_{A,B} - q_{B,A},\ d_B - d_A \rangle
+ \langle q_{B,A}, d_B \rangle - \langle q_{B,A}, d_A \rangle. \tag{4--6}
$$

具体地，

$$
\left|\langle q_{A,B} - q_{B,A},\ d_B - d_A \rangle\right|
\le \|q_{A,B} - q_{B,A}\|\,\|d_B - d_A\|
\le \sqrt{\|q_{A,B}\|^2 + \|q_{B,A}\|^2}\,\|d_B - d_A\|
= \sqrt{2}\,\sqrt{2 - 2\langle d_B, d_A \rangle}
\le 2\sqrt{\varepsilon}. \tag{7--11}
$$

因此，以概率 $1 - 3\delta$，

$$
\langle q_{A,B}, d_B \rangle - \langle q_{A,B}, d_A \rangle
\ge -2\sqrt{\varepsilon} + \langle q_{B,A}, d_B \rangle - \langle q_{B,A}, d_A \rangle
\ge -2\sqrt{\varepsilon} + 1 - \varepsilon
> 0. \tag{12--15}
$$

<!-- 原 PDF 第 14 页 -->

**表 5：查询生成与改写的提示模板。**

| 任务 | 提示模板 |
| --- | --- |
| 生成 | 将向你提供两篇文档，你需要：1. 生成一条与文档 1 和文档 2 都相关的查询；2. 修订该查询，纳入一个约束或条件，使其明确拒绝询问文档 1 中的任何信息。回复格式：Query: / Revised Query: |
| 改写 | 改写下列查询，使它更顺畅、更合理、更自然、更现实。不要回答该查询，只润色它。你应当使该查询更像真实人类查询，但不要改变该查询的语义。Query: 原始查询。Rewritten Query: |

## F ColBERT 在负文档相关性打分上的额外案例

我们也在表 7 至表 10 中呈现更多用于分析 ColBERT 的案例。可见，在计算负文档的相关性分数时，ColBERT 总是未能聚焦于像 aside from 和 other than 这样的排他短语。相反，它错误地聚焦于有词汇匹配的词，导致分数被抬高。原文此处写 “Table 7–10”，与附录 D 的表 7、表 8 编号可能冲突，按抽出的文字保留。

## G ExcluIR 数据集的案例

表 9 展示 ExcluIR 数据集的一些案例。

<!-- 原 PDF 第 15–16 页 -->

**表 6：各种模型在 ExcluIR 上的性能。** Training Data 表示模型训练数据的来源，Params 表示模型参数量。已从 `get_text` 对齐的行如下。其余交叉编码器等行以及表 7、表 8 的完整结果网格在默认抽取中被拆成竖排数字，列对齐不完整。表抽取失败，见原 PDF 第 15 页和第 16 页。

| 类型 | 训练数据 | 参数量 | 模型 | $\Delta$R@1 | $\Delta$MRR | RR |
| --- | --- | --- | --- | --- | --- | --- |
| 双编码器 | MSMarco | 218M | RocketQA v1 | 31.62 | 24.94 | 65.13 |
| 双编码器 | NQ | 218M | RocketQA v1 | 25.09 | 21.47 | 61.31 |
| 双编码器 | NQ | 218M | RocketQA v2 | 17.93 | 15.74 | 53.61 |
| 双编码器 | 多数据集 | 23M | all-MiniLM-L6-v2 | 26.41 | 19.42 | 62.09 |
| 双编码器 | 多数据集 | 33M | all-MiniLM-L12-v2 | 27.62 | 21.05 | 63.29 |
| 双编码器 | 多数据集 | 109M | all-mpnet-base-v2 | 39.32 | 32.01 | 69.04 |
| 双编码器 | 多数据集 | 82M | all-distilroberta-v1 | 37.56 | 27.63 | 67.98 |
| 双编码器 | 多数据集 | 66M | multi-qa-distilbert-cos-v1 | 25.90 | 18.42 | 61.77 |
| 双编码器 | 多数据集 | 109M | multi-qa-mpnet-base-dot-v1 | 37.80 | 29.04 | 68.41 |
| 双编码器 | 多数据集 | 23M | multi-qa-MiniLM-L6-cos-v1 | 24.11 | 17.87 | 60.97 |
| 双编码器 | 多数据集 | 278M | paraphrase-multilingual-mpnet-base-v2 | 33.72 | 27.61 | 65.85 |

<!-- 原 PDF 第 17–18 页 -->

第 17–18 页为 ColBERT 在负文档上的更多相关性热图案例（图 7 至图 10 一类可视化）。图见原 PDF。正文说明 ColBERT 未能聚焦排他短语，而错误聚焦于词汇匹配词。

<!-- 原 PDF 第 19 页 -->

**表 9：ExcluIR 数据集案例。**

案例 1。排他性查询：除了 Bob Dylan 参与为 2001 年电影 Blow 作曲配乐之外，还有谁参与了这部电影？正文档：Blow 是 2001 年美国传记犯罪片，关于美国可卡因走私者 George Jung，由 Ted Demme 执导。David McKenna 和 Nick Cassavetes 把 Bruce Porter 1993 年的书改编为剧本。它基于 George Jung、Pablo Escobar、Carlos Lehder Rivas（片中饰为 Diego Delgado）和麦德林集团的真实故事。片名来自可卡因的一个俚语。负文档：“All the Tired Horses” 是 Bob Dylan 写的一首歌，收录于 1970 年双专辑 “Self Portrait”。这首歌出现在 2001 年电影 “Blow” 中。

案例 2。排他性查询：能否推荐一部由 Paul Walker 主演、但不是圣诞主题剧情片 “Noel” 的电影？正文档：Paul William Walker IV（1973 年 9 月 12 日–2013 年 11 月 30 日）是美国演员。他从客串电视剧开始，后因 “She’s All That” 和 “Varsity Blues” 成名，并因在 “The Fast and the Furious” 中饰演 Brian O’Conner 获得国际名声，在拍摄 “Furious 7” 途中去世。他也主演 “Joy Ride”、“Timeline”、“Into the Blue”、“Eight Below” 和 “Running Scared”。负文档：Noel 是 2004 年圣诞主题剧情片，由 David Hubbard 编剧、Chazz Palminteri 执导，主演包括 Penélope Cruz、Susan Sarandon、Paul Walker、Alan Arkin、Daniel Sunjata 和未署名的 Robin Williams。在加拿大蒙特利尔拍摄。

案例 3。排他性查询：除了参加 2013 年 NFL 选秀之外，D. C. Jefferson 在 2013 年遇到了哪些重大事件？原文查询写作 “D C. What major events”。正文档：D. C. Jefferson（生于 1989 年 5 月 7 日）是美国橄榄球近端锋，目前是自由球员。他在罗格斯大学打大学橄榄球，在 2013 年 NFL 选秀第七轮第 219 顺位被亚利桑那红雀选中，并于 2013 年 11 月 4 日因涉嫌酒驾被捕后被释出。负文档：2013 年 NFL 选秀是国家橄榄球联盟特许经营选择新合格球员的第 78 届年会。选秀正式称为 “NFL Player Selection Meeting”，于 2013 年 4 月 25 日至 27 日在纽约无线电城音乐厅举行。

<!-- 译完 -->
