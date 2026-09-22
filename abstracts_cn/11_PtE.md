# PtE: 从 ID 到 LLM——重新思考推荐的表示学习

**原标题**: From ID to LLM: Rethinking Representation Learning for Recommendation

**作者**: Song-Li Wu, Zhaocheng Du, Weinan Gan 等

**单位**: Tsinghua University; Huawei Noah's Ark Lab; USTC

## 摘要

近期研究表明 ID 表示与语言模型（LM）表示之间存在根本不兼容性，因为它们分别捕获行为空间和语义空间的信息。这种不匹配导致 LM 表示在推荐任务中持续弱于 ID 表示。在本工作中，我们重新审视这一问题，从信息论的视角证明 LLM 表示保留了 ID 表示中的所有判别性信息。基于此，我们引入**画像然后嵌入（Profile-then-Embedding, PtE）**推荐框架，包含：**画像阶段**——通过基于 LLM 的双向推理对用户-物品交互进行语义用户和物品画像联合生成；以及**个性化嵌入阶段**——将这些画像编码为与任务对齐的推荐嵌入。我们在三个基准数据集上展示了 PtE 的有效性，涵盖冷启动和长尾场景，在判别式和生成式推荐模型上均取得了显著提升。
