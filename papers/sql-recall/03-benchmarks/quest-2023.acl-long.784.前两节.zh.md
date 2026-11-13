> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

原文件名：quest-2023.acl-long.784.pdf

原文标题：QUEST: A Retrieval Dataset of Entity-Seeking Queries with Implicit Set Operations

作者：Chaitanya Malaviya、Peter Shaw、Ming-Wei Chang、Kenton Lee、Kristina Toutanova（Malaviya 属 University of Pennsylvania，其余属 Google DeepMind；星号脚注说明该工作完成于其在 Google 的实习期间）

场合：Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics, Volume 1: Long Papers，页 14032–14047，2023 年 7 月 9–14 日

## 摘要

有选择的信息需求会写成隐含集合运算的查询，运算包括 intersection、union 和 difference。例子是 “shorebirds that are not sandpipers”，以及 “science-fiction films shot in England”。作者要测检索系统能不能满足这类需求，于是构建 QUEST：3357 条自然语言查询，都带隐含集合运算，并映射到一组对应 Wikipedia 文档的实体。模型既要把查询里的多条约束对上文档证据，又要做对各种集合运算。

数据半自动而来。原料是 Wikipedia 类别名：先把单个类别自动组成查询，再由众包改写，并另请人检查是否自然、是否流利。众包还根据实体文档判断相关性，并把查询约束高亮到文档片段上。若干现代检索系统在这些查询上经常吃力；否定和合取尤其难，两种运算叠在一起更难。数据发布在 https://github.com/google-research/language/tree/master/language/quest。

## 1 Introduction

人们的需求常常带多条偏好或约束，查询里就会隐含 intersection、difference、union。文中的例子包括：90 年代、不含外星人的科幻电影；背景在法国的历史小说；常绿且生长在巴拿马的灌木。若满足约束的实体不多，读者会想看一份尽量穷尽的名单；要信任系统，还需要来自可靠来源的证据。

这类问题以往主要放在结构化知识库问答里：约束落到预定义谓词上，再符号执行。知识库不完整，整理和维护又贵。信息检索的进展让人可以不靠结构化知识库，直接把约束对到文档证据上。但 MSMarco 和 Natural Questions 这类基准很少收录“多约束加隐含集合运算”的查询，也不以穷尽文档集合为目标，标注往往只覆盖某个基线检索器的前几条。

QUEST 因此收集四个领域的自然语言查询，每条对应一组相对完整、各自有 Wikipedia 页面的实体。构建时用 Wikipedia 类别及其到实体的映射作积木，推理时却不让系统访问这份半结构化数据，以模拟纯文本检索。类别名是对实体属性的自然语言描述，常常就像用户会发出的选择性查询；属性名和正文之间的对应往往很隐晦，需要较难的推理，这就是任务里的自然语言推断难点。Figure 1 把流程画成四步：抽样类别并找到相关实体；用集合运算组合成查询后请众包改写；再校验流利和自然；最后在文档里高亮可归因片段，标出实体是否相关。图中的例子把 “Birds of Venezuelan Andes” 与 “Birds of Colombia” 合成 “在委内瑞拉安第斯有、在哥伦比亚没有的鸟”，实体包括 Rose-crowned parakeet 和 Mérida sunangel。

正文把构造写得更具体：复杂查询由抽样类别按预定义模板组合，例子是 \(A \cap B \setminus C\)；众包改写时要保证流利，并清楚说出用户在找什么；另一批人按自然度和流利度过滤。数据的很大一部分还收了基于实体文档的标量相关性，以及把查询约束对到文本片段的细粒度归因。Figure 2 用查询 “Supernatural horror films set in Nevada” 和实体 Willy’s Wonderland 说明：不同约束的证据可以来自同一篇文档的不同位置，例如影片类型写在开头，地点 Hayesville, Nevada 写在后文。做好这个数据集，系统要能把约束对上证据、处理查询里隐含的集合运算，并扩展到很大的实体集合。作者在数据集上微调预训练模型，训练目标是给定查询检索多文档集合。双编码器和交叉注意力模型，规模到 T5-Large，对带集合运算的检索大体仍然无效；合取和否定尤其难，运算组合起来更难。错误分析认为，不相关的假阳性常常是因为模型忽略了被否定的约束，或忽略了查询里的合取约束。四个领域的具体名称、划分和实体总数不在这两节。

## 2 Related Work

相关工作从知识库问答、开放域问答与检索、多答案检索三条对照，说明 QUEST 既不假设有知识库，也不做跨文档多跳，而是在单篇文档上处理带集合约束的穷尽检索。

Knowledge Base QA 这一支要求找回知识库里作为节点或关系存在的实体集合，问题有时还附逻辑形式；Lan 等人有复杂 KBQA 数据集的综述。大规模整理过的知识库并不完整，而且 KBQA 被限制在既定答案模式里，能处理的查询类型有限，模式本身也贵。因此本文不假设推理时能访问知识库。已有工作把 KBQA 数据改到知识库残缺或不可用的设定，做法是删掉一部分知识库或完全不用它。和那些数据的关键差别是：本文不做跨多篇文档的多跳推理，一个实体相关与否只看它自己的文档。

Open-Domain QA and Retrieval 这一支里，TREC、MSMarco、Natural Questions 用搜索引擎上的真实查询这类 “found data” 构建；Thakur 等人把许多既有数据收成基准。HotpotQA 和 MultiRC 关注多跳问答。也有电商数据方面的工作，但没有公开。作者认为这些数据的焦点不同：本文要的是隐含集合运算、并且答案集合要尽量穷尽的查询；这类查询落在既有查询分布的尾部，所以现有数据里不多。

Multi-Answer Retrieval 要求一条查询给出多个不同答案。Min 等人把 WebQuestionsSP 等既有数据改到这个设定，并提出 MRecall@K 来衡量多答案的穷尽召回。本文同样做多答案集合检索，但查询本身隐含集合约束。同期的 RomQA 是开放域问答数据，约束组合抽自 Wikidata，动机同样是多约束、答案集可能很大。为了不做人工标注也能归因，RomQA 把问题限制在：各条约束能从 Wikipedia 摘要里单句、且已链到实体的句子上验证，关系用远程监督自动标注，精确率高、召回可能低（T-Rex 语料）。QUEST 把查询—证据匹配放宽到更全局的文档级推断；为了让人工归因做得动，则限制答案集大小，并且每条答案的证据只来自一篇文档。本节没有实验数字或表号。
