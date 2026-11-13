# AVATAR：通过对比推理优化 LLM 智能体的工具使用

- 原文件名：AvaTaR_arXiv2406.11200.pdf
- 原标题：AVATAR: Optimizing LLM Agents for Tool Usage via Contrastive Reasoning
- 中文标题：AVATAR：通过对比推理优化 LLM 智能体的工具使用
- 作者：Shirley Wu§、Shiyu Zhao§、Qian Huang§、Kexin Huang§、Michihiro Yasunaga§、Kaidi Cao§、Vassilis N. Ioannidis†、Karthik Subbian†、Jure Leskovec∗§、James Zou∗§（∗共同资深作者；§Department of Computer Science, Stanford University；†Amazon）
- 会议或 arXiv：arXiv:2406.11200v3 [cs.LG] 31 Oct 2024。附录含 NeurIPS Paper Checklist。
- 通信：{shirwu, jure, jamesz}@cs.stanford.edu

<!-- 原 PDF 第 1 页 -->

## 摘要

大语言模型（LLM）智能体已经展示出令人印象深刻的能力：利用外部工具和知识来提高准确率并减少幻觉。然而，开发使 LLM 智能体能有效使用这些工具和知识的提示技术，仍然是一项启发式的、劳动密集的任务。这里我们引入 AVATAR，一个新颖的自动化框架，它优化 LLM 智能体，使其有效利用所提供的工具，从而改善给定任务上的性能。在优化期间，我们设计一个比较器模块，通过在从训练数据中采样的正例与负例之间做对比推理，迭代地向 LLM 智能体提供有洞察力且全面的提示。我们在四个复杂的多模态检索数据集上展示 AVATAR，这些数据集包含文本、视觉和关系信息；并在三个一般问答（QA）数据集上展示。我们发现 AVATAR 在全部七项任务上始终优于最先进方法，在应用到新情形时表现出强泛化能力，并在检索数据集的 Hit@1 指标上取得平均 14% 的相对提升，在 QA 数据集上取得 13% 的相对提升。代码与数据集见 https://github.com/zou-group/avatar 。

## 1 引言

由大语言模型（LLM）驱动的自主智能体为复杂问题求解提供了巨大前景 [6, 39, 41, 55, 65]。这些智能体在推理 [46, 47, 54, 55] 和规划 [8, 13, 14, 62] 上展示出显著能力。此外，它们的功能通过外部工具得到扩展。这些工具提供对外部或私有数据以及专门操作的访问，例如用于与知识库和搜索引擎交互的 API。这些工具使智能体能够执行复杂任务，如多步问题求解和检索多样信息，这对复杂检索和问答（QA）是必要的 [13, 21, 26, 33, 38, 40, 48]。

尽管 LLM 智能体的能力令人期待，设计有效的提示来引导这些智能体走过面向真实世界问题求解的多阶段过程，仍然具有挑战。这一过程包括：（1）把复杂问题分解为带有更简单步骤的可执行计划；（2）策略性地使用所提供的工具来收集相关信息；最后（3）综合中间结果，产生连贯且准确的响应。每一步都需要大量人工努力，以及多次试错迭代来精炼提示。

当前方法主要聚焦于直接部署使用复杂的、由人设计的“巨型提示”的智能体 [18, 24, 55]，这需要大量人工试错。然而，这种手工设计的巨型提示也可能导致脆弱的实现和次优准确率（见图 2(a)），其中 ReAct 智能体 [55] 很容易对顾客关于特定产品的查询产生平凡且误导的答案。此外，把 LLM 用作优化器的现有研究 [4, 5, 45, 50, 56, 60, 64] 往往未能充分精炼那些用于增强工具整合与使用的复杂策略。缺乏这种策略性优化，会导致在复杂真实世界场景中智能体应用效果较差、且不可泛化。

**本工作：AVATAR。** 为应对这些挑战，我们引入 AVATAR，一个自动化框架，它优化智能体，以实现有效的工具利用和优秀的任务性能。具体而言，我们利用对比推理的关键洞见，构建一个比较器模块（“训练器”），以生成整体性的指令和提示（即计算一个稳健的“梯度”），来优化一个行动者 LLM。我们在知识库检索这一有挑战的任务上展示该框架。这些任务涉及复杂的多阶段过程和大量工具使用，以及一般 QA 任务。具体而言，AVATAR 包含两个阶段：

<!-- 原 PDF 第 2 页 -->

**图 1 见原 PDF。** 图 1：AVATAR 概览。AVATAR 由一个行动者 LLM 和一个比较器 LLM 组成。(a) 在优化期间，行动者通过利用所提供的工具生成动作来回答查询。然后比较器对比一组表现好的（正）查询和表现差的（负）查询，自动生成整体性提示，以教会行动者更有效的检索策略和工具使用（参见第 4 节）。(b) 在部署时，带有优化后提示或动作的行动者可以有效地用于回答新查询。图中文字包括：优化后的行动者与动作、工具、正负查询、（问题，答案）对、优化阶段、当前动作、比较器、采样数据、对比推理、初始指令、动作、用户、部署阶段、答案、查询、利用、行动者、关于工具使用和问题求解策略的更新指令、生成提示。

- **优化阶段。** 我们优化框架（图 1）的核心是一个比较器 LLM，它自动生成整体性提示，教会行动者 LLM 区分有效与无效的工具使用。比较器接收正数据样本和负数据样本——当前智能体分别表现好和表现差——以识别智能体所表现出的总体差距和系统性错误。与逐样本指令不同（逐样本指令很容易导致对个别数据点过拟合），通过把多个样本构造为一个“批次”，比较器可以抽出一个更稳健的“梯度”来“反向传播”给行动者。换句话说，比较器可以通过按批次的对比推理提供更有效、更自适应的提示，帮助智能体识别在求解有挑战的多阶段问题时的缺陷。遵循先前方法 [30, 41, 56, 63]，我们也维护一个记忆库，其中存放被选出的过去指令，以防止行动者 LLM 重复先前的错误。
- **部署阶段。** 优化阶段之后，可以选择表现最好的提示所对应的行动者用于测试实例。此外，在复杂检索任务中，通过我们的 AVATAR 框架做迭代优化，会把行动者更新为更有效、更可泛化的动作序列，从而在部署时能直接泛化到新的用户询问。在图 2(b) 中，优化后的行动者创造出三种新策略：1）通过抽取多方面属性来精确分解问题；2）通过一套精细且稳健的评分系统来有效使用工具；3）由学到的系数所决定的不同分数的策略性组合，以保证准确而全面的检索。

**实验评估。** 我们在四个检索数据集和三个 QA 数据集上做广泛实验。检索任务高度复杂，涉及多模态数据，包括文本、视觉和关系信息。AVATAR 始终优于最先进方法，在 Hit@1 指标上有实质性的 14% 提升。令人印象深刻的是，仅用 25 次迭代，AVATAR 就把 FLICKR30K-ENTITIES [35] 上的 Hit@1 从初始的 5.1% 提升到 28.6%，并把 STaRK-PRIME [49] 上的 Recall@20 从 30.3% 提升到 39.3%。对一般 QA 数据集，AVATAR 平均比最先进方法高出 13%。这些通过迭代更新提示所取得的改进，凸显了 AVATAR 优化智能体以应对复杂任务和有效工具使用的能力。我们的关键贡献是：

- 我们引入 AVATAR，一个新颖框架，它通过一个自动生成整体性提示的比较器模块，优化行动者以实现有效的工具利用。
- 我们在四个复杂检索任务和三个 QA 任务上展示 AVATAR，它在任务性能和泛化能力上显著优于现有智能体方法。
- 我们对优化期间行动者的演化提供全面分析，突出比较器如何自动提供有针对性的指令，从而改进并泛化行动者。

<!-- 原 PDF 第 3 页 -->

## 2 相关工作

**LLM 智能体。** 近期研究利用 LLM 出色的语言理解与推理能力 [1, 41, 47, 54, 55] 来完成下游任务。对需要增强能力的复杂任务，先前工作把 LLM 定位为能够与环境交互的智能体 [4, 6, 13, 18, 21, 26, 27, 40, 48, 55]，利用外部工具 [6, 28, 31, 33, 36, 38, 39, 66, 68]，并积累经验 [7, 61]。例如，ReAct [55] 以交错方式进行推理和行动，从维基百科检索信息以支持推理。

**用于检索的 LLM 智能体。** 先前研究通过预训练 [2, 9, 16, 57]、重排序 [12, 42] 和提示技术 [11, 18]，把 LLM 智能体应用到信息检索（IR）系统。在 IR 系统中，检索器模块直接影响下游任务的性能，例如检索增强生成 [20, 29, 30] 和知识密集型问答 [34, 52]。例如，EHRAgent [40] 面向电子健康记录问答，能够通过结构化的工具使用规划过程和交互式编码机制检索相关临床知识。然而，这些 LLM 智能体通常使用启发式（零样本）提示，或依赖少样本例子 [18, 25, 40, 55] 来做下游任务，缺乏关于如何生成有效检索策略和工具辅助动作的更有信息量的指导。

**智能体优化。** 在优化 LLM 智能体这一领域，先前工作通过微调或指令调优来修改 LLM 骨干的参数，以增强智能体能力 [3, 15, 19, 23, 32, 33, 37, 43, 51, 58, 59]，或通过迭代提示调优生成更好的提示 [11, 18, 45, 50, 56]。最近，Zhang 等人 [60] 根据执行历史迭代更新智能体的函数来做智能体训练。然而，这些方法没有明确考虑针对工具使用的优化，或对复杂多阶段任务的影响。此外，增强智能体的泛化能力 [10, 31, 44] 对真实世界应用是必要的，但受到的关注较少。在我们的工作中，我们聚焦于通过一种新颖的对比推理机制自动生成整体性指令，目标是有效的工具使用和智能体的泛化能力。与微调方法相比，AvaTaR 的优势在于只需要训练数据的一个小子集和工具描述，从而更可适应、计算上也更不密集。

## 3 问题形式化

**定义 1：工具。** 我们把工具或 API 定义为带有指定输入和输出变量的一组已实现函数。我们把抽象工具空间记为

$$
\mathcal{T} = \{f_k : I_{f_k} \to O_{f_k} \mid k = 1, 2, \ldots\},
$$

其中 $f_k$ 把输入 $I_{f_k}$ 映射到输出 $O_{f_k}$。例如，工具可以是用于经由搜索索引访问外部知识的 API、从文本或图像数据生成向量表示的编码器模型，或对一列类别输出概率的任务特定分类器。

**定义 2：智能体。** 一个 LLM 智能体定义为 $A : \mathcal{P} \to \alpha$，由言语提示控制，以生成完成任务所需的动作流。这里 $\alpha$ 表示动作序列 $[\alpha_1, \ldots, \alpha_L]$，其中每个动作由元组 $(f \in \mathcal{T},\ i \in I_f,\ o \in O_f)$ 定义，由一个工具函数、指定的输入，以及接收输出的指定变量组成。序列中的每个动作可以利用先前动作生成的输出，最终动作 $\alpha_L$ 给出该任务的结果。

<!-- 原 PDF 第 4 页 -->

**图 2 见原 PDF。** 图 2：AVATAR 与 ReAct 的比较。(a) ReAct 智能体表现出不完整的任务分解，并采用次优的工具组合，例如冗长的字符串匹配，导致任务性能差。(b) AVATAR 把任务分解为多个步骤，例如类型过滤和灵活的词元匹配。此外，它实现稳健的工具使用，并用优化阶段学到的参数做精确综合，从而在新查询上取得优秀性能。

图中示例查询包括：Q1：“Can you suggest any TUSA swim fins that has a split fin design for better propulsion?” ReAct 路径忽略品牌信息 “TUSA”，字符串匹配因没有完美匹配而全为零，相乘后仍全为零，导致平凡解。AVATAR 路径把查询解析为 brand: “TUSA”、type: “swim fins”、material: NA、features: “split fin design for better propulsion”，再用嵌入过滤类型、词元匹配品牌、用 LLM 推理验证功能，并以系数 $(0.43, 0.37, 0.20)$ 做加权和。另有小规模问答对示例，例如 Q2 关于 Sportsman Supply Inc. 的钓鱼坠，以及测试查询 “Looking for a durable 15-inch wide NFL car flag…”，真值实体 ID 为 [17, 105, 2517]。

**多步问题求解。** 真实世界问题本质上是复杂的，不能仅通过直截了当的解或简单的工具使用来有效解决。用 LLM 智能体求解真实世界问题可以结构化为一个多阶段过程：

- **问题分解：** 过程开始时，把一个复杂问题分解为以更简单步骤为特征的可执行计划。这种分解对于设定清晰目标、促进聚焦的问题求解至关重要。
- **工具辅助的子问题求解：** 在随后阶段，智能体策略性地利用已建立的工具空间 $\mathcal{T}$ 中的工具，为每一步收集解。这一阶段对于获取有效解决已分解问题的每个子问题所需的必要信息是关键的。

<!-- 原 PDF 第 5 页 -->

- **综合与响应形成：** 最后阶段把中间结果综合起来，构造精确响应。这种综合不仅组合数据，也可能通过试验和调整来精炼响应，保证解的准确性和相关性。

例如，检索任务本质上复杂且要求高。给定用户查询 $q$，检索任务旨在从知识库的实体空间中识别或生成相关实体 $E$ 的一个排序列表。每个查询关联一组真值答案，记为 $Y$，用于计算预测质量。具体而言，LLM 智能体需要：1）理解用户请求；2）利用所提供的工具，在可能包含多模态数据源的大知识空间中识别并分析相关信息；最后 3）整合全部收集到的信息，进行推理并生成准确响应。

**表 1：AVATAR 与主流智能体方法的关键差异。** AVATAR 展示出如下能力：1）在特定任务上自我改进；2）在整个优化过程中保留记忆；3）增强智能体的泛化能力；4）自主生成整体性的、高质量的提示以更好地使用工具。详见第 4 节。

| 方法 | 自我改进 | 记忆 | 泛化 | 整体性提示生成（关于工具使用） |
| --- | --- | --- | --- | --- |
| ReAct [55] | ✗ | ✗ | ✗ | ✗ |
| Self-refine [27] | ✔ | ✗ | ✗ | ✗ |
| Reflexion [41] | ✔ | ✔ | ✗ | ✗ |
| AVATAR（本文） | ✔ | ✔ | ✔ | ✔ |

## 4 我们的方法：为工具辅助的多步任务优化智能体

多阶段问题求解过程（第 3 节所述）中的每一步都需要有效的提示，以识别关键缺陷并改善任务性能。然而，精炼智能体的提示需要大量人工努力和多次试错迭代。

为此，我们引入一个自动化的新颖优化框架 AVATAR，它生成提示以改善智能体的工具使用和任务性能。在表 1 中，我们相对主流智能体框架 [27, 41, 55] 突出我们方法的四个关键方面。这里我们介绍 AVATAR 中的两个主要 LLM 组件：行动者 LLM（第 4.1 节）和比较器 LLM（第 4.2 节）。

### 4.1 行动者的构造与挑战

**行动者。** 如第 3 节所定义，行动者智能体负责基于初始指令/提示生成初始动作，并根据更新后的指令调整动作。具体而言，初始指令提供关于任务和可用工具的细节，工具可以用 Python 等编程语言来介绍。在优化期间，提示进一步纳入先前的动作序列和更新后的指令，以调整这些动作。行动者然后生成修订后的动作，其中可以包括通过编程语言进行的工具使用组合（代码生成），以及对工具如何被使用的自然语言解释。

**多步复杂任务中的挑战。** 更新指令的一种常见做法是利用某个特定实例的执行结果或性能数据，往往通过自我解释 [4, 27] 或自我反思 [41, 56] 之类的技术。然而，这一做法可能不适合涉及工具使用的复杂任务。复杂的多步任务包含多个相互作用的因素，它们影响总体性能，例如问题分解和工具选择。因此，为失败/负查询实例生成的指令往往范围狭窄，可能无法识别复杂解的全部组件中的缺陷。此外，某些工具组合对一种输入可能有效，但其有效性在不同场景中可能变化，应用到多样情形时可能导致性能下降。

<!-- 原 PDF 第 6 页 -->

**图 3 见原 PDF。** 图 3：优化期间的示意例子。最好彩色查看。比较器的任务是基于采样的正查询和负查询自动生成指令。然后比较器提供整体性指令，引导行动者改进查询分解、使用更好的工具，并纳入更全面的信息。图中查询例子包括 Santa Cruz 滑板板面、Top of the World 的可调节帽子、Football Fanatics 的汽车徽标，以及 Aminco 硅胶手环。更新后的动作把属性解析扩展为 brand、features、type、related_products，并用 CheckRequirementByLLM 与 GetRelatedProducts。

### 4.2 用比较器自动生成整体性指令

为应对这些挑战，我们构造一个比较器 LLM 来更新给行动者的指令。比较器的目标是识别贯穿结构化动作/解的系统性缺陷，而不是在一个采样实例上优化。

**步骤 1：构造正查询与负查询。** 为实现这一目标，如图 1 所示，比较器采样一组数据（问题–答案对），在这些查询上评估当前动作序列，并根据性能把它们分为表现好的（正）组和表现差的（负）组。具体而言，我们定义两个阈值 $\ell$ 和 $h$（其中 $0 < h \le \ell < 1$），分别作为构造正查询和负查询的上界与下界。评估指标（例如 Recall）值高于 $\ell$ 的查询被分类为正，低于 $h$ 的被分类为负。基于训练动态，可以考虑调整下界，以保证有足够数量的负样本可供选择。分类之后，我们用随机采样创建一个大小为 $b$ 的查询小批次，正查询与负查询等分（各 $b/2$），用于对比推理。

**步骤 2：通过对比推理生成指令。** 此后，比较器的任务是：基于两组查询的关键特征进行对比，把性能差距归因于复杂解内部的特定工具使用，并最终建议能够改善总体任务性能的一般性修改。比较器生成的指令随后被附加到初始提示上，以更新行动者。

**比较器的洞见/理由。** 为说明这些洞见，我们从深度神经网络训练作类比：极小的批次大小会在梯度估计中引入显著噪声，并在模型更新中带来高方差。通过采用分批训练策略，并把正查询和负查询采样为两个“小批次”，比较器可以抽出一个稳健的“梯度”来更新行动者。这一做法鼓励比较器对复杂动作序列生成更一般、更全面的指令，包括问题分解、子问题的解，以及最终综合。此外，由于对比推理直接针对解开与输入模式相关的性能差距，以及工具如何不同地处理这些模式，它在帮助比较器区分并选择要使用的工具方面特别有效。最后，通过在大量负查询上识别系统性缺陷，比较器生成的修改不仅针对个别样本，也针对多样的数据样本，从而增强对新情形的泛化。

<!-- 原 PDF 第 7 页 -->

**示意例子。** 图 3 展示一个例子：比较器对比正查询与负查询的模式，识别动作序列中工具使用的差异。它揭示：与正查询相比，负查询具有更复杂的产品描述、更隐晦的品牌提及，以及额外的相关产品提及。这些观察提示：1）问题分解不完整，未涉及详细产品特征等查询属性；2）使用嵌入相似度做品牌匹配可能不精确；3）结果中缺乏对相关产品的考虑。基于这些洞见，行动者更新其动作序列以处理这些子问题，并更有效地为该任务使用工具，例如用 LLM 验证工具替换嵌入工具。

### 4.3 后勤指令与记忆构造

**后勤指令。** 虽然来自比较器的指令旨在改善任务性能，我们纳入两类正交指令，以保证动作有效且能被高效执行。

- **有效性检查：** 这一指令在每个动作执行期间内部触发。它保证行动者动作的有效性，例如验证函数调用的正确使用。
- **超时错误：** 为防止可能使行动者停滞的低效动作序列，我们实现一个超时机制：若处理超过指定阈值就触发错误。这一错误促使行动者采用更高效的策略，例如消除冗余操作。

**记忆库。** 在优化期间，我们利用一个受人类决策过程启发的记忆库，遵循 Shinn 等人 [41]：人类通常通过分析当前情境并参考过去经验来处理当前问题。记忆库存放动作序列、来自比较器的指令，以及这些动作序列在一个小训练集（从正查询和负查询中采样）上的性能这三者的元组。为管理输入给行动者的上下文大小，我们只保留性能最好的前 5 个动作序列。这一记忆库使行动者既能从即时指令学习，也能从历史结果学习。

**部署。** 在部署时，我们可以应用优化后的指令，或者如图 1 所示，应用优化后的行动者/动作序列——其中包含有效的工具利用和问题求解策略——来回答查询或检索实体。在实验中，我们通过应用不同的部署策略来展示 AVATAR 的灵活性。

## 5 实验

**任务与评估。** 我们在下列数据集上做实验：

- 来自 STaRK [49] 和 FLICKR30K-ENTITIES [35] 的四个有挑战的检索数据集，以展示 AVATAR 处理复杂真实世界任务的能力（详见附录 A）。对检索数据集中的每个查询，任务是检索相关实体，例如知识图谱中的节点或知识库中的图像。在部署期间，我们把优化后的动作序列直接应用到测试查询。我们通过比较结果与数据集中真值答案的一致性来评估任务性能，使用 Hit@1、Hit@5、Recall@20 和平均倒数排名（MRR）作为指标。
- 三个问答（QA）基准：HotpotQA [53]、ArxivQA [22]、ToolQA [67]。任务是为问题提供自然语言答案。我们分别为三个基准采样 100、100 和 40 个训练查询，以及 100、100 和 60 个测试查询。在部署期间，行动者 LLM 使用优化后的指令来生成获得答案的动作序列。我们在 HotpotQA 上使用精确匹配（EM）分数，遵循先前方法。对 ArxivQA 和 ToolQA，我们使用 LLM 评判分数，以做更可靠的评估。

**基线。** 对知识检索任务，我们采用若干基于嵌入的检索器模型做评估，遵循 Wu 等人 [49]：稠密段落检索器（DPR），Karpukhin 等人 [17]；向量相似度检索方法 ada-002 和 multi-ada-002，使用来自 OpenAI 的 text-embedding-ada-002；以及一个关系感知模型 QAGNN [57]，用于 STaRK 基准。此外，我们纳入四个主流智能体框架以进一步丰富评估：

- ReAct [55] 以上下文内、交错的方式进行推理和行动，使 LLM 能交互地分析观察到的信息并执行动作。

<!-- 原 PDF 第 8 页 -->

**表 2：STaRK 基准上的检索性能（%）。** 最后一行是相对每一列中最佳指标值的相对提升。正文第 8 页称“表 3 表明……”，与此表题编号不一致，此处按表题记为表 2。

| 方法 | AMAZON Hit@1 | Hit@5 | R@20 | MRR | MAG Hit@1 | Hit@5 | R@20 | MRR | PRIME Hit@1 | Hit@5 | R@20 | MRR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DPR | 15.29 | 47.93 | 44.49 | 30.20 | 10.51 | 35.23 | 42.11 | 21.34 | 4.46 | 21.85 | 30.13 | 12.38 |
| QAGNN | 26.56 | 50.01 | 52.05 | 37.75 | 12.88 | 39.01 | 46.97 | 29.12 | 8.85 | 21.35 | 29.63 | 14.73 |
| ada-002 | 39.16 | 62.73 | 53.29 | 50.35 | 29.08 | 49.61 | 48.36 | 38.62 | 12.63 | 31.49 | 36.00 | 21.41 |
| multi-ada-002 | 40.07 | 64.98 | 55.12 | 51.55 | 25.92 | 50.43 | 50.80 | 36.94 | 15.10 | 33.56 | 38.05 | 23.49 |
| ReAct | 42.14 | 64.56 | 50.81 | 52.30 | 31.07 | 49.49 | 47.03 | 39.25 | 15.28 | 31.95 | 33.63 | 22.76 |
| Reflexion | 42.79 | 65.05 | 54.70 | 52.91 | 40.71 | 54.44 | 49.55 | 47.06 | 14.28 | 34.99 | 38.52 | 24.82 |
| AVATAR-C | 40.92 | 63.63 | 53.68 | 51.73 | 33.25 | 52.17 | 47.88 | 41.34 | 8.82 | 23.82 | 30.32 | 16.20 |
| AVATAR | 49.87 | 69.16 | 60.57 | 58.70 | 44.36 | 59.66 | 50.63 | 51.15 | 18.44 | 36.73 | 39.31 | 26.73 |
| 相对提升 | 16.6% | 6.3% | 9.9% | 12.2% | 9.6% | 2.1% | −0.3% | 8.7% | 20.7% | 5.0% | 2.1% | 7.7% |

- Reflexion [41] 对当前任务完成做自我反思，并把这些反思存在一个情节记忆缓冲区中，以增强后续试验中的决策。
- ExpeL [61] 从成功和失败的动作序列中抽取洞见，并在推断期间检索它们、纳入上下文。我们把 ExpeL 用于 QA 数据集；由于其在大规模检索任务上代价高，我们在一个采样的 STaRK-MAG 测试集上把它与 AVATAR 比较。
- Retroformer [56] 通过策略梯度学习一个回顾模型来强化 LLM 智能体并自动调优其提示。由于涉及额外训练，我们把 AVATAR 的性能与 Retroformer 在 HotpotQA 上报告的结果比较。

我们纳入一个消融模型 AVATAR-C，它从我们的优化流水线中移除比较器。这一比较旨在验证比较器的有效性。LLM 版本信息见附录 B。

**函数库。** 对知识检索任务，我们的函数库由二十八个函数组成，便于 LLM 智能体访问、操作知识信息并在其上推理。对 QA 任务，我们提供网络搜索工具，例如 Google 和 Arxiv 搜索 API。详见附录 E。我们在全部智能体方法上使用相同的函数库。

**一般流水线。** 对 AVATAR，我们把智能体优化固定的轮数，并选择性能最高的动作序列或指令。我们对全部数据集使用相同的初始提示结构、用于构造正负查询的指标 Recall@20 或 Accuracy，以及超参数（$\ell = h = 0.5$，$b = 20$）。

### 5.1 文本与关系检索任务

我们使用 STaRK 基准 [49] 中的 AMAZON、MAG 和 PRIME 数据集。这是一个大规模半结构化检索基准，整合文本与关系知识（详细描述见附录 A）。这里，待检索的实体定义为图结构中的节点，与每个实体关联的知识既包括文本描述也包括关系数据。我们使用 STaRK 基准的官方划分。

**要点 1：AVATAR 优于最先进模型。** 表中结果表明，AVATAR 在 STaRK 基准的全部指标上大幅优于 Reflexion 等领先模型。值得注意的是，AVATAR 在 Hit@1 上的平均提升为 15.6%，在 MRR 上为 9.5%。然而，ReAct 智能体不能基于指令来优化以改进工具使用，并且倾向于根据 LLM 的先验知识选择工具，这对给定任务可能不是最优的。我们观察到，ReAct 智能体在各种查询上应用相似的工具，即便有大量上下文内推理，也难以探索替代的工具使用。使用 GPT-4 Turbo 的智能体方法结果见附录 B，结论类似。与 ExpeL 的比较中，表 6 的结果表明它的表现与 ReAct 相似，大幅低于 AVATAR。

**要点 2：比较器极大地影响行动者的性能。** AVATAR 与其消融变体 AVATAR-C 的比较突出了比较器模块的显著优势。虽然 AVATAR-C 做有效性和超时检查，把比较器整合进 AVATAR 增加了一种全面的指令机制，对于识别改进智能体的清晰方向至关重要，这凸显了比较器在优化行动者中的关键作用。

<!-- 原 PDF 第 9 页 -->

**图 4 见原 PDF。** 图 4：AVATAR 智能体在 STaRK 上的优化动态。图中展示优化 AVATAR 期间验证性能（实线）及其移动平均（虚线）。

**图 5 见原 PDF（左为性能表，右为优化动态）。** FLICKR30K-ENTITIES 上的性能（左）与 AVATAR 的优化动态（右）。

| 方法 | Hit@1 | Hit@5 | R@20 | MRR |
| --- | --- | --- | --- | --- |
| clip-vit-large-patch14 | 37.2 | 56.4 | 72.8 | 46.3 |
| ReAct (claude3) | 38.8 | 54.8 | 71.6 | 46.1 |
| Reflexion (claude3) | 28.4 | 53.2 | 75.2 | 41.2 |
| AVATAR-C (claude3) | 28.8 | 53.2 | 78.4 | 40.0 |
| AVATAR (claude3) | 42.4 | 63.0 | 79.2 | 52.3 |
| 相对提升 | 9.2% | 11.7% | 5.3% | 13.0% |

**要点 3：AVATAR 在优化期间有效改进智能体。** 图 4 展示优化期间智能体在验证集上的性能。令人印象深刻的是，AVATAR 智能体显示出显著的性能提升，例如在 AMAZON 上从 35% 到 75%，在 MAG 上从 20% 到 78%。这一证据有力支持我们的比较器所生成指令的有效性。此外，我们的记忆库存放过去表现最好的动作，鼓励 AVATAR 智能体在优化过程结束时逐渐收敛。

**要点 4：AVATAR 可以泛化到真实世界任务。** 比较器生成针对成组检索查询的指令，促进对新查询的可泛化修改。我们通过把优化后的动作应用到 STaRK 基准中由人生成的留出查询来验证这一能力。这些查询与用于优化我们智能体的训练数据明显不同。附录 B 表 5 的结果表明，AVATAR 显著优于其他模型，在 Hit@1 上取得平均 20.9% 的提升。此外，在附录 B 的另一项研究中，我们评估 AVATAR 对超参数 $h$ 和 $\ell$ 的稳健性，表明它在不同参数值下保持稳定的性能和泛化。

### 5.2 图像检索任务

我们进一步在 FLICKR30K ENTITIES [35] 上实验。这是一个图像检索数据集，含 3 万张带标注边界框和描述短语的图像（附录 A）。在上表中，AVATAR 再次显示出显著改进。相比之下，Reflexion 智能体苦于“过拟合”：它们很容易被特定图像数据误导，导致不适当的动作（例如试图从没有帽子的图像中“抽取帽子的颜色”）。AVATAR 通过按批次的对比推理有效避免这类陷阱，从而提供更广的视角。

**要点 5：AVATAR 生成令人印象深刻且可泛化的动作。** AVATAR 智能体的最终动作见原 PDF 第 9 页 “Figure ??”（图号抽取为问号，见原 PDF 第 9 页），并在图 8（附录 B）中详述，达到先进性能。值得注意的是，AVATAR 熟练地管理输入查询，并利用逆文档频率（IDF）分数来精炼短语匹配，最终综合出准确答案。除使用现有工具外，AVATAR 智能体还能发展高层工具，例如基于 IDF 的再加权，这提示动态工具库和增强的工具生成是一个有前景的方向。

**要点 6：优化期间涌现的行为。** 在图 6 中，我们给出说明行动者与比较器之间关键交互的具体案例。在每个实例中，比较器识别关键缺陷，包括信息遗漏、无效的工具使用，以及对不同分数的次优综合。指令随后促使行动者增强检索策略、工具选择和精确的分数组合。此外，对工具使用的频繁提及凸显了比较器在优化期间对工具利用的聚焦考察。

<!-- 原 PDF 第 10 页 -->

**图 6 见原 PDF。** 图 6：来自比较器的代表性指令类型。我们给出三种情形，比较器引导行动者走向：（1）面向多步问题求解的更好分而治之策略；（2）对好与坏的工具使用/组合做更合理的区分；（3）调整权重以生成最终答案。我们记录 FLICKR30K-ENTITIES 上 25 次迭代中每种指令类型的出现次数 $X$，以 $(X/25)$ 表示。三类分别为：改进的分而治之（4/25）、合理的工具区分（16/25）、数值参数学习（5/25）。

图中文字大意：动作在提及物体（如动物和人：dog、man、woman）的查询上表现好，但在更抽象或聚焦风景的查询（如 people relaxing on grass、person jumping near a car）上吃力。建议提高 visual_weight 以更好捕捉整体场景元素。参数从 `{phrase_weight: 0.5, visual_weight: 0.5}` 变为 `{phrase_weight: 0.4, visual_weight: 0.6}`。另一情形建议把形容词、复合名词、动词短语分开抽取，模式为 NP、CP、VP。第三情形把 VqaByLLM 的冗长位置描述换成 GetVisualAttributesByLLM 的简洁属性，并把 StringMatch 换成 TokenMatchScore。

**表 3：三个 QA 基准上的性能（%）。** 最后一行是相对每一列中最佳指标值的相对提升。

| 方法 | HOTPOTQA | ARXIVQA | TOOLQA SCIREX-EASY | SCIREX-HARD | AGENDA-EASY | AGENDA-HARD |
| --- | --- | --- | --- | --- | --- | --- |
| CoT | 28.0% | 58.0% | 1.7% | 0.0% | 0.0% | 0.0% |
| ReAct | 40.0% | 72.0% | 31.7% | 17.5% | 38.3% | 3.33% |
| Reflexion | 46.0% | 77.0% | 28.3% | 13.3% | 30.0% | 3.33% |
| ExpeL | 39.0% | 73.0% | 36.7% | 14.5% | 56.6% | 1.67% |
| Retroformer（#retry=1） | 51.0% | — | — | — | — | — |
| AVATAR-C | 41.0% | 73.0% | 31.7% | 13.3% | 31.7% | 1.67% |
| AVATAR | 53.0% | 84.0% | 37.5% | 23.3% | 60.0% | 4.17% |
| 相对提升 | 3.92% | 9.09% | 2.18% | 33.1% | 5.82% | 25.0% |

### 5.3 问答任务

最后，我们把 AVATAR 应用到三个广泛使用的 QA 基准。对 ToolQA，我们在两个不同领域上测试 AVATAR 和基线：SciREX，聚焦于从全长机器学习论文中抽取信息；以及 Agenda，涉及与个人日程相关的问题。两个数据集都有容易和困难版本。

**要点 7：AVATAR 通过提供更好的上下文理解而在 QA 任务上胜出。** 表 3 表明，AVATAR 在全部三个 QA 数据集上始终优于最先进方法，在 TOOLQA 上结果尤其强。在聚焦于从长科学论文中抽取复杂信息的 SCIREX-HARD 上，AVATAR 显示出 33.1% 的提升；在 AGENDA-HARD 上，它取得 25.0% 的相对增益。这些改进归因于 AVATAR 生成优化提示的能力，这些提示帮助智能体更好地理解问题的更广模式和上下文，从而得到更准确的答案，并在从简单到复杂的问题类型上改善泛化。

## 6 结论与未来工作

在本研究中，我们引入 AVATAR，一个新颖框架，它自动化 LLM 智能体的优化，以增强多步问题中的工具利用，聚焦于复杂检索和 QA 任务。AVATAR 在七个多样数据集上展示出显著改进。这一成功在很大程度上可归因于比较器模块，它通过迭代生成整体性的、策略性的提示来有效精炼智能体性能。比较器的一项关键创新是使用带批次采样的对比推理，使它能识别系统性缺陷，并为跨多样场景的全面智能体改进抽出稳健的“梯度”。虽然我们从 AVATAR 观察到实质性进展，我们在附录 D 中讨论其关于可扩展性等的局限。未来工作可以探索把这一方法论扩展到其他有挑战的智能体任务、视觉推理任务和更动态的环境，或设计更好的记忆库，以动态存储来自过去训练的知识和经验。

<!-- 原 PDF 第 11 页 -->

## 致谢

我们感谢 Zou 和 Leskovec 实验室的成员对讨论以及对手稿提供反馈。我们也感谢下列资助：DARPA，编号 N660011924033（MCS）；NSF，编号 OAC-1835598（CINES）、CCF-1918940（Expeditions）、DMS-2327709（IHBEM）；Stanford Data Applications Initiative、Wu Tsai Neurosciences Institute、Stanford Institute for Human-Centered AI、Chan Zuckerberg Initiative、Amazon、Genentech、GSK、Hitachi、SAP 和 UCB。内容完全由作者负责，不一定代表资助实体的官方观点。

## 参考文献

[1] Maciej Besta, Nils Blach, Ales Kubicek, Robert Gerstenberger, Lukas Gianinazzi, Joanna Gajda, Tomasz Lehmann, Michal Podstawski, Hubert Niewiadomski, Piotr Nyczyk, and Torsten Hoefler. [n. d.]. 思维图：用大语言模型求解精细问题. arXiv:2308.09687

[2] Sebastian Borgeaud, Arthur Mensch, Jordan Hoffmann, Trevor Cai, Eliza Rutherford, Katie Millican, George van den Driessche, Jean-Baptiste Lespiau, Bogdan Damoc, Aidan Clark, Diego de Las Casas, Aurelia Guy, Jacob Menick, Roman Ring, Tom Hennigan, Saffron Huang, Loren Maggiore, Chris Jones, Albin Cassirer, Andy Brock, Michela Paganini, Geoffrey Irving, Oriol Vinyals, Simon Osindero, Karen Simonyan, Jack W. Rae, Erich Elsen, and Laurent Sifre. 2022. 通过从万亿词元中检索来改进语言模型. In ICML.

[3] Baian Chen, Chang Shu, Ehsan Shareghi, Nigel Collier, Karthik Narasimhan, and Shunyu Yao. 2023. FireAct：走向语言智能体微调. arXiv:2310.05915

[4] Xinyun Chen, Maxwell Lin, Nathanael Schärli, and Denny Zhou. 2023. 教大语言模型自我调试. (2023).

[5] Mingkai Deng, Jianyu Wang, Cheng-Ping Hsieh, Yihan Wang, Han Guo, Tianmin Shu, Meng Song, Eric P. Xing, and Zhiting Hu. 2022. RLPrompt：用强化学习优化离散文本提示. In EMNLP. ACL.

[6] Zane Durante, Qiuyuan Huang, Naoki Wake, Ran Gong, Jae Sung Park, Bidipta Sarkar, Rohan Taori, Yusuke Noda, Demetri Terzopoulos, Yejin Choi, Katsushi Ikeuchi, Hoi Vo, Li Fei-Fei, and Jianfeng Gao. [n. d.]. 智能体 AI：纵览多模态交互的地平线. arXiv:2401.03568

[7] Yao Fu, Dong-Ki Kim, Jaekyeom Kim, Sungryull Sohn, Lajanugen Logeswaran, Kyunghoon Bae, and Honglak Lee. 2024. AutoGuide：为大语言模型智能体自动生成并选择状态感知指南. CoRR abs/2403.08978 (2024). arXiv:2403.08978

[8] Ran Gong, Qiuyuan Huang, Xiaojian Ma, Hoi Vo, Zane Durante, Yusuke Noda, Zilong Zheng, Song-Chun Zhu, Demetri Terzopoulos, Li Fei-Fei, and Jianfeng Gao. [n. d.]. MindAgent：涌现的游戏交互. arXiv:2309.09971

[9] Kelvin Guu, Kenton Lee, Zora Tung, Panupong Pasupat, and Mingwei Chang. 2020. 检索增强的语言模型预训练. In ICML. PMLR.

[10] Simon Jerome Han, Keith J. Ransom, Andrew Perfors, and Charles Kemp. 2024. 人类与大语言模型中的归纳推理. Cogn. Syst. Res. (2024).

[11] Xiaoxin He, Yijun Tian, Yifei Sun, Nitesh V. Chawla, Thomas Laurent, Yann LeCun, Xavier Bresson, and Bryan Hooi. 2024. G-Retriever：面向文本图理解与问答的检索增强生成. arXiv:2402.07630

[12] Yupeng Hou, Junjie Zhang, Zihan Lin, Hongyu Lu, Ruobing Xie, Julian McAuley, and Wayne Xin Zhao. 2023. 大语言模型是推荐系统的零样本排序器. arXiv:2305.08845 (2023).

<!-- 原 PDF 第 12 页 -->

[13] Wenlong Huang, Pieter Abbeel, Deepak Pathak, and Igor Mordatch. 2022. 语言模型作为零样本规划器：为具身智能体抽取可执行知识. In ICML.

[14] Wenlong Huang, Fei Xia, Ted Xiao, Harris Chan, Jacky Liang, Pete Florence, Andy Zeng, Jonathan Tompson, Igor Mordatch, Yevgen Chebotar, Pierre Sermanet, Tomas Jackson, Noah Brown, Linda Luu, Sergey Levine, Karol Hausman, and Brian Ichter. 2022. 内心独白：通过用语言模型规划进行具身推理. In CoRL.

[15] Yue Huang, Jiawen Shi, Yuan Li, Chenrui Fan, Siyuan Wu, Qihui Zhang, Yixin Liu, Pan Zhou, Yao Wan, Neil Zhenqiang Gong, and Lichao Sun. 2024. 大语言模型的 MetaTool 基准：决定是否使用工具以及使用哪一个. ICLR (2024).

[16] Vassilis N Ioannidis, Xiang Song, Da Zheng, Houyu Zhang, Jun Ma, Yi Xu, Belinda Zeng, Trishul Chilimbi, and George Karypis. 2022. 语言与图神经网络模型的高效有效训练. arXiv preprint arXiv:2206.10781 (2022).

[17] Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick S. H. Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, and Wen-tau Yih. 2020. 面向开放域问答的稠密段落检索. In EMNLP.

[18] Omar Khattab, Keshav Santhanam, Xiang Lisa Li, David Hall, Percy Liang, Christopher Potts, and Matei Zaharia. 2023. 演示–搜索–预测：为知识密集型 NLP 组合检索与语言模型. arXiv:2212.14024 [cs.CL]

[19] Hung Le, Yue Wang, Akhilesh Deepak Gotmare, Silvio Savarese, and Steven Chu-Hong Hoi. 2022. CodeRL：通过预训练模型与深度强化学习掌握代码生成. In NeurIPS.

[20] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen tau Yih, Tim Rocktäschel, Sebastian Riedel, and Douwe Kiela. 2021. 面向知识密集型 NLP 任务的检索增强生成. arXiv:2005.11401 [cs.CL]

[21] Guohao Li, Hasan Abed Al Kader Hammoud, Hani Itani, Dmitrii Khizbullin, and Bernard Ghanem. 2023. CAMEL：用于大规模语言模型社会之“心智”探索的交流智能体. abs/2303.17760 (2023). arXiv:2303.17760

[22] Lei Li, Yuqi Wang, Runxin Xu, Peiyi Wang, Xiachong Feng, Lingpeng Kong, and Qi Liu. 2024. 多模态 ArXiv：一个用于改进大视觉–语言模型科学理解的数据集. In ACL.

[23] Minghao Li, Yingxiu Zhao, Bowen Yu, Feifan Song, Hangyu Li, Haiyang Yu, Zhoujun Li, Fei Huang, and Yongbin Li. 2023. API-Bank：工具增强 LLM 的综合基准. In EMNLP. Association for Computational Linguistics.

[24] Xiao Liu, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, Hangliang Ding, Kaiwen Men, Kejuan Yang, Shudan Zhang, Xiang Deng, Aohan Zeng, Zhengxiao Du, Chenhui Zhang, Sheng Shen, Tianjun Zhang, Yu Su, Huan Sun, Minlie Huang, Yuxiao Dong, and Jie Tang. 2023. AgentBench：把 LLM 作为智能体来评估. arXiv:2308.03688

[25] Robert Lo, Abishek Sridhar, Frank Xu, Hao Zhu, and Shuyan Zhou. 2023. 分层提示协助大语言模型做网页导航. In Findings of the Association for Computational Linguistics: EMNLP 2023.

[26] Pan Lu, Baolin Peng, Hao Cheng, Michel Galley, Kai-Wei Chang, Ying Nian Wu, Song-Chun Zhu, and Jianfeng Gao. 2023. Chameleon：用大语言模型做即插即用的组合推理. In NeurIPS.

[27] Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, Shashank Gupta, Bodhisattwa Prasad Majumder, Katherine Hermann, Sean Welleck, Amir Yazdanbakhsh, and Peter Clark. 2023. Self-Refine：带自我反馈的迭代精炼. In NeurIPS.

<!-- 原 PDF 第 13 页 -->

[28] Reiichiro Nakano, Jacob Hilton, Suchir Balaji, Jeff Wu, Ouyang Long, Christina Kim, Christopher Hesse, Shantanu Jain, Vineet Kosaraju, William Saunders, Xu Jiang, Karl Cobbe, Tyna Eloundou, Gretchen Krueger, Kevin Button, Matthew Knight, Benjamin Chess, and John Schulman. 2021. WebGPT：带人类反馈的浏览器辅助问答. ArXiv (2021).

[29] Reiichiro Nakano, Jacob Hilton, Suchir Balaji, Jeff Wu, Long Ouyang, Christina Kim, Christopher Hesse, Shantanu Jain, Vineet Kosaraju, William Saunders, Xu Jiang, Karl Cobbe, Tyna Eloundou, Gretchen Krueger, Kevin Button, Matthew Knight, Benjamin Chess, and John Schulman. [n. d.]. WebGPT：带人类反馈的浏览器辅助问答. arXiv:2112.09332

[30] Charles Packer, Vivian Fang, Shishir G. Patil, Kevin Lin, Sarah Wooders, and Joseph E. Gonzalez. 2023. MemGPT：走向作为操作系统的 LLM. 2310.08560 (2023).

[31] Bhargavi Paranjape, Scott Lundberg, Sameer Singh, Hannaneh Hajishirzi, Luke Zettlemoyer, and Marco Tulio Ribeiro. 2023. ART：大语言模型的自动多步推理与工具使用. arXiv:2303.09014 (2023).

[32] Aaron Parisi, Yao Zhao, and Noah Fiedel. 2022. TALM：工具增强语言模型. arXiv:2205.12255

[33] Shishir G. Patil, Tianjun Zhang, Xin Wang, and Joseph E. Gonzalez. 2023. Gorilla：连接海量 API 的大语言模型. CoRR (2023). arXiv:2305.15334

[34] Baolin Peng, Michel Galley, Pengcheng He, Hao Cheng, Yujia Xie, Yu Hu, Qiuyuan Huang, Lars Liden, Zhou Yu, Weizhu Chen, and Jianfeng Gao. 2023. 检查你的事实并再试一次：用外部知识和自动反馈改进大语言模型. arxiv 2302.12813 (2023).

[35] Bryan A. Plummer, Liwei Wang, Chris M. Cervantes, Juan C. Caicedo, Julia Hockenmaier, and Svetlana Lazebnik. 2017. Flickr30k Entities：为更丰富的图像到句子模型收集区域到短语的对应. Int. J. Comput. Vis. (2017).

[36] Yujia Qin, Zihan Cai, Dian Jin, Lan Yan, Shihao Liang, Kunlun Zhu, Yankai Lin, Xu Han, Ning Ding, Huadong Wang, Ruobing Xie, Fanchao Qi, Zhiyuan Liu, Maosong Sun, and Jie Zhou. 2023. WebCPM：面向中文长形式问答的交互式网页搜索. In Proceedings of ACL 2023. Association for Computational Linguistics.

[37] Yujia Qin, Shihao Liang, Yining Ye, Kunlun Zhu, Lan Yan, Yaxi Lu, Yankai Lin, Xin Cong, Xiangru Tang, Bill Qian, Sihan Zhao, Runchu Tian, Ruobing Xie, Jie Zhou, Mark Gerstein, Dahai Li, Zhiyuan Liu, and Maosong Sun. 2023. ToolLLM：促使大语言模型掌握 16000 多个真实世界 API. arxiv 2307.16789 (2023).

[38] Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Eric Hambro, Luke Zettlemoyer, Nicola Cancedda, and Thomas Scialom. 2023. Toolformer：语言模型可以教会自己使用工具. In NeurIPS.

[39] Yongliang Shen, Kaitao Song, Xu Tan, Dongsheng Li, Weiming Lu, and Yueting Zhuang. 2023. HuggingGPT：用 ChatGPT 及其在 Hugging Face 中的朋友解决 AI 任务. In NeurIPS.

[40] Wenqi Shi, Ran Xu, Yuchen Zhuang, Yue Yu, Jieyu Zhang, Hang Wu, Yuanda Zhu, Joyce Ho, Carl Yang, and May D Wang. 2024. EHRAgent：代码使大语言模型能够在电子健康记录上做复杂表格推理. arXiv:2401.07128 (2024).

[41] Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. 2023. Reflexion：带言语强化学习的语言智能体. In NeurIPS.

[42] Weiwei Sun, Lingyong Yan, Xinyu Ma, Shuaiqiang Wang, Pengjie Ren, Zhumin Chen, Dawei Yin, and Zhaochun Ren. [n. d.]. ChatGPT 擅长搜索吗？把大语言模型作为重排序智能体来考察. In EMNLP, year = 2023.

<!-- 原 PDF 第 14 页 -->

[43] Qiaoyu Tang, Ziliang Deng, Hongyu Lin, Xianpei Han, Qiao Liang, and Le Sun. 2023. ToolAlpaca：用 3000 个模拟案例为语言模型做泛化工具学习. arXiv:2306.05301

[44] Ruocheng Wang, Eric Zelikman, Gabriel Poesia, Yewen Pu, Nick Haber, and Noah D. Goodman. 2024. 假设搜索：用语言模型做归纳推理. ICLR (2024).

[45] Xinyuan Wang, Chenxi Li, Zhen Wang, Fan Bai, Haotian Luo, Jiayou Zhang, Nebojsa Jojic, Eric P. Xing, and Zhiting Hu. 2023. PromptAgent：用语言模型做战略规划，使专家级提示优化成为可能. arXiv:2310.16427

[46] Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V. Le, Ed H. Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou. 2023. 自一致性改进语言模型中的思维链推理. In ICLR.

[47] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed H. Chi, Quoc V. Le, and Denny Zhou. 2022. 思维链提示激发大语言模型中的推理. In NeurIPS.

[48] Qingyun Wu, Gagan Bansal, Jieyu Zhang, Yiran Wu, Shaokun Zhang, Erkang Zhu, Beibin Li, Li Jiang, Xiaoyun Zhang, and Chi Wang. 2023. AutoGen：通过多智能体对话框架使下一代 LLM 应用成为可能. arXiv:2308.08155

[49] Shirley Wu, Shiyu Zhao, Michihiro Yasunaga, Kexin Huang, Kaidi Cao, Qian Huang, Vassilis N. Ioannidis, Karthik Subbian, James Zou, and Jure Leskovec. 2024. STaRK：在文本与关系知识库上基准测试 LLM 检索. arXiv:2404.13207

[50] Chengrun Yang, Xuezhi Wang, Yifeng Lu, Hanxiao Liu, Quoc V. Le, Denny Zhou, and Xinyun Chen. 2024. 大语言模型作为优化器. (2024).

[51] Rui Yang, Lin Song, Yanwei Li, Sijie Zhao, Yixiao Ge, Xiu Li, and Ying Shan. 2023. GPT4Tools：通过自我指令教大语言模型使用工具. In NeurIPS.

[52] Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W Cohen, Ruslan Salakhutdinov, and Christopher D Manning. 2018. HotpotQA：一个多样、可解释的多跳问答数据集. EMNLP (2018).

[53] Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W. Cohen, Ruslan Salakhutdinov, and Christopher D. Manning. 2018. HotpotQA：一个多样、可解释的多跳问答数据集. In EMNLP.

[54] Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Tom Griffiths, Yuan Cao, and Karthik Narasimhan. 2023. 思维树：用大语言模型做审慎的问题求解. In NeurIPS.

[55] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik R. Narasimhan, and Yuan Cao. 2023. ReAct：在语言模型中协同推理与行动. In ICLR.

[56] Weiran Yao, Shelby Heinecke, Juan Carlos Niebles, Zhiwei Liu, Yihao Feng, Le Xue, Rithesh Murthy, Zeyuan Chen, Jianguo Zhang, Devansh Arpit, Ran Xu, Phil Mui, Huan Wang, Caiming Xiong, and Silvio Savarese. 2024. Retroformer：带策略梯度优化的回顾式大语言智能体. (2024).

[57] Michihiro Yasunaga, Hongyu Ren, Antoine Bosselut, Percy Liang, and Jure Leskovec. 2021. QA-GNN：用语言模型和知识图谱为问答做推理.

[58] Junjie Ye, Guanyu Li, Songyang Gao, Caishuang Huang, Yilong Wu, Sixian Li, Xiaoran Fan, Shihan Dou, Qi Zhang, Tao Gui, and Xuanjing Huang. 2024. ToolEyes：真实世界场景中大语言模型工具学习能力的细粒度评估. arXiv:2401.00741 (2024).

[59] Aohan Zeng, Mingdao Liu, Rui Lu, Bowen Wang, Xiao Liu, Yuxiao Dong, and Jie Tang. [n. d.]. AgentTuning：为 LLM 启用泛化的智能体能力. arXiv:2310.12823

<!-- 原 PDF 第 15 页 -->

[60] Shaokun Zhang, Jieyu Zhang, Jiale Liu, Linxin Song, Chi Wang, Ranjay Krishna, and Qingyun Wu. 2024. 在不修改语言模型的情况下训练语言智能体. arXiv:2402.11359

[61] Andrew Zhao, Daniel Huang, Quentin Xu, Matthieu Lin, Yong-Jin Liu, and Gao Huang. 2024. ExpeL：LLM 智能体是经验学习者. In AAAI.

[62] Wenqing Zheng, SP Sharan, Ajay Kumar Jaiswal, Kevin Wang, Yihan Xi, Dejia Xu, and Zhangyang Wang. 2023. 先大纲后细节：句法引导的由粗到细代码生成. ICML (2023).

[63] Wanjun Zhong, Lianghong Guo, Qiqi Gao, He Ye, and Yanlin Wang. 2024. MemoryBank：用长期记忆增强大语言模型. In AAAI.

[64] Yongchao Zhou, Andrei Ioan Muresanu, Ziwen Han, Keiran Paster, Silviu Pitis, Harris Chan, and Jimmy Ba. 2023. 大语言模型是人类水平的提示工程师. In ICLR.

[65] Yutao Zhu, Huaying Yuan, Shuting Wang, Jiongnan Liu, Wenhan Liu, Chenlong Deng, Zhicheng Dou, and Ji-Rong Wen. 2023. 用于信息检索的大语言模型：综述. arXiv:2308.07107 (2023).

[66] Yuchen Zhuang, Yue Yu, Kuan Wang, Haotian Sun, and Chao Zhang. 2023. ToolQA：一个用外部工具做 LLM 问答的数据集. In NeurIPS.

[67] Yuchen Zhuang, Yue Yu, Kuan Wang, Haotian Sun, and Chao Zhang. 2023. ToolQA：一个用外部工具做 LLM 问答的数据集. arXiv:2306.13304

[68] Chang Zong, Yuchen Yan, Weiming Lu, Eliot Huang, Jian Shao, and Yueting Zhuang. [n. d.]. Triad：一个利用多角色 LLM 智能体来求解知识库问答的框架. arXiv:2402.14320

<!-- 原 PDF 第 16 页 -->

## A 检索任务

**STaRK。** 在 STaRK 基准上，我们得到一个关系–文本知识库，基于知识图谱 $G = (V, E)$ 和一组自由文本文档 $D$。我们把大小为 $n$ 的关系–文本知识库表示为

$$
E = \{(v_i, d_i, g_i)\}_{i=1}^{n},
$$

其中 $v_i \in V$ 表示知识图谱上的一个节点，$d_i \in D$ 是与该节点相关的文本文档，$g_i$ 是 $G$ 中包含 $v_i$ 的连通分量。

STaRK 中的查询集 $Q$ 由 $G$ 和 $D$ 共同导出，其中每个 $q_i \in Q$ 包含基于 $d_i$ 和 $g_i$ 的要求。答案集 $A_i$（包含 $v_i$）是同时满足关系和文本要求的一组节点。STaRK 上的任务定义如下：给定由关系和文本信息组成的知识库 $E$，以及文本查询 $q_i$，输出是一组节点 $A_i$，使得 $\forall a_i \in A_i$，$a_i$ 满足知识图谱中的关系要求和其文本文档中的文本要求。

**FLICKR30K ENTITIES。** 在 FLICKR30K ENTITIES 数据集上，我们得到一个图像–文本知识库。我们把大小为 $n$ 的图像–文本知识库记为

$$
E = \{(v_i, q_i, T_i)\}_{i=1}^{n}.
$$

样本 $i$ 由图像 $v_i$、其描述性说明文字 $q_i$，以及实体边界框信息 $T_i$ 组成。具体而言，$T_i = \{(c_{ij}, p_{ij})\}_{j=1}^{b_i}$，其中 $b_i$ 表示图像 $i$ 中标注的边界框数量，$c_{ij}$ 是第 $j$ 个边界框的坐标，$p_{ij}$ 描述对应边界框中的实体。

在我们的任务中，图像说明文字充当文本查询；因此，数据集中的全部 $q_i$ 对智能体不可访问，以防止信息泄漏。然而，智能体可以访问 $v_i$ 和 $T_i$，以充分利用视觉和语言信息。FLICKR30K ENTITIES 上的任务定义如下：给定带有图像和边界框信息的知识库 $E$，以及文本查询 $q_i$，输出是一张图像 $v_i$，它满足图像中的视觉要求以及对应边界框 $T_i$ 中的文本要求。

**图 7 见原 PDF。** 图 7：FLICKR30K ENTITIES 上的示例数据。每个实体是一张图像，连同其图像块以及与图像块关联的短语。图中短语包括 Orange hat、An orange hat、Glasses、Rainbow flags、A group of youth、City street、Wedding attire、A bride、Wedding cake、A table，以及 N/A（masked）。

## B 实验细节与附加结果

### B.1 实验设定

智能体方法的 LLM 版本。

- 对知识检索任务，我们在正文中默认使用 claude-3-opus 作为骨干 LLM，并因篇幅限制在附录 B 中报告使用 gpt-4-turbo 的结果。
- 对 QA 任务，我们在 HotpotQA 上使用 gpt-4，以便与先前方法公平比较，并在另外两个 QA 数据集上使用 gpt-4o。

<!-- 原 PDF 第 17 页 -->

**表 4：STaRK 基准上的检索性能（%）。** 最后一行是相对基线中最佳指标值的相对提升。表中最后一方法行在原 PDF 写为 AIR (gpt4)。

| 方法 | AMAZON Hit@1 | Hit@5 | R@20 | MRR | MAG Hit@1 | Hit@5 | R@20 | MRR | PRIME Hit@1 | Hit@5 | R@20 | MRR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DPR (roberta) | 15.29 | 47.93 | 44.49 | 30.20 | 10.51 | 35.23 | 42.11 | 21.34 | 4.46 | 21.85 | 30.13 | 12.38 |
| QAGNN (roberta) | 26.56 | 50.01 | 52.05 | 37.75 | 12.88 | 39.01 | 46.97 | 29.12 | 8.85 | 21.35 | 29.63 | 14.73 |
| ada-002 | 39.16 | 62.73 | 53.29 | 50.35 | 29.08 | 49.61 | 48.36 | 38.62 | 12.63 | 31.49 | 36.00 | 21.41 |
| multi-ada-002 | 40.07 | 64.98 | 55.12 | 51.55 | 25.92 | 50.43 | 50.80 | 36.94 | 15.10 | 33.56 | 38.05 | 23.49 |
| ReAct (gpt4) | 38.83 | 62.50 | 50.39 | 49.16 | 23.50 | 46.50 | 43.11 | 33.91 | 10.83 | 30.83 | 32.16 | 19.39 |
| Reflexion (gpt4) | 41.45 | 64.83 | 53.98 | 52.22 | 33.44 | 51.33 | 49.14 | 41.34 | 14.27 | 35.11 | 39.29 | 23.61 |
| Reranker (gpt4) | 44.79 | 71.17 | 55.35 | 55.69 | 40.90 | 58.18 | 48.60 | 49.00 | 18.28 | 37.28 | 34.05 | 26.55 |
| AVATAR-C (gpt4) | 32.03 | 58.46 | 54.03 | 44.00 | 25.97 | 45.62 | 46.68 | 35.12 | 9.52 | 26.04 | 32.62 | 17.58 |
| AIR (gpt4) | 48.82 | 72.03 | 56.04 | 57.17 | 46.08 | 59.32 | 49.70 | 52.01 | 20.10 | 39.89 | 42.23 | 29.18 |
| 相对提升（相对最佳基线） | 9.0% | 1.2% | 1.3% | 2.7% | 12.7% | 2.1% | −2.2% | 6.1% | 10.0% | 7.0% | 11.0% | 9.9% |

### B.2 附加实验结果

（1）以 GPT-4 Turbo（0125）为 LLM 骨干时，AVATAR 在 STaRK 上的结果。在表 4 中，我们给出以 GPT-4 Turbo（0125）为骨干 LLM 时在 STaRK 上的结果。

**表 5：STaRK 中由人生成的查询之留出集上的检索性能（%）。** 相对提升一行在 `get_text` 中只出现 9 个百分数，未与 12 列对齐。表抽取失败，见原 PDF 第 17 页。

| 方法 | AMAZON Hit@1 | Hit@5 | R@20 | MRR | MAG Hit@1 | Hit@5 | R@20 | MRR | PRIME Hit@1 | Hit@5 | R@20 | MRR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DPR (roberta) | 16.05 | 39.51 | 15.23 | 27.21 | 4.72 | 9.52 | 25.00 | 7.90 | 2.04 | 9.18 | 10.69 | 7.05 |
| ada-002 | 39.50 | 64.19 | 35.46 | 52.65 | 28.57 | 41.67 | 35.95 | 35.81 | 17.35 | 34.69 | 41.09 | 26.35 |
| multi-ada-002 | 46.91 | 72.84 | 40.22 | 58.74 | 23.81 | 41.67 | 39.85 | 31.43 | 24.49 | 39.80 | 47.21 | 32.98 |
| ReAct | 45.65 | 71.73 | 35.95 | 58.81 | 27.27 | 40.00 | 35.95 | 33.94 | 21.73 | 33.33 | 41.09 | 28.20 |
| Reflexion | 49.38 | 64.19 | 35.95 | 58.96 | 28.57 | 39.29 | 35.95 | 36.53 | 16.52 | 33.03 | 41.09 | 23.99 |
| AVATAR | 58.32 | 76.54 | 42.43 | 65.91 | 33.33 | 42.86 | 35.94 | 38.62 | 33.03 | 51.37 | 53.34 | 41.00 |

相对提升一行已抽出的百分数，按阅读顺序为：17.5%、5.1%、11.8%、16.7%、2.9%、5.7%、28.7%、27.3%、21.4%。其余单元格抽取失败，见原 PDF 第 17 页。

（2）AVATAR 在 STaRK 由人生成的划分上的结果。在表 5 中，我们展示 AVATAR 泛化到测试查询的能力，这些查询的分布不同于用来优化行动者智能体的问答对。

**表 6：STaRK-MAG 数据集子集上不同模型的性能指标。** MAG（#Test=50）。

| 方法 | Hit@1 | Hit@5 | Recall@20 | MRR |
| --- | --- | --- | --- | --- |
| DPR | 16.00 | 40.00 | 51.84 | 27.39 |
| QAGNN | 20.00 | 52.00 | 49.71 | 36.39 |
| ada-002 | 40.00 | 58.00 | 55.93 | 47.76 |
| multi-ada-002 | 32.00 | 58.00 | 58.81 | 43.58 |
| ReAct | 46.00 | 60.00 | 54.67 | 50.92 |
| ExpeL | 40.00 | 58.00 | 55.94 | 47.43 |
| Reflexion | 48.00 | 64.00 | 57.43 | 52.31 |
| AvaTaR-C | 44.00 | 60.00 | 52.49 | 50.16 |
| AvaTaR | 52.00 | 64.00 | 53.86 | 56.74 |
| 相对提升 | 8.33% | 0.00% | −8.42% | 8.48% |

<!-- 原 PDF 第 18 页 -->

（3）AVATAR 的结果以及在 STaRK-MAG 子集上与 ExpeL 的比较。在表 6 中，AVATAR 在大多数指标上始终高于 ExpeL，尤其取得最高的 Hit@1 和 MRR 分数。虽然 ExpeL 在 Recall@20 上表现好，AVATAR 的总体改进凸显了它在精确检索任务和工具辅助知识检索上的更优能力。

（4）AVATAR 在 FLICKR30K-ENTITIES 上的最终动作序列。在图 8 中，我们给出 AVATAR 在 FLICKR30K-ENTITIES 上优化出的最终动作。

**图 8 见原 PDF。** 图 8：AVATAR 在 FLICKR30K-ENTITIES 上的优化动作序列。输入为任意查询（例子：“A man with pierced ears is wearing glasses and an orange hat.”）。动作空间包括 GetImages、GetEmbeddingSimilarity、GetVisualAttributesByLLM 等。输出为检索到的图像 ID。步骤包括：清洗查询文本；GetBagofPhrases；ComputeIDFScores；GetVisualAttributesByLLM，属性为 color、object、action、count；把短语列表连成句子；分别对短语句子和视觉属性计算嵌入相似度；MatchQueryPhrases；用 IDF 再加权；WeightedSum，权重 $(0.5, 0.3, 0.2)$；NormalizeScores；GetTopkEntities，$k=5$。图注称任务性能优秀。

（5）AVATAR 对上界和下界的敏感性。我们评估 $\ell$ 和 $h$ 的各种组合，因计算约束而聚焦于 STaRK-AMAZON 数据集。表 7 给出不同 $\ell$ 和 $h$ 值的 Hit@1 结果。

**表 7：STaRK-AMAZON 数据集上不同 $\ell$ 与 $h$ 组合的 Hit@1 结果。**

|  | $h = 0.3$ | $h = 0.4$ | $h = 0.5$ |
| --- | --- | --- | --- |
| $\ell = 0.5$ | 48.32 | 50.01 | 49.87 |
| $\ell = 0.6$ | 47.89 | 49.56 | 50.45 |
| $\ell = 0.7$ | 47.75 | 48.56 | 49.34 |

**关键观察**

- 该框架对 $\ell$ 和 $h$ 的变化表现出稳健性，Hit@1 波动限于 2.7% 的范围。
- 当 $\ell$ 与 $h$ 之间的差距变得太大时观察到性能下降，可能是由于排除了落在区间 $(h, \ell)$ 内的某些训练查询。
- $\ell$ 与 $h$ 之间的适度差距带来轻微的性能改进，提示正查询与负查询之间的平衡分离可以增强模式区分，而不损害训练查询的数量。

<!-- 原 PDF 第 19 页 -->

结果表明，设置 $\ell = 0.6$ 且 $h = 0.5$ 得到的 Hit@1 分数优于原文报告的基线。总体而言，这一分析凸显了该框架的稳健性。它依赖一组最小的超参数，包括 $\ell$、$h$、批次大小 $b$ 和训练轮数。

## C 提示

我们在全部任务上只为框架保留两个提示模板：（1）作为初始指令给行动者的提示模板；（2）给比较器、用于进行对比推理并为行动者生成指令的提示模板。下面是完整模板。

给行动者作为初始指令的提示：

你是知识库的专家用户，你的任务是回答一组查询。我将向你提供这个知识库的模式：

`<knowledge_base_schema>`

你可以访问若干已预先实现的 API，用于与知识库交互：

`<func_call_description>`

查询信息：下面是若干查询例子，你需要仔细通读：

`<example_queries>`

任务：给定一个输入查询，你应当用 Python 代码写出动作，为 `<n_init_candidates>` 个节点 ID 计算一个 `node_score_dict`。这些节点 ID 作为列表输入，称为 `candidate_ids`，是知识库节点 ID 的一个子集，并且这些节点属于类型 `<candidate_types>`。在 `node_score_dict: Dict[int, float]` 中，每个键应是一个节点 ID，每个值应是对应的节点分数。该分数应表示该节点是该查询正确答案的可能性。

输出格式：首先，你应当在给定查询与查询模式之间，以及知识库模式之间建立联系。其次，为将要计算查询例子中所提供的全部候选节点分数的代码生成一个大纲。最后，开发名为 `get_node_score_dict` 的主函数，它接受两个必需参数 `query` 和 `candidate_ids`，以及在 `parameter_dict` 中声明的可选参数。注意 `parameter_dict` 是参数及其默认值的字典，你可以在其中声明计算节点分数期间使用的任何参数或权重。若不需要可选参数，把 `parameter_dict` 留为空字典。总体而言，你的输出应遵循如下结构：

```python
# <代码大纲>
import <package1>
...
parameter_dict = {<parameter_name1>: <default_value1>,
<parameter_name2>: <default_value2>,
...}
def get_node_score_dict(query, candidate_ids, **parameter_dict):
    node_score_dict = {}
    # 你的代码
    return node_score_dict
```

提示：

<!-- 原 PDF 第 20 页 -->

- 仔细观察示例查询，并考虑要抽取的关键属性。
- 用 \`\`\`python 和 \`\`\` 包裹完整代码，不要使用任何其他定界符。
- 你可以使用任何预先实现的 API，但应避免修改它们。
- 你可以包含 `get_node_score_dict` 之外的其他函数，但要确保它们被完全实现。
- 代码应当完整，没有占位符和哑函数。
- 优化代码的完整性，例如角落情形。
- 通过尽早淘汰不满足关系要求（若有）的候选节点来最小化计算开销。
- 避免进行不必要和冗余的计算，尤其是在使用循环时。
- 利用 `parameter_dict` 来避免把参数和权重硬编码。
- 明智地使用以 `by_llm` 结尾的函数，以做更准确的搜索。
- 聪明地使用 `debug_print` 来打印任何有信息量的中间结果以便调试。
- 在输出代码中排除或注释掉 `get_node_score_dict` 的任何示例用法。

你的输出：

给比较器、用于为行动者生成指令的提示：

`<initial_prompt>`

`<previous_actions>`

在用户查询上执行上述动作之后，一些查询得到了好结果，另一些则没有。下面是这些查询及其对应的评估指标：

表现好的查询：

`<positive_queries_and_metric>`

表现差的查询：

`<negative_queries_and_metric>`

任务：

（1）首先，识别并对比取得好结果的查询与没有取得好结果的查询的模式。

（2）然后，审查计算逻辑，查找先前动作中的任何不一致。

（3）最后，指明能够导致负查询上性能改进的修改。你应当聚焦于捕捉与知识库模式相关的查询的高层模式。

## D 局限

我们识别出本工作的若干潜在局限：

- **可扩展性：** AvaTaR 被设计为随支持扩展上下文长度（至多 128k 词元）的大语言模型（LLM）而扩展，使它能处理众多工具和复杂任务。然而，延迟增加和其他实际限制可能在需要数百个工具或高复杂度的场景中妨碍性能。未来研究可以聚焦于纳入专门的、工具增强的 LLM 作为辅助智能体，以促进更平滑的扩展。
- **计算需求：** 在 AvaTaR 内管理更长的上下文和多次工具交互会增加计算需求，这可能显著提高运营成本。这些需求需要大量资源来维持高效性能，尤其是在扩展到更大的数据集或更复杂的任务时。
- **潜在失败模式：** 虽然 AvaTaR 在已知查询上表现好，当面对需要新的或不熟悉的工具组合的查询时，其性能可能下降。这一局限可以通过整合自适应学习技术和持续监控来缓解，从而使 AvaTaR 能更好地处理新颖的工具需求。

<!-- 原 PDF 第 21 页 -->

## E 函数库

### E.1 复杂检索任务

详细函数请见表 8 和表 9。

### E.2 一般 QA 任务

对一般 QA 任务，我们使用下列工具：

- WEB_SEARCH：一个通用工具，执行网页搜索来回答问题。当其他来源不可用时，用于从互联网检索最新信息。
- ARXIV_SEARCH：该工具使用论文的唯一 ID 从 Arxiv 检索学术论文信息。这一函数调用可以提供学术参考文献的元数据和其他细节。
- Wiki_SEARCH：如果你有一个问题或名称要查找，该工具使用维基百科搜索来检索相关信息。
- RETRIEVE_FROM_DB：该工具用于从数据库检索相关信息。它只在 ToolQA 上可用。

<!-- 原 PDF 第 22 页 -->

**表 8：STaRK 上的函数库。** 函数名保留英文。原文函数名 GetSatisfictionScoreByLLM 按抽取串保留。

| 函数名 | 输入 | 输出 |
| --- | --- | --- |
| ParseAttributeFromQuery | query：要解析的字符串；attributes：要从查询中抽取的属性列表 | 该函数根据输入列表 attributes 把 query 解析为一个字典 |
| GetTextEmbedding | string：要嵌入的列表数组 | 把列表中的 N 个字符串嵌入为 N 个张量 |
| GetRelevantChunk | query：输入查询字符串；node_id：节点 ID | 基于查询获取该节点的相关信息块 |
| GetFullInfo | node_id：节点 ID | 获取指定 ID 节点的完整信息 |
| GetEntityDocuments | node_id：节点 ID | 获取指定 ID 节点的文本信息 |
| GetRelationInfo | node_id：节点 ID | 获取指定 ID 节点的关系信息 |
| GetRelationDict | node_id：节点 ID | 获取指定 ID 节点的关系字典，键为关系类型，值为邻居节点 |
| GetRelatedEntities | node_id：节点 ID | 获取与指定节点相关的节点 |
| GetEntityIdsByType | type：要检索的节点类型 | 获取指定类型节点的 ID |
| GetEntityTypes | node_id：节点 ID | 获取指定 ID 节点的类型 |
| GetEntityEmbedding | node_ids：要嵌入的候选节点 ID 数组 | 获取 ID 为 node_ids 的节点的嵌入索引 |
| ComputingEmbeddingSimilarity | embedding_1 与 embedding_2 | 两个嵌入的余弦相似度分数 |
| ComputeQueryEntitySimilarity | query：输入查询字符串；node_ids：要与查询比较的候选节点 ID 数组 | 计算 query（字符串）与 node_ids（列表）中节点之间的嵌入相似度 |
| ComputeExactMatchScore | string：要匹配的字符串；node_ids：要与该字符串比较的候选节点 ID 列表 | 对 node_ids 中的每个节点，根据 string 是否包含在该节点信息中计算精确匹配分数 |
| TokenMatchScore | string：要匹配的字符串；node_ids：候选节点 ID 列表 | 对 node_ids 中的每个节点，计算 string 与该节点完整信息之间的 Recall 分数 |
| SummarizeTextsByLLM | texts：要摘要的文本列表 | 用 LLM 摘要所提供的文本 |
| ClassifyEntitiesByLLM | node_ids：要分类的候选节点 ID 数组；classes：要分入的类别列表 | 用 LLM 把 node_ids 指定的每个节点分入给定 classes 之一或 NA |
| ClassifyByLLM | texts：要分类的文本列表；classes：类别列表 | 用 LLM 把每段文本分入给定 classes 之一或 NA |
| ExtractRelevantInfoByLLM | texts：要从中抽取信息的文本列表；extract_term：用于识别相关信息的词项 | 用 LLM 基于 extract_term 从文本中抽取相关信息，返回句子或 NA |
| CheckRequirementsByLLM | node_ids：要检查的候选节点 ID 数组；requirement：要检查的要求 | 用 LLM 检查 node_ids 的节点是否满足 requirement |
| GetSatisfictionScoreByLLM | node_ids：要打分的候选节点 ID 数组；query：用户输入查询 | 用 LLM 基于给定 query 为 node_ids 的节点打分 |
| FINISH | final_reranked_answer_list：最终答案 | 该函数用于指示任务结束 |

<!-- 原 PDF 第 23 页 -->

**表 9：Flickr30K Entities 上的函数库。**

| 函数名 | 输入 | 输出 |
| --- | --- | --- |
| ParseAttributeFromQuery | query：要解析的字符串；attributes：要从查询中抽取的属性列表 | 根据输入列表 attributes 把 query 解析为一个字典 |
| GetBagOfPhrases | image_ids：要从中获取短语的图像 ID 数组 | 返回 image_ids 列表中每张图像的短语列表的列表 |
| GetEntityDocuments | image_ids：要从中获取文本信息的图像 ID 数组 | 返回 image_ids 列表中每张图像的文本信息列表 |
| GetClipTextEmbedding | string：要嵌入的字符串列表 | 把一个字符串或 N 个字符串的列表嵌入为 N 个嵌入 |
| GetPatchIdToPhraseDict | image_ids：要从中获取 patch_id 到短语列表字典的图像列表 | 返回每张图像的 patch_id 到短语列表字典的列表 |
| GetImages | image_id_lst：图像 ID 列表 | 返回具有对应 ID 的图像列表 |
| GetClipImageEmbedding | image_lst：要嵌入的图像列表 | 把 N 个 image_ids 的图像嵌入为 N 个张量 |
| GetImagePatchByPhraseId | image_id：图像 ID；patch_id：图像上的块 ID | 返回给定 image_id 和 patch_id 的块图像 |
| ComputingEmbeddingSimilarity | embedding_1 与 embedding_2 | 两个嵌入的余弦相似度分数 |
| ComputeF1 | string_to_match：要匹配的关键词；strings：要与关键词计算 F1 分数的字符串列表 | 基于 string_to_match 与 strings 中每个字符串的相似度计算 F1 分数 |
| TokenMatchScore | string_to_match：要匹配的关键词；strings：要计算 Recall 分数的字符串列表 | 基于 string_to_match 与 strings 中每个字符串的相似度计算 Recall 分数 |
| ComputeExactMatchScore | string_to_match：要精确匹配的关键词；strings：要与关键词精确匹配的字符串列表 | 根据 string_to_match 是否与 strings 中每个字符串完全相同来计算精确匹配分数 |
| VqaByLLM | question：要回答的问题；image_lst：图像列表 | 用 LLM 基于图像回答给定 question |
| ExtractVisualAttributesByLLM | attribute_lst：要抽取的属性列表；image_lst：图像列表 | 用 LLM 从每张图像中抽取关于给定 attribute_lst 的属性 |
| FINISH | final_reranked_answer_list：最终答案 | 该函数用于指示任务结束 |

<!-- 原 PDF 第 24 页 -->

## NeurIPS 论文检查清单

### 1. 主张

问题：摘要和引言中提出的主要主张是否准确反映论文的贡献和范围？

回答：[是]

理由：我们设计了一个新颖的自动框架，它优化 LLM 智能体以有效使用所提供的工具，并对我们关键模块的演化做全面分析。

指南：

- 回答 NA 意味着摘要和引言不包含论文中提出的主张。
- 摘要和/或引言应当清楚陈述所提出的主张，包括论文中的贡献以及重要假设和局限。对这一问题回答否或 NA，审稿人不会有好印象。
- 所提出的主张应当与理论和实验结果匹配，并反映结果可以在多大程度上被预期泛化到其他设定。
- 把抱负性目标作为动机是可以的，只要清楚这些目标并不是由本论文达成的。

### 2. 局限

问题：论文是否讨论作者所做工作的局限？

回答：[是]

理由：我们对 LLM 智能体、智能体优化、用于检索的 LLM 智能体这一领域的相关工作做了广泛调查，并进一步讨论它们的局限。

指南：

- 回答 NA 意味着论文没有局限，而回答否意味着论文有局限，但论文中没有讨论。
- 鼓励作者在论文中单独设立“局限”一节。
- 论文应当指出任何强假设，以及结果对这些假设被违反时有多稳健（例如独立性假设、无噪声设定、模型设定良好、渐近近似只在局部成立）。作者应当反思这些假设在实践中可能如何被违反，以及含义会是什么。
- 作者应当反思所提出主张的范围，例如该方法是否只在少数数据集或少数次运行上被测试。一般而言，经验结果往往依赖隐含假设，这些假设应当被阐明。
- 作者应当反思影响该方法性能的因素。例如，人脸识别算法在图像分辨率低或在低光照下拍摄时可能表现差。或者语音转文本系统可能不能被可靠地用于为在线讲座提供隐藏式字幕，因为它无法处理技术行话。
- 作者应当讨论所提出算法的计算效率，以及它们如何随数据集大小扩展。
- 若适用，作者应当讨论其方法在处理隐私和公平问题时的可能局限。
- 虽然作者可能担心对局限的完全诚实会被审稿人用作拒稿理由，更糟的结果可能是审稿人发现论文中未被承认的局限。作者应当运用最佳判断，并认识到有利于透明的个人行动在发展维护社区诚信的规范中扮演重要角色。审稿人将被特别指示，不要因关于局限的诚实而惩罚作者。

### 3. 理论假设与证明

<!-- 原 PDF 第 25 页 -->

问题：对每个理论结果，论文是否提供完整的假设集合以及完整（且正确）的证明？

回答：[NA]

理由：论文不包含理论结果。

指南：

- 回答 NA 意味着论文不包含理论结果。
- 论文中的全部定理、公式和证明应当编号并交叉引用。
- 全部假设应当在任何定理的陈述中被清楚陈述或引用。
- 证明可以出现在正文或补充材料中，但如果出现在补充材料中，鼓励作者提供一个简短的证明概要以提供直觉。
- 反过来，论文核心中提供的任何非正式证明都应当由附录或补充材料中的形式证明来补充。
- 证明所依赖的定理和引理应当被适当引用。

### 4. 实验结果的可复现性

问题：论文是否充分披露复现论文主要实验结果所需的全部信息，以至于影响论文的主要主张和/或结论（无论代码和数据是否被提供）？

回答：[是]

理由：我们在实验一节中阐述实验细节，包括数据集、基线、函数库等。我们也为可复现性发布实验中使用的全部提示。

指南：

- 回答 NA 意味着论文不包含实验。
- 如果论文包含实验，对这一问题回答否不会给审稿人好印象：使论文可复现是重要的，无论代码和数据是否被提供。
- 如果贡献是数据集和/或模型，作者应当描述为使结果可复现或可验证所采取的步骤。
- 取决于贡献，可复现性可以用多种方式实现。例如，如果贡献是一种新颖架构，充分描述该架构可能就够了；如果贡献是一个特定模型和经验评估，可能有必要使他人能用相同数据集复现该模型，或提供对该模型的访问。一般而言，发布代码和数据常常是实现这一点的一种好方式，但可复现性也可以通过关于如何复现结果的详细指令、对托管模型的访问（例如大语言模型的情形）、发布模型检查点，或其他适合于所做研究的手段来提供。
- 虽然 NeurIPS 不要求发布代码，会议确实要求全部投稿提供某种合理的可复现途径，这可能取决于贡献的性质。例如：（a）如果贡献主要是一种新算法，论文应当清楚说明如何复现该算法。（b）如果贡献主要是一种新模型架构，论文应当清楚而充分地描述该架构。（c）如果贡献是一个新模型（例如大语言模型），那么要么应当有办法访问该模型以复现结果，要么有办法复现该模型（例如用开源数据集，或关于如何构造数据集的指令）。（d）我们认识到可复现性在某些情形下可能棘手，在这种情况下欢迎作者描述他们为可复现性所提供的特定方式。对闭源模型，对该模型的访问可能以某种方式受限（例如仅限注册用户），但其他研究者应当有某种路径来复现或验证结果。

### 5. 数据与代码的开放获取

<!-- 原 PDF 第 26 页 -->

问题：论文是否提供对数据与代码的开放获取，并有足够指令来忠实地复现主要实验结果，如补充材料所述？

回答：[是]

理由：我们的代码和数据可在 https://anonymous.4open.science/r/AvaTaR-FBC4/ 获取。

指南：

- 回答 NA 意味着论文不包含需要代码的实验。
- 更多细节请见 NeurIPS 代码与数据投稿指南（https://nips.cc/public/guides/CodeSubmissionPolicy）。
- 虽然我们鼓励发布代码和数据，我们理解这可能并不总是可能，因此“否”是可接受的回答。论文不能仅仅因为不包含代码就被拒，除非这对贡献是核心的（例如一个新的开源基准）。
- 指令应当包含复现结果所需运行的确切命令和环境。更多细节见上述指南。
- 作者应当提供关于数据访问和准备的指令，包括如何访问原始数据、预处理数据、中间数据和生成数据等。
- 作者应当提供脚本以复现新提出方法和基线的全部实验结果。如果只有一部分实验可复现，他们应当说明哪些被从脚本中省略以及为什么。
- 在投稿时，为保持匿名，作者应当发布匿名版本（若适用）。
- 建议在补充材料（附于论文）中提供尽可能多的信息，但包含指向数据与代码的 URL 是允许的。

### 6. 实验设定/细节

问题：论文是否指定理解结果所必需的全部训练和测试细节（例如数据划分、超参数、它们如何被选择、优化器类型等）？

回答：[是]

理由：我们在实验部分和附录中包含数据集信息和训练细节。我们也清楚描述知识库并形式化介绍任务设定。

指南：

- 回答 NA 意味着论文不包含实验。
- 实验设定应当在论文核心中以欣赏结果并理解它们所必需的细节水平来呈现。
- 完整细节可以随代码、在附录中或作为补充材料提供。

### 7. 实验统计显著性

问题：论文是否适当地、正确地定义误差条，或提供关于实验统计显著性的其他适当信息？

回答：[NA]

理由：[NA]

指南：

- 回答 NA 意味着论文不包含实验。
- 如果结果附有误差条、置信区间或统计显著性检验，至少对支持论文主要主张的实验如此，作者应当回答“是”。

<!-- 原 PDF 第 27 页 -->

- 误差条所捕捉的变异因素应当被清楚陈述（例如训练/测试划分、初始化、某个参数的随机抽取，或在给定实验条件下的总体运行）。
- 计算误差条的方法应当被解释（闭式公式、调用库函数、自助法等）。
- 应当给出所做的假设（例如误差正态分布）。
- 应当清楚误差条是标准差还是均值的标准误。
- 报告 1-sigma 误差条是可以的，但应当加以说明。如果误差正态性的假设未被验证，作者最好报告 2-sigma 误差条，而不是声称他们有 96% 置信区间。
- 对非对称分布，作者应当小心，不要在表或图中显示对称误差条，以免产生超出范围的结果（例如负的错误率）。
- 如果在表或图中报告误差条，作者应当在正文中解释它们如何被计算，并在正文中引用对应的图或表。

### 8. 实验计算资源

问题：对每个实验，论文是否提供足够信息，说明复现实验所需的计算机资源（计算工人类型、内存、执行时间）？

回答：[是]

理由：我们在单块 NVIDIA A100-SXM4-80GB GPU 和 32 核 CPU 上运行实验。

指南：

- 回答 NA 意味着论文不包含实验。
- 论文应当指出计算工人的类型：CPU 或 GPU、内部集群或云提供商，包括相关内存和存储。
- 论文应当提供每一次个别实验运行所需的计算量，并估计总计算量。
- 论文应当披露整个研究项目是否需要比论文中报告的实验更多的计算（例如没有进入论文的初步或失败实验）。

### 9. 伦理准则

问题：论文中进行的研究是否在每一方面都符合 NeurIPS 伦理准则 https://neurips.cc/public/EthicsGuidelines ？

回答：[是]

理由：我们在论文中没有诱发 NeurIPS 伦理准则中提到的任何潜在研究伤害。

指南：

- 回答 NA 意味着作者没有审阅 NeurIPS 伦理准则。
- 如果作者回答否，他们应当解释要求偏离伦理准则的特殊情况。
- 作者应当确保保持匿名（例如，若因其司法管辖区的法律或法规而有特殊考虑）。

### 10. 更广泛的影响

问题：论文是否讨论所做工作的潜在正面社会影响和负面社会影响？

回答：[是]

理由：我们在引言一节讨论了影响。

指南：

- 回答 NA 意味着所做工作没有社会影响。

<!-- 原 PDF 第 28 页 -->

- 如果作者回答 NA 或否，他们应当解释为什么他们的工作没有社会影响，或为什么论文不讨论社会影响。
- 负面社会影响的例子包括潜在的恶意或非预期用途（例如虚假信息、生成虚假画像、监视）、公平性考虑（例如部署可能做出不公平影响特定群体之决策的技术）、隐私考虑和安全考虑。
- 会议预期许多论文将是基础研究，不绑定于特定应用，更不必说部署。然而，如果存在通向任何负面应用的直接路径，作者应当指出。例如，指出生成模型质量的改进可能被用来生成用于虚假信息的深度伪造是正当的。另一方面，不必指出一个用于优化神经网络的通用算法可能使人们能更快地训练生成深度伪造的模型。
- 作者应当考虑：当技术按预期使用且正确运行时可能产生的伤害；当技术按预期使用但给出不正确结果时可能产生的伤害；以及技术被（有意或无意）误用之后的伤害。
- 如果存在负面社会影响，作者也可以讨论可能的缓解策略（例如模型的门控发布、在攻击之外提供防御、监控误用的机制、监控系统如何随时间从反馈中学习的机制、改善 ML 的效率与可及性）。

### 11. 保障措施

问题：论文是否描述为负责任地发布具有高误用风险的数据或模型（例如预训练语言模型、图像生成器或抓取的数据集）而已经落实的保障措施？

回答：[NA]

理由：我们的方法提供一个更好地使用语言模型的框架，但并不发布语言模型。

指南：

- 回答 NA 意味着论文不构成此类风险。
- 具有高误用或两用风险的已发布模型应当带有必要的保障措施来发布，以允许受控使用该模型，例如要求用户遵守使用指南或访问限制，或实现安全过滤器。
- 从互联网抓取的数据集可能构成安全风险。作者应当描述他们如何避免发布不安全的图像。
- 我们认识到提供有效保障措施具有挑战，许多论文并不需要这一点，但我们鼓励作者把这一点考虑进去并尽最大诚信努力。

### 12. 现有资产的许可

问题：论文中使用的资产（例如代码、数据、模型）的创建者或原始所有者是否被适当署名，许可和使用条款是否被明确提及并得到适当尊重？

回答：[是]

理由：论文中提到的资产的创建者或原始所有者被适当引用，许可和使用条款得到尊重。

指南：

- 回答 NA 意味着论文不使用现有资产。
- 作者应当引用产生代码包或数据集的原始论文。
- 作者应当说明使用的是该资产的哪个版本，并在可能时包含 URL。
- 应当为每项资产包含许可名称（例如 CC-BY 4.0）。
- 对来自特定来源（例如网站）的抓取数据，应当提供该来源的版权和服务条款。

<!-- 原 PDF 第 29 页 -->

- 如果发布资产，应当提供包中的许可、版权信息和使用条款。对流行数据集，paperswithcode.com/datasets 为一些数据集整理了许可。他们的许可指南可以帮助确定数据集的许可。
- 对被重新打包的现有数据集，应当同时提供原始许可和派生资产的许可（如果它已改变）。
- 如果这一信息在网上不可用，鼓励作者联系资产的创建者。

### 13. 新资产

问题：论文中引入的新资产是否被良好记录，并且文档是否与资产一起提供？

回答：[NA]

理由：论文不发布新资产。

指南：

- 回答 NA 意味着论文不发布新资产。
- 研究者应当通过结构化模板，把数据集/代码/模型的细节作为投稿的一部分来传达。这包括关于训练、许可、局限等的细节。
- 论文应当讨论是否以及如何从资产被使用的人那里获得同意。
- 在投稿时，记得把你的资产匿名化（若适用）。你可以创建匿名 URL，或包含一个匿名压缩文件。

### 14. 众包与人类受试者研究

问题：对众包实验和人类受试者研究，论文是否包含给参与者的指令全文和截图（若适用），以及关于报酬（若有）的细节？

回答：[NA]

理由：论文不涉及众包，也不涉及人类受试者研究。

指南：

- 回答 NA 意味着论文不涉及众包，也不涉及人类受试者研究。
- 把这一信息放在补充材料中是可以的，但如果论文的主要贡献涉及人类受试者，那么应当在正文中包含尽可能多的细节。
- 根据 NeurIPS 伦理准则，参与数据收集、整理或其他劳动的工作者应当至少获得数据收集者所在国家的最低工资。

### 15. 人类受试者研究的机构审查委员会（IRB）批准或等效批准

问题：论文是否描述研究参与者所承担的潜在风险、此类风险是否向受试者披露，以及是否获得了机构审查委员会（IRB）批准（或基于你的国家或机构要求的等效批准/审查）？

回答：[NA]

理由：论文不涉及众包，也不涉及人类受试者研究。

指南：

- 回答 NA 意味着论文不涉及众包，也不涉及人类受试者研究。
- 取决于进行研究的国家，任何人类受试者研究可能都需要 IRB 批准（或等效批准）。如果你获得了 IRB 批准，应当在论文中清楚陈述这一点。

<!-- 原 PDF 第 30 页 -->

- 我们认识到这一程序在机构和地点之间可能有显著差异，我们期望作者遵守 NeurIPS 伦理准则及其机构的指南。
- 对初次投稿，不要包含任何会破坏匿名性的信息（若适用），例如进行审查的机构。

<!-- 译完 -->
