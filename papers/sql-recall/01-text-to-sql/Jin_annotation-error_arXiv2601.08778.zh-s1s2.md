# Pervasive Annotation Errors Break Text-to-SQL Benchmarks and Leaderboards

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`Jin_annotation-error_arXiv2601.08778.pdf`。

## Abstract 摘要

研究者提出了大量 text-to-SQL 技术，以简化数据分析并加速数据驱动应用的开发。为比较这些技术并选出最适合部署的方案，社区依赖公开基准及其排行榜。由于这些基准在问题构建与答案评测中严重依赖人工标注，标注是否有效至关重要。

本文开展一项实证研究：（i）测定两个广泛使用的 text-to-SQL 基准 BIRD 与 Spider 2.0-Snow 的标注错误率；（ii）修正 BIRD 开发集（development, Dev）的一个子集，以衡量标注错误对 text-to-SQL 智能体（agent）性能与排行榜排名的影响。通过专家分析，我们表明 BIRD Mini-Dev 与 Spider 2.0-Snow 的错误率分别为 52.8% 与 62.8%。我们在原始与修正后的 BIRD Dev 子集上，重新评测了 BIRD 排行榜上全部 16 个开源智能体。结果表明，性能变化（按相对值）范围为 −7% 到 31%，排名变化范围为 −9 到 +9 个位次。我们进一步评估这些影响能否推广到完整的 BIRD Dev 集。我们发现，未修正子集上的智能体排名与完整 Dev 集上的排名强相关（Spearman’s 𝑟𝑠=0.85，𝑝=3.26e-5），而与修正子集上的排名弱相关（Spearman’s 𝑟𝑠=0.32，𝑝=0.23）。这些发现表明，标注错误会显著扭曲所报告的性能与排名，并可能误导研究方向或部署选择。代码与数据见 https://github.com/uiuc-kang-lab/text_to_sql_benchmarks。

## 1 Introduction 引言

随着 text-to-SQL 技术对数据分析与数据驱动应用日益重要 [18, 19, 40, 41, 44, 51, 57]，研究者与实践者引入了多种 text-to-SQL 基准 [12, 22, 26, 27, 31, 32, 45, 58, 60, 62]。这些基准引导研究者改进 text-to-SQL 技术，并帮助实践者在真实场景的下游应用中选择最佳的 text-to-SQL 技术。

当前 text-to-SQL 基准因标注错误而不可靠。已有工作报告，BIRD [31] 在迷你开发集（mini development set, Mini-Dev）的样例中有 32% 存在标注错误 [4]，金融领域样例中则有 49% [56]。此类错误会扭曲所报告的智能体性能与排名，并误导研究者与实践者。

为理解如何构建标注错误尽可能少的可靠 text-to-SQL 基准，我们对 text-to-SQL 基准中的标注错误作深入分析。分析基于四种反复出现的 text-to-SQL 标注错误模式。给定目标数据库 D，人工标注者整理 text-to-SQL 样例，每个样例包含自然语言输入 T 与金标准 SQL 查询 Q。¹ 标注错误可以出现在任一单独成分之内，也可以来自各成分之间的不一致，包括：

E1. Q 的语义与 T 的逻辑不匹配。

E2. 由于对数据或模式（schema）理解有限，Q 的语义与 D 不匹配。

E3. Q 的语义与同 T 相关的领域知识不匹配，或 T 中的领域知识标注有误。

E4. T 存在歧义，例如有多种可能解释，或输出格式不明确。

图 1a 展示了对 Snowflake 函数的误用（E1）。图 1b 给出 BIRD 中因标注者缺乏领域知识而产生的错误标注（E3）。各错误模式的更多代表性样例见第 4.4 节。

图 1：来自现有 text-to-SQL 基准、用以展示错误标注的两个例子。

（a）Spider 2.0-Snow 的 sf_bq291。标注者误将 ST_POINT 参数中的经度–纬度顺序对调（E1）。

标注的用户问题：能否提供 2019 年 7 月、纬度 26.75 与经度 51.5 周围 5 km 半径内的每日天气摘要？……

标注的 SQL：

```sql
... ST_DWITHIN(ST_GEOGFROMWKB("TRI"."geography"),
ST_POINT(26.75, 51.5), 5000) ...
```

问题：Snowflake 的 ST_POINT 期望参数顺序为 (longitude, latitude)。该查询传入 ST_POINT(26.75, 51.5)，把顺序颠倒了。

（b）BIRD Mini-Dev 的样例 46。标注者对 “K-12” 理解有限（E3）。

标注的用户问题：哪些州立特殊学校（state special schools）在 1 至 12 年级的入学人数最多？

标注的外部知识：State Special Schools 指 DOC = 31；Grades 1 through 12 意味着 K-12。

标注的 SQL：

```sql
SELECT T2.School
FROM frpm AS T1 INNER JOIN schools AS T2
ON T1.CDSCode = T2.CDSCode WHERE T2.DOC = 31
ORDER BY T1."Enrollment (K-12)" DESC LIMIT 1
```

问题：‘Enrollment (K-12)’ 包含幼儿园（kindergarten），因此并不等同于 1 至 12 年级的入学人数。

¹ 输入 T 由用户问题组成，并可选地包含外部知识。

我们开展了人在回路（human-in-the-loop）的三阶段审计，所有最终决定均由人类 SQL 专家作出，用以测定两个广泛使用的基准 BIRD [31] 与 Spider 2.0-Snow [27] 的标注错误率。为便于审计，我们开发了 SAR-Agent（SQL Annotation Reviewer agent），这是首个协助 SQL 专家检测 text-to-SQL 基准中标注错误的 AI 智能体。三阶段审计包括：（1）SAR-Agent 为每条标注生成诊断报告；（2）人类 SQL 专家裁决所有被智能体标出的案例，核验所述错误原因并赋予最终正确性标签；（3）人类 SQL 专家依据反复出现的错误模式，把人工复查扩展到更多样例。

我们人工修正了 BIRD Dev 集的一个子集，以衡量标注错误对 text-to-SQL 智能体性能与排行榜排名的影响。为支持 SQL 专家进行人工修正，我们引入 SAPAR（SQL Annotation Pipeline with an AI Agent Reviewer），把 SAR-Agent 集成进标准 text-to-SQL 标注流程 [31]。我们从 1,534 个 BIRD Dev 样例中随机抽取 100 个，并在 SAPAR 指导下人工修正全部已识别错误。随后，我们在原始与修正后的 Dev 子集上，重新评测 BIRD 排行榜上全部 16 个开源 text-to-SQL 智能体。

下文我们（i）量化 BIRD Mini-Dev（BIRD Dev 集的官方子集）[31] 与 Spider 2.0-Snow [27] 中的标注错误率，（ii）分析其对智能体性能与排行榜排名的影响，（iii）评估 SAR-Agent 的错误检测能力，以展示其改善基准质量的效用。

**现有 text-to-SQL 基准中的高错误率。** 我们的分析表明，text-to-SQL 基准中的标注错误范围比先前认识到的更广。我们在 BIRD Mini-Dev 与 Spider 2.0-Snow 上运行 SAR-Agent，为每个样例生成诊断报告。经人工核验，我们发现 BIRD Mini-Dev [31] 中 52.8% 的样例含有标注错误，比先前报告的 32.3% [4] 高 20.5%。此外，我们首次全面考察 Spider 2.0-Snow [27] 中的标注错误；该基准近期发布，是广泛使用的 Spider 1.0 [62] 的后继。Spider 2.0 团队使用大语言模型（large language models, LLMs）改写用户问题以提高清晰度，并在第一轮验证中修正了 45% 的样例、在第二轮中修正了 5% [27]。尽管如此，在金标准 SQL 公开可用的全部 121 个问题中，我们仍识别出 62.8% 的标注错误率。

**BIRD 排行榜不可靠。** 这些标注错误造成对智能体性能的严重误估与错误排名。通过对 16 个智能体在原始与修正后的 BIRD Dev 子集上的重新评测，我们发现显著的性能变化：相对值范围为 −7% 到 31%，排名位置变化范围为 −9 到 +9。例如，CHESS [51] 此前在我们选定的 16 个智能体中排名第 7，修正后性能从 62% 提高到 81%，并升至第 1 位。

我们进一步计算了两个 Spearman 秩相关系数（𝑟𝑠），以评估标注错误对智能体排名的影响。我们发现，原始 Dev 子集上的排名与原始完整 Dev 集上的排名强相关（𝑟𝑠=0.85，𝑝=3.26e-5），但与修正后 Dev 子集上的排名相关很弱（𝑟𝑠=0.32，𝑝=0.23）。

这些结果表明，标注错误会扭曲所报告的性能与排名，削弱排行榜的可靠性。这种不可靠性可能误导研究者与实践者改进 text-to-SQL 技术，以及挑选最佳智能体。

**SAR-Agent 的有效性。** SAR-Agent 在检测标注错误方面是有效的。我们对每条标注样例的诊断报告作人工核验，表明 SAR-Agent 在 BIRD Mini-Dev 上达到 83% 的精确率（precision）。在此前尚无分析的 Spider 2.0-Snow 上，SAR-Agent 达到 89% 的精确率。我们进一步把 SAR-Agent 在 BIRD Mini-Dev 上检出的错误样例（经人工核验后）与 Arcwise 团队 SQL 专家所报告的结果 [4] 进行比较。在所报告的 161 个错误样例中，SAR-Agent 的命中率（hit rate）为 85.7%。SAR-Agent 识别出的错误样例也比 Arcwise 多 41.6%。

我们的贡献总结如下：

（1）通过 SQL 专家的深入人工复查，我们发现 BIRD Mini-Dev 的标注错误率为 52.8%，Spider 2.0-Snow 为 62.8%。

（2）通过重新评测 BIRD 排行榜上全部 16 个开源 text-to-SQL 智能体，我们发现显著的性能变动：相对性能变化范围为 −7% 到 31%，排名变化范围为 −9 到 +9。

（3）我们引入由 SAR-Agent 与 SAPAR 组成的工具包，用于标注错误的检测与修正。

## 2 Experiment Design 实验设计

本工作开发一个工具包，帮助人类 SQL 专家分析并修正现有 text-to-SQL 基准，并从中形成认识。我们设计实验以研究下列问题：

Q1. 广泛使用的 text-to-SQL 基准中，标注错误率是多少？

Q2. 标注错误如何影响 text-to-SQL 智能体在排行榜上的性能与排名？

Q3. SAR-Agent 检测标注错误的效果如何？

### 2.1 Benchmark Selection 基准选择

我们基于使用情况与查询复杂度，为本实证研究选择了两个 text-to-SQL 基准：BIRD [31] 与 Spider 2.0-Snow [27]。² 我们以各基准排行榜上被评测方法的数量来量化使用情况，并以六个基准 [27, 31, 52, 53, 62] 中金标准 SQL 查询的平均词元数（采用空白分词（whitespace tokenization）[27]）来量化复杂度。如图 2 所示，BIRD 排行榜上被评测的方法数量最多（100）。Spider 2.0-Snow 的 SQL 查询最为复杂（其金标准 SQL 查询的平均词元数最高，每条 SQL 查询 161.8 个词元），并且是广泛使用的 Spider 1.0 [62] 的后继。

图 2：各 text-to-SQL 基准排行榜中被评测方法的数量，以及金标准 SQL 的词元数（数据截止：October 20, 2025）。除正文已给出的 100 与 161.8 外，图中其余序列未被抽成文字，【抽取不清】。

² BIRD 注：BIRD 由 Train、Dev 与 Test 集组成。我们聚焦 Dev 集，因为（i）Train 集只用于微调 LLM 的研究，（ii）Test 集是隐藏的，（iii）研究者依赖 Dev 集做本地评测与错误分析。Spider 2.0-Snow 注：Spider 2.0 的金标准查询于 Oct. 29, 2025 更新。由于我们的评测在此之前完成，我们使用截至 Aug. 20, 2025 的标注，见 https://github.com/xlang-ai/Spider2/tree/84911f375c87903c73ed5fe93769b593a14efb42/spider2-snow/evaluation_suite/gold/sql 。

### 2.2 Toolkit for Annotation Error Detection and Correction 标注错误检测与修正工具包

我们开发了由 SAR-Agent 与 SAPAR 组成的工具包，以方便人工分析并修正 text-to-SQL 标注错误。在错误检测中，我们在标注上运行 SAR-Agent，生成逐样例的诊断报告。随后由 SQL 专家复查所报告的问题，并赋予最终正确性标签。在标注错误修正中，我们依据 SAPAR，在抽样得到的 BIRD Dev 子集里人工修复已识别的错误。SAR-Agent 与 SAPAR 的实现细节见第 3 节。

### 2.3 Evaluation Overview 评测概述

我们围绕研究问题来组织实验。在第 4 节，我们用三步检查程序检测两个广泛使用的基准 BIRD Mini-Dev [31] 与 Spider 2.0-Snow [27] 中的标注错误，并量化其错误率，以回答 Q1。在第 5 节，我们从 BIRD Dev 集抽取 100 个样例，并应用 SAPAR 人工修正标注错误。为回答 Q2，我们随后在该抽样子集的原始版本与修正版本上，重新评测 BIRD 排行榜列出的全部 16 个开源智能体，并量化执行准确率（execution accuracy）的变化以及这些智能体之间的相对排名。在第 6 节，我们评估 SAR-Agent 的性能，并将其检出的错误数量与 Arcwise 的 SQL 专家在先前审计中识别出的错误 [4] 进行比较，以回答 Q3。
