# BLaIR: 桥接语言与物品——评测 LLM 作为推荐语义编码器

**原标题**: Bridging Language and Items for Retrieval and Recommendation: Benchmarking LLMs as Semantic Encoders

**作者**: Yupeng Hou, Jiacheng Li, Xiangjun Fu 等

**单位**: UC San Diego (UCSD); UCLA

## 摘要

特征工程长期以来一直是推荐系统的核心，但有效利用文本物品特征仍然充满挑战。大语言模型（LLMs）的最新进展使其能够作为推荐场景中的语义编码器，但它们在这一环境中的角色和行为尚未被充分理解。此前的研究在选择 LLM 时通常依赖通用嵌入基准（如 MTEB），忽视了推荐任务的独特特性。为解决这一差距，我们引入 BLaIR，一个全面评测 LLM 作为推荐场景语义编码器的基准。我们贡献了：(1) 一个新的大规模 Amazon Reviews 2023 数据集，包含超过 5.7 亿条评论和 4800 万个物品；(2) 一个统一的评测基准，覆盖序列推荐、协同过滤和商品搜索；(3) 一个新的复杂查询商品搜索任务，包含半合成和真实世界评测数据集。对 11 个主流 LLM 的实验表明，它们在 BLaIR 上的排名与 MTEB 几乎无相关性，揭示了推荐场景中语义编码的独特挑战。
