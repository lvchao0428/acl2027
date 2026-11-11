# BiomedSQL: Text-to-SQL for Scientific Reasoning on Biomedical Knowledge Bases

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`BiomedSQL_arXiv2505.20321.pdf`。

## Abstract 摘要

生物医学研究者越来越依赖大规模结构化数据库来完成复杂的分析任务。然而，现有的 text-to-SQL 系统往往难以把定性的科学问题映射为可执行的 SQL，尤其是在需要隐式领域推理时。我们提出 BiomedSQL，这是第一个明确用于评测 text-to-SQL 生成中科学推理能力的基准，其底层是一个真实世界的生物医学知识库。BiomedSQL 包含 68,000 条问题 / SQL 查询 / 答案三元组，由模板生成，并落实在一个经过协调的 BigQuery 数据库上。该数据库整合了基因–疾病关联、来自组学数据的因果推断，以及药物批准记录。每个问题都要求模型推断领域特定的标准，例如全基因组显著性阈值、效应方向或试验阶段过滤，而不是只做句法翻译。我们在多种提示策略和交互范式下评测了一系列开源与闭源 LLM。结果揭示出显著的性能差距：在基线提示下，Gemini-3-Pro 的执行准确率（execution accuracy）为 58.1%，我们定制的多步智能体 BMSQL 达到 62.6%，二者都远低于 90.0% 的专家基线。BiomedSQL 为推进 text-to-SQL 系统提供了新的基础，使这些系统能够通过对结构化生物医学知识库的稳健推理来支持科学发现。BiomedSQL 基准与代码库公开于 https://datatecnica.github.io/biomedbench-suite/biomedsql 。

## 1 Introduction 引言

现代生物医学研究日益以数据为中心。电子健康记录（electronic health records, EHRs）、高通量检测和人群规模的研究，填充着研究者每天都要查询的大型数据库。自然语言接口，尤其是 text-to-SQL 系统，有望让这些资源的获取更加普及。然而，当前大多数系统把查询生成当作句法翻译任务，把问题结构映射为 SQL 语法，而没有更深的领域理解。这种抽象在生物医学情境中会失效。领域专家经常提出这样的问题：“What SNPs are most significantly associated with Alzheimer’s disease?”（哪些 SNP 与阿尔茨海默病的关联最为显著？），或者 “What drugs target genes up-regulated in Parkinson’s disease?”（哪些药物靶向在帕金森病中上调的基因？）。这些问题立足于科学惯例，例如统计阈值、药物批准路径，以及跨模态的因果推断。这些领域特定惯例——例如全基因组显著性截止值、试验阶段过滤或效应量解释——仅从模式（schema）本身是看不见的。

尽管通用 text-to-SQL 基准（例如 SPIDER（Yu et al., 2018）、BIRD（Li et al., 2023））推动了该领域，它们并不评测复杂领域所需要的科学推理。类似地，面向 EHR 的基准（Wang et al., 2020; Lee et al., 2022）强调时间逻辑或患者检索，但并没有孤立地、严格地检验在大规模数据库上解释生物医学数据所需要的科学推理。这包括像生物医学分析人员那样，推断统计显著性阈值，或跨本体串联多步过滤逻辑。

为填补这一空白，我们提出 BiomedSQL，第一个专门用于评测生物医学领域 SQL 生成中科学推理的基准。BiomedSQL 包含 68,000 条生物医学问题 / SQL 查询 / 答案三元组，反映真实、复杂的科学查询。这些查询由 40 个独特问题模板化而来；这 40 个问题由领域专家生成并核验，既因其对真实生物医学研究的影响，也因其能够通过结构化数据来回答。它们可以在一个经过协调、公开可用的 BigQuery 数据库上执行。该数据库整合了基因–疾病关联、多组学因果推断和药物批准记录。这些数据源也由在日常计算研究中使用它们的领域专家核验为最新。BiomedSQL 中的每个问题都要求模型把细致、定性的科学语言翻译成可执行的 SQL 逻辑。

图 1 给出评测流水线的概览：我们在多种提示与交互设定下，要求各种 LLM 生成准确的 SQL 查询，并把执行结果总结为基于给定问题的简洁自然语言回答。我们在 BiomedSQL 上的评测表明，把 LLM 部署到生物医学 text-to-SQL 任务上仍有很大改进空间。表现最好的模型 Gemini-3-Pro 的执行准确率只有 58.1%。我们定制的多步智能体 BMSQL 将其提高到 62.6%，但仍落后于专家表现（90%）。我们的贡献如下：（a）基准：我们提出 BiomedSQL，包含 68,000 条增强的问题 / SQL 查询 / 答案三元组，用于在真实生物医学数据库上评测 text-to-SQL 系统的科学推理能力。（b）基础设施：我们发布 BigQuery 数据库、专家撰写的金标准查询、执行结果，以及评测工具包。（c）评测：我们评估一系列模型、提示风格和交互范式，包括一个定制的 text-to-SQL 系统（BMSQL），揭示出相对领域专家表现约 25–30 个百分点的差距。

图 1 的版面在抽取中与示例问题和结果表粘连，部分单元格【抽取不清】。可辨认的内容包括：问题 “Are there any C9orf72 gene mutations that increase the risk of Parkinson’s disease?”；生成的 SQL 为 `SELECT SNP, p, b, gene FROM \`biomedsql.PD_GWAS\` WHERE gene = 'C9orf72' AND p < 5e-08 AND b > 0 ORDER BY p DESC`；图中另有一张 Alzheimer’s Disease GWAS 表，标注为 21M rows × 13 cols，可见片段包括 SNP、A1、A2、p，以及 rs752837160、rs35718606、rs34161239 等行和 0.3405、0.9438、0.9815 等数值，中间行未完整抽出。图注原文为：图 1：用于评测 LLM 在 BiomedSQL 上表现的 text-to-SQL 工作流示例。给定问题和数据库模式，LLM 必须生成 SQL 查询，并利用其执行结果返回自然语言回答。

## 2 Related Work 相关工作

我们把相关工作组织为四条线索：（1）通用 text-to-SQL 基准；（2）面向临床数据库的 text-to-SQL 基准；（3）NLP 中科学推理的评测；（4）BiomedSQL 与先前基准的直接比较。

**通用 text-to-SQL 基准。** Text-to-SQL 研究在很大程度上由跨领域基准推动。早期工作如 Seq2SQL（Zhong et al., 2017）针对简单的单表查询引入了 SQL 生成。SPIDER（Yu et al., 2018）跨越 200 个多表数据库，扩大了泛化方面的挑战，并催生了模式链接（schema linking）技术。更近一些，KaggleDBQA（Lee et al., 2021）和 BIRD（Li et al., 2023）通过纳入企业规模的数据，并要求关注数据质量、连接和延迟，增加了真实感。尽管有所进展，在 BIRD（Li et al., 2023）这类通用基准上，顶尖模型的执行准确率仍比人类低 15–20%。这些基准强调句法翻译和模式泛化，而不是许多科学学科查询所依赖的推理。相比之下，BiomedSQL 使用富含领域特定语义的多表模式，要求模型解释统计惯例和生物医学本体——这些能力此前未被评估。

**面向临床数据库的 text-to-SQL 基准。** 已有若干工作针对 EHR 的临床数据库查询。MIMICSQL（Wang et al., 2020）在 MIMIC-III 上给出了一个合成 SQL 基准，但受限于狭窄的模式。EHRSQL（Lee et al., 2022）通过众包，从临床医生那里收集了跨越 MIMIC-III 和 eICU 的 1,000 余条自然语言查询，推进了真实感，并突出了时间逻辑与数据稀疏性方面的挑战。近期数据集把查询多样化到关系、文档和图数据模型（Sivasubramaniam et al., 2024），反映了 EHR 数据日益增加的异质性。这些基准聚焦以患者为中心的信息检索，评估把依赖于模式的查询映射出来的能力。相反，BiomedSQL 针对生物医学研究中的发现：查询需要隐式的科学推理，例如应用显著性阈值、组合多组学关联，或解析药物–基因–疾病关系，从而提供一种互补的、以推理密集的数据探索为重点的评测。

**评测 NLP 中的科学推理。** 对于需要多跳推理、证据综合和结构化决策的任务，科学推理已成为 NLP 的一个关键前沿。SciFact（Wadden et al., 2020）和 EntailmentBank（Dalvi et al., 2021）等基准评测科学主张验证，以及基于文本证据的多步推理。思维链（Chain-of-Thought）（Wei et al., 2022）和 ReAct（Yao et al., 2023）等提示技术，在一般设定和生物医学设定的多步推理任务上都展示了性能提升。更近的工作把评测扩展到结构化数据，例如 SQL-R1（Ma et al., 2026）和 Science Hierarchography（Gao et al., 2025），它们评估 LLM 在本体和关系程序上的推理。尽管有这些进展，把模型推理与生物医学在严谨性、安全性和可解释性上的标准对齐，仍然是关键挑战。BiomedSQL 针对这一点，评测模型在大规模生物医学知识库上的 text-to-SQL 生成中，推断并落实科学推理的能力，包括统计阈值、本体解析和复杂过滤。

**基准比较。** 我们在表 1 中把 BiomedSQL 与若干近期 text-to-SQL 基准进行比较。BiomedSQL 在四个方面是独特的：（1）它包含的问题 / SQL 查询 / 答案三元组数量最多；（2）它的平均 SQL 查询是最长者之列（仅次于 EHRSQL）；（3）它明确针对科学推理，而不是模式翻译；（4）它同时评测生成的 SQL 和模型的自然语言回答。BiomedSQL 也是唯一一个检验超出模式本身范围之推理的生物医学领域专用基准，并且是唯一使用 BigQuery 这一云原生 SQL 方言的基准，从而进一步模拟部署环境。

表 1：BiomedSQL 与其他 text-to-SQL 基准的比较。BiomedSQL 独特地评测科学推理、自然语言回答，以及 BigQuery SQL 生成。

| 数据集（Dataset） | 问题数（Number of Questions） | 查询数（Number of Queries） | 平均词元数（Avg. Tokens） | 知识（Knowledge） | 模板（Template） | 科学推理（Scientific Reasoning） | 自然语言回答（NL Response） | BigQuery |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| MIMICSQL (Wang et al., 2020) | 10,000 | 10,000 | 57.4 | ✗ | ✓ | ✗ | ✗ | ✗ |
| EHRSQL (Lee et al., 2022) | 24,000 | 24,000 | 109.9 | ✗ | ✓ | ✗ | ✗ | ✗ |
| SM3 (Sivasubramaniam et al., 2024) | 10,000 | 40,000 | 26.1 | ✗ | ✓ | ✗ | ✗ | ✗ |
| BIRD (Li et al., 2023) | 12,751 | 12,751 | 50.6 | ✓ | ✗ | ✗ | ✗ | ✗ |
| BiomedSQL | 68,227 | 68,227 | 96.4 | ✓ | ✓ | ✓ | ✓ | ✓ |
