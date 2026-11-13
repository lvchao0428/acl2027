> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文标题：** EComAgentBench: Benchmarking Shopping Agents on Long-Horizon Tasks with Distributed Hidden Intent

**作者：** Zeyao Du、Tong Li、Haibo Zhang（Shopee）。

**场合：** EMNLP 2026 Industry Track，页 1012–1027，2026 年 10 月 24–29 日。

**PDF：** `ecomagentbench-2026.emnlp-industry.61.pdf`

## Abstract

摘要的论点是：购物需求不是一次给全的。它可能含蓄地写在问句里，记在人设里，或者只有问对了问题才出现。把完整意图事先摊开、只给最终选择打分的基准，既造不出这种长程困难，也解释不了智能体漏了哪一条要求。EComAgentBench 因此做了 662 条任务，落在真实 Amazon 商品和评论上。每条任务把要求拆进可见问句、要靠工具才能读到的人设，以及脚本化的澄清。智能体要找出隐藏意图，对照属性和评论证据检查候选，并在 100 次工具调用内交一件商品。打分用带类型、带来源的 rubric，把每次失败记到某一条要求及其来源上。构造是自动的，但答案在写句子之前就在代码里锁定，并且每条样本都经过验证。摘要对七个模型的总判断是：最强的模型整体准确率也只有 57.1%。

## 1 Introduction

第 1 节把「购物智能体进了生产」接到「现有基准测不到分散意图」。作者把失败模式写成：问句里的要求是隐含的，人设和澄清要主动去取，评论里的意见不能靠字段相等来判定。只看一句查询、并且事先给出全部条件的基准，测的是条件已经收集完之后的选择，测不到寻找和提问。

节内的设计原则有三条，和摘要对应。意图要拆开，其中两处被工具挡住，这样恢复意图本身就是长程轨迹。rubric 既有类型也有来源，失败能对上是哪一条要求、从哪来的。构造要能复现：自动生成，但答案先于文本锁定，并经过验证。作者说这三件事同时做到，是先前购物基准没有的组合。具体环境和工具表留在第 3 节。

## 2 Related Work

第 2 节用三组对照说明缺口，并用表 1 把对照收成一张能力表。

**E-commerce shopping benchmarks。** WebShop 把智能体放在真实购物页上，重点是浏览器交互，不是找回隐藏要求。ShoppingBench 的意图基本在问句里，任务自动生成，但没有独立验证。ShopSimulator 用模拟用户加个性化，依赖人工标注。DeepPlanning 做可验证约束的长程规划，物品却是合成的。作者的结论是：这些基准即使给部分分数，也没有标出失败的要求来自哪里。

**Web-agent and interactive evaluation。** Mind2Web、WebArena、VisualWebArena、AssistantBench 说明真实的智能体评测要看它怎么收集信息、怎么用环境，不能只看最终答案。EComAgentBench 把这个想法收窄到购物：意图来自问句、人设和澄清。

**Evaluator design and rubric decomposition。** VitaBench 用 rubric 拆复杂轨迹。本文在此之上加上类型和来源。LLM-as-judge 的文献支持用模型打分，但也警告不要让裁判自由给分。因此本文把裁判要核对的目标事先写死在代码里，绑到带类型的 rubric 上，而不是开放式评分。
