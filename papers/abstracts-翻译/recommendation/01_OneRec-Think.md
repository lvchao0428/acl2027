# ONEREC-THINK: In-Text Reasoning for Generative Recommendation

> 来源文件：01_OneRec-Think.pdf
> 发表年份：2026
> 单位：Kuaishou- 快手科技；University of Science and Technology of China

## 英文原文摘要（Original Abstract）

The powerful generative capacity of Large Language Models (LLMs) has instigated a paradigm shift in recommendation. However, existing generative models (e.g., OneRec) operate as implicit predictors, critically lacking the capacity for explicit and controllable reasoning—a key advantage of LLMs. To bridge this gap, we propose OneRec-Think, a unified framework that seamlessly integrates dialogue, reasoning, and personalized recommendation. OneRec-Think incorporates: (1) Itemic Alignment: cross-modal Item-Textual Alignment for semantic grounding; (2) Reasoning Activation: Reasoning Scaffolding to activate LLM reasoning within the recommendation context; and (3) Reasoning Enhancement, where we design a recommendation-specific reward function that accounts for the multi-validity nature of user preferences. Experiments across public benchmarks show state-of-the-art performance. Moreover, our proposed "Think-Ahead" architecture enables effective industrial deployment on Kuaishou, achieving a 0.159% gain in APP Stay Time and validating the practical efficacy of the model's explicit reasoning capability.

## 中文翻译（Chinese Translation）

大语言模型（LLM）强大的生成能力引发了推荐领域的范式转变。然而，现有的生成式推荐模型（例如 OneRec）仅作为隐式预测器运行，严重缺乏显式、可控推理的能力——而这恰恰是 LLM 的关键优势。为弥合这一差距，我们提出了 OneRec-Think，一个将对话、推理与个性化推荐无缝整合的统一框架。OneRec-Think 包含三个核心模块：（1）Itemic Alignment（物品对齐）：通过跨模态 Item-Textual Alignment（物品-文本对齐）实现语义 grounding；（2）Reasoning Activation（推理激活）：采用 Reasoning Scaffolding（推理脚手架）在推荐上下文中激活 LLM 的推理能力；（3）Reasoning Enhancement（推理增强）：设计面向推荐的奖励函数，以刻画用户偏好的多有效性（multi-validity）特性。在多个公开基准上的实验表明，该方法达到了 SOTA 性能。此外，我们提出的"Think-Ahead"架构已在快手实现工业级部署，使 APP 停留时长提升 0.159%，验证了模型显式推理能力在实际场景中的有效性。
