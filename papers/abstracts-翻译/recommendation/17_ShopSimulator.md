# ShopSimulator: Evaluating and Exploring RL-Driven LLM Agent for

> 来源文件：17_ShopSimulator.pdf

## 英文原文摘要（Original Abstract）

Large language model (LLM)-based agents are increasingly deployed in e-commerce shopping. To perform thorough, user-tailored product searches, agents should interpret personal preferences, engage in multi-turn dialogues, and ultimately retrieve and discriminate among highly similar products. However, existing research has yet to provide a uniﬁed simulation environment that consistently captures all of these aspects, and always focuses solely on evaluation benchmarks without training support. In this paper, we introduce ShopSimulator, a large-scale and challenging Chinese shopping environment. Leveraging ShopSimulator, we evaluate LLMs across diverse scenarios, ﬁnding that even the best-performing models achieve less than 40% full-success rate. Error analysis reveals that agents struggle with deep search and product selection in long trajectories, fail to balance the use of personalization cues, and to effectively engage with users. Further training exploration provides practical guidance for overcoming these weaknesses, with the combination of supervised ﬁne-tuning (SFT) and reinforcement learning (RL) yielding signiﬁcant performance improvements. Code and data are released at https://github.com/ShopAgent-Team/ShopSimulator.

## 中文翻译（Chinese Translation）

基于大语言模型（LLM）的智能体正越来越多地部署在电商购物场景中。要完成彻底、贴合用户的商品搜索，智能体应解读个人偏好、进行多轮对话，并最终在高度相似的商品中检索与判别。然而，现有研究尚未提供一个统一的模拟环境来一致地涵盖这些方面，且往往仅关注评测基准而不提供训练支持。本文引入 ShopSimulator，一个大规模、具挑战性的中文购物环境。基于 ShopSimulator，我们在多样化场景下评测 LLM，发现即便是表现最好的模型，完整成功率也不足 40%。错误分析显示，智能体在长轨迹中的深度搜索与商品选择、个性化线索的平衡使用、以及与用户的有效互动方面均存在困难。进一步的训练探索为克服这些弱点提供了实用指引：监督微调（SFT）与强化学习（RL）相结合可带来显著性能提升。代码与数据：https://github.com/ShopAgent-Team/ShopSimulator。
