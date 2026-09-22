# 镜像用户：利用推荐系统用户反馈构建偏好对齐的用户模拟器

**原标题**: Mirroring Users: Towards Building Preference-aligned User Simulator with User Feedback in Recommendation

**作者**: Tianjun Wei, Huizhong Guo, Yingpeng Du 等

**单位**: Nanyang Technological University (NTU); Zhejiang University; SUTD

## 摘要

用户模拟对于开发和评估推荐系统（RSs）日益重要。尽管大语言模型（LLMs）为模拟用户行为提供了有前景的途径，但它们常常面临推荐系统所需的特定任务对齐缺失以及大规模模拟的效率需求等问题。推荐系统中固有的大量用户反馈是增强这种对齐的巨大但未被充分利用的资源，但由于其歧义性、噪声和海量体量，利用这些反馈具有挑战性，阻碍了高效的偏好对齐。为克服这些困难，我们引入一个新的数据构建框架，利用推荐系统中的用户反馈和先进的 LLM 能力来生成高质量的模拟数据。该框架分两个关键阶段展开：(1) 使用 LLM 生成决策过程作为模拟样本的解释性推理依据（rationale），从而降低歧义；(2) 基于不确定性估计和行为采样的数据蒸馏，高效筛选最具信息量的去噪样本。相应地，我们使用这些高质量数据集及其对应的决策过程对轻量级 LLM 进行微调，使其作为用户模拟器。大量实验证实，我们的框架显著提升了微调 LLM 与人类偏好的对齐度以及领域内推理能力，为推荐系统交互提供了更具洞察力和可解释性的信号。
