> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名：** `relagent-arxiv-2605.07840.pdf`

**原文标题：** RELAGENT: LLM Agents as Data Scientists for Relational Learning

**作者：** Xingyue Huang（Oxford；研究大部分在 AITHYRA 做博前工作）、Louis Tichelman（TU Wien、AITHYRA）、Jinwoo Kim（KAIST）、Krzysztof Olejniczak（Oxford）、İsmail İlkan Ceylan（TU Wien、AITHYRA、Oxford）

**场合：** PDF 首页印有 40th Conference on Neural Information Processing Systems (NeurIPS 2026)。arXiv:2605.07840v2，2026-10-21

## 摘要（Abstract）

关系学习已有图模型（GNN、graph transformer）、表格方法（含表格基础模型）和序列方法（LLM），各有短板。RELAGENT 把 LLM 当成自主的数据分析师，分两段。搜索阶段：agent 用数据库、验证和 evaluation workspace 三类工具，写出 SQL 特征程序并选定预测模型。推理阶段：只执行选中的程序，不再调用 LLM。最终预测器是 SQL 查询加一个经典模型。特征是人能读的查询，预测只依赖这些查询定义的特征，因此可以用普通数据库部署，并且快、确定、可解释。

## 1 Introduction

实务里，关系库上的预测靠分析师写 SQL：沿外键路径 join，在时间窗口上聚合，做出次数、新近性和活动趋势，再交给下游模型。特征空间大，试错依赖领域经验，schema 一复杂就难扩展。

现有自动化被分成三类，并指向表 1。表格模型吃扁平特征矩阵，用到关系库上要么大量特征工程，要么用可能对不上任务的通用聚合。GNN、graph transformer 和关系基础模型吃由库诱导出的图，但邻域大小和聚合深度事先定死，不一定适合下游任务。把表或图序列化后交给 LLM，接口灵活，但归纳偏置和结构化预测不对齐。作者的互补方向是：关系结构留在库外、保持可执行，自动化的是「找哪些查询对任务有用」。

搜索阶段的三个接口是：探索查询（只读地看库）、特征查询（构成特征程序）、评估查询（查看 evaluation workspace 里的历史试验）。agent 迭代提出特征程序，挑选下游模型（例子是 XGBoost、LightGBM），再按反馈改程序和模型。推理阶段把选中的程序跑在目标实体上，特征送给在训练样本上拟合好的预测器。

假设类由可执行查询参数化，而不是由固定网络结构参数化。可解释性来自：能追溯到哪些查询、物化出的特征值、以及下游模型怎么用这些特征。归纳偏置也改了说法：两条样本只要在选中的 SQL 特征上输出相同，预测就相同；不变性来自查询，不来自固定的图编码、序列顺序或网络结构。

贡献五条：把关系学习写成对查询特征和预测模型的自主搜索；用验证反馈和 evaluation workspace 做有执行依据的改进循环；搜索和推理分开，部署时不需要 LLM；用查询定义的特征映射表述关系学习；在关系基准上与强基线竞争，同时保留可解释性和可扩展性。第 1 节没有给出具体分数。

## 2 Related Work

**Relational deep learning。** 传统流程是手工做成任务专用的特征表，再上 XGBoost、LightGBM 或 AutoGluon，换 schema 或换预测目标就要重做。RDL 把库当成带时间的异构图（行是节点，主键–外键是边，training table 是目标），对应 RelGNN、RelGT，以及 Griffin、Relational Transformers、KumoRFM 的两个版本这类关系基础模型。另一路是表格或语言基础模型：GNN 加 TabPFN-2.5、RDBLearn，以及把库序列化进上下文的 LLM 预测器。RDL 也被放进图和知识图谱基础模型的更大背景里，但专门处理带 schema 和时间预测目标的关系库。

**LLMs for structured data。** 把表和 schema 串成文本，可以做表格预测和 text-to-SQL；按行序列化做少样本表格学习时，对提示和表示很敏感。图也有同样问题：格式和邻域选择一变就脆。后续有 graph prompting、指令微调和 graph tokenization。工具使用（ReAct、Toolformer、Plan-and-Execute、Reflexion，以及面向图的工具调用或可执行程序）让模型通过显式操作接触结构。RELAGENT 与「把表或邻域塞进上下文」的差别是：库留在外面，只通过 SQL 访问。

**LLMs as feature engineers。** 单表上，CAAFE 和 FeatLLM 用 LLM 合成特征或规则，推理时不再用 LLM。LLM-FE 把特征构造当成由验证反馈引导的程序搜索；OCTree 用决策树推理去改单条规则。多关系库上，ReFuGe 是固定顺序的流水线，用聚合后的验证反馈，下游模型也固定。RELAGENT 改成三个查询接口，并能对 SQL 特征和下游模型一起搜索；部署出去的预测器仍然只由查询和经典模型组成。
