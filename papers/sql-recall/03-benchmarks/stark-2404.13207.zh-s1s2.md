# STARK: Benchmarking LLM Retrieval on Textual and Relational Knowledge Bases

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`stark-2404.13207.pdf`。

## Abstract 摘要

回答真实世界中的复杂查询，例如复杂商品搜索，往往需要从半结构化知识库中准确检索；这类知识库混合了非结构化信息（例如商品的文本描述）与结构化信息（例如商品的实体关系）。然而，许多先前工作把文本检索与关系检索当作彼此分开的题目来研究。为填补这一差距，我们开发 STARK，一个在文本与关系知识库上的大规模半结构化检索基准（Semi-structure retrieval benchmark on Textual and Relational Knowledge Bases）。我们的基准覆盖三个领域：商品搜索、学术论文搜索，以及精准医学中的查询。我们设计一条新的流水线，合成把多样关系信息与复杂文本属性整合在一起的真实用户查询，并给出它们的真实答案（物品）。我们进行严格的人工评估，以验证合成查询的质量。我们进一步用高质量的人工生成查询增强该基准，以提供真实参照。STARK 作为综合测试平台，用于评估由大语言模型（large language models, LLMs）驱动的检索系统的性能。实验表明，STARK 对当前的检索系统与 LLM 系统构成显著挑战，凸显了对更有能力的半结构化检索系统的需求。

## 1 Introduction 引言

自然语言查询是人类获取信息的主要形式 [17, 21, 27]。例如，电商网站上的用户希望通过组合自由形式的要素与约束来表达复杂信息需求，比如商品搜索中的 “Can you help me find a push-along tricycle from Radio Flyer that’s both fun and safe for my kid?”。医学科学家可能会问 “What disease is associated with the PNPLA8 gene and presents with hypotonia as a symptom?”。回答这类查询对于提升用户体验、支持知情决策以及防止幻觉至关重要。

要回答这类查询，底层知识可以表示在半结构化知识库（semi-structured knowledge bases, SKBs）中 [35, 40, 50]。SKB 把非结构化数据——例如自然语言描述与表达（如三轮车的描述）——与结构化数据——例如知识图谱上的实体交互（如一辆三轮车的 “brand” 是 Radio Flyer）——整合在一起。这使 SKB 能够表示特定应用中的综合知识，从而在电商 [15]、社交媒体 [31] 与精准医学 [8, 18, 23] 等领域中不可或缺。

**先前工作的局限。** 先前工作要么聚焦非结构化知识上的纯文本查询 [12, 14, 20, 24, 25, 29, 53, 55]，要么聚焦结构化的 SQL [59, 59, 60, 60] 或知识图谱查询 [2, 4, 7, 13, 16, 45–47, 57, 58]，它们在知识覆盖面上有限，不足以研究 SKB 上检索的复杂性。近来，大语言模型（LLMs）在信息检索任务上展现出显著潜力 [14, 30, 43, 61]。尽管如此，LLM 能在多大程度上有效应用于 SKB 上具有挑战性的检索任务，仍是一个开放问题。此外，现有工作主要聚焦一般知识，例如来自维基百科的知识。然而，知识常常可能来自私有来源，要求检索系统在私有 SKB 上运行。因此，当前 LLM 检索系统如何处理查询中复杂的文本要求与关系要求——这些要求可以涉及私有知识——存在差距。

**本文工作。** 为填补这一差距，我们提出大规模基准 STARK（Semi-structure retrieval benchmark on Textual and Relational Knowledge Bases）（图 1）。我们解决的关键技术挑战是如何准确地模拟 SKB 上的用户查询。这一困难来自文本信息与关系信息的相互依赖，从而导致从数百万候选中精确构造真实答案时的挑战。此外，确保查询有用并贴近真实场景，进一步增加了基准构建的复杂性。

我们开发一条新的流水线，使用三个由大量文本与来自公开来源的数百万实体关系构建的 SKB，模拟用户查询并构造精确的真实答案。我们通过详细分析与人工评估验证基准中查询的质量，重点考察其自然性、多样性与实用性。此外，我们纳入 274 条人工生成的查询，以便与合成查询比较并丰富测试场景。借助 STARK，我们更深入地研究 SKB 上的检索任务，评估当前检索系统的能力，并为未来进展提供洞见。STARK 的关键特征是：

- **SKB 上听起来自然的查询（表 1）：** 基准中的查询纳入丰富的关系信息与复杂的文本属性。此外，这些查询密切反映用户在真实场景中会自然提出的问题类型，例如查询格式灵活，并且可能带有额外上下文。
- **特定于上下文的推理：** 查询要求特定于上下文的推理能力。这包括推断顾客兴趣、理解专业领域描述，以及推导查询中提到的多个主体之间的关系。例如，上下文 “I had a dozen 2.5-inch Brybelly air hockey pucks, so I’m trying to find matching strikers.” 蕴含用户在寻找互补商品的兴趣。这类推理能力对于准确解释并回应每条查询的细微要求至关重要。
- **多样的领域：** 我们的基准跨越三个知识库，应用包括商品推荐、学术论文搜索与精准医学问询。STARK 在多样的上下文与领域中对检索系统提供综合评估。知识库浏览器见 https://stark.stanford.edu/skb_explorer.html 。

我们在 LLM 检索系统上开展广泛实验，突出处理文本与关系数据时的挑战，以及在拥有数百万实体或关系的大规模 SKB 上的延迟。最后，我们为构建更能应对真实世界复杂性的检索系统提供洞见。

图 1：STARK 的特点是在同时含文本知识与关系知识的半结构化知识库（SKB）上提出查询，并以节点实体作为真实答案。STARK 由模拟用户与 SKB 交互的合成查询，以及提供真实参照的人工生成查询组成。它评估 LLM 检索系统在给出准确回复方面的性能。

表 1：涉及半结构化（关系与文本）信息的 STARK 问答示例。真实答案以尖括号中的物品标题给出。

| 子集 | 示例查询 | 真实答案物品标题 |
| --- | --- | --- |
| STARK-AMAZON | Looking for durable Dart World brand dart flights that resist easy tearing. Any recommendations? | Amazon Standard Flights；Dart World Broken Glass Flight（另有 12 个） |
| STARK-AMAZON | What are recommended scuba diving weights for experienced divers that would fit well with my Gorilla PRO XL waterproof bag? | Sea Pearls Vinyl Coated Lace Thru Weight |
| STARK-MAG | Search publications by Hao-Sheng Zeng on non-Markovian dynamics. | Distribution of non-Markovian intervals...；Comparison between non-Markovian... |
| STARK-MAG | What are some nanofluid heat transfer research papers published by scholars from Philadelphia University? | A Numerical Study on Convection Around A Suqare Cylinder using AL2O3-H2O Nanofluid |
| STARK-PRIME | Could you provide a list of investigational drugs that interact with genes or proteins active in the epididymal region? | (S)-3-phenyllactic Acid；Anisomycin；Puromycin |
| STARK-PRIME | Search for diseases without known treatments and induce pruritus in pregnant women, potentially associated with Autoimmune. | Intrahepatic Cholestasis |
| STARK-PRIME | Please find pathways involving the POLR3D gene within nucleoplasm. | RNA Polymerase III Chain Elongation |
| STARK-PRIME | Which gene or protein associated with lichen amyloidosis can bind interleukin-31 to activate the PI3K/AKT and MAPK pathways? | OSMR；IL31RA |

（“Suqare” 按抽取原文保留。）

## 2 Benchmarking Retrieval Tasks over Textual and Relational Knowledge 在文本与关系知识上评测检索任务

### 2.1 Problem Definition 问题定义

给定一个半结构化知识库（SKB），它由知识图谱 \(G\) 与一组自由文本文档 \(D\) 组成。形式上，令 \(G = (V, E)\) 为知识图谱，其中 \(V\) 是节点集合，\(E \subseteq V \times V\) 是表示节点之间关系的边集合。文档集合在抽取文本中写为 \(D = S_{i \in V} D_i\)，即与节点相关联的自由形式文本文档的集合，其中 \(D_i\) 是与节点 \(i\) 相关联的文档集合。（并集符号在 PDF 中显示为 “S”，此处按 “对全部节点取并” 理解，不改其他符号。）例如，电商中的商品知识图谱可以捕获商品与品牌/颜色/类别之间的关系，相应文本文档包括商品描述、评论等。

我们把基准数据集上的任务定义如下：给定知识图谱 \(G = (V, E)\)、自由文本文档集合 \(D\) 与查询 \(Q\)，输出是节点集合 \(A \subseteq V\)，使得对每个节点 \(i \in A\)，它满足 \(Q\) 中所指定的、由 \(G\) 的结构施加的关系要求，并且相关联的文档 \(D_i\) 满足 \(Q\) 中指定的文本要求。

### 2.2 Semi-structured Knowledge Bases (SKBs) 半结构化知识库

如图 2 所示，我们构建三个大规模 SKB，每个实体都带有关系信息与文本信息。基本数据统计见表 2，细节见附录 A.1。

图 2：半结构化知识库的示意。每个知识库都以复杂方式同时组合文本信息与关系信息，从而使检索任务具有挑战。图中可读标签包括：Amazon 侧商品 “Ultimate Stroll 'N Tricycle”（适用年龄 1 至 5 岁，尺寸 37.2”×34.3”×22”，描述为可随儿童成长的三轮车）、颜色 Red / Pink、类别 Wooden Furniture，以及 has brand、also bought、also viewed 等关系；MAG 侧论文 “Distribution of non-Markovian intervals for open qubit systems”（摘要起句为研究开放量子比特系统的非马尔可夫性，发表日期 2011-11-01，venue 为 Chinese Physics B），以及 author、field of study、cites、institute 等关系；Prime 侧实体 GPANK1（别名 DYRK1AP3、PAHX-AP、PAHXAP1）与 GM1 gangliosidosis type I，以及 drug、gene/protein、disease、pathway、phenotype 等类型。大量重复的关系边标签未逐条列出。

表 2：所构建半结构化知识库的数据统计。表头在抽取中竖排为：实体类型数、关系类型数、平均度、实体数、关系数、token 数。

| | 实体类型数 | 关系类型数 | 平均度 | 实体数 | 关系数 | token 数 |
| --- | --- | --- | --- | --- | --- | --- |
| STARK-AMAZON | 4 | 5 | 18.2 | 1,035,542 | 9,443,802 | 592,067,882 |
| STARK-MAG | 4 | 4 | 43.5 | 1,872,968 | 39,802,116 | 212,602,571 |
| STARK-PRIME | 10 | 18 | 125.2 | 129,375 | 8,100,498 | 31,844,769 |

**Amazon 半结构化知识库。** 该 SKB 有四种实体类型：product、brand、color 与 category，以及五种关系类型：商品实体之间的 also_bought、also_viewed，以及与商品相关联的 has_brand / color / category。我们把 Amazon Product Reviews [15] 与 Amazon Q&A Data [32] 结合起来，导出商品节点的文本信息。这提供了大量文本，包括商品描述与顾客评论。对于其他实体，我们抽取其名称或标题作为文本属性。Amazon SKB 的大量文本主要来自顾客评论与问答。

**MAG 半结构化知识库。** 该 SKB 包括 paper、author、institute 与 field_of_study 等节点实体。我们通过从 obgn-mag [19] 抽取子图来导出其关系结构；该子图包含与 obgn-papers100M [19] 共享的论文节点以及全部非论文节点。（这两处名称按 PDF 文本层原文作 obgn，未改写。）我们滤除非英语论文，因为只考虑单语查询。论文文档包括标题与摘要。此外，我们整合来自 Microsoft Academic Graph 数据库（2019-03-22 版本）[44, 50] 的细节，提供论文 venue、作者与机构名称等额外文本信息。该 SKB 展示了与论文节点相关联的大量关系，尤其是引用与作者关系。

**Prime 半结构化知识库。** 我们利用现有知识图谱 PrimeKG [8]，它包含十种实体类型，包括 disease、gene/protein，以及十八种关系类型，例如 associated_with、indication。与 Amazon 和 MAG 的 SKB 相比，Prime SKB 更稠密，关系类型也更多样。虽然 PrimeKG 提供 disease 与 drug 实体的文本信息，我们还为 gene/protein 与 pathway 实体整合来自多个数据库的数据，例如基因组位置、基因活动摘要与通路直系同源事件。

### 2.3 Retrieval Tasks on Semi-structured Knowledge Bases 半结构化知识库上的检索任务

我们的检索基准（表 3）由三个新的、基于检索的问答数据集组成，每个数据集包含合成的训练/验证/测试集，查询总数为 9k 到 14k，以及一个高质量的人工生成查询集。查询综合了关系知识与文本知识，在听起来自然以及格式灵活方面反映真实世界查询。

**STARK-AMAZON。** 该任务旨在商品推荐，合成查询中有 68% 产生多于一个真实答案。数据集优先考虑面向顾客的标准，突出商品质量、功能与风格等文本要素。此外，它把单跳关系方面（附录 A.2）纳入查询，包括品牌、类别以及商品之间的联系（例如互补或替代物品）。查询以类似对话的格式表述，从而丰富上下文并增强数据集与真实场景的相关性。

**STARK-MAG。** 在 STARK-AMAZON 的单跳关系要求之外，STARK-MAG 强调把文本要求与多跳查询融合起来，以进行精确的学术论文搜索。例如，“Are there any papers from King’s College London” 突出关系结构上的元路径（institution → author → paper）。我们设计了三个单跳与四个多跳关系查询模板（附录 A.3）。文本方面聚焦论文的主题、方法与贡献等。

**STARK-PRIME。** 该任务是回答复杂的生物医学问询。对于合成查询，我们开发了 28 个多跳查询模板（附录 A.4），以覆盖各种关系类型并保证其实用相关性。例如，模板 “What is the drug that targets genes or proteins in \<anatomy\>?” 通过识别针对特定解剖部位的治疗来辅助精准医学。对于 drug、disease、gene/protein 与 pathway 实体，查询是关系要求与文本要求的混合。对于 effect/phenotype 等实体，由于文本信息有限，查询只依赖关系数据。我们展示三种不同的用户角色——医学科学家、医生与患者——来生成关于药物与疾病的查询，从而使语言多样化，以全面评估检索系统。

表 3：STARK 基准数据集的统计。人工生成部分仅用于测试。

| | 查询数 | 有多个答案的查询数 | 平均答案数 | 训练 / 验证 / 测试 |
| --- | --- | --- | --- | --- |
| 合成（第 2.4、2.5 节） | | | | |
| STARK-AMAZON | 9,100 | 7,082 | 17.99 | 0.65 / 0.17 / 0.18 |
| STARK-MAG | 13,323 | 6,872 | 2.78 | 0.60 / 0.20 / 0.20 |
| STARK-PRIME | 11,204 | 4,188 | 2.56 | 0.55 / 0.20 / 0.25 |
| 人工生成（第 2.6 节，仅测试） | | | | |
| STARK-AMAZON | 81 | 64 | 19.50 | |
| STARK-MAG | 84 | 34 | 3.26 | |
| STARK-PRIME | 98 | 41 | 2.77 | |

图 3：生成半结构化检索数据集的构建流水线。图中示例查询为 “Can you help me find a push-along tricycle from Radio Flyer that’s both fun and safe for my kid?”，并标出关系信息（例如属于 Radio Flyer）、文本属性（来自描述的 “push-along tricycle”，以及来自评论的 “fun and safe for kids”）与真实节点。

### 2.4 Benchmark Construction: Synthesized Queries 基准构建：合成查询

在图 3 中，我们提出一条新的流水线，合成 SKB 查询并自动生成真实答案。关键思想是在合成时把关系信息与文本信息缠结在一起，在答案过滤时再把它们拆开。它包括以下四步：

- **1）抽样关系要求：** 对每条查询，我们抽样一个用专家/领域知识构建的实用关系模板，例如 “(a product) belongs to \<brand\>”，并用抽样到的实体（即某个具体品牌）把它落地，例如 “belongs to Radio Flyer”。这一关系要求产生一组候选实体，即属于 Radio Flyer 的商品。
- **2）抽取文本属性：** 我们从第一步随机抽样一个候选实体，称为黄金答案，LLM 从其文本文档中抽取与特定角色（例如顾客、研究者或医生）的兴趣相一致的属性。在图 3 中，我们从一件 Radio Flyer 商品中抽取关于功能与用户体验的多项属性。
- **3）组合文本信息与关系信息：** 我们使用两个 LLM，从文本属性与关系要求合成查询，以增强多样性并减少依赖单一 LLM 所带来的偏差。第一个 LLM 专注于生成自然的、特定于角色的、风格一致的查询（例如 ArXiv 搜索）。第二个 LLM 丰富上下文并改写查询，这使得在复杂上下文下理解它们需要高级推理。
- **4）过滤额外答案：** 最后，我们使用多个 LLM 验证第一步的候选是否满足所抽取的文本属性。只有通过全部 LLM 验证的候选才被纳入最终真实答案集合。为评估这一过滤机制的精确率，我们计算黄金答案被验证通过的平均比例，在三个数据集上分别为 86.6%、98.9% 与 92.3%，说明我们在产生高质量真实答案方面是有效的。

这条数据集构建流水线是自动的、高效的，并且广泛适用于我们形式化中的 SKB。上述步骤中的全部提示与 LLM 版本见附录 E。

### 2.5 Synthesized Data Distribution Analysis and Human Evaluation 合成数据的分布分析与人工评估

- **查询与答案长度。** 查询长度（以词计）反映用户提供的上下文信息量，而答案数量表示查询的歧义性/具体性。图 4 显示各数据集的查询长度分布相似，多数查询在 16 个词左右。更长的查询（长达 50 个词）常常提到其他实体或提供详细上下文。值得注意的是，STARK-AMAZON 有显著的长尾形态，约 22% 的答案拥有超过 30 个实体，反映了多样的电商推荐与有歧义的用户查询。

图 4：STARK 数据集上查询长度与答案长度的分布。图为密度曲线，抽取文本不含各点数值。

- **查询多样性。** 多样化的查询集合对更广泛地满足不同用户需求提出挑战。我们用 Shannon Entropy 度量词分布，用 Type-Token Ratio（TTR）度量独特词。更高的值表示更大的词汇多样性。表 4 显示全部数据集上 Shannon Entropy 较高且 TTR 稳定。作为参照，我们计算了 Barack Obama 维基百科页面的这些指标（https://en.wikipedia.org/wiki/Barack_Obama）。指标定义见附录 B。

表 4：STARK 上的查询多样性度量。

| | Shannon Entropy | Type-Token Ratio |
| --- | --- | --- |
| STARK-AMAZON | 10.39 | 0.179 |
| STARK-MAG | 10.25 | 0.180 |
| STARK-PRIME | 9.63 | 0.143 |
| 参照文章 | 10.44 | 0.261 |

- **关系信息与文本信息的比例。** 基准查询的特征是文本信息与关系信息的组成。为理解信息类型的分布，我们按词数计算每个数据集中查询里关系要求与文本要求的平均比例。需要注意，这些比例并不直接反映它们在决定最终答案时的重要性。图 5 显示比例各不相同，这突出了对文本要求与关系要求的不同侧重，并挑战检索系统去适应不同分布。

图 5：关系信息与文本信息的平均相对构成。抽取文本不含各柱数值。

**人工评估。** 我们请 63 名参与者，从自然性（类似于自然对话）、多样性（覆盖各种问题结构与复杂度）与实用性（与真实情境相关）方面，对基准中抽样的查询作定性评估。评估结果由 5 点 Likert 式量表转换为正面/持平/负面量表，正面与非负面比例见表 10（附录 D.1）。平均而言，94.1%、85.3% 与 89.4% 的参与者分别在自然性、多样性与实用性上把查询评为中性或以上。这些结果验证了基准的质量及其用于多样、真实检索任务的潜力。

### 2.6 Benchmark Construction: Human-Generated Queries 基准构建：人工生成的查询

为增强基准的实际相关性，我们邀请 31 名参与者（其中 22 名以英语为母语）按照详细说明（附录 C）以及我们的交互平台，在三个 SKB 上生成 263 条查询。我们人工核验并过滤真实答案，以确保答案正确。表 3 给出人工生成数据集的统计。最后，我们分析合成查询与人工生成查询的共同点与差异。

**共同点。** 合成查询与人工生成查询的答案数量相当，表明查询歧义程度相似。此外，我们观察到人工生成查询的大多数风格已包含在合成数据集中。例如，表 5 突出了它们在短商品查询、特定作者/领域问询以及复杂上下文查询上的相似性。

**差异。** 我们发现人工生成的查询常常表现出比合成查询更独特的表达，例如 “Give me a fat cross and road tire that works with my Diamondback bicycle tube” 以及 “this sneaky bone-killing culprit”。这一发现提示，未来让基准纳入现代且动态的语言细微差别是一个方向。

表 5：人工生成查询与合成查询的比较。

| 查询类型 | 人工生成查询 | 合成查询 |
| --- | --- | --- |
| 短而直接 | Red sweatshirt for proud Montreal Canadiens | Suggestions for a Suunto bike mount? |
| 特定作者与领域 | Find me papers that discuss improving condenser performance authored by Stojan Hrnjak | Show me papers by Seung-Hyeok Kye that discuss separability criteria. |
| 复杂上下文 | Help me. I am trying to diagnose a patient with persistent joint pain, and I suspect a condition where the bone is dying due to compromised blood supply, often linked to factors like steroid use, ... what’s the name of this sneaky bone-killing culprit? | I’m experiencing joint pain accompanied by swelling... I’m concerned about medications aggravating my fuzzy eyesight and potential blood clotting complications. Could you recommend treatments while minimizing these side effects? |
