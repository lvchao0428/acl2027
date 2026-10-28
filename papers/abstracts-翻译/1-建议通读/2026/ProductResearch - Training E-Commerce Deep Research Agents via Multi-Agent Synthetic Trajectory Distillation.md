# ProductResearch: Training E-Commerce Deep Research Agents via Multi-Agent Synthetic Trajectory Distillation
> 来源文件：ProductResearch - Training E-Commerce Deep Research Agents via Multi-Agent Synthetic Trajectory Distillation.pdf
> 发表年份：2026
> 单位：Anthology 未著录

## 英文原文摘要（Original Abstract）

Large Language Model (LLM)-based agents show promise for e-commerce conversational shopping, yet existing implementations lack the interaction depth and contextual breadth required for complex product research. Meanwhile, the Deep Research paradigm, despite advancing information synthesis in web search, suffers from domain gaps when transferred to e-commerce. We propose ProductResearch, a multi-agent framework that synthesizes highfidelity, long-horizon tool-use trajectories for training robust e-commerce shopping agents. The framework employs a User Agent to infer nuanced shopping intents from behavioral histories, and a Supervisor Agent that orchestrates iterative collaboration with a Research Agent to generate synthetic trajectories culminating in comprehensive, insightful product research reports. These trajectories are rigorously filtered and distilled through a reflective internalization process that consolidates multi-agent supervisory interactions into coherent singlerole training examples, enabling effective finetuning of LLM agents for complex shopping inquiries. Extensive experiments show that a compact MoE model fine-tuned on our synthetic data achieves substantial improvements over its base model in response comprehensiveness, research depth, and user-perceived utility, approaching the performance of frontier proprietary deep research systems and establishing multi-agent synthetic trajectory training as an effective and scalable paradigm for enhancing LLM-based shopping assistance.

## 中文翻译（Chinese Translation）

基于大语言模型（LLM）的智能体在电商对话购物中展现出前景，但现有实现缺乏复杂产品研究所需的交互深度与上下文广度。与此同时，Deep Research 范式尽管推进了网络搜索中的信息综合，但迁移到电商时存在领域鸿沟。我们提出 ProductResearch，这是一个多智能体框架，用于合成高保真、长时序的工具使用轨迹，以训练鲁棒的电商购物智能体。该框架采用一个 User Agent（用户智能体）从行为历史中推断细腻的购物意图；以及一个 Supervisor Agent（监督智能体），它协调与 Research Agent（研究智能体）的迭代协作，生成合成轨迹，最终产出全面、有洞见的产品研究报告。这些轨迹经过反思性内化（reflective internalization）过程被严格过滤与蒸馏，将多智能体监督交互整合为连贯的单角色训练样本，从而能对 LLM 智能体进行有效微调，以应对复杂购物查询。大量实验表明：在我们合成数据上微调的紧凑 MoE 模型，相比其基模型在回答全面性、研究深度和用户感知效用上均取得显著提升，性能逼近前沿商业 Deep Research 系统，并确立了"多智能体合成轨迹训练"作为增强基于 LLM 的购物助手的一种有效、可扩展范式。
