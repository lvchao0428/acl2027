# Bridging Language and Items for Retrieval and Recommendation:

> 来源文件：02_BLaIR.pdf
> 发表年份：2026
> 单位：University of California, San Diego；Facebook；University of Pennsylvania, University of Pennsylvania；Google DeepMind；SalesForce；University of Illinois at Urbana-Champaign；University of California, San Diego, University of California, San Diego

## 英文原文摘要（Original Abstract）

Feature engineering has long been central to recommender systems, yet effectively leveraging textual item features remains challenging. Recent advances in large language models (LLMs) have enabled their use as semantic encoders for recommendation, but their roles and behaviors in this setting are still not well understood. Prior studies often rely on general-purpose embedding benchmarks (e.g., MTEB) when selecting LLMs, overlooking the unique characteristics of recommendation tasks. To address this gap, we introduce BLAIR, a comprehensive benchmark for evaluating LLMs as semantic encoders in recommendation scenarios. We contribute (1) a new large-scale Amazon Reviews 2023 dataset with over 570 million reviews and 48 million items, (2) a unified benchmark covering sequential recommendation, collaborative filtering, and product search, and (3) a new complex-query product search task featuring both semi-synthetic and real-world evaluation datasets. Experiments with 11 leading LLMs show that their rankings on BLAIR show little correlation with MTEB, highlighting the unique challenges of semantic encoding in recommendation.

## 中文翻译（Chinese Translation）

特征工程长期以来一直是推荐系统的核心，但有效利用物品的文本特征仍颇具挑战。大语言模型（LLM）的最新进展使其能够作为语义编码器用于推荐，然而它们在该场景下的作用与行为尚未被充分理解。以往研究在选择 LLM 时通常依赖通用嵌入基准（如 MTEB），而忽略了推荐任务的独特性。为填补这一空白，我们提出了 BLaIR——一个用于评估 LLM 在推荐场景中作为语义编码器的综合基准。我们的贡献包括：（1）一个全新的大规模 Amazon Reviews 2023 数据集，包含超过 5.7 亿条评论和 4800 万个物品；（2）一个覆盖序列推荐、协同过滤和商品搜索的统一基准；（3）一个新的复杂查询商品搜索任务，同时包含半合成和真实世界的评测数据集。我们在 11 个主流 LLM 上的实验表明，这些模型在 BLaIR 上的排名与在 MTEB 上的排名几乎不相关，凸显了推荐场景下语义编码的独特挑战。
