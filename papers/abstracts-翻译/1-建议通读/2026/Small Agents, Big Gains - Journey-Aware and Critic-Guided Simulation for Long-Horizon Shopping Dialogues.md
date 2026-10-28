# Small Agents, Big Gains: Journey-Aware and Critic-Guided Simulation for Long-Horizon Shopping Dialogues
> 来源文件：Small Agents, Big Gains - Journey-Aware and Critic-Guided Simulation for Long-Horizon Shopping Dialogues.pdf
> 发表年份：2026
> 单位：Anthology 未著录

## 英文原文摘要（Original Abstract）
Modern e-commerce assistants must go beyond simple product search to support inspiration, comparison, and tool-grounded fact-checking across non-linear shopping journeys. However, distilling these complex behaviors into efficient, deployable models is bottle-necked by a lack of post-training data: trajectories must cover diverse agentic workflows with high fidelity, yet the desired outputs are open-ended without a single ground truth. We propose a closed-loop Multi-Agent Simulation Framework to synthesize diverse, faithful, and policy-aligned shopping trajectories. The system orchestrates a journey-aware, stateful user simulator to drive exploration, a shopping agent that manages both tools and UI elements, and a critic agent that provides rubric-driven feedback to iteratively refine the data. On a domain-specific benchmark, this synthetic data enables a small model to significantly outperform same-size baselines and surpass a large-model baseline, making it viable to deploy the smaller backbone at 8× higher inference throughput than the large baseline.

## 中文翻译（Chinese Translation）
现代电商助手必须超越简单的商品搜索，在非线性购物旅程中支持灵感激发、商品比较以及基于工具的事实核查。然而，将这些复杂行为蒸馏为高效、可部署的模型，其瓶颈在于后训练数据的匮乏：轨迹需要高保真地覆盖多样化的智能体工作流，而期望输出又是开放式的、不存在唯一标准答案。本文提出一种闭环多智能体仿真框架，用以合成多样化、高保真且与策略对齐的购物轨迹。该系统编排了一个旅程感知（journey-aware）、有状态的用户模拟器来驱动探索，一个同时管理工具与 UI 元素的购物智能体，以及一个评分驱动（rubric-driven）的批判智能体（critic agent）来提供反馈、迭代式地精炼数据。在领域专用基准上，这些合成数据使一个小模型显著超越同尺寸基线，并超过一个大模型基线；从而使得部署更小的骨干模型、以比大基线高 8 倍的推理吞吐进行服务成为可行。
