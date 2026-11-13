# Knowledge-Aware Query Expansion with Large Language Models for Textual and Relational Retrieval

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`KAR_arXiv2410.13765.pdf`。

## Abstract 摘要

大语言模型（large language models, LLMs）已被用来生成查询扩展（query expansions），以增强原始查询并改进信息搜索。近期研究还探索向大语言模型提供初始检索结果，从而生成更贴近文档语料的查询扩展。然而，这些方法大多聚焦于增强搜索查询与目标文档之间的文本相似度，忽略了文档关系。对于诸如 “Find me a highly rated camera for wildlife photography compatible with my Nikon F-Mount lenses” 这样的查询，现有方法可能生成语义相似、但在结构上与用户意图无关的扩展。为处理同时带有文本要求与关系要求的半结构化查询，本文提出一种知识感知的查询扩展框架，用来自知识图谱（knowledge graph, KG）的结构化文档关系增强大语言模型。为进一步应对现有基于知识图谱的方法中基于实体打分的局限，我们把文档文本用作丰富的知识图谱节点表示，并在我们的知识感知检索（Knowledge-Aware Retrieval, KAR）中使用基于文档的关系过滤。在三个不同领域数据集上的大量实验表明，与最先进基线相比，我们的方法在文本与关系半结构化检索上具有优势。

## 1 Introduction 引言

大语言模型已被用来为原始查询补充额外上下文，以捕捉目标文档的相似语义，并因此提升检索性能（Gao et al., 2023; Wang et al., 2023）。直接生成会引入幻觉、信息过时以及缺乏领域知识等问题，近期方法（Jagerman et al., 2023; Lei et al., 2024; Shen et al., 2024）探索用初始检索作为上下文来增强大语言模型，例如伪相关反馈（pseudo relevance feedback, PRF）（Lv and Zhai, 2010; Li et al., 2022），从而生成更贴近特定领域文档语料的扩展。

图 1：HyDE（Gao et al., 2023）、RAR（Shen et al., 2024）与 KAR（本文）针对一条半结构化商品搜索查询生成的查询扩展示例。该查询同时具有文本要求与关系要求（Wu et al., 2024b）。HyDE 与 RAR 丰富了文本信息，例如 “wildlife” 与 “highly rated”，但编造了不正确的文档关系，例如 “Nikon Coolpix P1000” 与 “F-Mount lenses” 的兼容性。相比之下，我们的 KAR 利用知识图谱中的文档关系，例如顾客把 “Nikon Z7 II” 与 “F-Mount lenses” 一起购买，从而生成语义相似且结构相关的查询扩展。图中查询为 “Find me a highly rated camera for wildlife photography compatible with my Nikon F-Mount lenses.”。可辨认的商品卡片包括 Nikon Z7 II（Feature: 45.7 megapixels; autofocus…；Description: wildlife flexible lens adapter…；Reviews: 4.5/5 “autofocus fast animals…”；Relations 中 products also bought: Nikon F-Mount lenses，products also viewed: FTZ adapter）、Nikon Coolpix P1000（Feature: impressive 125x zoom for wildlife photography…；Description: built-in lens options inc. Nikon F-Mount lenses…；Reviews: 5 stars “captured wildlife birds without a hitch!”），以及 Nikon camera（Feature: the camera is designed for wildlife photography…；Description: compatible with Nikon F-Mount lenses；Reviews: “This is a great camera for shooting wildlife animals!”）。三种方法标注为 KAR (Ours)、RAR 与 HyDE，并各自经过 Query Expansion 与 Final Retrieval。卡片中的省略号为图内缩写。

尽管这些方法有效，现有工作大多聚焦于增强扩展查询与目标文档文本之间的语义相似度。然而在真实搜索场景中，除文本描述外，文档常常以某些类型的关系相互连接（Talmor and Berant, 2018; Cao et al., 2022）。用户往往以半结构化方式同时查询文本细节与关系细节（Wu et al., 2024b; Patel et al., 2024; Wu et al., 2024a; Boer et al., 2024），以便更好地描述其搜索意图，而现有查询扩展方法忽略了这一点。例如，图 1 中的用户查询同时规定了商品的文本要求 “highly rated” 与 “wildlife photography”，以及关系要求 “compatible with Nikon F-Mount lenses”。现有方法可能就该商品生成语义相似的扩展，但倾向于编造不正确的商品关系，即相机与镜头之间的兼容性，从而导致次优的检索结果。

为处理这类半结构化查询，我们提出一种知识感知的查询扩展框架，用来自知识图谱的结构化文档关系增强大语言模型。我们首先用大语言模型解析原查询中被显式提及的实体，然后检索这些实体的文本文档，以及它们在知识图谱上的关联节点与关系。现有基于知识图谱的问答方法（Yasunaga et al., 2021; Zhang et al., 2022; Taunk et al., 2023）根据查询与实体名称之间的语义相似度（例如 “Nikon camera”）为节点相关性打分，从而滤除无关关系，但它们忽略了用户所查询实体的丰富文本细节，例如 “highly rated” 与 “wildlife”。

为此，我们把文档文本用作丰富的知识图谱节点表示，并使用基于文档的关系过滤来抽取聚焦于查询的关系。随后，以收集到的文本知识与关系知识作为输入，大语言模型生成既贴近文档语料、又保留用户所规定文档关系的查询扩展。扩展后的查询再用于最终检索，即我们的知识感知检索（KAR）。我们在 STaRK 基准（Wu et al., 2024b）的三个文本与关系半结构化检索数据集上进行了大量实验，分别对应商品、学术论文与生物医学搜索。结果表明，我们的方法优于最先进的查询扩展方法，并且与基于大语言模型的检索智能体相比，至少达到相当的性能。

总之，我们做出以下贡献：i) 为处理同时具有文本要求与关系要求的复杂搜索查询，我们提出一种用知识图谱增强大语言模型的知识感知查询扩展框架；ii) 为应对基于实体打分的局限，我们用文档文本作为知识图谱节点表示，并为知识感知检索（KAR）采用基于文档的关系过滤；iii) 在三个半结构化检索数据集上的实验展示了我们方法的优势及其实际适用性。

## 2 Related Work 相关工作

### 2.1 LLM-based Query Expansion 基于大语言模型的查询扩展

查询扩展是信息搜索应用中被广泛采用的技术（Azad and Deepak, 2019）：用额外上下文扩展原始查询，以匹配目标文档。早期研究把初始检索到的文档用作伪相关反馈（PRF）（Yu et al., 2003; Cao et al., 2008; Lv and Zhai, 2010; Li et al., 2022），抽取相关内容作为补充信息。然而，这些方法的有效性受初始检索质量限制。

近年来，大语言模型增强的信息检索成为一个突出方向（Zhu et al., 2023），大语言模型被用来凭借其内在知识生成查询扩展。HyDE（Gao et al., 2023）用大语言模型直接生成回答该查询的假设文档，再用这些文档的嵌入去检索相似的真实文档。Query2Doc（Wang et al., 2023）通过向大语言模型提供少样本示例，进一步提升扩展质量。Jagerman et al. (2023) 也探索把思维链（chain-of-thought）用作扩展。为应对大语言模型可能缺乏特定领域知识这一局限，Shen et al. (2024) 提出检索增强检索（retrieval-augmented retrieval, RAR），把初始检索作为上下文，供大语言模型生成查询扩展。Lei et al. (2024) 让大语言模型先从初始检索中抽取关键信息，再扩展查询。AGR（Chen et al., 2024）设计了 Analyze-Generate-Refine 这一多步查询扩展框架，以便在以初始检索为参照时纳入大语言模型的自我精炼能力。Jia et al. (2024) 也探索了类似的验证策略。尽管有这些进展，现有方法大多聚焦文本相似度，并忽略文档关系。相比之下，我们的知识感知查询扩展用来自知识图谱的结构化文档关系增强大语言模型，以处理半结构化检索任务。

### 2.2 KG-Augmented LLM 知识图谱增强的大语言模型

在更早的研究中，语言模型被用来提供文本嵌入，以增强知识图谱推理任务上的图神经网络（Feng et al., 2020; Lin et al., 2021; Yasunaga et al., 2021; Spillo et al., 2023）。随着大语言模型在各种文本结构上涌现出推理能力，知识图谱反过来被用作结构化知识来源，用事实性或领域特定的信息增强大语言模型，以进行更有依据的推理与生成（Pan et al., 2024）。例如，Think-on-Graph（Sun et al., 2024）进行实体与关系探索，以检索用于问答的相关三元组。Reason-on-Graph（Luo et al., 2024）从知识图谱中检索推理路径，供大语言模型做忠实推理。HyKGE（Jiang et al., 2024）生成假设推理路径，并在知识图谱上加以落实，用于答案生成。LPKG（Wang et al., 2024）从知识图谱构造规划数据，用于复杂问答。图检索增强生成近期也迅速增加（Peng et al., 2024; Xu et al., 2024; He et al., 2024; Hu et al., 2024），它利用知识图谱等图数据作为检索来源，以生成更准确、更有结构的回复。

与这些把大语言模型与知识图谱结合起来的研究相比，我们的工作在两个关键方面不同。第一，先前研究大多聚焦知识图谱问答，其中查询更偏事实，答案被精确编码在知识图谱中。我们的工作聚焦文档检索，其中查询往往更具描述性，也更依赖具体领域。第二，在先前研究中，知识图谱是唯一的检索来源。在我们的工作中，文本文档与知识图谱共同构成半结构化知识来源，其信息覆盖多个方面（Wu et al., 2024b）。检索来源的这种半结构化性质，给有效的知识抽取与检索带来了不同的挑战（Patel et al., 2024; Wu et al., 2024a; Boer et al., 2024）。
