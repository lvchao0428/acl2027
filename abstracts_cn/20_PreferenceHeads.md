# PreferenceHeads: 大语言模型中的偏好头——面向可解释个性化的机制性框架

**原标题**: Preference Heads in Large Language Models: A Mechanistic Framework for Interpretable Personalization

**作者**: Weixu Zhang, Ye Yuan, Changjiang Han 等

**单位**: McGill University; Mila; MBZUAI; Salesforce

## 摘要

大语言模型（LLMs）展现出强大的隐式个性化能力，但大多数现有方法将这种行为视为黑箱，依赖提示工程或在用户数据上微调。在本工作中，我们采用**机制可解释性**视角，假设存在一组稀疏的**"偏好头"（Preference Heads）**——编码用户特定的风格和主题偏好并对生成施加因果影响的注意力头。我们引入**差分偏好引导（Differential Preference Steering, DPS）**，一个无需训练的框架，(1) 通过因果掩码分析识别偏好头，(2) 在推理时利用它们实现可控且可解释的个性化。DPS 为每个注意力头计算**偏好贡献分数（PCS）**，直接度量其对用户对齐输出的因果影响。在解码过程中，我们对比有偏好头和无偏好头的模型预测，放大个性化与通用 logits 之间的差异，选择性地增强偏好对齐的延续信号。在多个 LLM 上广泛使用的个性化基准实验表明，该方法在个性化保真度上取得了持续提升，同时保持了内容连贯性和较低的计算开销。除了实证改进之外，DPS 还提供了关于个性化在 Transformer 架构中何处以及如何涌现的机制性解释。
