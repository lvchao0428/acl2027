# AGRec：以图推理适配自回归解码器的 LLM 序列推荐
> 来源文件：AGRec - Adapting Autoregressive Decoders with Graph Reasoning for LLM-based Sequential Recommendation.pdf
> 发表年份：2025
> 单位：Yamanashi University
## 英文原文摘要（Original Abstract）
Autoregressive decoders in large language mod-els (LLMs) excel at capturing users’ sequen-tial behaviors for generative recommendations. However, they inherently struggle to leverage graph-structured user-item interactions, which are widely recognized as beneficial. This pa-per presents AGRec, adapting LLMs’ decoders with graph reasoning for recommendation. We reveal that LLMs and graph neural networks (GNNs) manifest complementary strengths in distinct user domains. Building on this, we augment the decoding logits of LLMs with an auxiliary GNN model to optimize token gener-ation. Moreover, we introduce a rankable finite state machine to tackle two challenges: (1) ad-justing autoregressive generation with discrimi-native decoders that directly predict user-item similarity, and (2) token homogeneity, where LLMs often generate items with similar prefix tokens, narrowing the scope of beam search. Our AGRec outperforms state-of-the-art mod-els in sequential recommendations.
## 中文翻译（Chinese Translation）
大语言模型（LLM）中的自回归解码器擅长捕捉用户的序列行为，适用于生成式推荐。然而，它们本质上难以利用图结构的用户-商品交互信息，而这类信息被公认为是有益的。本文提出 AGRec，将图推理引入 LLM 的解码器以服务推荐。我们发现 LLM 与图神经网络（GNN）在不同用户域上呈现出互补优势。基于此，我们用一个辅助 GNN 模型来增强 LLM 的解码 logits，以优化 token 生成。此外，我们引入一个可排序的有限状态机来应对两大挑战：(1) 用直接预测用户-商品相似度的判别式解码器来调整自回归生成；(2) token 同质化问题——即 LLM 往往生成前缀 token 相近的商品，从而缩小束搜索（beam search）的搜索范围。我们的 AGRec 在序列推荐上优于当前最优模型。
