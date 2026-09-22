# Visual Inception: Compromising Long-term Planning in Agentic Recommenders via Multimodal Memory Poisoning

| 项目 | 内容 |
|------|------|
| **Paper** | Visual Inception: Compromising Long-term Planning in Agentic Recommenders via Multimodal Memory Poisoning |
| **Authors** | Jiachen Qian |
| **Affiliation** | City University of Hong Kong |
| **Theme** | Agentic 推荐安全 / 对抗攻击 / 多模态 Memory Poisoning |
| **Problem** | Agentic 推荐系统依赖 Long-term Memory (LTM)，引入新攻击面；Visual Inception 在用户上传图像中注入 trigger 作为 "sleeper agents"，在无需 prompt injection 的情况下劫持推理链 |
| **Method** | 攻击：Visual Inception — 向图像注入 adversarial trigger，作为 LTM 中的 sleeper agent；防御：CognitiveGuard 双过程框架 — System 1 Perceptual Sanitizer（上传时 diffusion-based 净化）+ System 2 Reasoning Verifier（查询时 counterfactual consistency 检查，Reasoning Divergence Score） |
| **Benchmark** | Mock e-commerce agent 环境 |
| **Result** | Visual Inception ~85% Goal-Hit Rate；CognitiveGuard 将风险降至 ~10%（延迟可配置：lite 1.5s / full 6.5s）；ASR-M 从 82.3% 降至 8.3% |
| **Question** | Diffusion purification 对正常图像质量的影响？Reasoning Divergence Score 的阈值如何自适应？攻击在真实 MLLM（如 GPT-4V）上的迁移性？ |

## 详细笔记

### 研究背景与动机

Agentic Recommender Systems 将 LLM/MLLM agent 与 Long-term Memory（LTM）结合，支持跨会话的个性化与长期规划（如记住用户偏好、历史决策、视觉上下文）。LTM 通常存储用户上传的多模态内容（图像、文档等），在后续 query 时被检索并参与推理。

这一架构引入新的安全漏洞：

- **Multimodal Memory Poisoning**：攻击者可在用户"正常"上传的图像中嵌入 **adversarial triggers**
- Triggers 作为 **sleeper agents** 写入 LTM，在特定 query 条件下被激活
- 与 prompt injection 不同：**无需修改用户 query**，仅通过污染 LTM 中的视觉记忆即可劫持 agent 的 reasoning chain
- 攻击可 compromise 长期规划（如 persistent 误导推荐、泄露隐私、执行非预期操作）

作者 Jiachen Qian 来自香港城市大学，提出 Visual Inception 攻击及 CognitiveGuard 防御框架。

### 核心方法详解

**Visual Inception 攻击**：

1. 构造 adversarial perturbation，嵌入用户上传图像
2. Perturbation 对人眼难以察觉，但在 MLLM 视觉编码器中激活特定 pattern
3. 被 poisoned 的图像存入 LTM；当后续 query 触发条件满足时，agent 推理被 hijack
4. 目标：达到高 Goal-Hit Rate（攻击目标达成率），如 ~85%

**CognitiveGuard 防御（双过程框架）**：

1. **System 1 — Perceptual Sanitizer（感知净化器）**：
   - 在 **upload 时** 运行
   - 使用 diffusion-based purification 去除 adversarial perturbation
   - 类似"视觉消毒"，在记忆写入前拦截 poison

2. **System 2 — Reasoning Verifier（推理验证器）**：
   - 在 **query 时** 运行
   - 进行 counterfactual consistency checks：若推理依赖的记忆内容被替换/移除，结论是否剧烈变化
   - 使用 **Reasoning Divergence Score** 量化不一致程度，高分数触发 alert 或拒绝
   - 延迟可配置：lite 模式 ~1.5s，full 模式 ~6.5s

### 实验设置与结果

- **环境**：Mock e-commerce agent（模拟真实 agentic 推荐场景）
- **攻击指标**：Goal-Hit Rate (GHR)、Attack Success Rate under Memory (ASR-M)
- **防御指标**：攻击成功率降幅、额外延迟
- **关键结果**：
  - Visual Inception：~85% Goal-Hit Rate（无防御时）
  - CognitiveGuard：风险降至 ~10%
  - ASR-M：从 82.3% 降至 8.3%
  - 延迟：lite 1.5s，full 6.5s

### 个人思考

Visual Inception 揭示了 agentic RS 中 LTM 的 "supply chain" 风险——用户上传内容成为 trusted input，却可携带 sleeper agents，比传统 prompt injection 更隐蔽。CognitiveGuard 的 System 1+2 设计借鉴 Kahneman 双过程理论，upload-time 净化 + query-time 验证形成纵深防御。与 SiPeR（13）对比：后者用视觉增强推荐能力，本文揭示视觉 LTM 的安全代价。工业部署需权衡：1.5s lite 模式是否可接受取决于场景（高价值交易 vs 浏览推荐）。
