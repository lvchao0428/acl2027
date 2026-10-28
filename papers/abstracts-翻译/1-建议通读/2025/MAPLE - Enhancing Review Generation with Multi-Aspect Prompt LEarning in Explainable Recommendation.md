# MAPLE: Enhancing Review Generation with Multi-Aspect Prompt LEarning in Explainable Recommendation
> 来源文件：MAPLE - Enhancing Review Generation with Multi-Aspect Prompt LEarning in Explainable Recommendation.pdf
> 发表年份：2025
> 单位：Chang Gung University；Google；Department of Computer Science, National Tsing Hua University, National Tsinghua University

## 英文原文摘要（Original Abstract）

The Explainable Recommendation task is designed to receive a pair of user and item and output explanations to justify why an item is recommended to a user. Many models approach review generation as a proxy for explainable recommendations. While these models can produce ﬂuent and grammatically correct sentences, they often lack precision and fail to provide personalized, informative recommendations. To address this issue, we propose a personalized, aspect-controlled model called Multi-Aspect Prompt LEarner (MAPLE), which integrates aspect category as another input dimension to facilitate memorizing ﬁne-grained aspect terms. Experiments conducted on two real-world review datasets in the restaurant domain demonstrate that MAPLE signiﬁcantly outperforms baseline review-generation models. MAPLE excels in both text and feature diversity, ensuring that the generated content covers a wide range of aspects. Additionally, MAPLE delivers good generation quality while maintaining strong coherence and factual relevance.

## 中文翻译（Chinese Translation）

可解释推荐任务旨在接收一对用户-商品，输出相应的解释以论证为何向用户推荐该商品。许多模型把评论生成作为可解释推荐的代理（proxy）。尽管这些模型能生成流畅、语法正确的句子，但往往缺乏精度，难以提供个性化、信息丰富的推荐。为解决该问题，我们提出一个个性化、方面可控的模型 Multi-Aspect Prompt LEarner（MAPLE），它将方面类别（aspect category）作为另一输入维度，以便记忆细粒度的方面词（aspect terms）。在餐厅领域两个真实评论数据集上的实验表明，MAPLE 显著优于基线评论生成模型。MAPLE 在文本多样性和特征多样性上都表现出色，确保生成内容覆盖广泛的方面；同时在保持强连贯性和事实相关性的前提下，提供良好的生成质量。本文所用代码与数据集见 https://github.com/Nana2929/MAPLE。
