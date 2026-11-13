- 原文件名：Binder_ICLR2023.pdf
- 原标题：BINDING LANGUAGE MODELS IN SYMBOLIC LANGUAGES
- 中文标题：在符号语言中绑定语言模型
- 作者：Zhoujun Cheng、Tianbao Xie、Peng Shi、Chengzu Li、Rahul Nadkarni、Yushi Hu、Caiming Xiong、Dragomir Radev、Mari Ostendorf、Luke Zettlemoyer、Noah A. Smith、Tao Yu
- 会议或 arXiv：ICLR 2023 会议论文；arXiv:2210.02875v2 [cs.CL] 1 Mar 2023

作者单位（原文以上标符号标注；PDF 文本抽取时部分上标符号互相碰撞，机构按原文列出）：The University of Hong Kong、Shanghai Jiao Tong University、University of Washington、Allen Institute for AI、University of Waterloo、Salesforce Research、Yale University、Meta AI。

脚注：同等贡献。作者按字母序排列。工作主要在 The University of Hong Kong 完成。更多资源见 https://lm-code-binder.github.io/ 。代码见 https://github.com/hkunlp/binder 。

<!-- 原 PDF 第 1 页 -->

## 摘要

尽管端到端神经方法近来在性能和易用性上主导了自然语言处理任务，它们缺少可解释性与稳健性。我们提出 Binder，一个免训练的神经符号框架，把任务输入映射为一段程序。该程序：（1）允许把语言模型功能的统一 API 绑定到编程语言（例如 SQL、Python）上，从而扩展其语法覆盖，处理更多样的问题；（2）在执行期间把语言模型同时用作程序解析器，以及 API 所调用的底层模型；（3）只需要少量上下文范例标注。具体而言，我们采用 GPT-3 Codex 作为语言模型。在解析阶段，仅凭少量上下文范例，Codex 就能够识别任务输入中原编程语言无法回答的部分，正确生成 API 调用来提示 Codex 解决这部分，并确定把 API 调用放在何处，同时与原有语法兼容。在执行阶段，只要 API 调用中的提示得当，Codex 就可以完成多种功能（例如常识问答、信息抽取）。Binder 在 WikiTQ 与 TABFACT 数据集上达到当时最佳结果，并给出有利于人工调试的显式输出程序。此前的最佳系统都要在数万条任务专用样本上微调，而 Binder 只把数十条标注当作上下文范例，不做任何训练。代码见 https://github.com/hkunlp/binder 。

## 1 引言

自然语言处理任务上的性能，目前由直接把输入映射到输出的神经端到端系统主导（Devlin et al., 2019; Liu et al., 2019; Lewis et al., 2020; Raffel et al., 2020 等）。这些端到端方法灵活、易用，但缺少可解释性与稳健性。与之相对，符号方法产生显式的中间表示，例如逻辑形式、推理路径或程序代码，再加以执行以得到最终输出（Zettlemoyer & Collins, 2005; Gulwani et al., 2017; Chen et al., 2019b 等）。这些方法产生的中间形式以及随后的执行，使它们对输入变化更为稳健。然而，其语义覆盖受所选符号语言的语法能力限制（例如无法处理图 1 中的 “North America?”），因而在真实世界的多样问题上会失败；中间形式的标注也需要专家知识与研究人员的劳动。

已有若干工作（Andreas et al., 2016; Gupta et al., 2019; Khot et al., 2021; Zhu et al., 2022 等）把神经模块与符号语言结合起来（神经符号方法），以兼取两种路线的长处。然而，它们需要精心设计符号语言，并校准相应的神经模块，才能在特定领域、借助大量训练数据解决问题。更具体地说，这些工作大多提出任务专用的符号语言及相应模块，只覆盖特定任务和领域中有限的语义现象。因此，把它们迁到新任务和新领域时，必须引入新的语言和神经模块。

<!-- 原 PDF 第 2 页 -->

### 图 1

图 1 的文字抽取如下。图中左侧为非结构化知识与结构化知识库。表格列包括 Shirt、Made_in、Sales、Price。抽出的行包括：Polo，U.S.，500，$29.8；Luckyland，U.S.，900，$19.8；Timber Bay，Mexico，400，$25.9；Office，Turkey，600，$31.8。Polo 的详情文字包括 “100% cotton”“220GSM (6.5 oz)”“Natural stretch for comfortable fit”；Timber Bay 的详情包括 “90% cotton, 10% polyester”。图中另有列 no_chemicals，取值为 yes、no、no、no；列 North_America，取值为 yes、yes、yes、no。问题为：Which is the best-selling shirt made in North America and with no chemicals?（哪一件是在北美制造、且不含化学品的最畅销衬衫？）

Binder-SQL 程序抽出为：

```sql
SELECT Shirt FROM T
WHERE f("No chemicals?"; Shirt) = 'yes'
  AND f("North America?"; Made_in) = 'yes'
ORDER BY Sales DESC LIMIT 1
```

Binder-Python 抽出的片段为：

```python
df = df.sort_values('Sales', ascending=False)
df = df[f("North America?"; Made_in) == 'yes']
```

图中还给出不含 API、改用派生列的 SQL：

```sql
SELECT Shirt FROM T
WHERE No_Chemicals = 'yes'
AND North_America = 'yes'
ORDER BY Sales DESC LIMIT 1
```

图中标注利用 GPT-3 Codex 的知识与能力（Utilize GPT-3 Codex’s knowledge/abilities），对 Shirt 列（Polo、Luckyland、Timber Bay、Office）与 Made_in 列（U.S.、U.S.、Mexico、Turkey）分别提问 “Is it no chemicals?”（它是否不含化学品？）与 “Is it North America?”（它是否在北美？）。图内标签还包括：Binder program: SQL/Python binding LM API calls（Binder 程序：SQL／Python 绑定语言模型 API 调用）、Binder parsing（Binder 解析）、prompt（提示）、execute（执行）、predict（预测）、Program Interpreter（程序解释器）、unstructured knowledge（非结构化知识）、structured knowledge base（结构化知识库）。解析与执行两处都标有 GPT-3 Codex。衬衫答案处标出 Polo。图中版式为示意图，行列对应关系以原 PDF 第 2 页为准。

图 1 题注：Binder 流水线两阶段（解析与执行）的概览。（1）解析阶段，给定问题以及可选的知识源，语言模型把输入映射为一段 Binder 程序。程序中以蓝底标出的表达式是用于获取外部结果的 API 调用。（2）执行阶段，语言模型根据提示实现这些 API 调用，返回值再送回原来的编程语言。确定性的程序解释器执行已经不含 API 调用的程序，得到最终答案。

其覆盖范围仍受定制符号语言和神经模块限制。此外，它们还需要多样且大规模的训练数据，才能保证所有模块都训练充分。因此，我们期望一种神经符号系统：它支持灵活的神经模块调用，从而提高符号语言的覆盖，同时只需要少量标注。

我们提出 Binder，一个免训练的神经符号框架。它把任务输入映射为某种编程语言（例如 SQL、Python）中的可执行程序，并绑定统一 API 来调用语言模型（LM；Brown et al., 2020; Chen et al., 2021），以完成多种功能。这样的程序称为 Binder 程序（例如图 1 中的 Binder-SQL、Binder-Python）。标注只需要少量“输入—Binder 程序”配对，用作上下文范例。更具体地说，Binder 首先提示 Codex（GPT-3 的代码预训练版本）把问题输入解析成 Binder 程序。此时 Codex 必须决定：（1）输入中哪些部分可以转换成目标编程语言（图 1 中以灰色标出的问题片段）；（2）相应的任务 API 调用（例如 `f("North America?"; Made_in)`），用来提示 Codex 解决其余部分；（3）这些 API 调用应插入 Binder 程序的何处。接着，Binder 再次提示 Codex，为任务 API 调用生成答案（依据生成出的任务提示），并把生成结果整合回编程语言。具体如图 1：API 调用中的提示（例如 “North America?”）和数据（例如列 Made_in）被送入 Codex，输出是基于输入数据回答该提示的新列（即 Made_in 列中的国家是否来自北美，取 yes 或 no）。最后，改写成标准编程语言的程序被执行，以得到最终答案。

概括而言，Binder 把灵活的功能整合进编程语言，以提高其覆盖，并且只需要少量标注。Binder 程序用对 Codex 的统一提示 API 替换定制神经模块，用通用编程语言替换任务专用语言，从而在开放领域处理远为多样的任务输入，而不必设计复杂的语言和神经模块。Binder 建立在语言模型上下文学习的进展之上，不需要任何训练，也不需要大规模标注。

我们在两个需要在表格上进行复杂推理的结构化知识接地数据集上展示 Binder 框架的有效性：WikiTQ（原文记为 WIKITABLEQUESTIONS，WIKITQ；Pasupat & Liang, 2015）与 TABFACT（Chen et al., 2019a）。以 Codex（Chen et al., 2021）为语言模型，Binder 在 WikiTQ 和 TABFACT 上达到当时最佳结果。此前的最佳方法都需要在超过 1 万条标注训练样本上微调，甚至还需要大量任务相关的预训练数据；我们的方法不做训练，只需要大约十几条标注。进一步分析中，我们发现 Binder 在原语言语法（SQL 与 Python）无法支持的问题上增益最大，说明 Binder 确实提高了编程语言的覆盖。我们还展示 Binder 可以用于多模态知识源（文本、表格、图像及其组合），数据集为 MultiModalQA（原文记为 MULTIMODALQA；Talmor et al., 2021）。此外，相对端到端方法，Binder 在调试模型时更可解释，对很大的输入更能扩展，对带噪声的输入也更稳健。

<!-- 原 PDF 第 3 页 -->

## 2 方法

### 任务定义

给定一个自然语言处理任务，输入为自然语言问题或陈述 $Q$，以及可选上下文 $D$（例如段落、表格、图像，或以上几者的组合），目标是基于输入输出答案 $A$，从而正确回应 $Q$。例如，在段落问答中，$Q$ 是关于段落 $D$ 的问题；在表格事实验证中，$Q$ 是关于表格 $D$ 的陈述。

### 2.1 Binder 框架

**概述。** 用 Binder 框架求解自然语言处理任务的定义如下：给定自然语言输入 $Q$ 和可选上下文 $D$，生成一段可执行的 Binder 程序 $Z$。最后，用 Binder 解释器执行 $Z$，得到输出答案 $A$。

**Binder 解析。** 在解析阶段，输入的自然语言 $Q$ 被解析为 Binder 程序 $Z$。Binder 程序是符号语言中的表达式，只在核心符号语言提供不了所需功能的地方可选地加入 API 调用。我们把程序中的 API 调用定义为函数 $f(\hat{Q}; \hat{D})$，它接受待回答的问题 $\hat{Q}$，以及要在其上查询的上下文 $\hat{D}$。这里 $\hat{Q}$ 是仅靠编程语言无法回答的那一部分 $Q$，$\hat{D}$ 是 $D$ 中与回答 $\hat{Q}$ 相关的上下文。例如，图 1 中的 “North America?” 就是一个 $\hat{Q}$，用来回答它的对应上下文 $\hat{D}$ 是列 Made_in。$\hat{Q} = Q$ 或 $\hat{D} = D$ 也同样合法（若 $\hat{Q} = Q$ 且 $\hat{D} = D$，该程序就等价于用语言模型以端到端方式求解）。API 调用 $f(\hat{Q}; \hat{D})$ 的输出是 $\hat{Q}$ 的答案，并表示为一个与符号语言语法兼容的变量，以便程序能够执行。

**Binder 执行。** 在执行阶段，程序 $Z$ 由 Binder 解释器执行，得到答案 $A$。Binder 解释器由标准符号语言解释器，以及实现 API 调用的模型组成。执行阶段包括词法分析、语法分析和程序求值。在词法和语法分析中，$f(\hat{Q}; \hat{D})$ 被加入语法，作为一个新的标识符，程序再依据这个扩展语法解析为抽象语法树（AST）。在程序求值中，API 调用通过调用底层神经模型来求值。API 调用的输出被存成与标准符号语言语法兼容的变量，于是程序最终可以由现成的符号语言解释器执行，得到输出。具体而言，Binder 扩展了符号语言的产生式规则，以便解析 Binder 程序的抽象语法树。抽象语法树按自底向上的顺序求值，因此也支持嵌套的 API 调用。嵌套允许不同程度的问题分解，以及为复杂问题自由组合语言模型。语法扩展和 Binder 程序抽象语法树的更多细节见附录 A.4。

### 2.2 用于 Binder 的上下文学习

近期很多工作使用大语言模型做上下文学习（Brown et al., 2020; Chen et al., 2021; Chowdhery et al., 2022b）。与微调相比，上下文学习（1）只把少量标注或演示当作提示，（2）推理时不训练模型参数。这两点都是传统语义解析的长期困难。我们把 Binder 的实验建立在 Codex 上。Codex 是 GPT-3 的代码预训练版本，已表明它在代码生成任务上表现熟练（Rajkumar et al., 2022; Chen et al., 2022），甚至在对话状态跟踪这类关系较弱的任务上也能工作（Hu et al., 2022）。我们把 Codex 同时用作语义解析器，以及执行 API 调用功能的模型。

在解析阶段，生成 Binder 程序是困难的，因为插入 API 调用之后，其语法不同于原来的编程语言语法。因此，我们利用 Codex 的少样本泛化能力，并发现只需少量上下文例子，它就能有效学会这套修改过的语法。在执行阶段，作为底层语言模型的 Codex 负责给出 API 调用的输出：把 API 调用的输入 $\hat{Q}$ 与 $\hat{D}$ 拼接成语言模型提示（提示样式见第 3.1 节）。Codex 的输出结果被存为标准编程语言中的变量，以便编程语言解释器执行。

<!-- 原 PDF 第 4 页 -->

这些变量与程序其余部分的组合，由语言解释器执行。

具体而言，我们按下列方式对 Binder 做上下文学习：输入是 $k$ 个上下文范例 $\{(Q_i, D_i, Z_i)\}_{i=1}^{k}$，以及待推断样本 $(Q, D)$。这 $k$ 个例子应在问题类型的多样性与模型最大输入容量之间取得平衡；既可以按推断样本人工选定（固定），也可以自动检索（动态）。模型输出 $n$ 个候选 Binder 程序 $Z = \{Z_1, \ldots, Z_n\}$，旨在求解推断问题 $Q$。接着，这些程序 $Z$ 由 Binder 解释器执行，产生 $n$ 个答案 $A = \{A_1, \ldots, A_n\}$。最后，对产生的答案集合 $A$ 做多数投票，得到输出答案 $A$（投票方法与 MBR-EXEC（Shi et al., 2022）所用的方法类似，详见附录 A.3）。$k$ 与 $n$ 是上述流程中的超参数。

### 2.3 Binder 的一种实现

本节以结构化知识上的 SQL 与 Python 为例，描述 Binder 的实现。Binder 的设计可以扩展到多种编程语言和 API 功能，我们在附录 D 中给出一条流水线，便于用户把 Binder 快速迁到新领域。

我们实现两个 API：$f_{\mathrm{col}}(\hat{Q}; \hat{D})$ 与 $f_{\mathrm{val}}(\hat{Q}; \hat{D})$。其中 $\hat{D} = \{c_1, \ldots, c_{|\hat{D}|}\}$ 是由一组表格列构成的（子）表，$c = \{v_i, \ldots, v_{|c|}\}$ 是填有单元格值的一列。基于 $\hat{Q}$，$f_{\mathrm{col}}$ 把 $\hat{D}$ 映射成一列，$f_{\mathrm{val}}$ 把 $\hat{D}$ 映射成一个值。两种返回类型，即列和值，都与 SQL 以及 Python（配合 Pandas 包）的语法兼容，因此可以把 $f_{\mathrm{col}}$ 与 $f_{\mathrm{val}}$ 插入进去，替换列和值，形成一段合法的 Binder 程序。

以图 1 中的问题为例：“which is the best-selling shirt made in North America and with no chemicals?”（哪一件是在北美制造、且不含化学品的最畅销衬衫？）Made_in 列中的国名本身不足以表明它们所属的大洲，因此纯 SQL 无法（用这张表的数据）求解。然而，对（大）语言模型来说，判断一个国家是否来自北美很容易，这在标准 SQL 中本应写列名的位置，表示为表达式 $f_{\mathrm{col}}(\text{“North America?”}; \mathrm{Made\_in})$。类似地，表达式 $f_{\mathrm{col}}(\text{“No chemicals?”}; \mathrm{Shirt})$ 调用（大）语言模型，根据 Shirt 列中的文本细节，判断这些衬衫是否不含化学品（此例中即纯棉）。

当一个（子）问题过于复杂，或不适合通过 $f_{\mathrm{col}}$ 先造出中间新列来求解时，我们改用 $f_{\mathrm{val}}$ 直接得到答案。例如，对图 1 的表格提问 “which shirt is the most suitable for a formal event?”（哪一件衬衫最适合正式场合？），很难把 Shirt 映射成一列新的“正式程度”，再接一条 SQL 的 `ORDER BY` 子句。因此表达式将是 $f_{\mathrm{val}}(\text{“The most formal?”}; \mathrm{Shirt})$，它输出一个值作为答案。$f_{\mathrm{val}}$ 看起来更像端到端问答，但有两个重要差别：（1）它的结果可以作为一个值，整合进组合性更强的 SQL 查询；（2）它输入的是子表而不是整张表，从而减轻输入容量方面的困难。

## 3 实验

### 3.1 实验设置

**数据集。** 我们在三个知识接地数据集上评估方法。这些数据集此前都由端到端方法主导：WikiTQ（Pasupat & Liang, 2015）与 TABFACT（Chen et al., 2019a）。WikiTQ 需要复杂的表格推理技能来回答问题。此外，根据 SQUALL（Shi et al., 2020b），约 20% 的 WikiTQ 问题无法用纯 SQL 回答，原因要么是需要额外知识，要么是 SQL 语法覆盖有限；这两点都是 Binder 所要解决的问题。TABFACT 是小表格上的二值事实验证基准。端到端方法在该基准上优势很大，但不提供可解释性。

<!-- 原 PDF 第 5 页 -->

表 1 与表 2 在原 PDF 中并排。`find_tables` 未抽出这两张表，下列数字来自按页文本，按方法名之后依次出现的数值排列，未另补数字。

**表 1：WikiTQ 在开发集与测试集上的执行准确率。** † 表示输出中间语言的符号方法。

| 方法 | 开发集 | 测试集 |
| --- | --- | --- |
| **微调** | | |
| T5-3B（Xie et al., 2022） | 51.9 | 50.6 |
| Tapex（Liu et al., 2021） | 60.4 | 59.1 |
| TaCube（Zhou et al., 2022） | 61.1 | 61.3 |
| OmniTab（Jiang et al., 2022） | - | 63.3 |
| **不做微调** | | |
| Codex 端到端问答 | 50.5 | 48.7 |
| Codex SQL† | 60.2 | 61.1 |
| Codex Binder†（本文） | 65.0 | 64.6 |

**表 2：TABFACT 在官方小测试集上的准确率。** † 表示输出中间语言的符号方法。

| 方法 | 测试集 |
| --- | --- |
| **微调** | |
| SASP†（Ou & Liu, 2022） | 77.0 |
| BART-Large（Lewis et al., 2020） | 82.5 |
| T5-3B（Xie et al., 2022） | 85.4 |
| Tapex（Liu et al., 2021） | 85.9 |
| **不做微调** | |
| Codex 端到端问答 | 72.6 |
| Codex SQL† | 80.7 |
| Codex Binder†（本文） | 85.1 |
| 使用少样本检索器 | 86.0 |

**评估。** 评估指标是执行准确率（EA），用于 WikiTQ 与 TABFACT，沿用这些数据集的通行做法。程序执行结果在语义上往往正确，却无法与标准答案精确匹配——例如，对是否问题，SQL 输出 1 或 0。按人工评估这应算正确，但精确匹配评估器会判为错误。因此，我们在 WikiTQ 的官方评估器上，为这些语义正确的情形增加了预匹配检查。为公平比较，我们计算所有基线方法的输出，并用同一评估器重新评估。评估器的更多细节见附录 A.5；全部基线与本文方法在官方评估器下的结果列于 C.2。

**基线。** 我们把本文方法与这些数据集上一系列已发表的强基线比较，包括 Tapex（Liu et al., 2021）、OmniTab（Jiang et al., 2022）、TaCube（Zhou et al., 2022）、T5-3B（Xie et al., 2022; Raffel et al., 2020）以及 SASP（Ou & Liu, 2022）。这些基线都在全量训练集上微调，其中许多（Liu et al., 2021; Zhou et al., 2022）还在与目标领域和任务专门相关的额外语料上进一步预训练；Binder 则免训练，只需要少量上下文范例标注。

为进一步展示 Binder 的有效性，我们还用另外两种推断模式评估 Codex：（1）端到端问答，即根据输入问题和表格直接输出答案；（2）用标准 SQL 语言做语义解析。限于篇幅，有兴趣了解这些基线的读者请参阅各自论文（Liu et al., 2021; Jiang et al., 2022; Zhou et al., 2022; Xie et al., 2022; Raffel et al., 2020; Ou & Liu, 2022）。我们在附录 C.1 中给出这些数据集上更多先前系统的完整列表与评估结果。

**实现细节。** 实验中使用 OpenAI Codex（code-davinci-002）API（https://beta.openai.com/），既作为生成程序的解析器，也作为每个程序执行期间 API 调用的底层模型。我们为每个数据集标注 14 个带 Binder 程序的上下文范例。挑选时考虑演示中问题类型的多样性，以及 Codex 的最大词元限制（8,000 个词元）。提示格式主要遵循 Rajkumar et al.（2022），输入表格模式以及表格的前三行。各数据集所用的详细提示模板见附录 A.1。在 TABFACT 上，我们进一步用 vote-k 选择性标注（Su et al., 2022），从训练集中标注一个含 200 个例子、带 Binder 程序的池，并在推断时为每个样本检索相关的少样本例子：对问题的 SentenceBert（Clark et al., 2019）嵌入做最大内积相似度检索。解析与执行所用的 Codex 超参数见附录 A.2。经验上，在 Codex 允许每分钟 200 次查询的条件下，评估 1,000 个例子（即每个例子生成并执行 20 个程序）平均大约需要 6 小时。考虑到时间成本，我们在 TABFACT 的官方小测试集（2,000 个样本）上评估。

### 3.2 主要结果

**WikiTQ。** WikiTQ 数据集上的全部结果见表 1。我们的 Codex Binder 以较大幅度超过所列的强基线系统，绝对超过此前最佳结果

<!-- 原 PDF 第 6 页 -->

1.3 个百分点。注意，所有基线方法都需要使用完整训练数据集并进一步微调，而我们的方法只用 14 个范例标注就能达到当时最佳性能。在测试集上，Codex Binder 比使用标准 SQL 的语义解析高 3.5 个百分点，说明 Binder 确实缓解了原语言的覆盖限制。此外，Codex Binder 与 Codex SQL 相对端到端问答都有大幅优势（分别为 15.9 与 12.4 个百分点），说明在结构化知识接地和代码相关任务上，用 Codex 做语义解析是更好的默认选择。Binder 为何优于端到端问答和纯 SQL，细粒度分析见第 4.1 节。

**TABFACT。** 表 2 给出 TABFACT 官方小测试集上的结果。Codex Binder 比此前最好的符号方法 SASP 高出 8.1 个百分点。注意，在事实验证（二分类）中，符号方法通常落后于端到端方式，因为答案空间很小。当从已标注的 200 个例子池中检索少量相关问题时，我们的方法达到新的最佳结果，超过此前最好的微调方法。不过，检索少量相似例子带来的提升相对较小（0.9 个百分点）。面向上下文学习的有效样本选择方法仍是一个开放问题。在 Codex 少样本设定内（不使用少样本检索器），Binder 相对标准 SQL（4.4 个百分点）和端到端问答（12.5 个百分点）都有很大优势，说明 Binder 框架是必要的。除性能增益外，Binder 还有两项额外优点：（1）可解释性，有利于人工调试；（2）稳健性，使它对很大或带噪声的输入保持稳定。我们在第 4.2 节与第 4.3 节中展开说明。

## 4 分析

### 4.1 消融研究

把神经模块 API 调用绑定进编程语言，有助于求解该语言单独无法求解的查询。因此，我们特别关心 Binder 在不可解问题上的表现。根据 SQUALL（Shi et al., 2020b），约 20% 的 WikiTQ 问题无法用 SQL 标注；我们称之为程序不可解，把已标注的称为程序可解。如表 3 所示，在程序不可解问题上，Codex Binder 显著超过 Codex SQL，幅度为 10.1 个百分点，与我们的设计动机一致。我们的方法甚至在程序不可解子集上优于所有端到端问答方法，而这些端到端方法本应对该子集更稳健。我们注意到，SQL 在大约 31.2% 的不可解问题上表现良好，但其中许多是偶然推出正确答案的伪程序。Binder 在很大程度上减轻了这一现象。我们从 SQL 与 Binder 都预测正确的程序不可解集合中随机抽取 100 个正确预测，发现 Binder 的伪正确率远低于 SQL（12% 对 33%）。还需注意的一点是，Binder 在程序可解子集上的分数也高于 SQL。我们发现，这是因为 SQUALL 为了运行所标注的 SQL，对一些表格做了人工清洗（例如从文本中抽出数值部分），这意味着即使在程序可解子集里，也仍然存在不可解的问题。我们在附录 C.4 中给出关于 WikiTQ 有多大比例可以用 SQL 求解的人工统计。我们也展示 Codex 仅凭内部知识能在多大程度上回答问题。Codex 只能正确回答少量 WikiTQ 问题（12.4%），说明它并没有被预训练到在下游数据集问题上过拟合。

**表 3：WikiTQ 开发集上执行准确率的分解。** 由 SQUALL（Shi et al., 2020b）标注了 SQL 的问题记为程序可解，其余记为程序不可解。OmniTab（Jiang et al., 2022）未提供其开发集结果。`find_tables` 未抽出该表，数字来自按页文本。

| 方法 | 程序不可解 | 程序可解 | 总体 |
| --- | --- | --- | --- |
| T5-3B（Xie et al., 2022） | 37.6 | 56.0 | 51.9 |
| Tapex（Liu et al., 2021） | 33.6 | 68.0 | 60.4 |
| TaCube（Zhou et al., 2022） | 34.9 | 68.5 | 61.1 |
| Codex 端到端问答 | 40.3 | 53.4 | 50.5 |
| 其中：不含表格输入 | 14.2 | 11.9 | 12.4 |
| Codex SQL | 31.2 | 68.4 | 60.2 |
| Codex Binder（本文） | 41.3 | 71.8 | 65.0 |

<!-- 原 PDF 第 7 页 -->

**表 4：Binder（SQL）在 WikiTQ 开发集上 100 个样本的错误类型。** `find_tables` 未抽出该表，数字来自按页文本。Token、Structure、Binder usage 三行的比例之和为 64，与“语义错误”一行相同，故按子类排列；原文层级以原 PDF 第 7 页为准。

| 错误类型 | 描述 | 比例（%） |
| --- | --- | --- |
| 语法错误 | 程序语法不正确（非法语法） | 5% |
| 语义错误 | 程序语义不正确 | 64% |
| 　词元 | 列、值或运算符不正确或缺失 | 10% |
| 　结构 | 程序结构不正确（语法合法） | 22% |
| 　Binder 用法 | 缺少 Binder API 的使用 | 32% |
| 执行不正确 | 程序正确，但执行答案不正确 | 15% |
| 假阴性 | 标注不正确，或评估器误判 | 16% |

**表 5：WikiTQ 开发集中的一个例子。** 查询为 “When was the first game that kansas state won by double digits?”（堪萨斯州立大学第一次以两位数优势获胜是在何时？），标准答案为 1926。各输出中不正确的片段在原文中以红色标出。该例的完整上下文见附录 E。`find_tables` 未抽出该表，程序文本来自按页抽取。

| 系统 | 程序 | 答案 |
| --- | --- | --- |
| 端到端问答 | — | 1967 |
| SQL | `SELECT year FROM t WHERE win_team='kansas state' AND win_team - los_team > 10` | `<empty>` |
| Binder | `SELECT year FROM t WHERE win_team='kansas state' AND f("Points?";win_team) - f("Points?";los_team) > 10` | `<empty>` |

### 4.2 可解释性

Binder 相对端到端方法的一个重要优点是可解释性更好：显式程序可以帮助人工调试和错误分析。我们从 WikiTQ 开发集中抽取 Codex Binder（基于 SQL）的 100 个错误案例（约占全部错误例子的 10%）做错误分析。我们把错误分为语法错误、语义错误、执行不正确和假阴性，如表 4 所列。分类的更多细节和示例见附录 E。对 WikiTQ 而言，错误主要落在语义错误中的 Binder 用法（32%）和结构错误（22%），以及执行不正确（15%）。这表明，若正确使用 Binder，32% 的错误例子还有望被纠正；15% 可以通过更好的执行来纠正，例如使用更强的语言模型、更好的上下文学习方法，以及标注更多范例。

我们也用一个例子说明使用 Binder 进行调试和解释结果的好处。如表 5 的例子所示，端到端系统的结果是 1967，这一结果不正确，但没有提供该预测背后原因的线索。Binder 的结果也不正确，因为程序对表格中的 win_team 列使用了不正确的值和运算符（应当是 `LIKE "%kansas state%"`），将来有可能通过加入相似的上下文范例或模糊匹配后处理来修正。对标准 SQL 而言，尽管我们发现直接做 `win_team − los_team` 的减法是不正确的（其中含有非数值文本），但由于语法覆盖有限，它无法被修正。因此，在这个例子里，Binder 既能找到错误来源（这是相对端到端方法的优点），其表达能力也足以让用户找到修正办法（这是相对纯符号系统的优点），从而使 Binder 适合调试，并让使用它的系统具备可解释性。我们把更系统的评估方法留给未来工作：这类方法应考虑调试的难易，例如估计人类纠正系统错误所需的工作量。

### 4.3 稳健性

#### 4.3.1 可扩展性

Binder 相对端到端问答的一大优点是可扩展性。也就是说，即使知识源大到无法放入模型的输入容量或内存（例如公司数据库、领域知识图谱），解析并执行符号语言仍然可行；端到端问答则因为必须把整张表作为输入来预测答案而失败或退化。我们从 WikiTQ 开发子集（随机 150 个样本）出发，把表格扩展到 100、200 和 500 行：提示 Codex 用与内容一致的行填充原表，再由两名标注者人工标注问答对。当表格超过 Codex 的最大词元限制（8,000 个词元）时，我们截断表格行，直到能够放下。如图 2 所示，随着表格变大，Codex

<!-- 原 PDF 第 8 页 -->

**图 2：** WikiTQ 上、表格很大时的执行准确率（原始表格，以及 100、200、500 行）。图中曲线的具体坐标点未抽出，不编造数值，见原 PDF 第 8 页。

**图 3：** WikiTQ 上、表格含噪声内容时的执行准确率。图中曲线的具体坐标点未抽出，不编造数值，见原 PDF 第 8 页。

**表 6：以 Python 为编程语言时，WikiTQ 在程序不可解子集上的准确率。** `find_tables` 未抽出该表，数字来自按页文本。

| 方法 | 程序不可解 |
| --- | --- |
| Codex Python | 30.7 |
| Codex Binder（本文） | 34.4 |

**表 7：MMQA 开发集上的 F1 / EM。** `find_tables` 未抽出该表，数字来自按页文本。

| 方法 | F1 | EM |
| --- | --- | --- |
| **微调** | | |
| Implicit-Decomp（Talmor et al., 2021） | 55.5 | 48.8 |
| PReasM-Large（Yoran et al., 2022） | 65.5 | 59.0 |
| **不做微调** | | |
| Codex 端到端问答 | 55.4 | 48.0 |
| Codex Binder（本文） | 57.1 | 51.0 |
| 使用 oracle 检索器 | 64.5 | 58.1 |

端到端问答的性能随表格变大而急剧下降，而 Binder 始终优于它，且只有轻微的性能下降。注意，对所有表格规模，Binder 的输入都只是三行表格。

#### 4.3.2 噪声内容

端到端方法对噪声输入更脆弱，尤其是当存在与问题相关（标准）内容相似的干扰项时。我们用三个步骤构造一个带噪声的 WikiTQ 开发子集（随机 150 个样本），并在其中放入干扰项：（1）用启发式模糊匹配找到标准表格单元格和列；（2）把标准列中 15% 的单元格替换掉，替换文本取 WordNet 语料中与标准单元格字符串编辑距离最小的文本，或取等于标准单元格数值 ±1 的数字；（3）由一名标注者检查，内容扰动之后问答对仍然有效。如图 3 所示，面对干扰项时 Binder 保持稳定（下降 1.3%），而端到端问答更容易被相似的文本和数字迷惑（下降 6.7%）。

### 4.4 Binder 的扩展

**使用 Python 的 Binder。** 我们把 Binder 设计成易于扩展到多种编程语言。因此，我们探索在 WikiTQ 上用 Python（配合 Pandas 包）作为 Binder 语言。与 SQL 类似，Python 上的 Binder 通过把神经 API $f(\cdot;\cdot)$ 纳入其中来实现。由于该神经 API 也是用 Python 调用语言模型，我们直接使用原来的 Python 解释器来执行带 Python 的 Binder。我们在 WikiTQ 的程序不可解子集上评估它，以检验本文方法是否提高了 Python 的能力。尽管该子集是按 SQL 划分的，Python 与 SQL 有一些相似的弱点，例如需要外部知识，以及存在不被支持的功能。如表 6 所示，带 Python 的 Binder 有效提高了 Python 在这个困难子集上的覆盖。Python 与 SQL 在 WikiTQ 上的性能差距，可能来自两种编程语言各自的性质，如 Guo et al.（2020）所指出的。我们推测，Codex 更熟悉把表格数据语义解析成 SQL，而 Python 在这一场景中不那么常用。

**多模态应用。** 我们进一步探索把 Binder 用于跨文本、表格和图像的多模态数据集 MultiModalQA（MMQA）。为了把图像输入到语言模型的程序生成中，图像事先由视觉–文本预训练模型 OFA（Wang et al., 2022）转换成文本形式的图像说明。对与表格相关的问题，Binder 程序基于

<!-- 原 PDF 第 9 页 -->

SQL。对非表格问题，则生成带有 $f_{\mathrm{val}}$ 的程序，目标为相应段落或图像标题。我们遵循 Yoran et al.（2022），在预处理中检索与问题相关的段落和图像。就我们所知，我们首次表明：跨文本、表格和图像的多模态问答可以用可解释、可执行的程序来处理。如表 7 所列，在 Codex 少样本设定下，Binder 的性能优于端到端问答，也优于微调基线 Implicit-Decomp，说明 Binder 用于多模态知识源是可行的。若使用 oracle 检索器，即假定每个问题都给定了标准段落和图像，Binder 可以达到与当时最佳结果相当的性能，显示出 Binder 路线在未来的潜力。

## 5 相关工作

**语义解析。** 语义解析（Zelle & Mooney, 1996; Zettlemoyer & Collins, 2005）一直是符号方法的主干：给定自然语言输入，产生可执行程序，生成有助于求解的中间结构，并比后来出现的、直接生成解答的神经方法更可解释。结构化知识接地任务主要采用语义解析，因为 SQL、SPARQL 等符号语言可以在其上执行（Berant et al., 2013; Liang et al., 2017; Yin & Neubig, 2017; Zhong et al., 2018; Yu et al., 2018; Shaw et al., 2021; Scholak et al., 2021）。在结构化知识之外，Chen et al.（2019b）与 Thorne et al.（2021）设计了可在文本上执行的领域专用语言。近来，Chen et al.（2021）提出一种用于代码生成的生成式预训练语言模型，不需要额外的人工标注。许多工作基于该模型提出方法并取得很大成功（Rajkumar et al., 2022; Shi et al., 2022）。然而，语义解析方法受其语法覆盖限制，无法求解需要外部知识或外部函数的问题。

**神经符号方法。** 一些工作把神经模块与符号语言整合起来，以兼取两种路线的优点，即良好的性能与可解释性。Andreas et al.（2016）、Hu et al.（2017）、Das et al.（2018）以及 Gupta et al.（2019）生成程序，再由相应的神经模块做软执行。Khot et al.（2021）提出文本模块网络，把复杂任务分解成更简单的任务，交由已有的问答模型和一个符号计算器求解。BREAK（Wolfson et al., 2020）提出一种有意义的表示 QDMR，把问题分解为多个步骤。然而，它们需要精心设计任务中要使用的函数，并校准相应的神经模块；这些模块需要复杂的训练步骤和大规模训练数据（通常为数万条），才能处理特定领域中的问题。

与这些方法相比，Binder 表达力强、也更灵活，能够处理真实世界中多样的问题，因为它可以做适当的 API 调用来增强功能。此外，Binder 免训练，只需要基于某种符号语言的数十条标注，就能在领域专用任务上工作，同时保持：优秀的性能、在输入上扩展的能力、可解释性，以及对噪声内容的稳健性。

## 6 结论

我们提出 Binder，一个免训练的神经符号框架。它把任务输入映射为一段程序，并允许绑定统一的语言模型 API，以获得额外功能。Binder 旨在结合端到端方法（高覆盖）与符号方法（高可解释性）的长处。以 Codex 为语言模型，Binder 在 WikiTQ 和 TABFACT 上达到当时最佳性能，只用数十条上下文演示，且不做额外训练。对照之下，现有的最佳系统要在数千条任务专用训练样本上微调，还可能需要进一步的领域专用预训练。我们还对 Binder 做了一系列分析：分解性能增益，检验对很大或带噪声输入的稳健性，把它用于多模态知识源，并扩展到 Python 语言。我们把 Binder 视为一种新的、以语言模型为中心的尝试，用来整合自然语言处理中两种被广泛采用的范式：端到端方法与符号方法。有了近来强大的大语言模型，免训练地正确生成并执行 Binder 程序已经成为可行的事。未来，我们相信只要编程语言和功能选择得当，Binder 可以扩展到更多场景；我们也希望它能启发更多想法，在模型能力与可解释性之间取得平衡。

<!-- 原 PDF 第 10 页 -->

## 7 可复现性

Binder 实验主要基于 OpenAI Codex（code-davinci-002）API（https://beta.openai.com/）。我们提供：（1）附录 A.1 中使用的输入提示模板；（2）附录 A.2 中各数据集所采用的 Codex 超参数；（3）附录 A 中的更多实现细节。此外，我们也在材料中上传了源代码，使结果易于复现。

<!-- 原 PDF 第 11 页 -->

## 参考文献

参考文献的题目译为中文，作者姓名、会议名、页码与链接保留英文。

Rishabh Agarwal, Chen Liang, Dale Schuurmans, and Mohammad Norouzi. 从稀疏且欠指定的奖励中学习泛化. In International conference on machine learning, pp. 130–140. PMLR, 2019.

Jacob Andreas, Marcus Rohrbach, Trevor Darrell, and Dan Klein. 神经模块网络. In Proceedings of the IEEE conference on computer vision and pattern recognition, pp. 39–48, 2016.

Jonathan Berant, Andrew Chou, Roy Frostig, and Percy Liang. 基于问答对在 Freebase 上做语义解析. In Proc. of EMNLP, 2013. URL https://aclanthology.org/D13-1160.

Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel Ziegler, Jeffrey Wu, Clemens Winter, Chris Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. 语言模型是少样本学习者. In Proc. of NeurIPS, 2020. URL https://proceedings.neurips.cc/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf.

Bei Chen, Fengji Zhang, Anh Nguyen, Daoguang Zan, Zeqi Lin, Jian-Guang Lou, and Weizhu Chen. Codet：借助生成测试的代码生成. arXiv preprint arXiv:2207.10397, 2022.

Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al. 评估在代码上训练的大语言模型. arXiv preprint arXiv:2107.03374, 2021.

Wenhu Chen, Hongmin Wang, Jianshu Chen, Yunkai Zhang, Hong Wang, Shiyang Li, Xiyou Zhou, and William Yang Wang. Tabfact：面向基于表格的事实验证的大规模数据集. arXiv preprint arXiv:1909.02164, 2019a.

Xinyun Chen, Chen Liang, Adams Wei Yu, Denny Zhou, Dawn Song, and Quoc V Le. 神经符号阅读器：为阅读理解可扩展地整合分布式表示与符号表示. In International Conference on Learning Representations, 2019b.

Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra, Adam Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Sebastian Gehrmann, et al. Palm：用 Pathways 扩展语言建模. arXiv preprint arXiv:2204.02311, 2022a.

Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra, Adam Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Sebastian Gehrmann, et al. Palm：用 Pathways 扩展语言建模. arXiv preprint arXiv:2204.02311, 2022b.

Hyung Won Chung, Le Hou, Shayne Longpre, Barret Zoph, Yi Tay, William Fedus, Eric Li, Xuezhi Wang, Mostafa Dehghani, Siddhartha Brahma, et al. 扩展经过指令微调的语言模型. arXiv preprint arXiv:2210.11416, 2022.

Elizabeth Clark, Asli Celikyilmaz, and Noah A. Smith. 句子搬运相似度：面向多句文本的自动评估. In Proc. of ACL, July 2019. URL https://aclanthology.org/P19-1264/.

Abhishek Das, Georgia Gkioxari, Stefan Lee, Devi Parikh, and Dhruv Batra. 面向具身问答的神经模块化控制. In Conference on Robot Learning, pp. 53–62. PMLR, 2018.

Pradeep Dasigi, Matt Gardner, Shikhar Murty, Luke Zettlemoyer, and Eduard Hovy. 弱监督语义解析的迭代搜索. In Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers), pp. 2669–2680, 2019.

Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. BERT：面向语言理解的深度双向 Transformer 预训练. In Proc. of NAACL, 2019. URL https://arxiv.org/abs/810.04805.

<!-- 原 PDF 第 12 页 -->

Julian Eisenschlos, Syrine Krichene, and Thomas Mueller. 借助中间预训练理解表格. In Findings of the Association for Computational Linguistics: EMNLP 2020, pp. 281–296, 2020.

Sumit Gulwani, Oleksandr Polozov, Rishabh Singh, et al. 程序合成. Foundations and Trends® in Programming Languages, 4(1-2):1–119, 2017.

Jiaqi Guo, Qian Liu, Jian-Guang Lou, Zhenwen Li, Xueqing Liu, Tao Xie, and Ting Liu. 为神经语义解析中的意义表示建立基准. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP), pp. 1520–1540, 2020.

Jiaqi Guo, Jian-Guang Lou, Ting Liu, and Dongmei Zhang. 通过从错误中学习做弱监督语义解析. In Findings of the Association for Computational Linguistics: EMNLP 2021, pp. 2603–2617, Punta Cana, Dominican Republic, November 2021. Association for Computational Linguistics. doi: 10.18653/v1/2021.findings-emnlp.222. URL https://aclanthology.org/2021.findings-emnlp.222.

Nitish Gupta, Kevin Lin, Dan Roth, Sameer Singh, and Matt Gardner. 面向文本推理的神经模块网络. arXiv preprint arXiv:1912.04971, 2019.

Jonathan Herzig, P. Nowak, Thomas Müller, Francesco Piccinno, and Julian Martin Eisenschlos. Tapas：借助预训练做弱监督表格解析. In Proceedings of ACL, 2020.

Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor Cai, Eliza Rutherford, Diego de Las Casas, Lisa Anne Hendricks, Johannes Welbl, Aidan Clark, et al. 训练计算最优的大语言模型. arXiv preprint arXiv:2203.15556, 2022.

Ronghang Hu, Jacob Andreas, Marcus Rohrbach, Trevor Darrell, and Kate Saenko. 学习推理：面向视觉问答的端到端模块网络. In Proceedings of the IEEE international conference on computer vision, pp. 804–813, 2017.

Yushi Hu, Chia-Hsuan Lee, Tianbao Xie, Tao Yu, Noah A Smith, and Mari Ostendorf. 面向少样本对话状态跟踪的上下文学习. arXiv preprint arXiv:2203.08568, 2022.

Zhengbao Jiang, Yi Mao, Pengcheng He, Graham Neubig, and Weizhu Chen. Omnitab：用自然数据与合成数据预训练，服务少样本的基于表格的问答. In Proceedings of the 2022 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, pp. 932–942, 2022.

Tushar Khot, Daniel Khashabi, Kyle Richardson, Peter Clark, and Ashish Sabharwal. 文本模块网络：用已有模型的语言学习分解任务. In Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, pp. 1264–1279, 2021.

（上条文献在原 PDF 中从第 12 页跨到第 13 页，此处按完整条目写出。）

<!-- 原 PDF 第 13 页 -->

第 13 页开头是 Khot et al.（2021）条目的后半，会议信息已并入上条。

Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa. 大语言模型是零样本推理者. arXiv preprint arXiv:2205.11916, 2022.

Mike Lewis, Yinhan Liu, Naman Goyal, Marjan Ghazvininejad, Abdelrahman Mohamed, Omer Levy, Veselin Stoyanov, and Luke Zettlemoyer. BART：面向自然语言生成、翻译与理解的去噪序列到序列预训练. In Proc. of ACL, July 2020. URL https://arxiv.org/abs/1910.13461.

Chen Liang, Jonathan Berant, Quoc Le, Kenneth D. Forbus, and Ni Lao. 神经符号机器：在弱监督下于 Freebase 上学习语义解析器. In Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 23–33, Vancouver, Canada, July 2017. Association for Computational Linguistics. doi: 10.18653/v1/P17-1003. URL https://aclanthology.org/P17-1003.

Chen Liang, Mohammad Norouzi, Jonathan Berant, Quoc V Le, and Ni Lao. 面向程序合成与语义解析的记忆增强策略优化. Advances in Neural Information Processing Systems, 31, 2018.

Qian Liu, Bei Chen, Jiaqi Guo, Zeqi Lin, and Jian guang Lou. Tapex：通过学习神经 SQL 执行器做表格预训练, 2021.

Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy, Mike Lewis, Luke Zettlemoyer, and Veselin Stoyanov. Roberta：一种经过稳健优化的 BERT 预训练方法. arXiv preprint arXiv:1907.11692, 2019.

Arvind Neelakantan, Quoc V Le, and Ilya Sutskever. 神经程序员：用梯度下降归纳潜在程序. arXiv preprint arXiv:1511.04834, 2015.

Suixin Ou and Yongmei Liu. 通过结构感知的语义解析，学习为表格事实验证生成程序. In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 7624–7638, Dublin, Ireland, May 2022. Association for Computational Linguistics. doi: 10.18653/v1/2022.acl-long.525. URL https://aclanthology.org/2022.acl-long.525.

Panupong Pasupat and Percy Liang. 半结构化表格上的组合语义解析. In Proceedings of the 53rd Annual Meeting of the Association for Computational Linguistics and the 7th International Joint Conference on Natural Language Processing (Volume 1: Long Papers), pp. 1470–1480, Beijing, China, July 2015. Association for Computational Linguistics. doi: 10.3115/v1/P15-1142. URL https://aclanthology.org/P15-1142.

Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, and Peter J. Liu. 探索统一文本到文本 Transformer 的迁移学习极限. JLMR, 21, 2020. URL http://jmlr.org/papers/v21/20-074.html.

Nitarshan Rajkumar, Raymond Li, and Dzmitry Bahdanau. 评估大语言模型的 text-to-SQL 能力. arXiv preprint arXiv:2204.00498, 2022.

Torsten Scholak, Nathan Schucher, and Dzmitry Bahdanau. PICARD：为语言模型的约束自回归解码做增量解析. In Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, pp. 9895–9901, Online and Punta Cana, Dominican Republic, November 2021. Association for Computational Linguistics. doi: 10.18653/v1/2021.emnlp-main.779. URL https://aclanthology.org/2021.emnlp-main.779.

Peter Shaw, Ming-Wei Chang, Panupong Pasupat, and Kristina Toutanova. 组合泛化与自然语言变异：语义解析方法能否同时处理这两者？ In Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers), Online, August 2021. Association for Computational Linguistics.

Freda Shi, Daniel Fried, Marjan Ghazvininejad, Luke Zettlemoyer, and Sida I Wang. 带执行的自然语言到代码翻译. arXiv preprint arXiv:2204.11454, 2022.

Qi Shi, Yu Zhang, Qingyu Yin, and Ting Liu. 学习结合语言信息与符号信息，以做基于表格的事实验证. In Proceedings of the 28th International Conference on Computational Linguistics, pp. 5335–5346, 2020a.

Tianze Shi, Chen Zhao, Jordan Boyd-Graber, Hal Daumé III, and Lillian Lee. 论词汇–逻辑对齐对于把语句解析为 SQL 查询的潜力. In Findings of the Association for Computational Linguistics: EMNLP 2020, pp. 1849–1864, 2020b.

Hongjin Su, Jungo Kasai, Chen Henry Wu, Weijia Shi, Tianlu Wang, Jiayi Xin, Rui Zhang, Mari Ostendorf, Luke Zettlemoyer, Noah A Smith, et al. 选择性标注使语言模型成为更好的少样本学习者. arXiv preprint arXiv:2209.01975, 2022.

Alon Talmor, Ori Yoran, Amnon Catav, Dan Lahav, Yizhong Wang, Akari Asai, Gabriel Ilharco, Hannaneh Hajishirzi, and Jonathan Berant. Multimodalqa：面向文本、表格与图像的复杂问答. arXiv preprint arXiv:2104.06039, 2021.

James Thorne, Majid Yazdani, Marzieh Saeidi, Fabrizio Silvestri, Sebastian Riedel, and Alon Halevy. 在文本上做数据库式推理. arXiv preprint arXiv:2106.01074, 2021.

Bailin Wang, Ivan Titov, and Mirella Lapata. 借助潜在结构化对齐与抽象程序，从指称学习语义解析器. In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP), pp. 3774–3785, 2019.

<!-- 原 PDF 第 14 页 -->

Peng Wang, An Yang, Rui Men, Junyang Lin, Shuai Bai, Zhikang Li, Jianxin Ma, Chang Zhou, Jingren Zhou, and Hongxia Yang. 用简单的序列到序列学习框架统一架构、任务与模态. arXiv preprint arXiv:2202.03052, 2022.

Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Ed Chi, Quoc Le, and Denny Zhou. 思维链提示激发大语言模型中的推理. arXiv preprint arXiv:2201.11903, 2022.

Tomer Wolfson, Mor Geva, Ankit Gupta, Matt Gardner, Yoav Goldberg, Daniel Deutch, and Jonathan Berant. 把它拆开：一个问题理解基准. Transactions of the Association for Computational Linguistics, 2020.

Tianbao Xie, Chen Henry Wu, Peng Shi, Ruiqi Zhong, Torsten Scholak, Michihiro Yasunaga, Chien-Sheng Wu, Ming Zhong, Pengcheng Yin, Sida I. Wang, Victor Zhong, Bailin Wang, Chengzu Li, Connor Boyle, Ansong Ni, Ziyu Yao, Dragomir Radev, Caiming Xiong, Lingpeng Kong, Rui Zhang, Noah A. Smith, Luke Zettlemoyer, and Tao Yu. Unifiedskg：用文本到文本语言模型统一并多任务化结构化知识接地. arXiv preprint arXiv:2201.05966, 2022.

Xiaoyu Yang, Feng Nie, Yufei Feng, Quan Liu, Zhigang Chen, and Xiaodan Zhu. 借助言辞化与图注意力网络的程序增强事实验证. In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP), pp. 7810–7825, 2020.

Pengcheng Yin and Graham Neubig. 面向通用代码生成的句法神经模型. In Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 440–450, Vancouver, Canada, July 2017. Association for Computational Linguistics. doi: 10.18653/v1/P17-1041. URL https://aclanthology.org/P17-1041.

Pengcheng Yin, Graham Neubig, Wen-tau Yih, and Sebastian Riedel. TaBERT：面向文本与表格数据联合理解的预训练. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics. Association for Computational Linguistics, July 2020.

Ori Yoran, Alon Talmor, and Jonathan Berant. 翻转表格：从半结构化表格生成样例，使语言模型具备推理技能. In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 6016–6031, Dublin, Ireland, May 2022. Association for Computational Linguistics. doi: 10.18653/v1/2022.acl-long.416. URL https://aclanthology.org/2022.acl-long.416.

Tao Yu, Rui Zhang, Kai Yang, Michihiro Yasunaga, Dongxu Wang, Zifan Li, James Ma, Irene Li, Qingning Yao, Shanelle Roman, et al. Spider：面向复杂、跨领域语义解析与 text-to-SQL 任务的大规模人工标注数据集. In Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing, pp. 3911–3921, 2018.

Tao Yu, Chien-Sheng Wu, Xi Victoria Lin, Yi Chern Tan, Xinyi Yang, Dragomir Radev, Caiming Xiong, et al. Grappa：面向表格语义解析的语法增强预训练. In International Conference on Learning Representations, 2020.

John M. Zelle and Raymond J. Mooney. 用归纳逻辑程序设计学习解析数据库查询. In AAAI 1996, pp. 1050–1055, 1996.

Luke S. Zettlemoyer and Michael Collins. 学习把句子映射为逻辑形式：用概率范畴语法做结构化分类. UAI, 2005.

Yuchen Zhang, Panupong Pasupat, and Percy Liang. 面向高效语义解析的宏语法与整体触发. In Proceedings of the 2017 Conference on Empirical Methods in Natural Language Processing, pp. 1214–1223, 2017.

Victor Zhong, Caiming Xiong, and Richard Socher. Seq2sql：用强化学习从自然语言生成结构化查询. 2018.

Wanjun Zhong, Duyu Tang, Zhangyin Feng, Nan Duan, Ming Zhou, Ming Gong, Linjun Shou, Daxin Jiang, Jiahai Wang, and Jian Yin. Logicalfactchecker：用图模块网络借助逻辑运算做事实核查. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, pp. 6053–6065, 2020.

<!-- 原 PDF 第 15 页 -->

Fan Zhou, Mengkang Hu, Haoyu Dong, Zhoujun Cheng, Shi Han, and Dongmei Zhang. Tacube：预计算数据立方，以回答表格数据上的数值推理问题. arXiv preprint arXiv:2205.12682, 2022.

Zhaocheng Zhu, Mikhail Galkin, Zuobai Zhang, and Jian Tang. 面向知识图谱逻辑查询的神经符号模型. arXiv preprint arXiv:2205.10128, 2022.

<!-- 原 PDF 第 16 页 -->

## 附录

### A 更多实现细节

我们为有兴趣的读者给出 Codex Binder 实现中的更多细节。

#### A.1 Codex 的输入提示

下面列出主实验中 Binder 在各数据集上使用的提示。如图所示，提示以描述任务的说明开头，随后是若干供上下文学习使用的例子。我们遵循 Rajkumar et al.（2022）的表格提示格式：（1）`CREATE TABLE` 模式；（2）表格的前三行；（3）问题 $Q$ 以及解析得到的逻辑形式，即 Binder 程序。此外，我们还加入 `row_id`，并把所有表格内容转为小写；我们发现这会提高 Codex 的解析表现。对待推断样本，我们把 Binder 程序留空，让 Codex 生成它，并输入完整表格以提供更多信息。若完整表格过大，我们就减少上下文样本数，直到表格能放进 Codex 的最大词元限制。

以下提示中的说明与问题译为中文；表名、列名、单元格和程序保留原文。

**WikiTQ。** 说明：给定问题与表格，生成能够正确回答该问题的 SQL。

```
CREATE TABLE Electoral district of Lachlan(
row_id int,
member text,
party text,
term text)
/*
3 example rows:
SELECT * FROM w LIMIT 3;
row_id member party term
0 john ryan none 1859-1864
1 james martin none 1864-1869
2 james watson none 1869-1880
*/
Q: of the members of the third incarnation of the lachlan,
who served the longest?
Binder: SELECT member FROM w ORDER BY
f("How long does it last?"; term) DESC LIMIT 1
```

问题译为：在 Lachlan 选区第三届成员中，谁任职最久？API 中的 “How long does it last?” 译为：这段任期持续多久？

**TabFact。** 说明：给定陈述与表格，生成能够正确验证该陈述的 SQL。模式为 `british records in athletics`，列包括 `row_id`、`event`、`data`、`athlete`、`date`、`place`。本页抽出的示例行只到第一行：

```
row_id event data athlete date place
0 5 km t19:29 andi drake 1990-05-27 00:00:00 søfteland , norway
```

其余行、问题与 Binder 程序接在下一页。

<!-- 原 PDF 第 17 页 -->

示例行续：

```
1 5 miles 32:38 + ian mccombie 1985-03-23 00:00:00
york , united kingdom
2 10 km 40:17 chris maddocks 1989-04-30 00:00:00
burrator , united kingdom
*/
Q: there be 8 different event that take place within
the united kingdom
Binder: SELECT (SELECT COUNT(place) FROM w WHERE
f("Is it in united kingdom?"; place) = 'yes') = 8
```

问题译为：在英国境内举行的不同赛事有 8 项。API 中的 “Is it in united kingdom?” 译为：它是否在英国？

**MMQA。** 说明：给定问题、表格、段落与图像说明，生成能够正确回答该问题的 SQL。

```
CREATE TABLE 2018 Warrington Wolves season(
row_id int,
player text,
signed from text,
contract length text,
announced text)
/*
3 example rows:
SELECT * FROM w LIMIT 3;
row_id player signed from contract length announced
0 sitaleki akauola penrith panthers 2 2017-08-01
1 bryson goodwin south sydney rabbitohs 2 2017-10-01
2 tyrone roberts gold coast titans 3 2017-10-01
*/
CREATE TABLE Images(
row_id int,
gold coast titans text)
/*
All rows of the table:
SELECT * FROM w;
row_id gold coast titans
0 a logo for the golden knights is painted on the beach.
*/
Q: What player was transferred from the team that has crossed
swords on its logo to the Warrington Wolves in the 2018 season?
Binder: SELECT player FROM w WHERE
f("Has crossed swords on its logo?"; ‘signed from‘) = 'yes'
```

问题译为：哪一名球员是在 2018 赛季从队徽上有交叉剑的球队转会到 Warrington Wolves 的？API 中的 “Has crossed swords on its logo?” 译为：它的队徽上是否有交叉剑？图像说明译为：沙滩上画着 golden knights 的队徽。

在端到端问答设定中，提示几乎相同，只是所有上下文例子都使用完整表格内容，因为多数情况下问答必须看到完整表格才能正确回答问题。我们凭经验发现，把完整表格输入 Codex 对端到端问答是必要的，对语义解析则只有很小的额外收益。

在消融实验中，提示也几乎相同；例外是在超大表格的可扩展性设定下，我们截断的是表格行数，而不是上下文样本数，以便放进 Codex 的最大词元限制。这样做是为了模拟一种现实情形：只有表格的一部分能够输入模型。

#### A.2 Codex 超参数

在 Codex Binder 流水线的两个阶段，即解析与执行中，都会调用 Codex API。我们把 Codex 上下文学习的超参数设置如表 8 所示。

<!-- 原 PDF 第 18 页 -->

**表 8：主实验中设置的 Codex 超参数。** Codex 用于两个阶段：解析与执行。`find_tables` 未抽出该表。表头在文本中的顺序是：超参数、解析、执行，然后两组 WIKITQ、TABFACT、MMQA。每一数据行随后有 6 个值，按下表对应到“解析”的三列与“执行”的三列。

| 超参数 | 解析 / WikiTQ | 解析 / TABFACT | 解析 / MMQA | 执行 / WikiTQ | 执行 / TABFACT | 执行 / MMQA |
| --- | --- | --- | --- | --- | --- | --- |
| temperature | 0.4 | 0.6 | 0.4 | 0.0 | 0.0 | 0.0 |
| top_p | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| max_output_tokens | 512 | 512 | 512 | 1024 | 1024 | 1024 |
| sampling_n | 20 | 50 | 20 | 1 | 1 | 1 |
| stop_tokens | `\n\n` | `\n\n` | `\n\n` | `\n\n` | `\n\n` | `\n\n` |
| num_shots | 14 | 14 | 18 | 8 | 8 | 8 |

**解析。** 在解析阶段，也就是把问题解析成编程语言时，我们为每个数据集从训练集中标注大约十几个例子，或改写开发集中的例子，作为上下文演示。temperature 用来控制生成的随机性。我们发现，在多数情况下 0.4 是生成程序的忠实度与多样性之间合适的折中。sampling_n 是每个样本的生成数量（程序数）。我们启发式地把 WikiTQ 和 MMQA 的 sampling_n 设为 20，以平衡执行的时间成本与多数投票可能带来的性能增益。对 TABFACT，我们把 temperature 提高到 0.6，并把采样数提高到 50，因为我们凭经验发现，对二分类任务（或输出空间很小的任务），更多、更多样的生成能更好地确定最终答案。

**执行。** 如第 2 节所述，执行器会调用具有各种功能的模型。实验中，我们把 Codex 用作所有神经模块的底层模型，因为 Codex 本身是很强的大语言模型，能够实现文本和代码上的大多数功能。图像则事先由 OFA（Wang et al., 2022）通过图像说明转换成文本。注意，在 MMQA 上，若用专门的 VQA 模型替换 Codex（连同图像说明），图像上的性能很可能会提高，因为图像说明与问题无关，而 VQA 模型可以根据问题预测答案。

考虑到时间成本，我们让 Codex 对每个输入只以 temperature 0.0 输出一个答案，而不是输出多个答案再做多数投票。一个有趣的现象是，即使 temperature 为 0.0，Codex 在两次推断中的输出仍可能不同。OpenAI 团队表示，这来自 GPU 计算所固有的随机性，总体上输出在多数情况下是一致的，这与我们的观察相符。

我们还发现，为神经模块功能给 Codex 一些上下文演示会更好。我们标注了 50 个样本，作为一个小的检索池（各数据集共用），用于按问题把一列映射成新的一列，也就是 Binder 语法中的 $f_m$ API（原文抽取为 fm）。一个简单的 BLEU 分数检索器会从池中为每个到来的样本检索 8 个相似项，作为上下文演示。下面若干例子展示神经模块功能提示的格式。输出的（子）表包含一个按查询命名的新映射列，它会被进一步合并进原表。注意，把输出也写成一张（子）表是重要的；否则，如果 Codex 输出的是一列答案，它会搞不清自己正在为哪一行生成答案，表现会很差。

下面三则示例的提示外壳均为：Give a database as shown below（给定如下所示的数据库），输出标记为 QA map@ output。

**例 1。** 表名：Highest mountain peaks of California（加利福尼亚州最高的山峰）。列 prominence 的抽出值依次为：`10080 ft; 3072 m`、`1677 ft; 511 m`、`7196 ft; 2193 m`、`2894 ft; 882 m`、`9832 ft; 2997 m`、`2563 ft; 781 m`，对应 row_id 0 到 5。问题原文为：Answer question "What is the value of in feet?" row by row.（逐行回答问题“以英尺计的数值是多少？”）输出标记为 `QA map@ output`。新列名即为该问题，抽出的英尺值为：10080、1677、7196、2894、9832、2563。

<!-- 原 PDF 第 19 页 -->

例 1 的输出表按 row_id 0–5 排列，prominence 与英尺值如上。

**例 2。** 表名：2010-11 UAB Blazers men’s basketball team（2010–11 赛季 UAB Blazers 男子篮球队）。列 hometown 的抽出值为：`chicago, il, u.s.`、`oklahoma city, ok, u.s.`、`montgomery, al, u.s.`、`greenville, ms, u.s.`、`birmingham, al, u.s.`。问题原文为：Answer question "Is it from alabama?" row by row.（逐行回答“它是否来自阿拉巴马？”）抽出的答案依次为 no、no、yes、no、yes。其中 row_id 1 在抽取时城市与答案落在同一行：`oklahoma city, ok, u.s. no`；row_id 4 抽出为 `4.`。

**例 3。** 表名：1963 International Gold Cup（1963 年国际金杯赛）。列 driver 的抽出值为：jim clark、richie ginther、graham hill、jack brabham、tony maggs。问题原文为：Answer question "What is his/her country?" row by row.（逐行回答“他／她来自哪个国家？”）抽出的国家依次为：scotland、united states、england、australia、south africa。

<!-- 原 PDF 第 20 页 -->

#### A.3 多数投票策略

多数投票被广泛用于集成多个候选答案。多数投票的一种简单实现是：选择在候选中出现次数最多的答案作为最终答案。例如，给定含有 $n$ 个答案的候选答案池 $C$，输出答案 $a_{\mathrm{out}}$ 由下式得到：

$$
a_{\mathrm{out}} = \arg\max_{a}(\mathrm{count}(a)), \quad a \in \mathrm{set}(C)
\tag{1}
$$

其中 $\mathrm{count}(\cdot)$ 统计输入答案在 $C$ 中出现的次数，$\mathrm{set}(\cdot)$ 对输入列表去重。原文把下标 $a$ 与 $\arg\max$ 拆到了相邻行，$\in$ 与 set 之间无空格；上式按该处文字与后文定义还原。在我们的情形中，每个样本生成 $n$ 个程序，它们的执行结果组成候选答案池。

实验中我们采用多数投票的两种变体。第一种称为偏向答案。在 TABFACT 上，我们推测：用 SQL 程序把一条由多个子陈述组成的陈述验证为蕴含（即答案 1）是困难的，因为程序中的小错误就会使执行输出反驳（即答案 0）。换句话说，当答案 1 出现时我们更看重它，因为它表明该陈述有较高概率为蕴含。因此，我们重新加权：答案 1 计 4 票，答案 0 计 1 票。第二种是偏向程序。我们给生成程序中出现的 Binder 语言更大的权重，因为 Binder 在少样本提示中只占一小部分，从而更多生成会落在标准编程语言上。具体而言，在 WikiTQ 和 MMQA 上，我们把 Binder 程序重新加权为 10 票，其余为 1 票。

#### A.4 把 Binder 语法适配到 SQL

**图 4：** Binder 程序抽象语法树，以及对 SQL 语法的扩展示意。产生式规则中的蓝色类型由 Binder 扩展。树的连线在文本抽取中不完整，见原 PDF 第 20 页。抽出的问题为：Which is the best-selling solid-color Shirt made in America?（哪一件是在美国制造的、最畅销的纯色衬衫？）抽出的 SQL 为：

```sql
SELECT Shirt
FROM T
WHERE f(Solid-Color?; Shirt) = 'yes'
AND f(North America?; Made_in) = 'yes'
ORDER BY Sales DESC LIMIT 1
```

抽出的产生式扩展为：

```
Object Identifier  => Table | … | API Column
API Column         => Column | fcol(Q; D)
Function           => Aggregate | … | fval(Q; D)
```

抽出的树节点文字还包括：SQL、SELECT、FROM、WHERE、ORDER BY、Shirt、T、AND、LIMIT、`=`、yes、`f(Solid-Color?; Shirt)`、`f(North America?; Made_in)`、Sales、DESC、1。节点之间的边未完整抽出，不补画。

Binder 扩展编程语言的产生式规则，以保证 API 调用的返回值能与原来的语法兼容。以 SQL 为例，在图 4 中，两个 API $f_{\mathrm{col}}$ 与 $f_{\mathrm{val}}$ 被加入产生式规则，作为标识符，以便分别充当 SQL 中的列和值。所示 Binder 程序的抽象语法树与标准 SQL 的抽象语法树相当相似，只是 API 调用被放在列的位置。

#### A.5 评估器

当答案不是输入知识源中的一个片段时，程序执行结果天然更难与标准答案精确匹配；端到端模型则可能通过微调来匹配这种模式，或从问题中推断短语。然而，我们发现在 WikiTQ 中，程序执行输出的一些错误案例按人工判断是正确的。这些案例主要分为两类。第一类是 A 或 B 的选择问题，例如表 9 中的 “Are there at least 13 different components on the chart?”（图上是否至少有 13 种不同的组件？）。SQL 程序 `SELECT COUNT(component) > 13` 返回 1 表示“是”，返回 0 表示“否”。一般在 A 或 B 问题中，我们把 1 与 A 匹配、把 0 与 B 匹配。第二类是带单位的数字问题，例如表 9 中的 “what is the difference in years between constituency 1 and 2”（选区 1 与选区 2 相差多少年）。标准答案中含有单位 years，而程序几乎不可能推出 years；在这种情况下，4 也是一个合理的正确答案。因此，我们在 WikiTQ 官方评估器之上，为这两类问题增加了预匹配逻辑。此外，我们还用 Python 中的 Recognizers 包规范化日期。表 9 给出一些例子，以显示三种 WikiTQ 评估器的差异。为公平比较，实验中所有先前基线都用语义匹配评估器重新评估。

<!-- 原 PDF 第 21 页 -->

**表 9：用来说明 WikiTQ 上三种精确匹配评估器差异的例子。** 实验中，我们用语义匹配评估器评估所有基线与本文方法。`find_tables` 未抽出该表。判断符号按每个例子的三个标记依次对应三列评估器。原文问题 “constiuency” 的拼写按抽出文本保留。

| 例子 | EM（TaPEx 字符串匹配） | EM（WikiTQ 官方） | EM（语义匹配） |
| --- | --- | --- | --- |
| （规范化）问题：What was the same problem that Bernard Collomb had as Innes Ireland?（Bernard Collomb 与 Innes Ireland 遇到的是同一个什么问题？）标准答案：oil pressure。预测答案：oil pressure (56 laps)。 | × | ✓ | ✓ |
| （浮点精度）问题：What is the difference between the qualifying time in 1967 and 1965?（1967 年与 1965 年的排位赛用时相差多少？）标准答案：7.45。预测答案：7.449999999999989。 | × | ✓ | ✓ |
| （A 或 B 选择）问题：Are there at least 13 different components on the chart?（图上是否至少有 13 种不同的组件？）标准答案：Yes。预测答案：1。 | × | × | ✓ |
| （带单位的数字）问题：What is the difference in years between constiuency 1 and 2?（选区 1 与选区 2 相差多少年？）标准答案：4 years。预测答案：4。 | × | × | ✓ |

**图 5：** 把 Binder 方法（本文）与其他大语言模型用法范式相比较：端到端、思维链，以及语义解析／代码生成。图内示意的版式文字未完整抽出，见原 PDF 第 21 页；比较的文字说明见下文附录 B。

### B 与其他大语言模型用法范式的比较

除本文外，也有其他工作关注如何以有创造性的方式利用大语言模型，在下游任务上取得更好的性能，并因设计得当而看到提升。我们把 Binder 方法与此前三种大语言模型用法范式相比较：端到端（原文一处写作 End-End）、思维链（Chain-of-Thought），以及语义解析／代码生成。

**端到端。** 端到端方法（Brown et al., 2020; Hoffmann et al., 2022 等）旨在用大语言模型直接生成最终答案，通常的做法是提供任务描述和／或少量例子供上下文学习。尽管它已经有效到足以在大量基准上达到或接近当时最佳性能，它的问题是不可解释，并且稳健性不足。

**思维链。** 思维链方法（Wei et al., 2022; Chowdhery et al., 2022a; Kojima et al., 2022; Chung et al., 2022 等）通过生成一系列中间推理步骤，提高大语言模型做复杂推理的能力。尽管它在多个基准上取得很大成功，思维链作为模型生成的自然语言，存在不可靠和不可控的问题。

**语义解析／代码生成。** 语义解析／代码生成方法（Chen et al.,

<!-- 原 PDF 第 22 页 -->

2021; Rajkumar et al., 2022; Shi et al., 2022）旨在把问题解析成预先定义的程序（SQL、Python 等），再通过相应的解释器执行。相对端到端和思维链方法，它在可解释性和稳健性上有优势，但仍然受预先定义的编程语言的固定语法所困，因而覆盖范围先天有限（Shi et al., 2020b）。

**Binder。** Binder 是一种神经符号范式，旨在把问题映射到一段程序，并允许绑定统一的语言模型 API 以获得额外功能。这样既保持语义解析方法的可解释性与稳健性，又解开语法对其覆盖的限制。

### C 更多实验结果

#### C.1 更多先前系统的结果

限于篇幅，我们没有在 WikiTQ 和 TABFACT 的主要结果中列出全部先前系统。本节给出更多先前方法与本文方法的比较，如表 10 与表 11 所示。两表在原 PDF 中并排。`find_tables` 未抽出它们，数字来自按页文本，按每个方法名之后依次出现的数值填入，未另补数字。

**表 10：更多先前系统在 WikiTQ 上的执行准确率。** ¶ 表示该结果已用表 9 中的语义匹配评估器重新评估。† 表示输出中间语言的符号方法。

| 方法 | 开发集 | 测试集 |
| --- | --- | --- |
| **微调** | | |
| Pasupat & Liang (2015) | 37.0 | 37.1 |
| Neelakantan et al. (2015) | 34.1 | 34.2 |
| Zhang et al. (2017) | 40.6 | 43.7 |
| Liang et al. (2018) | 42.7 | 43.8 |
| Dasigi et al. (2019) | 43.1 | 44.3 |
| Agarwal et al. (2019) | 43.2 | 44.1 |
| Wang et al. (2019) | 43.7 | 44.5 |
| Herzig et al. (2020) | - | 48.8 |
| Xie et al. (2022)¶ | 51.9 | 50.6 |
| Yin et al. (2020) | 53.0 | 52.3 |
| Yu et al. (2020) | 51.9 | 52.7 |
| Guo et al. (2021) | 53.6 | 52.3 |
| Liu et al. (2021)¶ | 60.4 | 59.1 |
| Zhou et al. (2022)¶ | 61.1 | 61.3 |
| Jiang et al. (2022)¶ | - | 63.3 |
| **不做微调** | | |
| Codex 端到端问答¶ | 50.5 | 48.7 |
| Codex SQL¶† | 60.2 | 61.1 |
| Codex Binder†（本文） | 65.3 | 65.2 |

**表 11：更多先前系统在 TABFACT 小测试集上的准确率。** † 表示输出中间语言的符号方法。

| 方法 | 小测试集 |
| --- | --- |
| **微调** | |
| Chen et al. (2019a)† | 68.1 |
| Zhong et al. (2020)† | 74.3 |
| Shi et al. (2020a)† | 74.2 |
| Yang et al. (2020)† | 76.2 |
| Ou & Liu (2022)† | 77.0 |
| Liu et al. (2021)（BART-Large） | 82.5 |
| Eisenschlos et al. (2020) | 83.9 |
| Xie et al. (2022) | 85.4 |
| Liu et al. (2021)（Tapex） | 85.9 |
| **不做微调** | |
| Codex 端到端问答 | 72.6 |
| Codex SQL† | 80.7 |
| Codex Binder†（本文） | 85.1 |
| 使用少样本检索器 | 86.0 |

#### C.2 使用 WikiTQ 官方评估器的结果

我们在表 12 中列出 Binder 在 WikiTQ 官方评估器下的性能。如图所示，相对语义匹配评估器存在性能下降。带 SQL 和 Binder 的符号方法下降更大（约 2.5%），端到端方法下降较小（约 1%），因为 A 或 B 选择问题以及带单位的数字答案（见表 9 的说明）被判为不正确。

#### C.3 多数投票候选数量的消融

本节经验地研究生成数量（即候选 Binder 程序的数量）如何影响多数投票的性能。如图 6 与图 7 所示，增加多数投票的候选数会有效提高 WikiTQ 和 TABFACT 上的性能。经

<!-- 原 PDF 第 23 页 -->

**表 12：使用 WikiTQ 官方评估器、并带有日期识别规范化器时的执行准确率。** `find_tables` 未抽出该表，数字来自按页文本。

| 方法 | 开发集 | 测试集 |
| --- | --- | --- |
| **微调** | | |
| T5-3B（Xie et al., 2022） | 51.6 | 50.3 |
| Tapex（Liu et al., 2021） | 60.1 | 58.5 |
| TaCube（Zhou et al., 2022） | 60.9 | 60.8 |
| OmniTab（Jiang et al., 2022） | - | 62.9 |
| **不做微调** | | |
| Codex 端到端问答 | 49.3 | 47.6 |
| Codex SQL† | 57.6 | 55.1 |
| Codex Binder†（本文） | 62.6 | 61.9 |

验上，TABFACT 需要更多候选才能判定蕴含或反驳。我们目前还没有在 WikiTQ 上用超过 20 个候选程序做实验，那样做或许还能把当前最佳性能再抬高一点。

**图 6：** WikiTQ 开发集上、多数投票使用不同生成数量（横轴）时的执行准确率。抽出的横轴刻度为 1、5、10、15、20，纵轴刻度为 59、60、61、62、63、64、65、66。曲线上的具体坐标点未抽出，不编造数值，见原 PDF 第 23 页。

**图 7：** TABFACT 小测试集上、多数投票使用不同生成数量（横轴）时的执行准确率。抽出的横轴刻度为 1、5、10、20、30、40、50、60，纵轴刻度为 81、82、83、84、85、86、87。曲线上的具体坐标点未抽出，不编造数值，见原 PDF 第 23 页。

#### C.4 按我们的统计，WikiTQ 中 SQL 不可解的比例

在表 3，即 WikiTQ 开发集执行准确率的分解中，可以看到 Binder 方法在程序可解子集上也取得优势（而纯 SQL 方法在程序不可解部分仍能有一定性能）。这令人意外，因为按照 SQUALL 数据集的标注，这一部分本已可以由 SQL 求解，因此我们的方法在理论上并不会提高这一部分的性能。进一步地，我们发现原因在于：在 SQUALL 中，作者在做 SQL 标注之前规范化了表格的一部分，并且也漏掉了一些在规范化表格之后本可以求解的样本。反过来，SQUALL 所标记的数据中有相当一部分，当我们使用原始表格而不是作者修改过的表格时，会发现它属于程序无法解决的部分，于是 Binder 能在其上获得一些优势。SQUALL 未标记的那一部分也是如此。我们把 SQUALL 数据集的 SQL 标注，在我们为每个样本规范化之后的表格上重新执行，通过执行结果是否与先前结果匹配来检查并重新判断该样本是否为程序可解样本，得到新的划分：程序不可解 1251 条（44.19%），程序可解 1580 条（55.81%）。（按 SQUALL 的先前划分是 625 条（22.08%）与 2206 条（77.92%）。人工清洗表格减少了表格内容噪声，但也低估了真实数据所带来的挑战。）新的划分将在我们的代码中发布，供今后更细粒度的分析或探索使用。

<!-- 原 PDF 第 24 页 -->

### D 扩展 Binder 的流水线

本节介绍一条使用 Codex 的流水线，把 Binder 扩展到带有新编程语言和神经模块的新领域。图 8 说明该流水线。

**图 8：** 把 Binder 扩展到新领域的流水线。抽出的步骤文字为：（1）选择一种编程语言；（2）标注 Binder 程序（大约十几个就够）；（3）用 Codex 生成 Binder 程序；（4）把底层模型应用到神经模块（一个大语言模型可能就够）；（5）执行 Binder 程序。结果侧标出良好性能、可解释性、可扩展性。图中还区分自动化与人工劳动。方框之间的连线未完整抽出，见原 PDF 第 24 页。

（1）根据领域选择一种编程语言作为中间表示。例如，SQL 适合表格领域，SPARQL 与 Cypher 适合知识图谱领域，而 Python、Lisp、Java 等通用语言更可能被适配到各种领域。

（2）在把文本解析成 Binder 程序之前，需要上下文例子，帮助 Codex 学习这项任务，以及相对原语言的语法适配（即插入的神经模块）。经验上，由于 Codex 已在代码上做过大量预训练，大约十几个 Binder 程序标注就够了。此外，标注一个更大的例子池（例如 100 个），再为每个推断样本检索上下文例子，已被证明是提高解析准确率的有效办法，正如我们在 TABFACT 上所做的那样。

（3）给定上下文例子和推断查询，用 Codex 生成 Binder 程序。Codex 的超参数可以根据任务调整。

（4）把模型与 Binder 程序中的神经模块功能绑定。在本文中，我们把 Codex 设为所有功能的唯一底层模型，例如常识问答、信息抽取，因为大语言模型能力强且易用。如果单个大语言模型不足以实现所需功能，例如 VQA，而输入是图像，就把 API 与专门的 VQA 模型绑定。

（5）用确定性的语言执行器与神经模型执行 Binder 程序。

### E 错误分析

#### E.1 错误类型

我们把错误类型分为：

（1）语法错误：预测不满足 Binder 程序的语法。

（2）语义错误：

- 列：选错列，或遗漏来自某列的限制。
- 值：使用错误的值，或把模糊匹配与精确匹配混淆。
- 运算符：使用错误的运算符，或遗漏运算符的限制。
- 结构：查询产生了整体结构错误。要么查询的整体含义被误解；要么查询只考虑了问题，对该表格完全不适用。
- Binder 用法：在需要时没有使用 Binder，或 Binder 单元格内部的指令不恰当、含糊，无法执行。

（3）执行不正确：预测的程序是正确的，但最终结果是错的，因为执行过程中预测出了一些错误的中间答案（信息抽取出错、处理边界值出错等）。

（4）假阴性：标准答案的标注是错的；或者预测实际上是对的，但执行器因能力有限而误判为错。

<!-- 原 PDF 第 25 页 -->

**表 13：WikiTQ 样本 nt-1239 的表格，标题为 “Kansas–Kansas State football rivalry”（堪萨斯大学对堪萨斯州立大学的橄榄球对抗）。** 我们用它演示可解释性（原文拼作 interpretibility）。与得到答案无关的行已删去。查询为：When was the first game that kansas state won by double digits?（堪萨斯州立大学第一次以两位数分差获胜是在何时？）标准答案为 1926。`find_tables` 未抽出该表。下列各行按抽出的字段顺序排列：row_id、year、site、winning team、losing team、series。省略号为原文中的删节。

| row_id | year | site | winning team | losing team | series |
| --- | --- | --- | --- | --- | --- |
| 0 | 1902 | lawrence | kansas 16 | kansas state 0 | ku 1–0 |
| 1 | 1903 | lawrence | kansas 34 | kansas state 0 | ku 2–0 |
| 2 | 1904 | manhattan | kansas 41 | kansas state 4 | ku 3–0 |
| 3 | 1905 | lawrence | kansas 28 | kansas state 0 | ku 4–0 |
| 4 | 1906 | manhattan | kansas state 6 | kansas 4 | ku 4–1 |
| 5 | 1907 | lawrence | kansas 29 | kansas state 10 | ku 5–1 |
| … | | | | | |
| 21 | 1924 | manhattan | kansas state 6 | kansas 0 | ku 17–2–3 |
| 22 | 1925 | lawrence | kansas state 14 | kansas 7 | ku 17–3–3 |
| 23 | 1926 | manhattan | kansas state 27 | kansas 0 | ku 17–4–3 |
| 24 | 1927 | lawrence | kansas state 13 | kansas 2 | ku 17–5–3 |
| 25 | 1928 | manhattan | kansas 7 | kansas state 0 | ku 18–5–3 |
| … | | | | | |

#### E.2 错误示例

WikiTQ nt-1239 的上下文（表格、查询、答案）见表 13。

### F 标注界面

我们构建了一个标注界面，可以借助 Hugging Face Spaces 做实时执行（https://huggingface.co/spaces）。目前支持 SQL，以及带 SQL 的 Binder。我们将发布源代码，希望有助于社区中那些需要符号语言的任务标注，例如语义解析和代码生成。图 9 与图 10 展示我们的界面。

<!-- 原 PDF 第 26 页 -->

**图 9：** WikiTQ 标注界面的一个例子。界面画面中的文字未抽出，见原 PDF 第 26 页。

<!-- 原 PDF 第 27 页 -->

**图 10：** TABFACT 标注界面的一个例子。界面画面中的文字未抽出，见原 PDF 第 27 页。

<!-- 译完 -->
