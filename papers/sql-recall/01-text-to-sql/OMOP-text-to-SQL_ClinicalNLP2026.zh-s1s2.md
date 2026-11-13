# An OMOP-Based Open-Source Text-to-SQL Benchmark Dataset

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`OMOP-text-to-SQL_ClinicalNLP2026.pdf`。

## Abstract 摘要

获取电子健康记录（electronic health record, EHR）仓库受限于 SQL 专业能力与复杂的临床模式。我们提出一个开源的 OMOP 通用数据模型（Common Data Model, CDM）v5.4 text-to-SQL 基准，并带有一项安全契约：对可回答请求输出一条可执行 SQL 语句，对不可回答请求输出弃答标记（`<NO_SQL>`）。输入经过概念规范化（concept-normalized），即把实体表示为 OMOP concept ID，从而使 SQL 生成与实体链接（entity linking）解耦。我们在一个合成的 OMOP PostgreSQL 数据库上执行预测查询与参考查询来评测，报告执行准确率（Execution Accuracy，结果等价）以及一个可靠性分数：该分数奖励正确弃答，并惩罚不安全的尝试。数据集包含来自 75 个经 OMOP 适配的模板的 6,690 条释义，并采用抗泄漏的模板 / SQL 变体划分。经 LoRA 调优的 Llama-3-8B-Instruct 达到 93.55% 的执行准确率，弃答可靠性也有提高；而注入模式的基线未能满足该契约。我们发布数据集、划分、数据库转储以及可复现的评测流程，以支持可靠的临床分析助手。

关键词（Keywords）：Text-to-SQL，Electronic Health Records (EHR)，OMOP CDM，Large Language Models (LLMs)。

## 1. Introduction 引言

EHR 中存有丰富的结构化临床数据，但抽取队列或汇总统计仍然需要 SQL 与模式方面的专门知识。Text-to-SQL 有望支持自然语言查询，但临床部署很困难：性能高度依赖模式，而且看似合理的 SQL 可能在不报错的情况下给出错误队列。因此，评测应当优先考虑可执行、忠实于模式的 SQL，并量化对风险敏感的可靠性，包括当请求无法由数据库回答时的弃答（abstention）（Geifman and El-Yaniv, 2019）。Spider（Yu et al., 2018）等通用基准推动了进展，但其模式与评测设置不同于真实医院数据仓库，迁移受限；基于执行的评分必不可少，因为语法有效的 SQL 仍可能因错误的连接或谓词而在临床上是错的。较早的系统往往依赖显式的模式链接，以及关系感知的模式编码器（例如 RAT-SQL（Wang et al., 2020））。

近期的临床数据集加入了模板化问题与不可回答问题，以测试弃答；然而，尽管 OMOP-CDM 已被广泛采用，明确以它为根据的基准式资源仍然稀缺。面向 OMOP 的工作在范围上往往更窄（例如流行病学问答），也很少被构建为针对特定引擎、完全可执行的基准（例如 PostgreSQL），并带有明确的弃答 / 拒绝契约。例如，Ziletti and DAmbrosi (2024) 用基于 RAG 的流程探索面向流行病学问答的 OMOP-CDM text-to-SQL；我们的设定与之不同：我们明确纳入不可回答请求，并规定专用的弃答标记，以支持具备拒绝意识的可执行基准。

OMOP Common Data Model (CDM) 是由观察性健康数据科学与信息学（Observational Health Data Sciences and Informatics, OHDSI）社区推动的标准化关系模式（Hripcsak et al., 2015），已在异构数据库上被验证可用于可扩展的观察性安全监测（Overhage et al., 2012），并被评估为纵向登记库的一种实用 CDM（Garza et al., 2016）。

我们把临床医生风格的自由文本请求，落实为针对 OMOP CDM v5.4 的可执行查询，接口很严格：要么只输出 SQL（一条语句，且恰好以一个分号结束），要么输出弃答标记 `<NO_SQL>`。由于 OMOP 概念名称并不是可靠的键，稳健的队列定义使用基于 concept_id 的谓词（可选地经由词汇表关系展开）；因此我们把医学约束编码为概念标识符，以评测扎根于 OMOP 的 SQL 生成，而不是脆弱的字符串匹配。相应地，本基准在给定概念规范化输入的条件下，评测下游 SQL 生成组件；把上游从原始文本做临床实体链接整合进来，留待未来的端到端工作。

我们发布¹一个开源基准与可复现流程，包括：

- 一个扎根于 OMOP CDM v5.4 的 text-to-SQL 数据集，对不可回答请求带有明确的安全弃答标签（`<NO_SQL>`）；
- 抗泄漏的训练 / 验证 / 测试划分，把释义归在一起，并控制模板 / SQL 变体的重叠；
- 一套标准化评测，结合基于文本的指标、可回答性检测，以及在只读 PostgreSQL 中的基于执行的评分，外加事后诊断分析；
- 端到端可复现产物，包括训练 / 推理脚本（LoRA 微调与注入模式的基线），以及一份可选的合成 OMOP PostgreSQL 转储。

¹ https://github.com/red1dwarf/TEXT-TO-OMOP

图 1：基准与评测协议概览。图中连线与分支的版面抽取不全，【抽取不清】。抽出的文字标签如下：临床问题（自由文本）；概念规范化输入（问题 + OMOP concept_id）；SQL 生成器（Llama-3-8B-Instruct + LoRA）；输出：仅 SQL，或 `<NO_SQL>`；实体链接（未来工作）；name → id；若为 `<NO_SQL>` 则不执行；沙箱执行（合成 PostgreSQL 数据库）：只读事务、语句超时；基于执行的评分：执行准确率（Execution Accuracy；可回答样本；规范化结果集比较）、带严格弃答的可靠性分数 RS(c)；训练与推理协议：划分单位 = 模板、SQL 变体（以防止释义泄漏），确定性解码（temperature = 0）以及在第一个分号处截断；基于规则的事后诊断：模式漂移（非 OMOP 表）、遗漏 visit_detail、缺少 FROM / 方言漂移（DATEDIFF）、弃答错误（错误弃答）。

## 2. Method 方法

我们描述 OMOP CDM v5.4 text-to-SQL 的基准任务、数据集构建、划分协议、训练 / 评测设置以及指标。

### 2.1. Task definition 任务定义

我们研究在严格可执行契约下、面向 EHR 分析的模式扎根 SQL 生成。给定输入问题 x，模型必须输出一条可执行、扎根于 OMOP 的 SQL 语句 q̂（只有 SQL，没有散文），且恰好以一个分号结束；或者，当问题无法由数据库回答时（定义见第 2.4 节），输出恰好为弃答标记 `<NO_SQL>`。推理时，我们在第一个分号处截断生成，以强制单语句约束。任何并非恰好为 `<NO_SQL>` 的输出都视为一次 SQL 尝试并加以执行以便评分；无效或空的 SQL 因此导致执行失败。所有模型都用同一条指令进行训练和评测：只使用 OMOP CDM 的表 / 列以及有效关系；绝不输出 `SELECT *`；只输出以恰好一个分号结束的 SQL；否则用 `<NO_SQL>` 弃答。违反 OMOP 扎根的情况（例如模式漂移）通过事后诊断检出，并反映在基于执行的指标中。

### 2.2. Target schema 目标模式

目标环境是采用 PostgreSQL 方言的 OMOP Common Data Model (CDM) v5.4（Observational Health Data Sciences and Informatics (OHDSI), 2021; PostgreSQL Global Development Group, 2025）。有效查询只能引用 OMOP CDM 的表 / 列，并且必须遵循 OMOP 关系与约定（例如通过标准化词汇表进行概念驱动的过滤，以及事件表语义）。引用非 OMOP 模式元素的查询被视为模式漂移（schema drift），并在诊断与基于执行的评测中受到惩罚。

### 2.3. Dataset construction 数据集构建

该基准包含 75 个问题模板，与 OMOP 的连接模式及约定对齐。我们从 EHRSQL 模板集出发（一种面向 EHR 数据的、基于模板的临床 text-to-SQL 资源；（Lee et al., 2023）），建立本地模板池，并保留一个子集以限制结构冗余（即共享同一查询骨架、仅有槽位 / 取值替换或细微表层差异的模板）。随后我们把这些模板适配到 OMOP CDM v5.4 的连接路径与约定，并增加少量 OMOP 特有模板，以更好覆盖代表性不足的领域与连接（例如 note / note_nlp 自由文本表、provider 与 death，以及 episode / episode_event 模式）。

为覆盖与自由文本相连的查询，我们纳入了以 note 与 note_nlp 为中心的模板。在一个本地的、已映射到 OMOP 的 MIMIC-IV 实例中（Johnson et al., 2023; OHDSI, 2025），note 表由 MIMIC-IV NOTE 模块填充，note_nlp 表来自 MedCAT 对放射学报告和出院小结导出的标注（Kraljevic et al., 2021）。我们使用这一已映射到 OMOP 的 MIMIC-IV 环境，是为了反映结构化 OMOP 领域与非结构化文本并存的常见临床仓库设定；它也使我们能在开发期间检查模式连通性与模板的合理性。该环境只用于数据集 / 模板开发；基于执行的评测完全在所发布的合成 OMOP PostgreSQL 数据库上进行（第 2.8 节）。

每个模板通常被实例化为三个（模板, SQL）变体：SQL 结构固定，插入的值（例如 concept ID、患者 ID、阈值、时间窗）变化，从而得到 223 个（模板, SQL）变体。

金标准查询经常使用公用表表达式（common table expressions, CTE；`WITH`），以符合临床分析实践，并使队列定义、时间约束与就诊层级逻辑显式化，从而鼓励结构化的 OMOP 分解，而不是单体式的嵌套子查询。

对每个变体，我们生成 30 种表层形式：1 个规范问题，外加 29 条 GPT-4.1 释义（OpenAI, 2025a）。释义受到约束：（i）保持含义；（ii）类型化标签内的占位取值保持不变。由此得到 6,690 个可回答样例。不可回答问题不计入这一总数；我们仅从 EHRSQL-2024 取用它们，用于弃答评测。发布的 `*.jsonl` 文件在应用第 2.4 节所述的类型化标签与格式规范化之后，把这些不可回答问题与可回答划分放在一起。

**类型化标识符标签。** 标识符被包在轻量的类型化标签中（例如 `<DRUG>...</DRUG>`、`<PERSON_ID>...</PERSON_ID>`）。这些标记没有 XML 语义；它们通过把临床提及表示为 concept_id 值（而不是自由文本提及或 concept_name 字符串），同时显式标明标识符类型，从而实现概念规范化输入。例如，“Did patient 289 take Panadol yesterday?”（患者 289 昨天是否服用了 Panadol？）变为 “Did patient`<PERSON_ID>289</PERSON_ID>` take `<DRUG>839681</DRUG>` yesterday?”。同时标注概念标识符（药物、病情等）与非概念标识符（患者 ID），可以减少歧义，抑制原始整数与 OMOP 字段之间的脆弱关联，并鼓励由模式驱动的推理（把类型化角色映射到正确的 `*_concept_id` 谓词与连接路径，而不是依赖词汇线索）。

**人工核验协议。** 作者复查每条释义，以确保语义等价、全部槽位值与时间约束得以保留，并且没有临床上不合理的增补；不合格者被修改或删除。

### 2.4. Normalization of unanswerables 不可回答问题的规范化

我们使用 EHRSQL-2024 共享任务中的不可回答问题（Lee et al., 2024b）。与 EHRSQL（Lee et al., 2023）一样，当仅凭结构化 OMOP 实例不足以回答时，问题被标为不可回答：它或者（i）需要数据库中未存储的外部 / 规范性临床知识，或者（ii）询问数据库 / 模式之外的信息。

在初始设定中存在一条捷径：不可回答问题往往缺少类型化标签，使“是否带标签”能够预测可回答性。在发布的规范化划分（`*.jsonl`）中，我们通过以下方式减弱这一线索：（i）当出现类似实体的标识符时插入类型化标签；（ii）抽样合成标识符，以镜像可回答样本的分布（例如类似 person 的 ID 长度）；（iii）统一标点，从而削弱“有标签 ⇒ 可回答”这一提示。

### 2.5. Concept-normalized inputs and anti-memorization design 概念规范化输入与抗记忆设计

OMOP 查询通常需要标准化词汇标识符（例如 `*_concept_id`）。由于把表层提及（例如 “troponin”）映射到 OMOP ID 是上游的实体链接步骤，每个样例包含两个对齐的输入：question_name（人类可读的概念名称）与 question_concept（关键实体被替换为 concept ID）。重要的是，两种视图之间没有显式的名称到 ID 的对应：question_name 中的表层概念名称，并不对应 question_concept 中出现的 concept ID。我们同时发布二者，以便阅读和未来的端到端研究，但只报告从概念规范化输入生成 SQL 的结果（图 1），因此指标反映的是在类似金标准的 OMOP 标识符条件下的生成，而不是原始文本的实体链接。为限制虚假的“ID 绑定”，标识符是合成的（类似 concept / person 的整数），并不绑定到真实轨迹；不过其中少数可能对应 OHDSI 标准化词汇表中的公开 OMOP concept_id（Reich et al., 2024）。

### 2.6. Unanswerables & abstention 不可回答问题与弃答

纳入不可回答问题是为了压力测试可靠性。它们既包括规范性 / 外部知识请求，也包括“差一点就在模式内”的模式外查询（例如跨本体的编码查找，如 ICD-11 → ICD-10），以镜像真实用户意图：数据库支持的助手应当安全拒绝，而不是用一条看似合理的代理 SQL 来回答。对这些样例，唯一正确的输出是单个弃答标记 `<NO_SQL>`（没有解释性文字），从而使弃答可供下游路由 / 澄清作机器可执行的处理。

### 2.7. Split protocol 划分协议

在释义很多的数据集上，样例级划分可能泄漏，因此我们在（模板, SQL）变体这一层划分：同一底层查询的释义从不跨划分。对每个模板，至多指定两个变体为已见（seen）；每个已见变体有 30 条释义，按 20/5/5 划入训练 / 验证 / 测试。其余变体均为未见（unseen）；我们为验证抽取 37 个未见变体、为测试抽取 37 个，每个未见变体增加 5 条释义，以评测受控的泛化。不可回答问题按固定比例注入（训练 10%；验证 / 测试 20%），得到 3,312 个训练样例（2,980 个可回答 + 332 个不可回答），验证与测试各 1,162 个样例（930 + 232）。划分是确定性的，固定种子（默认 42），我们发布 JSONL 划分文件以便精确复现。

表 1：可回答样例的数据集汇总统计。

| 类别 | 统计（可回答样例） |
| --- | --- |
| 模板 / 变体 | 75 个模板；223 个（模板, SQL）变体 |
| 规模（可回答） | 6,690 个样例 |
| JOIN（金标准 SQL） | 中位数 1；p90 3；最大 4 |
| CTE 使用（WITH） | 40.36% |
| GROUP BY / DISTINCT | 28.25% / 20.63% |
| ORDER BY / LIMIT | 60.54% / 60.54% |
| 标注（问题） | 标签中位数 1；12.57% 无标签 |
| 最常用的 OMOP 表 | concept (45.74%), visit_occurrence (30.04%), condition_occurrence (26.91%), drug_exposure (21.52%), measurement (17.49%), visit_detail (16.14%), person (13.45%), procedure_occurrence (10.76%), device_exposure (10.76%) |

### 2.8. Synthetic OMOP database for execution-based evaluation 用于基于执行的评测的合成 OMOP 数据库

基于执行的评测是衡量 text-to-SQL 正确性最忠实的办法（Wang et al., 2018），但在使用合成标识符时，即便正确的 SQL 也可能在真实 OMOP 实例上返回空结果。因此我们发布一个受控的合成 OMOP PostgreSQL 数据库，仅用于评测（绝不用于训练）。它是在固定的金标准 SQL 集合之后生成的（post hoc，与模型无关），并且不会根据模型输出被迭代修改：对每条金标准查询，我们在相关 OMOP 表中插入使该查询返回非空结果所需的最少合成行，同时保留基本的异质性（多名患者、多个日期、多个事件）。填充通过 GPT-5.1 辅助的 PostgreSQL 插入脚本完成（OpenAI, 2025b），随后由作者复查、核验并执行；OMOP 完整性约束未被强制（可能存在重复）。所有金标准查询均被验证可以成功执行，我们发布用于全部已报告执行指标的完整数据库转储与画像产物。金标准 SQL 在数据集开发期间，针对一个真实的、已映射到 OMOP 的 MIMIC-IV 环境撰写并验证（第 2.3 节），并在创建该合成实例之前定稿，从而保证查询设计与评测数据库之间没有循环。

画像表明该实例并非平凡：23 张 OMOP 表、117,010 行（约 10 MB），其中包括 1,858 名人员与 6,453 次就诊。事件密度呈强烈的长尾：平均每人 125.48 个事件，中位数为每人 9 个事件，p99 为每人 992.92 个事件，最大为每人 2,374 个事件。就诊层级相当可观（63,826 行 visit_detail，约为 visit_occurrence 的 9.9 倍），使连接路径以及聚合 / 时间逻辑具有挑战性，而不是“玩具式”的。该数据库是为判别性评分而设计的，而不是为流行病学真实性；对相对时间的模板（例如 “today”），我们使用单一固定的参考日期（见第 6 节）。

### 2.9. Models and training setup 模型与训练设置

我们用 LoRA（Hu et al., 2021）微调 Llama-3-8B-Instruct（Grattafiori et al., 2024）。输入遵循 Llama-3 对话模板，并带有固定的系统提示，以强制只输出 SQL 以及 `<NO_SQL>` 弃答；损失只在生成的词元上计算（提示被掩码）。LoRA：r = 32，α = 64，dropout 0.05，应用于注意力与 MLP 投影模块。训练：3 个 epoch，batch 8，梯度累积 4，学习率 1.5 × 10−4，余弦调度，warmup 比例 0.05，可选使用 bf16 和 / 或梯度检查点。

### 2.10. Inference protocol 推理协议

所有模型都使用确定性推理（seed 42；temperature 0.0；top_p 1.0；max_new_tokens 1024），每个样例恰好产生一个输出（SQL 或 `<NO_SQL>`）。输出保存为 JSONL，并在所发布的合成 OMOP PostgreSQL 实例上用同一套基于执行的流程评分。我们对在第一个分号处截断后的原始生成结果评分，不做特定于模型的后处理。

**注入模式的基线提示。** 对基线，我们把一块 OMOP PostgreSQL DDL 模式（仅 OMOP 表 / 列）前置到每个样例的用户消息中，与 Natural-SQL 风格的提示对齐。我们在相同的模式注入设定下运行 Natural-SQL-7B（ChatDB, 2024）（一个公开的 7B ChatDB text-to-SQL 指令模型），以及 Llama-3-8B-Instruct（基座）（Grattafiori et al., 2024）和 Mistral-7B-Instruct-v0.3（Jiang et al., 2023）。尽管提示遵循各模型自己的对话 / 模板约定，我们在所有模型（基线与 LoRA）上保持相同的系统指令，以及相同的“只输出 SQL / `<NO_SQL>`”输出契约；注入的模式块是基线与 LoRA 之间唯一不同的提示内容。

### 2.11. Evaluation metrics 评测指标

我们优先考虑语义正确性与可靠性，并把执行准确率（Execution Accuracy, ExecAcc）以及对风险敏感的可靠性分数（Reliability Score, RS(c)）作为 EHR text-to-SQL 的主要基准指标。其余指标都作为次要分析与诊断来报告。

**主要 text-to-SQL 指标。**

执行准确率（ExecAcc）。预测 SQL 与金标准 SQL 在合成 OMOP 数据库上于 PostgreSQL 中执行（只读事务；每条查询有语句超时）。ExecAcc 只在可回答样例上计算：当且仅当预测不是 `<NO_SQL>`、执行成功，并且返回与金标准查询相同的规范化（与顺序无关）结果集时，该预测为正确。不可回答样例不计入 ExecAcc，而通过 RS(c) 以及面向可回答性的指标来评测。

形式定义。设 A 为可回答样例集合（金标准 ≠ `<NO_SQL>`），且其金标准 SQL 在评测数据库上执行无误。设 q̂_i 为模型输出，Res(q) 为 PostgreSQL 返回的规范化（与顺序无关）结果集。若执行失败（例如语法错误、超时），我们定义 Res(q) = ⊥，因此等式 Res(q̂_i) = Res(q_i) 只可能对成功的执行成立。ExecAcc 计算为：

```
ExecAcc = (1/|A|) Σ_{i∈A} 1[q̂_i ≠ <NO_SQL> ∧ Res(q̂_i) = Res(q_i)]    (1)
```

我们在规范化之后比较金标准结果与预测结果：（i）把 NULL 映射为空字符串；（ii）以原生 Python 类型保留取值（不做字符串强制转换）；（iii）把每一行规范化为其取值的有序元组，先按 Python 类型分组、再按稳定的文本排序键作确定性排序，从而使比较对输出列的置换不变；（iv）对得到的行列表排序，使之与顺序无关。

列名与列顺序被有意忽略。把 NULL 映射为空字符串，可以提高对驱动特定 NULL 处理的稳健性；在我们的评测集中，可回答问题的金标准查询从不返回 NULL 或空字符串，因此这一选择不改变所报告的执行指标。

可靠性分数（RS(c)）。遵循 TrustSQL（Lee et al., 2024a）中提出的、对风险敏感的可靠性评测，我们按五种情形赋予样例级分数，惩罚参数 c ∈ {0, 1, 10}：

1. 可回答 + 正确 SQL → +1
2. 可回答 + 弃答（`<NO_SQL>`）→ 0
3. 可回答 + 不正确 / 失败的 SQL → −c
4. 不可回答 + 弃答（`<NO_SQL>`）→ +1
5. 不可回答 + SQL 尝试 → −c

数据集级 RS(c) 是样例分数的平均；较大的 c 对不安全尝试的惩罚强于对弃答的处理，符合临床偏好：答错比拒绝更糟。报告 c ∈ {0, 1, 10}，是为了显示结论如何从中性设定（c = 0，此时不安全 SQL 尝试并不比弃答受到更重的惩罚）变化到越来越厌恶风险的设定。

**次要指标（支撑分析）。** 我们还报告：（i）可回答性 F1（F1_ans），针对 SQL 与 `<NO_SQL>` 的二选一（回答 vs. 弃答），以“可回答”为正类（SQL = 正，`<NO_SQL>` = 负）；（ii）不可回答召回（Unanswerable Recall, UnansRec），即被预测为 `<NO_SQL>` 的不可回答样本所占比例；（iii）错误弃答（False abstain, %），即可回答样本中被预测为 `<NO_SQL>` 的比例；（iv）F1_exe，它在被尝试的 SQL 输出上概括可执行正确性（按定义 R_exe = ExecAcc），计算为 P_exe 与 R_exe 的调和平均。F1_exe 与 F1_ans 受到 EHRSQL（Lee et al., 2023）的启发。

F1_exe 的形式化。设 A 为金标准 SQL 在评测数据库上无误运行的可回答样例；设 T ⊆ A 为模型输出 SQL 的那些样例（q̂_i ≠ `<NO_SQL>`），C ⊆ T 为执行正确的那些（Res(q̂_i) = Res(q_i)）。与 EHRSQL 不同，我们在 T 上计算 Precision_exe（以金标准可回答为条件），因为对不可回答样本的尝试由我们的弃答 / 可靠性指标处理。因此 Precision_exe = |C|/|T|，Recall_exe = |C|/|A|（= ExecAcc），并且 F1_exe = 2PR/(P + R)，其中 P = Precision_exe，R = Recall_exe。

**辅助的字符串重叠与基于规则的诊断。** 我们报告精确匹配（Exact Match, EM）、规范化精确匹配（Exact Match Normalized, EMN）以及 ROUGE-L，作为字符串重叠诊断，但把它们视为次要指标，因为语义等价的 SQL 在句法上可以不同（例如连接顺序、谓词重排）（Finegan-Dollak et al., 2018）。EM 是精确字符串匹配（Rajpurkar et al., 2016）；EMN 施加轻量规范化（小写化、去掉末尾分号、合并空白）；ROUGE-L 基于最长公共子序列（longest common subsequence, LCS）重叠（Lin, 2004）。我们还报告基于规则的诊断（例如模式漂移、表集合不匹配、方言漂移、就诊层级遗漏），以刻画常见失败模式。
