# KERL: Knowledge-Enhanced Personalized Recipe Recommendation using Large Language Models
> 来源文件：KERL - Knowledge-Enhanced Personalized Recipe Recommendation using Large Language Models.pdf
> 发表年份：2025
> 单位：Anthology 未著录

## 英文原文摘要（Original Abstract）

Recent advances in large language models (LLMs) and the abundance of food data have resulted in studies to improve food understanding using LLMs. Despite several recommendation systems utilizing LLMs and Knowledge Graphs (KGs), there has been limited research on integrating food related KGs with LLMs. We introduce KERL, a unified system that leverages food KGs and LLMs to provide personalized food recommendations and generates recipes with associated micro-nutritional information. Given a natural language question, KERL extracts entities, retrieves subgraphs from the KG, which are then fed into the LLM as context to select the recipes that satisfy the constraints. Next, our system generates the cooking steps and nutritional information for each recipe. To evaluate our approach, we also develop a benchmark dataset by curating recipe related questions, combined with constraints and personal preferences. Through extensive experiments, we show that our proposed KG-augmented LLM significantly outperforms existing approaches, offering a complete and coherent solution for food recommendation, recipe generation, and nutritional analysis.

## 中文翻译（Chinese Translation）

近年来大语言模型（LLM）的进展与食物数据的丰富，催生了利用 LLM 改进食物理解的研究。尽管已有若干推荐系统同时使用 LLM 与知识图谱（KG），但将食物相关 KG 与 LLM 相整合的研究仍然有限。我们引入 KERL，一个统一系统，它利用食物 KG 和 LLM 提供个性化食物推荐，并生成附带微量营养信息的食谱。给定一个自然语言问题，KERL 抽取实体、从 KG 检索子图，再将这些子图作为上下文喂给 LLM，以选出满足约束的食谱；随后系统为每个食谱生成烹饪步骤和营养信息。为评估本方法，我们还构建了一个基准数据集，整合了与食谱相关的问题、约束以及个人偏好。大量实验表明，我们提出的 KG 增强 LLM 显著优于现有方法，为食物推荐、食谱生成和营养分析提供了一套完整、连贯的解决方案。代码与基准数据集见 https://github.com/mohbattharani/KERL。
