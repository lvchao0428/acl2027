# RecMind: Large Language Model Powered Agent For Recommendation
> 来源文件：RecMind - Large Language Model Powered Agent For Recommendation.pdf
> 发表年份：2024
> 会议：NAACL 2024 Findings
> 单位：Arizona State University；Amazon Alexa AI

## 英文原文摘要（Original Abstract）

While the recommendation system (RS) has advanced significantly through deep learning, current RS approaches usually train and fine-tune models on task-specific datasets, limiting their generalizability to new recommendation tasks and their ability to leverage external knowledge due to model scale and data size constraints. Thus, we designed an LLM-powered autonomous recommender agent, RecMind, which is capable of leveraging external knowledge, utilizing tools with careful planning to provide zero-shot personalized recommendations. We propose a Self-Inspiring algorithm to improve the planning ability. At each intermediate step, the LLM "self-inspires" to consider all previously explored states to plan for the next step. This mechanism greatly improves the model's ability to comprehend and utilize historical information in planning for recommendation. We evaluate RecMind's performance in various recommendation scenarios. Our experiment shows that RecMind outperforms existing zero/few-shot LLM-based recommendation baseline methods in various tasks and achieves comparable performance to a fully trained recommendation model P5.

## 中文翻译（Chinese Translation）

推荐系统借助深度学习已经有了明显进展，但现有方法通常在特定任务的数据上训练和微调，既难迁移到新的推荐任务，也难以利用外部知识，原因是模型规模和数据规模都有限。为此我们设计了由大语言模型驱动的自主推荐 agent RecMind。它能利用外部知识，在谨慎规划下调用工具，做零样本的个性化推荐。我们提出 Self-Inspiring 算法来加强规划：每一步，模型都会「自我启发」，把此前探索过的全部状态纳入下一步计划。这使模型在做推荐规划时更能理解和利用历史信息。我们在多种推荐场景中评估 RecMind。实验表明，它在多项任务上超过已有的零样本和少样本 LLM 推荐基线，并达到与全量训练的推荐模型 P5 相当的水平。
