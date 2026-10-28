# On Generative Agents in Recommendation
> 来源文件：On Generative Agents in Recommendation.pdf
> 发表年份：2024
> 会议：SIGIR 2024
> 单位：论文首页（作者包括新加坡国立大学、中国科学技术大学）

## 英文原文摘要（Original Abstract）

Recommender systems are the cornerstone of today's information dissemination, yet a disconnect between offline metrics and online performance greatly hinders their development. Addressing this challenge, we envision a recommendation simulator, capitalizing on recent breakthroughs in human-level intelligence exhibited by Large Language Models (LLMs). We propose Agent4Rec, a user simulator in recommendation, leveraging LLM-empowered generative agents equipped with user profile, memory, and actions modules specifically tailored for the recommender system. In particular, these agents' profile modules are initialized using real-world datasets (e.g., MovieLens, Steam, Amazon-Book), capturing users' unique tastes and social traits; memory modules log both factual and emotional memories and are integrated with an emotion-driven reflection mechanism; action modules support a wide variety of behaviors, spanning both taste-driven and emotion-driven actions. Each agent interacts with personalized recommender models in a page-by-page manner, relying on a pre-implemented collaborative filtering-based recommendation algorithm. We delve into both the capabilities and limitations of Agent4Rec, aiming to explore an essential research question: to what extent can LLM-empowered generative agents faithfully simulate the behavior of real, autonomous humans in recommender systems? Extensive and multi-faceted evaluations of Agent4Rec highlight both the alignment and deviation between agents and user-personalized preferences. Beyond mere performance comparison, we explore insightful experiments, such as emulating the filter bubble effect and discovering the underlying causal relationships in recommendation tasks.

## 中文翻译（Chinese Translation）

推荐系统是当今信息分发的基础，但离线指标和线上表现脱节，严重阻碍了它的发展。针对这个问题，我们设想一个推荐模拟器，借助大语言模型已经表现出的接近人类的智能。我们提出 Agent4Rec，一种面向推荐的用户模拟器。它使用由 LLM 驱动的生成式 agent，并配备专门为推荐系统改造的用户画像、记忆和行动模块。画像用真实数据初始化，例如 MovieLens、Steam、Amazon-Book，以捕捉用户的口味和社交特征；记忆同时记录事实和情绪，并带有由情绪驱动的反思；行动既包括由口味驱动的行为，也包括由情绪驱动的行为。每个 agent 按页与个性化推荐模型交互，底层是一个预先实现的协同过滤推荐算法。我们同时考察 Agent4Rec 的能力和局限，核心问题是：LLM 生成式 agent 能在多大程度上忠实模拟推荐系统中真实、自主的人类行为？多方面评估既看到 agent 与用户个性化偏好的对齐，也看到偏离。除了性能对比，我们还模拟过滤气泡，并探查推荐任务中的因果关系。
