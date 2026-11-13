> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名：** `Binder_ICLR2023.pdf`

**原文标题：** Binding Language Models in Symbolic Languages

**作者：** Zhoujun Cheng、Tianbao Xie、Peng Shi、Chengzu Li、Rahul Nadkarni、Yushi Hu、Caiming Xiong、Dragomir Radev、Mari Ostendorf、Luke Zettlemoyer、Noah A. Smith、Tao Yu。Cheng 与 Xie 为同等贡献，按字母序排列，工作主要在 The University of Hong Kong 完成。首页机构行列出 The University of Hong Kong、Shanghai Jiao Tong University、University of Washington、Allen Institute for AI、University of Waterloo、Salesforce Research、Yale University、Meta AI。

**场合：** ICLR 2023 conference paper。首页同时印有 arXiv:2210.02875v2 [cs.CL]，2023 年 3 月 1 日。

## 摘要

作者认为端到端神经方法在 NLP 上又强又好用，但缺少可解释性和稳健性。BINDER 是一个不用训练的神经-符号框架：把任务输入映射成一段程序。这段程序做三件事：把语言模型的一组统一 API 绑进 SQL、Python 这类编程语言，从而补上原语法盖不住的问题；同一个 LM 既当程序解析器，又在执行时充当 API 背后的模型；标注只需要少量上下文示例。具体用的是 GPT-3 Codex。

解析阶段，少量示例就让 Codex 找出原编程语言答不了的部分，生成相应 API 调用，并把它嵌进与原语法兼容的位置。执行阶段，API 里的提示可以让 Codex 做常识问答、信息抽取等。摘要的结果句是：BINDER 在 WIKITABLEQUESTIONS 和 TABFACT 上达到当时最优，而且输出的是显式程序，方便人来调试。此前最好的系统都要在数万条任务样本上微调，BINDER 只用几十条标注做上下文示例、不做训练。摘要没有指向表号。

## 1 Introduction

第 1 节用对照把问题立住。端到端系统直接从输入映射到输出，灵活、好用，但不可解释、也不够稳（Devlin et al., 2019; Liu et al., 2019; Lewis et al., 2020; Raffel et al., 2020）。符号方法产出逻辑形式、推理路径或程序再执行，中间表示让它对输入变化更稳（Zettlemoyer & Collins, 2005; Gulwani et al., 2017; Chen et al., 2019b），可是覆盖范围被所选符号语言的语法卡住。文中的例子是图 1 里的 “North America?”：纯 SQL 表达不了。真实问题因此会失败，而且中间表示的标注需要专家。已有的神经-符号工作（Andreas et al., 2016; Gupta et al., 2019; Khot et al., 2021; Zhu et al., 2022）要把符号语言和对应神经模块都设计、校准好，通常只覆盖某一任务、某一领域里有限的语义现象，换任务就要新语言和新模块，还要大量训练数据。作者要的是：神经模块调用足够灵活，符号语言覆盖更高，标注却只要很少。

BINDER 的定义在这一节给全：不训练；把输入映射成可执行的 BINDER 程序，即 SQL 或 Python 再绑上统一的 LM API；上下文里只有少量 “输入–BINDER 程序” 示例。解析时 Codex 要决定三件事：输入里哪些部分能写成目标语言（图 1 里灰色部分），哪些要变成 API 调用（如 `f(“North America?”; Made_in)`），以及这些调用插在程序的哪里。执行时再提示 Codex 回答这些 API，把返回值填回程序，最后用确定性解释器跑掉已经没有 API 的程序。图 1 的具体走法是：API 里的问题（如 “North America?”）和数据（如列 `Made_in`）送给 Codex，得到一列 yes/no，表示产地是不是北美；衬衫是否 “no chemicals” 同样处理。作者把这套设计的好处收成：用统一的 Codex 提示 API 换掉定制神经模块，用通用编程语言换掉任务专用语言，从而覆盖更杂的开放域输入，而且建立在上下文学习上，不需要训练和大规模标注。

第 1 节末尾已经预告后文主结果，这里只保留结论、不展开实验：在需要复杂表格推理的 WIKITABLEQUESTIONS（Pasupat & Liang, 2015）和 TABFACT（Chen et al., 2019a）上，以 Codex 为 LM 的 BINDER 达到当时最优；先前最优都要在超过 1 万条标注上微调，或再加大量任务相关预训练，本文只要大约十几条标注且不训练。进一步分析里，增益最大的是原语法（SQL 和 Python）支持不了的问题；BINDER 还能用到 MULTIMODALQA（Talmor et al., 2021）的文本、表格、图像及其组合上；相对端到端，它更便于调试、更能扩到很大的输入、对噪声输入也更稳。这些句子没有指向表号，具体数字在第 3 节之后。

## 2 Approach

第 2 节先给任务，再定义框架、上下文学习用法，以及 SQL/Python 上的两个 API。任务写成：自然语言问题或陈述 Q，加上可选上下文 D（段落、表、图像或它们的组合），输出答案 A。BINDER 的解法是生成可执行程序 Z，再由 BINDER 解释器执行得到 A。

**2.1 Binder Framework。** 解析阶段的 BINDER 程序是一段符号语言表达式，只在原语言做不到的地方插入 API。API 定义为 `f(Q̂; D̂)`：Q̂ 是仅用编程语言答不了的那一部分，D̂ 是 D 里用来回答它的相关上下文。图 1 里 “North America?” 是 Q̂，对应的 D̂ 是列 `Made_in`。若 Q̂ 就是整个 Q、D̂ 就是整个 D，程序退化为端到端 LM。API 的返回值必须是符号语法能接受的变量，程序才能接着执行。执行阶段的解释器由标准符号解释器加上实现 API 的模型组成，经过词法、语法分析和求值。语法上把 `f(Q̂; D̂)` 加成新标识符，按扩展语法解析成抽象语法树；求值时调用神经模型，把结果存成标准语法里的变量，再用现成解释器跑完。语法扩展的细节放在附录 A.4。求值按自底向上进行，因此支持嵌套 API，复杂问题可以有不同程度的分解，也可以自由组合语言模型。

**2.2 In-context Learning for Binder。** 这一小节解释为什么用上下文学习：只要少量示例当提示，推理时不更新参数，正好避开传统语义解析的两个老问题。实验底座是代码预训练的 GPT-3，即 Codex，它同时当语义解析器和 API 功能的实现模型。解析的难点是插入 API 之后语法已经不是原编程语言；作者的观察是，少量上下文示例就够 Codex 学会这套改过的语法。执行时把 API 的 Q̂ 和 D̂ 拼成提示（提示样式留到 3.1），Codex 的输出再存成标准语言里的变量。具体流程是：输入为 k 个示例 `{(Qi, Di, Zi)}` 加上当前的 `(Q, D)`。k 要在问题类型多样性和模型输入上限之间取舍，示例可以人工固定，也可以按当前例子检索。模型产出 n 个候选程序，解释器得到 n 个答案，再用多数投票选出最终答案；投票方式类似 MBR-EXEC（Shi et al., 2022），细节在附录 A.3。k 和 n 是超参数。第 2 节没有给出 k、n 的具体取值。

**2.3 Binder Implementation。** 实现示范是结构化知识上的 SQL 和 Python；换领域的流程放在附录 D，这里不展开。两个 API 是 `f_col(Q̂; D̂)` 和 `f_val(Q̂; D̂)`。D̂ 是若干列组成的子表，列里是单元格。按 Q̂，`f_col` 把子表映射成一列，`f_val` 映射成一个值。返回类型与 SQL、以及带 Pandas 的 Python 兼容，所以可以替换程序里的列名或值。图 1 的问句 “which is the best-selling shirt made in North America and with no chemicals?” 被用来说明：`Made_in` 里的国名本身推不出洲，纯 SQL 解不了，但语言模型容易判断某国是否在北美，于是写成列位置上的 `f_col(“North America?”; Made_in)`；`f_col(“No chemicals?”; Shirt)` 则根据衬衫文本细节判断是不是无化学品（文中例子是纯棉）。若子问题复杂到不适合先造一列中间结果，就改用 `f_val`。例如 “which shirt is the most suitable for a formal event?” 很难先映射出 “formality value” 再 `ORDER BY`，于是写成 `f_val(“The most formal?”; Shirt)`，直接输出一个值。作者强调它和端到端问答仍有两点差别：返回值可以嵌进更大的 SQL 里当一个值用；输入的是子表而不是整张表，从而减轻输入长度压力。第 2 节到此结束，实验从第 3 节 Experiments 起。
