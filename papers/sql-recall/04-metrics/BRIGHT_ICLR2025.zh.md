# BRIGHT：面向推理密集型检索的现实且有挑战的基准

- 原文件名：BRIGHT_ICLR2025.pdf
- 原标题：BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval
- 中文标题：BRIGHT：面向推理密集型检索的现实且有挑战的基准
- 作者：Hongjin Su∗h、Howard Yen∗p、Mengzhou Xia∗p、Weijia Shi w、Niklas Muennighoff s、Han-yu Wang h、Haisu Liu h、Quan Shi p、Zachary S. Siegel p、Michael Tang p、Ruoxi Sun g、Jinsung Yoon g、Sercan Ö. Arık g、Danqi Chen p、Tao Yu h（∗同等贡献；h The University of Hong Kong；p Princeton University；s Stanford University；w University of Washington；g Google Cloud AI Research）
- 会议或 arXiv：Published as a conference paper at ICLR 2025；arXiv:2407.12883v4 [cs.CL] 26 Mar 2025
- 邮箱：{hjsu,tyu}@cs.hku.hk；{hyen,mengzhou,danqic}@cs.princeton.edu

<!-- 原 PDF 第 1 页 -->

## 摘要

现有检索基准主要由信息寻求型查询构成（例如从搜索引擎汇总的问题），此时基于关键词或语义的检索通常就够用。然而，许多复杂的真实世界查询需要深入推理，才能识别超出表面形式匹配的相关文档。例如，为一道编程题寻找文档，需要理解所涉函数的逻辑和语法。为了更好地在这类有挑战的查询上基准测试检索，我们引入 BRIGHT，第一个需要密集推理才能检索相关文档的文本检索基准。我们的数据集由 1,384 条真实世界查询组成，跨越经济、心理、数学和编程等多样领域。这些查询来自自然发生并经仔细整理的人类数据。广泛评估表明，即便最先进的检索模型在 BRIGHT 上表现也很差。MTEB 排行榜上的领先模型（Muennighoff et al., 2023）SFR-Embedding-Mistral（Meng et al., 2024）在 BEIR 上取得 59.0 的 NDCG@10，【脚注 1】在 BRIGHT 上的 NDCG@10 却只有 18.3。我们表明，把关于查询的显式推理纳入检索，最多可以把检索性能提高 12.2 个点。此外，纳入来自表现最好的检索器的检索文档，会提升问答性能。我们相信 BRIGHT 为在更现实、更有挑战的设定下研究检索系统开辟了道路。【脚注 2】

【脚注 1】取自 2024-05-28 的 MTEB 排行榜。

【脚注 2】代码与数据见 https://github.com/xlang-ai/BRIGHT 与 https://huggingface.co/datasets/xlangai/BRIGHT 。

## 1 引言

信息检索是一项被广泛使用的技术，帮助用户从包含文档、网页和日志记录的大规模语料中定位相关信息（Bajaj et al., 2016; Thakur et al., 2021）。相关信息可以以不同方式与用户查询关联——有时通过直接的匹配模式，如共享关键词或语义相似；有时通过更深、更细微的联系，如类似的底层原理。在许多真实世界场景中，用户查询可以高度复杂，找到相关文档需要密集推理。例如，一位经济学家可能想找到由与另一个故事相同的经济理论所解释的故事，或者一位程序员可能想用一条错误信息定位对应的语法文档。对这些应用，相关文档不能仅通过词汇或语义匹配直接检索到，而需要额外的推理步骤来识别。

在本工作中，我们用 BRIGHT 研究推理密集型检索问题。BRIGHT 是一个新基准，检索相关文档需要密集推理。现有检索基准，如 BEIR（Thakur et al., 2021）和 MTEB（Muennighoff et al., 2023），主要聚焦于基于事实的、

<!-- 原 PDF 第 2 页 -->

**图 1 见原 PDF。** 图 1：现有检索基准聚焦于基于关键词的检索（第 1 级）或基于语义的检索（第 2 级），例如 NQ、MS MARCO 数据集（Kwiatkowski et al., 2019; Bajaj et al., 2018）。BRIGHT 引入第 3 级检索，查询与文档之间的相关性需要密集推理才能判定。我们的数据由来自多样领域（例如经济、数学、地球科学等）的自然用户查询组成。BRIGHT 语料也跨越网页数据，如博客、语法文档和 STEM 问题–解答。

图中例子包括：查询 “Who sang the song I Think We're Alone Now?”，正文档靠关键词匹配；可持续生活帖子问能否把花盆下的水再用，正文档讨论土壤中可溶盐；代码问题问 Snowflake 中是否有比 UNPIVOT 更好的函数，正文档是 FLATTEN；数学题 “Let k=2008^2+2^2008. What is the units digit of k^2+2^k?”，正文档使用同一条定理。

通常来自搜索引擎的查询，查询与文档之间的相关性往往直截了当，可以通过简单的关键词或语义匹配检测出来（Lee et al., 2019; Karpukhin et al., 2020）。这些数据集聚焦于检索特定信息片段（例如 “the widest highway in North America”），因此相关文档往往与查询有高词汇或语义重叠。相比之下，BRIGHT 中查询与文档之间的相关性不容易通过简单的关键词或语义匹配检测出来，并且由于我们的领域和查询的复杂性质，需要审慎推理（图 1）。

BRIGHT 由来自多样且高阶领域的 12 个数据集组成，来源是自然发生的人类数据和精心整理的来源。该基准包含两个主要部分：1）七个数据集由 StackExchange 构造，相关性由一篇文档是否在答案中被引用来定义，并进一步经多位标注者验证，以确保正文档有效支持处理查询。鉴于这一评估固有的主观性，我们只纳入标注者一致同意的文档。2）其余五个数据集聚焦于编程和数学问题，查询由于共享底层算法或定理而与正文档内在相连。

我们评估 13 个代表性检索模型，规模和架构各异。综合实验凸显了 BRIGHT 带来的挑战：表现最好的模型 SFR-Embedding-Mistral（Meng et al., 2024）在 MTEB 检索子集 BEIR（Thakur et al., 2021）上得分为 59.0，在 BRIGHT 上的 NDCG@10 只有 18.3。为识别改进 BRIGHT 的有前景方向，我们探索多种策略——一种有效做法是利用 LLM 在检索之前生成关于查询的思维链推理步骤（Wei et al., 2022），平均提升最高达 12.2 个点。此外，用来自表现最好的检索器 Qwen 的检索文档增强下游模型，相对于闭卷设定提升了问答性能。然而，使用预言文档会带来更大的提升，凸显了改进检索器模型的潜在收益。

此外，我们的结果表明 BRIGHT 对大规模预训练期间潜在的数据泄漏是稳健的：即便模型在基准数据集的文档上进一步训练，也没有观察到实质性的性能增益。我们希望这些发现能启发研究方向，推进推理密集型检索的最新水平。

<!-- 原 PDF 第 3 页 -->

## 2 相关工作

**基准测试检索。** 现有信息检索（IR）数据集通常为信息寻求任务而构造，例如问答（Voorhees & Tice, 2000; Craswell et al., 2020; Kwiatkowski et al., 2019; Chen et al., 2017; Maia et al., 2018）、主张验证（Thorne et al., 2018; Diggelmann et al., 2020; Wadden et al., 2020）或实体检索（Hasibi et al., 2017; Petroni et al., 2021）。近期工作用更多场景扩展检索基准，例如指令遵循（Su et al., 2023; Weller et al., 2024; Oh et al., 2024; Li et al., 2024）、多跳（Yang et al., 2018）和长上下文检索（Saad-Falcon et al., 2024; Zhu et al., 2024）。像 BEIR（Thakur et al., 2021）这样的综合基准在多样领域和任务上评估检索系统，相关文档与查询共享高语义重叠。与我们的工作最接近的是 BIRCO（Wang et al., 2024），它通过利用现有数据集，基于多方面目标评估检索系统。然而，它限于 LLM 重排序设定，并且每个查询只使用一个小候选池（约 100 篇文档）。RAR-b（Xiao et al., 2024）把现有常识、数学和代码数据集改造成检索设定，以测试模型能否直接检索推理问题的答案。然而，我们聚焦于更现实的场景：答案不太可能作为文档中的子串被找到。【脚注 3】虽然两个基准都聚焦于推理密集型检索，BRIGHT 是第一个收集现实用户查询、并把它们与来自大规模语料的相关自然文档对齐的基准，识别正确匹配需要深度推理。

**稠密检索模型与检索增强生成。** 最先进的检索系统常常用稠密模型以丰富表示来编码文本。这些模型在无监督数据（Lee et al., 2019; Izacard et al., 2022）、有监督数据（Su et al., 2023; Asai et al., 2023a; Muennighoff, 2022）以及 LLM 生成的数据（Lee et al., 2024; Wang et al., 2023a; Muennighoff et al., 2024）上训练。在本工作中，我们沿不同轴基准测试多样的模型集合：稀疏与稠密；小与大；开源与专有。此外，随着稠密生成模型持续改进，检索增强生成（RAG；Asai et al., 2020; Borgeaud et al., 2022; Asai et al., 2023b; Muennighoff et al., 2024; Asai et al., 2024; Gao et al., 2023; Shi et al., 2024）——检索相关文档以帮助生成连贯答案——已成为一项重要应用。虽然本工作主要聚焦于检索，我们做了初步分析，并表明使用更强的检索器会改进推理密集型任务上的模型生成。

**基准测试推理。** 许多基准旨在评估 LLM 的推理能力，尤其聚焦于数学和编程。就数学而言，数据集包括 GSM8K（Cobbe et al., 2021）及其扩展 GSM1K（Zhang et al., 2024）、TheoremQA（Chen et al., 2023a）、MATH（Hendrycks et al., 2021）和 LeanDojo（Yang et al., 2023）。就编程而言，常用 HumanEval（Chen et al., 2021）、MBPP（Austin et al., 2021）和 LiveCodeBench（Jain et al., 2024）。这些基准包含问答对，通常来自教科书、在线资源、竞赛或领域专家。我们从选定的高质量数据集中获取查询，并通过额外标注构造 BRIGHT，从而创建一个现实的推理密集型检索基准。

【脚注 3】我们在附录 I 中与 RAR-b 做详细比较。

## 3 构造 BRIGHT

我们引入 BRIGHT，一个检索基准，它测试检索系统能否匹配这样的查询和文档：其相关性需要密集推理才能求解，而不仅仅是词汇和语义相似。在本节中，我们首先形式化推理密集型检索任务（第 3.1 节）。然后，我们详细说明来自 StackExchange 的数据（第 3.2 节）、编程数据集（第 3.3 节）和基于定理的问题（第 3.4 节）的数据收集过程。在表 1 中，我们给出基准统计。

<!-- 原 PDF 第 4 页 -->

**表 1：BRIGHT 的数据统计。** 对每个数据集，我们给出查询数（Q）和文档数（D）、每个例子的平均正文档数（D+）、查询和文档的平均长度（由 GPT-2 分词器 Radford et al. (2019) 衡量），以及查询和文档的来源。Q&Sol 指问题–解答对的演示例子。TheoremQA-Q 和 TheoremQA-T 分别指基于 TheoremQA 的问题检索和定理检索。每个数据集的例子见附录 C。

| 分组 | 数据集 | Q | D | D+ | 查询平均长度 | 文档平均长度 | 查询来源 | 文档来源 | 例子 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| StackExchange | Biology | 103 | 57,359 | 3.6 | 115.2 | 83.6 | StackExchange 帖子 | 网页：文章、教程、新闻、博客、报告等 | 表 20 |
|  | Earth Science | 116 | 121,249 | 5.3 | 109.5 | 132.6 | 同上 | 同上 | 表 21 |
|  | Economics | 103 | 50,220 | 8.0 | 181.5 | 120.2 | 同上 | 同上 | 表 22 |
|  | Psychology | 101 | 52,835 | 7.3 | 149.6 | 118.2 | 同上 | 同上 | 表 23 |
|  | Robotics | 101 | 61,961 | 5.5 | 818.9 | 121.0 | 同上 | 同上 | 表 24 |
|  | Stack Overflow | 117 | 107,081 | 7.0 | 478.3 | 704.7 | 同上 | 同上 | 表 25 |
|  | Sustainable Living | 108 | 60,792 | 5.6 | 148.5 | 107.9 | 同上 | 同上 | 表 26 |
| Coding | LeetCode | 142 | 413,932 | 1.8 | 497.5 | 482.6 | 编程题 | 编程题与解答 | 表 27 |
|  | Pony | 112 | 7,894 | 22.5 | 102.6 | 98.3 | 编程题 | 语法文档 | 表 28 |
| Theorems | AoPS | 111 | 188,002 | 4.7 | 117.1 | 250.5 | 数学奥林匹克题 | STEM 题与解答 | 表 29 |
|  | TheoremQA-Q | 194 | 188,002 | 3.2 | 93.4 | 250.5 | 基于定理的问题 | STEM 题与解答 | 表 30 |
|  | TheoremQA-T | 76 | 23,839 | 2.0 | 91.7 | 354.8 | 基于定理的问题 | 定理 | 表 31 |

### 3.1 任务形式化

给定查询 $Q$ 和检索语料 $D = \{D_1, \ldots, D_n\}$，检索器的任务是找到相关文档 $D_Q^+ = \{D_{Q,1}^+, \ldots, D_{Q,m}^+\} \subset D$，其中 $m \ll n$（正例）。负文档定义为 $D_Q^- = D \setminus D_Q^+$。在推理密集型检索中，相关文档集 $D_Q^+$ 通过与查询相关的特定推理轨迹或解释（例如底层原理、算法或定理）与查询 $Q$ 相连。例如，常见推理轨迹可能涉及识别查询意图、分析并建模问题，以及基于所给描述得出子结论。这类推理轨迹通常不出现在查询本身中，使得仅用查询做直接检索非常有挑战。

### 3.2 StackExchange：检索有助于回答问题的网页

**相关性：** 一篇文档只有在被一篇被接受或高票答案引用，并且被标注者和领域专家一致确认它能用关键概念或理论帮助对查询进行推理时，才被视为与查询相关。

StackExchange【脚注 4】是一个流行的社区驱动平台，用户在上面提问并收到其他用户的回答。在其 170 多个站点中，我们选择 7 个多样且知识密集的领域：Sustainable Living、Economics、Psychology、Robotics、Earth Science、Biology，以及 Stack Overflow 中的编程。与传统检索基准中的短问题不同，StackExchange 上的问题常常包含对问题的长而技术性的描述，并以一个逻辑复杂的问题结束，例如修复一个缺陷。回答常常链接到包含处理该问题的相关信息的外部网页。我们基于用户帖子和答案中引用的文档构造查询–文档对（见图 2）。

**选择帖子。** 人类标注者【脚注 5】从最新到最旧浏览帖子，并选择至少有一个答案满足以下条件的帖子：（1）被用户接受或获得超过 5 票，并且（2）包含一个或多个 URL 链接。这一过程保证每个数据集有足够数量的高质量例子。

【脚注 4】https://stackexchange.com/

【脚注 5】作者以及来自相应领域的大学生。

<!-- 原 PDF 第 5 页 -->

**图 2 见原 PDF。** 图 2：StackExchange 数据标注过程概览。帖子内容用作查询。正文档是答案中所链接网页里被选出的段落，其余段落、来自 Google 的结果，以及被标注者滤掉的段落被视为负例。网页可以包括来自 Wikipedia、博客、文章、报告等的内容。图中查询大意为：住在公寓里，浇花后水会流到花盆下的盘子，能否再用来浇花。答案讨论土壤中盐分积累，并链接到关于可溶盐的文章。

**构造查询与正文档。** 对每个被选中的帖子，我们如下构造查询和正文档：

步骤 1：标注者把帖子的标题和内容合并，形成查询 $Q$。

步骤 2：标注者访问答案中链接的网页，若它们与查询相关则纳入为正文档，否则丢弃。

步骤 3：若没有任何网页被视为正例，该帖子本身被丢弃。对每个收集到的网页，标注者把内容切成段落，并按照相关性定义选出正例 $D_{Q,i}^+$。

**构造负文档。** 为防止模型纯粹依赖词汇或语义相似，我们保证每个查询的负文档也处理相似主题。具体而言，标注者从 Google 收集同一主题的搜索结果，并选择那些主题相关、但不满足查询具体要求的文档（更多例子见附录 C）。收集过程如下：

步骤 1：标注者用帖子标题或 LLM 摘要出的帖子关键词搜索 Google，识别语义相似但对回答问题不相关的网页。

步骤 2：标注者为每个查询收集至多 5 个负网页，并把它们切成硬负段落，构成 $D_Q^-$。

对每个数据集，我们把全部收集到的段落编译成一个统一的检索语料 $D$。对任何给定查询，语料中除其正段落之外的全部段落都被当作负例，包括与其他查询关联的正段落和负段落。与开放域问答等传统检索任务（Fan et al., 2019; Kwiatkowski et al., 2019）不同——那些任务的检索池通常包含直接回答查询的文档——我们模拟一种现实场景：正文档只提供有用信息，帮助用户推导出答案。数据集构造的更多细节见附录 B.1。

标注过程由一名计算机科学学生做初始标注，然后由两名相应领域的博士生核验。只有获得所有相关方——原始标注者和两名专家审阅者——一致批准的标注，才保留在最终数据集中。这一批准过程同时适用于正文档和负文档标注，以保证标注例子的高准确性和可靠性。给标注者的更多指南见附录 F。

### 3.3 编程：检索文档或相似的已解问题

**相关性：** 查询与正文档之间的相关性由编程问题（即查询）是否需要对应的语法文档、或是否涉及相同的算法和/或数据结构来定义。

<!-- 原 PDF 第 6 页 -->

为解决一道编程题，程序员常常需要查阅文档，或找到共享相同算法设计的相似问题。然而，只给定问题描述，很难通过简单的关键词或语义匹配找到相关文档或相似问题。我们构造两个编程检索数据集，查询与文档之间的相关性奠基于语法用法和算法设计。

**Pony。** 在使用一种罕见编程语言时，查阅手册对于理解其语法和函数用法可能非常有价值。然而在这种情况下，问题描述很可能与相关文档的语义相似度和词汇重叠都很低。这种差异使得识别与手头问题相关的特定语法或函数需要密集推理。我们采用一个以 Pony（Su et al., 2024）为特色的代码生成数据集——Pony 是一种罕见编程语言——并构造一个检索数据集。我们把编程问题的指令用作查询 $Q$，把关于所需语法的标注文档用作正文档 $D_Q^+$，并把完整的语言手册用作文档检索池 $D$，其中每个 $D_i$ 包含关于 Pony 语法用法的描述，例如条件、循环和类。

**LeetCode。** 我们也探索处理算法和数据结构的编程问题，目标是检索共享相同算法设计的问题和解答。我们从 LeetCode 获取编程问题和解答。【脚注 6】问题描述用作查询 $Q$，正文档 $D_Q^+$ 是被 LeetCode 标注为相似问题的已解问题（带解答）。来自 LeetCode 的每篇文档 $D_i = (Q_i, A_i)$ 包含问题陈述 $Q_i$ 和一段 Python 解答 $A_i$。为增加难度，我们只保留扎根于真实世界场景的问题，到达关键算法或数据结构需要密集推理。我们通过合并来自 LeetCode 的问题与解答以及来自 CodeSearchNet（Husain et al., 2019）的 Python 代码，构造一个大语料 $D$。数据集的更多细节见附录 B.6。

【脚注 6】https://leetcode.com/

### 3.4 基于定理的问题：检索使用相同定理的已解问题，或相关定理陈述

**相关性：** 一个查询（即一道已解问题）与一篇文档相关，如果该文档引用了查询中使用的同一条定理。

在处理一道新的数学或物理问题时，用户常常参考先前已解的问题，或直接查阅相关定理陈述来引导推理。检索这类相似问题或定理可能有挑战，因为共享相同底层逻辑的问题在表面形式上可能差异很大，如表 30 所示。在这一设定中，查询 $Q$ 是一道基于定理的问题，语料 $D$ 由已解的 STEM 问题 $D_i = (Q_i, A_i)$ 组成，其中 $Q_i$ 是问题陈述、$A_i$ 是其解答，或者 $D_i$ 是来自 ProofWiki 等形式定理集合的定理文档。若 $D_i$ 与查询的解答共享同一条定理，我们把它视为正文档。该数据集由高质量 STEM 来源构建（Cobbe et al., 2021; Yuan et al., 2023; Hendrycks et al., 2021; Ling et al., 2017; Chen et al., 2023a; Li et al., 2023a），语料构造细节见附录 B.2。

**TheoremQA。** 源自教科书、在线资源和专家，TheoremQA（Chen et al., 2023b）包含基于特定数学或科学定理（例如二项式定理）的问题，代表学生和其他用户在学习中可能遇到的问题。为确保模型不只是依赖问题的表面措辞，我们用 GPT-4【脚注 7】把问题改写成更具体的应用场景，同时保持所需的同一条定理。用于改写问题的提示和一个例子见表 13。人类标注者仔细审阅改写后的问题，并做必要修订，以确保它们有效且与原问题一致。一篇文档 $D_i = (Q_i, A_i)$ 为正，如果 $A_i$ 使用与查询解答相同的定理。更多细节见附录 B.3。

**AoPS。** 数学竞赛问题已被广泛用于评估学生和 LLM 的问题求解技能（Hendrycks et al., 2021）。源自美国和国际数学奥林匹克，这些问题常常需要应用高级数学定理和技巧，例如费马小定理或托勒密定理。为备考，学生常常通过求解需要相同问题求解技能的其他问题来学习。为此，我们收集一个新的数学竞赛问题数据集，称为 AoPS，并用 AoPS Wiki 上各自的问题求解技能加以标注。【脚注 8】收集到的问题求解技能见表 18。与 TheoremQA 类似，若一道已解数学问题 $D_i = (Q_i, A_i)$ 的解答使用与查询解答相同的问题求解技能，我们就把它视为正例。从初步定性分析中，我们发现竞赛问题被刻意写成多样的方式，使得识别所需技巧具有挑战；因此我们不改写问题陈述。细节见附录 B.5。

【脚注 7】本工作中 GPT-4 指版本 gpt-4-0125-preview。

【脚注 8】https://artofproblemsolving.com/wiki/

<!-- 原 PDF 第 7 页 -->

**定理检索。** 除相似问题外，检索相关定理定义也有帮助。我们使用前述 TheoremQA 数据集的查询，但换一个语料 $D$，其中每篇文档 $D_i$ 是来自 ProofWiki 的一条定理陈述。【脚注 9】我们用标题匹配把 TheoremQA 中的定理与 ProofWiki 文档对齐，随后用 GPT-4 验证，以确保候选定理被用在解答中。我们只保留至少有一条相关定理陈述的查询。问题与文档之间相关性的人工标注也显示，人类标注者与 GPT-4 之间有实质性一致（Cohen 的 $\kappa = 0.62$）。细节见附录 B.4。

【脚注 9】proofwiki.org；一个收录超过 2 万条数学定理形式定义与证明的集合。

## 4 实验

### 4.1 实验设定

我们评估 13 个代表性检索模型，从传统词袋模型到大型稠密检索模型，包括 MTEB 排行榜检索集合（Muennighoff et al., 2023）、BEIR（Thakur et al., 2021）上的顶尖表现者。首先，我们采用 BM25（Robertson et al., 2009）作为主要的稀疏、基于词汇的检索模型，它在 BEIR（Thakur et al., 2021）上表现出与更大的已训练稠密检索模型相当的强性能。我们也评估一组多样的开源稠密检索模型：小模型（<1B）是 SentenceBERT（1.09 亿；Reimers & Gurevych, 2019）、BGE（3.35 亿；Xiao et al., 2023）和 Instructor-Large（3.35 亿；Su et al., 2022）；大模型（>1B）是 Instructor-XL（15 亿；Su et al., 2022）、E5-Mistral（71 亿；Wang et al., 2023a）、SFR-Embedding-Mistral（71 亿；Meng et al., 2024）、GritLM（71 亿；Muennighoff et al., 2024）和 gte-Qwen1.5（77 亿；Li et al., 2023b）。值得注意的是，所有大型稠密模型和 Instructor-Large 都经过指令调优。最后，我们纳入来自 Cohere（Cohere）、Voyage（Voyage AI）、OpenAI（OpenAI）和 Google（12 亿）（Lee et al., 2024）的专有模型。每个模型的细节见附录 A.1。遵循先前工作（Thakur et al., 2021; Bajaj et al., 2018; Voorhees & Tice, 2000），我们用 NDCG@10 作为主指标。计算资源见附录 A.2。

**表 2：检索模型在 BRIGHT 上的性能。** 我们报告全部数据集的 NDCG@10：Biology（Bio.）、Earth Science（Earth.）、Economics（Econ.）、Psychology（Psy.）、Robotics（Rob.）、Stack Overflow（Stack.）、Sustainable Living（Sus.）、LeetCode（Leet.）、Pony、AoPS、TheoremQA 问题检索（TheoQ.）和定理检索（TheoT.）。Avg. 表示 12 个数据集上的平均分。每个数据集上的最佳分数在原文中加粗，次佳加下划线。推理密集型检索对当前检索器是有挑战的，最佳模型平均 NDCG@10 只有 24.3。模型细节见附录 A.1。数值按 `get_text` 逐列还原。

| 模型 | Bio. | Earth. | Econ. | Psy. | Rob. | Stack. | Sus. | Leet. | Pony | AoPS | TheoQ. | TheoT. | Avg. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BM25 | 18.9 | 27.2 | 14.9 | 12.5 | 13.6 | 18.4 | 15.0 | 24.4 | 7.9 | 6.2 | 10.4 | 4.9 | 14.5 |
| BGE | 11.7 | 24.6 | 16.6 | 17.5 | 11.7 | 10.8 | 13.3 | 26.7 | 5.7 | 6.0 | 13.0 | 6.9 | 13.7 |
| Inst-L | 15.2 | 21.2 | 14.7 | 22.3 | 11.4 | 13.3 | 13.5 | 19.5 | 1.3 | 8.1 | 20.9 | 9.1 | 14.2 |
| SBERT | 15.1 | 20.4 | 16.6 | 22.7 | 8.2 | 11.0 | 15.3 | 26.4 | 7.0 | 5.3 | 20.0 | 10.8 | 14.9 |
| E5 | 18.6 | 26.0 | 15.5 | 15.8 | 16.3 | 11.2 | 18.1 | 28.7 | 4.9 | 7.1 | 26.1 | 26.8 | 17.9 |
| SFR | 19.1 | 26.7 | 17.8 | 19.0 | 16.3 | 14.4 | 19.2 | 27.4 | 2.0 | 7.4 | 24.3 | 26.0 | 18.3 |
| Inst-XL | 21.6 | 34.3 | 22.4 | 27.4 | 18.2 | 21.2 | 19.1 | 27.5 | 5.0 | 8.5 | 15.6 | 5.9 | 18.9 |
| GritLM | 24.8 | 32.3 | 18.9 | 19.8 | 17.1 | 13.6 | 17.8 | 29.9 | 22.0 | 8.8 | 25.2 | 21.2 | 21.0 |
| Qwen | 30.6 | 36.4 | 17.8 | 24.6 | 13.2 | 22.2 | 14.8 | 25.5 | 9.9 | 14.4 | 27.8 | 32.9 | 22.5 |
| Cohere | 18.7 | 28.4 | 20.4 | 21.6 | 16.3 | 18.3 | 17.6 | 26.8 | 1.9 | 6.3 | 15.7 | 7.2 | 16.6 |
| OpenAI | 23.3 | 26.7 | 19.5 | 27.6 | 12.8 | 14.3 | 20.5 | 23.6 | 2.4 | 8.5 | 23.5 | 11.7 | 17.9 |
| Voyage | 23.1 | 25.4 | 19.9 | 24.9 | 10.8 | 16.8 | 15.4 | 30.6 | 1.5 | 7.5 | 27.4 | 11.6 | 17.9 |
| Google | 22.7 | 34.8 | 19.6 | 27.8 | 15.7 | 20.1 | 17.1 | 29.6 | 3.6 | 9.3 | 23.8 | 15.9 | 20.0 |

原文把 Qwen 的平均分写成 22.5，但摘要中另称 SFR 的 NDCG@10 为 18.3，与本表 SFR 的 Avg. 一致。正文第 8 页说最佳模型只有 24.3，与本表中任何一行的 Avg. 都不相同；24.3 更接近后文使用推理步骤后的结果。此处按表内数字照录。

<!-- 原 PDF 第 8 页 -->

### 4.2 主要结果

**现有检索系统在 BRIGHT 上表现差。** 表 2 的结果表明 BRIGHT 非常有挑战，最佳模型只达到 24.3 的 NDCG@10（正文如此表述）。虽然 BM25 与小于 10 亿参数的模型相当，它显著低于更大的模型。这表明传统关键词匹配（“第 1 级搜索”）对 BRIGHT 是不够的。虽然在 MS MARCO 等基于语义的检索数据集上训练过的更大模型（图 1），例如 GritLM（Muennighoff et al., 2024），表现优于 BM25，它们仍然无法解决 BRIGHT。专有模型的表现与大型开源模型相似。总体而言，低性能表明现有检索系统不能做推理密集型检索，需要新方法来解决“第 3 级搜索”。

**用 LLM 推理步骤做查询会改善检索性能。** 考虑到 LLM 的强推理能力，我们提出：把 LLM 生成的推理步骤用作查询，可能增强检索性能。为验证这一假设，我们用如下提示让 LLM 给定查询后写出推理轨迹：“（1）识别帖子中的核心问题。（2）逐步思考相关文档中应当包含什么。（3）起草一个答案。”我们鼓励 LLM 先通过摘要来理解问题，然后用思维链推理（Wei et al., 2022）识别相关内容，最后写出一个候选答案。然后我们把这些增强了推理的文本用作新查询，来评估全部检索模型。我们使用 GPT-4【脚注 10】、GritLM（Muennighoff et al., 2024）和 Llama-3-70B-Instruct【脚注 11】来生成推理步骤。图 3 表明，用 Llama-3-70B 或 GPT-4 的推理步骤作为查询，相对于原始查询显著改善性能（详细分数见表 34 至表 38）。GritLM 生成的推理步骤改善了 BM25 的性能，但对其他模型效果较差，可能是因为参数更少。总体而言，BM25 提升最多，可能因为 BM25 能适应不同查询，而 LLM 生成的查询对已训练模型是分布外的。最佳分数仍低于 30，BRIGHT 上仍有显著的改进空间。

【脚注 10】gpt-4-0125-preview

【脚注 11】https://huggingface.co/meta-llama/Meta-Llama-3-70B-Instruct

**检索增强提升问答中的性能。** 检索的一项重要应用是最终改善问答（QA）结果。在处理一篇 StackExchange 帖子时，一条典型流水线是先检索有用文档，然后利用检索到的内容回答问题。虽然第二步可能涉及推理过程来推导答案，我们强调第一步中为找到文档而做的密集推理。我们评估 Claude-3.5-sonnet 在被不同模型检索到的文档增强时的端到端 QA 性能，并用 Claude-3.5-sonnet 评估答案正确性。如表 4 所示，更强的检索器通常带来更好的 QA 性能，表现最好的检索器 Qwen 取得 1.9 个点的增益。然而，使用预言文档把性能提升 4.1 个点，凸显推理密集型检索在增强下游 QA 结果上仍有大量改进空间。TheoremQA 和 AoPS 数据集上的类似实验见附录 E。

**表 4：使用不同检索器的问答结果。** 我们用 Claude-3.5-sonnet 作为生成模型，并用 Claude-3.5-sonnet 评估答案。我们发现更强的检索通常带来更好的 QA 结果，表明标注文档有助于处理 StackExchange 帖子。

| 检索器 | Bio. | Earth. | Econ. | Psy. | Rob. | Stack. | Sus. | 平均 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 无 | 79.4 | 82.3 | 75.6 | 74.5 | 76.7 | 81.8 | 73.5 | 77.7 |
| BM25 | 78.2 | 82.6 | 76.3 | 78.2 | 76.3 | 83.0 | 73.6 | 78.3 |
| SBERT | 79.6 | 82.5 | 75.8 | 80.6 | 77.0 | 83.4 | 74.1 | 79.0 |
| Qwen | 80.2 | 83.5 | 77.0 | 81.1 | 77.2 | 85.8 | 72.6 | 79.6 |
| 预言 | 82.4 | 84.5 | 78.3 | 82.4 | 78.5 | 87.9 | 78.6 | 81.8 |

虽然更好的检索质量与更高的 QA 性能相关，QA 结果可能并不总是准确捕捉检索性能，原因如下：1）生成模型可能不能有效理解或把检索文档整合进其响应；2）评估者可能不能充分识别两个开放式答案之间的异同。LLM 所用的推断和评估提示见表 45 和表 46。

<!-- 原 PDF 第 9 页 -->

**图 3 见原 PDF。** 图 3：在 BRIGHT 上使用原始查询，对比使用由 GritLM、Llama3-70B 和 GPT-4 生成的推理步骤做检索时的平均 NDCG@10。用 LLM 推理步骤搜索显著改善性能。令人惊讶的是，BM25 在把 GPT-4 写出的推理步骤用作新查询的排行榜上取得最佳性能。详细分数见表 34 至表 38。图为柱状图，柱高数值未从默认 `find_tables` 抽齐（该页表格空白单元格比例很高）。图抽取失败，见原 PDF 第 9 页。

**表 3：BRIGHT 上的平均重排序性能。** 我们也纳入检索结果（重排序器为无）以便比较。详细分数见表 41 和表 42。

| 检索器 | 重排序器 | $k$ | NDCG@10 |
| --- | --- | --- | --- |
| BM25 | 无 | — | 14.3 |
| BM25 | MiniLM | 10 | 13.1 |
| BM25 | MiniLM | 100 | 8.3 |
| BM25 | Gemini | 10 | 15.7 |
| BM25 | GPT-4 | 10 | 17.4 |
| BM25 | GPT-4 | 100 | 17.0 |
| Google | 无 | — | 19.5 |
| Google | MiniLM | 10 | 16.0 |
| Google | MiniLM | 100 | 9.4 |
| Google | Gemini | 10 | 20.1 |
| Google | GPT-4 | 10 | 21.5 |
| Google | GPT-4 | 100 | 22.6 |

## 5 分析

### 5.1 用 LLM 重排序增强检索性能

改善检索结果的一种常见做法是利用能够在查询和文档上做联合计算的强大重排序器。为此，我们考察 BRIGHT 上的性能能否通过重排序得到改善。我们用一个经典交叉编码器 MiniLM【脚注 12】以及 LLM，对检索到的前 $k \in \{10, 100\}$ 篇文档做重排序来测试这一点。交叉编码器在 MS MARCO 重排序任务（Bajaj et al., 2016）上训练，并为每一对查询和文档 $(Q, D_i)$ 输出一个相关性分数。遵循 Sun 等人（2023），我们也用 LLM 重排序：把查询和前 $k$ 篇文档放进提示，并要求 LLM 根据文档与查询的相关性对文档排序（详细提示见表 43）。表 3 表明，传统交叉编码器对检索质量有负面影响，随着被重排序的文档增多，性能下降，提示在 MS MARCO 上训练重排序器不能很好地迁移到 BRIGHT。另一方面，由 LLM 做重排序通常增强性能。更强的 LLM 提供更显著的改进；例如，基于 BM25 检索结果，Gemini-1.0 重排序把分数提高 1.4，GPT-4 重排序提高 3.1，并且随 $k$ 增大继续改进。LLM 可以作为推理密集型检索的有效工具，但最终结果仍然高度依赖底层检索系统。

【脚注 12】https://huggingface.co/cross-encoder/ms-marco-MiniLM-L-12-v2

<!-- 原 PDF 第 10 页 -->

### 5.2 对预训练数据泄漏的稳健性

许多现有基准由于大规模预训练期间的基准数据污染而性能虚高（Zhou et al., 2023; Xu et al., 2024）。我们表明，即便检索文档在预训练期间被完全暴露，BRIGHT 对这种数据泄漏仍然稳健。为测试这一点，我们模拟一种现实场景：语言模型在基于互联网的训练期间遇到 StackExchange 数据。我们在来自检索池的 StackExchange 数据上继续训练 GritLM（Muennighoff et al., 2024），同时使用语言建模损失和问答对上的对比学习（训练细节见附录 A.3）。这一做法使模型接触到 BRIGHT 中的全部 StackExchange 内容，同时避免直接在需要密集推理的查询–文档映射上训练。如表 5 所示，微调后的 GritLM 只表现出轻微的性能下降，提示常规训练过程对 BRIGHT 性能的影响有限。这些结果展示了 BRIGHT 对预训练数据泄漏的稳健性，并凸显需要新方法来推进推理密集型检索。

**表 5：BRIGHT 对大规模预训练是稳健的。** 通过在 StackExchange 数据上继续训练 GritLM，而不展示查询与文档之间的映射，模型在学习领域内知识之后并没有提高平均性能，表明推理能力在检索过程中的重要性。

| 模型 | Bio. | Earth. | Econ. | Psy. | Rob. | Stack. | Sus. | 平均 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GritLM | 25.0 | 32.8 | 19.0 | 19.9 | 17.3 | 11.6 | 18.0 | 20.5 |
| 微调后的 GritLM | 21.1 | 25.5 | 18.8 | 30.7 | 12.7 | 12.1 | 21.9 | 20.4 |

### 5.3 搜索空间缩小后的长上下文检索仍然有挑战

从长文档中检索信息对法律合同、公司财务文件和病历等应用至关重要（Saad-Falcon et al., 2024; Zhu et al., 2024）。为在涉及长文档的推理密集型任务上评估检索模型，我们把 StackExchange 数据集转换成长上下文检索设定：文档是完整网页，词元显著更多，但文档总数更少（表 40）。由于大多数数据集只含几百篇文档，评估前 10 个结果的 NDCG@10 更容易受随机性影响。此外，处理平均长度高达 40,000 词元的 10 篇长文档，对人类和 LLM 都有挑战。因此，我们决定在这一设定中使用 Recall@1 指标，以提供更可靠的度量。表 6 给出 StackExchange 和 Pony 共 8 个数据集的平均分。达到的最高 Recall 是 27.8，表明即便检索池显著缩小，长上下文文档与密集推理的组合对现有检索模型仍然有挑战。

**表 6：检索器从未切分网页中检索时的长上下文检索性能。** 结果报告为 StackExchange 和 Pony 数据集的平均 Recall@1。更详细的数字见表 39。

| BM25 | BGE | Inst-L | SBERT | E5 | SFR | Inst-XL | GritLM | Qwen | Cohere | OpenAI | Voyage | Google |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 11.4 | 14.8 | 18.2 | 17.4 | 25.5 | 26.0 | 17.8 | 26.0 | 27.8 | 18.4 | 21.9 | 24.6 | 22.4 |

## 6 结论

我们引入 BRIGHT，第一个涵盖现实检索场景的检索基准，识别相关文档需要密集推理步骤。我们利用现有的在线文档结构，并投入大量人力来整理 BRIGHT 并核验其正确性。通过广泛评估，我们发现现有检索模型在 BRIGHT 上表现极差，最高 NDCG@10 只有 24.3。用 LLM 生成的推理步骤增强检索查询会改善性能，但即便最佳模型的分数仍低于 30。此外，强检索结果可以显著改善推理任务上的下游性能，凸显了推理密集型检索的一项实际应用。我们希望 BRIGHT 将有助于未来研究，推动这一方向的最新水平。

<!-- 原 PDF 第 11 页 -->

## 致谢

我们感谢 Adithya Bhaskar、Catherine Chen、Howard Chen、Tianyu Gao、Lucy He 以及 Princeton Language and Intelligence 的其他成员提供有益反馈和讨论。我们也感谢 Qilin Liao、Yun Han、Xiaoru Teng、Cong Gao、Shengyu Wang、Xiaodong Wei 和 Yan Pan 标注并审阅数据集。本工作得到一项 NSF CAREER 奖（IIS-2239290）以及 Microsoft Accelerate Foundation Models Research（AFMR）资助计划的支持。

## 伦理准则与伦理声明

在为 BRIGHT 收集数据集的过程中，我们确保全部来源来自公共数据，仅用于学术研究而非商业目的，完全遵守来源所授予的版权。我们保证数据集中都不含对社会有害的信息，例如种族歧视、暴力或任何私人数据。我们的工作旨在增进社会与人类的福祉，任何研究者都可以自由地把我们的数据集用于研究目的。论文中呈现的全部数据和实验都遵守科学卓越的最高标准，保证数据的真实性与准确性。

## 可复现性

我们的数据集和标注过程在第 3 节介绍，实验设定在第 4 节描述。具体实现细节见附录 A。为便于复现实验，代码和数据提供于 https://brightbenchmark.github.io/ 。

## 参考文献

Akari Asai, Zexuan Zhong, Danqi Chen, Pang Wei Koh, Luke Zettlemoyer, Hanna Hajishirzi, and Wen tau Yih. 可靠、可适应且可归属的带检索语言模型. 2024. 原 PDF 第 11 页该条与另一引文粘连，抽取串保留：url https://api. semanticscholar. org/corpusid: 268248911. oprea, and colin raffel. extracting training data from large language models. In USENIX Security Symposium (USENIX), 2020.

Akari Asai, Timo Schick, Patrick Lewis, Xilun Chen, Gautier Izacard, Sebastian Riedel, Hannaneh Hajishirzi, and Wen-tau Yih. 带指令的任务感知检索. In Findings of the Association for Computational Linguistics: ACL 2023, pp. 3650–3675, Toronto, Canada, July 2023a. Association for Computational Linguistics.

Akari Asai, Zeqiu Wu, Yizhong Wang, Avirup Sil, and Hannaneh Hajishirzi. Self-RAG：通过自我反思学习检索、生成与批评. In The Twelfth International Conference on Learning Representations, 2023b.

Akari Asai, Zexuan Zhong, Danqi Chen, Pang Wei Koh, Luke Zettlemoyer, Hannaneh Hajishirzi, and Wen tau Yih. 可靠、可适应且可归属的带检索语言模型, 2024.

Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Bosma, Henryk Michalewski, David Dohan, Ellen Jiang, Carrie Cai, Michael Terry, Quoc Le, et al. 用大语言模型做程序合成. arXiv preprint arXiv:2108.07732, 2021.

Payal Bajaj, Daniel Campos, Nick Craswell, Li Deng, Jianfeng Gao, Xiaodong Liu, Rangan Majumder, Andrew McNamara, Bhaskar Mitra, Tri Nguyen, et al. MS MARCO：一个由人生成的机器阅读理解数据集. arXiv preprint arXiv:1611.09268, 2016.

Payal Bajaj 等. MS MARCO：一个由人生成的机器阅读理解数据集, 2018.

<!-- 原 PDF 第 12 页 -->

Sebastian Borgeaud 等. 通过从万亿词元中检索来改进语言模型. In International Conference on Machine Learning (ICML), volume 162, pp. 2206–2240, 2022.

Danqi Chen, Adam Fisch, Jason Weston, and Antoine Bordes. 阅读维基百科以回答开放域问题. In Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 1870–1879, Vancouver, Canada, July 2017. Association for Computational Linguistics.

Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al. 评估在代码上训练的大语言模型. arXiv preprint arXiv:2107.03374, 2021.

Wenhu Chen, Ming Yin, Max Ku, Pan Lu, Yixin Wan, Xueguang Ma, Jianyu Xu, Xinyi Wang, and Tony Xia. TheoremQA：一个由定理驱动的问答数据集. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pp. 7889–7901, Singapore, December 2023a. Association for Computational Linguistics.

Wenhu Chen 等. TheoremQA：一个由定理驱动的问答数据集. In The 2023 Conference on Empirical Methods in Natural Language Processing, 2023b.

Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John Schulman. 训练验证器来求解数学应用题, 2021.

Cohere. Cohere-embed-english-light-v3.0, 2022.

Nick Craswell, Bhaskar Mitra, Emine Yilmaz, Daniel Campos, and Ellen M. Voorhees. TREC 2019 深度学习赛道概述, 2020.

Tri Dao. FlashAttention-2：用更好的并行与工作划分做更快的注意力. In International Conference on Learning Representations (ICLR), 2024.

Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, and Christopher Ré. FlashAttention：具有 IO 意识的快速且内存高效的精确注意力. In Advances in Neural Information Processing Systems (NeurIPS), 2022.

Thomas Diggelmann, Jordan Boyd-Graber, Jannis Bulian, Massimiliano Ciaramita, and Markus Leippold. Climate-FEVER：一个用于验证真实世界气候主张的数据集. arXiv preprint arXiv:2012.00614, 2020.

Angela Fan, Yacine Jernite, Ethan Perez, David Grangier, Jason Weston, and Michael Auli. ELI5：长形式问答. arXiv preprint arXiv:1907.09190, 2019.

Tianyu Gao, Howard Yen, Jiatong Yu, and Danqi Chen. 使大语言模型能够生成带引用的文本. In Empirical Methods in Natural Language Processing (EMNLP), 2023.

Faegheh Hasibi, Fedor Nikolaev, Chenyan Xiong, Krisztian Balog, Svein Erik Bratsberg, Alexander Kotov, and Jamie Callan. DBpedia-Entity v2：一个实体搜索测试集. In Proceedings of the 40th International ACM SIGIR Conference on Research and Development in Information Retrieval, pp. 1265–1268, 2017.

<!-- 原 PDF 第 13 页 -->

Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and Jacob Steinhardt. 用 MATH 数据集衡量数学问题求解. In Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2), 2021.

Hamel Husain, Ho-Hsiang Wu, Tiferet Gazit, Miltiadis Allamanis, and Marc Brockschmidt. CodeSearchNet 挑战：评估语义代码搜索的现状. arXiv preprint arXiv:1909.09436, 2019.

Gautier Izacard, Mathilde Caron, Lucas Hosseini, Sebastian Riedel, Piotr Bojanowski, Armand Joulin, and Edouard Grave. 用对比学习做无监督稠密信息检索. Transactions on Machine Learning Research, 2022.

Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun Zhang, Sida Wang, Armando Solar-Lezama, Koushik Sen, and Ion Stoica. LiveCodeBench：面向代码的大语言模型整体且无污染评估. arXiv preprint arXiv:2403.07974, 2024.

Vladimir Karpukhin, Barlas O˘guz（原 PDF 第 13 页抽取串，变音符号乱码）, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, and Wen-tau Yih. 面向开放域问答的稠密段落检索. arXiv preprint arXiv:2004.04906, 2020.

Tom Kwiatkowski 等. Natural Questions：问答研究的一个基准. Transactions of the Association for Computational Linguistics, 7:453–466, 2019.

Jinhyuk Lee 等. Gecko：从大语言模型蒸馏出的通用文本嵌入. arXiv preprint arXiv:2403.20327, 2024.

Kenton Lee, Ming-Wei Chang, and Kristina Toutanova. 面向弱监督开放域问答的潜在检索. In Association for Computational Linguistics (ACL), pp. 6086–6096, 2019.

Guohao Li, Hasan Abed Al Kader Hammoud, Hani Itani, Dmitrii Khizbullin, and Bernard Ghanem. CAMEL：用于大语言模型社会之“心智”探索的交流智能体. In Thirty-seventh Conference on Neural Information Processing Systems, 2023a.

Zehan Li, Xin Zhang, Yanzhao Zhang, Dingkun Long, Pengjun Xie, and Meishan Zhang. 通过多阶段对比学习走向通用文本嵌入. arXiv preprint arXiv:2308.03281, 2023b.

Zhuoqun Li 等. URL：经由任务指令表示压缩的通用指称知识链接. arXiv preprint arXiv:2404.16248, 2024.

Wang Ling, Dani Yogatama, Chris Dyer, and Phil Blunsom. 通过生成理由做程序归纳：学习求解并解释代数应用题. In Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 158–167, Vancouver, Canada, July 2017. Association for Computational Linguistics.

Macedo Maia 等. WWW’18 开放挑战：金融观点挖掘与问答. In Companion proceedings of the the web conference 2018, pp. 1941–1942, 2018.

Rui Meng, Ye Liu, Shafiq Rayhan Joty, Caiming Xiong, Yingbo Zhou, and Semih Yavuz. SFR-Embedding-Mistral：用迁移学习增强文本检索. Salesforce AI Research Blog, 3, 2024.

Niklas Muennighoff. SGPT：用于语义搜索的 GPT 句子嵌入. arXiv preprint arXiv:2202.08904, 2022.

<!-- 原 PDF 第 14 页 -->

Niklas Muennighoff, Nouamane Tazi, Loic Magne, and Nils Reimers. MTEB：大规模文本嵌入基准. In Proceedings of the 17th Conference of the European Chapter of the Association for Computational Linguistics, pp. 2014–2037, Dubrovnik, Croatia, May 2023. Association for Computational Linguistics.

Niklas Muennighoff, Hongjin Su, Liang Wang, Nan Yang, Furu Wei, Tao Yu, Amanpreet Singh, and Douwe Kiela. 生成式表示指令调优. arXiv preprint arXiv:2402.09906, 2024.

Hanseok Oh, Hyunji Lee, Seonghyeon Ye, Haebin Shin, Hansol Jang, Changwook Jun, and Minjoon Seo. InstructIR：信息检索模型指令遵循的一个基准, 2024.

OpenAI. 新的嵌入模型与 API 更新, 2024.

Fabio Petroni 等. KILT：知识密集型语言任务的一个基准. In Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, pp. 2523–2544, Online, June 2021. Association for Computational Linguistics.

Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, Ilya Sutskever, et al. 语言模型是无监督的多任务学习者. OpenAI blog, 1(8):9, 2019.

Nils Reimers and Iryna Gurevych. Sentence-BERT：用孪生 BERT 网络做句子嵌入. arXiv preprint arXiv:1908.10084, 2019.

Stephen Robertson, Hugo Zaragoza, et al. 概率相关性框架：BM25 及其延伸. Foundations and Trends® in Information Retrieval, 3(4):333–389, 2009.

Jon Saad-Falcon, Daniel Y Fu, Simran Arora, Neel Guha, and Christopher Ré. 用 LoCo 和 M2-BERT 基准测试并构建长上下文检索模型. arXiv preprint arXiv:2402.07440, 2024.

Weijia Shi, Sewon Min, Michihiro Yasunaga, Minjoon Seo, Rich James, Mike Lewis, Luke Zettlemoyer, and Wen tau Yih. REPLUG：检索增强的黑盒语言模型, 2024.

Hongjin Su 等. 一个嵌入器，任何任务：指令微调的文本嵌入. arXiv preprint arXiv:2212.09741, 2022.

Hongjin Su 等. 一个嵌入器，任何任务：指令微调的文本嵌入. In Findings of the Association for Computational Linguistics: ACL 2023, pp. 1102–1121, Toronto, Canada, July 2023. Association for Computational Linguistics.

Hongjin Su, Shuyang Jiang, Yuhang Lai, Haoyuan Wu, Boao Shi, Che Liu, Qian Liu, and Tao Yu. ARKS：知识浓汤中面向代码生成的主动检索. arXiv preprint arXiv:2402.12317, 2024.

Weiwei Sun, Lingyong Yan, Xinyu Ma, Pengjie Ren, Dawei Yin, and Zhaochun Ren. ChatGPT 擅长搜索吗？把大语言模型作为重排序智能体来考察. arXiv preprint arXiv:2304.09542, 2023.

Nandan Thakur, Nils Reimers, Andreas Rücklé, Abhishek Srivastava, and Iryna Gurevych. BEIR：信息检索模型零样本评估的异质基准. arXiv preprint arXiv:2104.08663, 2021.

<!-- 原 PDF 第 15 页 -->

James Thorne, Andreas Vlachos, Christos Christodoulopoulos, and Arpit Mittal. FEVER：一个大规模事实抽取与验证数据集. arXiv preprint arXiv:1803.05355, 2018.

Ellen M. Voorhees and Dawn M. Tice. 构建一个问答测试集. In Proceedings of the 23rd Annual International ACM SIGIR Conference on Research and Development in Information Retrieval, SIGIR ’00, pp. 200–207, New York, NY, USA, 2000. Association for Computing Machinery.

Voyage AI. 嵌入, 2024.

David Wadden 等. 事实还是虚构：验证科学主张. arXiv preprint arXiv:2004.14974, 2020.

Liang Wang, Nan Yang, Xiaolong Huang, Linjun Yang, Rangan Majumder, and Furu Wei. 用大语言模型改进文本嵌入. arXiv preprint arXiv:2401.00368, 2023a.

Xiaoyue Wang, Jianyou Wang, Weili Cao, Kaicheng Wang, Ramamohan Paturi, and Leon Bergen. BIRCO：带复杂目标的信息检索任务基准. arXiv preprint arXiv:2402.14151, 2024.

Zengzhi Wang, Rui Xia, and Pengfei Liu. 用于数学的生成式 AI：第一部分——MathPile：一个十亿词元规模的数学预训练语料, 2023b.

Jason Wei 等. 思维链提示激发大语言模型中的推理. Advances in neural information processing systems, 35:24824–24837, 2022.

Orion Weller 等. FollowIR：评估并教会信息检索模型遵循指令. arXiv preprint arXiv:2403.15246, 2024.

Chenghao Xiao, G Thomas Hudson, and Noura Al Moubayed. RAR-b：把推理当作检索的基准, 2024.

Shitao Xiao, Zheng Liu, Peitian Zhang, and Niklas Muennighoff. C-Pack：推进通用中文嵌入的打包资源, 2023.

Ruijie Xu, Zengzhi Wang, Run-Ze Fan, and Pengfei Liu. 在大语言模型中基准测试基准泄漏. arXiv preprint arXiv:2404.18824, 2024.

Kaiyu Yang 等. LeanDojo：用检索增强语言模型做定理证明, 2023.

Zhilin Yang 等. HotpotQA：一个多样、可解释的多跳问答数据集. arXiv preprint arXiv:1809.09600, 2018.

Zheng Yuan 等. 用大语言模型学习数学推理的缩放关系, 2023.

Xiang Yue, Xingwei Qu, Ge Zhang, Yao Fu, Wenhao Huang, Huan Sun, Yu Su, and Wenhu Chen. MAmmoTH：通过混合指令调优构建数学通才模型, 2023.

Hugh Zhang 等. 对大语言模型在小学算术上表现的仔细考察. arXiv preprint arXiv:2405.00332, 2024.

Kun Zhou 等. 不要让你的 LLM 成为评估基准的作弊者. arXiv preprint arXiv:2311.01964, 2023.

Dawei Zhu 等. LongEmbed：为长上下文检索扩展嵌入模型, 2024.

<!-- 原 PDF 第 16 页 -->

## 目录

1 引言；2 相关工作；3 构造 BRIGHT（3.1 任务形式化；3.2 StackExchange；3.3 编程；3.4 基于定理的问题）；4 实验（4.1 实验设定；4.2 主要结果）；5 分析（5.1 用 LLM 重排序；5.2 对预训练数据泄漏的稳健性；5.3 长上下文检索）；6 结论。附录 A 实验细节；B 数据集构造；C 数据例子；D 推理分类；E 下游性能；F 标注者指令；G 局限与未来工作；H 潜在社会影响；I 与 RAR-b 的比较。

<!-- 原 PDF 第 17 页 -->

## A 实验细节

### A.1 模型与指令

对本文使用的每个模型，表 7 提供规模、架构、查询和文档的最大上下文长度、我们是否纳入指令，以及实验中使用的具体版本。全部参数按官方教程设置。唯一的例外是 Inst-L 和 Inst-XL：我们从经验上发现，把最大上下文长度扩展到 2048 会显著增强性能。在表 8、9、10 和 11 中，我们指定 BGE、Inst-L、Inst-XL、E5、GritLM、Qwen 和 SFR 在每个数据集上使用的指令。对来自 Google 的嵌入模型，我们使用参数 “task”，取值为 “RETRIEVAL_QUERY” 和 “RETRIEVAL_DOCUMENT”，以区分查询与文档；对来自 Voyage 的嵌入模型，使用参数 “input_type”，取值为 “query” 和 “document”。

**表 7：实验中被基准测试的全部 13 个模型。** 我们报告每个模型的参数量，稀疏模型 BM25 和没有公开信息的专有模型除外。关于模型架构，我们区分稀疏与稠密模型，并在已知时进一步把稠密模型分为编码器或解码器。Max $|Q|$ 和 Max $|D|$ 表示实验中我们为每个模型使用的最大上下文长度。指令列表示检索中是否纳入指令。版本列表示具体检查点或实现。

| 模型 | 规模 | 架构 | Max $|Q|$ | Max $|D|$ | 指令 | 版本 | 许可 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BM25 (Robertson et al., 2009) | N/A | 稀疏 | $\infty$ | $\infty$ | 否 | gensim | LGPL-2.1-only |
| SBERT (Reimers & Gurevych, 2019) | 109M | 编码器 | 512 | 512 | 否 | all-mpnet-base-v2 | Apache-2.0 |
| BGE (Xiao et al., 2023) | 335M | 编码器 | 512 | 512 | 否 | bge-large-en-v1.5 | MIT |
| Inst-L (Su et al., 2022) | 335M | 编码器 | 2048 | 2048 | 是 | instructor-large | Apache-2.0 |
| Inst-XL (Su et al., 2022) | 1.5B | 编码器 | 2048 | 2048 | 是 | instructor-xl | Apache-2.0 |
| E5 (Wang et al., 2023a) | 7.1B | 解码器 | 4096 | 4096 | 是 | e5-mistral-7b-instruct | MIT |
| GritLM (Muennighoff et al., 2024) | 7.1B | 解码器 | 256 | 2048 | 是 | GritLM-7B | Apache-2.0 |
| SFR (Meng et al., 2024) | 7.1B | 解码器 | 4096 | 4096 | 是 | SFR-Embedding-Mistral | CC-BY-NC-4.0 |
| Qwen (Li et al., 2023b) | 7.7B | 解码器 | 8192 | 8192 | 是 | gte-Qwen1.5-7B-instruct | Apache-2.0 |
| Cohere | N/A | 稠密 | 512 | 512 | 否 | Cohere-embed-english-v3.0 | 公司 |
| Google (Lee et al., 2024) | 1.2B | 稠密 | 2000 | 2000 | 是 | text-embedding-preview-0409，dimension=768 | 公司 |
| OpenAI | N/A | 稠密 | 8191 | 8191 | 否 | text-embedding-3-large | 公司 |
| Voyage | N/A | 稠密 | 16000 | 16000 | 是 | voyage-large-2-instruct | 公司 |

<!-- 原 PDF 第 18 页 -->

**表 8：用于基准测试 StackExchange 数据集的指令。** {domain} 是 Biology、Earth Science、Economics、Psychology、Robotics、Stack Overflow 和 Sustainable Living 之一。

| 模型 | 指令 |
| --- | --- |
| BGE | 查询：把这篇 {domain} 帖子表示为用于搜索相关段落的向量： |
| Inst-L、Inst-XL | 查询：把这篇 {domain} 帖子表示为用于检索相关段落的向量：文档：把这段 {domain} 段落表示为用于检索的向量： |
| E5、GritLM、Qwen、SFR | 查询：给定一篇 {domain} 帖子，检索有助于回答该帖子的相关段落 |

**表 9：用于基准测试 LeetCode 数据集的指令。**

| 模型 | 指令 |
| --- | --- |
| BGE | 查询：把这道编程题表示为用于搜索相关例子的向量： |
| Inst-L、Inst-XL | 查询：把这道编程题表示为用于检索相关例子的向量：文档：把这个编程例子表示为用于检索的向量： |
| E5、GritLM、Qwen、SFR | 查询：给定一道编程题，检索有助于回答该问题的相关例子 |

**表 10：用于基准测试 Pony 数据集的指令。**

| 模型 | 指令 |
| --- | --- |
| BGE | 查询：把这个 Pony 问题表示为用于搜索相关段落的向量： |
| Inst-L、Inst-XL | 查询：把这个 Pony 问题表示为用于检索相关段落的向量：文档：把这段 Pony 段落表示为用于检索的向量： |
| E5、GritLM、Qwen、SFR | 查询：给定一个 Pony 问题，检索有助于回答该问题的相关段落 |

**表 11：用于基准测试数学数据集（AoPS 和 TheoremQA）的指令。**

| 模型 | 指令 |
| --- | --- |
| BGE | 查询：把这道数学题表示为用于搜索相关例子的向量： |
| Inst-L、Inst-XL | 查询：把这道数学题表示为用于检索相关例子的向量：文档：把这个数学例子表示为用于检索的向量： |
| E5、GritLM、Qwen、SFR | 查询：给定一道数学题，检索有助于回答该问题的相关例子 |

### A.2 计算资源

我们在 NVIDIA V100、A100 或 H100 GPU 上运行全部实验。完成一轮实验所需时间取决于模型。对稀疏模型 BM25，评估在仅 CPU 的机器上不到 1 小时。对开源稠密模型（<1B），评估在一块 H100 GPU 上大约需要 8 小时。对开源稠密模型（>1B），评估在一块 H100 GPU 上最多需要 36 小时。评估稠密模型时，我们利用 FlashAttention（Dao et al., 2022; Dao, 2024）来加速。对专有模型，评估速度取决于 API 带宽，但我们发现一轮实验可以在 2 天内完成。

<!-- 原 PDF 第 19 页 -->

### A.3 持续训练设定

在第 5.2 节中，我们介绍在 StackExchange 数据上持续训练 GritLM 的方法，以评估在领域内数据上训练是否增强 BRIGHT 的性能。详细实验设定在本节描述。具体而言，我们遵循 GritLM，用两个不同目标训练模型：一个对比损失以维持模型的检索能力，一个语言建模损失以保持模型的语言生成能力。对用对比损失的训练，我们从 StackExchange 的 Biology、Earth Science、Economics、Psychology、Robotics 和 Stack Overflow 版块收集 3,200 个（帖子，答案）对，并从 Sustainable Living 收集 1,538 对。每个帖子的答案用作正例，其他答案作为批内负例。对用语言建模损失的训练，我们使用 BRIGHT 的 StackExchange 子部分中每个领域的正文档和负文档。这些文档被切成 2048 词元的块，我们最多采样 3,200 个块用于训练。我们使用较小的批次大小 64，以保证足够的学习步数，同时遵循 Muennighoff 等人（2024）所概述的其他超参数。我们继续训练 GritLM 10 个轮次，并在 BRIGHT 的 StackExchange 数据集上基准测试每一轮的检查点。详细分数见表 12，其中我们把 GritLM 的分数复制到 epoch=0 以便对照。结果表明 10 个轮次中没有显著改进，提示即便在语言模型或检索器的训练数据中密集纳入 StackExchange 数据或相关领域知识，若不增强把推理纳入检索过程，性能也可能不会大幅提高。

【脚注 13】具体而言，我们使用 gensim 的 LuceneBM25Model 和 pyserini 的文本分析器。

**表 12：微调后的 GritLM 在 BRIGHT 的 StackExchange 数据集上每一轮的分数。** Epoch=0 表示未经进一步训练的 GritLM 的性能。

| 轮次 | Bio. | Earth. | Econ. | Psy. | Rob. | Stack. | Sus. | 平均 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0（GritLM） | 25.0 | 32.8 | 19.0 | 19.9 | 17.3 | 11.6 | 18.0 | 20.5 |
| 1 | 22.2 | 25.4 | 17.6 | 28.1 | 11.1 | 9.8 | 19.6 | 19.1 |
| 2 | 18.7 | 23.8 | 13.5 | 19.3 | 10.7 | 10.2 | 16.5 | 16.1 |
| 3 | 20.9 | 23.6 | 16.9 | 25.2 | 11.1 | 8.5 | 16.6 | 17.5 |
| 4 | 24.3 | 28.0 | 18.3 | 26.9 | 13.4 | 13.3 | 20.0 | 20.6 |
| 5 | 23.1 | 28.5 | 18.4 | 26.1 | 14.6 | 11.7 | 21.6 | 20.6 |
| 6 | 19.9 | 26.4 | 16.0 | 27.9 | 9.6 | 9.3 | 19.3 | 18.3 |
| 7 | 24.3 | 25.4 | 16.5 | 28.1 | 11.0 | 9.8 | 17.0 | 18.9 |
| 8 | 21.6 | 28.7 | 19.2 | 28.7 | 11.1 | 11.8 | 22.4 | 20.5 |
| 9 | 21.3 | 29.0 | 20.0 | 28.7 | 11.4 | 14.3 | 22.0 | 21.0 |
| 10 | 21.1 | 25.5 | 18.8 | 30.7 | 12.7 | 12.1 | 21.9 | 20.4 |

<!-- 原 PDF 第 20 页 -->

## B 数据集构造

### B.1 StackExchange

**段落切分。** 为把网页或长文档切成更小的段落，我们采用简单启发式，分隔符如两个换行符、markdown 文件中的 “#”，不对文件结构做额外假设。虽然这种切分对每篇文档可能不是最优的，它模拟了长文档在没有人类或专家干预的情况下被自动处理的现实设定。

**假阳性与假阴性。** 我们讨论在数据收集过程中避免假阳性与假阴性的理由。在 StackExchange 中，查询与文档之间的正相关性由标注者人工核验，并带有详细推理轨迹来说明其思考过程。为避免假阴性，标注者只选择在同一领域中与先前标注例子明显区分的 StackExchange 帖子，例如帖子和答案中的实体与语义都不同。这保证没有任何一对例子共享相同的正文档。

### B.2 用于 TheoremQA 和 AoPS 的 STEM 问题与解答语料

在本小节中，我们描述 STEM 问题与解答语料的构造，它同时用于 TheoremQA 问题和 AoPS。我们从现有数据集获取文档（问题陈述与解答对）$D_i = (Q_i, A_i)$：GSM8K（Cobbe et al., 2021）、GSM8K-RFT（Yuan et al., 2023）、MATH（Hendrycks et al., 2021）、AQuA-RAT（Ling et al., 2017）、TheoremQA（Chen et al., 2023a）和 CAMEL-Math（Li et al., 2023a）。为降低 STEM 语料中的假阴性可能性，我们利用原始数据集的元数据，为每个测试查询从语料中排除特定文档。例如，CAMEL-Math 包含标有类别 “Calculus” 的问题–解答对，涵盖涉及导数和积分的不同问题。因此，对使用 “derivative chain rule” 或 “integral rules” 的 TheoremQA 查询，我们排除类别为 “Calculus” 的 CAMEL-Math 对，以减少可能的假阴性。于是，对 TheoremQA-Q 和 AoPS 中的每个测试查询，我们根据元数据人工决定要排除其他数据集中的哪些标签。由于 GSM8K、GSM8K-RFT 或 AQuA-RAT 的难度相对初级（大多是基础代数问题），而我们的测试查询利用更高级的定理和技巧，我们不从这三个数据集中排除任何问题–解答对。从测试查询类别到被排除的问题–解答类别的映射见表 14、15 和 16。

另一种从语料中为每个测试查询排除假阴性的做法，是检查每一对问题–解答并标注它们是否与测试查询相关。虽然这会得到更难的负例和额外的正例，由于其在每个测试查询与可能候选之间做标注的昂贵代价，我们选择不使用这一做法。原文 “we opt to not to use” 按“我们选择不使用”译。

### B.3 TheoremQA：把问题改写成具体场景

TheoremQA 是一个由定理驱动的问题数据集，涵盖数学、物理、金融、计算机科学和电气工程（Chen et al., 2023a）。对 TheoremQA 中的每个问题，我们把它对应到 MathInstruct 数据集【脚注 14】（Yue et al., 2023），因为该数据集中每个问题都标注了推理步骤和最终答案。

从初步分析中，我们发现 TheoremQA 问题常常写成这样：用于求解问题的定理在问题中被明确提及。结果，使用同一条定理的问题可能有高关键词重叠，这意味着检索器可以很容易地通过匹配关键词检索到正确文档。因此，我们把 TheoremQA 中的问题改写为扎根于真实世界场景或应用，这使推理步骤不那么显式，并提供更多样的问题。我们用人工撰写的指令和上下文内演示，利用 GPT-4 改写查询 $Q$。我们在表 13 中提供用于改写 TheoremQA 问题的提示和一个例子。改写问题之后，作者人工检查每个改写后的问题，以确保问题可解且与原问题一致（即推理步骤和最终答案仍然成立）。在适用时，我们人工编辑改写后的问题以改善流畅性和连贯性，并在改写后的问题不可解或与原问题不一致时丢弃该查询。因此，我们从原始的 800 道 TheoremQA 问题中得到 206 道改写后的问题。

【脚注 14】https://huggingface.co/datasets/TIGER-Lab/MathInstruct

### B.4 TheoremQA：标注相关定理

对 TheoremQA-Theorems，我们使用来自 TheoremQA-Questions 的测试查询，并为它们标注有用的定理证明和定义。我们从 ProofWiki 获取数学定理证明和定义。ProofWiki 是一项社区驱动的努力，有超过 2 万条数学定理的形式定义和证明。ProofWiki 由 MathPile（Wang et al., 2023b）预处理并提供。我们选择把原始定理名映射到 ProofWiki 中的文档，以便黄金文档与语料中其他文档具有一致的形式。

对每个测试查询，我们首先用原始 TheoremQA 数据集提供的定理名和定义，从 ProofWiki 构造一个有用文档的候选集。具体而言，我们用如下步骤构造候选集：

<!-- 原 PDF 第 21 页 -->

1. 找出定理名作为子串出现的文档。若这样的文档超过 100 篇，我们丢弃这一集合，这通常意味着定理名太常见。
2. 用原始数据集中的定理名和定义作为查询，我们用 BM25 从 ProofWiki 检索前 $k = 10$ 篇文档。

然后，我们提示 GPT-4（gpt-4-0125-preview）检查每篇文档所描述的定理是否被用在问题解答中，从而把每个候选标为正文档或负文档。这一步的提示见表 17。作者人工标注了 50 个实例，发现与模型判断有实质性一致，Cohen 的 $\kappa = 0.62$。最后，我们保留至少有一篇正文档的测试查询。

### B.5 AoPS：把 AoPS 问题连接到 MATH 数据集

AoPS Wiki 是一个社区驱动的平台，用户可以发布数学竞赛问题的题目和解答。这些数学竞赛包括但不限于 American Mathematics Competitions（AMC）、American Invitational Mathematics Examination（AIME）和 International Mathematical Olympiad（IMO）。除问题外，AoPS Wiki 还包含数学中各种主题的文章，例如费马小定理以及球与罐。这些文章不仅描述定理或技巧，还链接到可以用它们求解的问题。我们浏览 AoPS Wiki，收集主题和被链接的问题。主题列在表 18 中。

虽然数学竞赛问题被用于先前数据集，例如 MATH（Hendrycks et al., 2021），它们缺乏构造正文档所需的关于问题求解技能的标注。因此，我们选择从 AoPS Wiki 收集这些标注。

此外，由于 MATH 例子被用在 STEM 语料中，我们通过把收集到的问题与 MATH 实例匹配来去重。具体而言，对从 AoPS 收集的每个问题 $Q$，我们用 n-gram 重叠在 MATH 中找到最接近的问题陈述，并人工检查它们是否是同一道题。若找到相同问题，我们把它们合并为一个实例；否则，我们创建一个新实例并插入语料。

### B.6 LeetCode

我们首先从 HuggingFace 获取公开可用的 LeetCode 问题。【脚注 15】【脚注 16】我们的检索池来自 LeetCode 与 CodeSearchNet 的组合，每个例子包含问题描述和一段解答。在以下各节中，我们概述构造正例的过程，以及为在保证使用大检索池的同时最小化假阴性可能性而做的额外检查。

**用相似问题作为正例。** 对每个问题，我们从 “Similar Questions” 字段获得黄金对标注，该字段包含指向其他与该问题相似的 LeetCode 问题的链接。虽然网站没有明确描述该字段如何被填充的指南，我们的定性分析表明，这些问题在用于求解问题的数据结构、算法和/或逻辑推理上有高重叠。

**基于真实世界场景选择问题，以避免来自 CodeSearchNet 的假阴性。** 从初步定性分析中，我们发现 LeetCode 中的一些问题由于某些算法的流行性和问题陈述的简单性而经常出现在 CodeSearchNet 中。例子包括实现排序算法或合并两个链表，这可能意外地给这一检索设定引入假阳性。因此，我们使用一个额外的过滤步骤——我们只保留扎根于真实世界概念、且这些概念在编程问题语境中不那么常用的问题。其背后的直觉类似于 TheoremQA 的标注过程：推理步骤（即用于求解问题的算法和数据结构）不能像问题陈述清楚描述所用算法和数据结构时那样容易被破解。为此，我们首先人工撰写带六样本上下文学习演示的指令，并使用 GPT-4（gpt-4-0125-preview）对全部 LeetCode 问题分类。

【脚注 15】https://leetcode.com/

【脚注 16】https://huggingface.co/datasets/greengerong/leetcode

<!-- 原 PDF 第 22 页 -->

然后，我们用作者的 80 条标注来验证 GPT-4 的判断。作者与 GPT-4 的标注具有 Cohen 的 kappa 0.73，提示实质性一致。这一步使用的提示和例子见表 19。GPT-4 判定共有 291 个样本扎根于真实世界概念，我们从这一集合中随机采样 142 道问题来构造测试集。

**从池中移除主题高重叠的例子，以避免 LeetCode 中的假阴性。** 为避免未被 LeetCode 网站标注的潜在假阴性，我们利用网站的 “Topics” 字段，它包含关于问题中所用算法和数据结构的信息，例如 “stack” 和 “breath first search”（原 PDF 第 22 页抽取串；按广度优先搜索理解）。对每个问题 $Q$，我们从 LeetCode 网站收集其主题 $T(Q) = \{t_1^q, \ldots, t_m^q\}$，其中 $t_q$ 表示网站赋给该问题的 $m \ge 1$ 个不同主题。由于每个问题可能有多个标签，我们为该特定问题从语料中排除与测试问题有高重叠的其他问题。具体而言，若

$$
\frac{|T(Q) \cap T(Q')|}{|T(Q)|} \ge 0.5,
$$

我们就为测试查询 $Q$ 从语料中排除问题 $Q'$，因为 $Q'$ 中使用的主题有一半以上也在 $Q$ 中使用。这意味着两道问题在推理步骤上可能高度相关。重叠小于 0.5 阈值意味着 $Q'$ 不太可能与测试问题 $Q$ 相关，因而不太可能是假阴性。最后，我们从 CodeSearchNet（Husain et al., 2019）构造语料的其余部分。【脚注 17】我们只考虑 Python 函数，因为 LeetCode 问题的解答都是 Python。

【脚注 17】https://huggingface.co/datasets/code_search_net

## C 数据例子

在表 20、21、22、23、24、25、26、27、28、29、30 和 31 中，我们展示 BRIGHT 中的更多例子。这些例子的全文见后文对应页。

## D 推理分类

为更好地理解 BRIGHT 所要求的推理能力，我们用来自 12 个 BRIGHT 数据集中每一个的代表性例子，总结 4 种推理类型。

- **演绎推理：** 文档通常描述一条可以用来解释查询中特定场景或求解特定问题的一般原理或定理。例如，在表 20 中，分生组织的一般机制被用来解释树干被砍后仍能发芽生长的场景。（更多例子见表 21、25、22、31。）
- **类比推理：** 文档在底层逻辑上与查询形成平行，这表明文档中使用的方法也可以用来求解查询问题。例如，在表 29 中，虽然查询问题看起来与文档中的问题不同，它们共享相似的底层逻辑，并且都可以由 Chicken McNugget 定理求解。（更多例子见表 27、30。）
- **因果推理：** 文档与查询呈现因果关系，即为了修复查询中的问题，我们需要在文档中找到原因。例如，在表 24 中，查询呈现调试信息缺失的问题，其原因是源代码中的参数设置（正文档）。
- **分析推理：** 文档提供支持推理链以求解查询中问题的关键概念或知识。例如，在表 26 中，人们需要先分析查询中的问题：要判断把水再用于植物是否有益，我们需要先理解水从哪里来、水中可能含有什么；如查询所述，水来自浇水，它经过植物和土壤，最终到达花盆下的盘子；这表明水可能携带土壤和植物中的矿物质、可溶盐和其他物质。文档提供关键知识：可溶盐可能溶解并在水中积累，这对植物有害。这一信息帮助完成推导查询最终答案的推理链。（更多例子见表 23、28。）

<!-- 原 PDF 第 23 页 -->

有了分类后的推理能力，使用 BRIGHT 的人如果在特定数据集上观察到改进，现在可以更好地理解自己的成就。我们希望这将促进未来更系统地发展具有强推理能力的检索模型。

## E 下游性能

在本工作中，我们评估了检索对下游任务的影响。在本小节中，我们继续考察基于定理的任务——TheoremQA Questions、TheoremQA Theorems 和 AoPS——上的下游性能，在这些任务上评估 gpt-4o-2024-08-06。我们用上下文中的三类文档运行：无（闭卷）、随机（从语料中随机采样的文档）和预言（标注的语料）。我们使用温度 0.2 和 top-p 0.9，并在 5 个不同随机种子上平均结果。我们在表 47 中展示结果，并发现预言文档可以在全部数据集上一致地改善性能。这一改进在 TheoremQA Questions 和 TheoremQA Theorems 上具有统计显著性，提示使用强检索结果的益处。

## F 标注者指令

在本节中，我们描述标注者为 BRIGHT 收集数据的指令。

### F.1 StackExchange

1. 从最新到最旧浏览帖子。
2. 丢弃没有被用户接受的答案、或没有获得超过 5 票的帖子。
3. 丢弃答案中没有 URL 链接的帖子。
4. 对答案中的每个链接，写下对以下问题的回答：（1）为什么文档和帖子相关；（2）理解帖子与文档之间的相关性需要什么推理。如果做不到，丢弃该链接。
5. 检查被链接的文档是否提供理解帖子或处理问题的关键信息。相关性可以包括解释关键概念或细节，或提供有助于求解问题的定理、引理或代码片段。参考例子以更好地理解相关性（表 20 至表 26 中的例子）。
6. 使用 LLM（例如 ChatGPT、Claude 等）生成帖子关键词，或使用帖子标题在 Google 中搜索具有大关键词或语义重叠的网页。每个查询最多搜索 5 个负网页。确保硬负例对处理帖子完全没有帮助。常见硬负例包括相似语境但不同问题的描述或文档，或共享相同变量名但与帖子无关的代码片段。
7. 检查所有其他负段落，包括同一数据集中先前标注例子的正文档和负文档。确保那些文档与当前问题聚焦于不同子主题，因而完全不相关。
8. 把每个网页切成小段落，分隔可以是两个换行符、markdown 文件中的 “#”，或固定长度词元，并按照步骤 4 和 5 中的标准细粒度地标出正例。

### F.2 TheoremQA

在 TheoremQA 中，标注者的主要任务是检查 GPT-4 改写的问题是否有效。具体指令如下：

1. 阅读改写后的问题，并判断它是否可解。
2. 如果可解，阅读原问题和解答，并判断改写后的问题是否与原问题一致。也就是说，相同的推理步骤和最终答案应当成立。

<!-- 原 PDF 第 24 页 -->

3. 如果也一致，把该问题标为有效，并按你认为合适的方式对问题陈述做任何小编辑（例如改善语法或流畅性）。
4. 如果不可解或不一致，阅读原问题和解答，并在可能时改正改写后的问题。如果不能，则丢弃该问题。

### F.3 AoPS

在 AoPS 中，标注者的任务是从 AoPS Wiki 找到问题并记录这些问题：

1. 浏览 AoPS Wiki，找到主题/类别页面（例子 1，例子 2）。
2. 浏览每一页，找到可以用来求解问题的特定定理或技巧页面。该页面应当链接到至少两道竞赛题（例子 1，例子 2）。
3. 记录定理/技巧以及问题页面的链接。

标注者被分配一个类别来寻找定理，以避免重叠。类别为 {algebra, geometry, calculus, probability, number theory, other}。全部链接收集之后，我们用网络爬虫收集问题陈述和解答，并人工检查抓取数据的质量。

### F.4 LeetCode

在 LeetCode 中，标注者判断一个问题是否扎根于真实世界概念。我们给标注者与给 GPT-4 相似的指令：

1. 仔细阅读问题陈述。
2. 把问题分入三类之一：
   - 0：问题不扎根于任何真实世界概念。描述只使用编程特定术语，例如 “linked list”、“binary search”、“palindrome”、“sorting” 等。
   - 1：问题不扎根于任何真实世界概念，或只扎根于在编程语境中常用的真实世界概念，例如草堆中的针、字符串/词，或螺旋矩阵。
   - 2：问题扎根于在编程语境中不常用的真实世界概念，例如建筑高度、植树或游戏。它仍可能使用一些代码特定术语来指定所涉数据结构。

### F.5 LLM 的使用

标注者使用 LLM 没有特定流程。LLM 充当帮助标注者理解查询和文档的工具，即每当他们无法理解某事时，就向 LLM 请求澄清、解释等。它们也被用来摘要 StackExchange 帖子的内容，以便在 Google 中为 StackExchange 搜索负文档。为使搜索结果多样化，标注者用角色扮演场景（例如作为一名生物学学生）提示 LLM，以生成帖子的关键词。LLM 的响应不被纳入任何 BRIGHT 数据集。由于 LLM 的响应不保证正确，标注者总是搜索可信来源来核验信息。标注中使用的 LLM 包括 ChatGPT【脚注 18】、GPT-4 和 Claude-3。

【脚注 18】https://chatgpt.com/

### F.6 敏感信息

BRIGHT 中的全部数据都是人工收集、仔细核验并审阅的，以移除任何个人可识别信息或冒犯性内容。

<!-- 原 PDF 第 25 页 -->

## G 局限与未来工作

本工作的一个局限是，关于查询与文档之间相关性的判断是主观的。即便 StackExchange 答案被用户接受或获得高票，也不能保证每个人都会同意所引用的文档是相关的。我们可能不期望人类检索结果与我们的标注完全相同。然而，我们通过使用多名标注者、并且只保留所有标注者（包括领域专家）都同意相关性的查询来缓解这一问题。因此，我们相信 BRIGHT 中的相关性判断是可靠且一致的。

除检索之外，聚类等其他嵌入任务也可能需要推理。我们在本文中没有处理多模态设定，但它们代表未来探索的有趣途径。

## H 潜在社会影响

本文提出一个新的检索基准，其相关性超出词汇和语义相似，并且需要密集推理才能求解。我们的工作有许多潜在的社会后果，例如改进搜索算法、促进更好的信息获取、发展更先进的检索模型等。它也可以促进研究者之间的合作，并推动更有效的搜索引擎的发展，最终通过增强人们寻找和获取信息的方式而有益于社会。

## I 与 RAR-b 的比较

虽然 Reasoning as Retrieval Benchmark（RAR-b）和 BRIGHT 都在推理能力上评估检索系统，它们在方法和目标上有显著差异：

- **数据集构造：**
  - RAR-b：把现有多项选择基准改造成检索格式，查询是原始问题，语料由全部问题的互不重复选项组成。
  - BRIGHT：有目的地构建为检索基准，在现实检索场景中使用查询和文档。
- **文档特征：**
  - RAR-b：常常使用来自多项选择选项的很短序列（少于 10 个词）。
  - BRIGHT：聚焦于长得多的文档（超过 100 个词元），更接近实际检索场景。
- **实际相关性：**
  - RAR-b：它更偏概念而非实用，因为真实世界检索通常涉及检索文档而不是答案，使这一测试更关于抽象推理能力。
  - BRIGHT：被设计来反映真实世界的信息寻求行为和需求。

我们相信两个数据集都有效评估检索器处理推理密集型查询的能力，我们将在修订中加入与 RAR-b 更清楚的比较。

<!-- 原 PDF 第 26 页 -->

**表 13：用于改写 TheoremQA 问题的提示。** 蓝色文字表示实例特定输入。紫色文字表示 GPT-4 输出的改写问题和答案。对每个问题，我们提供原问题和答案，以及来自原始 TheoremQA 数据集的定理名和定理定义。指令提示模型在不改变推理步骤或最终答案的情况下，用不同的表面形式改写问题。我们手写三个例子来说明改写过程。我们也允许模型跳过该问题。抽取中部分定理定义被标为 additional text omitted，那些被省略的原文不在 PDF 文本流中，此处只译抽出的提示。

按如下方式改写下列问题：逻辑步骤和最终答案仍然相同，只改变问题的表面形式。避免使用与问题中所用定理相关的词。你可以通过使用真实世界的例子和应用来说明概念，以一种外行更容易理解的方式来做到这一点。尽量把问题扎根于金融和工程问题等真实世界语境，但要有创意，可以自由使用你喜欢的任何领域！然而，问题应当是独立的并且可解。用 json 格式改写问题，字段为 “question” 和 “answer”。“theorem” 字段表示问题中使用的定理，但你不应在改写后的问题中使用与该定理相关的词。如果你认为该问题不能以独立的方式用外行术语改写，那么你可以写一个 json 对象，把字段 “skip” 设为 True。

示例输入包括：10 人、每人有 3 种眼睛颜色之一，至少多少人眼睛颜色相同，答案 “4”，定理 pigeonhole principle。演示之一被省略。另一例：$dy/dt = \sqrt{t}$，$y(1) = 1$，求 $y(4)$，答案 “5.667”，定理 integral rules。改写后：你在跟踪一株从种子长出的植物。植物长高的速率等于自种植以来天数的平方根。种子种下一天后，植物高 1 英寸。4 天后植物会有多高？答案 “5.667”。另一道关于 4 比特图像阈值分割的问题被改写成：你有 12 张独特贴纸，稀有度从 0 到 7。按某个稀有度阈值分成 “Common” 和 “Rare” 两组。给定分布（7、6、5 级各两张，3 级三张，1 级和 0 级各一张），用作分界的稀有度是多少？答案 “4”。原文对部分定理定义标注 “[additional text omitted...]”，那些被省略的定义不在抽出的文本中。

<!-- 原 PDF 第 27 页 -->

**表 14：TheoremQA-Q 的定理名，以及从 CAMEL-Math 排除的主题名。** 定理名保留英文，主题名译为中文。

| TheoremQA-Q 定理 | CAMEL-Math 主题 |
| --- | --- |
| acyclic graph | 图论、组合学 |
| binomial theorem | 组合学、代数 |
| catalan-mingantu number | 组合学 |
| cauchy’s integral theorem | 复分析 |
| cayley’s formula | 图论、组合学 |
| convexity | 优化 |
| cramer rao lower bound | 统计 |
| definite matrix criteria | 代数、线性代数 |
| derivative chain rule | 微积分 |
| double integral theorem | 微积分 |
| eigenvalues and eigenvectors | 线性代数 |
| euler’s method | 微积分、数值分析、微分方程 |
| euler’s theory | 图论、组合学 |
| expected utility | 博弈论 |
| fisher information | 统计 |
| fourier’s theorem | 傅里叶分析 |
| gauss’s lemma | 数论、代数 |
| integral rules | 微积分 |
| intermediate value theorem | 微积分 |
| isomorphisms | 群论、代数 |
| jensen’s inequality | 统计、概率 |
| l’hôpital’s rule | 微积分 |
| limit laws for sequences | 微积分 |
| limiting theorem | 微积分 |
| linear independence | 代数、线性代数 |
| linear subspaces | 代数、线性代数 |
| linear systems | 代数、线性代数 |
| liouville’s theorem | 复分析 |
| martingale | 统计、概率 |
| matrix determinant formula | 代数、线性代数 |
| maximal planar graph | 图论、组合学 |
| maximum entropy | 统计、概率 |
| message passing algorithm | 图论、组合学 |
| multinomial theorem | 组合学 |
| newton-raphson method | 微积分、数值分析 |
| order | 群论、代数 |
| ordinary differential equation | 微积分、微分方程 |
| p-value | 统计 |
| pigeonhole principle | 组合学 |
| poisson process | 统计、概率 |
| projection theory | 代数、线性代数 |
| ramsey’s theorem | 图论、组合学 |
| rolle’s theorem | 微积分 |
| series convergence | 微积分 |
| shortest path | 图论、优化、组合学 |
| similarity | 几何 |
| squeeze theorem | 微积分 |
| stirling number of the first kind | 组合学 |
| stirling number of the second kind | 组合学 |
| t-test | 统计 |
| taylor’s approximation theorem | 微积分 |
| trapezoidal rule | 微积分、数值分析 |
| vertex cover | 图论、组合学 |
| viterbi algorithm | 统计 |
| wave theorem | 微分方程 |

<!-- 原 PDF 第 28 页 -->

**表 15：原始 TheoremQA 数据集中的子领域名及其在 BRIGHT 中的对应类别。** 每个类别用于指定从 MATH 和 AoPS 中排除的问题–解答对。类别名 algebra、calculus、geometry、number theory、probability、others 保留为原文类别标签，并给出中文。

| 名称 | 类别 |
| --- | --- |
| Algebra（代数） | algebra |
| Atomic physics（原子物理） | others |
| Calculus（微积分） | calculus |
| Celestial mechanics（天体力学） | others |
| Classic mechanics（经典力学） | others |
| Combinatorics（组合学） | number theory |
| Complex analysis（复分析） | calculus |
| Computer networking（计算机网络） | others |
| Condensed matter physics（凝聚态物理） | others |
| Derivatives（导数） | calculus |
| Economics（经济学） | others |
| Electromagnetism（电磁学） | others |
| Equity investments（权益投资） | others |
| Fixed income（固定收益） | others |
| Fluid mechanics（流体力学） | others |
| Functional analysis（泛函分析） | calculus |
| Geometry（几何） | geometry |
| Graph theory（图论） | others |
| Group theory（群论） | algebra |
| Information theory（信息论） | others |
| Kinetics（动力学） | others |
| Machine learning（机器学习） | others |
| Mathematical analysis（数学分析） | calculus |
| Number theory（数论） | number theory |
| Numerical analysis（数值分析） | calculus |
| Optics（光学） | others |
| Particle（粒子） | others |
| Portfolio management（投资组合管理） | others |
| Probability theory（概率论） | probability |
| Quantitive methods（定量方法；原文拼写 Quantitive） | others |
| Quantum（量子） | others |
| Real analysis（实分析） | calculus |
| Relativity（相对论） | others |
| Signal processing（信号处理） | others |
| Statistical physics（统计物理） | others |
| Statistics（统计） | others |
| Stochastic process（随机过程） | probability |
| Thermodynamics（热力学） | others |
| Wave（波） | others |

<!-- 原 PDF 第 29 页 -->

**表 16：AoPS 定理与技巧，以及从 CAMEL-Math 和 TheoremQA 排除的主题名。**

| AoPS 定理 | CAMEL-Math 主题 | TheoremQA 定理 |
| --- | --- | --- |
| Binomial Theorem | 组合学、代数 | binomial theorem、multinomial theorem |
| Vietas Formulas | 代数 | vieta’s formula、birg-vieta’s theorem |
| Ptolemys theorem | 几何 | 风筝形的性质、相似性、菱形、矩形、四边形、三角形、等腰三角形、平行四边形 |
| Recursive Series | 微积分、代数 | |
| Power of a Point | 几何 | 相似性 |
| Ball and urn | 组合学 | |
| Newtons Sums | 代数 | vieta’s formula |
| Probability | 概率、统计 | probability |
| Fibonacci sequence | 组合学、数论 | |
| Chicken McNugget Theorem | 组合学、数论 | |
| Central Tendency | 统计 | |
| Principle of Inclusion Exclusion | 组合学、集合论 | inclusion-exclusion principle |
| Factorial | 组合学 | |
| Picks Theorem | 几何 | 相似性、三角形、等腰三角形、平行四边形、菱形、四边形、矩形、三角形中位线定理 |
| Shoelace Theorem | 几何 | 菱形、矩形、四边形、三角形、等腰三角形、平行四边形 |
| Geometric probability | 几何、概率 | |
| Euclidean algorithm | 数论、密码学、代数 | euclidean algorithm |
| Mass Points | 几何 | 相似性、三角形、等腰三角形、平行四边形、菱形、四边形、矩形、三角形中位线定理 |
| Geometric Series | 代数 | |
| Triangle Inequality | 几何 | 不等式、三角形、等腰三角形 |
| Simons Favorite Factoring Trick | 数论、代数 | |
| Properties of Logarithms | 代数 | |
| Fermats Little Theorem | 数论、密码学 | fermat’s little theorem、euler’s totient theorem |

<!-- 原 PDF 第 30 页 -->

**表 17：用于检查 TheoremQA-Theorem 文档的提示。** 蓝色文字表示实例特定输入。对每个问题，我们提供问题陈述、解答、定理名、定理定义，以及来自一篇 ProofWiki 文档的文档文本。

指令：判断给定文本是否有助于理解和求解给定问题。用定理、其定义和问题解答来帮助你做决定。如果文本使用与解答非常相似的推理步骤，并且以与解答应用该定理来求解问题相关的方式应用该定理，则文本可以是有帮助的。文本应当能够协助一个不熟悉该定理的学生最终求解该问题。输入以 json 格式给你，键如下。问题陈述：学生试图求解的问题陈述。解答：问题的解答。定理：解答中使用的定理。定理定义：定理的定义。文本：你需要评估的文本。先逐步思考并推理定理和文本，然后再做最终决定。若文本有帮助则输出 True，否则输出 False。随后按如下格式写出答案：推理：[你的推理]；答案：[True/False]。

**表 18：AoPS 数据集中使用的定理和技巧，及其对应的子领域类别。**

| 名称 | 类别 |
| --- | --- |
| Ball and urn | number theory |
| Binomial Theorem | algebra |
| Central Tendency | others |
| Chicken McNugget Theorem | algebra |
| Euclidean algorithm | number theory |
| Factorial | number theory |
| Fermat’s Little Theorem | number theory |
| Fibonacci sequence | number theory |
| Geometric Series | algebra |
| Geometric probability | probability |
| Mass Points | geometry |
| Newtons Sums | algebra |
| Picks Theorem | geometry |
| Power of a Point | geometry |
| Principle of Inclusion Exclusion | number theory |
| Probability | probability |
| Properties of Logarithms | algebra |
| Ptolemy’s theorem | geometry |
| Recursive Series | algebra |
| Shoelace Theorem | geometry |
| Simon’s Favorite Factoring Trick | number theory |
| Triangle Inequality | algebra |
| Vieta’s Formulas | algebra |

<!-- 原 PDF 第 31 页 -->

**表 19：用于检查 LeetCode 问题的提示。** 蓝色文字表示实例特定输入。紫色文字表示 GPT-4 的输出。对每个问题，我们提供标题和问题陈述。我们使用六个上下文内演示，指令提示模型根据所给标准对问题分类。虽然有三种可能标签，我们只保留被标为 2 的问题，即扎根于真实世界概念的问题。为简洁起见，原文只展示一个例子，其他例子见代码仓库。

阅读这道编程题，并用下列标准分类。0：问题不扎根于任何真实世界概念。描述只使用编程特定术语，例如 “linked list”、“binary search”、“palindrome”、“sorting” 等。1：问题不扎根于任何真实世界概念，或只扎根于在编程语境中常用的真实世界概念，例如草堆中的针、字符串/词或螺旋矩阵。2：问题扎根于在编程语境中不常用的真实世界概念，例如建筑高度、植树或游戏。它仍可能使用一些代码特定术语来指定所涉数据结构。你只应考虑初始问题陈述和问题标题，而不是例子或约束。用下列例子帮助你分类。例 1 标题 “Merge Two Sorted Lists”，问题大意：给定两个已排序链表的头，把它们合并成一个有序链表，返回合并后链表的头。标签 0。例 2 至例 6 因简洁而省略。然后考虑下面的问题并用上述标准分类，以 json 输出。标题 “Container With Most Water”：给定长度为 n 的整数数组 height，有 n 条竖线，第 i 条线的两端点是 (i, 0) 和 (i, height[i])。找出两条线，使它们与 x 轴构成的容器装水最多。返回容器能储存的最大水量。标签 2。

<!-- 原 PDF 第 32 页 -->

**表 20：生物学例子。** 正文档解释分生组织的概念，这是植物细胞发育成其他组织和器官的机制。这为树干被砍后为何会发芽生长提供关键支持。

查询：冬天我把树砍成原木并去掉树枝之后，它们开始生长。它们抽出看起来完全正常的茎和叶，并整个夏天维持它们。芽大多出现在被砍的枝条周围。有时它们能熬过整个冬天并再长一年。树干被砍之后是如何发芽并生长的？

为找到文档的思维链推理：核心问题是弄清树被砍之后的生长机制。它通常与细胞分裂有关，细胞分裂后来发育成组织和器官。我们需要找到植物中这些细胞及其被砍后生长能力的相关信息。

正文档例子：分生组织。顶端分生组织（生长尖端）的原套–原体模型。表皮（L1）和表皮下（L2）层形成称为原套的外层。内部 L3 层称为原体。L1 和 L2 层中的细胞以侧向方式分裂，从而保持这些层彼此区分，而 L3 层以更随机的方式分裂。在细胞生物学中，分生组织是植物中的一类组织。它由能够进行细胞分裂的未分化细胞（分生细胞）组成。分生组织中的细胞可以发育成植物中出现的所有其他组织和器官。这些细胞持续分裂，直到它们分化并失去分裂能力。有三类分生组织：顶端（在尖端）、居间或基部（在中间）和侧生（在侧面，也称为形成层）。在分生组织顶端，有一小群分裂缓慢的细胞，通常称为中心区。这一区的细胞具有干细胞功能，对维持分生组织至关重要。分生组织顶端的增殖和生长速率通常与外围显著不同。在适当条件下，每个茎分生组织都可以发育成一株完整的新植物或克隆。这类新植物可以从含有顶端分生组织的茎插条长出。

负文档例子：安全而容易地从伐倒的树上砍木柴（造材）。网上有大量文章展示如何（有时是如何不要）砍倒树，但关于树被伐倒并去掉树枝（在树艺师用语中称为 snedding 或 limbing）之后实际砍木柴的内容没那么多。这篇操作说明展示同时砍许多原木来生产木柴的最容易方法。我实际上把砍木柴当作健身计划的一部分，比去健身房有用得多，第二天肌肉同样酸痛。我先把树砍成 10 英尺（3 米）的原木，以便轻松把它们拖到靠近装车点的清理过的工作区。你可以用结实的建筑木材（2 乘 4）做一个自制“摇篮”，托住一整捆原木。这使你能一次安全地砍许多根，只要把一些重原木既放在底部也放在顶部。别忘了把摇篮做得足够窄，以适应你的链锯导板尺寸。内部尺寸通常不超过 12 英寸或 300 毫米。确保它的构造方式使你不会用链锯碰到任何钉子等。把原木放到摇篮上，使原木末端一侧齐平（或至少按 12 英寸的台阶错开）。如果你像我一样挑剔，可以用粉笔在上面一根原木上每隔 12 英寸（300 毫米）做标记，以保证原木长度均匀。然后交替两侧来锯（以免倒向一侧），最后在摇篮本身上方再锯几刀，别忘了在把东西锯成两半之前停下来（见下面的升级版）。

<!-- 原 PDF 第 33 页 -->

**表 21：地球科学例子。** 正文档描述 Airy 均衡模型，计算静力平衡时需要它。

查询：如何计算静力平衡？我试图求解如下问题。过去的海平面比今天高 200 米。海水与洋盆达到均衡。洋盆深度 $x$ 的增加是多少？水密度 $p_w = 1000\,\mathrm{kg\,m^{-3}}$，地幔密度为 $3300\,\mathrm{kg\,m^{-3}}$。用补偿柱，我得到 $x = (p_w \cdot 200\,\mathrm{m})/3300 = 60.60\,\mathrm{m}$，但我本来预期会得到 290 米。有人能解释我错在哪里吗？

思维链：这个问题关于静力平衡。这可能与帕斯卡定律有关，它给出流体力学中压力变化的洞见。要理解静力平衡或帕斯卡定律，提供计算中所用概念和公式的详细解释会有帮助。关于定理应用的其他内容，或同样聚焦于与洋盆的均衡讨论的相关引理，也会有用。

正文档：Airy。该模型的基础是帕斯卡定律，尤其是其推论：在静力平衡的流体中，同一高度上每一点的静水压相同（静力补偿面）：$h_1 \cdot p_1 = h_2 \cdot p_2 = h_3 \cdot p_3 = \cdots = h_n \cdot p_n$。对所示简化图，山带根的深度 $b_1$ 计算如下：$(h_1 + c + b_1)p_c = (c p_c) + (b_1 p_m)$，$b_1(p_m - p_c) = h_1 p_c$，$b_1 = h_1 p_c / (p_m - p_c)$，其中 $p_m$ 是地幔密度（约 $3{,}300\,\mathrm{kg\,m^{-3}}$），$p_c$ 是地壳密度（约 $2{,}750\,\mathrm{kg\,m^{-3}}$）。因此一般有 $b_1 = 5 h_1$。

负文档：全球或海面海平面在地球历史上显著波动。影响海平面的主要因素是可用水的数量与体积，以及洋盆的形状与体积。对水体积的主要影响是海水温度（影响密度），以及保留在河流、含水层、湖泊、冰川、极地冰盖和海冰等其他水库中的水量。在地质时间尺度上，洋盆形状和海陆分布的变化影响海平面。除海面变化外，局部海平面变化由地壳抬升和沉降引起。在地质时间上，海平面波动超过 300 米，可能超过 400 米。过去 1500 万年海平面波动的主要原因是南极冰盖，以及暖期的南极冰川后回弹。当前海平面大约比历史最低值高 130 米。历史上的低值出现在末次冰盛期（LGM），约 2 万年前。上一次海平面高于今天是在埃姆间冰期，约 13 万年前。

<!-- 原 PDF 第 34 页 -->

**表 22：经济学例子。** 正文档描述随机占优，这是求解该问题所用的底层概念。

查询：在指数分布下，具有冯·诺伊曼–摩根斯坦偏好的消费者会选择这两张彩票中的哪一张？考虑两张彩票，各自服从指数分布。指数分布的累积分布函数是 $F(x;\lambda) = 1 - e^{-\lambda x}$，$\forall x \in \mathbb{R}^+$。该分布给出的期望收益是 $\mathbb{E}[X] = 1/\lambda$。设第一张彩票 $F_1$ 的参数为 $\lambda_1$，第二张 $F_2$ 的参数为 $\lambda_2$，且 $\lambda_1 < \lambda_2$。具有冯·诺伊曼–摩根斯坦偏好的消费者会选择哪一张？我对这个问题感到困惑。

思维链：期望值不同于期望效用。这种情况下不确定性下的偏好应当联系到一阶随机占优。我们需要查阅详细定义，以理解如何用该框架求解问题。

正文档：状态占优蕴含一阶随机占优（FSD），其定义为：若对任何结果 $x$，随机变量 $A$ 给出至少得到 $x$ 的概率至少与 $B$ 一样高，并且对某个 $x$，$A$ 给出更高的至少得到 $x$ 的概率，则 $A$ 对 $B$ 具有一阶随机占优。记号为：对所有 $x$，$P[A \ge x] \ge P[B \ge x]$，并且对某个 $x$，$P[A \ge x] > P[B \ge x]$。用两个随机变量的累积分布函数来说，$A$ 占优 $B$ 意味着对所有 $x$，$F_A(x) \le F_B(x)$，并且在某个 $x$ 处严格不等。在分布函数不相交的情形下，Wilcoxon 秩和检验检验一阶随机占优。扩展例子：考虑公平六面骰一次投掷上的三种赌博。状态（骰子结果）1 到 6：赌博 A 赢得 1、1、2、2、2、2 美元；赌博 B 赢得 1、1、1、2、2、2 美元；赌博 C 赢得 3、3、3、1、1、1 美元。赌博 A 状态占优赌博 B，因为 A 在所有可能状态中给出至少同样好的收益，并在其中一个状态（状态 3）给出严格更好的收益。由于 A 状态占优 B，它也一阶占优 B。

负文档：美国境内哪张彩票最容易中？中彩票是人生中最不可能发生的事情之一。然而，有些彩票比另一些容易中得多。许多美国人做白日梦，幻想中彩票，这很常见。这些梦对少数幸运赢家成为现实，他们一夜之间成为百万富翁。冷酷的事实是，压倒性多数的彩票梦将仍然是梦。大多数人知道中彩票的赔率对你不利。如果容易中，人人都会玩，奖金只会是几分钱。你更可能被闪电击中、活到 110 岁，并被天主教会封圣。高头奖与低赔率的组合使许多人试图在彩票中作弊。这些尝试可能短期内成功，但它们总是以监禁告终。幸运的是，有几种方法可以合法地改善你的中奖赔率。它将从选择赔率最好的游戏开始。

<!-- 原 PDF 第 35 页 -->

**表 23：心理学例子。** 正文档描述解释帖子中困惑所需的关键方程。

查询：为什么 fNIRS 设备通常使用两种不同频率？当今功能神经成像最常用的技术之一是功能性近红外光谱（趣闻：我记得 Natalie Portman 做过一篇以 fNIRS 为模态的研究论文），它把近红外光从光源照入大脑再到探测器（两者都称为光极），呈“香蕉”形。阅读到这些设备——无论是连续波（CW），还是涉及快速调制的两种之一，频域（FD）或时域（TD）——大多需要发射两个分开的频率，这并不罕见。例如 NIRx 在其网站上如此解释：“对神经成像应用，用两个离散波长照明是迄今最常见的，这是独立评估血红蛋白分子两种氧合状态的相对变化的最低要求。”为什么是这样？我没有深入其细节，但没有理由立刻跳出来。例如，在 CW 的情形下，重要的只是强度的相对差，为什么我们需要两个频率？

思维链：为理解为什么 fNIRS 需要两个频率，我们需要检查连续波系统中的测量和计算。这可能与脑中的氧合血红蛋白（HbO）和脱氧血红蛋白（HbR）有关。我们需要参考双波长方法，它是 fNIRS 提供关于局部脑活动的有意义信息的能力的基础。

正文档（公式按抽出的矩阵还原）：其中 OD 是光密度或衰减，$I_0$ 是发射光强，$I$ 是测量光强，$\epsilon$ 是衰减系数，$[X]$ 是发色团浓度，$l$ 是光源与探测器之间的距离，DPF 是差分路径长度因子，$G$ 是与散射相关的几何因子。当衰减系数 $\epsilon$ 已知、假定散射损失为常数、并且测量在时间上被差分处理时，方程简化为 $\Delta[X] = \Delta OD / (\epsilon d)$，其中 $d$ 是校正后的总光子路径长度。使用双波长系统，HbO$_2$ 和 Hb 的测量可以从矩阵方程解出：

$$
\begin{pmatrix} \Delta OD_{\lambda_1} \\ \Delta OD_{\lambda_2} \end{pmatrix}
=
\begin{pmatrix}
\epsilon^{\lambda_1}_{\mathrm{Hb}} d & \epsilon^{\lambda_1}_{\mathrm{HbO_2}} d \\
\epsilon^{\lambda_2}_{\mathrm{Hb}} d & \epsilon^{\lambda_2}_{\mathrm{HbO_2}} d
\end{pmatrix}
\begin{pmatrix} \Delta[X]_{\mathrm{Hb}} \\ \Delta[X]_{\mathrm{HbO_2}} \end{pmatrix}
$$

原 PDF 第 35 页的矩阵排版被拆成多行，上式按符号含义重排。

负文档：什么是波的频率？在给定时间内通过一个固定点的波的数量就是波的频率。波的频率可以通过计数在 1 秒或其他时间段内通过固定点的波峰（高点）数量来测量。这个数越高，波的频率越大。波频率的国际单位是赫兹（Hz），1 赫兹等于 1 秒内有 1 个波通过固定点。下图展示高频和低频横波。问：波的波长是相邻波上对应点之间的距离。例如，它是图中横波两个相邻波峰之间的距离。推断波频率如何与波长相关。答：频率更高的波，波峰靠得更近，因此更高频率的波具有更短的波长。

<!-- 原 PDF 第 36 页 -->

**表 24：机器人学例子。** 正文档提供要修改的代码片段。

查询：用 RCLCPP_DEBUG 看不到调试消息。我无法在终端和 rqt 中看到使用 RCLCPP_DEBUG 的消息，但用其他详细级别（INFO、ERROR、FATAL 等）可以看到。在 rqt 中选择 debug 来看那些消息也不起作用。我使用 rolling，在一个控制器插件中用 C++ 工作，并从 nav2_bringup 启动 tb3_simulation_launch.py。我也看到这里有一篇帖子，他们建议设置环境变量 RCLCPP_LOG_MIN_SEVERITY=RCLCPP_LOG_MIN_SEVERITY_DEBUG，但那也不起作用。一定是我漏掉了什么傻事。这在你身上发生过吗？谢谢。

思维链：问题看起来与日志级别的设置有关。如果在 rqt 中选择 debug 不起作用，我们可以检查关于可能影响日志消息和详细程度的潜在参数的代码。

正文档包含启动参数 `log_level`，默认值为 `info`，并在节点参数中传入 `['--ros-args', '--log-level', log_level]`，包为 nav2_controller，可执行文件为 controller_server。

负文档按严重程度描述日志方法：DEBUG 是详细信息，通常只在诊断问题时有兴趣；INFO 确认事情按预期工作；WARNING 表示发生了意外之事，或预示不久的将来有问题（例如磁盘空间低），软件仍按预期工作；ERROR 表示由于更严重的问题，软件未能执行某项功能；CRITICAL 是严重错误，表明程序本身可能无法继续运行。

<!-- 原 PDF 第 37 页 -->

**表 25：Stack Overflow 例子。** 正文档提供解释求解方法的文档。

查询：是否有一条 Snowflake 命令可以做如下事情：把列为 a、b、c、行为 (1, 10, 0.1)、(2, 11, 0.12)、(3, 12, 0.13) 的表变成键值表：a 对应 1、2、3，b 对应 10、11、13，c 对应 0.1、0.12、0.13。这一操作在其他表格系统中常称为 melt，但基本想法是把表转换成键值对列表。SnowSQL 中有 UNPIVOT，但据我理解 UNPIVOT 要求手动指定每一列。对大量列这似乎不实用。

思维链：这一操作是一种表变换，如重塑、序列化或展平。我们在寻找 Snowflake 中的一种操作，它能取二维值，并把它们变换成呈现键与值之间一一对应映射的视图。

正文档：FLATTEN。把复合值展平（展开）成多行。FLATTEN 是一个表函数，它接受 VARIANT、OBJECT 或 ARRAY 列，并产生一个横向视图（即一个内联视图，包含指向 FROM 子句中先于它的其他表的相关引用）。FLATTEN 可用于把半结构化数据转换成关系表示。语法：`FLATTEN( INPUT => <expr> [, PATH => <constant_expr>] [, OUTER => TRUE | FALSE] [, RECURSIVE => TRUE | FALSE] [, MODE => 'OBJECT' | 'ARRAY' | 'BOTH'] )`。

负文档：SYSTEM$EXTERNAL_TABLE_PIPE_STATUS。检索与外部表关联的内部（隐藏）管道对象的当前刷新状态的 JSON 表示。自动刷新外部表的元数据在内部依赖 Snowpipe，当被监控的云存储发生变化时，Snowpipe 接收事件通知。更多信息见外部表简介。语法：`SYSTEM$EXTERNAL_TABLE_PIPE_STATUS('<external_table_name>')`。

<!-- 原 PDF 第 38 页 -->

**表 26：可持续生活例子。** 正文档解释可溶盐这一关键概念，表明它们含有溶解的矿物质，并且可能对植物有害。

查询：再用花盆里的水有多好？我住在公寓里，浇花之后水会流到花盆下面的盘子里。花盆在盘子上方的金属结构里，所以我可以把盘子拿起来再用水（再浇到植物上）。这种再用似乎有益，因为我想我可以除掉会在积水中繁殖的蚊子。而且土壤的一些养分（以及蚯蚓）可以回到花盆。这样做有什么负面之处吗？

思维链：浇水后积在盘子里的水很可能含有存在于土壤或植物中的矿物质、可溶盐和其他物质。要弄清再用那水是否有任何负面之处，我们因此需要理解那水中的成分是否会导致任何不利影响。

正文档：可溶盐。可溶盐可能在土壤顶部积累，形成黄色或白色硬壳。盐沉积环可能在土壤线处或排水孔周围的花盆上形成。盐也可能在陶盆外侧积累。在室内植物上，过量可溶盐的迹象包括生长减缓、叶尖变棕、下部叶子脱落、新生长很小、根尖死亡和萎蔫。可溶盐是溶解在水中的矿物质。溶解在水中的肥料成为一种可溶盐。当水从土壤蒸发时，矿物质或盐留在后面。随着土壤中的盐变得越来越浓，植物吸水变得更加困难。如果盐积累到极高水平，水可以从根尖被吸出，导致根尖死亡。高水平的可溶盐直接损伤根，削弱植物，使它更容易受到昆虫和疾病的攻击。与高盐水平相关的最常见问题之一是根腐。防止可溶盐伤害的最好办法是阻止盐积累。浇水时，让一些水从容器中排出，然后倒空托盘。不要让花盆坐在水里。如果排出的水被土壤吸收，被洗出的盐会通过排水孔或直接通过陶盆被重新吸收。

负文档：加利福尼亚的水回用。加利福尼亚的水回用是把再生水用于有益用途。作为一个位于干旱、易旱的西部、人口稠密的州，水回用正在发展为加利福尼亚用水的一个组成部分，使经济和人口都能增长。废水：再生水是来自住宅和商业的经处理废水，例如水槽水、淋浴水和马桶水，包括倒进废水排水管的一切，从洗衣皂到漂白剂到油到人类排泄物。废水可以分为灰水和黑水，前者被定义为曾用于洗衣、沐浴、水槽洗涤和洗碗机的水。黑水被定义为包括来自马桶的粪便的污水。由于灰水中物理污染物量低，其大多数污染物是溶解有机物，可以通过各种膜物理过滤和清洁，也可以通过生物处理方法。

<!-- 原 PDF 第 39 页 -->

**表 27：LeetCode 例子。** 查询和正文档的解都使用双指针。负例由 BM25 检索得到。

查询：给定 n 个非负整数，表示一幅海拔图，每根柱的宽度为 1，计算下雨后它能接住多少水。例 1：输入 height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]，输出 6。解释：上述海拔图（黑色部分）由数组表示，此情况下有 6 个单位的雨水（蓝色部分）被接住。例 2：输入 height = [4, 2, 0, 3, 2, 5]，输出 9。约束：n 等于 height 的长度，1 小于等于 n 小于等于 $2 \times 10^4$，0 小于等于 height[i] 小于等于 $10^5$。原文 “2 * 104” 与 “105” 按 $2\times 10^{4}$ 与 $10^{5}$ 理解。

思维链：这个问题可以用双指针方法求解，并使用动态规划的想法来跟踪每根柱左右两侧的最大高度。我们可以找到同样使用这些技术的其他示例代码。

正文档是函数 `max_area`：给定长度为 n 的整数数组 height，有 n 条竖线，找出与 x 轴构成装水最多的容器的两条线，返回容器能储存的最大水量。注意不能倾斜容器。用左右指针，当 left 小于 right 时更新面积，较矮的一侧向内移动。

负文档是函数 `get_power`：你的国家有无限个湖。最初所有湖都是空的，但当下雨在第 n 个湖上时，第 n 个湖充满水。如果雨下在已经充满水的湖上，就会发生洪水。目标是避免任何湖发生洪水。给定整数数组 rains。原文其余部分省略。

<!-- 原 PDF 第 40 页 -->

**表 28：Pony 例子。**

查询：给定三角形各边的长度，写一个 Pony 程序，把它分类为等边、等腰或不等边。

思维链：要确定三角形的类别，我们需要比较边长。许多其他编程语言中用于条件和比较的常见语法是与控制结构相关的 if 或 switch。我们需要找到允许指定这类条件的语法。

正文档：控制结构。要在程序中做真正的工作，你必须能够做决定、遍历条目集合并重复执行动作。为此你需要控制结构。Pony 有对用过大多数语言的程序员会熟悉的控制结构，例如 if、while 和 for，但在 Pony 中它们的工作方式略有不同。条件：最简单的控制结构是老式的 if。它允许你只在条件为真时执行某个动作。在 Pony 中它看起来像：`if condition then control_body end`。简单例子：若 a 大于 b，则打印 “a is bigger”。条件常常可以由 and 和 or 连接的许多子条件组成。

负文档：类。就像其他面向对象语言一样，Pony 有类。类用关键字 class 声明，并且必须有一个以大写字母开头的名字，例如 `class Wombat`。所有类型都以大写字母开头吗？是的！并且没有别的东西以大写字母开头。所以当你在 Pony 代码中看到一个名字，你会立刻知道它是不是一个类型。类由什么组成？一个类由字段、构造函数和函数组成。

<!-- 原 PDF 第 41 页 -->

**表 29：AoPS 例子。** 负例由 BM25 检索得到，它用星与条求解问题，而查询和黄金文档使用 Chicken McNugget 定理。

查询（来自 2015 AMC 10B 第 15 题）：哈姆雷特镇每匹马对应 3 个人，每头牛对应 4 只羊，每个人对应 3 只鸭。下列哪一个不可能是哈姆雷特镇的人、马、羊、牛和鸭的总数？（A）41（B）47（C）59（D）61（E）66。

思维链：我们可以用 Chicken McNugget 定理求解这个问题。我们可以找到同样应用该定理的其他解答。

正文档：求所有正整数 n 的和，使得在面额为 5、n 和 n+1 分的邮票供应无限时，91 分是无法组成的最大邮资。由 Chicken McNugget 定理，使 91 分无法组成的最小可能 n 满足 $5n - (5+n) = 91$，从而 $n = 24$，所以 n 至少为 24。要使某个 n 成立，我们不仅必须无法组成 91，还必须能够组成 92 到 96，因为有了这五个值，我们可以用额外的 5 分邮票组成任何大于 96 的值。注意我们必须组成 96 而不组成 91。如果组成 96 时使用任何 5 分邮票，我们可以简单地去掉一张得到 91。这意味着我们必须只用面额为 n 和 n+1 的邮票得到 96。回忆 n 至少为 24，我们可以容易地找出能用来得到 96 的有效 (n, n+1) 对，因为我们最多可以用 $96/24 = 4$ 张邮票而不超出。潜在集合是 (24, 25)、(31, 32)、(32, 33)、(47, 48)、(48, 49)、(95, 96) 和 (96, 97)。最后两个显然不行，因为它们太大，无法组成 92 到 94；经过一点测试，只有 (24, 25) 和 (47, 48) 能组成必要的值，所以 n 属于 {24, 47}。24 + 47 = 71。

负文档：Alice 有 24 个苹果。她可以用多少种方式与 Becky 和 Chris 分享，使三个人每人至少有两个苹果？（A）105（B）114（C）190（D）210（E）380。注：此解使用非负版本的星与条。使用正版本星的解类似（先从每个人去掉 1 个苹果而不是 2 个）。该方法使用星与条计数法（非负版本）。由于每人必须至少有 2 个苹果，我们可以从需要分配的总数中去掉 $2 \times 3$ 个苹果。对剩下的 18 个苹果，我们可以用星与条确定可能性的数量。假设一行有 18 颗星和 2 根条，条将被放置以把星分成 3 组。总共有 18 个星的位置加上 2 个条的位置，共 20 个位置。我们现在可以计算 $\binom{20}{2}$。原 PDF 第 41 页该二项式抽取为乱码分行，按 $\binom{20}{2}$ 理解。这是因为如果我们为条选择 2 个不同位置，每一种 3 组组合都会不同，并且全部苹果加起来为 18。我们也可以这样做，因为苹果是不可区分的。$\binom{20}{2}$ 是 190，因此答案是（C）190。

<!-- 原 PDF 第 42 页 -->

**表 30：TheoremQA 问题例子。** 查询和正文档都用鸽巢原理求解。负文档由 BM25 检索得到，它只需要简单算术就能求解。

查询：Mary 计划恰好烤 10 块饼干，每块饼干可以是三种形状之一——三角形、圆形和正方形。Mary 希望饼干形状尽可能多样。十块饼干中最常见形状的最小可能数量是多少？

思维链：这个问题类似于鸽巢原理的表述。我们可以找到也能用这一原理求解的其他例子的解答。

正文档：在单位正方形中任意放置 19 个点，并用直径为 $\sqrt{2}/3$ 的圆覆盖尽可能多的这些点。问题：至少可以保证覆盖多少个点？我们可以把单位正方形分成 9 个更小的正方形，每个边长为 $1/3$。由于有 19 个点和 9 个更小的正方形，由鸽巢原理，这些更小的正方形中至少有一个必须包含至少 3 个点。现在考虑直径为 $\sqrt{2}/3$ 的圆。每个更小正方形的对角线长度为 $\sqrt{2}/3$，因此圆可以放在更小正方形内部，使其覆盖整个正方形。因此圆可以覆盖该正方形中至少 3 个点。因此答案是 3。原 PDF 第 42 页把 $\sqrt{2}/3$ 拆成多行。

负文档：Yanna 早上烤了二十块黄油饼干和四十块饼干。下午她烤了十块黄油饼干和二十块饼干。她烤的饼干比黄油饼干多多少？她烤了 $20+10=30$ 块黄油饼干。并且她烤了 $40+20=60$ 块饼干。因此她烤的饼干比黄油饼干多 $60-30=30$ 块。答案是 30。

<!-- 原 PDF 第 43 页 -->

**表 31：TheoremQA 定理例子。** 查询使用鸽巢原理，它是来自 ProofWiki 的黄金文档。负文档由 BM25 检索得到，与问题不相关。

查询与表 30 相同：Mary 计划恰好烤 10 块饼干……最常见形状的最小可能数量是多少？

思维链：这个问题类似于鸽巢原理的表述。我们可以查看该原理，并找到关于如何用该原理求解这个问题的提示。

正文档：鸽巢原理。标签：Pigeonhole Principle、Named Theorems、Combinatorics。定理：令 $S$ 为基数为 $n$ 的有限集。令 $S_1, S_2, \ldots, S_k$ 为把 $S$ 划分成 $k$ 个子集的一个划分。则 $S$ 的至少一个子集 $S_i$ 包含至少 $\lfloor n/k \rfloor$ 个元素，其中 $\lfloor \cdot \rfloor$ 表示上取整函数。原文把 floor 符号写成 ceiling，按抽出的 “ceiling function” 保留这一用词，同时符号是 $\lfloor \cdot \rfloor$。证明用反证法：假设没有任何子集 $S_i$ 有多达 $\lfloor n/k \rfloor$ 个元素，则任一 $S_i$ 的元素个数最多为 $\lfloor n/k \rfloor - 1$，从而 $S$ 的元素总数不超过 $k(\lfloor n/k \rfloor - 1) = k\lfloor n/k \rfloor - k$。分两种情形：$n$ 能被 $k$ 整除，以及不能。若 $k$ 整除 $n$，则 $\lfloor n/k \rfloor = n/k$ 是整数，且 $k\lfloor n/k \rfloor - k = n - k$，于是 $|S| = \sum_{i=1}^{k}|S_i| \le n-k < n$，与 $|S|=n$ 矛盾。若 $k$ 不整除 $n$，则 $|S| = k\lfloor n/k \rfloor - k < k(n+k)/k - k = n$，再次矛盾。因此由反证法，至少一个 $S_i \subseteq S$ 中至少有 $\lfloor n/k \rfloor$ 个元素。原 PDF 第 43 页证明中的整除符号和分式被拆行，上式按抽出的符号关系整理。

负文档是条件句语义的定义：令 $p \Rightarrow q$，其中 $\Rightarrow$ 表示条件算子。$p \Rightarrow q$ 可以陈述为：若 $p$ 为真则 $q$ 为真；$q$ 为真如果 $p$ 为真；$p$ 的真蕴含 $q$ 的真；$q$ 的真被 $p$ 的真所蕴含；$q$ 由 $p$ 推出；$p$ 为真仅当 $q$ 为真。最后一条可能需要解释：$p$ 可以为真或假，$q$ 也可以。但如果 $q$ 为假且 $p \Rightarrow q$，则 $p$ 不能为真。因此 $p$ 可以为真仅当 $q$ 也为真。其他口语解释包括：只要、一……就、每当、倘若、在……情况下、假定、在……条件下。例子包括妈妈说做完作业才能去看电影。

<!-- 原 PDF 第 44 页 -->

**表 32：Gemini 在可持续生活上的推理例子。**

查询与表 26 相同：再用花盆里的水有多好？

LLM 推理步骤。（1）核心问题：用户想知道再用从花盆排水盘收集的水是有益还是有害。他们担心潜在的蚊子繁殖以及对植物生长的影响。（2）推理。被再用水的成分：可能含有来自土壤的溶解养分、矿物质和盐；可能含有微生物；如果停滞，可能藏有蚊子幼虫。对植物生长的负面影响：积水会吸引蚊子；来自肥料的高盐浓度会伤害植物；水传播病原体可能伤害植物。（3）草稿答案：再用花盆里的水是一种平衡。你在寻找节约用水并可能有益于植物的方法，这值得称赞。再用花盆排水盘里的水可以是个好主意，但有一些缺点要考虑。蚊子繁殖：盘子里的积水可以成为蚊子的繁殖地，构成健康风险。定期倒空并清洗盘子以防止这一点。盐积累：反复使用同一份水会导致来自肥料的盐积累，这会伤害植物。病原体风险：虽然不太常见，水传播病原体可能伤害你的植物。使用过滤水或煮过的水可以最小化这一风险。

<!-- 原 PDF 第 45 页 -->

**表 33：Gemini 在可持续生活上的推理例子（续）。** 正文档例子再次给出可溶盐一文，内容与表 26 的正文档相同：可溶盐可能在土壤顶部积累，形成黄或白色硬壳；室内植物上过量可溶盐的迹象包括生长减缓、叶尖变棕、下部叶子脱落、新生长很小、根尖死亡和萎蔫；可溶盐是溶于水的矿物质；盐变浓后植物更难吸水；极高盐水平会把水从根尖吸出并导致根腐；浇水时应让一些水排出并倒空托盘，不要让花盆坐在水里。

**表 34：把 GritLM 生成的推理步骤用作查询时，检索模型的性能。** 列与表 2 相同：Bio.、Earth.、Econ.、Psy.、Rob.、Stack.、Sus.、Leet.、Pony、AoPS、TheoQ.、TheoT.、Avg.。默认 `find_tables` 只对齐了 BM25 一行，其余模型的 13 列被拆开。表抽取失败，见原 PDF 第 45 页。已对齐的 BM25 行为：33.1、38.7、19.2、28.0、16.8、18.9、20.6、19.7、13.2、3.3、13.0、8.9、19.4。同页可见 Google 一行的末尾数字包括 25.6、34.7、22.2、30.0、14.5、21.0、16.3、28.9、1.6、8.4、18.8、12.9、19.6。

<!-- 原 PDF 第 46–48 页 -->

**表 36**（第 46 页起）：把 Llama3-70B 生成的推理步骤用作查询时的检索性能。列与表 2 相同。BM25 开头数字为 53.8、51.4、24.1、35.3，其后各模型的完整对齐表抽取失败，见原 PDF 第 46 页。

**表 39–40**（第 47 页）：长上下文设定的分数与文档统计。默认 `find_tables` 把多模型挤进同一单元格。表抽取失败，见原 PDF 第 47 页。能读出的长上下文平均 Recall@1 与正文表 6 一致。文档统计（查询数、文档数、平均查询长度、平均文档长度、平均黄金文档数）按阅读顺序为：Biology 103、524、115.2、9422.4、1.3；Earth Science 116、601、109.5、27312.3、1.6；Economics 103、516、181.5、11896.4、1.1；Psychology 101、512、149.6、12411.66、1.1；Robotics 101、508、818.9、14998.2、1.1；Stack Overflow 117、1858、478.3、40759.7、1.1；Sustainable Living 108、554、148.5、12077.7、1.2；Pony 112、577、102.6、1361.0、6.9。

**表 41**（第 48 页）：基于 BM25 前 10 或前 100 检索结果的 MiniLM（交叉编码器）、Gemini 和 GPT-4 重排序分数。分组为 StackExchange、Code、Math、Avg.。完整对齐表抽取失败，见原 PDF 第 48 页。正文表 3 已给出平均 NDCG@10。

<!-- 原 PDF 第 49 页 -->

**表 45：QA 推断提示。** 问题：{problem_description}。文档：{retrieved_doc}。基于所提供的文档，为该问题写一个答案。

同页另有一张在 BEIR 风格数据集上的分数表，列名为 Argu.、Climate.、CQA.、DBPedia、FEVER、FIQA.、Hot.、MS.、NF.、NQ、Quora.、SCI.、Sci.、Touche.、TREC.、Avg.。默认 `find_tables` 把每个模型的全部分数挤进一个单元格，列对齐不可靠。表抽取失败，见原 PDF 第 49 页。BM25 一行按抽出顺序为：31.5、21.3、29.9、31.3、75.3、23.6、60.3、22.8、32.5、32.9、78.9、15.8、66.5、36.7、65.6、41.6。

<!-- 原 PDF 第 50–51 页 -->

第 50 页给出下游 QA 的均值与标准差式数字，包括 Random、Qwen、Oracle 等行，例如 Oracle 为 79.3、0.4、89.7、1.7、37.2、3.8。列标题在抽取中未与这些数字对齐。表抽取失败，见原 PDF 第 50 页。

**表 48**（第 51 页）：检索模型在 BRIGHT 上以 Precision@10 衡量的性能。列与表 2 相同。默认 `find_tables` 只完整对齐了 BM25：7.6、12.4、7.1、6.0、5.6、8.0、6.1、6.0、7.9、3.1、2.2、1.3、6.1。其余模型的 Precision@10 以及同页后续 Recall 类表被拆列。表抽取失败，见原 PDF 第 51 页。同页另一张表的 BM25 行为 21.8、31.4、16.8、15.5、19.4、16.8、21.1、29.5、3.6、6.0、11.4、9.0、16.9。

<!-- 译完 -->
