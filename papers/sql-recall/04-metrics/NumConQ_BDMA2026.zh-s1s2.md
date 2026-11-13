# Numerical Constraint-Aware Dense Retrieval with Two-Phase Contrastive Learning

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`NumConQ_BDMA2026.pdf`。

## Abstract 摘要

检索增强生成（Retrieval-Augmented Generation, RAG）通过整合外部知识来增强大语言模型（Large Language Models, LLMs），从而在事实准确性与任务表现上带来显著提升。然而，现有稠密检索器在处理数值约束时面临相当大的挑战，尤其是在需要精确过滤条件的查询上。为系统考察这些问题，我们提出数值约束问题（Numerical Constraint Question, NumConQ），这是一个覆盖医疗、金融、教育、体育与电影的多领域综合基准数据集，包含超过 6500 条查询。实证分析表明，当前最优稠密检索器在数值约束满足上的准确率仅为 16.3%，显著低于其语义匹配能力。针对这些局限，我们提出数值约束感知检索器（Numerical Constraint-aware Retriever, NC-Retriever），其特点是：（1）两阶段对比学习框架，把批内负采样与逐步引入的硬负例结合起来；（2）用于一致分词的混合数值表示方案。大量实验表明，相对当前最优方法，NC-Retriever 在 recall@10 上取得 65.84% 的相对提升，precision@10 提高 78.28%。代码与基准数据集见 https://github.com/Tongji-KGLLM/NumConQ。

## 1 Introduction 引言

检索增强生成（RAG）[1] 已成为知识密集型任务的一种有力范式，它把大语言模型与外部数据仓库结合起来，以增强事实准确性与上下文深度。RAG 过程中的关键一步是检索：从庞大语料中找出相关文档；生成器再借助这些检索到的文档产生最终输出[2]。稠密检索的近期进展把查询与文档都编码为高维嵌入向量[3]，在多种开放域任务上大幅提升了性能。然而，现有稠密检索器主要聚焦语义匹配，常常难以顾及用户查询中陈述的数值约束[4]。数值约束查询带来的挑战不同于纯语义或主题查询。在从医疗记录分析[5, 6]到财务审计的许多真实场景中，查询往往包含严格的数值条件，例如 “over 65 years old”、“revenue less than 10 million” 或 “release in 2009”。满足这些约束既要理解语义上下文，也要按数值做精确过滤。主要在大量非结构化文本语料上训练的标准稠密检索器，倾向于强调概念相似性（例如 “film genre” 或 “country”），而忽略检索到的文档是否满足查询所规定的精确数值要求[7]。如图 1 所示，当查询规定 “average salary is lower than 6 183 974 USD” 时，表现较强的北京智源人工智能研究院（Beijing Academy of Artificial Intelligence, BAAI）通用嵌入 M3（General Embedding M3, BGE-M3）检索器[8] 检索到的文档中，联盟薪水分别为 6 650 000 USD（超出阈值 7.54%）与 10 710 000 USD（超出阈值 73.19%）。这凸显出现有方法对数值边界的敏感度不足。

图 1：稠密检索器处理数值约束查询失败的示例。可辨认内容如下。查询：“Find Football leagues where the Average Player Salary is lower than 6 183 974 and the league is based in India.” 真正相关文档（True relevant document）：“NFL, a Football league in India, stands out with its impressive revenue of 1 406 030 000 USD and average player salaries of 3 810 000 USD. Founded in 1898, it features 11 teams, with Dallas Cowboys being a dominant force. The league's viewership of 321.19 million highlights its global appeal.” 由 BGE-M3 模型检索出的前 2 篇文档（Top 2 Retrieval documents）：“Ligue 1, founded in 1895, is a Football league based in India. It consists of 10 teams, including the renowned Lyon. The league generates 4 147 490 000 USD annually, with players earning an average salary of 6 650 000 USD. It boasts a viewership of 343.04 million.” 以及 “In Bundesliga, a Football league based in India, players earn an average salary of 10 710 000 USD. Founded in 1990, the league includes 27 teams, with Borussia Dortmund being a fan favorite. It generates 6 495 300 000 USD annually and enjoys a viewership of 59.15 million.” GPT4 的错误回复（Wrong response）：“The football leagues in India with the average player salary lower than 6 183 974 are Bundesliga and Ligue 1. …” 正确回复（Right response）：“The football league in India with the average player salary lower than 6 183 974 is NFL. …”

当前方法呈现出三个关键局限：（1）多位数字的分词不一致；（2）注意力偏向文本特征；（3）缺乏数值约束感知的训练目标。

在此背景下，我们构建数值约束问题（NumConQ）这一多领域基准数据集，包含跨医疗、金融、教育、体育与电影的 6577 条数值约束查询，并配有 5362 篇自然语言文档。在每个领域中，我们把结构化条目转换为文本描述，并确保每条查询至少包含一个数值约束。基于该数据集，我们系统评估了五种广泛采用的稠密检索器：Contriever[9]、TAS-B[10]、DPR[11]、BGE-M3[8]，以及 JinaAI 的 jina-embeddings-v2-base-en[12]。实验结果表明，即便表现最好的检索器 BGE-M3，Recall@10 与 Precision@10 也分别仅为 40.37% 与 10.45%，凸显出稠密检索器准确处理数值约束的持续挑战。

为更有效地捕捉数值约束，我们通过细微修改查询中的数值来构造硬负例。训练时，我们同时使用批内负采样[13]与这些硬负例，但把硬负例的引入推迟到中后期。这种分阶段做法帮助检索器先掌握一般语义线索，再处理要求更高的基于数值的区分，从而使检索器对数值信息有更深的理解。此外，我们观察到，位数较高的数字在分词时经常以不一致的模式被切成多个子词词元，妨碍模型理解数量级与位置上下文。为此，我们实现一种混合数值表示：较小的数字保留原来的数字形式，较大的数字转换为基于单词的表达。这一做法减轻不一致分词，使模型对数值有更细粒度的把握，最终提升数值约束查询上的检索性能。

本文的主要贡献如下：

多领域数值基准：我们提出 NumConQ，一个由 6577 条带数值约束的文本查询与 5362 篇自然语言文档组成的多领域检索数据集，覆盖医疗、金融、教育、体育与电影。该基准系统评估检索器处理数值条件的能力。

对检索器处理数值约束能力的深入分析：我们考察当前稠密检索器在处理数值约束时的不足，指出分词不一致以及缺乏有针对性的训练数据等因素，这些因素妨碍准确的数值过滤。

面向数值约束检索的分阶段学习与混合表示：我们提出一种双管齐下的方法来提升检索性能：纳入数值约束硬负例的分阶段对比学习框架，以及增强分词一致性与数值理解的混合数值表示。

## 2 Related Work 相关工作

本节简要回顾数值约束查询与稠密检索器方面的相关工作。

### 2.1 Numerical constraint query 数值约束查询

由于神经网络架构的进步，语义搜索已取得显著进展。然而，处理数值数据对已提出的方法而言仍是挑战。

Qsearch[14] 作为端到端系统开创了这一领域，它利用深度神经网络从文本中抽取数值，并将其转换为语义结构，以回答数值约束查询。该系统引入语义角色标注（Semantic Role Labeling, SRL），把词分为实体、数量或上下文，从而抽取数值事实三元组。此外，它采用一种新的统计匹配方法，以高效检索并排序相关答案。

在此基础上，Faith[15] 把数值约束查询系统的能力扩展到异构数据源上的时间问答。Faith 通过中间问题与递归系统调用来处理隐式时间约束，把它们转换为显式值。这一做法便于准确且具备上下文感知地处理时间查询，展示了把数值约束查询方法适配到更复杂场景的潜力。

为增强大语言模型处理数值查询的能力，Han et al.[16] 针对大语言模型在财务报告中理解数值约束查询的局限展开工作。他们引入 XBRL agent 框架，通过整合外部工具来提升大语言模型的表现，从而有效应对金融语境中数值推理的细微之处。此外，他们提出一个专用数据集，即面向 XBRL 报告的数值类型查询任务，用以设立基准并推动该领域进展。Biswal et al.[17] 提出表增强生成（Table-Augmented Generation, TAG）方法，把大语言模型与数据库系统结合起来，处理包括带数值约束查询在内的复杂自然语言查询。

这些系统共同表明，面向知识库问答（Question-Answer, QA）任务、建立在结构化知识之上的数值查询能力在逐步精炼与扩展；相对非结构化文档，在结构化知识上查询数值知识更容易。然而，结构化知识库比非结构化文档更难获取与维护，这使得我们的方法能够利用更广范围的数值知识。

### 2.2 Dense retriever 稠密检索器

近年来，稠密检索器因在传统稀疏检索方法之上、尤其在需要语义理解的场景中表现更优而受到大量关注。从大型语料中检索相关信息是信息检索（Information Retrieval, IR）中的基础任务。词频-逆文档频率（Term Frequency-Inverse Document Frequency, TF-IDF）与最佳匹配 25（Best Matching 25, BM25）等传统稀疏检索方法依赖精确词项匹配，往往难以处理语义相似性。稠密检索器把查询与文档编码为稠密向量表示，从而在共享嵌入空间中计算相似度，以应对这一局限。

稠密编码器通常利用预训练模型获得丰富的上下文向量表示。稠密编码器有两种常见架构范式：双编码器（dual-encoder）与交叉编码器（cross-encoder）。双编码器架构用两个不同的编码器分别编码查询与文档，随后计算查询向量与文档向量之间的语义相似度。交叉编码器架构则把查询与文档拼接为输入，用单一编码器建模查询-文档交互，并直接捕捉细粒度语义匹配特征。交叉编码器架构在捕捉细微语义特征上强于双编码器，而双编码器允许对文档预先编码并建立索引，计算效率更高。鉴于朴素 RAG 系统中通常出现的文档量很大，双编码器架构主要用于大规模检索，交叉编码器则常用作重排序机制。

DPR[11] 是一种直接的双编码器模型，只需一小部分问题与段落数据集就能学习嵌入，从而仅用稠密表示进行检索。它使用来自问答数据集的正例，以及来自 BM25 的困难负例进行判别式训练。Xiong et al.[18] 分析了先前的稠密检索器，指出局部负采样是稠密检索性能的瓶颈。据此，他们提出近似负例对比估计（Approximate Negative Contrastive Estimation, ANCE）。与随机负例或批内局部负例不同，ANCE 利用已优化的稠密检索模型从整个语料中检索，以生成全局负例，从而使训练时负样本的分布与测试时不相关文档的分布对齐。Contriever[9] 针对低资源设定下改进稠密检索模型的挑战，提出用对比学习训练无监督稠密检索器，并表明对比学习能在多种检索设定下提升这些模型的表现。近期，LARMOR[19] 是一种无监督方法，它利用大语言模型生成伪相关信号，用于选择并排序稠密检索器。KaLM-Embedding[20] 把大语言模型的多语言知识与动态训练策略结合起来，为 RAG 系统提供稳健的语义理解基础。

尽管稠密检索器在语义理解上表现更优，它们在处理数值敏感查询时仍面临挑战。数值敏感查询往往需要精确匹配并准确检索详细的数值信息，而稠密检索器主要依赖潜在空间中的语义相似度，可能捕捉不到细粒度的数值差异。这是因为稠密模型更关注复杂的上下文与语义关系，对精确的数值精度关注较少。
