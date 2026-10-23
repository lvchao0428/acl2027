# Multimodal Item Scoring for Natural Language Recommendation via Gaussian Process Regression with LLM Relevance Judgments
> 来源文件：Multimodal Item Scoring for Natural Language Recommendation via Gaussian Process Regression with LLM Relevance Judgments.pdf
> 发表年份：2026
> 单位：Department of Computer Science, University of Toronto；University of Toronto；Department of Mechanical and Industrial Engineering, University of Toronto and Department of Computer Science

## 英文原文摘要（Original Abstract）

Natural Language Recommendation (NLRec) generates item suggestions based on the relevance between user-issued NL requests and NL item description passages. Existing NLRec approaches often use Dense Retrieval (DR) to compute item relevance scores from aggregation of inner products between user request embeddings and relevant passage embeddings. However, DR views the request as the sole relevance signal, resulting in a unimodal scoring function centered on the request embedding, which is often a weak proxy for true relevance. To better capture the multiple relevance modes that may arise in complex NLRec data, we propose GPR-LLM, which uses Gaussian Process Regression (GPR) to estimate the underlying relevance function from multiple LLMjudged anchor passages instead of treating the request as the sole relevance signal. Experiments on four NLRec datasets and three LLM backbones demonstrate that GPR-LLM consistently outperforms baseline methods including DR, cross-encoder, and pointwise LLM-based relevance scoring by up to 65%.

## 中文翻译（Chinese Translation）

自然语言推荐（Natural Language Recommendation, NLRec）基于用户发出的自然语言请求与自然语言商品描述段落之间的相关性，生成商品建议。现有 NLRec 方法常使用稠密检索（Dense Retrieval, DR），通过对用户请求嵌入与相关段落嵌入的内积进行聚合来计算商品相关性分数。然而，DR 把请求视为唯一的相关性信号，导致以请求嵌入为中心的单模态打分函数，而这常是真实相关性的弱代理。为更好地捕获复杂 NLRec 数据中可能出现的多种相关性模式，我们提出 GPR-LLM：它使用高斯过程回归（Gaussian Process Regression, GPR），从多个由 LLM 判定的锚点段落出发估计底层相关性函数，而不是把请求当作唯一相关性信号。在四个 NLRec 数据集与三个 LLM 骨干上的实验表明，GPR-LLM 一致优于包括 DR、cross-encoder 以及 pointwise LLM 相关性打分在内的基线方法，提升最高达 65%。
