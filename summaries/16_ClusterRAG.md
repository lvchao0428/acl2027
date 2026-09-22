# ClusterRAG: Cluster-Based Collaborative Filtering for Personalized Retrieval-Augmented Generation

| 项目 | 内容 |
|------|------|
| **Paper** | ClusterRAG: Cluster-Based Collaborative Filtering for Personalized Retrieval-Augmented Generation |
| **Authors** | Gibson Nkhata, Uttamasha Anjally Oyshi, Quan Mai, Susan Gauch |
| **Affiliation** | University of Arkansas; Walmart Inc. |
| **Theme** | 个性化 RAG / 协同过滤 / 用户聚类 |
| **Problem** | 现有个性化 RAG 方法检索成本高，且忽略了来自相似用户的协作信号可以增强个性化生成 |
| **Method** | ClusterRAG：通过用户画像文档表示用户，使用 HDBSCAN 密度聚类组织为语义连贯的用户簇，在簇级和文档级进行层次化检索。支持三种模式：User-only、Collaborative-only、Hybrid |
| **Benchmark** | LaMP benchmark（多个个性化任务） |
| **Result** | Hybrid 模式一致最优；检索器无关（兼容 ColBERTv2、BGE、BM25）；对微调和 zero-shot LLM 均有效 |
| **Question** | 用户簇的动态更新策略？新用户冷启动时如何快速归入合适的簇？ |

## 详细笔记

### 研究背景与动机

个性化 RAG 依赖于准确选择用户相关的文档来增强 LLM 生成。现有方法面临两个问题：检索成本高（在大规模用户文档库中搜索），以及忽略了协作信号（相似用户的文档可以补充当前用户的信息）。

### 核心方法详解

**用户表示**：每个用户通过其历史文档（profile documents）进行表示。

**HDBSCAN 聚类**：使用密度聚类算法将用户组织为语义连贯的簇，不需要预设簇数量，自适应发现用户群体结构。

**层次化检索**：先在簇级别找到最相似的 top-k 用户，再在这些用户的文档中进行细粒度排序。

**三种模式**：User-only（仅用目标用户文档）、Collaborative-only（仅用相似用户文档）、Hybrid（两者结合）。实验表明 Hybrid 模式一致最优。

### 实验设置与结果

- **数据集**：LaMP benchmark 多个个性化任务
- **关键结果**：Hybrid 模式一致最优；兼容多种检索器；对微调和 zero-shot LLM 均有效；计算开销低

### 个人思考

ClusterRAG 将传统协同过滤思想引入 RAG 个性化，简单有效。HDBSCAN 不需要预设簇数这一特性很适合真实场景中用户规模动态变化的情况。与 PURPLE 的区别在于：PURPLE 优化单个用户的 profile 构建，ClusterRAG 利用群体信息补充个体信息，两者可互补。
