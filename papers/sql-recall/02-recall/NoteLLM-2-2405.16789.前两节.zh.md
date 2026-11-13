> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名**：NoteLLM-2-2405.16789.pdf

**原文标题**：NoteLLM-2: Multimodal Large Representation Models for Recommendation

**作者**：Chao Zhang、Haoxin Zhang、Shiwei Wu、Di Wu、Tong Xu、Xiangyu Zhao、Yan Gao、Yao Hu、Enhong Chen。Chao Zhang 署 University of Science and Technology of China、City University of Hong Kong 与 State Key Laboratory of Cognitive Intelligence；Shiwei Wu、Tong Xu、Enhong Chen 署中国科学技术大学与该重点实验室；Xiangyu Zhao 署 City University of Hong Kong；Haoxin Zhang、Di Wu、Yan Gao、Yao Hu 署 Xiaohongshu Inc.。Tong Xu、Xiangyu Zhao、Enhong Chen 为通讯作者。

**场合 / arXiv**：KDD ’25，Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.1，2025 年 8 月 3–7 日，Toronto, ON, Canada。ACM ISBN 979-8-4007-1245-6/25/08，DOI 10.1145/3690624.3709440。同时为 arXiv:2405.16789v2 [cs.IR]，2025-01-21。代码：https://github.com/Applied-Machine-Learning-Lab/NoteLLM 。

## 摘要

LLM 做文本理解和文本 embedding 已经很强，但多模态表示、尤其是 item-to-item（I2I）推荐，还没被充分用起来。直接拿现成的 Multimodal Large Language Model（MLLM）有两个麻烦：相对同代 LLM 发布更晚，而且它们并不适合做表示任务。作者提出一种端到端微调，把任意已有 LLM 和视觉编码器接成高效的多模态表示模型。初步实验发现，微调后的 LLM 常常忽略图像。NoteLLM-2 用两条路补视觉：一是基于提示把视觉和文本拆开，再用多模态 In-Context Learning 平衡两种模态；二是 late fusion，把视觉信息直接并进最终表示。在线与离线实验被用来说明有效。

## 1 Introduction

平台上的多模态推荐依赖把原始图文压成稠密向量，再用向量相似度做检索、聚类和物品建模。CLIP、METER 一类模型已经做成多模态表示，但参数规模仍有放大空间；已有放大工作主要加视觉支路，文本支路又缺少充分的纯文本预训练，文本理解偏弱。LLM 的文本理解和文本 embedding 很强，用在多模态表示里却少。Fig. 1 对比两条路。一条是把已有开源 MLLM 转成表示任务，图中列出的代价是高质量数据、昂贵训练和复杂训练阶段：MLLM 预训练要大量高质量多模态数据和算力，导致不带视觉的 LLM 往往先于多模态版本发布，最新 LLM 和视觉编码器不好定制；现有 MLLM 又偏理解和生成，做表示不经济。另一条是端到端微调，不要求事先对齐，图中列出的好处是高效、可定制、只需目标域数据。目标 LLM 没有预训练视觉组件时，这条路不用再收集预训练数据，还可以按表示任务改结构。作者把用 LLM 增强多模态表示的模型称为 Multimodal Large Representation Models（MLRMs）。

场景定在 I2I 多模态推荐。初步端到端微调显示，朴素 MLRM 偏向文本、忽略图像；图像更多是在放大多模态内容里的关键元素，而不是被表示直接聚合。NoteLLM-2 用两种办法减轻这种视觉忽视。multimodal In-Context Learning（mICL）把内容拆成视觉和文本，各自压成一个 modality-compressed word，再让同模态的压缩词做 batch 内对比。多数 MLLM 用 early fusion，把视觉特征映射进 LLM 的文本空间再交互，纯视觉信息容易在融合中丢掉；late fusion 叠在 early fusion 之后，用 multimodal gate，拿视觉编码器的视觉表示和 LLM 的表示一起生成最终多模态表示。贡献有三条：据作者所称，这是第一次在推荐场景里探索由 LLM 协助的多模态表示，并用端到端微调把任意 LLM 与视觉编码器收成高效 MLRM；指出微调未对齐的 MLRM 会因忽略视觉而造成模态失衡，并用含 mICL 与 late fusion 的 NoteLLM-2 应对；在线与离线实验用来证明对多模态推荐表示有效。具体做法在第 3 节，此处不展开。

## 2 Preliminary Investigation

### 2.1 Problem Statement

这里的物品是用户写的 note，记录生活经历。笔记池 \(\mathrm{N}=\{n_1,\ldots,n_m\}\)。第 \(i\) 条笔记 \(n_i=(t_i, tp_i, ct_i, v_i)\)，依次是标题、话题、正文和图像。给定查询笔记 \(n_i\)，I2I 按多模态内容相似度给池中其余笔记排序，目标是把相关的目标笔记排到前面。

### 2.2 Basic Representation Method of MLRMs

基础表示沿用“压成一个词”的提示：用 JSON 放图像占位符 `<IMG>`、标题、话题和正文，再要求把这条 note 压成一个词。Fig. 2(a) 是这条基础通路，Fig. 2(b) 才是后文的 mICL 加 late fusion。视觉编码器 \(V_\theta\) 把图像变成 \(Z_v\in\mathbb{R}^{L\times h_v}\)；连接器 \(C_\pi\) 把它映到 LLM 词空间，得到 \(E_v\in\mathbb{R}^{L_c\times h_t}\)。文本 token 得到 \(E_t\in\mathbb{R}^{T\times h_t}\)，再用 \(E_v\) 替换 `<IMG>` 位置，拼成 \(E_m\)。LLM 产出最后一层隐状态，取最后一个向量作为笔记表示 \(\mathbf{n}_i\)，相当于用 next token prediction 的形式把多模态内容压进一个向量。LLM 原本按语言建模训练，和表示任务不一致，所以改用对比学习：每个 minibatch 有 \(B\) 对相关笔记，共 \(2B\) 条；损失是带可学习温度 \(\tau\) 的 batch 内对比，相似度是余弦。式 (1) 只更新连接器 \(C_\pi\) 和 LLM，视觉编码器冻结，以便用更大的 batch。

### 2.3 Datasets and Experimental Settings

相关笔记对不靠人工标注，而用共现：用户看过笔记 \(n_A\) 再点 \(n_B\) 时，得分 \(s_{n_A\to n_B}\) 是这些用户各自“行为数据里点过的不同笔记数”的倒数之和，即式 (2)。对每条笔记去掉共现分高于 \(up\) 或低于 \(low\) 的离群，再取过滤后最高的 \(t\) 条作为相关笔记。数据来自作者平台的真实多模态 I2I。训练对从两周用户行为里随机抽，其中十分之一做验证；测试笔记池从下一周随机抽，并避开训练集，再在池内统计相关对。Table 1：训练集 1,487,613 条笔记、1,130,906 对，标题、话题数、话题词数、正文的平均词数分别为 12.38、5.26、4.53、133.20；测试集 534,144 条笔记、21,262 对，对应平均为 11.68、4.58、4.50、116.00。

为减少“只靠文本就能做对”，测试集里单列短笔记：token 长度小于 50，大约占测试笔记的 10%。短查询对 5,620，短目标对 5,582。构造相关对时 \(up=30\)、\(low=0.01\)、\(t=3\)。标题截到 20 词、正文截到 80 词。微调实验里用线性投影把笔记向量降到 64 维以便公平比较。\(B=128\)，因此每批 256 条笔记；温度初值 \(\tau=3\)。召回按查询笔记与测试池其余笔记的相似度排序，报 Recall@100、Recall@1k、Recall@10k，覆盖全部对、短查询对和短目标对，三次随机种子 \(\{42,43,44\}\) 取平均。脚注写明这些模型在 8 张 80GB Nvidia A100 上训练，每卡 batch 为 16。

### 2.4 Performance of Multimodal Representation of Fine-tuned MLRMs

附录里的零样本 MLLM 不如 BM25，作者归因于预训练任务和表示任务错位，因此必须微调。三个端到端 MLRM：MTomato-Base 的 LLM 是 Tomato（在 LLaMA 2 上继续预训练、本身不能看图），视觉编码器是 CLIP ViT-B，连接器是随机初始化的 Q-Former；MQwen-Base 把 Tomato 换成 Qwen-Chat；MQwen-bigG 再把 CLIP ViT-B 换成 ViT-bigG。视觉 embedding 长度都设为 16。对照的预训练 MLLM 是 BLIP-2 和 Qwen-VL-Chat，视觉编码器同样冻结。基线都在同一训练集上训练：只看图的 CLIP ViT-B，BM25，中文文本编码器 RoBERTa-wwm-ext，Tomato，把 embedding 生成和话题生成合成一个任务的 NoteLLM，以及融合方式分别为 merged attention 与 co-attention 的 METER Merge-attn、METER Co-attn。

Table 2 的 All Pair R@100（单位 %）大致排成：CLIP ViT-B 23.21，BM25 55.22，RoBERTa-wwm-ext 67.59，Tomato 71.01，Tomato+NoteLLM 71.42，Qwen-Chat 73.03；多模态一侧 METER Merge-attn 68.22，METER Co-attn 70.90，BLIP-2 68.38，MTomato-Base 71.94，MQwen-Base 74.02，MQwen-bigG 77.63，Qwen-VL-Chat 78.53。星号表示相对最佳基线的双侧 t 检验 \(p<0.05\)，标在 Qwen-VL-Chat 一行。正文点出的相对提升是：Qwen-VL-Chat 的 R@100 比 METER Co-attn 在全部对上高 10.78%；MQwen-bigG 比 Qwen-Chat 高 6.31%；视觉编码器较小（CLIP ViT-B）时增益很小，MTomato-Base 相对 Tomato 只高 1.31%，MQwen-Base 相对 Qwen-Chat 只高 1.36%。短笔记上文本模型掉得更明显，例如短查询 R@100：Qwen-Chat 45.52、Tomato 43.55，而 METER Co-attn 52.70、MQwen-bigG 57.45、Qwen-VL-Chat 60.41。MQwen-bigG 与 Qwen-VL-Chat 用同一视觉编码器和 LLM，效率更高（见 Section 4.4，此处不展开），但性能仍有差距。Qwen-VL-Chat 每张图有 256 个视觉 embedding，在 32 张 80GB A100 上训练，每卡 batch 为 4。

Table 3 把同一批多模态微调模型改成只输入图像或只输入文本。只看图像时，MTomato-Base 与 MQwen-Base 的 All Pair R@100 只有 0.60 和 1.92，几乎不能表示图像；MQwen-bigG 升到 18.32，仍低于做过多模态预训练的 BLIP-2（24.72）和 Qwen-VL-Chat（24.67）。只看文本时这几个端到端模型仍在 70 上下（MTomato-Base 71.49，MQwen-Base 73.14，MQwen-bigG 70.63）。作者据此认为小视觉编码器的端到端微调忽略了视觉。

### 2.5 Exploring the Information Flow of Fine-tuned MLRMs

为解释这种忽略，作者用显著性分数看压缩词和两种模态 token 在各层的信息流。从训练集按批随机取 10,000 条笔记。层 \(l\) 的显著性矩阵由各注意力头的注意力值与对比损失对该值的梯度相乘后，对头求和得到；\(S_v\)、\(S_t\) 分别是视觉 embedding、文本 embedding 流向最终压缩位置的平均显著性，\(S_o\) 是去掉这两部分之后、其余位置之间的平均显著性。Fig. 3 画了 BLIP-2、MTomato-Base、MQwen-Base、MQwen-bigG，横轴 Layer 标到 0–30，纵轴 \(S\) 标到 0–1.0，曲线是 \(S_v\)、\(S_t\)、\(S_o\)；各点精确读数正文没有列表。观察是：预训练 MLLM（BLIP-2，以及附录 C 中的 Qwen-VL-Chat）在浅层上 \(S_v\) 与 \(S_o\) 比较均衡；未经多模态预训练、端到端微调的 MLRM 在浅层 \(S_v\) 低、\(S_o\) 高，说明图像带来的信息更多流向重要的多模态 embedding，而不是直接汇进最终压缩向量。层数变深后 \(S_v\) 上升、\(S_o\) 明显下降，模型转向把相关信息直接聚合进压缩向量。因此在端到端 MLRM 里，图像主要是帮信息流找出关键信息，而不是被表示直接聚合；文本信息流也明显压过视觉信息流。第 3 节 Methodology 起不在本导读范围内。
