# ClusterRAG: 基于聚类的协同过滤实现个性化检索增强生成

**原标题**: ClusterRAG: Cluster-Based Collaborative Filtering for Personalized Retrieval-Augmented Generation

**作者**: Gibson Nkhata, Uttamasha Anjally Oyshi, Quan Mai, Susan Gauch

**单位**: University of Arkansas; Walmart Inc.

## 摘要

个性化检索增强生成（RAG）依赖于准确选择与用户相关的文档。在实践中，现有的 RAG 方法常常面临高检索成本的问题，并忽视了来自相似用户的协作信号可以增强当前用户个性化生成的事实。我们提出 **ClusterRAG**，一种基于聚类的协同过滤个性化检索增强生成方法。ClusterRAG 通过用户的画像文档来表示用户，使用基于密度的聚类方法将用户组织为语义连贯的簇，并在簇级和文档级通过簇级相似度和细粒度排序进行检索。在 LaMP 基准上的大量实验表明，联合利用目标用户的画像和来自最相似用户的画像在多样化任务中持续取得最佳性能。进一步分析显示，ClusterRAG 可以与不同的稠密检索器和排序器无缝集成，并在配合微调和零样本语言模型时均保持有效。
