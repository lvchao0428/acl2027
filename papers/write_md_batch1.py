#!/usr/bin/env python3
"""Write bilingual markdown files for the first batch of papers."""
import os

OUT_DIR = "/Users/a58/project/paper/acl2027/papers/abstracts-翻译/3-关键词撞车"
os.makedirs(OUT_DIR, exist_ok=True)

FILES = []

# 1. SSUF
FILES.append({
    "filename": "A Semi-supervised Scalable Unified Framework for E-commerce Query Classification.md",
    "title": "A Semi-supervised Scalable Unified Framework for E-commerce Query Classification",
    "source": "A Semi-supervised Scalable Unified Framework for E-commerce Query Classification.pdf",
    "en": """Query classification, including multiple sub-tasks such as intent and category prediction, is vital to e-commerce applications. E-commerce queries are usually short and lack context, and the information between labels cannot be used, resulting in insufficient prior information for modeling. Most existing industrial query classification methods rely on users' posterior click behavior to construct training samples, resulting in a Matthew vicious cycle. Furthermore, the subtasks of query classification lack a unified framework, leading to low efficiency for algorithm optimization. In this paper, we propose a novel Semi-supervised Scalable Unified Framework (SSUF), containing multiple enhanced modules to unify the query classification tasks. The knowledge-enhanced module uses world knowledge to enhance query representations and solve the problem of insufficient query information. The label-enhanced module uses label semantics and semi-supervised signals to reduce the dependence on posterior labels. The structure-enhanced module enhances the label representation based on the complex label relations. Each module is highly pluggable, and input features can be added or removed as needed according to each subtask. We conduct extensive offline and online A/B experiments, and the results show that SSUF significantly outperforms the state-of-the-art models.""",
    "zh": """查询分类（query classification）包含意图预测、类目预测等多个子任务，对电商应用至关重要。电商查询通常很短、缺乏上下文，且标签之间的信息无法被利用，导致建模时先验信息不足。现有工业界查询分类方法大多依赖用户的后验点击行为来构造训练样本，从而形成马太效应式的恶性循环。此外，查询分类的各子任务缺乏统一框架，导致算法优化效率低下。本文提出一种新颖的半监督可扩展统一框架 SSUF（Semi-supervised Scalable Unified Framework），通过多个增强模块来统一各类查询分类任务。其中，知识增强模块利用世界知识增强查询表示，解决查询信息不足的问题；标签增强模块利用标签语义和半监督信号，降低对后验标签的依赖；结构增强模块基于复杂的标签关系增强标签表示。各模块高度可插拔，可根据各子任务的需要灵活增删输入特征。我们进行了大量离线和在线 A/B 实验，结果表明 SSUF 显著优于当前最优模型。"""
})

# 2. Agent-Ops
FILES.append({
    "filename": "Agent-Ops - A Multi-Agent Orchestration Framework for End-to-End SOP Automation in E-Commerce Operations.md",
    "title": "Agent-Ops: A Multi-Agent Orchestration Framework for End-to-End SOP Automation in E-Commerce Operations",
    "source": "Agent-Ops - A Multi-Agent Orchestration Framework for End-to-End SOP Automation in E-Commerce Operations.pdf",
    "en": """While Large Language Models excel at reasoning and language understanding, they struggle with multi-step operational workflows requiring precise procedural adherence, which is fundamental for industrial automation. Existing SOP-guided agents assume well-defined procedures and structured APIs, failing to address enterprise realities like incomplete SOPs, dynamic web interfaces, and unpredictable document formats. We present Agent-Ops, an end-to-end multi-agent framework automating Standard Operating Procedures in e-commerce. Agent-Ops contributes: (1) SOP Groomer, a human-AI framework transforming ambiguous documentation into automation-ready specifications, (2) WebAgent, achieving 91.3% task completion and 86.5% execution consistency through demonstration-based learning, and (3) a Document Verification Agent performing multi-lingual validation across tax invoices, certificates, and supply chain documents with 94.2% accuracy. Deployed across seven SOP categories in three geographic regions, Agent-Ops achieves 85-97% end-to-end accuracy while reducing case resolution time by 83%. Use across 100 Account Managers validates that LLM-based agents achieve enterprise-grade reliability when augmented with robust web automation, comprehensive document understanding, and systematic SOP refinement.""",
    "zh": """大语言模型（LLM）虽然在推理和语言理解上表现出色，但在需要严格遵循流程的多步运营工作流中却力不从心，而这正是工业自动化的基础。现有的 SOP 引导型 Agent 通常假设流程定义清晰、API 结构化，无法应对企业现实中的 SOP 不完整、Web 界面动态变化、文档格式不可预测等问题。我们提出 Agent-Ops，一个用于电商标准作业程序（SOP）端到端自动化的多智能体框架。Agent-Ops 的贡献包括：（1）SOP Groomer，一个人机协同框架，将模糊的文档转化为可用于自动化的规范；（2）WebAgent，通过基于示范的学习（demonstration-based learning）实现 91.3% 的任务完成率和 86.5% 的执行一致性；（3）文档核验智能体，对税务发票、证照和供应链文档进行多语言校验，准确率达 94.2%。Agent-Ops 在三个地区的七类 SOP 上部署后，端到端准确率达到 85%–97%，工单解决时间缩短 83%。在 100 名客户经理中的使用表明，当 LLM 智能体辅以稳健的 Web 自动化、全面的文档理解和系统化的 SOP 打磨后，可以达到企业级可靠性。"""
})

# 3. AIGuard
FILES.append({
    "filename": "AIGuard - A Benchmark and Lightweight Detection for E-commerce AIGC Risks.md",
    "title": "AIGuard: A Benchmark and Lightweight Detection for E-commerce AIGC Risks",
    "source": "AIGuard - A Benchmark and Lightweight Detection for E-commerce AIGC Risks.pdf",
    "en": """Recent advancements in AI-generated content (AIGC) have heightened concerns about harmful outputs, such as misinformation and malicious misuse. Existing detection methods face two key limitations: (1) lacking real-world AIGC scenarios and corresponding risk datasets, and (2) both traditional and multimodal large language models (MLLMs) struggle to detect risks in AIGC. Towards this end, we introduce AIGUARD, the first benchmark for AIGC risk detection in real-world e-commerce. It includes 253,420 image-text pairs (i.e., the risk content and risk description) across four critical categories: abnormal body, violating physical laws, misleading or illogical context, and harmful or problematic message. To effectively detect these risks, we propose distilling text annotations into dense soft prompts and identifying risk content through image soft prompt matching during inference. Experiments on the benchmark show that this method achieves a 9.68% higher recall than leading multimodal models while using only 25% of the training resources and improving inference speed by 37.8 times. For further research, our benchmark and code are available at https://github.com/wenh-zhang/aiguard-dataset.""",
    "zh": """AI 生成内容（AIGC）的最新进展引发了人们对虚假信息、恶意滥用等有害输出的担忧。现有检测方法存在两个关键局限：（1）缺乏真实世界的 AIGC 场景及对应的风险数据集；（2）传统方法和多模态大语言模型（MLLM）都难以检测 AIGC 中的风险。为此，我们提出 AIGUARD，这是首个面向真实电商场景的 AIGC 风险检测基准。它包含 253,420 个图文对（即风险内容与风险描述），覆盖四大关键类别：异常身体画面、违反物理规律、误导或不合逻辑的上下文、以及有害或有问题的信息。为有效检测这些风险，我们提出将文本标注蒸馏为稠密软提示（soft prompt），并在推理时通过图像软提示匹配来识别风险内容。在该基准上的实验表明，相比主流多模态模型，本方法召回率提升 9.68%，训练资源仅需 25%，推理速度提升 37.8 倍。基准与代码已开源：https://github.com/wenh-zhang/aiguard-dataset 。"""
})

# 4. Aligning AI Research
FILES.append({
    "filename": "Aligning AI Research with the Needs of Clinical Coding Workflows - Eight Recommendations Based on US Data Analysis and Critical Review.md",
    "title": "Aligning AI Research with the Needs of Clinical Coding Workflows: Eight Recommendations Based on US Data Analysis and Critical Review",
    "source": "Aligning AI Research with the Needs of Clinical Coding Workflows - Eight Recommendations Based on US Data Analysis and Critical Review.pdf",
    "en": """Clinical coding is crucial for healthcare billing and data analysis. Manual clinical coding is labour-intensive and error-prone, which has motivated research towards full automation of the process. However, our analysis, based on US English electronic health records and automated coding research using these records, shows that widely used evaluation methods are not aligned with real clinical contexts. For example, evaluations that focus on the top 50 most common codes are an oversimplification, as there are thousands of codes used in practice. This position paper aims to align AI coding research more closely with practical challenges of clinical coding. Based on our analysis, we offer eight specific recommendations, suggesting ways to improve current evaluation methods. Additionally, we propose new AI-based methods beyond automated coding, suggesting alternative approaches to assist clinical coders in their workflows.""",
    "zh": """临床编码（clinical coding）对医疗计费和数据分析至关重要。人工临床编码劳动密集且容易出错，这促使学界研究该流程的完全自动化。然而，我们基于美国英语电子健康档案（EHR）以及利用这些档案开展的自动编码研究进行分析后发现：目前广泛采用的评估方法与真实临床场景并不对齐。例如，只聚焦前 50 个最常用编码的评估是一种过度简化，因为实际工作中使用的编码多达数千个。本立场论文旨在让 AI 编码研究更贴近临床编码的实际挑战。基于分析，我们给出八条具体建议，提出改进当前评估方法的思路；此外，我们还提出超越"自动编码"本身的新型 AI 方法，建议用替代性手段辅助临床编码员的日常工作流程。"""
})

# 5. AutoPKG
FILES.append({
    "filename": "AutoPKG - An Automated Framework for Dynamic E-commerce Product-Attribute Knowledge Graph Construction.md",
    "title": "AutoPKG: An Automated Framework for Dynamic E-commerce Product-Attribute Knowledge Graph Construction",
    "source": "AutoPKG - An Automated Framework for Dynamic E-commerce Product-Attribute Knowledge Graph Construction.pdf",
    "en": """Product attribute extraction in e-commerce is bottlenecked by ontologies that are inconsistent, incomplete, and costly to maintain. We present AutoPKG, a multi-agent Large Language Model (LLM) framework that automatically constructs a Product-attribute Knowledge Graph (PKG) from multimodal product content. AutoPKG induces product types and type-specific attribute keys on demand, extracts attribute values from text and images, and consolidates updates through a centralized decision agent that maintains a globally consistent canonical graph. We also propose an evaluation protocol for dynamic PKGs that measures type/key validity and consolidation quality, as well as edge-level accuracy for value assertions after canonicalization. On a large real-world marketplace catalog dataset from Lazada (Alibaba), AutoPKG achieves up to 0.953 Weighted Knowledge Efficiency (WKE) for product types, 0.724 WKE for attribute keys, and 0.531 edge-level F1 for multimodal value extraction. Across three public benchmarks, we improve edge-level exact-match F1 by 0.152 and yield a 0.208 precision gain on the attribute extraction application. Online A/B tests show that AutoPKG-derived attributes increase Gross Merchandise Value (GMV) in Badge (+3.81%), Search (+5.32%), and Recommendation (+7.89%), supporting AutoPKG's practical value in production.""",
    "zh": """电商中的产品属性抽取长期受困于不一致、不完整且维护成本高昂的本体（ontology）。我们提出 AutoPKG，一个由多智能体大语言模型（LLM）组成的框架，可从多模态商品内容中自动构建产品-属性知识图谱（PKG）。AutoPKG 能够按需归纳产品类型与类型相关的属性键（attribute key），从文本和图片中抽取属性值，并通过一个中心化决策智能体整合更新，维护全局一致的规范化图谱。我们还提出了一套面向动态 PKG 的评估协议，用于度量类型/键的有效性、整合质量，以及规范化之后取值断言的边级准确率。在 Lazada（阿里巴巴）的大规模真实商城目录数据集上，AutoPKG 在产品类型上取得最高 0.953 的加权知识效率（WKE），属性键上 0.724，多模态取值抽取的边级 F1 达 0.531。在三个公开基准上，边级精确匹配 F1 提升 0.152，属性抽取应用的精确率提升 0.208。在线 A/B 实验表明，AutoPKG 产出的属性在商品标签（Badge）、搜索和推荐场景下分别提升 GMV +3.81%、+5.32% 和 +7.89%，验证了其在生产环境中的实用价值。"""
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
