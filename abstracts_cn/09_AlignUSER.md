# AlignUSER: 通过世界模型实现与人类对齐的 LLM 推荐系统评估智能体

**原标题**: AlignUSER: Human-Aligned LLM Agents via World Models for Recommender System Evaluation

**作者**: Nicolas Bougie, Gian Maria Marconi, Xiaotong Ye, Narimasa Watanabe

**单位**: Woven by Toyota

## 摘要

由于离线指标与真实用户行为之间的差距以及交互数据的稀缺性，评估推荐系统仍然充满挑战。近期研究探索将大语言模型（LLM）智能体用作合成用户，但它们通常依赖少样本提示（few-shot prompting），这只能获得对环境的浅层理解，限制了其忠实复现用户行为的能力。我们引入 AlignUSER，一个从人类交互中学习世界模型驱动智能体的框架。给定动作和状态的展开序列，我们将世界建模形式化为下一状态预测任务，帮助智能体内化环境动力学。为使动作与人类画像对齐，我们围绕演示生成反事实轨迹，并提示 LLM 将其决策与人类选择进行比较，识别次优动作并提取经验教训。学习到的策略随后用于驱动智能体与推荐系统的交互。我们在多个数据集上评估 AlignUSER，证明其在微观和宏观层面上均比先前工作更贴近真实人类。
