# Preference Heads in Large Language Models: A Mechanistic Framework

> 来源文件：20_PreferenceHeads.pdf

## 英文原文摘要（Original Abstract）

Large Language Models (LLMs) exhibit strong implicit personalization ability, yet most existing approaches treat this behavior as a black box, relying on prompt engineering or fine-tuning on user data. In this work, we adopt a mechanistic interpretability perspective and hypothesize the existence of a sparse set of Preference Heads, attention heads that encode user specific stylistic and topical preferences and exert a causal influence on generation. We introduce Differential Preference Steering (DPS), a training free framework that (1) identifies Preference Heads through causal masking analysis and (2) leverages them for controllable and interpretable personalization at inference time. DPS computes a Preference Contribution Score (PCS) for each attention head, directly measuring its causal impact on user aligned outputs. During decoding, we contrast model predictions with and without Preference Heads, amplifying the difference between personalized and generic logits to selectively strengthen preference aligned continuations. Experiments on widely used personalization benchmarks across multiple LLMs demonstrate consistent gains in personalization fidelity while preserving content coherence and low computational overhead. Beyond empirical improvements, DPS provides a mechanistic explanation of where and how personalization emerges within transformer architectures. Our implementation is fully open-sourced.

## 中文翻译（Chinese Translation）

大语言模型（LLM）展现出强大的隐式个性化能力，但现有方法大多将其视为黑盒，依赖提示工程或在用户数据上微调。本工作采用机制可解释性（mechanistic interpretability）视角，假设存在一组稀疏的"偏好头"（Preference Heads）——即编码用户特定风格与话题偏好、并对生成施加因果影响的注意力头。我们提出 Differential Preference Steering（DPS），一个无需训练（training-free）的框架：（1）通过因果掩码分析识别 Preference Heads；（2）在推理时利用它们实现可控、可解释的个性化。DPS 为每个注意力头计算"偏好贡献分数"（Preference Contribution Score, PCS），直接衡量其对用户对齐输出的因果影响。在解码过程中，我们对比有/无 Preference Heads 时的模型预测，放大个性化 logit 与通用 logit 之间的差异，从而选择性地强化偏好对齐的续写。在多种 LLM 的常用个性化基准上的实验表明，DPS 在保持内容连贯性与低计算开销的同时，一致提升了个性化保真度。除经验性提升外，DPS 还为"个性化在 Transformer 架构中何处、以何种方式涌现"提供了机制层面的解释。我们的实现已完全开源。
