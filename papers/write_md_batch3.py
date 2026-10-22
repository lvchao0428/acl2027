#!/usr/bin/env python3
"""Write bilingual markdown files - batch 3."""
import os

OUT_DIR = "/Users/a58/project/paper/acl2027/papers/abstracts-翻译/3-关键词撞车"

FILES = []

# 12. LLM-Enhanced Self-Evolving RL for Payment Fraud
FILES.append({
    "filename": "LLM-Enhanced Self-Evolving Reinforcement Learning for Multi-Step E-Commerce Payment Fraud Risk Detection.md",
    "title": "LLM-Enhanced Self-Evolving Reinforcement Learning for Multi-Step E-Commerce Payment Fraud Risk Detection",
    "source": "LLM-Enhanced Self-Evolving Reinforcement Learning for Multi-Step E-Commerce Payment Fraud Risk Detection.pdf",
    "en": """This paper presents a novel approach to e-commerce payment fraud detection by integrating reinforcement learning (RL) with Large Language Models (LLMs). By framing transaction risk as a multi-step Markov Decision Process (MDP), RL optimizes risk detection across multiple payment stages. Crafting effective reward functions, essential for RL model success, typically requires significant human expertise due to the complexity and variability in design. LLMs, with their advanced reasoning and coding capabilities, are well-suited to refine these functions, offering improvements over traditional methods. Our approach leverages LLMs to iteratively enhance reward functions, achieving better fraud detection accuracy and demonstrating zero-shot capability. Experiments with real-world data confirm the effectiveness, robustness, and resilience of our LLM-enhanced RL framework through long-term evaluations, underscoring the potential of LLMs in advancing industrial RL applications.""",
    "zh": """本文提出一种将强化学习（RL）与大语言模型（LLM）相结合的电商支付欺诈检测新方法。通过将交易风险建模为多步马尔可夫决策过程（MDP），RL 可在多个支付阶段上优化风险检测效果。设计有效的奖励函数是 RL 模型成功的关键，但由于奖励设计复杂多变，通常需要大量人工专家经验。LLM 凭借其强大的推理与代码能力，非常适合用于优化这些奖励函数，可带来优于传统方法的效果。本方法利用 LLM 迭代地改进奖励函数，在欺诈检测准确率上取得更好效果，并展现出零样本能力。基于真实数据的长期实验验证了我们 LLM 增强的 RL 框架的有效性、鲁棒性与韧性，凸显了 LLM 在推进工业级 RL 应用方面的潜力。"""
})

# 13. MICE
FILES.append({
    "filename": "MICE - Mixture of Image Captioning Experts Augmented e-Commerce Product Attribute Value Extraction.md",
    "title": "MICE: Mixture of Image Captioning Experts Augmented e-Commerce Product Attribute Value Extraction",
    "source": "MICE - Mixture of Image Captioning Experts Augmented e-Commerce Product Attribute Value Extraction.pdf",
    "en": """Attribute value extraction plays a crucial role in enhancing e-commerce search, filtering, and recommendation systems. However, prior visual attribute value extraction methods typically rely on both product images and textual information such as product descriptions and titles. In practice, text can be ambiguous, inaccurate, or unavailable, which can degrade model performance. We propose Mixture of Image Captioning Experts (MICE), a novel augmentation framework for product attribute value extraction. MICE leverages a curated pool of image captioning models to generate accurate captions from product images, resulting in robust attribute extraction solely from an image. Extensive experiments on the public ImplicitAVE dataset and a proprietary women's tops dataset demonstrate that MICE significantly improves the performance of state-of-the-art large multimodal models (LMMs) in both zero-shot and fine-tuning settings. An ablation study validates the contribution of each component in the framework. MICE's modular design offers scalability and adaptability, making it well-suited for diverse industrial applications with varying computational and latency requirements.""",
    "zh": """属性值抽取对提升电商搜索、筛选和推荐系统至关重要。然而，以往的视觉属性值抽取方法通常同时依赖商品图片和文本信息（如商品描述和标题）。在实际业务中，文本可能存在歧义、不准确甚至缺失，从而降低模型性能。我们提出 Mixture of Image Captioning Experts（MICE），一个新颖的商品属性值抽取增强框架。MICE 利用一组经过精心挑选的图像描述模型池，从商品图片中生成准确的图像描述，从而仅依靠图片即可实现稳健的属性抽取。在公开数据集 ImplicitAVE 和内部女装上衣数据集上的大量实验表明，无论在零样本还是微调设置下，MICE 都显著提升了当前最优大 multimodal 模型（LMM）的性能。消融实验验证了框架中各组件的贡献。MICE 的模块化设计具有良好的可扩展性和适应性，适用于不同算力与时延要求的多样化工业场景。"""
})

# 14. MIRA
FILES.append({
    "filename": "MIRA - Empowering One-Touch AI Services on Smartphones with MLLM-based Instruction Recommendation.md",
    "title": "MIRA: Empowering One-Touch AI Services on Smartphones with MLLM-based Instruction Recommendation",
    "source": "MIRA - Empowering One-Touch AI Services on Smartphones with MLLM-based Instruction Recommendation.pdf",
    "en": """The rapid advancement of generative AI technologies is driving the integration of diverse AI-powered services into smartphones, transforming how users interact with their devices. To simplify access to predefined AI services, this paper introduces MIRA, a pioneering framework for task instruction recommendation that enables intuitive one-touch AI tasking on smartphones. With MIRA, users can long-press on images or text objects to receive contextually relevant instruction recommendations for executing AI tasks. Our work introduces three key innovations: 1) A multimodal large language model (MLLM)-based recommendation pipeline with structured reasoning to extract key entities, infer user intent, and generate precise instructions; 2) A template-augmented reasoning mechanism that integrates high-level reasoning templates, enhancing task inference accuracy; 3) A prefix-tree-based constrained decoding strategy that restricts outputs to predefined instruction candidates, ensuring coherent and intent-aligned suggestions. Through evaluation using a real-world annotated dataset and a user study, MIRA has demonstrated substantial improvements in the accuracy of instruction recommendation. The encouraging results highlight MIRA's potential to revolutionize the way users engage with AI services on their smartphones, offering a more seamless and efficient experience.""",
    "zh": """生成式 AI 技术的快速发展正推动各类 AI 服务集成到智能手机中，改变着用户与设备的交互方式。为简化用户对预定义 AI 服务的调用，本文提出 MIRA，这是一个开创性的任务指令推荐框架，可在手机上实现直观的一键式 AI 任务调用。借助 MIRA，用户长按图片或文本对象，即可获得与上下文相关的指令推荐，用于执行相应的 AI 任务。本文的主要创新包括：1）基于多模态大语言模型（MLLM）的推荐流水线，通过结构化推理抽取关键实体、推断用户意图并生成精准指令；2）模板增强的推理机制，融合高层推理模板，提升任务推断准确率；3）基于前缀树的约束解码策略，将输出限制在预定义指令候选集中，保证推荐建议连贯且与意图对齐。基于真实标注数据集的评测和用户研究表明，MIRA 在指令推荐准确率上取得了显著提升。令人鼓舞的结果显示，MIRA 有潜力革新用户在手机上使用 AI 服务的方式，带来更无缝、高效的体验。"""
})

# 15. MTIVE
FILES.append({
    "filename": "MTIVE - Multi-Task Image Verification Engine Using Vision-Language Models for E-commerce.md",
    "title": "MTIVE: Multi-Task Image Verification Engine Using Vision-Language Models for E-commerce",
    "source": "MTIVE - Multi-Task Image Verification Engine Using Vision-Language Models for E-commerce.pdf",
    "en": """Vision-language models show promise for e-commerce automation but struggle with noisy real-world images and multi-task requirements. We introduce MTIVE, a curriculum learning framework that progressively adapts base models through three stages: continued pre-training on large-scale e-commerce datasets with contrastive learning and diverse dialogue templates, instruction tuning on synthetic data, and modular task-specific expert training. Our architecture uses frozen base weights with stacked LoRA adapters—shared modules for domain knowledge and lightweight task-specific experts—enabling continual learning without catastrophic forgetting. MTIVE outperforms open-source and proprietary baselines in both standard and continual learning settings.""",
    "zh": """视觉语言模型在电商自动化中展现出潜力，但在真实世界的噪声图片和多任务要求下表现不佳。我们提出 MTIVE，一个课程学习框架，通过三个阶段渐进式地适配基座模型：第一阶段在大规模电商数据集上进行持续预训练，融合对比学习与多样化对话模板；第二阶段在合成数据上进行指令微调；第三阶段进行模块化的任务专家训练。架构上采用冻结基座权重 + 堆叠 LoRA 适配器（LoRA adapter）的方式——共享模块承载领域知识，轻量任务专家负责具体任务——从而在持续学习过程中避免灾难性遗忘。在标准设置和持续学习设置下，MTIVE 均优于开源与商业基线。"""
})

# 16. Open-World Attribute Mining (MSIT)
FILES.append({
    "filename": "Open-World Attribute Mining for E-Commerce Products with Multimodal Self-Correction Instruction Tuning.md",
    "title": "Open-World Attribute Mining for E-Commerce Products with Multimodal Self-Correction Instruction Tuning",
    "source": "Open-World Attribute Mining for E-Commerce Products with Multimodal Self-Correction Instruction Tuning.pdf",
    "en": """In e-commerce, effective product Attribute Mining (AM) is essential for enhancing product features and aiding consumer decisions. However, current AM methods often focus on extracting attributes from unimodal text, underutilizing multimodal data. In this paper, we propose a novel framework called Multimodal Self-Correction Instruction Tuning (MSIT) to mine new potential attributes from images and texts with Multimodal Large Language Models (MLLMs). The tuning process involves two datasets: Attribute Generation Tuning Data (AGTD) and Chain-of-Thought Tuning Data (CTTD). AGTD is constructed utilizing in-context learning with a small set of seed attributes, aiding the MLLMs in accurately extracting attribute-value pairs from multimodal information. To introduce explicit reasoning and improve the extraction accuracy, we construct CTTD, which incorporates a structured 5-step reasoning process for self-correction. Finally, we employ a 3-stage inference process to filter out redundant attributes and sequentially validate each generated attribute. Comprehensive experimental results on two datasets show that MSIT outperforms state-of-the-art methods. We will release our code and data in the near future.""",
    "zh": """在电商中，有效的产品属性挖掘（Attribute Mining, AM）对于丰富商品特征、辅助消费者决策至关重要。然而，当前 AM 方法大多仅从单模态文本中抽取属性，未充分利用多模态数据。本文提出一个新框架：多模态自纠错指令微调（Multimodal Self-Correction Instruction Tuning, MSIT），借助多模态大语言模型（MLLM）从图片和文本中挖掘新的潜在属性。微调过程涉及两个数据集：属性生成微调数据（AGTD）和思维链微调数据（CTTD）。AGTD 通过小批量种子属性利用上下文学习（ICL）构建，帮助 MLLM 从多模态信息中准确抽取属性-值对。为引入显式推理、提升抽取准确率，我们构建了 CTTD，其中包含结构化的 5 步推理过程用于自我纠错。最后，我们采用三阶段推理流程过滤冗余属性，并对每个生成的属性依次进行校验。在两个数据集上的综合实验表明，MSIT 优于当前最优方法。代码与数据将于近期开源。"""
})

# 17. Progressive Fine-Tuning
FILES.append({
    "filename": "Progressive Fine-Tuning for Cost-Effective Structured Attribute Generation in E-commerce.md",
    "title": "Progressive Fine-Tuning for Cost-Effective Structured Attribute Generation in E-commerce",
    "source": "Progressive Fine-Tuning for Cost-Effective Structured Attribute Generation in E-commerce.pdf",
    "en": """Large language models (LLMs) excel at structured information generation but face cost and latency challenges when deployed at scale in user-facing products. We present a parameter-efficient supervised fine-tuning pipeline for adapting a small language model (SLM) to structured attribute generation in e-commerce product listing, enabling continuous model improvement with implicit user feedback without expensive manual annotation. Our approach involves completeness-deficit guided curation, which ranks samples by divergence between model predictions and catalog listing attributes, selecting the highest completeness gap examples for progressive fine-tuning. Our system is deployed on a large-scale product listing service, reducing inference costs by 98% and p90 latency by 70% using a fine-tuned SLM relative to the baseline LLM while preserving an 86.4% user acceptance rate, translating to significant monthly infrastructure savings.""",
    "zh": """大语言模型（LLM）擅长结构化信息生成，但在面向用户的产品中大规模部署时面临成本和时延挑战。我们提出一个参数高效的有监督微调流水线，用于将小语言模型（SLM）适配到电商商品标题中的结构化属性生成任务，能够借助隐式用户反馈持续改进模型，而无需昂贵的人工标注。该方法包含"完整度赤字引导的数据筛选"（completeness-deficit guided curation）：按模型预测与目录列表属性之间的差异度对样本排序，挑选完整度缺口最大的样本用于渐进式微调。我们的系统已部署在大规模商品发布服务上，使用微调后的 SLM 相比基线 LLM 将推理成本降低 98%、p90 时延降低 70%，同时保持 86.4% 的用户接受率，每月带来可观的基础设施成本节约。"""
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
