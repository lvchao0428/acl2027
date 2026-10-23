# Visual Inception: Compromising Long-term Planning in Agentic

> 来源文件：14_VisualInception.pdf
> 发表年份：2026
> 单位：Anthology 未著录

## 英文原文摘要（Original Abstract）

The evolution from static ranking models to Agentic Recommender Systems (Agentic RecSys) empowers AI agents to maintain long-term user profiles and autonomously plan service tasks. While this paradigm shift enhances personalization, it introduces a vulnerability: reliance on Long-term Memory (LTM). In this paper, we uncover a threat termed "Visual Inception." Unlike traditional adversarial attacks that seek immediate misclassification, Visual Inception injects triggers into user-uploaded images (e.g., lifestyle photos) that act as "sleeper agents" within the system's memory. When retrieved during future planning, these poisoned memories hijack the agent's reasoning chain, steering it toward adversary-defined goals (e.g., promoting high-margin products) without prompt injection. To mitigate this, we propose COGNITIVEGUARD, a dual-process defense framework inspired by human cognition. It consists of a System 1 Perceptual Sanitizer (diffusion-based purification) to cleanse sensory inputs and a System 2 Reasoning Verifier (counterfactual consistency checks) to detect anomalies in memory-driven planning. Extensive experiments on a mock e-commerce agent environment demonstrate that Visual Inception achieves about 85% Goal-Hit Rate (GHR), while COGNITIVEGUARD reduces this risk to around 10% with configurable latency trade-offs (about 1.5s in lite mode to about 6.5s for full sequential verification), without quality degradation under our setup. Latency reporting uses separate accounting: query-time overhead excludes one-time upload-time preprocessing.

## 中文翻译（Chinese Translation）

从静态排序模型到智能体推荐系统（Agentic Recommender Systems, Agentic RecSys）的演进，使 AI 智能体能够维护长期用户画像并自主规划服务任务。这一范式转变在增强个性化的同时，也引入了一个脆弱性：对长期记忆（Long-term Memory, LTM）的依赖。本文揭示了一种被称为"Visual Inception（视觉植入）"的威胁。与追求即时误分类的传统对抗攻击不同，Visual Inception 将触发器注入用户上传的图像（如生活照）中，使其在系统记忆中充当"休眠智能体"。当未来规划阶段检索到这些被污染的记忆时，它们会劫持智能体的推理链，将其导向攻击者预设的目标（例如推广高毛利商品），且无需提示注入（prompt injection）。为防御此威胁，我们提出 COGNITIVEGUARD，一个受人类认知启发的双过程防御框架。它由 System 1 感知净化器（基于扩散模型的净化）与 System 2 推理验证器（反事实一致性检查）组成，分别负责清洗感官输入与检测记忆驱动规划中的异常。在模拟电商智能体环境上的大量实验表明：Visual Inception 能达到约 85% 的目标命中率（Goal-Hit Rate, GHR），而 COGNITIVEGUARD 将该风险降至约 10%，并支持可配置的时延权衡（轻量模式约 1.5 秒，完整串行验证约 6.5 秒），且在我们的设定下不损失质量。时延报告采用独立记账：查询时开销不包含一次性的上传时预处理。
