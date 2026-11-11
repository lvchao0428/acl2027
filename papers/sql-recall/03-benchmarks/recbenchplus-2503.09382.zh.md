# 迈向下一代推荐系统：用 LLM 做个性化推荐助手的基准

- 原文件名：recbenchplus-2503.09382.pdf
- 原标题：Towards Next-Generation Recommender Systems: A Benchmark for Personalized Recommendation Assistant with LLMs
- 中文标题：迈向下一代推荐系统：用 LLM 做个性化推荐助手的基准
- 作者：Jiani Huang、Shijie Wang、Liang-bo Ning、Wenqi Fan、Shuaiqiang Wang、Dawei Yin、Qing Li
- 会议或 arXiv：PDF 页眉为 WSDM ’26, February 22–26, 2026, Boise, ID, USA；第 1 页页脚为 arXiv:2503.09382v2 [cs.IR] 2 Feb 2026。DOI：https://doi.org/10.1145/3773966.3777954

<!-- 原 PDF 第 1 页 -->

**Jiani Huang**  
jianihuang01@gmail.com  
The Hong Kong Polytechnic University，Hong Kong, China

**Shijie Wang**  
shijie.wang@connect.polyu.hk  
The Hong Kong Polytechnic University，Hong Kong, China

**Liang-bo Ning**  
BigLemon1123@gmail.com  
The Hong Kong Polytechnic University，Hong Kong, China

**Wenqi Fan**<sup>†</sup>  
wenqi.fan@polyu.edu.hk  
The Hong Kong Polytechnic University，Hong Kong, China

**Shuaiqiang Wang**  
shqiang.wang@gmail.com  
Baidu Inc.，Beijing, China

**Dawei Yin**  
yindawei@acm.org  
Baidu Inc.，Beijing, China

**Qing Li**<sup>†</sup>  
qing-prof.li@polyu.edu.hk  
The Hong Kong Polytechnic University，Hong Kong, China

## 摘要

推荐系统（RecSys）被广泛用于各种现代数字平台，并已获得大量关注。传统推荐系统通常只聚焦固定而简单的推荐场景，难以在交互范式中泛化到新的、未见过的推荐任务。近来，大语言模型（LLM）的进展革新了 RecSys 的基础架构，推动其演化为更智能、更具交互性的个性化推荐助手。然而，大多数现有研究依赖固定的、任务特定的提示模板来生成推荐并评估个性化助手的性能，这限制了对它们能力的全面评估。原因在于，常用数据集缺乏能够反映真实推荐场景的高质量文本用户查询，因此不适合评估基于 LLM 的个性化推荐助手。为填补这一空白，我们引入 RecBench+，一个新的数据集基准，用于评估 LLM 时代中处理复杂用户推荐需求的能力。RecBench+ 包含一组多样的查询，同时覆盖硬条件与软偏好，并具有不同难度。我们在 RecBench+ 上评估了常用 LLM，并得到如下发现：1）LLM 展现出充当推荐助手的初步能力；2）LLM 更擅长处理条件被明确陈述的查询，而在需要推理或包含误导信息的查询上面临挑战。我们的数据集已发布于 https://github.com/jiani-huang/RecBenchPlus。

## CCS 概念

- Information systems → Personalization

## 关键词

推荐系统，推荐助手，大语言模型（LLM），数据集基准

<sup>†</sup>通讯作者：Wenqi Fan 与 Qing Li，Department of Computing, The Hong Kong Polytechnic University。

WSDM ’26, Boise, ID, USA.  
2026. ACM ISBN 979-8-4007-2292-9/2026/02  
https://doi.org/10.1145/3773966.3777954

## ACM 参考格式

Jiani Huang, Shijie Wang, Liang-bo Ning, Wenqi Fan†, Shuaiqiang Wang, Dawei Yin, and Qing Li†. 2026. 迈向下一代推荐系统：用 LLM 做个性化推荐助手的基准. In Proceedings of the Nineteenth ACM International Conference on Web Search and Data Mining (WSDM ’26), February 22–26, 2026, Boise, ID, USA. ACM, New York, NY, USA, 10 pages. https://doi.org/10.1145/3773966.3777954

推荐系统（RecSys）在现代数字平台中扮演关键角色，使个性化内容能够在电子商务 [2]、娱乐 [7] 与教育 [32] 等领域投放。例如，YouTube 曾报告其主页上 60% 的点击来自推荐内容 [4]，揭示了 RecSys 巨大的商业价值。一般而言，这些系统被训练来处理典型推荐场景，例如用「看过此物品的顾客也看过」来推荐替代或相似物品，以及用「基于你的浏览历史」利用用户历史数据推荐感兴趣的 Top-K 物品，如图 1（a）所示。作为最具代表性的算法之一，矩阵分解（matrix factorization，MF）技术 [15] 被提出，以基于用户—物品交互学习用户与物品的潜在表示，从而预测推荐中的匹配分数。然而，这些传统推荐方法只适用于有限范围的简单、固定推荐场景，依赖预先设计并充分训练的推荐方法，并且难以在交互范式中泛化到新的、未见过的推荐任务（即推荐查询）。例如，若用户搜索「1500 美元以下、适合平面设计的耐用笔记本电脑」，MF 等传统方法只依赖用户与物品之间的相关性，无法捕捉这些细微需求并给出合适的推荐。

近来，GPT-o1 [12]、DeepSeek-R1 [8] 与 LLaMA [6] 等大语言模型（LLM）在泛化与推理上展现出很强的能力。例如，AUTOGLM [19] 充当自主助手，利用 LLM 类人的理解与规划智能，帮助用户通过图形界面控制数字设备，并处理订机票 [28]、收集数据 [26] 与编程 [14, 22] 等复杂任务，显著提升人们日常生活的便利。受 LLM 强大能力的启发，已有许多工作把 LLM 纳入 RecSys，使其在交互范式中成为个性化推荐

arXiv:2503.09382v2 [cs.IR] 2 Feb 2026

<!-- 原 PDF 第 2 页 -->

本页及后续页面的页眉为：WSDM ’26, February 22–26, 2026, Boise, ID, USA. / Jiani Huang et al. 下文不再逐页重复。

助手。例如，LLaRA [16] 直接把用户的历史交互转换为自然语言格式（即提示），以进行个性化推荐。得益于 LLM，如图 1（b）所示，这些个性化推荐助手可以处理更具交互性、更具挑战的场景，例如「告诉你你会喜欢什么」，允许用户以对话方式提问并收到相应推荐。

尽管取得了显著成功，当前研究缺乏对这些基于 LLM 的个性化推荐助手之推荐能力的全面评估。具体而言，在训练与测试阶段，大多数现有方法利用固定而简单的任务特定提示模板来生成推荐回应，并评估这些助手的推荐性能，例如用「用户会喜欢 {movie_i} 吗？请回答 Yes 或 No。」来判断是否推荐某件特定物品，或用「请从候选列表 {movie_1, movie_2, ...} 中选择一部电影」来推荐用户喜欢的物品。然而，这一评估范式无法与真实实践场景对齐：当用户与基于 LLM 的推荐助手交互时，用户查询可能高度复杂。考虑图 1（c）中的复杂查询，基于 LLM 的推荐助手必须首先解释用户的描述以识别正确的电影，然后识别主演，最后建议由该演员出演的相似电影。这一过程要求助手理解查询、执行多步推理并考虑多个条件——这些能力超出基本的属性匹配或浅层语义理解。因此，现有基于 LLM 的 RecSys 在传统基准数据集上的结果，未必适用于 LLM 时代的新推荐范式。

现有常用数据集，如 LastFM [25]、Amazon Beauty [21] 与 Movielens-1M [9]，通常只包含基本用户信息、物品元数据（例如标题）以及用户—物品交互。这些数据集更适合评估传统 RecSys 的准确性，但由于缺乏能够满足实际推荐场景的多样复杂用户查询，并不适合有效评估 LLM 时代的推荐助手。为弥合这一差距，我们引入新基准 RecBench+，专门用于评估 LLM 充当个性化推荐助手的潜力。具体而言，我们提出一个约 30,000 条复杂用户查询的新数据集，覆盖需要复杂推理的一系列推荐场景，包括多个条件、多跳推理、误导信息以及多样的用户画像。该数据集由若干常用推荐数据集构建（例如 Movielens-1M [9] 与 Amazon book<sup>1</sup>）。

我们在 RecBench+ 上全面评估了七个广泛使用的 LLM 的性能，包括 GPT-4o [11]、Gemini-1.5-Pro [31]、DeepSeek-R1 [8] 等。我们进一步分析影响模型性能的多种因素，例如条件数量、用户交互历史的纳入，以及不同的微调范式。通过在我们的基准上对当前最优 LLM 进行大量实验，我们得到若干有洞察的发现：（1）**LLM 展现出充当推荐助手的初步能力，但其优势各不相同。** GPT-4o 与 DeepSeek-R1 在条件清晰的用户查询上表现出色，而 Gemini-1.5-Pro 与 DeepSeek-R1 在没有清晰条件、但需要清楚理解用户画像的查询上表现更好。（2）**微调显著提升 LLM 的推荐性能，结合监督微调（SFT）与强化微调（RFT）的两阶段方法总体表现最好。** 这表明 SFT 有效地为任务预热模型，使 RFT 能够进一步精炼性能。（3）**对于带有用户指定条件的查询，LLM 更擅长处理条件被明确陈述的查询。** 相比之下，需要推理或包含扰动的查询带来更大挑战。然而，配备先进推理能力的模型在此类任务上往往表现更好。（4）**对于需要理解用户画像的查询，LLM 在不同用户兴趣与人口统计上表现不一。** 例如，LLM 可能更擅长为流行兴趣提供推荐，并且对女性用户往往比对男性用户更有效。我们的贡献概括如下：

- **新的推荐范式：** 我们为下一代推荐系统引入一种新范式，探索 LLM 以交互且智能的方式充当个性化推荐助手的有效性。作为以这种方式整合 LLM 的首个基准，我们把传统推荐范式转变为更个性化、更具上下文意识的体验，为该领域设定新的标准。
- **数据集构建：** 我们提出一个全面的数据集，称为 RecBench+，以模拟 LLM 时代的实际推荐场景。我们的数据集包含大约

<sup>1</sup> https://archive.ics.uci.edu/ml/datasets/Amazon+book+reviews

<!-- 原 PDF 第 3 页 -->

30,000 条需要复杂推理的用户查询，包括多个条件、多跳推理、误导信息以及多样的用户画像。据我们所知，这是第一个可用于在复杂且推理密集的推荐设定中评估基于 LLM 的推荐助手性能的公开数据集。

- **全面评估：** 我们用当前最优的 LLM 进行大量实验，并针对该任务微调开源模型，分析它们在该任务中的优势与局限，并提供可操作的见解。

图 1 见原 PDF。

**图 1：** 不同推荐范式的示意。（a）基于传统方法：通过学习用户/物品表示，在固定场景中生成推荐。（b）基于 LLM 的推荐：采用固定而简单的查询模板，缺乏在更复杂场景中的评估。（c）本文：评估 LLM 作为推荐助手处理复杂、灵活用户查询的能力。

图中文字（自文本层抽取）包括：用户；基于 LLM 的推荐助手；「我记得一部科幻电影，英雄踩着悬浮滑板、带着时光机追坏人。我真的很喜欢男主角。我想看更多有他出演的相似电影！」；进阶推理过程；「我首先需要弄清你指的是哪部电影。根据你的描述，这部电影可能是 Back to the Future Part II。」；「Back to the Future Part II 的男主角是 Michael J. Fox，他扮演 Marty McFly，电影里那个踩悬浮滑板的少年。」；「你可能会喜欢 Back to the Future 和 Teen Wolf。」；「Michael J. Fox 还主演了 Back to the Future 和 Teen Wolf 等电影，他的角色体现了同样的幽默与冒险混合。」；「两者都是由 Michael J. Fox 主演的惊险冒险！」；传统推荐中的「看过此物品的顾客也看过」「基于你的浏览历史」；观看历史；Top-k 物品；相似物品；分数 0.93、0.91、0.83、0.79；「我看过 {movie_list}。{movie_i} 适合我吗？」；「我看过 {movie_list}。请为我挑选下一部最合适的电影：{movie A, ..., movie C}。」；多条件；多跳推理；更复杂的设定。

## 1 RecBench+ 基准

在本节中，我们首先给出 RecBench+ 基准的概览。然后，我们提供所提出数据集中每一数据类型的构建方法。

### 1.1 概览

在实际应用中，用户需求一般可分为两类，每一类都要求基于 LLM 的推荐助手具备专门能力。第一类由特定条件或约束驱动，例如要求某位导演的电影或某一类型的电影。该场景要求推荐助手具备很强的推理能力，因为它需要助手准确解释并应用给定约束，以生成合适的推荐。第二类不涉及指定条件，而是要求推荐助手基于对用户画像的理解（例如用户兴趣、职业、性别）生成推荐，这强调助手解释画像并提供个性化建议的能力。鉴于这两种场景对推荐助手要求不同的能力，我们构建两种不同的查询类型来评估其性能：基于条件的查询（Condition-based）与基于用户画像的查询（User Profile-based）。如表 1 所示，我们的基准使用 Amazon-Book 与 Movielens-1M<sup>2</sup>。下面，我们基于这些来源详述基于条件的查询与基于用户画像的查询的构建。

<sup>2</sup> 与 10M/20M 版本不同，MovieLens-1M 包含必要的用户人口统计数据。

#### 1.1.1 基于条件的查询

基于条件的查询模拟用户施加具体约束（例如特定导演或类型）的场景。核心挑战在于准确满足这些条件。为评估推理能力，我们把该查询分为三类：显式条件查询（直接陈述的约束）、隐式条件查询（需要多跳推理的模糊输入），以及错误信息条件查询（包含错误或错字）。

- **显式条件查询：** 这些查询以自然语言格式明确指定被推荐物品应当满足的条件。例如，查询「你能推荐由 Gwyneth Paltrow 出演的电影吗？」直接陈述了推荐必须满足的条件（「由 Gwyneth Paltrow 出演」）。显式条件查询相对直接，因为约束被清楚表述。

**表 1：** RecBench+ 的统计。列依次为：大类、子类、条件数、Movie、Book。

| 大类 | 子类 | 条件 | Movie | Book |
| --- | --- | --- | --- | --- |
| 基于条件的查询 | 显式条件 | 1 | 2,225 | 2,260 |
| | | 2 | 2,346 | 2,604 |
| | | 3,4 | 426 | 271 |
| | 隐式条件 | 1 | 1,753 | 1,626 |
| | | 2 | 1,552 | 2,071 |
| | | 3,4 | 344 | 213 |
| | 错误信息条件 | 1 | 1,353 | 1,626 |
| | | 2 | 1,544 | 2,075 |
| | | 3,4 | 342 | 215 |
| 基于用户画像的查询 | 基于兴趣 | - | 7,365 | 2,004 |
| | 基于人口统计 | - | 279 | 0 |
| 查询总数 | | | 19,529 | 14,965 |
| 用户数 | | | 6,036 | 48,535 |
| 物品数 | | | 3,247 | 50,088 |
| 用户—物品交互数 | | | 29,459 | 55,424 |

- **隐式条件查询：** 与显式条件查询不同，隐式条件查询涉及不完整的说明，需要多跳推理才能推出目标条件。例如，请求「与 Stay Hungry 和 Beethoven 同一位摄影指导的电影」，需要先推断未说出的名字（David Worth）。该类别作为对推理能力更具挑战的基准。
- **错误信息条件查询：** 用户有时会在查询中提供关于物品的不正确或误导性信息。例如，查询「我喜欢 Spielberg 导演的《Avatar》。请推荐由他导演的相似电影。」错误地把电影 Avatar 归于 Steven Spielberg。期望推荐助手能够首先识别并纠正这一错误信息——认识到 Avatar 并非由 Spielberg 导演——然后再生成相关推荐。该子类对推荐助手的稳健性构成显著挑战，要求它准确识别用户查询中的不准确信息。

#### 1.1.2 基于用户画像的查询

在许多真实场景中，用户可能不提供用于过滤物品的特定条件，而是期望基于其画像信息获得个性化结果，例如兴趣（如对特效的兴趣）或人口统计属性（如性别、职业）。这是因为用户往往对自己的需求缺乏清楚理解，转而寻求与其背景或偏好直观对齐的推荐。为应对这一常见情形，我们引入基于用户画像的查询，它通过要求推荐助手基于用户画像信息生成个性化建议来模拟这些场景。我们进一步把基于用户画像的查询分为基于兴趣的查询与基于人口统计的查询，因为兴趣反映用户的动态偏好，而人口统计捕捉性别或职业等更稳定、并影响其需求的属性。

- **基于兴趣的查询：** 这些查询反映无法用特定条件清楚定义的用户兴趣。例如，历史上看过 “The Tree of Life” 与 “2046” 的用户可能偏好具有独特叙事与视觉美感的电影。为捕捉此类兴趣，我们创建如下查询：「我刚看了 “The Tree of Life”，喜欢它诗意的叙事与视觉设计。你能推荐其他基调相似的电影吗？」此类查询没有显式条件，但要求个性化推荐助手理解并基于用户的个人兴趣建议物品。

<!-- 原 PDF 第 4 页 -->

- **基于人口统计的查询：** 这些查询聚焦用户的人口统计属性如何影响推荐。不同用户基于年龄、性别或职业，可能有不同的偏好与需求。例如，哲学教授可能对探讨道德困境的电影感兴趣。利用这些模式，我们可以构造如下查询：「我是一名哲学教授，在找主题复杂、带有道德困境的电影。你能推荐一些吗？」通过与真实世界的人口统计行为对齐，这些查询可以反映个性化推荐助手应当提供的个性化推荐，确保建议与用户的背景和身份相关并量身定制。

### 1.2 基于条件的查询的构建

用户查询常常通过与物品属性对应的条件来表达偏好，例如按类型、导演或演员过滤电影。然而，由于物品与其属性之间关系错综复杂，生成能够反映用户如何组合这些属性的、真实而多样的查询是具有挑战的。值得注意的是，知识图谱（Knowledge Graph，KG）作为一种结构化表示，显式地把物品（例如电影）连接到其属性（例如导演），并捕捉它们之间的相互依赖（例如「导演 X 经常与演员 Y 合作」）。因此，我们提议利用 KG 抽取有意义的条件，并生成与真实用户行为对齐的查询。具体而言，我们的方法包含三个关键步骤：物品知识图谱（Item KG）构建、共享关系抽取，以及查询生成，如图 2 所示。我们首先构建 Item KG，它把物品链接到其属性。接着，我们从用户交互历史中识别共享相同属性的物品集合（例如由 Christopher Nolan 导演的电影），形成查询的条件。最后，我们采用 LLM 模拟用户，并基于这些抽取的条件生成查询。满足条件的物品集合可作为评估的真实标签。

图 2 见原 PDF。

**图 2：** 构建基于条件的查询的流水线概览。图中文字包括：数据来源；知识图谱；用户—物品交互；电影 KG；图书 KG；共享关系；从 KG 检索物品；抽取关系；知识子图；显式条件 (Director, Cameron), (Genre, Fiction)；隐式条件 (Genre, Fiction), (Director, “The Abyss 的导演”)；错误信息条件 (Genre, Fiction), (Director, Cameron)，以及「Cameron 导演了 Startreck」；指令：给定若干条件，请模拟真实用户并生成一条覆盖这些条件、以请求相关物品推荐的自然语言查询；生成的显式查询：「我喜欢 Cameron 作品独特的叙事，请推荐他的虚构类电影。」；生成的隐式查询：「我喜欢 The Abyss 的导演手法。我想看更多同一导演的电影。」；生成的错误信息查询：「我喜欢 Cameron 在 StarTreck 中的导演手法。我想看更多他拍的虚构类作品！」；真实标签。步骤标记为 #1 Item KG 构建、#2 共享关系抽取、#3 基于条件的查询生成。

#### 1.2.1 Item KG 构建

Item KG 构成在 RecBench+ 中生成真实的基于条件的查询的基础。我们针对电影与图书领域利用不同的 KG：

- **电影：** 我们从 Wikipedia 抽取数据，聚焦导演、演员、作曲者与类型等 7 个关键属性。每个电影节点都链接到这些属性。
- **图书：** 我们使用 Amazon Book 数据集的元数据，把作者与类目等属性连接到图书节点。

一旦 KG 建成，我们把它们与传统推荐数据集 Movielens-1M 和 Amazon-Book 结合起来，逐步生成条件与查询。

#### 1.2.2 共享关系抽取

共享关系是用户交互历史中的物品之间共有的属性。例如，若用户看过多部同一导演或同一演员主演的电影，这些共享属性有助于生成基于条件的查询。给定用户 $u$ 及其交互历史 $\mathcal{H}_u = \{i_1, i_2, \ldots, i_k\}$，我们采用 KG 检索函数 $\mathcal{R}$，在 $\mathcal{H}_u$ 的物品子集上识别共享属性（关系）。每个共享关系定义为元组 $(r, t)$，其中 $r$ 是关系类型（例如 “directed by”、“starring”），$t$ 是目标值（例如导演姓名）。抽取过程产生多组共享关系及其对应的物品子集，可表示如下：

$$
\mathcal{R}(\mathcal{H}_u, KG) = \{(\mathcal{G}_{\mathrm{sub}}, C_{\mathrm{shared}}) \mid \mathcal{G}_{\mathrm{sub}} \subseteq \mathcal{H}_u,\ C_{\mathrm{shared}} = \{(r_1, t_1), (r_2, t_2), \ldots\}\}. \qquad (1)
$$

这里，$\mathcal{G}_{\mathrm{sub}}$ 表示共享同一组关系 $C_{\mathrm{shared}}$ 的物品子集。抽取的共享关系随后将作为查询生成的条件。

#### 1.2.3 查询生成

从用户交互历史中抽取共享关系之后，我们生成三类基于条件的查询：显式、隐式与错误信息。生成这些条件与最终查询的步骤如下：

- **显式条件构建：** 对于显式条件，我们直接采用从用户交互历史中抽取的共享关系。具体而言，我们设显式条件 $C_{\mathrm{explicit}} = C_{\mathrm{shared}}$。这意味着条件直接来自与用户交互过的物品相关联的共享属性（例如导演、类型）。

<!-- 原 PDF 第 5 页 -->

图 3 见原 PDF。

**图 3：** 构建基于用户画像的查询的流水线概览。（a）基于兴趣的查询构建；（b）基于人口统计的查询构建。图中文字包括：交互记录；用户；交互过的物品；用户组；按（职业，性别）分组；按（年龄，性别）分组；共同兴趣集合；其前序物品；最受欢迎的电影；生成理由与生成查询的指令；示例查询「我喜欢看像……这样的浪漫经典。你能推荐其他来自好莱坞黄金时代的爱情电影吗？」以及「作为一名历史教授，我喜欢带有历史或政治语境的爱情电影。有推荐吗？」；真实标签。

- **隐式条件构建：** 对于隐式条件，我们不直接陈述具体值（例如导演姓名），而是利用 KG 通过相关物品间接描述它们。例如，不直接提及 James Cameron，我们可能使用「The Abyss 的导演」。具体而言，对于共享关系 $(r_m, t_m) \in C_{\mathrm{shared}}$（例如 (director, Cameron)），我们把需要被推断的值 $t_m$（例如 Cameron）替换为描述 $t_m$ 与另一物品 $i_k$（例如 The Abyss）之关系的间接指称，该物品来自 KG。数学上可表示为：

$$
i_k \in \{ i \in \mathcal{I} \mid (t_m) \xrightarrow{r_m} (i)\ \text{in KG} \}, \qquad (2)
$$

其中 $\mathcal{I}$ 是 KG 中全部物品的集合。所得隐式条件为：

$$
C_{\mathrm{implicit}} = (r_i,\ \mathrm{ref}(i_k)), \qquad (3)
$$

其中 $\mathrm{ref}(i_k)$ 表示对 $i_k$ 的文本指称。例如，共享关系 (director, Cameron) 可以变换为隐式条件 (director, “the director of ‘The Abyss’”)，其中 “The Abyss”（$i_k$）从 KG 中检索得到，经由 “director” 关系（$r_0$）连接到 “Cameron”（$t_0$）。

- **错误信息条件构建：** 对于错误信息条件，我们有意在条件中引入事实错误，模拟真实用户可能错误引用属性或关系的情形。为生成一条错误信息条件，对于共享关系 $(r_i, t_i) \in C_{\mathrm{shared}}$，我们从 KG 中随机选择一件或多件与 $t_i$ 不具有指定关系 $r_i$ 的物品 $\{i_1, i_2, \ldots, i_m\} \in \mathcal{I}$（即对每个 $i_k \in \{i_1, i_2, \ldots, i_m\}$ 有 $i_k \not\rightarrow t_i$）。然后我们用「错误信息」构造条件，虚假地声称这些物品通过 $r_i$ 与 $t_i$ 相关：

$$
C_{\mathrm{misinformed}} = (r_i,\ t_i,\ \text{error info:}\ \{i_1, i_2, \ldots, i_m\} \xrightarrow{r_i} t_i), \qquad (4)
$$

其中集合 $\{i_1, i_2, \ldots, i_m\}$ 包含 KG 中实际上并不与 $t_i$ 共享关系 $r_i$ 的物品。例如，一条错误信息条件可以是 (director, Cameron, error info: Cameron is the director of ‘Startreck’)。

- **查询生成：** 对每种条件类型，我们应用 GPT-4o [11] 生成相应查询：

$$
q = \mathrm{LLM}(C, \mathcal{P}), \qquad (5)
$$

其中 $\mathcal{P}$ 是提示。对每条生成的查询 $q$，我们构造一个样本，由以下组成：

$$
(q,\ H'_u,\ G_q),\quad \text{其中}\ H'_u = H_u \setminus G_q, \qquad (6)
$$

$$
G_q = \{ i \in \mathrm{KG} \mid C_{\mathrm{shared}} \subseteq A_i \}. \qquad (7)
$$

这里，$H'_u$ 是排除了 $G_q$ 中物品之后的用户交互历史，$G_q$ 包含满足查询条件的真实物品。$A_i$ 表示物品 $i$ 在 KG 中的属性。

### 1.3 基于用户画像的查询的构建

除提供具体约束外，用户可能只提供观看历史或人口统计属性（例如年龄、职业）等基本个人信息。为评估 LLM 推荐助手处理此类场景的能力，我们引入基于用户画像的查询，其目标是在不要求特定过滤条件的情况下，基于用户画像信息生成个性化推荐。如第 1.1.2 节所述，基于用户画像的查询包含两个子类：基于兴趣的查询与基于人口统计的查询。构建过程如图 3 所示。

#### 1.3.1 基于兴趣的查询

这些查询旨在捕捉并非由特定条件显式定义、而是从用户交互中推断出的用户兴趣。为有效模拟真实场景，我们聚焦于捕捉从多位用户的共享行为中涌现的集体兴趣，它们更能代表一般偏好与趋势。例如，若许多看过 “The Dark Knight” 的用户也看了 “Inception”，这表明对动作与悬疑有明确兴趣。这样，我们可以构造反映从共享行为中导出的集体用户兴趣的查询。具体而言，我们首先识别共同兴趣集合，即被多位用户频繁连续交互的物品集合。令 $H_u$ 表示用户 $u$ 的交互历史，$H = \{H_u \mid u \in \mathcal{U}\}$ 表示所有用户的交互历史集合。共同兴趣集合可定义为：

$$
S = \{ s \mid \exists u \in \mathcal{U},\ s \subseteq H_u,\ f(s) \ge \theta \}, \qquad (8)
$$

其中 $f(s)$ 是序列 $s$ 在所有用户历史中的频次，$\theta$ 是预定义的频次阈值。

一旦识别出共同兴趣集合，我们接着抽取前序物品序列，即通常出现在共同兴趣集合中的物品之前的物品序列。令 $P(s)$ 表示目标序列 $s$ 的前序物品序列集合。前序序列可定义为：

$$
P(s) = \{ p \mid \exists u \in \mathcal{U},\ p \prec s \subseteq H_u \}, \qquad (9)
$$

其中 $p \prec s$ 表示序列 $p$ 在交互历史 $H_u$ 中紧挨在序列 $s$ 之前出现。

基于所识别的共同兴趣集合与前序物品序列，我们采用 LLM 分析模式，并推断多位用户共同兴趣背后的理由。生成的查询旨在同时反映物品的上下文特征与用户的共同兴趣。

#### 1.3.2 基于人口统计的查询

人口统计相似的个体常常共享偏好；例如，儿童通常偏爱动画电影（例如 Disney），而青少年可能偏好动作或超级英雄电影。利用这一点，我们按

<!-- 原 PDF 第 6 页 -->

属性排列对用户分组（例如 18–24 岁的学生），并识别他们消费最多的物品。然后我们把这些人口统计与物品列表输入 LLM，以合成捕捉群体特定模式的查询。所识别的流行物品作为评估的真实标签。

### 1.4 数据过滤与选择

对于基于条件的查询，我们用字符串匹配检查所提供的信息（例如演员、导演）是否出现在查询中，并滤除省略该信息的查询。对于基于用户画像的查询，我们人工核验查询，并滤除过于宽泛或不合理的查询。

## 2 实验

### 2.1 实验设置

#### 2.1.1 基线

我们评估若干广泛使用的模型，包括 GPT-4o（2024-08-06）[11]、GPT-4o-mini（2024-07-18）[11]、Llama（Llama-3.1-70B-Instruct）[6]、Gemini（gemini-1.5-pro-002）[30]、Claude（claude-3-5-sonnet-20241022）、DeepSeek-V3 [17] 与 DeepSeek-R1 [8]，均在我们所提出的数据集上。然而，我们无法测试 GPT-o1 [12] 模型，因为它把我们的提示标记为违反其使用政策。此外，我们进一步在 Qwen-2.5-3B-Instruct 与 LLaMA-3.2-3B-Instruct 模型上进行全参数监督微调（SFT）以及强化微调（RFT，基于 GRPO [27] 算法），以探索它们在任务特定优化下的潜在性能增益。

#### 2.1.2 评估指标

我们使用下列指标评估 LLM 性能。为模拟用户通常不预先规定所需推荐数量的真实场景，我们在测试提示中不指定固定的推荐数量 $K$；不过，我们也在第 2.2 节纳入若干固定 $K$ 的实验作为参考。

- **Precision：** 被推荐物品中实际与用户查询相关的比例。
- **Recall [10]：** 在所有可用的相关物品中，被成功推荐的相关物品所占比例。
- **条件匹配率（Condition Match Rate，CMR）：** 满足指定条件的被推荐物品的百分比。对于基于条件的查询，检查模型的推荐是否严格与给定条件对齐很重要，因为不满足这些条件的物品很可能不能令人满意。Precision 与 Recall 等传统指标不足以评估这一对齐。因此，我们提出 CMR 来实现该目标。
- **未能推荐（Fail to Recommend，FTR）：** 该指标衡量模型未能生成被推荐物品的查询所占比例。更低的 FTR 更可取，表明模型能够生成物品列表。然而，在错误信息条件查询中，更高的 FTR 表明模型识别不正确信息、从而避免错误推荐的能力。

**表 2：** 基于条件的查询上的性能。/ 表示最佳结果与次佳结果。误导条件列的 FTR 为 ↑（越高越好），其余 FTR 为 ↓。

| 领域 | 模型 | 显式条件（易）P↑ | R↑ | CMR↑ | FTR↓ | 隐式条件（中）P↑ | R↑ | CMR↑ | FTR↓ | 错误信息条件（难）P↑ | R↑ | CMR↑ | FTR↑ | 平均 P↑ | R↑ | CMR↑ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Movie | GPT-4o-mini | 0.185 | 0.322 | 0.531 | 0.009 | 0.083 | 0.167 | 0.198 | 0.017 | 0.028 | 0.060 | 0.153 | 0.104 | 0.099 | 0.183 | 0.294 |
| | GPT-4o | 0.308 | 0.408 | 0.714 | 0.016 | 0.145 | 0.224 | 0.301 | 0.021 | 0.019 | 0.039 | 0.106 | 0.270 | 0.157 | 0.224 | 0.374 |
| | Gemini | 0.256 | 0.408 | 0.644 | 0.052 | 0.104 | 0.206 | 0.203 | 0.014 | 0.024 | 0.049 | 0.076 | 0.030 | 0.128 | 0.221 | 0.308 |
| | Claude | 0.201 | 0.422 | 0.658 | 0.014 | 0.105 | 0.269 | 0.281 | 0.011 | 0.033 | 0.079 | 0.128 | 0.087 | 0.069 | 0.183 | 0.277 |
| | DeepSeek-V3 | 0.190 | 0.401 | 0.621 | 0.001 | 0.090 | 0.260 | 0.217 | 0.001 | 0.027 | 0.078 | 0.105 | 0.013 | 0.102 | 0.246 | 0.314 |
| | DeepSeek-R1 | 0.224 | 0.447 | 0.651 | 0.001 | 0.197 | 0.463 | 0.496 | 0.005 | 0.024 | 0.068 | 0.096 | 0.024 | 0.148 | 0.326 | 0.414 |
| | Llama-3.1-70B | 0.238 | 0.342 | 0.609 | 0.003 | 0.097 | 0.164 | 0.210 | 0.012 | 0.037 | 0.050 | 0.116 | 0.109 | 0.124 | 0.185 | 0.312 |
| Book | GPT-4o-mini | 0.059 | 0.159 | 0.475 | 0.003 | 0.035 | 0.081 | 0.446 | 0.003 | 0.013 | 0.038 | 0.581 | 0.044 | 0.036 | 0.093 | 0.501 |
| | GPT-4o | 0.088 | 0.192 | 0.567 | 0.027 | 0.057 | 0.133 | 0.472 | 0.021 | 0.011 | 0.024 | 0.500 | 0.445 | 0.052 | 0.116 | 0.513 |
| | Gemini | 0.076 | 0.221 | 0.623 | 0.011 | 0.035 | 0.135 | 0.319 | 0.013 | 0.014 | 0.044 | 0.274 | 0.072 | 0.042 | 0.133 | 0.405 |
| | Claude | 0.054 | 0.193 | 0.608 | 0.010 | 0.043 | 0.161 | 0.515 | 0.010 | 0.020 | 0.068 | 0.444 | 0.056 | 0.039 | 0.141 | 0.522 |
| | DeepSeek-V3 | 0.040 | 0.124 | 0.667 | 0.008 | 0.056 | 0.190 | 0.385 | 0.005 | 0.014 | 0.047 | 0.230 | 0.066 | 0.037 | 0.120 | 0.351 |
| | DeepSeek-R1 | 0.072 | 0.230 | 0.471 | 0.018 | 0.060 | 0.194 | 0.167 | 0.031 | 0.015 | 0.051 | 0.333 | 0.097 | 0.049 | 0.159 | 0.324 |
| | Llama-3.1-70B | 0.073 | 0.170 | 0.542 | 0.022 | 0.038 | 0.082 | 0.470 | 0.052 | 0.014 | 0.028 | 0.178 | 0.158 | 0.042 | 0.093 | 0.397 |

### 2.2 基于条件的查询上的结果

**观察 1。对于不同的 LLM，GPT-4o 与 DeepSeek-R1 优于其他模型。** 如表 2 所示，GPT-4o 在电影与图书数据集上都取得最高的 Precision 以及次高的 CMR 平均分，而 DeepSeek-R1 在 Recall 上排名第一、在 Precision 上排名第二。值得注意的是，具有先进推理能力的模型，例如 DeepSeek-R1，擅长处理需要推理的查询类型。例如，在隐式条件查询中，当从显式条件过渡到隐式条件时，DeepSeek-R1 的性能下降显著小于其他模型。这使它成为隐式条件查询性能的领先者。这表明先进的推理能力使基于 LLM 的助手能够推断条件中未明确提及的隐式属性，从而得到更准确的推荐。附录 B 中有一个案例研究。

**观察 2。对于不同的查询类型，模型性能随查询难度增加而下降。** 在电影与图书数据集上，大多数 LLM 在显式条件查询上表现最好，优于另外两种查询类型。这表明 LLM 更擅长处理清楚陈述条件的查询。相比之下，隐式条件带来更大挑战，因为模型必须推断关于物品的、未被明确陈述的约束。值得注意的是，DeepSeek-R1 等具有强推理能力的模型保持强性能，表明其受益于推理能力。此外，错误信息条件被证明最困难，Recall 与 CMR 最低，表明当查询包含误导信息时，提供个性化推荐经常失败。而且，

<!-- 原 PDF 第 7 页 -->

图 4 见原 PDF。

**图 4：** 条件数量的影响。图中包含显式查询、隐式查询与错误信息查询，曲线为 Recall、Precision、CMR 与 FTR。

在该条件下更高的 FTR 表明，基于 LLM 的助手可能利用一般知识来检测查询中的错误信息，并避免直接生成不准确的推荐。

**观察 3。对于查询中不同的条件数量，Precision 与 Recall 随条件增多而提高，而 CMR 在显式条件查询上下降、在其他查询上上升。** 如图 4 所示，我们以电影数据集为例，研究改变查询中条件数量对模型性能的影响。我们注意到，额外的条件缩小推荐范围，从而提高推荐准确性。例如，「2010 年之后上映的 Nolan 动作电影」的候选集合远小于「Nolan 的电影」，减少了歧义并提高了推荐的相关性。条件数量对 CMR 指标的影响因查询类型而异。在显式条件查询中，单一条件时 CMR 最高，因为增加更多条件会提高满足全部约束的难度，导致覆盖下降。相比之下，对于隐式与错误信息条件查询，额外条件提供更多上下文，使模型能够更好地推断隐式条件，并降低条件中事实错误的影响。因此，在这些查询类型中，CMR 随条件增多而提高。

**观察 4。对于用户—物品交互历史的影响，纳入它们以两种关键方式增强推荐质量。** 纳入用户—物品交互历史的影响如图 5 所示。第一，纳入用户—物品历史通过生成更个性化的推荐列表，在所有查询类型上提高 Precision。原因可能是，条件有限的查询（例如「由 Nolan 导演的电影」）往往产生很大的候选池。通过利用历史交互，模型可以优先选择与用户偏好对齐并满足查询条件的物品，从而有效过滤无关候选。

第二，纳入用户历史并不总是提高 CMR。通过分析 LLM 助手的输出，我们注意到加入历史也可能引入降低模型严格遵守条件程度的「干扰」物品。例如，由于用户历史中的奇幻类型偏向，LLM 助手可能为「Nolan 的电影」推荐 “The Prestige”。这表明纳入历史可能转移模型的注意力，使严格遵守给定条件变得更困难。这些结果凸显一个重要的权衡：纳入历史可以增强模型对用户偏好的理解，但也可能妨碍模型与查询中具体要求紧密对齐的能力。因此，平衡历史数据的影响与精确遵守条件的需要，对于优化推荐助手的性能至关重要。

图 5 见原 PDF。

**图 5：** 纳入用户—物品历史的影响。子图为显式/隐式/错误信息条件下的 Precision 与 CMR，比较 GPT-4o、Gemini、Claude 在有历史与无历史时的结果。

**观察 5。要求 LLM 生成 $K$ 条推荐与先前的观察一致。** 对于基于条件的查询，存在一些样本，其查询条件所能满足的物品数量可能少于 $K$。在这种情况下，要求模型输出 $K$ 条推荐可能导致次优结果。因此，在表 2 给出的主实验中，我们并不要求模型生成 $K$ 条推荐。然而，为进一步探索这一点，我们也进行了额外实验，指示 LLM 输出 $K$ 件物品。结果如表 3 所示，基于电影数据集，并与先前发现一致：LLM 在显式条件查询上表现最好，在隐式条件与错误信息条件查询上性能逐渐下降。

**表 3：** 基于条件的查询在 $K=5$ 时的结果。

| 模型 | 显式 Recall | 显式 CMR | 隐式 Recall | 隐式 CMR | 错误信息 Recall | 错误信息 CMR | 平均 Recall | 平均 CMR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-4o | 0.436 | 0.657 | 0.245 | 0.266 | 0.052 | 0.077 | 0.244 | 0.333 |
| Gemini | 0.416 | 0.607 | 0.205 | 0.195 | 0.048 | 0.062 | 0.223 | 0.288 |
| Claude | 0.436 | 0.647 | 0.247 | 0.277 | 0.075 | 0.105 | 0.253 | 0.343 |

**观察 6。对于微调的性能，SFT 与 RFT 都显著增强模型的推荐性能。** 鉴于近来使用 RFT 来改进模型推理能力的兴趣 [27, 34]，我们旨在探索它在这一上下文中的潜力。我们把全参数 SFT 与 RFT（基于 GRPO [27] 算法）应用于微调 Qwen-2.5-3B-Instruct 与 LLaMA-3.2-3B-Instruct 模型，并评估不同查询类型上的 Recall 性能。如表 4 所示，两种微调范式都显著改进了模型的推荐性能。然而，仅用 RFT 训练的模型比用 SFT 训练的模型更差。这一性能

**表 4：** 基于条件的查询上的微调性能。表中数字为 Recall。

| 领域 | 模型 | 微调 | 显式 | 隐式 | 错误信息 |
| --- | --- | --- | --- | --- | --- |
| Movie | Qwen-2.5-3B | - | 0.019 | 0.002 | 0.004 |
| | | SFT | 0.391 | 0.255 | 0.296 |
| | | RFT | 0.178 | 0.119 | 0.089 |
| | | SFT+RFT | 0.410 | 0.262 | 0.307 |
| | Llama-3.2-3B | - | 0.018 | 0.003 | 0.003 |
| | | SFT | 0.285 | 0.176 | 0.186 |
| | | RFT | 0.191 | 0.124 | 0.080 |
| | | SFT+RFT | 0.293 | 0.181 | 0.195 |
| Book | Qwen-2.5-3B | - | 0.012 | 0.007 | 0.002 |
| | | SFT | 0.136 | 0.251 | 0.249 |
| | | RFT | 0.055 | 0.090 | 0.081 |
| | | SFT+RFT | 0.139 | 0.262 | 0.264 |
| | Llama-3.2-3B | - | 0.006 | 0.004 | 0.002 |
| | | SFT | 0.088 | 0.221 | 0.181 |
| | | RFT | 0.056 | 0.092 | 0.090 |
| | | SFT+RFT | 0.112 | 0.237 | 0.190 |

<!-- 原 PDF 第 8 页 -->

差距可能归因于推理缺少预热阶段，而预热对于强化学习期间的有效探索是必要的 [1]。为验证这一点，我们进一步把训练过程分为两个阶段：首先应用 SFT 作为预热，然后进行 RFT 训练。实验结果表明，这一两阶段方法进一步提高了 LLM 的性能。例如，在电影的显式条件查询上，SFT+RFT 模型取得 0.410 的 Recall，优于仅 SFT 的模型（0.391）和仅 RFT 的模型（0.178）。

**表 5：** 基于用户画像的查询上的性能。/ 分别表示最佳结果与次佳结果。Book 没有基于人口统计的查询，对应单元格为 “-”。

| 领域 | 模型 | 基于兴趣 P↑ | R↑ | FTR↓ | 基于人口统计 P↑ | R↑ | FTR↓ | 平均 P↑ | R↑ | FTR↓ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Movie | GPT-4o-mini | 0.013 | 0.058 | 0.000 | 0.018 | 0.054 | 0.000 | 0.015 | 0.056 | 0.000 |
| | GPT-4o | 0.018 | 0.067 | 0.001 | 0.021 | 0.059 | 0.000 | 0.020 | 0.063 | 0.000 |
| | Gemini | 0.019 | 0.072 | 0.007 | 0.019 | 0.063 | 0.000 | 0.019 | 0.072 | 0.004 |
| | Claude | 0.015 | 0.082 | 0.000 | 0.018 | 0.054 | 0.000 | 0.017 | 0.068 | 0.000 |
| | DeepSeek-V3 | 0.015 | 0.071 | 0.000 | 0.019 | 0.060 | 0.000 | 0.017 | 0.066 | 0.000 |
| | DeepSeek-R1 | 0.014 | 0.081 | 0.000 | 0.015 | 0.068 | 0.000 | 0.015 | 0.075 | 0.000 |
| | Llama-3.1-70B | 0.014 | 0.061 | 0.000 | 0.015 | 0.046 | 0.000 | 0.015 | 0.054 | 0.000 |
| Book | GPT-4o-mini | 0.038 | 0.104 | 0.004 | - | - | - | 0.038 | 0.104 | 0.004 |
| | GPT-4o | 0.043 | 0.101 | 0.022 | - | - | - | 0.043 | 0.101 | 0.022 |
| | Gemini | 0.056 | 0.127 | 0.049 | - | - | - | 0.056 | 0.127 | 0.049 |
| | Claude | 0.018 | 0.072 | 0.012 | - | - | - | 0.018 | 0.072 | 0.012 |
| | DeepSeek-V3 | 0.020 | 0.081 | 0.005 | - | - | - | 0.020 | 0.081 | 0.005 |
| | DeepSeek-R1 | 0.030 | 0.112 | 0.031 | - | - | - | 0.030 | 0.112 | 0.031 |
| | Llama-3.1-70B | 0.049 | 0.098 | 0.003 | - | - | - | 0.049 | 0.098 | 0.003 |

### 2.3 基于用户画像的查询上的结果

**观察 7。对于不同的 LLM，Gemini-1.5 Pro 与 DeepSeek-R1 相比其他模型表现更好。** 如表 5 所示，DeepSeek-R1 与 Gemini-1.5-Pro 等更大、更先进的模型持续取得更高的 Precision 与 Recall。相比之下，GPT-4o-mini 等较小模型往往落后。从 FTR（未能推荐）指标来看，大多数模型表现出低失败率，表明它们能够有效遵循指令并按要求的格式生成推荐列表。

**观察 8。对于不同的查询类型，基于人口统计的查询的 Recall 低于基于兴趣的查询，但 Precision 相似。** 在所有模型上，基于人口统计的查询的 Recall 总体上低于基于兴趣的查询。这表明当依赖用户人口统计时，LLM 难以识别相关推荐。Recall 的差异可归因于这些查询的构建方式不同。基于兴趣的查询利用清晰的兴趣，使模型更容易生成相关推荐。相比之下，基于人口统计的查询要求推荐助手从更广泛的人口统计与行为趋势中推断偏好，这引入更多变异性与歧义。

**观察 9。对于基于兴趣的查询，由较不普遍的兴趣构造的查询往往更具挑战。** 如图 6 所示，我们按流行度把查询分为四组，并在电影与图书数据集上进行实验。可以观察到，被更多用户共享的兴趣往往产生更高的 Precision 与 Recall。这很可能是因为广泛共享的兴趣更容易被 LLM 识别和解释，从而带来更好的性能。相比之下，图书领域呈现相反趋势。这是由于图书数据与评估过程的性质。图书常常有多个版本或出版商，流行书名往往有更多变体。

图 6 见原 PDF。

**图 6：** 兴趣流行度对 Precision 与 Recall 的影响。

因此，流行图书（例如 “Dune”）可能得到更低的指标，因为 LLM 混淆版本/出版商（例如 “Dune: 1965” 与 “2021 adaptation”）。对于较不流行的图书，变体更少，LLM 更容易给出精确匹配，从而导致更高的性能指标。

图 7 见原 PDF。

**图 7：** 不同人口统计的查询性能。

**观察 10。对于基于人口统计的查询，LLM 的性能基于不同用户人口统计呈现明显变化。** 例如，如图 7 所示，我们注意到模型对女性用户表现出更高的准确性。这反映了女性用户更一致的偏好模式（例如浪漫喜剧等稳定的类型偏好），使模型能够作出准确推荐。从年龄角度看，LLM 对 50–55 岁的人在 Recall 上表现更好。这很可能是因为他们的偏好更集中，并且与更年轻的用户相比，较少受快速变化的流行文化影响；更年轻的用户往往有更多样的偏好。对于 56 岁及以上的用户，模型的有效性不如 50–55 岁年龄组，可能是因为年长用户较少频繁参与在线活动，例如给电影评分。因此，LLM 的训练集中关于该年龄组的数据更少，使 LLM 更难理解他们的偏好。

**观察 11。对于基于用户画像的查询，两种微调方法都带来明显的性能增益。** 如表 6 所示，

**表 6：** 基于用户画像的查询上的微调。表中数字为 Recall。Book 无基于人口统计的查询。

| 领域 | 模型 | 微调 | 基于兴趣 | 基于人口统计 |
| --- | --- | --- | --- | --- |
| Movie | Qwen-2.5-3B | - | 0.015 | 0.029 |
| | | SFT | 0.287 | 0.154 |
| | | RFT | 0.143 | 0.228 |
| | | SFT+RFT | 0.289 | 0.230 |
| | Llama-3.2-3B | - | 0.014 | 0.019 |
| | | SFT | 0.139 | 0.102 |
| | | RFT | 0.111 | 0.122 |
| | | SFT+RFT | 0.144 | 0.131 |
| Book | Qwen-2.5-3B | - | 0.026 | - |
| | | SFT | 0.268 | - |
| | | RFT | 0.108 | - |
| | | SFT+RFT | 0.270 | - |
| | Llama-3.2-3B | - | 0.022 | - |
| | | SFT | 0.189 | - |
| | | RFT | 0.095 | - |
| | | SFT+RFT | 0.193 | - |

<!-- 原 PDF 第 9 页 -->

所有微调后的模型都持续优于基座模型。SFT+RFT 方法给出最强的总体性能，SFT 紧随其后。然而，在某些情况下——例如基于人口统计的查询——RFT 优于 SFT；例如，在 Qwen-2.5-3B 模型上，RFT 取得 0.228 的 Recall，而 SFT 为 0.154。我们还观察到，微调之后 Qwen 模型总体上比 LLaMA 模型结果更好。

## 3 相关工作

基于 LLM 的推荐系统的近期进展 [23, 24, 33] 促成了各种用于评估其能力的基准 [13, 18, 29, 35, 36]。LLMRec [18] 等早期工作聚焦传统推荐任务（例如评分预测、序列推荐），为 LLM 相对于经典方法建立基线。除传统推荐任务外，近期研究日益聚焦于评估 LLM 用于推荐的独特特征。例如，一项近期研究 [13] 引入一个多维框架，不仅评估效用与新颖性，还评估 LLM 的特定行为，如历史长度敏感性（在稀疏用户历史上推荐表现如何）与幻觉（生成不存在的物品）。类似地，PerRecBench [29] 通过消除用户与物品评分中的偏差来隔离个性化准确性，测试 LLM 是否推断用户偏好。

与此同时，随着 LLM 的兴起，已提出各种基准来评估它们作为助手的能力。例如，Gaia [20] 衡量 LLM 作为通用 AI 助手的能力。此外，VoiceBench（面向语音助手）[5] 与 Mobile-Bench（面向移动助手）[3] 等领域特定框架评估 LLM 作为特定助手的能力。然而，尽管推荐评估与助手评估都有进展，在把 LLM 作为个性化推荐助手进行评估方面仍存在空白。为弥合这一空白，我们引入 RecBench+，一个用于评估 LLM 作为个性化推荐助手之潜力的新基准。

## 4 结论

在本文中，我们为下一代推荐系统引入一种新范式，并提出一个新的基准数据集 RecBench+，以评估 LLM 作为个性化推荐助手的潜力。我们的基准包括五种专门设计的查询类型，全面评估基于 LLM 的助手在真实场景中处理复杂用户查询的能力。我们在一组多样的 LLM 上进行大量实验，包括具有先进推理能力的模型。通过这些实验，我们给出 11 条详细观察，阐明 LLM 作为个性化推荐助手的优势与局限。我们还探索了不同微调策略对增强推荐性能的影响。我们希望我们的基准与发现为该领域未来的研究与开发奠定基础。

## 致谢

本文所描述的研究部分得到香港研究资助局优配研究金的支持（项目编号 PolyU 15207322、15200023、15206024 与 15224524），以及香港理工大学内部研究经费（项目编号 P0042693、P0048625 与 P0051361）。本工作由香港理工大学大模型中心（The Centre for Large AI Models，CLAIM）提供的计算资源支持。

## 案例研究（页面中的示例框）

**查询：** 我最近喜欢 Taps (1981) 与 Absence of Malice (1981) 中的摄影，两者都展示了 Scott Ambrozy 了不起的工作。我渴望找到更多体现他摄影风格的电影。有推荐吗？

**真实标签：** 3 Days of the Condor (a.k.a. Three Days of the Condor) (1975)，Network (1976)，The Exorcist (1973)，The Stepford Wives (1975)；或 “None”。

**输出（DeepSeek-V3）：** The Chosen (1981)，Four Friends (1981)，Split Image (1982)，Heart Like a Wheel (1983)。✗

**输出（DeepSeek-R1）：** The French Connection (1971)，The Exorcist (1973)，Network (1976)，Three Days of the Condor (1975)，The Electric Horseman (1979)，Straight Time (1978)，The Prince of the City (1981)，Wyatt Earp (1994)。注：上面列出的电影体现了 Owen Roizman 的摄影，他拍摄了 Taps 与 Absence of Malice。Scott Ambrozy 似乎是查询中的混淆或错字。✓

**推理（DeepSeek-R1）：** ……等等，首先，Scott Ambrozy 是谁？我知道一些大牌摄影指导，但这个名字并不耳熟。也许我应该核实业界是否有 Scott Ambrozy。让我想想。也许用户把名字拼错了？在 IMDb 上查 Taps，对，Owen Roizman 是 Taps 的摄影指导。Absence of Malice 也列出 Owen Roizman。所以 Scott Ambrozy 可能是与另一个名字的混淆。因此用户大概指的是 Owen Roizman。所以要正确回答，我应当推荐 Owen Roizman 的其他电影。既然用户想要具有他摄影风格的电影，我应当列出那些。Roizman 的著名作品包括……

## 附录

### A 模型测试所用提示

我们用于测试不同 LLM 的提示是：

- 无用户—物品交互历史：你是一个电影推荐系统。你得到一条来自用户的查询。你需要推荐满足用户查询的电影。请直接输出推荐的电影；不要输出其他内容。
- 有用户—物品交互历史：你是一个电影（/图书）推荐系统。你得到用户看过的电影（/阅读历史）以及一条来自用户的查询。你需要推荐满足用户查询与用户偏好的电影（/图书）。请直接输出推荐的电影；不要输出其他内容。

### B 案例研究

我们给出一个案例研究，以说明 LLM 如何处理复杂用户查询。在该例中，用户寻找与两部给定电影同一位摄影指导的电影。缺乏强推理能力的模型 DeepSeek-V3 错误地列出 Scott Ambrozy 的电影，导致不正确的推荐。相比之下，DeepSeek-R1 首先核实 Scott Ambrozy 是否为摄影指导，然后正确识别 Owen Roizman 才是实际的摄影指导。它最终推断用户意在询问 Roizman 的电影，并给出准确的推荐。

<!-- 原 PDF 第 10 页 -->

## 伦理考量

我们的工作利用 LLM 与公开推荐数据集来生成查询。我们已在论文正文中描述数据集生成过程的细节。值得注意的是，数据集中的所有数据都经过人类标注者检查，以避免有害内容。因此，我们的数据集不对人类社会构成任何潜在伤害。

## 参考文献

[1] Hongyi James Cai, Junlin Wang, Xiaoyin Chen, and Bhuwan Dhingra. 2025. 多少回溯才够？探索 SFT 与 RL 在增强 LLM 推理中的相互作用. arXiv preprint arXiv:2505.24273 (2025).

[2] Jiao Chen, Luyi Ma, Xiaohan Li, Nikhil Thakurdesai, Jianpeng Xu, Jason HD Cho, Kaushiki Nag, Evren Korpeoglu, Sushant Kumar, and Kannan Achan. 2023. 知识图谱补全模型是少样本学习者：用 LLM 对电子商务中关系标注的实证研究. arXiv preprint arXiv:2305.09858 (2023).

[3] Yiming Chen, Xianghu Yue, Chen Zhang, Xiaoxue Gao, Robby T Tan, and Haizhou Li. 2024. VoiceBench：对基于 LLM 的语音助手进行基准评测. arXiv preprint arXiv:2410.17196 (2024).

[4] James Davidson, Benjamin Liebald, Junning Liu, Palash Nandy, Taylor Van Vleet, Ullas Gargi, Sujoy Gupta, Yu He, Mike Lambert, Blake Livingston, et al. 2010. YouTube 视频推荐系统. In Proceedings of the fourth ACM conference on Recommender systems. 293–296.

[5] Shihan Deng, Weikai Xu, Hongda Sun, Wei Liu, Tao Tan, Jianfeng Liu, Ang Li, Jian Luan, Bin Wang, Rui Yan, et al. 2024. Mobile-Bench：面向基于 LLM 的移动智能体的评估基准. arXiv preprint arXiv:2407.00993 (2024).

[6] Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan, et al. 2024. Llama 3 模型群. arXiv preprint arXiv:2407.21783 (2024).

[7] Yunfan Gao, Tao Sheng, Youlin Xiang, Yun Xiong, Haofen Wang, and Jiawei Zhang. 2023. Chat-Rec：迈向交互式、可解释的、由 LLM 增强的推荐系统. arXiv preprint arXiv:2303.14524 (2023).

[8] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al. 2025. DeepSeek-R1：通过强化学习激励 LLM 的推理能力. arXiv preprint arXiv:2501.12948 (2025).

[9] F Maxwell Harper and Joseph A Konstan. 2015. MovieLens 数据集：历史与上下文. Acm transactions on interactive intelligent systems (tiis) 5, 4 (2015), 1–19.

[10] Xiangnan He, Kuan Deng, Xiang Wang, Yan Li, Yongdong Zhang, and Meng Wang. 2020. LightGCN：简化并强化用于推荐的图卷积网络. In Proceedings of the 43rd International ACM SIGIR conference on research and development in Information Retrieval. 639–648.

[11] Aaron Hurst, Adam Lerer, Adam P Goucher, Adam Perelman, Aditya Ramesh, Aidan Clark, AJ Ostrow, Akila Welihinda, Alan Hayes, Alec Radford, et al. 2024. GPT-4o 系统卡. arXiv preprint arXiv:2410.21276 (2024).

[12] Aaron Jaech, Adam Kalai, Adam Lerer, Adam Richardson, Ahmed El-Kishky, Aiden Low, Alec Helyar, Aleksander Madry, Alex Beutel, Alex Carney, et al. 2024. OpenAI o1 系统卡. arXiv preprint arXiv:2412.16720 (2024).

[13] Chumeng Jiang, Jiayin Wang, Weizhi Ma, Charles LA Clarke, Shuai Wang, Chuhan Wu, and Min Zhang. 2024. 超越效用：把 LLM 作为推荐系统进行评估. arXiv preprint arXiv:2411.00331 (2024).

[14] Majeed Kazemitabaar, Runlong Ye, Xiaoning Wang, Austin Zachary Henley, Paul Denny, Michelle Craig, and Tovi Grossman. 2024. CodeAid：评估一种在课堂中部署的、平衡学生与教育者需求的基于 LLM 的编程助手. In Proceedings of the 2024 chi conference on human factors in computing systems. 1–20.

[15] Yehuda Koren, Robert Bell, and Chris Volinsky. 2009. 推荐系统的矩阵分解技术. Computer 42, 8 (2009), 30–37.

[16] Jiayi Liao, Sihang Li, Zhengyi Yang, Jiancan Wu, Yancheng Yuan, Xiang Wang, and Xiangnan He. 2024. LLaRA：大语言推荐助手. In Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval. 1785–1795.

[17] Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chenyu Zhang, Chong Ruan, et al. 2024. DeepSeek-V3 技术报告. arXiv preprint arXiv:2412.19437 (2024).

[18] Junling Liu, Chao Liu, Peilin Zhou, Qichen Ye, Dading Chong, Kang Zhou, Yueqi Xie, Yuwei Cao, Shoujin Wang, Chenyu You, et al. 2023. LLMRec：在推荐任务上对大语言模型进行基准评测. arXiv preprint arXiv:2308.12241 (2023).

[19] Xiao Liu, Bo Qin, Dongzhu Liang, Guang Dong, Hanyu Lai, Hanchen Zhang, Hanlin Zhao, Iat Long Iong, Jiadai Sun, Jiaqi Wang, et al. 2024. AutoGLM：面向图形界面的自主基础智能体. arXiv preprint arXiv:2411.00820 (2024).

[20] Grégoire Mialon, Clémentine Fourrier, Thomas Wolf, Yann LeCun, and Thomas Scialom. 2023. GAIA：通用 AI 助手的基准. In The Twelfth International Conference on Learning Representations.

[21] Jianmo Ni, Jiacheng Li, and Julian McAuley. 2019. 用远程标注的评论与细粒度方面来为推荐提供理由. In Proceedings of the 2019 conference on empirical methods in natural language processing and the 9th international joint conference on natural language processing (EMNLP-IJCNLP). 188–197.

[22] Gustavo Pinto, Cleidson De Souza, João Batista Neto, Alberto Souza, Tarcísio Gotto, and Edward Monteiro. 2024. 构建 StackSpot AI 的经验：一种上下文化的 AI 编程助手. In Proceedings of the 46th International Conference on Software Engineering: Software Engineering in Practice. 408–417.

[23] Haohao Qu, Wenqi Fan, and Shanru Lin. 2025. 用连续词元扩散做生成式推荐. arXiv preprint arXiv:2504.12007 (2025).

[24] Haohao Qu, Wenqi Fan, Zihuai Zhao, and Qing Li. 2024. TokenRec：学习为基于 LLM 的生成式推荐对 ID 进行词元化. arXiv preprint arXiv:2406.10450 (2024).

[25] Markus Schedl. 2016. 用于音乐检索与推荐的 LFM-1b 数据集. In Proceedings of the 2016 ACM on international conference on multimedia retrieval. 103–110.

[26] Samuel Schmidgall, Yusheng Su, Ze Wang, Ximeng Sun, Jialian Wu, Xiaodong Yu, Jiang Liu, Zicheng Liu, and Emad Barsoum. 2025. Agent Laboratory：把 LLM 智能体用作研究助手. arXiv preprint arXiv:2501.04227 (2025).

[27] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, YK Li, Yang Wu, et al. 2024. DeepSeekMath：推动开放语言模型中数学推理的极限. arXiv preprint arXiv:2402.03300 (2024).

[28] Harmanpreet Singh, Nikhil Verma, Yixiao Wang, Manasa Bharadwaj, Homa Fashandi, Kevin Ferreira, and Chul Lee. 2024. 个人大语言模型智能体：量身定制的旅行规划案例研究. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing: Industry Track. 486–514.

[29] Zhaoxuan Tan, Zinan Zeng, Qingkai Zeng, Zhenyu Wu, Zheyuan Liu, Fengran Mo, and Meng Jiang. 2025. 大语言模型能否理解个性化推荐中的偏好？ arXiv preprint arXiv:2501.13391 (2025).

[30] Gemini Team, Rohan Anil, Sebastian Borgeaud, Jean-Baptiste Alayrac, Jiahui Yu, Radu Soricut, Johan Schalkwyk, Andrew M Dai, Anja Hauth, Katie Millican, et al. 2023. Gemini：一族能力很强的多模态模型. arXiv preprint arXiv:2312.11805 (2023).

[31] Gemini Team, Petko Georgiev, Ving Ian Lei, Ryan Burnell, Libin Bai, Anmol Gulati, Garrett Tanzer, Damien Vincent, Zhufeng Pan, Shibo Wang, et al. 2024. Gemini 1.5：解锁跨越数百万词元上下文的多模态理解. arXiv preprint arXiv:2403.05530 (2024).

[32] María Cora Urdaneta-Ponte, Amaia Mendez-Zorrilla, and Ibon Oleagordia-Ruiz. 2021. 面向教育的推荐系统：系统综述. Electronics 10, 14 (2021), 1611.

[33] Shijie Wang, Wenqi Fan, Yue Feng, Shanru Lin, Xinyu Ma, Shuaiqiang Wang, and Dawei Yin. 2025. 面向基于 LLM 的推荐的知识图谱检索增强生成. arXiv preprint arXiv:2501.02226 (2025).

[34] Fengli Xu, Qianyue Hao, Zefang Zong, Jingwei Wang, Yunke Zhang, Jingyi Wang, Xiaochong Lan, Jiahui Gong, Tianjian Ouyang, Fanjin Meng, et al. 2025. 迈向大型推理模型：用大语言模型进行强化推理的综述. arXiv preprint arXiv:2501.09686 (2025).

[35] Haochen Xue, Feilong Tang, Ming Hu, Yexin Liu, Qidong Huang, Yulong Li, Chengzhi Liu, Zhongxing Xu, Chong Zhang, Chun-Mei Feng, et al. 2025. MMRC：用于理解真实对话中多模态大语言模型的大规模基准. arXiv preprint arXiv:2502.11903 (2025).

[36] Jizhi Zhang, Keqin Bao, Yang Zhang, Wenjie Wang, Fuli Feng, and Xiangnan He. 2023. ChatGPT 对推荐公平吗？评估大语言模型推荐中的公平性. In Proceedings of the 17th ACM Conference on Recommender Systems. 993–999.

<!-- 译完 -->
