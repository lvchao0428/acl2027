# HARPO: Hierarchical Agentic Reasoning for User-Aligned Conversational Recommendation

| 项目 | 内容 |
|------|------|
| **Paper** | HARPO: Hierarchical Agentic Reasoning for User-Aligned Conversational Recommendation |
| **Authors** | Subham Raj, Aman Vaibhav Jha, Mayank Anand, Sriparna Saha |
| **Affiliation** | IIT Patna; IIIT Allahabad |
| **Theme** | 对话式推荐 / Agentic Reasoning / 偏好优化 |
| **Problem** | 现有对话式推荐系统优化的是代理指标（Recall@K、BLEU）而非推荐质量本身，导致实际推荐效果与指标表现脱节 |
| **Method** | 四大组件：(i) CHARM - 层次化偏好学习（relevance/diversity/satisfaction/engagement 四维度 + 上下文依赖权重）；(ii) STAR - 基于 value network 的审慎树搜索推理；(iii) BRIDGE - 领域无关的推理抽象 + Virtual Tool Operations；(iv) MAVEN - 多 agent 协作精炼。使用 DeepSeek-R1-Distill-Qwen-7B 骨干 |
| **Benchmark** | ReDial, INSPIRED, MUSE |
| **Result** | 相比 GPT-4 平均提升 17-21%；INSPIRED 上 R@10 提升 45.7%；CHARM 与人类判断的 Pearson 相关系数达 0.64-0.73 |
| **Question** | 树搜索推理的计算开销在实时对话场景中是否可接受？四个维度的权重如何在不同领域间迁移？ |

## 详细笔记

### 研究背景与动机

对话式推荐系统（CRS）需要在用户逐步揭示偏好的过程中做出推荐决策，本质上是不确定性下的决策问题。然而现有方法虽然在 Recall@K 和 BLEU 等代理指标上表现优异，但在实际推荐质量上往往不尽人意——因为它们优化的是中间目标，而非推荐质量本身。

来自 IIT Patna 的 Raj 等人提出 HARPO，将对话式推荐重新定义为一个结构化决策过程，显式优化多维度推荐质量。

### 核心方法详解

**CHARM（Hierarchical Preference Learning）**：将推荐质量分解为四个可解释维度（Relevance、Diversity、Satisfaction、Engagement），学习上下文依赖的权重，在不同对话阶段四个维度的重要性动态调整。

**STAR（Deliberative Tree-Search Reasoning）**：展开多条候选推荐策略路径，使用学习到的 value network 评估每条路径的预测推荐质量，选择最优路径生成最终回复——类似"先想后说"的决策模式。

**BRIDGE（Domain-Agnostic Reasoning）**：Virtual Tool Operations 实现领域无关的推理抽象，使推荐推理能力跨领域迁移。

**MAVEN（Multi-Agent Refinement）**：多 agent 协作精炼，通过专业化的 Recommender、Explainer 等角色协作改进推荐。整体使用 DeepSeek-R1-Distill-Qwen-7B 作为骨干模型。

### 实验设置与结果

- **数据集**：ReDial、INSPIRED、MUSE 三个对话式推荐基准
- **关键结果**：相比 GPT-4 平均提升 17-21%；INSPIRED 上 R@10 提升 45.7%；人类评估推荐质量、解释质量、整体评分分别比 GPT-4 高 +0.55、+0.50、+0.55

### 个人思考

HARPO 的最大亮点是"直接优化推荐质量而非代理指标"——这在推荐系统研究中是重要的范式转变。CHARM 将推荐质量分解为四个可解释维度的做法非常优雅。在 INSPIRED 上的巨大提升说明社交对话场景中隐式偏好推理是现有方法的软肋。值得关注的是树搜索推理的延迟问题——在实时对话中用户对响应时间很敏感。
