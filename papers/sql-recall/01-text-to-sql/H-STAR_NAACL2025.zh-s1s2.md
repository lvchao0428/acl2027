# H-STAR: LLM-driven Hybrid SQL-Text Adaptive Reasoning on Tables

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`H-STAR_NAACL2025.pdf`。

## Abstract 摘要

表格推理涉及解释关于表格数据的自然语言查询，其独特挑战在于把语言理解与结构化数据分析结合起来。现有方法或者采用文本推理——它擅长语义解释，但难以处理数学运算；或者采用符号推理——它善于处理计算，但缺乏语义理解。本文提出一种新算法 H-STAR，在两阶段过程中整合符号方法与语义（文本）方法，以应对这些局限。H-STAR 采用：（1）逐步的表格抽取，先做“多视图”（multi-view）列检索，再做行抽取；（2）自适应推理，根据问题类型调整推理策略：对直接查找和复杂词汇查询使用语义推理，同时对定量和逻辑任务用符号推理来增强文本推理。我们的大量实验表明，H-STAR 在三个表格问答（question-answering, QA）和事实验证数据集上显著优于最先进方法，从而突出其有效性与效率。代码与数据见 https://github.com/nikhilsab/H-STAR 。

## 1 Introduction 引言

表格数据是真实世界应用中存储结构化信息最广泛使用的格式之一。表格推理是一个内在困难的问题，需要在非结构化查询和结构化表格上进行逻辑、数学和文本推理（Ye et al., 2023）。因此，理解并推断表格数据已成为自然语言处理中的一个重要研究领域。表格推理任务（图 1），例如基于表格的问答（Pasupat and Liang, 2015; Nan et al., 2022）和基于表格的事实验证（Chen et al., 2019），在过去已被广泛探索。

大语言模型（Large Language Models, LLMs）的进展，通过精心设计的提示，在各种任务上带来了更好的性能。在表格推理领域，已探索符号方法，如 Program of Thought（Chen et al., 2023），以及文本方法，如思维链（Chain of Thought, CoT）（Wei et al., 2022; Brown et al., 2020）。然而，当单独应用时（见图 2），这些方法常常因数值、时间和文本数据的复杂混合，再加上复杂的表结构而陷入困难（Shi et al., 2023; Liu et al., 2023; Sui et al., 2024）。文本推理擅长自然语言理解，但常常误解表结构，并难以进行定量推理。相比之下，基于 SQL 的方法在定量问题求解上很强，但在噪声或非结构化输入上表现较差（Liu et al., 2023）。因此，仅依赖文本或符号推理的近期技术（Cheng et al., 2022; Ye et al., 2023; Wang et al., 2023; Nahid and Rafiei, 2024）也有类似局限。所以，探索如下问题至关重要：如何把符号方法与文本方法整合进一种混合的表格推理方法，以利用它们的互补优势，同时缓解各自的局限？

本文引入 H-STAR，它结合 LLM 的符号推理能力与文本推理能力，从而两全其美。H-STAR 把表格推理任务分解为两个子任务：（a）表格抽取（Table Extraction）和（b）自适应推理（Adaptive Reasoning）。在表格抽取阶段，我们采用逐步的“多视图”链：首先利用原始表及其转置形式识别相关列。然后用过滤后的表进行行抽取；这与其他方法相反，其他方法对行选择和列选择都使用原始表（Ye et al., 2023; Nahid and Rafiei, 2024）。聚焦相关单元格，通过提供正确的上下文来帮助 LLM，从而减少推理中的幻觉。我们在 H-STAR 的表格抽取阶段组合基于 SQL 和基于文本的技术。在自适应推理阶段，我们利用 LLM 的语言理解能力，用少样本示例引导它们决定何时用符号（SQL）方法来支持语义方法。H-STAR 普遍采用语义推理：对直接查找、常识和复杂词汇查询只使用语义推理；对定量、数学和逻辑任务则额外使用一个 SQL 步骤。这一策略优化了在多样问题类型上的性能，在需要时用计算来支持文本理解。

我们在涉及表格 QA 和表格事实验证的三个表格基准上展示 H-STAR 的效力。实验表明，使用与多视图抽取和自适应推理对齐的 H-STAR 组合方法，优于所有先前的最先进方法。我们的分析表明，H-STAR 在不同 LLM 上稳健且可泛化，在各种任务上展示出更强的推理能力。我们的主要贡献如下：（a）我们引入 H-STAR，一种两步方法，把表格抽取与自适应推理统一起来，以增强表格推理上的性能。它是一种混合方法，有效整合符号（SQL 逻辑）与语义（文本）方法。（b）通过大量实验，我们表明 H-STAR 的混合方法超越仅依赖符号或仅依赖语义技术的最先进方法，尤其是在更大的表上推理时。（c）我们的消融研究与分析突出 H-STAR 在各种模型和数据集上的表格抽取与推理效果，强调每个阶段对提升总体性能的重要性。代码与其他资源见 https://hstar-llm.github.io/ 。

图 1 说明不同的表格推理任务：（a）事实验证、（b）短形式 QA、（c）长形式 QA。对每个任务，问题 Q 与其答案 A 配对，答案因任务而异。证据给出回答问题所需的相关列和行。可辨认的示例为：

- 事实验证。Q: NY Americans did not qualify for playoffs in 1936/37。证据：Columns: [year, national cup]；Rows: [1]。A: False。
- 短形式 QA。Q: When did NY Americans win the cup after 1936? 证据：Columns: [year, playoffs]；Rows: [1, 18]。A: 1953/54。
- 长形式 QA。Q: How was the cup performance in 1936/37 and 1953/54? 证据：Columns: [year, national cup]；Rows: [1, 18]。A: NY Americans won the national cup in 1936/37 and 1953/54。

表中可见年份包括 1935/36、1936/37、1953/54、1954/55，以及 Champion、DNQ、No playoff 等单元格；行列对齐在抽取中有粘连，【抽取不清】。

图 2 说明表格推理的复杂性以及整合方法的必要性：（a）原始表；（b）符号推理误解问题，返回一个值而不是 yes/no 回答；（c）基于文本的方法未能正确求解数学问题，导致错误答案。可辨认的片段包括：问题 “did the new york americans win the national cup in 1936?”，SQL 为 ``SELECT `national cup` FROM w WHERE `year` = '1936/37'``，以及文本推理给出 “yes”；另一问题 “how long did it take for the new york americans to win the national cup after 1936?”，符号侧称 1936 之后球队赢得全国杯的实例是 1953，因此答案是 18，对应 SQL 片段 ``SELECT (CAST(SUBSTR(year, 1, 4) AS INTEGER) - 1936) AS years_after_1936 FROM ...``。图中其余单元格【抽取不清】。

## 2 H-STAR Approach H-STAR 方法

H-STAR 把表格推理任务分解为抽取阶段和推理阶段，把 LLM 的文本理解与符号推理结合起来。它把原始表（T）转换为针对查询的表（T_CR）（参见算法 1）。图 3 说明我们的 H-STAR 方法。与 DATER（Ye et al., 2023）和 TabSQLify（Nahid and Rafiei, 2024）不同——它们分别使用文本推理和 text-to-SQL——H-STAR 以互补方式把两种推理整合进表格抽取。我们的推理步骤对定量问题在语义方法之外动态使用符号技术，从而克服纯文本推理的限度。H-STAR 在两个主要阶段中运行：1）表格抽取；2）自适应推理。实现细节，包括提示、输入表格式和超参数，见附录 C 和 D。

### 2.1 Table Extraction 表格抽取

二维表由列和行组成。表格抽取涉及两步推理链：（1）列抽取和（2）行抽取（见图 3）。如算法 1 所示，对给定表 T，表格抽取基于输入查询 Q 返回表 T_CR（第 1–8 行）。

**列抽取。** 如算法 1 所示，H-STAR 使用“多视图”技术：先用原始表 T（第 1 行），再用其转置形式 T_T（第 2 行）做列抽取。改变“视图”起到验证器的作用，考虑到因表结构而遗漏的任何信息，从而提高总体性能（见附录 A.3）。在图 3 中，给定输入表 T 和问题 Q（“How long did it take the New York Americans to win the National Cup after 1936?”），LLM 使用 col_sql 生成一条 SQL 查询来抽取列 “year”（C_1）。随后是基于文本的步骤 col_text，它处理表 T_T 并返回列 C_2（“year”、“national cup”）。这一步捕捉到与回答该查询相关的 “national cup” 信息，而这是 col_sql 所遗漏的。然后对表 T 按从 C_1 和 C_2 得到的列 “year”、“national cup”（C′）进行过滤，得到表 T_c（第 3、4 行）。

**行抽取。** 在得到带有相关列的过滤表 T_C 之后（算法 1 第 4 行），H-STAR 进入行抽取阶段，最终得到针对查询的表 T_CR（第 5–8 行）。过滤表 T_C 的词元数少于 T，从而落在词元限制之内，并使行抽取更高效。如图 3 所示，row_sql 在列过滤后的表 T_C 上生成的 SQL 查询抽取相关行 R_1（“row 18”）。尽管它返回了合适的行，仍不足以回答该问题。为克服这些局限，我们使用基于文本的行验证 row_text 来获得缺失的行，最终检索到 “row 1” 和 “row 18”（R_2）。合并 R_1 和 R_2 得到相关行 R′（“row 1”、“row 18”），从而得到最终表 T_CR。

算法 1：H-STAR。输入：(T, Q) → 表–问题对。输出：Â → 预测答案。

```
Stage A: Table Extraction
Column Extraction
1: C_1 ← colsql(T, Q)          ▷ SQL 方法
2: C_2 ← coltext(T_T, Q)       ▷ 文本方法；T_T 指转置表
3: C′ ← C_1 ∪ C_2
4: T_C ← T.filter(C′)          ▷ 用列 C′ 过滤表 T，得到 T_C
Row Extraction
5: R_1 ← rowsql(T_C, Q)        ▷ SQL 方法
6: R_2 ← rowtext(T_C, Q, R_1)  ▷ 文本方法
7: R′ ← R_1 ∪ R_2
8: T_CR ← T_C.filter(R′)       ▷ 用行 R′ 过滤表 T_C，得到 T_CR
Stage B: Adaptive Reasoning
9:  if math(Q) == True then
10:   E_v ← fsql(T_CR, Q)
11:   Â ← ftext(T_CR, Q, E_v)   ▷ 用 SQL 生成的 E_v 与 T_CR 生成 Â
12: else
13:   Â ← ftext(T_CR, Q)        ▷ 只用表 T_CR 生成 Â
14: end if
15: return Â
```

### 2.2 Adaptive Reasoning 自适应推理

我们提出一个自适应推理框架：它利用文本推理的优势，同时通过符号推理缓解其定量局限。首先，我们提示 LLM 利用其语言理解能力来评估查询需求。我们对需要定量分析的查询应用符号推理，并把生成的输出（E_v）与表（T_CR）一起作为最终文本推理步骤的输入。例如，在图 3 中，面对 “How long did it take the New York Americans to win the National Cup after 1936?” 这样的问题时，LLM 需要计算答案，我们的流水线通过 SQL 生成的代码优先进行符号推理（f_sql）。该代码在 SQL 引擎上执行，从而从表 T_CR 得到精确答案。这一基于 SQL 的评估输出 E_v 作为额外证据，支持最终推理步骤（f_text）。通过显式整合这一定量方法，我们的算法有效应对 LLM 在处理定量推理上的局限，从而提高处理需要数值推理的问题时的准确率与稳健性。

图 3：H-STAR 概览，由代码生成与基于文本的验证组合而成。给定一张复杂的表及其问题，H-STAR 通过以下方式回答：（a）表格抽取：先选择列、再选择行，从原始表中抽出针对问题的表。（b）自适应推理：当问题含有任何数学成分时，用 SQL 生成一张额外的表，用于文本推理步骤。图中流程图的箭头与中间表在抽取中大面积粘连，【抽取不清】。可辨认的 SQL 片段包括 ``SELECT year FROM w;``，以及 ``SELECT * FROM w WHERE (CAST(SUBSTR(year,1,4) AS INTEGER) > 1936 AND `national cup` = 'champion'``（该条在抽取中未闭合）。最终表 T_CR 中可见 row_id 1 为 1936/37 Champion，row_id 18 为 1953/54 Champion。
