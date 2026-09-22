# AlignUSER: Human-Aligned LLM Agents via World Models for Recommender System Evaluation

| 项目 | 内容 |
|------|------|
| **Paper** | AlignUSER: Human-Aligned LLM Agents via World Models for Recommender System Evaluation |
| **Authors** | Nicolas Bougie, Gian Maria Marconi, Xiaotong Ye, Narimasa Watanabe |
| **Affiliation** | Woven by Toyota |
| **Theme** | 用户模拟 / LLM Agent / 推荐系统评估 |
| **Problem** | 推荐系统评估中 offline 指标与真实用户行为存在 gap；现有 LLM 合成用户依赖 few-shot prompting，对环境理解浅层，难以可靠替代真实用户 |
| **Method** | (1) World modeling 作为 next-state prediction 任务，使 agent 内化环境动力学；(2) Counterfactual trajectory 生成并与人类选择对比以提取 lessons；(3) AlignUSER+ 增加 graph-based memory 与 causal reasoning |
| **Benchmark** | OPeRA benchmark、购物与 RS 评估场景、AmazonBook |
| **Result** | AlignUSER+ 达 89.3% thought-action consistency、85.6% persona-behavior consistency；与真实 A/B 测试 Spearman 相关 0.71；显著优于 SimUSER、Agent4Rec、RecAgent |
| **Question** | World model 在长尾/冷启动场景下的泛化能力如何？Graph memory 的构建成本与更新策略是否适合大规模在线评估？ |

## 详细笔记

### 研究背景与动机

推荐系统的评估长期面临"offline-online gap"：Hit Rate、NDCG 等 offline 指标与真实 A/B 测试中的用户行为（点击率、转化率、留存）往往不一致。LLM agent 作为 synthetic user 进行模拟评估是近年新兴方向，但现有方法（SimUSER、Agent4Rec、RecAgent 等）主要依赖 few-shot prompting，agent 对推荐环境（物品空间、用户状态转移、反馈机制）的理解停留在表面，导致：

- Thought-action 不一致（想一套做一套）
- Persona-behavior 不一致（人设与行为脱节）
- 与真实 A/B 结果相关性低

作者来自 Woven by Toyota，提出 AlignUSER，通过 world modeling 使 LLM agent 真正"理解"推荐环境，并与人类行为对齐。

### 核心方法详解

**AlignUSER 三阶段设计**：

1. **World Modeling（世界建模）**：
   - 将环境动力学建模为 next-state prediction 任务
   - Agent 通过预测"给定当前状态与动作，下一状态是什么"来内化推荐环境的转移规律
   - 相比 few-shot prompting，world model 提供结构化的、可泛化的环境理解

2. **Counterfactual Trajectory Learning（反事实轨迹学习）**：
   - 生成 counterfactual trajectories（若用户做了不同选择，轨迹会如何演变）
   - 与人类真实选择对比，提取 lessons（哪些决策模式与人类一致/不一致）
   - 用这些 lessons 进一步对齐 agent 行为

3. **AlignUSER+（增强版）**：
   - **Graph-based Memory**：以图结构存储用户-物品-交互关系，支持复杂依赖检索
   - **Causal Reasoning**：引入因果推理，区分相关性与因果性，避免 spurious correlation 导致的错误模拟

### 实验设置与结果

- **Benchmark**：OPeRA benchmark、购物场景、RS 评估场景、AmazonBook
- **基线**：SimUSER、Agent4Rec、RecAgent
- **评估维度**：
  - Thought-action consistency（思维-行动一致性）
  - Persona-behavior consistency（人设-行为一致性）
  - 与真实 A/B 测试结果的 Spearman 相关系数
- **关键结果**：
  - AlignUSER+：89.3% thought-action consistency，85.6% persona-behavior consistency
  - 与真实 A/B 测试 Spearman ρ = 0.71（显著高于基线）
  - 在多个场景下 consistently 优于 SimUSER、Agent4Rec、RecAgent

### 个人思考

AlignUSER 将 user simulator 从"prompt 工程"提升到"world model + 反事实学习"的范式，与 MirroringUsers（07）形成互补：前者强调环境理解，后者强调 preference alignment via user feedback。0.71 的 A/B 相关性在 synthetic evaluation 领域已属较高水平，但仍意味着约 30% 方差无法解释——需明确其适用边界（哪些 RS 场景可信赖模拟结果）。Graph memory + causal reasoning 的 AlignUSER+ 设计合理，但图构建与维护成本是实际部署的关键瓶颈。对工业界而言，若能在更大规模电商场景验证，将大幅推动 LLM-based offline evaluation 的落地。
