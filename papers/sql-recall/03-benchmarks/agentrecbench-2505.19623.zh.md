# AgentRecBench：对基于 LLM 智能体的个性化推荐系统进行基准评测

- 原文件名：agentrecbench-2505.19623.pdf
- 原标题：AgentRecBench: Benchmarking LLM Agent-based Personalized Recommender Systems
- 中文标题：AgentRecBench：对基于 LLM 智能体的个性化推荐系统进行基准评测
- 作者：Yu Shang、Peijie Liu、Yuwei Yan、Zijing Wu、Leheng Sheng、Yuanqing Yu、Chumeng Jiang、An Zhang、Fengli Xu、Yu Wang、Min Zhang、Yong Li
- 会议或 arXiv：Preprint；arXiv:2505.19623v2 [cs.IR] 28 May 2025（见 PDF 第 1 页页脚）

<!-- 原 PDF 第 1 页 -->

**Yu Shang**<sup>1∗</sup>，**Peijie Liu**<sup>1∗</sup>，**Yuwei Yan**<sup>2</sup>，**Zijing Wu**<sup>3</sup>，**Leheng Sheng**<sup>4</sup>，**Yuanqing Yu**<sup>1</sup>，**Chumeng Jiang**<sup>1</sup>，**An Zhang**<sup>3</sup>，**Fengli Xu**<sup>1</sup>，**Yu Wang**<sup>1</sup>，**Min Zhang**<sup>1</sup>，**Yong Li**<sup>1</sup>

<sup>1</sup> Tsinghua University  
<sup>2</sup> The Hong Kong University of Science and Technology (Guangzhou)  
<sup>3</sup> University of Science and Technology of China  
<sup>4</sup> National University of Singapore

## 摘要

由大语言模型（LLM）驱动的智能体推荐系统的出现，代表个性化推荐的一次范式转变：它利用 LLM 先进的推理与角色扮演能力，实现自主、自适应的决策。与传统推荐方法不同，智能体推荐系统能够从复杂环境中动态收集并解释用户—物品交互，生成可在多样场景中泛化的稳健推荐策略。然而，该领域目前缺乏标准化评估协议来系统评估这些方法。为填补这一关键空白，我们提出：（1）一个交互式文本推荐模拟器，纳入丰富的用户与物品元数据，以及三种典型评估场景（经典、兴趣演化与冷启动推荐任务）；（2）一个用于开发和研究智能体推荐系统的统一模块化框架；（3）首个全面基准，比较 10 种经典与智能体推荐方法。我们的发现表明智能体系统的优越性，并为其核心组件建立可操作的设计准则。该基准环境已通过一场公开挑战得到严格验证，并保持公开可用，配有持续维护的排行榜<sup>†</sup>，以促进持续的社区参与与可复现研究。基准可在以下地址获取：https://huggingface.co/datasets/SGJQovo/AgentRecBench。

## 1 引言

推荐系统通过建模用户偏好，已成为应对网络平台信息过载所不可或缺的工具 [1–4]。数十年来，该领域已从基于规则的推荐 [5, 6] 演化到数据驱动的深度学习方法 [7, 8]，在准确性与效率上取得显著收益。尽管有这些进展，仍存在一些关键挑战，包括：（1）推荐的黑箱性质限制了推荐结果的可解释性 [9, 10]；（2）大多数方法主要依赖历史交互数据，未能充分利用真实应用中丰富的上下文信息 [11]；（3）现有方法往往依赖手工特征与固定的推荐策略 [12]，这制约了它们对不同场景的适应能力。

基于 LLM 的智能体的近期进展，为革新推荐系统范式提供了变革性机会 [13–17]。凭借 LLM 带来的复杂推理与角色扮演

<!-- 原 PDF 第 2 页 -->

能力，基于 LLM 的智能体可以通过类人的规划 [18, 19]、反思式推理 [20, 21] 与迭代行动 [22, 23] 自动处理复杂任务。与传统推荐系统相比，智能体推荐系统有若干关键优势。首先，以自然语言为媒介，这些系统可以显式阐述其推荐逻辑，增强透明度并培养用户信任。其次，凭借先进的感知与推理能力，智能体推荐系统可以自主地从环境中收集并整合丰富的个性化上下文信息，超越基于 ID 的交互以丰富用户建模。第三，这些系统通过与环境的交互表现出持续的自我改进，通过纳入外部反馈与内部记忆来动态精炼推荐策略，从而在各种场景中实现前所未有的适应性。

尽管这一范式转变前景可观，该领域目前缺乏标准化基准来系统评估智能体推荐方法，阻碍了我们对其有效性与实际部署的理解。为弥合这一差距，我们引入 AgentRecBench，首个面向智能体推荐系统的全面基准。我们的基准为推进智能体推荐系统作出四项关键贡献。第一，我们通过处理 Yelp、GoodReads 与 Amazon 数据集，构建统一的文本交互环境。该环境提供标准化函数接口，使智能体能够在各种条件下进行灵活的信息检索，同时维持一个全面的多领域数据库。第二，我们建立三种精心设计的评估场景：用于一般性能评估的经典推荐任务、用于评估动态适应能力的兴趣演化任务，以及用于衡量泛化能力的冷启动任务。这些场景共同反映真实推荐系统中的核心挑战。第三，我们提出一个带有必要认知组件 [24, 25] 的模块化智能体框架，用于快速构建智能体推荐系统。该框架包括四个核心模块：用于任务分解的动态规划、用于决策的复杂推理、用于环境交互的工具利用，以及用于经验保留与利用的记忆管理。最后，通过对 10 种现有推荐智能体与传统方法进行广泛评估，我们建立了智能体推荐系统的首个全面基准。我们的分析揭示当前能力与局限的关键见解，并由此导出实用的设计准则，以促进这一新兴领域的未来发展。

该基准的实际效用已通过 AgentSociety Challenge [13] 得到展示。该挑战在全球吸引了 295 支参赛队伍，并在 37 天的比赛中收到超过 1,400 份提交。参赛者在开发阶段的推荐赛道上取得 20.3% 的性能提升，在最终阶段又进一步获得 15.9% 的增益，验证了我们评估框架的实际效用。完整的基准环境保持公开可用，并配有持续维护的排行榜以支持正在进行的研究。

总之，本工作有如下主要贡献：

- 我们提出 AgentRecBench，首个大规模、全面的基准，在多样场景中系统评估新兴的智能体推荐系统与传统推荐方法。
- 我们提供一个配备多领域推荐数据集的文本环境模拟器，以及一个标准化的智能体开发框架，从而建立闭环的开发—评估流水线。该工具包有助于促进推荐智能体的快速原型制作与系统测试。
- 通过对 10 种方法的深入分析，我们提炼出当前方法中更优设计的关键见解。我们的发现提供可操作的设计准则，以启发更强大的智能体推荐系统。

<sup>∗</sup>同等贡献。

<sup>†</sup> https://tsinghua-fib-lab.github.io/AgentSocietyChallenge/pages/overview.html

预印本。arXiv:2505.19623v2 [cs.IR] 28 May 2025

## 2 智能体推荐系统的定义

我们把智能体推荐系统形式化为：一个基于 LLM 的智能体与环境 $E = (U, I, H)$ 交互以产生推荐。这里，$U$ 与 $I$ 分别表示用户与物品的特征空间，而 $H = \{(u, i, c, \tau)\}$ 表示带有上下文元数据 $c$（例如评分、评论）与时间戳 $\tau$ 的用户—物品历史交互。在每一步 $t$，智能体观察状态 $s_t \in S$（编码用户与物品画像、交互以及其他环境反馈），并通过策略 $\pi_\theta$ 选择动作 $a_t \in A$：

$$
a_t \sim \pi_\theta(a \mid s_t), \qquad \pi_\theta : S \rightarrow p(A), \qquad (1)
$$

其中 $p(A)$ 是动作空间 $A = I \cup A_{\mathrm{seek}}$ 上的概率分布，该空间包括物品推荐与信息寻求动作，$\theta$ 参数化智能体的内部功能模块，例如推理与记忆。

智能体推荐系统表现出三种将其与传统方法区分开的特征。第一，它可以自适应地从环境中收集个性化上下文信息，同时在多样场景中维持可泛化、零样本自适应的推荐策略。第二，系统通过持续精炼其内部表示与决策策略，借助积累的经验与外部反馈展现自我改进能力，从而实现持续的性能增强。第三，该系统有望通过战略性地发起有针对性的交互、超越被动回应范式，来增强主动参与。

<!-- 原 PDF 第 3 页 -->

## 3 文本环境模拟器

文本实验环境模拟社交与网络平台中通常具有的信息检索逻辑与功能。它提供一个标准化的交互空间，使推荐智能体能够系统地查询并接收反馈。该环境处理两个主要关切：定义清晰的交互空间，以及确保受控的数据可访问性。总体框架如图 1 所示。

图 1 见原 PDF。

**图 1：** 我们的交互式文本环境模拟器的总体框架。图中文字包括：用户、评论、物品；推荐智能体；场景 #1 与场景 #2 的智能体与任务；文本实验环境；网络构建；物品查询、评论查询、用户查询、标准查询；U/R/I；类型；排序方法；返回形式；数据集；U-R-I 网络。

### 3.1 数据与交互空间

清晰定义的交互空间对于可靠评估推荐智能体至关重要。它通过提供统一条件，使各种推荐方法之间能够进行一致比较。为此，我们把多样的数据源合并为一个连贯的网络结构，形成具有标准化查询能力的统一用户—评论—物品（U-R-I）网络。

构建 U-R-I 网络涉及聚合来自多个来源的数据，例如用户画像、物品特征以及用户生成内容（例如评论与评分）。用户节点表示与平台交互的个体，物品节点表示可推荐的实体，评论节点封装用户反馈与评分。这些节点之间的边说明交互，形成一个结构化、可导航的数据空间供智能体探索。

标准化查询功能定义为：

$$
\mathrm{Query}(\mathrm{Type}, \mathrm{SortMethod}, \mathrm{Formation}) \rightarrow \mathrm{StructuredData} \mid \mathrm{TextualData} \qquad (2)
$$

在该函数中，Type 指定检索的数据类型（例如用户、物品、评论）。SortMethod 定义查询结果如何排序，例如按日期、相关性或流行度。布尔量 Formation 指示返回数据的格式（结构化或文本）；结构化查询产生适合算法处理的明确定义属性（键—值），而文本查询返回用于解释性任务的自然语言内容。

<!-- 原 PDF 第 4 页 -->

然而，不同的推荐场景可能需要各种数据控制机制，例如时间过滤（例如把数据限制在特定时间范围内）、基于物品的过滤（例如选择具有最低评论阈值的物品），或基于用户属性的约束。

### 3.2 动态数据可见性控制

动态数据可见性控制旨在应对上文概述的、特定于场景的数据需求。如图 2 所示，核心概念是一个由场景与任务组成的两层控制系统。场景定义宽泛的过滤标准，为一组相关任务塑造环境，而每个任务聚焦于一个目标与上下文都明确的推荐目标。

场景被形式化地结构如下：

$$
\mathrm{Scenario} = \{\mathrm{TimeFilter}, \mathrm{ItemFilter}\}, \qquad (3)
$$

其中 TimeFilter 管理可访问数据的时间范围，例如选择在指定时期内发布的评论。ItemFilter 设定物品纳入标准，例如强制最低评论阈值以确保足够的数据质量。在每个场景内，任务指定一个精确的推荐问题：

$$
\mathrm{Task} = \{\mathrm{TargetUser}, \mathrm{GroundTruth}\}, \qquad (4)
$$

其中 TargetUser 标识为其生成推荐的个人，GroundTruth 提供评估推荐准确性所必需的基准数据（例如已知的用户偏好或过去的交互）。所提出的动态数据可见性控制确保灵活的、由场景驱动的数据可访问性管理，便于在多样实验条件下对智能体推荐系统进行全面而系统的评估。

图 2 见原 PDF。

**图 2：** 我们的文本环境模拟器的动态数据可见性控制工作流示意。图中文字包括：推荐场景 #1；智能体加载；场景上下文；任务；时间过滤；物品过滤；任务用户；任务真实标签；基准评测前的场景过滤（时间窗口、物品列表）；运行时的任务过滤（用户查询、评论查询、物品查询）。

## 4 实验设置

我们的实验评估利用三个大规模公开数据集（Yelp<sup>∗</sup>、GoodReads<sup>†</sup> 与 Amazon<sup>‡</sup>），它们共同提供大量用户交互记录以及丰富的用户/物品画像，从而能够进行全面的检索与个性化分析。下面，我们详细描述数据集、所定义的任务场景、基线与评估指标。

<sup>∗</sup> https://www.yelp.com/dataset

<sup>†</sup> https://sites.google.com/eng.ucsd.edu/ucsdbookgraph/home

<sup>‡</sup> https://amazon-reviews-2023.github.io/

<!-- 原 PDF 第 5 页 -->

**表 1：** 聚合数据的结构，包括用户侧、物品侧画像与评论信息。

| 数据类型 | 描述与关键字段 |
| --- | --- |
| 用户 | • 用户 ID；• 评论数；• 社交连接（好友关系）；• 平均评分 |
| 物品 | • 物品 ID；• 物品名称；• 类型（产品/商家/图书）；• 元数据（价格、标题、描述、位置等）；• 平均评分；• 评论数 |
| 评论 | • 评论 ID；• 用户 ID；• 物品 ID；• 评分（1–5）；• 文本评论内容；• 交互时间戳；• 有用性投票（funny/useful/cool） |

### 4.1 数据集

所使用的三个数据集介绍如下：

**Amazon。** Amazon 数据集捕捉电子商务平台上多个类目中的用户购买行为、产品评论与评分。它包含大规模用户—物品交互记录以及详细的文本评论，为建模消费者偏好提供丰富来源。

**GoodReads。** Goodreads 数据集由用户对图书的评分与评论组成，反映多样的阅读兴趣与偏好。该数据集对于在文学内容的上下文中研究推荐模型尤其有价值。

**Yelp。** Yelp 数据集包含用户对本地商家（包括餐厅与零售店）的大量评论与评分。它有效捕捉多种服务领域中的真实消费者体验与偏好。

我们把这些数据集组织为三个结构化子数据集（物品、用户与评论），以促进有效的智能体交互并增强用户与物品特征的抽取。这一结构化划分使个性化推荐的信息检索更高效。表 1 概括了结构化数据集的关键字段。如图 3（a）所示，该数据集呈现互补的领域覆盖：Yelp 贡献了大多数用户，Goodreads 提供了最广泛的物品。图 3（b）与（c）中用户/物品交互的幂律分布忠实地反映真实推荐场景：大多数用户参与程度中等，只有少数表现出极高的活跃水平。

### 4.2 任务场景

为系统评估智能体推荐系统，我们设计三种反映真实推荐挑战的代表性评估场景。下面给出每个场景的详细描述。

**经典推荐。** 这是我们的基础基准，在标准条件下评估一般性能：智能体可以从环境中访问完整的用户画像与交互。

**兴趣演化推荐。** 为严格评估智能体推荐系统的时间适应能力，我们设计一个多尺度评估框架，同时捕捉

<!-- 原 PDF 第 6 页 -->

图 3 见原 PDF。

**图 3：** 我们聚合的多平台数据集的统计分布，展示（a）用户/物品分布；（b）用户交互分布；（c）物品交互分布。

渐进的与即时的偏好动态。长期推荐任务使用三个月的用户交互窗口。我们抽样活跃用户（$\ge 5$ 次交互），测试系统识别稳定用户偏好的能力。该任务允许评估智能体进行纵向用户建模的能力。作为补充，短期推荐任务通过压缩为一周的交互窗口，聚焦即时适应。该任务主要衡量智能体建模新兴交互模式的能力。

**冷启动推荐。** 为系统评估智能体推荐系统应对真实数据稀疏挑战的能力，我们为用户侧与物品侧冷启动场景都设计了全面评估。在用户冷启动推荐中，我们构建由历史交互少于 $m$ 次的用户组成的测试集（$m$ 依赖于数据集）。该设定严格检验系统从稀疏交互信号生成准确推荐、并有效利用可用上下文用户数据的能力。对于物品冷启动推荐，我们在记录交互少于 $n$ 次的物品上评估，测试系统对物品属性进行推理、并检测与现有物品的相似模式的能力。该评估特别衡量智能体系统如何通过物品信息挖掘能力，超越传统基于 ID 的推荐方法的局限。

### 4.3 基线

我们在三种推荐系统范式上进行全面评估：

**传统推荐系统。** 我们选择矩阵分解（Matrix Factorization，MF）[5] 作为代表性的传统推荐方法。它把用户—物品交互矩阵分解为低维潜在因子，以捕捉隐式用户偏好与物品特征。

**基于深度学习的推荐系统。** LightGCN [8] 代表一种有效的、基于现代图学习的推荐方法，采用简化的图卷积操作，在用户—物品交互图中有效传播并聚合邻域信息。

**智能体推荐系统。** 我们的评估包括八种不同的可用智能体推荐系统，详述如下：

- **BaseAgent。** 一个手工构建的基础智能体，通过标准 LLM 推理直接生成推荐，没有额外的推理组件。
- **CoTAgent。** 用零样本思维链（chain-of-thought，CoT）[26] 提示扩展 BaseAgent，以生成显式的推荐理由并逐步决策。
- **MemoryAgent。** 用记忆机制 [19] 增强 BaseAgent，维护并检索相关交互历史以指导推荐。
- **CoTMemAgent。** 通过把思维链推理与记忆增强结合起来，将 CoTAgent 的推理能力与 MemoryAgent 的上下文保持结合起来。
- **Baseline666。** AgentSociety Challenge 推荐赛道的获胜方案 [13]，其特点是平台感知的特征抽取，根据数据源特征动态适配特征表示。

<!-- 原 PDF 第 7 页 -->

- **RecHackers。** AgentSociety Challenge 推荐赛道的第二名方案 [13]，通过把用户历史评论与详细物品属性全面整合，实现稳健的基于内容的推荐。
- **DummyAgent。** AgentSociety Challenge 推荐赛道的第三名方案 [13]，采用先进的评论特征工程，识别并利用高信息量内容以增强用户/物品建模。
- **Agent4Rec [15]。** 一个先进框架，通过编排 LLM 智能体交互，为复杂推荐场景实现多步推理。

### 4.4 评估指标

原文小节标题为 “Envaluation Metric”。

我们使用基于排序的指标评估推荐性能，重点是 Top-N 准确性。遵循标准评估协议 [5, 7]，每个测试实例由 20 个候选物品组成：一个从用户交互历史中抽样的真实正例物品，以及 19 个从未观测交互中抽样的负例物品。主要指标是 Hit Rate@N（HR@N），衡量真实物品出现在排序前 $N$ 位的概率（$N \in \{1, 3, 5\}$）。形式化为：

$$
\mathrm{HR@}N = \frac{1}{|T|} \sum_{t \in T} \mathbb{I}(p_t \in R^{N}_{t}), \qquad (5)
$$

其中 $T$ 是测试集，$p_t$ 是测试样本 $t$ 的真实正例物品，$R^{N}_{t}$ 表示前 $N$ 个推荐，$\mathbb{I}(\cdot)$ 是指示函数。

## 5 实验结果

在本节中，我们给出在 AgentRecBench 基准上评估的若干代表性基线方法的性能。分析分为三个关键部分：（1）总体性能；（2）冷启动场景中的性能；（3）用户兴趣演化下的性能。

### 5.1 主要性能

我们首先在经典推荐场景中评估模型性能。实验在三个数据集上、使用三个模型族进行：Qwen-72B-Instruct、DeepSeek-v3 与 GPT-4o-mini。详细结果概括于表 2。

我们在可用数据的一个子集上训练传统基线与基于深度学习的基线。然而，由于数据集高度稀疏，这些模型无法有效学习有意义的模式。因此，我们报告均值预测作为比较的参考点。实验结果揭示，预测准确性在 Amazon、Goodreads

**表 2：** 经典推荐任务上的性能比较，指标为平均 HR@N（$N=1,3,5$）。列分组为 Amazon、Goodreads、Yelp，每组下为 Qwen、Deepseek、GPT。

| 类别 | 方法 | Amazon Qwen | Amazon Deepseek | Amazon GPT | Goodreads Qwen | Goodreads Deepseek | Goodreads GPT | Yelp Qwen | Yelp Deepseek | Yelp GPT |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 传统 RS | MF | 15.0 | | | 15.0 | | | 15.0 | | |
| 基于深度学习的 RS | LightGCN | 15.0 | | | 15.0 | | | 15.0 | | |
| 智能体 RS | BaseAgent | 39.0 | 44.0 | 27.0 | 15.7 | 20.3 | 13.7 | 3.7 | 4.0 | 4.7 |
| | CoTAgent | 39.0 | 39.7 | 26.7 | 16.0 | 23.0 | 15.0 | 5.0 | 4.3 | 5.0 |
| | MemoryAgent | 37.3 | 43.7 | 0.0 | 17.3 | 18.0 | 0.0 | 5.3 | 3.7 | 0.0 |
| | CoTMemAgent | 37.0 | 33.3 | 0.0 | 16.7 | 17.3 | 0.0 | 3.7 | 4.3 | 0.0 |
| | Baseline666 | 69.0 | 60.0 | 44.7 | 45.0 | 54.7 | 33.0 | 7.0 | 7.3 | 6.0 |
| | DummyAgent | 44.0 | 54.0 | 31.0 | 46.0 | 56.3 | 23.7 | 5.3 | 6.3 | 5.7 |
| | RecHackers | 54.0 | 63.0 | 50.7 | 45.3 | 55.0 | 29.3 | 7.7 | 7.0 | 6.7 |
| | Agent4Rec | 23.3 | 28.3 | 17.7 | 9.3 | 9.3 | 9.3 | 5.7 | 7.6 | 5.3 |

注：MF 与 LightGCN 每个数据集只报告一个参考值 15.0，不按 Qwen/Deepseek/GPT 分开。

<!-- 原 PDF 第 8 页 -->

与 Yelp 数据集上逐渐下降，反映出推荐难度递增。Baseline666 在几乎所有设定中持续优于其他方法，表现出很强的稳健性。此外，Baseline666、DummyAgent 与 RecHackers 大幅优于更简单的设计，凸显结构良好的智能体工作流可以显著增强推荐性能。这些发现强调了智能体设计在提高基于智能体的推荐系统预测准确性中的关键作用。

**表 3：** 冷启动推荐任务上的性能比较，指标为平均 HR@N（$N=1,3,5$）。每个数据集下分为 User 与 Item。

| 类别 | 方法 | Amazon User | Amazon Item | Goodreads User | Goodreads Item | Yelp User | Yelp Item |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 传统 RS | MF | 15.0 | 15.0 | 15.0 | 15.0 | 15.0 | 15.0 |
| 基于深度学习的 RS | LightGCN | 15.0 | 15.0 | 15.0 | 15.0 | 15.0 | 15.0 |
| 智能体 RS | BaseAgent | 16.6 | 15.0 | 16.0 | 21.2 | 2.0 | 3.3 |
| | CoTAgent | 15.7 | 17.3 | 18.0 | 18.5 | 2.3 | 2.3 |
| | MemoryAgent | 16.3 | 12.0 | 18.3 | 17.8 | 3.3 | 4.3 |
| | CoTMemAgent | 16.7 | 14.3 | 17.7 | 20.2 | 2.3 | 3.3 |
| | Baseline666 | 48.7 | 48.3 | 36.7 | 44.1 | 1.3 | 2.3 |
| | DummyAgent | 44.7 | 45.6 | 39.3 | 47.8 | 1.7 | 0.3 |
| | RecHackers | 44.7 | 49.3 | 38.3 | 42.1 | 1.0 | 2.3 |
| | Agent4Rec | 25.7 | 48.3 | 40.7 | 9.1 | 2.3 | 0.7 |

**表 4：** 兴趣演化推荐任务上的性能比较，指标为平均 HR@N（$N=1,3,5$）。每个数据集下分为长期与短期。

| 类别 | 方法 | Amazon 长期 | Amazon 短期 | Goodreads 长期 | Goodreads 短期 | Yelp 长期 | Yelp 短期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 传统 RS | MF | 38.4 | 49.5 | 17.7 | 21.3 | 42.0 | 65.9 |
| 基于深度学习的 RS | LightGCN | 32.3 | 59.1 | 18.0 | 22.3 | 31.6 | 68.9 |
| 智能体 RS | BaseAgent | 16.0 | 13.3 | 21.3 | 25.0 | 5.7 | 6.0 |
| | CoTAgent | 14.0 | 15.0 | 22.3 | 23.7 | 3.3 | 4.3 |
| | MemoryAgent | 10.3 | 14.0 | 21.7 | 22.7 | 4.0 | 3.7 |
| | CoTMemAgent | 12.3 | 15.0 | 23.3 | 22.0 | 3.3 | 4.6 |
| | Baseline666 | 50.6 | 55.3 | 63.0 | 55.7 | 0.0 | 0.0 |
| | DummyAgent | 53.0 | 56.7 | 59.7 | 54.0 | 10.6 | 6.3 |
| | RecHackers | 52.7 | 57.3 | 62.0 | 54.0 | 11.3 | 5.3 |
| | Agent4Rec | 26.3 | 37.7 | 36.7 | 43.9 | 8.6 | 9.0 |

### 5.2 冷启动场景上的性能

在冷启动场景中，我们聚焦历史交互有限的用户与物品。表 3 报告基于 Qwen-72B-Instruct 的各种方法的性能。表 4 与表 3 的比较揭示，几乎所有基线都有明显的性能下降，凸显冷启动设定固有的不确定性与挑战。这些结果表明，我们所提出的任务可以作为在数据稀疏条件下更全面评估推荐效率的基础。

### 5.3 兴趣演化上的性能

为评估模型对变化中的用户偏好的适应能力，我们构造一个用户兴趣演化的场景。该设定捕捉真实推荐任务中常见的时间动态。相应结果见表 4。尽管大多数方法在该设定下经历性能下降，Baseline666 与 RecHackers 等基于智能体的方法表现出相对稳定的性能，表明它们建模并回应用户行为演化的能力更强。我们在图 4 中给出 Baseline666 的案例研究。

<!-- 原 PDF 第 9 页 -->

图 4 见原 PDF。

**图 4：** 一个更优推荐智能体（Baseline666）的智能体工作流示意。它进行领域自适应的物品侧特征工程以增强个性化。

图中提示文字（译文）：你是在线平台上的一位真实用户。你的历史物品评论文本与星级如下：['user_id', 'review_count', 'friends', 'stars' ...]。现在你需要对以下 20 件物品按其与你偏好的匹配程度排序：[候选物品列表]。请把更感兴趣的物品排在排序列表更靠前的位置。上述 20 个候选物品的信息如下：['item_id', 'name', 'stars', 'review_count', 'attributes', 'title', 'average_rating', 'rating_number', 'description' ...]。你的最终输出应当只是 [候选列表] 的一个排序后的物品列表，格式如下。不要引入任何其他物品 ID。不要输出你的分析过程。正确的输出格式：[排序后的候选物品列表]。

## 6 相关工作

### 6.1 智能体推荐系统

基于 LLM 的智能体的近期进展为推荐系统引入了变革性范式。智能体推荐系统展现出自主收集并处理用户—物品交互的能力，同时利用复杂推理进行个性化推荐。现有方法可分为三个主要分支：（1）面向排序的智能体 [27–29]，从历史行为推断用户偏好以生成推荐，以 RecMind [27] 为例，它是一个用于直接生成推荐的统一 LLM 智能体；（2）面向模拟的智能体 [15, 17, 30]，通过智能体的角色扮演能力模拟类人行为，例如 Agent4Rec [15] 利用智能体模拟用户以进行真实的交互建模；（3）交互式对话智能体 [16, 31, 32]，把推荐框定为基于对话的意图理解，如 RAH 所展示的那样，它建立一个人—推荐系统交互框架，用于迭代精炼用户偏好。然而，目前还没有全面的基准来系统评估这类新兴的智能体推荐方法。

### 6.2 基于 LLM 的智能体

LLM 的近期进展使能够进行复杂推理 [26, 21, 33] 与类人行为模拟 [19, 34] 的自主智能体得以发展，并带来多个领域的多样应用。在决策上下文中，由 LLM 驱动的智能体已在沙盒游戏环境 [35]、机器人控制系统 [36] 与网页导航 [37] 任务中展示成功。超越单智能体应用，当代研究已表明多智能体系统 [38–40] 展现出涌现的协作智能。这些系统达成两个重要里程碑：第一，它们通过复杂的交互协议忠实地复现类人的组织动态；第二，它们通过利用分布式认知与专门的角色分配，在复杂问题求解场景中超越单智能体方法。

## 7 结论

在本工作中，我们提出 AgentRecBench，首个用于评估新兴的、由 LLM 驱动的智能体推荐系统的全面基准。该基准在多个领域与场景中建立严格的评估协议，并由我们新颖的文本交互环境支持，该环境整合了三个丰富的推荐数据集。通过对 10 余种经典与智能体方法的广泛实证分析，我们不仅展示了基于 LLM 的方法的优越性能，还识别了它们的关键设计。所提出的模块化智能体设计框架与标准化评估平台，为研究者推进智能体推荐系统的发展提供了必要工具。我们相信，本工作为推进下一代推荐系统提供了一个基础平台。

<!-- 原 PDF 第 10 页 -->

## 参考文献

[1] Qi Wang, Jindong Li, Shiqi Wang, Qianli Xing, Runliang Niu, He Kong, Rui Li, Guodong Long, Yi Chang, and Chengqi Zhang. 迈向下一代基于 LLM 的推荐系统：综述及展望. arXiv preprint arXiv:2410.19744, 2024.

[2] Yu Shang, Chen Gao, Nian Li, and Yong Li. 一个带有移动短视频平台行为、属性与内容的大规模数据集. arXiv preprint arXiv:2502.05922, 2025.

[3] Chen Gao, Yu Zheng, Nian Li, Yinfeng Li, Yingrong Qin, Jinghua Piao, Yuhan Quan, Jianxin Chang, Depeng Jin, Xiangnan He, et al. 面向推荐系统的图神经网络综述：挑战、方法与方向. ACM Transactions on Recommender Systems, 1(1):1–51, 2023.

[4] Yu Shang, Chen Gao, Jiansheng Chen, Depeng Jin, Meng Wang, and Yong Li. 为微视频推荐学习细粒度用户兴趣. In Proceedings of the 46th international ACM SIGIR conference on research and development in information retrieval, pages 433–442, 2023.

[5] Yehuda Koren, Robert Bell, and Chris Volinsky. 推荐系统的矩阵分解技术. Computer, 42(8):30–37, 2009.

[6] J Ben Schafer, Dan Frankowski, Jon Herlocker, and Shilad Sen. 协同过滤推荐系统. In The adaptive web: methods and strategies of web personalization, pages 291–324. Springer, 2007.

[7] Xiangnan He, Lizi Liao, Hanwang Zhang, Liqiang Nie, Xia Hu, and Tat-Seng Chua. 神经协同过滤. In Proceedings of the 26th international conference on world wide web, pages 173–182, 2017.

[8] Xiangnan He, Kuan Deng, Xiang Wang, Yan Li, Yongdong Zhang, and Meng Wang. LightGCN：简化并强化用于推荐的图卷积网络. In Proceedings of the 43rd International ACM SIGIR conference on research and development in Information Retrieval, pages 639–648, 2020.

[9] Yunfan Gao, Tao Sheng, Youlin Xiang, Yun Xiong, Haofen Wang, and Jiawei Zhang. Chat-Rec：迈向交互式、可解释的、由 LLM 增强的推荐系统. arXiv preprint arXiv:2303.14524, 2023.

[10] Likang Wu, Zhi Zheng, Zhaopeng Qiu, Hao Wang, Hongchao Gu, Tingjia Shen, Chuan Qin, Chen Zhu, Hengshu Zhu, Qi Liu, et al. 面向推荐的大语言模型综述. World Wide Web, 27(5):60, 2024.

[11] Qiyao Peng, Hongtao Liu, Hua Huang, Qing Yang, and Minglai Shao. 面向推荐系统的、由 LLM 驱动的智能体综述. arXiv preprint arXiv:2502.10050, 2025.

[12] Eui-Hong Han and George Karypis. 基于特征的推荐系统. In Proceedings of the 14th ACM international conference on Information and knowledge management, pages 446–452, 2005.

[13] Yuwei Yan, Yu Shang, Qingbin Zeng, Yu Li, Keyu Zhao, Zhiheng Zheng, Xuefei Ning, Tianji Wu, Shengen Yan, Yu Wang, et al. AgentSociety Challenge：为网络平台上的用户建模与推荐设计 LLM 智能体. arXiv preprint arXiv:2502.18754, 2025.

[14] Chengkai Huang, Junda Wu, Yu Xia, Zixu Yu, Ruhan Wang, Tong Yu, Ruiyi Zhang, Ryan A Rossi, Branislav Kveton, Dongruo Zhou, et al. 迈向多模态大语言模型时代的智能体推荐系统. arXiv preprint arXiv:2503.16734, 2025.

[15] An Zhang, Yuxin Chen, Leheng Sheng, Xiang Wang, and Tat-Seng Chua. 论推荐中的生成式智能体. In Proceedings of the 47th international ACM SIGIR conference on research and development in Information Retrieval, pages 1807–1817, 2024.

[16] Yubo Shu, Haonan Zhang, Hansu Gu, Peng Zhang, Tun Lu, Dongsheng Li, and Ning Gu. RAH！RecSys–助手–人：一个以人为中心的、带 LLM 智能体的推荐框架. IEEE Transactions on Computational Social Systems, 2024.

<!-- 原 PDF 第 11 页 -->

[17] Junjie Zhang, Yupeng Hou, Ruobing Xie, Wenqi Sun, Julian McAuley, Wayne Xin Zhao, Leyu Lin, and Ji-Rong Wen. AgentCF：用自主语言智能体为推荐系统进行协同学习. In Proceedings of the ACM Web Conference 2024, pages 3679–3689, 2024.

[18] Xu Huang, Weiwen Liu, Xiaolong Chen, Xingmei Wang, Hao Wang, Defu Lian, Yasheng Wang, Ruiming Tang, and Enhong Chen. 理解 LLM 智能体的规划：综述. arXiv preprint arXiv:2402.02716, 2024.

[19] Joon Sung Park, Joseph O’Brien, Carrie Jun Cai, Meredith Ringel Morris, Percy Liang, and Michael S Bernstein. 生成式智能体：人类行为的交互式拟像. In Proceedings of the 36th annual acm symposium on user interface software and technology, pages 1–22, 2023.

[20] Fengli Xu, Qianyue Hao, Zefang Zong, Jingwei Wang, Yunke Zhang, Jingyi Wang, Xiaochong Lan, Jiahui Gong, Tianjian Ouyang, Fanjin Meng, et al. 迈向大型推理模型：用大语言模型进行强化推理的综述. arXiv preprint arXiv:2501.09686, 2025.

[21] Yu Shang, Yu Li, Fengli Xu, and Yong Li. 思想协同：在混合语言模型中引出高效推理. arXiv preprint arXiv:2402.02563, 2024.

[22] Lei Wang, Chen Ma, Xueyang Feng, Zeyu Zhang, Hao Yang, Jingsen Zhang, Zhiyuan Chen, Jiakai Tang, Xu Chen, Yankai Lin, et al. 基于大语言模型的自主智能体综述. Frontiers of Computer Science, 18(6):186345, 2024.

[23] Zhiheng Xi, Wenxiang Chen, Xin Guo, Wei He, Yiwen Ding, Boyang Hong, Ming Zhang, Junzhe Wang, Senjie Jin, Enyu Zhou, et al. 基于大语言模型的智能体的兴起与潜力：综述. Science China Information Sciences, 68(2):121101, 2025.

[24] Yu Shang, Yu Li, Keyu Zhao, Likai Ma, Jiahe Liu, Fengli Xu, and Yong Li. AgentSquare：在模块化设计空间中自动搜索 LLM 智能体. arXiv preprint arXiv:2410.06153, 2024.

[25] Theodore Sumers, Shunyu Yao, Karthik Narasimhan, and Thomas Griffiths. 面向语言智能体的认知架构. Transactions on Machine Learning Research, 2023.

[26] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al. 思维链提示在大语言模型中引出推理. Advances in neural information processing systems, 35:24824–24837, 2022.

[27] Yancheng Wang, Ziyan Jiang, Zheng Chen, Fan Yang, Yingxue Zhou, Eunah Cho, Xing Fan, Xiaojiang Huang, Yanbin Lu, and Yingzhen Yang. RecMind：由大语言模型驱动的推荐智能体. arXiv preprint arXiv:2308.14296, 2023.

[28] Zhefan Wang, Yuanqing Yu, Wendi Zheng, Weizhi Ma, and Min Zhang. MACRec：用于推荐的多智能体协作框架. In Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval, pages 2760–2764, 2024.

[29] Yuyue Zhao, Jiancan Wu, Xiang Wang, Wei Tang, Dingxian Wang, and Maarten De Rijke. 让我来替你做：经由工具学习迈向由 LLM 赋能的推荐. In Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval, pages 1796–1806, 2024.

[30] Shihao Cai, Jizhi Zhang, Keqin Bao, Chongming Gao, and Fuli Feng. FLOW：一个同时增强推荐与用户智能体的反馈回路框架. arXiv preprint arXiv:2410.20027, 2024.

[31] Xu Huang, Jianxun Lian, Yuxuan Lei, Jing Yao, Defu Lian, and Xing Xie. 推荐 AI 智能体：整合大语言模型以进行交互式推荐. arXiv preprint arXiv:2308.16505, 2023.

<!-- 原 PDF 第 12 页 -->

[32] Luke Friedman, Sameer Ahuja, David Allen, Zhenning Tan, Hakim Sidahmed, Changbo Long, Jun Xie, Gabriel Schubiner, Ajay Patel, Harsh Lara, et al. 在对话式推荐系统中利用大语言模型. arXiv preprint arXiv:2305.07961, 2023.

[33] Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Tom Griffiths, Yuan Cao, and Karthik Narasimhan. 思想之树：用大语言模型进行审慎的问题求解. Advances in Neural Information Processing Systems, 36, 2024.

[34] Yuan Li, Yixuan Zhang, and Lichao Sun. MetaAgents：通过协作式生成智能体，为基于 LLM 的面向任务的协调模拟人类行为交互. arXiv preprint arXiv:2310.06500, 2023.

[35] Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and Anima Anandkumar. Voyager：一个带大语言模型的开放式具身智能体. arXiv preprint arXiv:2305.16291, 2023.

[36] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. ReAct：在语言模型中协同推理与行动. In International Conference on Learning Representations (ICLR), 2023.

[37] Xiang Deng, Yu Gu, Boyuan Zheng, Shijie Chen, Sam Stevens, Boshi Wang, Huan Sun, and Yu Su. Mind2Web：迈向面向网页的通用智能体. Advances in Neural Information Processing Systems, 36:28091–28114, 2023.

[38] Taicheng Guo, Xiuying Chen, Yaqi Wang, Ruidi Chang, Shichao Pei, Nitesh V Chawla, Olaf Wiest, and Xiangliang Zhang. 基于大语言模型的多智能体：进展与挑战综述. arXiv preprint arXiv:2402.01680, 2024.

[39] Sirui Hong, Xiawu Zheng, Jonathan Chen, Yuheng Cheng, Jinlin Wang, Ceyao Zhang, Zili Wang, Steven Ka Shing Yau, Zijuan Lin, Liyang Zhou, et al. MetaGPT：面向多智能体协作框架的元编程. arXiv preprint arXiv:2308.00352, 3(4):6, 2023.

[40] Weize Chen, Yusheng Su, Jingwei Zuo, Cheng Yang, Chenfei Yuan, Chen Qian, Chi-Min Chan, Yujia Qin, Yaxi Lu, Ruobing Xie, et al. AgentVerse：促进多智能体协作并探索智能体中的涌现行为. arXiv preprint arXiv:2308.10848, 2(4):6, 2023.

<!-- 原 PDF 第 13 页 -->

## 附录

### A.1 更广泛的影响

本工作提出的基准与工具包有望推进智能体推荐系统的发展，并带来显著的正面社会影响。智能体推荐系统改进的上下文理解能够实现更高质量的个性化推荐，从而惠及电子商务、短视频平台等多样领域。此外，标准化评估框架促进更稳健、更可适应的推荐系统的发展，从而更好地服务演化中的用户需求。我们的平台还可以为把公平性与隐私保护等伦理 AI 原则纳入未来推荐系统提供灵活基础。这些进展共同有助于构建更以用户为中心、可解释且对社会有益的推荐技术。

### A.2 局限

尽管 AgentRecBench 为智能体推荐系统提供了全面的评估框架，若干局限指出了未来工作的有价值方向。第一，当前基准主要聚焦于评估新兴的智能体推荐系统，我们计划纳入更多传统与基于深度学习的基线，以进行更彻底的比较分析。第二，我们的环境目前在文本信息上运行，我们旨在把它扩展到纳入多模态数据（例如图像、视频），以更好地反映智能体需要处理多样内容类型的真实推荐场景。最后，尽管当前框架评估单智能体系统，我们计划把它扩展为支持多智能体推荐系统的评估，其中协作或竞争的智能体通过交互来改进推荐结果。

### A.3 冷启动推荐任务与兴趣演化推荐任务的补充实验结果

表 5 与表 6 展示我们的任务在 DeepSeek V3 与 GPT-4o-mini 上的补充实验结果。总体而言，我们在 DeepSeek V3 与 GPT-4o-mini 等其他主流模型上的评估结果表明，智能体的性能与正文中给出的发现一致。Baseline666、DummyAgent 与 RecHackers 都表现出强性能，进一步验证了我们的评估方法在准确反映智能体能力方面的稳健性与可靠性。

### A.4 案例研究

我们分别在图 5 与图 6 中给出 DummyAgent 与 RecHackers 这两个智能体的核心工作流。总体而言，这些智能体在排序过程中依赖相似类型的信息，尽管具体实现不同。排序决策主要基于三个关键组件：（1）历史用户评论，反映过去的偏好；（2）待排序的候选物品列表；（3）详细的物品信息，有助于评估每件物品与用户偏好的相关性。

这些智能体的一项主要创新在于物品侧特征工程。值得注意的是，Baseline666 团队采用了特定于平台的特征抽取方法，从而在不同数据源上实现稳健且可适应的排序策略。例如，在 Amazon 平台上，抽取了物品 ID、名称、星级、评论数与物品描述等特征。在 Yelp 上，他们聚焦物品 ID、名称、星级与评论数等核心属性。相比之下，Goodreads 平台需要更多样的特征，包括作者、出版年份与相似图书。

评论侧特征工程是另一个关键组件，旨在识别并抽取信息量最大的评论，以丰富对用户偏好与物品特征的理解。例如，DummyAgent 团队实现了针对平台定制的策略：在 Yelp 上，他们不仅抽取评论文本，还抽取 “useful”、“cool” 与 “funny” 等交互属性；在 Amazon 上，他们纳入出版日期与购买验证指示；在 Goodreads 上，除评论文本与评分外，他们还利用评论日期、投票数、评论数与阅读状态等元数据。

<!-- 原 PDF 第 14 页 -->

**表 5：** 冷启动推荐任务上的性能比较，指标为平均 HR@N（$N=1,3,5$）。上半部分为 DeepSeek-V3，下半部分为 GPT-4o-mini。列依次为 Amazon 的 User/Item、Goodreads 的 User/Item、Yelp 的 User/Item。

| 模型 | 方法 | Amazon User | Amazon Item | Goodreads User | Goodreads Item | Yelp User | Yelp Item |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DeepSeek-V3 | BaseAgent | 16.3 | 14.0 | 22.3 | 16.2 | 4.0 | 4.0 |
| | CoTAgent | 19.3 | 9.0 | 20.3 | 14.5 | 4.3 | 4.3 |
| | MemoryAgent | 15.3 | 11.0 | 16.7 | 15.5 | 4.3 | 4.3 |
| | CoTMemAgent | 16.7 | 12.0 | 16.7 | 15.5 | 3.7 | 4.3 |
| | Baseline666 | 50.3 | 48.7 | 38.7 | 49.5 | 1.3 | 2.7 |
| | DummyAgent | 59.0 | 45.0 | 37.7 | 49.5 | 1.3 | 2.7 |
| | RecHackers | 59.7 | 47.0 | 49.3 | 46.1 | 3.0 | 3.3 |
| | Agent4Rec | 45.6 | 28.0 | 37.3 | 11.1 | 2.7 | 0.7 |
| GPT-4o-mini | BaseAgent | 15.3 | 9.0 | 18.7 | 15.2 | 3.0 | 4.0 |
| | CoTAgent | 17.0 | 9.3 | 20.0 | 15.5 | 2.7 | 4.3 |
| | MemoryAgent | 15.0 | 7.3 | 16.0 | 18.2 | 3.0 | 4.3 |
| | CoTMemAgent | 14.7 | 7.7 | 15.3 | 16.0 | 3.7 | 4.0 |
| | Baseline666 | 46.0 | 32.0 | 33.0 | 21.5 | 0.3 | 2.3 |
| | DummyAgent | 36.7 | 30.7 | 32.7 | 24.6 | 0.3 | 3.3 |
| | RecHackers | 39.0 | 36.3 | 37.7 | 33.3 | 1.3 | 3.3 |
| | Agent4Rec | 36.0 | 20.3 | 39.3 | 7.1 | 0.7 | 1.3 |

**表 6：** 兴趣演化推荐任务上的性能比较，指标为平均 HR@N（$N=1,3,5$）。上半部分为 DeepSeek-V3，下半部分为 GPT-4o-mini。每个数据集下分为长期与短期。

| 模型 | 方法 | Amazon 长期 | Amazon 短期 | Goodreads 长期 | Goodreads 短期 | Yelp 长期 | Yelp 短期 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DeepSeek-V3 | BaseAgent | 17.3 | 19.7 | 32.0 | 29.7 | 5.7 | 4.3 |
| | CoTAgent | 17.7 | 16.0 | 24.0 | 16.3 | 3.3 | 3.0 |
| | MemoryAgent | 18.3 | 17.7 | 29.3 | 29.7 | 5.0 | 4.0 |
| | CoTMemAgent | 13.3 | 18.7 | 23.3 | 21.3 | 4.3 | 4.0 |
| | Baseline666 | 50.7 | 71.3 | 66.0 | 63.3 | 0.0 | 0.0 |
| | DummyAgent | 65.0 | 65.7 | 66.7 | 60.7 | 10.3 | 6.3 |
| | RecHackers | 64.3 | 68.0 | 68.7 | 66.3 | 9.3 | 7.7 |
| | Agent4Rec | 34.0 | 46.3 | 41.3 | 42.7 | 10.0 | 6.0 |
| GPT-4o-mini | BaseAgent | 13.3 | 12.0 | 12.7 | 14.0 | 5.3 | 4.7 |
| | CoTAgent | 13.3 | 11.7 | 12.7 | 13.0 | 5.3 | 4.7 |
| | MemoryAgent | 12.0 | 10.7 | 16.3 | 15.7 | 5.3 | 4.3 |
| | CoTMemAgent | 11.3 | 12.3 | 17.7 | 16.3 | 5.3 | 4.7 |
| | Baseline666 | 35.0 | 49.0 | 35.0 | 38.7 | 0.0 | 0.0 |
| | DummyAgent | 34.7 | 48.0 | 42.7 | 31.3 | 4.0 | 2.3 |
| | RecHackers | 39.7 | 46.3 | 53.7 | 44.3 | 5.7 | 2.0 |
| | Agent4Rec | 24.0 | 34.7 | 32.7 | 35.3 | 7.0 | 4.3 |

<!-- 原 PDF 第 15 页 -->

总之，这些智能体的关键设计要素可以提炼为三条核心原则：（1）有效的工作流建立在用户历史、候选物品、物品细节与平台特定特征的组合之上，全部通过大语言模型（LLM）整合以产生排序；（2）抽取有代表性的、特定于平台的物品属性，对于增强模型性能是必要的；（3）优先考虑既高度相关又信息丰富的评论，对于提高排序质量至关重要。

图 5 见原 PDF。

**图 5：** 一个更优推荐智能体（DummyAgent）的智能体工作流示意。它进行领域自适应的物品侧特征工程以增强个性化。

图中提示文字（译文）：你是在线平台上的一位真实用户。你的历史物品评论文本与星级如下：['item_id', 'text', 'timestamp', 'source', 'type', 'sub_item_id', 'stars', 'helpful_vote', 'verified_purchase', 'title' ...]。现在你需要按与你偏好的匹配程度，对以下 {final_item_list_len} 件物品排序：{final_item_list}。请把更感兴趣的物品排在排序列表更靠前的位置。上述 {final_item_list_len} 个候选物品的信息如下：['item_id', 'name', 'stars', 'review_count', 'attributes', 'title', 'average_rating', 'rating_number', 'description', 'ratings_count', 'title_without_series']。你的最终输出应当只是 {final_item_list} 的一个排序后的物品列表，格式如下。不要引入任何其他物品 ID。不要输出你的分析过程。正确的输出格式：[排序后的候选物品列表]。

图 6 见原 PDF。

**图 6：** 一个更优推荐智能体（RecHacker）的智能体工作流示意。它进行领域自适应的物品侧特征工程以增强个性化。

图中提示文字（译文）：你是 {task_type} 上的一位真实人类用户，该平台用于众包的 {task_item} 评论。这里是你的 {task_type} 画像与评论历史：{user}。你的历史 {task_item} 评论如下显示你的偏好：['user_id', 'review_count', 'friends', 'stars' ...]。现在你需要按与你偏好的匹配程度，对以下 20 个 {task_item} 排序：[候选列表]。上述 20 个候选 {task_item} 的信息如下：['item_id', 'name', 'stars', 'review_count', 'attributes', 'title', 'average_rating', 'rating_number', 'description', 'ratings_count' ...]。你的最终输出应当只是 [候选列表] 的一个排序后的 {task_item} 列表，格式如下。不要引入任何其他 {task_item} ID。你只需要从候选列表中选出前 5 个 {task_item}。请把更感兴趣的 {task_item} 排在排序列表更靠前的位置。你应当在最终答案之前逐步思考。不要输出你的分析过程。严格遵循正确的最终答案输出格式，记住输出 {task_item} 的 ID 而不是名称：[排序后的候选物品列表]。

<!-- 译完 -->
