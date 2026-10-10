# ACL 2027 选题 Proposal：Agent × RecSys

> 作者：charlie（PKU 在职）| 版本：v0.1（2026-09-22，课前选题稿）| 配套调研：[01_ACL2024-2026_Agent+RecSys_调研.md](01_ACL2024-2026_Agent+RecSys_调研.md)
> 目标会议：ACL 2027（京都，2027-08-17~22），ARR 投稿截止 **2027 年 1 月**（具体日期 TBA），距今约 **4 个月**。

---

## 0. 一页摘要（给老师）

| 项目 | 内容 |
|---|---|
| **暂定题目** | **The Delegation Gap: Do LLM Agents Choose What Their Users Would?** — Measuring and Closing the Divergence between Recommendation Delegates and the Users They Represent |
| **一句话 idea** | 推荐的"消费者"正在从人变成**替人做决定的 LLM agent**（agentic commerce）。我们用**真实用户的真实购买 + 事后满意度**做 ground truth，系统测量"agent 替我选" 与 "我自己选 / 我事后满意" 之间的差距（delegation gap），刻画差距的系统性来源（位置 / 价格 / 评论数 / 营销文案 / 赞助标签 / 身份刻板印象），比较不同"偏好传递通道"（指令 / 画像 / 历史 / 澄清提问）的性价比，并训练一个 4B–8B 的开源受托 agent，在**一致性、避免踩雷、抗操纵**三方面超过 GPT-5 级 API 模型。 |
| **为什么是现在** | ① Spotify 团队 2026-09 的 RecSys position paper（*Who Are We Recommending To?*）刚把 "recommending to agents / dual-audience / regret-based evaluation / manipulation" 列为议程，**但没有任何实验**；② ACL 2026 刚开源了做这件事所需的全部原料：OPeRA（真人购物会话含最终购买）、Mirroring Users（3B 对齐模拟器）、ShopSimulator（中文环境）、BLaIR/Amazon Reviews 2023；③ 现有购物 agent benchmark（EComAgentBench、Shopping Companion、ShopperBench、ShopSimulator）全部用**合成 persona / 脚本 rubric**打分，**没有一个用真实用户的选择与满意度**。 |
| **为什么是我** | agent 背景（agent 架构、prompt/tool/RL 训练流程熟悉）正好是这个题的核心；推荐侧只需要 Amazon 数据处理与标准评测协议，入门成本可控。 |
| **三条贡献** | (1) **DelegateBench**：首个以真实用户选择 + 满意度为 ground truth、带因果干预探针的"推荐受托"评测集（Amazon 多品类 + OPeRA 真人会话 + 可选中文 ShopSimulator）；(2) **系统实证**：6+ 个前沿 LLM 的 delegation gap 分解、"模拟器 ≠ 受托人"的实证、四种偏好传递通道的性价比曲线；(3) **方法**：Preference-Grounded Delegate（SFT + 满意度加权 DPO + 操纵不变性正则 + 预算化澄清提问），小模型超 API。 |
| **数据集** | Amazon Reviews 2023 + Amazon-C4（主）、OPeRA（真人对照）、ShopSimulator（中文迁移，可选）、UserMirrorer（模拟器对照 / oracle） |
| **模型 / 算力** | API：GPT-5、Claude、Gemini、DeepSeek；开源：Qwen3-4B/8B/32B、Llama-3.x；训练：Qwen3-4B/8B LoRA（RTX 5090 32GB 可跑），RL 阶段可选租 A100/H800。预算估算 **≤ 1 万元**（API ≈ 3k，租卡 ≈ 4–6k）。 |
| **时间线** | 10 月：数据 + baseline；11 月：分析 + 通道实验；12 月：训练 + 鲁棒性；1 月：写作与投稿。 |
| **备选方向** | 第 4 节：*Goodhart in Simulator-Trained Conversational Recommendation Agents*（模拟器作为 RL reward 的可靠性与鲁棒训练） |

---

## 1. 从调研到选题的逻辑

### 1.1 三届 ACL 的演进（详见调研文档）
- **ACL 2024**：LLM-as-Recommender 打地基（BinLLM、RecLM-gen、RDRec、NL user profile、LLM 合成 CRS 数据、Stealthy Attack）。agent 几乎没出现。
- **ACL 2025**：Agent 化。推荐侧 agent 用 DPO/RL 调（T-PRA、ECPO），**用户侧 agent** 出现（iAgent: user–agent–platform 范式），用户模拟器开始被训练与对齐（USP、SimUSER、AILO）。
- **ACL 2026**：RL + 推理 + 环境。GRPO 训练推理型推荐器（OneRec-Think、ReRec、ROS、HARPO），agentic memory（MemRec），模拟器用真实反馈/世界模型对齐（Mirroring Users、AlignUSER），购物 agent 有了训练环境与真人数据（ShopSimulator、OPeRA），agentic 安全（Visual Inception）。

### 1.2 排除掉的方向（避免撞车 / 算力不匹配）
| 方向 | 排除理由 |
|---|---|
| 推理 + RL 生成式推荐 | ACL'26 主流，工业数据 + 集群算力优势明显；个人 5090 难以形成对比 |
| agentic 记忆 / 兴趣漂移 / 遗忘 | 2026-07~09 arXiv 已有 AtomRec、MEMOIR、LION、CALMRec、EvoRec 连发，半年内饱和 |
| "又一个"购物 agent benchmark | ShopSimulator、OPeRA、ShopperBench、EComAgentBench、Shopping Companion 五个在一年内出现 |
| 物品文本对抗攻击 | Stealthy Attack / CheatAgent / Visual Inception 已形成攻防范式 |

### 1.3 留下的缺口
- **Gap A（主推）**：agent 作为推荐的**消费者 / 受托人**——只有 position paper 与两篇合成场景的行为学探针（sponsorship bias、role coherence），**无真实用户 ground truth、无多品类实证、无训练方法**。
- **Gap B（备选）**：用户模拟器作为 RL reward 的 **Goodhart 风险**——被 PEPPER、"How Reliable is Your Simulator"、Turing-RL 反复提及，但推荐域无人系统测量与防御。

---

## 2. 主推方向：The Delegation Gap

### 2.1 问题定义

**场景**（对应 position paper 的 "delegable context"）：用户 \(u\) 给受托 agent 一条自然语言指令 \(q\)（"我需要一个洗澡时能逗孩子玩、弄脏也没关系的玩具"），agent 可以访问 \(u\) 的部分信息（画像 \(P_u\) / 历史 \(H_u\)），也可以向用户提**不超过 \(k\) 个澄清问题**；平台返回候选集 \(C=\{c_1,\dots,c_K\}\)（含标题、价格、均分、评论数、要点、若干条他人评论，以及可能的 [Sponsored] 标签 / 营销文案）；agent 必须替用户**选定一个**（或给出 top-n）。

**Ground truth**：\(u\) 真实购买的商品 \(i^*\in C\) 与其事后评分 \(r^*\)。

**Delegation gap** 的两面：
- **满意型 episode**（\(r^*\ge 4\)）：好受托人应**与用户一致**（选 \(i^*\)）。
- **后悔型 episode**（\(r^*\le 2\)，verified purchase）：好受托人应**与用户不一致**——避开 \(i^*\)、选一个同样满足 \(q\) 硬约束但质量更高的替代品。

> 这正是 **delegate ≠ simulator** 的关键：模拟器的目标是复现人（包括人的错误），受托人的目标是服务人的利益。我们会用 UserMirrorer（ACL'26 模拟器）作为对照，预期它在后悔型 episode 上"忠实地"复现踩雷。

### 2.2 基本想法与假设

- **H1（gap 存在且系统化）**：前沿 LLM 在 \(K=10\) 时与真实用户的一致率显著低于人类自我一致性上界；偏差不是随机的，而是集中在几类可解释的因素：过度依赖均分/评论数（"平均消费者"先验）、位置偏差、价格锚定、对营销文案与 [Sponsored] 标签的敏感性、以及由身份线索触发的刻板化推荐（延续 ACL'25 *Stereotype or Personalization?*）。
- **H2（通道性价比不同）**：指令-only < +NL 画像（PersonaX 式离线画像）< +原始近期历史（RecICL 式）< +1~2 个澄清问题；但历史越长越会"稀释"（context dilution），画像的 token 性价比最高，澄清提问的边际收益最大。
- **H3（小模型可超 API）**：在真实选择 + 满意度上训练的 4B–8B 开源受托 agent，在一致率、后悔避免率、抗操纵性上超过 GPT-5 级 API（Mirroring Users 已在"模拟器"上验证 3B > GPT-5，我们在"受托人"上复现并扩展）。
- **H4（agent 与人的可操纵性不同）**：在 OPeRA 真人会话上对比，agent 对位置 / 赞助标签的敏感度与人类**方向相同但幅度不同**——这直接回应 *Whom Do AI Agents Work For?* 的发现，并把它扩展到真实购物数据与多品类。

### 2.3 研究问题
- **RQ1 Measure**：delegation gap 有多大？由哪些系统性因素构成？agent 与真人的偏差结构是否一致？
- **RQ2 Channel**：哪种偏好传递通道（指令 / 画像 / 历史 / 澄清）在单位成本下最有效？何时该问、问什么？
- **RQ3 Close**：能否用真实选择 + 满意度信号训练出更好、更鲁棒的受托 agent？

### 2.4 数据集与 DelegateBench 构建

| 来源 | 角色 | 规模 | 关键字段 | 备注 |
|---|---|---|---|---|
| **Amazon Reviews 2023**（McAuley Lab） | 主数据源 | 5.7 亿评论 / 4800 万商品 | user_id、parent_asin、rating、评论文本、timestamp、verified_purchase、商品 title/features/description/price/store | 构造用户历史 \(H_u\) 与后悔型 episode |
| **Amazon-C4**（BLaIR 作者） | 满意型 episode 种子 | 21,223 条 | 第一人称复杂需求 query、user_id、item_id、ori_rating(=5)、ori_review；不带逐条候选集，只附约 106 万件商品的公共池 | 风格参照与改写器校验集；满意型与后悔型统一从 Amazon Reviews 2023 用同一改写器构造（见 04 号文档 3.1 节） |
| **OPeRA**（ACL'26） | 真人对照 | 51 人 / 692 会话（会话按购买信号切分，含购买的会话数需下载后统计） | persona（Big Five、MBTI、购物风格）、页面观测、动作、加购/购买时的 rationale、最终购买 ASIN/价格/选项 | 候选集 = 用户实际浏览过的商品详情页；rationale 作 oracle 与解释 gold |
| **ShopSimulator**（ACL'26，阿里） | 中文迁移（可选） | 130 万淘宝商品 | persona 模式、多轮 | 若时间允许，验证结论跨语言/跨平台 |
| **UserMirrorer**（ACL'26） | 对照 / oracle | 3B checkpoint + 10K 数据 | 8 领域 | ① 作为"模拟器当受托人"的对照；② 作为回答澄清问题的 user oracle（条件于真实历史） |

**Episode 构造流程（Amazon 部分）**
1. **指令 \(q\)**：满意型（5 星）与后悔型（1–2 星）都从 ≥100 字、verified 的评论中由同一个 LLM 改写器生成**购前需求**（只保留"我想要什么"，剥离"结果如何"）；泄漏检查用关键词规则 + 两个 LLM judge，作者自查 50 条（见 04 号文档 3.1 节）。
2. **历史 \(H_u\)**：取该用户在 \(i^*\) 时间戳**之前**的评论（标题 + 评分 + 摘要），按时间排序；≥5 条为"有历史"分层，<5 条为冷启动分层。
3. **候选集 \(C\)**（\(K=10\)，附 \(K=20\) 变体）：同细分品类、经 embedding 检索 + LLM 硬约束核验**都满足 \(q\)** 的商品，刻意在价格档 / 均分 / 评论数 / 品牌上多样化，含 \(i^*\)。保证 \(u\) 对候选的评论不出现在卡片中。
4. **呈现格式**：统一的 product card（title / price / avg rating / #reviews / 3 条要点 / 2–3 条他人评论），可选 [Sponsored] 标签与营销化改写。
5. **干预变体（RQ1 探针）**：位置随机置换（≥3 次）、干扰项加 [Sponsored]、干扰项营销化改写、评论数 ×10、价格 ±20%、画像中插入身份线索（性别/年龄/种族中性 vs. 显式）。
6. **去泄漏与污染检查**：优先选 2023-06 之后、低热度商品；做"闭卷回忆 ASIN 评论"探针并报告污染率；候选 title 与 \(q\) 的 n-gram 重叠上限。
7. **规模**：Amazon 满意型 3,000 + 后悔型 1,500（自动泄漏过滤后）+ OPeRA ~200 会话；训练集另从 Amazon 训练切分中自动构造 ~30k episode。

### 2.5 评测指标

| 维度 | 指标 | 说明 |
|---|---|---|
| 一致性 | **Hit@1 / MRR**（满意型） | agent 选择 vs. 真实购买 |
| 利益服务 | **Regret-Avoidance Rate**（后悔型）、**Constraint Satisfaction Rate**（ETAPP 式 key-point LLM 评测） | 是否避开踩雷商品、是否满足 \(q\) 的硬约束 |
| 综合 | **Delegation Score** = 满意型一致 − 后悔型踩雷 | 单一数字便于排行 |
| 偏差 | Position Sensitivity、Sponsored Lift、Marketing Lift、Price Elasticity、Identity Shift | 干预前后选择分布变化（与 OPeRA 人类基线对比） |
| 通道效率 | gap 下降 / 每 1k token、gap 下降 / 每个澄清问题 | RQ2 |
| 鲁棒性 | 扰动下 Delegation Score 的下降幅度 | RQ3 |
| 可解释 | 与 OPeRA 人类 rationale 的 key-point 重合度 | 附加 |

### 2.6 方法（可能的技术）

**Stage 1 — 测量（RQ1, RQ2，10–11 月）**
- 受托 agent = 统一的 ReAct 式 prompt（读候选 → 可选提问 → 输出选择 + 理由），在 4 个通道条件下评测：
  - C0 指令-only；C1 +NL 画像（用 PersonaX 思路离线生成）；C2 +原始历史（最近 5/10/20 条，RecICL 式）；C3 +预算化澄清（\(k\in\{1,2,3\}\)，oracle = 基于真实历史与真实评论的 LLM / UserMirrorer）。
- 模型：GPT-5、Claude、Gemini、DeepSeek-V3.x；Qwen3-8B/32B、Llama-3.x；开/关 thinking。
- 非 agent 基线：Popularity、按均分、BLaIR embedding + \(q\) 重排、SASRec/UniSRec（仅历史）、"历史-only LLM"（无 \(q\)）。
- 对照：UserMirrorer-3B 直接当受托人。

**Stage 2 — 方法：Preference-Grounded Delegate（RQ3，12 月）**
- **SFT**：在自动构造的 ~30k 训练 episode 上，用强模型条件于真实选择 + 真实评论生成 EKB 式决策 rationale（Mirroring Users 的做法），不确定性过滤后训练 Qwen3-4B/8B（LoRA）。
- **满意度加权 DPO**：满意型 \(i^*\succ\) 硬负例；后悔型 **反转**：最优替代 \(\succ i^*\)；权重随 \(|r^*-3|\) 增大。
- **操纵不变性正则**：训练时对干扰项随机注入 [Sponsored] / 营销改写 / 位置置换，加入选择一致性损失（同一 episode 的扰动副本应选同一商品）。
- **预算化澄清**：先用候选 logprob 熵做阈值触发"提问 vs. 选择"（training-free）；若时间允许，用 GRPO 以 "gap 下降 − λ·问题数" 为 reward 训练提问策略（agent 背景的发挥点）。
- **算力**：8B LoRA SFT/DPO 在 5090 32GB 可跑（bf16 + grad-ckpt，seq 4k）；GRPO 阶段建议租 1×A100/H800 80G 约 100–200 小时。

**Stage 3 — 可选扩展（dual-audience，若进度快）**
- 平台侧：比较把候选呈现为 ranked list / 结构化属性表 / 对比摘要（Q-STRUM Debate 式）时受托 agent 的表现——回应 position paper 的 "machine-actionable representation" 议程。

### 2.7 预期结论（写进 abstract 的形态）
1. 前沿 LLM 受托人在 \(K=10\) 时与真实用户一致率约 30–50%，且在后悔型 episode 上仍有相当比例"陪用户踩雷"；模拟器（UserMirrorer）更是系统性复现踩雷 → delegate ≠ simulator。
2. 偏差可分解：均分/评论数先验 > 位置 > 赞助标签 > 营销文案；身份线索会显著改变推荐。agent 的位置/赞助敏感度与 OPeRA 真人**方向一致但幅度不同**。
3. 通道：NL 画像的 token 性价比最高；1–2 个澄清问题带来最大边际收益；长历史出现稀释。
4. 4B–8B 的 Preference-Grounded Delegate 在 Delegation Score 上超过 GPT-5，且在操纵扰动下的下降幅度显著更小。

### 2.8 与相关工作的区分（预演审稿意见）

| 可能的质疑 | 回答 |
|---|---|
| "这不就是用户模拟器评测？"（Agent4Rec、SimUSER、Mirroring Users、AlignUSER） | 目标不同：模拟器**复现**人（含错误），受托人**服务**人。我们用后悔型 episode 实证两者分歧，并给出面向受托的训练目标。 |
| "又一个购物 agent benchmark？"（EComAgentBench、Shopping Companion、ShopperBench、ShopSimulator） | 它们用**合成 persona / 脚本 rubric**打分；我们用**真实用户的真实选择与满意度**，并加入因果干预探针与通道性价比分析。 |
| "sponsorship bias / role coherence 已经研究过" | 它们是合成旅行场景的行为学探针，无真实 ground truth、单品类、无方法；我们多品类 + 真人数据 + 训练方法。 |
| "iAgent 已提出用户侧 agent" | iAgent 用指令重排平台推荐；我们问的是"这个 agent 到底是否代表用户"以及"如何训练它更代表用户"。 |
| 数据泄漏 / 污染 | 时间切分、低热度筛选、闭卷探针报告污染率、候选与 \(q\) 的重叠上限、作者自查子集；均分与评论数按目标时间戳之前重算。 |

### 2.9 算力与预算（上限 2 万元，预计 ≤ 1 万元）

| 项目 | 估算 | 说明 |
|---|---|---|
| API 评测 | ≈ 6 模型 × 4.5k episode × 4 通道 × ~3.5k token ≈ 4 亿 token 上限；实际用分层抽样（每通道 1k）→ ~1 亿 token | ≈ 2–3k 元（GPT-5/Claude 为主，DeepSeek 便宜） |
| 数据构造（LLM 改写 + rationale 生成） | ~35k 次调用 | ≈ 1k 元 |
| 本地训练 | Qwen3-4B/8B LoRA SFT + DPO | RTX 5090 自有，电费忽略 |
| 租卡（可选） | 1×A100/H800 80G × 150 h × ~10–15 元/h | ≈ 2–3k 元 |
| 质量检查 | 自动泄漏检查 + 两个 LLM judge 一致率；作者自查 50 条；不招募他人 | 0 元 |
| **合计** | | **≈ 6–8k 元** |

### 2.10 时间线（每天 3h，约 90h/月）

| 阶段 | 时间 | 里程碑 | 产出 |
|---|---|---|---|
| P0 补课 | 9/22–10/5 | 推荐基础 + 10 篇必读（见第 5 节） | 读书笔记；跑通 RecBole 的 SASRec baseline |
| P1 数据 | 10/6–10/31 | DelegateBench v0：Amazon 满意型 3k + 后悔型 1.5k + OPeRA 200；干预变体脚本 | 数据卡 + 统计表；污染率报告 |
| P2 测量 | 11/1–11/30 | 6 模型 × 4 通道 × 干预探针；非 agent 基线；UserMirrorer 对照 | RQ1/RQ2 主表 + 图；确定"故事" |
| P3 方法 | 12/1–12/31 | SFT → 满意度加权 DPO → 操纵不变性；预算化澄清；消融 | RQ3 主表；鲁棒性曲线 |
| P4 写作 | 1/1–ARR 截止 | 初稿 → 老师把关 → 修改；补 LLM judge 一致率报告（不做人工评测） | 8 页 long paper + 附录 + 代码/数据发布 |
| 缓冲 | 全程 | 若 P3 不及预期，退回 "benchmark + analysis" 定位（仍可投 Findings） | |

### 2.11 风险与应对

| 风险 | 概率 | 应对 |
|---|---|---|
| Amazon-C4 的 \(q\) 源自目标商品评论，可能"太好猜" | 中 | 候选全部满足 \(q\)；用 embedding 相似度上限筛掉 trivial 项；报告 retrieval-only 基线作为 sanity check |
| 后悔型 \(q\) 改写混入"结果信息" | 中 | 提示词只允许购前需求；关键词规则 + 两个 LLM judge 双重过滤，报告一致率与剔除率；作者自查 50 条 |
| OPeRA 规模小、购买会话有限 | 高 | 仅作真人对照与 rationale 分析，不做主表 |
| 训练增益不显著 | 中 | 退回 benchmark + analysis 定位；把 UserMirrorer 与 API 的对比做深 |
| API 成本超预算 | 低 | 分层抽样；主实验用 1 个 API 模型 + 开源模型，其余模型只跑子集 |
| 被同期工作抢先 | 中 | 11 月底前挂 arXiv 预印本占位（ARR 现行政策允许预印本，但需遵守其匿名与"不主动宣传"要求，投稿前再核对当期 CFP） |

---

## 3. 老师模板对应信息

**第一部分：学生基础信息**
- 姓名/昵称：charlie
- 学校/年级：PKU，在职
- 研究方向：**Agent × 推荐系统**（agent 作为推荐的受托消费者；LLM 用户模拟器）
- 计划发论文时间：ACL 2027（ARR 2027 年 1 月截止）
- 学习目标：发一篇 ACL long paper（主会或 Findings）
- 每日学习时间：3 小时以上
- 基础薄弱点：推荐系统是新领域（评测协议、经典 baseline、数据处理需补课）
- 希望得到的帮助：选题把关、实验设计与算力建议、论文写作指导与成稿把关
- 兴趣点：LLM agent；好切入、算力可控的方向均可
- GPU 与设备：RTX 5090（32GB）×1；租算力预算 2 万元以内

**第二部分：论文初稿进度**
- 项目进度：① 已完成 ACL 2026 推荐方向 20 篇论文阅读笔记 + 算力总览；② 已完成 ACL 2024/2025/2026 三届 agent × recsys 系统调研（本目录 01 文档）；③ 已形成主推 + 备选两个方向的 proposal（本文档）。
- 学习收获：三年趋势 = LLM-as-Rec → Agent 化 → RL/推理/环境；agent 在推荐中有三种角色（推荐侧 / 用户侧 / 模拟侧）；模拟器与受托人的目标差异是本 proposal 的核心洞察。
- 初稿进度：0%（计划 2027-01 完成初稿）。

---

## 4. 备选方向（Plan B）：Goodhart in Simulator-Trained Conversational Recommendation Agents

**一句话**：越来越多 CRS agent 用 LLM 用户模拟器当 RL reward（ECPO/AILO ACL'25、SMTPO 2026、GRSU、ShopSimulator RL、HARPO），但**没有人测量**被模拟器训练出的 agent 在"换模拟器 / 留出的公开真人对话"上掉多少、学到了哪些讨好模拟器的行为、如何鲁棒训练。

| 项目 | 内容 |
|---|---|
| RQ | (1) 训练模拟器得分与外部得分随训练步数的分叉曲线有多陡？(2) 利用行为分类：奉承、冗长、诱导式提问、复述目标属性（PEPPER 指出的 target-biased 漏洞）等；(3) 哪种防御最有效：模拟器集成/随机化、Turing 式判别锚（Turing-RL 思路迁移到推荐）、reward capping、target-free 模拟器、KL 约束 |
| 技术 | Qwen3-1.7B/4B LoRA + GRPO（TRL/verl），训练模拟器 \(S_{train}\in\{\)prompted GPT 类、UserMirrorer-3B、AILO 式\(\}\)，评测模拟器 \(S_{test}\neq S_{train}\) + 留出的公开真人对话（ReDial / INSPIRED / Reddit-Movie）；单人版本用 best-of-n + 迭代 DPO 代替 GRPO（见 04 号文档 3.2 节） |
| 数据 | ReDial、INSPIRED、Reddit-Movie（He et al. 2023）、LLM-REDIAL、PEARL；模拟器：UserMirrorer、AILO（若开源）、PEPPER 协议 |
| 算力 | 中：RL 需租 1×A100/H800 约 200–300 h（≈ 3–5k 元） |
| 优点 | 问题定义干净、结论对整个"模拟器训练 agent"社区有价值、agent 背景直接可用 |
| 风险 | RL 工程量大、结果噪声大；ReDial/INSPIRED 已被反复研究，绝对指标提升空间小 |
| 与主推的关系 | 可作为主推第二篇：受托 agent 训练若用模拟器当 reward，也会面临同样的 Goodhart 问题 |

---

## 5. 补课与必读清单（P0，两周）

**推荐系统基础（第 1 周）**
1. 评测协议与陷阱：Krichene & Rendle (KDD'20) *On Sampled Metrics for Item Recommendation*；leave-one-out、时间切分、负采样。
2. 序列推荐 baseline：SASRec (ICDM'18)、UniSRec (KDD'22)；用 [RecBole](https://recbole.io/) 跑通一个 Amazon 子集。
3. LLM4Rec 入门：TALLRec (RecSys'23)、LLMRank/Hou et al. (ECIR'24)、BinLLM (ACL'24, 已收录 #497)。

**Agent × RecSys 必读 10 篇（第 2 周，按顺序）**
| # | 论文 | 为什么读 |
|---|---|---|
| 1 | Survey on LLM-powered Agents for RS（EMNLP'25 Findings） | 建立三范式 × 四模块的地图 |
| 2 | RecMind（NAACL'24 Findings） | 第一个推荐 agent 长什么样 |
| 3 | iAgent（ACL'25 Findings） | user–agent–platform 范式，本题的直接前驱 |
| 4 | T-PRA（ACL'25） | agent-tuning with DPO 的工程范本，代码开源 |
| 5 | SimUSER（ACL'25 Industry）→ AlignUSER（ACL'26 #09） | 模拟器如何被验证"像人" |
| 6 | Mirroring Users（ACL'26 #07） | 3B 超 GPT-5 的数据蒸馏 + SFT/DPO 配方，直接复用 |
| 7 | OPeRA（ACL'26 #18） | 真人数据字段与 next-action 基准 |
| 8 | ShopSimulator（ACL'26 #17） | 购物 agent 的 SFT+RL 训练经验与失败分析 |
| 9 | Stereotype or Personalization?（ACL'25 Findings） | 身份线索干预实验的设计模板 |
| 10 | *Who Are We Recommending To?*（RecSys'26 position）+ *Whom Do AI Agents Work For?*（arXiv 2609.17989） | 本题的议程来源与最近实证 |

**工程准备**：Amazon Reviews 2023 下载与按品类抽样脚本；Amazon-C4 → episode 构造脚本；统一 product card 渲染；LLM 评测 harness（缓存、重试、成本统计）；TRL/PEFT 的 LoRA SFT/DPO 模板。
