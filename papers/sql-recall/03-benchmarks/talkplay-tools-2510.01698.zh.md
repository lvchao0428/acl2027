# TalkPlay-Tools：基于 LLM 工具调用的对话式音乐推荐

- 原文件名：talkplay-tools-2510.01698.pdf
- 原标题：TalkPlay-Tools: Conversational Music Recommendation with LLM Tool Calling
- 中文标题：TalkPlay-Tools：基于 LLM 工具调用的对话式音乐推荐
- 作者：Seungheon Doh、Keunwoo Choi、Juhan Nam
- 会议或 arXiv：arXiv:2510.01698v4 [cs.IR] 2 Jun 2026（Preprint，见 PDF 第 1 页页脚）

<!-- 原 PDF 第 1 页 -->

**Seungheon Doh**<sup>1,2,∗</sup>，**Keunwoo Choi**<sup>1,2,∗</sup>，**Juhan Nam**<sup>1</sup>

<sup>1</sup> KAIST，韩国；<sup>2</sup> talkpl.ai，美国

https://talkpl-ai.github.io/talkplay_tools

## 摘要

尽管大语言模型（LLM）的最新进展已经成功使生成式推荐系统能够进行自然语言交互，其推荐行为仍然有限，元数据过滤、属性过滤等更简单却至关重要的组件在系统中未得到充分利用。我们提出一种基于 LLM、带工具调用的音乐推荐系统，将其作为统一的检索—重排序流水线。该系统把 LLM 定位为端到端推荐系统：它解释用户意图、规划工具调用，并编排若干专用组件——布尔过滤（SQL）、稀疏检索（BM25）、稠密检索（嵌入相似度）以及生成式检索（Semantic ID）。通过工具规划，系统预测应使用哪些类型的工具、它们的执行顺序，以及为找到符合用户偏好的音乐所需的参数；在无缝整合多种数据库过滤方法的同时，支持多样的模态。我们表明，这一统一的工具调用框架能够根据用户查询有选择地采用合适的检索方法，从而在多样的推荐场景中取得有竞争力的性能，并展望对话式音乐推荐系统的一种新范式。

## 1 引言

音乐推荐长期以来一直围绕如何按用户偏好过滤数据库而形成。早期系统依赖对收听历史日志以及标题、艺人、发行年份等元数据的布尔过滤 [1]。大规模音乐条目目录以及用户—物品特征学习算法 [12] 的出现，使该领域转向由大规模用户与物品嵌入驱动的检索与重排序流水线 [25, 9]。随着表示学习的进展，该领域已超越收听历史，发展出更深的内容理解 [28, 17]。此外，面向音频 [13]、歌词 [19] 与视觉封面 [8] 的音乐表示使基于样例的推荐成为可能，而多模态音乐表示 [14, 10, 7, 6, 31, 30, 16, 26] 则支持自然语言查询理解。基于大语言模型（LLM）的推荐系统的最新进展 [4, 18] 表明，物品可以表示在语义空间中，并量化为离散的 Semantic ID [20, 15]，从而同时实现生成式推荐以及与用户的交互式对话。在这些方法中，用户可以通过多轮交互主动发现符合其目标与偏好的音乐。

然而，依赖单一检索方法在识别满足用户需求的物品时有明显局限 [29]。生产级推荐系统 [3, 11] 基于多阶段、经路由的检索—重排序流水线运行，必须严格满足运营约束（例如用户画像、流派、情绪、活动、新颖度等），同时反映听者的历史与文本查询。若不组合多种类型的检索方法，就无法充分捕捉推荐的全部相关上下文。

∗同等贡献。通讯作者：seungheondoh@kaist.ac.kr，juhan.nam@kaist.ac.kr。

预印本。arXiv:2510.01698v4 [cs.IR] 2 Jun 2026

<!-- 原 PDF 第 2 页 -->

图 1 见原 PDF。

**图 1：** 带工具调用的音乐推荐智能体概览。

本文提出一种带工具调用的对话式音乐推荐系统。我们的贡献是：（i）将结合多种检索方法的对话式音乐推荐形式化，使 LLM 能够在给定用户画像与对话上下文的条件下预测工具类型、顺序与参数；（ii）设计一套统一的工具集，在单一智能体下组合布尔过滤（SQL）、稀疏检索（BM25）、跨模态稠密检索（文本到物品、物品到物品、用户到物品）以及生成式检索（Semantic ID）；（iii）在对话式推荐基准上展示零样本有效性，相对强基线提高 Hit@K，并对其行为作详细分析。

## 2 带工具调用的音乐推荐

图 1 展示了我们的框架，它由两个主要组件构成。第一个组件是音乐推荐智能体，包括 LLM 与工具。第二个组件是外部环境，它执行工具，并通过检索与重排序给出最终推荐。

### 2.1 问题形式化

给定用户 $u$ 及其画像 $p_u$、先前对话状态 $s_{t-1}$，以及当前轮次 $t$ 的用户查询 $q_t$，所提出的系统通过（i）用 LLM 生成工具调用，以及（ii）用预测的工具 $C_t$ 过滤数据库 $\mathcal{D}$，产生音乐物品的排序列表 $m_t$。最后再次调用 LLM，生成自然语言回应 $r_t$，在维持对话上下文的同时，对推荐给出对话式解释。

$$
C_t = \mathrm{LLM}(q_t, s_{t-1}, p_u; \mathcal{P}_{\mathrm{tool}}, \mathcal{T}) \qquad (1)
$$

$$
m_t = \mathrm{ToolEnv}(C_t; \mathcal{D}) \qquad (2)
$$

$$
r_t = \mathrm{LLM}(m_t, q_t, s_{t-1}, p_u; \mathcal{P}_{\mathrm{response}}) \qquad (3)
$$

令 $\mathcal{T}$ 表示可用工具，$\mathcal{P}$ 表示提示，且 $C_t = \left[(\mathrm{tool}_n, \mathrm{args}_n)\right]_{n=1}^{N}$ 为 LLM 预测的工具调用序列，工具数量为 $N$。工具环境执行每一对 $(\mathrm{tool}_n, \mathrm{args}_n)$，将结果检索并重排序为最终排序列表 $m_t$。

工具执行环境作为顺序流水线运行：每个工具的输出直接影响下一个工具的输入空间，也就是说，每个工具都为下游工具过滤并精炼曲目池。因此，工具的顺序显著影响最终推荐质量。通过提示 $\mathcal{P}_{\mathrm{tool}}$，我们引导 LLM 不把推荐当作单次操作，而是当作由检索阶段与重排序阶段组成的分阶段过程，从而保证工具执行遵循顺序流水线。

<!-- 原 PDF 第 3 页 -->

**表 1：** 不同工具的能力比较。灰色文字表示由上下文信息激活、而非由用户自然语言查询直接激活的工具。

| 工具 | 能力 | 环境 | 查询示例 |
| --- | --- | --- | --- |
| *布尔检索* | | | |
| SQL | 数值过滤 | SQL Server | 「BPM 超过 130 的近期歌曲」 |
| *稀疏检索* | | | |
| BM25 | 词汇匹配 | BM25 索引 | 「Adele 的《21》里的歌曲」 |
| *稠密检索* | | | |
| Text-to-Item | 语义匹配 | Qwen3、CLAP、SigLIP2 | 「播放一首平静的钢琴曲」 |
| Item-to-Item | 多模态匹配 | CLAP、SigLIP2、BPR | 「好的，再来一些更相似的嗓音」 |
| User-to-Item（灰色） | 个性化 | BPR | user_id:10021 |
| *生成式检索* | | | |
| Semantic ID（灰色） | 多模态上下文 | Residual VQ 表 | audio:semantic_id:[63, 36, 44, 3] |

### 2.2 工具

我们的框架纳入多种工具，通过结构化过滤与语义检索，实现精确而灵活的音乐推荐。表 1 概括了它们的能力、环境与使用示例。

**SQL（布尔检索）：** SQL 工具能够对关系型音乐元数据做精确的结构化查询。我们构建一张表，字段包括标题、艺人、专辑、发行日期、速度、调性与流行度。工具参数包括用于 SQL 语句的 `query` 以及用于结果数量上限的 `topk`，例如 `sql(query="SELECT * FROM tracks WHERE date>=2020 ORDER BY tempo", topk=100)`。

**BM25（稀疏检索）：** 该工具使用 BM25 排序函数 [22] 提供经典的基于词元的文本检索。BM25 提供词汇匹配，因此对错字常见、精确字符串匹配困难的文本查询尤其有效。我们构建五个文本语料库：标题、艺人、专辑、歌词与属性（语义标签）。工具参数包括 `query`、`corpus` 与 `topk`，例如 `bm25(query="taylor swift songs", corpus="artist", topk=100)`。

**Text-to-Item（稠密检索）：** 该工具把文本查询映射到跨多种模态的音乐内容，从而通过自然语言描述实现语义音乐发现。利用预训练的文本编码器 [32] 与多模态编码器 [31, 27]，该工具在相应嵌入空间中按余弦相似度检索最相似的物品。工具参数包括查询、物品模态类型、向量数据库类型与 `topk`，例如 `text_to_item(query="Tracks with an album cover that shows a baby swimming underwater.", item_modality="image", vector_db="image", topk=20)`（查询意为「专辑封面显示婴儿在水下游泳的曲目」）。

**Item-to-Item（稠密检索）：** 该工具用稠密表示寻找相似物品，从而支持基于样例的推荐。LLM 根据先前推荐的曲目或多轮对话中用户提供的样例生成曲目 ID，然后我们从预先抽取的向量数据库中查找对应嵌入 [31, 27, 21]，进行基于相似度的检索。工具参数包括曲目 ID、物品模态类型、向量数据库类型与 `topk`，例如 `item_to_item(track_id="22L7bfCiAkJo5xGSQgmiIO", item_modality="audio", vector_db="audio", topk=20)`。

**User-to-Item（稠密检索）：** 该工具使用经由收听历史训练的用户嵌入 [21] 提供个性化推荐。与由用户查询激活的其他工具不同，该工具使用用户画像信息中的用户 ID 来激活。工具参数包括 `user_id` 与 `topk`，例如 `user_to_item(user_id=10021, topk=200)`。

**Semantic ID（生成式检索）：** Semantic ID 是由物品内容特征导出的离散表示 [20, 15]。内容被编码为稠密嵌入，再用残差向量量化器（Residual Vector Quantizer，RVQ）量化为离散码本索引。Semantic ID 作为上下文信息，帮助 LLM 理解音乐的多模态属性。我们建立从码位置到物品 ID 的倒排索引，以便按精确码匹配或小编辑距离快速查找。工具参数包括物品模态类型、Semantic ID 索引与 `topk`，例如 `semantic_id(item_modality="audio", indices=[52, 42, 5, 9], topk=20)`。

<!-- 原 PDF 第 4 页 -->

### 2.3 推理所用的上下文信息

在所提出的框架中，推荐依据提供给 LLM 的上下文信息作出。这一条件提示包含四类信息。

**系统提示：** 框架的两个阶段有两套不同的提示：一套用于工具调用，另一套用于回应生成。对于工具调用，我们设计结构化的三阶段提示，把复杂的推荐过程分解为规划、检索与重排序阶段。阶段 1（规划）要求 LLM 选出确切的检索工具与重排序工具，并为每一选择给出理由。阶段 2（检索）执行所选检索工具，从音乐数据库中收集至少 `topk` 个互不相同的 `track_id`。阶段 3（重排序）应用所选重排序工具对候选重新排序，以提高推荐质量。该工作流施加严格约束：工具必须按顺序使用（检索 → 重排序），角色互补，且功能不重叠。回应生成提示旨在清楚解释推荐结果，确保所推荐曲目与用户查询一致。

**工具函数：** 我们提供完整的工具函数列表及其 JSON schema，其中包括名称、描述与参数数据类型。详细函数示例见附录 A。

**用户画像：** 为了个性化，我们把用户人口统计信息与近期收听历史作为上下文信息提供给 LLM。人口统计信息包括用户 ID、类型、年龄组与性别。用户 ID 作为推理时的上下文信息，用以正确激活 “User-to-Item” 工具。对于近期收听历史，我们纳入用户收听会话中最近五首曲目的元数据；每首曲目的信息包括元数据、属性与 Semantic ID。

**先前对话历史：** 我们把先前对话状态作为上下文信息提供给 LLM。对话状态包括用户查询、被推荐的音乐，以及 LLM 的回应。为纳入音乐的多模态信息，我们不仅纳入曲目 ID，还把元数据、属性与 Semantic ID 作为上下文信息纳入。

## 3 实验

**数据集：** 我们使用 TalkPlayData 2 [2]，这是一个为多模态对话式音乐推荐设计的合成数据集。该数据集包含来自 LFM-2b [23] 的、带有人口统计信息（性别、年龄、国家）的多样用户画像。它还提供全面的多模态音乐表示，包括收听历史、元数据、语义标签、歌词、专辑封面与音频。我们在 1000 段测试对话上评估不同的对话式推荐系统，每段对话由 8 轮组成。

**环境：** 我们的环境由一个执行器以及供工具调用使用的数据库组成。对于 SQL 与 BM25 [22]，我们使用基本元数据（曲目名、专辑名、艺人名）以及来自 LFM-2b [23] 的 last.fm 流派/风格标注。对于稠密检索工具，我们用多种预训练模型构建多个向量数据库：文本模态使用 Qwen3-0.6 嵌入 [32]，音频模态使用 CLAP [31]，图像模态使用 SigLIP2 [27]，用户与物品嵌入使用贝叶斯个性化排序（Bayesian Personalized Ranking，BPR）[21]。最后，对于 Semantic ID [20, 15]，我们在预先抽取的每一种表示（收听历史、元数据、语义标签、歌词、专辑封面与音频）上分别训练一个残差向量量化器（RVQ），再把它们组合起来生成多模态语义标识。RVQ 架构采用 4 层残差量化，每层 64 个码本，以承诺损失（commitment loss）优化。超参数通过验证实验选取，以平衡承诺损失与码本利用率。为确保公平评估并防止数据泄漏，我们在训练 BPR 与 RVQ 模型时都采用按时间顺序的数据划分，训练集严格先于测试集。

**评估：** 对于对话式推荐，我们以 Hit@K 为主要指标，$k=\{1,10,20\}$。我们将工具调用方法与若干基线比较：（1）BM25，一种经典稀疏检索方法；（2）Qwen3-LM + BM25，它把语言模型生成与模糊匹配结合起来；（3）我们所提出的 Qwen3-LM + Tool Calling，它利用多种工具。我们使用 Qwen3-LM-4B [32] 作为基座模型，<sup>2</sup> 借助其较强的推理能力来完成复杂的工具调用与查询分解。生成参数设为 `temperature=0.6`、`top_p=0.95`。我们把所有标识符（用户 ID、曲目 ID、Semantic ID）表示为自然语言字符串，而不是通过扩展词表得到的特殊词元。

<sup>2</sup> https://huggingface.co/Qwen/Qwen3-4B

<!-- 原 PDF 第 5 页 -->

**表 2：** 对话式音乐推荐结果。QU、RG、TC 分别表示查询理解、回应生成与工具调用能力。

| 模型 | 方法 | QU | RG | TC | Hit@1（↑） | Hit@10（↑） | Hit@20（↑） |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BM25 | 稀疏 | ✓ | ✗ | ✗ | 0.017 | 0.073 | 0.107 |
| Qwen3-LM + BM25 | 生成式 | ✓ | ✓ | ✗ | 0.018 | 0.076 | 0.110 |
| Qwen3-LM + Tool（本文） | 生成式 | ✓ | ✓ | ✓ | 0.022 | 0.082 | 0.111 |

图 2 见原 PDF。

**图 2：** 首次尝试时的工具调用频次。

图 3 见原 PDF。

**图 3：** 首次尝试时的工具调用成功率。

## 4 结果

**多轮推荐：** 表 2 表明，我们的工具调用方法在零样本对话式音乐推荐上优于基线方法。Hit@1 的提升（0.022，相对于 Qwen3-LM + BM25 的 0.018）凸显了通过整合多种工具进行重排序的有效性。当某次工具调用在推理中失败时（后文详细讨论），系统会自动重试该调用，从而保证所有推理步骤都成功完成。

**工具调用频次：** 图 2 与图 3 基于任何重试机制之前的首次尝试，分析工具调用模式。在反复重试之后，在我们的实验中，系统总能抽取到一个结果。工具频次分布显示，SQL 与 BM25 这类对自然语言友好的工具使用频次更高，而物品到物品匹配、Semantic ID 工具等针对特定物品模态的工具频次较低。这一模式很可能反映了预训练时的接触程度：SQL 与 BM25 这类通用算子经常出现在信息检索语料中，而物品到物品匹配与 Semantic ID 工具往往具有领域特定的函数名与接口。因此，预训练 LLM 对这些工具较不熟悉，调用它们的频率也更低。

**工具调用成功率：** 然而，成功率分析揭示了更复杂工具所面临的性能挑战。SQL 查询的成功率仅为 27.4%，原因是其句法复杂，以及常见错误，例如不正确的 SQL 语法、使用无效列名，以及由同义词或错字导致元数据与查询不匹配、从而检索失败。物品到物品匹配的成功率为 68.4%，这可归因于预测完整曲目 ID 的困难——曲目 ID 是与音乐目录相关的私有信息。出乎意料的是，依赖在 LLM 预训练中从未见过的信息类型的工具，例如用户 ID 与 Semantic ID，却表现出高成功率。User-to-Item 个性化的成功率为 98.8%，Semantic ID 检索的成功率为 95.8%。这一高性能来自通过用户画像与先前对话历史所提供的丰富上下文信息。

**定性示例：** 表 3 展示了 TalkPlay-Tools 的一次推理示例。推理过程从用户信息与对话聊天上下文开始，其中包括先前推荐的曲目与用户画像数据。系统接着进入工具调用阶段，模型分析用户查询并确定合适的检索工具。检索结果随后被用于生成自然语言回应。这一多阶段过程同时保证最终回应中的检索准确性与对话流畅性。

<!-- 原 PDF 第 6 页 -->

**表 3：** 一次推理示例，含 LLM 的输入与输出。

**输入：用户人口统计**

UserID: N/A（冷启动用户），年龄组：20 多岁，国家：Slovenia，性别：女，先前曲目：N/A（冷启动用户）

**输入：聊天上下文（先前轮次）**

用户：我在找一位德国电子音乐艺人，我记得他们有一张叫 “Walls” 的专辑，里面有一些非常极简、忧郁的曲目。

助手：TrackID: 1KsqDnRQXFdFypQdFkB0wA，title: not a number，artist: apparat，album: walls，tags: experimental, 00s, post-rock, instrumental, soundtrack, ambient, electronica, electronic，tempo: 130.37，key: C major，release_date: 2007.05.25，‘audio:semanticID’: [0, 39, 63, 53]，‘image:semanticID’: [41, 10, 17, 48]，‘metadata:semanticID’: [15, 49, 15, 36]，‘lyrics:semanticID’: [45, 38, 39, 50]，‘attributes:semanticID’: [20, 55, 58, 51]，‘cf_item:semanticID’: [59, 21, 42, 34]

助手：哦，完全正确！专辑 Walls 里的 Apparat 正是我想到的。若要那种非常极简、忧郁的氛围，你一定该听听 Not A Number。它恰好捕捉到那种大气、内省的感觉。

用户：对，这正是我在找的艺人！太好了，就是 Apparat。你能从他们的作品里再推荐一些别的曲目吗，尤其是更偏器乐或氛围的？

**中间结果：工具调用的思维链**

好的，用户刚刚确认 Apparat 就是他们在找的艺人，并希望从该艺人的作品中得到更多推荐，特别是器乐或氛围曲目。让我拆解该如何处理。

首先，该用户是 cold_start 用户，所以我需要使用合适的工具。

……［原文省略］……

另一种做法是，用 BM25、以 “artist” 为 `corpus_type` 查找 Apparat 的曲目，再过滤出器乐与氛围。但可用工具包括 BM25，它用于词汇匹配。也可以用 `text_to_item`，`modality_type` 为 “text”、`corpus_type` 为 “attributes”，查询 instrumental、ambient。

……［原文省略］……

因此第一次工具调用是 BM25，query 为 “Apparat”，`corpus_type` 为 “artist”，topk 为 20。然后第二次工具调用是 `text_to_item_similarity`，query 为 “instrumental, ambient”，`modality_type` 为 “text”，`corpus_type` 为 “attributes”，topk 为 20。但用户要找的是 Apparat 的曲目，所以初始检索是 Apparat 的曲目，重排序则基于属性。

**中间结果：工具调用结果**

```json
[{"tool_name": "bm25", "tool_args": {"query": "Apparat", "corpus_type": "artist", "topk": 20}},
 {"tool_name": "text_to_item", "tool_args": {"query": "instrumental, ambient", "modality_type": "text", "corpus_type": "attributes", "topk": 20}}]
```

**输出：推荐曲目**

助手：TrackID: 40HHuqH12ssXNpnHkiz0fk，title: tod，artist: apparat，album: krieg und frieden (music for theatre)，tags: experimental, ambient, dance, electronic, soundtrack，tempo: 85.83，key: A major，release_date: 2013.02.19

**中间结果：回应生成的思维链**

好的，用户刚刚确认 Apparat 就是他们在找的艺人，并要求更多推荐，特别是器乐或氛围曲目。所给曲目是 Krieg und Frieden (Music for Theatre) 中的 Tod。我需要核实 Tod 是否确实是器乐或氛围。标签包括 experimental、electronic 与 soundtrack。速度是 85.83，偏慢，调性是 A major。发行日期是 2013。

……［原文省略］……

我应当把这首曲目作为推荐呈现出来，突出其流派、情绪，以及它为何匹配良好。我需要确保回应热情而自信，确认这首曲目符合他们的偏好。然后邀请他们探索更多相似曲目，或讨论其他偏好。

**输出：回应**

助手：当然！Krieg und Frieden (Music for Theatre) 中的 Tod 是一首出色的氛围曲目，恰好补足你喜欢的那种极简、内省的氛围。它缓慢、富有空气感，带着萦绕不去的忧郁，既电子又深具情感。A major 调性与稳定的速度营造出冥想式、沉浸式的体验。你还想要更多推荐，或探索其他情绪吗？

## 5 结论

我们提出了一种用于对话式音乐推荐的新型工具调用框架，它把多种模态以及检索—重排序流水线中的各个组件无缝整合在一起。为成功整合，我们提出通过 LLM 工具调用来编排外部执行器与模型。借助多种类型的工具，所提出的框架有效利用了跨越文本、音频、视觉与行为数据的多模态信息，在对话上下文中给出增强的音乐推荐。未来研究方向有若干有前景的途径：（1）引入强化学习方法，以优化工具调用精度并减少对重试机制的依赖；（2）设计个性化的工具调用策略，超越以曲目为中心的做法，更有效地捕捉细微的用户偏好与行为模式。

<!-- 原 PDF 第 7 页 -->

## 参考文献

[1] O. Celma. 音乐推荐：载于《音乐推荐与发现》，2010.

[2] K. Choi, S. Doh, and J. Nam. TalkPlayData 2：面向多模态对话式音乐推荐的智能体式合成数据流水线. arXiv preprint arXiv:2509.09685, 2025.

[3] P. Covington, J. Adams, and E. Sargin. 用于 YouTube 推荐的深度神经网络. In Proceedings of the 10th ACM conference on recommender systems, pages 191–198, 2016.

[4] S. Doh, K. Choi, and J. Nam. TalkPlay：基于大语言模型的多模态音乐推荐. arXiv preprint arXiv:2502.13713, 2025.

[5] S. Doh, J. Koo, M. A. Martínez-Ramírez, W. Choi, W.-H. Liao, Q. Wu, J. Nam, and Y. Mitsufuji. LLM2FX-Tools：面向音乐后期制作的工具调用. International Conference on Learning Representations, 2026.

[6] S. Doh, M. Lee, D. Jeong, and J. Nam. 用微调 LLM 与元数据丰富音乐描述，以进行文本到音乐检索. In ICASSP 2024-2024 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2024.

[7] S. Doh, M. Won, K. Choi, and J. Nam. 迈向通用的文本到音乐检索. In ICASSP 2023-2023 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2023.

[8] C.-C. Hsia, K.-H. Lai, Y. Chen, C.-J. Wang, and M.-F. Tsai. 面向基于图像的音乐推荐的表示学习. arXiv preprint arXiv:1808.09198, 2018.

[9] Y. Hu, Y. Koren, and C. Volinsky. 面向隐式反馈数据集的协同过滤. In International conference on data mining (ICDM), 2008.

[10] Q. Huang, A. Jansen, J. Lee, R. Ganti, J. Y. Li, and D. P. Ellis. MuLan：音乐音频与自然语言的联合嵌入. International Society for Music Information Retrieval (ISMIR), 2022.

[11] K. Jacobson, V. Murali, E. Newett, B. Whitman, and R. Yon. Spotify 上的音乐个性化. In Proceedings of the 10th ACM Conference on Recommender Systems, pages 373–373, 2016.

[12] Y. Koren, R. Bell, and C. Volinsky. 推荐系统的矩阵分解技术. Computer, 42(8):30–37, 2009.

[13] J. Lee, N. J. Bryan, J. Salamon, Z. Jin, and J. Nam. 面向音乐相似度的解耦多维度量学习. In IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP), 2020.

[14] I. Manco, E. Benetos, E. Quinton, and G. Fazekas. 面向音乐的对比式音频—语言学习. International Society for Music Information Retrieval (ISMIR), 2022.

[15] M. J. Mei, F. Henkel, S. E. Sandberg, O. Bembom, and A. F. Ehmann. 用于音乐推荐的 Semantic ID. arXiv preprint arXiv:2507.18800, 2025.

[16] S. Oramas, A. Ferraro, A. Sarasua, and F. Gouyon. 与你的推荐交谈：用于推荐与检索的多模态嵌入. In MuRS 2024: 2nd Music Recommender Systems Workshop, 2024.

[17] S. Oramas, O. Nieto, M. Sordo, and X. Serra. 面向冷启动音乐推荐的深度多模态方法. In Proceedings of the 2nd workshop on deep learning for recommender systems, pages 32–37, 2017.

[18] E. Palumbo, G. Penha, A. Damianou, J. L. R. García, T. C. Heath, A. Wang, H. Bouchard, and M. Lalmas. Text2Tracks：经由生成式检索的基于提示的音乐推荐. arXiv preprint arXiv:2503.24193, 2025.

[19] B. G. Patra, D. Das, and S. Bandyopadhyay. 为音乐推荐系统检索相似歌词. In Proceedings of the 14th International Conference on Natural Language Processing (ICON-2017), 2017.

[20] S. Rajput, N. Mehta, A. Singh, R. Hulikal Keshavan, T. Vu, L. Heldt, L. Hong, Y. Tay, V. Tran, J. Samost, et al. 基于生成式检索的推荐系统. Advances in Neural Information Processing Systems, 36:10299–10315, 2023.

[21] S. Rendle, C. Freudenthaler, Z. Gantner, and L. Schmidt-Thieme. BPR：来自隐式反馈的贝叶斯个性化排序. arXiv preprint arXiv:1205.2618, 2012.

<!-- 原 PDF 第 8 页 -->

[22] S. E. Robertson and S. Walker. Okapi/Keenbow 在 TREC-8 上的结果. In TREC, 1999.

[23] M. Schedl, S. Brandl, O. Lesota, E. Parada-Cabaleiro, D. Penz, and N. Rekabsaz. LFM-2b：用于推荐系统研究与公平性分析的富化音乐收听事件数据集. In Proceedings of the 2022 Conference on Human Information Interaction and Retrieval, 2022.

[24] T. Schick, J. Dwivedi-Yu, R. Dessì, R. Raileanu, M. Lomeli, E. Hambro, L. Zettlemoyer, N. Cancedda, and T. Scialom. Toolformer：语言模型可以自学使用工具. Advances in neural information processing systems, 2023.

[25] X. Su. 协同过滤技术综述，2009.

[26] R. Surana, A. Namburi, G. Mundada, A. Lal, Z. Novack, J. McAuley, and J. Wu. MusicRS：以音频为中心的对话式推荐基准. arXiv preprint arXiv:2509.19469, 2025.

[27] M. Tschannen, A. Gritsenko, X. Wang, M. F. Naeem, I. Alabdulmohsin, N. Parthasarathy, T. Evans, L. Beyer, Y. Xia, B. Mustafa, et al. SigLIP 2：语义理解、定位与稠密特征均有改进的多语言视觉—语言编码器. arXiv preprint arXiv:2502.14786, 2025.

[28] A. Van den Oord, S. Dieleman, and B. Schrauwen. 基于深度内容的音乐推荐. Advances in neural information processing systems, 26, 2013.

[29] O. Weller, M. Boratko, I. Naim, and J. Lee. 论基于嵌入的检索的理论局限. arXiv preprint arXiv:2508.21038, 2025.

[30] S. Wu, Z. Guo, R. Yuan, J. Jiang, S. Doh, G. Xia, J. Nam, X. Li, F. Yu, and M. Sun. CLaMP 3：跨未对齐模态与未见语言的通用音乐信息检索. arXiv preprint arXiv:2502.10362, 2025.

[31] Y. Wu, K. Chen, T. Zhang, Y. Hui, T. Berg-Kirkpatrick, and S. Dubnov. 结合特征融合与关键词到描述增强的大规模对比式语言—音频预训练. In ICASSP 2023-2023 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP). IEEE, 2023.

[32] A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao, C. Huang, C. Lv, et al. Qwen3 技术报告. arXiv preprint arXiv:2505.09388, 2025.

<!-- 原 PDF 第 9 页 -->

## 附录 A 工具调用函数

本附录以 Python 风格说明智能体所使用的可调用工具。沿袭先前工作 [24, 5]，每一块给出函数签名、用途、输入参数与期望返回值。所有工具都返回至多 `topk` 个 `track_id` 字符串组成的列表，并设计为在检索—重排序流水线中按顺序组合。

```python
def sql(sql_query: str, topk: int) -> list[str]:
    """
    执行 SQL 查询，用于布尔（结构化）匹配。
    必须返回带有 track_id 的结果
    （例如 ‘SELECT track_id FROM tracks WHERE ...’）。
    SQL 模式（表：tracks）：
        track_id      TEXT PRIMARY KEY
        title         TEXT
        artist        TEXT
        album         TEXT
        popularity    INTEGER
        release_date  DATE (YYYY-MM-DD)
        tempo         REAL
        key           TEXT
    参数：
        sql_query：要执行的 SQL 查询字符串。
        topk：要返回的 track_id 的最大数量。
    返回：
        List[str]：至多 ‘topk’ 个 track_id。
    """

def bm25(query: str, corpus_type: str, topk: int) -> list[str]:
    """
    执行 BM25 检索，用于词汇匹配。
    将所有输入字符串转为小写。
    BM25 语料库：
        ’title’      ：曲目名的小写形式
        ’artist’     ：艺人名的小写形式
        ’album’      ：专辑名的小写形式
        ’lyrics’     ：歌词的小写形式
        ’attributes’ ：流派、乐器、情绪、主题、用途等的小写形式
    参数：
        query：搜索查询字符串。
        corpus_type：取 {"title", "artist", "album", "lyrics", "attributes"} 之一。
        topk：要返回的 track_id 的最大数量。
    返回：
        List[str]：至多 ‘topk’ 个 track_id。
    """

def text_to_item_similarity(
    query: str, modality_type: str,
    vector_db_type: str, topk: int
) -> list[str]:
    """
    执行文本到物品的语义相似度检索。
    参数：
        query：搜索查询字符串。
        modality_type：取 {"text", "audio", "image"} 之一。
```

<!-- 原 PDF 第 10 页 -->

```python
        vector_db_type：取 {"metadata", "lyrics", "attributes", "audio", "image"} 之一。
        topk：要返回的 track_id 的最大数量。
    返回：
        List[str]：至多 ‘topk’ 个 track_id（与文本查询最相似）。
    """

def item_to_item_similarity(
    track_id: str, modality_type: str,
    vector_db_type: str, topk: int
) -> list[str]:
    """
    执行物品到物品的相似度检索（基于样例的推荐）。
    注：‘track_id’ 是长度为 22 的字符串。
    参数：
        track_id：唯一曲目标识。
        modality_type：取 {"audio", "image", "cf"} 之一。
        vector_db_type：取 {"audio", "image", "cf"} 之一。
        topk：要返回的 track_id 的最大数量。
    返回：
        List[str]：至多 ‘topk’ 个与输入物品相似的 track_id。
    """

def user_to_item_similarity(user_id: str, topk: int) -> list[str]:
    """
    执行用户到物品的相似度检索（个性化）。
    只使用人口统计/画像信息中的 ‘user_id’。
    若 ‘user_type’ 为 "cold_start"，不要选择该工具。
    参数：
        user_id：唯一用户标识（字符串）。
        topk：要返回的结果的最大数量。
    返回：
        List[str]：至多 ‘topk’ 个个性化 track_id。
    """

def semantic_id_matching(
    modality_type: str,
    indices: list[int],
    topk: int
) -> list[str]:
    """
    通过码本索引查找执行 Semantic ID 匹配。
    参数：
        modality_type：取 {"audio", "image", "metadata", "lyrics", "attributes", "cf_item"} 之一。
        indices：码索引列表（例如残差 VQ 码）。
        topk：要返回的结果的最大数量。
    返回：
        List[str]：至多 ‘topk’ 个由 Semantic ID 匹配到的 track_id。
    """
```

<!-- 译完 -->
