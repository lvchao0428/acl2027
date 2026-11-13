> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名**：LLM2Rec-2506.21579.pdf

**原文标题**：LLM2Rec: Large Language Models Are Powerful Embedding Models for Sequential Recommendation

**作者**：Yingzhi He、Xiaohao Liu、An Zhang、Yunshan Ma、Tat-Seng Chua。Yingzhi He、Xiaohao Liu、Tat-Seng Chua 署 National University of Singapore；An Zhang 署 University of Science and Technology of China；Yunshan Ma 署 Singapore Management University。Yingzhi He 与 Xiaohao Liu 为同等贡献。An Zhang 为通讯作者。

**场合 / arXiv**：KDD ’25，Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.2，2025 年 8 月 3–7 日，Toronto, ON, Canada。ACM ISBN 979-8-4007-1454-2/2025/08，DOI 10.1145/3711896.3737029。同时为 arXiv:2506.21579v1 [cs.IR]，2025-06-16。

## 摘要

序列推荐要靠历史行为里的 collaborative filtering（CF）信号预测用户接下来会交互什么。传统做法主要用 ID embedding，从高阶共现里记 CF，但表示只来自过去的交互，缺少能迁到未见领域的知识。用文本描述抽物品表示能加强泛化，却编不进 CF，也就是物品之间的潜在相关和偏好模式。作者认为理想的 embedding 模型应同时带上 CF 和语义，兼顾域内与域外。LLM2Rec 因此分两段训练：Collaborative Supervised Fine-tuning 让 LLM 根据历史交互推断物品关系；Item-level Embedding Modeling 再把这种专用 LLM 收成结构化的物品 embedding，同时编码语义和协同信息。真实数据上的实验用来说明域内、域外的推荐质量都有提升。代码在 https://github.com/HappyPointer/LLM2Rec 。

## 1 Introduction

序列推荐被定义成学习物品表示，以同时抓住用户偏好和物品内容，从而预测未来交互。常规模型给物品唯一 ID，再从历史序列里学表示，CF 主要来自序列轨迹上的多跳共现。作者认为这种表示缺物品内容，强依赖领域，见不到新物品或新领域。高质量表示因此要同时装下语义和 CF。

围绕 LLM 的语义，已有纯文本表示，也有把语义和 CF 融合的混合表示。纯文本从预训练语言模型抽物品向量，泛化强，但不记 CF。混合路线包括：把 ID 表示和语义表示直接拼接；用内容特征指导 ID 表示学习；采用混合融合结构；以及微调 embedding 模型去接通 CF 空间和语义空间。作者认为，无论简单拼接还是 cross-attention 这类融合，都难以学到统一表示空间，物品语义和用户行为会对不齐。更值得做的是一个本身就同时含 CF 与语义的通用 embedding 模型。已有用对比预训练把语义对齐到行为空间的工作，通常要大规模样本和很大的 batch 才能编进 CF，也没有用上 Qwen、Llama 这类 LLM 的语义理解和推理。

LLM2Rec 的做法是：先用监督微调让 LLM 从交互序列里意识到 CF（依据是已有研究表明 LLM 能通过监督微调学会推荐任务），再把目标从 token 级预测转到物品级 embedding。两阶段分别是 Collaborative Supervised Fine-Tuning（CSFT）和 Item-level Embedding Modeling（IEM）。CSFT 在六个真实推荐数据集的混合上微调 LLM，令其根据历史序列预测下一个物品。Fig. 1 用任天堂游戏作例子：行为上相关的 Mario Party 与 Animal Crossing，在语言模型的 text embedding 上相似度是 0.18，在推荐器的 ID embedding 上相似度是 0.93。预训练阶段这几款游戏（Mario Party、Animal Crossing、Paper Mario、Yoshi）的点是散开的；它们常被偏好相近的用户一起购买，CSFT 之后聚成一团，用来说明 LLM 学到了 CF。第二阶段打开双向注意力，配合 Masked Next Token Prediction（MNTP），并做物品级对比学习。双向注意力用来抓住标题内部的上下文，MNTP 让 LLM 适应新的双向 mask；对比学习把预训练目标从 token 级改到物品级，使 embedding 更可区分，同时留住 CF。两者都被说成轻量。Fig. 1(d) 里这些游戏的点仍然靠近，但彼此拉开。实验覆盖域内和域外数据、多种下游序列推荐器；作者称 LLM2Rec 稳定优于已有 embedding 模型，且在跨品类混合数据上训练有助于泛化。这两节没有表格。

## 2 Related Work

### 2.1 Sequential Recommendation

从物品表示看，序列推荐被分成 ID、纯文本、ID–文本混合三类。ID 方法给每个物品唯一标识，用循环网络、卷积网络或 Transformer 从交互序列里学相关性和用户兴趣，但处理不了未见领域或未见物品。纯文本方法用标题或画像，经预训练语言模型得到文本 embedding；统一语言空间使其有机会泛化到未见领域，效果却受所用 embedding 模型限制，而这些模型是为语言任务预训练的，不是为推荐准备的。混合方法有三条常见技术：用文本 embedding 指导或增强 ID 表示学习；拼接文本与 ID embedding；用注意力结构融合 ID 和文本。它们仍然依赖 ID embedding，要在目标域上训练才有效，因此和新领域上的泛化一样受限制。

### 2.2 Embedding Models

预训练 embedding 模型被放到信息检索、文本相似度和分类等下游任务里，并分成两类。一类是带双向注意力的语言编码器，用 Transformer 抓上下文、产出句子 embedding；训练目标包括 next sentence prediction、masked language modeling，以及后来很常用的对比学习。另一类基于 LLM：直接从 decoder-only LLM 的最后隐状态取句子向量，用 EOS 的隐状态或对句中全部 token 做平均池化。作者认为未经额外训练就这样用，效果不好，因为原模型优化的是预测后续 token，不是整句表示。后续工作用句子级对比学习和修改 attention mask，把 LLM 收成专用 embedding 模型。

推荐里物品之间的隐式关系，即 CF，和语义同样重要。多数序列推荐器用的是通用 embedding 模型；也有人做推荐专用 embedding。Blair 用对比学习把用户评论的表示和物品标题对齐，数据来自 Amazon，超过 30 million 条实例、33 个类目。EasyRec 把用户表示和其交互过的物品对齐，并在对比学习里加入多种用户与物品画像。两者都把骨干限制在 BERT、RoBERTa 这类较小模型上，原因是对比学习要大 batch 和足够的训练迭代，计算贵。LLMEmb 改用 LLM，做属性级增强，并对同一物品的增强视图对齐；它主要把 LLM 当语义编码器，没有把 CF 明确写进所学 embedding。LLM2Rec 则用 collaborative supervised fine-tuning 把 CF 融进 LLM，再用轻量的物品级 embedding 适配，作者称这样能得到更好的推荐专用 embedding，同时保持计算效率。本节没有表格。
