#!/usr/bin/env python3
"""Write bilingual markdown files - batch 2."""
import os

OUT_DIR = "/Users/a58/project/paper/acl2027/papers/abstracts-翻译/3-关键词撞车"

FILES = []

# 6. Chinese Live-Streaming E-Commerce Morph Resolution
FILES.append({
    "filename": "Chinese Live-Streaming E-Commerce Morph Resolution - Datasets and Methods.md",
    "title": "Chinese Live-Streaming E-Commerce Morph Resolution: Datasets and Methods",
    "source": "Chinese Live-Streaming E-Commerce Morph Resolution - Datasets and Methods.pdf",
    "en": """Live-stream E-commerce faces significant challenges from morphs, deliberate linguistic variants used to evade real-time voice filters and amplify product claims illegally. While critical for regulatory enforcement, Live Auditory Morph Resolution (LiveAMR) research is hindered by limited datasets: prior work relied on narrow, redundant health domain corpora, restricting model robustness. To bridge this gap, we introduce two datasets: (1) HealthAMR, a refined health-domain corpus via deduplication and re-annotation; (2) GeneralAMR, a general domain benchmark with 28K annotated sentences from 77 channels across 7 E-commerce categories. Further, we propose JointMRE, a multi-task framework that jointly resolves morphs and generates structured explanations, transferring grammatical insights from large language models to enhance generalization. Predictions are refined by our Conflict-aware Dual-output Refinement Framework (CDRF), which detects inconsistencies between corrections and explanations. Experiments show CDRF significantly improves morph resolution accuracy and interpretability. Our datasets and code are available.""",
    "zh": """直播电商面临"谐音变体"（morph）带来的严峻挑战——这是商家刻意使用的语言变体，用以绕过实时语音过滤、违规夸大商品宣传。直播听觉谐音变体消解（Live Auditory Morph Resolution, LiveAMR）研究对监管执法至关重要，却受限于数据集匮乏：已有工作依赖范围狭窄、冗余严重的健康领域语料，限制了模型鲁棒性。为弥补这一缺口，本文发布两个数据集：（1）HealthAMR，经去重与重新标注后的精炼健康领域语料；（2）GeneralAMR，覆盖 7 个电商类目、77 个频道、28K 标注句子的通用领域基准。进一步，我们提出 JointMRE，一个多任务框架，联合完成谐音变体消解与结构化解释生成，并将大语言模型中的语法知识迁移过来以增强泛化能力。预测结果再由我们提出的冲突感知双输出精炼框架（CDRF）进一步打磨，该框架可检测修正结果与解释之间的不一致。实验表明 CDRF 显著提升了谐音变体消解的准确率与可解释性。数据集与代码已开源。"""
})

# 7. ConECT
FILES.append({
    "filename": "ConECT Dataset - Overcoming Data Scarcity in Context-Aware E-Commerce MT.md",
    "title": "ConECT Dataset: Overcoming Data Scarcity in Context-Aware E-Commerce MT",
    "source": "ConECT Dataset - Overcoming Data Scarcity in Context-Aware E-Commerce MT.pdf",
    "en": """Neural Machine Translation (NMT) has improved translation by using Transformer-based models, but it still struggles with word ambiguity and context. This problem is especially important in domain-specific applications, which often have problems with unclear sentences or poor data quality. Our research explores how adding information to models can improve translations in the context of e-commerce data. To this end we create ConECT – a new Czech-to-Polish e-commerce product translation dataset coupled with images and product metadata consisting of 11,400 sentence pairs. We then investigate and compare different methods that are applicable to context-aware translation. We test a vision-language model (VLM), finding that visual context aids translation quality. Additionally, we explore the incorporation of contextual information into text-to-text models, such as the product's category path or image descriptions. The results of our study demonstrate that the incorporation of contextual information leads to an improvement in the quality of machine translation. We make the new dataset publicly available.""",
    "zh": """神经机器翻译（NMT）借助 Transformer 模型取得了显著进步，但仍难以处理词义歧义与上下文依赖问题。这一问题在特定领域应用中尤为突出——这类场景常伴有句子含义不清或数据质量欠佳的问题。本文研究如何向模型引入额外信息，以改善电商数据场景下的翻译质量。为此，我们构建了 ConECT——一个新的捷克语到波兰语的电商商品翻译数据集，附带图片和商品元数据，包含 11,400 个句对。随后我们调研并比较了多种适用于上下文感知翻译的方法。我们测试了视觉语言模型（VLM），发现视觉上下文有助于提升翻译质量。此外，我们还探索在文本到文本模型中引入上下文信息，例如商品类目路径或图片描述。研究结果表明，引入上下文信息能够提升机器翻译质量。我们已将该数据集公开。"""
})

# 8. DiaLLMs
FILES.append({
    "filename": "DiaLLMs - EHR-Enhanced Clinical Conversational System for Clinical Test Recommendation and Diagnosis Prediction.md",
    "title": "DiaLLMs: EHR-Enhanced Clinical Conversational System for Clinical Test Recommendation and Diagnosis Prediction",
    "source": "DiaLLMs - EHR-Enhanced Clinical Conversational System for Clinical Test Recommendation and Diagnosis Prediction.pdf",
    "en": """Recent advances in Large Language Models (LLMs) have led to remarkable progresses in medical consultation. However, existing medical LLMs overlook the essential role of Electronic Health Records (EHR) and focus primarily on diagnosis recommendation, limiting their clinical applicability. We propose DiaLLM, the first medical LLM that integrates heterogeneous EHR data into clinically grounded dialogues, enabling clinical test recommendation, result interpretation, and diagnosis prediction to better align with real-world medical practice. To construct clinically grounded dialogues from EHR, we design a Clinical Test Reference (CTR) strategy that maps each clinical code to its corresponding description and classifies test results as "normal" or "abnormal". Additionally, DiaLLM employs a reinforcement learning framework for evidence acquisition and automated diagnosis. To handle the large action space, we introduce a reject sampling strategy to reduce redundancy and improve exploration efficiency. Furthermore, a confirmation reward and a class-sensitive diagnosis reward are designed to guide accurate diagnosis prediction. Extensive experimental results demonstrate that DiaLLM outperforms baselines in clinical test recommendation and diagnosis prediction. Our code is available at Github.""",
    "zh": """大语言模型（LLM）的最新进展在医疗问诊领域取得了显著成效。然而，现有医疗 LLM 忽视了电子健康档案（EHR）的关键作用，且主要聚焦诊断推荐，限制了其临床适用性。我们提出 DiaLLM，这是首个将异构 EHR 数据融入临床对话的医疗 LLM，能够在对话中完成临床检查推荐、结果解读和诊断预测，使其更贴近真实医疗实践。为从 EHR 构建有临床依据的对话，我们设计了临床检查参考（Clinical Test Reference, CTR）策略，将每个临床编码映射到对应描述，并把检查结果划分为"正常"或"异常"。此外，DiaLLM 采用强化学习框架进行证据收集与自动诊断。为应对巨大的动作空间，我们引入拒绝采样策略以减少冗余、提升探索效率；进一步设计了确认奖励和类别敏感的诊断奖励，以引导模型做出准确的诊断预测。大量实验表明，DiaLLM 在临床检查推荐和诊断预测任务上均优于基线。代码已在 Github 开源。"""
})

# 9. Domain Adaptation of Foundation LLMs for e-Commerce
FILES.append({
    "filename": "Domain Adaptation of Foundation LLMs for e-Commerce.md",
    "title": "Domain Adaptation of Foundation LLMs for e-Commerce",
    "source": "Domain Adaptation of Foundation LLMs for e-Commerce.pdf",
    "en": """We present the e-Llama models: 8 billion and 70 billion parameter large language models that are adapted towards the e-commerce domain. These models are meant as foundation models with deep knowledge about e-commerce, that form a base for instruction- and fine-tuning. The e-Llama models are obtained by continuously pretraining the Llama 3.1 base models on 1 trillion tokens of domain-specific data. We discuss our approach and motivate our choice of hyperparameters with a series of ablation studies. To quantify how well the models have been adapted to the e-commerce domain, we define and implement a set of multilingual, e-commerce specific evaluation tasks. We show that, when carefully choosing the training setup, the Llama 3.1 models can be adapted towards the new domain without sacrificing significant performance on general domain tasks. We also explore the possibility of merging the adapted model and the base model for a better control of the performance trade-off between domains.""",
    "zh": """我们发布 e-Llama 模型：分别为 80 亿和 700 亿参数、面向电商领域适配的大语言模型。这些模型作为具备深厚电商知识的基础模型，可作为后续指令微调和精调的底座。e-Llama 模型通过在 1 万亿 token 的领域专属数据上对 Llama 3.1 基座模型进行持续预训练得到。我们讨论了方法设计，并通过一系列消融实验说明超参数选择的依据。为量化模型对电商领域的适配程度，我们定义并实现了一组多语种、电商专属的评测任务。结果表明，在精心设计训练配置的前提下，Llama 3.1 模型可以较好地适配新领域，而不会在通用领域任务上损失显著性能。我们还探索了将领域适配后模型与基座模型进行模型合并（model merging）的可能性，以便更好地权衡不同领域之间的性能折中。"""
})

# 10. E-ABSA20K
FILES.append({
    "filename": "E-ABSA20K - A Dataset and Propose-and-Verify for Aspect-Based Sentiment Analysis in Long E-commerce Reviews.md",
    "title": "E-ABSA20K: A Dataset and Propose-and-Verify for Aspect-Based Sentiment Analysis in Long E-commerce Reviews",
    "source": "E-ABSA20K - A Dataset and Propose-and-Verify for Aspect-Based Sentiment Analysis in Long E-commerce Reviews.pdf",
    "en": """Aspect-Based Sentiment Analysis (ABSA) is critical for extracting actionable product insights from e-commerce reviews. However, most public ABSA benchmarks are restricted to short texts and a limited range of domains, and therefore underrepresent the challenges posed by real-world reviews—where multiple aspects co-occur, colloquial and noisy expressions are common, and evidence must often be aggregated across sentences in long contexts. We introduce E-ABSA20K, a multi-domain dataset of 20K reviews from four product categories (WomenBags, Dresses, Cosmetics, and Furniture), annotated with review-level sentiment quads. Compared to existing benchmarks, E-ABSA20K contains substantially longer and more aspect-dense reviews, averaging 63.9 words and 6.0 quads per review. We further propose a two-stage propose-and-verify framework for review-level quad extraction (target, aspect, opinion, sentiment). The first stage generates high-recall candidates under strict schema constraints, while the second stage conducts explicit grounding, scope, and modality verification, followed by review-level consolidation to mitigate hallucinations and scope leakage in long reviews. Experiments across multiple Qwen3 model sizes demonstrate that our approach consistently outperforms single-stage prompting (with and without chain-of-thought) as well as competitive ABSA extraction baselines, improving quad-level micro-F1 (µF) and robustness on discourse-hard cases such as comparisons and conditionals. The dataset was collected from a major English-language e-commerce platform in Southeast Asia; while reviews are predominantly written in English, a small fraction (approximately 0.8%) contains code-mixed tokens, reflecting realistic multilingual user-generated content.""",
    "zh":"""方面级情感分析（ABSA）对于从电商评论中提取可落地的产品洞察至关重要。然而，现有公开 ABSA 基准大多局限于短文本和有限领域，无法充分反映真实评论中的挑战：多方面共现、口语化和噪声表达常见，且证据往往需要在长上下文中跨句聚合。我们发布 E-ABSA20K，一个多领域数据集，包含来自四个品类（女包、女装、化妆品、家具）的 20K 条评论，标注到评论级的情感四元组。与现有基准相比，E-ABSA20K 的评论显著更长、方面更密集，平均每条评论 63.9 个词、6.0 个四元组。我们进一步提出一个两阶段"提出-验证"（propose-and-verify）框架，用于评论级四元组抽取（目标、方面、观点、情感）。第一阶段在严格 schema 约束下生成高召回候选；第二阶段进行显式的证据定位、范围和情态验证，并在评论层面做整合，以缓解长评论中的幻觉与范围泄漏问题。在多个 Qwen3 模型规模上的实验表明，本方法始终优于单阶段提示（无论是否使用思维链）以及有竞争力的 ABSA 抽取基线，提升了四元组级 micro-F1（µF），并在比较句、条件句等语篇困难样本上更鲁棒。数据集采集自东南亚一家主流英语电商平台；评论以英语为主，少量（约 0.8%）包含语码混用 token，反映了真实多语种用户生成内容。"""
})

# 11. Grounded Multimodal ICL
FILES.append({
    "filename": "Grounded Multimodal In-Context Learning for Product Weight Estimation at Scale in E-commerce.md",
    "title": "Grounded Multimodal In-Context Learning for Product Weight Estimation at Scale in E-commerce",
    "source": "Grounded Multimodal In-Context Learning for Product Weight Estimation at Scale in E-commerce.pdf",
    "en": """Accurately inferring implicit physical attributes of products, such as weight, is critical for large-scale e-commerce logistics but challenging due to sparse or unreliable textual metadata and high visual variability. We formulate weight estimation as a grounded multimodal reasoning problem and investigate whether large vision-language models (LVLMs) can infer discretized weight buckets through in-context learning (ICL) over product images and descriptions. We introduce a scalable inference framework that conditions predictions on automatically retrieved, category-specific exemplars and propose a distribution-calibrated retrieval strategy that aligns few-shot contexts with the empirical weight distribution of each product subcategory. Offline evaluations shows that across 14 high-variance product categories, our approach significantly outperforms strong multimodal KNN baselines in both exact-match accuracy and near-bucket reliability. Deployed in production on a large e-commerce platform, our system processes millions of listings daily and reduces shipping-related revenue leakage by ~22%, demonstrating that multimodal ICL can serve as a practical and cost-effective alternative to manual or hardware-based verification.""",
    "zh": """准确推断商品的隐式物理属性（如重量）对大规模电商物流至关重要，但由于文本元数据稀疏或不可靠、视觉外观差异大而极具挑战。我们将重量估计建模为一个有依据的多模态推理问题，探究大型视觉语言模型（LVLM）能否通过对商品图片和描述进行上下文学习（ICL）来推断离散化的重量区间。我们提出一个可扩展的推理框架，将预测建立在自动检索到的、特定类别的样例之上，并设计一种分布校准的检索策略，使少样本上下文与每个商品子类别的经验重量分布对齐。离线评估表明，在 14 个高方差商品类目上，本方法在精确匹配准确率和近区间可靠性上均显著优于强多模态 KNN 基线。该系统已在某大型电商平台生产环境部署，每日处理数百万条商品，并将物流相关的收入损失降低约 22%，证明多模态 ICL 可作为人工或硬件校验的一种实用且高性价比的替代方案。"""
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
