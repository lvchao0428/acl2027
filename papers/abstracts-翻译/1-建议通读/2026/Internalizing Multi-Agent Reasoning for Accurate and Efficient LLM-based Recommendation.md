# Internalizing Multi-Agent Reasoning for Accurate and Efficient LLM-based Recommendation
> 来源文件：Internalizing Multi-Agent Reasoning for Accurate and Efficient LLM-based Recommendation.pdf
> 发表年份：2026
> 单位：Tencent Technology (Beijing) Co., Ltd.；Tencent

## 英文原文摘要（Original Abstract）

Large Language Models (LLMs) are reshaping recommender systems by leveraging extensive world knowledge and semantic reasoning to interpret user intent. However, effectively integrating these capabilities with collaborative signals while avoiding prohibitive inference latency remains a critical bottleneck. To address this, we propose a trajectorydriven internalization framework to develop a Single-agent Trajectory-Aligned Recommender (STAR). Specifically, to internalize complex reasoning capabilities into a single efficient model, we first design a multi-agent teacher system capable of multi-turn tool usage and reflection. This teacher utilizes a Collaborative Signal Translation mechanism to explicitly convert latent behavioral patterns into descriptive natural language evidence to enhance reasoning accuracy. Subsequently, a trajectorydriven distillation pipeline transfers this agentic logic, including planning, tool usage, and self-reflection, into the compact STAR model. Extensive experiments demonstrate that STAR surpasses its teacher by 8.7% to 39.5% while eliminating iterative latency, paving the way for real-time, reasoning-enhanced recommendation.

## 中文翻译（Chinese Translation）

大语言模型（LLM）正借助其广博的世界知识和语义推理能力解读用户意图，从而重塑推荐系统。然而，如何将这些能力与协同信号有效整合，同时避免高昂的推理延迟，仍是一个关键瓶颈。为此，我们提出一个轨迹驱动的内化框架，用以开发单智能体轨迹对齐推荐器（Single-agent Trajectory-Aligned Recommender, STAR）。具体地，为把复杂推理能力内化到单个高效模型中，我们首先设计了一个能够进行多轮工具使用与反思的多智能体教师系统。该教师利用"协同信号翻译（Collaborative Signal Translation）"机制，将潜在的行为模式显式转换为描述性的自然语言证据，以增强推理准确率。随后，一条轨迹驱动的蒸馏流水线将这种智能体逻辑（包括规划、工具使用和自我反思）迁移到紧凑的 STAR 模型中。大量实验表明，STAR 相比其教师模型性能提升 8.7% 到 39.5%，同时消除了迭代式延迟，为实时、推理增强型推荐铺平了道路。
