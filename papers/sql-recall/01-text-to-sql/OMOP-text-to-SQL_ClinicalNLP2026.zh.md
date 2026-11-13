- 原文件名：`OMOP-text-to-SQL_ClinicalNLP2026.pdf`
- 原标题：An OMOP-Based Open-Source Text-to-SQL Benchmark Dataset
- 中文标题：基于 OMOP 的开源 Text-to-SQL 基准数据集
- 作者：Paul Legrand, Kawsar Noor, Satyam Bhagwanani, Richard J Dobson
- 会议或 arXiv：Proceedings of the 8th Workshop on Clinical Natural Language Processing (Clinical NLP) @ LREC 2026, pages 381–393, 16 May 2026

<!-- 原 PDF 第 1 页 -->

Proceedings of the 8th Workshop on Clinical Natural Language Processing (Clinical NLP) @ LREC 2026，第 381–393 页。2026 年 5 月 16 日。©ELRA Language Resources Association (ELRA), 2026。

# 基于 OMOP 的开源 Text-to-SQL 基准数据集

Paul Legrand<sup>1</sup>, Kawsar Noor<sup>1</sup>, Satyam Bhagwanani<sup>1</sup>, Richard J Dobson<sup>1,2</sup>

<sup>1</sup> University College London, London, United Kingdom

<sup>2</sup> King’s College London, London, United Kingdom

paul.legrand@etu.univ-amu.fr, kawsar.noor.15@ucl.ac.uk, s.bhagwanani@ucl.ac.uk, richard.j.dobson@kcl.ac.uk

## 摘要

电子健康记录（EHR）仓库的使用受限于 SQL 专业能力与复杂的临床模式。我们提出一个开源的 OMOP 通用数据模型 Text-to-SQL 基准（CDM v5.4），并带有安全契约：输出一条可执行的 SQL 语句，或对不可回答的请求输出弃答记号（`<NO_SQL>`）。输入经过概念规范化（实体表示为 OMOP concept ID），从而把 SQL 生成与实体链接解耦。评测时，在合成的 OMOP PostgreSQL 数据库上执行预测查询与参考查询，报告执行准确率（结果等价）以及一种可靠性分数：正确弃答得到奖励，不安全尝试受到惩罚。数据集包含来自 75 个经 OMOP 适配的模板的 6,690 条释义，划分方式对模板与 SQL 变体抗泄漏。经 LoRA 调优的 Llama-3-8B-Instruct 达到 93.55% 的执行准确率，弃答可靠性亦有提升；注入模式的基线则未能满足该契约。我们发布数据集、划分、数据库转储以及可复现的评测流程，以支持可靠的临床分析助手。

**关键词：** Text-to-SQL，电子健康记录（EHR），OMOP CDM，大语言模型（LLM）

## 1. 引言

EHR 含有丰富的结构化临床数据，但抽取队列或汇总统计仍需要 SQL 与模式方面的专门知识。Text-to-SQL 可以使自然语言查询成为可能，但临床部署很困难：性能高度依赖具体模式，看似合理的 SQL 也可能静默地给出错误队列。因此，评测应优先考虑可执行、忠实于模式的 SQL，并量化风险敏感的可靠性，包括当请求无法由数据库回答时的弃答（Geifman and El-Yaniv, 2019）。Spider 等通用基准（Yu et al., 2018）推动了进展，但其模式与评测设定不同于真实医院仓库，迁移因此受限；基于执行的评分必不可少，因为语法合法的 SQL 仍可能因错误的连接或谓词而在临床上是错的。更早的系统常常依赖显式的模式链接和关系感知的模式编码器（例如 RAT-SQL（Wang et al., 2020））。

近期的临床数据集加入了模板化问题与不可回答题，用以检验弃答，但尽管该模型已被广泛采用，明确锚定于 OMOP-CDM 的基准式资源仍然稀缺。面向 OMOP 的工作范围往往更窄（例如流行病学问答），也很少被表述为针对特定引擎、完全可执行的基准（例如 PostgreSQL），并带有显式的弃答/拒绝契约。例如，Ziletti and DAmbrosi（2024）用基于 RAG 的流程探索面向流行病学问答的 OMOP-CDM Text-to-SQL；我们的设定与之不同：我们明确纳入不可回答的请求，并规定专用的弃答记号，以支持感知拒绝的可执行基准。

OMOP 通用数据模型（CDM）是由 Observational Health Data Sciences and Informatics（OHDSI）社区推广的标准化关系模式（Hripcsak et al., 2015），已在异构数据库上的可扩展观察性安全监测中得到验证（Overhage et al., 2012），并被评估为纵向登记库可用的实用 CDM（Garza et al., 2016）。

我们把临床风格的自由文本请求落实为针对 OMOP CDM v5.4 的可执行查询，接口很严格：要么只输出 SQL（一条语句，以恰好一个分号结尾），要么输出弃答记号 `<NO_SQL>`。由于 OMOP 概念名称并不是可靠的键，稳健的队列定义使用基于 `concept_id` 的谓词（可选地沿词汇关系展开）；因此我们把医疗约束编码为概念标识，用以评测锚定于 OMOP 的 SQL 生成，而不是脆弱的字符串匹配。相应地，本基准评测的是在给定概念规范化输入时的下游 SQL 生成组件；把上游从原始文本做临床实体链接整合进来，留待今后的端到端工作。

我们发布<sup>1</sup>一个开源基准与可复现流程，其中包括：

- 一个锚定于 OMOP CDM v5.4 的 Text-to-SQL 数据集，对不可回答请求带有显式的安全弃答标签（`<NO_SQL>`）；
- 抗泄漏的训练/验证/测试划分，使释义保持在同一组内，并控制

<sup>1</sup> https://github.com/red1dwarf/TEXT-TO-OMOP

<!-- 原 PDF 第 2 页 -->

**图 1：基准与评测协议概览。** 图中文字如下。

- 临床问题（自由文本）
- 概念规范化输入（问题 + OMOP `concept_id`）
- SQL 生成器（Llama-3-8B-Instruct + LoRA）
- 输出：仅 SQL，或 `<NO_SQL>`
- 实体链接（今后的工作）：名称 → id
- 若为 `<NO_SQL>`（不执行）
- 沙箱执行（合成 PostgreSQL 数据库）
  - 只读事务
  - 语句超时
- 评分（基于执行）
  - 执行准确率（可回答样本；规范化后的结果集比较）
  - 可靠性分数 RS(\(c\))，并要求严格弃答
- 训练与推理协议
  - 划分单位 = 模板、SQL 变体（以防止释义泄漏）
  - 确定性解码（温度 = 0），并在第一个分号处截断
- 事后诊断（基于规则）
  - 模式漂移（非 OMOP 表）
  - 漏用 `visit_detail`
  - 缺少 FROM / 方言漂移（`DATEDIFF`）
  - 弃答错误（错误弃答）

图 1：基准与评测协议概览。

模板与 SQL 变体之间的重叠；

- 一套标准化评测，结合基于文本的指标、可回答性检测，以及在只读 PostgreSQL 上基于执行的评分，外加事后诊断分析；
- 端到端可复现材料，包括训练/推理脚本（LoRA 微调与注入模式的基线）以及可选的合成 OMOP PostgreSQL 转储。

## 2. 方法

我们描述 OMOP CDM v5.4 Text-to-SQL 的基准任务、数据集构建、划分协议、训练/评测设置以及指标。

### 2.1. 任务定义

我们研究 EHR 分析中锚定于模式的 SQL 生成，并遵守严格的可执行契约。给定输入问题 \(x\)，模型必须输出一条可执行、锚定于 OMOP 的 SQL 语句 \(\hat{q}\)（只有 SQL，没有散文），以恰好一个分号结尾；或者，当问题无法由数据库回答时（定义见第 2.4 节），输出精确的弃答记号 `<NO_SQL>`。推理时，我们在第一个分号处截断生成，以强制单语句约束。任何并非精确等于 `<NO_SQL>` 的输出都视为一次 SQL 尝试并加以执行以便评分；因此非法或空的 SQL 会导致执行失败。所有模型都用同一条指令进行训练和评测：只使用 OMOP CDM 的表、列和合法关系；绝不输出 `SELECT *`；只输出以恰好一个分号结尾的 SQL；否则用 `<NO_SQL>` 弃答。违反 OMOP 锚定的情况（例如模式漂移）通过事后诊断发现，并反映在基于执行的指标中。

### 2.2. 目标模式

目标环境是使用 PostgreSQL 方言的 OMOP 通用数据模型（CDM）v5.4（Observational Health Data Sciences and Informatics (OHDSI), 2021; PostgreSQL Global Development Group, 2025）。合法查询只能引用 OMOP CDM 的表和列，并且必须遵循 OMOP 的关系与惯例（例如通过标准化词汇做概念驱动的过滤，以及事件表语义）。引用非 OMOP 模式元素的查询视为模式漂移，并在诊断与基于执行的评测中受罚。

### 2.3. 数据集构建

本基准包含 75 个问题模板，与 OMOP 的连接模式和惯例对齐。我们从 EHRSQL 模板集出发（这是一个基于模板、面向 EHR 数据的临床 Text-to-SQL 资源；（Lee et al., 2023）），建立本地池并保留一个子集，以限制结构冗余（即模板共享同一查询骨架，只做槽位/取值替换或细微的表面差异）。随后我们把这些模板适配到 OMOP CDM v5.4 的连接路径和惯例，并补充少量 OMOP 特有模板，以更好地覆盖代表性不足的领域和连接（例如 `note`/`note_nlp` 自由文本表、`provider` 与 `death`，以及 `episode`/`episode_event` 模式）。

为捕捉与自由文本相连的查询，我们纳入了以笔记为中心、使用 `note` 和 `note_nlp` 的模板。在一个本地的、已映射到 OMOP 的 MIMIC-IV 实例中（Johnson et al., 2023; OHDSI, 2025），`note` 表由 MIMIC-IV 的 NOTE 模块填充，`note_nlp` 表来自 MedCAT 对放射报告和出院小结的标注（Kraljevic et al., 2021）。我们使用这一已映射到 OMOP 的 MIMIC-IV 环境，以反映结构化 OMOP 领域与非结构化文本并存的常见临床仓库设定；它也使我们能在开发期间检查模式连通性与模板合理性。该环境只用于数据集/模板开发；基于执行的评测完全在发布的合成 OMOP PostgreSQL 数据库上进行（第 2.8 节）。

每个模板通常实例化为三个（模板，SQL）变体：SQL 结构固定，插入的值（例如概念 ID、患者 ID、阈值、时间窗）变化，共得到 223 个（模板，SQL）变体。金标查询经常使用公共表表达式（CTE；`WITH`），以符合临床分析实践，并把队列定义、时间约束和就诊层级逻辑写明确，从而鼓励

<!-- 原 PDF 第 3 页 -->

结构化的 OMOP 分解，而不是单体式的嵌套子查询。

对每个变体，我们生成 30 种表面形式：一条规范问题，加上 29 条由 GPT-4.1 生成的释义（OpenAI, 2025a）。释义受到约束：（i）保持原意；（ii）类型标签内的占位值保持不变。由此得到 6,690 条可回答样本。不可回答问题不计入这一总数；我们仅从 EHRSQL-2024 取它们，用于弃答评测。发布的 `*.jsonl` 文件在应用第 2.4 节所述的类型标签与格式规范化之后，把这些不可回答题与可回答划分放在一起。

**类型标识标签。** 标识符包在轻量的类型标签中（例如 `<DRUG>...</DRUG>`、`<PERSON_ID>...</PERSON_ID>`）。这些标记没有 XML 语义；它们通过把临床提及表示为 `concept_id` 值（而不是自由文本提及或 `concept_name` 字符串），同时把标识符类型写明，从而使概念规范化输入成为可能。例如，“Did patient 289 take Panadol yesterday?” 变成 “Did patient `<PERSON_ID>289</PERSON_ID>` take `<DRUG>839681</DRUG>` yesterday?”。对概念标识（药物、病情等）和非概念标识（患者 ID）都加类型，可以减少歧义，抑制原始整数与 OMOP 字段之间的脆弱关联，并鼓励由模式驱动的推理（把带类型的角色映射到正确的 `*_concept_id` 谓词和连接路径，而不是依赖词汇线索）。

**人工核对协议。** 作者审阅每条释义，以确保语义等价、全部槽值与时间约束得以保留，并且没有临床上不合理的增补；不合格者被修改或删除。

### 2.4. 不可回答题的规范化

我们使用 EHRSQL-2024 共享任务中的不可回答问题（Lee et al., 2024b）。与 EHRSQL（Lee et al., 2023）一样，当仅靠结构化 OMOP 实例不足以回答时，问题被标为不可回答：它或者（i）需要数据库中未存储的外部/规范性临床知识，或者（ii）所问的信息超出数据库/模式。

在最初的设置中存在一条捷径：不可回答题常常缺少类型标签，于是“有没有标签”就能预测可回答性。在发布的规范化划分（`*.jsonl`）中，我们这样削弱该线索：（i）当出现类似实体的标识符时插入类型标签；（ii）抽样合成标识符，使其分布贴近可回答题（例如类似人员的 ID 长度）；（iii）统一标点，从而削弱“有标签 \(\Rightarrow\) 可回答”这一线索。

### 2.5. 概念规范化输入与抗记忆设计

OMOP 查询通常需要标准化词汇标识（例如 `*_concept_id`）。由于把表面提及（例如 “troponin”）映射到 OMOP ID 是上游的实体链接步骤，每条样本包含两个对齐的输入：`question_name`（人类可读的概念名称）和 `question_concept`（关键实体被替换为概念 ID）。重要的是，两个视图之间没有显式的名称到 ID 的链接：`question_name` 中的表面概念名称并不对应于 `question_concept` 中出现的概念 ID。我们同时发布二者，以便阅读和今后的端到端研究，但只报告从概念规范化输入生成 SQL 的结果（图 1），因此指标反映的是带有类似金标的 OMOP 标识的生成，而不是原始文本上的实体链接。为限制虚假的“ID 绑定”，标识符是合成的（类似概念或人员的整数），并不绑定真实轨迹，不过少数可能与 OHDSI 标准化词汇中的公开 OMOP `concept_id` 重合（Reich et al., 2024）。

### 2.6. 不可回答题与弃答

纳入不可回答题是为了压力测试可靠性。它们既包括规范性/外部知识请求，也包括“近失”的模式外查询（例如 ICD-11 \(\rightarrow\) ICD-10 这类跨本体代码查找），以反映现实中的用户意图：有数据库支撑的助手应当安全拒绝，而不是用一条看似合理的代理 SQL 来回答。对这些样本，唯一正确的输出是单独的弃答记号 `<NO_SQL>`（不附解释文字），从而使弃答对下游的路由/澄清可被机器执行。

### 2.7. 划分协议

在释义很多的数据集上，按实例划分会泄漏，因此我们在（模板，SQL）变体这一层划分：同一底层查询的释义从不跨划分。每个模板至多指定两个变体为“见过”；每个见过的变体有 30 条释义，按 20/5/5 分到训练/验证/测试。其余变体为“未见”；我们为验证抽取 37 个未见变体，为测试抽取 37 个，每个未见变体加入 5 条释义，以评测受控的泛化。不可回答题按固定比例注入（训练 10%；验证/测试 20%），得到 3,312 条训练样本（2,980 条可回答 + 332 条不可回答），验证和测试各 1,162 条（930 + 232）。划分在固定种子下是确定的（默认 42），我们发布 JSONL 划分文件以便精确复现。

<!-- 原 PDF 第 4 页 -->

| 类别 | 统计量（可回答样本） |
| --- | --- |
| 模板 / 变体 | 75 个模板；223 个（模板，SQL）变体 |
| 规模（可回答） | 6,690 条样本 |
| JOIN（金标 SQL） | 中位数 1；第 90 百分位 3；最大 4 |
| CTE 使用（WITH） | 40.36% |
| GROUP BY / DISTINCT | 28.25% / 20.63% |
| ORDER BY / LIMIT | 60.54% / 60.54% |
| 标签（问题） | 标签数中位数 1；12.57% 无标签 |
| 最常用的 OMOP 表 | concept（45.74%），visit_occurrence（30.04%），condition_occurrence（26.91%），drug_exposure（21.52%），measurement（17.49%），visit_detail（16.14%），person（13.45%），procedure_occurrence（10.76%），device_exposure（10.76%） |

表 1：可回答样本的数据集汇总统计。

### 2.8. 用于基于执行的评测的合成 OMOP 数据库

基于执行的评测是衡量 Text-to-SQL 正确性最忠实的办法（Wang et al., 2018），但在使用合成标识符时，即使 SQL 正确，在真实 OMOP 实例上也可能返回空结果。因此我们发布一个受控的合成 OMOP PostgreSQL 数据库，只用于评测（绝不用于训练）。它在固定的金标 SQL 集合之后事后生成（与模型无关），并不根据模型输出迭代改写：对每条金标查询，我们在相关 OMOP 表中插入使该金标查询返回非空结果所需的最少合成行，同时保留基本的异质性（多名患者、多个日期、多个事件）。填充通过由 GPT-5.1 协助的 PostgreSQL 插入脚本完成（OpenAI, 2025b），随后由作者复核、验证并执行；OMOP 完整性约束未强制执行（可能存在重复）。全部金标查询均被验证为能够成功执行，并且我们发布用于全部已报告执行指标的完整数据库转储与画像材料。金标 SQL 在数据集开发期间针对真实的、已映射到 OMOP 的 MIMIC-IV 环境撰写并验证（第 2.3 节），并在创建这一合成实例之前定稿，从而保证查询设计与评测数据库之间没有循环。

画像显示该实例并非平凡：23 张 OMOP 表，共 117,010 行（约 10 MB），其中包括 1,858 名人员与 6,453 次就诊。事件密度呈明显的长尾：人均事件均值 125.48，中位数 9，第 99 百分位 992.92，最大 2,374。就诊层级相当可观（63,826 行 `visit_detail`，约为 `visit_occurrence` 的 9.9 倍），使连接路径以及聚合/时间逻辑具有挑战，而不是“玩具式”的。该数据库是为有区分度的评分而设计的，并不追求流行病学上的真实性；对相对时间模板（例如 “today”），我们使用单一固定参照日（见第 6 节）。

### 2.9. 模型与训练设置

我们用 LoRA（Hu et al., 2021）微调 Llama-3-8B-Instruct（Grattafiori et al., 2024）。输入遵循 Llama-3 对话模板，并带有固定的系统提示，强制只输出 SQL 以及用 `<NO_SQL>` 弃答；损失只在生成的词元上计算（提示被掩码）。LoRA：\(r = 32\)，\(\alpha = 64\)，dropout 为 0.05，加在注意力与 MLP 投影模块上。训练：3 个 epoch，批大小 8，梯度累积 4，学习率 \(1.5\times 10^{-4}\)，余弦调度，预热比例 0.05，可选使用 bf16 和/或梯度检查点。

### 2.10. 推理协议

所有模型都使用确定性推理（种子 42；温度 0.0；top_p 1.0；max_new_tokens 1024），每条样本恰好产生一个输出（SQL 或 `<NO_SQL>`）。输出保存为 JSONL，并在发布的合成 OMOP PostgreSQL 实例上用同一套基于执行的流程评分。我们对在第一个分号处截断的原始生成结果评分，不做针对模型的后处理。

**注入模式的基线提示。** 对基线，我们在每条样本的用户消息前加上一段 OMOP PostgreSQL DDL 模式块（只有 OMOP 的表和列），与 Natural-SQL 风格的提示对齐。我们运行 Natural-SQL-7B（ChatDB, 2024）（一个公开的 7B ChatDB Text-to-SQL 指令模型），以及 Llama-3-8B-Instruct（基座）（Grattafiori et al., 2024）和 Mistral-7B-Instruct-v0.3（Jiang et al., 2023），设置同为注入模式。尽管提示遵循各模型的对话/模板惯例，我们在所有模型（基线与 LoRA）上保持相同的系统指令，以及相同的只输出 SQL / `<NO_SQL>` 输出契约；

<!-- 原 PDF 第 5 页 -->

注入的模式块是基线与 LoRA 之间唯一不同的提示内容。

### 2.11. 评测指标

我们优先考虑语义正确性与可靠性，并把执行准确率（ExecAcc）和风险敏感的可靠性分数（RS(\(c\))）作为 EHR Text-to-SQL 的主要基准指标。其余指标都作为次要分析与诊断来报告。

**主要的 Text-to-SQL 指标。**

**执行准确率（ExecAcc）。** 预测 SQL 与金标 SQL 都在合成 OMOP 数据库上的 PostgreSQL 中执行（只读事务；每条查询有语句超时）。ExecAcc 只在可回答样本上计算：一条预测正确，当且仅当它不是 `<NO_SQL>`、执行成功，并且返回与金标查询相同的规范化（顺序无关）结果集。不可回答样本不计入 ExecAcc，而通过 RS(\(c\)) 和面向可回答性的指标来评测。

**形式定义。** 设 \(A\) 为可回答样本的集合（金标 \(\neq\) `<NO_SQL>`），且其金标 SQL 在评测数据库上执行无误。设 \(\hat{q}_i\) 为模型输出，\(\mathrm{Res}(q)\) 为 PostgreSQL 返回的规范化（顺序无关）结果集。若执行失败（例如语法错误、超时），定义 \(\mathrm{Res}(q) = \bot\)，因此等式 \(\mathrm{Res}(\hat{q}_i) = \mathrm{Res}(q_i)\) 只可能在执行成功时成立。ExecAcc 的计算式如下。公式抽取不完整，见原 PDF 第 5 页。抽取到的原串为：

```
ExecAcc =
1
|A|
X
i∈A
1[ˆqi ̸= <NO_SQL>
∧Res(ˆqi) = Res(qi)]
(1)
```

我们在规范化之后比较金标结果与预测结果：（i）把 NULL 映射为空串；（ii）值保持 Python 原生类型（不做字符串强制转换）；（iii）把每一行规范化为其值的有序元组，先按 Python 类型分组、再按稳定的文本排序键确定地排序，从而使比较对输出列的置换不变；（iv）对得到的行列表排序，使其与行序无关。

列名和列序被有意忽略。把 NULL 映射为空串，可以提高对驱动相关的 NULL 处理的稳健性；在我们的评测集中，可回答问题的金标查询从不返回 NULL 或空串，因此这一选择不改变所报告的执行指标。

**可靠性分数（RS(\(c\))）。** 沿用 TrustSQL 中提出的风险敏感可靠性评测（Lee et al., 2024a），我们按五种情形给样本打分，惩罚参数 \(c \in \{0, 1, 10\}\)：

1. 可回答 + 正确 SQL \(\rightarrow +1\)
2. 可回答 + 弃答（`<NO_SQL>`）\(\rightarrow 0\)
3. 可回答 + 不正确或失败的 SQL \(\rightarrow -c\)
4. 不可回答 + 弃答（`<NO_SQL>`）\(\rightarrow +1\)
5. 不可回答 + SQL 尝试 \(\rightarrow -c\)

数据集层面的 RS(\(c\)) 是样本分数的平均；\(c\) 越大，相对弃答而言，对不安全尝试的惩罚越重，这符合临床偏好：答错比拒绝更糟。报告 \(c \in \{0, 1, 10\}\) 用来显示结论如何从中性设定（\(c = 0\)，此时不安全的 SQL 尝试并不比弃答受到更重的惩罚）变化到越来越厌恶风险的设定。

**次要指标（支撑分析）。** 我们还报告：

（i）可回答性 F1（\(\mathrm{F1}_{ans}\)），针对 SQL 与 `<NO_SQL>` 的二选一（回答 vs. 弃答），以“可回答”为正类（SQL = 正，`<NO_SQL>` = 负）；（ii）不可回答召回（UnansRec），被预测为 `<NO_SQL>` 的不可回答样本所占比例；（iii）错误弃答（%），被预测为 `<NO_SQL>` 的可回答样本所占比例；（iv）\(\mathrm{F1}_{exe}\)，它在模型确实尝试输出 SQL 的结果上概括可执行正确性（按定义 \(R_{exe} = \mathrm{ExecAcc}\)），计算为 \(P_{exe}\) 与 \(R_{exe}\) 的调和平均。

\(\mathrm{F1}_{exe}\) 与 \(\mathrm{F1}_{ans}\) 受 EHRSQL 启发（Lee et al., 2023）。

**\(\mathrm{F1}_{exe}\) 的形式化。** 设 \(A\) 为金标 SQL 在评测数据库上无误运行的可回答样本；设 \(T \subseteq A\) 为模型输出了 SQL 的那些样本（\(\hat{q}_i \neq\) `<NO_SQL>`），\(C \subseteq T\) 为执行正确的那些（\(\mathrm{Res}(\hat{q}_i) = \mathrm{Res}(q_i)\)）。与 EHRSQL 不同，我们在 \(T\) 上计算 \(\mathrm{Precision}_{exe}\)（以金标可回答为条件），因为对不可回答题的尝试由我们的弃答/可靠性指标处理。因此

\[
\mathrm{Precision}_{exe} = |C|/|T|, \quad \mathrm{Recall}_{exe} = |C|/|A| \;(=\mathrm{ExecAcc}),
\]

\[
\mathrm{F1}_{exe} = 2PR/(P+R),
\]

其中 \(P = \mathrm{Precision}_{exe}\)，\(R = \mathrm{Recall}_{exe}\)。

**辅助的字符串重叠与基于规则的诊断。** 我们报告精确匹配（EM）、规范化精确匹配（EMN）和 ROUGE-L，作为字符串重叠诊断，但把它们视为次要，因为语义等价的 SQL 在句法上可以不同（例如连接顺序、谓词重排）（Finegan-Dollak et al., 2018）。EM 是精确字符串匹配（Rajpurkar et al., 2016）；EMN 做轻量规范化（小写化、去掉末尾分号、折叠空白）；

<!-- 原 PDF 第 6 页 -->

ROUGE-L 基于最长公共子序列（LCS）重叠（Lin, 2004）。我们还报告基于规则的诊断（例如模式漂移、表集合不匹配、方言漂移、就诊层级遗漏），以刻画常见失败模式。

## 3. 结果

我们在留出的测试划分上、于统一流程下报告结果：相同的指令（只输出 SQL；单条语句；用 `<NO_SQL>` 弃答），确定性解码，在第一个分号处截断，并在合成数据库上用基于执行和面向可靠性的指标评分。

### 3.1. 主要结果

表 2 显示，经 OMOP 适配的模型与通用模型之间有明显差距。为使训练动态透明，我们还报告 LoRA-150。它不是另一个模型族，而是同一次 LoRA 训练中更早的检查点。最好的适配器 LoRA-312 达到 93.55% 的 ExecAcc，\(\mathrm{F1}_{exe}=93.65\%\)，同时保持近乎完美的可回答性（\(\mathrm{F1}_{ans}=99.46\%\)）以及为正的风险敏感可靠性（RS(10)\(=0.373\)）。LoRA-150 与 LoRA-312 应被理解为同一次训练中早期检查点与最终检查点的对比，而不是两个独立训练的方法。

**敏感性分析。** 在更严格的等价下（匹配列标题，并保留行内值的顺序，行序仍然无关），LoRA-312 的表现基本不变（93.44% ExecAcc），说明 ExecAcc 并不是结果集规范化的产物（也就是说，我们的默认比较忽略列名/列序，并对行做规范化；第 2.11 节）。此外，发布的合成数据库强制标识唯一（不同实体从不共享一个 ID），可回答金标查询也从不返回 NULL 或空串，因此实践中并不预期出现跨列的、取值相同而含糊的多重集。

尽管提示中注入了模式，现成基线的可执行正确性仍然低得多：Natural-SQL-7B（18.39%）、Llama-3-8B-Instruct（基座）（10.54%）和 Mistral-7B-Instruct-v0.3（4.09%）。它们的 RS(10) 明显为负（\(-8.381\) 到 \(-9.517\)），说明在我们的严格契约下，它们经常尝试 SQL 而不是弃答，面向可靠性的评分对此惩罚很重。所有基线的 EM/EMN \(= 0.00\)，主要是因为 SQL 不正确，同时也表明罕见的正确输出很少与金标 SQL 的形式一致，这强化了基于执行的评测的必要性。

总体而言，严格的 OMOP 查询需要与模式和领域对齐的监督，这超出了通用指令微调或 Text-to-SQL 调优。

### 3.2. 可回答性：弃答行为

测试集中有 20% 的不可回答题（232/1,162），弃答必须被明确评测。在类别不平衡下（930 条可回答 vs. 232 条不可回答），\(\mathrm{F1}_{ans}\)（SQL vs. `<NO_SQL>`）会被几乎总是尝试 SQL 的模型抬高：基线仍能达到 \(\mathrm{F1}_{ans} \approx 89\%\)，但 RS(10) \(\approx -9\)，说明的是不安全的过度尝试，而不是校准过的弃答。因此，对安全关键行为，我们优先看不可回答召回和 RS(\(c\))。表 3 显示，LoRA-312 在 96.55%（224/232）的不可回答题上正确弃答，同时很少过度拒绝可回答题（0.22%，2/930）；LoRA-150 在不可回答题上略低（92.67%），错误弃答率相同（0.22%）。基线几乎从不弃答（UnansRec 为 0–5.60%），从而在高惩罚下造成很大的可靠性损失。

### 3.3. 诊断：失败与挑战

为补充汇总分数，表 3 报告可解释的失败代理。错误弃答和不可回答召回遵循第 3.2 节；模式漂移 / 表集合不匹配 / `DATEDIFF` 使用 / CTE 使用，是在模型尝试了 SQL（排除 `<NO_SQL>`）的金标可回答条目上计算的，而不可回答召回是在不可回答题上计算的。模式漂移标记任何 FROM/JOIN 关系记号，只要它既不是 OMOP 表，也不是 CTE 名，也不在白名单的集合返回函数之中。表集合不匹配比较金标与预测中的基表集合（排除 CTE）。`DATEDIFF` 使用检测与 PostgreSQL 不兼容的 `DATEDIFF`。CTE 使用检查预测是否以 `WITH` 开头。`visit_detail` 漏用在金标 SQL 使用了 `visit_detail` 的样本上计算：只要预测省略 `visit_detail`（或弃答），就计为一次漏用。

当需要就诊层级推理时，基线表现出很大的表集合不匹配（52–79%）和频繁的 `visit_detail` 遗漏（70–89%），外加模式漂移（FROM/JOIN 中出现非 OMOP 表；Llama-3-8B-Instruct（基座）高达 14.62%）和方言漂移（例如 `DATEDIFF`，部分基线约为 5–6%）。LoRA 大体消除了模式/方言漂移（约 0%），并把表集合不匹配降到 0.65–1.19%，剩下的关键残留错误是就诊层级锚定：漏掉 `visit_detail`（LoRA-312 为 1.33%）仍可能产生可执行的 SQL，但临床语义不同（例如 ICU 分段时间 vs. 整体住院）。

### 3.4. 定性错误案例（LoRA-312）

我们为最好的适配器突出三种有代表性的残留失败模式（表 4），并把每个例子对应到表 3 中的诊断。

<!-- 原 PDF 第 7 页 -->

| 模型 | ExecAcc (%) | F1_exe (%) | F1_ans (%) | EM (%) | EMN (%) | ROUGE-L (%) | RS(0) | RS(1) | RS(10) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| LoRA-312 | 93.55 | 93.65 | 99.46 | 90.54 | 90.86 | 98.77 | 0.941 | 0.885 | 0.373 |
| LoRA-150 | 89.68 | 89.77 | 98.99 | 81.40 | 82.26 | 97.65 | 0.903 | 0.807 | -0.052 |
| Natural-SQL-7B | 18.39 | 18.39 | 88.91 | 0.00 | 0.00 | 40.23 | 0.147 | -0.706 | -8.381 |
| Llama-3-8B-Instruct (base) | 10.54 | 10.54 | 89.21 | 0.00 | 0.00 | 36.74 | 0.090 | -0.819 | -9.006 |
| Mistral-7B-Instruct-v0.3 | 4.09 | 4.09 | 89.47 | 0.00 | 0.00 | 31.08 | 0.043 | -0.912 | -9.517 |

表 2：OMOP Text-to-SQL 基准上的模型表现（测试集）。LoRA-150 与 LoRA-312 是同一次 LoRA 训练中的两个检查点（早期检查点 vs. 最终检查点）。RS(0)、RS(1) 与 RS(10) 表示惩罚参数 \(c \in \{0, 1, 10\}\) 下的可靠性分数，较大的 \(c\) 相对弃答更重地惩罚不安全的 SQL 尝试。

| 模型 | 错误弃答 (%) | 不可回答召回 (%) | 模式漂移 (%) | 表集合不匹配 (%) | DATEDIFF 使用 (%) | CTE 使用 (%) | visit_detail 漏用 (%) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| LoRA-312 | 0.22 | 96.55 | 0.00 | 0.65 | 0.00 | 40.30 | 1.33 |
| LoRA-150 | 0.22 | 92.67 | 0.00 | 1.19 | 0.00 | 40.09 | 0.67 |
| Natural-SQL-7B | 0.00 | 0.00 | 0.43 | 52.47 | 0.00 | 15.05 | 78.67 |
| Llama-3-8B-Instruct (base) | 0.00 | 3.02 | 14.62 | 76.88 | 5.81 | 0.32 | 70.00 |
| Mistral-7B-Instruct-v0.3 | 0.00 | 5.60 | 8.17 | 79.25 | 5.27 | 9.68 | 88.67 |

表 3：测试集上的诊断分析（930 条可回答 / 232 条不可回答）。

## 4. 讨论

结果表明，针对 OMOP 的适配是必要的：通用 SQL 能力并不能迁移，残留错误集中在连接路径、就诊层级以及时间/聚合语义上。

### 4.1. 为什么通用 SQL 在 OMOP 中失败

我们观察到，通用的指令微调基线与经 OMOP 适配的 LoRA 模型之间差距很大：基线常常产生看似合理的“像 SQL”的输出，但在 OMOP 中失败。在 OMOP 中，查询必须遵循领域惯例（通过标准化词汇做概念驱动的过滤、事件表语义，以及跨 person、就诊和临床领域表的规范连接路径）。诊断结果把这一点说得很明确：基线错误以表集合不匹配、就诊层级错误以及模式/方言漂移为主，说明通用的 SQL 能力并不能产生 OMOP 正确的查询。反过来，最好的 LoRA 适配器表明，这些惯例可以用轻量开源模型上适度的参数高效调优学到，从而支持医院本地部署以及 CDM/方言适配，而无须依赖大型或专有系统。

### 4.2. 可靠性与弃答应当是一等的评测目标

临床分析不同于许多 Text-to-SQL 设定：一条错误查询可以静默地产生看似合理但不正确的队列或统计。因此，本基准纳入不可回答问题，并强制单一弃答记号 `<NO_SQL>`。感知可靠性的评分（RS(\(c\))）补充 ExecAcc：随着 \(c\) 增大，相对弃答，对不安全尝试的惩罚加重，这反映一种常见的临床偏好：答错比拒绝更糟。LoRA 模型更高的 RS(\(c\))，加上高不可回答召回和低错误弃答率，表明在一条简单、可被机器执行的策略下，弃答既可学习，也可量化。实践上，在 SQL 生成组件内部给出自由形式的解释可能适得其反：“有帮助”的自然语言对下游系统可能含糊，并被误认为可执行意图。严格契约（只输出 SQL，或 `<NO_SQL>`）更能支持安全的智能体集成：`<NO_SQL>` 可以触发澄清、后备工具或人工复核。

### 4.3. 残留挑战：连接、就诊、时间/聚合

微调之后，表 3 显示残留差距是语义性的，集中在三个对 OMOP 关键的选择上：（i）当存在多条与模式一致的路径时，跨事件表选择连接路径（尤其是多领域查询）；（ii）就诊层级的选择（`visit_occurrence` vs. `visit_detail`），选错层级或漏掉所需的 `visit_detail` 会隐含地改变队列；（iii）时间/聚合语义（窗口边界、

<!-- 原 PDF 第 8 页 -->

**表 4：LoRA-312 的代表性残留失败模式。**

**失败模式：就诊层级锚定（漏用 `visit_detail`；与表 3 中的 `visit_detail` 漏用一致）**

问题：患者 `<PERSON_ID>6102133621015</PERSON_ID>` 在本次住院期间住了多久 ICU？

金标（使用 ICU 分段时间）：

```sql
SELECT
...
FROM visit_occurrence vo
JOIN visit_detail vd ON vd.visit_occurrence_id = vo.visit_occurrence_id
JOIN concept c ON vd.visit_detail_concept_id = c.concept_id
WHERE ...
c.concept_name ILIKE '%intensive care%' ...;
```

LoRA-312（丢掉 `visit_detail`）：

```sql
SELECT ... FROM visit_occurrence vo
JOIN concept c ON vo.visit_concept_id = c.concept_id
WHERE ... c.concept_name ILIKE '%intensive care%' ...;
```

影响：SQL 可执行，但临床语义不同（医院层面的住院时长 vs. ICU 分段时长）。

**失败模式：表锚定混淆（measurement vs. 就诊表；与表 3 中的表集合不匹配一致）**

问题：能否找出患者 `<PERSON_ID>3720242571871</PERSON_ID>` 在去年 5 月 6 日记录的第三次体重？

金标（OMOP measurement 检索 + 偏移）：

```sql
SELECT m.value_as_number
FROM measurement m
WHERE m.person_id = 3720242571871
  AND m.measurement_concept_id = 3025315
  AND m.measurement_date = MAKE_DATE(EXTRACT(YEAR FROM CURRENT_DATE)::int - 1, 5, 6)
ORDER BY m.measurement_datetime OFFSET 2 LIMIT 1;
```

LoRA-312（表选择错误）：

```sql
SELECT ...
FROM visit_occurrence vo
JOIN concept c ON ...
WHERE vo.person_id = 3720242571871
  AND vo.visit_start_date = MAKE_DATE(...)
  AND c.concept_name ILIKE '%weight%'
ORDER BY ... OFFSET 2 LIMIT 1;
```

影响：错误的 OMOP 事件表语义；漏掉概念驱动的过滤和测量排序逻辑。

**失败模式：对不可回答题的不安全尝试（与表 3 中的不可回答召回以及 RS(\(c\)) 惩罚一致）**

问题：患者 `<PERSON_ID>4773708619089828657</PERSON_ID>` 上个月应该服用 `<DRUG>942384</DRUG>` 多久？

金标：`<NO_SQL>`

LoRA-312（不安全的 SQL 尝试）：

```sql
SELECT MAX(de.drug_exposure_start_datetime) ...,
MIN(...) ...
FROM drug_exposure de
WHERE de.person_id = ...
  AND de.drug_concept_id = 942384
  AND EXTRACT(MONTH FROM de.drug_exposure_start_date) = EXTRACT(MONTH FROM CURRENT_DATE) - 1;
```

影响：对一个规范性/外部知识请求，用时间戳（错误地）编造一个可计算的代理来回答。

分组粒度、DISTINCT），细小的不匹配可以看起来合理，却使统计失效。这意味着：（a）该基准对临床上有后果的推理仍然有区分度，包括锚定于模式的关系结构、事件级 vs. 就诊级意图，以及忠实的时间/聚合线索；（b）进展很可能需要结构化锚定和语义验证，而不仅仅是扩大规模。三个方向是：（1）在 OMOP 连接图上做约束感知解码（例如 PICARD；Scholak et al. (2021)），以降低或阻断非法的表转移；（2）选择性的模式检索，只返回相关的表、键和概念映射，减少全模式注入带来的干扰项（例如 RASL；Eben et al. (2025)）；（3）针对高影响承诺做有目标的生成后检查，包括时间谓词与问题时间框架的对齐，以及聚合层级（含 DISTINCT）与所请求度量的对齐（例如 Ren et al. (2025)）。总体而言，残留差距是锚定于模式的语义忠实性，这促使人们为可靠的临床 Text-to-SQL 采用生成再检查的混合流程。

## 5. 结论

总之，本基准提供一个锚定于 OMOP CDM v5.4、面向可靠性的 EHR Text-to-SQL 试验台，输出契约严格且便于部署。结果表明，参数高效的适配可以达到很高的可执行正确性，并实质改善弃答行为，而通用基线在 OMOP 约束下仍然脆弱。我们期望这一资源能支持更安全的临床分析助手研究：把上游实体链接与可靠的 SQL 生成、受约束的执行，以及稳健的弃答/路由策略结合起来。通过提供一个锚定于 OMOP、按执行评分、并带有校准弃答的基准，我们旨在加速更安全的自由文本界面，用于队列发现和临床分析。

<!-- 原 PDF 第 9 页 -->

## 6. 局限

我们报告的是概念规范化输入上的结果（实体表示为 OMOP 概念标识），因此没有评测从原始临床文本做端到端实体链接（例如使用 MedCAT 这类临床实体链接器（Kraljevic et al., 2021））。虽然我们同时发布人类可读的问题与概念规范化的问题，以支持端到端工作，真实部署仍会遇到概念歧义和链接错误，并可能传递到 SQL 执行。部署时，链接不确定性可能需要确认或弃答策略（例如在概念歧义高时弃答）。

我们的划分协议旨在检验对未见（模板，SQL 变体）结构以及释义后的表面形式的受控泛化。它并不直接度量独立 OMOP 部署之间的跨机构分布偏移；在那些部署中，数据分布、本地惯例和完整性约束可能不同。因此，在真实机构的 OMOP 数据库上，绝对执行准确率可能改变，即便严格的只输出 SQL / `<NO_SQL>` 输出契约以及我们面向可靠性的评测仍然适用。

本基准的覆盖面和词汇多样性也受限于基于模板的构建；今后的工作应更紧密地对照真实医院的信息需求来扩大多样性。

此外，我们的不可回答样本改编自 EHRSQL-2024，而不是针对 OMOP 特有失败模式原生构造的，因此今后的工作应整理面向特定模式弃答场景的 OMOP 原生不可回答题。

最后，基于执行的评分依赖一个受控的合成 OMOP PostgreSQL 实例，其填充方式使金标查询返回非空输出，从而在保留抗记忆设计的同时，使基于执行的评分有区分度。这一合成数据库并不打算反映真实的患病率、编码分布或完整性约束；因此绝对执行指标在实践中可能不同。对时间敏感的模板（例如 “today”），我们在发布的评测转储中把参照日固定为 2026-02-02。

## 7. 伦理声明

本工作通过严格的 Text-to-SQL（或 `<NO_SQL>`）接口支持临床数据访问，供研究使用。发布的基准包括：（i）自然语言问题；（ii）金标 SQL 查询；（iii）为有区分度的、基于执行的评测而设计的合成 OMOP CDM v5.4 PostgreSQL 转储。

不发布任何 MIMIC-IV 内容：我们不发布任何源自 MIMIC 的临床笔记、患者级记录或其他受保护的/可识别的健康信息。

尽管有严格的输出契约和基于执行的评测，若没有防护就使用，模型生成的 SQL 仍可能不正确或不安全；我们建议采取纵深防御措施（例如沙箱执行、超时、查询允许/拒绝列表、日志，以及对高风险用途的人工监督）。

## 8. 补充材料

### 8.1. 数据集构建

**图 2：数据集构建概览。** 图中文字如下。

模板适配

- [template]：「患者 {patient_id} 的该项输出叫什么名字……」
- [adapted_template]：「患者 {patient_id} 的该项测量叫什么名字……」

模板选择：来自 EHRSQL 的问题模板池。

模板创建

- [new_template]：「比较 2010 年之前和之后，先前接受过 {procedure_name} 操作、年龄在 30 多岁的男性中，由 {diagnosis_name} 导致的死亡人数。」

槽位填充

- [template]：「比较由 {diagnosis_name} 导致的死亡人数……」
- [question_concept]：「比较由 `<CONDITION>312327</CONDITION>` 导致的死亡人数……」

释义

- [question_concept]：「统计当前 20 多岁患者的人数」
- [paraphrase 1]：「目前二十多岁的在诊患者总数」
- ……
- [paraphrase 29]：「目前在接受照护的 20–29 岁的人有多少？」

可回答合计

- 74 个模板 → 每个 3 个变体
- 1 个模板（无槽位）→ 1 个变体
- 223 个（模板，SQL）变体
- 每个变体 30 种表面形式
- 6,690 条可回答样本

不可回答题选择：来自 EHRSQL2024 的不可回答问题池。

格式化

- [unanswerable]：「phentolamine mesylate 有哪些副作用？」
- [normalized_unanswerable]：「`<DRUG>35412113</DRUG>` 有哪些副作用？」

不可回答合计：796 条规范化的不可回答样本。

75 个模板；223 个变体；6,690 条样本。

数据集

- 6,690 条可回答样本
- 796 条不可回答样本

图 2：数据集构建概览。经 OMOP 适配的 EHRSQL 模板产生 223 个（模板，SQL）变体和 6,690 条可回答样本；另行选出并规范化的 EHRSQL-2024 不可回答题再贡献 796 条样本。

<!-- 原 PDF 第 10 页 -->

### 8.2. 划分协议

**图 3：在（模板，SQL）变体层构建抗泄漏划分。** 图中文字如下。

223 个变体：74 个模板各有 3 个变体，1 个模板有 1 个变体。

模板/SQL 变体划分：对每个有 3 个变体的模板，2 个变体分到“见过”组，1 个分到“未见”组；只有 1 个变体的模板贡献 1 个见过的变体。

- 见过：149 个变体（148 + 1）
- 未见：74 个变体

对每个变体：

- 20 条释义 → 训练
- 5 条释义 → 验证
- 5 条释义 → 测试

训练：\(149 \times 20 = 2980\)

验证：\(149 \times 5 = 745\)

测试：\(149 \times 5 = 745\)

37 个变体只分到验证集。对每个变体：5 条释义 → 验证。

37 个变体只分到测试集。对每个变体：5 条释义 → 测试。

验证：\(37 \times 5 = 185\)

测试：\(37 \times 5 = 185\)

训练：2980

验证：\(745 + 185 = 930\)

测试：\(745 + 185 = 930\)

训练：\(2980 + 332 = 3312\)

验证：\(930 + 232 = 1162\)

测试：\(930 + 232 = 1162\)

加入不可回答样本：训练集中占 10%（332）；验证/测试中各占 20%（各 232）。

图 3：在（模板，SQL）变体层构建抗泄漏划分。见过的变体进入训练/验证/测试，未见的变体只进入验证或测试，不可回答题按固定比例加入。

### 8.3. 基准专用例子中所用 OMOP 表的简要说明

为方便不太熟悉 OMOP CDM 的读者，表 5 简要概括若干与本基准相关、仅从名称上不那么直观的 OMOP 表。

| 表 | 在 OMOP 中的角色 / 与本文的关系 |
| --- | --- |
| visit_occurrence | 存储粗粒度的照护遭遇（例如住院或门诊就诊）。用于就诊级推理和“最近一次就诊”类查询。 |
| visit_detail | 存储一次就诊内部更细的子就诊片段（例如一次住院中的 ICU 停留）。当临床上正确的答案取决于子就诊粒度时，这一点很重要。 |
| note | 把非结构化临床笔记存为与患者和就诊相连的文本文档。 |
| note_nlp | 存储临床笔记上由 NLP 得到的标注（例如抽出的概念/提及），从而支持与笔记相连的结构化查询。 |
| episode | 表示更高层的临床 episode，把一段时间内相关的事件归为一组。 |
| episode_event | 把一个 episode 链接到属于它的那些 OMOP 事件。 |

表 5：对非 OMOP 读者可能较陌生、但出现在基准构建或错误分析中的 OMOP 表的简短词汇表。

### 8.4. 所发布实例的具体例子

为把基准格式说得更明确，下面给出发布的 JSON 实例中的一个可回答例子和一个不可回答例子。如正文所述，每条可回答条目可以包含人类可读的问题（`question_name`）、概念规范化的问题（`question_concept`）、金标 SQL 查询，以及来源模板。不可回答例子使用相同的输入格式，但唯一正确的目标输出是弃答记号 `<NO_SQL>`。

**可回答例子。** 这个例子说明一种概念规范化输入：药物提及被替换为 OMOP `concept_id`，同时保留对应的人类可读版本以便阅读。

```json
{
  "question_name": "在最近一次住院就诊中于同一时间也被开具了 <DRUG>bisacodyl 10 MG Rectal Suppository [Bisac-Evac]</DRUG> 的患者，最常被开具的前 4 种药物是什么？",
  "question_concept": "在最近一次住院就诊中于同一时间也被开具了 <DRUG>19041823</DRUG> 的患者，最常被开具的前 4 种药物是什么？",
  "sql": "WITH last_visits AS (SELECT DISTINCT ON (vo.person_id) vo.visit_occurrence_id FROM visit_occurrence AS vo ORDER BY vo.person_id, vo.visit_start_date DESC), patients_with_19041823 AS (SELECT lv.visit_occurrence_id FROM last_visits AS lv JOIN drug_exposure AS de1 ON lv.visit_occurrence_id = de1.visit_occurrence_id WHERE de1.drug_concept_id = 19041823), co_prescribed_drugs AS (SELECT de2.drug_concept_id FROM drug_exposure de2 JOIN patients_with_19041823 AS p ON de2.visit_occurrence_id = p.visit_occurrence_id WHERE de2.drug_concept_id != 19041823) SELECT d.drug_concept_id AS concept_id, c.concept_name, COUNT(*) AS count FROM co_prescribed_drugs AS d JOIN concept AS c ON d.drug_concept_id = c.concept_id GROUP BY d.drug_concept_id, c.concept_name ORDER BY count DESC LIMIT 4;",
  "template": "are_verb 最常被开具的前 [n_rank] 种药物，对象是同时也
```

<!-- 原 PDF 第 11 页 -->

```json
开具了 {drug_name} 的患者 [time_filter_within] [time_filter_global1]？"
}
```

这个例子突出本基准的设计选择：从概念规范化输入评测 SQL 生成。模型应把带类型的标识 `<DRUG>19041823</DRUG>` 映射到正确的 OMOP 谓词结构（此处为 `drug_exposure.drug_concept_id`），并产生一条可执行的 PostgreSQL 查询。

**不可回答例子。** 下面的例子说明弃答设定。问题询问药物副作用，按我们的任务定义，不能仅凭 OMOP 数据库实例回答。因此唯一正确的输出是弃答记号 `<NO_SQL>`。

```json
{
  "input": "<DRUG>43833975</DRUG> 的副作用是什么？",
  "output": "<NO_SQL>"
}
```

这个例子属于基准中的不可回答部分，并体现本任务预定的安全契约：如果答案需要的是外部或规范性医学知识，而不是结构化 OMOP 数据库中可用的信息，模型必须弃答，而不是生成一条看似合理但没有依据的 SQL 查询。

### 8.5. LoRA 模型与注入模式的基线所用的推理提示

为便于复现，下面报告推理时使用的提示结构。所有模型都以确定性解码运行（temperature=0.0，top_p=1.0），生成在第一个分号处截断，使输出满足单语句契约。LoRA 模型与基线使用同一条核心指令，主要差别是基线提示额外把 PostgreSQL DDL 模式注入用户提示。

**共用系统指令。** 推理中使用如下系统消息：

```text
你是一个助手，为遵循 OMOP Common Data Model (CDM) 的电子健康记录中所存储的数据生成合法的 PostgreSQL SQL 查询。严格遵守以下规则：
- 只使用 OMOP CDM 的表、列和关系。
- 绝不编造表或列。
- 绝不虚构模式细节。
- 绝不使用 SELECT *。
- 用分号结束 SQL 查询。
- 只输出 SQL 查询，不要散文、注释或解释。
- 如果问题无法从 OMOP CDM 数据回答，输出 <NO_SQL>。
- 在第一个分号之后停止。
```

**LoRA 推理提示（Llama-3 对话格式）。** LoRA 推理时，模型以原生 Llama-3 对话格式接受提示，不注入模式。用户消息只包含问题：

```text
<|begin_of_text|><|start_header_id|>system<|end_header_id|>
[SYSTEM_MSG]<|eot_id|>
<|start_header_id|>user<|end_header_id|>
生成回答下列问题的 SQL 查询：
[QUESTION]
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
```

具体而言，[SYSTEM_MSG] 替换为上面的共用系统指令，[QUESTION] 替换为基准输入字符串。

**注入模式的基线提示。** 对基线模型，模式通过用户消息注入提示。共用的用户侧内容为：

```text
你得到了 PostgreSQL DDL 形式的数据库模式。
用它写出正确的查询。
### 数据库模式（DDL）
[SCHEMA_DDL]
### 问题
[QUESTION]
```

此处 [SCHEMA_DDL] 表示 OMOP PostgreSQL DDL 块，[QUESTION] 表示基准输入。

**Llama-3 基线提示。** Llama-3 基线使用与 LoRA 模型相同的原生对话包装，但用户块是注入了模式的那一段：

```text
<|begin_of_text|><|start_header_id|>system<|end_header_id|>
[SYSTEM_MSG]<|eot_id|>
<|start_header_id|>user<|end_header_id|>
[USER_BLOCK_WITH_SCHEMA]
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
```

其中 [USER_BLOCK_WITH_SCHEMA] 是上面所示的、注入了模式的内容。

<!-- 原 PDF 第 12 页 -->

**Mistral 基线提示。** Mistral 基线在分词器提供对话模板时使用该模板，消息结构同样是两条：（i）共用系统指令；（ii）注入了模式的用户消息。当对话模板不可用时，回退的纯文本提示为：

```text
System: [SYSTEM_MSG]
User: [USER_BLOCK_WITH_SCHEMA]
Assistant:
```

这样在把格式适配到分词器实现的同时，指令内容保持完全相同。

**Natural-SQL 基线提示。** Natural-SQL 基线使用如下任务式提示：

```text
# 任务
[SYSTEM_MSG]
生成一条 SQL 查询来回答下列问题：`[QUESTION]`
### PostgreSQL 数据库模式
该查询将在具有如下模式的数据库上运行：
[SCHEMA_DDL]
# SQL
下面是回答该问题的 SQL 查询：`[QUESTION]`
```sql
```

因此，同样的指令约束被保留下来，只是嵌入在 Natural-SQL 的提示格式中。

## 9. 参考文献

ChatDB. 2024. Natural-SQL-7B. Hugging Face 模型卡。访问日期：2026-01-31。

Jeffrey Eben, Aitzaz Ahmad, and Stephen Lau. 2025. RASL：面向大规模数据库 Text-to-SQL 的检索增强模式链接. arXiv preprint arXiv:2507.23104. Accepted to the KDD Workshop on Structured Knowledge for Large Language Models (SKnowLLM ’25).

Catherine Finegan-Dollak, Jonathan K. Kummerfeld, Li Zhang, Karthik Ramanathan, Sesh Sadasivam, Rui Zhang, and Dragomir Radev. 2018. 改进 Text-to-SQL 评测方法. In Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 351–360, Melbourne, Australia. Association for Computational Linguistics.

Maryam Garza, Guilherme Del Fiol, Jessica Tenenbaum, Anita Walden, and Meredith Nahm Zozus. 2016. 评估用于纵向社区登记库的通用数据模型. Journal of Biomedical Informatics, 64:333–341.

Yonatan Geifman and Ran El-Yaniv. 2019. SelectiveNet：带集成拒绝选项的深度神经网络. In Proceedings of the 36th International Conference on Machine Learning, volume 97 of Proceedings of Machine Learning Research, pages 2151–2159. PMLR.

Aaron Grattafiori, Abhimanyu Dubey, Anish Jha, et al. 2024. Llama 3 模型群.

George Hripcsak, Jon D. Duke, Nigam H. Shah, Christian G. Reich, Vojtech Huser, Martijn J. Schuemie, Marc A. Suchard, Rae Woong Park, Ian C. K. Wong, Peter R. Rijnbeek, Johan van der Lei, Nicole Pratt, G. Niklas Norén, Yu-Chuan (Jack) Li, Paul E. Stang, David Madigan, and Patrick B. Ryan. 2015. 观察性健康数据科学与信息学（OHDSI）：观察性研究者的机遇. In Studies in Health Technology and Informatics, volume 216, pages 574–578.

Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen. 2021. LoRA：大语言模型的低秩适配. arXiv preprint arXiv:2106.09685.

Albert Q. Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, Devendra Singh Chaplot, Diego de las Casas, Florian Bressand, Gianna Lengyel, Guillaume Lample, Lucile Saulnier, Lélio Renard Lavaud, Marie-Anne Lachaux, Pierre Stock, Teven Le Scao, Thomas Wang, Timothée Lacroix, and William El Sayed. 2023. Mistral 7B.

Alistair E. W. Johnson, Lucas Bulgarelli, Lu Shen, Alvin Gayles, Ayad Shammout, Steven Horng, Tom J. Pollard, Sicheng Hao, Benjamin Moody, Brian Gow, Li-Wei H. Lehman, Leo A. Celi, and Roger G. Mark. 2023. MIMIC-IV：一个可自由获取的电子健康记录数据集. Scientific Data, 10(1):1.

Zeljko Kraljevic, Thomas Searle, Anthony Shek, Lukasz Roguski, Kawsar Noor, Daniel Bean, Aurelie Mascio, Leilei Zhu, Amos A. Folarin, Angus Roberts, Rebecca Bendayan, Mark P. Richardson, Robert Stewart, Anoop D. Shah, Wai Keong Wong, Zina Ibrahim, James T. Teo, and Richard
