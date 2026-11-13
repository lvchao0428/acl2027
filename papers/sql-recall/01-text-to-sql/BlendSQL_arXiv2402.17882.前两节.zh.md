> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名：** `BlendSQL_arXiv2402.17882.pdf`

**原文标题：** BLENDSQL: A Scalable Dialect for Unifying Hybrid Question Answering in Relational Algebra

**作者：** Parker Glenn、Parag Pravin Dakle、Liang Wang、Preethi Raghavan（Fidelity Investments, AI Center of Excellence）。

**场合：** arXiv:2402.17882v2 [cs.CL]，2024 年 6 月 10 日。首页未印会议名称。

## 摘要

作者把现有混合问答的端到端系统概括成 “prompt-and-pray”：用户既控制不了、也看不清中间推理，而且 transformer LLM 的上下文装不下完整的结构化和非结构化内容，零样本尚且勉强，少样本更不现实。BLENDSQL 被定义成 SQLite 的超集，用来把结构化数据和无结构数据上的推理收成一种方言。对需要多跳的混合问答，整条分解后的推理路线写进一条可解释的 BLENDSQL 查询。

摘要里已经给出的结果句是：BLENDSQL 可以扩到很大的数据集，并在少用 35% prompt token 的情况下提高端到端系统的表现。没有指向表号。代码以包的形式放在 `github.com/parkervg/blendsql`。

## 1 Introduction

第 1 节的主线是：混合问答不该再用自然语言当中间推理，而该用关系代数能执行的 SQL 式程序。问题分解一段先承认显式中间步骤有用：Scratchpad（Nye et al., 2021）预测完整执行轨迹能改善微调后的执行输出；后来的提示方法也是先把难题拆成小步再给答案（Wei et al., 2022; Yao et al., 2023; Wang et al., 2022）。作者的批评是这些方法的中间表示仍是自然语言，有损且有歧义。BLENDSQL 改用类似 SQL 的语法，借助关系代数的组合性（Codd, 1970）让推理更确定，中间步骤也更好读。图 1 是一条 OTT-QA 开发集例子的 BLENDSQL 表示，图中查询文本抽取不全。

接着用四块相关工作把差异说清。Agent 文献把任务交给很窄的专家，再靠 router 或 planner 拆任务（Parisi et al., 2022; Liang et al., 2022; Schick et al., 2023 等）；LLM 当 planner 时输出子任务列表、该用哪个 agent、输入和期望返回。BLENDSQL 的 parser 也是 planner，负责生成回答问题要用的 API，文中称为 Ingredients。差别在于它不满足于生成一段复杂分解的字符串，而是用抽象语法树把分解收成一条字符串；它也不是只把原句改写成形式结构（Lu et al., 2021; Wu et al., 2022），还会利用参考数据库、输入提示和模型内部知识补信息。Text-to-SQL 一段点出 Spider（Yu et al., 2018）上少样本或零样本已经很强，并举 Hu et al. (2022) 把对话状态跟踪写成 text-to-SQL、用 SQL 当中间表示的先例。Hybrid Question Answering 被定义成：用表格语料加上非结构化多模态内容回答问题；本文重点是表格加无结构文本，图像等格式留到附录 C。已有工作里，Li et al. (2021) 在端到端模型和产出 SQL 的解析器之间做路由，但两边不能互相传信息。UniK-QA（Oguz et al., 2022）把结构化表转成文本；本文相反，把无结构文本转成表。作者认为 `<subj, pred, obj>` 这种三元组盖不住嵌在文档、音频或列名里的复杂关系。和本文最近的是 BINDER（Cheng et al., 2023）。三点差别写在第 1 节末尾：API 专为 SQL 设计，能在含无结构内容的多表库上执行并优化 JOIN、别名、条件表表达式和大多数 SQLite 操作；按数据库 schema 做约束解码；用户可以自己加任意多个自定义函数，放进 BLENDSQL 脚本。

**1.1 Main Contributions。** 贡献被收成三条：据作者所知，第一次把混合问答的上下文框成关系数据库；放出开源查询语言 BLENDSQL，用来编排并优化跨 SQL 逻辑和 LLM 推理的混合函数；只用少量上下文示例，BLENDSQL 就能超过端到端方法，token 少 35%，而且 parser 不直接看到无结构上下文。这句没有指向表号。后文实验不在这里展开。

## 2 BLENDSQL: Overview

第 2 节把系统定义成 SQLite 的超集。一条脚本执行后返回 smoothie：里面有最终结果，也有走过的中间推理。比喻是配料（ingredients）加搅拌机（blender）。

**2.1 Blender vs. Parser。** blender 是真正执行每条 ingredient 函数、接收相应提示的 LLM。parser 在执行前拿到一组少样本示例，再根据问题和数据库上下文生成 BLENDSQL 查询。核心实验里两者都用 GPT-4-0613（Achiam et al., 2023）。

**2.2 Ingredients。** ingredient 是把一部分逻辑交给 LLM 函数的子程序，语法上用双花括号 `{{` 和 `}}` 标出。整个方言是用 PyParsing（McGuire, 2007）实现的解析表达式语法。和普通 SQL 一样，ingredient 调用可以递归，传给一个调用的上下文里可以再调用别的 ingredient。三种内置函数是这一节的核心定义。LLMMap 是一元标量函数，类似 SQLite 的 `LENGTH` 或 `ABS`：接受 `"table::column"` 形式的表和列，对目标列的每个值做映射，结果写成临时表里的新列。若列中有 \(n_c\) 个值，\(V=\{v_i\}\)，则 \(f_{map}(V)\rightarrow\{v'_1,\ldots,v'_{n_c}\}\)。图 2 的例子是对每个值问 “Is this a team event?”；同一列里 “team event”“4x100 medley relay” 等写法不统一，纯字符串规则很难覆盖整张表，LLMMap 按语义指称做统一变换。LLMQA 是聚合函数，把表子集 \(T\) 收成一个标量 \(v'\)，即 \(f_{qa}(T)\rightarrow v'\)。`options` 参数可以把输出限制成某一列里已经存在的值；约束解码用 guidance，通过 OpenAI API 的 `logit_bias` 实现。图 2 里它收到一段无结构文档和问题 “Which NBA season was suspended due to COVID-19?”，并用一组列值限制生成。事实核验用的变体叫 LLMValidate，只返回 true 或 false。LLMJoin 在两组值 \(V_1,V_2\) 之间做自定义映射，再建成辅助表去做 SQL 的 `INNER JOIN`：\(f_{join}(V_1,V_2)\rightarrow\{(v1'_1,v2'_1),\ldots\}\)。它针对没有正规外键、但语义上仍能对齐的情况。图 2 的例子是 “joshua fields” 和 “josh fields (pitcher)” 指向同一实体，相当于做实体链接。表 1 给出与后文图 3 对齐的 HybridQA 库配置：上表 `w` 是维基页面上的结构化表（列 `name`、`position`、`school`，示例行包括 joshua fields / university of georgia 等），下表 `documents` 是文章无结构内容（列 `title`、`content`），并用 FTS5 建索引。

**2.3 Query Optimizations。** 能先做的 SQL 谓词放进子查询，结果放进会话临时表。原生 SQLite 便宜，昂贵的 LLM ingredient 只应看到生成忠实结果所必需的那一份数据，不能多也不能少。文中的例子是：只把 `w` 里 `w.school = 'university of georgia'` 的行子集交给 LLM ingredient。这些优化用一套测试套件验证。第 2 节到此结束，数据集从第 3 节 Datasets 起。
