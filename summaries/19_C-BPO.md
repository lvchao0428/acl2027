# Personalizing LLMs with Binary Feedback: A Preference-Calibrated Optimization Framework

| 项目 | 内容 |
|------|------|
| **Paper** | Personalizing LLMs with Binary Feedback: A Preference-Calibrated Optimization Framework |
| **Authors** | Xilai Ma, Liye Zhao, Weijun Yao, Haibing Di, Wenya Wang, Jing Li |
| **Affiliation** | Harbin Institute of Technology (Shenzhen)（哈工大深圳）; Huawei Technologies; Nanyang Technological University (NTU) |
| **Theme** | LLM 个性化 / 偏好优化 / Positive-Unlabeled Learning |
| **Problem** | 现有 LLM 个性化方法关注孤立的用户历史，忽略用户间差异的重要性；当使用其他用户数据作为负样本时，共享的任务知识被错误惩罚（偏好重叠问题） |
| **Method** | C-BPO 框架：将目标用户数据作为正反馈，其他用户数据作为隐式负信号。使用 Positive-Unlabeled (PU) Learning 推导偏好校准目标函数，通过减去"正向偏差"来净化负信号。无需显式的 pairwise 对比数据 |
| **Benchmark** | 5 个个性化文本生成任务，多个骨干 LLM |
| **Result** | 一致性地超越 SFT 和标准 BPO 基线；有效捕捉用户间差异而不损害通用能力 |
| **Question** | PU Learning 中正样本比例的先验估计对性能有多敏感？在用户偏好高度重叠的场景中效果如何？ |

## 详细笔记

### 研究背景与动机

LLM 个性化旨在使模型行为与个体用户偏好对齐。现有方法通常仅关注单个用户的历史数据，忽略了用户间差异的作用。一种自然的思路是将其他用户的数据作为负样本来凸显个体差异，但这面临"偏好重叠"问题——不同用户可能共享某些通用任务知识（如语法规则、格式偏好），这些共享知识不应被惩罚。

### 核心方法详解

**C-BPO（Calibrated Binary Preference Optimization）**：
- 将目标用户数据视为正反馈
- 将其他用户数据作为隐式负信号的辅助集
- 使用 PU Learning 理论推导校准目标函数
- 通过减去"正向偏差"（positive bias）净化负信号中的共享知识部分
- 确保仅对齐用户独特的个性特征，而不损害通用能力

### 实验设置与结果

- **数据集**：5 个个性化文本生成任务
- **骨干模型**：多个 LLM
- **关键结果**：一致性地超越 SFT 和标准 BPO 基线

### 个人思考

C-BPO 的核心洞察是"个性化 = 差异化"，通过对比用户间的差异来定义个性。PU Learning 的引入优雅地解决了负样本中混入正信号的问题。与 RecPO 的区别：RecPO 关注偏好的强度和时间维度，C-BPO 关注用户间的差异维度，两者可以结合使用。
