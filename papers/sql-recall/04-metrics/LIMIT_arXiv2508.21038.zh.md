# 基于嵌入的检索的理论局限性

- 原文件名：LIMIT_arXiv2508.21038.pdf
- 原标题：On the Theoretical Limitations of Embedding-Based Retrieval
- 中文标题：基于嵌入的检索的理论局限性
- 作者：Orion Weller, Michael Boratko, Iftekhar Naim, Jinhyuk Lee
- 会议或 arXiv：页眉为 Published as a conference paper at ICLR 2026；页边 arXiv 号为 arXiv:2508.21038v2 [cs.IR] 12 Mar 2026
- 单位：1Google DeepMind，2Johns Hopkins University
- 邮箱：oweller@cs.jhu.edu, jinhyuklee@google.com

<!-- 原 PDF 第 1 页 -->

## 摘要

多年来，向量嵌入被赋予了越来越多的检索任务，并且开始被用于推理、指令遵循、编程等场景。这些新基准要求嵌入对任意查询、以及可能给出的任意相关性定义都有效。先前工作已经指出向量嵌入的理论局限，但一个常见假设是：这些困难完全来自不现实的查询，而那些做不到的情况可以用更好的训练数据和更大的模型来克服。在本文中，我们证明，在现实设定下，即便查询极其简单，也可能会遇到这些理论局限。我们联系学习理论中的已知结果，表明：能够作为某个查询的结果被返回的文档 top-k 子集的数量，受到嵌入维度的限制。我们从经验上表明，即便直接在测试集上用自由参数化的嵌入进行优化，这一结论仍然成立。随后我们基于这些理论结果构造了一个名为 LIMIT 的现实数据集，用以对嵌入模型进行压力测试，并观察到：尽管任务本身很简单，即便是当前最先进的模型也会在该数据集上失败。我们的工作揭示了现有单向量范式下嵌入模型的极限，并呼吁未来研究发展能够解决这一根本局限的新技术。

## 1 引言

过去二十年里，信息检索（IR）从以稀疏技术为主的模型（例如 BM25，Robertson et al. (1995)）转向以神经语言模型（LM）为骨干的模型（Lee et al., 2019; Craswell et al., 2020; Izacard et al., 2021; Wang et al., 2022）。这些神经模型主要以单向量方式使用：它们为整个输入输出一个嵌入（也称为稠密检索）。这些嵌入模型能够泛化到新的检索数据集，并被要求解决越来越复杂的检索问题（Thakur et al., 2021; Enevoldsen et al., 2025; Lee et al., 2025）。

近年来，随着指令遵循检索基准的兴起，这一趋势被推得更远：模型被要求为任意查询表示任意相关性定义（Weller et al., 2025a;c; Song et al., 2025; Xiao et al., 2024; Su et al., 2024）。例如，QUEST 数据集（Malaviya et al., 2023）用逻辑算子组合不同概念，研究复杂查询的检索难度（例如 “Moths or Insects or Arthropods of Guadeloupe”）。另一方面，BRIGHT（Su et al., 2024）等数据集通过把相关性定义成需要推理的方式，探索不同相关性定义带来的挑战。其中一个子任务是：给定一道 Leetcode 题目作为查询，找出共享某一子任务的其他 Leetcode 题目（例如其他使用动态规划的题目）。尽管模型目前还解不了这些基准，社区提出这些问题，是为了推动稠密检索器能力的边界——而这一边界现在被隐含地理解成“任何可以被定义的任务”。

与其再提出经验性基准去测量嵌入模型能做到什么，我们希望在更根本的层面上理解其局限是什么。由于嵌入模型使用

<!-- 原 PDF 第 2 页 -->

**图 1 见原 PDF。** 图中文字大意：左侧为“查询—文档相关性”，属性包括 Quokkas、Apples 等，文档为 Jon、Ovid、Leslie 等；中间问句是“嵌入能否表示全部相关性组合？”；右侧为 LIMIT 的现实实例，例如查询 “Who likes Quokkas?”，以及 “Jon Durben likes Quokkas and Apples.”、“Ovid Rahm likes Quokkas and Rabbits.”、“Leslie Laham likes Apples and Candy.”。

图 1：LIMIT 数据集构造过程的示意，其依据是理论局限。我们对 N 篇文档的全部相关性组合进行测试（图中是三篇文档、每个查询两篇相关文档的全部相关性组合），并用一种简单映射把它实例化。

几何空间中的向量表示，因而存在研究充分的数学领域（Papadimitriou & Sipser, 1982），可以用来分析这些表示。

我们的工作旨在弥合这一缺口，把线性代数中的已知理论结果与神经信息检索的现代进展联系起来。我们借助高维几何中的研究，给出表示给定相关文档与查询组合所需嵌入维度的下界。具体而言，我们证明：对于给定的嵌入维度 $d$，存在一些文档的 top-k 组合，无论查询是什么都无法被返回——这指出了嵌入模型的一个理论且根本的极限。

为了表明这一理论极限对任何检索模型或训练数据集都成立，我们测试这样一种设定：向量本身直接用测试数据来优化。这使我们能够从经验上展示嵌入维度如何决定检索任务能否被解出。我们发现，对每个嵌入维度 $d$ 都存在一个关键点：文档数量太大，以至于该嵌入维度无法编码全部组合。然后我们收集多种 $d$ 下的这些关键点，并表明这一关系可以用一个多项式函数从经验上拟合。

我们还更进一步，基于这些理论局限构造了一个现实但简单的数据集（称为 LIMIT）。【脚注 1】尽管任务很简单（例如 “who likes Apples?” 以及 “Jon likes Apples, ...”），我们发现，即便是 MTEB（Enevoldsen et al., 2025）上当前最先进的嵌入模型（Lee et al., 2025; Zhang et al., 2025）也非常困难，而对嵌入维度较小、使用标准优化技术的模型则几乎不可能。

总体而言，我们的贡献是：（1）为嵌入模型的根本局限提供理论基础；（2）一种最佳情形的经验分析，表明该证明对任何数据集实例都成立（通过对自由嵌入的优化）；（3）一个简单的现实自然语言实例 LIMIT，即便当前最先进的嵌入模型也无法解决。

这些结果对社区有一些值得注意的含义：一方面，神经嵌入模型正在取得巨大成功；然而，学术基准只测试了可能被提出的查询中的很小一部分（而且这些查询常常被过拟合），从而掩盖了这些局限。我们的工作表明，当交给嵌入模型的任务要求返回越来越多的 top-k 相关文档组合时（例如通过指令用逻辑算子把原先无关的文档连接起来），我们会达到它们所能表示的组合数量的极限。

因此，社区应当意识到这些局限：既要在构造评测时意识到，也要在试图覆盖全部指令查询——即任意查询与任意相关性定义——时使用替代架构，例如交叉编码器、多向量、或表达能力更强的相似度函数。

【脚注 1】数据与代码见 https://github.com/google-deepmind/limit 。

<!-- 原 PDF 第 3 页 -->

## 2 相关工作

### 2.1 神经嵌入模型

近年来嵌入模型取得了巨大进展（Lee et al., 2019; Craswell et al., 2020; BehnamGhader et al., 2024），从简单的网页搜索（仅文本）走向高级的指令遵循与多模态表示。这些模型大体上跟随语言模型的进展，例如预训练 LM（Hoffmann et al., 2022）、多模态 LM（Li et al., 2024; Team, 2024），以及指令遵循方面的进展（Zhou et al., 2023; Ouyang et al., 2022）。检索中的一些突出例子包括：聚焦多模态嵌入的 CoPali（Faysse et al., 2024）与 DSE（Ma et al., 2024），用于指令遵循的 Instructor（Su et al., 2022）与 FollowIR（Weller et al., 2024a），以及把预训练 LM 变成嵌入器的 GritLM（Muennighoff et al., 2024）与 Gemini Embeddings（Lee et al., 2025）。

我们的工作为简便起见只关注文本表示，但它适用于任何数据集领域中的全部单向量嵌入模态。随着要表示的空间通过指令或多模态而增长，它们将越来越多地撞上这些理论局限。

### 2.2 把稠密检索推向极限的经验任务

检索模型已被推出其最初用例，以处理广泛的领域。值得注意的工作包括：表示大量领域（Thakur et al., 2021; Lee et al., 2024），多样的指令集合（Weller et al., 2024a; Zhou et al., 2024; Oh et al., 2024; Weller et al., 2025b），以及对查询进行推理（Xiao et al., 2024; Su et al., 2024）。这把嵌入模型的重点从基本的关键词匹配，推向能够表示语言完整语义的嵌入。因此，把原先无关的文档连接进 top-k 相关集合比以往更常见，【脚注 2】从而增加了模型必须能够表示的组合数量。这促使我们去理解嵌入能够表示什么的极限，因为当前工作期望它处理每一项任务。

先前工作从经验上探索过模型的极限：Reimers & Gurevych (2020) 表明，维度更小的嵌入模型有更多假阳性，尤其是在更大规模的语料上。Ormazabal et al. (2019) 展示了跨语言设定中模型的经验局限，Yin & Shen (2018) 表明嵌入维度如何与偏差—方差权衡相关。与之相对，我们的工作在嵌入维度与它能够检索的 top-k 集合之间建立理论联系，同时也展示经验上的局限。

### 2.3 几何空间中向量的理论极限

在语义空间中理解并寻找最近邻，在数学研究中有很长的历史，早期工作如 Voronoi 图的研究可追溯到 1644 年，并于 1908 年被形式化（Voronoi, 1908）。$k$ 阶 Voronoi 图（即按最近的 $k$ 个点把空间划分成区域的 Voronoi 图）显然与信息检索相连，并已被研究多年（Clarkson, 1988）。此类区域的数量等于大小为 $k$ 的唯一检索集合的数量，然而这个量 notoriously 难以被紧致地界定（Bohler et al., 2015; Lee, 1982; Chen et al., 2023）。（原文 “notoriously difficult to bound tightly”，此处译为“众所周知很难给出紧界”。）

我们从另一个角度处理这个问题：不问给定构型实现了多少个 $k$-子集，而问要以带保证的分数间隔实现全部 $k$-子集，需要多大的嵌入维度。通过应用经典的球体填充体积论证（Vershynin, 2018; Conway et al., 1999），我们得到一个用 $n$、$k$ 和间隔 $\gamma$ 表示的嵌入维度下界。我们的结果在概念上与 Johnson–Lindenstrauss 引理（Johnson et al., 1984）相关：该引理给出保持 $n$ 个点之间成对距离的充分维度；与之相对，我们的界给出的是以一定间隔实现全部检索集合所必需的维度。间隔在控制可实现构型复杂度中的作用，也平行于统计学习理论中的经典结果，包括 fat-shattering 维（Kearns & Schapire, 1994）以及线性分类器基于间隔的泛化界（Bartlett, 2002; Vapnik, 1998）：更大的间隔同样约束假设类的容量。

【脚注 2】可以想象一种很容易把任意两篇文档连起来的办法：只用逻辑算子，即 X and Y。

<!-- 原 PDF 第 4 页 -->

## 3 向量嵌入的表示容量

在本节中，我们形式化地定义满足给定检索目标所需的最小嵌入维度，并借助高维几何中的经典球体填充结果建立下界。我们指出，这将是一个极端的下界，因为实际模型还必须处理其他约束，例如通过梯度下降学习，以及使用 LM 的分词。

**设定。** 令 $v_1, \ldots, v_n \in \mathbb{R}^d$ 为文档向量（按原文为 unit document vectors，即单位文档向量），令查询为单位向量 $u \in \mathbb{R}^d$。【脚注 3】固定 $\gamma > 0$。一个 $k$-子集 $S \subseteq [n]$ 以间隔 $\gamma$ 被实现，如果存在单位查询 $u_S$，使得

$$
\min_{i \in S} \langle u_S, v_i \rangle \geq \max_{j \notin S} \langle u_S, v_j \rangle + 2\gamma. \tag{1}
$$

由于对单位向量有 $\langle u, v_i \rangle \in [-1, 1]$，任何分数间隙至多为 $2$，因此式 (1) 仅当 $0 < \gamma \leq 1$ 时可行。全文中 $\log$ 表示自然对数。

**定理 1（维度下界）。** 假设 $1 \leq k < n$，并且每个 $k$-子集 $S \subseteq [n]$ 都像式 (1) 那样以间隔 $\gamma$ 被实现。则

$$
\binom{n}{k} \leq \left(1 + \frac{1}{\gamma}\right)^{d}, \quad \text{因而} \quad d \geq \frac{\log \binom{n}{k}}{\log\left(1 + 1/\gamma\right)}. \tag{2}
$$

**证明。** 固定两个不同的 $k$-子集 $S \neq T$，并选取 $i \in S \setminus T$ 与 $j \in T \setminus S$。把式 (1) 分别用于 $S$ 和 $T$，得到

$$
\langle u_S, v_i - v_j \rangle \geq 2\gamma, \qquad \langle u_T, v_j - v_i \rangle \geq 2\gamma.
$$

相加得到 $\langle u_S - u_T, v_i - v_j \rangle \geq 4\gamma$。由 Cauchy–Schwarz，以及对任意单位向量普遍成立的

$$
\|v_i - v_j\| \leq \|v_i\| + \|v_j\| = 2,
$$

我们得到 $\|u_S - u_T\| \geq 2\gamma$。因此，$M = \binom{n}{k}$ 个单位查询 $\{u_S\}$ 两两 $2\gamma$-分离，所以开球 $B(u_S, \gamma)$ 互不相交。此外，由于 $\|u_S\| = 1$，每个

$$
B(u_S, \gamma) \subseteq B(0, 1 + \gamma),
$$

因而

$$
M \cdot \mathrm{vol}\, B_d(\gamma) \leq \mathrm{vol}\, B_d(1 + \gamma).
$$

利用 $\mathrm{vol}(B_d(r)) = C_d r^d$，其中常数 $C_d$ 只依赖于 $d$（会消去），我们得到 $M \gamma^d \leq (1 + \gamma)^d$，即

$$
\binom{n}{k} \leq \left(\frac{1+\gamma}{\gamma}\right)^d = \left(1 + \frac{1}{\gamma}\right)^d.
$$

整理即得式 (2)。

表 1：由定理 1 在 $\gamma = 0.1$ 时给出的嵌入维度下界。当 $n$ 与 $k$ 都是 1000 时，结果是 trivial，因为 $\binom{1000}{1000} = 1$，只有一个 $k$-子集，因而没有要分开的“不相关”项。我们看到，对于较大的 $k$ 和 $n$，这些维度要求已经大于当前网页规模搜索所使用的维度。如果由于梯度学习约束或其他基于 LM 的约束（例如分词、泛化），这些数字被一个小的倍数放大，这些界就会落在任何合理的嵌入维度之外。

| 语料规模 $n$ | $k = 2$ | $k = 10$ | $k = 100$ | $k = 1000$ |
| --- | ---: | ---: | ---: | ---: |
| $10^{2}$ | 4 | 13 | trivial | — |
| $10^{3}$ | 6 | 23 | 135 | trivial |
| $10^{4}$ | 8 | 33 | 233 | 1354 |
| $10^{5}$ | 10 | 42 | 329 | 2334 |
| $10^{6}$ | 12 | 52 | 425 | 3296 |
| $10^{7}$ | 14 | 61 | 521 | 4257 |
| $10^{8}$ | 16 | 71 | 617 | 5217 |
| $10^{9}$ | 17 | 81 | 713 | 6177 |
| $10^{10}$ | 19 | 90 | 809 | 7137 |
| $10^{11}$ | 21 | 100 | 905 | 8098 |

【脚注 3】为简便起见，因为几乎所有最先进检索模型都使用单位向量。

<!-- 原 PDF 第 5 页 -->

### 3.0.1 推论

**数值实例。** 我们可以用 $\gamma = 0.1$（分数间隙 $2\gamma = 0.2$）来说明这一下界的效果，按经验使用情况，这对基于模型的系统大致是标准的。于是式 (2) 变成

$$
d \geq \frac{\log \binom{n}{k}}{\log 11},
$$

各种 $k$ 与 $n$ 的数值见表 1。

当 $n \gg k$ 时，$\log \binom{n}{k} \approx k \log(en/k)$，因此式 (2) 迫使

$$
d = \Omega\left(\frac{k \log(en/k)}{\log(1 + 1/\gamma)}\right).
$$

更严格的间隔要求（更大的 $\gamma$）需要更高的维度，因为 $\log(1 + 1/\gamma)$ 随 $\gamma$ 减小（可行性要求 $\gamma \leq 1$，所以分母至少是 $\log 2$）。

**后果。** 由于空间与速度的要求，用于网页规模搜索的大多数嵌入会被量化或截断（例如通过 Matryoshka 嵌入（Kusupati et al., 2022））到小于 1k 维，而研究中使用的最大嵌入大约是 4096（Zhang et al., 2025）。我们看到，即便间隔只是中等——而处理来自杂乱数据或量化的噪声需要这样的间隔——表 1 中的下界已经可以大于实践中所使用的维度。

现实模型上的额外约束（例如需要泛化、从梯度下降中学习，以及使用自然语言和分词）会使实践中所需的维度高得多。如表 1 所示，即便只是这一下界的一个小倍数，也会使嵌入维度要求变得不可行。这个倍数看起来是有根据的，我们将在下一节从最佳情形的优化设定（例如自由嵌入）中加以展示。

## 4 经验联系：最佳情形优化

在基于嵌入维度 $d$ 建立了嵌入模型的理论局限之后，我们希望表明它在经验上也成立。

为了展示可能达到的最强优化情形，我们设计实验，使向量本身可以直接用梯度下降优化。【脚注 4】我们称之为“自由嵌入”（free embedding）优化，因为嵌入可以自由优化，不受自然语言约束；而自然语言会给任何现实的嵌入模型施加约束。因此，这展示的是：对任何嵌入模型而言，解决这个问题是否可行。如果自由嵌入优化都解不了，真实的检索模型也解不了。还值得注意的是，我们通过对目标 qrel 矩阵（测试集）直接优化嵌入来做到这一点。这不会泛化到新数据集，而是为了展示可能出现的最高性能。

**实验设定。** 我们创建一个随机文档矩阵（规模为 $n$）和一个随机查询矩阵，查询的 top-k 集合取全部组合，即规模 $m = \binom{n}{k}$，二者都是单位向量。然后我们用 Adam 优化器（Kingma & Ba, 2014）直接优化以求解这些约束。【脚注 5】每次梯度更新都是对全部正确三元组的一次完整遍历（即整个数据集作为一个 batch），损失函数为 InfoNCE（Oord et al., 2018），【脚注 6】并把所有其他文档作为 batch 内负例（即整个数据集都在 batch 中）。由于几乎所有嵌入模型都使用归一化向量，我们也这样做（通过投影梯度下降）。当损失连续 1000 次迭代没有改进时，我们提前停止。我们逐步增加文档数量（从而二项式数量的查询也增加），直到优化不再能够解决问题（即达到 100% 准确率）。我们把这一点称为 critical-$n$ 点。

我们关注相对较小的 $n$、$k$ 和 $d$，因为文档数变大时组合会爆炸（例如 5 万篇文档、top-k 为 100，会给出 $7.7\times 10^{311}$ 种组合，这等价于该自由嵌入实验中维度为 $d$ 的查询向量的数量）。

【脚注 4】这也可以看成一种嵌入模型：每个查询/文档通过查表对应一个单独的向量。

【脚注 5】我们用 SGD 得到了相似结果，但使用 Adam 是为了速度，并与现有训练方法保持一致。

【脚注 6】在预备实验中，我们发现 InfoNCE 表现最好，优于 MSE 和 Margin。由于我们用全数据集 batch 直接优化向量，损失为

$$
L_{\mathrm{total}} = -\frac{1}{M}\sum_{i=1}^{M}\log\frac{\sum_{d_r \in R_i}\exp(\mathrm{sim}(q_i, d_r)/\tau)}{\sum_{d_k \in D}\exp(\mathrm{sim}(q_i, d_k)/\tau)},
$$

其中 $D$ 是全部文档，$d_r$ 是查询 $q_i$ 的相关文档，$d_k$ 是不相关文档。关于 sigmoid 学习函数的实验（例如 Bangachev et al. (2025)），见附录 C。

<!-- 原 PDF 第 6 页 -->

我们使用 $k = 2$，并对每个 $d$ 把 $n$ 每次增加 1，直到它失败。我们对数据拟合一条多项式回归线，以便建模并向外外推结果。

**结果。** 图 2 表明曲线拟合一条三次多项式，公式为

$$
y = -10.5322 + 4.0309d + 0.0520d^{2} + 0.0037d^{3}
$$

（$r^{2} = 0.999$）。把这条曲线向外外推，得到临界 $n$（对应嵌入规模）：512 维为 50 万，768 维为 170 万，1024 维为 400 万，3072 维为 1.07 亿，4096 维为 2.5 亿。我们指出这是最佳情形：真实的嵌入模型不能直接优化查询向量和文档向量去匹配测试 qrel 矩阵（并且受到诸如“对自然语言建模”等因素的约束）。

**图 2 见原 PDF。** 图中为 critical-$n$ 随维度 $d$ 变化的散点及三次回归曲线（Regression (Degree 3)），横轴 $d$ 约从 10 到 40，纵轴 Critical $n$ 约从 0 到 600。

图 2：维度太小、从而无法成功表示全部 top-2 组合时的 critical-$n$ 值。我们将趋势线画成多项式函数。

结果还表明，上一节中的下界严重低估了真实性能：表 1 对 $n = 100$ 给出的下界是 4，而我们看到自由嵌入需要 $d > 18$（即便在没有泛化、也没有自然语言的情形下，也有 4.5 倍的乘数）。总体而言，这些数字已经表明：对于网页规模搜索，即便最大的嵌入维度加上理想的测试集优化，也不足以对全部组合建模。

## 5 经验联系：现实世界数据集

自由嵌入实验为理论结果确实成立提供了经验证据。然而它们仍然是抽象的——这对真实的嵌入模型意味着什么？在本节中，我们（1）把这一理论与现有数据集联系起来，并（2）为现有最先进模型构造一个平凡简单、却极其困难的检索任务。

### 5.1 与现有数据集的联系

现有检索数据集通常使用静态评测集，查询数量有限，因为对每个查询做相关性标注都很昂贵。这意味着，实践上用于评测的查询空间只是潜在查询数量的一个非常小的样本。例如，QUEST 数据集（Malaviya et al., 2023）有 32.5 万篇文档，每个查询 20 篇相关文档，查询总数为 3357。用 QUEST 语料能够返回的唯一 top-20 文档集合的数量是 $\binom{325000}{20}$，等于 $7.1\times 10^{91}$（大于可观测宇宙中原子数的估计 $10^{82}$）。因此，QUEST 中的约 3 千条查询只能覆盖 qrel 组合空间中无穷小的一部分。

尽管在使用大规模语料时不可能实例化全部组合，搜索评测数据集是“任何用户会问什么”的一个代理，并且理想情况下应当被设计成测试许多组合，因为用户会这么做。在许多情况下，新评测的开发者只是因为成本或评测的计算开销而选择使用更少的查询。例如，QUEST 的查询 “Novels from 1849 or George Sand novels” 用 “OR” 算子把两类小说组合起来——人们可以实例化新查询，通过把其他类别做 OR 来关联概念。类似地，随着搜索智能体的兴起，我们看到超具体查询的使用更多：BrowseComp（Wei et al., 2025）每个查询有 5 个以上的条件，包括范围算子。有了这些工具，如果文档足够有表达力（即非平凡），就有可能用合适的算子子选出任意相关集合。因此，现有数据集只实例化其中一些组合，主要是出于实际原因，而不是因为这些组合不存在。

与这些先前工作相对，我们试图构建一个数据集，对少量文档评测全部 top-k 集合组合。我们不使用 QUEST、BrowseComp 等已经因为 qrel 矩阵之外的原因而困难的查询算子，而是选择非常简单的查询和文档，以突出表示全部 top-k 集合本身的难度。

<!-- 原 PDF 第 7 页 -->

**图 3 见原 PDF。** 横轴为嵌入维度（32、512、1024、2048、3072、4096），三个子图分别为 Recall@2、Recall@10、Recall@100。图例包括 E5-Mistral 7B、GritLM 7B、Qwen3 Embed、BM25、Snowflake Arctic L、Promptriever Llama3 8B、Gemini Embed、GTE-ModernColBERT。星号表示用 MRL 训练的模型。数值表见后文表 5。

图 3：LIMIT 任务上的分数。尽管任务简单，我们看到最先进模型仍然吃力。我们还看到模型维度是一个限制因素，维度增加时性能也随之提高。即便多向量模型也很吃力。BM25 这类词法模型由于其更高的维度而表现很好。星号表示用 MRL 训练的模型。

### 5.2 LIMIT 数据集

**数据集构造。** 为了得到该数据集的自然语言版本，我们需要某种办法，把文档组合映射成可以用查询检索的东西。一种简单做法【脚注 7】是：为查询和文档创建带潜变量的合成版本，再用自然语言把它实例化。对于这一映射，我们选择使用一个人可能喜欢的属性（即 Jon likes Hawaiian pizza, sports cars, etc.），因为它们数量充足，并且不会相对其他项目产生问题：一个人可以喜欢 Hawaiian pizza 而不喜欢 pepperoni，所有偏好都是合法的。然后我们为了真实性施加两条约束：（1）用户不应有太多属性，从而保持文档较短（每个用户少于 50 个）；（2）每个查询只询问一个项目，以保持任务简单（即 “who likes X”）。我们通过提示 Gemini 2.5 Pro 收集一个人可能喜欢的属性列表。然后我们把它清洗到最终 1850 个项目：迭代地要求它去掉重复项/上位词，同时用 BM25 检查失败最多的情况，以确保没有重叠。

我们选择使用 5 万篇文档，以便得到一个困难但相对较小的语料，并使用 1000 条查询，以在保持统计显著性的同时仍然评测得很快。对每个查询，我们选择使用两篇相关文档（即 $k=2$），既是为了实例化的简单，也是为了与先前工作一致（即 NQ、HotpotQA 等（Kwiatkowski et al., 2019; Yang et al., 2018））。

最后一步是选择一个 qrel 矩阵来实例化这些属性。尽管我们不能用理论确定地证明最难的 qrel 矩阵，我们直觉上认为理论结果意味着：qrel 矩阵越相互连接（例如稠密地包含全部组合），模型就越难表示。据此，我们使用文档数最多、且全部组合刚刚超过 1000 条查询的那个 qrel 矩阵，top-k 为 2（46 篇文档，因为 $\binom{46}{2} = 1035$，是大于 1k 的最小者）。

然后我们把随机的自然语言属性分配给查询，并把这些属性加到各自的相关文档上（参见图 1）。我们从开源姓名列表中给每篇文档一个随机的名和姓。最后，我们为每篇文档随机抽样新属性，直到所有文档的属性数量相同。由于这一设定中，与任何查询都不相关的文档远多于相关文档（46 篇与某个查询相关，4.995 万篇与任何查询都不相关），我们也创建一个“小”版本，只包含与 1000 条查询之一相关的那 46 篇文档。

**模型。** 我们评测当前最先进的嵌入模型，包括 GritLM（Muennighoff et al., 2024）、Qwen 3 Embeddings（Zhang et al., 2025）、Promptriever（Weller et al., 2024b）、Gemini Embeddings（Lee et al., 2025）、Snowflake 的 Arctic Embed Large v2.0（Yu et al., 2024），以及 E5-

【脚注 7】这只是一种方式，设计成现实且简单。然而我们的框架允许任何实例化方式，并不绑死在这种任意的自然语言设计上。

<!-- 原 PDF 第 8 页 -->

**图 4 见原 PDF。** 横轴为嵌入维度，三个子图为 Recall@2、Recall@10、Recall@20，语料为 LIMIT small（$N=46$）。图例与图 3 相同。数值表见后文表 4。

图 4：LIMIT 小任务（$N=46$）上随嵌入维度变化的分数。尽管只有 46 篇文档，模型即便在 Recall@10 上也很吃力，并且即便用 Recall@20 也无法解决该任务。

Mistral Instruct（Wang et al., 2022; 2023）。这些模型的嵌入维度从 1024 到 4096 不等，训练风格也不同（基于指令、硬负例优化等）。我们还评测三个非单向量模型以显示区别：BM25（Robertson et al., 1995; Lù, 2024）、gte-ModernColBERT（Chaffin, 2025a; Chaffin & Sourty, 2024），以及一个按词元的 TF-IDF。【脚注 8】

我们展示完整嵌入维度上的结果，也展示截断嵌入维度上的结果（通常与 Matryoshka 学习，即 MRL（Kusupati et al., 2022）一起使用）。对没有用 MRL 训练的模型，这会导致偏低的分数，因此用 MRL 训练的模型在图中用星号标出。然而，由于没有嵌入维度小于 384 的 LLM，我们对所有模型都包含到小维度（32）的 MRL，以展示嵌入维度的影响。

**结果。** 图 3 给出完整 LIMIT 上的结果，图 4 给出小版本（46 篇文档）上的结果。结果令人惊讶：尽管任务平凡地简单，模型仍然严重吃力。例如，在完整设定中，模型甚至难以达到 20% 的 Recall@100；在 46 篇文档的版本中，模型即便用 Recall@20 也无法解决该任务。

我们看到模型性能关键地依赖于嵌入维度（维度越大性能越好）。有趣的是，用更多样指令训练的模型，例如 Promptriever，表现更好，也许是因为它们的训练允许它们使用更多的嵌入空间（相比之下，用 MRL 训练、并且任务范围更小的模型，也许可以被压缩进一个更小的嵌入流形）。

对于替代架构，GTE-ModernColBERT 显著好于单向量模型（尽管远未解决问题），而 BM25 接近满分。这两种替代架构（稀疏与多向量）各有权衡，分析见 §5.3。

**图 5 见原 PDF。** 横轴为嵌入维度（32、128、256、384、512、768、1024），纵轴为 Recall@2。两条曲线分别为在 Test 上训练和在 Train 上训练。数值表见后文表 3。

图 5：在 LIMIT 训练集上训练并没有显著帮助，表明问题不是领域偏移。但如果模型过拟合到测试集，就可以解决它。

**这是领域偏移吗？** 尽管我们的查询看起来与标准网页搜索查询相似，我们想知道低性能是否可能由某种领域偏移引起。如果是，我们会期望在相似例子的训练集上训练会显著提高性能。另一方面，如果任务本质上就难，那么在训练集上训练帮助很小，而在测试集上训练会让模型过拟合到那些词元（类似于自由嵌入）。

为了检验这一点，我们取一个现成的嵌入模型，在训练集（用非测试集属性合成得到）或 LIMIT 的官方测试集上训练它。我们使用 lightonai/modernbert-embed-large（Chaffin, 2025c），并在这些划分上微调，使

【脚注 8】该模型把每个唯一项目变成一个词元，然后做 TF-IDF。我们构建它是为了表明它在所有任务上得到 100%（因为它逆向了我们的数据集构造），因此我们不把它放进后续图表。

<!-- 原 PDF 第 9 页 -->

**图 6 见原 PDF。** 比较 LIMIT small 与 LIMIT small（同义词）上的 Recall@2。横轴模型为 BM25、GTE-ColBERT、Promptriever 8B、GritLM 7B、E5-Mistral 7B、Snowflake Arctic、Qwen3 Embed。图中可见的柱高标签包括 97.8、83.5、54.3、38.4、29.5、19.4、19.0，以及同义词版本上更低的一组标签（如 25.6、15.1、14.3、12.8、11.6、10.6、8.5）。柱与系列的精确对应以原 PDF 为准，此处不另排成表，以免把未对齐的标签配错模型。

图 6：比较 LIMIT small 与 LIMIT small（同义词）上的分数。使用同义词使任务更难，因此所有模型都变差。然而词法模型 BM25 下降近 90%，在 LIMIT 的同义词版本上比大多数单向量模型更差。因此词法模型有其自身的弱点（更多讨论见第 5.3 节），并非万灵药。

用 SentenceTransformers（Reimers & Gurevych, 2019），并以整个数据集作为 batch 内负例（排除正例）。我们通过在训练时把隐藏层投影到指定大小来展示一系列维度（而不是使用 MRL）。

图 5 表明，在训练集上训练的模型无法解决问题，尽管它确实看到了非常小的改进：Recall@10 从接近 0 提高到至多 2.8。领域内训练时性能没有提升，表明差的性能不是由于领域偏移。通过在测试集上训练模型，我们看到它可以学会该任务，过拟合到测试查询中的词元。这与我们的自由嵌入结果一致：只用 12 维就有可能过拟合到 $N = 46$ 的版本。然而值得注意的是，64 维的真实模型仍然不能完全解决该任务，这意味着真实模型显著差于 §4 中所示的界。

**非词法匹配又如何？** 我们先前的结果表明词法模型大大优于其神经对应物。然而，这并不是说词法模型是万灵药——尽管它们的维度高于单向量模型，它们有其他短处。我们通过创建一个 LIMIT-small 版本来说明这一点：把语料中的所有项目替换成它们的同义词，从而减少词法重叠。我们让 Gemini 2.5 Pro 想出同义词，这些同义词不与任何其他已有同义词或原始项目匹配，办法是使用学名、相近含义，或在必要时使用上位词。这产生诸如 “glasses” 到 “spectacles” 之类的映射。【脚注 9】

我们在 LIMIT-small（同义词）上重复先前实验，并在图 6 中与 LIMIT-small 比较。我们发现，由于任务现在更难，所有模型的性能都下降，但 BM25 下降最多，并且现在不如神经模型（例如 BM25 下降超过 89%，而 Qwen3 embedding 下降 38.9%）。因此我们可以看到，尽管词法模型有更高维度这样的优点，它们受限于只能做关键词匹配。我们在第 5.3 节进一步展开它们在指令遵循方面的长处与短处。

**含义。** 单向量模型从根本上受其嵌入维度限制。LIMIT 数据集是一个特定实例，查询和文档都非常简单，目的是突出这一性质。LIMIT 的这个小版本只需 12 维就可以嵌入（如自由嵌入实验所见），然而所有模型都表现不好，这暗示还有其他架构弱点。不过，无论涉及何种架构，我们的框架都可以扩展数据集的难度，以持续展示这一根本局限。

### 5.3 嵌入模型的替代方案

我们先前的结果从理论上和经验上都表明，嵌入模型不能在其 top-k 集合中表示文档的全部组合，因而无法表示并解决某些检索任务。随着当前嵌入模型变大（例如直到 4096），这对较小的数据集规模有助于减轻负面影响。然而，只要 top-k 集合的组合足够多，维度就不得不增加到对非玩具数据集不可行的规模。因此，尽管它们对第一阶段结果有用，仍需要表达能力更强的检索器架构。

**交叉编码器。** 尽管它们不适合大规模的第一阶段检索，它们通常已经被用来改进第一阶段结果。LIMIT 对重排器也有挑战吗？作为比较，我们在小设定上评测一个长上下文重排器 Gemini-2.5-Pro（Comanici et al., 2025）。我们一次把全部 46 篇文档和全部 1000 条查询给 Gemini，要求它用一次生成输出每个查询的相关文档。我们发现，它可以在一次前向传播中成功解决全部 1000 条查询（100%）。这与即便最好的嵌入模型 Recall@2 仍低于

【脚注 9】我们指出，它并没有去掉全部词法重叠，因为存在诸如 “Scuba Diving” → “Underwater Diving” 这样的项目。

<!-- 原 PDF 第 10 页 -->

60%（图 4）形成对照。因此我们可以看到，LIMIT 对当前最先进的重排模型是容易的，它们没有基于嵌入维度的同样局限。

**多向量模型。** 多向量模型通过每个序列使用多个向量，并结合 MaxSim 算子（Khattab & Zaharia, 2020），表达能力更强。这些模型在 LIMIT 数据集上显示出前景，分数大大高于单向量模型，尽管使用了更小的骨干（ModernBERT，Warner et al. (2024)）。然而，这些模型通常不用于指令遵循或基于推理的任务（Chaffin (2025b) 是少数存在的例子之一），因此多向量技术能在多大程度上迁移到这些任务仍是一个开放问题。

**稀疏模型。** 稀疏模型（词法的和神经的）可以被看成单向量，但维度非常高。这一维度帮助 BM25 避开神经嵌入模型的问题，如图 3 所示。由于它们向量的 $d$ 很高，它们可以扩展到比稠密向量对应物多得多的组合。然而，如何把稀疏模型应用到没有词法重叠、甚至没有释义式重叠的指令遵循和基于推理的任务上，则不那么清楚。我们把这个方向（以及稀疏/稠密混合方案）留给未来工作。

我们指出，所有这些选项都有各种权衡，没有一个按现状提供解决该问题的清晰路径。我们留给未来工作去发展新技术以缓解这些问题：也许通过这些替代类别之一，或者通过关于单向量模型的新想法，以解决底层问题（可能通过诸如超编码器（hyperencoders，Killingback et al., 2025）之类的技术，或其他尚未发展出来的单向量架构上的未来工作）。

## 6 结论

我们引入 LIMIT 数据集，它突出了嵌入模型的一个根本局限。我们提供一个理论联系，表明：对于固定的嵌入维度，会存在某个文档集合，使得某些集合无法作为 top-k 集合被达到。我们表明这些理论结果在经验上成立：通过对向量本身做最佳情形优化，并通过创造理论的一个现实且简单的实例 LIMIT，把它与现有最先进模型做实际联系，而这些模型无法解决 LIMIT。我们的结果意味着，社区应当重新考虑基于指令的检索将如何影响未来的检索器。

## 局限性

尽管我们的实验为最常见的嵌入模型类型（单向量）提供了理论洞见，它们并不必然对其他架构成立，例如多向量模型。尽管我们展示了非单向量模型的初步经验结果，我们把把理论联系扩展到这些设定留给未来工作。我们也没有对用户允许一些错误的设定给出理论结果，例如只捕获大多数组合。我们把给这一情形加界留给未来工作，并邀请读者查看 Ben-David et al. (2002) 之类的工作。

我们已经展示了证明某些组合不能被嵌入模型表示的理论联系，然而我们不能先验地证明它们会在哪些类型的组合上失败。因此，有可能存在一些它们可以完美解决的指令遵循或推理任务；然而，我们知道存在一些它们永远无法解决的任务。

## 致谢

我们感谢 Tanmaya Dabral、Zhongli Ding、Anthony Chen、Ming-Wei Chang、Kenton Lee 和 Kristina Toutanova 的有益反馈。我们感谢 Kiril Bangachev、Guy Bresler、Iliyas Noman、Yury Polyanskiy、Antonio Vergari、Adam Lopez 和 Andreas Grivas 指出关于符号秩的工作。

## 参考文献

Noga Alon, Peter Frankl, and Vojtech Rodl. 集合系统的几何实现与概率通信复杂度. In 26th Annual Symposium on Foundations of Computer Science (sfcs 1985), pp. 277–280. IEEE, 1985.

<!-- 原 PDF 第 11 页 -->

Samy Badreddine, Emile van Krieken, and Luciano Serafini. 打破知识图谱嵌入中的秩瓶颈. arXiv preprint arXiv:2506.22271, 2025.

Kiril Bangachev, Guy Bresler, Iliyas Noman, and Yury Polyanskiy. Sigmoid 对比损失的全局最小化解. arXiv preprint arXiv:2509.18552, 2025.

Peter L Bartlett. 神经网络模式分类的样本复杂度：权重大小比网络规模更重要. IEEE transactions on Information Theory, 44(2):525–536, 2002.

Parishad BehnamGhader, Vaibhav Adlakha, Marius Mosbach, Dzmitry Bahdanau, Nicolas Chapados, and Siva Reddy. LLM2Vec：大语言模型其实是强大的文本编码器. arXiv preprint arXiv:2404.05961, 2024.

Shai Ben-David, Nadav Eiron, and Hans Ulrich Simon. 通过欧几里得半空间中的嵌入进行学习的局限性. Journal of Machine Learning Research, 3(Nov):441–461, 2002.

Cecilia Bohler, Panagiotis Cheilaris, Rolf Klein, Chih-Hung Liu, Evanthia Papadopoulou, and Maksym Zavershynskyi. 高阶抽象 Voronoi 图的复杂度. Computational Geometry, 48(8):539–551, 2015. ISSN 0925-7721. doi: https://doi.org/10.1016/j.comgeo.2015.04.008. URL https://www.sciencedirect.com/science/article/pii/S0925772115000346.

Antoine Chaffin. GTE-ModernColBERT, 2025a. URL https://huggingface.co/lightonai/GTE-ModernColBERT-v1.

Antoine Chaffin. Reason-ModernColBERT, 2025b. URL https://huggingface.co/lightonai/Reason-ModernColBERT.

Antoine Chaffin. ModernBERT-embed-large, 2025c. URL https://huggingface.co/lightonai/modernbert-embed-large.

Antoine Chaffin and Raphaël Sourty. PyLate：面向后期交互模型的灵活训练与检索, 2024. URL https://github.com/lightonai/pylate.

Bi Yu Chen, Huihuang Huang, Hui-Ping Chen, Wenxuan Liu, Xuan-Yan Chen, and Tao Jia. 道路网络中构造 $k$ 阶 Voronoi 图的高效算法. ISPRS International Journal of Geo-Information, 12(4):172, 2023.

Kenneth L Clarkson. 随机抽样在计算几何中的应用（二）. In Proceedings of the fourth annual symposium on Computational geometry, pp. 1–11, 1988.

Gheorghe Comanici, Eric Bieber, Mike Schaekermann, Ice Pasupat, Noveen Sachdeva, Inderjit Dhillon, Marcel Blistein, Ori Ram, Dan Zhang, Evan Rosen, et al. Gemini 2.5：以高级推理、多模态、长上下文与下一代智能体能力推动前沿. arXiv preprint arXiv:2507.06261, 2025.

John H Conway, Chaim Goodman-Strauss, and N Sloane. 球体填充的最新进展. Current Developments in Mathematics, 1999(1):37–76, 1999.

Nick Craswell, Bhaskar Mitra, Emine Yilmaz, Daniel Campos, and Ellen M Voorhees. TREC 2019 深度学习赛道综述. arXiv preprint arXiv:2003.07820, 2020.

Kenneth Enevoldsen, Isaac Chung, Imene Kerboua, Márton Kardos, Ashwin Mathur, David Stap, Jay Gala, Wissam Siblini, Dominik Krzemiński, Genta Indra Winata, et al. MMTEB：大规模多语言文本嵌入基准. arXiv preprint arXiv:2502.13595, 2025.

Manuel Faysse, Hugues Sibille, Tony Wu, Bilel Omrani, Gautier Viaud, Céline Hudelot, and Pierre Colombo. ColPali：利用视觉语言模型进行高效文档检索. arXiv preprint arXiv:2407.01449, 2024.

Andreas Grivas, Antonio Vergari, and Adam Lopez. 驯服 sigmoid 瓶颈：可证明能够取 argmax 的稀疏多标签分类. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 38, pp. 12208–12216, 2024.

<!-- 原 PDF 第 12 页 -->

Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor Cai, Eliza Rutherford, Diego de Las Casas, Lisa Anne Hendricks, Johannes Welbl, Aidan Clark, et al. 训练计算最优的大语言模型. arXiv preprint arXiv:2203.15556, 2022.

Gautier Izacard, Mathilde Caron, Lucas Hosseini, Sebastian Riedel, Piotr Bojanowski, Armand Joulin, and Edouard Grave. 基于对比学习的无监督稠密信息检索. arXiv preprint arXiv:2112.09118, 2021.

William B Johnson, Joram Lindenstrauss, et al. Lipschitz 映射到 Hilbert 空间的扩张. Contemporary mathematics, 26(189-206):1, 1984.

Michael J Kearns and Robert E Schapire. 概率概念的高效无分布学习. Journal of Computer and System Sciences, 48(3):464–497, 1994.

Omar Khattab and Matei Zaharia. ColBERT：通过 BERT 上的上下文化后期交互实现高效而有效的段落检索. In Proceedings of the 43rd International ACM SIGIR conference on research and development in Information Retrieval, pp. 39–48, 2020.

Julian Killingback, Hansi Zeng, and Hamed Zamani. Hypencoder：用于信息检索的超网络. In Proceedings of the 48th International ACM SIGIR Conference on Research and Development in Information Retrieval, pp. 2372–2383, 2025.

Diederik P Kingma and Jimmy Ba. Adam：一种随机优化方法. arXiv preprint arXiv:1412.6980, 2014.

Aditya Kusupati, Gantavya Bhatt, Aniket Rege, Matthew Wallingford, Aditya Sinha, Vivek Ramanujan, William Howard-Snyder, Kaifeng Chen, Sham Kakade, Prateek Jain, et al. Matryoshka 表示学习. Advances in Neural Information Processing Systems, 35:30233–30249, 2022.

Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh, Chris Alberti, Danielle Epstein, Illia Polosukhin, Jacob Devlin, Kenton Lee, et al. Natural Questions：问答研究的一个基准. Transactions of the Association for Computational Linguistics, 7:453–466, 2019.

Der-Tsai Lee. 平面上的 $k$ 近邻 Voronoi 图. IEEE transactions on computers, 100(6):478–487, 1982.

Jinhyuk Lee, Zhuyun Dai, Xiaoqi Ren, Blair Chen, Daniel Cer, Jeremy R Cole, Kai Hui, Michael Boratko, Rajvi Kapadia, Wen Ding, et al. Gecko：从大语言模型蒸馏出的通用文本嵌入. arXiv preprint arXiv:2403.20327, 2024.

Jinhyuk Lee, Feiyang Chen, Sahil Dua, Daniel Cer, Madhuri Shanbhogue, Iftekhar Naim, Gustavo Hernández Ábrego, Zhe Li, Kaifeng Chen, Henrique Schechter Vera, et al. Gemini Embedding：来自 Gemini 的可泛化嵌入. arXiv preprint arXiv:2503.07891, 2025.

Kenton Lee, Ming-Wei Chang, and Kristina Toutanova. 面向弱监督开放域问答的潜在检索. In Anna Korhonen, David Traum, and Lluís Màrquez (eds.), Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics, pp. 6086–6096, Florence, Italy, July 2019. Association for Computational Linguistics. doi: 10.18653/v1/P19-1612. URL https://aclanthology.org/P19-1612/.

Chunyuan Li, Zhe Gan, Zhengyuan Yang, Jianwei Yang, Linjie Li, Lijuan Wang, Jianfeng Gao, et al. 多模态基础模型：从专用模型到通用助手. Foundations and Trends® in Computer Graphics and Vision, 16(1-2):1–214, 2024.

Xing Han Lù. BM25S：通过急切稀疏打分实现数量级更快的词法检索. arXiv preprint arXiv:2407.03618, 2024.

Xueguang Ma, Sheng-Chieh Lin, Minghan Li, Wenhu Chen, and Jimmy Lin. 通过文档截图嵌入统一多模态检索. arXiv preprint arXiv:2406.11251, 2024.

<!-- 原 PDF 第 13 页 -->

Chaitanya Malaviya, Peter Shaw, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. QUEST：带隐式集合运算的实体寻求查询检索数据集. arXiv preprint arXiv:2305.11694, 2023.

Niklas Muennighoff, Nouamane Tazi, Loïc Magne, and Nils Reimers. MTEB：大规模文本嵌入基准. arXiv preprint arXiv:2210.07316, 2022.

Niklas Muennighoff, SU Hongjin, Liang Wang, Nan Yang, Furu Wei, Tao Yu, Amanpreet Singh, and Douwe Kiela. 生成式表示指令调优. In ICLR 2024 Workshop: How Far Are We From AGI, 2024.

Hanseok Oh, Hyunji Lee, Seonghyeon Ye, Haebin Shin, Hansol Jang, Changwook Jun, and Minjoon Seo. InstructIR：信息检索模型指令遵循的基准. arXiv preprint arXiv:2402.14334, 2024.

Aaron van den Oord, Yazhe Li, and Oriol Vinyals. 基于对比预测编码的表示学习. arXiv preprint arXiv:1807.03748, 2018.

Aitor Ormazabal, Mikel Artetxe, Gorka Labaka, Aitor Soroa, and Eneko Agirre. 分析跨语言词嵌入映射的局限性. arXiv preprint arXiv:1906.05407, 2019.

Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. 用人类反馈训练语言模型遵循指令. Advances in neural information processing systems, 35:27730–27744, 2022.

Christos H Papadimitriou and Michael Sipser. 通信复杂度. In Proceedings of the fourteenth annual ACM symposium on Theory of computing, pp. 196–200, 1982.

Rohan Paul, Haw-Shiuan Chang, and Andrew McCallum. 多侧面通用模式. In Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics: Main Volume, pp. 909–919, 2021.

Nils Reimers and Iryna Gurevych. Sentence-BERT：使用孪生 BERT 网络的句子嵌入. In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing. Association for Computational Linguistics, 11 2019. URL https://arxiv.org/abs/1908.10084.

Nils Reimers and Iryna Gurevych. 大规模索引下稠密低维信息检索的诅咒. arXiv preprint arXiv:2012.14210, 2020.

Stephen E Robertson, Steve Walker, Susan Jones, Micheline M Hancock-Beaulieu, Mike Gatford, et al. Okapi 在 TREC-3. Nist Special Publication Sp, 109:109, 1995.

Tingyu Song, Guo Gan, Mingsheng Shang, and Yilun Zhao. IFIR：评估专家领域信息检索中指令遵循的综合基准. arXiv preprint arXiv:2503.04644, 2025.

Hongjin Su, Weijia Shi, Jungo Kasai, Yizhong Wang, Yushi Hu, Mari Ostendorf, Wen-tau Yih, Noah A Smith, Luke Zettlemoyer, and Tao Yu. 一个嵌入器，任意任务：指令微调的文本嵌入. arXiv preprint arXiv:2212.09741, 2022.

Hongjin Su, Howard Yen, Mengzhou Xia, Weijia Shi, Niklas Muennighoff, Han-yu Wang, Haisu Liu, Quan Shi, Zachary S Siegel, Michael Tang, et al. BRIGHT：面向推理密集型检索的真实且具有挑战性的基准. arXiv preprint arXiv:2407.12883, 2024.

Chameleon Team. Chameleon：混合模态早期融合基础模型. arXiv preprint arXiv:2405.09818, 2024.

Nandan Thakur, Nils Reimers, Andreas Rücklé, Abhishek Srivastava, and Iryna Gurevych. BEIR：用于信息检索模型零样本评测的异构基准. arXiv preprint arXiv:2104.08663, 2021.

<!-- 原 PDF 第 14 页 -->

Nandan Thakur, Jimmy Lin, Sam Havens, Michael Carbin, Omar Khattab, and Andrew Drozdov. FreshStack：为评测技术文档上的检索构建真实基准. arXiv preprint arXiv:2504.13128, 2025.

Vladimir Vapnik. 统计学习理论如今扮演着更积极的角色：在对学习过程做了一般分析之后，最优算法综合领域的研究开始了。然而这些研究还不属于历史。它们是当今研究活动的主题. PhD thesis，然而这些研究还不属于历史。它们是……的主题, 1998.

（说明：该条参考文献在 PDF 文本层中与一段重复的英文句子粘连，上面按抽出的文字翻译，未改写成其他版本的书目信息。）

Roman Vershynin. 高维概率：面向数据科学应用的导论, volume 47. Cambridge university press, 2018.

Georges Voronoi. 连续参数在二次型理论中的新应用。第二篇论文。关于本原平行多面体的研究. Journal für die reine und angewandte Mathematik (Crelles Journal), 1908(134):198–287, 1908.

David Wadden, Shanchuan Lin, Kyle Lo, Lucy Lu Wang, Madeleine van Zuylen, Arman Cohan, and Hannaneh Hajishirzi. 事实还是虚构：验证科学论断. arXiv preprint arXiv:2004.14974, 2020.

Liang Wang, Nan Yang, Xiaolong Huang, Binxing Jiao, Linjun Yang, Daxin Jiang, Rangan Majumder, and Furu Wei. 通过弱监督对比预训练得到的文本嵌入. arXiv preprint arXiv:2212.03533, 2022.

Liang Wang, Nan Yang, Xiaolong Huang, Linjun Yang, Rangan Majumder, and Furu Wei. 用大语言模型改进文本嵌入. arXiv preprint arXiv:2401.00368, 2023.

Benjamin Warner, Antoine Chaffin, Benjamin Clavié, Orion Weller, Oskar Hallström, Said Taghadouini, Alexis Gallagher, Raja Biswas, Faisal Ladhak, Tom Aarsen, et al. 更聪明、更好、更快、更长：一种面向快速、省内存与长上下文微调及推理的现代双向编码器. arXiv preprint arXiv:2412.13663, 2024.

Jason Wei, Zhiqing Sun, Spencer Papay, Scott McKinney, Jeffrey Han, Isa Fulford, Hyung Won Chung, Alex Tachard Passos, William Fedus, and Amelia Glaese. BrowseComp：面向浏览智能体的简单而具有挑战性的基准. arXiv preprint arXiv:2504.12516, 2025.

Orion Weller, Benjamin Chang, Sean MacAvaney, Kyle Lo, Arman Cohan, Benjamin Van Durme, Dawn Lawrie, and Luca Soldaini. FollowIR：评估并教导信息检索模型遵循指令. arXiv preprint arXiv:2403.15246, 2024a.

Orion Weller, Benjamin Van Durme, Dawn Lawrie, Ashwin Paranjape, Yuhao Zhang, and Jack Hessel. Promptriever：经指令训练的检索器可以像语言模型一样被提示. arXiv preprint arXiv:2409.11136, 2024b.

Orion Weller, Benjamin Chang, Eugene Yang, Mahsa Yarmohammadi, Sam Barham, Sean MacAvaney, Arman Cohan, Luca Soldaini, Benjamin Van Durme, and Dawn Lawrie. mFollowIR：检索中指令遵循的多语言基准. arXiv preprint arXiv:2501.19264, 2025a.

Orion Weller, Kathryn Ricci, Marc Marone, Antoine Chaffin, Dawn Lawrie, and Benjamin Van Durme. Seq vs Seq：一套开放的成对编码器与解码器. arXiv preprint arXiv:2507.11412, 2025b.

Orion Weller, Kathryn Ricci, Eugene Yang, Andrew Yates, Dawn Lawrie, and Benjamin Van Durme. Rank1：信息检索重排序中的测试时计算. arXiv preprint arXiv:2502.18418, 2025c.

Chenghao Xiao, G Thomas Hudson, and Noura Al Moubayed. RAR-b：把推理当作检索的基准. arXiv preprint arXiv:2404.06347, 2024.

Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W Cohen, Ruslan Salakhutdinov, and Christopher D Manning. HotpotQA：面向多样、可解释的多跳问答的数据集. arXiv preprint arXiv:1809.09600, 2018.

<!-- 原 PDF 第 15 页 -->

Zi Yin and Yuanyuan Shen. 论词嵌入的维度. Advances in neural information processing systems, 31, 2018.

Puxuan Yu, Luke Merrick, Gaurav Nuti, and Daniel Campos. Arctic-embed 2.0：不妥协的多语言检索. arXiv preprint arXiv:2412.04506, 2024.

Yanzhao Zhang, Mingxin Li, Dingkun Long, Xin Zhang, Huan Lin, Baosong Yang, Pengjun Xie, An Yang, Dayiheng Liu, Junyang Lin, Fei Huang, and Jingren Zhou. Qwen3 Embedding：借助基础模型推进文本嵌入与重排序. arXiv preprint arXiv:2506.05176, 2025.

Jeffrey Zhou, Tianjian Lu, Swaroop Mishra, Siddhartha Brahma, Sujoy Basu, Yi Luan, Denny Zhou, and Le Hou. 大语言模型的指令遵循评测. arXiv preprint arXiv:2311.07911, 2023.

Jianqun Zhou, Yuanlei Zheng, Wei Chen, Qianqian Zheng, Zeyuan Shang, Wei Zhang, Rui Meng, and Xiaoyu Shen. 超越内容相关性：评估检索模型中的指令遵循. ArXiv, abs/2410.23841, 2024. URL https://api.semanticscholar.org/CorpusID:273707185.

<!-- 原 PDF 第 16 页 -->

## 附录 A 与 $k$ 阶 Voronoi 区域的关系

我们也解释我们的结果如何与 Clarkson (1988) 比较，后者给出了 $k$ 阶 Voronoi 图中区域数量的界。$k$ 阶 Voronoi 图定义为：以 $S$ 中某一组 $n$ 个点作为其 $n$ 个最近邻的点的集合。这与检索对应得很好，因为每个 $k$ 阶区域等价于一个被检索出的 top-k 结果集合。于是 Voronoi 图中唯一区域的计数，就是对这些点可以被返回的组合总数。然而，对 $d > 3$ 构造经验性的 $k$ 阶 Voronoi 图在计算上不可行，并且在理论上也很难给出紧界。因此我们用另一种方法来展示嵌入模型的局限。

## 附录 B 超参数与计算细节

**推理。** 我们使用 MTEB 框架（Enevoldsen et al., 2025）评测模型时的默认长度设置。由于我们的文档相对较短（大约 100 个词元），这不会造成问题。

**训练。** 对于在 LIMIT 训练集和测试集上的训练，我们使用 SentenceTransformers 库（Reimers & Gurevych, 2019），损失为 MultipleNegativesRankingLoss。我们使用整个数据集作为 batch 大小，并采用 no duplicates sampler，以确保 batch 内负例不会与正例文档重复。学习率为 5e-5。我们训练 5 个 epoch，并把训练集略微限制到与测试集相同的规模（从 2.5k 条减到 2k 条，与测试集匹配）。

**计算。** LIMIT 的推理与训练在 Google Colab Pro 的 A100 GPU 上完成。自由嵌入实验主要在 H100 GPU 和 TPU v5 上完成，以便对更大的 $N$ 容纳全数据集 batch 向量优化所需的更高显存。

## 附录 C 自由嵌入的 sigmoid 损失函数

在 Bangachev et al. (2025) 的同期工作中，他们表明，对于更常用 sigmoid 损失函数的视觉—语言嵌入模型（如 CLIP），自由嵌入实验可以在比我们的设定更少的维度上被解决（假设没有间隔）。由于我们的结果发现 InfoNCE 性能最好，而 InfoNCE 试图制造尽可能宽的间隔，这表明围绕可学习性还有额外问题需要解决。我们欢迎对该问题的进一步理论与经验洞见，因为视觉—语言社区（其中 sigmoid 损失函数常常是最先进的）与纯文本社区（其中 sigmoid 损失函数由于性能更差而几乎从不使用）之间存在差异很大的实践。

这种 sigmoid 学习也与其他工作密切相关，例如 Grivas et al. (2024)，以及一般地与（Badreddine et al., 2025; Paul et al., 2021）这类主题上的工作相关。

## 附录 D 使用符号秩的证明

在本文的初始版本中，我们给出了一个不要求任何间隔、基于 qrel 矩阵符号秩的理论界。尽管证明是正确的，$\binom{n}{k}$ 矩阵的符号秩已在先前工作中建立（Alon et al., 1985），并且只依赖于 $k$。我们收入这个证明，它把与检索相关的概念和经典的符号秩概念联系起来；然而我们强调，由于它假设没有间隔，它对维度的要求更弱。

### D.1 形式化

我们考虑 $m$ 个查询和 $n$ 篇文档的集合，以及一个真实相关性矩阵 $A \in \{0, 1\}^{m \times n}$，其中 $A_{ij} = 1$ 当且仅当文档 $j$ 与查询 $i$ 相关。【脚注 10】向量嵌入模型把每个查询映射到向量 $u_i \in \mathbb{R}^d$，把每个文档映射到向量 $v_j \in \mathbb{R}^d$。相关性由点积 $u_i^{\top} v_j$ 建模，目标是相关文档的分数应当高于不相关文档。

【脚注 10】矩阵 $A$ 在信息检索中常被称为 “qrels”（query relevance judgments，查询相关性判定）矩阵。

<!-- 原 PDF 第 17 页 -->

把查询向量拼成矩阵 $U \in \mathbb{R}^{d \times m}$，把文档向量拼成矩阵 $V \in \mathbb{R}^{d \times n}$，这些点积就是分数矩阵 $B = U^{\top} V$ 的元素。能够实现给定分数矩阵的最小嵌入维度 $d$，按定义就是 $B$ 的秩。因此，我们的目标等价于：找到一个分数矩阵 $B$ 的最小秩，使其按照 $A$ 中指定的相关性正确排列文档。我们在如下定义中将其形式化。

**定义 1。** 给定矩阵 $A \in \mathbb{R}^{m \times n}$，$A$ 的按行保序秩是最小的整数 $d$，使得存在一个秩为 $d$ 的矩阵 $B$，保持 $A$ 每一行中元素的相对顺序。我们把它记为

$$
\mathrm{rank}_{\mathrm{rop}} A = \min\{\mathrm{rank}\, B \mid B \in \mathbb{R}^{m \times n},\ \text{使得对所有 } i, j, k,\ \text{若 } A_{ij} > A_{ik}\ \text{则 } B_{ij} > B_{ik}\}.
$$

换句话说，如果 $A$ 是二元真实相关性矩阵，$\mathrm{rank}_{\mathrm{rop}} A$ 就是任何向量嵌入模型为了在所有查询上都先返回相关文档、再返回不相关文档所必需的最小维度。或者，我们可能要求相关文档的分数能够被一个阈值与不相关文档的分数干净地分开。

**定义 2。** 给定二元矩阵 $A \in \{0, 1\}^{m \times n}$：

- $A$ 的按行可阈值化秩（$\mathrm{rank}_{\mathrm{rt}} A$）是矩阵 $B$ 的最小秩，使得存在按行的阈值 $\{\tau_i\}_{i=1}^{m}$，对所有 $i, j$，若 $A_{ij} = 1$ 则 $B_{ij} > \tau_i$，若 $A_{ij} = 0$ 则 $B_{ij} < \tau_i$。
- $A$ 的全局可阈值化秩（$\mathrm{rank}_{\mathrm{gt}} A$）是矩阵 $B$ 的最小秩，使得存在单一阈值 $\tau$，对所有 $i, j$，若 $A_{ij} = 1$ 则 $B_{ij} > \tau$，若 $A_{ij} = 0$ 则 $B_{ij} < \tau$。

**注记 1。** 这一双侧分离条件可以看成略强于“$B_{ij} > \tau_i$ 当且仅当 $A_{ij} = 1$”；然而由于 $B_{ij}$ 只有有限多个元素，我们总可以把后一种阈值扰动一个足够的量，使双侧条件成立。【脚注 11】

### D.2 理论界

对二元矩阵，按行排序与按行阈值化是等价的表示容量概念。

**命题 1。** 对二元矩阵 $A \in \{0, 1\}^{m \times n}$，我们有 $\mathrm{rank}_{\mathrm{rop}} A = \mathrm{rank}_{\mathrm{rt}} A$。

**证明。**（$\leq$）设 $B$ 与 $\tau$ 满足按行可阈值化秩条件。由于 $A$ 是二元矩阵，$A_{ij} > A_{ik}$ 意味着 $A_{ij} = 1$ 且 $A_{ik} = 0$，因此 $B_{ij} > \tau_i > B_{ik}$，因而 $B$ 也满足按行保序条件。

（$\geq$）设 $B$ 满足按行保序条件，于是 $A_{ij} > A_{ik}$ 意味着 $B_{ij} > B_{ik}$。对每一行 $i$，令 $U_i = \{B_{ij} \mid A_{ij} = 1\}$，$L_i = \{B_{ij} \mid A_{ij} = 0\}$。按行保序条件意味着 $U_i$ 的每个元素都大于 $L_i$ 的每个元素。因此我们总能找到一个把它们分开的阈值 $\tau_i$（例如当两者都非空时，$\tau_i = (\max L_i + \min U_i)/2$，否则是平凡的）。于是 $B$ 对 $A$ 也是按行可阈值化的。

到目前为止我们描述的概念与矩阵的符号秩密切相关，我们在论文其余部分用它来建立主要的界。

**定义 3（符号秩）。** 矩阵 $M \in \{-1, 1\}^{m \times n}$ 的符号秩是最小的整数 $d$，使得存在一个秩为 $d$ 的矩阵 $B$，其元素与 $M$ 的元素同号，即

$$
\mathrm{rank}_{\pm} M = \min\{\mathrm{rank}\, B \mid B \in \mathbb{R}^{m \times n},\ \text{使得对所有 } i, j\ \text{有 } \mathrm{sign}(B_{ij}) = M_{ij}\}.
$$

下文中，我们用 $\mathbf{1}_n$ 表示全 1 向量，用 $\mathbf{1}^{m \times n}$ 表示 $m \times n$ 的全 1 矩阵。

**命题 2。** 令 $A \in \{0, 1\}^{m \times n}$ 为二元矩阵。则 $2A - \mathbf{1}^{m \times n} \in \{-1, 1\}^{m \times n}$，并且

$$
\mathrm{rank}_{\pm}(2A - \mathbf{1}^{m \times n}) - 1 \leq \mathrm{rank}_{\mathrm{rop}} A = \mathrm{rank}_{\mathrm{rt}} A \leq \mathrm{rank}_{\mathrm{gt}} A \leq \mathrm{rank}_{\pm}(2A - \mathbf{1}^{m \times n}).
$$

【脚注 11】不失一般性，我们可以假设上述定义中的阈值不等于 $B$ 的任何元素，因为我们可以把阈值 $\tau$ 增加一个足够小的 $\epsilon$ 以保持不等式。

<!-- 原 PDF 第 18 页 -->

**证明。** 注意，等式已在命题 1 中证明。我们分别证明每个不等式。

1. $\mathrm{rank}_{\mathrm{rt}} A \leq \mathrm{rank}_{\mathrm{gt}} A$：由定义成立，因为任何满足全局可阈值化条件的矩阵，用每一行相同的阈值，平凡地满足按行可阈值化条件。

2. $\mathrm{rank}_{\mathrm{gt}} A \leq \mathrm{rank}_{\pm}(2A - \mathbf{1}^{m \times n})$：令 $B$ 为任意一个元素与 $2A - \mathbf{1}^{m \times n}$ 同号的矩阵，则

$$
B_{ij} > 0 \iff 2A_{ij} - 1 > 0 \iff A_{ij} = 1.
$$

因此 $B$ 以阈值 0 满足全局可阈值化条件。

3. $\mathrm{rank}_{\pm}(2A - \mathbf{1}^{m \times n}) - 1 \leq \mathrm{rank}_{\mathrm{rt}} A$：设 $B$ 以最小秩满足按行可阈值化条件，于是 $\mathrm{rank}_{\mathrm{rt}} A = \mathrm{rank}\, B$，并且存在 $\tau \in \mathbb{R}^{m}$，使得若 $A_{ij} = 1$ 则 $B_{ij} > \tau_i$，若 $A_{ij} = 0$ 则 $B_{ij} < \tau_i$。则 $B - \tau \mathbf{1}^{\top}$ 的元素与 $2A - \mathbf{1}^{m \times n}$ 同号，因为

$$
(B - \tau \mathbf{1}^{\top})_{ij} = B_{ij} - \tau_i,
$$

并且

$$
B_{ij} - \tau_i > 0 \iff A_{ij} = 1 \iff 2A_{ij} - 1 > 0, \tag{3}
$$

$$
B_{ij} - \tau_i < 0 \iff A_{ij} = 0 \iff 2A_{ij} - 1 < 0. \tag{4}
$$

因此

$$
\mathrm{rank}_{\pm}(2A - \mathbf{1}^{m \times n}) \leq \mathrm{rank}(B - \tau \mathbf{1}^{\top}) \leq \mathrm{rank}(B) + \mathrm{rank}(\tau \mathbf{1}^{\top}) = \mathrm{rank}_{\mathrm{rt}} A + 1.
$$

把这些合起来就得到所要的不等式链。

### D.3 后果

在向量嵌入模型的语境中，这为精确捕获给定检索目标集合所需向量的维度提供了下界和上界，精确的含义是按行排序、按行阈值化或全局阈值化。特别地，给定某个二元相关性矩阵 $A \in \{0, 1\}^{m \times n}$，我们至少需要 $\mathrm{rank}_{\pm}(2A - \mathbf{1}^{m \times n}) - 1$ 维才能精确捕获 $A$ 中的关系，并且总能在至多 $\mathrm{rank}_{\pm}(2A - \mathbf{1}^{m \times n})$ 维内做到这一点。

Alon et al. (1985) 中给出的分圆多项式构造意味着，任何 qrel 矩阵的符号秩至多为 $2k$，其中 $k$ 是某个查询的最大相关文档数。该构造得到的是未归一化的向量，然而可以通过多用一个维度，很容易改写成归一化向量。与定理 1 一致，这一构造一般需要无限精度，因此在实践中不可行。

### D.4 与 MTEB 的相关性

BEIR（用于 MTEB v1）（Thakur et al., 2021; Muennighoff et al., 2022）经常被引为嵌入模型已经过拟合的对象（Weller et al., 2025c; Thakur et al., 2025）。我们在图 7 中比较 LIMIT 与 BEIR 上的性能。我们看到性能总体上不相关，并且较小的模型（如 Arctic Embed）在两者上都更差，很可能是由于嵌入维度和预训练模型的知识。

**图 7 见原 PDF。** 横轴为 Limit Recall@100（约 0.0 到 0.2），纵轴为 BEIR（约 54 到 62）。标出的模型包括 Snowflake Arctic Emb.、Promptriever、E5-Mistral、GritLM、Gemini Emb.、Qwen3 E.。数值见后文表 7。

图 7：BEIR 与 LIMIT 之间没有明显相关。

## 附录 E 大语言模型的使用

大语言模型没有用于任何论文写作，只用于编程帮助和标题头脑风暴。

## 附录 F 度量 qrel 图密度的指标

我们给出两个把 qrel 矩阵当作图的指标，并表明 LIMIT 相对标准 IR 数据集具有独特性质（表 2）。我们称这些指标为图密度（Graph Density）和平均查询强度（Average Query Strength），并在下面描述它们。

**图密度。** 我们用 qrel 矩阵构造图：节点是文档，如果两篇文档至少对一个共同查询都相关，则它们之间有一条边。

<!-- 原 PDF 第 19 页 -->

对给定图 $G = (V, E)$，$V$ 是节点集，$E$ 是边集，图密度定义为图中边数与最大可能边数之比。对无向图，最大可能边数是 $\dfrac{|V|(|V|-1)}{2}$。因此密度 $\rho$ 计算为

$$
\rho = \frac{|E|}{\dfrac{|V|(|V|-1)}{2}} = \frac{2|E|}{|V|(|V|-1)}.
$$

该指标表明图的连接程度：密度为 1 表示完全图（所有可能的边都存在），密度接近 0 表示稀疏图。对一个 qrel 数据集而言也是如此。

**平均查询强度。** 在一个查询—查询图中，节点是查询，边表示查询之间的相似度（例如它们相关文档的 Jaccard 相似度）。查询节点 $i$ 的强度记为 $s_i$，定义为与它关联的所有边的权重之和。若 $w_{ij}$ 是查询 $i$ 与查询 $j$ 之间边的权重，$N(i)$ 是查询 $i$ 的邻居集合，则强度为

$$
s_i = \sum_{j \in N(i)} w_{ij}.
$$

平均查询强度 $\bar{s}$ 是图中所有查询节点这些强度的均值：

$$
\bar{s} = \frac{1}{|V_Q|}\sum_{i \in V_Q} s_i,
$$

其中 $V_Q$ 是图中全部查询节点的集合。该指标基于共享的相关文档，给出数据集中查询彼此平均连接有多强的总体度量。

**与其他数据集的比较。** 我们与标准 IR 数据集比较，例如 NQ（Kwiatkowski et al., 2019）、HotpotQA（Yang et al., 2018）和 SciFact（Wadden et al., 2020）。我们也给出一个指令遵循数据集 FollowIR Core17（Weller et al., 2024a）。对所有数据集，我们只用测试集。表 2 中的结果表明，LIMIT 在这两个指标上都显著更高（即查询相似度方面为 28，而其他数据集为 0.6 或更低）。

表 2：度量 qrel 矩阵密度的指标。我们看到 LIMIT 显著高于其他数据集，但最接近的是指令遵循数据集，例如 FollowIR 中的 Core17。我们的经验消融表明（尽管不能确定地证明），这里数值更高的数据集会更难被检索模型表示。

| 数据集名称 | 图密度 | 平均查询强度 |
| --- | ---: | ---: |
| NQ | 0 | 0 |
| HotPotQA | 0.000037 | 0.1104 |
| SciFact | 0.001449 | 0.4222 |
| FollowIR Core17 | 0.025641 | 0.5912 |
| LIMIT | 0.085481 | 28.4653 |

## 附录 G 图的表格形式

在本节中，我们给出若干图的表格形式。图 3 对应表 5，图 4 对应表 4，图 2 对应表 6，图 5 对应表 3。

<!-- 原 PDF 第 20 页 -->

表 3：微调结果的表格形式。可对照的图见图 5。

| 划分 | 维度 | Recall@2 | Recall@10 | Recall@100 |
| --- | ---: | ---: | ---: | ---: |
| Test | 32 | 85.5 | 98.4 | 100.0 |
| Test | 64 | 90.4 | 98.7 | 100.0 |
| Test | 128 | 93.1 | 99.5 | 99.9 |
| Test | 256 | 94.2 | 99.7 | 100.0 |
| Test | 384 | 95.6 | 99.6 | 100.0 |
| Test | 512 | 94.0 | 99.5 | 99.9 |
| Test | 768 | 96.1 | 99.8 | 100.0 |
| Test | 1024 | 96.5 | 99.8 | 100.0 |
| Train | 32 | 0.0 | 0.0 | 0.0 |
| Train | 64 | 0.1 | 0.3 | 2.2 |
| Train | 128 | 0.2 | 0.7 | 3.1 |
| Train | 256 | 0.0 | 0.0 | 0.4 |
| Train | 384 | 1.1 | 2.7 | 8.3 |
| Train | 512 | 0.7 | 2.3 | 9.8 |
| Train | 768 | 0.7 | 2.4 | 9.9 |
| Train | 1024 | 1.0 | 2.8 | 11.2 |

<!-- 原 PDF 第 21 页 -->

表 4：LIMIT 小版本的结果。可对照的图见图 4。

| 模型 | 维度 | Recall@2 | Recall@10 | Recall@20 |
| --- | --- | ---: | ---: | ---: |
| BM25 | default | 97.8 | 100.0 | 100.0 |
| E5-Mistral 7B | 32 | 7.9 | 32.6 | 56.2 |
| E5-Mistral 7B | 64 | 10.2 | 37.0 | 60.3 |
| E5-Mistral 7B | 128 | 14.5 | 41.9 | 65.9 |
| E5-Mistral 7B | 256 | 15.3 | 45.9 | 69.7 |
| E5-Mistral 7B | 512 | 22.2 | 54.7 | 74.8 |
| E5-Mistral 7B | 768 | 21.6 | 57.5 | 79.2 |
| E5-Mistral 7B | 1024 | 24.5 | 60.5 | 80.0 |
| E5-Mistral 7B | 2048 | 28.9 | 66.3 | 83.2 |
| E5-Mistral 7B | 3072 | 29.9 | 67.8 | 85.3 |
| E5-Mistral 7B | 4096 | 29.5 | 68.1 | 85.2 |
| GTE-ModernColBERT | default | 83.5 | 97.6 | 99.1 |
| GritLM 7B | 32 | 7.8 | 33.5 | 56.3 |
| GritLM 7B | 64 | 9.4 | 35.9 | 59.6 |
| GritLM 7B | 128 | 14.2 | 42.7 | 64.9 |
| GritLM 7B | 256 | 17.3 | 46.2 | 68.3 |
| GritLM 7B | 512 | 21.8 | 55.6 | 76.7 |
| GritLM 7B | 768 | 23.8 | 58.1 | 80.1 |
| GritLM 7B | 1024 | 26.2 | 61.4 | 80.1 |
| GritLM 7B | 2048 | 33.0 | 69.1 | 86.2 |
| GritLM 7B | 3072 | 36.3 | 72.9 | 89.9 |
| GritLM 7B | 4096 | 38.4 | 75.4 | 90.5 |
| Promptriever Llama3 8B | 32 | 6.1 | 31.4 | 56.0 |
| Promptriever Llama3 8B | 64 | 8.9 | 35.8 | 62.3 |
| Promptriever Llama3 8B | 128 | 13.7 | 44.5 | 67.6 |
| Promptriever Llama3 8B | 256 | 18.5 | 52.1 | 74.1 |
| Promptriever Llama3 8B | 512 | 27.0 | 61.8 | 81.7 |
| Promptriever Llama3 8B | 768 | 35.5 | 69.0 | 84.7 |
| Promptriever Llama3 8B | 1024 | 38.0 | 73.5 | 89.1 |
| Promptriever Llama3 8B | 2048 | 46.2 | 83.6 | 94.2 |
| Promptriever Llama3 8B | 3072 | 49.2 | 87.3 | 96.6 |
| Promptriever Llama3 8B | 4096 | 54.3 | 90.0 | 97.7 |
| Qwen3 Embed | 32 | 8.3 | 30.6 | 53.9 |
| Qwen3 Embed | 64 | 9.4 | 35.5 | 57.6 |
| Qwen3 Embed | 128 | 11.6 | 38.3 | 60.8 |
| Qwen3 Embed | 256 | 14.3 | 41.6 | 63.8 |
| Qwen3 Embed | 512 | 16.1 | 43.7 | 66.0 |
| Qwen3 Embed | 768 | 17.2 | 45.3 | 69.3 |
| Qwen3 Embed | 1024 | 17.8 | 48.7 | 70.3 |
| Qwen3 Embed | 2048 | 19.5 | 51.5 | 72.4 |
| Qwen3 Embed | 3072 | 19.3 | 52.8 | 73.3 |
| Qwen3 Embed | 4096 | 19.0 | 52.3 | 73.8 |
| Gemini Embed | 2 | 4.2 | 23.0 | 45.5 |
| Gemini Embed | 4 | 4.2 | 21.9 | 46.0 |
| Gemini Embed | 8 | 4.9 | 23.2 | 47.0 |
| Gemini Embed | 16 | 5.2 | 24.7 | 47.5 |
| Gemini Embed | 32 | 6.3 | 25.2 | 50.6 |
| Gemini Embed | 64 | 6.9 | 30.6 | 55.0 |
| Gemini Embed | 128 | 7.7 | 37.0 | 62.9 |
| Gemini Embed | 256 | 14.6 | 46.9 | 69.7 |
| Gemini Embed | 512 | 23.3 | 58.4 | 77.9 |
| Gemini Embed | 768 | 28.8 | 67.5 | 84.5 |
| Gemini Embed | 1024 | 31.8 | 69.9 | 86.1 |
| Gemini Embed | 2048 | 31.9 | 70.3 | 87.1 |
| Gemini Embed | 3072 | 33.7 | 72.4 | 87.9 |
| Snowflake Arctic L | 32 | 8.3 | 30.3 | 53.8 |
| Snowflake Arctic L | 64 | 9.0 | 35.4 | 58.5 |
| Snowflake Arctic L | 128 | 12.7 | 41.3 | 65.1 |
| Snowflake Arctic L | 256 | 16.0 | 48.2 | 72.6 |
| Snowflake Arctic L | 512 | 16.7 | 51.3 | 74.1 |
| Snowflake Arctic L | 768 | 17.9 | 53.5 | 74.6 |
| Snowflake Arctic L | 1024 | 19.4 | 54.9 | 76.0 |
| Snowflake Arctic L | 2048 | 19.4 | 54.9 | 76.0 |
| Snowflake Arctic L | 3072 | 19.4 | 54.9 | 76.0 |
| Snowflake Arctic L | 4096 | 19.4 | 54.9 | 76.0 |

<!-- 原 PDF 第 22 页 -->

表 5：LIMIT 上的结果。可对照的图见图 3。

| 模型 | 维度 | Recall@2 | Recall@10 | Recall@100 |
| --- | --- | ---: | ---: | ---: |
| E5-Mistral 7B | 32 | 0.0 | 0.0 | 0.5 |
| E5-Mistral 7B | 64 | 0.0 | 0.1 | 0.4 |
| E5-Mistral 7B | 128 | 0.1 | 0.3 | 1.0 |
| E5-Mistral 7B | 256 | 0.4 | 0.9 | 1.9 |
| E5-Mistral 7B | 512 | 0.7 | 1.3 | 3.8 |
| E5-Mistral 7B | 768 | 0.9 | 1.7 | 4.3 |
| E5-Mistral 7B | 1024 | 0.9 | 1.8 | 5.9 |
| E5-Mistral 7B | 2048 | 1.0 | 1.9 | 6.8 |
| E5-Mistral 7B | 3072 | 1.3 | 2.0 | 7.7 |
| E5-Mistral 7B | 4096 | 1.3 | 2.2 | 8.3 |
| Snowflake Arctic L | 32 | 0.0 | 0.1 | 0.6 |
| Snowflake Arctic L | 64 | 0.2 | 0.4 | 1.7 |
| Snowflake Arctic L | 128 | 0.1 | 0.3 | 1.8 |
| Snowflake Arctic L | 256 | 0.2 | 0.8 | 2.5 |
| Snowflake Arctic L | 512 | 0.3 | 1.0 | 2.5 |
| Snowflake Arctic L | 768 | 0.4 | 1.1 | 3.1 |
| Snowflake Arctic L | 1024 | 0.4 | 0.8 | 3.3 |
| Snowflake Arctic L | 2048 | 0.4 | 0.8 | 3.3 |
| Snowflake Arctic L | 3072 | 0.4 | 0.8 | 3.3 |
| Snowflake Arctic L | 4096 | 0.4 | 0.8 | 3.3 |
| GritLM 7B | 32 | 0.0 | 0.0 | 0.8 |
| GritLM 7B | 64 | 0.0 | 0.1 | 0.3 |
| GritLM 7B | 128 | 0.1 | 0.3 | 1.3 |
| GritLM 7B | 256 | 0.1 | 0.4 | 2.8 |
| GritLM 7B | 512 | 0.6 | 1.8 | 6.5 |
| GritLM 7B | 768 | 1.5 | 3.1 | 8.7 |
| GritLM 7B | 1024 | 1.8 | 3.5 | 10.6 |
| GritLM 7B | 2048 | 2.3 | 4.3 | 11.8 |
| GritLM 7B | 3072 | 2.0 | 4.3 | 12.9 |
| GritLM 7B | 4096 | 2.4 | 4.1 | 12.9 |
| Promptriever Llama3 8B | 32 | 0.0 | 0.0 | 0.1 |
| Promptriever Llama3 8B | 64 | 0.0 | 0.0 | 0.3 |
| Promptriever Llama3 8B | 128 | 0.0 | 0.1 | 0.6 |
| Promptriever Llama3 8B | 256 | 0.2 | 0.4 | 1.8 |
| Promptriever Llama3 8B | 512 | 0.6 | 1.4 | 5.4 |
| Promptriever Llama3 8B | 768 | 1.3 | 3.1 | 8.7 |
| Promptriever Llama3 8B | 1024 | 2.1 | 4.4 | 12.8 |
| Promptriever Llama3 8B | 2048 | 3.2 | 6.5 | 18.1 |
| Promptriever Llama3 8B | 3072 | 2.9 | 6.3 | 17.8 |
| Promptriever Llama3 8B | 4096 | 3.0 | 6.8 | 18.9 |
| Qwen3 Embed | 32 | 0.0 | 0.1 | 1.1 |
| Qwen3 Embed | 64 | 0.0 | 0.2 | 1.0 |
| Qwen3 Embed | 128 | 0.3 | 0.4 | 1.8 |
| Qwen3 Embed | 256 | 0.4 | 0.8 | 3.2 |
| Qwen3 Embed | 512 | 0.6 | 1.3 | 3.3 |
| Qwen3 Embed | 768 | 0.7 | 1.5 | 3.8 |
| Qwen3 Embed | 1024 | 0.7 | 1.6 | 4.6 |
| Qwen3 Embed | 2048 | 0.9 | 1.7 | 4.7 |
| Qwen3 Embed | 3072 | 0.8 | 1.6 | 4.8 |
| Qwen3 Embed | 4096 | 0.8 | 1.8 | 4.8 |
| Gemini Embed | 2 | 0.0 | 0.0 | 0.1 |
| Gemini Embed | 4 | 0.0 | 0.0 | 0.0 |
| Gemini Embed | 8 | 0.0 | 0.0 | 0.0 |
| Gemini Embed | 16 | 0.0 | 0.0 | 0.0 |
| Gemini Embed | 32 | 0.0 | 0.0 | 0.0 |
| Gemini Embed | 64 | 0.0 | 0.0 | 0.3 |
| Gemini Embed | 128 | 0.0 | 0.1 | 0.3 |
| Gemini Embed | 256 | 0.0 | 0.1 | 1.2 |
| Gemini Embed | 512 | 0.2 | 1.1 | 3.6 |
| Gemini Embed | 768 | 0.9 | 2.5 | 7.6 |
| Gemini Embed | 1024 | 1.3 | 2.7 | 8.1 |
| Gemini Embed | 2048 | 1.5 | 3.1 | 8.5 |
| Gemini Embed | 3072 | 1.6 | 3.5 | 10.0 |
| GTE-ModernColBERT | default | 23.1 | 34.6 | 54.8 |
| BM25 | default | 85.7 | 90.4 | 93.6 |

<!-- 原 PDF 第 23 页 -->

表 6：自由嵌入优化实验中不同 $d$ 的 $n$ 临界值。对应的图见图 2。

| $d$ | Critical-$n$ |
| ---: | ---: |
| 4 | 10 |
| 5 | 14 |
| 6 | 19 |
| 7 | 24 |
| 8 | 28 |
| 9 | 32 |
| 10 | 36 |
| 11 | 42 |
| 12 | 47 |
| 13 | 54 |
| 14 | 62 |
| 15 | 70 |
| 16 | 79 |
| 17 | 89 |
| 18 | 99 |
| 19 | 109 |
| 20 | 120 |
| 21 | 132 |
| 22 | 144 |
| 23 | 157 |
| 24 | 170 |
| 25 | 184 |
| 26 | 198 |
| 27 | 213 |
| 28 | 229 |
| 29 | 245 |
| 30 | 261 |
| 31 | 278 |
| 32 | 296 |
| 33 | 314 |
| 34 | 333 |
| 35 | 352 |
| 36 | 372 |
| 37 | 392 |
| 38 | 413 |
| 39 | 434 |
| 40 | 460 |
| 41 | 484 |
| 42 | 505 |
| 43 | 545 |
| 44 | 605 |
| 45 | 626 |

表 7：BEIR 与 LIMIT 的结果。可对照的图见图 7。

| 模型 | BEIR | LIMIT R@100 |
| --- | ---: | ---: |
| Snowflake Arctic | 55.22 | 3.3 |
| Promptriever | 56.40 | 18.9 |
| E5-Mistral | 57.07 | 8.3 |
| GritLM | 57.40 | 12.9 |
| Gemini Embed | 62.65 | 10.0 |
| Qwen3 Embed | 62.76 | 4.8 |

<!-- 译完 -->
