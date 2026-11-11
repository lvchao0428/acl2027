# RepeatNet：面向会话推荐的重复感知神经推荐机

- 原文件名：RepeatNet-1812.02646.pdf
- 原标题：RepeatNet: A Repeat Aware Neural Recommendation Machine for Session-based Recommendation
- 中文标题：RepeatNet：面向会话推荐的重复感知神经推荐机
- 作者：Pengjie Ren、Zhumin Chen、Jing Li、Zhaochun Ren、Jun Ma、Maarten de Rijke
- 会议或 arXiv：页边标注为 arXiv:1812.02646v1 [cs.IR] 6 Dec 2018。版权声明为 © 2019 Association for the Advancement of Artificial Intelligence（AAAI）。www.aaai.org。All rights reserved.

<!-- 原 PDF 第 1 页 -->

Pengjie Ren$^{1,2}$，Zhumin Chen$^1$，Jing Li$^1$，Zhaochun Ren$^3$，Jun Ma$^1$，Maarten de Rijke$^2$

$^1$ Shandong University, Jinan, China

$^2$ University of Amsterdam, Amsterdam, The Netherlands

$^3$ Data Science Lab, JD.com, Beijing, China

## 摘要

用于会话推荐的循环神经网络近来因其有希望的性能而受到大量关注。重复消费是许多推荐场景（例如电子商务、音乐和电视节目推荐）中的常见现象：同一物品会随时间被反复消费。然而，此前没有研究用神经网络强调重复消费。我们需要一种有效的神经方法来决定何时做重复推荐。本文把重复—探索机制纳入神经网络，并提出一个新模型 RepeatNet，它具有编码器—解码器结构。RepeatNet 在解码器中整合常规的神经推荐方法，并加入一种新的重复推荐机制，可以从用户历史中选择物品，并在恰当的时机推荐它们。我们在三个基准数据集上报告了大量实验。就 MRR 与 Recall 而言，RepeatNet 在全部三个数据集上都优于当时最先进的基线。此外，随着数据集规模和重复比例增加，RepeatNet 相对基线的提升也增大，这显示了它在处理重复推荐场景时的优势。

## 1 引言

会话推荐近来受到越来越多的关注，因为它广泛适用于许多在线服务（例如电子商务、视频观看、音乐收听）（Cheng et al. 2017）。这里，一次会话是在给定时间范围内发生的一组交互。同一用户的会话可以发生在同一天，也可以跨越数天、数周甚至数月（Quadrana et al. 2017）。

传统推荐方法处理会话推荐时，通常要么基于最近一次交互，要么基于最近一次会话。Zimdars, Chickering, and Meek (2001) 以及 Shani, Heckerman, and Brafman (2005) 研究如何抽取序列模式，用马尔可夫模型预测下一个物品。随后，Chen et al. (2012) 提出逻辑马尔可夫嵌入，以学习歌曲表示用于播放列表预测。这些模型的一个主要问题是：当试图纳入所有物品上全部可能的用户选择序列时，状态空间很快变得难以处理。循环神经网络（RNN）近来被用于会话推荐，并引起显著关注。Hidasi et al. (2016a) 引入带门控循环单元（GRU）的 RNN 做会话推荐。他们还提出若干并行 RNN（p-RNN）架构，同时基于点击以及被点击物品的特征（图像和文本）来建模会话（Hidasi et al. 2016b）。Quadrana et al. (2017) 用跨会话信息传递来个性化 RNN 模型，并设计了层次 RNN 模型，在用户会话之间传递并演化 RNN 的潜在隐状态。Li et al. (2017b) 把注意力机制引入会话推荐，并优于 Hidasi et al. (2016a)。尽管把深度学习用于会话推荐的研究越来越多，但没有工作强调所谓的重复消费。重复消费是许多推荐场景（例如电子商务、音乐和电视节目推荐）中的常见现象：同一物品会随时间被反复消费。

重复消费之所以存在，是因为人有规律的习惯。例如，我们都会反复购买同样的东西，定期在同一家餐馆吃饭，频繁收听同一首歌和同一位艺人（Anderson et al. 2014）。表 1 给出三个基准数据集上的重复消费比例，这些数据集在相关研究中常用（Hidasi et al. 2016a; Li et al. 2017b）。重复消费不仅存在，而且在某些应用中占交互的很大比例。本文通过把重复—探索机制纳入神经网络来研究重复消费，并提出名为 RepeatNet 的新模型，它具有编码器—解码器结构。与现有工作用单一解码器为每个物品评估一个分数不同，RepeatNet 用两个解码器分别在重复模式和探索模式下评估每个物品的推荐概率。

**表 1：三个基准数据集上的重复比例（%）。**

| 数据集 | Train | Validation | Test |
| --- | ---: | ---: | ---: |
| YOOCHOOSE 1/4 | 25.52 | 25.51 | 26.02 |
| DIGINETICA | 19.94 | 20.06 | 20.49 |
| LASTFM | 20.72 | 20.42 | 20.95 |

<!-- 原 PDF 第 2 页 -->

在重复模式下，我们从用户历史中推荐一个旧物品；在探索模式下，我们推荐一个新物品。具体而言，我们首先把每个会话编码成一个表示。然后用重复—探索机制学习重复模式与探索模式之间的切换概率。此后，我们提出重复推荐解码器，学习在重复模式下推荐旧物品的概率；以及探索推荐解码器，学习在探索模式下推荐新物品的概率。最后，我们以概率方式把模式切换概率与两种模式下每个物品的推荐概率结合起来，确定物品的推荐分数。模式预测与物品推荐在统一框架内、以端到端反向传播训练范式联合学习。

我们在三个基准数据集上进行了大量实验。结果表明，就 MRR 与 Recall 而言，RepeatNet 在全部三个数据集上都优于当时最先进的基线。此外，我们发现随着数据集规模和重复比例增加，RepeatNet 相对基线的提升也增大，这显示了它在处理重复推荐场景时的优势。

概括而言，本文的主要贡献是：

- 我们提出一个名为 RepeatNet 的、基于深度学习的新模型，它考虑了重复消费现象。据我们所知，我们是第一个在神经模型的会话推荐中考虑这一点的。
- 我们为会话推荐引入重复—探索机制，以自动学习重复模式与探索模式之间的切换概率。与使用单一解码器的现有工作不同，我们提出两个解码器，分别学习两种模式下每个物品的推荐概率。
- 我们在三个基准数据集上进行了大量实验与分析。结果表明，通过显式建模重复消费，RepeatNet 能够把会话推荐的性能提升到超过当时最先进的方法。

## 2 相关工作

我们从两个方面综述相关工作：会话推荐与重复推荐。

### 2.1 会话推荐

会话推荐的传统方法通常基于马尔可夫链，根据上一个动作预测下一个动作。Zimdars, Chickering, and Meek (2001) 提出基于马尔可夫链的序列推荐器，并研究如何抽取序列模式，用概率决策树模型学习下一个状态。Mobasher et al. (2002) 研究不同的序列模式用于推荐，发现连续序列模式比一般序列模式更适合序列预测任务。Shani, Heckerman, and Brafman (2005) 提出马尔可夫决策过程（MDP）以会话方式提供推荐；最简单的 MDP 退化为一阶马尔可夫链，下一个推荐可以直接通过物品之间的转移概率计算。Yap, Li, and Yu (2012) 在个性化序列模式挖掘中引入能力分数，用于下一物品推荐。Chen et al. (2012) 把播放列表建模为马尔可夫链，并提出逻辑马尔可夫嵌入来学习歌曲表示，用于播放列表预测。把马尔可夫链用于会话推荐任务的一个主要问题是：当试图纳入所有物品上全部可能的用户选择序列时，状态空间很快变得难以处理。

RNN 已被证明对序列点击预测有用（Zhang et al. 2014）。Hidasi et al. (2016a) 把 RNN 用于会话推荐，并相对传统方法取得显著提升。他们使用会话并行的小批量训练，并采用基于排序的损失函数来学习模型。随后，他们提出若干并行 RNN（p-RNN）架构，基于点击以及被点击物品的特征（图像和文本）来建模会话（Hidasi et al. 2016b）；他们还提出更适合 p-RNN 的替代训练策略。Tan, Xu, and Liu (2016) 提出两种技术来提升模型性能，即数据增强，以及一种考虑输入数据分布偏移的方法。Jannach and Ludewig (2017) 表明，在绝大多数被测配置和数据集上，一种基于启发式的会话最近邻方案优于 Hidasi et al. (2016a) 提出的模型。Quadrana et al. (2017) 提出用跨会话信息传递来个性化 RNN 模型的方法，并设计层次 RNN 模型，在用户会话之间传递并演化 RNN 的潜在隐状态。Li et al. (2017b) 探索带注意力机制的混合编码器，以建模用户的序列行为与意图，从而捕捉用户在当前会话中的主要目的。

与上述研究不同，我们在模型中强调重复消费现象。

### 2.2 重复推荐

Anderson et al. (2014) 研究用户随时间反复消费同一物品的模式，领域非常广泛，从在同一商户地点的签到，到对同一视频的反复观看。他们发现，消费的新近性是重复消费最强的预测因子。Chen, Wang, and Wang (2015) 推导出影响人们短期重复消费行为的四个通用特征。然后他们提出两种分别使用线性和二次核的快速算法，在给定上下文时预测用户是否会在特定时间进行短期重复消费。

推荐系统的一个重要目标是帮助用户发现新物品。除此之外，许多真实系统把推荐列表用于另一个目标，即提醒用户他们曾经浏览或消费过的物品。Lerche, Jannach, and Ludewig (2016) 通过在线实验研究这一点，旨在量化推荐列表中此类提醒的价值。

<!-- 原 PDF 第 3 页 -->

Benson, Kumar, and Tomkins (2016) 识别出重复消费的两种宏观行为模式。第一，在给定用户的生命周期中，只有极少数物品会存活很长时间。第二，一个物品的最后若干次消费呈现出不断增大的到达间隔，这与“厌倦逐渐增加、直至最终放弃”的概念一致。我们的工作与以往重复推荐工作的主要区别是：我们第一个提出神经推荐模型，在传统推荐任务和会话推荐任务中都显式强调重复消费。

## 3 RepeatNet

给定一个动作（例如点击、购物）会话 $I_S = \{i_1, i_2, \ldots, i_\tau, \ldots, i_t\}$，其中 $i_\tau$ 表示一个物品。会话推荐试图预测下一个事件是什么，如式 (1) 所示。不失一般性，本文以点击动作为贯穿全文的例子：

$$P(i_{t+1} \mid I_S) \sim f(I_S), \tag{1}$$

其中 $P(i_{t+1} \mid I_S)$ 表示在给定 $I_S$ 时推荐 $i_{t+1}$ 的概率。传统方法通常直接把 $f(I_S)$ 建模为判别函数或概率函数。

### 3.1 框架

我们提出 RepeatNet，从概率视角建模 $P(i_{t+1} \mid I_S)$，并显式考虑重复消费，如式 (2) 所示：

$$P(i_{t+1} \mid I_S) = P(r \mid I_S)\, P(i_{t+1} \mid r, I_S) + P(e \mid I_S)\, P(i_{t+1} \mid e, I_S), \tag{2}$$

其中 $r$ 与 $e$ 分别表示重复模式和探索模式。$P(r \mid I_S)$ 与 $P(e \mid I_S)$ 分别表示执行重复模式和探索模式的概率。$P(i_{t+1} \mid r, I_S)$ 与 $P(i_{t+1} \mid e, I_S)$ 分别表示在给定 $I_S$ 时、于重复模式和探索模式下推荐 $i_{t+1}$ 的概率。

如图 1 所示，RepeatNet 由四个主要组件构成：会话编码器、重复—探索机制、重复推荐解码器，以及探索推荐解码器。会话编码器把给定会话 $I_S$ 编码为潜在表示 $H = \{h_1, h_2, \ldots, h_\tau, \ldots, h_t\}$，其中 $h_t$ 表示时间戳 $t$ 处的会话表示。重复—探索机制以 $H$ 为输入，预测执行重复模式或探索模式的概率，对应于式 (2) 中的 $P(r \mid I_S)$ 与 $P(e \mid I_S)$。重复推荐解码器以 $H$ 为输入，预测 $I_S$ 中已点击物品上的重复推荐概率，对应于式 (2) 中的 $P(i_{t+1} \mid r, I_S)$。探索推荐解码器以 $H$ 为输入，预测 $I - I_S$ 中未点击物品上的探索推荐概率，其中 $I$ 指全部物品，对应于式 (2) 中的 $P(i_{t+1} \mid e, I_S)$。

图 1 见原 PDF。

**图 1：RepeatNet 总览。** 图中标出 Repeat-Explore Mechanism（重复—探索机制）、Attentive Encoder（注意力编码器）、Repeat Rec Decoder 与 Repeat Mode（重复推荐解码器与重复模式）、Explore Rec Decoder 与 Explore Mode（探索推荐解码器与探索模式），以及会话隐状态 $h_1, \ldots, h_t$ 与物品 $i_1, \ldots, i_t$。图中公式为

$$P(i \mid I_S) = P(r \mid I_S)\, P(i \mid r, I_S) + P(e \mid I_S)\, P(i \mid e, I_S).$$

### 3.2 会话编码器

与以往研究一样（Hidasi et al. 2016a; Li et al. 2017b），我们用 GRU 编码 $I_S$。GRU 定义为：

$$
\begin{aligned}
z_\tau &= \sigma(W_z [emb(i_\tau), h_{\tau-1}]) \\
r_\tau &= \sigma(W_r [emb(i_\tau), h_{\tau-1}]) \\
\widetilde{h}_\tau &= \tanh(W_h [emb(i_\tau), r_\tau \odot h_{\tau-1}]) \\
h_\tau &= (1 - z_\tau) \odot h_{\tau-1} + z_\tau \odot \widetilde{h}_\tau,
\end{aligned}
\tag{3}
$$

其中 $W_z$、$W_r$ 与 $W_h$ 是权重矩阵；$emb(i_\tau)$ 是 $i_\tau$ 的物品嵌入；$\sigma$ 表示 sigmoid 函数。GRU 的初始状态设为零向量，即 $h_0 = 0$。经过会话编码器之后，每个会话 $I_S$ 被编码为 $H = \{h_1, h_2, \ldots, h_\tau, \ldots, h_t\}$。

### 3.3 重复—探索机制

重复—探索机制可以看作一个二分类器，它基于 $H = \{h_1, h_2, \ldots, h_\tau, \ldots, h_t\}$ 预测推荐模式。为此，我们首先应用注意力机制（Bahdanau, Cho, and Bengio 2015），以得到 $I_S$ 的定长向量表示。

<!-- 原 PDF 第 4 页 -->

具体而言，我们先用最后一个隐状态 $h_t$ 与每个编码器隐状态 $h_\tau \in H$ 匹配，得到重要性分数：

$$e^{re}_\tau = v_{re}^{\top} \tanh(W_{re} h_t + U_{re} h_\tau), \tag{4}$$

其中 $v_{re}$、$W_{re}$ 与 $U_{re}$ 是参数。重要性分数随后被归一化，以加权和的形式得到 $I_S$ 的上下文向量，如式 (5)：

$$
\begin{aligned}
\alpha^{re}_\tau &= \frac{\exp(e^{re}_\tau)}{\sum_{\tau=1}^{t} \exp(e^{re}_\tau)} \\
c^{re}_{I_S} &= \sum_{\tau=1}^{t} \alpha^{re}_\tau h_\tau.
\end{aligned}
\tag{5}
$$

然后我们用 softmax 回归把 $c^{re}_{I_S}$ 变换为模式概率分布，分别对应于 $P(r \mid I_S)$ 与 $P(e \mid I_S)$，如式 (6)：

$$[P(r \mid I_S), P(e \mid I_S)] = \mathrm{softmax}(W^{c}_{re}\, c^{re}_{I_S}), \tag{6}$$

其中 $W^{c}_{re}$ 是权重矩阵。

### 3.4 重复推荐解码器

重复推荐解码器评估重新点击 $I_S$ 中某个物品的概率。受 CopyNet（Gu et al. 2016）启发，我们用注意力模型的一种改动来实现这一点。重新点击物品 $i_\tau \in I_S$ 的概率计算如下：

$$e^{r}_\tau = v_{r}^{\top} \tanh(W_{r} h_t + U_{r} h_\tau) \tag{7}$$

$$
P(i \mid r, I_S) =
\begin{cases}
\dfrac{\sum_{i} \exp(e^{r}_{\tau})}{\sum_{\tau=1}^{t} \exp(e^{r}_{\tau})} & \text{if } i \in I_S \\
0 & \text{if } i \in I - I_S,
\end{cases}
\tag{8}
$$

其中 $v_r$、$W_r$ 与 $U_r$ 是参数；$\sum_{i} \exp(e^{r}_{\tau})$ 表示物品 $i \in I_S$ 全部出现位置上的指数得分之和，因为同一物品可能在 $I_S$ 的不同位置多次出现。

### 3.5 探索推荐解码器

探索推荐解码器评估点击一个不在 $I_S$ 中的新物品的概率。为了更好地捕捉用户在会话 $I_S$ 中的兴趣，我们采用物品级注意力机制，使解码器能够动态选择并线性组合输入序列的不同部分（Li et al. 2017b）：

$$
\begin{aligned}
e^{e}_\tau &= v_{e}^{\top} \tanh(W_{e} h_t + U_{e} h_\tau) \\
\alpha^{e}_\tau &= \frac{\exp(e^{e}_\tau)}{\sum_{\tau=1}^{t} \exp(e^{e}_\tau)} \\
c^{e}_{I_S} &= \sum_{\tau=1}^{t} \alpha^{e}_\tau h_\tau,
\end{aligned}
\tag{9}
$$

其中 $v_e$、$W_e$ 与 $U_e$ 是参数。因子 $\alpha^{e}$ 决定做预测时应当强调或忽略输入序列的哪一部分。然后我们把最后一个隐状态与注意力状态组合成 $I_S$ 的混合表示 $c_{I_S}$，它是向量 $h_t$ 与 $c^{e}_{I_S}$ 的拼接：$c_{I_S} = [h_t, c^{e}_{I_S}]$。

最后，点击物品 $i_\tau \in I - I_S$ 的概率计算如下：

$$
f_i =
\begin{cases}
-\infty & \text{if } i \in I_S \\
W^{c}_{e}\, c_{I_S} & \text{if } i \in I - I_S
\end{cases}
\tag{10}
$$

$$
P(i \mid e, I_S) = \frac{\exp(f_i)}{\sum_{\tau=1}^{t} \exp(f_\tau)}, \tag{11}
$$

其中 $W^{c}_{e}$ 是权重矩阵，$-\infty$ 表示负无穷。由于 $\exp(-\infty) = 0$，我们假定：若某物品已存在于 $I_S$，则在探索模式下推荐它的概率为零。

### 3.6 目标函数

我们的目标是在给定输入会话时最大化输出预测概率。因此，我们按如下方式优化负对数似然损失函数：

$$
L_{rec}(\theta) = -\frac{1}{|\mathbb{I}_S|} \sum_{I_S \in \mathbb{I}_S} \sum_{\tau=1}^{|I_S|} \log P(i_\tau \mid I_S), \tag{12}
$$

其中 $\theta$ 是 RepeatNet 的全部参数，$\mathbb{I}_S$ 是训练集中所有会话的集合，$P(i_\tau \mid I_S)$ 是式 (2) 所定义的物品预测概率。

RepeatNet 加入了一个额外的重复—探索机制，以便在重复模式与探索模式之间软切换。我们假定：若下一个物品存在于 $I_S$，则它是在重复模式下生成的，否则是探索模式。这里，我们可以联合训练另一个模式预测损失，它同样是负对数似然损失：

$$
\begin{aligned}
L_{mode}(\theta) = -\frac{1}{|\mathbb{I}_S|} \sum_{I_S \in \mathbb{I}_S} \sum_{\tau=1}^{|I_S|} \Big[ & \mathbb{1}(i_\tau \in I_S) \log P(r \mid I_S) \\
& + \big(1 - \mathbb{1}(i_\tau \in I_S)\big) \log P(e \mid I_S) \Big],
\end{aligned}
\tag{13}
$$

其中 $\mathbb{1}(i_\tau \in I_S)$ 是指示函数，当 $i_\tau \in I_S$ 时等于 1，否则为 0。

在联合训练的情形下，最终损失是两个损失的线性组合：

$$L(\theta) = L_{rec}(\theta) + L_{mode}(\theta). \tag{14}$$

RepeatNet 的全部参数以及物品嵌入都在端到端反向传播训练范式中学习。由于式 (2) 中的完整概率项，两种模式的概率 $P(r \mid I_S)$、$P(e \mid I_S)$ 与物品预测概率 $P(i \mid r, I_S)$、$P(i \mid e, I_S)$ 本质上通过一个统一函数相互竞争。

## 4 实验

### 4.1 数据集与评价指标

我们在三个标准数据集上进行实验，即 YOOCHOOSE、DIGINETICA 和 LASTFM。YOOCHOOSE 与 DIGINETICA 经常用于会话推荐研究（Hidasi et al. 2016a; Tan, Xu, and Liu 2016; Li et al. 2017b; Jannach and Ludewig 2017）。由于二者都面向电子商务，我们选择了另一个领域（音乐）的第三个数据集 Last.fm。$^1$ 见表 2。数据集的划分与 Li et al. (2017b) 相同。

<!-- 原 PDF 第 5 页 -->

**表 2：三个数据集的统计（会话数与物品数）。**

| Dataset | Training | Validation | Test | Items |
| --- | ---: | ---: | ---: | ---: |
| YOOCHOOSE | 5,325,971 | 591,775 | 55,898 | 30,470 |
| DIGINETICA | 647,532 | 71,947 | 60,858 | 43,097 |
| LASTFM | 2,690,424 | 333,537 | 338,115 | 40,000 |

- YOOCHOOSE$^2$ 是 RecSys Challenge 2015 发布的公开数据集。我们遵循 Hidasi et al. (2016a) 与 Li et al. (2017b)，过滤掉长度为 1 的会话以及出现次数少于 5 的物品。他们指出，该数据集的 1/4 版本已足以完成该任务，增加数据量不会进一步提升性能。
- DIGINETICA$^3$ 由 CIKM Cup 2016 发布。我们同样遵循 Li et al. (2017b)，过滤掉长度为 1 的会话以及出现次数少于 5 的物品。
- LASTFM$^4$ 由 Celma (2010) 发布，并广泛用于推荐任务（Cheng et al. 2017）。我们用它做音乐艺人推荐；保留最流行的 40,000 位艺人，并过滤掉长于 50 或短于 2 个物品的会话。

推荐系统一次只能推荐少数物品，用户可能选择的真实物品应当位于列表的前几项之中（He et al. 2018b; Cheng et al. 2018）。因此，常用指标是 MRR@20 与 Recall@20（He et al. 2018a; Mei et al. 2018）。本文还报告 MRR@10 与 Recall@10。

- Recall@$k$：主要评价指标是 Recall@$k$，即在全部测试用例中，目标物品位于前 $k$ 个物品之中的比例。
- MRR@$k$：另一个使用的指标是 MRR@$k$（Mean Reciprocal Rank，平均倒数排名），即目标物品倒数排名的平均值。若排名大于 $k$，则倒数排名设为零。

### 4.2 实现细节

我们把物品嵌入大小和 GRU 隐状态大小都设为 100。我们使用 dropout（Srivastava et al. 2014），丢弃率 $p = 0.5$。我们用 Xavier 方法随机初始化模型参数（Glorot and Bengio 2010）。我们用 Adam 作为优化算法。对 Adam 优化器的超参数，学习率设为 $\alpha = 0.001$，两个动量参数分别为 $\beta_1 = 0.9$ 与 $\beta_2 = 0.999$，并且 $\epsilon = 10^{-8}$。每 3 轮把学习率 $\alpha$ 减半。训练中我们还使用梯度裁剪（Pascanu, Mikolov, and Bengio 2013），范围为 $[-5, 5]$。为加快训练并迅速收敛，我们通过网格搜索使用小批量大小 1024。每个 epoch 都在验证集上测试模型性能。模型用 Chainer（Tokui et al. 2015）编写，并在 GeForce GTX TitanX GPU 上训练。

$^1$ https://www.last.fm

$^2$ http://2015.recsyschallenge.com/challenge.html

$^3$ http://cikm2016.cs.iupui.edu/cikm-cup

$^4$ http://www.dtic.upf.edu/~ocelma/MusicRecommendationDataset/lastfm-1K.html

### 4.3 用于比较的方法

**传统方法。** 我们选择下列在会话推荐中常用作基线的传统方法（Hidasi et al. 2016a; Tan, Xu, and Liu 2016; Li et al. 2017b）。

- POP：POP 总是推荐训练集中最流行的物品。它经常被用作推荐系统领域的基线（He et al. 2017）。
- S-POP：S-POP 推荐当前会话中最流行的物品。并列时用全局流行度打破（Hidasi et al. 2016a）。
- Item-KNN：该基线推荐与当前物品相似的物品。相似度定义为两个物品在会话中的共现次数，除以各自出现会话数之积的平方根。还加入了正则化，以避免很少被访问的物品之间偶然出现的高相似度（Davidson et al. 2010）。
- BPR-MF：BPR-MF（Rendle et al. 2009）是常用的矩阵分解方法。我们把它用于会话推荐的方式是：用该会话中迄今出现过的物品的平均潜在因子来表示一个新会话。
- FPMC：FPMC（Rendle, Freudenthaler, and Schmidt-Thieme 2010）是下一购物篮推荐的一种当时最先进的混合模型。为把它适配到会话推荐，我们在计算推荐分数时忽略用户潜在表示。
- PDP：Benson, Kumar, and Tomkins (2016) 提出 PDP，并声称他们是第一个建模序列重复消费的。据我们所知，这是唯一考虑序列重复消费的推荐模型。

**深度学习方法。** 此前没有研究提出考虑序列重复消费的神经模型。我们选择近期最先进的神经会话推荐模型作为基线。

- GRU4REC：GRU4REC（Hidasi et al. 2016a）使用会话并行的小批量训练过程，并采用基于排序的损失函数来学习模型。
- Improved-GRU4REC：Improved GRU4REC（Tan, Xu, and Liu 2016）用两种技术改进 GRU4REC，即数据增强，以及一种考虑输入数据分布偏移的方法。
- GRU4REC-TOPK：Hidasi and Karatzoglou (2017) 进一步用基于 top-$k$ 的排序损失改进 GRU4REC。
- NARM：NARM（Li et al. 2017b）用神经注意力机制进一步改进 Improved-GRU4REC。

<!-- 原 PDF 第 6 页 -->

**表 3：三个数据集上的实验结果（%）。** 粗体表示对应指标上的最佳结果。相对最佳基线有显著提升的，用 $\dagger$ 标出（t 检验，$p < .05$）。Li et al. (2017b) 在 DIGINETICA 数据集上报告的分数与本文不同，因为他们没有按 “timeframe” 字段对会话物品排序，从而忽略了序列信息。我们运行 Hidasi et al. (2016a)、Tan, Xu, and Liu (2016)、Hidasi and Karatzoglou (2017)、Li et al. (2017b) 发布的代码，得到 GRU4REC、Improved-GRU4REC、GRU4REC-TOPK 和 NARM 的结果。

| Methods | YOOCHOOSE MRR@10 | MRR@20 | Recall@10 | Recall@20 | DIGINETICA MRR@10 | MRR@20 | Recall@10 | Recall@20 | LASTFM MRR@10 | MRR@20 | Recall@10 | Recall@20 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| POP | 0.26 | 0.30 | 0.81 | 1.33 | 0.18 | 0.20 | 0.53 | 0.89 | 1.09 | 1.26 | 2.90 | 5.26 |
| S-POP | 17.70 | 17.79 | 25.96 | 27.11 | 13.64 | 13.68 | 20.56 | 21.06 | 8.36 | 8.71 | 18.08 | 22.59 |
| Item-KNN | 20.89 | 21.72 | 41.56 | 52.35 | 10.77 | 11.57 | 25.04 | 35.75 | 4.48 | 4.85 | 9.77 | 14.84 |
| BPR-MF | 1.90 | 1.97 | 3.07 | 4.05 | 1.86 | 1.98 | 3.60 | 5.24 | 4.88 | 5.19 | 9.87 | 14.05 |
| FPMC | 16.59 | 17.50 | 38.87 | 51.86 | 6.30 | 6.95 | 17.07 | 26.53 | 4.58 | 4.99 | 11.67 | 17.68 |
| PDP | 18.44 | 19.15 | 40.03 | 52.98 | 6.75 | 7.24 | 19.57 | 28.77 | 4.86 | 5.05 | 12.11 | 18.09 |
| GRU4REC | 21.64 | 22.60 | 46.67 | 59.56 | 7.59 | 8.33 | 19.09 | 29.45 | 4.92 | 5.39 | 11.56 | 17.90 |
| Improved-GRU4REC | 28.36 | 29.15 | 57.91 | 69.20 | 13.63 | 14.69 | 33.48 | 46.16 | 9.60 | 10.15 | 20.98 | 29.04 |
| GRU4REC-TOPK | 29.76 | 30.69 | 58.15 | 70.30 | 13.14 | 14.16 | 31.54 | 45.23 | 7.44 | 7.95 | 15.73 | 22.61 |
| NARM | 28.52 | 29.23 | 58.70 | 69.73 | 15.25 | 16.17 | 33.62 | 49.70 | 10.31 | 10.85 | 22.04 | 29.94 |
| RepeatNet (no repeat) | 30.02 | 30.76 | 59.62 | 70.21 | 12.71 | 13.52 | 30.96 | 42.56 | 9.92 | 10.47 | 21.81 | 29.96 |
| RepeatNet | 30.50$\dagger$ | 31.03$\dagger$ | 59.76$\dagger$ | 70.71 | 16.90$\dagger$ | 17.66$\dagger$ | 36.86$\dagger$ | 47.79 | 11.46$\dagger$ | 12.03$\dagger$ | 24.18$\dagger$ | 32.38$\dagger$ |

## 5 结果与分析

### 5.1 结果

所有方法的结果见表 3。我们运行 Hidasi et al. (2016a) 与 Li et al. (2017b) 发布的代码，以报告 GRU4REC 和 NARM 的结果。从表 3 可以得到若干认识。第一，RepeatNet 既优于传统方法，也优于近期的神经方法，包括很强的基线 GRU4REC-TOPK 和 NARM。RepeatNet 相对 NARM 的提升，甚至大于 NARM 相对 Improved-GRU4REC 的提升。这些提升意味着显式建模重复消费是有帮助的，它使 RepeatNet 更有能力建模会话推荐中的复杂情形。

第二，随着重复比例增加，RepeatNet 的性能总体上也随之提高。我们基于 YOOCHOOSE 与 DIGINETICA 上不同的提升幅度得出这一结论。两个数据集都来自电子商务领域，但 YOOCHOOSE 的重复比例更高。

第三，RepeatNet 的性能随领域而变化。表 3 显示，RepeatNet 在音乐领域的优势大于电子商务领域；我们认为这是由于不同领域的特性不同。在 LASTFM 上，S-POP 比 Item-KNN 好得多，这意味着流行度在 LASTFM 上非常重要。然而在 YOOCHOOSE 上，Item-KNN 比 S-POP 好得多，这意味着协同过滤在 YOOCHOOSE 上更重要。此外，神经模型相对传统方法在所有数据集的全部评价指标上都有大幅增益。类似结论也已在其他近期研究中给出（Hidasi et al. 2016a; Tan, Xu, and Liu 2016; Li et al. 2017b）。

### 5.2 重复机制分析

**表 4：RepeatNet（有、无重复机制）在重复会话与非重复会话上的 MRR@20（%）。** Rep：重复会话；Non-Rep：非重复会话。表中数据集名 DIGINTICA 按原 PDF 拼写。

| RepeatNet | With repeat | No repeat |
| --- | ---: | ---: |
| YOOCHOOSE Rep | 58.78 | 60.18 |
| YOOCHOOSE Non-Rep | 21.60 | 20.42 |
| DIGINTICA Rep | 56.27 | 29.20 |
| DIGINTICA Non-Rep | 7.71 | 9.48 |
| LASTFM Rep | 41.63 | 32.68 |
| LASTFM Non-Rep | 4.18 | 5.06 |

一般来说，如表 3 所示，带重复机制的 RepeatNet 在所有数据集上都优于不带重复机制的 RepeatNet。RepeatNet（有、无重复机制）在重复会话与非重复会话上的结果见表 4 和表 5。可以看到，RepeatNet 的提升主要来自重复会话。尤其在 DIGINTICA 和 LASTFM 上，RepeatNet 在重复会话的 Recall@20 上分别提高 33.91% 和 24.16%。然而，RepeatNet 在非重复会话上略有下降。这些结果表明，通过显式建模重复模式与探索模式，RepeatNet 还有更大潜力。但这也显示出 RepeatNet 的局限：如果让它完全从数据中学习模式概率，它似乎过于倾向重复推荐。应当加入一种机制来纳入先验知识。

<!-- 原 PDF 第 7 页 -->

**表 5：RepeatNet（有、无重复机制）在重复会话与非重复会话上的 Recall@20（%）。** 数据集名 DIGINTICA 按原 PDF 拼写。

| RepeatNet | With repeat | No repeat |
| --- | ---: | ---: |
| YOOCHOOSE Rep | 97.41 | 93.70 |
| YOOCHOOSE Non-Rep | 61.32 | 61.95 |
| DIGINTICA Rep | 99.09 | 65.18 |
| DIGINTICA Non-Rep | 34.58 | 36.73 |
| LASTFM Rep | 91.22 | 67.06 |
| LASTFM Non-Rep | 16.79 | 20.10 |

### 5.3 注意力与重复机制的对比分析

神经注意力已在许多任务上展现潜力（Bahdanau, Cho, and Bengio 2015; Ren et al. 2017; Li et al. 2017a），近来在推荐系统上也是如此（Li et al. 2017b; Xiao et al. 2017; Chen et al. 2017）。我们在表 6 和表 7 中比较 RepeatNet 有无注意力、有无重复机制的结果。结果表明，重复机制和注意力机制都能相对 Improved-GRU4REC 提升结果。重要的是，注意力与重复机制的贡献是互补的：二者结合在所有指标和所有数据集上都带来进一步提升，说明两者都是需要的。此外可以看到，注意力机制有助于提升 Recall，而重复机制有助于提升 MRR。

**表 6：RepeatNet 在注意力与重复机制对照下的 MRR@20（%）。** 数据集名 DIGINTICA 按原 PDF 拼写。

| RepeatNet | YOOCHOOSE | DIGINTICA | LASTFM |
| --- | ---: | ---: | ---: |
| No attention | 28.65 | 16.03 | 11.10 |
| No repeat | 30.76 | 13.52 | 10.47 |
| With both | 31.03 | 17.66 | 12.03 |

**表 7：RepeatNet 在注意力与重复机制对照下的 Recall@20（%）。** 数据集名 DIGINTICA 按原 PDF 拼写。

| RepeatNet | YOOCHOOSE | DIGINTICA | LASTFM |
| --- | ---: | ---: | ---: |
| No attention | 67.74 | 36.50 | 29.47 |
| No repeat | 70.21 | 42.56 | 29.96 |
| With both | 70.71 | 47.79 | 32.38 |

### 5.4 联合学习分析

有趣的是，如果联合训练推荐损失 $L_{rec}$ 与模式预测概率 $L_{mode}$，总体性能会略有下降，如表 8 所示。我们认为原因如下。第一，$L_{rec}$ 已经是学习模式预测的良好监督。这一结论可以从表 4 和表 5 得出：只使用 $L_{rec}$ 的 RepeatNet 在重复会话上取得了很大提升，而重复会话上尚余的改进空间相对较小。第二，只使用 $L_{rec}$ 的 RepeatNet 已经倾向于重复推荐。再加入 $L_{mode}$ 会进一步加剧这种情况。此外，$L_{mode}$ 假定若下一个物品存在于 $I_S$，则它是在重复模式下生成的，这并不总是合理的。

**表 8：RepeatNet 有、无联合学习时的 MRR@20 与 Recall@20（%）。**

| Loss | YOOCHOOSE MRR | YOOCHOOSE Recall | LASTFM MRR | LASTFM Recall |
| --- | ---: | ---: | ---: | ---: |
| $L_{rec}$ | 31.03 | 70.71 | 12.03 | 32.38 |
| $L_{rec} + L_{mode}$ | 28.99 | 69.64 | 11.58 | 31.94 |

## 6 结论与未来工作

我们提出具有编码器—解码器架构的 RepeatNet，以应对会话推荐任务中的重复消费。通过把重复—探索机制纳入 RNN，RepeatNet 能够更好地捕捉会话中“重复或探索”的推荐意图。我们在三个数据集上进行了大量实验与分析，并表明就 MRR 与 Recall 而言，RepeatNet 优于当时最先进的方法。

RepeatNet 可以从若干方向推进和扩展。第一，可以纳入人的先验知识来影响重复—探索机制。第二，可以考虑更多信息（例如元数据、文本）和更多因素（例如协同过滤），以进一步提升性能。此外，RepeatNet 的变体可以用于其他推荐任务，例如基于内容的推荐。

## 致谢

本工作得到中国国家自然科学基金（61672324, 61672322）、山东省自然科学基金（2016ZRE27468）、山东大学基本科研业务费、Ahold Delhaize、Amsterdam Data Science、Bloomberg Research Grant 计划、Elsevier、欧洲共同体第七框架计划（FP7/2007-2013）资助协议号 312827（VOX-Pol）、Google Faculty Research Awards 计划、Microsoft Research Ph.D. 计划、Netherlands Institute for Sound and Vision、荷兰科学研究组织（NWO）项目号 CI-14-25、652.002.001、612.001.551、652.001.003，以及 Yandex 的支持。全部内容代表作者的观点，并不必然为其各自雇主和/或赞助方所认同或背书。

## 代码

为便于复现本文结果，我们共享用于运行本文实验的代码：https://github.com/PengjieRen/RepeatNet 。

<!-- 原 PDF 第 8 页 -->

## 参考文献

[Anderson et al. 2014] Anderson, A.; Kumar, R.; Tomkins, A.; and Vassilvitskii, S. 2014. 重复消费的动态。In WWW ’14.

[Bahdanau, Cho, and Bengio 2015] Bahdanau, D.; Cho, K.; and Bengio, Y. 2015. 通过联合学习对齐与翻译的神经机器翻译。In ICLR ’15.

[Benson, Kumar, and Tomkins 2016] Benson, A. R.; Kumar, R.; and Tomkins, A. 2016. 建模用户消费序列。In WWW ’16.

[Celma 2010] Celma, Ò. 2010. 长尾中的音乐推荐与发现。Springer.

[Chen et al. 2012] Chen, S.; Moore, J. L.; Turnbull, D.; and Joachims, T. 2012. 通过度量嵌入做播放列表预测。In KDD ’12.

[Chen et al. 2017] Chen, J.; Zhang, H.; He, X.; Nie, L.; Liu, W.; and Chua, T.-S. 2017. 注意力协同过滤：带物品级与组件级注意力的多媒体推荐。In SIGIR ’17.

[Chen, Wang, and Wang 2015] Chen, J.; Wang, C.; and Wang, J. 2015. 你会“再次消费”最近的过去吗？短期再消费行为的快速预测。In AAAI ’15.

[Cheng et al. 2017] Cheng, Z.; Shen, J.; Zhu, L.; Kankanhalli, M.; and Nie, L. 2017. 利用音乐播放序列做音乐推荐。In IJCAI ’17, 3654–3660.

[Cheng et al. 2018] Cheng, Z.; Ding, Y.; Zhu, L.; and Kankanhalli, M. 2018. 方面感知的潜在因子模型：用评分和评论做评分预测。In WWW ’18, 639–648.

[Davidson et al. 2010] Davidson, J.; Liebald, B.; Liu, J.; Nandy, P.; Van Vleet, T.; Gargi, U.; Gupta, S.; He, Y.; Lambert, M.; Livingston, B.; and Sampath, D. 2010. YouTube 视频推荐系统。In RecSys ’10.

[Glorot and Bengio 2010] Glorot, X., and Bengio, Y. 2010. 理解训练深度前馈神经网络的困难。JMLR 9:249–256.

[Gu et al. 2016] Gu, J.; Lu, Z.; Li, H.; and Li, V. O. 2016. 在序列到序列学习中加入复制机制。In ACL ’16.

[He et al. 2017] He, X.; Liao, L.; Zhang, H.; Nie, L.; Hu, X.; and Chua, T.-S. 2017. 神经协同过滤。In WWW ’17.

[He et al. 2018a] He, X.; He, Z.; Du, X.; and Chua, T.-S. 2018a. 面向推荐的对抗个性化排序。In SIGIR ’18, 355–364.

[He et al. 2018b] He, X.; He, Z.; Song, J.; Liu, Z.; Jiang, Y.-G.; and Chua, T.-S. 2018b. NAIS：面向推荐的神经注意力物品相似度模型。TKDE 30(12):2354–2366.

[Hidasi and Karatzoglou 2017] Hidasi, B., and Karatzoglou, A. 2017. 带 top-k 增益的循环神经网络用于会话推荐。CoRR abs/1706.03847.

[Hidasi et al. 2016a] Hidasi, B.; Karatzoglou, A.; Baltrunas, L.; and Tikk, D. 2016a. 用循环神经网络做会话推荐。In ICLR ’16.

[Hidasi et al. 2016b] Hidasi, B.; Quadrana, M.; Karatzoglou, A.; and Tikk, D. 2016b. 面向特征丰富的会话推荐的并行循环神经网络架构。In RecSys ’16.

[Jannach and Ludewig 2017] Jannach, D., and Ludewig, M. 2017. 当循环神经网络遇上邻域：会话推荐。In RecSys ’17.

[Lerche, Jannach, and Ludewig 2016] Lerche, L.; Jannach, D.; and Ludewig, M. 2016. 论电子商务推荐中提醒的价值。In UMAP ’16.

[Li et al. 2017a] Li, H.; Min, M. R.; Ge, Y.; and Kadav, A. 2017a. 面向交互式问答的上下文感知注意力网络。In KDD ’17.

[Li et al. 2017b] Li, J.; Ren, P.; Chen, Z.; Ren, Z.; Lian, T.; and Ma, J. 2017b. 神经注意力会话推荐。In CIKM ’17.

[Mei et al. 2018] Mei, L.; Ren, P.; Chen, Z.; Nie, L.; Ma, J.; and Nie, J.-Y. 2018. 面向上下文感知推荐的注意力交互网络。In CIKM ’18, 157–166.

[Mobasher et al. 2002] Mobasher, B.; Dai, H.; Luo, T.; and Nakagawa, M. 2002. 在预测性 Web 使用挖掘任务中使用序列与非序列模式。In ICDM ’02.

[Pascanu, Mikolov, and Bengio 2013] Pascanu, R.; Mikolov, T.; and Bengio, Y. 2013. 论训练循环神经网络的困难。In ICML ’13.

[Quadrana et al. 2017] Quadrana, M.; Karatzoglou, A.; Hidasi, B.; and Cremonesi, P. 2017. 用层次循环神经网络个性化会话推荐。In RecSys ’17.

[Ren et al. 2017] Ren, P.; Chen, Z.; Ren, Z.; Wei, F.; Ma, J.; and de Rijke, M. 2017. 用神经注意力模型利用上下文句子关系做抽取式摘要。In SIGIR ’17.

[Rendle et al. 2009] Rendle, S.; Freudenthaler, C.; Gantner, Z.; and Schmidt-Thieme, L. 2009. BPR：来自隐式反馈的贝叶斯个性化排序。In UAI ’09.

[Rendle, Freudenthaler, and Schmidt-Thieme 2010] Rendle, S.; Freudenthaler, C.; and Schmidt-Thieme, L. 2010. 为下一购物篮推荐分解个性化马尔可夫链。In WWW ’10.

[Shani, Heckerman, and Brafman 2005] Shani, G.; Heckerman, D.; and Brafman, R. I. 2005. 基于 MDP 的推荐系统。JMLR 6:1265–1295.

[Srivastava et al. 2014] Srivastava, N.; Hinton, G.; Krizhevsky, A.; Sutskever, I.; and Salakhutdinov, R. 2014. Dropout：一种防止神经网络过拟合的简单方法。JMLR 15(1):1929–1958.

<!-- 原 PDF 第 9 页 -->

[Tan, Xu, and Liu 2016] Tan, Y. K.; Xu, X.; and Liu, Y. 2016. 改进的循环神经网络用于会话推荐。In DLRS ’16.

[Tokui et al. 2015] Tokui, S.; Oono, K.; Hido, S.; and Clayton, J. 2015. Chainer：下一代开源深度学习框架。In NIPS ’15.

[Xiao et al. 2017] Xiao, J.; Ye, H.; He, X.; Zhang, H.; Wu, F.; and Chua, T. 2017. 注意力因子分解机：通过注意力网络学习特征交互的权重。In IJCAI ’17.

[Yap, Li, and Yu 2012] Yap, G.-E.; Li, X.-L.; and Yu, P. S. 2012. 通过个性化序列模式挖掘做有效的下一物品推荐。In DASFAA ’12.

[Zhang et al. 2014] Zhang, Y.; Dai, H.; Xu, C.; Feng, J.; Wang, T.; Bian, J.; Wang, B.; and Liu, T.-Y. 2014. 用循环神经网络做赞助搜索的序列点击预测。In AAAI ’14.

[Zimdars, Chickering, and Meek 2001] Zimdars, A.; Chickering, D. M.; and Meek, C. 2001. 用时间数据做推荐。In UAI ’01.

<!-- 译完 -->
