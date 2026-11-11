# REGEN：带有自然语言批评与叙述的数据集及基准

- 原文件名：regen-2503.11924.pdf
- 原标题：REGEN: A Dataset and Benchmarks with Natural Language Critiques and Narratives
- 中文标题：REGEN：带有自然语言批评与叙述的数据集及基准
- 作者：Kun Su、Krishna Sayana、Hubert Pham、James Pine、Yuri Vasilevski、Raghavendra Vasudeva、Marialena Kyriakidi、Liam Hebert、Ambarish Jash、Anushya Subbiah、Sukhdeep Sodhi
- 会议或 arXiv：PDF 页眉为 Conference acronym ’XX, June 03–05, 2018, Woodstock, NY（ACM 模板占位）；第 1 页页脚为 arXiv:2503.11924v2 [cs.CL] 11 Jul 2025

<!-- 原 PDF 第 1 页 -->

**Kun Su**<sup>∗</sup>  
Google Research，Mountain View, CA, USA

**Krishna Sayana**<sup>∗</sup>  
Google Research，Mountain View, CA, USA

**Hubert Pham**<sup>∗</sup>  
Google Research，Mountain View, CA, USA

**James Pine**<sup>∗</sup>  
Google Research，Mountain View, CA, USA

**Yuri Vasilevski**<sup>∗</sup>  
Google Research，Mountain View, CA, USA

**Raghavendra Vasudeva**  
Google Research，Mountain View, CA, USA

**Marialena Kyriakidi**  
Google Research，Mountain View, CA, USA

**Liam Hebert**<sup>†</sup>  
University of Waterloo，Waterloo, Ontario, Canada

**Ambarish Jash**  
Google Research，Mountain View, CA, USA

**Anushya Subbiah**  
Google Research，Mountain View, CA, USA

**Sukhdeep Sodhi**  
Google Research，Mountain View, CA, USA

## 摘要

本文介绍一个新数据集 REGEN（Reviews Enhanced with GEnerative Narratives，用生成式叙述增强的评论），用于评测推荐大语言模型（LLM）的对话能力，以弥补现有数据集主要聚焦于序列物品预测的局限。REGEN 在 Amazon Product Reviews 数据集上补全两类关键的自然语言特征：（1）用户批评，即导致用户选择下一物品的「引导」查询；（2）叙述，即结合先前上下文、与每个被推荐物品相关联的丰富文本输出。叙述包括产品背书、购买解释，以及用户偏好摘要。

此外，我们为对话式推荐任务建立端到端建模基准：模型在以用户历史（物品与批评）为条件的情况下，被训练同时生成推荐与相应叙述。针对这一联合任务，我们提出建模框架 LUMEN（LLM-based Unified Multi-task Model with Critiques, Recommendations, and Narratives，基于 LLM 的、联合批评、推荐与叙述的统一多任务模型），它以 LLM 为骨干，用于批评、检索与生成。我们还用标准自动评分技术评估数据集质量，并通过训练传统推荐模型与基于 LLM 的推荐模型来建立基准。结果表明，纳入批评能够让推荐系统学习语言理解，并将其与推荐信号整合，从而提高推荐质量。进一步地，在我们的数据集上训练的 LLM 能够有效地同时生成推荐与上下文叙述，性能与当前最优的推荐系统及语言模型相当。

## CCS 概念

- Information systems → Recommender systems
- Computing methodologies → Natural language generation

## 关键词

序列推荐系统，大语言模型，生成式推荐系统

## ACM 参考格式

Kun Su, Krishna Sayana, Hubert Pham, James Pine, Yuri Vasilevski, Raghavendra Vasudeva, Marialena Kyriakidi, Liam Hebert, Ambarish Jash, Anushya Subbiah, and Sukhdeep Sodhi. 2018. REGEN：带有自然语言批评与叙述的数据集及基准. In Proceedings of Make sure to enter the correct conference title from your rights confirmation email (Conference acronym ’XX). ACM, New York, NY, USA, 11 pages. https://doi.org/XXXXXXX.XXXXXXX

<sup>∗</sup>同等贡献。

<sup>†</sup>工作完成于在 Google Research 期间。

允许为个人或课堂使用制作本作品全部或部分的数字或纸质副本，无需付费，前提是副本不为营利或商业优势而制作或分发，并且副本在首页载明本声明与完整引用。作者以外的他人对本作品组成部分所拥有的版权必须得到尊重。允许带署名的摘要。以其他方式复制、再发表、在服务器上张贴或向列表再分发，须事先获得特定许可和/或支付费用。许可请求请发至 permissions@acm.org。

Conference acronym ’XX, Woodstock, NY  
© 2018 Copyright held by the owner/author(s). Publication rights licensed to ACM.  
ACM ISBN 978-1-4503-XXXX-X/2018/06  
https://doi.org/XXXXXXX.XXXXXXX

## 1 引言

将大语言模型（LLM）用于对话式推荐系统 [9, 27, 35, 50, 53] 近来受到一些关注。除提供个性化推荐外，对话式推荐系统还与用户进行自然对话，例如解释推荐，以及根据用户的自然语言反馈改进推荐。LLM 有望满足此类推荐系统所需的语言能力。

这具有挑战性，因为现有的、用于训练对话式推荐系统的数据集缺乏丰富的上下文叙述与显式用户反馈。这样的数据集对于在被推荐物品的上下文中建模自然语言交互至关重要，从而使生成的文本与推荐及用户偏好一致且相关。尽管若干近期工作探索了把推荐系统内部状态与

arXiv:2503.11924v2 [cs.CL] 11 Jul 2025

<!-- 原 PDF 第 2 页 -->

本页及后续页面的页眉为：Conference acronym ’XX, June 03–05, 2018, Woodstock, NY；作者行：Kun Su, Krishna Sayana, Hubert Pham, James Pine, Yuri Vasilevski et al. 下文不再逐页重复该页眉。

图 1 见原 PDF。

**图 1：** REGEN 是用于训练对话式推荐模型的数据集。给定用户历史与反馈，模型同时输出物品推荐与有吸引力的自然语言。基于 Amazon Product Reviews 中的用户物品序列，REGEN 增加：（1）推断出的用户反馈，形式为自然语言批评；（2）丰富的文本叙述，形式为产品背书、购买理由与用户摘要——全部针对每个用户个性化。

图中文字（自文本层抽取）：

- 对话式推荐模型
- 用户物品序列：……；Avery 1" Durable View 3 Ring Binder……；Avery Heavy-Duty View Binder with 1.5-Inch One-Touch EZD Ring……
- 用户反馈（批评）：……；「2 英寸斜环，防撕裂的书脊与边缘」
- 被推荐物品：Avery 2" Durable View 3 Ring Binder, Slant Ring……
- 产品背书：「用 Avery 2" Durable View 3 Ring Binder 升级你的收纳！根据你此前购买的 Avery 活页夹，我们知道你看重耐用性以及……所提供的易用性。」
- 用户摘要：「这位顾客经常购买各种尺寸与颜色的 Avery 品牌活页夹，优先考虑耐用性与容量……」
- 叙述
- 购买理由：「顾客需要一个大容量活页夹来整理大量文件。」

LLM [16, 36, 50, 53] 整合起来的建模方法，但它们受限于现有数据集（例如 [5, 9, 25, 27, 34, 47]）。这些数据集集中于用户物品序列、简短对话片段、结构化输出，或缺乏丰富而多样对话要素的短摘要。

从用户处收集这样的数据集很困难，通常需要大量真实用户与对话式推荐系统交互。因此我们延续 [6, 23, 34] 的趋势，探索如下假设：LLM 能够（1）从现有的用户行为轨迹数据集中推断用户偏好与目标；（2）生成与真实行为一致、有说服力且合理的用户叙述与回应。除了便利之外，这一做法的一个优点是可以增强现有流行的序列推荐数据集。

我们提出 REGEN（Reviews Enhanced with GEnerative Narratives），一个通过纳入与对话式推荐相关的自然语言输出、来增强 Amazon Reviews 数据集 [34] 的数据集（图 1）。REGEN 增加多样的叙述，例如购买理由、解释、产品背书、用户摘要与简洁的用户画像，并针对每个用户个性化。它还增加合理的批评，即用户为引导推荐系统、针对推荐所发出的自然语言反馈。为增强数据集，我们使用 Gemini 1.5 Flash [44]，以少样本提示来补全叙述与批评。LLM 利用原始 Amazon Reviews 数据集中的用户评分历史、产品评论文本与物品描述来生成这些特征。作为可行性的初步度量，我们用一个自动评分 LLM [10] 自动检查质量。自动评分器跨多个属性评估生成输出，重点是基于用户历史交互的依据性（grounding）与事实性。

除数据集之外，还需要一个把用户行为与推荐整合起来的单一训练任务，以评估模型在这些方面的一致性与处理能力。尽管许多先前研究（例如 [9, 36]）提出的模型以各自独立的目标训练，例如做推荐、评分预测或评论生成，我们认为把这些方面结合起来的任务，是评估对话式推荐连贯性的关键一步。为帮助模型开发，我们提出单轮对话任务，作为迈向完全对话式推荐系统的一步。在该任务中，模型输入是用户的物品历史，并在部分物品之间加入用户批评。输出是下一个要推荐的物品，以及与被推荐物品和用户偏好一致的丰富自然语言叙述。该任务要求模型把个性化序列推荐、批评与自然语言生成有效地结合进完全对话式推荐系统的单一、连贯的一轮之中。

最后，为评估 REGEN 数据集与该任务的效用，我们给出参考模型与强基线。这里我们引入 LUMEN（LLM-based Unified Multi-task Model with Critiques, Recommendations, and Narratives），一个使用 LLM 骨干的单一模型，通过整合协同过滤信号、内容信号与自然语言批评输入，被训练来生成推荐与叙述。LUMEN 利用用户—物品交互数据、丰富的物品内容表示以及用户反馈，生成信息充分且与用户偏好对齐的输出。我们的实验建立了基准，表明该架构在产生类似人类的对话式推荐方面是有效的。

总之，主要贡献是：

- REGEN，一个开源数据集，<sup>1</sup> 带有与用户消费历史一致且个性化的批评与丰富自然语言叙述。我们从事实性、依据性以及准确反映用户上下文等方面评估它。
- 一个面向完全对话式推荐系统的相应任务，可作为未来研究的基础。
- 参考模型表明，把生成式推荐与语言任务结合起来的 LLM 架构，能够达到与当前最优推荐系统及语言模型相当的性能。
- 验证了模型学习并生成上下文丰富的叙述、以及利用用户批评动态引导推荐的能力。我们进一步展示了连贯对话轨迹的生成。

## 2 相关工作

REGEN 受到支持推荐系统开发与评估的现有数据集和建模任务的启发。

<sup>1</sup> https://www.kaggle.com/datasets/googleai/regen-reviews-enhanced-with-generative-narratives

<!-- 原 PDF 第 3 页 -->

### 2.1 数据集

#### 2.1.1 对话式

许多对话数据集基于对话，表示用户与智能体之间的会话。例如，DuRecDial [29, 30] 是一个众包的、带有预定义目标的多领域对话数据集。E-ConvRec [19] 提供一个基于用户与客服之间真实售前对话的大规模对话推荐数据集。ReDial [24] 是一个带标注的电影推荐对话数据集。TG-ReDial [52] 通过纳入主题信息来引导对话与推荐，从而扩展 ReDial；E-Redial [12] 则用外部知识扩展它，以改进可解释性。这些数据集聚焦于构造或收集对话，但通常缺乏对话与用户底层偏好或历史行为之间的耦合。LLM-Redial [27] 追求以用户为中心，通过植根于真实用户画像的模板来创建对话。REGEN 与 LLM-Redial 相似，都关注维持用户画像与叙述之间的一致性，但有若干不同。第一，REGEN 保留序列物品历史以维持时间一致性，从而能够以过去的用户行为为条件生成用户反馈与叙述。第二，REGEN 聚焦的不是短对话轮次，而是知识丰富的对话式推荐系统可能产生的、个性化的丰富叙述。我们认为，以叙述为中心的数据集有助于在被推荐物品与用户偏好的上下文中，检验推荐系统的语言理解。

#### 2.1.2 叙述

Ni 等人 [34] 的 “Justifying Recommendations” 数据集与 Chen 等人 [5] 的 “Unlocking the Why of Buying” 聚焦于从评论生成解释。Hou 等人 [15] 的 “Amazon-C4” 数据集提出一个新的评论数据集，它构造复杂查询并将其与物品关联，以在推荐任务上评估模型。REGEN 用适合若干推荐任务的开放式叙述扩展他们的工作：以整个用户历史为条件，并覆盖购买解释之外的用例。REGEN 的目标是反映 LLM 快速演进能力的自然语言输出，即更长、更细腻、半结构化与非结构化的回应。

#### 2.1.3 批评

经典推荐系统中的批评（critiquing）在 Chen and Pu [4]、Gao 等人 [8]、Jannach 等人 [18] 中有综述。早期批评系统允许用户对被推荐物品提供反馈，通常在特征层面，例如通过建议的预设计调整 [2]，或由语言驱动的对话系统 [11, 41, 46]。近期工作 [31, 32, 48] 探索联合学习用户、物品与关键短语的潜在表示的系统，其中关键短语作为批评，可通过潜在空间中的操作影响推荐。另一些工作探索属性的解释 [1, 33] 以支持批评。这些工作为把自然语言批评作为 REGEN 所提供的用户反馈载体奠定了基础。

### 2.2 推荐任务

#### 2.2.1 序列物品推荐

将 LLM 与推荐系统结合以做序列推荐，有大量正在进行的研究 [3, 7, 13, 14, 21, 26, 28, 36–38, 40, 42, 49, 51, 54]。这些模型探索表示物品与用户交互的不同方法（例如 ID 嵌入、文本嵌入），其中一些试图通过纳入物品和/或语义上下文来提高质量。物品推荐是 REGEN 支持的一项重要的首要任务。由于它基于流行的基准数据集 Amazon Reviews，我们认为 REGEN 自然适合把现有基于 LLM 的序列推荐系统扩展到同时生成语言。

#### 2.2.2 物品推荐与文本生成

有不少推荐模型同时输出物品推荐与自然语言。P5 [9] 把所有用户—物品信号连同相关上下文表示为自然语言序列，输入编码器/解码器模型。它为物品预测与文本生成提出若干任务族。User-LLM [36] 把用户历史编码为用户嵌入，并通过交叉注意力将其纳入 LLM。User-LLM 支持三项任务：下一物品推荐、流派预测与评论生成。尽管这些项目提出的任务同时涉及推荐与文本生成，它们是分开的任务。相比之下，REGEN 提议把这两类任务连同用户反馈一起，整合进一个单一的连贯任务，同时生成丰富而多样的叙述集合。

## 3 REGEN

本节详述 REGEN 数据集，包括批评与叙述的生成过程，以及用评分 LLM 的评估方法。用于建立基准的建模任务的进一步细节在下一节描述。

### 3.1 Amazon Reviews

我们使用 Amazon Product Reviews [34] 的数据集，作为用丰富叙述进行增强的基础。Amazon Reviews 数据集（2018）是跨越多种产品类目的大规模顾客评论集合。该版本于 2018 年发布，包含超过 2.33 亿条评论，是情感分析与推荐系统最大的公开数据集之一。每条评论包括标题、描述、类目、价格等物品特征，以及文本、时间戳、分数与摘要等评论特征。用户序列可通过按时间戳排序每个用户的评论来创建，从而形成序列推荐任务。在本工作中，我们使用 “Office Products” 与 “Clothing, Shoes and Jewelry” 这两个垂直领域。选择它们是为了作为物品数量不同的代表性样本：Office 有 2.7 万件物品，Clothing 有 37.6 万件物品。

**表 1：** 经 CALRec 处理的 Amazon Product Reviews 数据集统计。I/U 是每位用户的平均物品数，即平均序列长度。

| 数据集 | 用户数 | 物品数 | I/U |
| --- | --- | --- | --- |
| Office | 89,489 | 27,887 | 7.86 |
| Clothing | 1,168,735 | 376,847 | 9.21 |

### 3.2 数据集生成

#### 3.2.1 数据预处理

用户序列 $S_u = \{i_1, i_2, \ldots, i_n\}$ 由交互 $i$ 组成，首先按用户聚合评论并按时间戳排序而得到。为使结果可比较，我们使用 CALRec [26] 预处理后的数据集。值得注意的是，CALRec 的去重方法有助于缓解平凡的推荐策略，例如总是推荐最近的物品。数据集统计见表 1。

<!-- 原 PDF 第 4 页 -->

#### 3.2.2 用补全合成多轮对话

Amazon Reviews 数据集对推荐研究虽有价值，但主要反映的是一系列个别用户交互，而不是真实对话。为创建模拟多轮对话动态的合成数据集，我们采用补全（inpainting）技术，生成非对话式评论数据中通常缺失的要素。具体而言，我们利用 LLM 来合成这些要素，使用精心设计的提示与迭代评估过程，以确保高质量生成并尽量减少不准确之处。这使我们能够在推荐任务上与这些数据集上的现有研究比较，同时加入自然语言要素，并为语言任务设定新的基线。在本工作中，我们使用 Gemini 1.5 Flash 模型，即 Gemini 1.5 模型族 [44] 的一个快速、高效版本。

我们利用 LLM 的扩展上下文长度能力，有效处理每个用户 $u$ 的完整用户历史 $S_u$。我们的提示很简单：采用带有指令与期望输出格式的任务前缀。该前缀之后是用户的全部交互历史，包括物品元数据与评论文本。最后，提示指定期望的输出格式。我们使用用户历史及相关评论来生成批评、购买理由与摘要。然而，对于产品背书的生成，我们有意隐瞒用户的最后一条评论，使模型学习如何在不受该物品评论影响的情况下，为被推荐物品撰写背书。

#### 3.2.3 批评生成

REGEN 加入生成的批评（短语句），以把系统从当前被推荐物品引导到期望物品。我们的目标是聚焦如下设定：用户从一个物品细化到一个紧密相关的物品变体（例如从「红色圆珠笔」到「黑色圆珠笔」），而不是到另一个任意物品——后者更适合由其他机制处理，例如一条新的搜索查询。因此，REGEN 只在足够相似的相邻物品对之间生成批评。我们用 Amazon Reviews 提供的层次化物品类目作为物品相似度的粗略代理，若至少四级类目匹配，则认为物品足够相似。

为给满足相似度标准的相邻物品对生成批评，我们查询 Gemini 1.5 Flash 以合成若干选项，并指示 LLM 把第一件物品视为当前推荐，把第二件物品视为用户期望目标的代表。提示包含物品描述与少样本示例。我们随机选择一条生成的批评，补全到该物品对的数据集中。对于不满足相似度标准的物品对，REGEN 包含一个哨兵占位符。数据集使用者可以决定在占位符上训练，以建模终端用户不提供批评、从而模拟一次新搜索查询的情形，或者用其他批评替换它们。对于 “Clothing” 数据集，REGEN 为用户序列中约 18.6% 的相邻物品包含 LLM 生成的批评。对于 “Office” 数据集，这一比例约为 17.6%。

#### 3.2.4 叙述生成

我们旨在为对话式推荐系统生成多样的叙述，其变化体现在：

- 上下文化：基于近期上下文与汇总上下文信息的叙述（例如用户摘要相对于解释，以及对最近一次购买的背书）。
- 长度：面向不同对话场景的短篇与长篇叙述。

我们把 LLM 用作自动评估器，跨多个属性评估生成的批评与叙述。我们用 Amazon 产品评论数据集 [34] 展示该方法，并用 Gemini Pro 进行评估。叙述的详细描述与示例概括于表 2。

### 3.3 使用自动评分器的评估

我们采用 Gemini Pro LLM 作为自动评分器。评分器收到任务、对话历史与生成输出，并被提示根据定义的属性给输出打分。在本节中，我们展示 Office Products 数据集的评估指标与方法。我们在更大的 Clothing 数据集上总体上看到了相似的行为，因篇幅所限不予列入。

#### 3.3.1 总体方法

为提高可靠性，我们采用集成评分方法。每个输出被评分七次，分数聚合为最终分数。我们使用多数规则：若超过半数的集成运行在某个分数上一致，该分数即成为最终分数。若不存在多数，则使用平均分（向下取整）。尽管计算开销较大，该方法得到了更稳健的属性分数。我们给出全部对话上的分数分布，相应的用户分数也包含在发布的数据集中。此外，鉴于新的属性字段是在整个用户序列上补全的，我们通过在每个用户序列内随机选取属性值、再跨所有用户聚合，来捕捉分数分布。该方法提供了生成序列上属性分数分布的全面视图。属性定义概括于表 3。

#### 3.3.2 评估结果

对于叙述，我们提示评分 LLM 用七点 Likert 量表，在三个属性（真实性、个性化与说服力）上打分。所有叙述都评估真实性与个性化，产品背书还评估说服力。进一步地，我们用三次 LLM 调用进行评估，每次对应一个叙述组：i）购买理由与解释；ii）用户摘要；iii）产品背书。采用该做法是为了避免不同叙述类型之间由思维链（Chain of Thought，CoT）偏差引起的任何相关。

图 2 按属性分组展示评分分布。摘要显示出更高的个性化分数，而其他上下文叙述的分数较低。这是预期之中的，因为针对局部物品上下文做个性化本质上更难。对于检查幻觉与依据性的真实性，所有叙述上的分数相对更高。说服力针对产品背书评估，并在较低分数处呈现一定分布（约 35% 位于分数 = 3），这与部分用户上背书的个性化取值较低相关，可归因于序列中出现新产品。总体而言，这些结果表明，

<!-- 原 PDF 第 5 页 -->

**表 2：** 生成的叙述及其描述与示例。

| 上下文 | 生成输出 | 描述 | 示例 |
| --- | --- | --- | --- |
| 近期/物品 | 产品背书 | 根据购买历史与评论撰写的针对性背书/推销语 | 「这款 Michael Kors Bedford Top Zip Pocket Tote Bag 是奢华而实用的选择，非常适合欣赏品质与风格的人。根据你此前购买的舒适衣物与时尚凉鞋，这只包同时契合你对日常实用性与优雅点缀的品味。耐用的皮革、带多个口袋的宽敞内部，以及可调节提手，使它以精致的方式携带必需品。它是对一件永恒单品的很好投资，将提升你的日常造型，并在未来多年成为可靠的伴侣。」 |
| | 购买理由 | 对产品推荐背后原因的简洁解释 | 「顾客想要一只时尚、相对小巧、带多个口袋以便整理的托特包。」 |
| | 购买理由解释 | 在整个历史的上下文中，对最近一件物品的购买决定所作的详细、充分的解释 | 「顾客此前买过一条裙子，正在寻找一只能够搭配的时尚手提包。他们提到这只包比预期更小，但仍然时尚，并且有多个口袋。这表明顾客在寻找一只既实用又时髦的手提包。」 |
| 汇总/用户 | 简要用户摘要 | 对用户偏好与购买历史的简洁摘要 | 「这位顾客是一位女性，喜欢购买既时尚又舒适的衣物。她也对手提包等时尚配饰感兴趣。」 |
| | 详细用户摘要 | 对用户偏好与历史的全面摘要 | 「这位顾客是一位女性，品味偏向时尚而舒适的衣物。她购买过凉鞋、裙子和内衣，这些物品都表明她偏好时尚与舒适。她的评论还提到她看重品质，尤其是裙子这类衣物。她也对手提包等时尚配饰感兴趣。她似乎是偶尔购买的买家，购物方式更务实、频率更低。」 |
| | 用户画像 | 在产品/购物上下文中描述用户类型的短短语 | 「时尚而务实的女性」 |

**表 3：** 由自动 LLM 评分器生成的评分属性，用于评估批评与叙述的质量。

| 类别 | 评分属性 | 描述 |
| --- | --- | --- |
| 批评 | 质量 | 细化查询在有效引导推荐系统走向期望目标物品方面的有效性。 |
| | 具体性 | 查询在缩小搜索范围方面的精确程度。 |
| | 相关性 | 查询属性对于找到期望物品而言的意义与典型性。 |
| 叙述 | 真实性 | 购买理由的准确性与真实性，分析用户购买历史中的具体证据与不一致之处。 |
| | 个性化 | 叙述在何种程度上优先使用直接来自用户评论与陈述的信息，而不是依赖产品描述或一般假设。 |
| | 说服力 | LLM 作为熟练销售人员、撰写能有效向用户推销产品的语言的能力。 |

图 2 见原 PDF。

**图 2：** 按评分属性评估的叙述：i）个性化；ii）真实性；iii）说服力。对象为 Office Products。

<!-- 原 PDF 第 6 页 -->

图 3 见原 PDF。

**图 3：** 针对 Office Products 评估的批评：i）相关性；ii）具体性；iii）质量。

图 4 见原 PDF。

**图 4：** 在 Office Products 上用负采样进行的引导评估偏差。给定参考元组（历史，批评，下一物品）：A）随机化历史；B）把（历史，下一物品）随机化到另一位用户。这表明负样本上的分数低得多，并排除了自动评分器中的正向偏差。

在该数据集中，对某些用户的推荐与叙述受到流行行为的影响，而这种影响关联到他们自身的历史。

批评被表述为短查询，在三个关键属性上评估：i）质量；ii）具体性；iii）相关性，衡量它们在给定先前对话的情况下、引导推荐系统走向下一物品的有效性。图 3 展示分数分布，所有属性上的分数都高于平均。

#### 3.3.3 评估偏差

图 3 显示，批评在所有属性上的自动评分都很高。为处理潜在的正向偏差，我们生成负样本：A）通过交换与被推荐物品相关联的历史（重置为搜索场景）；B）通过同时交换历史与物品（从另一位用户选取）。真实的历史、批评、物品以及相应负样本分别表示为 $(\tilde{H}, C, I)$ 与 $(\tilde{H}, C, \tilde{I})$。图 4 展示高分（$\ge 6$）的比例：完全随机化的样本（B）更低，历史被交换的样本（A）略高，符合预期。具体性与历史和物品的相关性较低，因为它在一定程度上衡量的是批评本身的精确度。

## 4 基准方法

本节详述任务定义与建模架构。

### 4.1 任务定义

我们在用户交互序列的框架内形式化对话式推荐任务。考虑序列数据集 $S = \{i_1, i_2, \ldots, i_n\}$，其中每个交互（$i \in \mathcal{I}$）由元组 $(\mathrm{ID}, T, P, C, \mathcal{T})$ 表示。这里，$\mathrm{ID}$ 表示唯一物品标识；$T = \{t_1, t_2, \ldots, t_m\}$ 表示描述物品的一组自然语言成分（包括标题、详细产品描述、类目及其他文本元数据）；$P$ 表示与物品相关联的、用户特定的个性化文本（例如评论、评分或其他用户生成内容）；$C$ 表示影响后续物品选择的、用户显式批评指令；$\mathcal{T}$ 是与截至 $n$、包括当前物品在内的交互相对应的叙述。我们定义如下任务：

（1）**推荐任务（下一物品预测）：** 给定用户交互历史 $S$，预测下一物品 $i_{n+1}$。这是标准的序列推荐目标。

（2）**带批评的推荐任务：** 给定用户历史 $S$ 与用户批评 $C$，预测下一物品 $i_{n+1}$。

（3）**对话式推荐任务：** 以前序交互 $S$ 与批评 $C$ 为条件，生成推荐 $i_{n+1}$ 与自然语言叙述 $\mathcal{T}_{n+1}$。该任务强调捕捉用户偏好与批评，并生成推荐以及上下文相关的叙述。

本文以第二与第三项任务为中心，因为它们与所提出的数据集直接对齐。第一项任务已被广泛研究，我们把它作为基线纳入。

### 4.2 模型架构

我们评测两种架构，如图 5 所示：一种用 LLM 增强以产生生成式输出的混合序列推荐系统，以及 LUMEN，一种纯基于 LLM 的生成式推荐系统。下面详细描述。

#### 4.2.1 混合序列推荐系统 + LLM

该方法把传统序列推荐系统与 LLM 整合起来，如图 5a 所示。序列推荐系统聚焦于建模协同过滤信号（编码在用户—物品交互历史中），而 LLM 负责更深的语义理解与叙述生成。序列推荐系统在给定用户历史（包括每件物品的内容元数据）时产生推荐。我们使用 FLARE [14] 作为混合序列推荐系统，它用学习到的嵌入以及由语言模型对元数据（例如物品标题、描述）所作的基于内容的编码来表示每件物品。一个 Perceiver 重采样器 [17] 把二者结合起来，为每件物品产生单一嵌入。该架构允许在序列推荐任务内用自然语言进行引导。序列通过标准 Transformer 栈，并用标准掩码语言模型（例如 BERT4Rec [43]）训练。输出

<!-- 原 PDF 第 7 页 -->

图 5 见原 PDF。

**图 5：** 用于基准的建模架构。

**（a）** 混合序列推荐系统（FLARE）+ LLM。图中文字包括：嵌入表；LLM 嵌入器；Item_ID；物品元数据；Transformer 编码器；Softmax；已训练；冻结；掩码；Title: XL Printer；Description: This …；Category: Office…；B00EJ9HTE8；Gemma LLM；推荐；叙述；用户历史；用户批评；提示生成；投影。

**（b）** LUMEN：用于批评与生成式推荐的 LLM。图中文字包括：用户历史与批评；文本或 Item_ID；文本嵌入；物品嵌入；Gemma LLM；任务提示；推荐与叙述。

推荐既展示给用户，也作为 LLM 组件的条件。LLM 还以用户历史为条件生成叙述。该架构模拟把传统推荐系统与 LLM 整合的系统，二者可以一起训练或分开训练。在我们的实验中，这些组件是分开训练的。为生成叙述，我们用由一串交互以及任何用户批评组成的用户历史来提示 LLM。用如下结构表示用户购买历史中的每件物品：

**输入提示：** 这是一位用户购买历史的摘要。第一次物品购买是 START ID: \<id\> Title: \<title\> Category: \<category\> Description: \<description\> Price: \<price\> Rating: \<rating\> User Review: \<review\> User Critique: \<user critique\> END... 下一次物品购买是 START ... END ... 最后一次物品购买是：\<id（来自推荐系统）\> .... 预测最后购买物品的 \<叙述类型\>。

**目标：** \<叙述\>

#### 4.2.2 LUMEN：用 LLM 做批评、生成式推荐与叙述

图 5b 展示 LUMEN，一个建模框架，其中 LLM 被训练来既理解批评，又充当生成式推荐系统，此外还具备叙述生成能力。这是通过在语言模型中增加一张额外的嵌入表、以直接生成物品 ID 词元来实现的。具体而言，这张新的嵌入表通过对物品词表的 softmax 损失学习，用于预测这些 ID 词元。我们的方法受到 Semantic ID [39] 的启发，后者把物品表示为由语义嵌入导出、并在 LLM 训练期间精炼的词元序列。然而，Semantic ID 在词元化中采用预先计算的层次，LUMEN 则使用随机初始化的嵌入与单词元 ID，并与 LLM 一起完全训练。我们发现，鉴于基准数据集的词表规模，这一简化效果良好，并允许训练单一的端到端模型，从而提高基准的可复现性。

为同时管理物品 ID 与语言词元的生成，我们维持分开的词表。推理时，解码器动态选择合适的词表，并用一个特定词元来发出生成物品 ID 的信号。提示结构与前一方法一致，例外是用占位词元（ID_TOKEN）表示物品 ID 的位置。该做法类似于 Gemma [45] 中用于多模态输入与输出的技术。所用的输入与输出提示结构如下：

**输入提示：** 这是一位用户购买历史的摘要。第一次物品购买是 START ID: ID_TOKEN Title: \<title\> Category: \<category\> Description: \<description\> Price: \<price\> Rating: \<rating\> User Review: \<review\> User Critique: \<user critique\> END. 下一次物品购买是 START ID_TOKEN... END... 下一次物品购买以及产品背书是：

**目标：** ID: ID_TOKEN Text: \<叙述\>

训练期间，ID_TOKEN 占位符被替换为来自物品词表的对应物品 ID 嵌入。解码期间，当检测到 START 词元时，我们从文本词表切换到物品词表以生成一个 ID_TOKEN。一旦生成 ID_TOKEN，我们切换回文本词表，然后继续自回归解码文本词元，以生成相关联的叙述。我们的假设是，该方法使 LLM 能够在对话式推荐的上下文中学习一个有意义的物品嵌入空间，并与文本所表示的语义空间对齐。我们通过在一系列基准上比较这两种架构的性能来评估该假设。

## 5 实验

为建立基准，我们实现了两种模型架构：i）FLARE 序列推荐系统 [14] 用于生成推荐，并耦合 Gemma 2B [45] LLM，在以被推荐物品为条件的情况下生成叙述；ii）LUMEN，使用 Gemma 2B 作为 LLM，用于联合的推荐与叙述生成。我们在 REGEN 数据集上评估这些模型，聚焦于第 4.1 节详述的对话任务。评估跨越两个类目：i）Office Products，包含约 2.8 万件物品；ii）Clothing, Shoes, & Jewelry，包含约 37.6 万件物品。这使我们能够在物品词表规模显著不同的数据集上评估模型性能。

<!-- 原 PDF 第 8 页 -->

**表 4：** Office Products 数据集——联合推荐与生成任务的基准。为评估性能上界，在生成 Flare+LLM 叙述时，我们提供真实的下一物品 $\mathrm{ID}_{t+1}$。

| 对话任务 | 指标 | 购买理由 Flare+LLM | 购买理由 LUMEN | 用户摘要 Flare+LLM | 用户摘要 LUMEN | 产品背书 Flare+LLM | 产品背书 LUMEN | 购买理由解释 Flare+LLM | 购买理由解释 LUMEN | 长用户摘要 Flare+LLM | 长用户摘要 LUMEN |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 历史 → ID + 叙述 | Recall@10 | 0.124 | 0.098 | 0.124 | 0.10 | 0.124 | 0.10 | 0.124 | 0.091 | 0.124 | 0.098 |
| | NDCG@10 | 0.0976 | 0.078 | 0.0976 | 0.08 | 0.0976 | 0.08 | 0.0976 | 0.071 | 0.0976 | 0.078 |
| | MRR | 0.0925 | 0.072 | 0.0925 | 0.074 | 0.0925 | 0.074 | 0.0925 | 0.064 | 0.0925 | 0.072 |
| | BLEU | 19.99 | 5.43 | 15.05 | 12.47 | 16.77 | 5.34 | 20.2 | 10.34 | 15.14 | 11.4 |
| | ROUGE | 41.3 | 17.3 | 34.9 | 31.8 | 31.2 | 19.9 | 40.2 | 27.5 | 31.7 | 26.4 |
| | Sem. Sim. | 0.833 | 0.642 | 0.87 | 0.849 | 0.927 | 0.742 | 0.88 | 0.743 | 0.905 | 0.858 |
| 历史 + 批评 → ID + 叙述 | Recall@10 | 0.1402 | 0.123 | 0.1402 | 0.117 | 0.1402 | 0.124 | 0.1402 | 0.122 | 0.1402 | 0.122 |
| | NDCG@10 | 0.113 | 0.102 | 0.113 | 0.098 | 0.113 | 0.103 | 0.113 | 0.1 | 0.113 | 0.1 |
| | MRR | 0.1076 | 0.095 | 0.1076 | 0.092 | 0.1076 | 0.097 | 0.1076 | 0.094 | 0.1076 | 0.094 |
| | BLEU | 19.0 | 6.21 | 15.46 | 12.52 | 16.19 | 5.61 | 20.15 | 11.09 | 15.89 | 11.98 |
| | ROUGE | 41.3 | 19.0 | 36.5 | 31.9 | 30.7 | 20.0 | 40.0 | 28.8 | 33.3 | 27.8 |
| | Sem. Sim. | 0.816 | 0.651 | 0.87 | 0.851 | 0.929 | 0.747 | 0.891 | 0.757 | 0.897 | 0.87 |

**表 5：** Clothing 数据集——联合推荐与生成任务的基准。为评估性能上界，在生成 Flare+LLM 叙述时，我们提供真实的下一物品 $\mathrm{ID}_{t+1}$。

| 任务 | 指标 | 购买理由 Flare+LLM | 购买理由 LUMEN | 用户摘要 Flare+LLM | 用户摘要 LUMEN |
| --- | --- | --- | --- | --- | --- |
| 历史 → ID + 叙述 | Recall@10 | 0.126 | 0.127 | 0.126 | 0.118 |
| | NDCG@10 | 0.117 | 0.111 | 0.117 | 0.100 |
| | MRR | 0.115 | 0.106 | 0.115 | 0.094 |
| | BLEU | 19.2 | 10.2 | 16.4 | 12.8 |
| | ROUGE | 39.8 | 29.7 | 33.9 | 29.9 |
| | Sem. Sim. | 0.89 | 0.78 | 0.92 | 0.90 |
| 历史 + 批评 → ID + 叙述 | Recall@10 | 0.136 | 0.143 | 0.136 | 0.151 |
| | NDCG@10 | 0.124 | 0.122 | 0.124 | 0.134 |
| | MRR | 0.122 | 0.115 | 0.122 | 0.128 |
| | BLEU | 19.2 | 10.5 | 16.3 | 13.3 |
| | ROUGE | 40.0 | 30.2 | 34.1 | 30.3 |
| | Sem. Sim. | 0.89 | 0.79 | 0.92 | 0.90 |

### 5.1 设置

#### 5.1.1 训练与评估

我们用标准指标评估推荐性能：Recall@N、NDCG@N 与 MRR，$N$ 设为 10。这些指标在推荐任务中被广泛采用。为评估生成文本的质量，我们采用 BLEU 与 ROUGE 来衡量 n-gram 相似度。此外，我们使用语义相似度指标，计算为由 Gecko 嵌入模型 [22] 生成的句子嵌入之间的余弦相似度。为把数据集划分为训练、验证与测试集，我们采用留一法 [20]，这是序列推荐中的常见做法。具体而言，前 $N-2$ 次交互用于训练，前 $N-1$ 次交互且留出最后一件物品用于验证，全部 $N$ 次交互且留出最后一件物品用于测试。

#### 5.1.2 实现细节

我们建立基准的主要目标，是用近期研究中众所周知的架构，为对话式推荐提供有代表性的性能结果，而不是推崇某一种特定的模型配置。尽管我们加入了一些对该任务和该数据集效果良好的变体，并在每个框架内做了基本的超参数调优，我们承认更广泛的优化——包括更细粒度的调优以及使用更大的组件模型——有可能得到更好的结果。我们将这些留待未来研究。

对于混合序列推荐系统，我们在训练期间采用掩码语言建模（Masked Language Modeling，MLM）任务以提高样本效率。我们使用 Adam 优化器，$\beta_1 = 0.9$、$\beta_2 = 0.99$，并采用 [14] 中详述的超参数配置。此外，我们作了一个简化假设：真实物品对 LLM 可用。对物品推荐中的误差进行建模，需要把序列编码器与解码器 LLM 模型一起协同训练或一起评估，这难以复现。另一方面，在该假设下，我们把这一方法的结果视为联合推荐与生成任务的上界。该做法也易于复现，便于比较其他组件模型。

对于利用 LLM 做推荐的 LUMEN，我们在长度至多为 $N-2$ 的子序列上，为联合推荐与生成任务进行训练。我们使用 Gemma 2B 模型，批大小为 512，恒定学习率为 $1\mathrm{e}{-5}$，训练至多 10,000 步，并使用早停。

### 5.2 结果与讨论

我们的实验结果概括于表 4 与表 5，得到如下主要发现：

#### 5.2.1 推荐性能

为建立基线，我们首先比较推荐指标；在 Amazon 数据集的相关工作中，若干推荐模型的这些指标已有充分研究。在 REGEN Clothing（表 5）上，与作为基线的 FLARE（见 [14] 及其中的参考文献）相比，在联合任务上训练的 LUMEN 尽管在单一模型内同时生成推荐与叙述，仍取得有竞争力的性能，Recall@10 与 MRR 常常落在 $\pm 0.01$ 以内，并在某些情况下提升性能。

<!-- 原 PDF 第 9 页 -->

图 6 见原 PDF。

**图 6：** 来自 LUMEN 的一条示例轨迹。它在 REGEN 上使用联合生成任务，展示对话式推荐模型处理购买交互与上下文中自然语言批评的能力。这一处理改进了预测物品，并生成与预测对齐的自然语言背书。

图中文字：

- 对话式推荐系统（LUMEN）
- 用户物品序列：Sharpie 37003 Ultra-Fine Permanent Marker；Sharpie 37001 Permanent Markers；Sharpie Permanent Markers；Sharpie 37001 Permanent Markers（最后一件物品）
- 用户反馈（批评）：我需要更大的、凿尖的，用于工业用途
- 目标物品：Sharpie 15001 Box of 12 Sharpie Pro King Size Chisel Tip Permanent Markers
- 无批评时的预测物品：Sharpie 37003 Ultra-Fine Permanent Marker
- 背书：用 Sharpie 37001 Permanent Markers, Ultra Fine Point, Black, 12 支装升级你的书写体验！我们看到你此前购买并喜爱过……非常适合精细工作、记笔记，或任何需要精确度的任务，这些记号笔对家庭和办公室使用都很理想。鉴于你此前对 Sharpie 记号笔的正面体验……
- 有批评时的预测物品：Sharpie 15001 Box of 12 Sharpie Pro King Size Chisel Tip Permanent Markers
- 背书：根据你此前购买的黑色与紫色 Sharpie Ultra Fine Point 永久记号笔，以及你一贯的高评分，我们相信你会喜欢 Sharpie 37001 Industrial Chisel Tip Markers。这些记号笔提供同样的……并带有更大的凿尖，以便作出更醒目、更可见的标记。非常适合那些更大规模的项目……鉴于你使用 Sharpie 记号笔完成从贴标签到艺术项目等各类任务的历史，这些工业级记号笔将提供同样可靠的……

然而，对于 Office Products（表 4），我们看到推荐指标略低，处于基线的 10–15% 以内。Office 数据集的词表显著更小（约 2.7 万），训练数据规模也更小（约 9 万）（表 1）。我们认为这表明，要在联合任务上训练的模型中保持推荐性能，需要足够大的训练数据集。

#### 5.2.2 带自然语言批评的推荐性能

纳入用户批评持续提升推荐性能。对于混合模型与端到端 LUMEN 模型，Recall@10 与 NDCG@10 的提升为 $+0.01$–$0.02$，MRR 的提升为 $+0.01$–$0.03$（表 5）。

#### 5.2.3 叙述性能

正如预期，LUMEN 的叙述质量分数（BLEU、ROUGE）低于直接以真实物品为条件的混合模型。我们把这一性能差距主要归因于推荐误差，因为 LUMEN 的叙述在单一端到端模型中基于它自己预测的物品。我们发现，这种依赖对「用户摘要」这类汇总叙述影响较小，它们较少依赖最近一次物品推荐的准确性，而更多依赖整体用户历史。在这种情况下，LUMEN 与单独训练来生成叙述的 LLM 相比表现良好。进一步地，我们预期，在推荐系统的输出被直接用作 LLM 输入的整合式混合架构中，可能会看到类似的误差。

#### 5.2.4 用模型轨迹验证

图 6 展示一条示例轨迹，说明在 REGEN 数据集上、于联合任务中训练的 LUMEN 模型所具备的推荐、自然语言理解与生成能力。

## 6 局限与结论

本文介绍了 REGEN，一个用个性化叙述与批评增强 Amazon Reviews 的新数据集，从而促成对话式推荐中的一项新任务。对 REGEN 的批评做全面的人类评估、考察其「自然程度」会是有益的，尤其鉴于它们被用作用户反馈的代理；但我们认为，即便没有这一点，REGEN 仍然有价值。为规模化的、主观且依赖上下文的文本任务获得可靠的人类标注是困难的。此外，数据集的效用并不完全取决于与人类的完美对齐，Amazon Reviews 尽管有其局限仍被广泛使用，即是证明。我们通过展示 REGEN 在开发对话式推荐模型方面的有效性来表明其价值：这些模型整合了序列推荐、批评生成与叙述生成。

我们的基准工作虽然有效，但使用了相对简单的架构，包括随机初始化的嵌入与单词元 ID。对于更大的物品空间，未来工作可以探索多词元 Semantic ID [39] 或其他更丰富的表示等优化。

总之，REGEN 提供了一个具有一致的用户偏好、推荐与生成叙述的数据集，使人们能够研究 LLM 在对话式推荐中的能力。我们用 LUMEN——一个用于联合推荐与叙述生成的、基于 LLM 的模型——以及序列推荐模型评估了 REGEN，展示了它的效用。我们相信，REGEN 是研究对话式推荐模型能力的一项基础资源，而这是迈向个性化多轮系统的关键一步。

## 参考文献

[1] Krisztian Balog, Filip Radlinski, and Alexandros Karatzoglou. 2021. 论推荐中软属性的解释与度量. In SIGIR ’21. ACM, New York, NY, USA, 890–899.

[2] Robin Burke, Kristian Hammond, and Benjamin Christopher Young. 1996. 复杂信息空间的基于知识的导航. In AAAI 96 and IAAI 96, Vol. 1. 462–468.

[3] Chanapa Channarong, Chawisa Paosirikul, Saranya Maneeroj, and Atsuhiro Takasu. 2022. HybridBERT4Rec：基于 BERT 的混合（基于内容的过滤与协同过滤）推荐系统. IEEE Access 10 (2022), 56193–56206.

[4] Li Chen and Pearl Pu. 2012. 基于批评的推荐系统：综述与新兴趋势. User Model. User-adapt Interact. 22, 1 (April 2012), 125–150.

[5] Tao Chen, Siqi Zuo, Cheng Li, Mingyang Zhang, Qiaozhu Mei, and Michael Bendersky. 2024. 解开购买之「为什么」：引入用于购买理由与购后体验的新数据集与基准. arXiv:2402.13417 [cs.IR] https://arxiv.org/abs/2402.13417

[6] Zhuyun Dai, Arun Tejasvi Chaganty, Vincent Y Zhao, Aida Amini, Qazi Mamunur Rashid, Mike Green, and Kelvin Guu. 2022. 对话补全：把文档变成对话. In Proceedings of the 39th International Conference on Machine Learning (Proceedings of Machine Learning Research, Vol. 162), Kamalika Chaudhuri, Stefanie Jegelka, Le Song, Csaba Szepesvari, Gang Niu, and Sivan Sabato (Eds.). PMLR, 4558–4586. https://proceedings.mlr.press/v162/dai22a.html

<!-- 原 PDF 第 10 页 -->

[7] Sumanth Doddapaneni, Krishna Sayana, Ambarish Jash, Sukhdeep Sodhi, and Dima Kuzmin. 2024. 用于个性化语言提示的用户嵌入模型. arXiv:2401.04858 [cs.CL] https://arxiv.org/abs/2401.04858

[8] Chongming Gao, Wenqiang Lei, Xiangnan He, Maarten de Rijke, and Tat-Seng Chua. 2021. 对话式推荐系统的进展与挑战：综述. AI Open 2 (Jan. 2021), 100–126.

[9] Shijie Geng, Shuchang Liu, Zuohui Fu, Yingqiang Ge, and Yongfeng Zhang. 2022. 把推荐作为语言处理（RLP）：统一的预训练、个性化提示与预测范式（P5）. In RecSys ’22. Association for Computing Machinery, New York, NY, USA, 299–315.

[10] Sally Goldman and Yuri Vasilevski. 2024. RoboRater：用 LLM 自动评定面向任务的对话. In AAAI 2024 Spring Symposium on User-Aligned Assessment of Adaptive AI Systems. https://aair-lab.github.io/aia2024/papers/goldman_aia24.pdf

[11] Peter Grasch, Alexander Felfernig, and Florian Reinfrank. 2013. ReComment：迈向带语音交互的基于批评的推荐. In RecSys ’13. Association for Computing Machinery, New York, NY, USA, 157–164.

[12] Shuyu Guo, Shuo Zhang, Weiwei Sun, Pengjie Ren, Zhumin Chen, and Zhaochun Ren. 2023. 迈向可解释的对话式推荐系统. In Proceedings of the 46th International ACM SIGIR Conference on Research and Development in Information Retrieval (Taipei, Taiwan) (SIGIR ’23). Association for Computing Machinery, New York, NY, USA, 2786–2795. doi:10.1145/3539618.3591884

[13] Jesse Harte, Wouter Zorgdrager, Panos Louridas, Asterios Katsifodimos, Dietmar Jannach, and Marios Fragkoulis. 2023. 利用大语言模型做序列推荐. In RecSys ’23. Association for Computing Machinery, New York, NY, USA, 1096–1102.

[14] Liam Hebert, Marialena Kyriakidi, Hubert Pham, Krishna Sayana, James Pine, Sukhdeep Sodhi, and Ambarish Jash. 2024. FLARE：融合语言模型与协同架构以增强推荐系统. arXiv:2409.11699 [cs.IR] https://arxiv.org/abs/2409.11699

[15] Yupeng Hou, Jiacheng Li, Zhankui He, An Yan, Xiusi Chen, and Julian McAuley. 2024. 为检索与推荐桥接语言与物品. arXiv:2403.03952 [cs.IR] https://arxiv.org/abs/2403.03952

[16] Wenyue Hua, Shuyuan Xu, Yingqiang Ge, and Yongfeng Zhang. 2023. 如何为推荐基础模型索引物品 ID. In SIGIR-AP ’23. Association for Computing Machinery.

[17] Andrew Jaegle, Felix Gimeno, Andy Brock, Oriol Vinyals, Andrew Zisserman, and Joao Carreira. 2021. Perceiver：带迭代注意力的通用感知. In ICML ’21 (Proceedings of Machine Learning Research, Vol. 139). PMLR, 4651–4664.

[18] Dietmar Jannach, Ahtsham Manzoor, Wanling Cai, and Li Chen. 2021. 对话式推荐系统综述. ACM Comput. Surv. 54, 5 (May 2021), 1–36.

[19] Meihuizi Jia, Ruixue Liu, Peiying Wang, Yang Song, Zexi Xi, Haobin Li, Xin Shen, Meng Chen, Jinhui Pang, and Xiaodong He. 2022. E-ConvRec：面向电子商务客服的大规模对话推荐数据集. In Proceedings of the Thirteenth Language Resources and Evaluation Conference. 5787–5796.

[20] Wang-Cheng Kang and Julian McAuley. 2018. 自注意力序列推荐. In 2018 IEEE International Conference on Data Mining (ICDM). 197–206. doi:10.1109/ICDM.2018.00035

[21] Sein Kim, Hongseok Kang, Seungyoon Choi, Donghyun Kim, Minchul Yang, and Chanyoung Park. 2024. 大语言模型遇见协同过滤：一种高效、全面的基于 LLM 的推荐系统. In Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining (Barcelona, Spain) (KDD ’24). Association for Computing Machinery, New York, NY, USA, 1395–1406. doi:10.1145/3637528.3671931

[22] Jinhyuk Lee, Zhuyun Dai, Xiaoqi Ren, Blair Chen, Daniel Cer, Jeremy R. Cole, Kai Hui, Michael Boratko, Rajvi Kapadia, Wen Ding, Yi Luan, Sai Meher Karthik Duddu, Gustavo Hernandez Abrego, Weiqiang Shi, Nithi Gupta, Aditya Kusupati, Prateek Jain, Siddhartha Reddy Jonnalagadda, Ming-Wei Chang, and Iftekhar Naim. 2024. Gecko：从大语言模型蒸馏出的通用文本嵌入. arXiv:2403.20327 [cs.CL] https://arxiv.org/abs/2403.20327

[23] Megan Leszczynski, Shu Zhang, Ravi Ganti, Krisztian Balog, Filip Radlinski, Fernando Pereira, and Arun Tejasvi Chaganty. 2023. 边说边走：面向对话式音乐推荐的合成数据生成. arXiv:2301.11489 [cs.IR] https://arxiv.org/abs/2301.11489

[24] Raymond Li, Samira Ebrahimi Kahou, Hannes Schulz, Vincent Michalski, Laurent Charlin, and Chris Pal. 2018. 迈向深度对话式推荐. In Advances in Neural Information Processing Systems 31 (NIPS 2018).

[25] Xiangnan Li, Lei Zhao, Xiang He, Mengdi Zhang, Qi Wu, and Panupong Pasupat Chang. 2017. Redial：一个用于群组推荐的大规模数据集. In Proceedings of the 40th international ACM SIGIR conference on research and development in information retrieval. 1157–1160.

[26] Yaoyiran Li, Xiang Zhai, Moustafa Alzantot, Keyi Yu, Ivan Vulić, Anna Korhonen, and Mohamed Hammad. 2024. CALRec：面向序列推荐的生成式 LLM 对比对齐. In RecSys 2024.

[27] Tingting Liang, Chenxin Jin, Lingzhi Wang, Wenqi Fan, Congying Xia, Kai Chen, and Yuyu Yin. 2024. LLM-REDIAL：用 LLM 从用户行为创建的、面向对话式推荐系统的大规模数据集. In Findings of the Association for Computational Linguistics: ACL 2024, Lun-Wei Ku, Andre Martins, and Vivek Srikumar (Eds.). Association for Computational Linguistics, Bangkok, Thailand, 8926–8939. doi:10.18653/v1/2024.findings-acl.529

[28] Cheng-Te Lin, Hung-Yi Lee, Ming-Feng Sun, Wen-Chi Hwang, et al. 2021. M6-Rec：用于对话式推荐的生成式预训练语言模型. In Proceedings of the 15th ACM Conference on Recommender Systems. 629–637.

[29] Zeming Liu, Haifeng Wang, Zheng-Yu Niu, Hua Wu, and Wanxiang Che. 2021. DuRecDial 2.0：用于对话式推荐的双语平行语料库. In Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing. Association for Computational Linguistics, Online and Punta Cana, Dominican Republic, 4335–4347. doi:10.18653/v1/2021.emnlp-main.356

[30] Zeming Liu, Haifeng Wang, Zheng-Yu Niu, Hua Wu, Wanxiang Che, and Ting Liu. 2020. 迈向跨多类型对话的对话式推荐. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, Dan Jurafsky, Joyce Chai, Natalie Schluter, and Joel Tetreault (Eds.). Association for Computational Linguistics, Online, 1036–1049. doi:10.18653/v1/2020.acl-main.98

[31] Kai Luo, Scott Sanner, Ga Wu, Hanze Li, and Hojin Yang. 2020. 面向对话式推荐系统的潜在线性批评. In WWW ’20. Association for Computing Machinery, New York, NY, USA, 2535–2541.

[32] Kai Luo, Hojin Yang, Ga Wu, and Scott Sanner. 2020. 面向基于 VAE 的推荐系统的深度批评. In SIGIR ’20. Association for Computing Machinery, New York, NY, USA, 1269–1278.

[33] Preksha Nema, Alexandros Karatzoglou, and Filip Radlinski. 2021. 用 β-VAE 为推荐批评解耦偏好表示. In CIKM ’21. Association for Computing Machinery, New York, NY, USA, 1356–1365.

[34] Jianmo Ni, Jiacheng Li, and Julian McAuley. 2019. 用远程标注的评论与细粒度方面来为推荐提供理由. In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP). Association for Computational Linguistics, Hong Kong, China, 188–197.

[35] Lin Ning, Luyang Liu, Jiaxing Wu, Neo Wu, Devora Berlowitz, Sushant Prakash, Bradley Green, Shawn O’Banion, and Jun Xie. 2024. User-LLM：用用户嵌入实现高效的 LLM 上下文化. arXiv:2402.13598 [cs.CL] https://arxiv.org/abs/2402.13598

[36] Lin Ning, Luyang Liu, Jiaxing Wu, Neo Wu, Devora Berlowitz, Sushant Prakash, Bradley Green, Shawn O’Banion, and Jun Xie. 2024. User-LLM：用用户嵌入实现高效的 LLM 上下文化. arXiv:2402.13598 [cs.CL]

[37] Zhaopeng Qiu, Xian Wu, Jingyue Gao, and Wei Fan. 2021. U-BERT：为改进推荐而预训练用户表示. In Proceedings of the AAAI Conference on Artificial Intelligence, Vol. 35. 4320–4327.

[38] Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, and Peter J Liu. 2020. 探索统一文本到文本 Transformer 的迁移学习极限. Journal of machine learning research 21, 140 (2020), 1–67.

[39] Shashank Rajput, Nikhil Mehta, Anima Singh, Raghunandan Hulikal Keshavan, Trung Vu, Lukasz Heldt, Lichan Hong, Yi Tay, Vinh Tran, Jonah Samost, Maciej Kula, Ed Chi, and Maheswaran Sathiamoorthy. 2023. 基于生成式检索的推荐系统. In Advances in Neural Information Processing Systems, A. Oh, T. Naumann, A. Globerson, K. Saenko, M. Hardt, and S. Levine (Eds.), Vol. 36. Curran Associates, Inc., 10299–10315. https://proceedings.neurips.cc/paper_files/paper/2023/file/20dcab0f14046a5c6b02b61da9f13229-Paper-Conference.pdf

[40] Ahmed Rashed, Shereen Elsayed, and Lars Schmidt-Thieme. 2022. 经由交叉注意力的上下文与属性感知序列推荐. In Proceedings of the 16th ACM Conference on Recommender Systems (Seattle, WA, USA) (RecSys ’22). Association for Computing Machinery, New York, NY, USA, 71–80. doi:10.1145/3523227.3546777

[41] Hideo Shimazu. 2002. ExpertClerk：一种用于在电子商务网店中开发售货员智能体的对话式基于案例推理工具. Artificial Intelligence Review 18, 3 (Dec. 2002), 223–244.

[42] Hakim Sidahmed, Sameer Ahuja, and Manoj Kumar Tiwari. 2022. 经由大语言模型（LLM）生成个性化推荐. (2022).

[43] Fei Sun, Jun Liu, Jian Wu, Changhua Pei, Xiao Lin, Wenwu Ou, and Peng Jiang. 2019. BERT4Rec：用来自 Transformer 的双向编码器表示做序列推荐. In CIKM ’19. Association for Computing Machinery, New York, NY, USA, 1441–1450.

[44] Gemini Team. 2024. Gemini 1.5：解锁跨越数百万词元上下文的多模态理解. arXiv:2403.05530 [cs.CL] https://arxiv.org/abs/2403.05530

[45] Gemma Team. 2024. Gemma：基于 Gemini 研究与技术的开放模型. arXiv:2403.08295 [cs.CL] https://arxiv.org/abs/2403.08295

[46] Cynthia A Thompson, Mehmet H Göker, and Pat Langley. 2004. 一个用于对话式推荐的个性化系统. J. Artif. Intell. Res. 21, 1 (March 2004), 393–428.

[47] Bowen Wang, Zhongkai Lin, Rui Zhang, Hong Yang, Yan Song, Dongyan Zhang, Tao Yu, Bing Zhou, and Qiang Yang. 2024. 为检索与推荐桥接语言与物品. arXiv preprint arXiv:2403.03952 (2024). arXiv:2403.03952 [cs.IR]

<!-- 原 PDF 第 11 页 -->

[48] Ga Wu, Kai Luo, Scott Sanner, and Harold Soh. 2019. 面向推荐系统的基于深度语言的批评. In RecSys ’19. Association for Computing Machinery, New York, NY, USA, 137–145.

[49] Yuhui Zhang, Hao Ding, Zeren Shui, Yifei Ma, James Zou, Anoop Deoras, and Hao Wang. 2021. 把语言模型作为推荐系统：评估与局限. (2021).

[50] Bowen Zheng, Yupeng Hou, Hongyu Lu, Yu Chen, Wayne Xin Zhao, and Ji-Rong Wen. 2024. 通过整合协同语义来适配大语言模型以用于推荐. In ICDE ’24. IEEE.

[51] Kun Zhou, Hui Wang, Wayne Xin Zhao, Yutao Zhu, Sirui Wang, Fuzheng Zhang, Zhongyuan Wang, and Ji-Rong Wen. 2020. S3-Rec：用互信息最大化做序列推荐的自监督学习. In Proceedings of the 29th ACM international conference on information knowledge management. 1893–1902.

[52] Kun Zhou, Yuanhang Zhou, Wayne Xin Zhao, Xiaoke Wang, and Ji-Rong Wen. 2020. 迈向主题引导的对话式推荐系统. arXiv:2010.04125 [cs.CL] https://arxiv.org/abs/2010.04125

[53] Yaochen Zhu, Liang Wu, Qi Guo, Liangjie Hong, and Jundong Li. 2024. 用于推荐系统的协同大语言模型. In The ACM Web Conference (WWW) ’24. Association for Computing Machinery, New York, NY, USA.

[54] Jianhuan Zhuo, Jianxun Lian, Lanling Xu, Ming Gong, Linjun Shou, Daxin Jiang, Xing Xie, and Yinliang Yue. 2022. Tiger：用于领域级零样本推荐的可迁移兴趣图嵌入. In Proceedings of the 31st ACM International Conference on Information & Knowledge Management. 2806–2816.

<!-- 译完 -->
