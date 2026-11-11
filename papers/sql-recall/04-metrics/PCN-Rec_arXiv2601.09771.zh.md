# PCN-Rec：面向可靠治理约束推荐的智能体式可携带证明协商

- 原文件名：PCN-Rec_arXiv2601.09771.pdf
- 原标题：PCN-Rec: Agentic Proof-Carrying Negotiation for Reliable Governance-Constrained Recommendation
- 中文标题：PCN-Rec：面向可靠治理约束推荐的智能体式可携带证明协商
- 作者：Aradhya Dixit（Wake Technical Community College, Raleigh, North Carolina, USA，adixit1@my.waketech.edu）；Shreem Dixit（University of North Carolina at Charlotte, Charlotte, North Carolina, USA，sdixit6@charlotte.edu）
- 会议或 arXiv：页眉为 LARS @ WWW ’26, 2026, TBD；arXiv:2601.09771

<!-- 原 PDF 第 1 页 -->

## 摘要

基于现代大语言模型的推荐器可以生成有说服力的排序列表，但它们难以可靠地满足治理约束，例如最低长尾曝光或多样性要求。我们提出 PCN-Rec，一条可携带证明的协商（proof-carrying negotiation）流水线，把自然语言推理与确定性强制执行分开。基础推荐器（MF/CF）产生大小为 $W$ 的候选窗口，由两个智能体协商：User Advocate 优化相关性，Policy Agent 强制约束。一个调解者 LLM 综合出一个 Top-$N$ 推荐列表（slate），并附带一份结构化证书（JSON），描述所声称的约束满足情况。确定性验证器根据该列表重算全部约束，并且只接受经过验证器检查的证书；若验证失败，确定性的约束贪心修复会生成一份合规列表并重新验证，从而得到可审计的轨迹。在带治理约束的 MovieLens-100K 上，PCN-Rec 在可行用户上达到 $98.55\%$ 的通过率（$n = 551$，$W = 80$），对照是没有验证/修复的一次性（one-shot）LLM 基线；同时保持效用，NDCG@10 只下降 $0.021$ 的绝对值（0.403 对 0.424）；差异在统计上显著（$p < 0.05$）。

**关键词：** 推荐系统，LLM 智能体，约束排序，治理，验证，协商

## 1 引言

部署在真实平台上的推荐系统受到超出纯相关性的约束支配——例如硬性的最低长尾曝光、体裁多样性，或按列表的策略上限 [10, 12, 19]。这些约束常常有法律或合同上的动机，并且必须可审计：平台必须能够解释为什么提供了这份列表，并证明策略检查确实被满足。近期基于 LLM 的推荐器可以用自然语言产生有说服力的排序，但当被要求可靠地满足严格的组合要求时，它们很脆弱 [1, 2, 7, 14, 21]。实践中，单个 LLM 可能输出一份看似合理的理由，同时仍然违反约束，而且它的推理不能直接执行或验证。现有的单体 LLM 方法受困于“迷失在中间”（lost-in-the-middle）式推理，并且无法在组合约束上维持全局状态 [23]。通过把推荐任务分解成智能体之间的竞争，我们允许专门化的推理路径：User Advocate 对策略保持“盲目”，以最大化效用，而 Policy Agent 提供聚焦的“对抗性”检查。

我们提出 PCN-Rec，它把 LLM 当作提议者（proposer）而不是权威。关键想法是一种可携带证明的交互：LLM 参与协商，但每一份列表都必须通过用代码实现的确定性验证器。PCN-Rec 从一个标准候选生成器（例如 MF/CF）开始，它产生一份排序列表，我们从中取大小为 $W$ 的候选窗口。在这个窗口内，两个智能体代表相互竞争的目标：User Advocate 推动与用户偏好的相关性，Policy Agent 推动治理约束的满足（例如头部/尾部平衡和体裁多样性）。然后调解者 LLM 提出一份 Top-$N$ 列表，并发出一份结构化证书（JSON），描述哪些项目满足哪些约束。关键的是，确定性验证器根据所提出的列表重算全部约束函数，要么接受证书，要么拒绝它。被拒绝时，我们应用确定性的约束贪心修复来产生一份合规列表，重新验证，并记录轨迹以供审计。与单体 LLM 推荐器不同，我们的智能体方法把推荐任务分解成专门角色，确保“有创造性的”提议者与“严格的”验证器解耦。

我们做出三项贡献：

- **面向推荐的可携带证明协商：** 一种智能体框架，其中 LLM 提出列表和结构化证书，但正确性由确定性验证来强制 [6, 20]。
- **可行性分析：** 一种基于窗口大小的方法，把不可满足的用户历史（在 $W$ 内不存在可行列表）与方法失败（存在可行列表，但方法失败了）分开。
- **强治理且效用损失很小的经验证据：** 在 MovieLens-100K 上，PCN-Rec 在可行用户上达到接近完美的通过率，相对单 LLM 基线只有很小的 NDCG@10 下降 [8, 11]。

## 2 方法：面向推荐的可携带证明协商

令 $u$ 表示一个用户，令基础推荐器（例如 MF/CF）产生带预测相关性分数的排序候选列表 $C(u) = \langle i_1, i_2, \ldots \rangle$。我们把注意力限制在包含前 $W$ 个项目的候选窗口 $CW(u)$ 上，目标是输出一份列表 $S \subseteq CW(u)$，$|S| = N$，既有用又合规。

我们考虑必须按列表成立的治理约束 [4, 8, 12]。在我们的实验中，这些包括：（i）头部/尾部曝光约束，它强制最低的长尾表示，并可选地限制头部项目；（ii）体裁多样性约束，它强制列表中不同体裁的最小数量。每个项目 $i$ 带有元数据标签（例如流行度桶：头部/尾部；体裁标签），约束根据这些标签和列表内容确定性地计算。

<!-- 原 PDF 第 2 页 -->

**图 1 见原 PDF。**

图 1：PCN-Rec 可携带证明协商流水线。基础推荐器产生候选窗口（$W$）。两个智能体进行协商（User Advocate 负责相关性；Policy Agent 负责治理），调解者 LLM 提出一份 Top-$N$ 列表以及一份结构化证书。确定性验证器根据列表重算约束，并且只接受经过验证器检查的证书；失败会触发确定性的约束贪心修复，然后重新验证，产生可审计轨迹。

### 2.1 PCN-Rec 框架

图 1 给出概览。PCN-Rec 把自然语言推理与强制执行分开：把 LLM 当作提议者，并把全部正确性保证放在确定性代码中 [1, 2, 7, 14, 21]。

**候选窗口。** 基础推荐器提供一份排序的 $CW(u)$，它定义了所有下游步骤的可行搜索空间。这种“有界”观点对可审计性和可行性分析很重要：如果在 $CW(u)$ 内不存在合规列表，那么失败是不可满足的约束，而不是方法错误。

**协商智能体。** PCN-Rec 使用两个目标互补的智能体 [9, 22]：

- **User Advocate：** 主张那些最大化与用户历史和偏好的相关性的项目。
- **Policy Agent：** 主张那些满足治理约束的项目（例如最小尾部、最大头部、体裁多样性）。

两个智能体都只在 $CW(u)$ 中的候选上操作。

**调解者（LLM）+ 证书。** 调解者 LLM 综合两个智能体的论证，并提出一份 Top-$N$ 列表 $S$，外加一份结构化证书 $c$（JSON）[3, 15, 16, 20]。证书包含（a）被选中的项目 ID，以及（b）验证治理约束所需的显式字段（例如哪些项目被计为尾部；覆盖了哪些体裁），从而能够进行机器可检查的审计。

**确定性验证。** 用代码实现的验证器 $V$ 直接根据 $S$（以及项目元数据）重算全部约束函数，并且仅当每个约束都被满足时才接受输出 [6, 13]。关键的是，验证器并不信任 LLM 文本；它只信任确定性检查。这产生一个可携带证明的接口：系统仅当 $V(S, c) = 1$ 时返回 $(S, c)$。

**确定性修复（故障安全）。** 如果验证失败，PCN-Rec 运行一个确定性的约束贪心修复过程，在可能时从 $CW(u)$ 构造一份合规列表（例如先满足硬约束，再在剩余槽位中最大化相关性）[5, 10, 18]。修复后的列表随后被重新验证，并连同审计轨迹一起返回。这保证了在可行用户上的稳健合规，并把约束不可行与 LLM 提议失败干净地分开。

### 2.2 可行性与方法失败

因为约束是按列表强制的，某些用户在给定窗口大小 $W$ 下可能不可行。因此我们在（i）全部用户和（ii）在 $CW(u)$ 内存在合规列表的可行用户子集上报告结果。这一区分对公平评测至关重要：不可行情形不应被计为算法失败。在第 3 节中，我们量化可行性如何随 $W$ 变化，并用它来选择操作点 $W = 80$。

<!-- 原 PDF 第 3 页 -->

## 3 可行性分析与经验结果

我们在按列表治理约束下，于 MovieLens-100K 上评测 PCN-Rec。我们的核心问题是：给定有界候选窗口，约束何时是可满足的；以及失败何时来自方法（例如 LLM 提议错误），而不是真正的不可行。

### 3.1 问题设定与约束

令 $u$ 表示一个用户。基础推荐器返回排序候选窗口 $CW(u) = \langle i_1, \ldots, i_W \rangle$，带预测相关性分数 $r_u(i)$。一份列表是有序列表 $S = (s_1, \ldots, s_N)$，其中 $s_j \in CW(u)$，且所有项目互异。我们把窗口内的可行列表集合写成

$$
\mathcal{S}_W(u) = \{S \subseteq CW(u) : |S| = N\}. \tag{1}
$$

每个项目 $i$ 有确定性检查所用的元数据（例如流行度桶和体裁集合）。令 $\mathbb{I}[\cdot]$ 为指示函数。我们实例化两种常见的平台约束：

**头部/尾部曝光。** 令 $\mathrm{tail}(i) \in \{0, 1\}$ 表示 $i$ 是否为长尾（并且 $\mathrm{head}(i) = 1 - \mathrm{tail}(i)$）。我们要求至少有比例 $\tau$ 的尾部项目，以及至多有比例 $\kappa$ 的头部项目：

$$
\phi_{\mathrm{tail}}(S) := \frac{1}{N}\sum_{i \in S} \mathrm{tail}(i) \geq \tau, \tag{2}
$$

$$
\phi_{\mathrm{head}}(S) := \frac{1}{N}\sum_{i \in S} \mathrm{head}(i) \leq \kappa. \tag{3}
$$

**体裁多样性。** 令 $G(i)$ 为项目 $i$ 的体裁集合，并把列表覆盖的体裁定义为 $G(S) = \bigcup_{i \in S} G(i)$。我们要求

$$
\phi_{\mathrm{div}}(S) := |G(S)| \geq G_{\min}. \tag{4}
$$

### 3.2 可行性与方法失败

治理约束推荐中的一个关键区分是：约束在候选窗口内是否不可满足。我们把用户的窗口可行性定义为

$$
\mathrm{Feasible}_W(u) = \mathbb{I}\big[\exists S \in \mathcal{S}_W(u) : \phi_{\mathrm{tail}}(S) \wedge \phi_{\mathrm{head}}(S) \wedge \phi_{\mathrm{div}}(S)\big]. \tag{5}
$$

这把不可满足情形（$\mathrm{Feasible}_W(u) = 0$）与失败情形分开：后者存在可行列表，但提议者没能找到它。

操作上，“最好可能”的合规列表的最强概念是约束优化

$$
S^\star_u = \arg\max_{S \in \mathcal{S}_W(u)} \sum_{i \in S} r_u(i) \quad \text{s.t. (2), (3), (4)}. \tag{6}
$$

PCN-Rec 通过（i）LLM 调解的协商和（ii）确定性修复回退来近似 (6)。

### 3.3 可携带证明的验证指标

令调解者产生所提出的列表 $S$ 和结构化证书 $c$（JSON）。验证器用代码重算约束函数，并且仅当（a）证书格式良好且与 $S$ 一致，以及（b）全部治理约束都通过时才接受：

$$
V(S, c) = \mathbb{I}\Big[\mathrm{parse}(c) = S \wedge \bigwedge_{m \in \{\mathrm{tail}, \mathrm{head}, \mathrm{div}\}} \phi_m(S)\Big]. \tag{7}
$$

**图 2 见原 PDF。**

图 2：约束可行性随候选窗口大小 $W$ 的变化。可行性比率（在 $CW(u)$ 内至少存在一份合规列表的用户比例）随 $W$ 增加，而尾部短缺下降。我们选择 $W = 80$ 作为操作点。

我们把治理通过率报告为

$$
\mathrm{PassRate} = \frac{1}{|\mathcal{U}|}\sum_{u \in \mathcal{U}} V(S_u, c_u), \qquad
\mathrm{PassRate}_{\mathrm{feas}} = \frac{1}{|\mathcal{U}^+_W|}\sum_{u \in \mathcal{U}^+_W} V(S_u, c_u), \tag{8}
$$

其中 $\mathcal{U}^+_W = \{u \in \mathcal{U} : \mathrm{Feasible}_W(u) = 1\}$。

### 3.4 效用指标（NDCG@10）

我们用 NDCG@10 [11] 度量排序效用。对排序列表 $(s_1, \ldots, s_K)$，定义

$$
\mathrm{DCG@}K(u) = \sum_{j=1}^{K} \frac{2^{\mathrm{rel}_u(s_j)} - 1}{\log_2(j+1)}, \tag{9}
$$

$$
\mathrm{NDCG@}K(u) = \frac{\mathrm{DCG@}K(u)}{\mathrm{IDCG@}K(u)}, \tag{10}
$$

其中 $\mathrm{IDCG@}K(u)$ 是用户 $u$ 的理想排序的 DCG。

### 3.5 主要发现

图 2 表明，增大 $W$ 会提高可行性（更多用户至少容许一份合规列表），同时减少尾部短缺。我们选择 $W = 80$ 作为操作点，它产生一个较大的可行子集（943 个用户中的 551 个），而又不过度扩大候选集。在可行子集 $\mathcal{U}^+_{80}$ 上，PCN-Rec 达到接近完美的治理合规（经过验证器检查的列表），相对单 LLM 基线只有很小的效用下降（表 1）。这展示了核心权衡：确定性地强制治理，并把 LLM 当作其输出必须携带可检查证明的提议者。

### 3.6 治理合规与效用的权衡

我们把 PCN-Rec 与直接综合 Top-$N$ 列表、而不做确定性验证的单 LLM 基线比较。在可行子集 $\mathcal{U}^+_{80}$ 上，PCN-Rec 达到接近完美的治理合规：经过验证器检查的列表通过率为 0.985（单 LLM 为 0.000），

<!-- 原 PDF 第 4 页 -->

这表明确定性验证消除了脆弱的约束违反。这种合规带来较小的效用下降：NDCG@10 从 0.424 降到 0.403（$\Delta = -0.022$），与强制硬治理约束的预期代价一致。我们也报告一个确定性约束贪心界，作为同一约束集合下可达到的最佳合规效用的参考点。单 LLM 被评测为在同一候选窗口 $CW(u)$ 上的一次性提议者，没有验证或修复；PCN-Rec 增加了经过验证器检查的证书接口，以及一条确定性的故障安全修复路径。

表 1：可行用户上的治理合规与效用（$n=551$，$W=80$）。NDCG@10 一列的三个数 0.424、0.403、0.426 出现在 PDF 文本层中，并与正文“从 0.424 降到 0.403”以及贪心界的叙述对齐；PassRate 列中贪心界为破折号。

| 方法 | PassRate（可行） | NDCG@10 |
| --- | ---: | ---: |
| Single LLM（无验证器） | 0.000 | 0.424 |
| PCN-Rec（经过验证器检查） | 0.985 | 0.403 |
| 确定性贪心界（参考） | — | 0.426 |

效用下降：$\Delta$ NDCG@10 $= -0.022$（PCN-Rec 相对 Single LLM）。

**统计检验。** 为评估效用差异是否稳健，我们在 $\mathcal{U}^+_{80}$ 中的用户上使用配对检验（例如对每个用户的 NDCG@10 做配对 bootstrap）。除非另有说明，我们在 $p < 0.05$ 上报告显著性。

**算法 1** PCN-Rec 推理：可携带证明的验证与确定性修复。

**输入：** 用户 $u$，候选窗口 $CW(u)$，列表大小 $N$，策略约束 $\{\phi_k\}_{k=1}^{K}$。

**输出：** 合规列表 $S$，以及可审计轨迹（证书 + 验证器日志）。

1. $C \leftarrow \mathrm{BaseRank}(u)$（例如 MF/CF 分数）
2. $CW \leftarrow \mathrm{TopW}(C, W)$
3. $(S, c) \leftarrow \mathrm{Negotiate}(u, CW, N)$（LLM 调解者 + 智能体输出列表和结构化证书）
4. **if** $\mathrm{Verify}(S, c, \{\phi_k\})$ **then**
5. **return** $(S, c, \mathrm{Log}(\mathrm{PASS}))$
6. **else**
7. $S' \leftarrow \mathrm{RepairGreedy}(u, CW, N, \{\phi_k\})$
8. $c' \leftarrow \mathrm{MakeCert}(S', \{\phi_k\})$（确定性）
9. **if** $\mathrm{Verify}(S', c', \{\phi_k\})$ **then**
10. **return** $(S', c', \mathrm{Log}(\mathrm{FAIL} \rightarrow \mathrm{REPAIR} \rightarrow \mathrm{PASS}))$
11. **else**
12. **return** $(\bot, \bot, \mathrm{Log}(\mathrm{INFEASIBLE\ within\ } CW(u)))$
13. **end if**
14. **end if**

## 4 讨论与相关工作

**为什么是可携带证明的协商？** 治理约束推荐中的一个实际痛点是：平台策略是硬性的（必须始终成立），并且常常是可审计的（事后必须能够解释）。PCN-Rec 把这一点操作化：让 LLM 成为提议者，并把正确性放在确定性代码中。每一份被提供的列表都附带一份机器可检查的证书，以及验证器给出的显式通过/失败决定。这把合规从“尽力而为”转变为“在可行用户上有保证”，并为审计和调试提供直接的产物。

**与约束推荐的关系。** 先前关于约束推荐和约束排序的方法常常依赖基于优化的重排序、启发式或后处理，以便在保持相关性的同时满足约束 [4, 5, 10, 12, 17, 18]。PCN-Rec 与这条工作线兼容（我们的修复是一个确定性的约束贪心过程），但其接口契约不同：系统返回一个显式的证明对象（证书），它必须在确定性验证器下通过验证，从而使合规透明且可复现 [5, 10, 18]。

**与基于 LLM 和智能体的推荐器的关系。** 基于 LLM 的推荐器可以产生自然语言理由，并自适应地执行多目标对齐偏好，但在严格的组合约束下它们很脆弱。PCN-Rec 使用智能体和 LLM 调解者来获得灵活性和个性化，同时使约束满足独立于 LLM 的文本推理。这种分离保留了 LLM 的接口好处，同时防止静默的约束违反 [2, 9, 14, 21, 22]。

**局限性。** 首先，可行性依赖于候选窗口：如果约束在 $CW(u)$ 内不可满足，任何方法都不能在不扩大窗口或不放松约束的情况下产生合规列表。其次，验证器只检查已被形式化的约束（例如尾部曝光、多样性）；主观或不断演化的策略仍然需要仔细的形式化。第三，证书模式和元数据质量很重要：不正确的项目元数据会造成假拒绝或假接受，除非元数据框架被信任并被监控。

**未来工作。** 自然的扩展包括（i）更丰富的约束族（例如跨群体的公平约束、多列表曝光预算），（ii）按用户自适应选择 $W$，以在控制计算量的同时减少不可行性，以及（iii）把修复与效用优化更紧地耦合（例如近似保证，或仍然对验证器安全的学习式修复策略）。

## 5 结论

我们提出了 PCN-Rec，一个面向治理约束推荐的可携带证明协商框架。核心设计选择是把 LLM 当作能够协商相关性与策略权衡的提议者，同时通过在代码中重算全部约束的确定性验证器来强制正确性。这产生一个可审计接口：每一份被提供的列表都附带结构化证书和显式的验证器决定。

在经验上，我们表明治理失败应当被分成（i）有界候选窗口内的真正不可行，以及（ii）存在可行列表但提议者失败时的方法失败。在 MovieLens-100K 的按列表约束下，PCN-Rec 在可行用户上达到接近完美的治理合规 [8]，NDCG@10 只有很小的下降，说明了一条部署 LLM 驱动的推荐器而又不出现静默策略违反的实用做法。

<!-- 原 PDF 第 5 页 -->

## 6 局限性、伦理与可复现性

### 6.1 局限性

PCN-Rec 只在候选窗口 $CW(u)$ 内可行的条件下保证合规。如果对某个用户、在所选的 $W$ 上约束不可满足，任何协商策略都不能在不扩大窗口、不放松约束或不改变候选生成器的情况下产生合规列表。其次，验证器的好坏只取决于被形式化的约束和元数据质量（例如尾部/头部标签和体裁标签）；元数据中的错误会导致不正确的接受/拒绝决定。第三，尽管确定性修复是稳健的，它可能相对全局最优的约束排序引入效用差距；在保持对验证器安全的同时缩小这一差距，是一个重要方向。

### 6.2 伦理与治理方面的考虑

我们的目标是改进平台问责：必须成立的策略（例如曝光约束）由代码强制，并被记录以供审计。然而，治理约束可能被误用，或编码价值判断（例如什么算作“多样性”或“长尾”），因此利益相关者应当记录策略意图，并对照真实结果验证指标。审计日志和证书如果存储不当，也可能泄露敏感的偏好信号；部署应当尽量减少被记录的个人数据，施加访问控制，并考虑聚合/匿名化。最后，LLM 组件可能产生有说服力但误导的理由；PCN-Rec 缓解了静默的策略违反，但除非解释性声称本身也被验证，它并不自动保证解释是忠实的。

### 6.3 可复现性清单

为支持可复现性和审计，我们建议如下产物与报告内容：

- **数据与划分：** MovieLens-100K 版本、预处理步骤、训练/测试划分协议，以及评测用户。
- **候选生成：** 基础模型（例如 MF/CF）、超参数，以及 $CW(u)$ 的精确定义。
- **约束定义：** 显式公式和阈值（$\tau$、$\kappa$、$G_{\min}$），以及头部/尾部和体裁如何被指定。
- **验证器 + 证书模式：** JSON 模式字段、解析规则，以及确定性验证的代码路径。
- **LLM 设定：** 模型名称/版本、解码设置、智能体/调解者的系统提示，以及速率限制/超时。
- **确定性修复：** 算法细节（排序、平局打破），以及通过固定种子控制的任何随机性。
- **指标与检验：** NDCG@10 的计算细节，以及配对显著性检验过程。

总体而言，PCN-Rec 提供了一种轻量、可部署的模式，把 LLM 的灵活性与确定性的治理保证结合起来。

## 参考文献

[1] Keqin Bao, Jizhi Zhang, Wenkai Zhang, Yuxiang Biao, Hao Wang, Yong Yu, and Fang Zhang. 2023. TALLRec：把大语言模型与推荐对齐的有效且高效调优框架. In Proceedings of the 17th ACM Conference on Recommender Systems (RecSys ’23). ACM. doi:10.1145/3604915.3608857

[2] Keqin Bao, Jizhi Zhang, Wenkai Zhang, Yuxiang Biao, Hao Wang, Yong Yu, and Fang Zhang. 2024. 用于推荐的大语言模型：进展与未来方向. In Companion Proceedings of the ACM Web Conference 2024 (WWW ’24 Companion). ACM. doi:10.1145/3589335.3651581

[3] Luca Beurer-Kellner, Marc Fischer, and Martin Vechev. 2022. 提示即编程：面向大语言模型的查询语言. arXiv preprint arXiv:2212.06094 (2022). doi:10.48550/arXiv.2212.06094

[4] Diego Carraro and Derek Bridge. 2024. 用大语言模型重排序来增强推荐多样性. ACM Transactions on Recommender Systems (2024). doi:10.1145/3700604

[5] Clément Deffayet, Sébastien Foucher, and Romain Gaudel. 2023. 用强化学习做生成式列表推荐. In Proceedings of the 16th ACM International Conference on Web Search and Data Mining (WSDM ’23). ACM. doi:10.1145/3539597.3570412

[6] Wen Fan, Marilyn Rego, Xin Hu, Sanya Dod, Zhaorui Ni, Danning Xie, Jenna DiVincenzo, and Lin Tan. 2024. 评估大语言模型在 VeriFast 中生成可验证规范的能力. arXiv preprint arXiv:2411.02318 (2024). doi:10.48550/arXiv.2411.02318

[7] Shijie Geng, Shuchang Liu, Zuohui Fu, Yingqiang Ge, and Yongfeng Zhang. 2022. 把推荐当作语言处理（RLP）：统一的预训练、个性化提示与预测范式（P5）. In Proceedings of the 16th ACM Conference on Recommender Systems (RecSys ’22). ACM. doi:10.1145/3523227.3546767

[8] F. Maxwell Harper and Joseph A. Konstan. 2015. MovieLens 数据集：历史与背景. ACM Transactions on Interactive Intelligent Systems 5, 4, Article 19 (2015). doi:10.1145/2827872

[9] Xu Huang, Jianxun Lian, Yuxuan Lei, Jing Yao, Defu Lian, and Xing Xie. 2023. 推荐 AI 智能体：集成大语言模型以进行交互式推荐. arXiv preprint arXiv:2308.16505 (2023). doi:10.48550/arXiv.2308.16505

[10] Dietmar Jannach. 2023. 多目标推荐系统：综述与挑战. Frontiers in Big Data (2023). doi:10.3389/fdata.2023.1157899

[11] Kalervo Järvelin and Jaana Kekäläinen. 2002. 基于累积增益的信息检索技术评测. ACM Transactions on Information Systems 20, 4 (2002), 422–446. doi:10.1145/582415.582418

[12] Anna Klimashevskaia, Alexander Felfernig, Thanh Tran, et al. 2023. 缓解推荐系统中的流行度偏差：综述与未来方向. arXiv preprint arXiv:2308.01118 (2023). doi:10.48550/arXiv.2308.01118

[13] Jeffrey Lentz et al. 2025. 大语言模型能否验证系统软件？一项案例研究. In Proceedings of the 2025 Workshop on Hot Topics in Operating Systems (HotOS ’25). ACM. doi:10.1145/3713082.3730382

[14] Jiacheng Li, Shuo Xu, Wei Wang, et al. 2024. 用于生成式推荐的大语言模型：综述与展望. In Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024). https://aclanthology.org/2024.lrec-main.893/

[15] Ximing Lu, Sean Welleck, Peter West, Omer Levy, Ashish Sabharwal, and Yejin Choi. 2022. NeuroLogic A*：面向可控文本生成的有效且高效的 A* 搜索. In Proceedings of the 2022 Conference of the North American Chapter of the ACL: Human Language Technologies (NAACL 2022). doi:10.18653/v1/2022.naacl-main.57

[16] Kostis Michailidis, Dimitris Tsouros, and Tias Guns. 2024. 用上下文学习让 LLM 做约束建模. In 30th International Conference on Principles and Practice of Constraint Programming (CP 2024). doi:10.4230/LIPIcs.CP.2024.20

[17] Jie Ren, Wei Zhang, Yongfeng Zhang, et al. 2022. 通过基于梯度的再加权缓解推荐中的流行度偏差. arXiv preprint arXiv:2211.01154 (2022). doi:10.48550/arXiv.2211.01154

[18] Jie Ren, Wei Zhang, Yongfeng Zhang, et al. 2023. 面向推荐的列表感知排序. In Proceedings of the 16th ACM International Conference on Web Search and Data Mining (WSDM ’23). ACM. doi:10.1145/3539597.3570380

[19] Markus Schedl, Yashar Deldjoo, Pablo Castells, and Emine Yilmaz. 2025. 可信推荐系统专刊导言. ACM Transactions on Recommender Systems (2025). doi:10.1145/3702249

[20] Zhaoyang Wang, Jinqi Jiang, Huichi Zhou, Wenhao Zheng, Xuchao Zhang, Chetan Bansal, and Huaxiu Yao. 2025. 大语言模型生成的可验证格式控制. In Findings of the Association for Computational Linguistics: NAACL 2025. doi:10.18653/v1/2025.findings-naacl.194

[21] Likang Wu, Zhi Zheng, Zhaopeng Qiu, Hao Wang, Hongchao Gu, Tingjia Shen, Chuan Qin, Chen Zhu, Hengshu Zhu, Qi Liu, and Hui Xiong. 2024. 用于推荐的大语言模型综述. World Wide Web (2024). doi:10.1007/s11280-024-01291-2

[22] Yu Zhang, Shutong Qiao, Jiaqi Zhang, Tzu-Heng Lin, Chen Gao, and Yong Li. 2025. 大语言模型赋能的推荐与搜索智能体综述：迈向下一代信息检索. arXiv preprint arXiv:2503.05659 (2025). doi:10.48550/arXiv.2503.05659

[23] Chiwei Zhu, Benfeng Xu, Quan Wang, Yongdong Zhang, and Zhendong Mao. 2023. 论大语言模型的校准与对齐. arXiv preprint arXiv:2311.13240 (2023). doi:10.48550/arXiv.2311.13240

<!-- 译完 -->
