# Grounded Multimodal In-Context Learning for Product Weight Estimation at Scale in E-commerce
> 来源文件：Grounded Multimodal In-Context Learning for Product Weight Estimation at Scale in E-commerce.pdf
> 发表年份：2026
> 单位：Anthology 未著录

## 英文原文摘要（Original Abstract）

Accurately inferring implicit physical attributes of products, such as weight, is critical for large-scale e-commerce logistics but challenging due to sparse or unreliable textual metadata and high visual variability. We formulate weight estimation as a grounded multimodal reasoning problem and investigate whether large vision-language models (LVLMs) can infer discretized weight buckets through in-context learning (ICL) over product images and descriptions. We introduce a scalable inference framework that conditions predictions on automatically retrieved, category-specific exemplars and propose a distribution-calibrated retrieval strategy that aligns few-shot contexts with the empirical weight distribution of each product subcategory. Offline evaluations shows that across 14 high-variance product categories, our approach significantly outperforms strong multimodal KNN baselines in both exact-match accuracy and near-bucket reliability. Deployed in production on a large e-commerce platform, our system processes millions of listings daily and reduces shipping-related revenue leakage by ~22%, demonstrating that multimodal ICL can serve as a practical and cost-effective alternative to manual or hardware-based verification.

## 中文翻译（Chinese Translation）

准确推断商品的隐式物理属性（如重量）对大规模电商物流至关重要，但由于文本元数据稀疏或不可靠、视觉外观差异大而极具挑战。我们将重量估计建模为一个有依据的多模态推理问题，探究大型视觉语言模型（LVLM）能否通过对商品图片和描述进行上下文学习（ICL）来推断离散化的重量区间。我们提出一个可扩展的推理框架，将预测建立在自动检索到的、特定类别的样例之上，并设计一种分布校准的检索策略，使少样本上下文与每个商品子类别的经验重量分布对齐。离线评估表明，在 14 个高方差商品类目上，本方法在精确匹配准确率和近区间可靠性上均显著优于强多模态 KNN 基线。该系统已在某大型电商平台生产环境部署，每日处理数百万条商品，并将物流相关的收入损失降低约 22%，证明多模态 ICL 可作为人工或硬件校验的一种实用且高性价比的替代方案。
