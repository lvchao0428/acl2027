# MICE: Mixture of Image Captioning Experts Augmented e-Commerce Product Attribute Value Extraction
> 来源文件：MICE - Mixture of Image Captioning Experts Augmented e-Commerce Product Attribute Value Extraction.pdf

## 英文原文摘要（Original Abstract）

Attribute value extraction plays a crucial role in enhancing e-commerce search, filtering, and recommendation systems. However, prior visual attribute value extraction methods typically rely on both product images and textual information such as product descriptions and titles. In practice, text can be ambiguous, inaccurate, or unavailable, which can degrade model performance. We propose Mixture of Image Captioning Experts (MICE), a novel augmentation framework for product attribute value extraction. MICE leverages a curated pool of image captioning models to generate accurate captions from product images, resulting in robust attribute extraction solely from an image. Extensive experiments on the public ImplicitAVE dataset and a proprietary women's tops dataset demonstrate that MICE significantly improves the performance of state-of-the-art large multimodal models (LMMs) in both zero-shot and fine-tuning settings. An ablation study validates the contribution of each component in the framework. MICE's modular design offers scalability and adaptability, making it well-suited for diverse industrial applications with varying computational and latency requirements.

## 中文翻译（Chinese Translation）

属性值抽取对提升电商搜索、筛选和推荐系统至关重要。然而，以往的视觉属性值抽取方法通常同时依赖商品图片和文本信息（如商品描述和标题）。在实际业务中，文本可能存在歧义、不准确甚至缺失，从而降低模型性能。我们提出 Mixture of Image Captioning Experts（MICE），一个新颖的商品属性值抽取增强框架。MICE 利用一组经过精心挑选的图像描述模型池，从商品图片中生成准确的图像描述，从而仅依靠图片即可实现稳健的属性抽取。在公开数据集 ImplicitAVE 和内部女装上衣数据集上的大量实验表明，无论在零样本还是微调设置下，MICE 都显著提升了当前最优的大模型（LMM）的性能。消融实验验证了框架中各组件的贡献。MICE 的模块化设计具有良好的可扩展性和适应性，适用于不同算力与时延要求的多样化工业场景。
