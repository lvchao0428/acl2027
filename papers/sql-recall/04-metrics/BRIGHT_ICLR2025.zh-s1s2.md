# BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`BRIGHT_ICLR2025.pdf`。

## Abstract 摘要

现有检索基准主要由信息寻求类查询构成（例如从搜索引擎汇总而来的问题），此时基于关键词或语义的检索通常已经足够。然而，许多复杂的真实查询需要深入推理，才能识别超出表层形式匹配的相关文档。例如，为编程问题查找文档，需要理解所涉函数的逻辑与语法。为更好地评测此类困难查询上的检索，我们提出 BRIGHT，首个需要密集推理（intensive reasoning）才能检索出相关文档的文本检索基准。我们的数据集包含 1,384 条真实世界查询，覆盖经济学、心理学、数学与编程等多样领域。这些查询取自自然产生、并经仔细整理的人类数据。大量评估表明，即便最先进的检索模型在 BRIGHT 上表现也很差。MTEB 排行榜（Muennighoff et al., 2023）上的领先模型 SFR-Embedding-Mistral（Meng et al., 2024）取得 59.0 nDCG@10，¹ 但在 BRIGHT 上的 nDCG@10 仅为 18.3。我们表明，把对查询的显式推理纳入检索，最多可将检索性能提高 12.2 分。此外，纳入表现最好的检索器所返回的文档，也能提升问答性能。我们相信，BRIGHT 为在更真实、更具挑战的设定下研究检索系统开辟了道路。²

¹ 该分数取自 2024-05-28 的 MTEB 排行榜。

² 代码与数据见 https://github.com/xlang-ai/BRIGHT 与 https://huggingface.co/datasets/xlangai/BRIGHT。

## 1 Introduction 引言

信息检索是一项被广泛使用的技术，帮助用户从包含文档、网页与日志记录的大规模语料中定位相关信息（Bajaj et al., 2016; Thakur et al., 2021）。相关信息与用户查询的关联方式并不相同：有时经由共享关键词或语义相似等直接匹配模式，有时则经由更深、更细微的联系，例如类似的底层原理。在许多真实场景中，用户查询可能高度复杂，找到相关文档需要密集推理。例如，经济学家可能想找到一则故事，它与另一则故事由同一经济理论来解释；程序员可能想用一条错误信息去定位对应的语法文档。对这类应用，相关文档无法仅靠词汇或语义匹配直接检索，而需要额外的推理步骤才能识别。

本文用 BRIGHT 研究推理密集型检索（reasoning-intensive retrieval）。BRIGHT 是一个新基准，检索相关文档需要密集推理。现有检索基准，如 BEIR（Thakur et al., 2021）与 MTEB（Muennighoff et al., 2023），主要关注通常来自搜索引擎的事实型查询；查询与文档之间的相关性往往直白，可通过简单的关键词或语义匹配检测出来（Lee et al., 2019; Karpukhin et al., 2020）。这些数据集侧重于检索特定信息片段（例如 “the widest highway in North America”），因此相关文档往往与查询有很高的词汇或语义重叠。相比之下，BRIGHT 中查询与文档的相关性不易通过简单的关键词或语义匹配检测；由于领域与查询本身复杂，需要有意的推理才能判定（图 1）。

图 1：现有检索基准关注基于关键词的检索（level 1）或基于语义的检索（level 2），例如 NQ、MS MARCO 数据集（Kwiatkowski et al., 2019; Bajaj et al., 2018）。BRIGHT 引入 level 3 检索：查询与文档之间的相关性需要密集推理才能判定。我们的数据由来自多样领域（例如经济学、数学、地球科学等）的自然用户查询构成。BRIGHT 语料也覆盖网页数据，如博客、语法文档以及 STEM 问题与解答。

BRIGHT 由 12 个来自多样且高阶领域的数据集组成，来源包括自然产生的人类数据与精心整理的材料。该基准包含两个主要部分：1）七个数据集由 StackExchange 构建，相关性定义为某文档是否在答案中被引用，并经多名标注者进一步验证，以确保正例文档（positive documents）确实有助于回答查询。鉴于该判断固有的主观性，我们只保留标注者一致同意的文档。2）其余五个数据集关注编程与数学问题，查询因共享底层算法或定理而与正例文档内在关联。

我们评估 13 个规模与架构各异的代表性检索模型。全面实验凸显了 BRIGHT 带来的挑战：表现最好的模型 SFR-Embedding-Mistral（Meng et al., 2024）在 MTEB 检索子集 BEIR（Thakur et al., 2021）上得分为 59.0，在 BRIGHT 上的 nDCG@10 仅为 18.3。为寻找改进 BRIGHT 的有希望方向，我们探索了多种策略。一种有效做法是在检索前用大语言模型（large language models, LLMs）生成关于查询的思维链推理步骤（chain-of-thought; Wei et al., 2022），平均提升最高达 12.2 分。进一步地，用来自表现最好的检索器 Qwen 的检索文档增强下游模型，相比闭卷设定（closed-book）提升了问答性能。不过，使用 oracle 文档带来的提升更大，说明改进检索模型仍有潜在收益。

此外，我们的结果表明，BRIGHT 对大规模预训练期间可能的数据泄漏具有稳健性：即便模型在该基准数据集的文档上继续训练，也未观察到显著的性能增益。我们希望这些发现能启发后续研究，推进推理密集型检索的现有水平。

## 2 Related Work 相关工作

### Benchmarking retrieval 检索基准评测

现有信息检索（information retrieval, IR）数据集通常为信息寻求任务而构建，例如问答（Voorhees & Tice, 2000; Craswell et al., 2020; Kwiatkowski et al., 2019; Chen et al., 2017; Maia et al., 2018）、主张核查（Thorne et al., 2018; Diggelmann et al., 2020; Wadden et al., 2020）或实体检索（Hasibi et al., 2017; Petroni et al., 2021）。近期工作把检索基准扩展到更多场景，例如指令遵循（Su et al., 2023; Weller et al., 2024; Oh et al., 2024; Li et al., 2024）、多跳（Yang et al., 2018）以及长上下文检索（Saad-Falcon et al., 2024; Zhu et al., 2024）。BEIR（Thakur et al., 2021）等综合基准在多样领域与任务上评估检索系统，其相关文档与查询共享较高的语义重叠。与本文最接近的 BIRCO（Wang et al., 2024）利用已有数据集，按多方面目标评估检索系统。但它限于 LLM 重排序设定，且每个查询只用很小的候选池（∼ 100 篇文档）。RAR-b（Xiao et al., 2024）把已有的常识、数学与代码数据集改造成检索设定，以测试模型能否直接检索推理问题的答案。³ 然而，我们关注更真实的场景：答案不太可能作为子串出现在文档中。尽管这两个基准都关注推理密集型检索，BRIGHT 是第一个收集真实用户查询、并将其与大规模语料中的相关自然文档对齐、从而需要深度推理才能找出正确匹配的基准。

³ 我们在 Appendix I 中与 RAR-b 作详细比较。

### Dense retrieval models and retrieval augmented generation 稠密检索模型与检索增强生成

最先进的检索系统常常用稠密模型，以丰富的表示来编码文本。这些模型在无监督数据（Lee et al., 2019; Izacard et al., 2022）、有监督数据（Su et al., 2023; Asai et al., 2023a; Muennighoff, 2022）以及 LLM 生成的数据（Lee et al., 2024; Wang et al., 2023a; Muennighoff et al., 2024）上训练。本文沿不同轴向对多样模型做基准评测：稀疏与稠密、小与大、开源与专有。此外，随着稠密生成模型持续改进，检索增强生成（retrieval-augmented generation, RAG; Asai et al., 2020; Borgeaud et al., 2022; Asai et al., 2023b; Muennighoff et al., 2024; Asai et al., 2024; Gao et al., 2023; Shi et al., 2024）已成为一项重要应用：它检索相关文档，以帮助生成连贯的答案。尽管本文主要关注检索，我们仍做了初步分析，并表明使用更强的检索器可以改进推理密集型任务上的模型生成。

### Benchmarking reasoning 推理能力评测

许多基准旨在评估 LLM 的推理能力，尤其集中于数学与编程。数学方面，数据集包括 GSM8K（Cobbe et al., 2021）及其扩展 GSM1K（Zhang et al., 2024）、TheoremQA（Chen et al., 2023a）、MATH（Hendrycks et al., 2021）与 LeanDojo（Yang et al., 2023）。编程方面，常用 HumanEval（Chen et al., 2021）、MBPP（Austin et al., 2021）与 LiveCodeBench（Jain et al., 2024）。这些基准包含问答对，通常来自教材、在线资源、竞赛或领域专家。我们从选定的高质量数据集中获取查询，并通过额外标注构建 BRIGHT，从而形成一个真实的推理密集型检索基准。
