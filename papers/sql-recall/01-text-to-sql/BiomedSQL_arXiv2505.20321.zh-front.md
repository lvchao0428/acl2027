> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文标题：** BiomedSQL: Text-to-SQL for Scientific Reasoning on Biomedical Knowledge Bases

**作者：** Mathew J. Koretsky、Maya Willey、Owen Bianchi、Chelsea X. Alvarado、Tanay Nayak、Nicole Kuznetsov、Sungwon Kim、Mike A. Nalls、Daniel Khashabi、Faraz Faghri。单位：Center for Alzheimer’s and Related Dementias, NIA, NIH；DataTecnica LLC；Johns Hopkins University；Laboratory of Neurogenetics, NIA, NIH。通讯作者 Koretsky（mathew@datatecnica.com）。

**场合：** COLM 2026 会议论文。页脚同时标 arXiv:2505.20321v6 [cs.CL]，2026 年 8 月 12 日。

**PDF：** `BiomedSQL_arXiv2505.20321.pdf`

## 摘要

生物医学研究者已经依赖大规模结构化库做复杂分析，但现有 text-to-SQL 很难把定性的科学问题写成可执行 SQL，尤其当问题里藏着领域推理时。作者提出 BiomedSQL，并称为第一个专门评测“在真实生物医学知识库上做科学推理”的 text-to-SQL 基准。

规模与底座：68,000 条 question / SQL query / answer 三元组，由模板生成，落到一个经过整合的 BigQuery 库上。库里接了基因–疾病关联、来自组学数据的因果推断，以及药物批准记录。每道题要求模型自己推出领域标准，例如全基因组显著性阈值、效应方向、试验阶段过滤，而不是只做句法对译。

评测覆盖开源与闭源 LLM，以及不同提示和交互方式。摘要里的数字：基线提示下 Gemini-3-Pro 的 execution accuracy 为 58.1%；作者的多步 agent BMSQL 为 62.6%；专家基线为 90.0%。基准与代码在 https://datatecnica.github.io/biomedbench-suite/biomedsql 。

## 1 Introduction

第 1 节从使用场景起笔：EHR、高通量检测和人群研究已经把生物医学研究变成日常查库。自然语言接口本应降低门槛，但多数系统把生成 SQL 当成句法翻译，schema 里看不见的科学惯例一出现就失效。文中的问法是 “What SNPs are most significantly associated with Alzheimer’s disease?” 和 “What drugs target genes up-regulated in Parkinson’s disease?”。这些问句依赖统计阈值、药物批准路径和跨模态因果推断。全基因组显著性切点、试验阶段过滤、效应量解释，都不是表结构本身能读出来的。

对照基准被分成两类并都判为不够。通用基准 SPIDER（Yu et al., 2018）和 BIRD（Li et al., 2023）推进了领域，但不评测复杂领域里的科学推理。面向 EHR 的基准（Wang et al., 2020; Lee et al., 2022）强调时间逻辑或患者检索，没有单独、严格地测大规模库上的科学推理，例如推出显著性阈值，或像分析师那样跨本体做多步过滤。

BiomedSQL 的构造主张写在本节：68,000 条三元组，模板来自领域专家撰写并核过的 40 道独特问题；选题标准是对真实研究有用，且能用结构化数据回答。查询可在公开的整合 BigQuery 上执行，数据源覆盖基因–疾病关联、多组学因果推断和药物批准记录，并由日常使用这些数据的专家确认是当时较新的版本。每题都要把带细微差别的定性科学语言收成可执行 SQL。

图 1 给出评测流程：模型看到问题和 schema，生成 SQL，执行后再把结果收成自然语言回答。图中的例子是 “Are there any C9orf72 gene mutations that increase the risk of Parkinson’s disease?”，生成的 SQL 从 `biomedsql.PD_GWAS` 取出 SNP、p、b、gene，条件为 `gene = 'C9orf72' AND p < 5e-08 AND b > 0`，按 p 降序。图中还印出 Alzheimer’s Disease GWAS 为 21M rows × 13 cols，并标到 Table 10。`p < 5e-08` 与 `b > 0` 就是摘要所说的显著性阈值和效应方向，本节没有再解释阈值来源。

本节重复的结果数字与摘要一致：Gemini-3-Pro 58.1%，BMSQL 62.6%，专家 90%。贡献三条：(a) 68,000 条增强三元组的基准；(b) 放出 BigQuery 库、专家 gold 查询、执行结果和评测工具；(c) 比较模型、提示风格和交互范式，包括自建的 BMSQL，相对领域专家有 25–30 个百分点的差距。本节没有结果表。

## 2 Related Work

第 2 节把相关工作分成四条，最后用表 1 把“为什么现有基准替不了 BiomedSQL”收成可核对的列。

**General-purpose text-to-SQL benchmarks。** Seq2SQL（Zhong et al., 2017）面向简单单表。SPIDER 用 200 个多表数据库把泛化变成问题，并催生 schema linking。KaggleDBQA（Lee et al., 2021）和 BIRD（Li et al., 2023）加入企业级数据，要求处理数据质量、连接和延迟。即便如此，通用基准上最好模型的 execution accuracy 仍比人低 15–20%（以 BIRD 为例）。作者的分界是：这些基准测的是句法翻译和 schema 泛化，不是科学查询背后的推理。BiomedSQL 用带领域语义的多表 schema，要求解释统计惯例和生物医学本体。

**Text-to-SQL benchmarks for clinical databases。** MIMICSQL（Wang et al., 2020）是 MIMIC-III 上的合成 SQL，schema 窄。EHRSQL（Lee et al., 2022）更真实：从临床人员众包 1,000+ 条自然语言查询，覆盖 MIMIC-III 和 eICU，难点是时间逻辑和数据稀疏。后续数据集把查询分散到关系、文档和图模型（Sivasubramaniam et al., 2024）。这些工作测的是以患者为中心、依赖 schema 的检索。BiomedSQL 对的是研究发现：显著性阈值、多组学关联、药物–基因–疾病关系，这些都是 schema 里没有写明的推理。

**Evaluating scientific reasoning in NLP。** SciFact（Wadden et al., 2020）和 EntailmentBank（Dalvi et al., 2021）测的是文本证据上的主张验证和多步推理。Chain-of-Thought（Wei et al., 2022）和 ReAct（Yao et al., 2023）改善了多步推理，包括生物医学场景。结构化数据一侧被点到 SQL-R1（Ma et al., 2026）和 Science Hierarchography（Gao et al., 2025）。作者认为模型和生物医学的严谨、安全、可解释标准仍未对齐。BiomedSQL 的位置是：在大型生物医学知识库的 text-to-SQL 里，看模型能否把统计阈值、本体消解和复杂过滤真正写进 SQL。

**Benchmark comparison。** 四条独特点：三元组数量最大；平均 SQL 长度处于最长之列，仅次于 EHRSQL；目标是科学推理而不是 schema 翻译；同时评生成的 SQL 和自然语言回答。文中还称它是唯一测“超出 schema 本身的推理”的生物医学专用基准，也是唯一使用云原生方言 BigQuery 的一个。

表 1 的列是：问题数、查询数、平均 token、Knowledge、Template、Scientific Reasoning、NL Response、BigQuery。印出的数字如下（✓/✗ 按表中顺序对应后五列）：

| 数据集 | 问题数 | 查询数 | 平均 token | Knowledge | Template | Scientific Reasoning | NL Response | BigQuery |
| --- | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| MIMICSQL (Wang et al., 2020) | 10,000 | 10,000 | 57.4 | ✗ | ✓ | ✗ | ✗ | ✗ |
| EHRSQL (Lee et al., 2022) | 24,000 | 24,000 | 109.9 | ✗ | ✓ | ✗ | ✗ | ✗ |
| SM3 (Sivasubramaniam et al., 2024) | 10,000 | 40,000 | 26.1 | ✗ | ✓ | ✗ | ✗ | ✗ |
| BIRD (Li et al., 2023) | 12,751 | 12,751 | 50.6 | ✓ | ✗ | ✗ | ✗ | ✗ |
| BiomedSQL | 68,227 | 68,227 | 96.4 | ✓ | ✓ | ✓ | ✓ | ✓ |

摘要和第 1 节写的是约 68,000，表 1 的精确数是 68,227。平均长度上 EHRSQL 为 109.9，BiomedSQL 为 96.4，与“仅次于 EHRSQL”一致。第 2 节到表 1 结束。库如何建、40 道种子题如何标注，从第 3 节 BiomedSQL Construction 起，此处不展开。
