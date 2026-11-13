> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名：** TIGER-2305.05065.pdf

**原文标题：** Recommender Systems with Generative Retrieval

**作者：** Shashank Rajput（University of Wisconsin-Madison；与 Nikhil Mehta 共同一作；脚注说明工作完成于在 Google 期间），Nikhil Mehta、Anima Singh、Lichan Hong、Yi Tay、Maciej Kula、Ed H. Chi、Maheswaran Sathiamoorthy（Google DeepMind），Raghunandan Keshavan、Trung Vu、Lukasz Heldt、Vinh Q. Tran、Jonah Samost（Google）

**场合：** 37th Conference on Neural Information Processing Systems (NeurIPS 2023)。arXiv:2305.05065v3 [cs.IR]，2023 年 11 月 3 日。

## 摘要

现代推荐的大规模检索，通常是把查询和候选物品嵌到同一个空间，再用近似最近邻取出 top 候选。本文换成生成式检索：检索模型自回归地解码目标候选的标识。为此，每个物品得到一组有语义的 codeword，组成 Semantic ID。用户 session 里的物品都换成 Semantic ID 之后，用 Transformer 的 sequence-to-sequence 模型预测用户下一步会交互的物品的 Semantic ID。

摘要的结论是定性的：按这个范式训练的推荐系统，在多个数据集上明显超过当时的 SOTA。把 Semantic ID 放进序列模型还能加强泛化，证据是对没有历史交互的物品，检索效果也有提高。摘要没有给出具体的 Recall 或 NDCG 数字。

## 1 Introduction

推荐被放在 retrieve-and-rank 的框架里：检索先交出一批可行候选，排序模型只在这批候选上工作，所以检索阶段必须交出高度相关的物品。已有检索的标准做法是矩阵分解，把查询和候选嵌到同一空间；为了抓住非线性，后来流行双塔，一塔查询、一塔候选，用内积对齐，推理时用候选塔为全部物品建索引，查询塔算出查询向量后再做 Approximate Nearest Neighbors。双塔也被扩展到显式考虑交互顺序的序列推荐。

TIGER（Transformer Index for GEnerative Recommenders）不再做查询–候选匹配，而是用一个端到端生成模型直接预测候选 ID。它把 Transformer 的参数记忆当成推荐检索的端到端索引，想法来自把 Transformer 记忆用于文档检索的工作。Figure 1 用三双鞋说明表示法：原子 ID 分别是 233、515、64 的 “Orange shoes, Brand X”“Red shoes, Brand Y”“Orange shoes, Brand Y”，被 Semantic ID 生成器写成有序元组 (5, 23, 55)、(5, 25, 78)、(5, 25, 55)。相似鞋共享前面的码字。给定物品文本特征，先用预训练文本编码器（文中举例 SentenceT5）得到稠密内容嵌入，再量化成有序的 token / codeword，这串就是该物品的 Semantic ID，然后用来训练序列推荐的 Transformer。

作者认为语义 token 有几方面好处。在有语义的数据上训练，相似物品可以共享知识，因此可以不再使用以前当物品特征的原子 ID 和随机 ID。模型也不那么容易困在推荐系统固有的反馈环里，从而能泛化到语料里新加入的物品。用一串 token 表示物品，还能缓解物品库规模：可表示的物品数是序列中每个 token 的基数之积。物品库常常到十亿量级，为每个物品学一个独立嵌入很占内存。随机哈希可以压缩表示空间；本文要说明的是，有语义的 token 是更可取的替代。

贡献有三条。第一，TIGER 给每个物品分配 Semantic ID，并训练检索模型去预测用户可能交互的物品的 Semantic ID。第二，在多个数据集上，以 recall 和 NDCG 超过已有 SOTA；引言没有写出具体分数。第三，生成式检索还带来两样能力：能推荐新的、少见的物品，从而改善 cold-start；以及用一个可调参数生成更多样的推荐。后文安排只点到：第 2 节是文献，框架和实验在后面。

## 2 Related Work

序列推荐这条线从 GRU4REC 用 GRU 做序列推荐开始。NARM 在 GRU 上加 attention，追踪用户的长期意图。AttRec 用 self-attention 建模当前 session 的意图，并用度量学习建模用户–物品亲和来做个性化。SASRec 同样用 self-attention，形式接近 decoder-only Transformer。BERT4Rec 和 Transformers4Rec 借用掩码语言建模。S3-Rec 则在四个自监督任务上预训练，而不只是掩码。这些模型都为每个物品学高维嵌入，再在 Maximum Inner Product Search 空间里做近似最近邻来预测下一项。TIGER 的差别被收成一句：用生成式检索直接预测下一项的 Semantic ID。

P5 微调预训练大语言模型，做多任务推荐，并用 LLM 的 SentencePiece tokenizer 把随机分配的物品 ID 切成 token。TIGER 的 Semantic ID 是从物品内容学出来的。第 2 节指向 Table 2，称基于 Semantic ID 的推荐明显好于随机编码；该表的具体分数不在前两节，这里不引用。

Semantic ID 方面，VQ-Rec 也用内容信息生成类似的 code，但目标是可迁移的推荐系统，并不把这些 code 用于生成式检索。他们用 product quantization；本文用 RQ-VAE，并说这会得到层次化的物品表示，层次性的证据留在后文。同期工作表明，层次化 Semantic ID 可以替换大规模推荐排序模型里的物品 ID，并改善泛化。

生成式检索本身来自文档检索：从数据库返回相关文档，文中点名 GENRE、DSI、NCI、CGR，并说更全的综述在附录。作者声称，就他们所知，这是第一次用物品的 Semantic ID 表示，把生成式检索用到推荐系统上。
