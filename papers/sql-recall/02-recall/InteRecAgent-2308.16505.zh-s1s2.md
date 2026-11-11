# Recommender AI Agent: Integrating Large Language Models for Interactive Recommendations

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`InteRecAgent-2308.16505.pdf`。

## Abstract 摘要

推荐模型擅长利用大量用户行为数据提供领域特定的物品推荐。尽管它们能够充当轻量的领域专家，却难以完成提供解释、参与对话等多样化任务。另一方面，大语言模型（large language models, LLMs）代表了通向通用人工智能的重要一步，在指令理解、常识推理和人机交互上展现出显著能力。然而，LLM 缺少领域特定物品目录和行为模式的知识，尤其是在偏离一般世界知识的领域，例如在线电子商务。为每个领域微调 LLM 既不经济也不高效。本文弥合推荐模型与 LLM 之间的差距，结合各自的长处，以创建一个多用途且可交互的推荐系统。我们引入一个高效框架 InteRecAgent，它把 LLM 用作大脑，把推荐模型用作工具。我们首先勾勒把 LLM 转变为 InteRecAgent 所需的一组最小必要工具。然后，我们在 InteRecAgent 内提出一种高效的任务执行工作流，纳入记忆组件、动态示例增强的任务规划以及反思等关键组件。通过整合 LLM，InteRecAgent 使传统推荐系统——例如那些基于 ID 的矩阵分解模型——成为带有自然语言接口的交互系统。在若干公开数据集上的实验结果表明，InteRecAgent 作为对话推荐系统取得了令人满意的表现，优于通用 LLM。InteRecAgent 的源代码发布于 https://aka.ms/recagent 。

## 1 Introduction 引言

推荐系统（recommender systems, RSs）已经成为数字图景中的必要组成部分，在帮助用户驾驭电子商务和娱乐等各种领域中大量选择方面发挥着重要作用。通过分析用户偏好、历史数据和上下文信息，这些系统可以提供迎合个人口味的个性化推荐。多年来，推荐系统已经从简单的协同过滤算法演进为整合深度学习技术的更先进混合方法。然而，随着用户越来越依赖对话界面来发现和探索产品，越来越需要开发更复杂、更具交互性的推荐系统，能够以对话方式有效理解并回应用户多样的询问和意图。

大语言模型（LLMs），例如 GPT-3（Brown et al. 2020）和 PaLM（Chowdhery et al. 2022），近年来取得了显著进展，在通用人工智能上展示了出色能力，并正在变革自然语言处理领域。多种实际任务可以通过用户与 ChatGPT\(^1\) 和 Claude\(^2\) 等 AI 智能体对话的方式完成。凭借理解上下文、生成类人文本和执行复杂推理任务的能力，LLM 可以促进用户与 RS 之间更有吸引力和更直观的交互，从而为下一代 RS 提供有希望的前景。通过把 LLM 整合进 RS，有可能提供超出传统推荐技术的、更自然、更顺畅的用户体验，促成对用户偏好更及时的理解，并给出更全面、更有说服力的建议。

尽管有这些潜力，把 LLM 用于推荐系统并非没有挑战和局限。第一，虽然 LLM 在来自互联网的大量文本数据上预训练，覆盖多个领域并展示了令人印象深刻的一般世界知识，它们仍可能无法捕捉细粒度的、领域特定的行为模式，尤其是在训练数据规模巨大的领域。第二，如果领域数据是私有的、在互联网上较少公开可得，LLM 可能难以很好地理解该领域。第三，LLM 缺少预训练数据收集之后发布的新物品的知识，而用最新数据微调可能贵得令人却步。相比之下，领域内模型可以自然地应对这些挑战。克服这些局限的一种常见范式，是把 LLM 与领域内模型结合起来，从而填补差距并产生更强的智能。显著的例子包括 AutoGPT\(^3\)、HuggingGPT（Shen et al. 2023）和 Visual ChatGPT（Wu et al. 2023）。核心想法是把 LLM 用作“大脑”，把领域内模型用作在处理领域特定任务时扩展 LLM 能力的“工具”。

本文把 LLM 与传统推荐模型连接起来，用于交互式推荐系统。我们提出 InteRecAgent（Interactive Recommender Agent），一个明确为迎合推荐系统的特定要求和细微差别而设计的框架，从而在 LLM 的一般能力与推荐领域的专门需求之间建立更有效的连接。该框架由三组不同的工具组成，包括查询、检索和排序，旨在迎合用户日常询问的多样需求。鉴于物品候选的数量通常很大，把物品名称作为带提示的观察存入工具的输入和输出是不切实际的。因此，我们引入一条“共享候选总线”（shared candidate bus）来存储中间状态，并促进工具之间的通信。为增强处理长对话乃至终身对话的能力，我们引入“长期与短期用户画像”（long-term and short-term user profile）模块，以追踪用户的偏好和历史，并作为排序工具的输入来改善个性化。“共享候选总线”连同“长期与短期用户画像”构成 InteRecAgent 框架内的高级记忆机制。

关于任务规划，我们采用“先规划再执行”（plan-first execution）策略，而不是逐步方式。该策略不仅降低 LLM 的推理成本，还可以与动态示例策略无缝整合，以提升规划生成的质量。具体而言，InteRecAgent 一次生成工具调用的全部步骤，并严格遵循执行计划来完成任务。对话期间，InteRecAgent 解析用户意图，并检索与当前意图最相似的若干示例。这些动态检索到的示例帮助 LLM 形成正确的任务执行计划。此外，我们实现一种反思策略：另一个 LLM 充当批评者，评估结果质量并识别任务执行期间的任何错误。如果结果不令人满意或检测到错误，InteRecAgent 回退到初始状态，并重复“先规划、再执行工具”的过程。

在 InteRecAgent 中使用 GPT-4 作为 LLM，在我们的实验中产生了令人印象深刻的结果。这自然引出一个有吸引力的问题：是否可能利用一个更小的语言模型来充当大脑？为探索这一点，我们构建了一个模仿数据集，其中的工具规划生成来自 InteRecAgent 与用户模拟器之间的交互，二者都由 GPT-4 驱动。通过用该数据集微调 LlaMA 2（Touvron et al. 2023b）模型，我们创建了 RecLlama。值得注意的是，RecLlama 作为推荐智能体的核心，其有效性超过了若干更大的模型。我们的主要贡献概括如下：

- 我们提出 InteRecAgent，一个紧凑的、基于 LLM 的智能体框架，通过把 LLM 与三组不同的传统推荐工具连接起来，使交互式推荐系统更加易于获得。
- 针对把基于 LLM 的智能体用于推荐系统所带来的挑战，我们引入一套高级模块，包括共享候选总线、长期与短期用户画像、动态示例增强的先规划策略，以及反思策略。
- 为使小语言模型能够充当推荐智能体的大脑，我们创建了一个源自 GPT-4 的模仿数据集。利用该数据集，我们成功微调了一个 70 亿参数的模型，称之为 RecLlama。
- 来自三个公开数据集的实验结果表明 InteRecAgent 的有效性，在世界知识覆盖较少的领域优势尤其显著。

脚注：1 https://chat.openai.com/ ；2 https://claude.ai/ ；3 https://github.com/Significant-Gravitas/Auto-GPT 。

## 2 Related Work 相关工作

### 2.1 Conversational Recommender System 对话推荐系统

对话推荐系统（conversational recommender systems, CRS）的现有研究主要可以分为两个领域（Gao et al. 2021）：基于属性的问答（Zou and Kanoulas 2019; Zou, Chen, and Kanoulas 2020; Xu et al. 2021）和开放式对话（Li et al. 2018; Wang et al. 2022b, 2021）。在基于属性的问答 CRS 中，系统旨在尽可能少的轮次内向用户推荐合适的物品。系统与用户之间的交互主要围绕关于期望物品属性的问答，迭代地细化用户兴趣。该领域的关键研究挑战包括：开发选择所询问属性的策略（Mirzadeh, Ricci, and Bansal 2005; Zhang et al. 2018），以及处理探索–利用权衡（Christakopoulou, Radlinski, and Hofmann 2016; Xie et al. 2021）。在开放式对话 CRS 中，系统处理自由格式的对话数据。该领域最初的研究努力聚焦于利用预训练语言模型做对话理解和回复生成（Li et al. 2018; Penha and Hauff 2020）。后续研究纳入外部知识，以增强开放式 CRS 的表现（Chen et al. 2019; Wang, Su, and Chen 2022; Wang et al. 2022b）。尽管如此，这些方法难以对复杂的用户询问进行推理，也难以与用户保持顺畅沟通。LLM 的出现为革新对话推荐系统的构建提供了机会，有可能应对现有方法的局限并提升整体用户体验。

### 2.2 Enhancing LLMs 增强大语言模型

参数和数据的规模扩大，使 LLM 的能力取得了显著进展，包括上下文学习（Brown et al. 2020; Liu et al. 2021; Rubin, Herzig, and Berant 2021）、指令跟随（Ouyang et al. 2022; Touvron et al. 2023a; OpenAI 2023）、规划与推理（Wei et al. 2022; Wang et al. 2022a; Yao et al. 2022; Yang et al. 2023; Wang et al. 2023b）。在推荐系统中，LLM 的应用正在成为一个快速增长的趋势（Liu et al. 2023a; Dai et al. 2023; Kang et al. 2023; Wang and Lim 2023）。

随着模型展现出涌现智能，研究者开始探索把 LLM 用作自主智能体的潜力（Wang et al. 2023a; Zhao, Jin, and Cheng 2023），并用记忆模块、规划能力和工具使用能力加以增强。例如，（Wang et al. 2023c; Zhong et al. 2023; Liu et al. 2023b）为 LLM 配备了外部记忆，使 LLM 具有成长潜力。关于规划，CoT（Wei et al. 2022; Kojima et al. 2022）和 ReAct（Yao et al. 2022）提议通过逐步推理来增强规划；ToT（Yao et al. 2023）和 GoT（Besta et al. 2023）引入多路径推理以确保一致性和正确性；Self-Refine（Madaan et al. 2023）和 Reflexion（Shinn et al. 2023）引导 LLM 反思错误，最终目标是提高后续解题的成功率。为具备领域特定技能，一些工作（Qin et al. 2023a）研究引导 LLM 使用外部工具，例如网页搜索引擎（Nakano et al. 2021; Shuster et al. 2022）、数学工具（Schick et al. 2023; Thoppilan et al. 2022）、代码解释器（Gao et al. 2023a; Chen et al. 2022）和视觉模型（Wu et al. 2023; Shen et al. 2023）。据我们所知，本文是第一个在推荐系统领域探索 LLM + tools 范式的工作。
