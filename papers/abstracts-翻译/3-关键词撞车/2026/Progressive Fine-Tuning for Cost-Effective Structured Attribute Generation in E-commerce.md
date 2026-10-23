# Progressive Fine-Tuning for Cost-Effective Structured Attribute Generation in E-commerce
> 来源文件：Progressive Fine-Tuning for Cost-Effective Structured Attribute Generation in E-commerce.pdf
> 发表年份：2026
> 单位：Anthology 未著录

## 英文原文摘要（Original Abstract）

Large language models (LLMs) excel at structured information generation but face cost and latency challenges when deployed at scale in user-facing products. We present a parameter-efficient supervised fine-tuning pipeline for adapting a small language model (SLM) to structured attribute generation in e-commerce product listing, enabling continuous model improvement with implicit user feedback without expensive manual annotation. Our approach involves completeness-deficit guided curation, which ranks samples by divergence between model predictions and catalog listing attributes, selecting the highest completeness gap examples for progressive fine-tuning. Our system is deployed on a large-scale product listing service, reducing inference costs by 98% and p90 latency by 70% using a fine-tuned SLM relative to the baseline LLM while preserving an 86.4% user acceptance rate, translating to significant monthly infrastructure savings.

## 中文翻译（Chinese Translation）

大语言模型（LLM）擅长结构化信息生成，但在面向用户的产品中大规模部署时面临成本和时延挑战。我们提出一个参数高效的有监督微调流水线，用于将小语言模型（SLM）适配到电商商品标题中的结构化属性生成任务，能够借助隐式用户反馈持续改进模型，而无需昂贵的人工标注。该方法包含"完整度赤字引导的数据筛选"（completeness-deficit guided curation）：按模型预测与目录列表属性之间的差异度对样本排序，挑选完整度缺口最大的样本用于渐进式微调。我们的系统已部署在大规模商品发布服务上，使用微调后的 SLM 相比基线 LLM 将推理成本降低 98%、p90 时延降低 70%，同时保持 86.4% 的用户接受率，每月带来可观的基础设施成本节约。
