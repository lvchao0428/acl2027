> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名：** `refuge-arxiv-2601.17735.pdf`

**原文标题：** ReFuGe: Feature Generation for Prediction Tasks on Relational Databases with LLM Agents

**作者：** Kyungho Kim、Geon Lee、Juyeon Kim、Dongwon Choi、Shinhwan Kang、Kijung Shin（KAIST）

**场合：** WWW ’26，2026-04-13 至 17，迪拜。ACM 参考信息写明 4 页。arXiv:2601.17735v1，2026-01-25。代码：https://github.com/K-Kyungho/REFUGE

## 摘要（Abstract）

关系数据库不只有检索，预测任务也开始被关注。作者的做法不是换一个端到端模型，而是生成能提高预测的关系特征。难点是：要在复杂 schema 上推理，特征组合空间很大，又没有显式监督。ReFuGe 用三类专门的 LLM agent：schema selection 选出与任务相关的表和列；feature generation 从选中的 schema 产生多样候选特征；feature filtering 用推理和验证两道过滤留下有用的特征。整个过程放在迭代反馈里，直到性能收敛。摘要只说在 RDB 基准上各类预测任务有明显提升，没有给总表数字。

## 1 Introduction & Related Works

这一节把引言和相关工作写在一起。关系库上的研究长期偏检索（写出能取出相关信息的查询）。预测（例如分类）是后扩出来的：利用表之间的结构提高下游效果。实用路线是把散落在相关表里的信号做成特征，例如购买统计、近期交易次数、关联账户属性，再交给普通表格模型。

自动化被收成三个障碍。（C1）要从关系结构里抽出预测信号。（C2）表的变换和组合方式太多，特征空间极大。（C3）没有标准答案可监督，和 text-to-SQL 那种有金标准查询的检索任务不同。

对应设计：schema selection agent 处理（C1）；多个 feature generation agent 靠领域知识和关系上下文产生候选，再经 reasoning-based 和 validation-based 过滤，处理（C2）；没有金标准时用迭代自我改进，同时改 schema 选择和特征生成，处理（C3）。图 1 的例子是预测顾客未来 4 天是否会点击多于一条广告：迭代中验证 AUC 从 52.98 到 65.45，再到 65.92。这是图里的单个例子，不是全文主结果。贡献三条：把「为 RDB 预测任务生成特征」当成一个新问题；提出 ReFuGe；在七个数据集、十一项任务上超过当时的对比方法。具体表留在后文。

## 2 Task Formulation

给定关系库 R，表与表靠主键–外键相连。每张表被写成异构特征矩阵，列可以是数值或类别等。预测定义在指定目标表 T★ 的实体上。目标不是直接输出标签，而是利用 T★ 在全库里的关系上下文，为 T★ 再生成一些特征，与原有属性拼在一起，训练一个表格模型（例子是 LightGBM）。框架本身（三个 agent 和迭代循环）从第 3 节才展开。这篇是 4 页短文，第 2 节只到任务定义为止。
