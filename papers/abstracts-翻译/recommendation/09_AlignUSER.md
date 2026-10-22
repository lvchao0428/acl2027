# AlignUSER: Human-Aligned LLM Agents via World Models for

> 来源文件：09_AlignUSER.pdf

## 英文原文摘要（Original Abstract）

Evaluating recommender systems remains challenging due to the gap between offline metrics and real user behavior, as well as the scarcity of interaction data. Recent work explores large language model (LLM) agents as synthetic users, yet they typically rely on few-shot prompting, which yields a shallow understanding of the environment and limits their ability to faithfully reproduce user actions. We introduce ALIGNUSER, a framework that learns world-model-driven agents from human interactions. Given rollout sequences of actions and states, we formalize world modeling as a next state prediction task that helps the agent internalize the environment. To align actions with human personas, we generate counterfactual trajectories around demonstrations and prompt the LLM to compare its decisions with human choices, identify suboptimal actions, and extract lessons. The learned policy is then used to drive agent interactions with the recommender system. We evaluate ALIGNUSER across multiple datasets and demonstrate closer alignment with genuine humans than prior work, both at the micro and macro levels.

## 中文翻译（Chinese Translation）

推荐系统的评测仍具挑战，原因在于离线指标与真实用户行为之间存在差距，且交互数据稀缺。近期工作探索将大语言模型（LLM）智能体用作合成用户，但它们通常依赖少样本提示（few-shot prompting），对环境的理解较浅，限制了其忠实复现用户行为的能力。我们提出 ALIGNUSER，一个从人类交互中学习世界模型驱动（world-model-driven）智能体的框架。给定动作与状态的 rollout 序列，我们将世界建模形式化为下一状态预测任务，帮助智能体内化环境。为使动作与人类 persona 对齐，我们在演示（demonstration）周围生成反事实轨迹（counterfactual trajectories），并提示 LLM 将自身决策与人类选择对比，识别次优动作并提炼经验。学到的策略随后用于驱动智能体与推荐系统的交互。我们在多个数据集上评测 ALIGNUSER，结果表明它在微观与宏观层面都比以往工作更贴近真实人类。
