# HARPO: 面向用户对齐对话式推荐的层次化智能体推理

**原标题**: HARPO: Hierarchical Agentic Reasoning for User-Aligned Conversational Recommendation

**作者**: Subham Raj, Aman Vaibhav Jha, Mayank Anand, Sriparna Saha

**单位**: IIT Patna; IIIT Allahabad

## 摘要

对话式推荐系统（CRSs）在用户逐步揭示偏好的条件下运行，需要在不确定性下做出推荐决策。尽管近期基于 LLM 的方法在代理指标（如 Recall@K 和 BLEU）上取得了强劲表现，但它们在实践中往往无法提供高质量、与用户对齐的推荐，因为它们优化的是检索准确性或流畅生成等中间目标，而非推荐质量本身。我们提出 HARPO（带偏好优化的层次化智能体推理），一个将对话式推荐重新定义为面向多维推荐质量优化的结构化决策过程的智能体框架。HARPO 整合了：(i) **层次化偏好学习**：将推荐质量分解为可解释的维度（相关性、多样性、满意度和参与度），并配以上下文依赖的权重；(ii) **审慎的树搜索推理**：由学习到的价值网络引导，在预测质量上评估候选路径；(iii) **领域无关的推理抽象**：通过虚拟工具操作和多智能体精炼实现。我们在 ReDial、INSPIRED 和 MUSE 上评估 HARPO，展示了在以推荐为中心的指标上相比强基线的持续改进，同时保持有竞争力的回复质量。
