# AgentCF: Collaborative Learning with Autonomous Language Agents for Recommender Systems
> 来源文件：AgentCF - Collaborative Learning with Autonomous Language Agents for Recommender Systems.pdf
> 发表年份：2024
> 会议：The Web Conference (WWW) 2024
> 单位：论文首页（作者包括中国人民大学、UCSD、腾讯微信）

## 英文原文摘要（Original Abstract）

Recently, there has been an emergence of employing LLM-powered agents as believable human proxies, based on their remarkable decision-making capability. However, existing studies mainly focus on simulating human dialogue. Human non-verbal behaviors, such as item clicking in recommender systems, although implicitly exhibiting user preferences and could enhance the modeling of users, have not been deeply explored. The main reasons lie in the gap between language modeling and behavior modeling, as well as the incomprehension of LLMs about user-item relations. To address this issue, we propose AgentCF for simulating user-item interactions in recommender systems through agent-based collaborative filtering. We creatively consider not only users but also items as agents, and develop a collaborative learning approach that optimizes both kinds of agents together. Specifically, at each time step, we first prompt the user and item agents to interact autonomously. Then, based on the disparities between the agents' decisions and real-world interaction records, user and item agents are prompted to reflect on and adjust the misleading simulations collaboratively, thereby modeling their two-sided relations. The optimized agents can also propagate their preferences to other agents in subsequent interactions, implicitly capturing the collaborative filtering idea. Overall, the optimized agents exhibit diverse interaction behaviors within our framework, including user-item, user-user, item-item, and collective interactions. The results show that these agents can demonstrate personalized behaviors akin to those of real-world individuals, sparking the development of next-generation user behavior simulation.

## 中文翻译（Chinese Translation）

近来已有工作把 LLM agent 当作可信的人类代理，依据是它们较强的决策能力。但已有研究主要模拟人类对话。点击物品这类非言语行为隐含着用户偏好，本可以加强用户建模，却还没有被深入做过。原因是语言建模和行为建模之间有差距，LLM 也不理解用户与物品的关系。为此我们提出 AgentCF，用基于 agent 的协同过滤来模拟推荐系统中的用户–物品交互。我们不只把用户当成 agent，也把物品当成 agent，并让两类 agent 一起优化。每个时间步，先让用户 agent 和物品 agent 自主交互；再根据它们的决定与真实交互记录的差异，促使双方共同反思并修正错误模拟，从而建模双边关系。优化后的 agent 还能在后续交互中把偏好传给其他 agent，这隐含了协同过滤。框架里因此出现用户–物品、用户–用户、物品–物品以及集体交互。结果表明，这些 agent 能表现出接近真实个体的个性化行为，并推动下一代用户行为模拟。
