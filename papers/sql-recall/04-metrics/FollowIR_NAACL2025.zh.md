# FOLLOWIR：评估并教会信息检索模型遵循指令

- 原文件名：FollowIR_NAACL2025.pdf
- 原标题：FOLLOWIR: Evaluating and Teaching Information Retrieval Models to Follow Instructions
- 中文标题：FOLLOWIR：评估并教会信息检索模型遵循指令
- 作者：Orion Weller（ι）、Benjamin Chang（ι）、Sean MacAvaney（λ）、Kyle Lo（α）、Arman Cohan（γ α）、Benjamin Van Durme（ι）、Dawn Lawrie（ι）、Luca Soldaini（α）
- 单位：ι Johns Hopkins University；α Allen Institute for AI；λ University of Glasgow；γ Yale University
- 邮箱：oweller@cs.jhu.edu
- 会议：Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)，页码 11926–11942，2025 年 4 月 29 日–5 月 4 日。©2025 Association for Computational Linguistics

<!-- 原 PDF 第 1 页 -->

## 摘要

现代语言模型（Language Models, LMs）能够遵循冗长而复杂的指令，从而支持大量且多样的用户请求。尽管信息检索（Information Retrieval, IR）模型以这些语言模型作为架构骨干，但几乎没有检索模型允许用户在查询之外再提供详细指令，因而限制了它们满足复杂信息需求的能力。在本工作中，我们研究指令在 IR 系统中的使用。我们构建了 FOLLOWIR，一个用于在 IR 中遵循真实世界指令的严格评测基准。FOLLOWIR 重新利用了为专业评审员制定的详细指令（也称为叙述，narratives）来评估检索系统。具体而言，我们的基准来自为文本检索会议（Text REtrieval Conference, TREC）共享任务整理的三个文档集合。通过这一过程，我们可以借助一套新的成对评价框架，衡量 IR 模型遵循指令的程度。结果表明，现有检索模型未能正确使用指令：它们只把指令当作基本关键词，并且难以理解长文本信息。不过，我们也表明 IR 模型是可以学会遵循复杂指令的：我们的新模型 FOLLOWIR-7B 在训练集上微调之后有显著提升。¹

## 1 引言

现代语言模型经过大量调校，能够忠实遵循用户指令（Chung et al., 2022; Ouyang et al., 2022a; Rafailov et al., 2023; Wang et al., 2023b; Ivison et al., 2023），并且能够安全地这样做（Bai et al., 2022; Bianchi et al., 2024）。凭借这些能力，语言模型能够成功处理广泛的任务（Chiang et al., 2024; Liang et al., 2023; Yang et al., 2023; Jimenez et al., 2024; Zeng et al., 2023），即便并未针对这些任务显式微调。

¹ 代码、数据与模型的链接见 https://github.com/orionw/FollowIR

与更广泛的语言模型社区相比，信息检索的实践者与研究者尚未充分挖掘指令微调模型。由于语言模型能够有效估计查询与文档之间的语义相似度，它们已被采纳为神经检索架构的主要骨干（Karpukhin et al., 2020; Khattab and Zaharia, 2020; Reimers and Gurevych, 2019）。然而，这些系统中的绝大多数都被微调为只作为文本片段相似度估计器来运行（Khattab and Zaharia, 2020; Izacard et al., 2021; Nogueira and Cho, 2019; Pradeep et al., 2023; Ma et al., 2023）。超越这些临时检索（ad-hoc search）系统、改为带指令检索，将能够支持复杂的信息需求。例如，设想一位研究者希望找出必须同时具备多种属性才算相关的论文（来自给定会议、使用给定方法类别等），同时还要避开会使其不相关的条件（使用负面情感、使用某些领域的数据集等）。

近期工作已开始走向带指令的搜索，但这一主题仍然研究不足，只有少数论文涉及（Su et al., 2022; Asai et al., 2022; Muennighoff et al., 2024）。具体而言，我们发现他们使用指令的方式偏窄：指令通常很短（少于 10 个词），并且重复（每个数据集只有一条指令，例如 Su et al. (2022); Asai et al. (2022); Li and Li (2023); Xiao et al. (2023)）。此外，这些工作缺少显式衡量指令遵循的评测数据集，而是聚焦于标准的临时检索基准。

为弥补这些空白，我们引入 FOLLOWIR，它包含：（1）一个显式衡量检索模型指令遵循能力的基准；（2）包含多样且真实指令的训练数据。我们的关键直觉是，利用为 IR 系统专业标注员制定的指令，来研究遵循指令的 IR 模型的能力。这些指令被标注员用来判断给定查询下的文档相关性。幸运的是，IR 领域拥有丰富的此类数据，因为在任何构造良好的 IR 数据集中，所有查询都会创建这些指令（也称为叙述）。具体而言，我们使用为文本检索会议共享任务制定的叙述。

<!-- 原 PDF 第 2 页 -->

**图 1：** 标准检索查询与指令（或叙述）有何不同？指令包含关于何为相关的更具体细节，包含与直接相关程度较低的背景信息，并且常常用否定来规定哪些文档不相关。图中的百分比表示这些特征在 TREC 指令中出现的频率。

这些指令详尽而复杂，包含关于什么使文档相关、什么使其不相关的细微细节。因此，如果标注员可以使用这些 TREC 指令来标注文档相关性，那么遵循指令的检索模型也应该能够做到（查询与指令对的示例见图 1 与图 2）。

我们以三个经过深度判定的 TREC 集合作为评测集的基础：TREC Robust 2004（Voorhees, 2005）、TREC Common Core 2017（Allan et al., 2017）以及 TREC News 2021（Soboroff et al., 2020）。这些集合经过充分标注，以便评估检索中的召回，有数百到数千篇文档被判定为相关或不相关。我们取专业标注员所收到的指令，并对其作轻微改动，人工重新标注相关文档。于是我们得到成对的指令，可用于测试模型对改动后指令的反应：我们衡量模型是否会更新其相关文档，以匹配改动后的指令。

由于 IR 中尚无现成方法来比较成对查询，我们开发了一套新的评价框架来完成此事，衡量在同一查询、两条不同指令下文档的按名次分数变化（我们称之为 p-MRR）。FOLLOWIR 上的结果表明，当前模型通常无法在检索中遵循指令，除非它们达到 30 亿参数以上，或者并未针对检索进行训练。我们的分析表明，这些失败来自两种现象：（1）模型不习惯长指令；（2）模型把指令用于关键词搜索。

为了进一步推进能够理解指令的检索模型，我们构建了一套真实世界、由人使用过的指令训练集，并在其上微调一个模型（FOLLOWIR-7B）。结果表明，该模型在 FOLLOWIR 上无论是标准 IR 指标还是 p-MRR 都有明显提升，为未来进展提供了一个起点。

总结而言，我们的贡献如下：（1）一个用于评估检索中指令遵循的基准 FOLLOWIR，它由在三个本已高度判定的语料之上进行的人工标注构成；（2）对当前模型为何无法理解指令的分析；（3）用于教会检索模型遵循指令的训练数据，以及一个新的开源 IR 模型 FOLLOWIR-7B，它能够处理 IR 中的长指令。

## 2 相关工作

**TREC 会议。** 美国国家标准与技术研究院（United States National Institute of Science and Technology, NIST）于 1993 年创建了 TREC 组织。每年 TREC 会在给定数据集上主办许多赛道（tracks），即共享任务。这些赛道主题多样：从新闻上的标准临时检索（Soboroff et al., 2018; Soboroff, 2021），到更复杂的领域，例如法律检索（Oard et al., 2008），或检索增强生成 / 报告生成（Lawrie et al., 2024）。

<!-- 原 PDF 第 3 页 -->

**图 2：** 成对评价框架的示意图：模型先在带原始指令的查询上评估，再在带改动后指令的查询上评估。如果模型正确理解指令，它会改变哪些文档相对于该改动是相关的（右）。注意，给 TREC 标注员的真实世界指令（左）既包含关于相关性的细粒度细节，也包含否定。

图中示例（抽取文本，含省略）：

- 查询：指出哈勃望远镜自发射以来的正面成就。
- 指令：若文档表明哈勃望远镜产生了新数据、质量优于此前可得的数据，……，并且它们仅依赖哈勃，则相关。仅限于望远镜问题的文档不相关。不涉及正面成就的望远镜维修细节则不……
- 文档 1：来自美国宇宙背景探测器（Cosmic Explorer, Cobe）卫星、并带有哈勃空间望远镜想法的初生宇宙首批图像，启发了新的宇宙学理论……
- 文档 N：哈勃空间望远镜拍摄的土星巨型风暴照片显示，该风暴自九月被发现以来增长如此之多……它比地球大好几倍。
- 模型是否会随改动后的指令而改变？左侧为原始排序（文档 N、文档 1……），右侧为改动后排序（文档 1、文档 N……）。

作为这一过程的一部分，NIST 为这些集合资助标注。通常的做法是汇集来自多种检索模型的一组结果（runs），然后按名次顺序标注，直到经费用尽。为便于标注，赛道组织者为每条将发给标注员的查询提供一段叙述（或指令）——然而，IR 模型历来只收到查询。由于评估完全召回需要为每条查询标注集合中的每一篇文档（对拥有数百万文档的集合并不可行），召回误差是用事后抽样与标注来检验的。尽管并非每一对查询与文档都能被评估，查询的召回仍然很高。我们在 TREC 所做的严格评估之上继续推进，从他们的若干集合出发。

**面向语言模型的指令。** 遵循指令的语言模型因 InstructGPT（Ouyang et al., 2022a）、FLAN（Wei et al., 2022）和 T0（Sanh et al., 2022）等模型而流行。它们已成为自然语言处理社区的一大兴趣领域（Touvron et al., 2023a; Jiang et al., 2023; Groeneveld et al., 2024; Black et al., 2022）。已有大量工作评估它们能否泛化到新指令（Wang et al., 2022c; Ouyang et al., 2022b），能否在没有人工标注数据的情况下训练它们遵循指令（Wang et al., 2022b; Qin et al., 2023），以及将它们应用到各个领域（Zhao et al., 2021; Singhal et al., 2023; Shaghaghian et al., 2020）。由于 IR 社区在其流程中使用语言模型，我们希望拓宽 IR 的范围以纳入指令，使其与更广泛的 NLP 社区对齐。

**面向检索的指令。** 在检索中使用指令是一个刚起步的探索方向。Su et al. (2022) 与 Asai et al. (2022) 是最早训练检索模型在查询之外同时使用指令的工作之一。然而，这些指令通常非常短，例如 “Retrieve a Wikipedia paragraph that answers this question.”（检索一段回答该问题的维基百科段落）。近期工作把指令纳入更小的模型（Xiao et al., 2023; Chen et al., 2023, 2024），也有其他工作以 Llama（Touvron et al., 2023a; Weller et al., 2023）或 Mistral（Jiang et al., 2023）作为更大、能够使用指令的检索模型的骨干：GritLM（Muennighoff et al., 2024）训练 Mistral 同时做生成与嵌入，而 Wang et al. (2023a) 只用 Mistral 做嵌入。

尽管活动密集，这些努力并没有一个显式与指令相关的检索基准可供评估。它们转而在标准检索基准套件上评估，例如 MTEB（Muennighoff et al., 2022）和 BEIR（Thakur et al., 2021），而这些基准并不包含指令。因此，这些较新的指令检索模型手写少量指令，通常每条指令应用于整个数据集，与具体查询无关。这使得这些指令是通用的：只关注任务形式、“文档”的形式（段落、句子等）以及宽泛领域。请注意，正因为如此，当前没有任何指令包含额外背景信息或否定（Weller et al., 2024），而这两者在真实世界指令中很常见（这些差异的示例见图 1）。

在与我们同期的工作中，Oh et al. (2024) 也提出了一个数据集来评估检索模型中的指令。他们的数据集使用 MS MARCO 集合（Nguyen et al., 2016），并在若干关键方面与我们不同：

<!-- 原 PDF 第 4 页 -->

它每条查询只有一篇相关文档（例如，判定稀疏），由 GPT-4 生成并验证，聚焦于用户背景（抽取原文为 “I am a school teaching looking for ...”，即“我是一名学校教学人员，正在寻找……”），并且用同一查询上 N 条指令中的最低分来评估（衡量稳健性）。相比之下，我们使用高度判定的语料以确保能够衡量召回，使用专业生成的指令，具有经人工验证的相关性判定，提出一种新的成对评价协议，并提供用于教授指令遵循的训练数据集与模型。

## 3 构建 FOLLOWIR

我们从三个 TREC 集合派生 FOLLOWIR：TREC News 2021（源自 Washington Post v4 语料；Soboroff et al., 2020）、TREC Robust 2004（来自 Disks 4 与 5 集合中的新闻文章；Voorhees, 2005），以及 TREC Common Core 2017（来自 New York Times Annotated 语料；Allan et al., 2017）。每一集合都经过专业评审，每条查询包含数百条标注（见表 1），平均每条查询有 50–180 篇相关文档（以及多得多的不相关标注）。

这些 TREC 赛道都包含我们现在也提供给模型的、面向专业标注员的指令。尽管单独使用这些指令可以在一定程度上表明模型遵循指令的好坏，但它并不显式测试其指令遵循能力。为了在基准中更仔细地隔离这一点，我们测试模型能否对指令中的小改动作出响应。

为此，我们请两位专家标注员修改 TREC 指令。然而，若以朴素方式做这件事，就需要重新标注所有文档判定，这是一项不平凡的任务，需要巨大的标注工作量。² 我们改为要求标注员通过加入额外约束来使指令更具体，从而收窄相关性定义。这些变换会使一些原先相关的文档变为不相关，同时不会从池中引入任何新的相关文档。因此，只需要重新标注那些被原始 TREC 评审员判定为相关的文档。这使得标注变得可行：每条查询只需重新标注数十篇文档，而不是一个包含数千篇文档的集合。

² NIST 的预算为每年 100–200 万美元：trec.nist.gov/pubs/2010.economic.impact.pdf

由于成本与重叠，我们只标注原始 TREC 查询的一个子集：我们从 TREC Robust 2004 中抽样 50 条与 TREC Common Core 不重叠的查询（因为 Common Core 在一个新集合上使用了 Robust04 的 50 条查询），并从 TREC News 2021 中抽样 30 条查询。表 1 给出了已判定文档的数据集统计以及最终基准规模。我们要求标注员改动指令，使相关文档数量大致减半，从而包含相当数量的相关性判定变化。我们注意到，尽管按 NLP 标准查询数量看起来较小，但 30–50 条查询既有效（Webber et al., 2008），也是 IR 中的标准做法，因为对每条查询的许多文档做仔细标注代价高昂（见 §A）。

由于检索器质量不同，如果我们在整个集合上搜索来评估，每个模型将检索到不同数量的相关文档。然而，因为我们基于文档相关性的变化来评估指令遵循，初始检索表现差的模型在指令遵循评估中将有更少的相关性发生变化的文档。为纠正这一点，我们改为采用重排序任务：纳入所有相关文档，并用五个模型组成的池³ 来选择排名最高的不相关文档。为了能够依据合理使用法律自由分发数据，我们将文档切成 400 词的段落，重叠 200 词，并用 MaxP（Dai and Callan, 2019）选择得分最高的段落。这使我们能够分发数据，我们通过扩展 MTEB 评价框架（Muennighoff et al., 2022）来做到这一点。

### 3.1 FOLLOWIR 的评价指标

我们的基准提供两种衡量指令遵循的方式：（1）在查询与指令一起使用时的标准检索指标；（2）指令遵循的成对评价。对于（1），我们使用典型的 IR 评价指标，但把指令与查询一起使用：这些指标对 Core17/Robust04 是平均精度均值（mean average precision, MAP），对 News21 是截断在 5 的归一化折损累积增益（normalized discounted cumulative gain at 5, nDCG@5）。⁴ 对于（2），我们使用新的成对评价指标。

³ 我们使用 BM25、BGE-base、E5-base-v2、TART-Contriever 和 INSTRUCTOR-xl。

⁴ 我们对 News21 使用 nDCG@5，因为那是该 TREC 赛道使用的官方指标。

<!-- 原 PDF 第 5 页 -->

**表 1：** FOLLOWIR 评测集在标注之前（左）与之后（右）的统计。我们使用三个流行 TREC 赛道中的查询子集，以获得查询与文档上的多样性。|Q| 是查询的词长，|I| 是指令的词长。Rel. D/Q 表示集合中被标注为相关的文档数量，不含不相关标注。按照设计，FOLLOWIR 部分中被判定为相关的文档更少（因为标注为了评测而有意改变文档的相关性）。

| 数据集 | # Q | \|Q\| | \|I\| | Rel. D/Q | # Q | \|I\| | Rel. D/Q |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
|  | 标注前 |  |  |  | 标注后 |  |  |
| TREC News ’21 (Soboroff et al., 2020) | 50 | 15.3 | 40.1 | 50.1 | 32 | 46.9 | 19.2 |
| TREC Core ’17 (Allan et al., 2017) | 50 | 16.6 | 44.0 | 180.0 | 20 | 53.5 | 32.7 |
| TREC Robust ’04 (Voorhees, 2005) | 249 | 11.9 | 68.2 | 69.9 | 52 | 75.2 | 19.8 |

该指标衡量的是：遵循修改后的指令（而不是原始指令）时分数的差值。⁵

我们的新成对评价指标 p-MRR 衡量查询之间按名次的变化。在设计该指标时，我们有如下要求：它应当把原始指令的结果与新指令的结果相比较；它应当有一个标准化范围，从最差的指令遵循分数变化（即 −1）到最好的指令遵循分数（即 1），并在使用不同指令时允许“没有变化”这一选项（即 0）；最后，它应当考虑文档名次，使得从第 1 名到第 2 名的变化比从第 99 名到第 100 名的变化更突出。基于上述条件，我们对每条查询中每一篇相关性发生变化的文档使用如下方程（其中 RR 为倒数名次 reciprocal rank，R_og 为使用原始指令时该文档的名次，R_new 为新名次）：

公式抽取不完整，见原 PDF 第 5 页。原文抽取串保留如下：

```
p-MRR =



RRog
RRnew −1
if Rog > Rnew
1 −RRnew
RRog
otherwise
(1)
```

对于最终分数，我们先在给定查询内取平均，再对语料中的所有查询取平均——也就是跨查询做宏平均，以处理每条查询相关文档数量不同的情况。

### 3.2 为什么需要一个新指标？

原始 TREC 数据集并不需要正确使用指令才能被解出。nDCG 指标只表明它们在原始任务上（加上所附指令）的检索能力。然而，模型可以简单地忽略指令并得到很高的 nDCG 分数，因此这些分数并不评估指令遵循。这就是我们提出一个与模型关键词搜索能力解耦的新指标的原因。

⁵ 请注意，我们不展示在修改后指令的相关文档集合上的标准检索结果，因为标准检索分数不能在不同的查询相关性标注（qrels）之间直接比较。

## 4 评估指令遵循

本节描述我们所评估的模型、它们在 FOLLOWIR 上的结果，以及为更好理解当前模型而做的消融。

### 4.1 评估设置

我们评估多种 IR 模型（在训练中使用或不使用指令），包括参数量从 1 亿到 70 亿的神经模型。我们先在 FOLLOWIR 基准中的原始 TREC 指令上评估，再在新指令上评估，同时给出标准 IR 指标与新的成对指标 p-MRR。我们将模型分为四类：

**训练中无指令。** 这些检索模型在训练中没有见过指令，通常也不会被给予指令：Contriever（Izacard et al., 2021）、E5（Wang et al., 2022a）、MonoBERT（Nogueira et al., 2019）、MonoT5（Nogueira et al., 2020）以及 BM25（Robertson et al., 1995）。

**IR 训练中有指令。** 大多数使用指令的检索模型大致每个检索数据集收到一条指令，该指令一般定义领域（例如 “Financial”）、文档大小（句子、段落等）以及任务形式。这包括 INSTRUCTOR 模型（Su et al., 2022）、从 Contriever 训练而来的双编码器 TART 模型（Asai et al., 2022）、从 FLAN-T5 训练而来的重排序器 TART（Chung et al., 2022）、E5 Mistral-Instruct（Wang et al., 2023a）以及 GritLM（Muennighoff et al., 2024）。我们也将 BGE 模型（Xiao et al., 2023）归入此类，尽管它们对每个宽泛任务（检索、聚类等）总共只使用一条指令进行训练。

**API 模型。** 我们使用三个表现最好的 API 嵌入模型：Cohere 的 v3 English、Google 的 Gecko（Lee et al., 2024）以及 OpenAI 的 Text-Embedding-v3-Large。这些模型的训练过程大多未知——包括它们是否在指令上训练过——因此我们把它们放在单独一类。

<!-- 原 PDF 第 6 页 -->

**表 2：** 在 FOLLOWIR 上评估指令遵循。本工作提出的 p-MRR 是一个成对评价指标，衡量指令发生变化时的指令遵循，范围从 −100 到 100（越高越好）。一般而言，只有参数量超过 30 亿的模型，或者尚未在检索任务上训练过的指令微调语言模型，才会在遵循检索指令上表现出成功。

列组依次为：Robust04（MAP、p-MRR）、News21（nDCG、p-MRR）、Core17（MAP、p-MRR）、Average（Score、p-MRR）。下表数字按页内正文抽取的逐行顺序还原。

| 模型 | Robust04 MAP | Robust04 p-MRR | News21 nDCG | News21 p-MRR | Core17 MAP | Core17 p-MRR | Average Score | Average p-MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **No-Instruction IR** |  |  |  |  |  |  |  |  |
| E5-base-v2 | 13.4 | −6.7 | 20.9 | −2.0 | 14.0 | −2.9 | 16.1 | −3.9 |
| Contriever | 19.7 | −6.1 | 22.9 | −2.8 | 15.3 | −2.5 | 19.3 | −3.8 |
| MonoBERT | 21.0 | −9.4 | 25.1 | −0.8 | 18.4 | −0.2 | 21.5 | −3.5 |
| BM25 | 12.1 | −3.1 | 19.3 | −2.1 | 8.1 | −1.1 | 13.2 | −2.1 |
| MonoT5-base | 15.7 | −6.2 | 11.0 | +5.0 | 12.2 | −4.1 | 13.0 | −1.8 |
| E5-large-v2 | 17.4 | −4.2 | 24.3 | +0.9 | 17.0 | +0.1 | 19.6 | −1.1 |
| MonoT5-3B | 27.3 | +4.0 | 16.5 | +1.8 | 18.2 | +1.8 | 20.7 | +2.5 |
| **Instruction-IR** |  |  |  |  |  |  |  |  |
| TART-Contriever | 14.3 | −9.0 | 21.8 | −3.0 | 13.3 | −3.0 | 16.5 | −5.0 |
| INSTRUCTOR-base | 17.2 | −10.4 | 22.1 | −1.8 | 15.5 | −1.1 | 18.3 | −4.4 |
| E5-mistral | 23.1 | −9.6 | 27.8 | −0.9 | 18.3 | +0.1 | 23.1 | −3.5 |
| BGE-base | 16.8 | −6.5 | 20.0 | −0.1 | 14.6 | −2.7 | 17.1 | −3.1 |
| INSTRUCTOR-xl | 19.7 | −8.1 | 26.1 | −0.9 | 16.8 | +0.7 | 20.9 | −2.8 |
| BGE-large | 17.5 | −7.8 | 22.3 | +0.6 | 15.0 | +0.1 | 18.3 | −2.4 |
| GritLM-7B | 28.6 | −1.7 | 24.4 | −1.0 | 20.8 | +2.6 | 24.6 | −0.0 |
| TART-FLAN-T5-xl | 24.6 | −0.7 | 12.8 | +2.0 | 17.0 | +2.8 | 18.1 | +1.4 |
| **APIs** |  |  |  |  |  |  |  |  |
| OpenAI v3 Large | 27.2 | −5.8 | 27.2 | −2.0 | 21.6 | −0.2 | 25.3 | −2.7 |
| Cohere v3 English | 22.3 | −3.6 | 28.3 | +0.2 | 20.6 | +2.8 | 23.7 | −0.2 |
| Google Gecko | 23.3 | −2.4 | 29.5 | +3.9 | 23.2 | +5.4 | 25.3 | +2.3 |
| **Instruct LMs** |  |  |  |  |  |  |  |  |
| FLAN-T5-base | 6.4 | +5.3 | 6.1 | −0.1 | 6.5 | −3.3 | 6.3 | +0.6 |
| Llama-2-7B-chat | 6.3 | +2.0 | 1.7 | +0.2 | 5.4 | +2.8 | 4.5 | +1.7 |
| FLAN-T5-large | 14.7 | +3.9 | 8.0 | +8.9 | 11.4 | +1.3 | 11.4 | +4.7 |
| GritLM-Reranker | 9.7 | +6.1 | 10.2 | +3.4 | 9.8 | +8.6 | 9.9 | +6.0 |
| Mistral-7B-instruct | 23.2 | +12.6 | 27.2 | +4.8 | 19.7 | +13.0 | 23.4 | +10.1 |
| FollowIR-7B | 24.8 | +13.7 | 29.6 | +6.3 | 20.0 | +16.5 | 24.8 | +12.2 |

不过我们注意到，Google 的模型确实显式地用指令进行了训练，如其技术报告所述。

**指令微调语言模型。** 我们还评估了若干作为重排序器使用的指令微调语言模型，包括 FLAN-T5（Chung et al., 2022）、Llama v2（Touvron et al., 2023b）以及 Mistral-Instruct-v0.2（Jiang et al., 2023）。我们以与 MonoT5 重排序器相同的方式评估这些模型，比较 true 与 false 词元。请注意，这些模型没有在任何检索专用数据上训练。

### 4.2 FOLLOWIR 结果

表 2 给出主要结果，同时展示标准 IR 分数（MAP 或 nDCG@5）以及成对评价指标 p-MRR。

**无指令 IR 模型。** 我们看到，无指令模型在标准 IR 指标上（就 nDCG@5 与 MAP 而言）差异很大，但 p-MRR 一般为负（低至 −3.9）。唯一在平均上得分为正的非指令模型是 MonoT5-3B（p-MRR 为 +2.5）。

**指令 IR 模型。** 我们再次看到这些模型分数一般为负，例外是 GritLM（分数平均大致为零）以及 TART-FLAN-T5-xl，后者在三个数据集中的两个上略为正（平均 p-MRR 为 +1.4）。

**API 模型。** 我们看到 API 模型在标准 IR 指标上表现强劲，其中 OpenAI 与 Google 的模型总体最高。然而，Cohere 与 OpenAI 的模型在指令遵循上表现较差，分数为负（平均分别为 −0.2 与 −2.7），而 Google Gecko 分数为正（+2.3），很可能来自其指令数据集。

**指令微调语言模型。** 与前面的结果不同，所有指令微调语言模型在指令遵循上都显示正结果，尽管它们用标准 IR 指标时的表现范围最宽（从很差的分数到一些较高的分数）。我们看到这一类中表现最好的模型是 FOLLOWIR–7B，我们将在第 5 节更详细地描述它。

**总体。** 我们看到，唯一在遵循指令上显示正结果的模型，要么是参数量超过 30 亿的 IR 模型，要么是被显式训练来遵循指令的模型，

<!-- 原 PDF 第 7 页 -->

**图 3：** 从完全不使用指令，到把指令格式化为关键词、短文本或全文时的分数差。纵轴标签为 “p-MRR compared to using the query only”（相对于仅使用查询的 p-MRR）。能够正确使用指令的模型会因额外信息而获益，而大多数其他模型会随着指令变长而性能下降。图中分组为：No Instruction Training（无指令训练）、Uses Instructions in Training（训练中使用指令）、Instruct-Tuned LLMs and APIs（指令微调大语言模型与 API）。指令设置包括 Keywords（关键词）、Short Instruction（短指令）、Full Instruction（完整指令）。图中出现的模型名包括：MonoBERT、E5-base-v2、MonoT5-base、Contriever、E5-large-v2、BM25、MonoT5-3B；E5-mistral、INSTRUCTOR-b、BGE-base、TART-dual、BGE-large、INSTRUCTOR-xl、GritLM-7B、TART-FLAN；OpenAI v3、Cohere v3、Google Gecko、FLAN-T5-large、GritLM-Reranker、Mistral-7B-instruct、FollowIR-7B。柱状数值未以表格形式抽出，此处不抄录各柱高度。

（例如 FLAN-T5），且没有任何检索专用监督。这与自然语言处理社区中的工作一致：指令遵循能力随规模提升（Brown et al., 2020），并随有监督的指令微调而提升（Longpre et al., 2023）。

### 4.3 分析

为什么这么多模型在 nDCG 和 MAP 等典型 IR 指标上表现良好，却不能正确遵循指令？我们通过消融若干可能影响结果的成分来回答这个问题：（1）IR 模型是否不习惯那些不能用于简单关键词搜索的文本（即指令）；（2）它们是否不习惯更长指令的长度（因为当前检索器是在更短的输入上训练的）。

为检验这些因素，我们把仅有原始查询的结果，与额外给予模型完整指令、较短指令或指令中的关键词时的结果相比较。我们通过提示 GPT-4-Turbo-1106，从原始完整指令（对 TREC 数据）生成这些短指令与关键词；否则就使用模型作者给出的原始短指令（对 BEIR 数据）。完整提示文本见附录 H。

我们在表 3 中展示这些消融的结果：正分表示加入信息提升了模型，负分表示性能下降。我们看到一个一致趋势：在较长指令上表现差的模型，在关键词和较短指令上的表现优于完整指令。然而，能够遵循指令的模型通常会因额外信息而看到更好的结果。

这些结果表明，模型（1）把指令文本当作关键词使用（因为只用关键词时性能更高），并且（2）无法利用指令中的额外信息（因为它们通常会因这些额外信息而性能下降）。

我们还确认这些结果在 TREC 集合之外的数据集上仍然成立，并在三个 BEIR 数据集上展示结果：SciFact、NFCorpus 和 FiQA。我们在表 3 中给出原始分数（使用其论文中的短指令），以及只使用指令中的关键词时的分数变化（关键词同样由 GPT-4 抽出）。我们只展示在指令遵循上表现较差的模型的结果。

<!-- 原 PDF 第 8 页 -->

**表 3：** 对较长指令表现较差的模型在 BEIR 基准上的消融，比较其原始短指令与从这些指令中抽出的领域关键词（列表见附录 G）。OG 表示原始输入。如果模型已经学会正确使用指令，我们会看到指令模型与非指令模型的行为出现分化；然而，我们看到加入关键词与使用完整指令之间的表现相当（约在 ±1 分以内）。

| 模型 | SciFact OG | SciFact ∆w/Key. | NFCorpus OG | NFCorpus ∆w/Key. | FiQA OG | FiQA ∆w/Key. |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **No-Instruction** |  |  |  |  |  |  |
| BM25 | 67.9 | −1.7 | 32.2 | −5.1 | 23.6 | −1.6 |
| E5-base-v2 | 71.9 | −2.7 | 35.4 | −2.5 | 39.9 | −0.4 |
| Contriever | 64.9 | +0.4 | 31.7 | +0.0 | 24.5 | −3.2 |
| MonoT5-base | 73.1 | −0.6 | 35.6 | −0.9 | 41.2 | −0.3 |
| **Uses Instruction** |  |  |  |  |  |  |
| TART-Contriever | 67.6 | −0.3 | 33.4 | −5.3 | 31.8 | −0.4 |
| INSTRUCTOR-base | 57.8 | +1.0 | 31.6 | −0.4 | 39.2 | −0.1 |
| BGE-base | 73.2 | −0.5 | 35.5 | +0.0 | 40.8 | −2.3 |
| TART-FLAN-xl | 74.2 | +1.6 | 33.9 | +0.4 | 39.6 | −0.3 |
| INSTRUCTOR-xl | 62.4 | +0.2 | 36.0 | −0.6 | 46.9 | +0.8 |
| E5-Mistral | 77.1 | −5.1 | 38.8 | +0.3 | 56.7 | −6.5 |

**表 4：** 在 InstructIR 基准上的表现，使用其 “Robustness@10” 分数，即 10 条指令上 nDCG@10 的最小值。上半部分为双编码器，下半部分为重排序器。

| 模型 | Robustness@10 |
| --- | ---: |
| BM25 | 26.9 |
| TART-Contriever | 47.5 |
| RepLLaMa | 52.6 |
| E5-Mistral | 55.4 |
| Mistral-7B-instruct | 35.3 |
| FollowIR-7B | 71.5 |

我们看到，关键词与短指令的分数大体相似，大多数模型的变化大约在 ±1 分，例外是非指令遵循模型中最强的 E5-Mistral，它在某些数据集上下降更大。

**总体。** 我们在总体上（TREC 与 BEIR 数据集上）发现，模型把指令用于关键词匹配，并且不习惯可能包含较少相关词的较长指令。

## 5 教会模型遵循指令

是否有可能提升模型在遵循指令上的表现？我们表明，在一套较长指令的训练集上微调可以提供一种这样做的方法。我们首先收集训练集来教模型。我们收集所有不在 FOLLOWIR 中的任务的 TREC 叙述（即指令），共 1836 对查询与叙述。然而我们注意到，这并不为微调提供正例或负例文档。

为了获得用于训练的文档，我们提示 GPT-3.5-Turbo-1106 生成相关与不相关文档，每条查询大约生成两个相关实例与两个不相关实例。本实验的提示见附录 H。

然而，这些合成文档有噪声，并且相对于标签含有错误——为补救这一点，我们做一轮过滤，并使用表 2 中表现最好的开源模型（Mistral-7B-Instruct-v0.2），按指令为每一篇生成文档打分。然后我们根据 Mistral 是否正确预测了生成标签来过滤文档，最后平衡相关与不相关样本，每条查询只选择一篇相关文档和一篇不相关文档。我们的总量约为 1800 个训练实例，对应约 1200 个唯一的查询 / 指令对。

然后我们训练指令遵循模型 FOLLOWIR-7B：使用 Llama-Factory 框架（Hiyouga, 2023）与 LoRA（Hu et al., 2021），在我们的数据上微调 Mistral-7B-Instruct-v0.2。完整训练超参数见附录 C。

当我们在 FOLLOWIR 上评估该模型（表 2）时，发现分数持续提升。相对于原始的 Mistral-7B-Instruct-v0.2，我们的模型在标准 IR 指标上提升（相对提升 +6.0%），在指令遵循上提升（相对 +20.8%）。我们还表明这一提升在同期的 InstructIR 数据集上同样成立（表 4）：FollowIR-7B 的分数是基础 Mistral-7B 的两倍（Robustness@10 为 71.5，对比 35.3），并且是总体得分最高的模型。因此，我们可以看到，把 IR 模型训练成更好的指令遵循者是可能的。⁶

⁶ 关于以 Llama-3-8B 为基座的版本，见 §B。

<!-- 原 PDF 第 9 页 -->

## 6 结论

尽管语言模型被用作神经检索模型的骨干，大多数现有 IR 模型并不接受那些定义文档相关性的指令。此外，目前也没有现成资源来衡量检索模型遵循指令的程度。我们构建了一个新基准，显式衡量检索模型的指令遵循能力，并发现几乎所有检索模型都不遵循指令，例外是更大的模型（30 亿参数以上），或通常不用于检索的指令微调语言模型。然而，我们表明有可能提升它们的指令遵循能力，并构建、发布了一个用于教会检索模型遵循指令的训练语料。我们的新模型 FOLLOWIR-7B 在标准检索指标和指令遵循上都有提升，我们希望这将启发该主题上的未来工作。

## 7 局限性

**重排序与全量检索。** 由于我们评估指令遵循的设置需要评估那些相关性发生变化的文档，我们不能使用完整集合做检索（因为每个检索器按设计会找到不同的相关文档）。此外，由于许可限制，我们不能分发 TREC 赛道的完整语料——因此我们依据合理使用法律分发段落。不过，我们在附录 F 中给出一部分模型的全语料检索结果，并指出在“缺乏指令遵循”这一点上趋势相似。

**可能的错误。** 我们的工作建立在 TREC 文档集合与判定之上，也建立在新的标注工作之上。我们不检查 TREC 标注中的潜在错误，而我们新收集的标注也可能有小错误。尽管有这些保留，我们看到该数据集仍然为衡量指令遵循提供了有用的评估设置。

## 8 致谢

OW 得到 NSF GRFP 奖学金的支持。

## 参考文献

AI@Meta. 2024. Llama 3 模型卡.

James Allan, Donna Harman, Evangelos Kanoulas, Dan Li, Christophe Van Gysel, and Ellen M Voorhees. 2017. TREC 2017 Common Core 赛道概述. In TREC.

Akari Asai, Timo Schick, Patrick Lewis, Xilun Chen, Gautier Izacard, Sebastian Riedel, Hannaneh Hajishirzi, and Wen-tau Yih. 2022. 带指令的任务感知检索. arXiv preprint arXiv:2211.09260.

Yuntao Bai, Andy Jones, Kamal Ndousse, Amanda Askell, Anna Chen, Nova DasSarma, Dawn Drain, Stanislav Fort, Deep Ganguli, Tom Henighan, Nicholas Joseph, Saurav Kadavath, Jackson Kernion, Tom Conerly, Sheer El-Showk, Nelson Elhage, Zac Hatfield-Dodds, Danny Hernandez, Tristan Hume, Scott Johnston, Shauna Kravec, Liane Lovitt, Neel Nanda, Catherine Olsson, Dario Amodei, Tom Brown, Jack Clark, Sam McCandlish, Chris Olah, Ben Mann, and Jared Kaplan. 2022. 用人类反馈强化学习训练一个有帮助且无害的助手. Preprint, arXiv:2204.05862.

Parishad BehnamGhader, Vaibhav Adlakha, Marius Mosbach, Dzmitry Bahdanau, Nicolas Chapados, and Siva Reddy. 2024. LLM2Vec：大语言模型其实是强大的文本编码器. arXiv preprint arXiv:2404.05961.

Federico Bianchi, Mirac Suzgun, Giuseppe Attanasio, Paul Röttger, Dan Jurafsky, Tatsunori Hashimoto, and James Zou. 2024. 安全调校的 Llama：从提升遵循指令的大语言模型安全性中得到的教训. Preprint, arXiv:2309.07875.

Sid Black, Stella Biderman, Eric Hallahan, Quentin G. Anthony, Leo Gao, Laurence Golding, Horace He, Connor Leahy, Kyle McDonell, Jason Phang, Michael Martin Pieler, USVSN Sai Prashanth, Shivanshu Purohit, Laria Reynolds, Jonathan Tow, Benqi Wang, and Samuel Weinbach. 2022. GPT-NeoX-20B：一个开源自回归语言模型. ArXiv, abs/2204.06745.

Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. 2020. 语言模型是少样本学习者. Advances in Neural Information Processing Systems, 33:1877–1901.

Yinqiong Cai, Jiafeng Guo, Yixing Fan, Qingyao Ai, Ruqing Zhang, and Xueqi Cheng. 2022. 难负例还是假负例：纠正训练神经排序模型时的池化偏差. In Proceedings of the 31st ACM International Conference on Information & Knowledge Management, pages 118–127.

Haonan Chen, Zhicheng Dou, Kelong Mao, Jiongnan Liu, and Ziliang Zhao. 2024. 通过大语言模型认知数据增强来泛化对话式稠密检索. arXiv preprint arXiv:2402.07092.

Jianlv Chen, Shitao Xiao, Peitian Zhang, Kun Luo, Defu Lian, and Zheng Liu. 2023. BGE M3-Embedding：通过自知识蒸馏得到的多语言、多功能、多粒度文本嵌入. Preprint, arXiv:2309.07597.

<!-- 原 PDF 第 10 页 -->

Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al. 2021. 评估在代码上训练的大语言模型. arXiv preprint arXiv:2107.03374.

Wei-Lin Chiang, Lianmin Zheng, Ying Sheng, Anastasios Nikolas Angelopoulos, Tianle Li, Dacheng Li, Hao Zhang, Banghua Zhu, Michael Jordan, Joseph E. Gonzalez, and Ion Stoica. 2024. Chatbot Arena：一个通过人类偏好评估大语言模型的开放平台. Preprint, arXiv:2403.04132.

Hyung Won Chung, Le Hou, Shayne Longpre, Barret Zoph, Yi Tay, William Fedus, Yunxuan Li, Xuezhi Wang, Mostafa Dehghani, Siddhartha Brahma, Albert Webson, Shixiang Shane Gu, Zhuyun Dai, Mirac Suzgun, Xinyun Chen, Aakanksha Chowdhery, Alex Castro-Ros, Marie Pellat, Kevin Robinson, Dasha Valter, Sharan Narang, Gaurav Mishra, Adams Yu, Vincent Zhao, Yanping Huang, Andrew Dai, Hongkun Yu, Slav Petrov, Ed H. Chi, Jeff Dean, Jacob Devlin, Adam Roberts, Denny Zhou, Quoc V. Le, and Jason Wei. 2022. 扩展指令微调的语言模型. Preprint, arXiv:2210.11416.

Zhuyun Dai and Jamie Callan. 2019. 用上下文神经语言建模加深信息检索的文本理解. In Proceedings of the 42nd International ACM SIGIR Conference on Research and Development in Information Retrieval, pages 985–988.

Dirk Groeneveld, Iz Beltagy, Pete Walsh, Akshita Bhagia, Rodney Kinney, Oyvind Tafjord, A. Jha, Hamish Ivison, Ian Magnusson, Yizhong Wang, Shane Arora, David Atkinson, Russell Authur, Khyathi Raghavi Chandu, Arman Cohan, Jennifer Dumas, Yanai Elazar, Yuling Gu, Jack Hessel, Tushar Khot, William Merrill, Jacob Daniel Morrison, Niklas Muennighoff, Aakanksha Naik, Crystal Nam, Matthew E. Peters, Valentina Pyatkin, Abhilasha Ravichander, Dustin Schwenk, Saurabh Shah, Will Smith, Emma Strubell, Nishant Subramani, Mitchell Wortsman, Pradeep Dasigi, Nathan Lambert, Kyle Richardson, Luke Zettlemoyer, Jesse Dodge, Kyle Lo, Luca Soldaini, Noah A. Smith, and Hanna Hajishirzi. 2024. OLMo：加速语言模型的科学研究.

Hiyouga. 2023. Llama Factory. https://github.com/hiyouga/LLaMA-Factory.

Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. 2021. LoRA：大语言模型的低秩适配. arXiv preprint arXiv:2106.09685.

Hamish Ivison, Yizhong Wang, Valentina Pyatkin, Nathan Lambert, Matthew Peters, Pradeep Dasigi, Joel Jang, David Wadden, Noah A. Smith, Iz Beltagy, and Hannaneh Hajishirzi. 2023. 气候变化中的骆驼：用 Tulu 2 增强语言模型适配. Preprint, arXiv:2311.10702.

Gautier Izacard, Mathilde Caron, Lucas Hosseini, Sebastian Riedel, Piotr Bojanowski, Armand Joulin, and Edouard Grave. 2021. 用对比学习做无监督稠密信息检索. arXiv preprint arXiv:2112.09118.

Albert Qiaochu Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, Devendra Singh Chaplot, Diego de Las Casas, Florian Bressand, Gianna Lengyel, Guillaume Lample, Lucile Saulnier, Lélio Renard Lavaud, Marie-Anne Lachaux, Pierre Stock, Teven Le Scao, Thibaut Lavril, Thomas Wang, Timothée Lacroix, and William El Sayed. 2023. Mistral 7B. ArXiv, abs/2310.06825.

Carlos E Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik R Narasimhan. 2024. SWE-bench：语言模型能否解决真实世界的 GitHub 问题？ In The Twelfth International Conference on Learning Representations.

Vladimir Karpukhin, Barlas Oğuz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, and Wen-tau Yih. 2020. 面向开放域问答的稠密段落检索. arXiv preprint arXiv:2004.04906.

Omar Khattab and Matei Zaharia. 2020. ColBERT：通过 BERT 上的上下文化迟交互进行高效且有效的段落搜索. In Proceedings of the 43rd International ACM SIGIR Conference on Research and Development in Information Retrieval, pages 39–48.

Dawn Lawrie, Sean MacAvaney, James Mayfield, Paul McNamee, Douglas W. Oard, Luca Soldaini, and Eugene Yang. 2024. TREC 2023 NeuCLIR 赛道概述.

Jinhyuk Lee, Zhuyun Dai, Xiaoqi Ren, Blair Chen, Daniel Cer, Jeremy R Cole, Kai Hui, Michael Boratko, Rajvi Kapadia, Wen Ding, et al. 2024. Gecko：从大语言模型蒸馏出的通用文本嵌入. arXiv preprint arXiv:2403.20327.

Xianming Li and Jing Li. 2023. 角度优化的文本嵌入. arXiv preprint arXiv:2309.12871.

Percy Liang, Rishi Bommasani, Tony Lee, Dimitris Tsipras, Dilara Soylu, Michihiro Yasunaga, Yian Zhang, Deepak Narayanan, Yuhuai Wu, Ananya Kumar, Benjamin Newman, Binhang Yuan, Bobby Yan, Ce Zhang, Christian Cosgrove, Christopher D. Manning, Christopher Ré, Diana Acosta-Navas, Drew A. Hudson, Eric Zelikman, Esin Durmus, Faisal Ladhak, Frieda Rong, Hongyu Ren, Huaxiu Yao, Jue Wang, Keshav Santhanam, Laurel Orr, Lucia Zheng, Mert Yuksekgonul, Mirac Suzgun, Nathan Kim, Neel Guha, Niladri Chatterji, Omar Khattab, Peter Henderson, Qian Huang, Ryan Chi, Sang Michael Xie, Shibani Santurkar, Surya Ganguli, Tatsunori Hashimoto, Thomas Icard, Tianyi Zhang, Vishrav Chaudhary, William Wang, Xuechen Li, Yifan Mai, Yuhui Zhang, and Yuta Koreeda. 2023. 语言模型的整体评估. Preprint, arXiv:2211.09110.

<!-- 原 PDF 第 11 页 -->

Shayne Longpre, Le Hou, Tu Vu, Albert Webson, Hyung Won Chung, Yi Tay, Denny Zhou, Quoc V Le, Barret Zoph, Jason Wei, et al. 2023. FLAN 数据集：为有效指令微调设计数据与方法. In International Conference on Machine Learning, pages 22631–22648. PMLR.

Xueguang Ma, Liang Wang, Nan Yang, Furu Wei, and Jimmy Lin. 2023. 为多阶段文本检索微调 Llama. arXiv preprint arXiv:2310.08319.

Niklas Muennighoff, Hongjin Su, Liang Wang, Nan Yang, Furu Wei, Tao Yu, Amanpreet Singh, and Douwe Kiela. 2024. 生成式表示指令微调. arXiv preprint arXiv:2402.09906.

Niklas Muennighoff, Nouamane Tazi, Loïc Magne, and Nils Reimers. 2022. MTEB：大规模文本嵌入基准. arXiv preprint arXiv:2210.07316.

Tri Nguyen, Mir Rosenberg, Xia Song, Jianfeng Gao, Saurabh Tiwary, Rangan Majumder, and Li Deng. 2016. MS MARCO：一个由人生成的机器阅读理解数据集. CoRR, abs/1611.09268.

Ansong Ni, Matt Gardner, and Pradeep Dasigi. 2021. 用检索边缘化缓解多文档问答中的假负例上下文. arXiv preprint arXiv:2103.12235.

Rodrigo Nogueira and Kyunghyun Cho. 2019. 用 BERT 做段落重排序. arXiv preprint arXiv:1901.04085.

Rodrigo Nogueira, Zhiying Jiang, and Jimmy Lin. 2020. 用预训练序列到序列模型做文档排序. arXiv preprint arXiv:2003.06713.

Rodrigo Nogueira, Wei Yang, Kyunghyun Cho, and Jimmy Lin. 2019. 用 BERT 做多阶段文档排序. arXiv preprint arXiv:1910.14424.

Douglas W Oard, Björn Hedin, Stephen Tomlinson, and Jason R Baron. 2008. TREC 2008 法律赛道概述. In TREC, pages 500–277.

Hanseok Oh, Hyunji Lee, Seonghyeon Ye, Haebin Shin, Hansol Jang, Changwook Jun, and Minjoon Seo. 2024. InstructIR：信息检索模型指令遵循基准. arXiv preprint arXiv:2402.14334.

Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul F Christiano, Jan Leike, and Ryan Lowe. 2022a. 用人类反馈训练语言模型遵循指令. In Advances in Neural Information Processing Systems, volume 35, pages 27730–27744. Curran Associates, Inc.

Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. 2022b. 用人类反馈训练语言模型遵循指令. Advances in Neural Information Processing Systems, 35:27730–27744.

Piotr Padlewski, Max Bain, Matthew Henderson, Zhongkai Zhu, Nishant Relan, Hai Pham, Donovan Ong, Kaloyan Aleksiev, Aitor Ormazabal, Samuel Phua, et al. 2024. Vibe-Eval：一套用于衡量多模态语言模型进展的困难评测集. arXiv preprint arXiv:2405.02287.

Ronak Pradeep, Sahel Sharifymoghaddam, and Jimmy Lin. 2023. RankZephyr：有效且稳健的零样本列表式重排序轻而易举. arXiv preprint arXiv:2312.02724.

Yujia Qin, Shihao Liang, Yining Ye, Kunlun Zhu, Lan Yan, Yaxi Lu, Yankai Lin, Xin Cong, Xiangru Tang, Bill Qian, Sihan Zhao, Lauren Hong, Runchu Tian, Ruobing Xie, Jie Zhou, Mark Gerstein, Dahai Li, Zhiyuan Liu, and Maosong Sun. 2023. ToolLLM：帮助大语言模型掌握 16000 多个真实世界 API. Preprint, arXiv:2307.16789.

Rafael Rafailov, Archit Sharma, Eric Mitchell, Christopher D Manning, Stefano Ermon, and Chelsea Finn. 2023. 直接偏好优化：你的语言模型其实是一个奖励模型. In Advances in Neural Information Processing Systems, volume 36, pages 53728–53741. Curran Associates, Inc.

Nils Reimers and Iryna Gurevych. 2019. Sentence-BERT：用孪生 BERT 网络做句子嵌入. arXiv preprint arXiv:1908.10084.

Stephen E Robertson, Steve Walker, Susan Jones, Micheline M Hancock-Beaulieu, Mike Gatford, et al. 1995. Okapi 在 TREC-3. NIST Special Publication Sp, 109:109.

Victor Sanh, Albert Webson, Colin Raffel, Stephen Bach, Lintang Sutawika, Zaid Alyafeai, Antoine Chaffin, Arnaud Stiegler, Arun Raja, Manan Dey, M Saiful Bari, Canwen Xu, Urmish Thakker, Shanya Sharma Sharma, Eliza Szczechla, Taewoon Kim, Gunjan Chhablani, Nihal Nayak, Debajyoti Datta, Jonathan Chang, Mike Tian-Jian Jiang, Han Wang, Matteo Manica, Sheng Shen, Zheng Xin Yong, Harshit Pandey, Rachel Bawden, Thomas Wang, Trishala Neeraj, Jos Rozen, Abheesht Sharma, Andrea Santilli, Thibault Fevry, Jason Alan Fries, Ryan Teehan, Teven Le Scao, Stella Biderman, Leo Gao, Thomas Wolf, and Alexander M Rush. 2022. 多任务提示训练实现零样本任务泛化. In International Conference on Learning Representations.

Shohreh Shaghaghian, Luna Yue Feng, Borna Jafarpour, and Nicolai Pogrebnyakov. 2020. 为法律文档审阅定制上下文化语言模型. In 2020 IEEE International Conference on Big Data (Big Data), pages 2139–2148. IEEE.

<!-- 原 PDF 第 12 页 -->

Karan Singhal, Shekoofeh Azizi, Tao Tu, S Sara Mahdavi, Jason Wei, Hyung Won Chung, Nathan Scales, Ajay Tanwani, Heather Cole-Lewis, Stephen Pfohl, et al. 2023. 大语言模型编码了临床知识. Nature, 620(7972):172–180.

Ian Soboroff. 2021. TREC 2021 概述. In 30th Text REtrieval Conference. Gaithersburg, Maryland.

Ian Soboroff, Shudong Huang, and Donna Harman. 2018. TREC 2018 新闻赛道概述. In TREC, volume 409, page 410.

Ian Soboroff, Shudong Huang, and Donna Harman. 2020. TREC 2020 新闻赛道概述. In TREC.

Hongjin Su, Weijia Shi, Jungo Kasai, Yizhong Wang, Yushi Hu, Mari Ostendorf, Wen-tau Yih, Noah A. Smith, Luke Zettlemoyer, and Tao Yu. 2022. 一个嵌入器，任意任务：指令微调的文本嵌入.

Nandan Thakur, Nils Reimers, Andreas Rücklé, Abhishek Srivastava, and Iryna Gurevych. 2021. BEIR：用于信息检索模型零样本评估的异构基准. arXiv preprint arXiv:2104.08663.

Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, et al. 2023a. Llama：开放且高效的基础语言模型. arXiv preprint arXiv:2302.13971.

Hugo Touvron, Louis Martin, Kevin R. Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, Daniel M. Bikel, Lukas Blecher, Cristian Cantón Ferrer, Moya Chen, Guillem Cucurull, David Esiobu, Jude Fernandes, Jeremy Fu, Wenyin Fu, Brian Fuller, Cynthia Gao, Vedanuj Goswami, Naman Goyal, Anthony S. Hartshorn, Saghar Hosseini, Rui Hou, Hakan Inan, Marcin Kardas, Viktor Kerkez, Madian Khabsa, Isabel M. Kloumann, A. V. Korenev, Punit Singh Koura, Marie-Anne Lachaux, Thibaut Lavril, Jenya Lee, Diana Liskovich, Yinghai Lu, Yuning Mao, Xavier Martinet, Todor Mihaylov, Pushkar Mishra, Igor Molybog, Yixin Nie, Andrew Poulton, Jeremy Reizenstein, Rashi Rungta, Kalyan Saladi, Alan Schelten, Ruan Silva, Eric Michael Smith, R. Subramanian, Xia Tan, Binh Tang, Ross Taylor, Adina Williams, Jian Xiang Kuan, Puxin Xu, Zhengxu Yan, Iliyan Zarov, Yuchen Zhang, Angela Fan, Melanie Kambadur, Sharan Narang, Aurelien Rodriguez, Robert Stojnic, Sergey Edunov, and Thomas Scialom. 2023b. Llama 2：开放的基础模型与微调后的对话模型. ArXiv, abs/2307.09288.

Ellen M Voorhees. 2005. TREC Robust 检索赛道. In ACM SIGIR Forum, volume 39, pages 11–20. ACM New York, NY, USA.

Liang Wang, Nan Yang, Xiaolong Huang, Binxing Jiao, Linjun Yang, Daxin Jiang, Rangan Majumder, and Furu Wei. 2022a. 通过弱监督对比预训练得到的文本嵌入. arXiv preprint arXiv:2212.03533.

Liang Wang, Nan Yang, Xiaolong Huang, Linjun Yang, Rangan Majumder, and Furu Wei. 2023a. 用大语言模型改进文本嵌入. arXiv preprint arXiv:2401.00368.

Yizhong Wang, Hamish Ivison, Pradeep Dasigi, Jack Hessel, Tushar Khot, Khyathi Raghavi Chandu, David Wadden, Kelsey MacMillan, Noah A. Smith, Iz Beltagy, and Hannaneh Hajishirzi. 2023b. 骆驼能走多远？探索开放资源上指令微调的现状. Preprint, arXiv:2306.04751.

Yizhong Wang, Yeganeh Kordi, Swaroop Mishra, Alisa Liu, Noah A Smith, Daniel Khashabi, and Hannaneh Hajishirzi. 2022b. Self-Instruct：用自生成指令对齐语言模型. arXiv preprint arXiv:2212.10560.

Yizhong Wang, Swaroop Mishra, Pegah Alipoormolabashi, Yeganeh Kordi, Amirreza Mirzaei, Anjana Arunkumar, Arjun Ashok, Arut Selvan Dhanasekaran, Atharva Naik, David Stap, et al. 2022c. Super-NaturalInstructions：通过 1600 多个 NLP 任务上的声明式指令实现泛化. arXiv preprint arXiv:2204.07705.

William Webber, Alistair Moffat, and Justin Zobel. 2008. 检索实验中的统计功效. In Proceedings of the 17th ACM Conference on Information and Knowledge Management, pages 571–580.

Jason Wei, Maarten Bosma, Vincent Y. Zhao, Kelvin Guu, Adams Wei Yu, Brian Lester, Nan Du, Andrew M. Dai, and Quoc V. Le. 2022. 微调后的语言模型是零样本学习者. Preprint, arXiv:2109.01652.

Orion Weller, Dawn J Lawrie, and Benjamin Van Durme. 2024. NevIR：神经信息检索中的否定. Conference of the European Chapter of the Association for Computational Linguistics.

Orion Weller, Kyle Lo, David Wadden, Dawn Lawrie, Benjamin Van Durme, Arman Cohan, and Luca Soldaini. 2023. 生成式查询扩展与文档扩展何时失败？一项跨方法、检索器与数据集的综合研究. arXiv preprint arXiv:2309.08541.

Shitao Xiao, Zheng Liu, Peitian Zhang, and Niklas Muennighoff. 2023. C-Pack：推进通用中文嵌入的打包资源. Preprint, arXiv:2309.07597.

Rui Yang, Lin Song, Yanwei Li, Sijie Zhao, Yixiao Ge, Xiu Li, and Ying Shan. 2023. GPT4Tools：通过自指令教会大语言模型使用工具. In Advances in Neural Information Processing Systems, volume 36, pages 71995–72007. Curran Associates, Inc.

<!-- 原 PDF 第 13 页 -->

Zhiyuan Zeng, Jiatong Yu, Tianyu Gao, Yu Meng, Tanya Goyal, and Danqi Chen. 2023. 在评估指令遵循这件事上评估大语言模型. Preprint, arXiv:2310.07641.

Ming Zhao, Peter Anderson, Vihan Jain, Su Wang, Alexander Ku, Jason Baldridge, and Eugene Ie. 2021. 论视觉与语言导航指令的评估. arXiv preprint arXiv:2101.10504.

## 附录 A 常见问题

**为什么数据集这么小 / 只有大约 100 个实例？**

在 NLP 中，100 个实例会是一个小数据集（尽管并非闻所未闻，见 HumanEval（Chen et al., 2021）、VibeEval（Padlewski et al., 2024）等，它们常用于评估大语言模型，并且受到尊重）。

然而在 IR 中，由于每条查询都需要为相关性标注数百篇文档，查询数量更少，但标注数量相近。因此，对我们的 102 条查询集合而言，大约是 102 条查询 ×（50 篇相关与 150 篇不相关）文档，总计约 2 万条标注——这与 NLP 数据集中的标注量相似。由此可见，IR 的标注在每个实例上需要标准 NLP 基准大约 200 倍的成本。

另一种做法是每条查询收集更少的标注（例如 NQ 或 MS MARCO，它们每条查询只有一篇相关文档，但查询多得多），但这些已被证明大量包含相关、却未被标为相关的文档，使它们作为评估的质量较低（Ni et al., 2021; Cai et al., 2022）。因此 IR 社区会开发判定更充分、但查询数量更少的版本（例如建立在上文所引 MS MARCO 之上的 Deep Learning Tracks 2019–2022，或我们所基于的那些集合）。

**语言模型能处理这类长指令吗？**

能。查询加指令的长度平均大约 80 个词，文档大约 400 个词，大多数（如果不是全部）语言模型都能在其上下文长度内容纳 480 个词。对上下文长度大于 1024 个词元的现代语言模型尤其如此。总体而言，这对语言模型来说其实并不算长上下文。

**并非所有检索任务都会有指令，那我们能做什么？**

我们同意情况确实如此；事实上，我们只能找到这一个真实世界检索指令的来源。我们认为这部分是因为缺少能够处理它们的系统——如果检索系统不会使用指令，用户为什么要给它一条指令？然而，正如 TREC 所示，存在人们希望能够借助这些指令完成的用例。我们的数据集通过提供训练与测试数据，为构建能够处理它们的系统迈出第一步。不过，系统应当既能处理无指令的情形，也能处理有指令的情形——由于已有大量数据集用于评估无指令情形，我们的数据集提供了测试有指令情形的方法。

## 附录 B FollowIR 的 Llama-3-8B 版本

我们也训练了一个 Llama-3-8B（AI@Meta, 2024）版本的 FollowIR。然而，正如社区中许多其他人发现的那样，Llama 3 在检索上不如 Mistral（BehnamGhader et al., 2024）。我们发现基座模型的 p-MRR 为 0.03，在 FollowIR-train 上微调之后变为 5.1 p-MRR。就 nDCG 而言，FollowIR-Llama3-8B 得分为 15.4，而 FollowIR-Mistral 为 24.8。

## 附录 C 微调 Mistral 的超参数

我们使用如下超参数训练 Mistral：批大小 32，余弦调度器，学习率 3e-5，最大长度 2048，LoRA 秩 8、alpha 16，bfloat16，训练 8 个 epoch。LoRA 微调使用的模块为 “q_proj,v_proj,o_proj,k_proj”，并从 mistralai/Mistral-7B-Instruct-v0.2 开始训练。

## 附录 D 推理超参数

推理使用默认参数，取自我们所使用论文作者的原始代码（来自他们的 MTEB 评估）。

## 附录 E 所用算力

实验使用一张 A100 80GB。训练大约用 6 小时，推理依模型大小在 3–12 小时之间。

## 附录 F 全量检索结果

表 5 给出模型在 FOLLOWIR 所含 TREC 任务的完整集合上搜索的结果。请注意，由于每个模型检索到的相关文档不同，指令遵循评估中每个模型所评估的实例集合也不同（因为它只能在它检索到、随后变为不相关的文档上被评估）。

<!-- 原 PDF 第 14 页 -->

**表 5：** 在完整检索集合上的 FOLLOWIR 分数（因此不包含重排序器）。由于基础分数不同，它们在 p-MRR 上所评估的相关文档数量也不同。因此，我们只报告原始（无指令）分数，以及使用 TREC 指令时的差值。我们注意到，它与正文显示出相似的结果——检索模型并未有效使用指令，并且会因更长的文本而性能下降。

列组为 Robust04（mAP）、News21（nDCG@5）、Core17（mAP）。每组含 OG（原始）与 ∆（差值）。数字按页内正文抽取的逐行顺序还原。

| 模型 | Robust04 OG | Robust04 ∆ | News21 OG | News21 ∆ | Core17 OG | Core17 ∆ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **No Instruct** |  |  |  |  |  |  |
| BM25 | 21.4 | −1.2 | 30.1 | +5.3 | 16.8 | −0.2 |
| E5-base-v2 | 22.7 | −7.0 | 33.6 | +1.8 | 19.7 | −3.0 |
| Contriever | 19.2 | −7.7 | 22.5 | +9.0 | 22.6 | −7.6 |
| **Uses Instruct** |  |  |  |  |  |  |
| TART-Contriever | 25.5 | −10.1 | 40.0 | −5.0 | 22.6 | −7.6 |
| BGE-base | 23.6 | −3.1 | 36.5 | −7.8 | 23.0 | −2.1 |
| INSTRUCTOR-base | 22.5 | −2.2 | 33.3 | −2.8 | 20.0 | −0.2 |
| INSTRUCTOR-XL | 30.4 | −3.1 | 38.1 | −0.1 | 29.9 | −2.8 |

## 附录 G BEIR 实验所用关键词

GPT-4-Turbo-1106 从这些模型所使用的指令中抽出如下关键词（表 6），并由此产生表 3 中的结果。

## 附录 H 所用提示

我们用这些提示来生成短指令、关键词以及合成文档。“完整指令到短指令”提示中使用的示例部分由作者编写，因为 TART/INSTRUCTOR 只提供了短指令。

<!-- 原 PDF 第 15 页 -->

**表 6：** BEIR 关键词分析所用的关键词。注意，非指令模型收到的是 INSTRUCTOR-base 与 TART-dual 所使用的关键词（如表中所示）。关键词字符串保留抽取原文。

| 模型 | 数据集 | 关键词 |
| --- | --- | --- |
| BM25/Contriever/E5/MonoT5 | FiQA | Finance web |
| BM25/Contriever/E5/MonoT5 | SciFact | science paper verify |
| BM25/Contriever/E5/MonoT5 | NFCorpus | medicine relevant |
| TART-dual | FiQA | financial web |
| TART-dual | SciFact | scientific paper verify |
| TART-dual | NFCorpus | scientific paper paragraph |
| INSTRUCTOR-base | FiQA | financial supporting: |
| INSTRUCTOR-base | SciFact | scientific supporting passage: |
| INSTRUCTOR-base | NFCorpus | medicine relevant |
| BGE-base | FiQA | relevant passages: |
| BGE-base | SciFact | relevant passages: |
| BGE-base | NFCorpus | relevant passages: |
| INSTRUCTOR-xl | FiQA | finance supporting: |
| INSTRUCTOR-xl | SciFact | scientific supporting passages: |
| INSTRUCTOR-xl | NFCorpus | nutrition facts public medical: |
| E5-Mistral | FiQA | financial replies |
| E5-Mistral | SciFact | scientific |
| E5-Mistral | NFCorpus | retrieve relevant |
| TART-T5-FLAN-xl | FiQA | financial web |
| TART-T5-FLAN-xl | SciFact | scientific paper verify |
| TART-T5-FLAN-xl | NFCorpus | Scientific paper paragraph |

<!-- 原 PDF 第 16 页 -->

### 合成文档创建

我需要你为我的业务标注一些数据，严格遵循指令极其重要，否则你会被解雇。

给定一条 Google 搜索查询，以及关于什么使文档相关的指令，我需要你写两篇文档：一篇相关，一篇不相关。

搜索：TITLE_HERE

指令：NARRATIVE_HERE

我需要一些不同的选项以供选择，因此请为相关文档和不相关文档各给出三个**不同**的选项。它们应当是**长**的、段落规模的文档（每篇约 300 词），一行一篇。如果指令中没有否定，你的不相关文档应当稍微偏题：

### 短指令到关键词

我有一些针对某种检索风格的指令，但我希望你只关注这些指令中的相关关键词。你的任务是返回一份与查询相关的关键词列表。大概只需要抽出一到两个相关关键词。

## 示例

### 示例 1：

指令：帮我找一篇与此问题高度相关的 PubMed 论文。

关键词：["PubMed"]

### 示例 2：

指令：我想为这道 Trivia 问题找一个答案。你能找一些提供 Wikipedia 证据的段落吗？

关键词：["Trivia", "Wikipedia"]

### 示例 3：

指令：检查一道 Quora 问题是否与这个问题重复。

关键词：["Quora", "duplicated"]

### 示例 4：

指令：我想找一道在 StackExchange 上提出的相关问题。你能帮我找一道吗？

关键词：["related", "StackExchange"]

## 轮到你

指令：FILL_TEXT_HERE

关键词（一到两个关键词，且不是 “documents”、“questions”、“answer” 或 “articles”）：

<!-- 原 PDF 第 17 页 -->

### 完整指令到短指令

我有一些针对某个问题的具体指令，但我需要你帮忙把它们抽象成一种通用任务形式，以便交给别人。我需要你把它们变成一条抽象命令，只描述一般性的抽象任务（例如数据来自何处、文档是什么类型）。阅读并遵循这些指令至关重要；如果你成功，将获得一大笔奖金（200 美元）。

抽象命令只应提及**任务形式**。**不要**提及原始指令中的任何实体或具体文本。你的回答应在 10 个词左右。这条命令应当像是在对另一个人说话。

## 示例

### 示例 1：

原始指令：一篇相关文档会提供关于全血基灌注液的信息，以及它在离体心脏灌注期间是否能更好地保存心肌功能。这可以包括研究实验、评论或综述论文。仅关于全血基灌注液的信息并不相关，除非它也提到其对离体心脏灌注期间心肌功能的影响。

抽象命令：帮我找一篇与此问题高度相关的 PubMed 论文。

### 示例 2：

原始指令：一篇相关文档将包含可用于判断在给定情形下谁应拥有优先权的、关于国际水域航行权的信息。例如，它应包含关于事故中谁有过错的实例、这是否取决于船的大小，或关于这一点如何因国籍而不同的细节。尤其相关的是描述碰撞情形中谁有过错的文档。

抽象命令：检索一段回答该问题的 Wikipedia 段落。

### 示例 3：

原始指令：一个相关实例将是一个在语义上与给定查询等价的问题。例如，它可能包含不同的词汇，或是另一方的释义，但底层含义相同。如果该实例在语义上与查询不同，则不相关。

抽象命令：检查一道 Quora 问题是否与这个问题重复。

### 示例 4：

原始指令：一篇相关文档会包含关于 Medicare 时间安排、以及患者从几岁可以开始将其用于医疗的细节。它可能包括关于法律、保险或其他描述 Medicare 开始年龄的细节。不太相关的是那些谈论潜在法律或 Medicare 事实、却没有回答 Medicare 从几岁开始这一问题的文档。只要提到一个年龄以及何时开始使用 Medicare，即算相关。

抽象命令：我想知道这个问题的答案。你能在网上找到好的证据吗？

现在你可以很容易看出，抽象命令是模糊的，只描述一条关于如何获得所需信息的短命令。严格照此执行——不要引用具体内容（如上所述，“international waters” 与 “medicare” 并未出现在抽象命令中）。你应当让抽象命令保持模糊，并且只对任务本身做抽象。使用 “question” 这个词。

## 轮到你

原始指令：FILL_TEXT_HERE

抽象命令（记住要使用 “question” 这个词）：

<!-- 译完 -->
