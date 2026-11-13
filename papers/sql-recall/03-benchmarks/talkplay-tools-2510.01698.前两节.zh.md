> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

原文件名：talkplay-tools-2510.01698.pdf

原文标题：TalkPlay-Tools: Conversational Music Recommendation with LLM Tool Calling

作者：Seungheon Doh\*、Keunwoo Choi\*、Juhan Nam（Doh 与 Choi 属 KAIST 与 talkpl.ai；Nam 属 KAIST。\* 为同等贡献。通讯作者为 seungheondoh@kaist.ac.kr 与 juhan.nam@kaist.ac.kr）

场合：预印本，arXiv:2510.01698v4 [cs.IR]，2026 年 6 月 2 日。项目页 https://talkpl-ai.github.io/talkplay_tools。首页未见已确定的会议出版信息。

## 摘要

LLM 已经能做带自然语言交互的生成式推荐，但推荐行为仍然窄，元数据和属性过滤这些更简单、却很关键的部件没有被用起来。作者提出一套基于 LLM 工具调用的音乐推荐，把它做成统一的检索–重排流水线。LLM 位于端到端位置：理解用户意图、规划调用哪些工具、再调度专门部件。这些部件包括布尔过滤（SQL）、稀疏检索（BM25）、稠密检索（嵌入相似度）和生成式检索（Semantic ID）。

通过工具规划，系统要预测用哪几类工具、按什么顺序执行、参数是什么，从而找到符合偏好的音乐；同时支持多种模态，并把多种数据库过滤接在一起。作者认为，按查询选用合适的检索方法后，这套统一框架在多种推荐场景上能达到有竞争力的效果，并把它看作对话式音乐推荐的一种新范式。

## 1 Introduction

音乐推荐长期就是按用户偏好过滤数据库。早期用布尔过滤处理收听日志和标题、艺人、发行年份等元数据。曲库变大、用户–物品特征学习出现之后，主流变成由大规模用户和物品嵌入驱动的检索再重排。表示学习又从只看收听历史走到更深的内容理解：音频、歌词和封面支持基于例子的推荐，多模态表示则支持自然语言查询。最近的 LLM 推荐把物品放进语义空间，再量化成离散 Semantic ID，于是既能生成式推荐，也能和用户多轮对话，让人按目标和偏好主动找音乐。

只靠一种检索方法，找不全真正满足需求的物品。生产系统是多阶段、会路由的检索–重排，还要同时守住运营约束（用户画像、曲风、心情、活动、新旧等），并反映收听历史和文本查询。不把多种检索合在一起，就盖不住推荐所需的全部上下文。

本文的对话式音乐推荐因此用工具调用。贡献有三条：把对话音乐推荐写成多种检索方法的组合，让 LLM 根据用户画像和对话上下文预测工具类型、顺序和参数；设计统一工具集，在同一个代理下包括布尔过滤（SQL）、稀疏检索（BM25）、跨模态稠密检索（text-to-item、item-to-item、user-to-item）和生成式检索（Semantic ID）；并在一个对话推荐基准上展示零样本效果，Hit@K 高于强基线，同时分析这些工具的行为。具体 Hit@K 数字在后面的实验节，这两节没有给出。

## 2 Music Recommendation with Tool Calling

Figure 1 把系统分成两块：Music Recommendation Agent（LLM 加工具）和 External Environment（执行工具，并做最终的检索与重排）。

**2.1 问题形式。** 给定用户 \(u\)、画像 \(p_u\)、上一轮对话状态 \(s_{t-1}\) 和当前轮查询 \(q_t\)，系统给出排序后的音乐列表 \(m_t\)。先由 LLM 生成工具调用，再用这些调用去过滤数据库 \(D\)；然后再次调用 LLM，生成既解释推荐、又保持对话上下文的自然语言回复 \(r_t\)。三步写成：\(C_t=\mathrm{LLM}(q_t,s_{t-1},p_u;P_{\mathrm{tool}},T)\)，\(m_t=\mathrm{ToolEnv}(C_t;D)\)，\(r_t=\mathrm{LLM}(m_t,q_t,s_{t-1},p_u;P_{\mathrm{response}})\)。\(T\) 是可用工具，\(P\) 是提示，\(C_t\) 是长度为 \(N\) 的 \((\mathrm{tool}_n,\mathrm{args}_n)\) 序列。执行环境是顺序流水线：每个工具的输出直接收窄下一个工具面对的曲目池，所以顺序会明显影响最终质量。提示 \(P_{\mathrm{tool}}\) 要求模型不要把推荐当成一次操作，而要分成检索阶段和重排阶段。

**2.2 工具。** Table 1 按能力、环境和查询例子比较各工具；表注说明，灰色文字表示由上下文信息触发、而不是由用户直接的自然语言查询触发。SQL 做布尔检索和数值过滤，环境是 SQL Server。音乐元数据收成一张表，字段包括 title、artist、album、发行日期、tempo、key、popularity。参数是 SQL 语句和 topk，例子是选出 2020 年及以后的曲目并按 tempo 排序、取 100 条；表中的问法例子是 “Recent songs over 130 BPM”。BM25 做词法匹配，适合有错字、难以精确字符串匹配的文本。语料有五份：title、artist、album、lyrics，以及作为语义标签的 attributes。参数是 query、corpus、topk，例子是在 artist 语料里查 “taylor swift songs”、取 100 条；表中例子是 “Songs from Adele’s 21”。Text-to-Item 用预训练文本编码器和多模态编码器，在对应嵌入空间里按余弦相似度找内容。环境列写的是 Qwen3、CLAP、SigLIP2。参数包括查询、物品模态、向量库和 topk，例子是按封面检索 “专辑封面里有婴儿在水下游泳”，模态和向量库都是 image，topk 为 20；表中短例子是 “Play a calm piano piece”。Item-to-Item 做基于例子的推荐：LLM 根据先前推荐或用户给出的例子生成 track ID，再从预先抽好的向量库取嵌入做相似度检索，编码器包括 CLAP、SigLIP2 和 BPR。例子是对 track ID `22L7bfCiAkJo5xGSQgmiIO` 按音频找相似，topk 为 20；表中短例子是 “Ok, more similar voices”。User-to-Item 用收听历史训练出的用户嵌入做个性化，不由查询触发，而由画像里的用户 ID 触发，参数是 user_id 和 topk，例子是 user_id 10021、topk 200，训练方法为 BPR。Semantic ID 是从内容特征得到的离散表示：先编码成稠密向量，再用 Residual Vector Quantizer 量化成码本下标，作为帮助 LLM 理解音乐多模态属性的上下文。系统为码位到物品 ID 建倒排索引，支持精确码匹配或小编辑距离。参数是模态、下标和 topk，例子是音频模态、下标 [52, 42, 5, 9]、topk 20；表中另一例是 audio:semantic_id:[63, 36, 44, 3]。

**2.3 推理时的上下文。** 推荐条件是送给 LLM 的四类信息。系统提示分两套：工具调用和回复生成。工具调用再拆成三阶段：规划时选定检索工具和重排工具并给出理由；检索时从音乐库至少取出 topk 个不重复的 track_id；重排时用选定的重排工具重排候选。约束是工具必须按检索再到重排的顺序使用，角色互补、功能不重叠。回复提示要说清结果，并让曲目与用户查询对齐。工具函数以 JSON schema 提供名称、描述和参数类型，例子在附录。用户画像包括人口统计（User ID、类型、年龄组、性别）和近期收听：听歌会话里最近五首的元数据、属性以及 Semantic ID；User ID 用来正确触发 User-to-Item。先前对话状态包括用户查询、推荐过的音乐和 LLM 回复；为了带上多模态信息，上下文里不只放 track ID，还有元数据、属性和 Semantic ID。实验设置、数据和 Hit@K 结果从第 3 节才开始。
