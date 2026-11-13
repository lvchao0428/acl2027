# RecGPT Technical Report

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`RecGPT-2507.22879.pdf`。

## Abstract 摘要

原文未单独标出 Abstract 标题。以下译自首页标题与作者 RecGPT Team 之后、Figure 1 之前的两段正文。

推荐系统是人工智能最具影响力的应用之一，是连接用户、商家与平台的关键基础设施。然而，当前大多数工业系统仍然严重依赖历史共现模式和日志拟合（log-fitting）目标，即优化对过去用户交互的拟合，而不显式建模用户意图。这种日志拟合做法常常过拟合于狭窄的历史偏好，无法捕捉用户不断变化的潜在兴趣。结果是强化了过滤气泡（filter bubbles）与长尾现象，最终损害用户体验，并威胁整个推荐生态的可持续性。

为应对这些挑战，我们重新思考推荐系统的整体设计范式，提出 RecGPT，一种把用户意图置于推荐流水线中心的下一代框架。通过把大语言模型（large language models, LLMs）整合进用户兴趣挖掘、物品检索和解释生成等关键阶段，RecGPT 把日志拟合式推荐转变为以意图为中心的过程。为了在规模上把通用 LLM 有效对齐到上述领域特定的推荐任务，RecGPT 采用多阶段训练范式，把推理增强的预对齐（reasoning-enhanced pre-alignment）与自训练演化（self-training evolution）结合起来，并由 Human-LLM 协同评判系统引导。目前，RecGPT 已在淘宝 App（Taobao App）上全量部署。在线实验表明，RecGPT 对各利益相关方都取得了稳定的性能提升：用户侧的内容多样性与满意度提高（例如 CICD +6.96%，DT +4.82%），商家与平台获得更多曝光与转化（例如 CTR +6.33%，IPV +9.47%，DCAU +3.72%）。这些覆盖全部利益相关方的综合改进结果表明，由 LLM 驱动、以意图为中心的设计能够促成更可持续、互利的推荐生态。

图 1 位于首页摘要段落之后，图注可读。图 1：RecGPT 在淘宝 APP（Taobao APP）首页「Guess What You Like」场景中的在线表现。左图给出 RecGPT 相对基线系统在关键指标上的总体提升，包括点击率（Click Through Rate, CTR）、物品页浏览（Item Page View, IPV）、日点击活跃用户（Daily Click Active Users, DCAU）、每用户点击物品类目多样性（per-user Clicked Item Category Diversity, CICD）以及用户停留时长（Dwell Time, DT）。右图给出 RecGPT 与基线系统在不同流行度商品组上的 CTR 与页面浏览率（Page View Rate, PVR）分布。为保护商业机密，CTR、PVR 等商业指标已做归一化。左右图中的具体柱形与分布曲线【抽取不清】。

## 1 Introduction 引言

推荐系统已遍及现代数字生态，从淘宝（Taobao）、亚马逊（Amazon）等电商入口，到 YouTube、TikTok 等内容平台，从根本上重塑了人们发现和消费信息的方式（Lü et al., 2012）。理想的推荐系统应当把用户（常常是隐式的）意图与最相关的物品或内容匹配起来，使用户以最小努力获得最大的体验价值（Resnick and Varian, 1997）。当这种对齐实现时，会形成使所有利益相关方受益的正反馈回路：用户获得满意体验，商家销量增加，平台获得持续的流量与收入。然而，实现这一愿景的关键，在于从冗长且快速变化的行为轨迹中准确推断并建模用户的真实意图。

过去二十年里，学术界和工业界通过不懈优化特征工程与模型架构来追求这一愿景。特征表示从手工统计量，发展到序列特征与交叉特征，再到最近的超长行为建模（Schifferer et al., 2020）。模型架构从因子分解机（factorization machines）（Rendle, 2010），发展到深度匹配网络（Zhang et al., 2019）、图神经网络模型（Wu et al., 2022），以及最新的生成式 Transformer 骨干（Deng et al., 2025）。这些努力带来了显著的业务收益，但根本上仍受限于历史日志中的共现模式——它们本质上是在「从点击中学习点击」（“learn clicks from clicks”）。由于缺少对用户兴趣的显式理解，这类日志拟合方法倾向于强化相似用户已经消费过的内容，放大过滤气泡效应（Filter Bubble）（Nguyen et al., 2014; Wang et al., 2022），并进一步边缘化长尾稀疏性，即马太效应（Matthew Effects）（Gao et al., 2023; Liu and Huang, 2021）。弥合这一差距，需要一种新的建模范式，能够超越表层相关，并推理驱动用户行为的动机。

大语言模型（LLMs）的近期出现（Zhao et al., 2023），尤其是具备强推理能力的模型，为超越纯日志拟合推荐的局限开辟了一条有前景的路径。凭借广博的世界知识、细粒度语义理解以及逐步推理能力，LLM 能够帮助准确、全面地分析用户的潜在兴趣，并显式推理用户为何可能想要某件物品。尽管已有越来越多的工作开始用 LLM 增强推荐系统，大多数研究仍限于小型离线基准，无法应用于真实推荐环境（Wu et al., 2024; Zhao et al., 2024）。如何把 LLM 有效整合进大规模工业推荐系统，以真正理解和挖掘用户意图，从而克服日志拟合推荐的局限，在很大程度上仍未得到充分探索。

为填补这一空白，我们引入 RecGPT，一种生产规模的框架，把三个推理 LLM 整合进工业推荐流水线的核心，形成「用户兴趣挖掘（User Interest Mining）→ 物品标签预测（Item Tag Prediction）→ 物品检索（Item Retrieval）→ 解释生成（Explanation Generation）」的闭环（Figure 2）。具体而言，RecGPT 首先使用用户兴趣 LLM（User-Interest LLM），全面分析用户的终身行为历史，并显式生成一份简洁的、自然语言形式的当前兴趣画像。第二个物品标签 LLM（Item-Tag LLM）再对这些兴趣进行推理，生成细粒度物品标签，用以描述用户最可能在寻找的物品。这些标签被注入物品检索阶段，把传统的用户–物品双塔匹配器扩展为用户–物品–标签三塔架构。于是，只有与推断出的用户意图对齐的物品，才会进入下游的排序与重排序级联。通过把用户行为日志转化为动态更新的意图签名，RecGPT 把候选生成从协同过滤（collaborative filtering）重塑为兴趣增强的过程，在不改变下游基础设施的情况下提升召回相关性与长尾覆盖。最后，推荐解释 LLM（Recommendation-Explanation LLM）为最终推荐物品附上缓存的、自然语言的、对用户友好的解释，完成从意图发现到透明交付的闭环。

我们的主要贡献概括如下：

⋆ RecGPT 已在淘宝 APP 首页「Guess What You Like」场景中全量在线部署，并在多个利益相关方上取得显著性能提升。从用户视角看，系统将 CICD 提升 6.96%，将 DT 提升 4.82%，表明它能够有效发现超出历史交互模式的潜在、多样兴趣，从而突破信息茧房并扩展推荐边界。对商家和平台而言，CTR（+6.33%）、IPV（+9.47%）和 DCAU（+3.72%）均有明显提升，反映出可观的商业价值。此外，RecGPT 通过为不同商家提供更公平的曝光机会，有效缓解了马太效应，最终为用户、商家和平台建立起三方共赢的生态。

⋆ 与「从点击中学习点击」的传统协同过滤方法不同，我们利用 LLM 的世界知识与推理能力，从行为模式中显式挖掘用户的潜在兴趣，从表层相关转向深层画像分析与偏好建模。据我们所知，我们首次在服务超过十亿消费者与物品的工业应用中部署了推理增强的千亿级推荐基础模型，有力地验证并推进了大语言模型用于推荐系统的实际潜力与价值。

⋆ 为使 LLM 能够有效整合进大规模工业推荐系统，我们开发了一套系统性的多阶段训练框架，以应对把通用 LLM 适配到推荐特定任务时的独特挑战。我们的方法从推理增强的预对齐推进到自训练演化，并利用 LLM-as-a-Judge 能力进行自动化数据质量筛选与模型评估。该框架实现了从人工专家审核到 Human-LLM 协同评判系统的渐进过渡，在保持严格质量标准的同时显著加快模型迭代周期。

## 2 RecGPT Workflow RecGPT 工作流

本节给出 RecGPT 的整体工作流，如 Figure 2 所示。RecGPT 的核心思想是利用大语言模型增强推荐流水线的不同阶段，包括用户兴趣理解、物品预测，以及为最终结果生成对用户友好的推荐解释。我们引入三个对应的 LLM 模块：LLM_UI 负责用户兴趣挖掘任务，LLM_IT 处理物品标签预测任务，LLM_RE 生成推荐解释。此外，为了把 LLM_IT 预测出的物品（本文称为物品标签，item tags）映射到域内物品语料中的具体物品，我们提出一种标签感知的语义相关性检索方法。该方法利用由 LLM 生成的物品标签所带来的深层语义理解；这些标签通过基于推理的分析捕捉用户意图，而不是做表层特征匹配。通过把这些由 LLM 驱动的语义洞察与传统协同过滤信号结合起来，我们的物品检索方法有效平衡语义相关性与协同模式，从而既能探索用户潜在的多样偏好，也能利用其已形成的行为模式。

总体而言，RecGPT 工作流包含以下组成部分：

♦ 用户兴趣挖掘（User Interest Mining）（Section 2.1）：通过 LLM_UI，我们对用户的终身多行为序列进行显式兴趣挖掘，以识别多样的用户兴趣模式。

♦ 物品标签预测（Item Tag Prediction）（Section 2.2）：基于用户兴趣挖掘结果，我们使用 LLM_IT 预测代表用户潜在偏好分布的物品标签。

♦ 物品检索（Item Retrieval）（Section 2.3）：标签感知的语义检索方法把预测标签映射到具体物品，同时纳入用户行为协同信号，以平衡语义相关性与协同相关性。该条目在 PDF 中被 Figure 2 从句中拆开，此处按阅读顺序接回。

♦ 推荐解释生成（Recommendation Explanation Generation）（Section 2.4）：LLM_RE 综合用户兴趣与推荐物品，生成个性化且对用户友好的解释，使之与个体用户偏好相呼应，从而提升系统透明度与用户体验。

图 2 位于本节前部的组成列表之中，图注可读。图 2：RecGPT 的整体工作流。LLM_UI、LLM_IT 与 LLM_RE 分别表示用于用户兴趣挖掘、物品标签预测和推荐解释生成的 LLM。RecGPT 采用「用户兴趣挖掘 → 物品标签预测」来识别与用户偏好匹配的潜在物品，再通过标签感知的语义相关性结合行为协同进行物品检索，把推断出的标签映射到具体的域内物品。最后，LLM_RE 基于检索结果和用户兴趣生成对用户友好的推荐解释。图中还可读出的文字包括：Section 2.1 User Interest Mining、Section 2.2 Item Tag Prediction、Section 2.3 Item Retrieval、Section 2.4 Explanation Generation、User Behavior Sequence、User Interest、Item Tag、User Features & Behavior Sequence、Item Features、Tag Tower、Item Tower、User Tower、Semantic Relevance、Collaboration Relevance、Interest Pool、Item Corpus、Explanation Table、Interest、Item、Final Recommended Items、Personalized Recommendation Explanation。图中三个模块符号抽取为 ℒℒℳ!"、ℒℒℳ#!、ℒℒℳ$%，与图注中 LLM_UI、LLM_IT、LLM_RE 的对应关系【抽取不清】；末尾 “cd”【抽取不清】。各模块的具体连线与空间排布【抽取不清】。

与依赖潜在特征并以最终用户反馈做优化的传统推荐算法不同，RecGPT 在流水线各阶段通过大语言模型采用显式的基于文本的建模。这一做法带来两个关键优势：第一，它使中间过程与每一阶段的模型表现可以被解释性地监测；第二，它通过过程级监督促进专家知识的融入，从而允许对各个组件做有针对性的优化。通过把工作流分解为具有清晰输入–输出关系的可管理子任务，该方法简化了端到端优化，同时使独立评估与改进成为可能。

### 2.1 User Interest Mining 用户兴趣挖掘

推荐系统的根本目标，是通过用户的历史交互行为理解其个性化偏好，并完成物品商品推荐。然而，现有推荐算法仅依赖固定的、统计性的隐式用户特征，难以显式建模用户动态而复杂的兴趣。为克服这些根本局限，我们引入生成式用户画像（Generative User Profiling），一种利用 LLM 强大推理能力来革新用户兴趣建模的新方法。尽管 LLM 在自然语言理解方面潜力可观，仍有若干关键挑战妨碍其在用户兴趣挖掘中的有效性：

（1）上下文窗口限制（Context Window Limitations）。推荐系统中真实用户的行为历史规模大、复杂度高。在淘宝电商平台上，用户平均拥有超过 37k 条历史行为记录。这些超长行为序列对当前受 128k-token 上下文窗口限制的 LLM 构成显著挑战。

（2）领域知识缺口（Domain Knowledge Gaps）。尽管拥有广博的世界知识，LLM 缺少对淘宝等平台领域特定特征的专门理解。这一知识缺口妨碍模型以专家水平从原始交互数据中有效抽取并抽象用户兴趣。

为克服这些挑战，我们首先开发可靠行为序列压缩（Reliable Behavioral Sequence Compression），在保留关键时间信息的同时缩短输入长度，以便更好地适应 LLM 的上下文窗口约束（Section 2.1.1）。在此基础上，我们为用户兴趣 LLM（User-Interest LLM）LLM_UI 提出多阶段任务对齐（Task Alignment）框架，以增强领域特定的用户兴趣挖掘能力（Section 2.1.2）。

### 2.1.1 Reliable Behavioral Sequence Compression 可靠行为序列压缩

为提升用户行为序列的可靠性与有效性，我们首先采用可靠行为抽取（Reliable Behavior Extraction）方法，从用户行为中滤除噪声与冗余信息。此外，为了在 LLM 上下文窗口限制内容纳超长用户行为序列，我们开发了层次化行为压缩（Hierarchical Behavior Compression）方法，对异构行为进行压缩。

可靠行为抽取（Reliable Behavior Extraction）。为确保用户交互行为准确反映真实用户兴趣，我们首先从大规模、多源、多行为的用户序列中抽取可靠信号，作为用户兴趣建模的数据基础。我们定义如下可靠行为（以淘宝电商平台为例）：

♦ 有意反馈行为（Intentional Feedback Behaviors）包括高参与动作，如「收藏」（favorites）、「购买」（purchases）、「加购」（add-to-cart），以及有意的点击行为，如「商品详情浏览」（detailed product views）和「阅读评价」（reviews reading）。这些行为通过直接的参与动作，或反映对物品细节深度关注的聚焦点击模式，展示出强烈的用户兴趣，并为建模用户偏好与购买意图提供稳健信号。

♦ 搜索行为（Search Behaviors）包括用于商品发现的「搜索查询」（search queries）等动作。这些行为代表有意的探索努力，揭示用户对特定商品类目或属性的意图。

需要说明的是，我们排除普通的商品点击行为，因为这些动作可能含有相当多的噪声，并且与所定义的可靠行为相比，反映用户兴趣的效果较差。

层次化行为压缩（Hierarchical Behavior Compression）。为容纳超长用户行为序列，我们开发了一种层次化压缩方法，把多源异构行为压缩为统一的序列格式。具体而言，我们在物品级和序列级都采用压缩策略，旨在缩短输入长度，同时保留兴趣挖掘所必需的信息。

（1）物品级压缩（Item-level Compression）。原始物品信息包含大量冗余和无关细节，若将其直接作为 LLM 的输入，会导致信息密度低、token 消耗过大。因此，我们首先压缩每件物品的相关信息。这里，我们提示 LLM 压缩详细的物品信息，同时保留物品名称、类目、品牌及其他必要特征等核心属性。

（2）序列级压缩（Sequence-level Compression）。在压缩单件物品信息之后，我们通过两步聚合进一步压缩用户的行为序列。我们首先把用户行为序列划分到不同时间段（一个月以内的行为按日划分，跨多个月的行为按月划分，超过一年的行为按年划分）。压缩方法通过两个互补的聚合步骤运作：（1）步骤 1：时间–行为聚合（Temporal-Behavioral Aggregation）。我们以「时间–行为类型」对作为键，把用户在特定时间段内通过特定行为交互过的全部物品分组。（2）步骤 2：基于物品的反向聚合（Item-based Reverse Aggregation）。然后我们反转这一映射，以物品序列为键，聚合其对应的时间–行为类型组合。例如，在不同时间段和行为中频繁一起出现的物品被归为一组，并保留其关联的时间–行为上下文。这一双重聚合过程产生如下格式的压缩行为序列（具体案例见 Section 4.4）：

“Time1 (Behavior1, Behavior2, ... ), Time2 (Behavior1, Behavior3, ... ), ... | Item1, Item2, ... ”

该表示高效捕捉时间行为模式与物品共现关系，同时显著缩短整体提示序列长度。

通过上述行为抽取与压缩过程，我们得到信息密度更高、既精炼又可靠的多源异构用户行为序列 \(\mathrm{B}_{u}=[B_{u,1}, B_{u,2}, \ldots, B_{u,|\mathrm{B}_{u}|}]\)。其中每个行为 \(B_{u,i}\) 包含同一时间段内的多次交互，以及对应的交互行为类型和关联物品信息。我们的经验结果表明，所提出的可靠行为压缩方法能把 98% 的用户行为容纳进大语言模型的 128k-token 上下文窗口，而未压缩序列仅能覆盖 88%。此外，该压缩方法将兴趣推断效率提高 29%，在保持完整行为表示的同时显著降低推断时间与计算成本。

### 2.1.2 Task Alignment for User Interest Mining 面向用户兴趣挖掘的任务对齐

为增强用户兴趣 LLM LLM_UI 在兴趣挖掘任务上的能力，我们设计了包含以下阶段的多阶段任务对齐框架，以得到与人类对齐的 LLM_UI：

阶段 1：基于课程学习的多任务微调（Curriculum Learning-based Multi-task Fine-tuning）。我们首先设计 16 个预备子任务（含 16.3k 条训练样本），以增强通用 LLM 的领域特定基础能力。这些子任务在多个维度上培养关键能力，例如关键信息抽取、复杂用户画像分析和因果推理。为确保能力稳定提升，受课程学习原则启发（Bengio et al., 2009; Pentina et al., 2015; Soviany et al., 2022; Wang et al., 2021），我们按难度级别与依赖关系对子任务做拓扑排序，逐步引导模型掌握复杂任务。相关实验细节见 Appendix C。

阶段 2：推理增强的预对齐（Reasoning-Enhanced Pre-alignment）。我们利用 DeepSeek-R1（Guo et al., 2025a）的高级推理能力，为兴趣挖掘生成高质量训练数据。经过仔细的人工筛选，我们把最初生成的 90.0k 条样本蒸馏为精炼后的 19.0k 条高质量数据集。该数据集作为知识蒸馏的基础，使兴趣 LLM LLM_UI 通过预对齐微调达到与教师模型相当的表现。

阶段 3：自训练演化（Self-Training Evolution）。为进一步提高模型的能力上限，我们提出一种使模型能够持续自我演化的自训练范式。在此阶段，模型生成自己的训练数据，并用这些自生成样本进行迭代优化，形成能力改进的反馈回路。在这一自训练过程中，我们收集 21.1k 条高质量样本来推动模型演化。为了以低成本高效过滤这些自生成输出并评估模型表现，我们采用 Human-LLM 协同范式，并以 LLM-as-a-Judge 能力进行数据质量控制与评估。该协同框架显著提高筛选效率，同时降低人工标注成本。Human-LLM 协同评判系统的完整介绍见 Section 3。

下文重点说明兴趣挖掘任务的提示工程（Prompt Engineering）策略与数据质量控制（Data Quality Control）协议。此外，我们给出大量人工评估实验（Human Evaluation Experiments），以展示自训练方法的有效性，并提供实际的在线部署（Online Deployment）细节。

提示工程（Prompt Engineering）。我们精心设计的提示模板以压缩后的行为序列（参见 Section 2.1.1）和个人属性作为用户信息，指示 LLM 生成多样而精确的兴趣画像。为提高生成准确性，模板纳入思维链（Chain-of-Thought, CoT）推理，引导模型经过显式的逻辑步骤，而不是直接预测兴趣。提示模板结构见 Prompt 2.1.2，其中占位符 {User Attributes} 与 {Compressed Reliable Behavioral Sequences} 会用用户特定的上下文数据实例化。{Other Interest Mining Requirements} 与 {Other Constraints} 的详细说明因篇幅限制放在 Appendix B。{Matched Interest Pool} 填入动态的已匹配兴趣集合。

图 3 位于本小节前部，图注可读。图 3：用户兴趣挖掘模块示意图。左图展示终身用户行为序列的压缩处理，包括行为抽取与层次化行为压缩。右图展示面向用户兴趣挖掘的多阶段任务对齐框架以及数据质量控制标准。图中还可读出的文字包括：Reliable Behavioral Sequence Compression、Behavior Extraction、Intentional Feedback Behaviors、Search Behaviors、Hierarchical Compression、Item-Level、Sequence-Level、LLM-based Compression、Time、Behavior、Item、Sequence Format、Task Alignment、Curriculum Learning-based Multitask Fine-tuning（~16.3k Samples）、Reasoning-Enhanced Pre-Alignment（~19.0k Samples）、Self-Training Evolution（~21.1k Samples）、User Interest LLM、Data Quality Control、Willingness、Reasonableness。用户兴趣 LLM 的数学符号抽取为 𝓛𝓛𝓜𝑼𝑰【抽取不清】。各框的具体连线与空间排布【抽取不清】。

用户兴趣挖掘提示模板如下：

# Role
你是电商平台的导购。基于用户的行为历史，你需要准确、全面地分析其潜在兴趣与偏好。

# Input
User Attribute: {User Attributes}
User Behavioral Information: {Compressed Reliable Behavioral Sequences}

# Mandatory Requirements
Task Requirements {Interest Mining Requirements}
Task Constraints: {Constraints}

# Preset Interest List
{Matched Interest Pool}

# Output Format
（详细的输出格式要求）

按照该提示模板设计，我们把用户兴趣挖掘过程形式化如下。给定从用户提供的信息中抽取的目标用户属性 \(\mathrm{A}_{u}\)（例如年龄、性别、所在地）、压缩行为序列 \(\mathrm{B}_{u}\)，以及预先配置的已匹配候选兴趣池 \(\mathrm{I}_{m}\)，我们利用用户兴趣 LLM LLM_UI 进行推断：

\[\mathrm{I}_{u} = \mathrm{LLM}_{UI}(\mathrm{A}_{u}, \mathrm{B}_{u}, \mathrm{I}_{m} \mid \mathrm{P}_{UI}), \quad (1)\]

其中 \(\mathrm{P}_{UI}\) 表示用户兴趣挖掘提示模板，\(\mathrm{I}_{u}=\{I_{u,1}, I_{u,2}, \ldots, I_{u,|\mathrm{I}_{u}|}\}\) 表示从给定用户信息推断出的潜在用户兴趣集合。该方法使模型能够通过基于 CoT 的推理，综合用户属性、行为模式与候选兴趣，挖掘个性化兴趣画像。

数据质量控制（Data Quality Control）。为减轻潜在的 LLM 幻觉与不准确，我们在准备训练数据时采用多维拒绝采样。正确（✓）与不正确（✗）兴趣的评估标准包含 2 个维度：

♦ 意愿性（Willingness）。该标准评估所识别的兴趣是否真正反映用户自愿的偏好，而不是外部义务。真正的兴趣体现内在动机与主动探索，并与必要性驱动的行为相区分。

– ✓ 自发性（Spontaneity）。兴趣来自自愿的喜爱与个人选择，由好奇心、热情或与个人价值观、经历或志向一致的满足感驱动。这类兴趣反映真实的用户偏好与内在动机。

– ✗ 必要性（Necessity）。被误分类为兴趣的行为，实际上可能源于外部压力、生存需要或情境要求（例如与职业相关的技能习得）。它们代表功能性需求，而不是真正的个人兴趣。

♦ 合理性（Reasonableness）。该标准确保推断出的用户兴趣有充分的行为证据支持，从而维持兴趣识别的可靠性与准确性。我们设立四个相关程度来评估兴趣合理性：

– ✓ 强相关（Strong Correlation）。推断出的兴趣与观察到的行为表现出清晰、合乎逻辑的联系，并有有力证据。行为模式以最小的歧义强烈支持该兴趣推断。

– ✗ 弱相关（Weak Correlation）。用户行为与推断兴趣只有部分联系，但证据不足。例如，购买网球裙可能在一定程度上暗示对网球的兴趣，但不能确凿地确立这一偏好。

– ✗ 无相关（No Correlation）。用户行为与推断兴趣没有有意义的联系。例如，购买《网球王子》（“The Prince of Tennis”）周边并不表明对网球运动的兴趣，因为它更可能反映的是对动漫的兴趣，而不是对该运动的兴趣。

– ✗ 幻觉（Hallucination）。生成的兴趣没有行为证据，代表由 LLM 编造的无根据关联。

表 1 的表注可读，单元格在抽取时按列交错，下表按表注中的 Label、Evaluation Criteria、Example、Why ✓ or ✗ 四列重组，例子原文保留。表 1：评估模型生成兴趣的标准。Correct 表示同时满足 Willingness 与 Strong Correlation 的兴趣；Incorrect 包含四类：Necessity、Weak Correlation、No Correlation 与 Hallucination。「Both ✓→ ✓」表示两项标准都满足时该兴趣视为正确；「Any ✗→ ✗」表示任一标准被违反时该兴趣视为不正确。

| Label | Evaluation Criteria | Example | Why ✓ or ✗ |
| --- | --- | --- | --- |
| Correct（Both ✓→ ✓） | Spontaneity（Willingness） | [Interest] tennis. | Tennis is an interest from affection. (Willingness ✓) |
| Correct（Both ✓→ ✓） | Strong Correlation（Reasonableness） | [Reason] User purchased a tennis racket. | Reason and the interest are related reasonably. (Strong Correlation ✓) |
| Incorrect（Any ✗→ ✗） | Necessity（Willingness） | [Interest] Purchasing household necessities. [Reason] Most purchases are daily cleaning items. | Purchasing household items is a daily need, not a hobby. |
| Incorrect（Any ✗→ ✗） | Weak Correlation（Reasonableness） | [Interest] Yoga. [Reason] Purchases include yoga pants. | May indicate clothing hobby, not yoga preference. |
| Incorrect（Any ✗→ ✗） | No correlation（Reasonableness） | [Interest] Model making. [Reason] User searched for many blankets. | Interest and reasoning are unrelated. |
| Incorrect（Any ✗→ ✗） | Hallucination（Reasonableness） | [Interest] Smart home. [Reason] User purchased smart home accessories. | User history has no smart home-related activities. |

使用上述数据质量控制协议，我们保留表现出强用户意图和清晰相关性的数据用于训练，同时滤除意图弱、相关性差或存在幻觉的数据，将其视为可能向学习过程引入噪声和偏差的低质量样本。通过这一严格的数据筛选过程，我们确保预对齐与自训练两个阶段的数据质量持续较高，从而提升模型在用户兴趣挖掘任务上的表现。

人工评估实验（Human Evaluation Experiments）。为验证多阶段对齐框架的有效性，我们针对不同模型的用户兴趣挖掘表现进行人工评估。我们评估两个基础 LLM：DeepSeek-R1，以及 Qwen3-14B（下文称为 Qwen3-Base）；同时评估我们经过多阶段对齐的模型：Qwen3（下文称为 Qwen3-SFT），以及 TBStars-42B-A3.5（下文称为 TBStars-SFT）。TBStars-42B-A3.5 是淘宝内部开发的稀疏混合专家（Mixture-of-Experts, MoE）大语言模型，每次推断只激活 3.5B 参数。生成的兴趣只有在满足前文列出的全部数据质量评估标准，包括意愿性与合理性两个维度时，才被视为「通过」。

表 2 的表注与数值可读。表 2：不同模型在用户兴趣挖掘任务上的人工评估通过率。最佳表现以粗体标出。

| Model | DeepSeek-R1 | Qwen3-Base | Qwen3-SFT | TBStars-SFT |
| --- | --- | --- | --- | --- |
| Pass Rate (%) | 70.00 | 59.74 | 77.28 | 74.39 |

如 Table 2 所示，DeepSeek-R1 的通过率为 70.00%，显著高于 Qwen3-Base 的 59.74%。这一性能差距表明，推理增强的 LLM 在从超长行为序列中挖掘用户兴趣时具有更强的上下文理解能力。此外，我们经过多阶段对齐的 Qwen3-SFT 取得最高表现 77.28%，大幅优于其基座模型。实验结果验证了对齐框架在增强领域特定兴趣挖掘能力上的有效性。

就实际在线部署而言，TBStars-SFT 在用收集到的高质量数据做全参数微调后达到 74.39% 的通过率，相对两个基线模型（即 DeepSeek-R1 与 Qwen3-Base）都有显著提升，同时因其稀疏架构保持了更优的性能–效率平衡。这一特点使其特别适合准确率与推断速度都至关重要的大规模在线推荐场景。

在线部署（Online Deployment）。我们离线使用模型 LLM_UI 预测用户的兴趣偏好，平均每用户预测 16.1 个兴趣。在线部署期间，我们进行迭代式模型优化，并每两周刷新一次用户兴趣，以保证用户兴趣的时效性，同时精确捕捉用户个性化兴趣的动态变化。

### 2.2 Item Tag Prediction 物品标签预测

本节探讨如何利用大语言模型，基于推断出的用户画像来引导物品标签预测。为把 LLM 的世界知识适配到特定商品领域，与 User Interest LLM LLM_IT 类似，我们首先进行多阶段任务对齐（Task Alignment），以确保 LLM_IT 能够有效理解并处理与商品相关的上下文信息（Section 2.2.1）。抽取原文为 “the User Interest LLMLLM IT”，LLM_UI 与 LLM_IT 的符号在此处粘连，对应关系【抽取不清】。接下来，我们引入增量学习（Incremental Learning）方法，使模型能够持续适应不断变化的用户兴趣与新的商品趋势（Section 2.2.2）。

### 2.2.1 Task Alignment for Item Tag Prediction 面向物品标签预测的任务对齐

尽管基础大语言模型展现出令人印象深刻的通用能力，由于推荐系统的领域特定要求，把它们直接用于个性化物品预测任务时并不充分。为克服这一局限，我们采用与 Item-Tag LLM 方法类似的两阶段对齐过程。该过程使用推理增强的预对齐（Reasoning-Enhanced Pre-Alignment）和自训练演化（Self-Training Evolution）来增强 LLM_IT 的领域感知商品理解。这里，我们聚焦于专门为物品标签预测任务设计的提示工程（Prompt Engineering）与数据质量控制（Data Quality Control）协议。此外，我们提供扩展的人工评估实验（Human Evaluation Experiments），以展示对齐方法在提升模型表现上的有效性。

图 4 位于本小节前部，图注可读。图 4：物品标签预测模块示意图。左图展示物品标签 LLM 的两阶段对齐过程以及数据质量控制标准，右图展示基于真实在线用户反馈数据的数据清洗与增量学习。图中还可读出的文字包括：Task Alignment、Item Tag LLM、Data Quality Control、Relevance、Consistency、Specificity、Validity、Offline、Incremental Learning、High-Quality Training Sample、Online、Incremental Training、Data Purification、Interest Completion、Data Balancing、Reasoning-Enhanced Pre-Alignment（~90k Samples）、Self-Training Evolution（~5k Samples），以及序号 1、2。物品标签 LLM 的数学符号抽取为 𝓛𝓛𝓜𝑰𝑻【抽取不清】。各框的具体连线与空间排布【抽取不清】。

提示工程（Prompt Engineering）。我们要求物品标签 LLM LLM_IT 基于所提供的用户画像信息以及多行为交互序列（如点击、购买、搜索），以「修饰词 + 核心词」（“Modifier + Core-Word”）格式预测标签集合（例如 “Outdoor waterproof non-slip hiking boots”）。我们采用基于 CoT 的标签推理，以充分利用大语言模型的推理能力。此外，我们在提示中加入以下约束，使生成的标签集合满足推荐系统的实际要求：

♦ 兴趣一致性（Interest Consistency）：生成的标签被约束为与用户兴趣保持对齐，从而避免与已建立的用户偏好画像相矛盾的推荐。

♦ 多样性增强（Diversity Enhancement）：强制至少 50 个标签，以保证跨广泛类目的多样推荐，减轻过滤气泡现象。

♦ 语义精确性（Semantic Precision）：标签生成被限制为语义上聚焦的描述，消除含糊或过于宽泛、会损害推荐准确性与用户体验质量的分类。

♦ 时间新鲜度（Temporal Freshness）：生成的标签应优先考虑新颖商品类目，同时系统性地避免对最近已交互物品的重复推荐，从而同时保证时间相关性与建议的多样性。

♦ 季节相关性（Seasonal Relevance）：把时间上下文整合进标签生成过程，以产生与所给时间戳对齐的应季推荐，通过具备上下文感知的建议提升用户满意度。

通过上述多约束提示策略，LLM_IT 生成一组三元组，包含 (Tag, Associated Interest Preference, Rationale)，供后续物品检索使用。详细的标签预测提示模板结构见 Prompt 2.2.1，其中 {User Attributes}、{User Interests}、{Click Behavior Sequence}、{Purchase Behavior Sequence}、{Search Behavior Sequence} 与 {Extra Information} 是相关用户画像与行为记录的占位符，在模型推断过程中动态填入。关于提示中的 {Recommendation Principles}、{Recommendation Requirements}、{Quantity Requirements} 与 {Strict Prohibitions}，由于篇幅限制，此处省略详细描述，规范见 Appendix B。

抽取在此截断。Section 2.2.1 在第 12 页之后仍有后续内容，Section 2.2.2、Section 2.3、Section 2.4 亦未进入本次抽取范围。
