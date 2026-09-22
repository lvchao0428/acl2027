# Optimizing User Profiles via Contextual Bandits for Retrieval-Augmented LLM Personalization

| 项目 | 内容 |
|------|------|
| **Paper** | Optimizing User Profiles via Contextual Bandits for Retrieval-Augmented LLM Personalization |
| **Authors** | Linfeng Du, Ye Yuan, Zichen Zhao, Fuyuan Lyu, Emiliano Penaloza, Xiuying Chen, Zipeng Sun, Jikun Kang, Laurent Charlin, Xue Liu, Haolun Wu |
| **Affiliation** | McGill University; Mila – Quebec AI Institute; MBZUAI; Université de Montréal; Salesforce; HEC Montréal |
| **Theme** | RAG 个性化 / Contextual Bandit / User Profile 优化 |
| **Problem** | RAG 个性化通常按语义相关性选记录，但 relevance 是 utility 的不可靠代理；记录 utility 非单调（更多记录不一定更好），需学习最优 profile 组合 |
| **Method** | PURPLE：contextual bandit 框架；Plackett-Luce 排序模型建模记录间依赖；token-level cross-attention 建模 query-record 交互；以 frozen LLM 对 reference response 的 log-likelihood 作为 dense reward（等价于最大化 RAG 边缘化的 ELBO） |
| **Benchmark** | 9 个 personalization 任务（分类、回归、短/长文本生成） |
| **Result** | consistently 优于 heuristic 与 retrieval-augmented 基线；风格化 persona 适应的人类评估 preference margin 达 14.4% |
| **Question** | Frozen LLM 的 log-likelihood 作为 reward 是否偏向 LLM 自身偏好而非用户真实偏好？Plackett-Luce 在记录数较大时的计算开销如何？ |

## 详细笔记

### 研究背景与动机

Retrieval-Augmented Generation（RAG）用于 LLM 个性化时，常见做法是按语义相似度从用户历史中检索相关记录构建 user profile。然而：

1. **Relevance ≠ Utility**：语义相关的记录未必对当前任务最有用；有时看似不相关的记录反而提供关键风格/偏好信号。
2. **Utility 非单调性**：profile 中记录数量与最终生成质量并非单调关系——过少信息不足，过多则引入噪声，存在最优子集。
3. **记录间依赖**：记录组合效果非简单叠加，需建模 inter-record dependencies。

作者来自 McGill、Mila，提出 PURPLE（oPtimizes UseR Profiles for LLM pErsonalization），用 contextual bandit 框架学习最优 profile 选择策略。

### 核心方法详解

**PURPLE 框架**：

1. **Contextual Bandit formulation**：
   - Context：当前 query + 候选记录池
   - Action：选择哪些记录组成 user profile
   - Reward：frozen LLM 对 reference response 的 log-likelihood
   - 目标：学习最大化 expected reward 的 profile 选择策略

2. **Plackett-Luce 排序模型**：
   - 建模记录间的相对优先级与依赖关系
   - 避免将记录独立对待导致的组合次优

3. **Token-level Cross-Attention**：
   - 在 query 与每条 candidate record 之间做细粒度交互建模
   - 捕获"哪些 record 的哪些部分对当前 query 有用"

4. **Dense Reward Signal**：
   - 使用 frozen LLM 对 ground-truth reference response 的 log-likelihood 作为 reward
   - 理论等价于最大化 RAG 边缘化目标的 ELBO（Evidence Lower Bound）
   - 无需额外 human annotation 即可提供可微、稠密的训练信号

### 实验设置与结果

- **任务**：9 个 personalization 任务，覆盖分类、回归、短文本生成、长文本生成
- **基线**：Heuristic retrieval（如 top-k semantic similarity）、其他 retrieval-augmented 方法
- **评估**：Automatic metrics + 人类评估（风格化 persona 适应）
- **关键结果**：
  - 所有 9 个任务上 consistently 优于基线
  - 人类评估中 preference margin 达 14.4%（风格化 persona 适应场景）

### 个人思考

PURPLE 巧妙地将 profile 选择重新定义为 bandit 问题，并用 LLM 自身的 log-likelihood 作为 self-supervised reward，避免了昂贵的人工标注。与 MemRec（05）等 memory 管理工作的关系：PURPLE 关注"选哪些记录"，MemRec 关注"如何存储与更新记忆"，可组合使用。潜在风险：frozen LLM 的 log-likelihood 可能反映 LLM 训练语料的偏好而非目标用户偏好，在高度个性化场景下需验证。Plackett-Luce + cross-attention 的设计对记录池规模敏感，大规模候选集下的效率值得进一步讨论。
