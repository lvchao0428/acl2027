# LEARN: Knowledge Adaptation from Large Language Model to Recommendation for Practical Industrial Application

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`LEARN-2405.03988.pdf`。

说明：该文正文节标题未编号。以下按出现顺序译前两节 Introduction 与 Related Work。

## Abstract 摘要

当代推荐系统主要依赖 ID 嵌入来捕捉用户与物品之间的潜在关联。然而，这一做法忽略了物品文本描述中蕴含的丰富语义信息，导致表现欠佳、泛化较差。利用大语言模型理解文本内容并对其推理的能力，为推进推荐系统提供了一条有希望的途径。为此，我们提出 LEARN（Llm-driven knowlEdge Adaptive RecommeNdation）框架，把开放世界知识与协同知识结合起来。我们用预训练 LLM 作为物品编码器，并冻结 LLM 参数，以避免灾难性遗忘并保留开放世界知识，从而应对计算复杂度方面的顾虑。为弥合开放世界领域与协同领域之间的差距，我们设计了由推荐任务监督、并面向实际工业应用裁剪的双塔结构。通过在真实大规模工业数据集上的实验以及在线 A/B 测试，我们证明该方法在工业应用中的效力。我们还在六个 Amazon Review 数据集上取得最先进表现，以验证方法的优越性。

## Introduction 引言

受大语言模型（large language models, LLMs）近期出色能力与快速发展的启发，如何把 LLM 丰富的开放世界领域知识和强大的逻辑推理能力引入推荐系统（recommendation systems, RS），引起了学术界和工业界的关注。

当前 RS 严重依赖彼此区分的 ID 嵌入，并专注于基于历史交互捕捉潜在的用户–物品关联。这一做法忽略了物品文本描述中的语义信息，也难以泛化到未见数据，因而在工业冷启动场景和长尾用户推荐中表现欠佳。此外，与计算机视觉（computer vision, CV）和自然语言处理（natural language processing, NLP）领域不同，RS 中基于 ID 嵌入的建模方式不利于发展出一个能在下游任务和子场景上表现良好的预训练模型。

为缓解当前 RS 泛化差的问题，已有多种方法利用文本信息，并把 LLM 与 RS 结合起来，以生成文本预测，例如用户兴趣（Ren et al. 2024）、下一项物品信息（Li, Zhang, and Chen 2023）以及推荐理由（Zhang et al. 2023b）。

此前关于把推荐系统与 LLM 整合的研究（Lyu et al. 2023; Liu et al. 2023; Zhang et al. 2023a; Gao et al. 2023; Sanner et al. 2023; Hou et al. 2024）通常遵循一种统一策略，本文称之为 “Rec-to-LLM” 适配。该策略把用户–物品交互数据从推荐领域（目标领域）适配到 LLM 开放世界领域（源领域）的文本格式，如图 1 所示。具体而言，这些方法（Liao et al. 2023; Bao et al. 2023b; Yuan et al. 2023; Bao et al. 2023a; Lin et al. 2023b）设计任务特定的提示，把推荐数据转换为对话格式，并采用下一个 token 的预测损失，使输入组织方式和目标任务与 LLM 预训练阶段对齐。

然而，我们的实证调查表明，“Rec-to-LLM” 适配在真实工业应用中未能带来实际收益。这种无效可以归因于该方法固有的不足。第一，鉴于输入长度限制（2K 到 128K）以及 LLM 的计算复杂度，在工业场景中用文本化的交互去推理或微调 LLM 是负担不起的。在我们的短视频平台上，用户平均每周与近 800 条短视频交互。因此，用 LLM 处理跨越数月的全局用户历史交互会带来显著的计算负担。第二，用推荐数据微调 LLM 常常导致灾难性遗忘和欠佳表现，原因是 RS 的协同知识与 LLM 的一般开放世界知识之间存在显著的领域差距。第三，LLM 的训练目标与推荐器之间的错位，进一步使先前工作难以取得令人满意的表现。

为克服上述局限，我们引入 LEARN（Llm-driven knowlEdge Adaptive RecommeNdation）方法，旨在把 LLM 的开放世界知识与推荐器的协同知识协同起来。与遵循 “Rec-to-LLM” 适配的先前方法相反，我们的方法把知识从 LLM 适配到推荐（LLM-to-Rec），如图 1 所示。我们把 LLM 用作内容抽取器，并以推荐任务作为训练目标。具体而言，所提出的 LEARN 框架由一个用户塔和一个物品塔组成。两个塔都包含内容抽取（Content EXtraction, CEX）模块和偏好对齐（Preference ALignment, PAL）模块。为应对处理大量用户历史交互所带来的计算挑战，CEX 模块把预训练 LLM 用作物品编码器，而不是用户偏好编码器。为避免开放世界知识的灾难性遗忘，我们在训练阶段冻结 LLM。此外，为弥合开放世界知识与协同知识之间的领域差距，我们设计 PAL 模块，并采用推荐任务的自监督训练目标来指导模型优化。LEARN 生成的用户嵌入和物品嵌入被作为在线排序模型的输入。

为在真实工业应用中验证我们的方法，我们构建了一个从真实推荐场景收集的大规模数据集，并在在线 A/B 测试中评估该方法。实验也在 Amazon Reviews 数据集上进行（Ni, Li, and McAuley 2019），以便与先前方法公平比较。在六个数据集的三项指标上取得了最先进表现，验证了 LEARN 框架的优越性。

我们的贡献概括如下：

- 我们提出 LEARN（Llm-driven knowlEdge Adaptive RecommeNdation）框架，以高效地把封装在 LLM 中的开放世界知识聚合进 RS。
- 我们提出 CEX 和 PAL 模块，以解决 LLM 中开放世界知识的灾难性遗忘，并用推荐任务弥合开放世界知识与协同知识之间的领域差距。
- 我们在大规模工业数据集上评估该方法，并通过在线 A/B 测试加以验证，确认其在真实工业场景中的收益。
- 为确认该方法相对先前工作的优越性，我们在六个公开数据集上做实验，并在三项指标上取得 SOTA 表现，尤其是在 Recall@10 上带来平均 13.95% 的提升。

图 1：“Rec-to-LLM” 与 “LLM-to-Rec” 途径的示意。先前方法把推荐数据文本化为自然语言对话，再送入 LLM 以得到文本预测。相比之下，我们的方法 LEARN 把物品文本信息变换为 LLM 嵌入，再投影到协同领域，以实现对工业推荐任务的对齐。图中 “CollaborativeDomainofRS”“Open-WorldDomainofLLM”“TextualAdapt”“SequentialAdapt” 等标签因抽取粘连，【抽取不清】。

## Related Work 相关工作

### Content-based Recommendation. 基于内容的推荐

传统 RS 主要基于 ID 嵌入（Hidasi et al. 2015; Kang and McAuley 2018; Sun et al. 2019; Li et al. 2022），常常泛化能力有限。为解决这一点，大量研究聚焦于加深对用户和物品内容的理解，以带来增量信息，并增强在线 RS 的泛化能力。Wu et al. 开发了大规模 MIND 文本数据集（Wu et al. 2020），专门用于新闻推荐任务，推进了关于理解文本内容对 RS 推荐系统之影响的研究。在此之后，多项研究利用 BERT（Devlin et al. 2018）模型来改善内容理解。ZESRec（Ding et al. 2021）、UniRec（Hou et al. 2022）和 TBIN（Chen et al. 2023）把预训练 BERT 模型作为编码器，为物品文本描述抽取内容嵌入。Recformer（Li et al. 2023）从 BERT 的训练机制获得启发，把掩码语言模型损失与对比损失结合起来，并重新设计分词器以编码物品的文本信息。除利用文本信息外，一些方法也尝试把视觉信息纳入推荐模型。SimTier 和 MAKE（Sheng et al. 2024）采用 CLIP（Radford et al. 2021）和 MoCo（He et al. 2020）来抽取图像特征。MoRec（Yuan et al. 2023）和 MISSRec（Wang et al. 2023）在序列推荐中用 ResNet（He et al. 2016）和 ViT（Dosovitskiy et al. 2020）纳入来自物品图像的视觉内容。

### LLM-based Recommendation. 基于 LLM 的推荐

由于 LLM 在文本理解和常识推理上展现出的强大能力，越来越多的研究在探索把 LLM 整合进推荐系统（RS）（Lin et al. 2023a; Fan et al. 2023）。第一类冻结 LLM 参数，并把 LLM 当作推荐器。一些工作（Gao et al. 2023; Liu et al. 2023; Zhang et al. 2023a, 2024; Hou et al. 2024; Xi et al. 2023）提出任务特定的提示来构造推荐对话，并用 ChatGPT 生成候选。RLMRec（Ren et al. 2023）利用 ChatGPT 生成用户／物品画像。第二类在来自推荐领域的、专门准备的文本数据集上微调 LLM。LlamaRec（Yue et al. 2023）把物品标题作为文本数据，并通过排序分数优化 LLM。TALLRec（Bao et al. 2023b）提出两阶段调优框架，并用 LoRA（Hu et al. 2021）微调 LLM，用于少样本推荐。LLaRA（Liao et al. 2023）把 LLM 提示与 ID 嵌入结合起来，以使 LLM 与已经成熟的序列推荐器对齐。ReLLa（Lin et al. 2023b）提出一种检索增强的指令调优方法，并在混合数据集上微调 Vicuna（Chiang et al. 2023）。

两类先前研究都把推荐系统的用户–物品交互数据适配为 LLM 的文本对话格式，并用 LLM 的训练损失来微调模型。这些方法把数据和任务从推荐领域（目标领域）转移到 LLM 领域（源领域），因此在本文中被称为 “Rec-to-LLM” 方法。

图 2：LEARN（Llm-driven knowlEdge Adaptive RecommeNdation）框架示意。LEARN 采用双塔架构，包含用户塔和物品塔。用户塔处理历史交互以生成用户嵌入 \(E_{user}\)，物品塔处理目标交互以产生物品嵌入 \(E_{item}\)。User Tower 与 Item Tower (a) 利用因果注意力机制。Item Tower (b) 采用自注意力机制。若没有偏好对齐模块，Item Tower (c) 直接把内容嵌入用作物品嵌入。图中 Content Extraction Module、Preference Alignment Module、Text Description、Content Embedding、User Embedding、Item Embedding、chronological order 等标签可读；带乱码下标的嵌入符号【抽取不清】。
