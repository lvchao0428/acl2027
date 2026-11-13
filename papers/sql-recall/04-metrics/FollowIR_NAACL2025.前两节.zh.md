> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

原文件名：FollowIR_NAACL2025.pdf

原文标题：FOLLOWIR: Evaluating and Teaching Information Retrieval Models to Follow Instructions

作者：Orion Weller、Benjamin Chang、Sean MacAvaney、Kyle Lo、Arman Cohan、Benjamin Van Durme、Dawn Lawrie、Luca Soldaini。Weller、Chang、Van Durme、Lawrie 属 Johns Hopkins University；MacAvaney 属 University of Glasgow；Lo、Soldaini 属 Allen Institute for AI；Cohan 同时属 Yale University 与 Allen Institute for AI。通信邮箱为 oweller@cs.jhu.edu。

场合：Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)，页 11926–11942，2025 年 4 月 29 日至 5 月 4 日。©2025 Association for Computational Linguistics。

## 摘要

现代语言模型能跟随很长、很复杂的指令，检索模型也把这些语言模型当骨干，但几乎不允许用户在查询旁边写下详细指令，因此满足不了复杂信息需求。FOLLOWIR 是一套严格的指令跟随评测基准：它把原本写给专业评审员的详细说明（narrative）改造成检索评测，材料来自 Text REtrieval Conference（TREC）的三个共享任务集合，并用一种新的成对评价框架衡量模型是否真的按指令办事。

结果是现有检索模型不会正确使用指令，多半只拿去当关键词，也读不懂长说明。作者同时表明这件事可以学：在他们的训练集上微调得到的 FOLLOWIR-7B 有显著提升。代码、数据和模型在 https://github.com/orionw/FollowIR 。

## 1 Introduction

语言模型被大量调到能忠实、安全地跟随指令，因此能做很多没有专门微调的任务。检索这边虽然用语言模型估计查询和文档的语义相似度，系统却几乎只被训练成文本片段的相似度估计器。若能按指令检索，就可以表达更复杂的需求，例如论文必须来自某会议、用某类方法，同时排除负面情感或某些领域的数据。已有的指令检索仍然很窄：指令通常短于 10 个词，而且一个数据集往往只有一条指令；评测也仍是普通的 ad-hoc 检索，没有专门量指令跟随。

FOLLOWIR 同时提供评测基准和带有多样、真实指令的训练数据。核心想法是借用专业标注员判断相关性时使用的 narrative。这些说明本来就会为构造良好的检索数据集的每条查询写好，TREC 共享任务里尤其完整，细到什么算相关、什么算不相关。Figure 1 用英吉利海峡隧道对英国经济与生活方式的影响作例子：相关条件会写清 “or” / “and” 一类限定（TREC 指令中占 90.4%），夹一段对判断相关性没有用的背景（34.6%，图中举隧道长 50.46 公里、1994 年开通），并用否定规定哪类文档应排除（52.9%）。评测集来自三份标注很深的集合：TREC Robust 2004、TREC Common Core 2017、TREC News 2021，每条查询有数百到数千篇文档被判为相关或不相关。作者把给标注员的指令稍作改动，并人工重标相关文档，从而得到成对指令，看模型会不会把相关文档改到与新指令一致。已有指标无法比较成对查询，他们因此定义 p-MRR，衡量同一查询配上两条不同指令时文档排名分数的变化。Figure 2 用哈勃望远镜的正面成就说明：指令里既有细粒度相关条件也有否定，模型若读懂改写后的指令，相关文档集合应当跟着变。

FOLLOWIR 上的结果是，现有模型在检索里大体不会跟指令，除非参数达到 3B 以上，或者根本没有为检索训练过。失败被归成两点：模型不习惯长指令，以及把指令当成关键词搜索。作者于是用真实、被人用过的指令做训练集，微调出 FOLLOWIR-7B；标准检索指标和 p-MRR 都有明显提升。贡献是：在三份已经深度标注的语料上加人工标注，做成检索指令跟随基准；分析当前模型为何读不懂指令；并放出训练数据与开源模型 FOLLOWIR-7B，使检索能处理长指令。

## 2 Related Work

TREC 由 NIST 在 1993 年设立，每年主办多条 track。题目从新闻上的普通 ad-hoc 检索，到法律检索，再到检索增强生成和报告生成。标注通常把多个检索系统的 run 放进池子，按排名往下标，直到经费用完。组织者会为每条查询写 narrative 给标注员，但检索模型历来只拿到查询本身。全库每篇文档都标一遍并不可行，召回误差靠事后抽样检查；尽管如此，查询层面的召回仍然很高。本文就从若干 TREC 集合上的这套严格评测出发。

指令跟随语言模型由 InstructGPT、FLAN、T0 一带带起来，后续工作讨论能否泛化到新指令、能否不用人工标注数据来训练，以及如何用到各个领域。检索里使用指令还很新。Su 等人和 Asai 等人最早训练检索模型把指令和查询一起用，但指令通常很短，例如 “Retrieve a Wikipedia paragraph that answers this question.” 后来的小模型，以及以 Llama 或 Mistral 为骨干的更大模型，也开始吃指令：GritLM 把 Mistral 训练成既能生成又能做嵌入，Wang 等人则只用 Mistral 做嵌入。这些工作没有专门的指令检索基准，而是在不含指令的 MTEB 和 BEIR 上评测，再手写少数指令，通常一条指令覆盖整个数据集、与具体查询无关。这种指令只描述任务格式、文档是段落还是句子，以及大致领域，不包含真实指令里常见的额外背景和否定，Figure 1 用来对照这种差别。

与本文同时，Oh 等人也做了检索指令评测，数据来自 MS MARCO。他们的设定是：每条查询只有一篇相关文档，属于稀疏标注；指令由 GPT-4 生成并校验；重点是用户背景，文中的例子是 “I am a school teaching looking for ...”；评价方式是同一查询的 N 条指令里取最低分，用来量稳健性。FOLLOWIR 则用深度标注的语料以保证能测召回，指令由专业人员撰写，相关性判断经过人工确认，并提出成对评价协议，同时给出用于教学的训练数据和模型。这一节没有另给实验数字。
