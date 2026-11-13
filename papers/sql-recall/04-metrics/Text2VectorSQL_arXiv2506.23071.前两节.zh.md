> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

- 原文件名：Text2VectorSQL_arXiv2506.23071.pdf
- 原文标题：Text2VectorSQL: Towards a Unified Interface for Vector Search and SQL Queries
- 作者：Zhengren Wang、Bozhou Li、Dongsheng Ma、Bo Li、Bin Cui（Peking University）；Dongwen Yao（Shanghai Jiao Tong University）；Linpeng Tang（OriginHub Technology，并与 Institute for Advanced Algorithms Research, Shanghai 相关联）；Zhiyu Li、Feiyu Xiong（Institute for Advanced Algorithms Research, Shanghai）；Wentao Zhang（Peking University、OriginHub Technology、Zhongguancun Academy）。通讯作者为 Zhiyu Li 与 Wentao Zhang
- 场合：arXiv:2506.23071v2 [cs.CL]，2025 年 11 月 6 日

## 摘要

非结构化数据让传统数据库接口不够用。Text-to-SQL 打开了结构化数据，但处理不了语义查询和多模态查询。向量检索已成为查非结构化数据的事实标准；它和 SQL 的结合被称作 VectorSQL，却仍靠手工写查询，也没有统一评测，潜力用不上。作者把 Text2VectorSQL 定义成新任务：用自然语言同时查结构化和非结构化数据。

配套的基础设施工件有三块。一是可扩展的高质量 Text-to-VectorSQL 训练数据合成流水线。二是 VectorSQLBench，号称该任务第一个大规模、多面向评测，覆盖 12 种组合：后端是 SQLite、PostgreSQL、ClickHouse，数据源是 BIRD、Spider、arXiv、Wikipedia。三是若干更细的评价指标。实验一方面给出训练模型的强基线，一方面指出 recall degradation：SQL 过滤和向量检索合在一起时，正确结果被漏掉的程度可以比常规 filtered vector search 更严重。仓库在 https://github.com/OpenDCAI/Text2VectorSQL 。

## I. INTRODUCTION

第 1 节把问题写成两种数据世界的分裂。关系数据库靠 SQL 的精确逻辑；非结构化数据据估计占企业数据的 90% 以上 [1]，越来越用语义向量检索来查。用户因此要在分析接口和语义检索接口之间来回切换。Text-to-SQL 把自然语言翻成结构化查询，但看不见文本、图像等非结构化内容里的语义，答不了 “Find scientific papers discussing learned index structures published after 2020” 这种混合问题。把向量检索嵌进关系数据库的 VectorSQL [2], [3] 被认为能补上这个缺口，可查询仍要手写，同时懂向量检索和 SQL，而且把自然语言译成 VectorSQL 的学术工作被说成完全空白。

作者把实现困难收成三条：没有公开的自然语言–VectorSQL 配对数据，无法训练或微调；没有评测和指标，研究难以复现；翻译和执行里准确率与效率互相牵制，向量检索和 SQL 过滤交织时会出现不明显的召回失败。对应的生态是：合成流水线解决数据稀缺；VectorSQLBench 填评测空白，同样是上述 12 种后端与数据源组合，并配上 rank-based score、decomposed accuracy 等指标，而不只看执行准确率。Fig. 1 用 “Learned Indexes”、2020 年之后的论文检索说明统一查询：SQL 侧有 `year > 2020` 这类过滤，向量侧按 embedding 距离排序；图中还把全表扫描标成 O(N)、HNSW 标成 O(log N)，并列出 semantic filtering、multimodal matching 和 retrieval acceleration。

实验结论被提前放在引言里。训练出的模型被称作达到当时最优，但分析发现 post-filtering——先做向量检索、再用 SQL 谓词过滤——会比传统 filtered vector search 更严重地漏掉正确结果。带 JOIN 的复杂查询里，post-filtering 可以悄悄丢掉超过 30% 的正确结果。于是 Text2VectorSQL 不只是翻译问题，还和查询优化、执行策略缠在一起。贡献对应三条：首次形式化该任务；给出合成流水线和 VectorSQLBench；用多数据集、多数据库实验建立强基线，并把 recall degradation 标成后续要共同优化生成与执行的方向。

## II. PRELIMINARIES

第 2 节只铺定义，不展开后文的数据合成。它先定义向量检索，再定义 VectorSQL 和 Text-to-VectorSQL。

Definition 2.2 把向量检索写成：非结构化集合 D 经嵌入模型 E 映到 d 维向量；查询文本 Q_txt 得到查询向量，相似度可以是余弦或点积；要找大小为 k 的子集，使查询与各项嵌入的相似度之和最大。大规模时用 Approximate Nearest Neighbor，以换对数时间。实际里还常加上 filtered vector search：结果既要语义相近，也要满足过滤谓词。

Definition 2.3 把一条 VectorSQL 查询 Q_VSQL 拆成两部分。SQL 谓词分量 Q_S 约束结构化列，例如 WHERE 和 JOIN。向量分量 Q_V 是二元组 (查询向量, k)。过滤型向量检索作为 VectorSQL 的简化形式，有两种配合方式。Pre-filtering（Filter-then-Search）先执行 Q_S 得到精确子集 D′，再只在 D′ 上做 ANN，取 top-k。结果一定满足结构化条件，但可能破坏已建好的 ANN 索引假设，退化为对 D′ 的暴力扫描。Post-filtering（Search-then-Filter）先用 ANN 取出候选，k′ 可以大于最终的 k，再套 SQL 谓词。文中把 SQL 过滤看作硬约束、语义相似度看作软约束：pre-filtering 保真，post-filtering 更快，但可能因为召回下降而凑不齐正确结果。Definition 2.4 据此定义任务：给定带向量列的混合 schema S_hybrid 和自然语言问题 Q_NL，学习映射 f_T2VSQL，使 Q_VSQL = f_T2VSQL(Q_NL, S_hybrid)。
