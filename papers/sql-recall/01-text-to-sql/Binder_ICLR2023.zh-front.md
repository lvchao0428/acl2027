> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文标题：** Binding Language Models in Symbolic Languages

**作者：** Zhoujun Cheng、Tianbao Xie、Peng Shi、Chengzu Li、Rahul Nadkarni、Yushi Hu、Caiming Xiong、Dragomir Radev、Mari Ostendorf、Luke Zettlemoyer、Noah A. Smith、Tao Yu。Cheng 与 Xie 为同等贡献，作者按字母序排列，工作主要在 The University of Hong Kong 完成。单位还包括 Shanghai Jiao Tong University、University of Washington、Allen Institute for AI、University of Waterloo、Salesforce Research、Yale University、Meta AI。

**场合：** ICLR 2023 会议论文。页脚同时标 arXiv:2210.02875v2 [cs.CL]，2023 年 3 月 1 日。

**PDF：** `Binder_ICLR2023.pdf`

## 摘要

文章的对立面是端到端神经网络：性能和易用性占优，但缺少可解释性和稳健性。作者提出 BINDER，一个免训练的神经–符号框架，把任务输入映成一段程序。这段程序做三件事：把语言模型的能力绑成统一 API，接到 SQL、Python 等编程语言上，从而补上原语法覆盖不到的问题；同一个 LM 既当程序解析器，又当执行时被 API 调用的模型；标注只需要少量 in-context exemplars。具体 LM 用 GPT-3 Codex。

解析阶段，Codex 靠少量示例找出原编程语言答不了的部分，生成调用 Codex 的 API，并把它插到仍符合原语法的位置。执行阶段，API 提示里的 Codex 可以做常识问答、信息抽取等。摘要给出的结果主张是：WIKITABLEQUESTIONS 和 TABFACT 上达到当时最优，而且输出的是可调试的显式程序。对比被写得很具体：此前最好系统都在数万条任务样本上微调，BINDER 不用训练，只用几十条例子。代码在 https://github.com/hkunlp/binder 。

## 1 Introduction

第 1 节用两条路线的短处互相压。端到端系统直接从输入映到输出（Devlin et al., 2019; Liu et al., 2019; Lewis et al., 2020; Raffel et al., 2020），灵活但不可解释、不稳健。符号系统产出逻辑形式、推理路径或程序再执行（Zettlemoyer & Collins, 2005; Gulwani et al., 2017; Chen et al., 2019b），中间形式让它对输入变化更稳，但语义覆盖被所选符号语言的语法卡住。文中的例子是图 1 里的 “North America?”：纯 SQL 写不出来。中间形式还要专家标注。

已有神经–符号工作（Andreas et al., 2016; Gupta et al., 2019; Khot et al., 2021; Zhu et al., 2022）被批评为：符号语言和对应神经模块都要为特定领域手工设计，还要大量训练数据校准。换任务就要换语言和模块，覆盖仍被定制语法限制。作者要的是：神经模块调用更灵活、符号语言覆盖更高，同时只要很少标注。

BINDER 的定义在这里收束。输入被映成可执行的 BINDER program（图 1 中的 Binder-SQL、Binder-Python），编程语言绑定一个统一 API 去调用 LM（Brown et al., 2020; Chen et al., 2021），示例只是少量“输入–BINDER 程序”对。解析时 Codex（代码预训练的 GPT-3）要决定三件事：哪些片段能直接写成目标语言（图 1 灰色部分）；其余片段对应什么 API，例如 `f("North America?"; Made_in)`；API 插在程序的哪里。执行时再次提示 Codex，把 API 的返回接回编程语言。图 1 的具体数据流是：提示 “North America?” 加上列 `Made_in`，Codex 输出一列 yes/no，表示该国是否在北美；去掉 API 后的标准程序由确定性解释器算出最终答案。

图 1 的问句是：Which is the best-selling shirt made in North America and with no chemicals? Binder-SQL 写成 `SELECT Shirt FROM T WHERE f("No chemicals?"; Shirt)='yes' AND f("North America?"; Made_in)='yes' ORDER BY Sales DESC LIMIT 1`。表中示例行包括 Polo / U.S. / Sales 500、Luckyland / U.S. / 900 等。无化学品这一列来自衬衫文字详情，不是原表字段。

节末把贡献收成三点，并给出第 1 节里的对比数字。第一，用统一的 Codex 提示 API 替换定制神经模块，用通用编程语言替换任务专用语言，从而覆盖开放域里更多样的输入，且不训练、不需要大规模标注。第二，在需要表格复杂推理的 WIKITQ（Pasupat & Liang, 2015）和 TABFACT（Chen et al., 2019a）上，以 Codex 为 LM 达到当时最优；此前最优都要在超过 10K 条标注上微调，或再用大量任务相关预训练，本文只要大约十来条标注、不训练。进一步分析（细节不在本节）声称增益最大的是原 SQL / Python 语法支撑不了的问题。第三，可接到多模态知识源，数据集为 MULTIMODALQA（Talmor et al., 2021）；相对端到端，调试更可解释，对很大的输入更可扩展，对噪声输入更稳健。本节没有结果表。

## 2 Approach

第 2 节是方法，不是相关工作。论证按“任务定义 → 解析/执行框架 → 上下文学习怎么用 → SQL 与 Python 上的两个 API”推进。第 3 节 Experiments 起的数据和数字不在这里。

**Task Definition。** 输入是自然语言问题或陈述 Q，以及可选上下文 D（段落、表、图像或组合），输出答案 A。例子：篇章问答里 Q 问的是段落；表格事实验证里 Q 是关于表的陈述。

**2.1 BINDER Framework。** 总流程：由 Q 和 D 生成可执行程序 Z，再用 BINDER interpreter 执行 Z 得到 A。

解析：Z 是符号语言表达式，只在原语言做不到的地方插入 API。API 定义为 `f(Q̂; D̂)`。Q̂ 是只用编程语言答不了的那一段，D̂ 是回答它所需的相关上下文。图 1 里 Q̂ 是 “North America?”，D̂ 是列 Made_in。允许 Q̂ = Q 且 D̂ = D，这时程序退化为端到端 LM。API 的输出必须是符号语法能接住的变量。

执行：解释器 = 标准符号解释器 + 实现 API 的模型。经过词法、句法分析后，`f(Q̂; D̂)` 被加进语法作为新标识符，程序解析成抽象语法树。求值时先调用神经模型，把返回存成标准语言变量，再交给现成解释器。语法产生式被扩展以便解析这种 AST；AST 自底向上求值，因此支持嵌套 API，也就是不同程度的分解和 LM 的自由组合。语法扩展和 AST 例子放在附录 A.4，本节不展开公式。

**2.2 In-context Learning for BINDER。** 相对微调，上下文学习只要少量示范、推理时不更新参数，这被说成传统语义解析的两个老问题。实验基座是 Codex：既做语义解析，也实现 API。解析难在插入 API 后语法已经不是原编程语言，作者声称少量 in-context 例子就够 Codex 学会这套改过的语法。执行时把 Q̂ 和 D̂ 拼成提示（提示样式留到 3.1），输出再存回标准语言变量。

具体过程：输入是 k 个示例 `{(Qi, Di, Zi)}` 加当前 `(Q, D)`。k 个例子要在题型多样性和模型输入长度之间取舍，可以人工固定，也可以按当前题检索。模型产出 n 个候选程序，解释器得到 n 个答案，再用多数投票选出 A。投票方式类似 MBR-EXEC（Shi et al., 2022），细节在附录 A.3。k 和 n 是超参数，本节没有给出具体取值。

**2.3 BINDER Implementation。** 本节只用结构化知识上的 SQL 和 Python 作示范。换领域的流水线在附录 D。两个 API：`f_col(Q̂; D̂)` 和 `f_val(Q̂; D̂)`。D̂ 是若干列组成的（子）表，`c = {vi, ...}` 是一列单元格。`f_col` 把 D̂ 映成一列，`f_val` 映成一个值。列和值都能接进 SQL 以及带 Pandas 的 Python，所以这两个 API 可以替换列名或值，使程序仍然合法。

图 1 的问句在这里被用来说明 `f_col`：Made_in 里的国名本身不够判断大洲，纯 SQL 解不了；`f_col("North America?"; Made_in)` 放在标准 SQL 的列名位置。`f_col("No chemicals?"; Shirt)` 则根据 Shirt 列的文字详情判断是不是无化学品（本例里即纯棉）。

`f_val` 用于子问题太复杂、不适合先造中间列的情况。同一张表上的问句 “which shirt is the most suitable for a formal event?” 很难先映出 “formality value” 再 `ORDER BY`，于是写成 `f_val("The most formal?"; Shirt)`，直接输出一个值。它看起来像端到端问答，作者强调两个差别：返回值可以嵌进更组合的 SQL；输入的是子表而不是整表，用来减轻输入长度压力。

第 2 节没有实验结果表，也没有准确率数字。评测设置从第 3 节 Experiments 开始。
