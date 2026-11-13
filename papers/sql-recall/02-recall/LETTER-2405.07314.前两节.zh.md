> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名**：LETTER-2405.07314.pdf

**原文标题**：Learnable Item Tokenization for Generative Recommendation

**作者**：Wenjie Wang、Honghui Bao、Xinyu Lin、Jizhi Zhang、Yongqi Li、Fuli Feng、See-Kiong Ng、Tat-Seng Chua。Wenjie Wang、Honghui Bao、Xinyu Lin、See-Kiong Ng、Tat-Seng Chua 署 National University of Singapore；Jizhi Zhang、Fuli Feng 署 University of Science and Technology of China；Yongqi Li 署 The Hong Kong Polytechnic University。Wenjie Wang 与 Honghui Bao 为同等贡献，工作受 NExT Research Center 支持。Fuli Feng 为通讯作者。

**场合 / arXiv**：CIKM ’24（Proceedings of the 33rd ACM International Conference on Information and Knowledge Management），2024 年 10 月 21–25 日，Boise, ID, USA。ACM ISBN 979-8-4007-0436-9/24/10，DOI 10.1145/3627673.3679569。同时为 arXiv:2405.07314v3 [cs.IR]，2025-10-17。

## 摘要

用 LLM 做生成式推荐时，关键难点是把推荐数据变进 LLM 的语言空间，也就是物品怎么 token 化。已有的 ID、文本和 codebook 标识符，分别在语义编码、协同信号或 code 分配偏差上有缺口。LETTER（a LEarnable Tokenizer for generaTivE Recommendation）把层次语义、协同信号和 code 分配多样性一起放进标识符：用 Residual Quantized VAE 做语义正则，用对比对齐损失做协同正则，再用多样性损失减轻分配偏差。作者把 LETTER 接到两个模型上，并加一个 ranking-guided generation loss，从理论上加强排序能力。三个数据集上的实验被用来说明它推进了基于 LLM 的生成式推荐。

## 1 INTRODUCTION

生成式推荐被写成：给定用户历史交互物品，让 LLM 生成目标物品。Fig. 1 把这件事拆成物品 token 化，以及下一步生成。作者把 item tokenization 定义成给每个物品一个 identifier，即一段 token 序列，用来跨过推荐数据和 LLM 语言空间之间的缺口。已有做法主要是三类标识符。ID 标识符给每个物品一条唯一数字串，例子是 “28,128”，唯一性有了，但语义编码差，冷启动物品难泛化。文本标识符直接用标题、属性或描述。问题有两层：token 序列里的语义并不是从粗到细排的，若目标物品开头的 token 对不上用户偏好（电影标题里的 “With”“Be” 被当作例子），生成概率就低；序列只由语义决定，没有用户行为里的协同信号，语义相近但协同不同的物品会得到相近序列，从 Collaborative Filtering（CF）看就不够可区分，后文用 Section 2 和 Fig. 2 说明。Codebook 方法用自编码器把语义编成层次 code 序列，同样缺协同信号；Fig. 3 还表明 code 分配天然不均衡，高频 code 对应的物品更容易被生成。

由此，理想标识符要满足三条：token 序列先编码粗语义、再过渡到细语义，以配合自回归生成；token 分配要带上协同信号，使协同相近的物品有相近序列；提高分配多样性，减轻生成偏差、照顾生成公平。LETTER 在 codebook 标识符上加三种正则。语义正则用 Residual Quantized VAE（RQ-VAE）把物品语义翻成层次标识符。协同正则用对比对齐损失，把 RQ-VAE 里的语义量化 embedding 对齐到一个训好的 CF 模型（例子是 LightGCN）给出的 CF embedding。多样性损失则拉开 code embedding，以减轻分配偏差和生成偏差。作者把 LETTER 接到两个有代表性的生成式推荐模型上，并提出 ranking-guided generation loss，从理论上抬排序能力。三个数据集上的实验用来验证标识符同时顾到层次语义、协同信号和分配多样性。代码与数据放在 https://github.com/HonghuiBao2000/LETTER 。贡献概括为：先分析理想标识符应有的特征，再提出可学习的 LETTER；在两个生成模型上实例化，并用上述损失从理论上加强排序；在三个数据集、多种设定下比较，称优于已有物品 token 化方法。本节没有表格；Fig. 3 的分档标注见第 2 节。

## 2 ITEM TOKENIZATION

这一节把生成式推荐收成：根据用户历史交互生成下一个物品。基于 LLM 时，基础步骤是物品 token 化，即给每个物品一段 token 序列，供 LLM 编码和生成。用途有二：把历史交互改写成 identifier 序列来编码物品；自回归地生成下一个物品的 identifier 做推荐，对应 Fig. 1(b)。已有工作覆盖 ID 标识符、文本标识符和 codebook 标识符；ID 的语义编码能力不足。文本和 codebook 的关键问题被收成三点。

第一，非层次语义：文本标识符里的语义不是从粗到细分布的，这一点回指第 1 节。第二，缺协同信号：以往文本和 codebook 标识符在 token 序列的组成里不考虑协同，通常是在 LLM 训练阶段把协同信号注进 identifier 的 token embedding，例子是 TIGER 和 LC-Rec。Fig. 2 用两把六弦吉他说明错位：acoustic 与 electric 语义相近，identifier 分别是 `<a_8><b_66><c_93><d_8>` 和 `<a_8><b_66><c_93><d_1>`，序列和 embedding 都相近，但交互用户不同（一边是 User_1、User_5、User_6，另一边是 User_2、User_3、User_9）。作者认为，语义相近就共享相近 token 序列时，很难再对齐协同信号；若靠训练把协同硬注进这两个物品的 identifier embedding，会发生碰撞。第三，code 分配偏差：codebook 方法的分配不均衡，会带来物品生成偏差。经验调查用 TIGER 在 Instruments 上做：按训练数据里的分配热度把 identifier code 分成五组，再看 TIGER 的生成频率。Fig. 3 的横轴分档标为 top code percentage 的 [0,20)、[20,40)、[40,60)、[60,80)、[80,100]，并并列训练数据中的目标 identifier 与生成 identifier 的频率；正文结论是热门 identifier 更容易被生成，从而放大生成偏差。各柱的具体高度在抽取文本中没有给出数字。

据此，理想标识符的三个目标被写成：token 序列整合层次语义、token 序列整合协同信号、code 分配要有高多样性。本节没有表格。
