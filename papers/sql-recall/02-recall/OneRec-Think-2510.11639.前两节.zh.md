> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名**：OneRec-Think-2510.11639.pdf

**原文标题**：OneRec-Think: In-Text Reasoning for Generative Recommendation

**作者**：Zhanyu Liu、Shiyao Wang、Xingmei Wang、Rongzhou Zhang、Jiaxin Deng、Honghui Bao、Jinghao Zhang、Wuchao Li、Pengfei Zheng、Xiangyu Wu、Yifei Hu、Qigen Hu、Xinchen Luo、Lejian Ren、Zixing Zhang、Qianqian Wang、Kuo Cai、Yunfan Wu、Hongtao Cheng、Zexuan Cheng、Lu Ren、Huanjie Wang、Yi Su、Ruiming Tang、Kun Gai、Guorui Zhou。均署 Kuaishou Inc., Beijing, China。Zhanyu Liu 与 Shiyao Wang 为同等贡献。Guorui Zhou 为通讯作者。

**场合 / arXiv**：前两节与首页未见会议名称。arXiv:2510.11639v2 [cs.IR]，2025-11-11。

## 摘要

LLM 的生成能力把推荐推向了新范式，但现有生成模型（例子是 OneRec）仍是隐式预测器，缺少 LLM 那种显式、可控的推理。OneRec-Think 把对话、推理和个性化推荐收进同一个框架，包含三块：Itemic Alignment，即跨模态的 Item-Textual Alignment，用来把物品语义锚住；Reasoning Activation，用 Reasoning Scaffolding 在推荐上下文里激活 LLM 的推理；Reasoning Enhancement，设计考虑用户偏好“多个答案都可能成立”的推荐专用奖励。公开基准上称达到当时最优。面向工业的 “Think-Ahead” 架构在 Kuaishou 上部署，APP Stay Time 提升 0.159%，用来说明显式推理可以落地。

## 1 Introduction

生成式检索（generative retrieval, GR）用基于 Transformer 的 sequence-to-sequence 模型，自回归地解码目标候选的标识，取代传统的 query–candidate 匹配。由此出现端到端生成框架，点名 OneRec、OneLoc、OneSug、OneSearch。它们替换原来分开做召回和排序的多阶段漏斗，把优化对准最终目标，并把算力集中起来，便于工业上放大。这些模型用上了 LLM 的生成能力，却没有现代 LLM 突破所依赖的、可核验的显式推理路径，例如文本上的 Chain-of-Thought（CoT）。

OneRec-Think 把对话、推理和个性化生成推荐放进同一个模型，能生成可解释的文本推理路径，并称同时提高推荐准确性和用户信任；对话属性还可以按用户当下的约束改推荐，Fig. 1 给出描述视频、根据历史描述用户、边想边推荐，以及按“想看轻松内容”这类即时要求改推荐的例子。实现分三阶段。Itemic Alignment 把物品语义映进 LLM 的文本 embedding 空间，形成统一表示，从而打开推理能力。Reasoning Activation 要在推荐系统的上下文里引出 LLM 本来就有的推理。Reasoning Enhancement 用推荐专用奖励，刻画用户偏好的 multi-validity，即多个选择都可能成立。另外提出 OneRec-Think Inference Architecture，保证工业规模服务时的部署效率和实时响应。贡献对应三条：打通离散推荐物品和连续推理空间，使个性化推荐能嵌进 LLM 的自然语言理解；把多步斟酌和推荐优化编排在一起，通过协同训练得到可解释、又顾及准确性的个性化推荐；多个公开基准上称 SOTA，部署友好的 “Think-Ahead” 架构带来工业影响，APP Stay Time 提升 0.159%。这两节没有表格。第 3 节起的符号定义与第 4 节方法不在本导读范围内。

## 2 Related Work

### 2.1 Reasoning in Large Language Models

LLM 的复杂推理从提示技术讲起。CoT prompting 是基础，把问题拆成中间推理步骤；由此延伸出 zero-shot CoT、self-consistency decoding 和 tree-of-thoughts。这些技术支持 test-time scaling：推理时多花计算可以提升效果。近期重点从提示转到后训练，用强化学习加强推理，点名 DeepSeek-R1 和 Seed-1.5，所用技术包括 GRPO、DAPO 和 VAPO。

### 2.2 Reasoning-Based Recommendation

TIGER、HSTU、OneRec 这类生成式推荐有效，但本身没有推理。推理式推荐想用多步推导换更准、更可解释的结果，现有工作分成两类：显式推理生成人能读的理由，但局限在判别式任务；隐式推理在潜空间里推理，没有文本可解释性。本文把显式推理引进生成式推荐，希望同时有可解释的理由和可扩展的物品生成。本节没有实验数字或表号。
