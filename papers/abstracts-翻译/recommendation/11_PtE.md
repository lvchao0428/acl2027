# From ID to LLM: Rethinking Representation Learning

> 来源文件：11_PtE.pdf

## 英文原文摘要（Original Abstract）

Recent studies indicate a fundamental incompatibility between ID representations and language model (LM) representations, as they capture behavioral and semantic spaces respectively. This mismatch leads LM representations to consistently underperform ID representations in recommendation tasks. In this work, we revisit this problem and show, from an information-theoretic perspective, that LLM representations retain all discriminative information in ID representations. Based on this, we introduce a Profile-then-Embedding (PtE) framework for recommendation, consisting of a Profile Stage, in which semantic user and item profiles are generated jointly through LLM-based bidirectional reasoning over user-item interactions, and a Personalized Embedding Stage, which encodes these profiles into task-aligned recommendation embeddings. We demonstrate PtE's effectiveness across three benchmark datasets, including cold-start and long-tail scenarios, achieving substantial gains in both discriminative and generative recommendation models.

## 中文翻译（Chinese Translation）

近期研究表明，ID 表示与语言模型（LM）表示之间存在根本不兼容：前者刻画行为空间，后者刻画语义空间。这种错配导致 LM 表示在推荐任务上始终不如 ID 表示。本工作重新审视该问题，并从信息论视角证明：LLM 表示保留了 ID 表示中的全部判别性信息。基于此，我们提出了 Profile-then-Embedding（PtE）推荐框架，包含两个阶段：Profile 阶段，通过基于 LLM 的双向推理在用户-物品交互上联合生成语义化的用户与物品画像；Personalized Embedding 阶段，将这些画像编码为与任务对齐的推荐嵌入。我们在三个基准数据集（含冷启动与长尾场景）上验证了 PtE 的有效性，在判别式与生成式推荐模型上均取得了显著提升。
