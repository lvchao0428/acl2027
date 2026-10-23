# SymTax: Symbiotic Relationship and Taxonomy Fusion for Effective Citation Recommendation
> 来源文件：SymTax - Symbiotic Relationship and Taxonomy Fusion for Effective Citation Recommendation.pdf
> 发表年份：2024
> 单位：Indraprastha Institute of Information Technology, Delhi；Indraprastha Institute of Information Technology

## 英文原文摘要（Original Abstract）

Citing pertinent literature is pivotal to writing and reviewing a scientific document. Existing techniques mainly focus on the local context or the global context for recommending citations but fail to consider the actual human citation behaviour. We propose SymTax, a three-stage recommendation architecture that considers both the local and the global context, and additionally the taxonomical representations of query-candidate tuples and the Symbiosis prevailing amongst them. SymTax learns to embed the infused taxonomies in the hyperbolic space and uses hyperbolic separation as a latent feature to compute query-candidate similarity. We build a novel and large dataset ArSyTa containing 8.27 million citation contexts and describe the creation process in detail. We conduct extensive experiments and ablation studies to demonstrate the effectiveness and design choice of each module in our framework. Also, combinatorial analysis from our experiments shed light on the choice of language models (LMs) and fusion embedding, and the inclusion of section heading as a signal. Our proposed module that captures the symbiotic relationship solely leads to performance gains of 26.66% and 39.25% in Recall@5 w.r.t. SOTA on ACL-200 and RefSeer datasets, respectively. The complete framework yields a gain of 22.56% in Recall@5 w.r.t. SOTA on our proposed dataset. The code and dataset are available at https://github.com/goyalkaraniit/SymTax.

## 中文翻译（Chinese Translation）

引用相关文献对于撰写和评审科学论文至关重要。现有技术主要聚焦局部上下文或全局上下文来推荐引文，但未能考虑真实的人类引用行为。我们提出 SymTax，一个三阶段推荐架构，同时考虑局部与全局上下文，并进一步引入查询-候选对（query-candidate tuple）的分类学表示以及它们之间普遍存在的共生关系（Symbiosis）。SymTax 学习将融合后的分类学知识嵌入双曲空间（hyperbolic space），并利用双曲空间中的分离度作为隐特征来计算查询-候选相似度。我们构建了一个新颖且大规模的数据集 ArSyTa，包含 827 万个引用上下文，并详细描述了其构建过程。我们进行了大量实验与消融研究，以验证框架中各模块的有效性与设计选择。组合分析还揭示了语言模型（LM）选择、融合嵌入方式，以及引入章节标题作为信号的价值。我们提出的、仅用于捕捉共生关系的模块，在 ACL-200 和 RefSeer 数据集上分别使 Recall@5 相对当前最优提升 26.66% 和 39.25%；完整框架在我们自建数据集上使 Recall@5 相对当前最优提升 22.56%。代码与数据集见 https://github.com/goyalkaraniit/SymTax 。
