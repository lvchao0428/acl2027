# NevIR: Negation in Neural Information Retrieval

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`NevIR_arXiv2305.07614.pdf`。

## Abstract 摘要

否定（negation）是日常语言中的常见现象，也一直是语言模型（language models, LMs）的薄弱环节。尽管信息检索（Information Retrieval, IR）社区已把语言模型作为现代信息检索架构的骨干，关于否定如何影响神经信息检索的研究几乎没有。因此，我们围绕这一主题构建了一个直接的基准：要求信息检索模型对两篇仅在否定上不同的文档进行排序。我们表明，结果随信息检索架构类型而大幅变化：交叉编码器（cross-encoders）表现最好，其次是后期交互（late-interaction）模型，双编码器（bi-encoder）与稀疏神经架构垫底。我们发现，大多数信息检索模型（包括当前最优（state-of-the-art, SOTA）模型）并不考虑否定，其表现与随机排序相同或更差。我们还表明，尽管在包含否定的对比文档数据集上继续微调这一显而易见的做法能够提升性能（模型规模增大同样如此），机器与人类表现之间仍存在很大差距。1

1 代码与数据见 https://github.com/orionw/NevIR。

## 1 Introduction 引言

自然语言处理（natural language processing, NLP）的近期工作表明，语言模型难以理解包含否定的文本（Ravichander et al., 2022; McKenzie et al., 2022），其表现远不如人类。这一尚未解决的问题对信息检索模型具有下游影响，因为这些模型以语言模型作为其架构的起始骨干。

然而，信息检索中关于否定的工作主要集中在前神经时代（即不使用语言模型）的检索（Kim and Kim, 1990; McQuire and Eastman, 1998; Averbuch et al., 2004; Kim et al., 2019），尚无研究考察否定如何影响现代神经信息检索。在信息检索中无法理解否定，可能在高风险情境中导致严重后果。一个广为人知的案例是：Google Search 把某网站上明确说明“不该做什么”的要点逐条列出，告诉用户癫痫发作时该怎么做（图 1）。

图 1：否定是信息检索系统未能很好理解的内容。该截图显示 Google Search 因未能捕捉文章中的否定（例如 “do not ...”）而给出了致命建议。截图中可辨认的文字为：“Had a seizure Now what? Hold the person down or try to stop their movements. Put something in the person's mouth (this can cause tooth or jaw injuries) Administer CPR or other mouth-to-mouth breathing during the seizure. Give the person food or water until they are alert again.”

人们很容易想象法律、教育或政治等高风险领域中的其他严重失败情形。即便在日常使用中，神经信息检索对否定缺乏理解，也会忽略一整类用户查询，例如 “Where should I not stay in [vacation town]?”、“Who did not win an Oscar in 2023?”，或 “What information has OpenAI failed to release about GPT-4?”。

我们旨在填补文献中的这一空白，提出一个用于信息检索中否定评估的基准，称为 NevIR（Negation EValuation in Information Retrieval，读作 “never”）。NevIR 建立在既有否定研究（Ravichander et al., 2022）之上，使用 2,556 个对比文档对实例，这些文档对仅在一处关键否定上不同。随后，我们为每一对中的两篇文档众包查询标注，每条查询只与其中一篇文档相关，而与另一篇无关（图 2）。由此，我们可以检验模型在考虑否定时是否能正确排序文档。

图 2：一个实例及评估过程示例。初始文档来自 CondaQA（Ravichander et al., 2022），经 Mechanical Turk 生成查询。下半部分展示成对准确率（pairwise accuracy）的评估过程：模型必须对两条查询都正确排序。在此例中，信息检索模型的成对准确率为零，两条查询都把 Doc #1 排在 Doc #2 之上（未能考虑否定）。可辨认的文档文本如下。Doc #1：“Because it is resistant to corrosion, nickel was occasionally used as a substitute for decorative silver. Nickel was also occasionally used in some countries after 1859 as a cheap coinage metal (see above), but in the later years of the 20th century, it was replaced by cheaper stainless steel (i.e. iron) alloys, except in the United States and Canada.” Doc #2 前半相同，结尾为 “throughout the United States, Canada, and elsewhere in the Americas.” 两条查询分别为 “What countries did not replace nickel with iron alloys in the 20th century?”（对应 Doc #1）与 “What countries replaced nickel with iron alloys in the 20th century?”（对应 Doc #2）。两次排序结果均为 1 Doc #1、2 Doc #2。

我们发现，几乎所有信息检索系统都忽略否定，通常对两条查询都给两篇文档中的同一篇更高的分数。此外，当前最优模型的表现与随机排序文档对几乎相同，或差得多。我们对这些结果进行分析，表明尽管存在否定词，双编码器对两篇文档的表示几乎相同；而 ColBERT 等后期交互模型在 MaxSim 算子中忽略否定词。

我们还表明，在否定数据上继续微调信息检索模型，能在 NevIR 上带来一些增益，但仍有很大改进空间（同时还会略微损害在 MSMarco 等传统基准上的表现）。我们希望这一分析能促使学界更加关注信息检索中的否定问题，并提供一个可用于信息检索训练与评估的数据集。

## 2 Background 背景

### 2.1 Motivation 动机

信息检索是一项定义宽泛的任务：根据自然语言查询找到相关信息片段。信息检索的具体情形在语言、领域（例如法律）与目的（例如反论、列表、一般事实问答）上差异很大。值得注意的是，其中许多专门情形都会因更好地理解否定而得到改进，例如列表、反论以及领域特定语言（例如法律或医学）。

随着神经信息检索的进步，检索增强语言模型也迅速受到关注，例如 RAG（Lewis et al., 2020）、FiD（Izacard and Grave, 2021）与 SeeKeR（Shuster et al., 2022）。就在最近几个月，生成式检索已被投入生产，系统包括 Google 的 Bard、Bing Chat 与 You.com。2 这些系统把信息检索模型与大语言模型结合起来，使其能够即时查找并生成对查询的回复。因此，随着语言模型与信息检索系统日益交织并用于生产环境，理解并改进其失败情形（例如否定）对公司与用户都至关重要。

2 https://bard.google.com/、https://www.bing.com/new 与 https://you.com。

### 2.2 Neural IR 神经信息检索

自 2020 年以来，信息检索的神经模型在多数情形下普遍优于传统稀疏方法（例如 BM25）（Karpukhin et al., 2020; Khattab and Zaharia, 2020）。给定大量训练数据，这些模型用对比损失进行优化，以学习文档如何与给定查询相关。这些方法相对稀疏方法有若干优势，包括能够超越简单的词汇匹配，编码自然语言文本的语义相似度。

近期工作聚焦于神经模型在没有任何领域特定训练数据的情况下泛化到新领域的能力（例如零样本（zero-shot））。此类工作的一个突出基准是 BEIR 数据集套件（Thakur et al., 2021），它在一系列多样的信息检索数据集上评估模型的泛化。我们的工作同时提供零样本（不对模型微调）与标准的训练/测试划分，以兼顾两种范式。

### 2.3 Negation in NLP 自然语言处理中的否定

否定也是语言模型通常表现低于平均水平的领域（Li and Huang, 2009; He et al., 2017; Hartmann et al., 2021; Ettinger, 2020）。自然语言处理中关于否定的近期工作表明，尽管语言模型在否定上表现吃力，模型规模扩大与改进的提示（prompting）技术会带来提升（McKenzie et al., 2022; Wei et al., 2022）。尽管规模带来了改进，这些工作（以及其他后续工作，参见 Ravichander et al. (2022); Hossain et al. (2022)）表明，语言模型仍然难以处理否定，需要新的数据集与方法来提升表现。

由于现代信息检索模型以语言模型作为架构骨干，否定同样会给信息检索系统带来问题，这一点是直观的。这一问题因信息检索模型难以同样容易地扩展到更大的语言模型而更加严重，原因在于实时处理大量文档时的效率与延迟约束。

### 2.4 Negation in IR 信息检索中的否定

多年来，否定一直是信息检索方法的薄弱点。早期信息检索工作（Kim and Kim, 1990; Strzalkowski et al., 1995）表明，TF-IDF（Sparck Jones, 1972）与 BM25（Robertson et al., 1995）等非神经方法在开箱即用时难以处理否定。

据我们所知，关于神经模型否定问题的已发表工作很少或没有。信息检索中最相近的领域是论点检索（argument retrieval）（Wachsmuth et al., 2018; Bondarenko et al., 2022），它也包含在 BEIR 数据集中，目标是为给定查询找到反论。然而，这些数据集通过任务设计隐式地要求模型寻找查询的反论，并且明确不在查询中包含否定。因此，尽管论点检索数据集比 MSMarco（Nguyen et al., 2016）等标准信息检索数据集包含更多否定，否定并非文档或查询设计中的有意选择，并且与隐式任务定义相混淆。相比之下，我们显式地提供并度量否定对文档与查询双方的影响。

Opitz and Frank (2022) 的另一项近期工作纳入抽象意义表示（Abstract Meaning Representation, AMR）解析中的特征（否定是其中之一），以改进 SBERT 训练。然而，他们只在 AMR 解析上（并且在 AMR 数据集上）评估否定，而我们聚焦信息检索中的否定，并构建一个用于排序的基准。

### 2.5 Contrastive Evaluation 对比评估

对比评估已成为一种有前景的评估技术：构造由细微差异组成、但检验关键区分的数据集（Gardner et al., 2020; Kaushik et al., 2019）。具体到信息检索，这包括检验句子顺序（Rau and Kamps, 2022）、词汇结构（Nikolaev and Padó, 2023）、一般公理构造（Völske et al., 2021）、释义、拼写错误与顺序（Penha et al., 2022）、基于大语言模型的查询与文档扩展（Weller et al., 2023a），以及事实性、正式程度、流畅性等（MacAvaney et al., 2022）。我们遵循这些工作，不在经典信息检索评估语料上评估，而是使用成对的查询与文档。
