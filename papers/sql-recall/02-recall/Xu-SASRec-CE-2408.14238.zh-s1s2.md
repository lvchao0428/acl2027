# Are LLM-based Recommenders Already the Best? Simple Scaled Cross-entropy Unleashes the Potential of Traditional Sequential Recommenders

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`Xu-SASRec-CE-2408.14238.pdf`。

## Abstract 摘要

大语言模型（large language models, LLMs）在推荐社区中受到越来越多的关注。一些研究观察到：当用带有全量 softmax 的交叉熵（cross-entropy, CE）损失对 LLM 进行微调时，它们可以在序列推荐中取得所谓 “state-of-the-art” 的表现。然而，用于比较的大多数基线是用逐点（pointwise）或成对（pairwise）损失函数训练的。这种不一致的实验设置导致传统方法被低估，并进一步助长了对 LLM 排序能力的过度自信。

在本研究中，我们通过证明交叉熵损失的两个可取性质——紧性（tightness）与覆盖（coverage）——为其优越性提供理论依据。此外，本研究还揭示若干新的见解：1）若只考虑推荐表现，CE 还不是最优的，因为它对某些排序指标而言并不是一个相当紧的界。2）在无法执行全量 softmax 的场景中，一种有效的替代是放大采样得到的归一化项。这些发现随后帮助释放传统推荐模型的潜力，使它们能够超过基于 LLM 的对应方法。鉴于巨大的计算负担，现有基于 LLM 的方法在序列推荐上并不像所声称的那样有效。我们希望这些理论理解连同经验结果，将有助于未来对基于 LLM 的推荐做出客观评估。代码见于 https://github.com/MTandHJ/CE-SCE-LLMRec。

## 1 Introduction 引言

随着互联网的迅速发展，每一刻产生的信息量都远超人类的辨别能力。推荐系统因此被发展出来，帮助人类快速而准确地确定感兴趣的物品，并在电子商务 [50]、在线新闻 [13] 与教育 [47] 等多样应用中扮演越来越重要的角色。由于数据类型与推荐目标存在固有差异，不同任务通常用不同的技术与模型来处理。例如，图神经网络 [22] 已在协同过滤（collaborative filtering）[15, 31] 中占据主导，而 Transformer [45] 在序列推荐（sequential recommendation）[20, 41] 中日益流行。

近来，大语言模型（Large Language Models, LLMs）[36, 33, 43, 44] 的繁荣指出一条通向通用推荐器（universal recommenders）[12, 26] 的有前景方向。配备精心设计的提示之后，它们在可解释推荐与跨域推荐中显示出很大潜力 [9, 10]。尽管如此，除非注入领域特定知识，LLM 与传统方法之间仍存在不可忽视的差距 [21, 1]。经过微调 [27, 48] 之后，一些研究观察到 “compelling” 的结果，并匆忙肯定了基于 LLM 的推荐器的排序能力。译文：引人注目。考虑到 LLM 所伴随的巨大计算负担，我们认为此类声称在被接受和应用之前必须经过仔细审视，以避免大规模的资源浪费。回想一下，用于 LLM 预训练（以及微调）的下一 token 预测目标，本质上依赖一个交叉熵损失，该损失需要对整个语料做全量 softmax。与此相对，大多数传统推荐器使用逐点或成对损失来训练；例如，SASRec [20] 所采用的 BCE，或 FMLP-Rec [51] 中的 BPR，都为每个正物品动态采样一个负物品。一些研究 [5, 23] 已经指出，在序列推荐中 CE 通常优于 BCE 或 BPR，这使我们对先前比较的公平性产生疑虑。在本文中，我们要整体地澄清这些疑虑。

**Q1.** 当交叉熵损失被同时应用于双方时，基于 LLM 的推荐器是否优于传统模型？由于非 ID 模型的表现往往低于整合了 ID 的方法，我们比较了四个带有独立 ID 嵌入表的、当前最优的基于 LLM 的推荐器，以及四个分别建立在 MLP、CNN、RNN 或 Transformer 之上的传统模型。有趣的是，尽管传统方法在使用 BCE 或 BPR 时确实远远落后，一旦应用交叉熵损失，其中一些会以很大幅度超过 LLM。

**Q2.** 如何理解交叉熵损失在提升推荐器排序能力方面的优越性？一方面，Bruch 等人 [4] 已从理论上建立了交叉熵损失与某些排序指标之间的联系。另一方面，Wu 等人 [46] 进一步证明了它在缓解流行度偏差（popularity bias）方面的有益性质。这里，我们接续 [4]，揭示进一步的新见解：一个理想的推荐损失应当同时强调紧性与覆盖。前者要求推荐损失应当被设计成排序指标的一个良好软代理（soft proxy），以便获得一致的改进；后者强调在训练过程中探索足够数量的负样本。显然，CE 在覆盖上是最优的，因为它在每一次小批量（mini-batch）迭代中纳入全部物品。然而，我们从理论上表明，它在紧性上仍然次优。更优的推荐表现可以通过动态截断获得。

**Q3.** 当无法执行全量 softmax 时，传统模型是否仍然能够优于基于 LLM 的推荐器？需要注意的是，在实际场景中，物品数量可以达到数亿（hundreds of millions），使得精确执行全量 softmax 不可行。得益于子词切分算法（subword segmentation）[24] 的出现，语言模型的语料规模受到约束，从而只要那些分离的 ID 能够以同样的方式被表示 [19]，就为上述问题提供了一种可行的解决办法。因此，如果传统模型在这种实际情形下不能充分释放其潜力，当前基于 LLM 的推荐器的表现就仍然非常有前景。受 Q2 中理论发现的启发，我们提出一个非常简单的替代，称为放缩交叉熵（Scaled Cross-Entropy, SCE），以处理现实中的这些疑虑。SCE 均匀采样物品，以估计交叉熵的归一化项。与表现出较差紧性的普通采样 softmax 损失相对（其形式化论证见第 4 节），SCE 通过用一个额外权重放大采样项来处理这一问题。结果是，每次迭代只采样非常少的负样本，就足以达到与使用全量 softmax 的交叉熵相当的结果。

本文其余部分组织如下。第 2 节将对其表现做初步考察。然后第 3 节将在理论上讨论 Q2，而 Q3 的实际比较见于第 4 节。我们最后在第 5 节回顾序列推荐与基于 LLM 的推荐的相关工作。

## 2 Potential of Traditional Recommenders over LLM-based Recommenders 传统推荐器相对基于 LLM 的推荐器的潜力

在本节中，我们展示传统序列推荐模型在从 BCE/BPR 切换到 CE 时，表现如何变化。实验设置将首先介绍。

**Problem definition.** 问题定义。给定一个包含若干用户信息的查询 \(q\)，推荐系统旨在检索一些用户会感兴趣的物品 \(v \in \mathcal{I}\)。在序列推荐中，这是基于历史交互 \(q = [v_1, v_2, \ldots, v_t]\) 来预测下一个物品 \(v_{t+1}\)。关键组成部分是构造一个打分函数 \(s_{qv} := s_\theta(q, v)\)，以准确建模查询 \(q\) 对候选物品 \(v\) 的相关度。一种常见范式是通过由 \(\theta\) 参数化的模型把它们映射到同一潜在空间，随后用内积运算计算相似度。然后，基于这些分数排名靠前的物品将被优先推荐。通常，所期望的推荐器被训练来在所有已观测交互 \(\mathcal{D}\) 上最小化一个优化目标。原文写作 optimation。

\[
\min_\theta \mathbb{E}_{(q, v^+) \sim \mathcal{D}}[\ell(q, v^+; \theta)],
\]

其中 \(v^+\) 表示查询 \(q\) 的目标物品，本文所考虑的损失函数 \(\ell\)（见表 1）可以改写为

\[
\ell(q, v^+; \theta) := -\log \frac{\exp(s_\theta(q, v^+))}{Z_\theta(q)} = -s_\theta(q, v^+) + \log Z_\theta(q). \tag{1}
\]

这里，我们特意把 “normalizing” 项 \(Z_\theta(q)\) 分离出来，因为它在确定与排序指标的联系时扮演重要角色。译文：归一化项。若不会引起歧义，此后我们将省略 \(q\) 与 \(\theta\)。

**Datasets.** 数据集。我们选择两个公开数据集，即 Beauty 与 Yelp，它们在先前研究中被广泛使用 [20, 12, 26]。遵循 [51, 12]，我们过滤掉交互少于 5 次的用户与物品；验证集与测试集按留一法（leave-one-out）划分，即最后一次交互用于测试，倒数第二次用于验证。预处理之后的数据集统计见于附录 A.4。

**Evaluation metrics.** 评估指标。对每个用户，推荐器返回的分数将按降序排列，以生成候选列表。把目标物品 \(v^+\) 的预测名次记为

\[
r^+ := r(v^+) = |\{v \in \mathcal{I} : s_v \ge s_{v^+}\}|.
\]

归一化折损累计增益（Normalized Discounted Cumulative Gain, NDCG）与平均倒数排名（Mean Reciprocal Rank, MRR）常被用来评估排序质量。对于本文所考虑的下一项推荐，NDCG 与 MRR（对单个查询）可以简化为

\[
\mathrm{NDCG}(r^+) = \frac{1}{\log_2(1 + r^+)}, \qquad \mathrm{MRR}(r^+) = \frac{1}{r^+}. \tag{2}
\]

当目标物品 \(v^+\) 排名更高时，二者都增大，并在 \(v^+\) 排在第一（即 \(r^+ = 1\)）时达到最大。因此，在整个测试集上计算的平均质量，充当排序能力的一个指标。

脚注 1：在实践中，当 \(r^+\) 超过一个预先指定的阈值 \(k\)（例如 \(k = 1, 5, 10\)）时，它被视为没有意义。因此，广泛采用的 NDCG@\(k\) 与 MRR@\(k\) 指标被修改为：对这些较差的排序结果赋予零奖励。

**Baselines.** 基线。尽管 LLM 本身具有令人惊讶的零样本（zero-shot）推荐能力，除非注入领域特定知识，仍然存在不可忽视的差距 [21, 1]。因此，本文将只比较由独立 ID 嵌入表增强的、基于 LLM 的推荐器：P5 (CID+IID) [19]、POD [26]、LlamaRec [48] 与 E4SRec [27]。具体而言，前两种方法以 T5 为基础模型，后两种方法微调 Llama2，以做高效的序列推荐。因为随 POD 提供的数据预处理脚本可能导致信息泄漏 [37]，我们给物品分配随机整数 ID，而不是依次递增的整数 ID。此外，这里考虑四个序列模型，包括 Caser [42]、GRU4Rec [17]、SASRec [20] 与 FMLP-Rec [51]，以揭示传统方法的真实能力。它们覆盖多种架构，从而全面验证所提出近似方法的有效性。表 2 给出模型统计的概览。其他实现细节见于附录 A.7。

**Observations.** 观察。让我们关注表 3 的前三个区块。其中大多数传统模型明显落后于基于 LLM 的推荐器（例如 LlamaRec）。尽管当前最优模型 FMLP-Rec 在 Yelp 上取得相当好的结果，它在 Beauty 上相对 P5、LlamaRec 与 E4SRec 仍然表现不如，差距至少为 20%。特别是，SASRec 作为一种与基于 LLM 的推荐器相似的、基于 Transformer 的模型，比较之下不幸表现不佳。人们很容易把这一结果归因于 LLM 优越的模型表达能力与世界知识。然而，根据使用 CE 得到的结果，情况似乎并非如此：SASRec 与 FMLP-Rec 因这一细微改变而表现出显著的性能提升，最终在 Beauty 与 Yelp 两个数据集上都超过了所有基于 LLM 的推荐器。GRU4Rec 与 Caser 也从使用 CE 中受益，尽管由于表达能力有限，它们可能无法超过基于 LLM 的推荐器。

因此，我们认为，先前关于 LLM 推荐表现的肯定性断言，根植于有偏的比较：其中 BCE 或 BPR 被普遍用于训练传统模型。此外，膨胀的模型规模（从 P5 的 60M 到 LlamaRec 的 7B）只在部分指标上带来边际改进。丰富的世界知识与强大的推理能力在这里似乎用处有限。结论是：即便经过微调，当可以执行全量 softmax 时，基于 LLM 的推荐器并不能超过当前最优的传统序列模型。

表 1 出现在本节版面中。图注原文：Loss functions discussed in this paper and their bounding probabilities in the case of uniform sampling. \(\sigma(\cdot)\) stands for the sigmoid function。译文：本文讨论的损失函数，以及均匀采样情形下它们的定界概率。\(\sigma(\cdot)\) 表示 sigmoid 函数。列名为 Loss、Formulation、“Normalizing” term \(Z\)、Bounding probability \(\ge\)。求和号在抽取中呈 P、X；SSM 与 SCE 界概率式中的括号被抽成控制字符。下表按可辨认的分式、\(1 \cdot \sum_{i=1}^{K}\)、\(\alpha\)、\(1-r^+/|\mathcal{I}|\)、\(\lfloor K/m \rfloor\) 与 \(\lceil m/\alpha \rceil\) 还原。

| Loss | Formulation | “Normalizing” term \(Z\) | Bounding probability \(\ge\) |
| --- | --- | --- | --- |
| \(\ell_{\mathrm{CE}}\) | \(-\log \dfrac{\exp(s_{v^+})}{\sum_{v \in \mathcal{I}} \exp(s_v)}\) | \(\sum_{v \in \mathcal{I}} \exp(s_v)\) | \(1\) |
| \(\ell_{\mathrm{BCE}}\) | \(-\log\sigma(s_{v^+}) - \log(1-\sigma(s_{v^-}))\) | \((1+\exp(s_{v^+}))(1+\exp(s_{v^-}))\) | \(0\) |
| \(\ell_{\mathrm{BPR}}\) | \(-\log\sigma(s_{v^+}-s_{v^-})\) | \(\exp(s_{v^+})+\exp(s_{v^-})\) | \(0\) |
| \(\ell_{\mathrm{SSM}}\) | \(-\log \dfrac{\exp(s_{v^+})}{\exp(s_{v^+}) + 1 \cdot \sum_{i=1}^{K}\exp(s_{v_i})}\) | \(\exp(s_{v^+}) + \sum_{i=1}^{K}\exp(s_{v_i})\) | \(1 - m\left(1 - r^+/|\mathcal{I}|\right)^{\lfloor K/m \rfloor}\) |
| \(\ell_{\mathrm{SCE}}\) | \(-\log \dfrac{\exp(s_{v^+})}{\exp(s_{v^+}) + \alpha \sum_{i=1}^{K}\exp(s_{v_i})}\) | \(\exp(s_{v^+}) + \alpha \sum_{i=1}^{K}\exp(s_{v_i})\) | \(1 - \lceil m/\alpha \rceil \left(1 - r^+/|\mathcal{I}|\right)^{\lfloor K/\lceil m/\alpha \rceil \rfloor}\) |

表 2 出现在本节版面中。图注原文：Model statistics. “Max Seq. Len.” denotes the maximum input sequence length while “Max ID Seq. Len.” indicates the maximum number of historical user interactions used for prediction。译文：模型统计。Max Seq. Len. 表示最大输入序列长度，Max ID Seq. Len. 表示用于预测的历史用户交互的最大条数。传统模型的 Foundation Model 一列在抽取中为空。

| Model | Foundation Model | Architecture | Emb. Size | Max Seq. Len. | Max ID Seq. Len. | #Params |
| --- | --- | --- | --- | --- | --- | --- |
| P5 (CID+IID) [19] | T5 | Transformer | 512 | 512 | 50 | 60M |
| POD [26] | T5 | Transformer | 512 | 512 | 50 | 60M |
| LlamaRec [48] | Llama2 | Transformer | 4096 | 2048 | 50 | 7B |
| E4SRec [27] | Llama2 | Transformer | 4096 | 2048 | 50 | 7B |
| GRU4Rec [17] |  | RNN | 64 | 50 | 50 | 0.80M |
| Caser [42] |  | CNN | 64 | 50 | 50 | 3.80M |
| SASRec [20] |  | Transformer | 64 | 50 | 50 | 0.83M |
| FMLP-Rec [51] |  | MLP | 64 | 50 | 50 | 0.92M |

表 3 出现在本节版面中。图注原文：Overall performance comparison on the Beauty and Yelp datasets. The best results of each block are marked in bold. Gray results indicate less than that of best LLM-based recommenders. “▲ % over LLM” represents the relative gap between respective best results。译文：在 Beauty 与 Yelp 数据集上的总体表现比较。每个区块的最佳结果以粗体标出。灰色结果表示低于最佳的基于 LLM 的推荐器。“▲ % over LLM” 表示各自最佳结果之间的相对差距。粗体与灰色在纯文本抽取中丢失，【抽取不清】。数值按 Beauty 的 NDCG@5、NDCG@10、MRR@5、MRR@10，以及 Yelp 的同样四列拆开。

| Method | Beauty NDCG@5 | NDCG@10 | MRR@5 | MRR@10 | Yelp NDCG@5 | NDCG@10 | MRR@5 | MRR@10 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LLM: POD | 0.0125 | 0.0146 | 0.0107 | 0.0116 | 0.0330 | 0.0358 | 0.0267 | 0.0292 |
| LLM: P5 (CID+IID) | 0.0403 | 0.0474 | 0.0345 | 0.0376 | 0.0200 | 0.0252 | 0.0164 | 0.0186 |
| LLM: LlamaRec | 0.0405 | 0.0492 | 0.0344 | 0.0380 | 0.0306 | 0.0367 | 0.0270 | 0.0295 |
| LLM: E4SRec | 0.0376 | 0.0448 | 0.0326 | 0.0356 | 0.0207 | 0.0260 | 0.0174 | 0.0196 |
| BPR: GRU4Rec | 0.0155 | 0.0208 | 0.0125 | 0.0147 | 0.0106 | 0.0147 | 0.0086 | 0.0102 |
| BPR: Caser | 0.0173 | 0.0221 | 0.0143 | 0.0163 | 0.0211 | 0.0250 | 0.0185 | 0.0201 |
| BPR: SASRec | 0.0298 | 0.0374 | 0.0248 | 0.0279 | 0.0167 | 0.0218 | 0.0137 | 0.0158 |
| BPR: FMLP-Rec | 0.0321 | 0.0393 | 0.0269 | 0.0298 | 0.0334 | 0.0405 | 0.0286 | 0.0314 |
| BPR: ▲ % over LLM | -20.8% | -20.3% | -22.1% | -21.5% | +1.3% | +10.3% | +5.7% | +6.5% |
| BCE: GRU4Rec | 0.0134 | 0.0186 | 0.0108 | 0.0129 | 0.0098 | 0.0135 | 0.0079 | 0.0094 |
| BCE: Caser | 0.0185 | 0.0234 | 0.0154 | 0.0174 | 0.0224 | 0.0264 | 0.0198 | 0.0214 |
| BCE: SASRec | 0.0275 | 0.0353 | 0.0225 | 0.0257 | 0.0225 | 0.0281 | 0.0192 | 0.0215 |
| BCE: FMLP-Rec | 0.0301 | 0.0381 | 0.0248 | 0.0281 | 0.0330 | 0.0391 | 0.0287 | 0.0312 |
| BCE: ▲ % over LLM | -25.8% | -22.6% | -28.1% | -26.0% | -0.1% | +6.5% | +6.1% | +5.7% |
| CE: GRU4Rec | 0.0329 | 0.0398 | 0.0281 | 0.0310 | 0.0171 | 0.0231 | 0.0137 | 0.0161 |
| CE: Caser | 0.0303 | 0.0361 | 0.0260 | 0.0284 | 0.0211 | 0.0243 | 0.0187 | 0.0200 |
| CE: SASRec | 0.0510 | 0.0597 | 0.0443 | 0.0479 | 0.0345 | 0.0415 | 0.0302 | 0.0331 |
| CE: FMLP-Rec | 0.0507 | 0.0594 | 0.0438 | 0.0473 | 0.0364 | 0.0444 | 0.0316 | 0.0348 |
| CE: ▲ % over LLM | +25.7% | +21.3% | +28.1% | +26.0% | +10.3% | +21.0% | +16.9% | +18.1% |
