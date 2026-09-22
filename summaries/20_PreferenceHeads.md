# Preference Heads in Large Language Models: A Mechanistic Framework for Interpretable Personalization

| 项目 | 内容 |
|------|------|
| **Paper** | Preference Heads in Large Language Models: A Mechanistic Framework for Interpretable Personalization |
| **Authors** | Weixu Zhang, Ye Yuan, Changjiang Han, Yuxing Tian, Zipeng Sun, Linfeng Du, Jikun Kang, Hong Kang, Xue Liu, Haolun Wu |
| **Affiliation** | McGill University; Mila – Quebec AI Institute; MBZUAI; University of Montreal; Salesforce |
| **Theme** | 可解释个性化 / 机制可解释性 / Training-free Steering |
| **Problem** | LLM 个性化被当作黑箱处理，现有方法依赖 prompt engineering 或 fine-tuning，不理解个性化在模型内部何处和如何发生 |
| **Method** | Differential Preference Steering (DPS)：training-free 框架。(1) 通过因果掩码分析识别稀疏的"Preference Heads"（与用户偏好因果相关的注意力头），使用 Preference Contribution Score (PCS) 量化因果影响；(2) 解码时对比有/无 Preference Heads 的模型预测，放大偏好对齐的延续信号 |
| **Benchmark** | LaMP 及其他个性化基准，多个 LLM |
| **Result** | 一致性地超越对比解码基线（CAD、DeCoRe）；training-free 且计算开销低；提供了个性化在 transformer 架构中何处涌现的机制解释 |
| **Question** | Preference Heads 是否跨模型通用？不同类型的偏好（风格 vs 主题）是否由不同的头负责？ |

## 详细笔记

### 研究背景与动机

LLM 展现出强大的隐式个性化能力，但现有方法将其视为黑箱——通过 prompt engineering 或 fine-tuning 实现个性化，却不理解个性化信号在模型内部的位置和机制。

来自 McGill/Mila 的 Zhang 等人假设存在一组稀疏的"Preference Heads"——编码用户风格和主题偏好并因果地影响生成的注意力头。

### 核心方法详解

**Preference Contribution Score (PCS)**：通过因果掩码实验，逐一遮蔽每个注意力头，比较遮蔽前后模型在用户参考回复上的 NLL 变化，直接度量每个头对个性化输出的因果贡献。

**Differential Preference Steering (DPS)**：解码公式为 l_t = (1+gamma) * l_t^pref - gamma * l_t^gen，其中 l_t^pref 是完整模型的 logits，l_t^gen 是遮蔽 Preference Heads 后的 logits。当 gamma=0 时退化为原始模型，gamma 增大时放大偏好方向。这是一种内部路径增强，而非外部目标引导。

### 实验设置与结果

- **数据集**：LaMP 及其他个性化基准
- **模型**：多个不同规模的 LLM
- **关键结果**：一致性超越 CAD、DeCoRe 等对比解码基线；完全 training-free；计算开销低（仅需双 pass 解码）

### 个人思考

DPS 是少有的从机制可解释性角度出发的个性化方法。Training-free 特性使其对算力受限场景极具吸引力。与其他个性化方法（RecPO、C-BPO）可叠加使用——先用 DPS 增强推理时的偏好信号，再用 RecPO/C-BPO 优化训练时的偏好对齐。Preference Heads 的发现本身也是对 LLM 内部机制的有趣洞察。
