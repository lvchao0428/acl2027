# Stronger, Lighter, Better: Towards Life-Long Attribute Value Extraction for E-Commerce Products
> 来源文件：Stronger, Lighter, Better - Towards Life-Long Attribute Value Extraction for E-Commerce Products.pdf
> 发表年份：2024
> 单位：Amazon；University of California, San Diego；University of Illinois, Chicago

## 英文原文摘要（Original Abstract）

Attribute value extraction involves identifying the value spans of predetermined attributes in product texts. This area of research has traditionally operated under a closed-world assumption, focusing on products from a static set of categories and their associated attributes. However, products in e-commerce stores are ever-increasing and evolving, calling for life-long learning. If continuously trained on the fast-increasing products and attributes, most existing solutions not only struggle for parameter efficiency but also endure foreseeable defects due to data contamination, catastrophic forgetting, etc. As a remedy, we propose and study a new task, which aims to effectively maintain a strong single model for many domains in a life-long learning fashion, without jeopardizing the model performance and parameter efficiency. We introduce factorization into the model and make it domain-aware by decoupling the modeling of product type and attribute, as a way to promote de-contamination and parameter efficiency while scaling up. Tuning the model with distillation prevents forgetting historical knowledge and enables continuous learning from emerging domains. Experiments on hundreds of domains show that our model attains near state-of-the-art performance with affordable parameter size, the least historical knowledge forgetting, and the greatest robustness against noises, whilst adding only a few parameters per domain when compared with competitive baselines.

## 中文翻译（Chinese Translation）

属性值抽取（attribute value extraction）是指从商品文本中识别预定义属性对应的值片段。该研究方向传统上一直基于闭世界假设，聚焦于一组静态类目及其关联属性上的商品。然而，电商店铺中的商品不断增长和演变，要求系统具备终身学习（life-long learning）能力。若在快速增长的商品和属性上持续训练，现有大多数方案不仅在参数效率上捉襟见肘，还会因数据污染、灾难性遗忘等问题出现可预见的缺陷。作为对策，我们提出并研究一个新任务：以终身学习的方式，为众多领域有效地维护一个强大的单一模型，同时不损害模型性能与参数效率。我们在模型中引入因子分解（factorization），通过解耦商品类型与属性的建模来使其具备领域感知能力，从而在扩展规模的同时促进去污染和参数效率。使用蒸馏（distillation）来微调模型，可防止历史知识遗忘，并支持从新兴领域持续学习。在数百个领域上的实验表明，我们的模型以可接受的参数量达到接近当前最优的性能，历史知识遗忘最少，对噪声的鲁棒性最强，且相比有竞争力的基线，每个新领域仅需新增少量参数。
