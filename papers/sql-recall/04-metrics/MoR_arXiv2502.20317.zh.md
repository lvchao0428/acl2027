原文件名：MoR_arXiv2502.20317.pdf

原标题：Mixture of Structural-and-Textual Retrieval over Text-rich Graph Knowledge Bases

中文标题：面向文本丰富图知识库的结构与文本混合检索

作者：Yongjia Lei, Haoyu Han, Ryan A. Rossi, Franck Dernoncourt, Nedim Lipka, Mahantesh M Halappanavar, Jiliang Tang, Yu Wang

会议或 arXiv：arXiv:2502.20317v4 [cs.LG] 1 Jun 2025

<!-- 原 PDF 第 1 页 -->

# 面向文本丰富图知识库的结构与文本混合检索

Yongjia Lei^1，Haoyu Han^2，Ryan A. Rossi^3，Franck Dernoncourt^3，Nedim Lipka^3，Mahantesh M Halappanavar^4，Jiliang Tang^2，Yu Wang^1

^1 University of Oregon，^2 Michigan State University，^3 Adobe Research，^4 Pacific Northwest National Laboratory

{yuwang, yongjia}@uoregon.edu，{hanhaoy1, tangjili}@msu.edu

{ryrossi, dernonco, lipka}@adobe.com，hala@pnnl.gov

## 摘要

文本丰富图知识库（Text-rich Graph Knowledge Bases，TG-KB）通过同时提供文本知识与结构知识，对回答查询已变得日益关键。然而，现有检索方法常常把这两类知识孤立地取出，没有考虑它们之间的相互增强；一些混合方法甚至在邻居聚合之后完全绕开结构检索。为填补这一空白，我们提出结构与文本混合检索（Mixture of Structural-and-Textual Retrieval，MoR），通过规划—推理—组织（Planning-Reasoning-Organizing）框架来检索这两类知识。在规划阶段，MoR 生成文本规划图，刻画回答查询的逻辑。沿着规划图，在推理阶段，MoR 交织结构遍历与文本匹配，从 TG-KB 中得到候选。在组织阶段，MoR 再按结构轨迹对取回的候选排序。大量实验表明，MoR 在协调结构检索与文本检索方面具有优势，并得到若干发现，包括不同查询逻辑上检索性能不均衡，以及把结构轨迹纳入候选重排序的收益。代码见 https://github.com/Yoega/MoR 。

## 1 引言

文本丰富图知识库（TG-KB）以结构化方式表示文本文档，因而普遍同时存储文本知识与结构知识（Jin et al., 2024b）。例如，学者从论文管理系统中检索相关研究以推进科学发现，其中节点表示论文，边表示引用（Lu et al., 2024）。随着大语言模型（LLM）驱动的生成器在语言理解与生成上接近人类智能，从 TG-KB 中检索支撑知识、用以把生成情境化并落地，对于正确回答查询已变得越来越关键（Gao et al., 2023b; Ni et al., 2025）。

**图 1：**（a）文本检索与结构检索。（b）检索方法的有效性在不同 TG-KB 上有所不同。（c）在同一 TG-KB 内，由文本检索处理的查询（即 $Q_{\text{Text}}$）与由结构检索处理的查询（即 $Q_{\text{Struct}}$）既有重叠，也有各自独有的部分。

图中可见的查询示例为：Publications by Point Park University authors on stellar populations in tidal tails（Point Park University 作者关于潮汐尾中恒星族群的论文）。图中标注包括论文标题 “A tale of two tails: exploring stellar populations in the tidal tails of NGC 3256” 及其摘要片段，以及关系 “$Q_{\text{Text}} \neq Q_{\text{Struct}}$”、“$|Q_{\text{MoR}}| > |Q_{\text{Text}} \cup Q_{\text{Struct}}|$”，并标明为 MAG 上的检索结果。图中还出现标注 $Q_{\text{MoR}}$、$Q_{\text{Struct}}$、$Q_{\text{Text}}$ 及若干计数（抽取到的数字包括 306、552、74、23、50、653、102）；各数字与区域的对应关系见原 PDF 第 1 页图 1。图中还标有 Author、Field of Study、Paper、Institution，以及 Textual Retrieval 与 Structural Retrieval。

由于 TG-KB 中的支撑知识通常同时以文本形式和结构形式出现（Kolomiyets and Moens, 2011; Jin et al., 2024b），检索方法应当如图 1（a）所示，针对两种形式都有效地加以适配。文本检索方法根据与给定查询的相似度检索文本知识，例如已索引的文档，可大致分为词法方法（如 BM25）和语义方法（如 Contriever）（Karpukhin et al., 2020; Izacard et al., 2022）。结构检索方法通过图遍历与图机器学习，检索结构知识，例如邻居实体（Jiang et al., 2023; Edge et al., 2024; Wang et al., 2024）（Yasunaga et al., 2021; Tian et al., 2024）。尽管文本检索与结构检索都已取得进展，它们往往被独立使用，未能相互增强。如图 1（b）所示，无论是顺着查询逻辑结构进行的结构检索，还是进行 Top-K BM25 匹配的文本检索，都不能在 Amazon 与 MAG 两个数据集上同时取得更好的性能。

<!-- 原 PDF 第 2 页 -->

为了从 TG-KB 中有效检索文本知识与结构知识，近期工作（Xia et al., 2024; Li et al., 2024）把邻居文档聚合起来，把结构知识融进文本叙述，然后再做文本检索。其中 Xia et al.（2024）按关系过滤无关邻居，Li et al.（2024）按字段对邻居做加权聚合。然而仍有三个挑战。第一，改写聚合后的邻居需要频繁调用 LLM，对邻居数量呈指数增长的长文档而言，资源开销过大。第二，人类用来形成逻辑计划的结构信号，在邻居聚合之后被完全丢弃。第三，僵硬的邻居聚合忽略了不同查询、不同 TG-KB 对结构知识与文本知识的不同需求。即便在同一 TG-KB 内，例如图 1（c）中的 MAG，由文本检索回答的查询（即 $Q_{\text{Text}}$）也不同于由结构检索回答的查询（即 $Q_{\text{Struct}}$）。

为应对上述三个挑战，我们把混合专家的思想注入检索设计，并提出图 2 中的结构与文本混合检索（MoR）。MoR 首先用规划模块生成规划图，以勾勒查询逻辑并保留结构信号，同时不必改写聚合后的邻居，从而克服第一与第二项挑战。接着，MoR 在推理模块中交错进行结构遍历与文本匹配，使两种检索相互增强。最后，MoR 在组织模块中设计结构感知重排序器，自适应地调整所检索文本知识与结构知识的重要性，从而应对第三项挑战。经由规划—推理—组织，MoR 根据查询的逻辑结构，有选择地检索结构知识与文本知识。我们的主要贡献如下：

- **通过文本图生成进行规划：** 我们将检索规划定义为生成文本图，用以勾勒逻辑结构，即用于识别与查询相关实体的计划。
- **通过结构与文本混合遍历进行推理：** 我们设计一种混合遍历，把文本匹配与结构遍历交织起来，按照所生成计划描绘的查询逻辑结构检索知识。
- **通过结构感知重排序进行组织：** 在混合遍历得到候选之后，我们提出结构感知重排序，根据遍历轨迹选出 Top-K 候选。

## 2 预备知识

**记号：** 文本丰富图知识库（TG-KB）$\mathcal{B}$ 通常由一组相互连接的节点 $V$ 构成；每个节点 $v \in V$ 关联其对应文档 $D_v \in \mathcal{D}$ 以及类别 $E_v \in \mathcal{E}$。当为回答给定查询 $Q \in \mathcal{Q}$ 而从 $\mathcal{B}$ 中检索带有支撑文档的节点时，我们通常遵循某种依据，该依据封装了该查询的底层逻辑（Xu et al., 2024; Xue et al., 2024），并可用一张文本属性规划图 $G$ 来刻画。在许多已有工作中（Jin et al., 2024a; Wu et al.），该规划图通常可分解为多条推理路径

$$
G = \{P_i\}_{i=1}^{|G|}
$$

其中第 $i$ 条推理路径

$$
P_i = (p_{i1} \rightarrow p_{i2} \rightarrow \ldots \rightarrow p_{iL_i})
$$

是一条长度为 $L_i$ 的独特推理链，编码一种独特逻辑；第 $j$ 个节点 $p_{ij}$ 对应于 $\mathcal{B}$ 中的一个实体，具有自身类别 $E_{p_{ij}}$，以及从查询中抽出的文本限制 $T_{p_{ij}}$。例如，在图 1（a）中，查询 “Publications by Point...” 的规划图有两条路径，即 $P_1 = (\text{Institution} \rightarrow \text{Author} \rightarrow \text{Paper})$ 与 $P_2 = (\text{Field-of-Study} \rightarrow \text{Paper})$，其中 $P_1$ 上第一个节点的类别与文本限制分别为 $E_{p_{11}} = \text{Institution}$、$T_{p_{11}} = \langle \text{Point Park University} \rangle$。完整记号汇总于附录 A 的表 6。

**问题设定：** 在上述记号下，所研究的问题是检索实体集合 $C \subseteq V$，以回答给定查询 $Q$。

**文本检索**根据查询与文档双方的文本信号检索候选。一种常见策略是从全部文档 $\mathcal{D}$ 中检索与查询 $Q$ 具有 Top-K 文本相似度的候选 $\tilde{C}$，相似度由词法或语义相似度衡量（Vijaymeena and Kavitha, 2016）。MoR 中使用的文本检索，通过把文档与查询中的文本描述相匹配来检索文档，例如匹配图 1 中所示的 “stellar populations in tidal tails”。

**结构检索**通过对结构化数据库（如知识图谱和 SQL）施加预定规则来检索候选（Guo et al., 2023）。常见策略包括基于图的遍历（如 BFS、DFS）和规则获取（Jiang et al., 2023）。具体而言，MoR 通过遍历所生成规划图中特定类别的邻居来进行结构检索。例如，在图 1（a）中，我们的结构检索只能遍历 Author 的 “Paper” 类型邻居。

<!-- 原 PDF 第 3 页 -->

**图 2：** 我们的 MoR 框架包含：用于生成规划图的规划模块、用于进行混合遍历的推理模块，以及用于对检索候选重排序的组织模块。

图中示例查询为：Publications by Point Park University authors on stellar populations in tidal tails。规划图包含文本描述、类别 Paper、Institution、Author、Field of Study，以及限制 $\langle$Point Park University$\rangle$、$\langle$Stellar populations$\rangle$。两条推理路径为：Path 1: Institution $\rightarrow$ Author $\rightarrow$ Paper；Path 2: Field of Study $\rightarrow$ Paper。图中还标有结构检索、文本检索、邻居节点、结构感知重排序、Top-K 与逻辑流。

## 3 框架

简言之，我们把 MoR 表述为：在 TG-KB $\mathcal{B}$ 上，给定用户输入查询 $Q$ 时，检索候选 $C$ 的条件分布 $P_{\Theta}(C \mid Q, \mathcal{B})$。它进一步分解为三个分布，分别对应我们提出的三个模块：通过生成文本属性规划图 $G$ 进行规划；通过结构与文本混合遍历、沿着所生成规划图 $G$ 得到中间候选 $\tilde{C}$ 进行推理；通过对所得候选 $\tilde{C}$ 施加结构感知重排序、得到最终候选 $C$ 进行组织：

$$
\begin{aligned}
P_{\Theta}(C \mid Q, \mathcal{B})
&= \sum_{G \in \mathcal{G}}
\Bigg[
\sum_{\tilde{C} \in \mathcal{C}}
\underbrace{P_{\Theta_3}(C \mid \tilde{C}, G, Q, \mathcal{B})}_{\text{组织}}
\times
\underbrace{P_{\Theta_2}(\tilde{C} \mid G, Q, \mathcal{B})}_{\text{推理}}
\Bigg]
\times
\underbrace{P_{\Theta_1}(G \mid Q, \mathcal{B})}_{\text{规划}}
\end{aligned}
$$

其中 $P_{\Theta_1}(G \mid Q, \mathcal{B})$ 是在给定输入查询 $Q$ 与 TG-KB $\mathcal{B}$ 时生成文本属性规划图 $G$ 的概率分布；$P_{\Theta_2}(\tilde{C} \mid G, Q, \mathcal{B})$ 是在给定规划图 $G$ 与查询 $Q$ 时、经由我们的混合遍历检索中间候选 $\tilde{C}$ 的概率分布；$P_{\Theta_3}(C \mid \tilde{C}, G, Q, \mathcal{B})$ 是对中间候选重排序、使 Top-K 位置构成真实实体 $C$ 的概率分布。$\mathcal{G}/\mathcal{C}$ 表示全部可能规划图的空间，以及 TG-KB $\mathcal{B}$ 中全部节点 $V$ 上所有大小为 $K$ 的候选节点集合的全部可能配置。总目标是最大化每个输入查询 $Q \in \mathcal{Q}$ 检索到真实候选 $C$ 的似然：

$$
\Theta^{*} = \arg\max_{\Theta} \prod_{Q \in \mathcal{Q}} P_{\Theta}(C \mid Q, \mathcal{B})
\tag{1}
$$

按照上述范式，我们接下来介绍三个组成部分：第 3.1 节通过文本图生成进行规划，第 3.2 节通过混合遍历进行推理，第 3.3 节通过结构感知重排序进行组织。

### 3.1 通过文本图生成进行规划

为了有效地在查询的底层逻辑上进行推理并回答查询，我们提出一个规划模块，构建规划图以捕捉其底层逻辑结构。与依赖僵硬启发式的传统方法（例如知识图谱中的最短路径检索（Luo et al.; Delile et al., 2024））或逐步提示 LLM（会带来很高的计算代价（Sun et al., 2023; Wang et al., 2024））不同，我们的方法一次性生成整张规划图，从而消除反复的 LLM 调用。更重要的是，由于规划图把编码查询特定约束的实体限制、与捕捉更广逻辑结构的实体类别整合在一起，MoR 可以泛化已学到的模式，并高效适应具有相同底层逻辑的新查询。例如，任何形如 “与 $\langle$institution$\rangle$ 相关联、且属于 $\langle$field$\rangle$ 领域的论文” 的查询，都与图 2 中的查询共享相同模式。下面我们先形式化规划图，再优化其生成。

#### 3.1.1 规划图表述

规划图 $G$ 是一种结构化表示，其中节点表示实体，边表示它们的逻辑关系。每个实体同时关联一个类别和一项查询特定限制。例如，给定查询 “Can you give me publications by Point Park University authors on stellar populations in tidal tails”，生成的规划图为：

$$
G = \big(\text{Institution}\langle\text{Point Park University}\rangle \rightarrow \text{Author} \rightarrow \text{Paper} \leftarrow \text{Field-of-Study}\langle\text{Stellar Population}\rangle\big)
$$

其中 Institution、Author、Paper、Field-of-Study 为类别，$\langle$Point Park University$\rangle$、$\langle$Stellar Populations$\rangle$ 为限制。注意，我们规划图中的边也可以具有不同类别。例如，在生物医学 TG-KB 中，Disease 与 Drug 实体之间的关系可以是 Indication 或 Contra-indication（Wu et al.），从而在关系上增加更细的语义区分。

<!-- 原 PDF 第 4 页 -->

#### 3.1.2 规划图优化

为确保所生成的规划图捕捉查询逻辑，我们训练一个文本图生成器，以最大化在给定查询时生成真实规划图的似然。形式化地，给定查询与规划图训练对的联合分布 $P^{\text{Train}}_{Q \times G}$，我们通过求解下式来优化规划模块 $P_{\Theta_1}$：

$$
\arg\max_{\Theta_1}\ \mathbb{E}_{(Q,G)\sim P^{\text{Train}}_{Q \times G}} \log P_{\Theta_1}(G \mid Q, \mathcal{B})
\tag{2}
$$

为避免规划图候选随指数增长而带来的组合爆炸（You et al.），我们把每张规划图分解为多条推理路径 $G = \{P_i\}_{i=1}^{|G|}$。每条路径 $P_i = (p_{i1} \rightarrow \ldots \rightarrow p_{iL_i})$ 表示一条独特的推理链，其中节点 $p_{ij}$ 表示 TG-KB 中的一个实体，它与文本类别 $E_{p_{ij}}$ 相同，并满足来自查询的限制 $T_{p_{ij}}$。鉴于这些分解后的推理路径具有序列性质和文本格式，可以自然地使用 LLM 作为规划图生成器：它通过在前序词元 $t_{<j}$、查询 $Q$ 与 TG-KB $\mathcal{B}$ 的条件下预测第 $j$ 个词元 $t_j$，进行下一词元预测：

$$
P_{\Theta_1}(G \mid Q) = \prod_{j=1}^{n} P_{\Theta_1}(t_j \mid t_{<j}, Q, \mathcal{B}).
\tag{3}
$$

注意，我们提出的规划图生成器并不限于 LLM。任何同时保留结构依赖与文本关联的图生成模型都可以使用（Zhu et al.）。

### 3.2 通过混合遍历进行推理

沿着上述规划图 $G = \{P_i\}_{i=1}^{|G|}$ 的推理路径，推理模块通过交织邻居获取与文本匹配来进行混合遍历，形成中间候选 $\tilde{C}$。下面分别介绍。

#### 3.2.1 结构遍历

按照第 2 节的定义，结构检索遵循预定规则进行知识检索。这里我们把这些预定规则设为迭代地执行逐层广度优先搜索，遍历那些类别与推理路径中类别对齐的邻居实体。具体而言，在规划路径 $P_i$ 的第 $l$ 步进行推理时，我们对上一层候选集合中的每个节点 $\forall v \in \tilde{C}^{l-1}_{i}$ 进行检查，并取其邻居 $\forall u \in N_v$ 中与推理路径上对应节点 $p_{il}$ 类别相同者（即 $E_u = E_{p_{il}}$），可形式化为：

$$
\tilde{C}^{l,\text{Struct}}_{i}
= \bigcup_{v \in \tilde{C}^{l-1}_{i}}
\{u \mid u \in N_v,\ E_u = E_{p_{il}}\}
\tag{4}
$$

其中 $\tilde{C}^{l,\text{Struct}}_{i}$ 表示按照路径 $P_i$、在第 $l$ 个推理步上经结构检索得到的实体集合；$E_u = E_{p_{il}}$ 保证被遍历邻居 $u$ 的类别与规划图所规定的对应实体类别路线相匹配，这与基于规则的结构检索的性质一致。注意，第一层的种子候选 $\tilde{C}^{1,\text{Struct}}_{i}$ 由文本匹配检索 Top-K 实体来初始化，即 $\tilde{C}^{1,\text{Struct}}_{i} = \tilde{C}^{1,\text{Text}}_{i}$，文本匹配将在下一小节介绍。

#### 3.2.2 文本匹配

除检索结构知识外，MoR 还通过文本匹配检索文本知识，即根据与查询的文本相似度检索候选。对于沿推理路径 $P_i$、处于第 $l$ 个推理步的每个推理节点 $p_{il}$，我们把查询与 $p_{il}$ 的文本限制拼接起来，即 $Q' = [Q : T_{p_{il}}]$，然后计算它与 TG-KB 中节点文档的文本相似度，即 $\phi(Q', D_v)$，$\forall v \in V$，最后检索得分 Top-K 的候选：

$$
\tilde{C}^{l,\text{Text}}_{i}
= \mathrm{TopK}\big(\{v \mid v \in V,\ E_v = E_{p_{il}}\},\ \phi(Q', D_v)\big)
\tag{5}
$$

把结构遍历与文本匹配的候选合在一起，路径 $P_i$ 第 $l$ 步的最终候选形成为：

$$
\tilde{C}^{l}_{i}
= \tilde{C}^{l,\text{Struct}}_{i} \cup \tilde{C}^{l,\text{Text}}_{i},
\quad \forall l \in \{1, 2, \ldots, L_i\}
\tag{6}
$$

整合后的候选 $\tilde{C}^{l}_{i}$ 作为种子节点，初始化下一轮由规划图引导的结构遍历与文本匹配。这在结构知识与文本知识之间形成相互增强，因为此前检索到的两类知识都可以为下一轮结构知识或文本知识的检索提供信息。

我们对每条推理路径 $P_i \in G$ 迭代地进行混合遍历，并通过取交集把检索到的实体整合在一起，即 $\tilde{C} = \bigcap_{P_i \in G} \tilde{C}^{L_i}_{i}$。这符合如下事实：候选应当同时满足所有推理路径所规定的逻辑路线。注意，混合图遍历不涉及训练，即 $P_{\Theta_2}(\tilde{C} \mid G, Q, \mathcal{B}) = P(\tilde{C} \mid G, Q, \mathcal{B})$。未来工作可以探索用来自智能体—环境交互的奖励来优化图遍历（Nguyen et al., 2024）。

<!-- 原 PDF 第 5 页 -->

### 3.3 通过结构感知重排序进行组织

尽管第 3.2 节检索到的候选严格遵循规划图给出的预定规则，候选数量之大与现实约束并不相符（例如 Top-20 的检索预算（Zeng et al., 2024）），甚至可能给下游执行器带来困难，例如 LLM 的长上下文挑战。为了更好地模拟人类推理——收集多条线索、对照查询加以分析、并综合成连贯答案——我们提出结构感知重排序器，用以组织并重排候选 $\tilde{C}$，并选出 Top-K 作为最终检索答案 $C$。我们的重排序器并不只依赖文本特征（Hu et al., 2019），而是根据第 3.2 节混合遍历所得到的结构轨迹特征赋予排序分数，从而在重排序中同时利用结构知识与文本知识。

此前，$\tilde{C}$ 被定义为中间检索实体。为了在重排序中考虑结构特征，我们把 $\tilde{C}$ 中每个检索候选与其在推理模块中得到的对应遍历轨迹配对。具体而言，每条长度为 $L_i$ 的轨迹 $P_i$ 具有三类属性：

- **文本指纹（Textual Fingerprint，TF）：** 扩展查询与路径上每个节点之间相似度分数的拼接。公式抽取不完整，见原 PDF 第 5 页。抽出的原串为：`Li l=1 ϕ(Q′, Dpil)`。
- **结构指纹（Structural Fingerprint，SF）：** 路径上每一步节点类别的拼接。公式抽取不完整，见原 PDF 第 5 页。抽出的原串为：`Li l=1 Epil`。
- **遍历标识（Traversal Identifier，TI）：** 标明每一步使用结构检索还是文本检索的指示符的拼接。公式抽取不完整，见原 PDF 第 5 页。抽出的原串为：`Li l=1 Ipil`。

然后我们在这些轨迹上用交叉熵损失训练重排序器。对于训练查询 $Q$ 及其关联的候选轨迹 $P_i$，损失计算如下：

$$
\mathcal{L}_{\Theta_3}
= -\sum_{(P_i, Q) \in \tilde{C}} \sum_{j=1}^{2}
y^{i}_{j} \log\big(\sigma(f(\cdots))_{j}\big)
\tag{7}
$$

公式抽取不完整，见原 PDF 第 5 页。拼接算子未抽出。$f(\cdot)$ 的输入由三段以冒号分隔的指纹组成，原文分别标注为 Structural Fingerprint、Textual Fingerprint、Traversal Identifier。抽出的原串为：`Li l=1 Epil` : `Li l=1 ϕ(Q′, Dpil)` : `Li l=1 Ipil`，外层为 `yi j log(σ(f( ... ))j)`，并对 $(P_i,Q)\in \tilde{C}$ 以及 $j=1$ 到 $2$ 求和。

其中 $f(\cdot)$ 是重排序器，为每个 $(Q, P_i)$ 对产生一个分数；$\sigma(\cdot)$ 表示 softmax 函数；$y^{i}_{j} \in \{0, 1\}$ 表示第 $i$ 个候选对 $Q$ 而言是正确（正）匹配还是错误（负）匹配。这一形式鼓励重排序器给正轨迹赋予更高分数，从而提升排序性能。

## 4 实验

### 4.1 实验设置

我们简要介绍用于验证所提出 MoR 的实验设置，包括数据集与基线、实现细节和评价指标。更多细节见附录 B。

**数据集与基线：** 我们使用来自 STaRK（Wu et al.）的三个 TG-KB，覆盖三个知识领域，包括电子商务产品（Amazon）、学术论文（MAG）和生物医学（Prime）。我们将 MoR 与 Wu et al. 建立的基线比较，并把它们分为基于文本、基于结构和混合三类。我们也比较了面向 TG-KB 的更新近的混合检索方法，如 KAR（Xia et al., 2024）和 MFAR$^{*}$（Li et al., 2024）。

**实现细节：** 为增强规划模块的规划能力，我们在 1000 条采样查询及其对应的真实规划图上微调 Llama 3.2（3B），将其作为文本图生成器。在缺少真实标注时，我们用 LLM 合成它们。对于 Prime 数据集，我们凭经验发现，由于缺乏生物医学领域知识（Shen et al.），直接提示 LLM 很难生成准确的规划图。因此我们采用另一种做法。首先，我们指示 LLM 从每条查询中抽取三元组，然后通过合并共享实体的三元组来构建规划图。在混合遍历中，文本匹配可以用任何词法或语义方法实现。在本研究中，我们对 Amazon 和 MAG 使用 BM25，并微调一个 Contriever，以补充 Prime 所需的生物医学知识。为初始化结构遍历，我们用文本匹配定位与查询最相关的前 5 个节点作为种子。此外，在每一层，我们纳入经由文本匹配检索到的前 10 个节点，并把它们追加到当前候选集合，供下一轮遍历使用。需要指出的是，由于 LLM 的不确定性，生成的规划图可能无效。在这种情况下，我们将直接进行文本匹配来检索候选。对于不带重排序器的消融，我们采用 Ada-002（Wu et al.），以余弦相似度作为打分器对候选排序，从而评估性能。

**评价指标：** 我们遵循 Wu et al. 进行评测，报告 Hit@1（H@1）、Hit@5（H@5）、Recall@20（R@20）以及平均倒数排名 MRR，以在全谱上评估。

<!-- 原 PDF 第 6 页 -->

**表 1：** 在 Amazon、MAG 与 Prime 数据集上，将不同检索方法与我们提出的 MoR 及其消融进行比较。最优结果与次优结果在原文中分别以粗体和下划线标出；单元格的粗体与下划线格式未被抽出，见原 PDF 第 6 页。总体而言，MoR 取得最好的性能。MFAR$^{*}$ 表示（Li et al., 2024）中提出的最佳模型变体。

| 类别 | 检索基线 | 数据集 | Hit@1 | Hit@5 | Recall@20 | MRR |
| --- | --- | --- | --- | --- | --- | --- |
| 文本 | BM25（Wu et al.） | AMAZON | 44.94 | 67.42 | 53.77 | 55.30 |
| 文本 | BM25（Wu et al.） | MAG | 25.85 | 45.25 | 45.69 | 34.91 |
| 文本 | BM25（Wu et al.） | PRIME | 12.75 | 27.92 | 31.25 | 19.84 |
| 文本 | BM25（Wu et al.） | AVERAGE | 27.85 | 46.86 | 43.57 | 36.68 |
| 文本 | Ada-002（Wu et al.） | AMAZON | 39.16 | 62.73 | 53.29 | 50.35 |
| 文本 | Ada-002（Wu et al.） | MAG | 29.08 | 49.61 | 48.36 | 38.62 |
| 文本 | Ada-002（Wu et al.） | PRIME | 12.63 | 31.49 | 36.00 | 21.41 |
| 文本 | Ada-002（Wu et al.） | AVERAGE | 26.96 | 47.94 | 45.88 | 36.79 |
| 文本 | Multi-ada-002（Wu et al.） | AMAZON | 40.07 | 64.98 | 55.12 | 51.55 |
| 文本 | Multi-ada-002（Wu et al.） | MAG | 25.92 | 50.43 | 50.80 | 36.94 |
| 文本 | Multi-ada-002（Wu et al.） | PRIME | 15.10 | 33.56 | 38.05 | 23.49 |
| 文本 | Multi-ada-002（Wu et al.） | AVERAGE | 27.03 | 49.66 | 47.99 | 37.33 |
| 文本 | DPR（Karpukhin et al., 2020） | AMAZON | 15.29 | 47.93 | 44.49 | 30.20 |
| 文本 | DPR（Karpukhin et al., 2020） | MAG | 10.51 | 35.23 | 42.11 | 21.34 |
| 文本 | DPR（Karpukhin et al., 2020） | PRIME | 4.46 | 21.85 | 30.13 | 12.38 |
| 文本 | DPR（Karpukhin et al., 2020） | AVERAGE | 10.09 | 35.00 | 38.91 | 21.31 |
| 结构（KG） | QAGNN（Yasunaga et al., 2021） | AMAZON | 26.56 | 50.01 | 52.05 | 37.75 |
| 结构（KG） | QAGNN（Yasunaga et al., 2021） | MAG | 12.88 | 39.01 | 46.97 | 29.12 |
| 结构（KG） | QAGNN（Yasunaga et al., 2021） | PRIME | 8.85 | 21.35 | 29.63 | 14.73 |
| 结构（KG） | QAGNN（Yasunaga et al., 2021） | AVERAGE | 16.10 | 36.79 | 42.88 | 27.20 |
| 结构（KG） | ToG（Sun et al., 2023） | AMAZON | - | - | - | - |
| 结构（KG） | ToG（Sun et al., 2023） | MAG | 13.16 | 16.17 | 11.30 | 14.18 |
| 结构（KG） | ToG（Sun et al., 2023） | PRIME | 6.07 | 15.71 | 13.07 | 10.17 |
| 结构（KG） | ToG（Sun et al., 2023） | AVERAGE | 9.62 | 15.94 | 12.18 | 12.18 |
| 混合 | AvaTaR（Wu et al., 2025） | AMAZON | 49.87 | 69.16 | 60.57 | 58.70 |
| 混合 | AvaTaR（Wu et al., 2025） | MAG | 44.36 | 59.66 | 50.63 | 51.15 |
| 混合 | AvaTaR（Wu et al., 2025） | PRIME | 18.44 | 36.73 | 39.31 | 26.73 |
| 混合 | AvaTaR（Wu et al., 2025） | AVERAGE | 37.56 | 55.18 | 50.17 | 45.53 |
| 混合 | KAR（Xia et al., 2024） | AMAZON | 54.20 | 68.70 | 57.24 | 61.29 |
| 混合 | KAR（Xia et al., 2024） | MAG | 50.47 | 69.57 | 60.28 | 58.65 |
| 混合 | KAR（Xia et al., 2024） | PRIME | 30.35 | 49.30 | 50.81 | 39.22 |
| 混合 | KAR（Xia et al., 2024） | AVERAGE | 45.01 | 62.52 | 56.11 | 53.05 |
| 混合 | MFAR$^{*}$（Li et al., 2024） | AMAZON | 41.20 | 70.00 | 58.50 | 54.20 |
| 混合 | MFAR$^{*}$（Li et al., 2024） | MAG | 49.00 | 69.60 | 71.70 | 58.20 |
| 混合 | MFAR$^{*}$（Li et al., 2024） | PRIME | 40.90 | 62.80 | 68.30 | 51.20 |
| 混合 | MFAR$^{*}$（Li et al., 2024） | AVERAGE | 43.70 | 67.47 | 66.17 | 54.53 |
| 混合 | HYBGRAG（Lee et al., 2024） | AMAZON | - | - | - | - |
| 混合 | HYBGRAG（Lee et al., 2024） | MAG | 65.40 | 75.31 | 65.70 | 69.80 |
| 混合 | HYBGRAG（Lee et al., 2024） | PRIME | 28.56 | 41.38 | 43.58 | 34.49 |
| 混合 | HYBGRAG（Lee et al., 2024） | AVERAGE | 50.91 | 58.35 | 54.64 | 52.15 |
| 混合 | MoR | AMAZON | 52.19 | 74.65 | 59.92 | 62.24 |
| 混合 | MoR | MAG | 58.19 | 78.34 | 75.01 | 67.14 |
| 混合 | MoR | PRIME | 36.41 | 60.01 | 63.48 | 46.92 |
| 混合 | MoR | AVERAGE | 48.93 | 71.00 | 66.14 | 58.77 |
| 消融 | MoRw/o R | AMAZON | 44.21 | 68.87 | 56.50 | 55.28 |
| 消融 | MoRw/o R | MAG | 34.33 | 62.55 | 67.55 | 47.40 |
| 消融 | MoRw/o R | PRIME | 31.59 | 53.48 | 60.74 | 41.81 |
| 消融 | MoRw/o R | AVERAGE | 31.07 | 57.04 | 57.73 | 43.03 |
| 消融 | MoRw/o RT | AMAZON | 34.04 | 53.41 | 45.16 | 42.85 |
| 消融 | MoRw/o RT | MAG | 51.81 | 73.54 | 74.17 | 61.68 |
| 消融 | MoRw/o RT | PRIME | 28.95 | 46.12 | 49.54 | 36.56 |
| 消融 | MoRw/o RT | AVERAGE | 36.39 | 56.73 | 55.73 | 45.53 |
| 消融 | MoRw/o RS | AMAZON | 43.05 | 69.36 | 57.38 | 54.69 |
| 消融 | MoRw/o RS | MAG | 31.05 | 51.84 | 50.56 | 40.64 |
| 消融 | MoRw/o RS | PRIME | 22.27 | 38.45 | 39.21 | 29.41 |
| 消融 | MoRw/o RS | AVERAGE | 28.95 | 51.28 | 48.02 | 38.98 |

### 4.2 总体检索性能

我们在表 1 中于三个 TG-KB 上将 MoR 与其他基线比较。一般而言，混合方法 AvaTaR、KAR、MFAR$^{*}$ 以及我们的 MoR，由于能够整合结构知识与文本知识，表现优于纯文本或纯结构方法。在所有基线中，我们提出的 MoR 在平均意义上以较大幅度取得总体最好的性能，在 MAG 上排名第一，在 Amazon 与 Prime 上排名第二。这表明我们所提出的结构知识与文本知识混合检索是有效的。文本检索在 Amazon 上的表现好于 MAG，说明 Amazon 查询更依赖文本知识。相比之下，它在 MAG 上较弱，是因为 MAG 的文本丰富程度较低、结构信号更强。这一差异与 Wu et al. 给出的分布分析一致，并支持我们的假设：不同 TG-KB 数据集中的查询对文本知识与结构知识有不同需求。与此同时，结构检索方法，例如传统的基于知识图谱的方法，表现较差，因为它们是为文本信息极少的图设计的，而 TG-KB 与之不同。与 Amazon 和 MAG 不同，所有未经监督调优的现有方法（例如 Ada-002）在 Prime 上的性能都显著更低。这是因为生物学需要极强的领域专门知识，基于词数的方法、基于预训练文本相似度的方法，乃至更强的 LLM，在这里都难以适用。通过微调，MFAR$^{*}$ 与我们提出的 MoR 总体上取得更好的性能，说明在知识密集领域回答查询需要领域特定知识。

### 4.3 消融研究

在验证 MoR 的优势之后，我们进行消融研究，以评估其不同组成部分，包括模块消融与特征消融。

#### 4.3.1 模块消融

为评估 MoR 中每个模块的贡献，即基于文本匹配的检索、基于邻居获取的结构检索，以及重排序器，我们进行一系列消融实验。首先，我们去掉重排序器，得到变体 MoRw/o R。在此基础上，我们再分别去掉文本检索与结构检索，得到 MoRw/o RT 与 MoRw/o RS。如表 1 所示，完整的 MoR 框架在所有数据集上始终取得最高性能，表明文本检索器、结构检索器与重排序器具有协同效应。去掉重排序器之后，MoRw/o R 在所有数据集和所有评价指标上都出现一致的性能下降。这突出了重排序器的重要性：它通过滤除中间推理阶段的噪声候选来精炼检索。去掉文本检索，即 MoRw/o RT，会在 Amazon 上导致明显的性能下降，但在 MAG 上出现意料之外的提升。这表明，文本知识对 Amazon 有益，但会引入误导性的硬负例，从而损害 MAG 上的排序方法（例如 Ada-002）。反过来，去掉结构检索，即 MoRw/o RS，会在 MAG 上造成进一步的轻微性能下降，强化了结构知识对 MAG 相关查询的重要性。这些结果突出了重排序器的关键作用：自适应地协调、平衡并选择来自结构检索专家与文本检索专家的知识。

<!-- 原 PDF 第 7 页 -->

**表 2：** 消融研究，考察我们的结构感知重排序器所使用的遍历轨迹的三个特征——文本指纹（TF）、结构指纹（SF）与遍历标识（TI）——的重要性。✔ 表示使用该特征，✘ 表示不使用。

| 数据集 | TF | SF | TI | Hit@1 | Hit@5 | Recall@20 | MRR |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MAG | ✔ | ✘ | ✘ | 48.96 | 73.02 | 72.44 | 59.79 |
| MAG | ✘ | ✔ | ✘ | 18.79 | 41.91 | 52.85 | 29.84 |
| MAG | ✘ | ✘ | ✔ | 18.16 | 41.53 | 52.78 | 29.31 |
| MAG | ✔ | ✔ | ✘ | 58.04 | 77.14 | 74.42 | 66.75 |
| MAG | ✔ | ✘ | ✔ | 58.16 | 77.59 | 74.96 | 66.85 |
| MAG | ✘ | ✔ | ✔ | 17.93 | 38.01 | 46.79 | 27.48 |
| MAG | ✔ | ✔ | ✔ | 58.19 | 78.34 | 75.01 | 67.14 |
| Amazon | ✔ | ✘ | ✘ | 51.21 | 74.05 | 59.79 | 61.27 |
| Amazon | ✘ | ✔ | ✘ | 8.09 | 24.48 | 25.62 | 16.94 |
| Amazon | ✘ | ✘ | ✔ | 5.84 | 16.62 | 12.94 | 11.57 |
| Amazon | ✔ | ✔ | ✘ | 50.91 | 73.38 | 59.58 | 61.15 |
| Amazon | ✔ | ✘ | ✔ | 51.09 | 73.56 | 59.61 | 61.14 |
| Amazon | ✘ | ✔ | ✔ | 8.09 | 24.48 | 25.62 | 16.94 |
| Amazon | ✔ | ✔ | ✔ | 52.19 | 74.65 | 59.92 | 62.24 |
| Prime | ✔ | ✘ | ✘ | 35.23 | 59.44 | 63.15 | 46.02 |
| Prime | ✘ | ✔ | ✘ | 12.95 | 30.48 | 43.33 | 21.44 |
| Prime | ✘ | ✘ | ✔ | 11.81 | 27.81 | 40.36 | 19.73 |
| Prime | ✔ | ✘ | ✔ | 35.80 | 60.12 | 63.40 | 46.50 |
| Prime | ✔ | ✔ | ✘ | 35.70 | 60.01 | 63.21 | 46.19 |
| Prime | ✘ | ✔ | ✔ | 13.20 | 32.27 | 48.01 | 22.95 |
| Prime | ✔ | ✔ | ✔ | 36.41 | 60.01 | 63.48 | 46.92 |

#### 4.3.2 特征消融

上述消融研究突出了结构感知重排序器在自适应整合结构知识与文本知识中的关键作用。为进一步分析其三个关键特征——第 3.3 节所定义的文本指纹（TF）、结构指纹（SF）和遍历标识（TI）——的贡献，我们进行特征消融分析，并在表 2 中报告不同特征配置下的检索性能。总体而言，三个特征一起使用在 MAG 和 Amazon 上都得到最好的性能，突出了它们的协同效应。单独来看，TF 贡献最大，并在两个数据集上都优于 SF 和 TI。原因在于，按照第 3.3 节的定义，TF 直接捕捉查询与轨迹上被检索节点之间的相关性，而 SF 和 TI 主要刻画结构模式与检索类型，更多地作为补充因素。因此，把 TF 与这些补充因素（即 SF 或 TI）配合使用，在 MAG 上大约还能再带来 10% 的增益。这是因为 SF 和 TI 帮助重排序器有选择地强调 TF 为路径上某些节点给出的相关性分数。然而，在 Amazon 上没有观察到这种提升。我们假设，那里所需的文本知识主要来自每条路径上的最后一个节点，使得 SF 和 TI 提供的结构线索益处较小，甚至容易过拟合。第 4.4 节有更深入的分析，以进一步论证这一假设。总体而言，这些发现强调：结构特征在排序中的重要性随数据集而变化。

**表 3：** 比较使用检索轨迹中最后一个节点与使用整条轨迹进行重排序的性能。

| 特征 | MAG Hit@1 | MAG Recall@20 | MAG MRR | Amazon Hit@1 | Amazon Recall@20 | Amazon MRR | Prime Hit@1 | Prime Recall@20 | Prime MRR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 最后节点 | 49.91 | 73.49 | 59.92 | 50.36 | 59.62 | 61.05 | 33.52 | 61.95 | 44.15 |
| 全路径 | 58.19 | 75.01 | 67.14 | 52.19 | 59.92 | 62.24 | 36.41 | 63.48 | 46.92 |

**图 3：** 不同逻辑结构上，查询数量与不同检索器性能的不均衡。图中具体柱状数值未被文字抽出，见原 PDF 第 7 页。

### 4.4 进一步分析

本节通过考察三个问题来理解 MoR 的行为。每个问题都加深我们对 MoR 功能的认识，并为未来的查询检索研究提供新的视角。更多分析见附录 C。

**结构信号会影响重排序吗？** 为评估轨迹信息对重排序器决策的影响，我们引入一种基于节点的重排序器，它只用最后一个节点的 TF/SF/TI 来构造轨迹特征。在表 3 中，基于路径的重排序器优于基于节点的变体，在 MAG 上尤其明显。这突出了轨迹特征与结构知识在重排序中的关键作用。在 Amazon 上，改用全路径轨迹后只有轻微的性能提升，说明它更偏好最后一个节点上的文本知识，而不是整条轨迹。

**MoR 在不同逻辑结构上表现如何？** 图 3 展示了 MoR 在按逻辑结构分组的每个查询组上的平均性能，其中 “Others” 指 Wu et al. 中逻辑结构未定义的查询。在不同逻辑结构上，MoR 始终优于结构检索器与文本检索器。在所有查询中，MoR 在 “P $\rightarrow$ P” 查询上表现最差，原因是多步遍历中重复出现的 “product” 实体所独有地造成的歧义。表现居中的 “Others” 组说明，对同一查询采用多样的规划策略是有用的。最后，规划模式上偏斜的查询分布与检索性能，反映了真实世界规划需求的多样性质。我们希望这些认识能启发面向异构查询结构的、以数据为中心的推理以及规划的误差控制。

<!-- 原 PDF 第 8 页 -->

**图 4：** 查询注意力在检索路径上三个实体之间的显著性图可视化。（a）（b）中的示例如下。

问题：推荐一套与我的 Northwest Company NFL Seahawks Curtain Panel Pair 相配的 NFL Seattle Seahawks 双人床单套装？

规划图：$\langle$Northwest Company NFL Seahawks Curtain Panel Pair$\rangle \rightarrow \langle$NFL Seattle Seahawks twin sheet set$\rangle$

节点类别：Product $\rightarrow$ Product。

问题：是否有来自 University of Lausanne、关于电离室中无框架立体定向技术的研究？

规划图：$\langle$University of Lausanne$\rangle \rightarrow \rightarrow \langle$frameless stereotactic technology in Ionization chambers$\rangle$

节点类别：Institution $\rightarrow$ Author $\rightarrow$ Paper。

**MoR 是否确实自适应地利用轨迹知识？** 为理解我们提出的重排序器如何在 Top-K 结果中优先排列候选，我们通过计算排序分数相对于遍历路径上三个节点的文本指纹（TF）的梯度来可视化显著性图，从而量化它们对回答给定查询的重要性。图 4 通过分析 Amazon 与 MAG 数据集上 100 条查询的 100 个真实候选的轨迹来说明这一点。每个维度对应一个被遍历的节点，最后一个维度表示候选本身。Amazon 的显著性分数集中在最后一个维度，而 MAG 表现出更均匀分布的显著性模式，路径上的多个节点都对排序分数的计算有显著贡献。这表明结构知识对回答 MAG 中的查询更为关键，与表 1 中纯文本检索在 MAG 上较低的性能相一致。进一步的案例分析解释了为什么重排序器对不同查询会关注不同节点。在图 4（a）中，重排序器偏向最后两个维度，因为丰富的文本限制（即 “Northwest Company...” 与 “NFL Seattle...”）有助于在相应推理步识别正确节点，如第 3.2 节所讨论。这些与查询具有更高相似度分数的正确节点，有助于把检索过程引向真实答案。反过来，在图 4（b）中，由于第一个节点（“University of Lausanne”）有助于缩小搜索空间，最后一个节点（“frameless...”）进一步过滤候选，两个节点都有较高的显著性分数。总体而言，我们的发现表明，重排序器会根据数据集和查询，动态调整其对结构知识与文本知识的依赖。

**图 5：** Top-20 检索候选中的遍历标识分析，以及数据集中的信息比例。图中具体数值除正文给出者外，见原 PDF 第 8 页。

**MoR 是否针对不同数据集自适应地优先选择检索方法？** 为评估 MoR 在不同数据集上自适应利用结构检索与文本检索的程度，我们计算以下三个比例。Structure/All、Text/All：Top-20 检索候选中，经结构检索或文本检索得到的候选所占比例；Structure/Answer、Text/Answer：Top-20 中，经结构检索或文本检索得到的真实候选所占比例；结构（信息）、文本（信息）：查询构建中所使用的、采样得到的关系要求与属性要求的词数比例。

结果如图 5 所示。在 MAG 数据集上，Top-20 检索候选中的大多数（67%），以及超过 95% 的正确答案，来自结构检索。这突出了结构信号在该领域中的关键作用。这一发现与 MAG 固有的丰富结构性质一致，表现为结构（信息）的比例高于文本（信息），并进一步得到表 2 与表 3 的支持：纳入结构特征后有大幅性能提升。对于 Amazon 数据集，文本匹配占 Top-20 候选的 52%，并且比结构遍历贡献更多答案。这与图 5 中观察到的 Amazon 丰富文本内容相一致。总体而言，这些结果表明 MoR 在不同数据集上表现出自适应的检索行为，能够根据底层数据特征，有效地优先选择信息量最大的检索策略。这为如下论断提供了有力证据：MoR 可以在结构检索来源与文本检索来源之间动态协调。

<!-- 原 PDF 第 9 页 -->

**表 4：** 单查询检索过程中各组成部分的理论与经验时间复杂度。批处理优化与并行优化分别用于组织阶段与推理阶段。

| 方法 | 规划 | 推理 | 组织 |
| --- | --- | --- | --- |
| 理论 | $O(K \cdot D)$ | $O(A d^{L-1})$ | $O(B d^{L-1})$ |
| 经验（秒） | 0.971 | 0.463 | 0.0340 |
| 经验 + 批处理（秒） | – | – | 0.0134 |
| 经验 + 并行（秒） | – | 0.398 | – |

**表 5：** 各数据集在不同跳数深度上的经验遍历时间。

| 数据集 | 1-hop | 2-hop | 3-hop |
| --- | --- | --- | --- |
| Prime | 0.059 秒 | 0.068 秒 | 0.072 秒 |
| Amazon | 0.381 秒 | 0.403 秒 | 0.669 秒 |
| MAG | 0.289 秒 | 0.297 秒 | 1.233 秒 |

### 4.5 MoR 的效率与可扩展性

由于 MoR 由三个阶段组成，我们通过对每个阶段分别进行理论分析与经验分析来做复杂度分析。结果如表 4 所示，其中 $K$ 表示所生成规划图中的词元数，$D$ 是遵循 GPT 式解码与键值缓存时的模型维度，$d$ 表示每一步节点的平均度，$L$ 表示一条路径中的步数或层数，$A$ 与 $B$ 都是常数。受 LLM 所限，很难提高规划阶段的效率。由于遍历相互独立，我们实现了并行版本以加速推理。对于组织阶段，我们可以方便地用批处理同时计算多个候选与多条查询的排序分数，从而提高效率。

基于上述分析，整个框架的时间复杂度为 $O(K \cdot D + (A + B)d^{L-1}) \approx O(d^{L-1})$，表明复杂度随推理路径长度呈指数增长。为考察时间复杂度如何随路径长度变化，我们从经验上分析 MoR 相对于推理路径深度的可扩展性。我们按推理跳数（例如 1-hop、2-hop、3-hop）对测试查询分组，并在三个数据集上比较这三组的效率。如表 5 所示，大多数查询可以在 1 秒内处理完。更深的查询自然需要更多处理时间，但由于逐步遍历，并在必要时自适应地回退到文本检索，MoR 仍保持相当高的效率。

关于计算复杂度以及向大规模数据集扩展的更详细分析，见附录 D.1 与附录 D.2。

## 5 相关工作

**检索增强生成（Retrieval-augmented Generation，RAG）：** RAG 通过从外部知识源检索相关信息来增强生成任务（He et al., 2025; Gao et al., 2023b），并已被广泛用于改进问答（Liu et al., 2023）。在 LLM 的背景下，RAG 被用于缓解幻觉（Yao et al., 2023）、增强可解释性（Gao et al., 2023a），以及实现动态知识更新（Wang et al., 2024）。本工作实质上利用 RAG 的思想，从 TG-KB 中检索支撑实体，以使答案生成情境化。按照所检索知识的具体类型，现有检索器可分为结构检索与文本检索，下文将分别回顾。

**文本检索与结构检索：** 早期文本检索模型，如 TF-IDF 和 BM25（Robertson et al., 2009），依赖词法相似度与关键词匹配（Chen et al., 2017; Yang et al., 2019; Mao et al., 2021）。现代方法通过学习稠密表示来应对这一局限（Karpukhin et al., 2020）。在文本检索之外，结构检索利用基于图的技术抽取结构化知识。图遍历（Wang et al., 2024; Jiang et al., 2023）、社区检测（Edge et al., 2024）以及图机器学习模型（包括图神经网络（Yasunaga et al., 2021; Mavromatis and Karypis, 2024））等方法，在结构检索中起着关键作用。我们的方法把混合专家的思想注入检索设计，从而整合文本检索与结构检索双方的长处。

由于篇幅限制，相关工作的完整版本见附录 F。

## 6 结论

在本工作中，我们提出结构与文本混合检索（MoR），根据查询需求自适应地检索结构知识与文本知识。它首先利用文本图生成器生成规划图，然后执行混合遍历，并通过结构感知重排序器进行组织，以得到最终候选。实验表明，我们的 MoR 在协调文本知识与结构知识的检索方面具有优势，并带来有洞察力的发现，包括在不同模式的查询之间平衡检索性能，以及查询自适应的、对结构知识或文本知识的需求。

<!-- 原 PDF 第 10 页 -->

## 7 局限

在本文中，我们把混合专家的思想整合进检索设计，并提出结构与文本混合检索（MoR），以自适应地检索文本知识与结构知识。MoR 的局限可分为以下两个主要方面：

**缺乏领域特定知识：** 我们提出的 MoR 与其他基线类似，在 PRIME 上的性能并没有显著高于 AMAZON 和 MAG。原因是缺乏理解生物医学问题、抽取关键信息、在相关实体与关系中导航，以及对检索候选重排序所需的生物医学知识。这表明，当前最先进的检索模型，即便配上 LLM 的智能，仍然难以有效处理领域特定知识。此类局限可能延伸到其他专门领域，例如金融与法律。未来研究可以把领域特定知识整合进检索。

**在每一遍历层进行重排序：** 我们当前的 MoR 通过重排序，在最后一层把检索候选自适应地路由到 Top-K 位置，从而有效实现了一种常规的混合专家（Mixture of Experts，MoE）路由机制。尽管我们在表 1 中取得了当前最优的性能，这一路由机制也可以应用于中间层：每一步检索之后对候选重排序，只有 Top-K 进入下一轮遍历与检索。这使得混合遍历的每一层都能模拟 MoE 的路由器设计。

**多轨迹重排序：** 虽然我们当前的结构重排序器被设计为利用终止于每个候选的多条遍历路径的全部轨迹信息来计算排序分数（如图 2 所示），但由于实现复杂度，我们目前的实现只使用信息量最大的那条轨迹（即遍历路径最长的那一条）。未来工作应当探索自适应方法，把完整的遍历路径集合充分整合进候选排序过程，并比较在不同层面上利用遍历路径的效果。

## 参考文献

Payal Chandak, Kexin Huang, and Marinka Zitnik. 2023. 构建知识图谱以支持精准医学. Scientific Data, 10(1):67.

Danqi Chen, Adam Fisch, Jason Weston, and Antoine Bordes. 2017. 阅读 Wikipedia 以回答开放域问题. In Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics, pages 1870–1879, Vancouver, Canada. Association for Computational Linguistics.

Julien Delile, Srayanta Mukherjee, Anton Van Pamel, and Leonid Zhukov. 2024. 基于图的检索器捕捉生物医学知识的长尾. ArXiv, abs/2402.12352.

Darren Edge, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao, Apurva Mody, Steven Truitt, and Jonathan Larson. 2024. 从局部到全局：一种面向查询聚焦摘要的 Graph RAG 方法. ArXiv, abs/2404.16130.

Yunfan Gao, Tao Sheng, Youlin Xiang, Yun Xiong, Haofen Wang, and Jiawei Zhang. 2023a. Chat-rec：迈向交互式且可解释的 LLM 增强推荐系统. arXiv preprint arXiv:2303.14524.

Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia, Jinliu Pan, Yuxi Bi, Yi Dai, Jiawei Sun, and Haofen Wang. 2023b. 面向大语言模型的检索增强生成：综述. arXiv preprint arXiv:2312.10997.

Chunxi Guo, Zhiliang Tian, Jintao Tang, Shasha Li, Zhihua Wen, Kaixuan Wang, and Ting Wang. 2023. 基于检索增强 GPT-3.5 的 text-to-SQL 框架：样本感知提示与动态修正链. In International Conference on Neural Information Processing, pages 341–356. Springer.

Haoyu Han, Yu Wang, Harry Shomer, Kai Guo, Jiayuan Ding, Yongjia Lei, Mahantesh Halappanavar, Ryan A Rossi, Subhabrata Mukherjee, Xianfeng Tang, et al. 2024. 图上的检索增强生成（GraphRAG）. arXiv preprint arXiv:2501.00309.

Xiaoxin He, Yijun Tian, Yifei Sun, Nitesh Chawla, Thomas Laurent, Yann LeCun, Xavier Bresson, and Bryan Hooi. 2025. G-retriever：面向文本图理解与问答的检索增强生成. Advances in Neural Information Processing Systems, 37:132876–132907.

Minghao Hu, Yuxing Peng, Zhen Huang, and Dongsheng Li. 2019. 检索、阅读、重排序：迈向端到端多文档阅读理解. In Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics.

Gautier Izacard, Mathilde Caron, Lucas Hosseini, Sebastian Riedel, Piotr Bojanowski, Armand Joulin, and Edouard Grave. 2022. 基于对比学习的无监督稠密信息检索. Transactions on Machine Learning Research.

Jinhao Jiang, Kun Zhou, Zican Dong, Keming Ye, Wayne Xin Zhao, and Ji rong Wen. 2023. StructGPT：大语言模型在结构化数据上推理的通用框架. In Conference on Empirical Methods in Natural Language Processing.

<!-- 原 PDF 第 11 页 -->

Bowen Jin, Chulin Xie, Jiawei Zhang, Kashob Kumar Roy, Yu Zhang, Suhang Wang, Yu Meng, and Jiawei Han. 2024a. 图思维链：通过在图上推理来增强大语言模型. In Annual Meeting of the Association for Computational Linguistics.

Bowen Jin, Yu Zhang, Sha Li, and Jiawei Han. 2024b. 桥接文本数据与图数据：迈向语义与结构感知的知识发现. In Proceedings of the 17th ACM International Conference on Web Search and Data Mining, pages 1122–1125.

Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, and Wen-tau Yih. 2020. 面向开放域问答的稠密段落检索. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP), pages 6769–6781.

Oleksandr Kolomiyets and Marie-Francine Moens. 2011. 从信息检索视角看问答技术综述. Information Sciences, 181(24):5412–5434.

Meng-Chieh Lee, Qi Zhu, Costas Mavromatis, Zhen Han, Soji Adeshina, Vassilis N. Ioannidis, Huzefa Rangwala, and Christos Faloutsos. 2024. HybGRAG：文本知识库与关系知识库上的混合检索增强生成. ArXiv, abs/2412.16311.

Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, et al. 2020. 面向知识密集型 NLP 任务的检索增强生成. Advances in Neural Information Processing Systems, 33:9459–9474.

Millicent Li, Tongfei Chen, Benjamin Van Durme, and Patrick Xia. 2024. 多字段自适应检索. arXiv preprint arXiv:2410.20056.

Lihui Liu, Yuzhong Chen, Mahashweta Das, Hao Yang, and Hanghang Tong. 2023. 面向歧义查询的知识图谱问答. In Proceedings of the ACM Web Conference 2023.

Chris Lu, Cong Lu, Robert Tjarko Lange, Jakob Foerster, Jeff Clune, and David Ha. 2024. AI 科学家：迈向全自动的开放式科学发现. arXiv preprint arXiv:2408.06292.

Linhao Luo, Yuan-Fang Li, Reza Haf, and Shirui Pan. 图上推理：忠实且可解释的大语言模型推理. In The Twelfth International Conference on Learning Representations.

Yuning Mao, Pengcheng He, Xiaodong Liu, Yelong Shen, Jianfeng Gao, Jiawei Han, and Weizhu Chen. 2020. 面向开放域问答的生成增强检索. arXiv preprint arXiv:2009.08553.

Yuning Mao, Pengcheng He, Xiaodong Liu, Yelong Shen, Jianfeng Gao, Jiawei Han, and Weizhu Chen. 2021. 面向开放域问答的生成增强检索. In Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing.

Costas Mavromatis and George Karypis. 2024. GNN-RAG：面向大语言模型推理的图神经检索. ArXiv, abs/2405.20139.

Dang Nguyen, Viet Dac Lai, Seunghyun Yoon, Ryan A Rossi, Handong Zhao, Ruiyi Zhang, Puneet Mathur, Nedim Lipka, Yu Wang, Trung Bui, et al. 2024. Dynasaur：超越预定义动作的大语言智能体. arXiv preprint arXiv:2411.01747.

Bo Ni, Zheyuan Liu, Leyao Wang, Yongjia Lei, Yuying Zhao, Xueqi Cheng, Qingkai Zeng, Luna Dong, Yinglong Xia, Krishnaram Kenthapadi, et al. 2025. 迈向可信的大语言模型检索增强生成：综述. arXiv preprint arXiv:2502.06872.

Stephen Robertson, Hugo Zaragoza, et al. 2009. 概率相关性框架：BM25 及其拓展. Foundations and Trends® in Information Retrieval, 3(4):333–389.

Junhong Shen, Neil Tenenholtz, James Brian Hall, David Alvarez-Melis, and Nicolo Fusi. TAG-LLM：把通用 LLM 改造用于专门领域. In Forty-first International Conference on Machine Learning.

Jiashuo Sun, Chengjin Xu, Lumingyuan Tang, Sai Wang, Chen Lin, Yeyun Gong, Lionel M. Ni, Heung yeung Shum, and Jian Guo. 2023. Think-on-Graph：大语言模型在知识图谱上的深度且负责任的推理. In International Conference on Learning Representations.

Dhaval Taunk, Lakshya Khanna, Pavan Kandru, Vasudeva Varma, Charu Sharma, and Makarand Tapaswi. 2023. GrapeQA：通过图增强与剪枝来提升问答. Companion Proceedings of the ACM Web Conference 2023.

Yijun Tian, Huan Song, Zichen Wang, Haozhu Wang, Ziqing Hu, Fang Wang, Nitesh V Chawla, and Panpan Xu. 2024. 结合大语言模型的图神经提示. In Proceedings of the AAAI Conference on Artificial Intelligence.

MK Vijaymeena and K Kavitha. 2016. 文本挖掘中的相似度度量综述. Machine Learning and Applications: An International Journal.

Yu Wang, Nedim Lipka, Ryan A Rossi, Alexa Siu, Ruiyi Zhang, and Tyler Derr. 2024. 面向多文档问答的知识图谱提示. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 38, pages 19206–19214.

Shirley Wu, Shiyu Zhao, Qian Huang, Kexin Huang, Michihiro Yasunaga, Kaidi Cao, Vassilis Ioannidis, Karthik Subbian, Jure Leskovec, and James Y Zou.

<!-- 原 PDF 第 12 页 -->

2025. Avatar：通过对比推理优化 LLM 智能体的工具使用. Advances in Neural Information Processing Systems, 37:25981–26010.

Shirley Wu, Shiyu Zhao, Michihiro Yasunaga, Kexin Huang, Kaidi Cao, Qian Huang, Vassilis N Ioannidis, Karthik Subbian, James Zou, and Jure Leskovec. STaRK：在文本知识库与关系知识库上评测 LLM 检索. In The Thirty-eight Conference on Neural Information Processing Systems Datasets and Benchmarks Track.

Yu Xia, Junda Wu, Sungchul Kim, Tong Yu, Ryan A Rossi, Haoliang Wang, and Julian McAuley. 2024. 面向文本检索与关系检索的、基于大语言模型的知识感知查询扩展. arXiv preprint arXiv:2410.13765.

Mayi Xu, Yongqi Li, Ke Sun, and Tieyun Qian. 2024. Adaption-of-thought：学习问题难度以提升大语言模型的推理. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing, pages 5468–5495, Miami, Florida, USA. Association for Computational Linguistics.

Shangzi Xue, Zhenya Huang, Xin Lin, Jiayu Liu, Longhu Qin, Tianhuang Su, Haifeng Liu, and Qi Liu. 2024. 提升多步问答中推理依据的完整性. In Proceedings of the 33rd ACM International Conference on Information and Knowledge Management, pages 2753–2763.

Wei Yang, Yuqing Xie, Aileen Lin, Xingyu Li, Luchen Tan, Kun Xiong, Ming Li, and Jimmy Lin. 2019. 基于 BERTSerini 的端到端开放域问答. In Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics, pages 72–77.

Jia-Yu Yao, Kun-Peng Ning, Zhen-Hui Liu, Mu-Nan Ning, and Li Yuan. 2023. LLM 谎言：幻觉不是缺陷，而是作为对抗样本的特性. arXiv preprint arXiv:2310.01469.

Michihiro Yasunaga, Hongyu Ren, Antoine Bosselut, Percy Liang, and Jure Leskovec. 2021. QAGNN：用语言模型与知识图谱进行问答推理. In North American Chapter of the Association for Computational Linguistics.

Jiaxuan You, Rex Ying, Xiang Ren, William Hamilton, and Jure Leskovec. GraphRNN：用深度自回归模型生成真实图. In International conference on machine learning. PMLR.

Huimin Zeng, Zhenrui Yue, Qian Jiang, and Dong Wang. 2024. 通过混合检索增强生成进行联邦推荐. 2024 IEEE International Conference on Big Data (BigData).

Xikun Zhang, Antoine Bosselut, Michihiro Yasunaga, Hongyu Ren, Percy Liang, Christopher D Manning, and Jure Leskovec. GreaSeLM：图推理增强的语言模型. In International Conference on Learning Representations.

Yanqiao Zhu, Yuanqi Du, Yinkai Wang, Yichen Xu, Jieyu Zhang, Qiang Liu, and Shu Wu. 深度图生成综述：方法与应用. In Learning on Graphs Conference. PMLR.

## 附录 A 记号汇总

**表 6：** 记号及相应描述。

| 记号 | 定义或描述 |
| --- | --- |
| $\mathcal{B}$ | 文本丰富图知识库（TG-KB） |
| $V, \mathcal{E}, \mathcal{D}$ | TG-KB 的节点集合、类别集合与文档集合 |
| $D_v, E_v$ | 节点 $v$ 的文档与类别 |
| $Q \in \mathcal{Q}$ | 来自查询集合 $\mathcal{Q}$ 的查询 $Q$ |
| $Q_{\text{Struct}}, Q_{\text{Text}}$ | 分别由结构检索与文本检索所针对的查询 |
| $G = \{P_i\}_{i=1}^{\lvert G \rvert}$ | 由多条推理路径组成的规划图 |
| $P_i = (p_{i1} \rightarrow \ldots \rightarrow p_{iL_i})$ | 由 $L_i$ 个顺序实体组成的推理路径 |
| $E_{p_{ij}}, T_{p_{ij}}$ | 路径实体 $p_{ij}$ 的文本类别与限制 |
| $\tilde{C}$ | 推理模块之后检索到的候选 |
| $\tilde{C}^{l}_{i} = \tilde{C}^{l,\text{Struct}}_{i} \cup \tilde{C}^{l,\text{Text}}_{i}$ | 第 $i$ 条路径第 $l$ 层检索到的候选，包括结构检索得到的与文本检索得到的 |
| $C$ | 组织模块之后的最终检索候选 |
| $P_{Q \times G}$ | 查询与规划图的联合分布 |
| $N_v$ | 实体 $v$ 的邻居 |
| $I_{p_{il}}$ | 结构检索与文本检索的遍历标识 |
| $P_{\Theta_1}$ | 规划模块及其参数 $\Theta_1$ |
| $P_{\Theta_2}$ | 推理模块及其参数 $\Theta_2$ |
| $P_{\Theta_3}$ | 组织模块及其参数 $\Theta_3$ |

**表 7：** STaRK 基准（Wu et al.）中文本丰富图知识库的统计。

| 数据集 | 实体数 | 文本词元数 | 关系数 | 平均度 |
| --- | --- | --- | --- | --- |
| AMAZON | 1,035,542 | 592,067,882 | 9,443,802 | 18.2 |
| MAG | 1,872,968 | 212,602,571 | 39,802,116 | 43.5 |
| PRIME | 129,375 | 31,844,769 | 8,100,498 | 125.2 |

## 附录 B 实验细节

### B.1 数据集

为评估我们所提出框架的有效性，我们使用来自 STaRK（Wu et al.）的三个文本丰富图知识库（TG-KB）进行实验。这些 TG-KB 覆盖广泛领域，包括产品评论（Amazon）、学术论文（MAG）和生物医学知识（Prime）。每个 TG-KB 包含一张文本图以及一个相关联的语料；语料中的文档链接到图中的节点。查询针对每个 TG-KB 被精心构造，并涵盖不同复杂度，回答它们需要不同程度的文本知识与结构知识。

**Amazon：** 该数据集提供产品搜索与推荐的真实模拟。其文本图由四类节点组成：product、category、color 和 brand。节点通过诸如 has_brand 和 has_category 之类的关系相互连接。文本文档涵盖

<!-- 原 PDF 第 13 页 -->

对应节点的属性，例如产品描述与顾客评论。

**MAG：** 学术论文检索的综合资源。在文本图中，论文可以连接到其他节点，例如通过关系 paper_has_topic_field_of_study 连接到 field_of_study，以及通过 author_affiliated_with_institution 与 author_writes_paper 等关系的组合连接到 institution。每篇论文文档包含标题、摘要以及元数据，例如发表日期与 venue，为检索与分析提供丰富的上下文知识。

**Prime：** 高度领域特定的数据集。它聚焦医学问询，来源于 PrimeKG 知识图谱（Chandak et al., 2023）。该图谱包含十种实体类型和十八种关系类型，并提供多个目标节点类别，例如 disease、gene/protein 和 drug。相关联的文档聚合自多个数据库，提供丰富而多样的医学知识来源。

详细的数据集统计见表 7。

### B.2 实现细节

**规划图生成：** 在第 3.1 节中，我们遵循先前工作（Luo et al.; Wu et al.），通过把规划图分解为顺序的推理路径来把规划过程线性化，这些路径可以由 LLM 经由下一词元预测生成。由于缺少用于训练的真实规划图，我们借助 LLM 较强的推理能力，提示它们合成这些真实规划图。由于规划图中的节点是实体类别或类型，我们在提示中加入实体类型列表（Entity Type List）。我们还利用上下文学习，帮助 LLM 学习查询与对应规划图之间的映射。生成真实规划图的详细提示，以及微调规划图生成器（即 Llama 3.2-3B）的参数，见提示 1 与表 8。

**表 8：** 规划图生成器的超参数。

| 参数 | 取值 | 描述 |
| --- | --- | --- |
| per_device_train_batch_size | 4 | 每台设备上的训练样本数。 |
| gradient_accumulation_steps | 8 | 在 8 步上累积梯度。 |
| num_train_epochs | 100 | 在训练数据集上的完整遍历次数。 |
| max_steps | 1000 | 最大训练步数；一旦达到即停止训练。 |
| learning_rate | 2e-4 | 优化器的初始学习率。 |
| warmup_steps | 5 | 预热步数。 |
| optim | adamw_8bit | 用于高效训练的 8 比特 AdamW。 |
| lr_scheduler_type | linear | 学习率线性衰减。 |
| weight_decay | 0.01 | 用于防止过拟合的 L2 正则。 |
| seed | 3407 | 用于可复现性的随机种子。 |

**提示 1：规划图生成**

系统消息：你是一个规划图查找智能体。你的职责是：

1. 从给定问题中识别底层**元路径（meta-path）**，它由每个推理步上的**实体类型**组成。
2. 根据问题，为每个**实体类型**抽取**内容限制**。如果某个实体类型没有限制，则将其值留空。

你将得到一份预定义的**实体类型列表**。构造元路径和限制时，只使用该列表中的实体类型。你的回答必须简洁，并严格遵守指定的**输出格式**。

实体类型列表：提供实体类型列表。

示例：用于上下文学习的例子。

输出格式：Metapath: "", Restriction: {}。

**轨迹收集：** 如第 3.3 节所述，我们的重排序器根据轨迹对中间检索候选重新排序。为此，我们收集三个关键特征：文本指纹（TF）、结构指纹（SF）和遍历标识（TI）。

**文本指纹（TF）：** 我们记录查询与被遍历节点之间计算得到的 BM25 相似度分数。由于经验观察表明推理路径的长度通常小于三，我们把文本指纹固定为长度三：对长度小于三的推理路径用额外的 0 相似度分数填充，以便按批训练。此外，我们把用余弦相似度结合 Ada-002 嵌入计算得到的候选初始语义排序分数，追加到三个基于 BM25 的相似度分数末尾，以补充词法视角。然后该向量经过一个线性层，被变换为大小为 256 的嵌入。注意，这一初始排序分数也被用来选择供重排序使用的中间检索候选。

**结构指纹（SF）：** 我们把对应推理路径中所有节点的类别拼接成一个文本序列。如果推理路径短于三个节点，我们在序列前添加 “padding” 词元，以保证固定长度。然后用一个 transformer 模型处理结构指纹，把序列转换为大小为 768 的嵌入，再经过一个线性层投影到大小 256。

**遍历标识（TI）：** 我们记录每个节点是经由文本匹配还是结构遍历检索到的，并通过初始化一个可学习嵌入矩阵、把每种遍历标识编码映射到一个 $3 \times 256$ 维嵌入向量，用不同的值对它们编码。

在得到上述全部三类轨迹特征之后，

<!-- 原 PDF 第 14 页 -->

我们把所得向量拼接成一个统一向量（$256 + 256 + 256 \times 3 = 1280$），并施加两个全连接层，把组合表示变换为一个重排序分数。该分数决定最终排名。

## 附录 C 补充结果

### C.1 规划性能

为考察规划图生成器的性能，我们做实验评估所生成规划图对于查询的质量。如果一张规划图能够使其结构所引导的遍历检索到至少一个真实候选，我们就认为它是正确的。在表 9 中，MAG 与 Amazon 数据集上的大多数规划图是正确的，表明它们能有效引导遍历。即便对于领域特定的 Prime 数据集，也有超过 60% 的规划图能导向正确检索，说明 LLM 仍然能生成准确的计划，并有效支持下游推理与重排序。

**表 9：** 规划图生成器在三个数据集上的性能。

| 数据集 | MAG | Amazon | Prime |
| --- | --- | --- | --- |
| 准确率（%） | 88.85 | 70.03 | 60.44 |

### C.2 查询模式分析

**图 6：** 不同逻辑模式上，查询数量与不同检索器性能的不均衡。图中具体柱状数值未被文字抽出，见原 PDF 第 14 页。

图 6 展示了对 MAG 数据集中查询模式的分析。由于关系信息更丰富，该数据集中的查询形成更多样的模式，包括更长、更多样的结构。与 Amazon 数据集类似，我们观察到一个总体趋势：在不同模式上，随着查询数量减少，MoR 的性能下降。除这一总体趋势外，MAG 数据集中的某些查询模式较为突出，例如 “P $\rightarrow$ A $\rightarrow$ P”（产品到作者到产品）和 “P $\rightarrow$ P”（论文到论文）。尽管它们出现得相对频繁，MoR 在这些模式上仍然表现更差。这类似于 Amazon 数据集上观察到的 “Product $\rightarrow$ Product” 模式的低性能：单一查询中出现重复的实体类型。这种重复使文本检索器把焦点从目标转移到重复实体上，从而导致更低的性能。

## 附录 D 效率分析

### D.1 MoR 的计算复杂度

由于我们的规划—推理—组织框架是多阶段的，我们从理论上和经验上分析每个组成部分的时间复杂度：

- **规划：** 规划组件使用预训练语言模型，通过线性化的词元生成来生成文本规划图，这是大多数 LLM 已确立的技术。由于我们的规划图基于类别，其文本描述由直接从查询中抽出的简单词语组成，所得文本图相对简单，并保持较短的词元长度。因此生成效率很高，时间复杂度关于词元数是线性的，即 $O(K \cdot D)$，其中 $K$ 为规划图词元数，$D$ 为模型维度，并遵循 GPT 式解码与键值缓存。
- **推理：** 推理组件沿着所生成的文本规划图进行逐层广度优先遍历，其时间复杂度随遍历的层数或跳数呈指数增长。设 $L$ 为所有推理路径上的最大层数或跳数，$c$ 为从每张规划图分解出的互异推理路径总数，$d$ 为平均节点度，$t$ 表示每一层经由文本相似度检索到的节点数。我们从一组 $s$ 个种子节点开始混合遍历，并通过检索上一层节点的邻居来逐层扩展（受规划图中该对应层所规定的节点

<!-- 原 PDF 第 15 页 -->

类别约束）。从第二层起，我们额外纳入按与原始查询的文本相似度排名的前 $t$ 个节点，这些经文本检索得到的节点也会在下一层贡献邻居扩展。设 $z$ 表示文本匹配与节点实体约束检查所用的时间，则沿着 $c$ 条推理路径进行推理的总时间复杂度为

$$
\begin{aligned}
&O\Big(c\big(\underbrace{(((sd + t)d + t)\ldots )d + t}_{L}\big)z\Big) \\
&= O\Big(c s d^{L-1} z + c t \frac{d^{L-1} - 1}{d - 1} z\Big) \\
&\approx O(A d^{L-1})
\end{aligned}
\tag{8}
$$

公式抽取不完整，见原 PDF 第 15 页。上标与分式横线在抽取中断行。抽出的原串为：`O(c((((sd + t)d + t)...)d + t`（其下括注为 `L`）`)z) = O(csdL−1z + ctdL−1 −1` / `d −1` / `z) ≈ O(AdL−1)`。上式按这些词元复原。

因为 $s$、$t$、$c$、$z$ 通常是常数，其取值相对于呈指数增长的路径较小，并被一并吸收进 $A$。

- **组织：** 对于推理阶段给出的检索路径上的每个候选，组织模块计算排序分数，其开销为 $O(B d^{L-1})$，其中 $d^{L-1}$ 表示推理路径的总数，$B$ 表示用所定义的神经网络为每条路径计算排序分数的时间。

综合上述分析，整个框架的时间复杂度为 $O(KD + (A + B)d^{L-1}) \approx O(d^{L-1})$。由于我们的规划图生成遵循典型的 LLM 解码机制，它并不引入额外的时间开销。因此我们不把优化重点放在这一阶段。相反，考虑到检索路径数量呈指数增长，我们优化推理阶段与组织阶段：

- **推理：** 我们把遍历过程并行化，因为每条推理路径是独立探索的。
- **组织：** 我们同时评估一批推理路径及其候选。

我们在表 4 中报告单条查询检索在理论上分析并在经验上验证的时间复杂度。为计入数据集之间的差异并降低实验中随机性的影响，我们对每个数据集运行三次，并报告平均效率。可以看到，尽管推理与组织的时间复杂度呈指数增长，经验上的时间消耗相当低。

**表 10：** 不同数据集上顺序处理与并行处理的时间。

| 数据集 | 顺序（秒） | 并行（秒） |
| --- | --- | --- |
| Amazon | 0.416 | 0.271 |
| MAG | 0.891 | 0.846 |
| Prime | 0.081 | 0.076 |

### D.2 混合遍历对大规模 TG-KB 的可扩展性

我们的推理过程沿着所生成的文本规划图进行逐层广度优先遍历，其时间复杂度随遍历深度的增加呈指数增长。上述分析表明，时间代价（即 $O(A d^{L-1})$）主要由平均节点度 $d$ 与推理跳数 $L$ 决定。因此，即便对于大规模 TG-KB，遍历仍然高效，因为大多数图是稀疏的，而且推理路径相当短；这两点都已在（Wu et al.）中得到经验验证。此外，我们实验中的三个 TG-KB 本身规模已经很大，而我们的推理遍历方法在处理每条查询时仍取得显著的效率（见表 7 与表 10）。再者，由于遍历过程高度可并行，这一运行时间还可以通过在遍历多条推理路径时利用多进程来进一步降低。

## 附录 E 扩展到问答任务

已有研究表明，检索的改进往往带来问答结果的改进（Mao et al., 2020; Lewis et al., 2020）。为验证这一正相关，我们额外基于检索到的信息评估问答性能。具体而言，我们用 LLM GPT-4o 作为评判者，评估哪种检索方法为回答问题提供了更有帮助的上下文，从而考察检索质量的提升能否转化为更好的问答性能。为缓解幻觉，我们允许 LLM 在两种检索候选都不能支持答案时回答“我不知道”（原文 “I don’t know”）。我们对三个 TG-KB 各采样 100 条查询，并用我们提出的 MoR 以及经典文本匹配基线 BM25 检索 top-5 候选。为减轻位置偏差的影响，我们对两种方法检索到的候选评估两种不同的呈现顺序，从而每个数据集得到 200 次评估。两种方法在三个数据集上的胜率（即偏好百分比）报告于表 11。

<!-- 原 PDF 第 16 页 -->

**表 11：** BM25 与 MoR 在各数据集上的问答性能比较。

| 数据集 | BM25 | MoR |
| --- | --- | --- |
| MAG | 27.0% | 64.0% |
| Prime | 33.0% | 56.5% |
| Amazon | 40.0% | 42.5% |

## 附录 F 完整相关工作

### F.1 检索增强生成（RAG）

随着近期 LLM 在接近人类水平智能方面取得前所未有的成功，检索相关知识以支持下游生成已变得日益关键。检索增强生成通过整合来自外部知识源的相关信息来增强生成任务（He et al., 2025; Gao et al., 2023b; Han et al., 2024），并已被广泛采用以改进问答（Liu et al., 2023）。在 LLM 的语境中，RAG 被用于缓解幻觉（Yao et al., 2023）、增强可解释性（Gao et al., 2023a），以及实现动态知识更新（Wang et al., 2024）。本工作利用 RAG 从 TG-KB 中检索支撑实体，为答案生成提供上下文落地。按照所检索知识的类型，现有检索器可分为结构检索方法与文本检索方法，下文将分别回顾。

### F.2 文本检索与结构检索

由于真实世界的知识通常同时以文本形式和结构形式存储（Kolomiyets and Moens, 2011），例如已索引的文本和知识图谱，每一种都需要适配其独特表示的检索方法。文本检索器根据与给定查询的相似度检索知识，可分为：词法方法（例如 TF-IDF 和 BM25（Robertson et al., 2009））与语义方法（例如 DPR 和 Contriever（Karpukhin et al., 2020; Izacard et al., 2022））。尽管它们适用面广，预定义的语言规则与基于嵌入的语义，可能难以捕捉存储在图结构知识库中的结构知识，例如知识图谱和文本丰富网络。为应对这一挑战，人们提出了结构检索，使用图分析技术（例如图遍历（Wang et al., 2024; Jiang et al., 2023; Zhang et al.; Edge et al., 2024））和图机器学习模型（例如图神经网络（Yasunaga et al., 2021; Mavromatis and Karypis, 2024））。早期方法抽取种子节点的局部子图（Yasunaga et al., 2021; Taunk et al., 2023），或预定义通向答案的路径（例如最短路径（Luo et al.; Delile et al., 2024））。为避免局部子图中邻居呈指数扩张，并打破预定义路径所规定的僵硬逻辑，近期进展整合 LLM 以动态调整图遍历（Sun et al., 2023; Wang et al., 2024; Jin et al., 2024a）。尽管这些方法有前景，频繁调用 LLM 会带来难以承受的资源开销。尽管文本检索与结构检索都有上述进展，它们往往被独立使用，未能相互增强。这推动了近期发展混合检索的研究趋势，下文将加以回顾。

### F.3 混合检索

近来，若干工作探索了从 TG-KB 进行混合知识检索。一种方法（Xia et al., 2024; Li et al., 2024）聚合来自邻居节点的文档，其中 Xia et al.（2024）施加关系过滤以去除无关邻居，Li et al.（2024）根据字段重要性对邻居加权。另一种方法（Lee et al., 2024）使用 LLM 在结构检索与文本检索之间选择其一。相比之下，我们提出的 MoR 通过把文本匹配与图遍历整合进统一框架，充分利用图结构与丰富文本，使结构知识与文本知识之间能够有更顺畅、更可解释的交互。

<!-- 译完 -->

