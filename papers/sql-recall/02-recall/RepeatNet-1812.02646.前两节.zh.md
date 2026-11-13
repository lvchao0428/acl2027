> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名：** RepeatNet-1812.02646.pdf

**原文标题：** RepeatNet: A Repeat Aware Neural Recommendation Machine for Session-based Recommendation

**作者：** Pengjie Ren（山东大学、阿姆斯特丹大学），Zhumin Chen、Jing Li、Jun Ma（山东大学），Zhaochun Ren（京东 Data Science Lab），Maarten de Rijke（阿姆斯特丹大学）

**场合：** arXiv:1812.02646v1 [cs.IR]，2018 年 12 月 6 日。页脚版权为 2019 年 Association for the Advancement of Artificial Intelligence (AAAI)。

## 摘要

Session-based recommendation 上的循环神经网络已经显示出不错的效果，但作者认为有一类很常见的行为还没有被神经网络认真对待：repeat consumption，也就是同一件物品在电商、音乐、电视节目等场景里被反复消费。他们要解决的是“什么时候该做重复推荐”。

提出的模型叫 RepeatNet，采用 encoder-decoder。decoder 里保留常规的神经推荐，同时加一套 repeat 机制：能从用户历史里挑出旧物品，并在合适的时机推荐。实验用三个 benchmark。摘要的结论是定性的：三个数据集上 MRR 和 Recall 都超过当时的 state-of-the-art；数据集越大、repeat 比例越高，相对基线的提升也越大。摘要没有给出具体分数。

## 1 Introduction

Session 在这里指一段时间内发生的一组交互，可以在同一天，也可以跨天、跨周甚至跨月。早期 session 方法多半只依赖最后一次交互或最后一个 session：用 Markov 模型抽取序列模式来预测下一项（Zimdars, Chickering, and Meek 2001；Shani, Heckerman, and Brafman 2005），或用 logistic Markov embeddings 为歌曲学表示、做歌单预测（Chen et al. 2012）。这些模型的共同瓶颈是状态空间：一旦要把所有物品上的可能选择序列都放进去，状态很快就不可管理。

神经网络这条线从 Hidasi et al. (2016a) 用 GRU 做 session 推荐开始。后续工作包括：同时看点击以及物品图像、文本特征的 parallel RNN（Hidasi et al. 2016b）；把 RNN 隐状态跨 session 传递并演化的 Hierarchical RNN（Quadrana et al. 2017）；在 session 推荐里加入 attention、并超过 Hidasi et al. (2016a) 的 Li et al. (2017b)。作者指出，深度模型在增加，却没有人把 repeat consumption 当作要显式处理的对象。他们用日常习惯来说明这种现象：反复购买同类商品、固定去同一家餐厅、反复听同一批歌曲和艺人（Anderson et al. 2014）。Table 1 给出三个常用数据集的 repeat ratio（%）：

| 数据集 | Train | Validation | Test |
|---|---:|---:|---:|
| YOOCHOOSE 1/4 | 25.52 | 25.51 | 26.02 |
| DIGINETICA | 19.94 | 20.06 | 20.49 |
| LASTFM | 20.72 | 20.42 | 20.95 |

也就是说，这些数据里大约五分之一到四分之一的交互属于重复消费。

RepeatNet 不用单一 decoder 给每个物品打分。同一物品的推荐概率由两个 decoder 分别估计：repeat mode 从用户历史中推荐旧物品，explore mode 推荐新物品。具体顺序是：先把 session 编成表示；再用 repeat-explore 机制学习两种模式之间的切换概率；repeat recommendation decoder 估计旧物品概率，explore recommendation decoder 估计新物品概率；最后把模式切换概率和两种模式下的物品概率按概率方式合成推荐分数。模式预测和物品推荐在同一框架里用端到端反向传播联合训练。引言再次报告三个 benchmark 上 MRR、Recall 的优势，以及提升随数据规模和 repeat 比例增大而增大，仍未给出具体分数。贡献被概括为三点：第一次在 session-based recommendation 的神经模型中考虑 repeat consumption；用双 decoder 自动学习 repeat 与 explore 的切换概率；在三个 benchmark 上说明，显式建模重复消费可以超过当时的方法。

## 2 Related Work

相关工作分成 session-based recommendation 与 repeat recommendation 两块。

### 2.1 Session-based recommendation

传统方法通常是 Markov chain：用上一个动作预测下一个动作。Zimdars, Chickering, and Meek (2001) 用概率决策树从序列模式学习下一状态。Mobasher et al. (2002) 比较不同序列模式后认为，相邻的 contiguous sequential patterns 比一般序列模式更适合序列预测。Shani, Heckerman, and Brafman (2005) 用 Markov decision process 做 session 推荐，最简单的情形退化为物品间转移概率构成的一阶 Markov chain。Yap, Li, and Yu (2012) 在个性化序列模式挖掘中引入 competence score，用于下一项推荐。Chen et al. (2012) 把歌单建成 Markov chain，并用 logistic Markov embeddings 学习歌曲表示。作者再次把状态空间膨胀写成 Markov 路线的主要困难。

RNN 方面，Zhang et al. (2014) 已用于序列点击预测。Hidasi et al. (2016a) 把 RNN 用到 session 推荐，采用 session-parallel mini-batch 和基于排序的损失，相对传统方法有明显提升；随后的 p-RNN 同时建模点击和物品特征，并改用更适合该结构的训练策略（Hidasi et al. 2016b）。Tan, Xu, and Liu (2016) 用数据增强，以及处理输入分布漂移的方法来改进模型。Jannach and Ludewig (2017) 报告，基于启发式的 session 近邻在大多数测试配置和数据集上超过 Hidasi et al. (2016a)。Quadrana et al. (2017) 用跨 session 信息传递来个性化 RNN，Hierarchical RNN 在用户的多个 session 之间传递并演化隐状态。Li et al. (2017b) 用带 attention 的混合 encoder，同时建模序列行为和当前 session 的主要意图。作者把自身与上述工作的分界放在：RepeatNet 把 repeat consumption 放进模型。

### 2.2 Repeat recommendation

Anderson et al. (2014) 考察用户在多种领域里反复消费同一物品的模式，范围从同一地点的签到到同一视频的重看。他们发现，最近一次消费的时间远近（recency）是预测再次消费的最强因素。Chen, Wang, and Wang (2015) 归纳出影响短期重复消费的四类通用特征，并给出线性核与二次核的两个快速算法，用来在给定上下文下预测用户会不会在某个时刻发生短期重复消费。

推荐系统的常见目标是帮用户发现新物品；不少真实系统还有另一个目标，即提醒用户曾经看过或消费过的物品。Lerche, Jannach, and Ludewig (2016) 用线上实验衡量这种提醒在推荐列表中的价值。Benson, Kumar, and Tomkins (2016) 归纳重复消费的两条宏观规律：一个用户的生命周期里，能长期存在的物品很少；某物品临近被放弃时，相邻消费的间隔会变长，对应厌倦逐渐累积。作者把差别概括为：他们第一次用神经推荐模型，在传统推荐和 session-based recommendation 中都显式处理 repeat consumption。
