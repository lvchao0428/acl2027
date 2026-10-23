# Chinese Live-Streaming E-Commerce Morph Resolution: Datasets and Methods
> 来源文件：Chinese Live-Streaming E-Commerce Morph Resolution - Datasets and Methods.pdf
> 发表年份：2026
> 单位：Yangzhou University

## 英文原文摘要（Original Abstract）

Live-stream E-commerce faces significant challenges from morphs, deliberate linguistic variants used to evade real-time voice filters and amplify product claims illegally. While critical for regulatory enforcement, Live Auditory Morph Resolution (LiveAMR) research is hindered by limited datasets: prior work relied on narrow, redundant health domain corpora, restricting model robustness. To bridge this gap, we introduce two datasets: (1) HealthAMR, a refined health-domain corpus via deduplication and re-annotation; (2) GeneralAMR, a general domain benchmark with 28K annotated sentences from 77 channels across 7 E-commerce categories. Further, we propose JointMRE, a multi-task framework that jointly resolves morphs and generates structured explanations, transferring grammatical insights from large language models to enhance generalization. Predictions are refined by our Conflict-aware Dual-output Refinement Framework (CDRF), which detects inconsistencies between corrections and explanations. Experiments show CDRF significantly improves morph resolution accuracy and interpretability. Our datasets and code are available.

## 中文翻译（Chinese Translation）

直播电商面临"谐音变体"（morph）带来的严峻挑战——这是商家刻意使用的语言变体，用以绕过实时语音过滤、违规夸大商品宣传。直播听觉谐音变体消解（Live Auditory Morph Resolution, LiveAMR）研究对监管执法至关重要，却受限于数据集匮乏：已有工作依赖范围狭窄、冗余严重的健康领域语料，限制了模型鲁棒性。为弥补这一缺口，本文发布两个数据集：（1）HealthAMR，经去重与重新标注后的精炼健康领域语料；（2）GeneralAMR，覆盖 7 个电商类目、77 个频道、28K 标注句子的通用领域基准。进一步，我们提出 JointMRE，一个多任务框架，联合完成谐音变体消解与结构化解释生成，并将大语言模型中的语法知识迁移过来以增强泛化能力。预测结果再由我们提出的冲突感知双输出精炼框架（CDRF）进一步打磨，该框架可检测修正结果与解释之间的不一致。实验表明 CDRF 显著提升了谐音变体消解的准确率与可解释性。数据集与代码已开源。
