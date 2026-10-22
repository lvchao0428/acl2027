# ClusterRAG: Cluster-Based Collaborative Filtering for Personalized

> 来源文件：16_ClusterRAG.pdf

## 英文原文摘要（Original Abstract）

Personalized Retrieval-Augmented Generation (RAG) relies on accurately selecting user-relevant documents. In practice, existing RAG approaches often suffer from high retrieval costs and overlook that collaborative signals from similar users can enhance personalized generation for the current user. We propose ClusterRAG, a Cluster-Based Collaborative Filtering for Personalized Retrieval-Augmented Generation. ClusterRAG represents users through their profile documents, organizes users into semantically coherent clusters using density-based clustering, and performs retrieval at both the cluster and document levels via cluster-level similarity and fine-grained ranking. Extensive experiments on the LaMP benchmark demonstrate that jointly leveraging the target user's profile and profiles from top similar users consistently yields the best performance across diverse tasks. Further analysis shows that ClusterRAG integrates seamlessly with different dense retrievers and rankers, and remains effective when paired with both fine-tuned and zero-shot language models.

## 中文翻译（Chinese Translation）

个性化检索增强生成（Personalized RAG）依赖于准确选择与用户相关的文档。在实践中，现有 RAG 方法往往检索成本高昂，且忽略了相似用户的协同信号能提升对当前用户的个性化生成。我们提出 ClusterRAG，一种面向个性化检索增强生成的、基于聚类的协同过滤方法。ClusterRAG 以用户的画像文档表示用户，通过基于密度的聚类将用户组织成语义连贯的簇，并在簇级与文档级同时进行检索：先通过簇级相似度，再经细粒度排序。在 LaMP 基准上的大量实验表明，联合利用目标用户的画像与最相似用户的画像，在多类任务上一致取得最佳性能。进一步分析显示，ClusterRAG 能与不同稠密检索器、排序器无缝集成，且无论与微调语言模型还是零样本语言模型搭配都保持有效。
