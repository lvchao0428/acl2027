# ACL 2024 / 2025 / 2026 · Agent × RecSys 系统调研

> 调研日期：2026-09-22 | 目标：为 ACL 2027（京都，2027-08-17~22；ARR 投稿截止 **2027 年 1 月**，具体日期 TBA）选题
> 方法：抓取 ACL Anthology 三届 main / findings / short / industry 全量论文列表（2024: 865+976+77 篇；2025: 1603+1388+98+110 篇），按 recommend / user simulat / shopping / e-commerce / personaliz 等关键词过滤后逐篇读摘要；ACL 2026 以官方 accepted list + 本仓库已有 20 篇笔记为基础补充。
> 相关信息来源：[ACL Anthology](https://aclanthology.org/)、[ACL 2026 Accepted Papers](https://2026.aclweb.org/program/accepted_papers/)、[ACL 2027 官网](https://2027.aclweb.org/)、[ARR Dates](http://aclrollingreview.org/dates)

---

## 0. 一图看懂三年演进

| 年份 | 阶段关键词 | 代表工作 | Agent 的角色 |
|---|---|---|---|
| **ACL 2024** | **LLM-as-Recommender 打地基** | BinLLM、RecLM-gen(MSRA)、RDRec、Scrutable NL Profile、PEARL / LLM-REDIAL、Stealthy Attack、Generative Explore-Exploit | 几乎没有"agent"；RecMind（NAACL'24 Findings）是 ACL 系首个推荐 agent，Yoon et al.（NAACL'24）首个 LLM 用户模拟器评测协议 |
| **ACL 2025** | **Agent 化 + 用户模拟器可训练** | T-PRA（Actor-Advisor-Critic + DPO）、iAgent（用户侧 agent）、PersonaX、ECPO/AILO、USP、SimUSER、ETAPP、RecICL、MUSE、WoS、EcomScriptBench | agent 出现在推荐侧（T-PRA）、用户侧（iAgent）、模拟侧（SimUSER/AILO/USP）；开始用 DPO/RL 调 agent |
| **ACL 2026** | **RL + 推理 + 环境/数据** | OneRec-Think、ReRec、HARPO、ROS、MemRec、Mirroring Users、AlignUSER、ShopSimulator、OPeRA、Visual Inception、PreferenceHeads | GRPO 训练推理型推荐器；agentic memory；模拟器用 DPO / world model 对齐真人；购物 agent 有了训练环境（ShopSimulator）和真人数据（OPeRA）；agentic 安全 |
| **→ ACL 2027 预测** | **agent 成为推荐的"消费者"；模拟器成为 reward** | 见第 4 节 gap 分析 | 推荐系统要同时服务人和替人决策的 agent；训练依赖模拟器带来 Goodhart 风险 |

---

## 1. ACL 2024（曼谷）

### 1.1 推荐侧：LLM 作为推荐器（recommender-oriented）

| Anthology ID | 论文 | 单位 | 核心贡献 | 与 agent 的关系 |
|---|---|---|---|---|
| 2024.acl-long.497 | **BinLLM**: Text-like Encoding of Collaborative Information in LLMs for Rec | USTC | 把外部 CF embedding 编成二进制文本串喂给 LLM | 协同信号注入的经典解法，后续 Laser/AGRec 都在此延伸 |
| 2024.acl-long.443 | Aligning LLMs for **Controllable Recommendations** (RecLM-gen) | 深大 + MSRA | 推荐指令遵循的监督任务集 + RL 对齐，减少格式错误 | 让 LLM 能听懂"推荐指令"是 agent 化的前提 |
| 2024.acl-short.6 | **RDRec**: Rationale Distillation | — | 大模型从评论中蒸馏"为什么喜欢"的 rationale 给小模型 | 后来 Mirroring Users 的 rationale 思路雏形 |
| 2024.acl-short.29 | RecGPT: Generative Pre-training for Text-based Rec | — | 文本推荐的生成式预训练 | — |
| 2024.acl-long.753 | **Transparent and Scrutable Recs** using NL User Profiles | — | 用 LLM 从评论生成自然语言用户画像，仅凭画像做推荐，用户可编辑画像 | 可编辑记忆 / scrutable agent 的源头 |
| 2024.acl-long.295 | **Generative Explore-Exploit** (Amazon) | Amazon | training-free：LLM optimizer 接用户 CTR 反馈闭环，生成式探索-利用 | 最早的"LLM 优化器 + 反馈回路"，agentic 思想 |
| 2024.findings-acl.780 | Leveraging LLM Reasoning Enhances Personalized RS | — | 推理（CoT）提升个性化推荐 | ACL 2026 "推理推荐"的先声 |
| 2024.acl-long.399 | LaMP: When LLMs Meet Personalization | UMass | 个性化 LLM benchmark（7 任务） | 个性化评测基础设施 |

### 1.2 交互侧：对话式推荐 & 数据

| Anthology ID | 论文 | 核心贡献 |
|---|---|---|
| 2024.acl-long.138 | HyCoRec（超图多偏好，缓解 CRS 马太效应） | 传统 CRS 结构改进 |
| 2024.findings-acl.65 | **PEARL**：persona + knowledge 增强的 LLM 模拟器合成 57k 对话 | 用 LLM 模拟器造 CRS 数据 |
| 2024.findings-acl.529 | **LLM-REDIAL**：47.6k 多领域对话，由真实行为日志 + 模板驱动 LLM 生成 | 同上，行为一致性更好 |
| 2024.acl-long.424 | PlatoLM / Socratic：以真人问题为目标训练用户模拟器（通用对话） | 用户模拟器训练范式 |

### 1.3 安全

| Anthology ID | 论文 | 核心贡献 |
|---|---|---|
| 2024.acl-long.318 | **Stealthy Attack** on LLM-based Rec | 仅改物品文本即可提升曝光，隐蔽且不伤整体指标 |

### 1.4 ACL 系同年（NAACL 2024）必须知道的两篇
- **RecMind** (2024.findings-naacl.271, Amazon)：首个 LLM 推荐 agent（planning + memory + tools + Self-Inspiring），zero-shot 逼近全训练 P5。
- **Yoon et al.** (2024.naacl-long.83, UCSD)：LLM 作为 CRS 生成式用户模拟器的 5 任务评测协议，指出偏离真人行为的模式。

---

## 2. ACL 2025（维也纳）

### 2.1 推荐侧 agent 与 LLM 推荐器

| Anthology ID | 论文 | 单位 | 核心贡献 | 备注 |
|---|---|---|---|---|
| **2025.acl-long.944** | **T-PRA: Tunable LLM-based Proactive Recommendation Agent** | USTC (高崇铭/王翔) | Actor-Advisor-Critic 三 agent；Critic 给 advantage → 构造偏好对 → **DPO 调 Actor/Advisor**，优化长期 reward、打破 echo chamber | ACL 2025 主会最"正统"的推荐 agent；代码开源 |
| 2025.acl-long.751 | RecLM: Recommendation Instruction Tuning | — | 模型无关的指令微调 + RL reward 自增强 | |
| 2025.acl-long.949 | Laser: Bi-Tuning w/ Collaborative Info | — | 前后缀虚拟 token + MoE Q-Former 注入 CF 信号 | |
| 2025.findings-acl.369 | AGRec | — | GNN logits 增强 LLM 解码 + rankable FSM | |
| 2025.findings-acl.651 | CoVE | — | 物品 ID 扩展词表 + 压缩 embedding | |
| 2025.findings-acl.735 | **RecICL** | — | 用最近交互做 ICL demo，**不更新参数**适应兴趣漂移 | 兴趣漂移 training-free 方案 |
| 2025.findings-acl.917 | C2KD | — | LLM→1B SLM 的推荐蒸馏（端侧） | 低算力路线参考 |
| 2025.acl-long.1317 | K-RagRec | PolyU | KG 结构化 RAG 增强 LLM 推荐 | |
| 2025.acl-long.1283 | OptiRAG-Rec | — | RAG + 多头 early-exit 做 CTR | |
| 2025.acl-long.1596 | GRAM | — | 生成式推荐 + 多粒度 late fusion | |
| **2025.findings-acl.300** | **PersonaX: Recommendation Agent-Oriented User Modeling** | — | 长行为序列聚类→选核心子序列→**离线多 persona 画像缓存**，提升 AgentCF 3–11%、Agent4Rec 10–50% | agent 的 profile 模块 |
| **2025.findings-acl.928** | **iAgent: LLM Agent as a Shield between User and RS** | — | 提出 **user–agent–platform** 范式；InstructRec 四数据集；i²Agent 带动态记忆，+16.6%，缓解 echo chamber 和非活跃用户偏差 | **用户侧 agent** 的起点，与本 proposal 直接相关 |

### 2.2 交互侧：对话推荐 agent 与偏好优化

| Anthology ID | 论文 | 核心贡献 |
|---|---|---|
| **2025.findings-acl.307** | **ECPO**: Expectation Confirmation Preference Optimization for Multi-Turn CRA + **AILO 用户模拟器** | 用期望确认理论建模多轮满意度演化，turn-level 偏好优化；模拟器给反馈 |
| 2025.acl-long.758 | Beyond Single Labels：LLM 语义检索扩充 CRS 假负例，**用用户模拟器评测** | |
| 2025.findings-acl.292 / 1317 | HyperCRS（filter bubble）/ HyFairCRS（多兴趣公平） | 传统 CRS 结构改进 |
| 2025.findings-acl.1170 | Q-STRUM Debate：辩论式 prompt 生成对比摘要帮用户理解推荐 | 多 agent 辩论 |

### 2.3 模拟侧：用户模拟器成为可训练对象

| Anthology ID | 论文 | 核心贡献 |
|---|---|---|
| **2025.acl-long.1025** | **USP**：从人机交互推断隐式画像，条件 SFT + 循环一致性 RL，画像采样器保证多样性 | 通用对话，方法可迁移到推荐 |
| **2025.acl-industry.5** | **SimUSER** (Woven by Toyota)：persona/memory/perception/brain 模块；缩略图、曝光效应、评论影响实验；**离线 A/B → 真实线上提升** | ACL 2026 AlignUSER 的前作 |
| 2025.acl-long.1064 | **ETAPP**：个性化工具调用 benchmark（800 例，沙箱，key-point LLM 评测） | agent 个性化评测 |
| 2025.findings-acl.1063 / 1107 | ToolSpectrum / PEToolLLM：个性化工具使用 | 同上 |
| 2025.findings-acl.927 | PersonaLens：对话助手个性化评测 | |

### 2.4 数据与 benchmark（电商方向）

| Anthology ID | 论文 | 核心贡献 |
|---|---|---|
| 2025.acl-long.641 | **Wizard of Shopping (TRACER)**：决策树规划驱动 LLM 生成 3.6k 目标导向购物对话 | 对话式商品搜索 |
| 2025.acl-long.1 | **EcomScriptBench**：60 万脚本 × 240 万商品，"按步骤规划 + 每步推荐商品" | 电商 agent 规划 |
| 2025.findings-acl.58 | **MUSE**：多模态 CRS 数据集（7k 对话，服装），**多 agent 框架合成、场景驱动 persona** | |
| 2025.acl-long.152 | MAPS：咨询对话中的动机 → 个性化搜索 | |

### 2.5 公平 / 偏差 / 工业

| Anthology ID | 论文 | 核心贡献 |
|---|---|---|
| **2025.findings-acl.1254** | **Stereotype or Personalization?** 用户身份（显式/隐式）显著改变 LLM 推荐，且模型不透明 | LLM 推荐的身份偏差 |
| 2025.findings-acl.778 | 姓名年龄感知影响 LLM 职位推荐 | |
| **2025.acl-industry.70** | **User Feedback Alignment for LLM-powered Exploration** (Google/YouTube)：novelty LLM + user-aligned LLM 的 best-of-n **推理时扩展**，线上提升满意度与多样性 | 工业 inference scaling |
| 2025.acl-industry.65 | MotiR（淘宝）：LLM 生成购买动机增强长尾双塔检索，线上 CTR/CVR +4% | |

### 2.6 ACL 系同年（EMNLP 2025）必读
- **A Survey on LLM-powered Agents for RS** (2025.findings-emnlp.620)：三范式（recommender / interaction / simulation-oriented）× 四模块（profile / memory / planning / action），并指出 **memory bloat、无遗忘机制、评测缺标准、数据泄漏** 等 open problem。
- **CRAVE** (2025.findings-emnlp.119, Netflix)：CRS agent 的协同"言语化经验库" + debater-critic。
- **PEPPER** (2025.findings-emnlp.1067)：指出 target-biased 用户模拟器把 CRS 评测变成"猜谜游戏"，提出 target-free 模拟器与 preference-coverage 指标。

---

## 3. ACL 2026（本仓库已有 20 篇笔记，此处只做 agent 视角的重组 + 补漏）

### 3.1 按 agent 三范式重组

| 范式 | 论文（编号见 README） | agent 视角要点 |
|---|---|---|
| **Recommender-oriented（推荐器本身 agent 化 / 推理化）** | 01 OneRec-Think（快手，GRPO + multi-validity reward）、03 ReRec（RFT + reasoning-aware advantage）、06 ROS（4B GRPO 空间推理）、04 HARPO（value-network 树搜索 + 多 agent）、05 **MemRec**（LM_Mem 管协同记忆图 + LLM_Rec 推理，稀疏用户 +91%）、12 MHL、11 PtE、10 PURPLE、16 ClusterRAG、20 PreferenceHeads | 2026 主流 = **RL(GRPO) + 显式推理**；记忆从"孤岛"走向"协同" |
| **Interaction-oriented（对话 / 购物 agent）** | 04 HARPO、13 SiPeR（多模态情境 CRS）、17 **ShopSimulator**（阿里，130 万淘宝商品，4 场景，**可训练环境**，GPT-5 全成功率 <40%，SFT+RL 有效） | 购物 agent 有了 RL 环境；多轮 + 个性化最难（≈35%） |
| **Simulation-oriented（用户模拟器）** | 07 **Mirroring Users**（EKB rationale + 不确定性蒸馏 10K 样本 → 3B SFT+DPO 超 GPT-5；**模型/数据开源**）、09 **AlignUSER**（world model + 反事实轨迹；与真实 A/B Spearman 0.71）、18 **OPeRA**（51 真人 692 会话，persona+rationale+action，含最终购买 ASIN） | 模拟器不再靠 prompt，而是靠**真实反馈对齐**；有了真人 ground truth |
| **安全 / 评测** | 14 Visual Inception（多模态记忆投毒 ~85% GHR）、02 BLaIR、08 RecPO、19 C-BPO、15 NovelQR | agentic 记忆是新攻击面 |

### 3.2 官方 accepted list 中与本方向相邻、README 未收录的论文（建议补读）
- *A Functionality-Grounded Benchmark for Evaluating Web Agents in E-commerce Domains*
- *Benchmarking Web Agent Safety under E-commerce Deceptive Interfaces*
- *PersonalAlign: Hierarchical Implicit Intent Alignment for Personalized GUI Agent with Long-Term User-Centric Records*
- *RISK: A Framework for GUI Agents in E-commerce Risk Management*
- *Thinking Alignment of Scenario-Oriented User Simulation*
- *When Personalization Legitimizes Risks: Uncovering Safety Vulnerabilities in Personalized Dialogue Agents*
- *The Personalization Trap: How User Memory Alters Emotional Reasoning in LLMs*

> 观察：ACL 2026 的"电商 agent"已从"推荐器"扩展到 **web/GUI agent 替用户操作电商界面**，且开始关心 deceptive interface 和风险 —— 这正是"agent 替人做决策"叙事的前奏。

---

## 4. Gap 分析：哪些方向已经拥挤、哪些还开放（2026-09 时点）

### 4.1 已拥挤 / 不建议作为主线
| 方向 | 拥挤证据 | 对本人的额外风险 |
|---|---|---|
| 推理 + RL 训练推荐器（in-text reasoning） | OneRec-Think / ReRec / ROS / HARPO（ACL'26）+ arXiv 上 R2Rec、Reason-to-Recommend 等 | 算力高（集群级），工业数据优势明显 |
| agentic 记忆 + 兴趣漂移 / 遗忘 | MemRec（ACL'26）之后，**2026 年 7–9 月 arXiv 连出 AtomRec、MEMOIR、LION、CALMRec、EvoRec** | 半年内已被 5+ 篇覆盖，难做出增量 |
| 通用购物 agent benchmark | ShopSimulator、OPeRA（ACL'26）、ShopperBench（EACL'26 industry）、EComAgentBench（2026-06）、Shopping Companion Bench（2026-03） | "又一个 benchmark"审稿疲劳；且这些均用**合成 persona / 脚本化 rubric** 打分 |
| 物品文本对抗 / 投毒攻击 | Stealthy Attack（ACL'24）、CheatAgent（KDD'24）、Visual Inception（ACL'26）、GEO 系列 | 已有清晰攻防范式 |

### 4.2 仍然开放的两个缺口（本 proposal 的候选）

**Gap A：agent 作为推荐的"消费者 / 受托人"（delegation）——只有 position paper 与两篇偏差研究，无系统实证与方法**
- Spotify 团队 position paper *Who Are We Recommending To? Recommender Systems in the Agentic Web*（RecSys'26, arXiv 2609.11945, 2026-09）提出 **delegation spectrum**、**dual-audience optimization**、**agent preference modeling**、**evaluation beyond engagement（regret、constraint satisfaction）**、**manipulation** 六项议程，但**没有任何实验**。
- 仅有的实证：*Whom Do AI Agents Work For?*（arXiv 2609.17989, 2026-09-16）——system prompt 中把 principal 设为平台会削弱 agent 对 sponsored 的惩罚；*When Agents Shop for You: Role Coherence*（arXiv 2604.26220）——buyer agent 会泄漏用户支付意愿。两篇都是**旅行/合成场景的行为学实验**，不涉及真实用户的选择 ground truth，也不给出训练方法。
- ACL 谱系支撑：iAgent（ACL'25，用户侧 agent 范式）→ OPeRA / ShopSimulator / AlignUSER / Mirroring Users（ACL'26，真人数据与对齐模拟器）→ **ACL'27：衡量并缩小"agent 替我选"与"我自己选/我满意"之间的差距**。

**Gap B：用户模拟器作为 RL reward 的可靠性（Goodhart / reward hacking）——被反复提及但无人系统研究**
- 2025–2026 大量 CRS agent 训练依赖 LLM 模拟器反馈：ECPO/AILO（ACL'25）、SMTPO（2026-04, 对 ReDial/INSPIRED 用 GRPO）、GRSU（2025）、ShopSimulator RL、HARPO。
- 已知隐患：*How Reliable is Your Simulator?*（2024，iEvaLM 数据泄漏与 history 依赖）、PEPPER（EMNLP'25，target-biased 模拟器 = 猜谜）、Turing-RL（2026-06，在聊天域用 Turing reward 并**截断 judge reward 以抑制 reward hacking**——但不是推荐域）。
- **无人测量**：被模拟器训练出的推荐 agent，在换一个模拟器 / 真人数据 / 人工评估上掉多少？学到了哪些"讨好模拟器"的行为？如何设计鲁棒训练？

> 两个 gap 的共同点：都利用了 ACL'26 刚开源的资源（OPeRA 真人数据、UserMirrorer 3B 对齐模拟器、ShopSimulator 环境），且都是 **"agent 视角切入推荐"** 而非"推荐算法本身"——适合 agent 背景、推荐新手。

---

## 5. 可直接复用的开源资源清单

| 资源 | 内容 | 用途 |
|---|---|---|
| [Amazon Reviews 2023](https://amazon-reviews-2023.github.io/)（McAuley Lab） | 5.7 亿评论 / 4800 万商品，含 rating、评论文本、时间戳、verified_purchase、商品 title/features/description/price | 构造真实用户的选择 + 满意度 ground truth |
| [Amazon-C4](https://huggingface.co/datasets/McAuley-Lab/Amazon-C4) | 21,223 条由 5 星长评论改写的第一人称复杂需求 query，附 user_id、item_id、ori_review，每条 50 个同域候选 | 现成的"委托指令 + 真实用户 + 真实购买"三元组 |
| [OPeRA](https://huggingface.co/datasets/NEU-HAI/OPeRA)（ACL'26） | 51 真人 692 会话，persona（Big Five/MBTI/购物习惯）、页面观测、动作、rationale、最终购买 ASIN/价格/选项 | 高保真"真人 vs agent"对照；rationale 可当 oracle |
| [ShopSimulator](https://github.com/ShopAgent-Team/ShopSimulator)（ACL'26，阿里） | 130 万淘宝商品、Shopper–Agent–Env 三方交互、persona 模式、可训练 | 中文 / 多轮场景迁移验证 |
| [UserMirrorer](https://github.com/Joinn99/UserMirrorer)（ACL'26） | 8 领域 10K 蒸馏样本 + Qwen2.5-3B / Llama-3.2-3B SFT+DPO 模拟器 checkpoint | 作为 user oracle / 对照的 delegate / RL 环境 |
| T-PRA 代码 [gnaWeinrE/T-PRA](https://github.com/gnaWeinrE/T-PRA)（ACL'25） | LLM Actor-Critic agent + DPO agent-tuning | agent-tuning 的工程参考 |
| ETAPP [hypasd-art/ETAPP](https://github.com/hypasd-art/ETAPP)（ACL'25） | 个性化工具调用沙箱 + key-point 评测 | LLM-as-judge 去偏评测方法参考 |
| WebShop / EComAgentBench / Shopping Companion Bench | 现成购物 agent 环境与 benchmark | 对照实验、迁移验证 |
