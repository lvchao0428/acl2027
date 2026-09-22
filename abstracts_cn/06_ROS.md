# ROS: 空间推理——赋能 LLM 生成式下一 POI 推荐的地理推理能力

**原标题**: Reasoning Over Space: Enabling Geographic Reasoning for LLM-Based Generative Next POI Recommendation

**作者**: Dongyi Lv, Qiuyu Ding, Heng-Da Xu 等

**单位**: Xi'an Jiaotong University (XJTU); Amap, Alibaba Group（高德/阿里巴巴）

## 摘要

基于大语言模型（LLMs）的生成式推荐将预测重新定义为序列生成任务，但现有的基于 LLM 的推荐器在利用地理信号方面仍然有限，而这些信号在移动和本地服务场景中至关重要。在此，我们提出**空间推理（ROS）**框架，将地理信息作为推理过程中的关键决策变量。ROS 引入**层次化空间语义 ID（SID）**，将由粗到细的地理位置和 POI 语义离散化为组合式 token，并赋予 LLM 一个**三阶段移动思维链（CoT）**范式：建模用户个性、构建意图对齐的候选空间、以及执行地理信息引导的修剪。我们进一步通过**空间引导的强化学习（RL）**将模型与真实世界地理对齐。在三个广泛使用的基于位置的社交网络（LBSN）数据集上的实验表明，ROS 在命中率上相对最强 LLM 基线提升超过 10%，并改善了跨城市迁移能力，尽管使用了更小的骨干模型。
