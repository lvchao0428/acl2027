> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名：** `BiomedSQL_arXiv2505.20321.pdf`

**原文标题：** BiomedSQL: Text-to-SQL for Scientific Reasoning on Biomedical Knowledge Bases

**作者：** Mathew J. Koretsky、Maya Willey、Owen Bianchi、Chelsea X. Alvarado、Tanay Nayak、Nicole Kuznetsov、Sungwon Kim、Mike A. Nalls、Daniel Khashabi、Faraz Faghri。机构为 Center for Alzheimer’s and Related Dementias, NIA, NIH；DataTecnica LLC；Johns Hopkins University；Laboratory of Neurogenetics, NIA, NIH。Koretsky 为通讯作者。

**场合：** Published as a conference paper at COLM 2026。首页同时印有 arXiv:2505.20321v6 [cs.CL]，2026 年 8 月 12 日。

## 摘要

生物医学研究越来越依赖大规模结构化库，但现有 text-to-SQL 很难把定性的科学问题写成可执行 SQL，尤其当问题里藏着领域推理时。BiomedSQL 被定义为第一个专门评测这件事的基准：在真实生物医学知识库上，看模型能不能做科学推理，而不只是做句法翻译。规模是由模板生成的 68,000 条 question / SQL query / answer 三元组，落在一个整合过的 BigQuery 库上，库里包括基因–疾病关联、组学数据上的因果推断，以及药物批准记录。每道题都要求模型自己补上领域标准，例如全基因组显著阈值、效应方向，或临床试验分期过滤。

评测覆盖开源和闭源 LLM，以及不同提示和交互方式。摘要里已经给出的主结果是：基线提示下 Gemini-3-Pro 的 execution accuracy 为 58.1%；作者的多步代理 BMSQL 到 62.6%；两者都明显低于专家基线 90.0%。摘要没有指向表号。基准与代码公开在 `https://datatecnica.github.io/biomedbench-suite/biomedsql`。

## 1 Introduction

第 1 节先把场景说清楚：EHR、高通量测定和人群规模研究都在往大库里灌数据，自然语言接口本来可以降低使用门槛，但现有系统把生成 SQL 当成句法翻译，一到生物医学就不成立。文中的问法是 “What SNPs are most significantly associated with Alzheimer’s disease?” 和 “What drugs target genes up-regulated in Parkinson’s disease?”。全基因组显著阈值、试验分期、效应量解释这类惯例从 schema 上看不出来。SPIDER（Yu et al., 2018）和 BIRD（Li et al., 2023）推进的是通用 text-to-SQL，并不测科学推理；面向 EHR 的基准（Wang et al., 2020; Lee et al., 2022）更强调时间逻辑或病人检索，也没有把大规模库上的科学推理单独测出来，例如推断统计显著阈值，或按本体做多步过滤。

BiomedSQL 因此被收成：68,000 条生物医学三元组，模板来自 40 道由领域专家撰写并核过的问题，这些题既要有真实研究价值，又要能用结构化数据回答。查询打在一个公开、对齐过的 BigQuery 库上，整合基因–疾病关联、多组学因果推断和药物批准记录，数据源也由日常做计算研究的专家确认是较新的版本。图 1 给出评测流程：模型看到问题和 schema，生成 SQL，执行后再把结果收成自然语言回答。图里的例子是问 C9orf72 突变是否增加帕金森病风险，生成的 SQL 含 `p < 5e-08` 和 `b > 0`；图注还标出 Alzheimer’s Disease GWAS 为 21M 行 × 13 列。

贡献分三条。(a) 基准：68,000 条扩增后的三元组，测真实生物医学库上的科学推理。(b) 基础设施：放出 BigQuery 库、专家撰写的 gold 查询、执行结果和评测工具。(c) 评测：多种模型、提示和交互，包括自建系统 BMSQL。第 1 节再次写出主结果，并补上一句差距：Gemini-3-Pro 的 execution accuracy 只有 58.1%，BMSQL 提到 62.6%，仍落后专家的 90%，相对领域专家有 25–30 个百分点的差距。这两句没有指向表号。

## 2 Related Work

第 2 节把相关工作分成四股，最后用表 1 做横向对照。论证落点始终是：已有基准测的是句法翻译或病人检索，BiomedSQL 要测的是 schema 里写不出来的科学惯例。

**General-purpose text-to-SQL benchmarks。** Seq2SQL（Zhong et al., 2017）处理简单单表查询。SPIDER（Yu et al., 2018）用 200 个多表库把泛化做成主要困难，并推动 schema linking。KaggleDBQA（Lee et al., 2021）和 BIRD（Li et al., 2023）再加入企业规模数据，要求注意数据质量、连接和延迟。作者引用的现状是：在 BIRD 这类通用基准上，最好的模型执行准确率仍比人低 15–20%。这些基准强调句法翻译和 schema 泛化，不强调科学领域里查询背后的推理。对照句是：BiomedSQL 用带领域语义的多表 schema，要求模型解释统计惯例和生物医学本体。

**Text-to-SQL benchmarks for clinical databases。** MIMICSQL（Wang et al., 2020）是 MIMIC-III 上的合成 SQL 基准，schema 窄。EHRSQL（Lee et al., 2022）更接近真实：从临床医生众包了 1,000 条以上自然语言查询，覆盖 MIMIC-III 和 eICU，难点在时间逻辑和数据稀疏。后续数据集把关系、文档和图数据模型都纳入（Sivasubramaniam et al., 2024）。作者把这一脉概括成以病人为中心的检索，测的是 schema 相关的查询映射。BiomedSQL 转向研究发现：要会用显著阈值、合并多组学关联、解开药物–基因–疾病关系。

**Evaluating scientific reasoning in NLP。** SciFact（Wadden et al., 2020）和 EntailmentBank（Dalvi et al., 2021）测的是文本上的科学主张核验和多步推理。Chain-of-Thought（Wei et al., 2022）和 ReAct（Yao et al., 2023）在通用和生物医学的多步推理上有帮助。结构化数据一侧，SQL-R1（Ma et al., 2026）和 Science Hierarchography（Gao et al., 2025）评的是本体和关系程序上的 LLM 推理。作者认为，模型和生物医学所要求的严谨、安全、可解释仍然对不齐。BiomedSQL 的接法是：在大型生物医学知识库的 text-to-SQL 里，看模型能否推断并落实统计阈值、本体消解和复杂过滤。

**Benchmark comparison。** 表 1 把 BiomedSQL 和近期基准对齐。正文给出的四点独特之处是：question / SQL / answer 三元组数量最多；平均 SQL 长度处于很长的一档，仅次于 EHRSQL；明确针对科学推理而不是 schema 翻译；同时评生成的 SQL 和自然语言回答。另外两句是：它是唯一在生物医学领域里测试“超出 schema 本身”的推理的基准，也是唯一使用云原生方言 BigQuery 的。表 1 的列是问题数、查询数、平均 token，以及 Knowledge、Template、Scientific Reasoning、NL Response、BigQuery 五个是否项：

| 数据集 | 问题数 | 查询数 | 平均 token | Knowledge | Template | Scientific Reasoning | NL Response | BigQuery |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MIMICSQL | 10,000 | 10,000 | 57.4 | 否 | 是 | 否 | 否 | 否 |
| EHRSQL | 24,000 | 24,000 | 109.9 | 否 | 是 | 否 | 否 | 否 |
| SM3 | 10,000 | 40,000 | 26.1 | 否 | 是 | 否 | 否 | 否 |
| BIRD | 12,751 | 12,751 | 50.6 | 是 | 否 | 否 | 否 | 否 |
| BiomedSQL | 68,227 | 68,227 | 96.4 | 是 | 是 | 是 | 是 | 是 |

正文多处写 68,000，表 1 印出的是 68,227。EHRSQL 在正文里写的是众包 1,000 条以上查询，表 1 的问题数和查询数都是 24,000。第 2 节在表 1 后结束，库的构建从第 3 节 BiomedSQL Construction 起，此处不展开。
