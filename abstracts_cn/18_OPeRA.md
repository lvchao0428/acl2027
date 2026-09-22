# OPeRA: 用于评估 LLM 人类网购行为模拟的观察-画像-推理-行动数据集

**原标题**: OPeRA: A Dataset of Observation, Persona, Rationale, and Action for Evaluating LLMs on Human Online Shopping Behavior Simulation

**作者**: Ziyi Wang, Yuxuan Lu, Wenbo Li 等

**单位**: Northeastern University; USC; Columbia University 等

## 摘要

大语言模型（LLMs）能否准确模拟特定用户的下一步网页操作？尽管 LLM 已展现出生成"可信"人类行为的有前景的能力，但评估其模拟真实用户行为的能力仍然是一个开放挑战，主要原因是缺乏同时捕捉实际人类用户的可观察行为和内部推理过程的高质量公开数据集。为解决这一差距，我们引入 **OPeRA**，一个在真实人类参与者在线购物会话中收集的包含**观察（Observation）、画像（Persona）、推理依据（Rationale）和行动（Action）**的新型数据集。OPeRA 是首个全面捕捉以下要素的公开数据集：用户画像、浏览器观察、细粒度网页操作以及自报告的即时推理依据。我们开发了在线问卷和定制浏览器插件以高保真度收集该数据集。利用 OPeRA，我们建立了首个评测基准，用于评估当前 LLM 在给定画像和 <观察, 行动, 推理依据> 历史的条件下，预测特定用户下一步行动和推理依据的能力。该数据集为未来研究旨在作为个性化数字孪生的 LLM 智能体奠定了基础。
