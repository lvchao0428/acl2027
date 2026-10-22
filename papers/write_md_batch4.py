#!/usr/bin/env python3
"""Write bilingual markdown files - batch 4 (last 6)."""
import os

OUT_DIR = "/Users/a58/project/paper/acl2027/papers/abstracts-翻译/3-关键词撞车"

FILES = []

# 18. ProvBench
FILES.append({
    "filename": "ProvBench - A Benchmark of Legal Provision Recommendation for Contract Auto-Reviewing.md",
    "title": "ProvBench: A Benchmark of Legal Provision Recommendation for Contract Auto-Reviewing",
    "source": "ProvBench - A Benchmark of Legal Provision Recommendation for Contract Auto-Reviewing.pdf",
    "en": """Contract review is a critical process to protect the rights and interests of the parties involved. However, this process is time-consuming, labor-intensive, and costly, especially when a contract faces multiple rounds of review. To accelerate the contract review and promote the completion of transactions, this paper introduces a novel benchmark of legal provision recommendation and conflict detection for contract auto-reviewing (PROVBENCH), which aims to recommend the legal provisions related to contract clauses and detect possible legal conflicts. Specifically, we construct the first Legal Provision Recommendation Dataset: PROVDATA, which covers 8 common contract types. In addition, we conduct extensive experiments to evaluate PROVBENCH on various state-of-the-art models. Experimental results validate the feasibility of PROVBENCH and demonstrate the effectiveness of PROVDATA. Finally, we identify potential challenges in the PROVBENCH and advocate for further investigation.""",
    "zh": """合同审查是保护合同当事人权益的关键环节，但该过程耗时、费力且成本高昂，尤其当合同需要多轮审查时更是如此。为加速合同审查、促进交易达成，本文提出一个面向合同自动审查的法律条款推荐与冲突检测基准（PROVBENCH），旨在为合同条款推荐相关法律条文，并检测潜在的法律冲突。具体而言，我们构建了首个法律条款推荐数据集 PROVDATA，覆盖 8 类常见合同。此外，我们在多种当前最优模型上对 PROVBENCH 进行了大量实验评估。实验结果验证了 PROVBENCH 的可行性，也证明了 PROVDATA 的有效性。最后，我们指出了 PROVBENCH 中存在的潜在挑战，并呼吁学界进一步研究。"""
})

# 19. Scholar Inbox
FILES.append({
    "filename": "Scholar Inbox - Personalized Paper Recommendations for Scientists.md",
    "title": "Scholar Inbox: Personalized Paper Recommendations for Scientists",
    "source": "Scholar Inbox - Personalized Paper Recommendations for Scientists.pdf",
    "en": """Scholar Inbox is a new open-access platform designed to address the challenges researchers face in staying current with the rapidly expanding volume of scientific literature. We provide personalized recommendations, continuous updates from open-access archives (arXiv, bioRxiv, etc.), visual paper summaries, semantic search, and a range of tools to streamline research workflows and promote open research access. The platform's personalized recommendation system is trained on user ratings, ensuring that recommendations are tailored to individual researchers' interests. To further enhance the user experience, Scholar Inbox also offers a map of science that provides an overview of research across domains, enabling users to easily explore specific topics. We use this map to address the cold start problem common in recommender systems, as well as an active learning strategy that iteratively prompts users to rate a selection of papers, allowing the system to learn user preferences quickly. We evaluate the quality of our recommendation system on a novel dataset of 800k user ratings, which we make publicly available, as well as via an extensive user study.""",
    "zh": """Scholar Inbox 是一个全新的开放获取平台，旨在应对科研人员在科学文献数量快速膨胀背景下"追新读全"的难题。我们提供个性化论文推荐、来自开放获取档案（arXiv、bioRxiv 等）的持续更新、可视化论文摘要、语义搜索，以及一系列简化科研流程、推动开放科研访问的工具。平台的个性化推荐系统基于用户评分进行训练，确保推荐内容贴合每位研究者的兴趣。为进一步提升用户体验，Scholar Inbox 还提供一张"科学地图"（map of science），概览各领域的研究版图，帮助用户轻松探索特定主题。我们利用该地图解决推荐系统中常见的冷启动问题，并结合主动学习策略，迭代地请用户对一批论文打分，使系统快速学习用户偏好。我们在一个新发布的 80 万条用户评分数据集上评估了推荐系统的质量（该数据集已公开），并开展了大规模用户研究。"""
})

# 20. Stronger, Lighter, Better
FILES.append({
    "filename": "Stronger, Lighter, Better - Towards Life-Long Attribute Value Extraction for E-Commerce Products.md",
    "title": "Stronger, Lighter, Better: Towards Life-Long Attribute Value Extraction for E-Commerce Products",
    "source": "Stronger, Lighter, Better - Towards Life-Long Attribute Value Extraction for E-Commerce Products.pdf",
    "en": """Attribute value extraction involves identifying the value spans of predetermined attributes in product texts. This area of research has traditionally operated under a closed-world assumption, focusing on products from a static set of categories and their associated attributes. However, products in e-commerce stores are ever-increasing and evolving, calling for life-long learning. If continuously trained on the fast-increasing products and attributes, most existing solutions not only struggle for parameter efficiency but also endure foreseeable defects due to data contamination, catastrophic forgetting, etc. As a remedy, we propose and study a new task, which aims to effectively maintain a strong single model for many domains in a life-long learning fashion, without jeopardizing the model performance and parameter efficiency. We introduce factorization into the model and make it domain-aware by decoupling the modeling of product type and attribute, as a way to promote de-contamination and parameter efficiency while scaling up. Tuning the model with distillation prevents forgetting historical knowledge and enables continuous learning from emerging domains. Experiments on hundreds of domains show that our model attains near state-of-the-art performance with affordable parameter size, the least historical knowledge forgetting, and the greatest robustness against noises, whilst adding only a few parameters per domain when compared with competitive baselines.""",
    "zh": """属性值抽取（attribute value extraction）是指从商品文本中识别预定义属性对应的值片段。该研究方向传统上一直基于闭世界假设，聚焦于一组静态类目及其关联属性上的商品。然而，电商店铺中的商品不断增长和演变，要求系统具备终身学习（life-long learning）能力。若在快速增长的商品和属性上持续训练，现有大多数方案不仅在参数效率上捉襟见肘，还会因数据污染、灾难性遗忘等问题出现可预见的缺陷。作为对策，我们提出并研究一个新任务：以终身学习的方式，为众多领域有效地维护一个强大的单一模型，同时不损害模型性能与参数效率。我们在模型中引入因子分解（factorization），通过解耦商品类型与属性的建模来使其具备领域感知能力，从而在扩展规模的同时促进去污染和参数效率。使用蒸馏（distillation）来微调模型，可防止历史知识遗忘，并支持从新兴领域持续学习。在数百个领域上的实验表明，我们的模型以可接受的参数量达到接近当前最优的性能，历史知识遗忘最少，对噪声的鲁棒性最强，且相比有竞争力的基线，每个新领域仅需新增少量参数。"""
})

# 21. SymTax
FILES.append({
    "filename": "SymTax - Symbiotic Relationship and Taxonomy Fusion for Effective Citation Recommendation.md",
    "title": "SymTax: Symbiotic Relationship and Taxonomy Fusion for Effective Citation Recommendation",
    "source": "SymTax - Symbiotic Relationship and Taxonomy Fusion for Effective Citation Recommendation.pdf",
    "en": """Citing pertinent literature is pivotal to writing and reviewing a scientific document. Existing techniques mainly focus on the local context or the global context for recommending citations but fail to consider the actual human citation behaviour. We propose SymTax, a three-stage recommendation architecture that considers both the local and the global context, and additionally the taxonomical representations of query-candidate tuples and the Symbiosis prevailing amongst them. SymTax learns to embed the infused taxonomies in the hyperbolic space and uses hyperbolic separation as a latent feature to compute query-candidate similarity. We build a novel and large dataset ArSyTa containing 8.27 million citation contexts and describe the creation process in detail. We conduct extensive experiments and ablation studies to demonstrate the effectiveness and design choice of each module in our framework. Also, combinatorial analysis from our experiments shed light on the choice of language models (LMs) and fusion embedding, and the inclusion of section heading as a signal. Our proposed module that captures the symbiotic relationship solely leads to performance gains of 26.66% and 39.25% in Recall@5 w.r.t. SOTA on ACL-200 and RefSeer datasets, respectively. The complete framework yields a gain of 22.56% in Recall@5 w.r.t. SOTA on our proposed dataset. The code and dataset are available at https://github.com/goyalkaraniit/SymTax.""",
    "zh": """引用相关文献对于撰写和评审科学论文至关重要。现有技术主要聚焦局部上下文或全局上下文来推荐引文，但未能考虑真实的人类引用行为。我们提出 SymTax，一个三阶段推荐架构，同时考虑局部与全局上下文，并进一步引入查询-候选对（query-candidate tuple）的分类学表示以及它们之间普遍存在的共生关系（Symbiosis）。SymTax 学习将融合后的分类学知识嵌入双曲空间（hyperbolic space），并利用双曲空间中的分离度作为隐特征来计算查询-候选相似度。我们构建了一个新颖且大规模的数据集 ArSyTa，包含 827 万个引用上下文，并详细描述了其构建过程。我们进行了大量实验与消融研究，以验证框架中各模块的有效性与设计选择。组合分析还揭示了语言模型（LM）选择、融合嵌入方式，以及引入章节标题作为信号的价值。我们提出的、仅用于捕捉共生关系的模块，在 ACL-200 和 RefSeer 数据集上分别使 Recall@5 相对当前最优提升 26.66% 和 39.25%；完整框架在我们自建数据集上使 Recall@5 相对当前最优提升 22.56%。代码与数据集见 https://github.com/goyalkaraniit/SymTax 。"""
})

# 22. TablePilot
FILES.append({
    "filename": "TablePilot - Recommending Human-Preferred Tabular Data Analysis with Large Language Models.md",
    "title": "TablePilot: Recommending Human-Preferred Tabular Data Analysis with Large Language Models",
    "source": "TablePilot - Recommending Human-Preferred Tabular Data Analysis with Large Language Models.pdf",
    "en": """Tabular data analysis is crucial in many scenarios, yet efficiently identifying relevant queries and results for new tables remains challenging due to data complexity, diverse analytical operations, and high-quality analysis requirements. To address these challenges, we aim to recommend query–code–result triplets tailored for new tables in tabular data analysis workflows. In this paper, we present TablePilot, a pioneering tabular data analysis framework leveraging large language models to autonomously generate comprehensive and superior analytical results without relying on user profiles or prior interactions. Additionally, we propose Rec-Align, a novel method to further improve recommendation quality and better align with human preferences. Experiments on DART, a dataset specifically designed for comprehensive tabular data analysis recommendation, demonstrate the effectiveness of our framework. Based on GPT-4o, the tuned TablePilot achieves 77.0% top-5 recommendation recall. Human evaluations further highlight its effectiveness in optimizing tabular data analysis workflows.""",
    "zh": """表格数据分析在众多场景中都至关重要，但由于数据复杂性、分析操作多样以及高质量分析要求高，为新表格高效识别相关查询和结果仍极具挑战。为应对这些挑战，我们旨在为表格数据分析工作流中的新表格推荐"查询-代码-结果"三元组。本文提出 TablePilot，这是一个开创性的表格数据分析框架，利用大语言模型自主生成全面且高质量的分析结果，无需依赖用户画像或历史交互。此外，我们提出 Rec-Align 这一新方法，进一步提升推荐质量，使其更好地对齐人类偏好。在专门为综合表格数据分析推荐而设计的数据集 DART 上的实验验证了本框架的有效性。基于 GPT-4o 调优后的 TablePilot 达到 77.0% 的 top-5 推荐召回率。人工评估进一步凸显了其在优化表格数据分析工作流方面的效果。"""
})

# 23. Visualization Recommendation (HTP)
FILES.append({
    "filename": "Visualization Recommendation with Prompt-based Reprogramming of Large Language Models.md",
    "title": "Visualization Recommendation with Prompt-based Reprogramming of Large Language Models",
    "source": "Visualization Recommendation with Prompt-based Reprogramming of Large Language Models.pdf",
    "en": """Visualization recommendations, which aim to automatically match proper visual charts for specific data tables, can significantly simplify the data analysis process. Traditional approaches in this domain have primarily relied on rule-based or machine learning-based methodologies. These methods often demand extensive manual maintenance and yet fail to fully comprehend the tabular data, leading to unsatisfactory performance. Recently, Large Language Models (LLMs) have emerged as powerful tools, exhibiting strong reasoning capabilities. This advancement suggests their substantial promise in addressing visualization recommendation challenges. However, effectively harnessing LLMs to discern and rationalize patterns in tabular data, and consequently deduce the essential information for chart generation, remains an unresolved challenge. To this end, we introduce a novel Hierarchical Table Prompt-based reprogramming framework, named HTP. This framework aims to integrate multi-dimensional tabular data into LLMs through a strategically crafted prompt learning method while keeping the LLMs' backbone and weights unaltered. The HTP framework uniquely incorporates a four-level prompt structure, encompassing general, instance, cluster, and column levels. This multi-level approach is engineered to provide a comprehensive understanding of both general distribution and multifaceted fine-grained features of tabular data, before inputting the tabular data into the frozen LLM. Our empirical studies confirm that the HTP framework achieves state-of-the-art performance, marking an advancement in the field of data visualization and analysis.""",
    "zh": """可视化推荐旨在为特定数据表自动匹配合适的图表，可显著简化数据分析过程。该领域的传统方法主要依赖基于规则或基于机器学习的手段。这些方法通常需要大量人工维护，且无法充分理解表格数据，导致性能不尽如人意。近年来，大语言模型（LLM）展现出强大的推理能力，为解决可视化推荐挑战带来了广阔前景。然而，如何有效利用 LLM 来识别并合理解释表格数据中的模式，进而推断出图表生成所需的关键信息，仍是一个未解决的挑战。为此，我们提出一个新颖的、基于分层表格提示的重编程框架 HTP。该框架通过精心设计的提示学习方法，将多维表格信息融入 LLM，同时保持 LLM 主干结构与权重不变。HTP 框架独特地采用四级提示结构，涵盖通用级、实例级、簇级和列级。这种多层次设计旨在在将表格数据输入冻结的 LLM 之前，同时兼顾对整体分布和多方面细粒度特征的全面理解。实证研究表明，HTP 框架达到了当前最优性能，标志着数据可视化与分析领域的一项进步。"""
})


def write_file(f):
    path = os.path.join(OUT_DIR, f["filename"])
    content = f"""# {f["title"]}
> 来源文件：{f["source"]}

## 英文原文摘要（Original Abstract）

{f["en"]}

## 中文翻译（Chinese Translation）

{f["zh"]}
"""
    with open(path, "w", encoding="utf-8") as fp:
        fp.write(content)
    print("Wrote:", path)


for f in FILES:
    write_file(f)
