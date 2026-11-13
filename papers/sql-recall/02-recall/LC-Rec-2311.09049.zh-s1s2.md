# Adapting Large Language Models by Integrating Collaborative Semantics for Recommendation

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`LC-Rec-2311.09049.pdf`。

## Abstract 摘要

近来，大语言模型（large language models, LLMs）在推荐系统（recommender systems）中显示出很大潜力，既可以改进现有推荐模型，也可以充当骨干。然而，LLM 与推荐系统之间存在很大的语义鸿沟，因为待推荐物品往往由离散标识符（item ID）索引，而这些标识符处于 LLM 的词表之外。本质上，LLM 捕捉的是语言语义（language semantics），而推荐系统蕴含的是协同语义（collaborative semantics），这使得难以充分运用 LLM 的模型容量来做推荐。

为应对这一挑战，本文提出一种新的、基于 LLM 的推荐模型，称为 LC-Rec。它能更好地为推荐系统整合语言语义与协同语义。我们的方法可以直接从整个物品集合中生成物品来做推荐，而不依赖候选物品。具体而言，我们的方法有两项主要贡献。在物品索引方面，我们设计了一种带有均匀语义映射（uniform semantic mapping）的、基于学习的向量量化方法，它能为物品分配有意义且互不冲突的 ID（称为 item indices）。在对齐调优（alignment tuning）方面，我们提出一系列专门设计的调优任务，以增强 LLM 中对协同语义的整合。我们的微调任务迫使 LLM 深度整合语言语义与协同语义（由学到的物品索引所刻画），从而实现对推荐系统的有效适配。大量实验表明了我们方法的有效性：我们的方法能够超过若干有竞争力的基线，包括传统推荐器以及现有的基于 LLM 的推荐器。代码见于 https://github.com/RUCAIBox/LC-Rec/。

## I. Introduction 引言

如今，推荐系统已成为各种应用平台的必要组成部分，其目标是根据用户的特定偏好，向用户推荐潜在的信息资源。由于用户偏好随时间动态演变，序列推荐（sequential recommendation）因其在捕捉用户行为的序列特征方面的优势，而受到大量研究关注。为构建序列推荐器，现有推荐模型 [1], [2] 大多建立在用户交互日志的序列化格式之上，并以 item ID 为基本单元。

在现有文献中，序列推荐器采用各种深度神经网络，来建模由 item ID 序列表示的用户历史行为，包括 RNN [1], [3]、CNN [4], [5]、GNN [6], [7] 和 Transformer [2], [8]。除用户历史行为之内的协同语义外，一些研究 [9]–[11] 也尝试利用内容信息（例如标题、描述、类别）来增强物品序列建模。此外，预训练语言模型（pre-trained language models, PLMs）也被用于捕捉物品文本中所反映的文本语义 [12]–[15]，以提升推荐表现。

近来，大语言模型（LLMs）的出现在研究社区引发了一场重大变革。由于 LLM 在语义理解与生成方面的出色能力，它们在各种基于语言的任务中显示出很大潜力 [16]。具体而言，也有若干尝试 [17] 把 LLM 适配到推荐系统（recommender systems, RS），以改进物品排序表现 [18]，或增强综合推荐能力 [19]。要构建有能力的、基于 LLM 的推荐模型，一个根本挑战是：LLM 所建模的语言语义，与推荐系统所蕴含的协同语义之间，存在很大鸿沟。关键在于，在现有推荐模型中，用户行为常常被格式化成 item ID 序列（可能还带有特征 ID），而不是文本描述。换句话说，语言模型与推荐模型实际上使用两套不同的词表（token ID 对比 item ID，原文为 “v.s.”）来学习各自的语义空间。这样的语义鸿沟，使得难以充分运用 LLM 的模型容量来处理推荐任务。

为处理这一问题，现有工作可以分成两条主要路线。第一条路线 [18]–[21] 把用户行为言辞化成文本序列（例如，把交互过的物品的标题与类别标签拼接起来），并设计专门的提示，以指示 LLM 完成推荐任务。这一路线只捕捉有限的物品信息（只考虑语言语义），并且不能保证生成域内（in-domain）物品（它依赖一个候选集合）。作为另一条替代路线，若干研究 [22], [23] 设计专门的物品索引机制来构建物品词表，然后学习生成推荐的目标物品。然而，鉴于语义鸿沟很大，简单的做法（例如用普通 item ID 构建词表）或 shadow integration（例如只在目标任务上微调）在把 LLM 适配到推荐系统时都会不那么有效。原文用词为 “shadow integration”。

考虑到这些问题，我们旨在设计一种更有效的语义整合途径，用于构建基于 LLM 的推荐模型。我们从两个主要方面处理这一语义整合问题，即物品索引与对齐调优。对于物品索引，一种理想的分配机制应当产出有意义的（能捕捉物品相似度）、唯一的（没有分配冲突）且可扩展的（能泛化到新物品）ID，以便有效表示物品。对于对齐调优，它应当能够在 LLM 中充分整合语言语义与协同语义，而不是表面地拟合目标推荐任务。总体而言，我们的目标是有效建立这两类不同语义之间的联系，并充分运用 LLM 的模型容量来做序列推荐。

脚注 1：词语 “align” 与 “alignment” 主要指语言语义与协同语义之间的整合，而不是人类对齐（human alignment）[24] 中的含义；后者指示 LLM 遵循人类的价值或偏好。

为此，本文提出 LC-Rec，一种新方法，通过整合语言（Language）与协同（Collaborative）语义，来改进推荐系统中的 LLM。我们的方法以生成方式构建，推荐任务同样被改写成 token 生成任务。要做到这一点，关键在于语言语义与协同语义之间的语义整合，从而使 LLM 做出物品推荐时，就像它们生成普通文本内容一样。我们的方法在上述两个方面做出了两项主要贡献。在物品索引方面，我们提出一种树结构的向量量化（tree-structured vector quantization, VQ）方法，用离散 ID（称为 item indices）来索引物品。这些物品索引基于由 LLM 编码的物品文本嵌入来学习，使学到的 ID 能够捕捉物品之间的内在相似度。然而，原始的 VQ 方法很可能把相同的 ID 分配给多个物品，这在推荐系统中应当避免。为处理这一问题，我们进一步设计了一种均匀语义映射方法，以减轻 ID 分配中的潜在冲突。在对齐调优方面，我们设计一系列特定任务来微调 LLM，以实现语义整合。除序列物品预测之外，我们同时考虑显式的索引–语言对齐，以及隐式的、面向推荐的对齐。我们的微调任务迫使 LLM 深度整合语言语义与协同语义，从而实现对推荐系统的有效适配。

为评估我们的方法，我们在三个真实世界数据集上进行了大量实验。相对若干有竞争力的基线，我们的方法取得了最好的表现。实验结果表明，我们的方法能够经由专门学到的物品索引，有效对齐语言语义与协同语义，从而显著提升推荐表现。本工作的贡献可以概括如下：

- 我们提出 LC-Rec，一个基于 LLM 的序列推荐模型，通过有效整合语言语义与协同语义来构建。LC-Rec 能够以自回归生成的方式完成序列推荐任务，而不依赖候选集合。
- 我们的方法建立在一种专门设计的 VQ 方法之上，它能够捕捉物品相似度，并避免索引分配中的 ID 冲突。进而，我们提出一系列精心设计的调优任务，以经由物品索引实现有效的语义整合。
- 我们基于参数量为 7B 的 LLaMA [25] 实现了我们的方法。在三个公开数据集上的大量实验表明，我们的方法在把协同语义整合进 LLM 方面是有效的。所提出的方法 LC-Rec 在全量排序（full ranking）评测中，相对全部基线方法取得了平均 25.5% 的表现提升。

## II. Related Work 相关工作

### A. Sequential Recommendation 序列推荐

序列推荐旨在通过分析历史交互来推断用户偏好，并预测适合该用户的下一个物品 [1], [2], [8]。许多早期方法常常基于马尔可夫链（Markov Chains）技术 [26], [27]。近来，典型方法转而采用各种深度神经网络，来建模由 item ID 序列表示的用户历史行为，包括 RNN [1], [3]、CNN [4], [5]、GNN [6], [7] 和 Transformer [2], [8]。然而，这些方法只从用户–物品交互中捕捉物品之间的协同关系，而忽略了物品内容信息中丰富的额外信息（例如标题、描述、类别）。因此，若干研究致力于利用与物品相关联的额外信息，来增强 ID 序列建模 [9]–[11]。此外，物品标题与描述固有的自然语言特性，促使许多研究者探索在推荐系统中使用预训练语言模型（PLMs）[12]–[15]。在本文中，我们旨在以更有效的方式把 LLM 与推荐任务结合起来，这一点通过所提出的新物品索引方法与对齐调优方法来达成。

### B. Large Language Models for Recommendation 用于推荐的大语言模型

近来，大语言模型（LLMs）获得了显著的流行度，其应用范围覆盖人工智能的多个领域 [16], [28]–[30]。这在很大程度上归因于它们在语言语义理解与生成方面的优越能力。在推荐系统的语境中，研究者一直在努力把 LLM 适配到推荐系统，以提升推荐表现。一种常见做法是把用户行为表示为文本序列（例如，把历史物品的标题拼接起来），然后设计提示，引导 LLM 执行推荐任务 [31]–[33]。

然而，一个主要挑战仍然存在：LLM 所建模的语言语义与推荐系统所蕴含的协同语义之间有很大鸿沟，而这一鸿沟不能仅靠简单的提示设计来弥合。为处理这一问题，现有工作可以归为两条主要路线。第一条路线是用基于文本的用户行为序列来微调 LLM [19]–[21], [34]。然而，这些方法不能保证生成域内物品。由于有限上下文窗口大小的约束，这些方法只能在给定的候选集合上排序，并且很难应用于全量排序场景。第二条路线保持使用 item ID，或引入独特的物品索引机制。给定纯粹的 item ID 序列，模型被训练来直接生成推荐的目标 item ID [22], [23]。尽管物品索引之间的协同语义得以建立，LLM 所建模的语言语义与这些物品索引并没有被很好地对齐。

此外，我们注意到一些同期工作 [35]–[37]，它们同样认识到推荐任务与自然语言任务之间存在很大语义鸿沟这一问题。例如，TransRec [35] 采用多侧面标识符，把 ID、标题与属性结合起来，以平衡物品的可区分性与语义。CoLLM [36] 把一个外部协同模型的表示作为输入的一部分，从而把协同语义纳入 LLM。CLLM4Rec [37] 分别基于推荐任务与内容（例如评论）生成任务，学习成对的用户／物品嵌入。它引入一种互正则损失（mutually-regularization loss），用于这两类嵌入之间的交互。只有推荐任务的嵌入用于最终推荐。

与这些方法论相对，我们的重点是：通过精心构造的物品索引，在 LLM 内部发展出语言语义与协同语义的一种深入且统一的整合。具体而言，我们的方法使用树结构的向量量化方法来构造物品索引。这一方法通过向 LLM 增加少量（通常约 1,000，原文为 \(\sim 1{,}000\)）额外 token，来实现更好的语义整合。此外，我们引入一系列语义对齐任务来微调 LLM，目标是在实际的推荐设置（例如全量排序）中实现统一的语义整合。

图 1 出现在本节版面中。图注：The overall framework of our LC-Rec。译文：我们通过基于物品索引与对齐调优来整合语言语义与协同语义，从而增强语言模型，使 LLM 适配推荐系统。图注原文为 “We enhance language learning models (LLMs)”。

图中可读标签包括：Language Semantics、Language Tokens、Item Index Tokens、Language and Collaborative Alignment、Large Gap、Semantic Integration、Embedding Decoder、Embedding Encoder、Vector Quantization、CodeBook、Uniform Semantic Mapping、Collaborative Semantics、Recommendation、Large Language Models (e.g. LLaMA-7B)、LC-Rec、Item Titles, Description。可读任务名包括：A. Sequential Item Prediction；B. Explicit Index-Language Alignment；C. Implicit Recommendation-oriented Alignment；C 1-1. Asymmetric Item Prediction；C 1-2. Asymmetric Item Prediction；C 2. Item Prediction Based on User Intention；C 3. Personalized Preference Inference。

可读示例句包括：“Based on the user’s historical interactions:” 以及 “what to recommend to the user next?”；“Can you provide (the corresponding title) / (item) ?”；“Based on the user’s historical interactions: predict the title of next item.”；“Given the title sequence of user historical items: recommend a suitable next item.”；“Suppose you are a search engine, now a user searches that: The game has an open world environment…. can you select an item to respond to the user’s query?”；“Given the user's historical interactive items: what can be inferred about the preferences?”；“The user has recently been playing a game that requires a hard disk drive …”。可读专名示例包括 “Pokémon Moon − Nintendo 3DS”、“Ultimate Workout”、“Marvel Super Heroes”。可读索引串包括 \(a\_5 b\_2 c\_6 d\_7\)、\(a\_5 b\_4 c\_2 d\_1\)、\(a\_5 b\_3 c\_5 d\_7\)、\(a\_2 b\_2 c\_6 d\_4\)、\(a\_6 b\_2 c\_0 d\_7\)。这些标签、例句与索引串之间的版面连接【抽取不清】。
