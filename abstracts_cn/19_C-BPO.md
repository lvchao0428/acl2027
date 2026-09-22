# C-BPO: 通过二元反馈实现 LLM 个性化——偏好校准优化框架

**原标题**: Personalizing LLMs with Binary Feedback: A Preference-Corrected Optimization Framework

**作者**: Xilai Ma, Liye Zhao, Weijun Yao 等

**单位**: Harbin Institute of Technology (Shenzhen)（哈工大深圳）; Huawei Technologies; NTU

## 摘要

大语言模型（LLM）个性化旨在将模型行为与个体用户偏好对齐。现有方法通常关注孤立的用户历史，忽略了用户间差异的重要作用。我们提出 **C-BPO**，一个通过偏好校准的二元信号实现 LLM 个性化的框架。通过将目标用户数据作为正反馈，其他用户数据作为隐式负信号的辅助集，C-BPO 捕获了独特的用户间差异。为缓解**偏好重叠问题**——即共享的任务知识被错误惩罚——我们推导出一个基于**正无标记（PU）学习**理论的目标函数。该方法通过减去"正向偏差"来净化负信号，确保与独特个性特征的对齐而不损害通用有用性。在多种个性化任务和骨干 LLM 上的实证实验表明，C-BPO 持续优于基线方法，证明了偏好校准二元信号在建模用户间差异方面的有效性。
