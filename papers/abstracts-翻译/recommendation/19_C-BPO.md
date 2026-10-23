# Personalizing LLMs with Binary Feedback: A Preference-Corrected Optimization Framework

> 来源文件：19_C-BPO.pdf
> 发表年份：2026
> 单位：Nanyang Technological University；Harbin Institute of Technology

## 英文原文摘要（Original Abstract）

Large Language Model (LLM) personalization aims to align model behaviors with individual user preferences. Existing methods often focus on isolated user histories, neglecting the essential role of inter-user differences. We propose C-BPO, a framework that personalizes LLMs via preference-calibrated binary signals. By treating target user data as positive feedback and other users' data as an auxiliary set of implicit negative signals, C-BPO captures distinct inter-user differences. To mitigate the preference overlap issue, where shared task knowledge is erroneously penalized, we derive an objective grounded in Positive-Unlabeled (PU) learning theory. This approach purifies negative signals by subtracting "positive bias", ensuring alignment with unique idiosyncrasies without compromising general helpfulness. Empirical experiments across various personalization tasks and backbone LLMs show C-BPO consistently outperforms baselines, demonstrating the efficacy of preference-calibrated binary signals in modeling inter-user differences.

## 中文翻译（Chinese Translation）

大语言模型（LLM）个性化旨在使模型行为与个体用户偏好对齐。现有方法往往聚焦于孤立的用户历史，忽略了用户间差异（inter-user differences）的本质作用。我们提出 C-BPO，一个通过偏好校准的二值信号（preference-calibrated binary signals）实现 LLM 个性化的框架。通过将目标用户数据视为正反馈、将其他用户数据视为辅助的隐式负信号集，C-BPO 捕捉了 distinct 的用户间差异。为缓解"偏好重叠"问题——即共享的任务知识被错误惩罚——我们推导了一种基于正样本-未标注（Positive-Unlabeled, PU）学习理论的目标函数。该方法通过减去"正偏置"（positive bias）来纯化负信号，在不损害通用帮助性的前提下，确保与用户独特特质的对齐。在多种个性化任务与骨干 LLM 上的实证实验表明，C-BPO 一致优于基线，证明了偏好校准二值信号在建模用户间差异上的有效性。
