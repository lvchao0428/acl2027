# 将 LLM 推理蒸馏进稠密编码器：弥合推荐中的精度-效率鸿沟
> 来源文件：Distilling LLM Reasoning into Dense Encoders - Bridging the Accuracy-Efficiency Gap in Recommendation.pdf
> 发表年份：2026
> 单位：Korea Advanced Institute of Science & Technology；Korea Advanced Institute of Science and Technology
## 英文原文摘要（Original Abstract）
Large Language Models (LLMs) have shown remarkable potential in recommendation sys-tems but suffer from prohibitive inference la-tency. Existing distillation approaches typically target Small Language Models (SLMs) or Con-ventional Recommendation Models (CRMs), yet face a critical trade-off between compu-tational cost and semantic reasoning capac-ity. To bridge this accuracy-efficiency gap, we introduce Reasoning-to-Encoder Distilla-tion (R2END), a framework that establishes a text encoder as the optimal student architecture for scalable recommendation. Unlike meth-ods that mimic token generation, R2END com-presses the teacher’s reasoning into a dense vector space via a semantic alignment objec-tive, effectively capturing user-item dynamics. Extensive experiments on four datasets demon-strate that R2END not only outperforms state-of-the-art baselines but also achieves drastically reduced latency, offering a sweet spot for rec-ommendation.
## 中文翻译（Chinese Translation）
大语言模型（LLM）在推荐系统中展现出显著潜力，但推理延迟高昂。现有蒸馏方法通常以小语言模型（SLM）或传统推荐模型（CRM）为目标，却在计算成本与语义推理能力之间面临关键权衡。为弥合这一“精度-效率”鸿沟，我们提出 R2END（推理到编码器蒸馏）框架，确立文本编码器作为可规模化推荐的最优学生架构。与模仿 token 生成的方法不同，R2END 通过一个语义对齐目标，将教师模型的推理压缩进稠密向量空间，有效捕捉用户-商品动态。在四个数据集上的大量实验表明，R2END 不仅优于当前最优基线，还大幅降低延迟，为推荐提供了精度与效率的“甜点区”。
