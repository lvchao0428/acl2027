# LEARN：面向实际工业应用、从大语言模型到推荐的知识适配

- 原文件名：LEARN-2405.03988.pdf
- 原标题：LEARN: Knowledge Adaptation from Large Language Model to Recommendation for Practical Industrial Application
- 中文标题：LEARN：面向实际工业应用、从大语言模型到推荐的知识适配
- 作者：Jian Jia、Yipei Wang、Yan Li、Honggang Chen、Xuehan Bai、Zhaocheng Liu、Jian Liang、Quan Chen、Han Li、Peng Jiang、Kun Gai
- 会议或 arXiv：页边标注为 arXiv:2405.03988v3 [cs.IR] 26 Dec 2024。版权声明为 Copyright © 2025, Association for the Advancement of Artificial Intelligence（AAAI）。www.aaai.org。All rights reserved.

<!-- 原 PDF 第 1 页 -->

Jian Jia$^1$，Yipei Wang$^{2*}$，Yan Li$^1$，Honggang Chen$^1$，Xuehan Bai$^1$，Zhaocheng Liu$^1$，Jian Liang$^1$，Quan Chen$^{1\dagger}$，Han Li$^1$，Peng Jiang$^1$，Kun Gai$^1$

$^1$ Kuaishou Technology, Beijing, China

$^2$ Southeast University, Nanjing, China

{jiajian, liyan26, chenhonggang, baixuehan03, liuzhaocheng, liangjian03, chenquan06, lihan08, jiangpeng}@kaishou.com；230248984@seu.edu.cn；kun.gai@qq.com

$^*$ 在快手科技实习期间完成的工作。

$^\dagger$ 通讯作者。

## 摘要

当代推荐系统主要依赖 ID 嵌入来捕捉用户与物品之间的潜在关联。然而，这种方法忽略了物品文本描述中丰富的语义信息，导致性能欠佳、泛化较差。利用大语言模型理解并推理文本内容的能力，是推进推荐系统的一条有前景的途径。为此，我们提出由 LLM 驱动的知识自适应推荐框架 LEARN（Llm-driven knowlEdge Adaptive RecommeNdation），把开放世界知识与协同知识结合起来。为应对计算复杂度，我们把预训练 LLM 用作物品编码器，并冻结 LLM 参数，以避免灾难性遗忘、保留开放世界知识。为弥合开放世界域与协同域之间的差距，我们设计了由推荐任务监督、并面向实际工业应用的双塔结构。通过在真实大规模工业数据集上的实验以及在线 A/B 测试，我们证明了该方法在工业应用中的有效性。我们还在六个 Amazon Review 数据集上取得了当时最先进的性能，以验证方法的优越性。

## 引言

受大语言模型（LLM）近来卓越能力与快速发展的启发，如何把 LLM 丰富的开放世界领域知识与强大的逻辑推理能力引入推荐系统（RS），引起了学术界与工业界的关注。

当前的推荐系统严重依赖互不相同的 ID 嵌入，并专注于基于历史交互捕捉潜在的用户—物品关联。这种方法忽略了物品文本描述中的语义信息，并且难以泛化到未见数据，因而在工业冷启动场景和长尾用户推荐上性能欠佳。此外，与计算机视觉（CV）和自然语言处理（NLP）不同，推荐系统中基于 ID 嵌入的建模方式，不利于发展出一个能在下游任务和子场景中都表现良好的预训练模型。

图 1 见原 PDF。

**图 1：“Rec-to-LLM”与“LLM-to-Rec”两类途径的示意。** 以往方法把推荐数据文本化成自然语言对话，再送入 LLM 以得到文本预测。相反，我们的方法 LEARN 把物品文本信息变换为 LLM 嵌入，再投影到协同域，从而与工业推荐任务对齐。图中标有 Textual Adapt（文本适配）、Sequential Adapt（序列适配）、Collaborative Domain of RS（推荐系统的协同域）和 Open-World Domain of LLM（LLM 的开放世界域）。

为缓解当前推荐系统泛化差的问题，已有多种方法利用文本信息，并把 LLM 与推荐系统结合，以生成文本预测，例如用户兴趣（Ren et al. 2024）、下一物品信息（Li, Zhang, and Chen 2023）以及推荐理由（Zhang et al. 2023b）。

以往关于把推荐系统与 LLM 结合的研究（Lyu et al. 2023; Liu et al. 2023; Zhang et al. 2023a; Gao et al. 2023; Sanner et al. 2023; Hou et al. 2024）通常遵循一种统一策略，本文称之为 “Rec-to-LLM” 适配。该策略把用户—物品交互数据从推荐域（目标域）适配到 LLM 开放世界域（源域）的文本格式，如图 1 所示。具体而言，这些方法（Liao et al. 2023; Bao et al. 2023b; Yuan et al. 2023; Bao et al. 2023a; Lin et al. 2023b）设计任务特定的提示，把推荐数据变换为对话格式，并采用下一词元预测损失，使输入组织方式和目标任务与 LLM 预训练阶段一致。

然而，我们的实证考察表明，“Rec-to-LLM” 适配在真实工业应用中并不能带来实际收益。这种无效可以归因于该方法的固有缺陷。第一，鉴于输入长度限制（2K 到 128K）以及 LLM 的计算复杂度，

<!-- 原 PDF 第 2 页 -->

用文本化后的交互去推断或微调 LLM，在工业场景中是负担不起的。在我们的短视频平台上，用户平均每周与近 800 条短视频交互。因此，用 LLM 处理跨越数月的全局用户历史交互，会带来显著的计算负担。第二，用推荐数据微调 LLM 常常导致灾难性遗忘和欠佳的性能，因为推荐系统的协同知识与 LLM 的一般开放世界知识之间存在显著的领域差距。第三，LLM 的训练目标与推荐器的训练目标不对齐，进一步使以往工作无法取得令人满意的性能。

为克服上述局限，我们引入由 LLM 驱动的知识自适应推荐方法 LEARN，旨在把 LLM 的开放世界知识与推荐器的协同知识协同起来。与遵循 “Rec-to-LLM” 适配的以往方法相反，我们的方法把知识从 LLM 适配到推荐（LLM-to-Rec），如图 1 所示。我们把 LLM 用作内容抽取器，并以推荐任务作为训练目标。具体而言，所提出的 LEARN 框架由用户塔和物品塔组成。两个塔都包含内容抽取（Content EXtraction, CEX）模块和偏好对齐（Preference ALignment, PAL）模块。

为应对处理大量用户历史交互时的计算挑战，CEX 模块把预训练 LLM 用作物品编码器，而不是用户偏好编码器。为避免开放世界知识的灾难性遗忘，我们在训练阶段冻结 LLM。此外，为弥合开放世界知识与协同知识之间的领域差距，我们设计了 PAL 模块，并采用推荐任务的自监督训练目标来指导模型优化。LEARN 生成的用户嵌入和物品嵌入被用作在线排序模型的输入。

为在真实工业应用中验证我们的方法，我们构建了一个从真实推荐场景采集的大规模数据集，并在在线 A/B 测试中评估该方法。实验也在 Amazon Reviews 数据集（Ni, Li, and McAuley 2019）上进行，以便与以往方法公平比较。在六个数据集的三项指标上取得了当时最先进的性能，验证了 LEARN 框架的优越性。

我们的贡献概括如下：

- 我们提出由 LLM 驱动的知识自适应推荐框架 LEARN，以便高效地把封装在 LLM 中的开放世界知识聚合进推荐系统。
- 我们提出 CEX 与 PAL 模块，以解决 LLM 中开放世界知识的灾难性遗忘，并利用推荐任务弥合开放世界知识与协同知识之间的领域差距。
- 我们在大规模工业数据集上评估该方法，并通过在线 A/B 测试加以验证，证实其在真实工业场景中的收益。
- 为确认我们的方法优于以往工作，我们在六个公开数据集上进行实验，并在三项指标上达到 SOTA 性能，尤其是 Recall@10 平均提升 13.95%。

## 相关工作

**基于内容的推荐。** 传统推荐系统主要以基于 ID 的嵌入为基础（Hidasi et al. 2015; Kang and McAuley 2018; Sun et al. 2019; Li et al. 2022），它们常常受限于泛化能力。为解决这一问题，大量研究致力于加深对用户与物品内容的理解，以带来增量信息，并增强在线推荐系统的泛化能力。Wu 等人开发了大规模 MIND 文本数据集（Wu et al. 2020），专门用于新闻推荐任务，推动了关于理解文本内容对推荐系统之影响的研究。此后，多项研究利用 BERT（Devlin et al. 2018）模型来改进内容理解。ZESRec（Ding et al. 2021）、UniRec（Hou et al. 2022）和 TBIN（Chen et al. 2023）把预训练 BERT 模型作为编码器，为物品文本描述抽取内容嵌入。Recformer（Li et al. 2023）从 BERT 的训练机制获得启发，把掩码语言模型损失与对比损失结合起来，并重新设计了分词器来编码物品的文本信息。除利用文本信息外，一些方法还试图把视觉信息纳入推荐模型。SimTier 与 MAKE（Sheng et al. 2024）采用 CLIP（Radford et al. 2021）和 MoCo（He et al. 2020）抽取图像特征。MoRec（Yuan et al. 2023）和 MISSRec（Wang et al. 2023）使用 ResNet（He et al. 2016）和 ViT（Dosovitskiy et al. 2020），把物品图像中的视觉内容纳入序列推荐。

**基于 LLM 的推荐。** 由于 LLM 在文本理解与常识推理上展现出强大能力，越来越多的研究探索把 LLM 整合进推荐系统（Lin et al. 2023a; Fan et al. 2023）。第一类冻结 LLM 参数，并把 LLM 当作推荐器。一些工作（Gao et al. 2023; Liu et al. 2023; Zhang et al. 2023a, 2024; Hou et al. 2024; Xi et al. 2023）提出任务特定的提示来构造推荐对话，并用 ChatGPT 生成候选。RLMRec（Ren et al. 2023）利用 ChatGPT 生成用户/物品画像。第二类在专门准备的、来自推荐域的文本数据集上微调 LLM。LlamaRec（Yue et al. 2023）把物品标题作为文本数据，并通过排序分数优化 LLM。TALLRec（Bao et al. 2023b）提出两阶段调优框架，并用 LoRA（Hu et al. 2021）微调 LLM，用于少样本推荐。LLaRA（Liao et al. 2023）把 LLM 提示与 ID 嵌入结合起来，以使 LLM 与已经成熟的序列推荐器对齐。ReLLa（Lin et al. 2023b）提出检索增强的指令调优方法，并在混合数据集上微调 Vicuna（Chiang et al. 2023）。

<!-- 原 PDF 第 3 页 -->

图 2 见原 PDF。

**图 2：由 LLM 驱动的知识自适应推荐（LEARN）框架示意。** LEARN 框架采用双塔架构，包括用户塔和物品塔。用户塔处理历史交互以生成用户嵌入 $E_{\mathrm{user}}$，物品塔处理目标交互以产生物品嵌入 $E_{\mathrm{item}}$。用户塔与物品塔 (a) 利用因果注意力机制。物品塔 (b) 采用自注意力机制。若没有偏好对齐模块，物品塔 (c) 直接把内容嵌入用作物品嵌入。图中还标有文本描述、内容嵌入、偏好对齐模块、内容抽取模块，以及按时间顺序排列的物品。

两类先前研究都把推荐系统的用户—物品交互数据适配到 LLM 的文本对话格式，并利用 LLM 的训练损失来微调模型。这些方法把数据和任务从推荐域（目标域）转移到 LLM 域（源域），因此在本文中称为 “Rec-to-LLM” 方法。

## 方法

### 模型架构

给定按时间顺序排列的用户历史交互，交互序列按某个特定时间戳分成两段：第一段是历史交互序列 $U^{\mathrm{hist}}$，第二段是目标序列 $U^{\mathrm{tar}}$。历史交互与目标交互的长度分别记为 $H$ 与 $T$。我们提出 LEARN 框架，从历史交互中捕捉用户兴趣，并预测用户感兴趣的下一个物品。LEARN 框架由用户塔和物品塔组成，如图 2 所示。

**用户塔。** 用户塔包含内容抽取（CEX）模块和偏好对齐（PAL）模块，如图 3 所示。用户塔的输入是与用户发生交互的历史物品序列。每个物品按照图 3 所示的提示模板进行文本描述。提示被设计得非常简洁，以便有效评估文本描述的信息量。CEX 模块用预训练 LLM 和平均池化层处理这些物品描述，生成内容嵌入 $E_c$。训练期间，预训练 LLM 的参数保持冻结，最后一层解码器的隐状态被用作输出嵌入，随后送入池化层，如图 3(a) 所示。对于整个历史交互序列 $U^{\mathrm{hist}}$，CEX 模块把每个物品的文本描述转换成内容嵌入 $E_c$，形成内容嵌入序列。每个物品由 CEX 模块独立处理。

偏好对齐（PAL）模块捕捉用户偏好，并基于内容嵌入序列输出用户嵌入。PAL 模块以一个内容适配器开始，做维度变换。随后，12 层 Transformer 作为骨干网络，配置遵循 BERT-base（Devlin et al. 2018）。该 Transformer 专门用于学习隐式的物品关系并建模用户偏好。与 BERT 中的双向注意力（Devlin et al. 2018）不同，我们的模块采用因果注意力机制，只关注过去的物品，以建模序列依赖，这与用户偏好的时间顺序性质一致。我们的 Transformer 的输出嵌入再经过在线投影层，产生用户嵌入 $E_{\mathrm{user}} \in \mathbb{R}^{64}$，它们被直接用于图 5 中的在线电子商务推荐器。

**物品塔。** 物品塔处理物品内容的文本描述，并输出面向推荐域的物品嵌入 $E_{\mathrm{item}}$。如图 2 所示，提出了三种物品塔变体。

物品塔 (a) 采用与用户塔相同的因果注意力机制，而物品塔 (b) 采用自注意力机制，每个物品只关注自身内容。尽管有此差异，两种变体都保持相同的模型架构，并与用户塔共享权重。为弥合开放世界域与协同域之间的巨大差距，两种变体都把来自 LLM 的内容嵌入投影为推荐系统中使用的用户/物品嵌入，遵循 “LLM-to-Rec” 途径。相反，物品塔 (c) 直接把内容嵌入 $E_c$ 当作物品嵌入 $E_{\mathrm{item}}$，以 “Rec-to-LLM” 的方式指导用户偏好学习。在训练阶段，物品塔 (a) 把整个用户目标序列 $U^{\mathrm{tar}}$ 作为输入，而物品塔 (b) 和物品塔 (c) 独立处理单个物品。在推断阶段，三种变体都以单个物品为输入，并独立生成物品嵌入。由于表 5 中的性能更优，物品塔 (a) 被采用为默认设置。

<!-- 原 PDF 第 4 页 -->

图 3 见原 PDF。

**图 3：内容抽取（CEX）模块与偏好对齐（PAL）模块示意。** CEX 模块利用预训练 LLM，从物品文本描述生成内容嵌入。PAL 模块接收这些内容嵌入，并把它们从开放世界域投影到在线推荐器所使用的协同域嵌入。

图中物品描述示例为：The item information is given as follows. Item title is “Envy Versatile Five-Petal Flower Earrings 357”. This item belongs to “Earrings” and brand is “Envy”. The price is “9.9 yuan”. The key words of item are “Earrings, Five-Petal Flower Earrings”. This item supports “Returns for Damaged Packages”.（物品信息如下。物品标题是 “Envy Versatile Five-Petal Flower Earrings 357”。该物品属于 “Earrings”，品牌是 “Envy”。价格是 “9.9 yuan”。物品关键词是 “Earrings, Five-Petal Flower Earrings”。该物品支持 “Returns for Damaged Packages”。）

**训练目标。** 为弥合 LLM 开放世界域中的内容嵌入与推荐系统协同域中的用户/物品嵌入之间的差距，我们使训练目标与在线排序模型的目标对齐。

在在线推荐系统中，排序模型计算用户嵌入与图库中所有物品嵌入之间的相似度。相似度最高的前 $k$ 个物品被识别为可能让用户感兴趣的物品。因此，我们采用自监督对比学习机制来建模用户偏好，与在线推荐系统的目标对齐。该方法最大化用户嵌入与相关物品嵌入之间的相似度，同时最小化与不相关物品的相似度。我们从用户历史序列中采样用户嵌入，从同一用户的目标序列中采样物品嵌入，以构造正样本对。同一批次中其他用户的目标物品嵌入被采样为负样本。为充分利用用户交互并捕捉用户长期兴趣，我们采用 dense all action 损失（Pancha et al. 2022）。

从历史序列中采样 $N_h$ 个用户嵌入，从目标序列中采样 $N_t$ 个元素嵌入。这样就可以从单个用户的交互数据构造 $N_h \times N_t$ 个正样本对，以施加 dense all action 损失。$N_h$ 与 $N_t$ 默认设为 10。

**采样策略。** 尽管在构建工业数据集时已经按行为重要性对物品进行了采样，但由于训练资源限制，用户序列长度仍然过长。为此，我们在训练阶段设计了两阶段采样策略。第一阶段，我们从完整的用户历史/目标交互中随机采样，作为用户塔的输入，以确保用于建模用户兴趣的数据是无偏的。对用户交互数据的可视化表明，用户最近交互过的物品更能反映用户当前兴趣，也与用户偏好的目标物品更相关。因此，在第二阶段构造正负样本对时，我们实施一种优先考虑近期物品的样本加权策略。历史/目标序列中第 $i$ 个物品的权重 $\tilde{w}_i$ 计算为：

$$\tilde{w}_i = \frac{w_i}{\max(w)}, \quad \text{其中 } w_i = \log\left(\alpha + i \cdot \frac{\beta - \alpha}{N - 1}\right). \tag{1}$$

超参数 $\alpha$ 与 $\beta$ 设为 10 和 10000。$N$ 是第一阶段采样得到的用户历史/目标交互长度。

## 实验

### 实验设置

**数据集。** 面向工业应用，我们从短视频应用的电子商务平台构建了一个大规模实用推荐数据集。该工业数据集由 1200 万用户与 3100 万物品在 2022 年 6 月至 2023 年 4 月共 10 个月期间的交互组成。前九个月的交互用作历史数据，最后一个月的交互被指定为目标数据。收集六类信息（标题、类目、品牌、价格、关键词、属性）以形成物品描述。为公平比较，我们采用广泛使用的 Amazon Review 数据集（Ni, Li, and McAuley 2019），并遵循与 RecFormer（Li et al. 2023）相同的设置。七个类目被选为预训练数据，另外六个类目被选为微调数据以评估我们的方法。三类信息（标题、类目、品牌）被用来形成物品描述。公开数据集与工业数据集的统计见表 1 和表 2。

**表 1：Amazon Review 数据集的统计。** Avg. n 表示用户交互的平均长度。

| Datasets | #Users | #Items | #Inters. | Avg. n | Density |
| --- | ---: | ---: | ---: | ---: | ---: |
| Pre-training | 3,613,906 | 1,022,274 | 33,588,165 | 9.29 | 9.1e-6 |
| -Training | 3,501,527 | 954,672 | 32,291,280 | 9.22 | 9.0e-6 |
| -Validation | 112,379 | 67,602 | 1,296,885 | 11.54 | 1.7e-4 |
| Scientific | 11,041 | 5,327 | 76,896 | 6.96 | 1.3e-3 |
| Instruments | 27,530 | 10,611 | 231,312 | 8.40 | 7.9e-4 |
| Arts | 56,210 | 22,855 | 492,492 | 8.76 | 3.8e-4 |
| Office | 101,501 | 27,932 | 798,914 | 7.87 | 2.8e-4 |
| Games | 11,036 | 15,402 | 100,255 | 9.08 | 5.9e-4 |
| Pet | 47,569 | 37,970 | 420,662 | 8.84 | 2.3e-4 |

**表 2：工业数据集的统计。**

| Datasets | #Users | #Items | #Inters. | Avg. n | Density |
| --- | ---: | ---: | ---: | ---: | ---: |
| Train | 11,965,799 | 31,044,924 | 1,883,216,224 | 157.38 | 5.07e-6 |
| Test | 239,813 | 6,519,074 | 37,683,369 | 157.13 | 2.41e-5 |

**实现细节。** 采用 Baichuan2-7B（Baichuan 2023）作为 LLM，基于物品文本描述抽取内容嵌入，因为它在理解中文和英文文本方面能力较强。训练阶段 LLM 参数被冻结。所有实验默认采用 AdamW 优化器和余弦调度器。对于工业数据集，训练批大小设为 240，用户历史交互与目标交互的长度由于显存限制分别设为 80 和 40。训练轮数设为 10。使用 Top50 与 Top100 上的命中率（H@50、H@100）和召回率（R@50、R@100）做性能评估。对于 Amazon Review 数据集，预训练阶段批大小设为 1024，微调阶段设为 16。两个阶段的学习率分别为 5e-5 和 2e-5。预训练轮数设为 20，微调轮数设为 200。我们遵循 RecFormer 提出的评估设置，采用留一法（Kang and McAuley 2018）进行评估。使用三项指标——NDCG@10（N@10）、Recall@10（R@10）和 MRR——以确保公平比较。鉴于 Amazon Review 数据集中交互序列长度有限，我们选择在 LEARN 的训练阶段不应用任何采样策略。

<!-- 原 PDF 第 5 页 -->

**表 3：不同推荐模型的性能比较。** 最佳与次佳性能分别以粗体和下划线标出。Improv. 表示相对当时 SOTA 方法 RecFormer 的相对提升。Arts 上 NDCG@10 的 Improv. 在原表中为 “–”。Games 的 FDSA NDCG@10 在 PDF 文本中为 0.0600。

| Dataset | Metric | GRU4Rec | SASRec | BERT4Rec | RecGURU | FDSA | S3-Rec | ZESRec | UniSRec | RecFormer | LEARN | Improv. |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Scientific | NDCG@10 | 0.0826 | 0.0797 | 0.0790 | 0.0575 | 0.0716 | 0.0451 | 0.0843 | 0.0862 | 0.1027 | 0.1060 | +3.21% |
| Scientific | Recall@10 | 0.1055 | 0.1305 | 0.1061 | 0.0781 | 0.0967 | 0.0804 | 0.1260 | 0.1255 | 0.1448 | 0.1594 | +10.08% |
| Instruments | NDCG@10 | 0.0633 | 0.0634 | 0.0707 | 0.0468 | 0.0731 | 0.0797 | 0.0694 | 0.0785 | 0.0830 | 0.0878 | +5.78% |
| Instruments | Recall@10 | 0.0969 | 0.0995 | 0.0972 | 0.0617 | 0.1006 | 0.1110 | 0.1078 | 0.1119 | 0.1052 | 0.1240 | +17.87% |
| Arts | NDCG@10 | 0.1075 | 0.0848 | 0.0942 | 0.0525 | 0.0994 | 0.1026 | 0.0970 | 0.0894 | 0.1252 | 0.1225 | – |
| Arts | Recall@10 | 0.1317 | 0.1342 | 0.1236 | 0.0742 | 0.1209 | 0.1399 | 0.1349 | 0.1333 | 0.1614 | 0.1701 | +5.39% |
| Office | NDCG@10 | 0.0761 | 0.0832 | 0.0972 | 0.0500 | 0.0922 | 0.0911 | 0.0865 | 0.0919 | 0.1141 | 0.1167 | +2.28% |
| Office | Recall@10 | 0.1053 | 0.1196 | 0.1205 | 0.0647 | 0.1285 | 0.1186 | 0.1199 | 0.1262 | 0.1403 | 0.1549 | +10.41% |
| Games | NDCG@10 | 0.0586 | 0.0547 | 0.0628 | 0.0386 | 0.0600 | 0.0532 | 0.0530 | 0.0580 | 0.0684 | 0.0798 | +16.67% |
| Games | Recall@10 | 0.0988 | 0.0953 | 0.1029 | 0.0479 | 0.0931 | 0.0879 | 0.0844 | 0.0923 | 0.1039 | 0.1345 | +29.45% |
| Pet | NDCG@10 | 0.0648 | 0.0569 | 0.0602 | 0.0366 | 0.0673 | 0.0742 | 0.0754 | 0.0702 | 0.0972 | 0.0990 | +1.85% |
| Pet | Recall@10 | 0.0781 | 0.0881 | 0.0765 | 0.0415 | 0.0949 | 0.1039 | 0.1018 | 0.0933 | 0.1162 | 0.1284 | +10.50% |

### Amazon Review 上的性能

**总体性能。** 为验证方法的有效性，Amazon Review 上的性能报告于表 3。我们把 LEARN 与三类方法比较：仅 ID 的方法（GRU4Rec（Hidasi et al. 2015）、SASRec（Kang and McAuley 2018）、BERT4Rec（Sun et al. 2019）、RecGURU（Li et al. 2022）），ID-文本方法（FDSA（Zhang et al. 2019）、S3-Rec（Zhou et al. 2020）），以及仅文本的方法（ZESRec（Ding et al. 2021）、UniSRec（Hou et al. 2022）、RecFormer（Li et al. 2023））。我们的方法相对仅 ID、ID-文本和仅文本的方法都取得了显著提升。具体而言，相对当时的 SOTA 方法 RecFormer，LEARN 在 Scientific、Instruments、Arts、Office、Games 和 Pet 数据集上的 Recall@10 分别提升 10.08%、17.87%、5.39%、10.41%、29.45% 和 10.50%。与 RecFormer 使用掩码语言建模（MLM）损失和两阶段微调过程不同，所提出的 LEARN 模型仅由用户—物品对比损失在单一微调阶段监督。尽管损失约束更少、训练过程更简单，我们的方法仍取得显著的性能提升，进一步证明了框架的有效性。我们还在零样本设置（仅使用预训练阶段）下进行实验，并遵循 RecFormer 的设置。图 4 中的结果表明，LEARN 框架可以被当作预训练推荐模型，并在下游子场景中表现良好。图 4 中其他方法的性能引自 RecFormer。

图 4 见原 PDF。

**图 4：零样本设置下与仅文本 SOTA 方法的性能比较。** 纵轴为 NDCG@10，横轴为 Scientific、Arts、Instruments、Office、Games、Pet。图例包括 Fully-Supervised、UniSRec、ZESRec、Recformer 和 LEARN。柱状数值未从 PDF 文本中可靠抽出，见原 PDF，此处不编造读数。

**消融研究。** 我们性能提升背后的认识是：推荐器的协同域与 LLM 的开放世界域之间存在显著差距。既然内容嵌入作为输入是有信息量的，弥合这一差距的一种有效方式，是把用户—物品交互作为对齐目标，把内容嵌入变换为用户/物品嵌入。我们在表 4 中展示这一认识。首先，我们通过对用户交互过的所有物品的内容嵌入取平均来计算用户嵌入，并直接把物品的内容嵌入用作物品嵌入。由于 LLM 域与推荐域之间没有对齐，我们把该方法称为 “w/o Align”。我们发现 “w/o Align” 的性能很差，这证实了我们的假设：LLM 域的开放世界知识与推荐域的协同知识之间存在显著差距。因此，LLM 生成的内容嵌入不适合直接用于推荐任务。其次，我们把 LLM 生成的内容嵌入用作对齐目标，即图 2 所示的物品塔 (c)。物品塔 (c) 变体通过把推荐域变换到 LLM 域来实现对齐，

<!-- 原 PDF 第 6 页 -->

遵循与以往工作相同的 “Rec-to-LLM” 适配，以便与内容嵌入目标对齐。实验表明，物品塔 (c) 变体不如 LEARN。这是因为推荐知识（目标域）的独特特征在 LLM 的开放世界知识（源域）中没有得到很好的表示。相反，通过把源域投影到目标域空间，LEARN 模型能更好地贴合推荐（目标）分布的复杂性与细微之处，从而带来性能提升。

值得注意的是，对于 Amazon Review 数据集，物品塔 (a) 等价于物品塔 (b)，因为在留一法设置下用户目标序列的长度为 1（Kang and McAuley 2018; Li et al. 2023）。

**表 4：Amazon Review 上对齐策略的消融。** w/o Align 对全部已交互物品的内容嵌入取平均以构造用户嵌入。w/ ItemTower(c) 用物品的内容嵌入监督用户嵌入学习。括号内为相对 w/ ItemTower(c) 的变化，按原表保留。

| Dataset | Metric | w/o Align | w/ ItemTower(c) | LEARN |
| --- | --- | ---: | ---: | ---: |
| Scientific | N@10 | 0.0504 | 0.0978 | 0.1060 (+8.38%) |
| Scientific | R@10 | 0.0813 | 0.1389 | 0.1594 (+14.76%) |
| Instruments | N@10 | 0.0164 | 0.0679 | 0.0878 (+29.31%) |
| Instruments | R@10 | 0.0332 | 0.0940 | 0.1240 (+31.91%) |
| Arts | N@10 | 0.0308 | 0.0900 | 0.1225 (+36.11%) |
| Arts | R@10 | 0.0633 | 0.1337 | 0.1701 (+27.23%) |
| Office | N@10 | 0.0166 | 0.0890 | 0.1167 (+31.12%) |
| Office | R@10 | 0.0312 | 0.1144 | 0.1549 (+35.40%) |
| Games | N@10 | 0.0175 | 0.0555 | 0.0798 (+43.78%) |
| Games | R@10 | 0.0361 | 0.0891 | 0.1345 (+50.95%) |
| Pet | N@10 | 0.0312 | 0.0812 | 0.0990 (+21.92%) |
| Pet | R@10 | 0.0427 | 0.1010 | 0.1284 (+27.13%) |

### 工业数据集上的性能

**消融研究。** 为进一步验证模型设计的合理性，我们在从真实工业场景采集的大规模数据集上进行消融。数据集细节见表 2。如表 5 所示，“w/o Align” 由于 LLM 域与推荐域之间的显著差距而性能最差。在各种对齐策略中，采用物品塔 (a) 的 LEARN 性能最好，其次是物品塔 (b)，物品塔 (c) 最差。我们认为，使用序列到序列对齐的物品塔 (a) 相比物品塔 (b) 所使用的序列到物品对齐，能让模型更好地捕捉用户的长期兴趣。使用 “Rec-to-LLM” 适配、以与内容嵌入目标对齐的物品塔 (c)，表现不如物品塔 (a)。这一结果与 Amazon Review 数据集上的发现一致。由于用户交互长达十个月以上，我们应用式 (1) 提出的样本加权策略，并与随机采样策略比较。如表 5 所示，带样本加权的 LEARN 在 H@100 和 R@100 上分别取得 7.13% 和 7.18% 的提升。

**表 5：工业数据集上对齐策略与采样策略的消融。**

| Ablation | H@50 | R@50 | H@100 | R@100 |
| --- | ---: | ---: | ---: | ---: |
| w/o Align | 0.0069 | 0.0154 | 0.0101 | 0.0210 |
| w/ ItemTower(c) | 0.0292 | 0.0416 | 0.0468 | 0.0626 |
| w/ ItemTower(b) | 0.0313 | 0.0488 | 0.0505 | 0.0675 |
| w/ RandomSample | 0.0440 | 0.0610 | 0.0701 | 0.0905 |
| LEARN (ours) | 0.0477 | 0.0663 | 0.0751 | 0.0970 |

**ID 嵌入与内容嵌入的对比。** 鉴于 ID 嵌入在语义表示和泛化上的局限，我们在大规模真实工业场景中探索 ID 嵌入的替代方案是否可行。我们使用三种物品表示方法：可学习的 ID 嵌入、从预训练 BERT（Yang et al. 2022）抽取的冻结内容嵌入，以及预训练 LLM。ID 嵌入维度设为 64，以与在线系统对齐。如表 6 所示，基于 LLM 的内容嵌入相对 ID 嵌入带来显著性能提升，H@100 从 0.0504 提高到 0.0751，相当于 49.01% 的增强。相对基于 BERT 的内容嵌入，使用 LLM 嵌入的 LEARN 取得 30.38% 的提升。这可以归因于 LLM 嵌入包含更丰富的信息，它们在大规模文本语料上训练。我们的实验结果给出了一个有希望的方向：用语义内容嵌入替换 ID 嵌入。

**表 6：LEARN 框架在工业数据集上不同输入嵌入类型的性能比较。** 可训练参数数量记为 Params。

| Ablation | Params | H@50 | R@50 | H@100 | R@100 |
| --- | ---: | ---: | ---: | ---: | ---: |
| ID-emb | 2.3B | 0.0312 | 0.0499 | 0.0503 | 0.0754 |
| BERT-emb | 86M | 0.0357 | 0.0552 | 0.0576 | 0.0843 |
| LLM-emb (Ours) | 89M | 0.0477 | 0.0663 | 0.0751 | 0.0970 |

**PAL 模块的消融。** 鉴于 LLM 在文本理解与常识推理上的卓越能力，我们把图 2 中 PAL 模块里从头训练的 Transformer 层替换为预训练 LLM（Baichuan2-7B）。为保留开放世界知识，我们用 LoRA（Hu et al. 2021）微调 LLM，并调整不同设置以改变可训练参数数量。如表 7 所示，当可训练参数从 134M 增加到 572M 时，“w/ LLM” 变体的性能从 0.0376 提高到 0.0513。然而，这一性能仍然不及 LEARN，后者使用 12 层从头训练的 Transformer 作为骨干。考虑到 LoRA（Hu et al. 2021）的工作机制，“w/ LLM” 变体的输出特征是开放世界域中训练得到的原始特征与推荐域中训练得到的 LoRA 特征的混合。

**表 7：PAL 模块骨干的消融。** “w/ LLM” 变体用预训练 LLM 作为 PAL 的骨干，而不是 12 层 Transformer。可训练参数数量记为 Params。三行 LoRA 对应不同可训练参数规模。

| Ablation | Finetune | Params | H@100 | R@100 |
| --- | --- | ---: | ---: | ---: |
| w/ LLM | LoRA | 134M | 0.0376 | 0.0560 |
| w/ LLM | LoRA | 286M | 0.0504 | 0.0709 |
| w/ LLM | LoRA | 572M | 0.0513 | 0.0720 |
| LEARN (Ours) | Full | 89M | 0.0751 | 0.0970 |

<!-- 原 PDF 第 7 页 -->

由于 LLM 中冻结参数的数量显著大于可训练的 LoRA 参数，原始特征往往占主导。这些原始特征从开放世界域学习，并由下一词元预测损失监督。相反，LoRA 特征在推荐域中训练，并由对比损失监督。两类特征之间的这种差异，使混合特征无法达到最优性能。

### 在线 A/B 实验

我们通过在线 A/B 测试，在一个日活跃用户超过 4 亿的流行短视频流平台的排序模型上评估 LEARN 框架。我们的方法自 2024 年 1 月起部署于短视频信息流广告场景。更多细节见补充材料（本 PDF 未收录补充材料正文）。

**带 LEARN 适配器的排序模型。** 为使 LEARN 生成的用户嵌入和物品嵌入更好地与在线排序模型对齐，我们在基线模型之上引入了 LEARN-Adaptor。如图 5 所示，基线模型由原始排序模型组成，它以现有在线特征为输入（在图 5 中记为 “Other”）。LEARN-Adaptor 模块包括一个融合模块（两个线性层）和一个 MLP，它们通过转化率（CVR）损失把用户嵌入和物品嵌入聚合成融合嵌入。融合嵌入连同 LEARN 的用户嵌入、物品嵌入以及现有在线特征被拼接后送入排序模型。

图 5 见原 PDF。

**图 5：在线排序模型结构示意。** 图中标有 LEARN-Adaptor、排序模型、CVR 损失、MLP、融合嵌入、用户嵌入、物品嵌入、融合模块、拼接，以及现有在线特征（Other）。

**AUC 评估。** AUC 评估在该短视频应用电子商务平台的十亿规模数据集上进行。遵循常见的工业实践，我们采用 UAUC 和 WUAUC 指标，因为它们能更准确地评估每个用户的排序性能，并更好地反映用户体验。具体而言，UAUC 通过对用户施加均匀权重，来反映长尾用户的性能。如表 8 所示，我们的方法优于基线模型，UAUC 提升 0.84 个百分点（pp），WUAUC 提升 0.76 pp。这些收益可以归因于 LEARN 框架更强的泛化能力，它有效捕捉了长尾用户的兴趣。为进一步验证这一假设，我们进行了更全面的分析。我们根据历史交互频率把用户和物品分成三类。如表 9 所示，LEARN 带来显著的性能增强，对冷启动和长尾的用户与物品尤其如此，进一步证实了我们的方法对购买历史稀疏的用户和物品的泛化能力。

**表 8：我们电子商务平台上的 AUC 结果。**

| Method | UAUC | WUAUC |
| --- | ---: | ---: |
| Baseline | 0.6885 | 0.7002 |
| LEARN (Ours) | 0.6969 (+0.84pp) | 0.7078 (+0.76pp) |

**表 9：三类用户与物品的收入提升。** “Proportion” 表示各类别中用户/物品的百分比。

| Level | Type | Proportion | Revenue | AUC |
| --- | --- | ---: | ---: | ---: |
| User | cold-start | 7.16% | +1.56% | +0.17pp |
| User | long-tail | 27.54% | +5.79% | +0.68pp |
| User | others | 65.30% | +0.32% | +0.021pp |
| Item | cold-start | 3.15% | +8.77% | +0.29pp |
| Item | long-tail | 26.47% | +4.63% | +0.21pp |
| Item | others | 70.38% | +0.35% | +0.01pp |

**在线收入提升。** 我们把平台 20% 的流量分配给我们提出的 LEARN 和基线模型。实验在实时系统中进行 9 天。结果如图 6 所示。LEARN 框架在收入和 CVR 上都表现出稳定而显著的增长。考虑到在线推荐模型的收入以千万元计，即使 2% 的提升也非常显著。

图 6 见原 PDF。

**图 6：在线 A/B 测试期间 CVR 与收入的提升。** 相对基线方法，LEARN 取得稳定而显著的增长。横轴为 Time (days)，约 1 至 9 天；纵轴为提升百分比。逐日读数未从文本可靠抽出，见原 PDF。

## 结论

我们探索把 LLM 与推荐系统结合，并提出 LEARN 框架以取得显著的业务收益。LEARN 框架包括 CEX 与 PAL 模块。CEX 模块使用预训练 LLM 为每个物品抽取内容嵌入，而 PAL 模块把这些嵌入从开放世界域投影到推荐域中的用户/物品嵌入。在工业数据集和公开的 Amazon Review 数据集上取得的当时最先进性能，证明了 LEARN 框架的优越性能。

<!-- 原 PDF 第 8 页 -->

## 参考文献

Baichuan. 2023. Baichuan 2：开放的大规模语言模型。arXiv preprint arXiv:2309.10305.

Bao, K.; Zhang, J.; Wang, W.; Zhang, Y.; Yang, Z.; Luo, Y.; Feng, F.; He, X.; and Tian, Q. 2023a. 推荐系统中大语言模型的两步落地范式。arXiv preprint arXiv:2308.08434.

Bao, K.; Zhang, J.; Zhang, Y.; Wang, W.; Feng, F.; and He, X. 2023b. TALLRec：使大语言模型与推荐对齐的有效且高效的调优框架。In Proceedings of the 17th ACM Conference on Recommender Systems, 1007–1014.

Chen, S.; Li, X.; Dong, J.; Zhang, J.; Wang, Y.; and Wang, X. 2023. TBIN：为点击率预测建模长文本行为数据。arXiv preprint arXiv:2308.08483.

Chiang, W.-L.; Li, Z.; Lin, Z.; Sheng, Y.; Wu, Z.; Zhang, H.; Zheng, L.; Zhuang, S.; Zhuang, Y.; Gonzalez, J. E.; et al. 2023. Vicuna：一个达到 GPT-4 约 90% ChatGPT 质量的开源聊天机器人。See https://vicuna.lmsys.org (accessed 14 April 2023), 2(3): 6.

Devlin, J.; Chang, M.-W.; Lee, K.; and Toutanova, K. 2018. BERT：面向语言理解的深度双向 Transformer 预训练。arXiv preprint arXiv:1810.04805.

Ding, H.; Ma, Y.; Deoras, A.; Wang, Y.; and Wang, H. 2021. 零样本推荐系统。arXiv preprint arXiv:2105.08318.

Dosovitskiy, A.; Beyer, L.; Kolesnikov, A.; Weissenborn, D.; Zhai, X.; Unterthiner, T.; Dehghani, M.; Minderer, M.; Heigold, G.; Gelly, S.; et al. 2020. 一张图像值 16×16 个词：大规模图像识别的 Transformer。arXiv preprint arXiv:2010.11929.

Fan, W.; Zhao, Z.; Li, J.; Liu, Y.; Mei, X.; Wang, Y.; Tang, J.; and Li, Q. 2023. 大语言模型时代的推荐系统。arXiv preprint arXiv:2307.02046.

Gao, Y.; Sheng, T.; Xiang, Y.; Xiong, Y.; Wang, H.; and Zhang, J. 2023. Chat-REC：走向交互式、可解释的 LLM 增强推荐系统。arXiv preprint arXiv:2303.14524.

He, K.; Fan, H.; Wu, Y.; Xie, S.; and Girshick, R. 2020. 用于无监督视觉表示学习的动量对比。In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition, 9729–9738.

He, K.; Zhang, X.; Ren, S.; and Sun, J. 2016. 用于图像识别的深度残差学习。In Proceedings of the IEEE conference on computer vision and pattern recognition, 770–778.

Hidasi, B.; Karatzoglou, A.; Baltrunas, L.; and Tikk, D. 2015. 用循环神经网络做会话推荐。arXiv preprint arXiv:1511.06939.

Hou, Y.; Mu, S.; Zhao, W. X.; Li, Y.; Ding, B.; and Wen, J.-R. 2022. 走向推荐系统的通用序列表示学习。In Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, 585–593.

Hou, Y.; Zhang, J.; Lin, Z.; Lu, H.; Xie, R.; McAuley, J.; and Zhao, W. X. 2024. 大语言模型是推荐系统的零样本排序器。In European Conference on Information Retrieval, 364–381. Springer.

Hu, E. J.; Shen, Y.; Wallis, P.; Allen-Zhu, Z.; Li, Y.; Wang, S.; Wang, L.; and Chen, W. 2021. LoRA：大语言模型的低秩适配。arXiv preprint arXiv:2106.09685.

Kang, W.-C.; and McAuley, J. 2018. 自注意力序列推荐。In 2018 IEEE international conference on data mining (ICDM), 197–206. IEEE.

Li, C.; Zhao, M.; Zhang, H.; Yu, C.; Cheng, L.; Shu, G.; Kong, B.; and Niu, D. 2022. RecGURU：面向跨域推荐的广义用户表示的对抗学习。In Proceedings of the fifteenth ACM international conference on web search and data mining, 571–581.

Li, J.; Wang, M.; Li, J.; Fu, J.; Shen, X.; Shang, J.; and McAuley, J. 2023. 文本就是你所需要的一切：为序列推荐学习语言表示。In Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, 1258–1267.

Li, L.; Zhang, Y.; and Chen, L. 2023. 面向高效的基于 LLM 的推荐的提示蒸馏。In Proceedings of the 32nd ACM International Conference on Information and Knowledge Management, 1348–1357.

Liao, J.; Li, S.; Yang, Z.; Wu, J.; Yuan, Y.; Wang, X.; and He, X. 2023. LLaRA：使大语言模型与序列推荐器对齐。arXiv preprint arXiv:2312.02445.

Lin, J.; Dai, X.; Xi, Y.; Liu, W.; Chen, B.; Li, X.; Zhu, C.; Guo, H.; Yu, Y.; Tang, R.; et al. 2023a. 推荐系统如何从大语言模型中受益：综述。arXiv preprint arXiv:2306.05817.

Lin, J.; Shan, R.; Zhu, C.; Du, K.; Chen, B.; Quan, S.; Tang, R.; Yu, Y.; and Zhang, W. 2023b. ReLLa：用于推荐中终身序列行为理解的检索增强大语言模型。arXiv preprint arXiv:2308.11131.

Liu, J.; Liu, C.; Lv, R.; Zhou, K.; and Zhang, Y. 2023. ChatGPT 是好的推荐器吗？一项初步研究。arXiv preprint arXiv:2304.10149.

Lyu, H.; Jiang, S.; Zeng, H.; Xia, Y.; and Luo, J. 2023. LLM-Rec：通过提示大语言模型做个性化推荐。arXiv preprint arXiv:2307.15780.

Ni, J.; Li, J.; and McAuley, J. 2019. 用远距离标注的评论和细粒度方面为推荐提供依据。In Proceedings of the 2019 conference on empirical methods in natural language processing and the 9th international joint conference on natural language processing (EMNLP-IJCNLP), 188–197.

Pancha, N.; Zhai, A.; Leskovec, J.; and Rosenberg, C. 2022. PinnerFormer：Pinterest 上用户表示的序列建模。In Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining, 3702–3712.

<!-- 原 PDF 第 9 页 -->

Radford, A.; Kim, J. W.; Hallacy, C.; Ramesh, A.; Goh, G.; Agarwal, S.; Sastry, G.; Askell, A.; Mishkin, P.; Clark, J.; et al. 2021. 从自然语言监督中学习可迁移的视觉模型。In International conference on machine learning, 8748–8763. PMLR.

Ren, X.; Wei, W.; Xia, L.; Su, L.; Cheng, S.; Wang, J.; Yin, D.; and Huang, C. 2023. 用大语言模型做推荐的表示学习。arXiv preprint arXiv:2310.15950.

Ren, X.; Wei, W.; Xia, L.; Su, L.; Cheng, S.; Wang, J.; Yin, D.; and Huang, C. 2024. 用大语言模型做推荐的表示学习。In Proceedings of the ACM on Web Conference 2024, 3464–3475.

Sanner, S.; Balog, K.; Radlinski, F.; Wedin, B.; and Dixon, L. 2023. 大语言模型是语言与物品偏好的有竞争力的近冷启动推荐器。In Proceedings of the 17th ACM conference on recommender systems, 890–896.

Sheng, X.-R.; Yang, F.; Gong, L.; Wang, B.; Chan, Z.; Zhang, Y.; Cheng, Y.; Zhu, Y.-N.; Ge, T.; Zhu, H.; et al. 2024. 用多模态表示增强淘宝展示广告：挑战、方法与认识。arXiv preprint arXiv:2407.19467.

Sun, F.; Liu, J.; Wu, J.; Pei, C.; Lin, X.; Ou, W.; and Jiang, P. 2019. BERT4Rec：用 Transformer 双向编码器表示做序列推荐。In Proceedings of the 28th ACM international conference on information and knowledge management, 1441–1450.

Wang, J.; Zeng, Z.; Wang, Y.; Wang, Y.; Lu, X.; Li, T.; Yuan, J.; Zhang, R.; Zheng, H.-T.; and Xia, S.-T. 2023. MISSRec：面向推荐的多模态兴趣感知序列表示的预训练与迁移。In Proceedings of the 31st ACM International Conference on Multimedia, 6548–6557.

Wu, F.; Qiao, Y.; Chen, J.-H.; Wu, C.; Qi, T.; Lian, J.; Liu, D.; Xie, X.; Gao, J.; Wu, W.; et al. 2020. MIND：一个大规模新闻推荐数据集。In Proceedings of the 58th annual meeting of the association for computational linguistics, 3597–3606.

Xi, Y.; Liu, W.; Lin, J.; Zhu, J.; Chen, B.; Tang, R.; Zhang, W.; Zhang, R.; and Yu, Y. 2023. 用来自大语言模型的知识增强走向开放世界推荐。arXiv preprint arXiv:2306.10933.

Yang, A.; Pan, J.; Lin, J.; Men, R.; Zhang, Y.; Zhou, J.; and Zhou, C. 2022. Chinese CLIP：中文对比视觉—语言预训练。arXiv preprint arXiv:2211.01335.

Yuan, Z.; Yuan, F.; Song, Y.; Li, Y.; Fu, J.; Yang, F.; Pan, Y.; and Ni, Y. 2023. 推荐系统下一步往何处去？重新审视基于 ID 与基于模态的推荐模型。In Proceedings of the 46th International ACM SIGIR Conference on Research and Development in Information Retrieval, 2639–2649.

Yue, Z.; Rabhi, S.; Moreira, G. d. S. P.; Wang, D.; and Oldridge, E. 2023. LlamaRec：用大语言模型做排序的两阶段推荐。arXiv preprint arXiv:2311.02089.

Zhang, J.; Bao, K.; Zhang, Y.; Wang, W.; Feng, F.; and He, X. 2023a. ChatGPT 对推荐公平吗？评估大语言模型推荐中的公平性。In Proceedings of the 17th ACM Conference on Recommender Systems, 993–999.

Zhang, J.; Xie, R.; Hou, Y.; Zhao, W. X.; Lin, L.; and Wen, J.-R. 2023b. 把推荐当作指令遵循：一种由大语言模型赋能的推荐方法。arXiv preprint arXiv:2305.07001.

Zhang, T.; Zhao, P.; Liu, Y.; Sheng, V. S.; Xu, J.; Wang, D.; Liu, G.; Zhou, X.; et al. 2019. 面向序列推荐的特征级更深自注意力网络。In IJCAI, 4320–4326.

Zhang, Y.; Yu, W.; Zhang, E.; Chen, X.; Hu, L.; Jiang, P.; and Gai, K. 2024. RecGPT：通过 ChatGPT 训练范式为序列推荐生成个性化提示。arXiv preprint arXiv:2404.08675.

Zhou, K.; Wang, H.; Zhao, W. X.; Zhu, Y.; Wang, S.; Zhang, F.; Wang, Z.; and Wen, J.-R. 2020. S3-Rec：用互信息最大化做序列推荐的自监督学习。In Proceedings of the 29th ACM international conference on information & knowledge management, 1893–1902.

<!-- 译完 -->
