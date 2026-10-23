# HSUGA: LLM-Enhanced Recommendation with Hierarchical Semantic Understanding and Group-Aware Alignment
> 来源文件：HSUGA - LLM-Enhanced Recommendation with Hierarchical Semantic Understanding and Group-Aware Alignment.pdf
> 发表年份：2026
> 单位：Shenzhen University；Shenzhen Technology University

## 英文原文摘要（Original Abstract）

Large language model (LLM)-enhanced sequential recommendation typically aims to improve two core components: user semantic embedding extraction and utilization. Despite promising results, existing methods still have two limitations: 1) In the extraction stage, most methods directly input long interaction sequence fragments into LLM for preference summarization. However, excessively long sequences increase inference difficulty, making it challenging to reliably infer accurate user embeddings. 2) In the utilization stage, most methods employ the same semantic embedding utilization strategy for all users, neglecting the differences caused by user activity levels, leading to suboptimal performance. To address these issues, we propose HSUGA, which introduces a simple yet effective plugin for each of the two core components: Hierarchical Semantic Understanding (HSU) and Group-Aware Alignment (GAA). HSU performs a staged twophase preference mining and models preference evolution through constrained editing operations, thereby improving the reliability of user semantic extraction. GAA adjusts the intensity of semantic utilization based on user activity levels, providing weaker alignment for active users and stronger guidance for users with sparse historical data. Finally, extensive experiments on three benchmark datasets demonstrate the effectiveness and compatibility of HSUGA.

## 中文翻译（Chinese Translation）

LLM 增强的序列推荐通常旨在改进两个核心组件：用户语义嵌入（user semantic embedding）的提取与利用。尽管已取得不错结果，现有方法仍存在两点局限：1) 在提取阶段，多数方法直接把长交互序列片段输入 LLM 进行偏好总结，但过长的序列会增加推理难度，难以可靠地推断出准确的用户嵌入；2) 在利用阶段，多数方法对所有用户采用同一套语义嵌入利用策略，忽视了不同用户活跃度（activity level）带来的差异，导致性能次优。针对这些问题，我们提出 HSUGA，为两个核心组件各引入一个简单而有效的插件：分层语义理解（Hierarchical Semantic Understanding, HSU）与群感知对齐（Group-Aware Alignment, GAA）。HSU 进行分阶段的两阶段偏好挖掘，并通过约束编辑操作建模偏好演化，从而提升用户语义提取的可靠性；GAA 根据用户活跃度调整语义利用强度——对活跃用户给较弱的对齐，对历史数据稀疏的用户给更强的引导。最后，在三个基准数据集上的大量实验证明了 HSUGA 的有效性与兼容性。
