# FollowIR: Evaluating and Teaching Information Retrieval Models to Follow Instructions

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`FollowIR_NAACL2025.pdf`。

## Abstract 摘要

现代语言模型（Language Models, LMs）能够遵循长而复杂的指令，从而支持大量且多样的用户请求。尽管信息检索（Information Retrieval, IR）模型以这些语言模型作为架构骨干，但几乎没有系统允许用户在查询之外再提供详细指令，因而限制了它们满足复杂信息需求的能力。本文研究指令在 IR 系统中的使用。我们构建 FollowIR，一个用于在 IR 中遵循真实世界指令的严格指令评测基准。FollowIR 重新利用为专业评审员（professional assessors）制定、用于评价检索系统的详细指令——也称为叙述（narratives）。具体而言，我们的基准来自文本检索会议（Text REtrieval Conference, TREC）共享任务所整理的三个集合。借此，我们可以用一种新的成对评价框架（pairwise evaluation framework）衡量 IR 模型遵循指令的程度。结果表明，现有检索模型不能正确使用指令：它们把指令当作基本关键词，并且难以理解长文本信息。不过，我们表明 IR 模型可以学会遵循复杂指令：新模型 FollowIR-7B 在我们的训练集上微调后有显著提升。1

1 代码、数据与模型见 https://github.com/orionw/FollowIR。

## 1 Introduction 引言

现代语言模型经过大量调优，能够忠实（Chung et al., 2022; Ouyang et al., 2022a; Rafailov et al., 2023; Wang et al., 2023b; Ivison et al., 2023）且安全地（Bai et al., 2022; Bianchi et al., 2024）遵循用户指令。凭借这些能力，语言模型能够成功处理广泛任务（Chiang et al., 2024; Liang et al., 2023; Yang et al., 2023; Jimenez et al., 2024; Zeng et al., 2023），即便并未针对这些任务显式微调。

与更广泛的语言模型社区相比，信息检索的实践者与研究者尚未充分利用指令调优模型（instruction-tuned models）。由于语言模型能够有效估计查询与文档之间的语义相似度，它们已被用作神经检索架构的主要骨干（Karpukhin et al., 2020; Khattab and Zaharia, 2020; Reimers and Gurevych, 2019）。然而，这些系统中的绝大多数被微调为仅作为文本片段相似度估计器（text spans similarity estimators）运行（Khattab and Zaharia, 2020; Izacard et al., 2021; Nogueira and Cho, 2019; Pradeep et al., 2023; Ma et al., 2023）。超越这些 ad-hoc 检索系统、改为带指令检索，将能够支持复杂的信息需求。例如，设想一位研究者希望找出必须同时具备多种属性才算相关的论文（来自给定会议、使用给定类别的方法，等等），同时还要避开会使其不相关的条件（使用负面情感、使用某些领域的数据集，等等）。

近期工作已开始走向带指令的搜索，但这一主题仍然研究不足，仅有少数论文涉及（Su et al., 2022; Asai et al., 2022; Muennighoff et al., 2024）。我们特别发现，它们对指令的使用很窄：指令通常很短（少于 10 个词），并且重复（每个数据集只有一条指令，例如 Su et al. (2022); Asai et al. (2022); Li and Li (2023); Xiao et al. (2023)）。此外，这些工作缺少显式衡量指令遵循的评测数据集，而是聚焦于标准 ad-hoc 检索基准。

为弥补这些缺口，我们提出 FollowIR。它包括：（1）一个显式衡量检索模型指令遵循能力的基准；（2）包含多样且现实指令的训练数据。我们的关键直觉是，利用为 IR 系统专业标注员制定的指令，来研究具备指令遵循能力的 IR 模型。这些指令被标注员用来判断给定查询下的文档相关性。幸运的是，IR 领域拥有丰富的此类数据：在任何构造良好的 IR 数据集中，这些指令——也称为 narratives——都会为全部查询创建。具体而言，我们使用为 Text REtrieval Conference 共享任务制定的 narratives。这些指令详尽而复杂，包含使一篇文档相关或不相关的细微细节。因此，如果标注员能用这些 TREC 指令标注文档相关性，指令遵循检索模型也应能够做到（查询与指令对的例子见图 1 与图 2）。

图 1：标准检索查询与指令（或 narratives）有何不同？指令包含更多关于何者为相关的具体细节，较少包含直接相关的背景信息，并且常常用否定给出哪些文档不相关的指示。百分数表示这些特征在 TREC 指令中出现的频率。

我们以三个深度判定的 TREC 集合作为评测集基础：TREC Robust 2004（Voorhees, 2005）、TREC Common Core 2017（Allan et al., 2017）以及 TREC News 2021（Soboroff et al., 2020）。这些集合经过充分标注，以便评价检索召回，有数百到数千篇文档被判定为相关或不相关。我们取交给专业标注员的指令并稍作改动，人工重新标注相关文档。于是得到成对指令，用于测试模型对改动后指令的反应：我们衡量模型是否会更新其相关文档，使之与改动后的指令一致。

由于 IR 中尚无现成方法比较成对查询，我们开发了一种新的评价框架：对同一查询配以一对不同指令，衡量文档的逐排名分数变化（我们称之为 p-MRR）。FollowIR 上的结果表明，当前模型通常无法在检索中遵循指令，除非参数量达到 3B+，或者并未针对检索进行训练。分析表明，这些失败来自两种现象：（1）模型不习惯长指令；（2）模型把指令用于关键词搜索。

为推进能够理解指令的检索模型，我们构建了一套真实世界中由人使用的指令训练集，并在其上微调一个模型（FollowIR-7B）。结果显示，FollowIR 上的标准 IR 指标与 p-MRR 都有明显提升，为后续进展提供了一个起点。

总之，我们的贡献如下：（1）一个评价检索中指令遵循的基准 FollowIR，它在三个已经高度判定的语料之上加入人工标注；（2）对当前模型为何无法理解指令的分析；（3）用于教导检索模型遵循指令的训练数据，以及一个能够处理 IR 中长指令的新开源 IR 模型 FollowIR-7B。

## 2 Related Work 相关工作

### TREC Conferences TREC 会议

美国国家科学与技术研究院（National Institute of Science and Technology, NIST）于 1993 年创建了 TREC 组织。每年 TREC 赞助许多赛道（tracks），亦即共享任务，各自针对给定数据集。这些赛道涵盖多种主题：从新闻上的标准 ad-hoc 检索（Soboroff et al., 2018; Soboroff, 2021），到更复杂的领域，例如法律检索（Oard et al., 2008），或检索增强生成／报告生成（retrieval-augmented generation/report-generation）（Lawrie et al., 2024）。

图 2：成对评价框架的示意图。模型先在带原始指令的查询上被评价，再在带改动指令的查询上被评价。如果模型正确理解指令，它会改变哪些文档相对于该改动是相关的（右侧）。交给 TREC 标注员的真实世界指令（左侧）包含关于相关性的细粒度细节以及否定。图内可辨认的文字包括查询 “Identify positive accomplishments of the Hubble telescope since it was launched.”，以及指令中的 “Documents are relevant that show the Hubble telescope has produced new data, better quality data than previously available”、“relied solely on the Hubble”、“Documents limited to the problems of the telescope are be irrelevant”、“Details of repairs to the telescope without reference to positive achievements would not”。Doc 1 与 Doc N 分别涉及 Hubble Space Telescope、US Cosmic Explorer (Cobe) 与土星上的风暴。图中还有 “Does the model change with the altered instruction?”，以及 Original 与 Altered 下文档顺序由 Doc N、Doc 1 变为 Doc 1、Doc N。省略号与栏间交错处【抽取不清】。

作为这一过程的一部分，NIST 为这些集合赞助标注。通常做法是汇集（pooling）来自多种检索模型的一组结果（runs），再按排名顺序标注，直到经费用尽。为便于标注，赛道组织者为每条查询提供一段 narrative（或指令）交给标注员；然而 IR 模型历来只得到查询。评价总召回需要为每条查询标注集合中的每篇文档，对拥有数百万文档的集合并不可行，因此召回误差通过事后抽样与标注来检验。尽管并非每一对查询与文档都能被评价，查询上的召回非常高。我们以 TREC 所做的严格评价为起点，从其若干集合出发。

### Instructions for LMs 面向语言模型的指令

指令遵循语言模型因 InstructGPT（Ouyang et al., 2022a）、FLAN（Wei et al., 2022）和 T0（Sanh et al., 2022）等模型而普及，并已成为自然语言处理社区的一大研究方向（Touvron et al., 2023a; Jiang et al., 2023; Groeneveld et al., 2024; Black et al., 2022）。已有大量工作评估它们能否泛化到新指令（Wang et al., 2022c; Ouyang et al., 2022b），能否在没有人工标注数据的情况下训练它们遵循指令（Wang et al., 2022b; Qin et al., 2023），以及将它们应用到各个领域（Zhao et al., 2021; Singhal et al., 2023; Shaghaghian et al., 2020）。由于 IR 社区在流程中使用语言模型，我们希望把 IR 的范围扩展到包含指令，使之与更广泛的 NLP 社区对齐。

### Instructions for Retrieval 面向检索的指令

在检索中使用指令仍是一个刚起步的方向。Su et al. (2022) 与 Asai et al. (2022) 是最早训练检索模型将指令与查询一起使用的工作之二。然而这些指令通常非常短，例如 “Retrieve a Wikipedia paragraph that answers this question.” 近期工作在较小模型中纳入指令（Xiao et al., 2023; Chen et al., 2023, 2024）；另一些工作则以 Llama（Touvron et al., 2023a; Weller et al., 2023）或 Mistral（Jiang et al., 2023）作为能够使用指令的更大检索模型的骨干：GritLM（Muennighoff et al., 2024）训练 Mistral 同时做生成与嵌入，Wang et al. (2023a) 则仅将 Mistral 用于嵌入。

尽管这一方向进展密集，这些工作并没有显式的指令相关检索基准可供评价。它们转而在 MTEB（Muennighoff et al., 2022）和 BEIR（Thakur et al., 2021）等标准检索基准套件上评价，而这些套件并不包含指令。因此，这些较新的指令检索模型手写少量指令，通常每条指令作用于整个数据集，与具体查询无关。这使指令较为泛化：只关注任务格式、“文档”的格式（段落、句子等）以及宽泛领域。正因如此，当前指令都不包含额外背景信息或否定（Weller et al., 2024），而这些在真实世界指令中很常见（差异示例见图 1）。

在与我们同期的工作中，Oh et al. (2024) 也提出了一个数据集，用于评价检索模型中的指令。该数据集使用 MS MARCO 集合（Nguyen et al., 2016），并在若干关键方面不同：每条查询只有一篇相关文档（即稀疏判定），由 GPT-4 生成并验证，聚焦用户背景（“I am a school teaching looking for ...”），并用同一查询的 N 条指令中的最低分来评价（衡量稳健性）。与之相对，我们使用高度判定的语料以确保能够衡量召回，使用专业生成的指令，拥有经过人工验证的相关性判断，提出一种新的成对评价协议，并提供用于教授指令遵循的训练数据集与模型。
