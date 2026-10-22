# Open-World Attribute Mining for E-Commerce Products with Multimodal Self-Correction Instruction Tuning
> 来源文件：Open-World Attribute Mining for E-Commerce Products with Multimodal Self-Correction Instruction Tuning.pdf

## 英文原文摘要（Original Abstract）

In e-commerce, effective product Attribute Mining (AM) is essential for enhancing product features and aiding consumer decisions. However, current AM methods often focus on extracting attributes from unimodal text, underutilizing multimodal data. In this paper, we propose a novel framework called Multimodal Self-Correction Instruction Tuning (MSIT) to mine new potential attributes from images and texts with Multimodal Large Language Models (MLLMs). The tuning process involves two datasets: Attribute Generation Tuning Data (AGTD) and Chain-of-Thought Tuning Data (CTTD). AGTD is constructed utilizing in-context learning with a small set of seed attributes, aiding the MLLMs in accurately extracting attribute-value pairs from multimodal information. To introduce explicit reasoning and improve the extraction accuracy, we construct CTTD, which incorporates a structured 5-step reasoning process for self-correction. Finally, we employ a 3-stage inference process to filter out redundant attributes and sequentially validate each generated attribute. Comprehensive experimental results on two datasets show that MSIT outperforms state-of-the-art methods. We will release our code and data in the near future.

## 中文翻译（Chinese Translation）

在电商中，有效的产品属性挖掘（Attribute Mining, AM）对于丰富商品特征、辅助消费者决策至关重要。然而，当前 AM 方法大多仅从单模态文本中抽取属性，未充分利用多模态数据。本文提出一个新框架：多模态自纠错指令微调（Multimodal Self-Correction Instruction Tuning, MSIT），借助多模态大语言模型（MLLM）从图片和文本中挖掘新的潜在属性。微调过程涉及两个数据集：属性生成微调数据（AGTD）和思维链微调数据（CTTD）。AGTD 通过小批量种子属性利用上下文学习（ICL）构建，帮助 MLLM 从多模态信息中准确抽取属性-值对。为引入显式推理、提升抽取准确率，我们构建了 CTTD，其中包含结构化的 5 步推理过程用于自我纠错。最后，我们采用三阶段推理流程过滤冗余属性，并对每个生成的属性依次进行校验。在两个数据集上的综合实验表明，MSIT 优于当前最优方法。代码与数据将于近期开源。
