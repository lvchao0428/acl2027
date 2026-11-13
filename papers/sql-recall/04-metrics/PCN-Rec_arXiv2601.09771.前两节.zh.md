> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名**：PCN-Rec_arXiv2601.09771.pdf

**原文标题**：PCN-Rec: Agentic Proof-Carrying Negotiation for Reliable Governance-Constrained Recommendation

**作者**：Aradhya Dixit（Wake Technical Community College, Raleigh, North Carolina）；Shreem Dixit（University of North Carolina at Charlotte, Charlotte, North Carolina）。

**场合**：LARS @ WWW ’26, 2026, TBD；arXiv:2601.09771v1 [cs.AI]，2026 年 1 月 14 日。

## 摘要

基于大模型的推荐系统能排出看起来很有说服力的列表，但很难稳定满足治理约束，例如长尾曝光的下限或多样性要求。PCN-Rec 是一条 proof-carrying negotiation 流水线：自然语言推理和确定性的强制执行分开。基础推荐器（MF/CF）先给出大小为 \(W\) 的候选窗口；两个 agent 在窗口里协商，User Advocate 优化相关性，Policy Agent 执行约束。一个 mediator LLM 综合出 Top-\(N\) slate，并附上一份结构化 certificate（JSON），声称这些约束已经满足。确定性 verifier 再根据 slate 把全部约束重算一遍，只接受核验通过的证书。核验失败时，用确定性的 constrained-greedy repair 造出一份合规 slate，重新核验，并留下可审计的轨迹。

在带治理约束的 MovieLens-100K 上，对可行用户（\(n=551\)，\(W=80\)），PCN-Rec 的通过率为 98.55%，对照的是没有验证、也没有修复的 one-shot 单 LLM 基线。效用方面，NDCG@10 绝对下降 0.021（0.403 对 0.424），差异在 \(p<0.05\) 上显著。摘要没有给出该基线自己的通过率。

## 1 Introduction

线上推荐系统面对的是硬约束，而不只是相关性：长尾曝光下限、类型多样性、每份 slate 的政策上限（文献 [10, 12, 19]）。这些约束常常来自法律或合同，而且必须可审计：平台要能说明为什么推了这份列表，并证明政策检查确实过了。近期的大模型推荐能用自然语言写出有说服力的排序，但一碰到严格的组合要求就脆（[1, 2, 7, 14, 21]）。单个大模型可以给出像样的理由，列表却仍然违规；它的推理也不能直接执行或核验。作者还指出，单体大模型会碰到 lost-in-the-middle，也维持不住组合约束上的全局状态（[23]）。因此他们把任务拆成 agent 之间的竞争：User Advocate 对政策“看不见”，专心把效用拉高；Policy Agent 做有针对性的对抗检查。

PCN-Rec 把大模型当成提议者，而不是权威。关键是 proof-carrying 的交互：模型可以参与协商，但每一份 slate 都必须通过用代码实现的确定性 verifier。流程从标准候选生成器（如 MF/CF）的排序列表里截取大小为 \(W\) 的窗口。窗口内，User Advocate 推相关性，Policy Agent 推治理约束（如头部/尾部平衡和类型多样性）。mediator LLM 提出 Top-\(N\) slate，并输出结构化 certificate，说明哪些物品满足哪些约束。verifier 根据这份 slate 重算全部约束函数，接受或拒绝。被拒绝就做确定性的 constrained-greedy repair，再核验，并把轨迹记下来供审计。和单体大模型推荐的差别是：提议的一方和严格核验的一方拆开。

贡献有三条。第一，面向推荐的 proof-carrying negotiation：大模型提议 slate 和结构化证书，正确性由确定性验证来保证（[6, 20]）。第二，可行性分析：用窗口大小把两种失败分开——用户历史在 \(W\) 内根本不存在可行 slate（不可满足），以及可行 slate 存在但方法没找到（方法失败）。第三，治理可以做得很严、效用损失很小：在 MovieLens-100K 上，相对单 LLM 基线，可行用户的通过率接近满分，NDCG@10 只降一点（[8, 11]）。具体的 98.55% 和 0.021 写在摘要里，引言没有再列这组数字。

## 2 Method: Proof-Carrying Negotiation for Recommendation

用户记为 \(u\)。基础推荐器（如 MF/CF）给出带预测相关性分数的排序候选 \(C(u)=\langle i_1,i_2,\ldots\rangle\)。实际只看前 \(W\) 个组成的窗口 \(C_W(u)\)，输出 slate \(S\subseteq C_W(u)\)，且 \(|S|=N\)，既要有用也要合规。约束是按每一份 slate 计算的（[4, 8, 12]）。实验里用两类：head/tail exposure，要求长尾代表达到下限，并可选地给头部物品封顶；genre diversity，要求 slate 里不同题材至少达到某个数目。每件物品带元数据（流行度桶 head/tail，以及题材标签），约束由这些标签和 slate 内容确定性算出。

**2.1 PCN-Rec Framework。** 图 1 把大模型放在提议侧，把正确性放进确定性代码。候选窗口 \(C_W(u)\) 是后续所有步骤的搜索空间；若窗口里根本没有合规 slate，失败应算约束不可满足，而不是方法出错。两个 agent 目标互补（[9, 22]），且都只在 \(C_W(u)\) 里挑：User Advocate 按用户历史和偏好把相关性拉高；Policy Agent 推动 min-tail、max-head 和题材多样性。mediator LLM 综合双方论点，提出 Top-\(N\) 的 \(S\)，并给出证书 \(c\)（JSON）（[3, 15, 16, 20]）。证书里有选中的物品 ID，以及核验所需的显式字段，例如哪些物品算作尾部、覆盖了哪些题材。代码里的 verifier \(V\) 直接从 \(S\) 和物品元数据重算全部约束，只有每一条都满足才接受（[6, 13]）。它不信任模型写出的文字，系统只在 \(V(S,c)=1\) 时返回 \((S,c)\)。若核验失败，constrained-greedy repair 在可能时从 \(C_W(u)\) 造出合规 slate：先满足硬约束，再在剩余位置上把相关性尽量做高（[5, 10, 18]）。修好的 slate 重新核验，并连同审计轨迹一起返回。这样，可行用户上的合规更稳，也把“约束本身不可行”和“模型提议失败”分开。

**2.2 Feasibility vs. Method Failure。** 约束按 slate 执行时，给定窗口 \(W\)，有些用户就是不可行的。因此结果分两套报告：全部用户，以及窗口内确实存在合规 slate 的可行用户。不可行的例子不应算成算法失败。本节说明，可行性如何随 \(W\) 变化、以及为何把工作点定在 \(W=80\)，放到第 3 节量化；该节的实验表此处不展开。
