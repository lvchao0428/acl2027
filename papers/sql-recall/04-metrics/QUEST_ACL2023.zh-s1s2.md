# QUEST: A Retrieval Dataset of Entity-Seeking Queries with Implicit Set Operations

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`QUEST_ACL2023.pdf`。

## Abstract 摘要

把有选择性的信息需求表述出来，会产生隐式指定集合运算的查询，例如交集（intersection）、并集（union）与差集（difference）。例如，人们可能会搜索 “shorebirds that are not sandpipers” 或 “science-fiction films shot in England”。为研究检索系统满足此类信息需求的能力，我们构建了 QUEST，一个包含 3357 条带隐式集合运算的自然语言查询的数据集，这些查询映射到与维基百科（Wikipedia）文档对应的一组实体。该数据集要求模型把查询中提到的多个约束与文档中的相应证据匹配起来，并正确执行各种集合运算。数据集借助维基百科类别名称半自动构建。查询先由各个类别自动组合而成，再由众包人员改写，并进一步验证其自然度与流畅性。众包人员还根据实体文档评估实体的相关性，并高亮查询约束在文档文本片段上的归因。我们分析了若干现代检索系统，发现它们在这类查询上常常表现吃力。涉及否定与合取的查询尤其困难，这些运算的组合会进一步增加系统的难度。1

1 数据集见 https://github.com/google-research/language/tree/master/language/quest。

## 1 Introduction 引言

人们常常用多重偏好或约束来表达信息需求。对应此类需求的查询通常隐式表达交集、差集与并集等集合运算。例如，观影者可能在找一部 90 年代的、没有外星人的科幻电影，读者可能对一部以法国为背景的历史小说感兴趣。类似地，试图根据记忆鉴定物种的植物学家可能会搜索常绿且见于巴拿马的灌木。此外，若满足约束的实体集合相对较小，读者可能希望看到并浏览这些实体的穷尽列表。另外，为核验并信任系统的推荐，用户会受益于被展示来自可信来源的证据（Lamm et al., 2021）。

处理此类查询的研究主要出现在基于结构化知识库（knowledge bases, KBs）的问答中：查询约束被落实到预定义谓词上并被符号执行。然而，知识库可能不完整，且整理与维护成本高。与此同时，信息检索的进展可能使系统不必依赖结构化知识库，而是把查询约束直接匹配到文本文档中的支持证据，从而处理此类查询。然而，把多个约束与隐式集合运算结合起来的查询，在 MSMarco（Nguyen et al., 2016）与 Natural Questions（Kwiatkowski et al., 2019）等现有检索基准中代表性不足。这些数据集也不聚焦于检索穷尽的文档集合，而是把标注限制在某个基线信息检索系统的前若干结果上。

为分析检索系统在此类查询上的表现，我们提出 QUEST，一个包含四个领域自然语言查询的数据集，这些查询被映射到与维基百科页面对应的、相对完整的实体集合。我们把维基百科中的类别及其到实体的映射用作数据集构建的基础，但在推理时不允许访问这一半结构化数据源，以模拟基于文本的检索。维基百科类别代表了实体属性的一大类自然语言描述，并且常常对应于搜索引擎用户有可能发出的选择性信息需求查询。属性名称与文档文本之间的关系往往很微妙，需要复杂推理才能判定，这体现了该任务固有的自然语言推理挑战。

我们的数据集构建过程见图 1。基础查询使用维基百科类别名称半自动生成。为构造复杂查询，我们采样类别名称，并用预定义模板把它们组合起来（例如 A ∩ B \ C）。接下来，我们请众包人员改写这些自动生成的查询，同时确保改写后的查询流畅，并清楚描述用户可能在寻找什么。随后由另一批众包人员验证其自然度与流畅性，并按这些标准过滤。最后，对数据中的很大一个子集，我们基于实体文档收集标量相关性标签，以及把查询约束映射到文档文本片段的细粒度文本归因。此类标注有助于开发能够依据可信来源做出精确推断的系统。

图 1：QUEST 的数据集构建过程。首先，（1）我们采样维基百科类别名称并找到其对应的相关实体集合。（2）然后，我们用集合运算组合出一条查询，并请众包人员改写该查询。（3）这些查询随后被验证流畅性与自然度。（4）最后，众包人员通过高亮文档中可归因的文本片段来标注实体的相关性。图中可辨认的例子：类别 “Birds of Venezuelan Andes — Birds of Colombia” 被改写为 “Birds found in the Venezuelan Andes but not in Colombia”，并标有 Fluent 与 Natural。实体包括 Rose-crowned parakeet 与 Mérida sunangel，标注包括 Complete Evidence、Definitely Relevant、Partial Evidence 与 Likely Relevant。步骤还标有 Paraphrasing 与 Relevance & Attribution Labeling。

要在该数据集上表现良好，系统需要把查询约束与文档中的相应证据匹配起来，并处理查询隐式指定的集合运算（见图 2），同时还要能高效扩展到大规模实体集合。我们通过在该数据集上微调预训练模型来评估若干检索系统。系统被训练为给定查询后检索多文档集合。我们发现，当前的双编码器（dual encoder）与交叉注意力（cross-attention）模型，直至 T5-Large（Raffel et al., 2020）的规模，在带集合运算的查询上做检索大体上并不有效。带合取与否定的查询对模型尤其困难，集合运算的组合会进一步增加系统的难度。我们的错误分析表明，不相关的假正例实体往往是因为模型忽略了被否定的约束，或忽略了查询中的合取约束。

图 2：QUEST 中一条查询与相关实体的示例。不同查询约束的归因可以来自文档的不同部分。可辨认内容如下。Query：“Supernatural horror films set in Nevada”。Entity：Willy’s Wonderland。文档文本片段：“Willy’s Wonderland is a 2021 American action comedy horror film directed by Kevin Lewis from a screenplay by G. O. Parsons. The film stars Nicolas Cage, who also [...] It follows a quiet drifter who is tricked into cleaning up an abandoned family entertainment center haunted by eight murderous animatronic characters. The project was announced in October 2019, [...] When his car catches a flat tire on a remote country road, a quiet drifter ends up stranded outside of Hayesville, Nevada. Mechanic Jed Love picks [...]”。

## 2 Related Work 相关工作

先前关于问答与信息检索的工作聚焦于知识库上的问答，以及面向一组实体或文档的开放域问答与检索。下面说明它们与我们工作的关系。

### Knowledge Base QA 知识库问答

已有若干数据集被提出用于知识库上的问答（Berant et al., 2013; Yih et al., 2016; Talmor and Berant, 2018; Keysers et al., 2020; Gu et al., 2021, inter alia）。这些基准要求检索作为伴随知识库中节点或关系而存在的一组实体。问题可以选择性地附带逻辑形式。Lan et al. (2021) 对复杂知识库问答（KBQA）数据集做了全面综述。

先前工作同时也指出，大型经整理的知识库是不完整的（Watanabe et al., 2017）。值得注意的是，知识库问答系统在受约束的答案模式（schema）上运作，这限制了它们能处理的查询类型。此外，这些模式的构建与维护成本很高。因此，我们的工作聚焦于不假定能够访问知识库的设定。我们注意到，知识库问答数据集也曾被改造到知识库不完整或不可用的设定（Watanabe et al., 2017; Sun et al., 2019）。做法是从知识库中移除一部分数据，或完全忽略知识库。与这些数据集的一个关键差别还在于，我们不聚焦于跨多篇文档的多跳推理。实体的相关性可以仅依据其文档来判定。

### Open-Domain QA and Retrieval 开放域问答与检索

先前工作提出了许多开放域问答基准，它们考虑在非结构化文本语料上做问答。其中一些，例如 TREC（Craswell et al., 2020）、MSMarco（Nguyen et al., 2016）与 Natural Questions（Kwiatkowski et al., 2019），使用 “found data” 构建，即使用搜索引擎上的真实用户查询。Thakur et al. (2021) 提出一个基准，其中考虑许多此类既有数据集。HotpotQA（Yang et al., 2018）与 MultiRC（Khashabi et al., 2018）等数据集聚焦多跳问答。其他工作探索了电子商务数据集（例如 Kong et al., 2022），但这些数据集尚未公开发布。值得注意的是，这些数据集的焦点与我们不同：我们聚焦在穷尽答案集合上包含隐式集合运算的查询。此类查询在现有数据集中代表性不足，因为它们出现在所考虑的查询分布的尾部。

### Multi-Answer Retrieval 多答案检索

相关工作（Min et al., 2021; Amouyal et al., 2022）也研究多答案检索问题，即系统需要为一条查询预测多个不同的答案。Min et al. (2021) 改造既有数据集（例如 WebQuestionsSP（Yih et al., 2016））来研究这一设定，并提出新指标 MRecall@K，以评估对多个答案的穷尽召回。我们也考虑多答案集合检索问题，但考虑的是隐式包含集合约束的查询。

在同期工作中，RomQA（Zhong et al., 2022）提出一个开放域问答数据集，聚焦从 Wikidata 抽取的约束组合。RomQA 与我们的动机相同：使系统能够回答带有多个约束、且答案集合可能很大的查询。为了在没有人工标注的情况下使证据归因可行，RomQA 聚焦于其组成约束可以从维基百科摘要中的单个实体链接句得到验证的问题；这些句子通过远程监督自动标注关系，精确率高但召回率可能较低（T-Rex 语料）。在 QUEST 中，我们通过允许更全局的、文档级的推断来做归因，从而拓宽查询与证据匹配操作的范围。为使归因的人工标注可行，我们限制答案集合的大小，并把一个答案的证据限制在单篇文档内。
