# GrocLM: Grocery Category Recommendation in E-Commerce with Large Language Models
> 来源文件：GrocLM - Grocery Category Recommendation in E-Commerce with Large Language Models.pdf

## 英文原文摘要（Original Abstract）

The rapid growth of online grocery shopping requires recommendation systems that capture cyclical purchasing behavior and diverse user intents. Traditional item-level methods face scalability and accuracy challenges, motivating category-level recommendation as a more structured and practical alternative. We present GROCLM, a fine-tuned language model for grocery category recommendation in a real-world production environment. GROCLM employs a two-stage LoRA-based training strategy to encode cyclical purchasing patterns directly into model parameters, enabling more effective utilization of rebuying signals compared to prompt-based conditioning. To ensure valid and controllable outputs, we further introduce a trie-based constrained decoding mechanism over a predefined category space. Experiments on both proprietary production data and a public benchmark demonstrate that GROCLM consistently outperforms strong baselines. In a live production restocking task, GROCLM achieves a 7.5% relative improvement in cart-adds per impression, while maintaining efficient inference by generating all categories jointly. These results highlight the effectiveness and practicality of integrating large language models into structured recommendation systems.

## 中文翻译（Chinese Translation）

在线生鲜杂货购物的快速增长，要求推荐系统能够捕获周期性购买行为和多样化的用户意图。传统的商品级（item-level）方法在可扩展性和准确率上面临挑战，这促使品类级（category-level）推荐成为一种更具结构性、更实用的替代方案。我们提出 GROCLM，一个在真实生产环境中用于杂货品类推荐的微调语言模型。GROCLM 采用基于 LoRA 的两阶段训练策略，将周期性购买模式直接编码进模型参数中，相比基于提示的条件化方式，能更有效地利用复购信号。为保证输出合法、可控，我们进一步引入在预定义品类空间上的、基于 trie 树的约束解码机制。在私有生产数据和公开基准上的实验均表明，GROCLM 持续优于强基线方法。在一个线上生产补货任务中，GROCLM 使每千次曝光的加购量（cart-adds per impression）相对提升 7.5%，同时通过联合生成所有品类保持了高效推理。这些结果展示了将大语言模型融入结构化推荐系统的有效性与实用性。
