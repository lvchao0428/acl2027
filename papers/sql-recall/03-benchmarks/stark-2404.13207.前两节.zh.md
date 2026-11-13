> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

原文件名：stark-2404.13207.pdf

原文标题：STARK: Benchmarking LLM Retrieval on Textual and Relational Knowledge Bases

作者：Shirley Wu\*§、Shiyu Zhao\*§、Michihiro Yasunaga§、Kexin Huang§、Kaidi Cao§、Qian Huang§、Vassilis N. Ioannidis†、Karthik Subbian†、James Zou‡§、Jure Leskovec‡§（§ 为 Stanford University 计算机系，† 为 Amazon。\* 为共同第一作者，‡ 为共同资深作者。通讯邮箱为 shirwu、jamesz、jure@cs.stanford.edu）

场合：38th Conference on Neural Information Processing Systems (NeurIPS 2024) Track on Datasets and Benchmarks。亦为 arXiv:2404.13207v3 [cs.IR]，2024 年 10 月 20 日。项目页 https://stark.stanford.edu/

## 摘要

复杂产品搜索这类真实查询，往往要从半结构化知识库里检索：一边是非结构化文本，例如商品描述，一边是结构化关系，例如商品之间的实体关系。以往工作常把文本检索和关系检索分开做。STARK（Semi-structure retrieval benchmark on Textual and Relational Knowledge Bases）把两者放进同一套大规模基准，覆盖三个领域：商品搜索、学术论文搜索、精准医学查询。

作者设计了一条流水线，合成同时带多样关系信息和复杂文本属性的用户查询，并配上作为答案的物品。合成查询经过严格人工评估；基准里还加入高质量的人工编写查询，作为真实参照。STARK 用来测试由 LLM 驱动的检索系统。实验表明，现有检索系统和 LLM 在这上面困难很大，需要更能处理半结构化检索的系统。具体模型结果在第 3 节，不在本导读范围。

## 1 Introduction

自然语言是人获取信息的主要形式。电商用户会把自由描述和约束写在一起，例如找一辆 Radio Flyer 的推行三轮车，既好玩又要让孩子安全；医学研究者会问与 PNPLA8 基因相关、并以肌张力低下为症状的疾病。答对这类问题关系到体验、决策，以及减少幻觉。支撑它们的是半结构化知识库（SKB）：把非结构化描述和知识图谱上的实体关系放在一起，例如三轮车的文字说明加上 “品牌是 Radio Flyer”。SKB 因此用在电商、社交媒体和精准医学里。

先前工作要么做纯文本、非结构化知识上的查询，要么做结构化 SQL 或知识图谱查询，知识范围有限，盖不住 SKB 上的检索难度。LLM 在信息检索上已显示出潜力，但用在 SKB 检索上效果如何仍是开放问题。现有工作又多集中在 Wikipedia 这类通用知识，而知识常常来自私有来源，检索系统要能在私有 SKB 上工作。缺口就是：面对可能涉及私有知识、同时带复杂文本要求和关系要求的查询，现有 LLM 检索系统怎么处理。

STARK 要解决的技术难点是怎样在 SKB 上准确模拟用户查询。文本信息和关系信息互相依赖，从数百万候选里精确构造标准答案很难，查询还得有用、像真实场景。流水线在三个由大量文本和数百万实体关系建成的公开 SKB 上模拟查询并构造标准答案，再用自然度、多样性和实用性做分析和人工评估。引言写明另加入 274 条人工查询，用来和合成查询对比、并丰富测试场景（第 2.6 节的计数见下）。Figure 1 把流程画成：在 SKB 上检索，答案是节点实体；大量问答来自模拟用户，少量来自人工，用来评 LLM 检索系统。三个被强调的特点是：查询听起来自然，Table 1 给出三个子集的例子，关系信息和文本属性都有，问法灵活，还可以带额外上下文；查询要求随语境推理，例如 “我有一打 2.5 英寸的 Brybelly 空气曲棍球饼，想找配套的击球器” 意味着用户在找互补商品，还要能读专业领域描述、并推出查询里多个对象之间的关系；领域覆盖商品推荐、论文搜索和精准医学。引言最后说，在拥有数百万实体或关系的大规模 SKB 上，同时处理文本与关系、以及延迟，都是挑战。

## 2 Benchmarking Retrieval Tasks over Textual and Relational Knowledge

**2.1 问题定义。** SKB 由知识图谱 \(G=(V,E)\) 和自由文本集合 \(D\) 组成。\(V\) 是节点，\(E\subseteq V\times V\) 是关系。\(D=\bigcup_{i\in V} D_i\)，\(D_i\) 是挂在节点 \(i\) 上的文档。电商里，图可以连产品与品牌、颜色、类别，文档则是描述和评论。给定 \(G\)、\(D\) 和查询 \(Q\)，输出节点集合 \(A\subseteq V\)：每个答案节点既满足 \(Q\) 在图结构上提出的关系要求，其文档 \(D_i\) 也满足 \(Q\) 的文本要求。

**2.2 三个 SKB。** Figure 2 展示结构，Table 2 给出规模。STARK-AMAZON：4 种实体（product、brand、color、category），5 种关系（产品之间的 also_bought、also_viewed，以及 has_brand / has_color / has_category），平均度 18.2，实体 1,035,542，关系 9,443,802，token 592,067,882。产品文本由 Amazon Product Reviews 和 Amazon Q&A Data 拼成，含描述和顾客评论；其他实体用名称或标题。STARK-MAG：实体为 paper、author、institute、field_of_study，4 种关系类型，平均度 43.5，实体 1,872,968，关系 39,802,116，token 212,602,571。关系子图取自 obgn-mag，论文节点与 obgn-papers100M 共享，并保留全部非论文节点；非英文论文被滤掉。文档含标题和摘要，并接入 Microsoft Academic Graph（2019-03-22 版）的会议/期刊、作者和机构名。关系大量集中在引用和作者关系。STARK-PRIME 基于 PrimeKG：10 种实体类型（含 disease、gene/protein 等），18 种关系（如 associated_with、indication），平均度 125.2，实体 129,375，关系 8,100,498，token 31,844,769。它更密、关系类型更多。疾病和药物的文本来自 PrimeKG；gene/protein 和 pathway 再从多个数据库补基因组位置、基因活性摘要和通路同源事件。可在 https://stark.stanford.edu/skb_explorer.html 浏览。

**2.3 三个检索任务。** Table 3 中，合成集的训练/验证/测试查询总量在 9k 到 14k，另有人工查询集，只用于测试。STARK-AMAZON 做商品推荐：合成查询 9,100 条，其中 7,082 条有多个答案，平均答案数 17.99，划分比例 0.65 / 0.17 / 0.18；正文另写约 68% 的合成查询有不止一个标准答案。它强调质量、功能和风格等面向顾客的文本，并加入单跳关系（品牌、类别、互补或替代商品），问法像对话。STARK-MAG 做论文搜索：13,323 条，6,872 条多答案，平均 2.78 个答案，划分 0.60 / 0.20 / 0.20。它把文本要求与多跳关系合在一起，例如 “King’s College London 的论文” 对应 institution → author → paper；模板是 3 个单跳加 4 个多跳，文本侧重主题、方法和贡献。STARK-PRIME 做复杂生物医学提问：11,204 条，4,188 条多答案，平均 2.56 个答案，划分 0.55 / 0.20 / 0.25。合成查询用 28 个多跳模板，例如 “靶向 \<anatomy\> 中基因或蛋白的药物是什么”。药物、疾病、基因/蛋白和通路是关系加文本；effect/phenotype 等因文本有限，查询只靠关系。药物和疾病的问法模拟 medical scientist、doctor、patient 三种角色。

**2.4–2.6 构造与质量。** Figure 3 的合成流水线在生成时把关系和文本缠在一起，过滤答案时再拆开，共四步。先按专家模板抽样关系要求，例如 “(a product) belongs to \<brand\>”，落到具体品牌 “belongs to Radio Flyer”，得到候选实体。再从候选里随机抽一个金答案，让 LLM 按其角色兴趣从文档里抽文本属性，例如功能和体验。然后用两个 LLM 把文本属性和关系要求合成查询，以免单模型偏差：第一个写得自然、符合角色和文体（例如 ArXiv 检索），第二个补充上下文并改写，使理解需要更强推理。最后用多个 LLM 检查第一步的候选是否满足抽出的文本属性，全部通过才进入标准答案。金答案被核验通过的平均比例，三个数据集上为 86.6%、98.9% 和 92.3%；这一句没有逐一写出对应哪一个数据集。提示和模型版本在附录。

分布上，Figure 4 里多数查询大约 16 个词，最长到约 50 词，长查询常提到其他实体或给出详细上下文。STARK-AMAZON 的答案长度有长尾，约 22% 的答案超过 30 个实体。Table 4 用 Shannon Entropy 和 Type-Token Ratio 衡量词分布多样性：AMAZON 为 10.39 和 0.179，MAG 为 10.25 和 0.180，PRIME 为 9.63 和 0.143；参照是 Barack Obama 的 Wikipedia 页面，10.44 和 0.261。Figure 5 按词数比较查询里关系要求与文本要求的平均占比，三者侧重不同，但图中的具体比例正文没有写成数字，并说明占比不等于对最终答案的重要性。人工评估有 63 名参与者，从像自然对话、问题结构和复杂度是否多样、是否贴近真实场景三方面打分，5 点量表再收成正面/持平/负面；达到中性及以上的比例，自然度、多样性、实用性平均为 94.1%、85.3%、89.4%（细表在附录 Table 10）。

人工查询由 31 名参与者生成，其中 22 人是英语母语者，按附录说明和交互平台写出 263 条，再人工核对标准答案。Table 3：AMAZON 81 条（64 条多答案，平均 19.50 个答案），MAG 84 条（34 条多答案，平均 3.26），PRIME 98 条（41 条多答案，平均 2.77）。合成与人工查询的答案个数相近，说明含糊程度类似；多数人工问法在合成集里已有覆盖。Table 5 对照三类：短而直接（人工 “Red sweatshirt for proud Montreal Canadiens”，合成 “Suggestions for a Suunto bike mount?”）、指定作者与领域、以及带复杂病情上下文的长问句。差别是人工查询更常出现独特说法，例如 “fat cross and road tire that works with my Diamondback bicycle tube” 和 “this sneaky bone-killing culprit”。作者把吸收更时新、更活的说法留作后续方向。
