# 从 ID 到 LLM：重思推荐中的表示学习
> 来源文件：From ID to LLM - Rethinking Representation Learning for Recommendation.pdf
> 发表年份：2026
> 单位：Huawei Noah's Ark Lab；Tsinghua University
## 英文原文摘要（Original Abstract）
Recent studies indicate a fundamental incom-patibility between ID representations and lan-guage model (LM) representations, as they cap-ture behavioral and semantic spaces respec-tively. This mismatch leads LM representa-tions to consistently underperform ID repre-sentations in recommendation tasks. In this work, we revisit this problem and show, from an information-theoretic perspective, that LLM representations retain all discriminative infor-mation in ID representations. Based on this, we introduce a Profile-then-Embedding (PtE) framework for recommendation, consisting of a Profile Stage, in which semantic user and item profiles are generated jointly through LLM-based bidirectional reasoning over user-item interactions, and a Personalized Embed-ding Stage, which encodes these profiles into task-aligned recommendation embeddings. We demonstrate PtE’s effectiveness across three benchmark datasets, including cold-start and long-tail scenarios, achieving substantial gains in both discriminative and generative recom-mendation models.
## 中文翻译（Chinese Translation）
近期研究表明，ID 表示与语言模型（LM）表示之间存在根本的不兼容——二者分别刻画行为空间与语义空间。这种错位导致 LM 表示在推荐任务中始终逊于 ID 表示。本文重新审视这一问题，并从信息论视角证明：LLM 表示保留了 ID 表示中的全部可判别信息。基于此，我们提出 Profile-then-Embedding（PtE）推荐框架，包含两个阶段：画像阶段——通过 LLM 对用户-商品交互进行双向推理，联合生成语义化的用户与商品画像；个性化嵌入阶段——将这些画像编码为与任务对齐的推荐嵌入。我们在三个基准数据集上验证了 PtE 的有效性，覆盖冷启动与长尾场景，在判别式与生成式推荐模型上均取得显著提升。
