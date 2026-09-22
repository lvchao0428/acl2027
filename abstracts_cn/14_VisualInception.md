# Visual Inception: 通过多模态记忆投毒破坏智能体推荐器的长期规划

**原标题**: Visual Inception: Compromising Long-term Planning in Agentic Recommenders via Multimodal Memory Poisoning

**作者**: Jiachen Qian

**单位**: City University of Hong Kong

## 摘要

从静态排序模型到智能体推荐系统（Agentic RecSys）的演进赋予 AI 智能体维护长期用户画像和自主规划服务任务的能力。虽然这一范式转变增强了个性化，但也引入了一个脆弱性：对长期记忆（LTM）的依赖。在本文中，我们揭示了一种名为"**视觉植入（Visual Inception）**"的威胁。与寻求即时误分类的传统对抗攻击不同，Visual Inception 在用户上传的图像（如生活照片）中注入触发器，使其作为系统记忆中的"休眠特工"。当在未来的规划中被检索时，这些被投毒的记忆会劫持智能体的推理链，引导其朝向对手定义的目标（如推广高利润产品），而无需提示注入。为缓解这一威胁，我们提出 **CognitiveGuard**，一个受人类认知启发的双过程防御框架。它由 **System 1 感知净化器**（基于扩散的净化）清洁感知输入和 **System 2 推理验证器**（反事实一致性检查）检测记忆驱动规划中的异常组成。在模拟电商智能体环境中的大量实验表明，Visual Inception 达到约 85% 的目标命中率（GHR），而 CognitiveGuard 将此风险降低到约 10%，并提供可配置的延迟权衡（精简模式约 1.5 秒到完整顺序验证约 6.5 秒），在我们的设置下无质量下降。
