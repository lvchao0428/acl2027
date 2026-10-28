# MTIVE: Multi-Task Image Verification Engine Using Vision-Language Models for E-commerce
> 来源文件：MTIVE - Multi-Task Image Verification Engine Using Vision-Language Models for E-commerce.pdf
> 发表年份：2026
> 单位：Anthology 未著录

## 英文原文摘要（Original Abstract）

Vision-language models show promise for e-commerce automation but struggle with noisy real-world images and multi-task requirements. We introduce MTIVE, a curriculum learning framework that progressively adapts base models through three stages: continued pre-training on large-scale e-commerce datasets with contrastive learning and diverse dialogue templates, instruction tuning on synthetic data, and modular task-specific expert training. Our architecture uses frozen base weights with stacked LoRA adapters—shared modules for domain knowledge and lightweight task-specific experts—enabling continual learning without catastrophic forgetting. MTIVE outperforms open-source and proprietary baselines in both standard and continual learning settings.

## 中文翻译（Chinese Translation）

视觉语言模型在电商自动化中展现出潜力，但在真实世界的噪声图片和多任务要求下表现不佳。我们提出 MTIVE，一个课程学习框架，通过三个阶段渐进式地适配基座模型：第一阶段在大规模电商数据集上进行持续预训练，融合对比学习与多样化对话模板；第二阶段在合成数据上进行指令微调；第三阶段进行模块化的任务专家训练。架构上采用冻结基座权重 + 堆叠 LoRA 适配器（LoRA adapter）的方式——共享模块承载领域知识，轻量任务专家负责具体任务——从而在持续学习过程中避免灾难性遗忘。在标准设置和持续学习设置下，MTIVE 均优于开源与商业基线。
