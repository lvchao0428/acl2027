# Recommender Systems with Generative Retrieval

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`TIGER-2305.05065.pdf`。

## Abstract 摘要

现代推荐系统做大规模检索时，把查询和物品候选嵌入到同一个统一空间，再做近似最近邻搜索，以便在给定查询嵌入后选出顶部候选。本文提出一种新的生成式检索方法：检索模型自回归地解码目标候选的标识符。为此，我们为每个物品构造语义上有意义的码字元组，作为其 Semantic ID。给定用户会话中物品的 Semantic ID，我们训练一个基于 Transformer 的序列到序列模型，来预测用户下一步将交互的物品的 Semantic ID。我们表明，用这一范式训练的推荐系统在多个数据集上显著优于当前的 SOTA 模型。此外，我们表明，把 Semantic ID 纳入序列到序列模型会增强其泛化能力，证据是对没有先前交互历史的物品，检索表现有所提高。

## 1 Introduction 引言

推荐系统帮助用户发现感兴趣的内容，并广泛存在于多种推荐领域，例如视频 [4, 43, 9]、应用 [3]、商品 [6, 8] 和音乐 [18, 19]。现代推荐系统采用“先检索再排序”的策略：在检索阶段选出一组可行候选，再用排序模型对它们排序。由于排序模型只处理它收到的候选，我们希望检索阶段给出高度相关的候选。

构建检索模型已有标准且成熟的方法。矩阵分解 [19] 在同一空间中学习查询嵌入与候选嵌入。为了更好地捕捉数据中的非线性，双编码器架构 [39]（即一个塔用于查询、另一个塔用于候选）近年来变得流行：它们用内积把查询嵌入和候选嵌入放进同一空间。推理时使用这些模型，会用候选塔为所有物品的嵌入建立一个索引。对给定查询，用查询塔得到其嵌入，再用近似最近邻（Approximate Nearest Neighbors, ANN）算法进行检索。近年来，双编码器架构也被扩展到序列推荐 [11, 24, 41, 17, 32, 6, 44]，显式考虑用户–物品交互的顺序。

我们提出一种为序列推荐构建生成式检索模型的新范式。不同于传统的查询–候选匹配方法，我们的方法使用端到端生成模型，直接预测候选 ID。我们提议利用 Transformer [36] 的记忆（参数）作为推荐系统中用于检索的端到端索引，这让人想起 Tay et al. [34] 用 Transformer 记忆做文档检索。我们将该方法称为 TIGER（Transformer Index for GEnerative Recommenders）。TIGER 的高层概览见图 1。TIGER 的独特之处在于一种新的物品语义表示，称为 “Semantic ID”——从每个物品的内容信息导出的一串 token。具体而言，给定物品的文本特征，我们用预训练文本编码器（例如 SentenceT5 [27]）生成稠密内容嵌入。然后对物品嵌入施加一种量化方案，形成一组有序的 token／码字，我们称之为该物品的 Semantic ID。最终，这些 Semantic ID 被用来在序列推荐任务上训练 Transformer 模型。

把物品表示为语义 token 序列有许多优点。在语义上有意义的数据上训练 Transformer 记忆，可以在相似物品之间共享知识。这使我们不必再使用先前推荐模型中作为物品特征的、原子式且随机的物品 ID [33, 42, 11, 8]。有了物品的语义 token 表示，模型更不容易陷入推荐系统固有的反馈循环 [1, 26, 39]，从而能够泛化到语料中新加入的物品。此外，用 token 序列表示物品，有助于缓解与物品语料规模相关的挑战：用 token 能够表示的物品数，是序列中每个 token 的基数的乘积。通常，物品语料规模可以达到数十亿量级，为每个物品学习一个独特嵌入会很占内存。虽然可以采用基于随机哈希的技术 [16] 来缩小物品表示空间，但本文表明，用语义上有意义的 token 表示物品是一个有吸引力的替代方案。本工作的主要贡献概括如下：

1. 我们提出 TIGER，一个基于生成式检索的新推荐框架：为每个物品分配 Semantic ID，并训练检索模型去预测给定用户可能发生交互的物品的 Semantic ID。
2. 我们表明，以 recall 和 NDCG 衡量，TIGER 在多个数据集上优于现有的 SOTA 推荐系统。
3. 我们发现，这种生成式检索的新范式为序列推荐系统带来两项额外能力：1. 能够推荐新的和不常见的物品，从而改善冷启动推荐；2. 能够用一个可调参数生成多样的推荐。

论文概览。Section 2 简要综述推荐系统、生成式检索，以及本文使用的 Semantic ID 生成技术。Section 3 解释所提出的框架，并概述我们用于生成 Semantic ID 的各种技术。Section 4 给出实验结果，Section 5 总结全文。

图 1 位于本节开头，图注可读。图 1：TIGER（Transformer Index for GEnerative Recommenders）框架概览。在 TIGER 中，序列推荐被表述为生成式检索任务，方法是把每个物品表示为一个离散语义 token 元组。图中可读示例为：Orange shoes, Brand X，Atomic Item ID: 233；Red shoes, Brand Y，Atomic Item ID: 515；Orange shoes, Brand Y，Atomic Item ID: 64。Semantic ID Generator 给出 (5, 23, 55)、(5, 25, 78)、(5, 25, 55)。其余标签包括 Item Lookup、Generative Retrieval、User History、Next item。这些标签与示例的版面连接【抽取不清】。

## 2 Related Work 相关工作

### Sequential Recommenders. 序列推荐

在推荐系统中使用深度序列模型已经形成了丰富的文献。GRU4REC [11] 最先把基于 GRU 的 RNN 用于序列推荐。Li et al. [24] 提出神经注意力会话推荐（Neural Attentive Session-based Recommendation, NARM），用注意力机制连同 GRU 层来追踪用户的长期意图。Zhang et al. 提出的 AttRec [41] 用自注意力机制建模用户在当前会话中的意图，并通过度量学习建模用户–物品亲和度来保证个性化。与此同时，Kang et al. 也提出了 SASRec [17]，它使用类似于 decoder-only Transformer 模型的自注意力。受语言任务中掩码语言建模成功的启发，BERT4Rec [32] 和 Transformers4Rec [6] 把带掩码策略的 Transformer 模型用于序列推荐任务。S3-Rec [44] 不止于掩码，而是在四个自监督任务上预训练，以改善数据表示。上述模型为每个物品学习一个高维嵌入，并在最大内积搜索（Maximum Inner Product Search, MIPS）空间中做 ANN 来预测下一项。相比之下，我们提出的技术 TIGER 使用生成式检索（Generative Retrieval），直接预测下一项的 Semantic ID。

P5 [8] 微调一个预训练大语言模型，用于多任务推荐系统。P5 依赖 LLM 的分词器（SentencePiece tokenizer [29]），从随机分配的物品 ID 生成 token。而我们使用的是基于物品内容信息学习得到的 Semantic ID 表示。在实验中（Table 2），我们表明，基于物品 Semantic ID 表示的推荐系统，比使用随机码的结果好得多。

### Semantic IDs. 语义 ID

Hou et al. 提出 VQ-Rec [12]，用内容信息生成“码”（类似于 Semantic ID）来表示物品。然而，他们的重点是构建可迁移的推荐系统，并不以生成方式使用这些码来做检索。他们也使用乘积量化 [15] 来生成码，而我们使用 RQ-VAE（原文抽取为 “RQ-V AE”）来生成 Semantic ID，从而得到物品的层次表示（Section 4.2）。在与我们同期的工作中，Singh et al. [31] 表明，层次化 Semantic ID 可以在大规模推荐系统中替代物品 ID 用于排序模型，并改善模型泛化。

### Generative Retrieval. 生成式检索

尽管学习搜索索引的技术早已被提出 [20]，生成式检索是最近发展起来的文档检索方法，其任务是从数据库中返回一组相关文档。例子包括 GENRE [5]、DSI [34]、NCI [37] 和 CGR [22]。相关工作的更详细覆盖见 Appendix A。据我们所知，我们是第一个提出用物品的 Semantic ID 表示、为推荐系统做生成式检索的工作。

图 2 位于本节前部，图注可读。图 2：TIGER 所用建模方法概览。(a) 通过对内容嵌入量化来为物品生成 Semantic ID。(b) 基于 Transformer 的编码器–解码器设置，用于构建生成式检索所用的序列到序列模型。图中可读字段包括：User_5 的物品交互历史；Item 515，Sem. ID = (5, 25, 78)；Item 233，Sem. ID = (5, 23, 55)；Item 64，Sem. ID = (5, 25, 55)；以及 Bidirectional Transformer Encoder、Transformer Decoder、\<BOS\>、\<EOS\>、Encoded Context、Next Item、Tokens。token 之间的具体流向【抽取不清】。
