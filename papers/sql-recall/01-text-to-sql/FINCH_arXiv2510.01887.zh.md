原文件名：FINCH_arXiv2510.01887.pdf

原标题：FINCH: Financial Intelligence using Natural language for Contextualized SQL Handling

中文标题：FINCH：利用自然语言进行情境化 SQL 处理的金融智能

作者：Avinash Kumar Singh; Bhaskarjit Sarmah; Stefano Pasquali

arXiv：arXiv:2510.01887v1 [q-fin.CP] 2 Oct 2025

<!-- 原 PDF 第 1 页 -->

Avinash Kumar Singh  
Domyn  
Hyderabad, India  
avinash.kumarsingh@domyn.com

Bhaskarjit Sarmah  
Domyn  
Gurgaon, India  
bhaskarjit.sarmah@domyn.com

Stefano Pasquali  
Domyn  
New York, USA  
stefano.pasquali@domyn.com

## 摘要

Text-to-SQL，即将自然语言问题翻译成 SQL 查询的任务，长期以来一直是自然语言处理中的核心挑战。尽管进展显著，把它用到金融领域仍然特别困难，原因在于模式复杂、术语带有领域特殊性，以及出错的代价很高。尽管如此，目前并没有专门的大规模金融数据集来推进研究，从而留下一个关键缺口。为填补这一缺口，我们引入经过整理的金融数据集 FINCH，包含 292 张表和 75,725 条自然语言–SQL 对，既能用于微调，也能用于严格评测。在这一资源之上，我们对不同规模的推理模型和语言模型做了基准测试，系统分析它们在金融 Text-to-SQL 任务上的优势与局限。最后，我们提出面向金融的评测指标 FINCH Score。它捕捉现有指标所忽略的细微差别，从而对模型表现给出更忠实的评估。

## 关键词

Text-to-SQL，金融领域的大语言模型，金融基准数据集，面向金融的 Text-to-SQL 评测指标

## 1 引言

把自然语言问题翻译成 SQL 查询的任务，通常称为 Text-to-SQL，自关系数据库出现的早期以来，一直是核心研究挑战 [28]。早期方法以基于规则的文法和符号解析为主，神经网络方法的出现则从根本上重塑了这一领域。Seq2SQL（2017）[37] 表明，强化学习可以用来生成可执行查询，并超过基于模板的系统。此后不久，SQLNet [29] 用基于草图的解码策略取代强化学习，在保持较强性能的同时降低了复杂度。Spider（2018）[33] 作为首个大规模跨领域数据集发布，为评估模型在多样模式上的泛化提供了基础，并迅速成为首选基准。后续数据集 CoSQL 和 SParC（2019）[32, 34] 把任务扩展到对话式、依赖上下文的设定。模型层面的进展很快跟上：RAT-SQL（2020）[24] 引入用于模式链接的关系感知 Transformer，PICARD（2021）[20] 则对大规模预训练语言模型施加约束解码。更近一些，BIRD 基准（2023）[14] 把评测规模扩大到数十亿条查询，成为迄今衡量大规模稳健性最全面的资源。

尽管沿着这条轨迹不断前进，显著的挑战仍然存在。许多最先进的系统在基准上取得很高的成绩，却在偏离其训练语料的模式上表现不佳 [13, 22]。Spider [33] 和 BIRD [14] 强调跨领域泛化，但它们的模式大多反映百科式或开放领域知识，而不是特定行业的设定。RAT-SQL [24] 和 DCG-SQL（2025）[25] 等模式链接方法改善了上下文对齐，但对含噪描述和很宽的列空间仍然敏感，而这些情况在企业数据库中很常见 [4, 18, 20]。更新的方法，例如 NL2PY2SQL（2024）[16]，探索 Python 到 SQL 的中间表示，但在高风险领域中，其效率与可解释性仍是问题。最后，评测方法继续依赖精确匹配 [33] 和执行准确率 [37]，这些指标往往无法捕捉细微但有意义的结构差异。这些局限合在一起，暴露出由基准驱动的进展与真实部署需求之间的缺口。

与此同时，金融领域对可执行推理任务的兴趣不断增长。这些任务并不总是以 SQL 为中心，但处理的挑战与数据库查询直接相关 [12, 19]。FinQA（2021）[1] 引入了针对公司财务报告进行数值推理的基准，把文本输入与操作程序（program-of-operations）监督配对，以促进神经—符号融合。类似地，TAT-QA（2021）[39] 结合表格与文本信息，反映出金融数据的多模态性质。ConvFinQA（2022）[2] 进一步把这一点扩展到多轮推理，模拟分析师工作流中查询逐步演化的过程。除数据集之外，模块化方法也已经出现。例如，Nye 等人 [17] 提出一个系统：一个智能体从申报文件中抽取关键绩效指标，另一个智能体把它们翻译成 SQL 查询，从而把推理分配到专门的组件上。伴随这些进展，评测指标已从僵硬的精确匹配转向树编辑距离 [36] 和结构感知的相似度度量 [38]，与分析师的预期更为一致。

最近已有工作开始专门处理金融领域的 Text-to-SQL，不过与开放领域研究相比，这一方向仍处于初期。FinSQL（2024）[35] 做了第一次专门尝试，发布了 BULL 数据集，其中是为跨数据库泛化而设计的宽模式金融表。其结果显示，领域专门的调优相对通用基线最多可带来 36% 的相对提升，但也表明在更大的模式上性能会急剧下降。BookSQL（2024）[11] 与之互补，在会计领域提供 7.5 万条自然语言–SQL 对，暴露出大规模预训练模型在处理微妙业务语义和复杂连接时的局限。方法方面，NL2PY2SQL（2024）[6] 引入自然语言–Python–SQL 的两步流程，能更好地捕捉领域逻辑；DCG-SQL（2025）[15] 则利用深度上下文图表示，增强在列数多、关系复杂的表上的模式链接。在准确率之外，Reliable Text-to-SQL（RTS，2025）[26] 纳入自适应弃答和人在回路的纠正，强调在银行、审计和投资场景中，可靠性是核心要求。

<!-- 原 PDF 第 2 页 -->

综合来看，这些发展指出一个关键缺口：尽管基准成绩在稳步提高，当前系统仍然不适合金融部署 [3, 21, 30]。金融数据库有其独特挑战：模式宽且不断演化，领域约束严格，需要监管合规，并且对错误高度敏感。应对这些挑战，需要领域专门的数据集、明确针对金融模式来设计的架构，以及超越精确匹配、能够捕捉语义保真和运行安全的评测方法。弥合这一缺口，并不只是通用 Text-to-SQL 研究的增量一步，而是一次必要的转向：去构建能够在关键决策中支持分析师、审计人员和政策制定者的实用系统。

金融问答和领域专门的 Text-to-SQL 已经有相当进展，但先前工作大多仍以文档为中心，或做表格–文本混合推理，而不是直接查询金融 SQL 数据库。因此，专门面向金融的 Text-to-SQL 基准很少，社区仍然缺少一种资源，能够如实捕捉真实金融应用所要求的复杂性、术语和精度。填补这一缺口，既需要大规模、领域专门的数据集，也需要能够反映金融环境独特挑战的评测方法。

受这些挑战推动，本工作为推进金融领域的 Text-to-SQL 做出三项关键贡献：

- 大规模金融数据集整理：我们把 BIRD [14]、Spider [33]、FinSQL [35] 和 BookSQL [11] 等已有资源合并并扩展为一个统一数据集。所有 SQL 查询都经过规范化，以便与 SQLite 兼容，从而保证开源社区可以广泛使用。最终数据集 FINCH 覆盖 33 个数据库，领域包括零售、银行交易、贷款、保险、销售、营销、金融、电子商务、基金、股票和会计。合计包含 292 张表、2233 列、177 个关系，以及 75,725 条自然语言–SQL 对，提供了最大的面向金融的基准，既适合评测，也适合微调。
- 全面的模型基准测试：我们评测四类模型：大规模大语言模型（Qwen3-235B-A22B[^1]），中小规模开源模型（GPT-OSS-120B[^2]、GPT-OSS-20B[^3]、Qwen3-8B[^4]），以及以推理为中心的模型（Phi-4-mini-reasoning[^5] 和 Arctic-Text2SQL-R1-7B[^6]）。结果显示，GPT-OSS-120B 取得最强的总体表现，甚至超过 Qwen3-235B-A22B 这样更大的模型；Arctic-Text2SQL-R1-7B 尽管参数规模不大，却成为表现第三好的模型。这些发现表明，以推理为中心的架构在经过仔细适配之后，可以在金融 Text-to-SQL 任务上媲美甚至超过规模大得多的通用大语言模型。
- 金融专门的评测指标：我们提出定制的评测指标 FINCH Score。它把组件匹配和执行准确率与加权评分、容差阈值结合在一起。这一设计减轻了对轻微浮点不一致的不成比例惩罚，同时强调结构保真，优先保证列名、表引用和条件的正确性。实验表明，该指标对金融设定下的表现给出更忠实的评估，比传统的精确匹配指标更符合实际要求。

[^1]: https://huggingface.co/Qwen/Qwen3-235B-A22B
[^2]: https://huggingface.co/openai/gpt-oss-120b
[^3]: https://huggingface.co/openai/gpt-oss-20b
[^4]: https://huggingface.co/Qwen/Qwen3-8B
[^5]: https://huggingface.co/microsoft/Phi-4-mini-flash-reasoning
[^6]: https://huggingface.co/Snowflake/Arctic-Text2SQL-R1-7B

## 2 FINCH 数据集的构建

为回应面向金融的大规模 Text-to-SQL 基准这一迫切需求，我们通过审慎地合并并修订四个公开资源来整理 FINCH 数据集：BIRD [14]、Spider [33]、BULL [35] 和 BookSQL [11]。

Spider 和 BIRD 是 Text-to-SQL 社区广泛认可的基准，但它们最初并不是为金融应用设计的。它们的数据库跨越很宽的领域，从体育、教育到娱乐和地理，其中许多与金融系统关系不大。与此相对，使用金融数据的实践者和研究者面临高度专门的挑战，例如解读银行记录、分析卡交易、管理零售和销售数据，或处理贷款与保险查询 [1, 39]。使用通用基准，有可能冲淡模型的关注点，并限制它们在真实金融场景中的适用性。

为弥合这一缺口，我们进行了仔细的筛选，只保留与金融情境对齐的数据库。具体而言，我们识别并保留了覆盖零售销售、卡交易、银行服务、贷款处理、保险和电子商务的领域。由此，FINCH 并不只是又一次 Text-to-SQL 数据的汇集，而是对金融相关应用有直接用途的基准。

表 1 将 FINCH 与四个广泛使用的 Text-to-SQL 数据集进行比较。先前的基准或者强调规模（例如 BookSQL），或者强调跨领域泛化（例如 Spider、BIRD），FINCH 则在规模、模式多样性和金融相关性之间取得平衡。特别是，它提供 33 个金融专门的数据库，平均表数/库数比高于更早的资源，因此特别适合评估金融场景中的模式链接和组合推理。

### 2.1 数据集整理

FINCH 的整理经过若干审慎、有步骤的环节。我们从 Spider 中选出 22 个具有明确金融相关性的数据库，从 BIRD 中保留 7 个这样的数据库。BULL 和 BookSQL 在设计上已经以金融为中心，凡是自然语言问题及其对应 SQL 语句都存在的样本，我们全部保留。由此得到一个多样、同时又针对特定领域的数据集，结构如下：

- BIRD：1,139 条样本

<!-- 原 PDF 第 3 页 -->

**表 1：** FINCH 与现有 Text-to-SQL 数据集的比较。各列表示数据集规模（#Size）、数据库数量（#DB），以及（#T/DB）数据库–表比（database-to-table ratio）。

| 数据集 | #Size | #DB | #DB* | #Size* | #T/DB |
| --- | --- | --- | --- | --- | --- |
| Spider | 10,181 | 200 | 22 | 1,100 | 5.1 |
| BIRD | 12,751 | 95 | 7 | 812 | 7.3 |
| BULL | 4,966 | 3 | 3 | 4,966 | 26.0 |
| BookSQL | 78,433 | 1 | 1 | 68,907 | 7.0 |
| FINCH | - | - | 33 | 75,725 | 8.85 |

- Spider：1,100 条样本
- BULL：4,966 条样本
- BookSQL：78,433 条样本

在这一过程中，我们观察到 BookSQL 的测试划分没有对应的 SQL 查询，因此把这一部分排除出 FINCH，以保持完整性与可用性。为进一步保证数据可靠，每条 SQL 查询都在其关联的 SQLite 数据库上执行。这一校验步骤被证明至关重要，它揭示出大量异常；若不处理，数据集的可靠性会受到损害。具体而言，我们发现：

- 在 BIRD 中，1,139 条查询里有 327 条执行失败，其中 198 条列名错误，129 条表引用无效。
- 在 BULL 中，4,966 条查询里有 60 条有问题，包括 43 条语法错误、10 条错误的表引用、1 条列错误、4 条不完整查询，以及 2 条无法识别的记号。
- 在 BookSQL 中，78,433 条查询里有 9,526 条出现错误：7,018 条列名错误，1,494 条表引用无效，1,014 条语法错误。
- 值得注意的是，Spider 子集没有发现任何异常。

识别、登记并改正这些错误，并不纯粹是机械操作。它需要反复执行查询、仔细检查数据库模式，并结合上下文推断每个问题背后的意图。这种审慎保证 FINCH 不仅按规模汇集数据，也保持了金融专门的 Text-to-SQL 研究所需要的精度和稳健性。

FINCH 的最终版本由 33 个数据库组成，涵盖 292 张表、2,233 列和 177 个关系，自然语言–SQL 对总计超过 75,725 条。就难度分布而言，FINCH 包含 9,358 条易例、33,780 条中等例和 32,587 条难例。另有 7,035 条原先没有标签的样本，按照 [11] 提出的模式复杂度指南做了标注。这一设计保证覆盖多样的金融操作、模式复杂度和 SQL 结构。此外，FINCH 大量使用 ORDER BY、GROUP BY 和嵌套查询等 SQL 操作，这些操作对于在金融环境中建模复杂推理是必要的。

图 1 给出 FINCH 的高层总览，说明来自多个来源的数据库如何被合并成一个统一基准。该图也突出数据库模式的多样性，以及这次合并所达到的领域覆盖广度。

总之，FINCH 是第一个大规模、金融专门的 Text-to-SQL 数据集，同时具备广度（多个领域）、深度（丰富的模式复杂度）和难度（并不简单的 SQL 结构）。我们相信，FINCH 将成为在金融应用中评测和微调大语言模型以及以推理为中心的架构的基础资源。

## 3 实验设置与评测指标

### 3.1 实验设置

我们对一组多样的模型做基准测试，特别强调那些明确为推理而优化的模型，以检验这类能力能否有效迁移到金融领域的 Text-to-SQL。具体而言，评测覆盖：（i）大规模语言模型，如 Qwen3-235B-A22B 和 GPT-OSS-120B；（ii）中小规模模型，如 Qwen3-8B 和 GPT-OSS-20B；（iii）以推理为中心的模型，包括 Phi-4-mini-reasoning 和 Arctic-Text2SQL-R1-7B，它们是本研究中最强的面向推理的基线。

这一选择出于三个因素。第一，规模对照：模型参数量从数千亿一直到只有个位数个十亿，使我们能够考察 SQL 结构保真度是否会像缩放定律研究所提示的那样，随模型规模可预测地提高 [7, 9]。第二，纳入来自不同设计族的模型（Qwen 类、GPT 类和 Arctic），保证模型族的多样性，从而减轻与单一架构谱系相关的偏差。最后，推理对齐这一维度反映了一种日益增强的重视：模型宣称具有更强的思维链推理和工具使用能力 [10, 27, 31]。我们假设，这将改善模式落地、算子选择和组合式连接，而这些能力在金融 Text-to-SQL 任务中尤其关键。

为了保证模型之间可比，我们采用统一的单样本（one-shot）提示协议（见表 2）。每条提示由一个自然语言问题及其对应的数据库模式组成，模型需要生成一条句法有效、忠实于模式的 SQL 查询，不附加额外说明。模板、停止序列和后处理保持不变：去掉代码围栏，把输出限制为仅含 SQL 的回答，并解析其有效性。这一设计保证，观察到的性能差异可以归因于模型行为，而不是提示工程或解码伪影。提示模板强制一种受控设定，保证所有被评测系统之间的一致性。它明确规定任务，同时提供自然语言输入和模式上下文，并对查询生成施加严格约束，例如忠实于模式、句法正确，以及避免没有依据的假设。通过把这些指令标准化，我们把提示选择带来的变异降到最低，并直接检验模型把金融问题翻译成可执行 SQL 的内在能力。这种程度的控制在金融领域特别重要：即便很小的偏离，例如没有依据的连接、写错的列名，或形式不当的聚合，都可能导致实质上错误的结果。此外，提示中的约束与我们的评测指标紧密对齐：句法正确性

<!-- 原 PDF 第 4 页 -->

**图 1：** FINCH 数据集的表示，展示不同数据库与表在各个金融领域中的整合。

图中的图形未随文本抽出，见原 PDF 第 4 页。

支撑执行准确率 [37]，模式保真由组件匹配指标捕捉 [33]，逻辑合理性则对应结构感知的评测度量 [38]。合在一起，提示设计与评测标准构成紧密耦合的 FINCH Score，能够在真实的金融 Text-to-SQL 场景中忠实评估模型表现。

### 3.2 评测指标

Text-to-SQL 系统的评测通常依赖少数标准指标。精确匹配（Exact Matching，EM）[33] 衡量预测的 SQL 查询是否与黄金查询逐字符串一致。执行准确率（Execution Accuracy，EX）[37] 在查询输出与黄金查询输出一致时判定该查询正确，并把正确性当作二值（1/0）。组件匹配（Component Matching，CM）[33] 在子句层面比较查询，例如 SELECT、WHERE、GROUP BY 等，从而给出更细粒度的正确性图景。最后，有效效率分数（Valid Efficiency Score，VES）[14] 扩展这些想法，奖励那些不仅正确、而且执行起来高效的查询。这些指标合在一起，对查询准确率、执行忠实性和效率给出表层评估。

<!-- 原 PDF 第 5 页 -->

**表 2：** 所有模型评测所用的单样本提示示例。该提示规定任务，给出带有数据库模式的自然语言问题，并强制严格的 SQL 生成约束。

你是一名专家级 SQL 助手。你的任务是理解问题（Question），查看数据库模式（Schema），然后帮助用户找到一条句法正确且经过优化的 SQL 查询。

### 任务：

根据用户问题和模式生成一条 SQL 查询。

### 自然语言问题：

{QUESTION}

### 数据库模式：

{DATABASE}

### 约束：

- 使用标准 SQL 语法。
- 只使用数据库模式中指定的表和列。
- 避免任何在模式中并不明显的假设或连接。
- 如果需要聚合或过滤，须保证逻辑正确。

### 预期输出：

```sql
```

表抽取失败，见原 PDF 第 5 页。

然而，这些指标并不足以捕捉金融中真正重要的东西。EM 和 EX 过于严格：对于差异纯粹是表面现象的、接近正确的查询，例如使用别名或无害的重排，它们给零分。EX 也不考虑重要性（materiality），会惩罚那些只有很小舍入误差、或偏差可以忽略、并不带来金融意义的查询。CM 假定所有子句的贡献相同，而在金融中，WHERE、JOIN、GROUP BY、HAVING 和 AGG 子句承载最大的语义权重。VES 对衡量效率有用，但可能不公平地惩罚那些由于汇总（rollup）、风险分解或由合规驱动的连接而确实复杂的查询。因此，这些标准指标会过度惩罚并不重要的差异，也捕捉不到那些编码 SQL 真正金融含义的子句和容差。

为克服这些不足，我们提出 FINCH 指标。它把对子句敏感的结构评分，与带容差的执行准确率结合在一起。FINCH 引入可解释的控制项来平衡结构与执行，与金融中的重要性原则对齐，并且仍然与现有基准兼容，从而对金融 Text-to-SQL 的表现给出更忠实的评测。

**所提出的指标：FINCH Score。** 记黄金 SQL 为 $q^{*}$，模型 SQL 为 $\hat{q}$。

**1）分组件得分（结构／语义）。** 选取组件集合 $K$（例如 SELECT、WHERE、GROUP BY、HAVING、ORDER BY、JOIN、AGG、LIMIT、SUBQUERY）。对每个组件 $k \in K$，计算一个相似度

$$s_k(\hat{q}, q^{*}) \in [0, 1]$$

（例如精确匹配、集合 F1 或词元 F1）。赋予权重 $w_k \geq 0$。权重归一条件中的求和符号被抽成字符「Í」，原串为：

```
Í
𝑘∈𝐾𝑤𝑘= 1
```

公式抽取不完整，见原 PDF 第 5 页。按其已抽出的下标与等号，该条件即各权重之和为 1。加权组件得分为

$$
S(\hat{q}, q^{*}) = \sum_{k \in K} w_k \, s_k(\hat{q}, q^{*}) \in [0, 1].
\tag{1}
$$

在金融情境中，自然会给 WHERE、JOIN、GROUP BY、HAVING 和 AGG 更高的权重，因为这些子句编码业务规则、投资组合汇总和合规过滤。例如，在一条为一组投资组合计算在险价值（Value-at-Risk，VaR）的查询中，漏掉用来筛选“活跃头寸”（active positions）的 WHERE 子句，比漏掉一条 ORDER BY 子句损害大得多。权重 $w_k$ 可以通过分析历史上的错误查询来经验地估计：那些一旦被误解就会导致显著金融偏差的组件（例如风险敞口被错报达数百万美元）应当比影响可以忽略的组件得到更高的权重。这使该指标与真实的金融利害相一致。

**2）执行准确率（带容差）。** 定义执行相似度 $e(\hat{q}, q^{*}) \in \{0, 1\}$，容差为 $\tau$。分段括号被抽成私用区字形，原串为：

```
𝑒( ˆ𝑞,𝑞∗) =


1,
if
| 𝑟ˆ𝑞−𝑟𝑞∗|
max{1, |𝑟𝑞∗|} ≤𝜏,
0,
otherwise.
(2)
```

公式抽取不完整，见原 PDF 第 5 页。已抽出的分支是：若

$$
\frac{|r_{\hat{q}} - r_{q^{*}}|}{\max\{1, |r_{q^{*}}|\}} \leq \tau
$$

则为 1，否则为 0。其中 $r_{\hat{q}}$ 与 $r_{q^{*}}$ 是查询结果，$\tau$（例如 $10^{-4}$ 或 0.01%）强制一种顾及重要性的容差。

这种基于容差的评测对金融是必要的。考虑一条计算共同基金投资组合平均净资产价值（net asset value，NAV）的查询。如果预测查询因为舍入或浮点精度而相差 0.0001，EM 和 EX 会把它整条判为错误，即便没有任何金融决策会受到影响。通过纳入 $\tau$，FINCH 尊重重要性原则，而这一原则处于会计和监管标准的核心 [8]。容差可以按照领域实践来设定：对每日的投资组合估值，$\tau$ 可以非常小（例如 $10^{-5}$）；对汇总后的风险上卷，更高的容差（例如 0.1%）可以接受。

**3）组合指标。** 借助带惩罚的乘性包络来平衡结构与执行。式 (3) 的原串如下。乘号之后、$\delta$ 之前有控制字符 U+0000，$e(\hat{q}, q^{*})$ 之后有控制字符 U+0001，分组符号未抽出：

```
Score( ˆ𝑞,𝑞∗) = 𝑆( ˆ𝑞,𝑞∗)𝛽· [U+0000]𝛿+ (1 −𝛿) 𝑒( ˆ𝑞,𝑞∗)[U+0001]
(3)
```

公式抽取不完整，见原 PDF 第 5 页。

其中 $\beta \geq 1$ 控制结构保真度，$\delta \in [0, 1)$ 表示执行失败时的严厉程度。严格情形：$\delta = 0$；对金融更友好的情形：$\delta \in [0.2, 0.5]$。

实践中，$\beta$ 和 $\delta$ 的取值应当通过在金融数据集上的验证来估计。例如，可以用历史查询做回测来调节 $\beta$，以反映结构正确性对下游可解释性有多重要。更高的 $\beta$ 会对缺失的子句施加更严的惩罚，这对合规上至关重要的查询是合适的。另一方面，$\delta$ 捕捉执行不匹配所受的惩罚：把 $\delta$ 设为 0.3，意味着一条结构正确但执行失败的查询仍然保留部分分数。这反映出分析师往往可以改正较小的句法问题，而不必重新构思整条查询。这与金融数据团队的真实工作流相符：在那里，结构

<!-- 原 PDF 第 6 页 -->

往往比轻微的执行错误更难修正。在我们的实验中，$\beta$ 和 $\delta$ 的取值是 1 和 0.3。

## 4 结果与分析

我们对一组多样的模型做了基准测试，从 Qwen3-235B-A22B 以及 GPT 模型 GPT-OSS-120B 这类大规模系统，到 Qwen3-8B 和 GPT-OSS-20B 这类更小、计算上更高效的变体。我们也纳入了以推理为重点的模型，例如 Phi-4-mini-reasoning，以及经过领域适配的 Arctic-Text2SQL-R1-7B，后者被明确微调用于 Text-to-SQL 应用。评测在 FINCH 数据集上进行，既使用已有指标——精确匹配（EM）[37]、执行准确率（EX）[33]、组件匹配（CM）[33] 和严格匹配（Strict Matching）——也使用所提出的 FINCH Score。该分数把结构保真、执行准确率与金融领域的敏感性结合在一起。汇总结果见表 3。

### 4.1 模型的总体表现

结果显示，GPT-OSS-120B 取得最强的总体表现，在大多数评测指标上持续超过所有其他模型。这说明，只要优化充分，大规模模型在复杂的金融 Text-to-SQL 任务上仍然具有持续优势。值得注意的是，Arctic-Text2SQL-R1-7B 成为表现第三好的模型，尽管其参数量小得多。它的表现凸显了领域专门微调的价值：让模型训练与金融数据库、SQL 结构以及领域专门术语紧密对齐，能够在语义准确率和模式保真上带来切实改进。这些发现强化了一个双重认识：缩放赋予原始能力，而有针对性的适配可以让较小的模型媲美大得多的模型。这与领域自适应自然语言处理中的近期观察一致 [23]。

把严格匹配（EM+EX）与 FINCH Score 加以比较，可以看出 FINCH 对部分正确具有更细的敏感度。模型经常生成句法正确、结构上也忠实的 SQL 查询，但其中有小的错位，例如用了错误的聚合函数、把不等关系换成相等关系，或采用略有改动的过滤条件。FINCH 的加权设计针对这一点，优先考虑 SELECT、WHERE 和 JOIN 这类语义上关键的子句，同时降低 ORDER BY 或 LIMIT 这类外围子句的权重。这种加权更符合查询在金融实践中的真实效用：子句层面的精度，决定监管比率、流动性风险度量或投资组合敞口是否被正确计算。

### 4.2 错误在 SQL 子句上的分布

子句层面的结果（表 4）显示出所有被评测模型共有的系统性不足。错误最集中于 SELECT、FROM 和 WHERE 子句，而正确的模式落地在这些子句上最为关键。相比之下，GROUP BY、HAVING 和 ORDER BY 子句上的表现略好，但仍然远不可靠。这些发现说明，模型能够复现 SQL 句法，却仍然难以把自然语言查询在语义上映射到复杂的数据库模式。这一挑战与先前关于模式链接和组合泛化的研究一致 [5, 20]。

按查询难度分层后，模型呈现出明显的性能梯度。例如，GPT-OSS-120B 在易查询上的 FINCH Score 为 26.5%，但准确率急剧下降到中等查询的 10.6%，难查询则只有 4.5%。这一模式表明，当前的大语言模型无论参数规模如何，都难以处理组合推理和多表连接，而精确理解模式在这里必不可少。

总体来看，有三点尤为突出。第一，领域专门的微调重于单纯扩大规模：Arctic-Text2SQL 的表现说明，把模型裁剪到金融 SQL 上是有益的。第二，对模式敏感的子句仍然是瓶颈，大多数错误集中在 SELECT、FROM 和 JOIN。第三，FINCH Score 比传统指标更忠实地衡量查询的效用，因为它承认精确匹配所忽略的部分成功。这些结果合在一起，既表明已经取得的进展，也表明缺口仍然存在：大语言模型在捕捉 SQL 结构方面日益有效，但它们在金融数据库上的推理，距离人类水平的可靠性仍然很远。

## 5 结论与未来工作

在本工作中，我们引入 FINCH。它是大规模的金融 Text-to-SQL 基准，把多个开源资源合并为一个统一的、专门面向金融的数据集，在 33 个数据库上包含超过 86,000 条自然语言–SQL 对。与数据集一起，我们提出 FINCH 分数。相对于传统指标，这一具有金融意识的评测指标更好地捕捉子句敏感性、执行容差和领域相关性。我们在多种大语言模型和推理模型上的基准研究给出三点关键认识：（i）领域专门的微调，如 Arctic-Text2SQL-R1-7B 所示，常常超过甚至万亿参数规模模型的表现；（ii）模型的大多数错误集中在 SELECT、FROM 和 WHERE 这类对模式敏感的子句上，说明模式落地的挑战仍然存在；（iii）当前模型从易查询到中等查询和难查询时准确率陡降，显示出它们在组合推理和多表推理上的局限。未来工作包括把金融文本、表格和 SQL 做多模态整合，做稳健的模式链接，以及面向分析师迭代工作流的对话式 Text-to-SQL。我们把 FINCH 及其定制指标，设想为推进可靠、领域专门的金融 Text-to-SQL 研究的基础。

## 参考文献

[1] Zhiyu Chen, Wenhu Chen, Charese Smiley, Sameena Shah, Iana Borova, Dylan Langdon, Reema Moussa, et al. 2021. FinQA：面向金融数据的数值推理数据集. ArXiv abs/2109.00122 (2021).

[2] Zhiyu Chen, SHIYANG LI, Charese Smiley, Zhiqiang Ma, Sameena Shah, and William Yang Wang. 2022. ConvFinQA：探索对话式金融问答中的数值推理链. In Conference on Empirical Methods in Natural Language Processing.

[3] Hao Deng, Kai Xu, Tao Yu, and Ming Zhou. 2024. FinText-SQL：面向金融数据库的实用 Text-to-SQL. In Proceedings of the 2024 Annual Meeting of the Association for Computational Linguistics (ACL). forthcoming.

[4] Chia-Hsuan Gan, Yu Zhang, Pengjun Xie, and Yue Zhang. 2021. Natural SQL：让 SQL 更容易从自然语言规约中推断出来. In Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing (EMNLP). 9006–9018.

[5] Jiaqi Guo, Zecheng Zhan, Yan Gao, Yan Xiao, Jian-Guang Lou, Ting Liu, and Dongmei Zhang. 2019. 走向跨领域数据库中的复杂 Text-to-SQL

<!-- 原 PDF 第 7 页 -->

**表 3：** 各评测指标上的模型表现比较（准确率分数，单位为 %）。

| 准确率指标 | Qwen3-8B | Arctic-Text2SQL-R1-7B | Phi-4-mini-reasoning | GPT-OSS-20B | GPT-OSS-120B | Qwen3-235B-A22B |
| --- | --- | --- | --- | --- | --- | --- |
| 精确匹配 | 0.50 | 0.60 | 0.00 | 0.30 | 1.80 | 0.70 |
| 执行准确率 | 0.80 | 2.30 | 0.20 | 7.50 | 27.80 | 2.50 |
| 组件匹配 | 3.50 | 3.70 | 1.00 | 5.20 | 16.60 | 2.80 |
| 严格准确率（EM+EX） | 0.10 | 0.20 | 0.00 | 0.30 | 1.70 | 0.20 |
| FINCH Score | 1.20 | 1.50 | 0.40 | 3.00 | 11.60 | 1.20 |

**表 4：** SQL 子句表现比较（准确率分数，单位为 %）。

| 模型 | SELECT | FROM | WHERE | GROUP BY | HAVING | ORDER BY | LIMIT |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen3-8B | 1.60 | 3.90 | 0.90 | 4.80 | 2.20 | 1.40 | 38.20 |
| Arctic-Text2SQL-R1-7B | 2.50 | 3.60 | 0.70 | 4.70 | 1.00 | 1.30 | 42.70 |
| Phi-4-mini-reasoning | 2.00 | 2.30 | 0.40 | 2.10 | 1.30 | 0.40 | 27.60 |
| GPT-OSS-20B | 1.40 | 6.20 | 1.50 | 8.40 | 3.70 | 1.50 | 65.20 |
| GPT-OSS-120B | 4.70 | 27.30 | 6.90 | 7.50 | 6.30 | 6.30 | 73.80 |
| Qwen3-235B-A22B | 2.00 | 2.90 | 0.80 | 5.40 | 1.50 | 1.00 | 29.80 |
| 平均准确率 | 2.37 | 7.37 | 1.87 | 5.48 | 2.67 | 1.98 | 46.55 |

（[5] 续）借助中间表示。题目全文为：借助中间表示，走向跨领域数据库中的复杂 Text-to-SQL. In Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics (ACL). Florence, Italy, 4524–4535. doi:10.18653/v1/P19-1444

[6] Rohan Gupta, Arjun Mehta, and Debanjan Saha. 2024. NL2PY2SQL：经由 Python 风格的中间表示连接自然语言与 SQL. In Proceedings of the 2024 Annual Meeting of the Association for Computational Linguistics (ACL). 11234–11247.

[7] Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, et al. 2022. 训练计算最优的大语言模型. arXiv preprint arXiv:2203.15556 (2022).

[8] International Financial Reporting Standards (IFRS) Foundation. 2018. 财务报告概念框架. Available at https://www.ifrs.org/issued-standards/list-of-standards/conceptual-framework/.

[9] Jared Kaplan, Sam McCandlish, Tom Henighan, et al. 2020. 神经语言模型的缩放定律. arXiv preprint arXiv:2001.08361 (2020).

[10] Takeshi Kojima, Shixiang Gu, Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa. 2022. 大语言模型是零样本推理者. arXiv preprint arXiv:2205.11916 (2022).

[11] Rahul Kumar, Amar Raja Dibbu, Shrutendra Harsola, Vignesh T. Subrahmaniam, and Ashutosh Modi. 2024. BookSQL：面向会计领域的大规模 Text-to-SQL 数据集. ArXiv abs/2406.07860 (2024).

[12] Yifei Lan, Xiao Li, Pengcheng Yin, Tao Yu, and Graham Neubig. 2022. UniRPG：把表格与文本上的统一离散推理当作程序生成. In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (ACL). 6824–6839.

[13] Fangyuan Lei, Qian Li, and Tao Yu. 2020. 追踪 Text-to-SQL 模型中的知识. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP). 2100–2112.

[14] Jinyang Li, Binyuan Hui, Ge Qu, Binhua Li, Jiaxi Yang, Bowen Li, Bailin Wang, Bowen Qin, et al. 2023. 大语言模型能否已经充当数据库接口？面向大规模、以数据库为根基的 Text-to-SQL 的大型基准（BIg Bench）. ArXiv abs/2305.03111 (2023).

[15] Yuxuan Li, Wenhu Chen, Tao Yu, and Caiming Xiong. 2025. DCG-SQL：面向 Text-to-SQL 模式链接的深度上下文图学习. In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing (EMNLP). forthcoming.

[16] Haoran Liu, Qiang Sun, Min Zhao, and et al. 2024. NL2PY2SQL：经由 Python 中间表示生成复杂 Text-to-SQL 的两步框架. Future Internet 17, 1 (2024), 12.

[17] Benjamin Nye, Chenguang Wang, Shubham Shah, Yiming Yang, and Regina Barzilay. 2021. 把非结构化内容加以结构化：事件时间线构建的联合推断. In Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing (EMNLP). 5306–5318.

[18] Mohammad Pourreza and Davood Rafiei. 2023. DIN-SQL：带自校正的 Text-to-SQL 分解式上下文学习. In Proceedings of the 2023 Annual Conference of the Association for Computational Linguistics (ACL). 3204–3219.

[19] Yujia Qin, Wenhu Chen, Yushi Yang, Michihiro Yasunaga, Xing Yue, Xiang Ren, William Wang, and Rui Zhang. 2021. 面向财务报告的神经符号推理. In Findings of the Association for Computational Linguistics: EMNLP 2021. 894–906.

[20] Torsten Scholak, Nathan Schucher, and Dzmitry Bahdanau. 2021. PICARD：为语言模型的约束自回归解码做增量解析. ArXiv abs/2109.05093 (2021).

[21] Yanan Shen, Yulong Chen, Xi Victoria Li, and William Wang. 2023. 面向企业数据库的稳健 Text-to-SQL 解析：挑战与基准. In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (EMNLP). 5634–5647.

[22] Peng Shi, Yun Cao, Xinyun Chen, and Maosong Sun. 2021. 学习在跨领域 Text-to-SQL 上泛化. In Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics (ACL). 1770–1781.

[23] Yuan Tian, Daniel Lee, Fei Wu, Tung Mai, Kun Qian, Siddhartha Sahai, Tianyi Zhang, and Yunyao Li. 2025. 借助人类与大语言模型协同标注数据，实现 Text-to-SQL 的领域适应. In Proceedings of the 30th ACM Conference on Intelligent User Interfaces (IUI ’25).

[24] Bailin Wang, Richard Shin, Xiaodong Liu, Oleksandr Polozov, and Matthew Richardson. 2019. RAT-SQL：面向 Text-to-SQL 解析器的关系感知模式编码与链接. In Annual Meeting of the Association for Computational Linguistics.

[25] Lei Wang, Yuchen Zhou, Chengyu Li, and et al. 2025. DCG-SQL：用深度上下文模式链接图增强 Text-to-SQL 的上下文学习. arXiv preprint arXiv:2503.08142 (2025).

[26] Xin Wang, Rui Zhang, Yujia Qin, and Jianshu Chen. 2025. RTS：带弃答与人在回路核验的可靠 Text-to-SQL. In Proceedings of the 2025 International Conference on Learning Representations (ICLR). forthcoming.

[27] Jason Wei, Xuezhi Wang, Dale Schuurmans, et al. 2022. 思维链提示激发大语言模型中的推理. arXiv preprint arXiv:2201.11903 (2022).

[28] Albert Wong, Dakota Joiner, Chunyin Chiu, Mohamed Elsayed, Keegan Pereira, Youry Khmelevsky, and Joe Mahony. 2021. 数据查询系统中自然语言处理实现综述. In 2021 IEEE International Conference on Recent Advances in Systems Science and Engineering (RASSE). IEEE, 1–8.

[29] Xiaojun Xu, Chang Liu, and Dawn Xiaodong Song. 2017. SQLNet：无需强化学习，从自然语言生成结构化查询. ArXiv abs/1711.04436 (2017).

[30] Zhen Yang, Junyi Li, Fangyuan Chen, and Graham Neubig. 2025. TrustSQL：提升高风险领域中 Text-to-SQL 系统的可靠性. In Proceedings of the 2025 Conference of the North American Chapter of the Association for Computational Linguistics (NAACL). forthcoming.

[31] Shunyu Yao, Dian Yang, Karthik Narasimhan Cui, et al. 2023. ReAct：在语言模型中协同推理与行动. In International Conference on Machine Learning (ICML).

<!-- 原 PDF 第 8 页 -->

[32] Tao Yu, Rui Zhang, He Yang Er, Suyi Li, Eric Xue, Bo Pang, Xi Victoria Lin, Yi Chern Tan, et al. 2019. CoSQL：迈向数据库跨领域自然语言接口的对话式 Text-to-SQL 挑战. ArXiv abs/1909.05378 (2019).

[33] Tao Yu, Rui Zhang, Kai-Chou Yang, Michihiro Yasunaga, Dongxu Wang, Zifan Li, et al. 2018. Spider：面向复杂的跨领域语义解析与 Text-to-SQL 任务的大规模人工标注数据集. ArXiv abs/1809.08887 (2018).

[34] Tao Yu, Rui Zhang, Michihiro Yasunaga, Yi Chern Tan, Xi Victoria Lin, Suyi Li, Heyang Er, Irene Li, Bo Pang, Tao Chen, et al. 2019. Sparc：上下文中的跨领域语义解析. arXiv preprint arXiv:1906.02285 (2019).

[35] Chao Zhang, Yuren Mao, Yijiang Fan, Yu Mi, Yunjun Gao, Lu Chen, Dongfang Lou, and Jinshu Lin. 2024. FinSQL：面向金融分析、与模型无关的基于大语言模型的 Text-to-SQL 框架. Companion of the 2024 International Conference on Management of Data (2024).

[36] Rui Zhang, Tao Yu, Huan Sun Er, Xi Victoria Lin, Suyi Li, Heyang Chen, Xinyun Li, Srinivasan Iyer, Michihiro Yasunaga, and Shreya Wang. 2019. 面向跨领域、依赖上下文的问题的基于编辑的 SQL 查询生成. In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP). 5338–5349.

[37] Victor Zhong, Caiming Xiong, and Richard Socher. 2017. Seq2SQL：用强化学习从自然语言生成结构化查询. ArXiv abs/1709.00103 (2017).

[38] Yichao Zhou, Haitian Sun, Wenhu Chen, Caiming Xiong, and Tao Yu. 2022. 在真实的数据库模式上评估 Text-to-SQL 系统. In Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing (EMNLP). 8965–8980.

[39] Fengbin Zhu, Wenqiang Lei, Youcheng Huang, Chao Wang, Shuo Zhang, Jiancheng Lv, Fuli Feng, and Tat seng Chua. 2021. TAT-QA：金融中表格与文本混合内容上的问答基准. In Annual Meeting of the Association for Computational Linguistics.

<!-- 译完 -->
