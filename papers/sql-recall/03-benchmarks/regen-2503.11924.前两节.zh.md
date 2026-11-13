> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

原文件名：regen-2503.11924.pdf

原文标题：REGEN: A Dataset and Benchmarks with Natural Language Critiques and Narratives

作者：Kun Su\*、Krishna Sayana\*、Hubert Pham\*、James Pine\*、Yuri Vasilevski\*、Raghavendra Vasudeva、Marialena Kyriakidi、Liam Hebert†、Ambarish Jash、Anushya Subbiah、Sukhdeep Sodhi（\* 为同等贡献。除 Hebert 外均属 Google Research，Mountain View。Hebert 属 University of Waterloo，† 表示该工作完成于其在 Google Research 期间）

场合：arXiv:2503.11924v2 [cs.CL]，2025 年 7 月 11 日。首页 ACM 模板未填实：会议名仍是 Conference acronym ’XX，版权年为 2018，DOI 为占位符，因此这不是一份已确定会议版本的论文。

## 摘要

现有数据大多只支持按序列预测下一个物品，不够用来衡量推荐大模型会不会对话。REGEN（Reviews Enhanced with GEnerative Narratives）在 Amazon Product Reviews 上补两类自然语言：用户 critique，也就是把系统推向下一件物品的 “steering” 查询；以及 narrative，即结合先前上下文、附在每件被推荐物品上的长文本，包括产品背书、购买解释和用户偏好摘要。

作者还定了一个端到端的对话推荐基准：模型根据用户历史（物品和 critique）同时生成推荐和对应叙事。为此提出 LUMEN（LLM-based Unified Multi-task Model with Critiques, Recommendations, and Narratives），用 LLM 做批判、检索和生成的骨干。数据质量用常规自动评分检查，并用传统推荐模型和基于 LLM 的模型做基准。结果是：加入 critique 能提高推荐质量，因为推荐器学会了语言理解，并把它和推荐信号接在一起；在该数据上训练的 LLM 能同时给出推荐和情境化叙事，效果与当时的推荐系统和语言模型相当。

## 1 Introduction

对话推荐除了给个性化物品，还要能解释、并根据用户的自然语言反馈改推荐。LLM 看起来能承担这里的语言能力，但现有训练数据缺少丰富的情境叙事和显式用户反馈。没有这类数据，生成文本就很难和推荐物品、用户偏好保持一致。近期把推荐器内部状态接到 LLM 上的工作，仍受限于只含物品序列、短对话片段、结构化输出或很短摘要的数据。

向真实用户采集这种数据很难，通常要大批人与对话推荐系统交互。作者沿用一种假设：LLM 可以从已有行为轨迹推断偏好和目标，并生成与真实行为一致、看起来说得通的叙事和回复；好处是能直接扩充已有的流行序列推荐数据。REGEN 就这样扩充 Amazon Reviews。Figure 1 用 Avery 活页夹的购买序列举例：用户反馈写成 “2-inch slant rings, tear-resistant spine and edges” 这类 critique；系统推荐 Avery 2" Durable View 3 Ring Binder，并配上三类叙事——产品背书、购买原因（需要大容量活页夹来整理大量文件），以及用户摘要（常买 Avery、看重耐用和容量）。叙事还包括购买理由、解释、产品背书、用户摘要和简短用户画像，都按用户个性化。Critique 是用户对推荐作出的自然语言反馈，用来把推荐器往下一次选择上推。填充这些字段用的是 Gemini 1.5 Flash 的 few-shot 提示，输入来自原始数据里的评分历史、评论文本和物品描述。质量先用一个 auto-rater LLM 自动检查，重点是依据历史交互看接地和事实性。

作者认为还缺一个把行为和推荐合在一起的训练任务，否则很难评模型是否自洽。以往模型常把推荐、评分预测、评论生成拆成不同目标。他们提出单轮对话任务，作为走向完整多轮对话推荐的一步：输入是物品历史，以及穿插在部分物品之间的 critique；输出是下一件要推荐的物品，以及与该物品和用户偏好一致的叙事。模型必须在同一轮里同时做好个性化序列推荐、批判和自然语言生成。参考模型是 LUMEN：一个 LLM 骨干，把协同过滤信号、内容信号和自然语言 critique 合在一起，生成推荐和叙事。贡献有四条：开源数据，并检查事实性、接地和对用户上下文的反映，地址为 https://www.kaggle.com/datasets/googleai/regen-reviews-enhanced-with-generative-narratives；一个面向完整对话推荐的对应任务；把生成式推荐和语言任务合在一起、效果可与当时推荐系统和语言模型相比的参考模型；以及验证模型能学会生成有上下文的叙事，并用 critique 动态引导推荐，还能生成连贯的对话轨迹。具体实验数字不在这两节。

## 2 Related Work

相关工作从数据集和任务两侧说明 REGEN 补的是什么。2.1.1 的对话数据多是用户与代理的对话：DuRecDial 是众包、多领域、带预定义目标的对话；E-ConvRec 来自真实售前客服对话；ReDial 是电影推荐对话标注，TG-ReDial 加上话题引导，E-Redial 加上外部知识以改善可解释性。这些数据重在构造或收集对话，对话和用户底层偏好、历史行为往往对不上。LLM-Redial 用模板、从真实用户画像出发来造对话，和 REGEN 一样在意画像与叙事一致，但 REGEN 保留物品序列以维持时间一致性，从而能按过去行为生成反馈和叙事；它要的也不是短对话轮次，而是一个懂行的对话推荐器可能说出的个性化长叙事，用来测验推荐器在物品和偏好语境下的语言理解。

2.1.2 的叙事数据里，Ni 等人的 “Justifying Recommendations” 和 Chen 等人的 “Unlocking the Why of Buying” 从评论生成解释。Hou 等人的 Amazon-C4 构造复杂查询并关联到物品，用来评推荐任务。REGEN 在此之上做开放式叙事，条件是整段用户历史，用途也不限于购买解释，文本更长、更细，兼有半结构化和非结构化输出。2.1.3 的批判则回溯经典推荐里的 critiquing：早期多在特征层反馈，用预先设计的调整或语言对话；较新的工作联合学习用户、物品和关键短语的隐表示，用隐空间运算让批判影响推荐，也有工作解释属性以支持批判。这些工作给 REGEN 里的自然语言用户反馈提供了依据。

2.2 把任务分成两类。序列物品推荐已有大量把 LLM 和推荐接起来的研究，差别在于用 ID 嵌入还是文本嵌入表示交互，以及是否加入物品或语义上下文。物品推荐是 REGEN 支持的首要任务；因为它建在常用的 Amazon Reviews 上，作者认为适合把现有 LLM 序列推荐器扩成也能生成语言。另一类模型同时输出物品和文本：P5 把用户–物品信号和上下文都写成自然语言序列，送进编码器–解码器，并设了若干物品预测和文本生成任务族；User-LLM 把用户历史编成用户嵌入，用交叉注意力送进 LLM，支持下一物品推荐、类型预测和评论生成三项任务，但它们仍是分开的任务。REGEN 则要把推荐和文本生成、再加上用户反馈，收成一个连贯任务，并生成多样的长叙事。本节没有实验数字或表号。
