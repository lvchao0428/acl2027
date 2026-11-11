# CONTEXTGNN: BEYOND TWO-TOWER RECOMMENDATION SYSTEMS

- 原文件名：contextgnn-arxiv-2411.19513.pdf
- 原标题：CONTEXTGNN: Beyond Two-Tower Recommendation Systems
- 中文标题：ContextGNN：超越双塔推荐系统
- 作者：Yiwen Yuan，Zecheng Zhang，Xinwei He，Akihiro Nitta，Weihua Hu，Dong Wang，Manan Shah，Shenyang Huang，Blaž Stojanovič，Alan Krumholz，Jan Eric Lenssen，Jure Leskovec，Matthias Fey（Kumo.AI）
- 会议 / arXiv：各页页眉未印会议名。第 1 页底部为 arXiv:2411.19513v1 [cs.IR] 29 Nov 2024

<!-- 原 PDF 第 1 页 -->

## 摘要

推荐系统主要采用双塔架构，通过对各自嵌入做内积来评估用户–物品排序。然而，双塔模型的一个关键局限是，它们学到的是与配对无关的用户表示和物品表示。相比之下，成对表示要么因二次复杂度而难以扩展（原文用 ineffable），要么对待排序的候选配对限制过严。为处理这些问题，我们引入基于上下文的图神经网络（Context-based Graph Neural Networks，ContextGNN），一种用于推荐系统中链接预测的新深度学习架构。该方法对位于用户局部子图内的熟悉物品使用成对表示，同时利用双塔表示来促进探索性物品的推荐。最后由一个网络预测如何把成对推荐与双塔推荐融合成单一的物品排序。我们表明，ContextGNN 能够适应不同的数据特性，并在一组多样的实际推荐任务上优于现有方法，包括传统方法和基于 GNN 的方法，平均提升性能 20%。

## 1 引言

推荐系统在过去几十年中已成为预测性机器学习的一个重要应用领域（Webber, 2021; He et al., 2023; Li et al., 2024）。给定一组用户和一组物品（例如可供购买的商品），推荐系统旨在为每个用户找出最优的物品推荐（例如该用户最可能购买的商品）。传统上，这一问题通过双塔范式的不同变体来建模（Hu et al., 2008; Koren et al., 2009）：一座塔嵌入用户，另一座塔嵌入物品，再通过内积解码器进行匹配和排序。这一方案在推理阶段扩展推荐系统时非常高效，因为它允许预先计算用户和物品表示，并通过快速的（近似）最大内积搜索完成最终排序（Johnson et al., 2019）。

然而，基于双塔的推荐架构有一个关键局限：它们为用户和物品学习的是与配对无关的表示。也就是说，用户表示并不知道当前考虑的是哪个物品；同样，物品表示也不知道是哪个用户，因此物品表示没有捕获用户看待物品的独特性。于是，两端的表示都没有捕获它们正在为其做预测的那种成对依赖的知识。例如，考虑一位定期补货化妆品的用户。在这一情形中，用户–化妆品配对的细粒度上下文至关重要，而这无法仅由两个相互独立的用户表示和物品表示充分捕获。这种知识缺失对预测质量有严重后果，因为模型无法区分诸如熟悉购买（即用户反复与相似物品集合交互）与探索性购买（即用户喜欢探索新物品）之类的情形。成对表示纳入了关于其所预测配对的知识，因而能够把预测放进上下文之中；但若要对所有可能的用户–物品配对生成成对表示，则会因其二次复杂度而无法穷尽。另一种做法是预先过滤候选配对集合，例如通过基于内容的过滤或协同过滤（Ricci et al., 2010; Campana & Delmastro, 2017），但模型的能力随后就被候选生成过程的召回所限制。

第 1 页底部印有页码 1，以及 arXiv:2411.19513v1 [cs.IR] 29 Nov 2024。

<!-- 原 PDF 第 2 页 -->

这里，我们开发基于上下文的图神经网络（ContextGNN），一种新颖的、基于图神经网络（GNN）的单阶段推荐系统，它把成对表示与双塔表示融进一个统一架构。ContextGNN 被设计为在异构时序图上做时序推荐（预测用户接下来会与之交互的物品集合），并兼取两者之长：第一个模型为用户局部交互图内的所有物品支持成对表示（Zhu et al., 2021）。对于相距较远的用户–物品配对，即彼此不在对方 $k$ 跳邻域内的用户–物品配对，成对嵌入由一个全局的、基于双塔的 GNN 来补充，后者充当有效的回退模型。最后由一个网络预测一个特定于用户的、个性化的融合分数，规定如何把成对推荐与双塔推荐合并成单一排序。

ContextGNN 背后的关键想法（原文 They key idea）是：对用户有丰富过往交互的那片物品区域，把预测放进上下文。在这里，成对表示能够捕获过往用户–物品交互的细粒度模式，例如重复购买和其他先前行为（例如点击、标为收藏、加入购物车），或通过协同信号（例如朋友是否购买过同一物品）。第二个组件是一种基于浅层物品嵌入的、新颖的、与配对无关的双塔模型，它允许对探索性和意外发现式的推荐建模。对于这些「遥远」物品，并不存在特定的用户–物品上下文，成对表示带来的收益很小，因而回退到双塔表示是合适的。重要的是，双塔模型的设计方式使它可以以很小的计算开销集成进成对架构。最后，模型学习哪些用户更偏好熟悉物品而非探索性购买，并据此调整最终排序分数。

我们在关系深度学习（Fey et al., 2024）的语境中部署 ContextGNN，用于关系数据库内的推荐。关系数据库（Robinson et al., 2024）包含多样的表，带有丰富的多模态输入特征和丰富的多行为、时序交互，因而成为对我们的模型做压力测试的理想环境。此外，我们考察对人类行为复杂模式建模时的挑战。我们的分析和实验结果强调了混合架构的必要性，因为单一模型不足以有效应对真实数据集在任务内部和任务之间的多样性。我们表明，ContextGNN 能够适应不同的数据特性，同时在现实且实用的推荐任务上优于现有模型。具体而言，相对于最好的成对表示基线，ContextGNN 平均提升结果 20%；相对于最好的双塔表示基线，平均提升 344%。

## 2 相关工作

推荐系统是机器学习中一个长期存在的研究领域。推荐问题常被表述为二分图上的链接预测：两组节点，一组是用户，另一组是物品。这两组节点之间，过往交互被表示为链接，目标是预测哪些链接将在未来出现。传统做法是计算用户嵌入与物品嵌入的内积，例如通过矩阵分解（Koren et al., 2009）来发现并利用用户与物品之间的相似性，即协同过滤（Hu et al., 2008; Mnih & Salakhutdinov, 2007）。

与许多其他领域类似，深度学习影响了推荐系统，例如用非线性网络预测分数（H. & C., 2017; He et al., 2017），利用图嵌入技术（Perozzi et al., 2014; Grover & Leskovec, 2016），或从变分自编码器所建模的分布中抽样（Liang et al., 2018）。近来，生成式推荐这一新领域值得一提，它利用大语言模型通过文本生成来提供推荐（Wu et al., 2023）。本文的工作与两条研究线索相关：序列推荐系统，以及用 GNN 做推荐。

**序列上的推荐。** 推荐传统上被建模为序列预测问题。早期方法使用马尔可夫链（原文 Marcov chains）（Rendle et al., 2010; He & McAuley, 2016），后来被循环神经网络（Liu et al., 2018）、时间注意力（Kang & McAuley, 2018; Li et al., 2017）和 Transformer 表述（Sun et al., 2019; Yang et al., 2022; Xia et al., 2022）所取代。它们也被与 GNN 结合，以额外捕获协同信号（Ma et al., 2020）。

<!-- 原 PDF 第 3 页 -->

**用 GNN 做推荐。** 已有多种基于双塔的图神经网络（Hamilton et al., 2017）被开发用于链接预测任务，其思想是通过在用户–物品交互图上精炼嵌入，把协同过滤范式整合进来。早期例子使用基于 GNN 的自编码器（Kipf & Welling, 2016; Schlichtkrull et al., 2018）来得到图链接上的预测。由于 GNN 在局部传播信息（因而不能推理节点在图中的位置），已有工作表明，用深层 GNN 传播浅层用户嵌入和物品嵌入，对于捕获完整的协同信号至关重要（Wang et al., 2019）。LightGCN（He et al., 2020）和 UltraGCN（Mao et al., 2021）进一步简化用于嵌入生成的消息传播，以提升小规模数据集上的性能。另一条工作线通过加入自监督来加强基于 GNN 的推荐系统（Wu et al., 2021; Yu et al., 2022; Cai et al., 2023），例如基于图增强的对比学习。这些发现与我们的工作正交，但在底层仍然采用双塔架构。

与 ContextGNN 最接近的工作线，是把身份感知和位置感知编码进 GNN，以便关联用户–物品配对（You et al., 2019; 2021）。例如，局部子图已被扩展用来编码用户–物品配对的位置信息（Zhang & Chen, 2018; Teru et al., 2020），但缺少高效的推理过程。NBFNet（Zhu et al., 2021）引入一种基于路径的成对表示模型：它构造以用户节点为中心的子图，同时在物品节点处读出 GNN 的表示。该方法产生以特定用户为条件的物品表示，从而纳入成对信息，又不带来过高的计算成本。然而，该方法把候选限制在用户子图内的物品，这在涉及探索性推荐或冷启动物品的情形中极大限制了它的有效性。我们的局部成对表示模型建立在这一框架之上，并把它扩展到异构、多行为、时序的推荐系统语境。最重要的是，我们分析并消除它围绕局部性的主要局限，方法是用一个有效的回退模型来扩展它。

虽然绝大多数相关工作聚焦于在静态图上建模推荐系统，近来已出现多个时序推荐基准，例如 Temporal Graph Benchmark（Huang et al., 2023）和 RelBench（Robinson et al., 2024）。本文采用推荐系统任务的时序表述，并在 RelBench 的实际设定中广泛评估 ContextGNN，表明我们的方法显著优于先前方法。

## 3 时序推荐，以及到哪里去找它们

我们把时序推荐问题表述在直到时间戳 $T$ 的异构图快照上：

$$G^{(-\infty,T]} = (V, E, \phi, \psi),$$

其中节点集为 $V$，边集为 $E \subseteq V \times V$，每个节点 $v \in V$ 属于节点类型 $\phi(v)$，每条边 $e \in E$ 属于边类型 $\psi(e)$。我们把 $\mathcal{L} \subset V$ 称为异构图中的用户集，把 $\mathcal{R} \subset V$ 称为物品集。任务是为用户 $v \in \mathcal{L}$ 预测一组真值物品 $\mathcal{Y}_v^{(T, T+i]} \subseteq \mathcal{R}$，即在时间区间 $(T, T+i]$ 内、对给定区间长度 $i$，该用户出现过链接的那些物品。做预测时，模型只能访问直到时间戳 $T$ 的历史信息。

在最简单的情形中，$G^{(-\infty,T]}$ 是一个二分图，节点集 $V = \mathcal{L} \cup \mathcal{R}$，且只有单一边类型 $|\{\psi(e) : e \in E\}| = 1$。然而，推广到异构图允许纳入其他节点类型，更重要的是，纳入用户行为的不同边类型（例如点击、标为收藏、加入购物车），它们为预测目标行为（例如购买）提供互补信号（Xia et al., 2022）。节点和边可以（部分地）带有初始特征表示，例如 $h_v^{(0)} \in \mathbb{R}^d$，$v \in V$，以及标明其出现（或消失）的时间戳。在没有时间戳时，所给框架可以很容易地转化成静态链接预测问题，这是文献中的常见做法（Kipf & Welling, 2016; Wang et al., 2019; He et al., 2020）。然而，这种做法忽略了关键信息，例如过往活动的新近程度。注意，所给框架也允许用户和物品随时间新出现。不过，为记号简单起见，我们假定它们始终在 $\mathcal{L}$ 和 $\mathcal{R}$ 中。

**局部性分数。** 为推荐系统开发机器学习方案本质上具有挑战，因为人类行为的模式很复杂（He et al., 2023）。用户的偏好差异很大：有些人是探索者，不断寻求新体验；另一些人是重复者，

<!-- 原 PDF 第 4 页 -->

更偏好熟悉的事物。这类特性在不同数据集之间尤其明显，例如，用户重复一次先前购买的可能性，高于用户给同一部电影打两次分。为更好地理解这些效应，我们引入局部性分数，它度量落在以用户 $v \in \mathcal{L}$ 为中心、直到时间戳 $T$ 的子图的 $k$ 跳邻域 $\mathcal{N}_k^{(-\infty,T]}(v)$ 之内的真值链接所占的比例：

$$
s_k^{(T,T+i]} = \frac{1}{|\mathcal{L}|}\sum_{v \in \mathcal{L}} = \frac{\left|\mathcal{N}_k^{(-\infty,T]}(v) \cap \mathcal{R} \cap \mathcal{Y}_v^{[T,T+i)}\right|}{\left|\mathcal{Y}_v^{[T,T+i)}\right|}.
\tag{1}
$$

公式 (1) 按 PDF 文本层的符号抄录：求和号位于两个等号之间；真值集合在公式中的区间是 $[T, T+i)$，与上文正文中的 $(T, T+i]$ 写法不同。

直观上，局部性分数量化一个用户未来的真值物品中有多少是局部的。取决于子图深度 $k$，该分数反映不同的交互模式。对于浅子图（$k = 1$），它捕获用户是否重复购买，或是否先前通过点击、标为收藏等行为与该物品交互过。随着子图深度增加，分数开始纳入协同过滤信号，例如朋友是否在过去购买过该真值物品（$k = 2$），或者该真值物品是否曾被与当前用户购买行为相似的用户购买过（$k = 3$）。注意，实践中由于可扩展性方面的顾虑，超出深度 $k = 3$ 是不可行的。

**表 1：** RelBench 中全部推荐任务在验证/测试划分上、不同子图深度 $k \in \{1, 3\}$ 的局部性分数。

| 数据集 | 任务 | 划分 | $k = 1$ | $k = 3$ |
| --- | --- | --- | --- | --- |
| rel-amazon | user-item-purchase | val | 0.002 | 0.181 |
| rel-amazon | user-item-purchase | test | 0.001 | 0.168 |
| rel-amazon | user-item-rate | val | 0.002 | 0.183 |
| rel-amazon | user-item-rate | test | 0.002 | 0.170 |
| rel-amazon | user-item-review | val | 0.002 | 0.185 |
| rel-amazon | user-item-review | test | 0.001 | 0.175 |
| rel-hm | user-item-purchase | val | 0.045 | 0.395 |
| rel-hm | user-item-purchase | test | 0.048 | 0.417 |
| rel-stack | user-post-comment | val | 0.265 | 0.308 |
| rel-stack | user-post-comment | test | 0.256 | 0.298 |
| rel-stack | post-post-related | val | 0.109 | 0.225 |
| rel-stack | post-post-related | test | 0.141 | 0.280 |
| rel-trial | condition-sponsor-run | val | 0.000 | 0.241 |
| rel-trial | condition-sponsor-run | test | 0.000 | 0.242 |
| rel-trial | site-sponsor-run | val | 0.000 | 0.208 |
| rel-trial | site-sponsor-run | test | 0.000 | 0.229 |

我们在 RelBench（Robinson et al., 2024）上对不同的 $k$ 评估局部性分数。RelBench 是一个关系深度学习（Fey et al., 2024）基准，覆盖多种具有不同特性的真实推荐任务（见表 1）。有趣的是，局部性分数在任何数据集上都不超过 0.5，表明大多数真值物品完全是探索性的，不被图中任何长度 $\le 3$ 的路径所覆盖。然而，对于 $k = 1$，我们在 rel-hm 和 rel-stack 上观察到较高的局部性分数，表明用户倾向于频繁重复服装购买，或在同一帖子上多次评论。增加子图深度通常会提高覆盖率，如 rel-amazon 等数据集所示。虽然这里的用户通常不会对同一物品购买/评分/评论两次，他们倾向于购买「附近」用户买过的同样产品。总体而言，这一观察表明，虽然像 NBFNet（Zhu et al., 2021）这样的成对表示架构很强，它们往往无法在其候选集内提供足够的覆盖，从而极大降低其有效性。这就提出一个有趣的问题：如何利用成对表示的好处，同时支持对探索性推荐的建模，而又不需要复杂的多阶段方法。

## 4 用基于上下文的图神经网络做推荐

接下来，我们描述基于上下文的图神经网络（ContextGNN）。它由坐在同一个 GNN 骨干之后的两个分开的 GNN 架构组成。ContextGNN 把成对表示和双塔表示都融进单一架构，因而自然能够适应多样的数据集和任务特性。第一个模型基于局部的、以用户为中心的子图内给出的物品候选集，采用成对表示（见第 4.1 节）。第二个模型引入一种基于浅层物品表示的新颖双塔架构，用于为用户子图之外的全部用户–物品配对预测排序（见第 4.2 节）。最后，由用户 GNN 表示上的一个 MLP 产生的、特定于用户的融合分数，被加到成对表示模型的分数上，从而使两个模型各自不同的

<!-- 原 PDF 第 5 页 -->

图 1 见原 PDF。

**图 1：** 基于上下文的图神经网络总览。ContextGNN 利用一个双向 $\mathrm{GNN}_\theta$ 在用户的局部子图内学习用户表示 $h_v^{(2)}$ 和特定于用户的物品表示 $h_w^{(2)}$。其消息传递方案还额外传播浅层物品嵌入 $w_w$ 和种子用户的 $\mathrm{INDICATOR}_\theta$ 表示，从而得到增强。随后，根据物品是否位于用户子图内来产生物品分数。通过一个 $\mathrm{MLP}_\theta$ 学习特定于用户的融合分数，用偏移局部排序的贡献来产生最终排序。图中的示意分数见原 PDF，此处不另抄。

分数对齐，并捕获某个用户有多倾向于探索，从而给相应模型更多或更少的权重（见第 4.3 节）。我们在第 4.4 节讨论额外的考虑和扩展。ContextGNN 的总览见图 1。

### 4.1 成对表示

我们的局部成对表示模型建立在 Zhu et al. (2021) 所提框架之上，并把它扩展到异构、多行为、时序的推荐系统语境。NBFNet 是一种基于路径的方法，推广了 Bellman-Ford 算法（原文 Bellmann-Ford）（Baras & Theodorakopoulos, 2010）。NBFNet 并不通过两个独立的节点表示 $h_v^{(k)}$ 和 $h_w^{(k)}$（即通过两个独立子图）来学习成对表示，而只使用特定于用户的子图，但从中读出 GNN 的物品表示。因此，NBFNet 用特定于用户的物品表示 $h_w^{(k)}$ 来简称成对表示 $h_{(v,w)}^{(k)}$。于是，它在其表示中同时捕获关于物品 $w$ 和用户 $v$ 的知识。为了让 GNN 区分种子用户和子图内被采样到的其他用户，会向种子节点加上一个 $d$ 维的 $\mathrm{INDICATOR}_\theta$ 表示（You et al., 2021）。具体而言，我们的成对表示模型如下：

1. 在用户 $v \in \mathcal{L}$ 周围采样一个 $k$ 跳子图 $\tilde{G} \leftarrow G_k^{(-\infty,T]}[v]$，节点集为 $\tilde{V}$。
2. 向用户种子节点加上指示表示：$h_v^{(0)} \leftarrow h_v^{(0)} + \mathrm{INDICATOR}_\theta$。
3. 在第 $k$ 层读出 GNN 的用户表示和物品表示：

$$h_v^{(k)},\ \{h_w^{(k)} : w \in \tilde{V} \cap \mathcal{R}\} \leftarrow \mathrm{GNN}_\theta^{(k)}(\tilde{G}, H^{(0)}).$$

4. 对所有物品 $w \in \tilde{V} \cap \mathcal{R}$ 计算最终排序：$y^{(\mathrm{pair})}(v,w) \leftarrow h_v^{(k)} \cdot h_w^{(k)}$。

与 NBFNet 不同，我们从 GNN 中同时读出用户表示和物品表示，以便产生局部物品的排序。这让模型能够利用完整的 $k$ 跳用户信息；否则用户表示只在中间 GNN 层、基于有限的子图深度来计算。

还要注意，采样 $k$ 跳子图通常得到一张朝向种子节点的有向计算图（Fey & Lenssen, 2019）。然而，为便于抽取物品节点表示，采样得到的子图在应用 GNN 之前必须被变换成双向图。这一做法与先前把 GNN 的深度和范围解耦的工作一致（Zeng et al., 2021）。

<!-- 原 PDF 第 6 页 -->

这一做法在时序、异构图的语境中特别有效，因为 GNN 自然地学会整合来自不同边类型的多行为信号。例如，成对表示捕获全部过往的用户–物品交互，例如上次购买的新近程度，或该物品是否曾被点击或标记。尽管表达力强，这一方法也很高效：只需要对用户子图做一次 GNN 前向，就能为整组相关物品做预测。假定子图规模有界，对全部用户集的训练和推理可以在 $O(|\mathcal{L}|)$ 时间内完成，这与双塔模型所需的 $O(|\mathcal{L}| \cdot |\mathcal{R}|)$ 复杂度形成鲜明对照。此外，由于不使用浅层嵌入，这一做法自然扩展到随时间新出现的用户和物品。尽管如此，如第 3 节所讨论的，仅凭这一方法并不能完全满足现代推荐系统的多样需求，因为它的潜在候选集合有限。

### 4.2 双塔表示

ContextGNN 的双塔模型对用户子图之外的所有用户–物品配对排序，作为补充成对表示的有效回退机制。虽然灵感来自相关的双塔架构（Wang et al., 2019; He et al., 2020），我们的新颖双塔模型能够与成对架构高效集成。双塔模型的关键创新是使用浅层物品表示。具体而言，我们不部署 GNN 来计算物品表示；相反，我们完全依赖一个浅层嵌入矩阵 $W \in \mathbb{R}^{|\mathcal{R}| \times d}$ 来学习物品表示。这一设计受到多个关键观察的启发：

- **在物品侧应用 GNN 的信息增益有限。** 物品连接天然非常稠密。在极端情形中，热门物品可能收到超过 100 万次交互（一个物品连接到先前与之交互过的每个用户）。这给子图采样带来显著的挑战和不确定性，并容易使 GNN 暴露于过挤压和过平滑问题。
- **浅层嵌入矩阵非常有效。** 浅层物品嵌入矩阵能够同样有效地捕获关键信号，例如流行趋势、季节模式、人群偏好和物品相似性，并不逊于 GNN。
- **GNN 物品表示在训练期间扩展性差。** 同时纳入用户和物品的 GNN 表示，会因显存约束而把模型限制为只能使用少量负样本。相比之下，浅层物品嵌入支持针对大得多的负样本语料进行训练（$\approx 10\mathrm{M}$），这对提升模型性能至关重要。这一做法也消除了对复杂负采样策略的需要；当负样本数量有限时，这些策略常常是必需的。

重要的是，我们也把浅层物品嵌入注入用户的 GNN 前向过程，使用户表示能更好地与相应的物品表示对齐。因此，用户的 GNN 表示遵循与 NGCF（Wang et al., 2019）或 LightGCN（He et al., 2020）类似的精神，尽管我们不使用浅层用户嵌入，因为 GNN 本身已足够强大，可以在没有它们的情况下学到自己丰富的表示。因此，我们的双塔表示模型可以概括如下：

1. 在用户 $v \in \mathcal{L}$ 周围采样一个 $k$ 跳子图 $\tilde{G} \leftarrow G_k^{(-\infty,T]}[v]$，节点集为 $\tilde{V}$。
2. 向所有被采样的物品 $w \in \tilde{V} \cap \mathcal{R}$ 加上浅层嵌入：$h_w^{(0)} \leftarrow h_w^{(0)} + w_w$。
3. 在第 $k$ 层读出 GNN 的用户表示：$h_v^{(k)} \leftarrow \mathrm{GNN}_\theta^{(k)}(\tilde{G}, H^{(0)})$。
4. 对所有物品 $w \in \mathcal{R} \setminus \tilde{V}$ 计算最终排序：$y^{(\mathrm{tower})}(v,w) \leftarrow h_v^{(k)} \cdot w_w$。

### 4.3 基于上下文的图神经网络

我们最终的 ContextGNN 架构把成对表示和双塔表示融进一个统一架构。也就是说，对局部用户子图内的所有物品 $w \in \tilde{V} \cup \mathcal{R}$，我们利用从成对表示得到的分数 $y^{(\mathrm{pair})}(v,w)$；而对采样子图之外的所有物品 $w \in \tilde{V} \setminus \mathcal{R}$，我们回退到双塔分数 $y^{(\mathrm{tower})}(v,w)$。

<!-- 原 PDF 第 7 页 -->

用户行为是多样的，这一观察是使 ContextGNN 得以成立的最后一个要素。为适应不同用户之间的这种多样性，ContextGNN 从 GNN 的用户嵌入 $h_v^{(k)}$ 出发，经由一个 $\mathrm{MLP}_\theta$ 学习一个特定于用户的融合分数。这一个性化融合分数通过对齐不同的分数，来学习哪些用户更偏好熟悉物品而非探索性购买，并据此调整最终排序分数。由此，最终分数为

$$
y(v,w) =
\begin{cases}
y^{(\mathrm{pair})}(v,w) + \mathrm{MLP}_\theta\!\left(h_v^{(k)}\right) & \text{若 } w \in \tilde{V} \cup \mathcal{R}, \\
y^{(\mathrm{tower})}(v,w) & \text{否则.}
\end{cases}
\tag{2}
$$

在 ContextGNN 中，成对表示和双塔表示都来自同一个 GNN 骨干。由于两个模型都只依赖用户子图，用户嵌入 $h_v^{(k)}$ 可以在一次 GNN 前向中抽出，并在两个模型的下游使用中加以利用。这一精简做法使 ContextGNN 在计算上非常高效。ContextGNN 随后被端到端训练，同时优化两类物品分数以及融合分数，以最大化未来用户–物品交互的预测性能。实践中，我们使用交叉熵损失进行优化，尽管任何其他损失表述也同样适用（Rendle et al., 2009）。推理时，我们通过（近似）最大内积搜索从双塔模型得到最高分（Johnson et al., 2019），并在后处理过程中把它们与成对分数合并。

### 4.4 扩展

我们讨论在实践中应用 ContextGNN 时的额外考虑和扩展。

**纳入关系深度学习的语境。** ContextGNN 与关系深度学习框架（Fey et al., 2024）很好地对齐。关系深度学习是关系数据库上图表示学习的一份蓝图。具体而言，关系深度学习把关系数据库视为异构时序图，其中维表和事实表通过主键–外键关系相连。然后，采用具有时间意识的子图采样，生成直到时间戳 $T$ 的异构子图快照 $G_k^{(-\infty,T]}[v]$，用来预测未来的用户–物品交互。关系数据库（Robinson et al., 2024）包含多样的表，带有丰富的多模态输入特征和丰富的多行为、时序交互，因而成为对 ContextGNN 做压力测试的理想环境。

**转导式与归纳式建模。** 虽然 ContextGNN 中的成对表示在设计上是归纳式的，物品侧浅层嵌入矩阵的使用把它放在转导式设定中。这意味着，虽然 ContextGNN 可以自然地随时间容纳新出现的用户，它无法在预测时处理新物品，因为它们的浅层嵌入仍未初始化。为使 ContextGNN 能在归纳式设定中运行，我们提议用物品输入特征 $h_w^{(0)}$ 之上的一个深度神经网络来替换浅层物品嵌入矩阵。这一做法使 ContextGNN 能够扩展到诸如市场或活动推荐之类的任务，在这些任务中处理新物品是必要的。

**抽样 softmax 表述。** 由于针对完整物品集 $\mathcal{R}$ 来训练 ContextGNN 是不可行的，实践中我们依赖抽样 softmax 表述。这基本上把 ContextGNN 的目标转换成一个有 $C$ 个抽样类别的分类问题，这些类别在整个小批量上共享。所用的抽样过程基于优先队列：我们保证（1）所有真值物品，以及（2）给定小批量中被采样子图物品的并集，都被包含在类别集合中。然后，我们（3）根据均匀抽样过程，用来自该小批量所有子图之外的未探索物品，填满其余物品。实践中，我们在普通 GPU（15GB 显存）上把类别数 $C$ 扩展到 $\approx 1\mathrm{M}$ 没有问题，从而给 ContextGNN 丰富的学习信号。

## 5 实验评估

我们在来自不同领域的六个多样数据集上进行实验，包括十个不同的推荐任务。我们旨在回答以下研究问题：

<!-- 原 PDF 第 8 页 -->

- **Q1** ContextGNN 相对于它的每一个单独组件提供了哪些好处？
- **Q2** ContextGNN 相对于最先进的推荐系统方法表现如何？
- **Q3** 第 3 节的局部性分数如何影响 ContextGNN 的模型性能？
- **Q4** 与相关工作相比，ContextGNN 的效率和可扩展性如何？

我们的方法¹ 在 PyTorch（Paszke et al., 2019）中实现，使用 PyTorch Geometric（Fey & Lenssen, 2019）和 PyTorch Frame（Hu et al., 2024）库。

¹ 源代码：https://github.com/kumo-ai/ContextGNN

### 5.1 关系深度学习

**数据集描述。** 我们使用 RelBench（Robinson et al., 2024）中引入的推荐任务，它由八个不同的、现实且具有时间意识的推荐任务组成。RelBench 数据集含有丰富的关系结构，为推荐任务提供了具有挑战的环境。要取得强性能，方法必须能够利用多张关系表上的信息。所有数据集都可公开获取，并在领域、规模和稀疏性上各不相同。任务是在给定种子时间，给定一个用户，预测前 $k$ 个物品。我们使用的指标是平均精度均值（MAP）$@k$，其中 $k$ 按任务设定（越高越好）。

- **rel-amazon** 预测每个用户购买的不同物品列表（user-item-purchase）、给出 5 星的物品列表（user-item-rate），或给出详细评论的物品列表（user-item-review）。
- **rel-hm** 预测每个用户将购买的物品列表（user-item-purchase）。
- **rel-stack** 预测用户将评论的不同帖子列表（user-post-comment），或预测用户会把给定帖子链接到的帖子列表（post-post-related）。
- **rel-trial** 预测某种病情将有哪些申办方（condition-sponsor-run），或某个申办方是否会在某个机构开展试验（site-sponsor-run）。

**实验协议。** 我们将 ContextGNN 与以下基线方法比较：

- **LightGBM**（Ke et al., 2017）把用户特征和物品特征拼接起来，送入 LightGBM 决策树。
- **MultiVAE**（Liang et al., 2018）通过用户–物品交互矩阵，把变分自编码器扩展到面向隐式反馈的协同过滤。
- **GraphSAGE**（Hamilton et al., 2017）在用户侧和物品侧都使用异构 GNN，并通过内积解码器对所产生的嵌入排序。
- **NGCF**（Wang et al., 2019）扩展 GraphSAGE，在 GNN 内部同时传播浅层用户嵌入和物品嵌入。
- **NBFNet**（Zhu et al., 2021）采用成对 GNN 表示。这是 ContextGNN 中成对表示模型的骨干。
- **ShallowItem** 描述 ContextGNN 中的双塔模型，它通过内积解码器对用户 GNN 表示和浅层物品嵌入排序。

重要的是，所有基于 GNN 的模型都使用同一个 GNN 骨干，这保证训练过程的公平比较，且与底层模型实现无关。具体而言，我们使用 Robinson et al. (2024) 所引入的异构 GraphSAGE 变体：它利用一个 ResNet 表格模型（Gorishniy et al., 2021）把多模态输入数据编码到共享嵌入空间，再送入带有基于求和的邻居聚合的异构 GraphSAGE 变体（Hamilton et al., 2017）。所有实验中，优化使用 Adam（Kingma & Ba, 2015），最多 20 个 epoch。我们为每个任务调节的超参数是：（1）隐藏单元数 $\in \{32, 64, 128, 256, 512\}$，（2）批量大小 $\in \{256, 512, 1024\}$，（3）学习率 $\in \{0.001, 0.01\}$。

<!-- 原 PDF 第 9 页 -->

**表 2：** RelBench 上的推荐结果（MAP，越高越好，单位为 %）。表头方法从左到右为 LightGBM、MultiVAE、GraphSAGE、NGCF、NBFNet、ShallowItem、ContextGNN。平均一行按 PDF 原样抄录。表 2 的文本层没有 post-post-related 这一行。

| 数据集 | 任务 | 划分 | LightGBM | MultiVAE | GraphSAGE | NGCF | NBFNet | ShallowItem | ContextGNN |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| rel-amazon | user-item-purchase | val | 0.18 | 0.37 | 1.53 | 1.16 | 2.60 | 1.45 | 2.71 |
| rel-amazon | user-item-purchase | test | 0.16 | 0.23 | 0.74 | 0.88 | 2.06 | 0.56 | 2.93 |
| rel-amazon | user-item-rate | val | 0.22 | 0.34 | 1.42 | 1.22 | 1.61 | 1.62 | 2.68 |
| rel-amazon | user-item-rate | test | 0.17 | 0.24 | 0.87 | 0.86 | 1.24 | 0.74 | 2.25 |
| rel-amazon | user-item-review | val | 0.14 | 0.19 | 1.03 | 0.79 | 1.86 | 1.06 | 1.95 |
| rel-amazon | user-item-review | test | 0.09 | 0.10 | 0.47 | 0.55 | 1.57 | 0.40 | 1.63 |
| rel-hm | user-item-purchase | val | 0.44 | 0.33 | 0.92 | 0.81 | 2.64 | 0.49 | 3.00 |
| rel-hm | user-item-purchase | test | 0.38 | 0.28 | 0.80 | 0.75 | 2.81 | 0.40 | 2.93 |
| rel-stack | user-post-comment | val | 0.04 | 0.07 | 0.43 | 0.52 | 15.17 | 0.05 | 15.22 |
| rel-stack | user-post-comment | test | 0.04 | 0.01 | 0.11 | 0.13 | 12.72 | 0.03 | 13.34 |
| rel-trial | condition-sponsor-run | val | 4.88 | 2.59 | 3.12 | 3.71 | 11.33 | 0.88 | 11.59 |
| rel-trial | condition-sponsor-run | test | 4.82 | 2.47 | 2.89 | 3.88 | 11.36 | 0.85 | 11.65 |
| rel-trial | site-sponsor-run | val | 10.92 | 7.16 | 14.09 | 9.68 | 17.47 | 12.59 | 28.55 |
| rel-trial | site-sponsor-run | test | 8.40 | 6.17 | 10.70 | 6.54 | 19.06 | 10.66 | 28.02 |
| 平均（↑） |  | val | 2.30 | 1.46 | 2.82 | 2.24 | 7.56 | 2.35 | 9.22 |
| 平均（↑） |  | test | 2.01 | 1.29 | 2.08 | 1.72 | 7.71 | 1.81 | 9.23 |

**讨论。** 结果报告在表 2 中。我们通过把 ContextGNN 与其单独组件 NBFNet 和 ShallowItem 比较来回答 Q1，并通过把 ContextGNN 的性能与全部所报告基线联系起来来回答 Q2。

ContextGNN 优于所有竞争基线，常常以非常显著的幅度领先。值得注意的是，可以观察到双塔模型 MultiVAE、GraphSAGE 和 NGCF 都未能捕获 NBFNet 和 ContextGNN 能够利用的成对信号。这表明双塔表示的能力不足以捕获以高精度解决这些任务所需的细粒度成对依赖。在双塔 GNN 模型之中，GraphSAGE 与 NGCF 没有明确的胜者，表明浅层（用户）嵌入并不能显著推动改进（甚至可能妨碍性能，在具有内在时间动态的任务上尤其如此）。相对于最好的双塔基线，ContextGNN 平均提升结果 344%。

在基线之中，NBFNet 在所有任务上表现最好，而 ContextGNN 能够持续改进这些已经很强的结果。平均而言，ContextGNN 相对于 NBFNet 提升性能 20%，这强调了把「遥远」物品纳入排序过程的重要性——这一点是 NBFNet 在设计上忽略的。

我们自己的双塔 ShallowItem 模型与其他双塔 GNN 基线表现相当，尽管它只使用浅层物品信息，以便提高模型的总体效率。这支持如下假设：在大多数任务上，物品侧的深层 GNN 并不是特别有用，因为浅层嵌入可以同样好地捕获物品侧的大多数关键信号。然而，也存在特定情形，例如 rel-trial 数据集上的 condition-sponsor-run 任务，其中 ShallowItem 相对于 GraphSAGE 和 NGCF 表现较差。在这一任务上，物品侧的深层 GNN 对提升双塔模型的结果确实起着关键作用，而 ContextGNN 通过其成对表示模型捕获了这一点。最值得注意的结果出现在 rel-trial 数据集上的 site-sponsor-run 任务。这里，成对模型和双塔模型都取得了较强的初始结果。通过 ContextGNN 把这两种范式结合在一起，使最终性能提升约 100%，表明

<!-- 原 PDF 第 10 页 -->

ContextGNN 的每一个单独组件捕获的是正交信号。这些范式的融合产生一个在局部物品排序和遥远物品排序上都出色的排序模型，从而取得更优的总体性能。

为回答 Q3，我们现在分析局部性分数 $s_k^{[T, T+i)}$ 与 ContextGNN 性能之间的关系。我们观察到，在局部性分数较低的任务上，ContextGNN 相对于 NBFNet 的改进明显更高。这一观察在直观上是一致的，因为当局部性分数较低时，ContextGNN 在优化期间需要更重地依赖其双塔组件。具体而言，在局部性分数最低的任务上（例如来自 rel-amazon 和 rel-trial 数据集的 user-item-purchase、user-item-rate 和 site-sponsor-run 任务上的 0.168、0.170 和 0.229），ContextGNN 相对于 NBFNet 取得 42% 到 80% 的大幅性能增益。相反，对于局部性分数较高的任务（例如来自 rel-hm 和 rel-stack 数据集的 user-item-purchase、user-post-comment 和 post-post-related 任务上的 0.417、0.298 和 0.280），ContextGNN 相对于 NBFNet 的性能改进更为有限，范围在 3% 到 5%。这些发现强调了局部性分数对 NBFNet 性能的显著影响，而 ContextGNN 表现出稳健性，无论任务的具体特性如何都能取得突出的性能改进。

### 5.2 静态链接预测

**表 3：** Amazon-Book 上的结果。

| 模型 | Recall@20 | NDCG@20 |
| --- | --- | --- |
| NGCF (2019) | 0.0337 | 0.0261 |
| LightGCN (2020) | 0.0410 | 0.0318 |
| UltraGCN (2021) | 0.0681 | 0.0556 |
| LightGCL (2023) | 0.0585 | 0.0436 |
| SimGCL (2022) | 0.0478 | 0.0379 |
| SGL (2021) | 0.0468 | 0.0371 |
| ContextGNN | 0.0451 | 0.0377 |

虽然 ContextGNN 的主要焦点是在时序且异构的大规模真实用例上表现出色，它也可以以即插即用的方式用于任何链接预测任务。为加以验证，我们在 Amazon-Book 的静态链接预测任务上评估 ContextGNN（Wang et al., 2019）。这是一个小规模数据集，有 52,643 个用户和 91,599 个物品，不带输入特征，只考虑至少有十次交互的用户，并在与时间无关的、随机选出的 10% 交互上评估，见表 3。可以看到，ContextGNN 能够优于 NGCF 和 LightGCN，同时相对于例如 UltraGCN 或 LightGCL 略为落后。鉴于该数据集相对较小，基于 GNN 的推荐系统的许多进展集中在两个关键方向：（1）简化 GNN 架构，（2）纳入自监督学习技术。探索 ContextGNN 如何从更轻量的 GNN 骨干或互补的学习信号中受益，是未来研究的一个令人兴奋的方向。

### 5.3 时序的下一物品预测

**表 4：** IJCAI Contest 上的结果。

| 模型 | HR@1 | HR@5 | NDCG@5 | HR@10 | NDCG@10 |
| --- | --- | --- | --- | --- | --- |
| DeepFM (2017) | 0.138 | 0.332 | 0.244 | 0.469 | 0.290 |
| BERT4Rec (2019) | 0.141 | 0.356 | 0.261 | 0.467 | 0.297 |
| CHORUS (2020a) | 0.140 | 0.345 | 0.247 | 0.457 | 0.283 |
| HYREC (2020b) | 0.137 | 0.323 | 0.229 | 0.442 | 0.266 |
| NMTR (2019) | 0.141 | 0.360 | 0.254 | 0.481 | 0.304 |
| MATN (2020) | 0.142 | 0.375 | 0.273 | 0.489 | 0.309 |
| MBGCN (2020) | 0.137 | 0.332 | 0.228 | 0.463 | 0.277 |
| TGT (2022) | 0.148 | 0.399 | 0.293 | 0.519 | 0.330 |
| ContextGNN | 0.411 | 0.603 | 0.513 | 0.667 | 0.534 |

我们用 ContextGNN 在 IJCAI Contest 数据集上做时序的下一物品推荐（Xia et al., 2022）。这是评估序列推荐模型的一个常用数据集（Sun et al., 2019; Xia et al., 2020; 2022）。按照评估协议，我们在每个实体的 99 个抽样负例上报告 HitRate@$k$ 和 NDCG@$k$。值得注意的是，ContextGNN 擅长纳入多行为信号和时序信号，见表 4。我们观察到，ContextGNN 能够在这一任务的所有指标上优于全部基线（例如在 HitRate@1 上提升 170%）。

<!-- 原 PDF 第 11 页 -->

### 5.4 效率分析

**表 5：** 1,000 个优化步骤的运行时间（秒）。文本层将该基线行的字符从左到右抽成 NFBNET；全文其余处的对应模型名为 NBFNet。

| 模型 | rel-hm | rel-stack |
| --- | --- | --- |
| GraphSAGE（1 个负例） | 275s | 37s |
| GraphSAGE（10 个负例） | 293s | 44s |
| GraphSAGE（100 个负例） | OOM | OOM |
| NFBNET | 77s | 21s |
| ShallowItem | 92s | 22s |
| ContextGNN | 94s | 23s |

我们的混合 ContextGNN 模型被设计成：相对于它的两个组件各自独立运行，开销最小，因为模型的绝大部分在两种范式之间是共享的。为回答 Q4，我们报告不同模型达到 1,000 个优化步骤所需的运行时间（秒），见表 5。最重要的是，由于 ContextGNN 只需要一次 GNN 前向，它比任何双塔 GNN 都快一个非常显著的因子（也就是说，像 GraphSAGE 这样的双塔 GNN 需要在正例物品和负例物品上都运行 GNN）。特别是，当增加用于训练的负样本数量时，双塔 GNN 的扩展性非常差。对训练推荐系统而言，大量负例对于学习有判别力的特征很重要。然而，在最简单的情形中（每个正例配对一个负例配对），双塔 GNN 已经需要执行三次。ContextGNN 没有这一限制，并且可以在遇到 GPU 显存限制之前考虑多达 100 万个负例。

## 6 结论

我们提出了一种用于推荐的新颖混合 GNN 流水线，称为 ContextGNN。它可以通过成对表示为熟悉物品有效地把预测放进上下文，同时对探索性和意外发现式的物品回退到双塔表示。我们在真实数据集上评估了该架构，它持续改进了当时的最先进结果。

## 致谢

我们感谢整个 Kumo.AI 团队，他们为把 Hybrid-GNN 投入生产、服务数十个以上的客户以及任何规模的数据集提供了宝贵支持。特别感谢 Amitabha Roy、Myungwhan Kim 和 Federico Reyes Gómez 的有益讨论和反馈。

## 参考文献

J. S. Baras and G. Theodorakopoulos. 网络中的路径问题. Synthesis Lectures on Communication Networks, 3(1):1–77, 2010.

X. Cai, C. Huang, L. Xia, and X. Ren. LightGCL：简单而有效的推荐图对比学习. In ICLR, 2023.

M. G. Campana and F. Delmastro. 面向在线与移动社交网络的推荐系统：综述. Online Social Networks and Media, 3:75–97, 2017.

M. Fey and J. E. Lenssen. 用 PyTorch Geometric 做快速图表示学习. In ICLR Workshop on Representation Learning on Graphs and Manifolds, 2019.

M. Fey, W. Hu, K. Huang, J. E. Lenssen, R. Ranjan, J. Robinson, R. Ying, J. You, and J. Leskovec. 关系深度学习：关系数据库上的图表示学习. In ICML, 2024.

C. Gao, X. He, D. Gan, X. Chen, F. Feng, Y. Li, T. S. Chua, and D. Jin. 来自多行为数据的神经多任务推荐. In ICDE, 2019.

Yury Gorishniy, Ivan Rubachev, Valentin Khrulkov, and Artem Babenko. 再论表格数据的深度学习模型. In NeurIPS, 2021.

A. Grover and J. Leskovec. node2vec：网络上可扩展的特征学习. In SIGKDD, 2016.

H. Guo, R. Tang, Y. Ye, Z. Li, and X. He. DeepFM：基于因子分解机的神经网络，用于点击率预测. In ICJAI, 2017.

<!-- 原 PDF 第 12 页 -->

Xiangnan H. and Tat-Seng C. 面向稀疏预测分析的神经因子分解机. In SIGIR, 2017.

W. Hamilton, Z. Ying, and J. Leskovec. 大图上的归纳表示学习. In NIPS, 2017.

R. He and J. McAuley. 为稀疏序列推荐融合相似性模型与马尔可夫链. In ICDM, 2016.

X. He, L. Liao, H. Zhang, L. Nie, X. Hu, and T. Chua. 神经协同过滤. In WWW, 2017.

X. He, K. Deng, X. Wang, Y. Li, Y. Zhang, and M. Wang. LightGCN：简化并强化用于推荐的图卷积网络. In SIGIR, 2020.

Z. He, W. Liu, W. Guo, J. Qin, Y. Zhang, Y. Hu, and R. Tang. 推荐系统中的用户行为建模综述. In IJCAI, 2023.

W. Hu, Y. Yuan, Z. Zhang, A. Nitta, K. Cao, V. Kocijan, J. Leskovec, and M. Fey. PyTorch Frame：多模态表格学习的模块化框架. CoRR, abs/2404.00776, 2024.

Y. Hu, Y. Koren, and C. Volinsky. 隐式反馈数据集上的协同过滤. In ICDM, 2008.

S. Huang, F. Poursafaei, J. Danovitch, M. Fey, W. Hu, E. Rossi, J. Leskovec, M. Bronstein, G. Rabusseau, and R. Rabbany. 面向时序图机器学习的时序图基准. NeurIPS, 2023.

B. Jin, C. Gao, X. He, D. Jin, and Y. Li. 用图卷积网络做多行为推荐. In SIGIR, 2020.

J. Johnson, M. Douze, and H. Jégou. 用 GPU 做十亿规模的相似度搜索. IEEE Transactions on Big Data, 7(3):535–547, 2019.

W. Kang and J. McAuley. 自注意力序列推荐. In ICDM, 2018.

G. Ke, Q. Meng, T. Finley, T. Wang, W. Chen, W. Ma, Q. Ye, and T. Liu. LightGBM：一种高效的梯度提升决策树. In NIPS, 2017.

D. P. Kingma and J. L. Ba. Adam：一种随机优化方法. In ICLR, 2015.

T. N. Kipf and M. Welling. 变分图自编码器（原文标题写 Varitional graph auto-encoders）. In NIPS Workshop on Bayesian Deep Learning, 2016.

Y. Koren, R. Bell, and C. Volinsky. 推荐系统的矩阵分解技术. Computer, 42(8):30–37, 2009.

J. Li, P. Ren, Z. Chen, Z. Ren, T. Lian, and J. Ma. 基于神经注意力的会话推荐. New York, NY, USA, 2017.

Y. Li, K. Liu, R. Satapathy, S. Wang, and E. Cambria. 推荐系统的最新进展：综述. IEEE Computational Intelligence Magazine, 19:78–95, 2024.

D. Liang, R. G. Krishnan, M. D. Hoffman, and T. Jebara. 用于协同过滤的变分自编码器. In WWW, 2018.

Q. Liu, Y. Zeng, R. Mokhosi, and H. Zhang. STAMP：面向基于会话的推荐的短期注意力/记忆优先模型. In SIGKDD, 2018.

C. Ma, L. Ma, Y. Zhang, J. Sun, X. Liu, and M. Coates. 用于序列推荐的记忆增强图神经网络. In AAAI, 2020.

K. Mao, J. Zhu, X. Xiao, B. Lu, Z. Wang, and X. He. UltraGCN：用于推荐的图卷积网络的极致简化. In CIKM, 2021.

<!-- 原 PDF 第 13 页 -->

A. Mnih and R. R. Salakhutdinov. 概率矩阵分解. In NIPS, 2007.

A. Paszke, S. Gross, F. Massa, A. Lerer, J. Bradbury, G. Chanan, T. Killeen, Z. Lin, N. Gimelshein, L. Antiga, A. Desmaison, A. Kopf, E. Yang, Z. DeVito, M. Raison, A. Tejani, S. Chilamkurthy, B. Steiner, L. Fang, J. Bai, and S. Chintala. PyTorch：一种命令式、高性能的深度学习库. In NeurIPS, 2019.

B. Perozzi, R. Al-Rfou, and S. Skiena. DeepWalk：社会表示的在线学习. In SIGKDD, 2014.

S. Rendle, C. Freudenthaler, Z. Gantner, and L. Schmidt-Thieme. BPR：来自隐式反馈的贝叶斯个性化排序. In UAI, 2009.

S. Rendle, C. Freudenthaler, and L. Schmidt-Thieme. 为下一购物篮推荐分解个性化马尔可夫链. In WWW, 2010.

F. Ricci, L. Rokach, and B. Shapira. 推荐系统手册导论. In Recommender systems handbook. 2010.

J. Robinson, R. Ranjan, W. Hu, K. Huang, J. Han, A. Dobles, M. Fey, J. E. Lenssen, Y. Yuan, Z. Zhang, X. He, and J. Leskovec. RelBench：关系数据库上深度学习的基准. In NeurIPS, 2024.

M. Schlichtkrull, T. N. Kipf, P. Bloem, R. van den Berg, I. Titov, and M. Welling. 用图卷积网络建模关系数据. In The Semantic Web, 2018.

F. Sun, J. Liu, J. Wu, C. Pei, X. Lin, W. Ou, and P. Jiang. BERT4Rec：用来自 Transformer 的双向编码器表示做序列推荐. In CIKM, 2019.

K. K. Teru, E. G. Denis, and W. L. Hamilton. 通过子图推理做归纳关系预测. In ICML, 2020.

C. Wang, M. Zhang, W. Ma, Y. Liu, and Sh. Ma. 让它成为合唱：面向序列推荐的、具备知识与时间意识的物品建模. In SIGIR, 2020a.

J. Wang, K. Ding, L. Hong, H. Lui, and J. Caverlee. 用序列超图做下一物品推荐. In SIGIR, 2020b.

X. Wang, X. He, M. Wang, F. Feng, and T. Chua. 神经图协同过滤. In SIGIR, 2019.

J. Webber. 用图数据库技术支撑实时推荐. Technical report, Neo4J, 2021.

J. Wu, X. Wang, F. Feng, X. He, L. Chen, J. Lian, and X. Xie. 用于推荐的自监督图学习. In SIGIR, 2021.

L. Wu, Z. Zheng, Z. Qiu, H. Wang, H. Gu, T. Shen, C. Qin, C. Zhu, H. Zhu, Q. Liu, H. Xiong, and E. Chen. 面向推荐的大语言模型综述. CoRR, abs/2305.19860, 2023.

L. Xia, C. Huang, Y. Xu, P. Dai, B. Zhang, and L. Bo. 通过记忆增强 Transformer 网络为推荐学习多重行为关系. In SIGIR, 2020.

L. Xia, C. Huang, Y. Xu, and J. Pei. 用时序图 Transformer 做多行为序列推荐. In TKDE, 2022.

Y. Yang, C. Huang, L. Xia, Y. Liang, Y. Yu, and C. Li. 用于序列推荐的多行为超图增强 Transformer. In SIGKDD, 2022.

J. You, R. Ying, and J. Leskovec. 位置感知图神经网络. In ICML, 2019.

J. You, J. M. Gomes-Selman, R. Ying, and J. Leskovec. 身份感知图神经网络. In AAAI, 2021.

<!-- 原 PDF 第 14 页 -->

J. Yu, H. Yin, X. Xia, T. Chen, L. Cui, and Q. V. H. Nguyen. 图增强是必要的吗？用于推荐的简单图对比学习. In SIGIR, 2022.

H. Zeng, M. Zhang, Y. Xia, A. Srivastava, A. Malevich, R. Kannan, V. Prasanna, L. Jin, and R. Chen. 解耦图神经网络的深度与范围. In NeurIPS, 2021.

M. Zhang and Y. Chen. 基于图神经网络的链接预测. In NIPS, 2018.

Z. Zhu, Z. Zhang, L. P. Xhonneux, and J. Tang. 神经 Bellman-Ford 网络：面向链接预测的通用图神经网络框架（原文 Bellmann-Ford）. In NeurIPS, 2021.

<!-- 译完 -->
