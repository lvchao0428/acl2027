# ONEREC-THINK: In-Text Reasoning for Generative Recommendation

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`OneRec-Think-2510.11639.pdf`。

## Abstract 摘要

大语言模型（Large Language Models, LLMs）强大的生成能力，已经在推荐中引发了范式转变。然而，现有生成式模型（例如 OneRec）是隐式预测器，严重缺乏显式且可控的推理能力，而这正是 LLM 的一项关键优势。为弥补这一差距，我们提出 OneRec-Think，一个把对话、推理与个性化推荐无缝整合在一起的统一框架。OneRec-Think 包含：（1）Itemic Alignment：用于语义落地的跨模态 Item-Textual Alignment；（2）Reasoning Activation：用 Reasoning Scaffolding 在推荐语境中激活 LLM 的推理；（3）Reasoning Enhancement，我们在此设计一个面向推荐的奖励函数，以考虑用户偏好的多有效性（multi-validity）。在公开基准上的实验显示了最先进的表现。此外，我们提出的 “Think-Ahead” 架构能够在快手（Kuaishou）上有效地工业部署，使 APP Stay Time 提升 0.159%，从而验证了该模型显式推理能力的实际效力。

## 1 Introduction 引言

大语言模型（LLMs）的快速发展已经从根本上重塑了推荐系统，引出了生成式检索范式（generative retrieval, GR）（Peng et al., 2025; Zhang et al., 2025b; Deldjoo et al., 2024; Li et al., 2023; Wang et al., 2023）。这一途径代表了相对传统查询–候选匹配的深刻转变：它使用基于 Transformer 的序列到序列模型，自回归地解码目标候选的标识符。在此基础上，一个主要研究前沿是端到端生成式框架的发展，包括 OneRec、OneLoc、OneSug 和 OneSearch（Deng et al., 2025; Zhou et al., 2025a,b; Wei et al., 2025; Guo et al., 2025b; Chen et al., 2025）。这些统一模型取代了传统的多阶段推荐漏斗（包含彼此分开的检索与排序阶段），从而能够面向最终目标做整体优化，并把计算资源集中起来，以获得更好的工业扩展性与表现。

虽然这些模型成功地利用了 LLM 的输出生成能力，它们从根本上缺少定义现代 LLM 突破的那种显式、可验证的推理路径，例如基于文本的思维链（Chain-of-Thought, CoT）（Rajput et al., 2023; Zheng et al., 2024; Wang et al., 2024b）。为弥补这一关键差距，我们提出 OneRec-Think，一个在单一统一模型中整合对话、推理与个性化生成式推荐的新框架。它能够生成高质量、可解释的文本推理路径，从而显著提升推荐准确性和用户信任度。模型内在的对话性质进一步使建议能够针对具体的用户约束动态调整（如图 1 所示）。我们的方法通过一个三阶段框架实现：（1）Itemic Alignment，把物品语义映射到 LLM 的文本嵌入空间，建立一个统一的表示连续体，从而释放模型的推理能力；（2）Reasoning Activation，旨在直接于推荐系统语境中诱发 LLM 固有的推理能力；（3）Reasoning Enhancement，使用一个面向推荐的奖励函数，以捕捉用户偏好的多有效性（multi-validity，即多个都有效的选择）。此外，我们引入 OneRec-Think Inference Architecture，以确保在工业规模服务场景中的高效部署与实时响应。

我们的贡献概括如下：

- 我们引入一个统一框架，弥合离散推荐物品与连续推理空间之间的语义差距，使个性化推荐能够无缝整合进 LLM 的自然语言理解之中。
- 我们设计一种新的推理范式，把多步斟酌与推荐优化编排在一起，通过协同训练实现可解释且兼顾准确性的个性化推荐。
- 所提出的方法在多个公开基准上取得最先进结果；同时，便于部署的 “Think-Ahead” 架构带来显著的工业影响，使 APP Stay Time 提升 0.159%。

图 1 的示例插在“端到端生成式框架”一句中间，图注为：OneRec-Think 统一对话、推理与推荐框架的示例。可读示例要点如下（物品 ID 保持原文）：

- 提示要求描述 `<item_a_8121><item_b_3259><item_c_6391>` 的内容，并注明这些是一条视频的 itemic ID。随后的街市场景描述因空格抽取粘连，大意为熙攘的街头市场、各种食品摊与小贩叫卖，提到烤串、炒饭、煎饼和糖葫芦；若干粘连片段【抽取不清】。
- 另一提示要求根据交互历史描述用户偏好。历史中出现 Liked and favorited、Liked、Favorited 等行为及对应 itemic ID。Primary Interests 一行空格散落，可读部分为：喜欢幽默短剧、影片分析（超过 60% 的内容）和轻松娱乐，也会接触 Honor of Kings 内容，表明有休闲游戏兴趣。Secondary Interests：多样探索包括宠物（猫）视频、传统文化和本地美食内容。粘连处【抽取不清】。
- 随后的推荐示例较清晰：用户观看历史主要以国际关系与军事动态为主，对军事装备与技术进展、尤其是国家安全与国际竞争有强烈兴趣，因而可能继续观看他国军事发展、国际冲突分析或国防政策解读。一条聚焦中国军事技术进步、特别是新 J-35 战斗机首秀（标志着一次重大技术突破）的候选视频与这些兴趣高度相关：`<item_a_5083><item_b_2280><item_c_5301>`。
- 基于用户对军事主题和动作冒险游戏的兴趣（体现为接触 Battlefield 内容与 GTA6 爆料），以及为获得最佳游戏性能而主动比较 GPU，推荐视频为 `<item_a_4029><item_b_4601><item_c_5058>`。
- 用户主动搜索如何与叛逆青少年沟通，表明关注亲子关系或青少年教育难题，需要改善沟通的实用策略。提供有效沟通技巧的专业指导会直接回应这一需求，因此推荐视频 `<item_a_6786><item_b_4138><item_c_1091>` 高度相关。
- 图中还有 Rollout-1、Rollout-2、Rollout-3，均标注为 Reasoning and Recommendation。一段对话请求为：“我有点低落。能否推荐一些愉快、轻松的视频？”并注明该用户的历史行为与上文相同。模型在承认历史可能指向动作冒险或军事主题内容的同时，对齐用户对温暖、振奋内容的明确请求，优先推荐轻松游戏、动画和减压视频（如 Frozen、Zootopia 这类暖心故事，猫狗宠物 vlog，北极熊或珊瑚礁等自然纪录片），同时排除暴力、恐怖或制造紧张的内容，并提高积极励志短视频的比例。
- 图中还可辨认的短标签包括 Prompt、Describe the user、Think&Recommend、Interactive Recommendations、Historical Interactions。这些标签与长文本的版面顺序交错，连接关系【抽取不清】。

## 2 Related Work 相关工作

### 2.1 Reasoning in Large Language Models 大语言模型中的推理

大语言模型通过多种提示技术实现复杂推理，其中思维链提示（CoT prompting）（Wei et al., 2022）是基础方法，它把问题分解为中间推理步骤。这启发了众多扩展，包括 zero-shot CoT（Kojima et al., 2022）、self-consistency 解码（Wang et al., 2022）以及 tree-of-thoughts（Yao et al., 2023）。这些技术实现了测试时扩展（test-time scaling）：推理期间增加计算预算可以提升表现（Snell et al., 2024）。近期工作把焦点从提示转移到用强化学习等技术做后训练，以增强推理能力。包括 DeepSeek-R1（Guo et al., 2025a）和 Seed-1.5（Seed et al., 2025）在内的模型，通过 GRPO（Shao et al., 2024）、DAPO（Yu et al., 2025）和 VAPO（Yue et al., 2025；原文抽取为 “V APO”）等技术优化推理行为，显示了这一方向上有希望的进展。

### 2.2 Reasoning-Based Recommendation 基于推理的推荐

尽管 TIGER（Rajput et al., 2023）、HSTU（Zhai et al., 2024）和 OneRec（Zhou et al., 2025a）等生成式推荐模型已经展示了有效性，它们内在地缺少推理能力。最近，基于推理的推荐系统旨在进行多步推导，以得到更准确、更可解释的推荐。现有方法分为两类：显式推理（explicit reasoning）方法生成人类可读的理由，但局限于判别式任务（Tsai et al., 2024; Bismay et al., 2024; Fang et al., 2025; Kim et al.）；隐式推理（implicit reasoning）方法（Zhang et al., 2025a; Tang et al., 2025）进行潜在推理，但没有文本可解释性。我们的工作把显式推理引入生成式推荐，弥合这一差距，从而既能给出可解释的理由，又能规模化地生成物品。
