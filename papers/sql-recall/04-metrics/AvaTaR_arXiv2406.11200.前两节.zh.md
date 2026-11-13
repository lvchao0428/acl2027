> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

原文件名：AvaTaR_arXiv2406.11200.pdf

原文标题：AVATAR: Optimizing LLM Agents for Tool Usage via Contrastive Reasoning

作者：Shirley Wu、Shiyu Zhao、Qian Huang、Kexin Huang、Michihiro Yasunaga、Kaidi Cao、Vassilis N. Ioannidis、Karthik Subbian、Jure Leskovec、James Zou。Wu、Zhao、Qian Huang、Kexin Huang、Yasunaga、Cao、Leskovec、Zou 属 Stanford University 计算机系；Ioannidis 与 Subbian 属 Amazon。Leskovec 与 Zou 为共同资深作者。通信邮箱为 {shirwu, jure, jamesz}@cs.stanford.edu。

场合 / arXiv：arXiv:2406.11200v3 [cs.LG]，2024 年 10 月 31 日。

## 摘要

LLM agent 已经能借助外部工具和知识提高准确率、减少幻觉，但怎样写提示才能让它用好这些工具，仍然靠手工试。AVATAR 把这件事做成自动优化：优化过程中有一个 comparator，从训练数据里抽正例和负例，用对比推理反复给 agent 写出更完整的提示，从而让 agent 更好地调用给定工具、提高指定任务的表现。

演示覆盖四个复杂的多模态检索数据集（文本、视觉、关系信息）和三个一般问答数据集，一共七个任务。摘要的结果是：七个任务上都超过当时最好方法，换到新案例上也能泛化；检索数据集的 Hit@1 平均相对提升 14%，问答数据集平均相对提升 13%。代码和数据在 https://github.com/zou-group/avatar 。

## 1 Introduction

LLM agent 能推理、能规划，再接上知识库和搜索引擎一类 API，就可以做多步解题和多样信息检索，这对复杂检索和问答很关键。难的是提示本身：要把复杂问题拆成可执行步骤，决定何时用哪个工具收集信息，再把中间结果合成最终回答。每一步都要大量人工试错。现有做法多半直接上人工写的 mega-prompt。Figure 2 (a) 用商品咨询说明这种提示很脆：ReAct agent 容易给出空泛、误导的答案。把 LLM 当作优化器的工作，也往往改不好“如何把工具嵌进多步策略”这一层，于是 agent 在真实场景里既不够好用，也不容易泛化。

AVATAR 用对比推理做一个 comparator（文中比作 trainer），为 actor LLM 生成整体指令和提示，相当于算一个更稳的 “gradient”。Figure 1 把系统画成 actor 加 comparator。优化阶段，actor 用给定工具回答查询；comparator 拿当前 agent 做得好的正例和做得差的负例对照，自动写出整体提示，教 actor 区分有效和无效的工具用法。单条样本上的指令容易过拟合，把多条样本当成一个 batch，才能抽出更稳的更新方向，也就是文中说的把 “gradient” “backpropagate” 给 actor。系统还保留一个 memory bank，存挑选过的历史指令，避免 actor 重复旧错。部署阶段选出表现最好的提示；在复杂检索里，迭代更新还会改出更可泛化的动作序列，新问题可以直接用。Figure 2 (b) 里优化后的 actor 出现三种新策略：按多方面属性把问题拆开，用更精细的打分系统调用工具，再按学到的系数把不同分数合起来。

实验是四个检索数据集加三个问答数据集，检索同时涉及文本、视觉和关系信息。第 1 节给出的数字是：Hit@1 有 14% 的提升；只迭代 25 次，FLICKR30K-ENTITIES 上 Hit@1 从 5.1% 升到 28.6%，STARK-PRIME 上 Recall@20 从 30.3% 升到 39.3%；一般问答上平均超过当时最好方法 13%。贡献收成三条：用 comparator 自动生成整体提示来优化 actor 的工具使用；在四个复杂检索和三个问答上同时提高任务表现和泛化；并分析优化过程中 actor 如何被针对性指令改好、推广开。

## 2 Related Work

这一节把相关工作分成三块。LLM agent 方面，已有工作让模型与环境交互、调用外部工具、并积累经验。例子是 ReAct：推理和动作交错进行，并从 Wikipedia 取信息来支撑推理。检索方面，LLM agent 被用在信息检索的预训练、重排序和提示技术里；检索器会直接影响检索增强生成和知识密集型问答。EHRAgent 面向电子健康记录问答，用结构化的工具使用规划加上交互式代码去取临床知识。这些 agent 通常仍靠启发式的 zero-shot 提示或 few-shot 例子，缺少关于如何生成检索策略和工具辅助动作的更明确指导。

优化方面，已有路线要么微调或指令微调骨干模型，要么迭代改提示。Zhang 等人按执行历史迭代更新 agent 的函数。作者认为这些方法没有专门针对工具使用、也没有针对复杂多阶段任务做定向优化，而真实应用需要的泛化能力受到的关注更少。本文的做法是用对比推理自动生成整体指令，同时对准工具使用和泛化。相对微调，AvaTaR 只需要一小部分训练数据和工具描述，因此更灵活，计算开销也更低。这一节没有另给实验数字。
