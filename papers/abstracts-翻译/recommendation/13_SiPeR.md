# Where and What: Reasoning Dynamic and Implicit Preferences in

> 来源文件：13_SiPeR.pdf
> 发表年份：2026
> 单位：The Hong Kong Polytechnic University；Hong Kong Polytechnic University；The Hong Kong Polytechnic University, The Hong Kong Polytechnic University

## 英文原文摘要（Original Abstract）

Situated conversational recommendation (SCR), which utilizes visual scenes grounded in specific environments and natural language dialogue to deliver contextually appropriate recommendations, has emerged as a promising research direction due to its close alignment with real-world scenarios. Compared to traditional recommendations, SCR requires a deeper understanding of dynamic and implicit user preferences, as the surrounding scene often influences users' underlying interests, while both may evolve across conversations. This complexity significantly impacts the timing and relevance of recommendations. To address this, we propose situated preference reasoning (SiPeR), a novel framework that integrates two core mechanisms: (i) Scene transition estimation, which estimates whether the current scene satisfies user needs, and guides the user toward a more suitable scene when necessary; and (ii) Bayesian inverse inference, which leverages the likelihood of multimodal large language models (MLLMs) to predict user preferences about candidate items within the scene. Extensive experiments on two representative benchmarks demonstrate SiPeR's superiority in both recommendation accuracy and response generation quality. The code and data are available at https://github.com/DongdingLin/SiPeR.

## 中文翻译（Chinese Translation）

情境化对话式推荐（Situated Conversational Recommendation, SCR）利用根植于特定环境的视觉场景与自然语言对话来交付上下文恰当的推荐，因其与真实场景紧密契合，已成为颇具前景的研究方向。与传统推荐相比，SCR 需要更深入地理解动态、隐式的用户偏好，因为周边场景往往影响用户的底层兴趣，且二者都会在多轮对话中演化。这种复杂性显著影响推荐的时机与相关性。为此，我们提出情境化偏好推理（situated preference reasoning, SiPeR）框架，整合两个核心机制：（i）场景迁移估计（Scene transition estimation），判断当前场景是否满足用户需求，并在必要时引导用户前往更合适的场景；（ii）贝叶斯逆推理（Bayesian inverse inference），利用多模态大语言模型（MLLM）的似然预测用户对场景内候选物品的偏好。在两个代表性基准上的大量实验表明，SiPeR 在推荐准确率与回复生成质量上均具优越性。代码与数据：https://github.com/DongdingLin/SiPeR。
