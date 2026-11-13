> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名**：LEARN-2405.03988.pdf

**原文标题**：LEARN: Knowledge Adaptation from Large Language Model to Recommendation for Practical Industrial Application

**作者**：Jian Jia、Yipei Wang、Yan Li、Honggang Chen、Xuehan Bai、Zhaocheng Liu、Jian Liang、Quan Chen、Han Li、Peng Jiang、Kun Gai。除 Yipei Wang 外均署 Kuaishou Technology；Yipei Wang 署 Southeast University，脚注说明工作完成于在快手实习期间。Quan Chen 为通讯作者。

**场合 / arXiv**：版权页署 Association for the Advancement of Artificial Intelligence，2025（AAAI）。同时为 arXiv:2405.03988v3 [cs.IR]，2024-12-26。

## 摘要

推荐系统若只靠 ID embedding 记用户与物品的隐式关联，物品文本里的语义就用不上，效果和泛化都会变差。LEARN（Llm-driven knowlEdge Adaptive RecommeNdation）主张把 LLM 的开放世界知识与推荐里的协同知识接到一起：预训练 LLM 只当物品编码器，参数冻结，以免灾难性遗忘并保住开放世界知识；再用推荐任务监督的双塔结构，把两种知识对齐到可落地的工业设定。作者称该方法在真实大规模工业数据和在线 A/B 中有效，并在六个 Amazon Review 数据集上达到当时最优。

## Introduction

原文未给各节印节号。按正文顺序，Introduction 为第 1 节，Related Work 为第 2 节。Method 及之后不在本导读范围内。

现有推荐把历史交互压进彼此独立的 ID embedding，物品文本被丢掉，冷启动和长尾更吃亏；这种做法也不像视觉和语言那样，容易先得到一个能跨下游场景迁移的预训练模型。已有把 LLM 接进推荐的工作，作者统称为 Rec-to-LLM：把用户—物品交互改写成自然语言对话，再用 next token prediction，让输入组织和目标任务都贴着 LLM 的预训练形式，由模型直接生成兴趣、下一物品或推荐理由。Fig. 1 把这条路和 LEARN 的 LLM-to-Rec 对在一起。LEARN 不让 LLM 输出文本预测，而是把物品文本变成 LLM embedding，再投影进协同域，去对齐工业推荐任务。

作者认为 Rec-to-LLM 在真实工业场景里得不到实际收益，并给出三点原因。LLM 输入长度约在 2K 到 128K，计算也重；他们的短视频平台上，用户平均每周与近 800 条短视频交互，用 LLM 处理数月的全局历史负担过大。用推荐数据微调 LLM 时，协同知识与开放世界知识差距大，容易灾难性遗忘、效果也不好。LLM 的训练目标和推荐器进一步错位。LEARN 因此反过来做：LLM 只做内容抽取，训练目标改成推荐任务。框架是用户塔加物品塔，两塔都含 Content EXtraction（CEX）和 Preference ALignment（PAL）。CEX 把预训练 LLM 用作物品编码器，而不是用户偏好编码器，训练时冻结 LLM；PAL 用推荐任务的自监督目标去补开放世界与协同知识之间的域差。产出的用户、物品向量再送进在线排序模型。

验证分工业与公开数据两头：自建真实推荐场景的大规模数据并做在线 A/B，同时在 Amazon Reviews（Ni, Li, and McAuley 2019）上与已有方法比较。作者列出的贡献是：用 LEARN 把 LLM 中的开放世界知识收进推荐系统；用 CEX 与 PAL 处理开放世界知识的遗忘，并以推荐任务弥合域差；用大规模工业数据与在线 A/B 看真实收益；在六个公开数据集的三项指标上称达到 SOTA，其中 Recall@10 平均提高 13.95%。这两节没有印出表格。

## Related Work

内容推荐这一支从 ID embedding 的泛化不足写起，点到 GRU4Rec、SASRec、BERT4Rec、RecGURU。补内容的工作里，MIND 是面向新闻推荐的大规模文本数据；ZESRec、UniRec、TBIN 用预训练 BERT 抽取物品文本的 content embedding；Recformer 借用 BERT 的训练方式，把 masked language model 损失和对比损失合在一起，并重做 tokenizer。图像侧，SimTier 与 MAKE 用 CLIP 和 MoCo 抽图像特征，MoRec 与 MISSRec 则用 ResNet 和 ViT 把物品图像放进序列推荐。

LLM 推荐被分成两类。一类冻结 LLM，直接把它当推荐器：用任务提示构造推荐对话，让 ChatGPT 生成候选；RLMRec 用 ChatGPT 生成用户和物品画像。另一类在推荐域文本上微调：LlamaRec 以物品标题为文本、按排序分数优化 LLM；TALLRec 做两阶段微调，并用 LoRA 做 few-shot 推荐；LLaRA 把 LLM 提示和 ID embedding 接到已有的序列推荐器上；ReLLa 提出检索增强的指令微调，在混合数据上微调 Vicuna。作者把这两类都收进 Rec-to-LLM：交互数据被改成 LLM 的文本对话，损失也沿用 LLM 的训练损失，等于把推荐这个目标域的数据和任务搬进 LLM 这个源域。本节没有给出实验数字或表号。
