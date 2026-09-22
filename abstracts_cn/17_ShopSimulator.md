# ShopSimulator: 评测和探索 RL 驱动的 LLM 购物助手智能体

**原标题**: ShopSimulator: Evaluating and Exploring RL-Driven LLM Agent for Shopping Assistants

**作者**: Pei Wang, Yanan Wu, Xiaoshuai Song 等

**单位**: Alibaba Group（阿里巴巴）

## 摘要

基于大语言模型（LLM）的智能体在电商购物中的部署日益增多。为了执行全面、用户定制的商品搜索，智能体应能解读个人偏好、参与多轮对话，并最终从高度相似的商品中进行检索和辨别。然而，现有研究尚未提供一个统一的模拟环境来一致性地覆盖所有这些方面，且始终仅聚焦于评测基准而缺乏训练支持。在本文中，我们引入 **ShopSimulator**，一个大规模且具有挑战性的中文购物环境。利用 ShopSimulator，我们在多种场景下评估 LLM，发现即使是表现最好的模型也仅达到不到 40% 的完全成功率。错误分析揭示，智能体在长轨迹中的深度搜索和商品选择方面存在困难，难以平衡个性化线索的使用，以及无法有效与用户互动。进一步的训练探索为克服这些弱点提供了实用指导，其中监督微调（SFT）与强化学习（RL）的组合带来了显著的性能提升。
