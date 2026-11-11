# ReFuGe: Feature Generation for Prediction Tasks on Relational Databases with LLM Agents

- 原文件名：refuge-arxiv-2601.17735.pdf
- 原标题：ReFuGe: Feature Generation for Prediction Tasks on Relational Databases with LLM Agents
- 中文标题：ReFuGe：用大语言模型智能体为关系数据库上的预测任务生成特征
- 作者：Kyungho Kim，Geon Lee，Juyeon Kim，Dongwon Choi，Shinhwan Kang，Kijung Shin（KAIST，首尔，大韩民国）
- 会议 / arXiv：页眉为 WWW ’26, April 13–17, 2026, Dubai, United Arab Emirates。ACM Reference 写明 Proceedings of the ACM Web Conference 2026 (WWW ’26)，ACM, New York, NY, USA, 4 pages，https://doi.org/10.1145/3774904.3792895。第 1 页底部另有 arXiv:2601.17735v1 [cs.AI] 25 Jan 2026。

<!-- 原 PDF 第 1 页 -->

## 摘要

关系数据库（relational database，RDB）在许多真实网络应用中起着关键作用，支撑着多张相互关联的表上的数据管理。除典型的面向检索的任务之外，RDB 上的预测任务近来受到关注。本文通过生成能够提升预测性能的信息性关系特征来处理这一问题。然而，生成此类特征具有挑战：需要在复杂模式上推理，并探索组合上极大的特征空间，且全程没有显式监督。为应对这些挑战，我们提出 ReFuGe，一个智能体框架，使用专门的大语言模型（large language model，LLM）智能体：（1）模式选择智能体识别与任务相关的表和列；（2）特征生成智能体从所选模式中产生多样的候选特征；（3）特征过滤智能体通过基于推理的过滤和基于验证的过滤，评估并保留有希望的特征。该框架在迭代反馈循环中运行，直到性能收敛。在 RDB 基准上的实验表明，ReFuGe 在多种 RDB 预测任务上大幅提升性能。代码与数据集见 https://github.com/K-Kyungho/REFUGE。

## CCS 概念

- 信息系统 → 关系数据库模型。

## 关键词

关系数据库，特征生成，大语言模型

## ACM 参考文献格式

Kyungho Kim, Geon Lee, Juyeon Kim, Dongwon Choi, Shinhwan Kang, and Kijung Shin. 2026. ReFuGe: Feature Generation for Prediction Tasks on Relational Databases with LLM Agents. In Proceedings of the ACM Web Conference 2026 (WWW ’26), April 13–17, 2026, Dubai, United Arab Emirates. ACM, New York, NY, USA, 4 pages. https://doi.org/10.1145/3774904.3792895

## 1 引言与相关工作

关系数据库广泛用于各类网络应用，例如在线零售平台、社交网络服务和论坛平台。多年来，RDB 研究在面向检索的任务上取得了显著进展，其目标是生成能够抽取相关信息的查询 [10, 11, 15]。近来，这一范围扩展到预测任务（例如分类），旨在利用 RDB 的关系结构来提升下游预测性能 [5–8, 17, 18]。

在 RDB 上实现预测的一种实用而有效的做法，是生成能够捕获分布在相关表中的预测信号的特征 [14]。例如，客户表可以用聚合的购买统计、近期交易次数，或从其他表得到的关联账户属性来充实。有了这张包含生成特征的充实表，就可以直接应用标准的表格学习方法 [4, 12]。

然而，在 RDB 中自动生成有效特征面临若干挑战。首先，需要从关系结构中理解并抽取预测信号（C1）。其次，潜在特征的空间极大，因为表可以被变换或组合的方式很多（C2）。第三，特征生成缺少真值监督，因而无法做直接的监督学习；这与检索任务（例如 text-to-SQL）不同，后者有真值查询可用（C3）。

为应对这些挑战，我们提出 ReFuGe（RElational FeatUre GEneration，关系特征生成），一个利用 LLM 推理能力的智能体框架。针对（C1），我们引入一个

图 1 见原 PDF。

**图 1：** ReFuGe 跨迭代生成特征的一个例子。ReFuGe 迭代地生成关系特征，并追加到目标表。

脚注：本作品采用 Creative Commons Attribution 4.0 International License 授权。WWW ’26, Dubai, United Arab Emirates。© 2026 Copyright held by the owner/author(s). ACM ISBN 979-8-4007-2307-0/2026/04。https://doi.org/10.1145/3774904.3792895

第 1 页底部印有：arXiv:2601.17735v1 [cs.AI] 25 Jan 2026。

<!-- 原 PDF 第 2 页 -->

模式选择智能体，它识别 RDB 中为预测任务提供最相关关系信息的表和列。针对（C2），我们使用多个特征生成智能体，它们借助领域知识以及对关系上下文的理解，为预测表产生有意义的候选特征。所得候选特征再经过基于推理和基于验证的过滤步骤，被选择性地加入表中。最后，针对（C3），我们采用迭代的自我改进机制，使智能体能够在没有真值监督的情况下改进模式选择并生成特征。如图 1 所示，ReFuGe 逐步利用多张表中的信息生成新特征，使验证 AUROC 随迭代持续提升。在多个 RDB 上的实验表明，ReFuGe 能有效提升预测性能。

我们的主要贡献概括如下：

- **新问题。** 我们提出一个新问题：为 RDB 上的预测任务生成特征。
- **智能体框架。** 我们提出 ReFuGe，一个用于 RDB 特征生成的、基于 LLM 的有效智能体框架。
- **经验验证。** 我们表明，ReFuGe 在七个数据集、十一项任务上优于最先进的竞争方法。

## 2 任务形式化

给定一个关系数据库 $R = \{T_1, T_2, \ldots, T_{|R|}\}$，其中每张表 $T_i \in R$ 包含一组实体（即行），并通过主键–外键关系与其他表相连。非正式地，我们假定每张表是一个异构特征矩阵 $T_i \in \mathcal{F}^{N_i \times d_i}$，其中 $N_i$ 与 $d_i$ 分别表示实体数和特征数，$\mathcal{F}$ 表示可接受数据类型的空间（例如数值型、类别型）。

我们考虑定义在指定目标实体表 $T_\star \in R$ 的目标实体上的预测任务（例如分类）。我们的目标是利用 $T_\star$ 在整个关系数据库 $R$ 内的关系上下文，为 $T_\star$ 生成额外特征。生成的特征随后与 $T_\star$ 的原始属性拼接，并用于训练一个表格模型（例如 LightGBM [12]）。

## 3 所提框架

我们提出 ReFuGe，一个为 RDB 上的预测任务生成关系特征的智能体框架（图 2）。ReFuGe 由三个专门的 LLM 智能体组成：（1）模式选择智能体，（2）特征生成智能体，（3）特征过滤智能体。这些智能体在迭代反馈循环中运行，随迭代逐步生成并改进特征。每一步的详细输入提示见附录 [1]。

图 2 见原 PDF。

**图 2：** ReFuGe 总览。经由（1）模式选择、（2）特征生成和（3）特征过滤——每一步由一个专门的 LLM 智能体执行——ReFuGe 迭代地生成关系特征，充实目标表，并提升 RDB 预测任务上的性能。每一轮迭代都会生成反馈，并传给各智能体，以指导下一轮。

**步骤 1：模式选择。** 作为初始步骤，模式选择智能体决定应从何处生成特征。该智能体接收 RDB 模式信息，包括表、列名、列类型和主键–外键关系，以及任务描述。利用这些信息，它借助推理能力识别与预测任务相关的表和列子集，并滤除不相关者。这一步有效缩小了后续步骤生成特征的搜索空间。

**步骤 2：特征生成。** 接下来，特征生成智能体在所选模式上产生候选特征。即使缩小了模式，可能的关系特征数量仍然呈指数级，其中只有少数可能有用。为此，该智能体利用推理能力，提出可能具有信息量、并可能提升预测性能的特征。为鼓励所生成特征的多样性，该智能体使用多个 LLM 实例，¹ 每个实例生成一组可能互不相同的候选特征。这些特征随后被汇总到一个统一的特征池中。

**步骤 3：特征过滤。** 给定步骤 2 生成的候选特征集合，特征过滤智能体应用两阶段过滤过程，只保留最有希望的特征。

- **步骤 3.1. 基于推理的特征过滤。** 智能体审阅候选特征，并依据任务描述和模式上下文，选出一个更小的、可能对任务有益的子集。重要的是，在第一次迭代中，智能体仅依赖对所提供信息的语义推理；从第二次迭代起，它还额外考虑先前生成特征的性能。
- **步骤 3.2. 基于验证的特征过滤。** 每个被选中的特征随后被（临时）加入目标表，并用于训练表格学习模型（例如 LightGBM）。² 若纳入某特征能提升验证性能，则保留该特征并追加到目标表；否则丢弃。

¹ 我们使用同一模型，随机性由正的温度保证。

² 实践中，为提高效率，我们抽样训练集的一个子集，而不是使用全部数据。

<!-- 原 PDF 第 3 页 -->

**表 1：**（RQ1）实体分类性能。所有指标均以 AUROC 报告。最佳结果以粗体标出，次佳结果加下划线。

| 方法 | rel-avito visits | rel-avito clicks | rel-stack engage | rel-stack badge | rel-f1 dnf | rel-f1 top3 | rel-event repeat | rel-event ignore | rel-trial outcome | rel-hm churn | rel-amazon churn | 平均 AUROC | 平均秩 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LightGBM [12] | 53.05 | 53.60 | 63.39 | 63.43 | 68.56 | 73.92 | 68.04 | 79.93 | 70.09 | 55.21 | 52.22 | 63.77 | 6.8 |
| XGBoost [4] | 53.67 | 54.59 | 54.78 | 61.98 | 65.32 | 70.08 | 56.85 | 74.25 | 71.21 | 55.46 | 59.06 | 61.57 | 7.5 |
| FeatLLM [9] | 51.15 | 48.69 | 42.56 | - | 70.43 | 52.72 | 46.67 | 47.88 | 57.35 | - | 55.11 | 52.51 | 8.7 |
| ICL [20] | 60.28 | 61.32 | 81.01 | 71.13 | 65.81 | 88.47 | 76.38 | 78.55 | 55.72 | 64.34 | 60.56 | 69.42 | 4.7 |
| Rel-LLM [19] | 56.17 | 62.28 | 69.46 | 62.12 | 71.84 | 70.64 | 68.12 | 61.32 | 59.02 | 55.95 | 60.07 | 63.36 | 6.0 |
| RT-Gemma [16] | 62.70 | 59.80 | 78.00 | 80.00 | 75.80 | 91.40 | - | - | 57.20 | 48.70 | 50.50 | 67.12 | 5.9 |
| GPT [2] | 65.21 | 58.04 | 83.82 | 80.21 | 65.16 | 77.04 | 71.26 | 76.41 | 72.94 | 55.50 | 63.72 | 69.94 | 4.3 |
| Claude [3] | 64.90 | 60.90 | 80.36 | 80.37 | 54.99 | 79.74 | 66.39 | 76.20 | 68.27 | 67.64 | 64.66 | 69.49 | 4.7 |
| LLM-CoT [13] | 64.89 | 60.19 | 82.30 | 80.97 | 61.41 | 75.92 | 70.13 | 82.58 | 68.03 | 68.06 | 64.42 | 70.81 | 4.2 |
| ReFuGe（本文） | 66.43 | 63.20 | 87.66 | 83.80 | 76.26 | 83.04 | 77.14 | 83.40 | 72.22 | 68.10 | 67.00 | 75.30 | 1.3 |

表中前三行属于「单表」方法，后七行属于「RDB」方法。原表将 LightGBM、XGBoost、FeatLLM 标在 Single Table 下，将其余方法标在 RDB 下。粗体与下划线是原 PDF 的视觉标注，抽取文本未保留各单元格的粗体或下划线，故表中数字原样列出，不另加标注。

值得注意的是，两个过滤阶段相互补充。基于推理的过滤依据语义推理缩小搜索空间，基于验证的过滤则评估每个特征的经验效用。二者共同保证最终特征既在语义上有意义，又在经验上有效。

**迭代反馈循环。** ReFuGe 迭代重复步骤 1–3，直到不再有额外特征被选中。在这一迭代循环中，ReFuGe 被设计为根据先前迭代的结果自我改进。具体而言，在过滤步骤结束时，它生成自然语言反馈，总结每个被评估特征如何影响性能，例如：“[Ad View Diversity] 使验证 AUROC 从 65.06 提高到 66.30”，或“[Direct Search Ratio] 使验证 AUROC 从 66.68 下降到 66.40”。该反馈随后作为输入提供给每个智能体，作为指导后续迭代决策的参考。反馈跨迭代累积，使智能体能够自行学会哪些方向有希望、哪些应当避免。

## 4 实验

本节考察以下五个研究问题：

- **RQ1. 性能比较。** 与现有基线方法相比，ReFuGe 在 RDB 预测任务上有多准确？
- **RQ2. 消融研究。** ReFuGe 的关键组件是否对其总体性能有贡献？
- **RQ3. 带反馈的迭代的效果。** ReFuGe 的性能是否通过其反馈驱动的迭代循环得到提升？
- **RQ4. 案例研究。** ReFuGe 生成什么样的特征？
- **RQ5. 参数分析。** 特征生成智能体中的 LLM 实例数如何影响性能？

### 4.1 实验设置

实验设置的全部细节见 [1]。

**数据集。** 我们在七个真实世界 RDB 基准数据集 [17] 上做实验，覆盖多样的领域。

**基线。** 我们将 ReFuGe 与单表方法和 RDB 方法比较。单表方法包括（i）机器学习模型 [4, 12] 和（ii）一个基于 LLM 的模型 [9]。这些方法只依赖目标表的属性，不纳入关系信息。RDB 方法包括（iii）把 LLM 当作预测器的方法，其中 LLM 直接使用从 RDB 连接得到的数据做预测 [16, 19, 20]；以及（iv）把 LLM 当作生成器的方法，其中单个 LLM 实例使用与 ReFuGe 相同的输入直接生成关系特征，但没有模式选择、特征过滤或反馈循环 [2, 3, 13]。这些方法利用来自 RDB 的信息。

### 4.2 实验结果

**（RQ1）性能比较。** 如表 1 所示，ReFuGe 在 11 项任务中的 9 项上优于全部基线，并取得最好的平均性能和总体平均秩。这些结果表明，LLM 能够有效理解 RDB 的关系结构，并为预测任务生成有信息量的特征。值得注意的是，ReFuGe 不仅在模式简单的 RDB 上表现最好（例如 rel-amazon 和 rel-hm，有 3 张表和 2 条主键–外键关系），在模式更复杂的 RDB 上同样最好（例如 rel-stack，有 7 张表和 12 条主键–外键关系），表明它适用于不同的模式复杂度。

**（RQ2）消融研究。** 为考察 ReFuGe 关键组件的有效性，我们考虑三个变体：

- **ReFuGe-SS：** 跳过模式选择步骤（原文写 step 2），直接从完整 RDB 模式生成特征。
- **ReFuGe-FF：** 用候选特征的随机选择替换基于推理的特征过滤（步骤 3.1）。
- **ReFuGe-FB：** 迭代过程中不纳入反馈。

如表 2 所示，ReFuGe 在 11 种情形中的 7 种上优于其全部变体，并取得最好的平均秩。值得注意的是，ReFuGe-FF 造成最大的性能下降，表明对所生成特征进行推理并选出最有希望者很重要。ReFuGe-FB 造成第二大的下降，表明较早迭代的性能信号为后续特征生成提供了有意义的指导。

**（RQ3）带反馈的迭代的效果。** 如图 3 所示，ReFuGe 的评估性能大体随迭代提升，表明其反馈驱动的迭代循环是有效的。当不再有额外特征被选中时迭代停止，ReFuGe 在全部任务上平均执行 2.4 次迭代。

**（RQ4）案例研究。** 在图 1 中，我们给出 rel-avito 数据集上 user-clicks 任务的案例研究。该任务预测目标表中的每个用户在未来 4 天内是否会点击超过一条广告。ReFuGe 首先导出一个特征，它捕获

<!-- 原 PDF 第 4 页 -->

**表 2：**（RQ2）ReFuGe 关键组件的有效性。最佳性能以粗体标出，次佳性能加下划线。

| 方法 | rel-avito visits | rel-avito clicks | rel-stack engage | rel-stack badge | rel-f1 dnf | rel-f1 top3 | rel-event repeat | rel-event ignore | rel-trial outcome | rel-hm churn | rel-amazon churn | 平均 AUROC | 平均秩 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ReFuGe-SS | 66.61 | 60.15 | 82.70 | 83.89 | 73.37 | 79.46 | 73.34 | 88.36 | 72.19 | 68.04 | 63.40 | 73.77 | 2.3 |
| ReFuGe-FF | 66.56 | 58.25 | 88.51 | 82.17 | 62.42 | 62.20 | 70.62 | 82.47 | 71.00 | 68.04 | 63.94 | 70.56 | 3.0 |
| ReFuGe-FB | 66.43 | 61.21 | 87.61 | 63.41 | 62.40 | 81.32 | 68.00 | 83.35 | 71.65 | 67.92 | 66.39 | 70.88 | 3.1 |
| ReFuGe | 66.43 | 63.20 | 87.66 | 83.80 | 76.26 | 83.04 | 77.14 | 83.40 | 72.22 | 68.10 | 67.00 | 75.30 | 1.5 |

粗体与下划线是原 PDF 的视觉标注，抽取文本未保留各单元格的粗体或下划线，故表中数字原样列出。

每个用户点击的不同广告数，所用的是 VisitStream 表，从而带来大幅性能增益。在下一次迭代中，它加入一个特征，捕获用户搜索位置的平均地理层级，该特征通过连接 SearchStream 表与 Location 表得到，并进一步提升性能。

图 3 见原 PDF。

**图 3：**（RQ3）在全部三项任务上，评估性能趋于随迭代提升。★ 表示各次迭代中最好的验证性能。图中三条曲线对应 Avito-Visits、Stack-Engage、Event-Repeat，纵轴为 AUROC，横轴为迭代次数。曲线上的具体读数未能从文本层抽出，见原 PDF。

**（RQ5）参数分析。** 如图 4 所示，我们观察到，使用更多 LLM 实例作为特征生成智能体，在三项任务上趋于提升性能，只有少数例外。这表明，增加所生成候选特征的多样性总体上是有益的。实验中，为简单和效率起见，我们将实例数固定为三。更多参数分析见 [1]。

## 5 结论

本文从特征生成的角度处理 RDB 上的预测。我们引入一个新问题：为 RDB 上的预测任务生成特征（第 2 节），并提出 ReFuGe，一个利用 LLM 智能体、基于反馈迭代生成并改进关系特征的智能体框架（第 3 节）。我们在多个 RDB 基准数据集上进行大量实验，以展示 ReFuGe 的有效性（第 4 节）。未来工作中，我们打算把该框架扩展到更多下游任务，例如回归和链接预测。

**致谢。** 本工作得到韩国政府（MSIT）资助、由信息通信技术规划与评估研究所（Institute of Information & Communications Technology Planning & Evaluation，IITP）下达的课题支持：（No. RS-2024-00438638，EntireDB2AI：面向完整关系数据库的综合深度表示学习与预测的基础和软件，60%）（No. RS-2022-II220157，稳健、公平、可扩展的以数据为中心的持续学习，30%）（No. RS-2019-II190075，人工智能研究生院项目（KAIST），10%）。

图 4 见原 PDF。

**图 4：**（RQ5）随着用作特征生成智能体的 LLM 实例数增加，评估性能趋于上升。★ 表示最好的测试性能。图中三条曲线对应 Avito-Visits、Stack-Engage、Event-Repeat，纵轴为 AUROC，横轴为实例数。曲线上的具体读数未能从文本层抽出，见原 PDF。

## 参考文献

[1] 2026. ReFuGe 的代码、数据集与附录. https://github.com/K-Kyungho/REFUGE.

[2] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. 2023. GPT-4 技术报告. arXiv:2303.08774 (2023).

[3] Anthropic. 2025. Claude 4 模型卡. https://www.anthropic.com.

[4] Tianqi Chen and Carlos Guestrin. 2016. XGBoost：一种可扩展的树提升系统. In KDD.

[5] Tianlang Chen, Charilaos Kanatsoulis, and Jure Leskovec. 2025. RelGNN：面向关系深度学习的复合消息传递. arXiv:2502.06784 (2025).

[6] Dongwon Choi, Sunwoo Kim, Juyeon Kim, Kyungho Kim, Geon Lee, Shinhwan Kang, Myunghwan Kim, and Kijung Shin. 2025. RDB2G-Bench：关系数据库自动图建模的综合基准. In NeurIPS.

[7] Vijay Prakash Dwivedi, Charilaos Kanatsoulis, Shenyang Huang, and Jure Leskovec. 2025. 关系深度学习：挑战、基础与下一代架构. In KDD.

[8] Matthias Fey, Weihua Hu, Kexin Huang, Jan Eric Lenssen, Rishabh Ranjan, Joshua Robinson, Rex Ying, Jiaxuan You, and Jure Leskovec. 2024. 关系深度学习：关系数据库上的图表示学习. In ICML.

[9] Sungwon Han, Jinsung Yoon, Secran O Arik, and Tomas Pfister. 2024. 大语言模型能够为少样本表格学习自动构造特征. In ICML.

[10] Zijin Hong, Zheng Yuan, Qinggang Zhang, Hao Chen, Junnan Dong, Feiran Huang, and Xiao Huang. 2024. 下一代数据库接口：基于大语言模型的 text-to-SQL 综述. arXiv:2406.08426 (2024).

[11] George Katsogiannis-Meimarakis and Georgia Koutrika. 2023. 面向 text-to-SQL 的深度学习方法综述. The VLDB Journal 32, 4 (2023), 905–936.

[12] Guolin Ke, Qi Meng, Thomas Finley, Taifeng Wang, Wei Chen, Weidong Ma, Qiwei Ye, and Tie-Yan Liu. 2017. LightGBM：一种高效的梯度提升决策树. In NeurIPS.

[13] Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa. 2022. 大语言模型是零样本推理器. In NeurIPS.

[14] Jiaming Liang, Chuan Lei, Xiao Qin, Jiani Zhang, Asterios Katsifodimos, Christos Faloutsos, and Huzefa Rangwala. 2024. FeatNavigator：表格数据上的自动特征增强. arXiv:2406.09534 (2024).

[15] Xinyu Liu, Shuyu Shen, Boyan Li, Peixian Ma, Runzhi Jiang, Yuxin Zhang, Ju Fan, Guoliang Li, Nan Tang, and Yuyu Luo. 2024. 大语言模型 NL2SQL 综述：我们在哪里，要往哪里去？ arXiv:2408.05109 (2024).

[16] Rishabh Ranjan, Valter Hudovernik, Mark Znidar, Charilaos Kanatsoulis, Roshan Upendra, Mahmoud Mohammadi, Joe Meyer, Tom Palczewski, Carlos Guestrin, and Jure Leskovec. 2025. Relational Transformer：迈向关系数据的零样本基础模型. arXiv:2510.06377 (2025).

[17] Joshua Robinson, Rishabh Ranjan, Weihua Hu, Kexin Huang, Jiaqi Han, Alejandro Dobles, Matthias Fey, Jan Eric Lenssen, Yiwen Yuan, Zecheng Zhang, et al. 2024. RelBench：关系数据库上深度学习的基准. In NeurIPS.

[18] Minjie Wang, Quan Gan, David Wipf, Zheng Zhang, Christos Faloutsos, Weinan Zhang, Muhan Zhang, Zhenkun Cai, Jiahang Li, Zunyao Mao, et al. 2024. 4DBInfer：面向 RDB 上以图为中心的预测建模的四维基准工具箱. In NeurIPS.

[19] Fang Wu, Vijay Prakash Dwivedi, and Jure Leskovec. 2025. 大语言模型是良好的关系学习器. In ACL.

[20] Marek Wydmuch, Lukasz Borchmann, and Filip Gralinski. 2024. 用大语言模型处理关系数据库中的预测任务. arXiv:2411.11829 (2024).

<!-- 译完 -->
