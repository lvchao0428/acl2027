> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

原文件名：ExcluIR_arXiv2404.17288.pdf

原文标题：ExcluIR: Exclusionary Neural Information Retrieval

作者：Wenhao Zhang、Mengqi Zhang、Shiguang Wu、Jiahuan Pei、Zhaochun Ren、Maarten de Rijke、Zhumin Chen、Pengjie Ren。Zhang、Mengqi Zhang、Wu、Chen、Ren 属 Shandong University（青岛）；Pei 属 Centrum Wiskunde & Informatica（阿姆斯特丹）；Zhaochun Ren 属 Leiden University；de Rijke 属 University of Amsterdam。Pengjie Ren 为通信作者。

场合 / arXiv：arXiv:2404.17288v1 [cs.IR]，2024 年 4 月 26 日。

## 摘要

排除是人用来表达“不要什么”的基本语言能力，但信息检索里很少研究用户在查询中明确说出不想要什么。本文第一次在文档检索里考察这种 exclusionary retrieval，并给出资源包 ExcluIR：一套评测基准，外加一份用来帮检索模型理解排除式查询的训练集。基准有 3,452 条高质量排除式查询，全部人工标注。训练集有 70,293 条，每条配一篇正文档和一篇负文档。

实验收成三条观察：不同结构的现有检索模型都难以真正理解排除式查询；把这份训练数据加进去能提高排除式检索的表现，但和人的水平仍有差距；生成式检索模型处理这类查询有天然优势。基准和评测脚本在 https://github.com/zwh-sdu/ExcluIR 。

## 1 Introduction

选择性注意被定义为盯住相关信息、同时忽略无关信息，作者把它从认知心理学接到用户的搜索行为上：用户会明确要求排除某些内容，这就是 exclusionary retrieval。理解失败会直接伤相关性。Figure 1 用电影检索对比两种问法。非排除式是 “What are the American sci-fi action movies released in 2019?”；排除式是 “What other sci-fi movies (besides Avengers: Endgame) were released in 2019?”。系统若读不懂 besides 这类排除，就会把用户点名不要的 Avengers: Endgame 检回来，而用户真正想要的是同档期的其他科幻片，例如图中的 Alita: Battle Angel。

早期排除式检索主要把否定词写进布尔查询，本质是后处理，而且依赖结构化查询，盖不住复杂的自然语言。较近的否定研究看的是文档内部的否定语义，而不是查询本身的排除意图。作者认为当时还没有数据集能评模型做排除式检索的能力。第一项贡献就是 ExcluIR。数据建在 HotpotQA 上：对两篇相关文档，用 ChatGPT（脚注指向 GPT-3.5）生成一条排除式查询，要求答案只在其中一篇里，并明确拒绝另一篇的信息；再由 17 名工人核对基准中的每条数据。训练集 70,293 条，基准 3,452 条人工标注查询。

第二项贡献是拿不同结构的现有方法做排除式检索，覆盖稀疏检索、稠密检索和生成式检索。这一节给出的三条观察是：现有模型不能充分理解排除式查询的真实意图；生成式模型有独特优势，而 ColBERT 这类 late interaction 模型有明显短板；用 ExcluIR 训练集微调能提高表现，但仍然远不能令人满意。作者说后文会对这些观察做深入分析。

## 2 Dataset Construction

Figure 2 把构造收成四步：从 HotpotQA 抽文档对，用 ChatGPT 生成排除式查询，再改写以增加多样性，最后按标注规范做人工修正。2.1 利用 HotpotQA 的多跳问答设定：每条数据有两篇相互关联的支撑文档。从每条抽出两篇，共 74,293 对；合并去重后文档库有 90,406 篇。2.2 用两步提示保证正负文档都被覆盖：先生成一条与两篇都相关的查询，再改写成拒绝负文档信息。提示细节放在 Appendix A。

2.3 指出即便提示调过，生成结果仍反复使用少数排除说法，例如 “excluding any information about”“except for any information”“without referencing any information about”，不够像真实查询。于是再让 ChatGPT 改写，然后把这一步得到的数据划成训练和测试；测试集还要人工修正才成为基准。2.4 雇 17 名工人，从 74,293 条里抽 4,000 条，每条含两篇文档和一条合成查询。工人要检查自然性和正确性，并被鼓励用更多样的排除表达。在线修正系统提供三种操作：已达标则不动；不达标则改写查询；若两篇文档很难写出合格查询，可以丢弃。具体要求在 Appendix B。

2.5 的质量措施包括：书面指南（任务定义、修正流程、排除式查询的具体标准）、多个示例、全过程演示视频、工人可实时反馈问题并由作者讨论解决，以及对每位工人随机抽 10% 数据检查，有错则退回重改。2.6 的结果是基准 3,452 条人工标注，训练集 70,293 条排除式查询。查询平均词数在训练集为 22.37，在基准上为 21.64。Figure 3 显示查询长度分布较散，复杂程度和细节量并不整齐。
