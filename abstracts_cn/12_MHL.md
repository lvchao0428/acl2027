# MHL: 从过去到路径——生成式推荐中面向下一物品预测的掩码历史学习

**原标题**: From Past To Path: Masked History Learning for Next-Item Prediction in Generative Recommendation

**作者**: Kaiwen Wei, Kejun He, Xiaomian Kang 等

**单位**: Chongqing University; Institute of Automation, CAS; City University of Hong Kong

## 摘要

生成式推荐通过直接生成物品标识符，已成为推荐系统中一种有前景的范式。然而，这种从左到右的范式固有地使模型偏向局部上下文，无法捕获理解复杂用户意图所需的更深层历史依赖。为解决这一局限，我们提出**掩码历史学习（MHL）**，一个将目标从简单的下一步预测转向对历史深度理解的新型训练框架。MHL 在标准自回归目标之上增加一个辅助任务——重建被掩码的历史物品，迫使模型理解物品路径"为什么"从用户过去行为中形成，而不仅仅是"什么"物品是下一个。我们引入两个关键贡献来增强该框架：(1) **熵引导的掩码策略**，智能地选择信息量最大的历史物品进行重建；(2) **课程学习调度器**，渐进地从历史重建过渡到未来预测。在三个公开数据集上的实验表明，我们的方法显著优于最先进的生成式模型，突出表明对过去的全面理解对于准确预测用户未来路径至关重要。
