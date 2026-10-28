# From Past To Path: Masked History Learning for Next-Item Prediction in Generative Recommendation

> 来源文件：12_MHL.pdf
> 发表年份：2026
> 单位：Institute of automation, Chinese academy of science；Hong Kong University of Science and Technology；Chongqing University；Institute of automation, Chinese academy of science, Chinese Academy of Sciences

## 英文原文摘要（Original Abstract）

Generative recommendation, which directly generates item identifiers, has emerged as a promising paradigm for recommendation systems. However, this left-to-right paradigm inherently biases the model towards local contexts, failing to capture deeper historical dependencies necessary for understanding complex user intents. To address this limitation, we propose Masked History Learning (MHL), a novel training framework that shifts the objective from simple next-step prediction to deep comprehension of history. MHL augments the standard autoregressive objective with an auxiliary task of reconstructing masked historical items, compelling the model to understand "why" an item path is formed from the user's past behaviors, rather than just "what" item comes next. We introduce two key contributions to enhance this framework: (1) an entropy-guided masking policy that intelligently targets the most informative historical items for reconstruction, and (2) a curriculum learning scheduler that progressively transitions from history reconstruction to future prediction. Experiments on three public datasets show that our method significantly outperforms state-of-the-art generative models, highlighting that a comprehensive understanding of the past is crucial for accurately predicting a user's future path. The code is available at https://github.com/CQU-MM-Intelligent-Lab/MHL.

## 中文翻译（Chinese Translation）

直接生成物品标识的生成式推荐（generative recommendation）已成为推荐系统颇具前景的范式。然而，这种从左到右的范式固有地将模型偏向局部上下文，无法捕捉理解复杂用户意图所需的深层历史依赖。为弥补这一局限，我们提出 Masked History Learning（MHL），一种新颖的训练框架，将目标从简单的下一步预测转变为对历史的深度理解。MHL 在标准自回归目标之外，增加了"重建被掩码的历史物品"这一辅助任务，迫使模型理解用户历史行为"为何"形成这样的物品路径，而不仅是"下一个物品是什么"。我们进一步引入两项关键贡献：（1）熵引导的掩码策略（entropy-guided masking policy），智能地针对最具信息量的历史物品进行重建；（2）课程学习调度器（curriculum learning scheduler），渐进地从历史重建过渡到未来预测。在三个公开数据集上的实验表明，我们的方法显著优于 SOTA 生成式模型，凸显对过去的全面理解是准确预测用户未来路径的关键。代码：https://github.com/CQU-MM-Intelligent-Lab/MHL。
