> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名：** Jin_annotation-error_arXiv2601.08778.pdf

**原文标题：** Pervasive Annotation Errors Break Text-to-SQL Benchmarks and Leaderboards

**作者：** Tengjun Jin、Yoojin Choi、Yuxuan Zhu、Daniel Kang，均为 University of Illinois (UIUC)，Urbana，USA。

**arXiv：** arXiv:2601.08778v3 [cs.AI]，2026 年 1 月 19 日。DOI：https://doi.org/10.48550/arXiv.2601.08778 。

## 摘要 Abstract

公开基准和排行榜是比较 text-to-SQL 方法、决定部署哪一个的依据，而出题和判分都依赖人工标注，标注是否成立决定榜单能不能信。本文做两项实证：统计 BIRD 与 Spider 2.0-Snow 的标注错误率，并改正 BIRD 开发集（Dev）的一个子集，看错误怎样改写智能体成绩和名次。

摘要所报的后文主结果可以收成一句：专家分析显示 BIRD Mini-Dev 与 Spider 2.0-Snow 的错误率分别为 52.8% 和 62.8%；把 BIRD 榜上全部 16 个开源智能体放到原始子集和改正后的子集上重评，相对性能变化为 −7% 到 31%，名次变化为 −9 到 +9；未改正子集的名次与完整 Dev 强相关（Spearman’s \(r_s=0.85\)，\(p=3.26\times10^{-5}\)），与改正后子集只弱相关（\(r_s=0.32\)，\(p=0.23\)）。摘要未标表号。代码与数据：https://github.com/uiuc-kang-lab/text_to_sql_benchmarks 。

## 1 INTRODUCTION

作者认为现有 text-to-SQL 基准不可靠，是因为标注错误。先前工作已经报过：BIRD 的 Mini-Dev 里 32% 的例子有标注错误 [4]，金融领域例子里为 49% [56]。为了看怎样把错误压到最低，本文按四种反复出现的模式检查标注。给定目标库 \(D\)，每个例子包含自然语言输入 \(T\) 和标准 SQL \(Q\)；脚注说明 \(T\) 由用户问题组成，也可以带外部知识。四类错误是：E1，\(Q\) 的语义和 \(T\) 的逻辑不一致；E2，对数据或 schema 理解不足，使 \(Q\) 和 \(D\) 对不上；E3，\(Q\) 与 \(T\) 所涉领域知识不一致，或 \(T\) 里的领域知识标错；E4，\(T\) 有歧义，包括多种解释或输出格式不清楚。Figure 1 给了两个实例。Spider 2.0-Snow 的 sf_bq291（E1）问 2019 年 7 月、纬度 26.75、经度 51.5、半径 5 km 内的逐日天气，SQL 写成 `ST_POINT(26.75, 51.5)`，而 Snowflake 的 `ST_POINT` 要求先经度后纬度，参数顺序被写反。BIRD Mini-Dev 例 46（E3）问州立特殊学校里 1 至 12 年级入学人数最多的学校，外部知识把 “grades 1 through 12” 写成 K-12、把 State Special Schools 写成 `DOC = 31`，SQL 按 `Enrollment (K-12)` 降序取第一；问题在于 K-12 含幼儿园，并不等于 1 到 12 年级。更多例子留在第 4.4 节。

核查是人在回路中的三阶段，最终判断都由人类 SQL 专家做。为了减轻人工，作者做了 SAR-Agent（SQL Annotation Reviewer agent），称其为第一个协助专家发现 text-to-SQL 标注错误的 AI 智能体。三阶段是：SAR-Agent 给每条标注出诊断报告；专家复核所有被标出的案例，核对错误理由并给出最终对错；专家再按反复出现的错误模式，把人工复查扩到更多例子。改正则用 SAPAR（SQL Annotation Pipeline with an AI Agent Reviewer），把 SAR-Agent 接进 BIRD 那套标准标注流程。作者从 1,534 条 BIRD Dev 中随机抽 100 条，在 SAPAR 引导下改完全部查出的错误，再把 BIRD 榜上 16 个开源智能体同时放到原始子集和改正后的子集上重评。

引言随后直接给出三项发现。错误面比先前认识的更宽：人工核验后，BIRD Mini-Dev 有 52.8% 的例子含标注错误，作者称这比先前报告的 32.3% 高出 20.5%；Spider 2.0-Snow 作为 Spider 1.0 的后继，此前没有被这样全面查过，原团队用大语言模型改写问题以求更清楚，第一轮改正了 45% 的例子、第二轮改正了 5%，但在全部 121 道公开了标准 SQL 的题上，错误率仍为 62.8%。这些错误会严重改写成绩和名次：16 个智能体的相对性能变化为 −7% 到 31%，名次变化为 −9 到 +9；其中 CHESS 在这 16 个里原列第 7，改正后从 62% 升到 81%，升到第 1。原始 Dev 子集上的名次与完整原始 Dev 的 Spearman \(r_s=0.85\)（\(p=3.26\times10^{-5}\)），与改正后子集只有 \(r_s=0.32\)（\(p=0.23\)）。SAR-Agent 在 BIRD Mini-Dev 上的精确率为 83%，在尚无先前分析的 Spider 2.0-Snow 上为 89%；对照 Arcwise 专家报告的 161 个错误例子，命中率 85.7%，并且比 Arcwise 多找出 41.6% 的错误例子。贡献对应这三块：给出 52.8% 与 62.8% 两个错误率；用 16 个智能体的重评显示相对变化 −7% 到 31%、名次 −9 到 +9；提出由 SAR-Agent 和 SAPAR 组成的检测与改正工具。

## 2 EXPERIMENT DESIGN

实验围绕三个问题设计：Q1，常用 text-to-SQL 基准的标注错误率是多少；Q2，这些错误怎样影响智能体的成绩和榜上名次；Q3，SAR-Agent 发现错误的效果如何。基准选 BIRD 和 Spider 2.0-Snow，依据是使用广度和查询复杂度。使用广度用各榜已评测方法数衡量，复杂度用标准 SQL 的平均 token 数衡量，分词方式是按空白切分，比较范围是六个基准。Figure 2 的数据截止 2025 年 10 月 20 日；文中给出的读数是，BIRD 榜上已评测方法最多，为 100 个，Spider 2.0-Snow 的标准 SQL 最复杂，平均 161.8 个 token，并且它是 Spider 1.0 的后继。脚注说明只看 BIRD 的 Dev：训练集主要给微调用，测试集不公开，研究者本地评测和错误分析都靠 Dev。Spider 2.0 的标准查询在 2025 年 10 月 29 日更新过，本文评测更早，用的是 2025 年 8 月 20 日的标注，提交位于 https://github.com/xlang-ai/Spider2/tree/84911f375c87903c73ed5fe93769b593a14efb42/spider2-snow/evaluation_suite/gold/sql 。

工具包由 SAR-Agent 和 SAPAR 组成，用来协助人工分析和改正标注。检测时，SAR-Agent 为每条例子生成诊断报告，再由 SQL 专家复核并给出最终对错；改正时，按 SAPAR 手工修改抽到的那份 BIRD Dev 子集。二者的实现放在第 3 节。

评测安排与三个问题对齐，本文第 2 节只给出路线，不展开后文结果。第 4 节用三步检查程序统计 BIRD Mini-Dev 和 Spider 2.0-Snow 的错误率，回答 Q1。第 5 节从 BIRD Dev 抽 100 例，用 SAPAR 改正后，把榜上全部 16 个开源智能体在原始版和改正版上重评，看执行准确率和相对名次，回答 Q2。第 6 节评 SAR-Agent 本身，并与 Arcwise 的 SQL 专家审计 [4] 比较检出数量，回答 Q3。
