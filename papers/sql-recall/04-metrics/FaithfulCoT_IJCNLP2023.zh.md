原文件名：FaithfulCoT_IJCNLP2023.pdf

原标题：Faithful Chain-of-Thought Reasoning

中文标题：忠实的思维链推理

作者：Qing Lyu\*、Shreya Havaldar\*、Adam Stein\*、Li Zhang、Delip Rao、Eric Wong、Marianna Apidianaki、Chris Callison-Burch（University of Pennsylvania；\*同等贡献）

会议：Proceedings of the 13th International Joint Conference on Natural Language Processing and the 3rd Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics (Volume 1: Long Papers)，第 305–329 页，2023 年 11 月 1–4 日。©2023 Association for Computational Linguistics

<!-- 原 PDF 第 1 页 -->

# 忠实的思维链推理

Qing Lyu\*　Shreya Havaldar\*　Adam Stein\*　Li Zhang　Delip Rao　Eric Wong　Marianna Apidianaki　Chris Callison-Burch

University of Pennsylvania

{lyuqing, shreyah, steinad, zharry, exwong, marapi, ccb}@seas.upenn.edu, deliprao@gmail.com

\*同等贡献。

## 摘要

尽管思维链（Chain-of-Thought，CoT）提示提升了语言模型（Language Model，LM）在一系列复杂推理任务上的表现，所生成的推理链并不必然反映模型如何得出答案（即忠实性，faithfulness）。我们提出 Faithful CoT，一种包含两个阶段的推理框架：翻译（自然语言查询 → 符号推理链）与问题求解（推理链 → 答案），分别使用一个 LM 与一个确定性求解器。这保证推理链对最终答案给出忠实解释。除可解释性之外，Faithful CoT 也提升了经验性能：在来自 4 个不同领域的 10 个基准中，它在 9 个上优于标准 CoT，相对准确率增益在数学应用题（Math Word Problems，MWP）上为 6.3%，在规划（Planning）上为 3.4%，在多跳问答（Multi-hop Question Answering，QA）上为 5.5%，在关系推理（Relational Inference）上为 21.4%。此外，配合 GPT-4 与 Codex，它在 7 个数据集上创下新的少样本（few-shot）最先进性能（其中 6 个准确率达到 95.0 以上），表明忠实性与准确率之间存在很强的协同。¹

¹ 我们的代码、数据与提示见 https://github.com/veronica320/Faithful-COT 。

## 1 引言

常识推理、数学推理等复杂推理任务，长期以来一直是 LM 的阿喀琉斯之踵（Bengio, 2019），直到近期关于 CoT 推理的一系列工作（Wei et al., 2022; Wang et al., 2022, 等）带来显著的性能提升。CoT 仅给出少量上下文示例，就提示 LM 在生成答案的同时生成一条推理链。

除性能提升外，CoT 还被声称能够“为观察模型行为提供一个可解释的窗口”（Wei et al., 2022）。然而，这些推理链在多大程度上准确反映模型预测背后的底层推理过程，亦即它们作为解释有多忠实（Jacovi and Goldberg, 2020, 等），并不清楚。在标准 CoT 中，忠实性没有保证，甚至被系统性地违背（Turpin et al., 2023），因为最终答案并不必然由所生成的推理链推出。换言之，CoT 可能就模型的真实推理过程“撒谎”。图 1 给出 Wei et al. (2022) 在 GSM8K 上一次不忠实的 CoT 生成：答案“0”甚至没有出现在推理链中。这一点，连同附录 B.1 中的更多例子，说明标准 CoT 并不能提供模型如何预测答案的可解释性。

**图 1：** CoT 提示（Wei et al., 2022）在 GSM8K 上的一次不忠实输出。答案（绿色）并不能由推理链（蓝色）推出。

问：John 打算卖掉他所有的玩具，并用这笔钱买电子游戏。他有 13 套乐高，每套卖 15 美元。最后他以每款 20 美元买了 8 款电子游戏，还剩下 5 美元。他还剩多少套乐高？

答：他一开始有 13 套乐高。他以每套 15 美元卖掉它们。因此卖掉后他一定得到了 $13 \times \$15 = \$195$。他用这笔钱以每款 20 美元买了 8 款电子游戏。这意味着他在电子游戏上花了 $8 \times \$20 = \$160$。他还剩 5 美元，所以他总共一定曾经有 $\$195 + \$5 = \$200$。答案是 0。

CoT 缺乏忠实性，在高风险应用中可能是危险的：它会误导人们相信模型是自解释的，而推理链与答案之间并无真实的因果关系。更糟的是，当一个不忠实的解释看起来合理（即对人类有说服力）（Jacovi and Goldberg, 2020）时，人们（例如法律从业者）就更容易过度信任模型（例如再犯预测器），即便该模型带有隐性偏见（例如针对少数族裔）（Pruthi et al., 2020; Slack et al., 2020）。

为应对这一担忧，我们提出 Faithful CoT：一种推理框架，其中答案是确定性执行推理链的结果。具体而言，我们把一个复杂推理任务拆成两个阶段：

<!-- 原 PDF 第 2 页 -->

**图 2：** Faithful CoT 框架概览。它包含翻译（Translation）与问题求解（Problem Solving）：在翻译中，一个 LM 把自然语言（Natural Language，NL）查询翻译成一条推理链（NL 与符号语言 Symbolic Language，SL 交错）；在问题求解中，一个确定性求解器执行该推理链以得出答案。流程为：查询（NL）→ 翻译（语言模型）→ 推理链（NL + SL）→ 问题求解（确定性求解器）→ 答案。

翻译与问题求解（图 2）。在翻译阶段，一个 LM 把查询翻译成一条推理链，其中 NL 与 SL 交错出现。NL 部分把原始查询分解为多个更简单、相互依赖的子问题。随后，每个子问题用依赖任务的 SL 来处理，例如 Python、Datalog，或规划领域定义语言（Planning Domain Definition Language，PDDL）。在问题求解阶段，推理链由确定性求解器执行，例如 Python/Datalog 解释器或 PDDL 规划器，从而得出答案。

我们的推理链（翻译阶段的结果）保证能为最终答案如何产生（问题求解阶段的结果）提供忠实解释，因此本方法比标准 CoT 方法更可解释。² 可解释性并不等同于正确性（即本方法既能揭示正确答案背后的推理过程，也能揭示错误答案背后的推理过程），但我们发现它在经验上确实能提高正确性：在来自 4 个不同领域（MWP、规划、多跳 QA 与关系推理）的 10 个推理数据集上评估时，Faithful CoT 在不同 LM 与解码策略下，相对三个现有基线都带来一致的性能增益。使用 Codex 时，我们的方法在 10 个数据集中的 9 个上优于原版 CoT，相对准确率增益在 MWP 上为 6.3%，在规划上为 3.4%，在多跳 QA 上为 5.5%，在关系推理上为 21.4%。使用 GPT-4 时，我们的方法在 7 个数据集上取得新的少样本最先进（state-of-the-art，SOTA）性能，其中 6 个准确率达到 95.0 以上。这表明可解释性不必以性能为代价；相反，二者之间存在很强的协同。

² 我们并不声称生成推理链本身的过程，即翻译阶段，是可解释的。更多讨论见“局限性”。

我们的主要贡献如下：

（a）我们提出 Faithful CoT，把推理分解为翻译与问题求解。推理链把用户可理解的自然语言注释与可执行的符号语言程序交错在一起，从而忠实地解释模型如何得出答案。

（b）得益于可与任意 SL 及外部求解器灵活结合，本方法能够推广到算术推理与简单符号推理之外的多个领域。我们在 10 个推理数据集中的 7 个上取得新的 SOTA 性能，表明忠实性与准确率之间存在很强的协同。

（c）我们对本方法的优劣作了广泛分析，展示了它在不同 LM 上的可推广性、对示例选择与提示措辞的稳健性、求解器的关键作用、所生成推理链的合理性，以及它仍然容易出错的常见错误模式。

## 2 相关工作

**忠实性。** 在可解释性中，忠实性（也称为保真度 fidelity 或可靠性 reliability）意味着解释应当“准确表征模型预测背后的推理过程”，这是对解释的一项基本要求（Harrington et al., 1985; Ribeiro et al., 2016; Gilpin et al., 2018; Jacovi and Goldberg, 2020）。³ 它应与合理性（plausibility，也称说服力或可理解性）相对照；合理性指的是“一个解释对人类有多令人信服”（Herman, 2019; Jacovi and Goldberg, 2020）。在 CoT 提示的语境中，忠实的推理链需要准确反映模型如何得出最终答案，而合理的推理链则是在人类看来合理且连贯的推理链。标准 CoT（Wei et al., 2022）生成的推理链完全是自然语言，因而常常看起来合理；然而，最终答案并不需要因果地从推理链推出，因此不能保证忠实性。

³ 请注意，这不同于自然语言生成（Natural Language Generation，NLG）文献中的忠实性概念，主要差别在于什么构成真值。在可解释性中，我们谈论的是解释相对于模型底层推理机制的忠实性——真值通常未知。在 NLG 中，我们谈论的是生成文本（例如一个译句或一篇摘要）相对于某个显式来源（例如源句或全文）的忠实性——真值是透明的。

<!-- 原 PDF 第 3 页 -->

**思维链式提示。** 在 CoT 式提示中，给定一个复杂问题 $Q$，LM 被提示生成推理链 $C$ 以及最终答案 $A$。具体而言，提示由若干 $(Q, C, A)$ 三元组示例组成，称为上下文示例。这使预训练 LM（例如 GPT-3（Brown et al., 2020））在解答未见问题时的准确率远高于标准提示；在标准提示中，示例不包含推理链 $C$。

我们将现有 CoT 式提示方法分为三类：一次完成（all-at-once）、基于集成（ensemble-based）与模块化（modularized）。一次完成提示指 LM 把 $C$ 与 $A$ 作为一段连续字符串生成，二者之间没有任何依赖或约束。Scratchpad（Nye et al., 2021）、标准 CoT（Wei et al., 2022）以及“让我们一步一步思考”（Kojima et al., 2022）都属于这一类。基于集成的提示旨在克服前述方法中一次生成的局部最优问题：采样多个 $(C, A)$ 对，再通过多数投票等策略选择最佳答案。例子包括自一致 CoT（Self-Consistent CoT，Wang et al., 2022）、Minerva（Lewkowycz et al., 2022）与 DIVERSE（Li et al., 2022），它们的主要差别在于投票粒度与底层 LM。模块化方法把 $Q$ 分解为子问题，再逐个攻克（Jung et al., 2022; Qian et al., 2022, 等）。其中，从易到难提示（Least-to-Most，Zhou et al., 2022）与我们有相似的问题分解过程，但由于推理链完全是 NL，仍然没有忠实性保证。

与我们的工作同期，Chen et al. (2022) 与 Gao et al. (2022) 都生成 Python 程序（即仅含 SL 的推理链）来得出答案。我们希望强调以下质性差别：⁴（a）就动机而言，我们的方法由可解释性驱动，而他们的方法由性能驱动。（b）我们的推理链包含对问题的结构化 NL 分解，使没有编程背景的用户也能更好地理解系统，并有可能与之交互。（c）他们只使用 Python 作为 SL，并且只处理数学与简单符号推理任务，而我们展示了本方法对多种符号语言以及其他多个领域的可推广性。特别地，我们创新地把一组多样化的现实任务（规划、多跳 QA 与关系推理）改写为符号表示，从而可以用单一框架处理它们。（d）与先前工作相比，我们做了更全面的分析，尤其是对推理链正确性的人工评估。

⁴ 经验比较亦见附录 B.3。

## 3 方法

我们的方法 Faithful CoT 是一个两阶段流水线，如图 2 所示。与先前的 CoT 式工作一样，我们的提示由 $(Q, C, A)$ 三元组组成。显著差别在于我们在 $C$ 中独特地把 NL（自然语言）与 SL（符号语言）交错在一起，以及我们导出最终答案 $A$ 的方式。

在翻译阶段，给定一个 NL 形式的复杂查询 $Q$，我们提示 LM 把它翻译成推理链 $C$，其中 NL 注释与 SL 程序交错。NL 部分把原始查询分解为多个更简单、相互依赖的子问题。随后，每个子问题用依赖任务的 SL 处理，例如 Python、Datalog 或 PDDL。在问题求解阶段，我们调用一个确定性的外部求解器，例如 Python 解释器、Datalog 执行器或 PDDL 规划器（取决于任务），从推理链 $C$ 得到答案 $A$。如图 3 所示，我们把 $C$ 中的 NL 部分（黑色）记为 $C_{\mathrm{NL}}$，把 SL 部分（蓝色）记为 $C_{\mathrm{SL}}$。尽管记号上把两部分分开，它们在生成中是交错的。用这种方法，$C$ 保证是一个忠实的模型解释，因为最终的 $A$ 是确定性执行 $C_{\mathrm{SL}}$ 的结果。此外，$C_{\mathrm{NL}}$ 使用户能更好地理解推理过程。⁵

⁵ 在主实验中，我们没有在 $C_{\mathrm{NL}}$ 与 $C_{\mathrm{SL}}$ 之间施加约束；我们在第 C.4 节分析这一点。

我们把该方法应用于 4 类复杂推理任务：MWP、多跳 QA、规划与关系推理。接下来，我们用图 3 中的例子说明该方法在每一类任务上如何工作。

### 3.1 数学应用题（MWP）

给定一道用 NL 写成的小学数学题 $Q$（“如果停车场里有 3 辆车，又来了 2 辆车，停车场里一共有多少辆车？”，图 3 中为绿色），我们希望得到一个实数值 $A$（5）。在翻译阶段，我们提示 LM 接收 $Q$ 并生成推理链 $C$，其中 $C_{\mathrm{NL}}$ 与 $C_{\mathrm{SL}}$ 交错。具体而言，$C_{\mathrm{NL}}$ 包含三类信息：

（a）子问题：把 $Q$ 拆成多个更小规模的子问题，例如“1. 一开始有多少辆车？”“2. 来了多少辆车？”以及“3. 停车场里有多少辆车？”。

（b）依赖图：每个子问题既可以借助上下文直接回答（子问题 1 和 2 是“独立的”），也可以依赖先前子问题的答案（子问题 3“依赖于 1 和 2”）。

（c）依据：每个子问题都附有支持答案的依据（“support”字段）。依据可以是原始上下文的一个子集（“又来了 2 辆车”），也可以是与该子问题相关的任何外部知识（“一周有 7 天”）。

每个子问题及其对应的依赖与依据，指导随后 $C_{\mathrm{SL}}$ 的生成。在图 3 的例子中，$C_{\mathrm{SL}}$ 由为回答 $C_{\mathrm{NL}}$ 中每个子问题而生成的 Python 代码组成。在问题求解阶段，我们用求解器（一个 Python 解释器）执行 $C_{\mathrm{SL}}$，得到 $A$（最终有 5 辆车）。

### 3.2 多跳 QA

给定一个需要多步推理的复杂问题 $Q$（例如“一只梨会沉入水中吗？”，图 3 中为红色），我们希望得到布尔值或字符串值变量形式的答案 $A$。与 MWP 的任务形式类似，$C$ 交错 $C_{\mathrm{NL}}$（NL 注释）与 $C_{\mathrm{SL}}$（符号程序）。根据任务性质，推理链 $C$ 的格式略有不同：对某些数据集，LM 先用 NL 生成全部子问题及其答案，再把这些答案表示为 SL 以导出 $A$（见图 3）；对另一些数据集，LM 把 NL 子问题与 SL 程序交错生成，类似于 MWP（见表 14 与表 15 的例子）。在 SL 方面，我们同时使用 Python 与 Datalog，同样取决于数据集。由于多跳 QA 问题需要多步推理才能解决，$C_{\mathrm{SL}}$ 常常使用布尔代数与字符串比较（在 Python 中），以及关系定义与逻辑程序（在 Datalog 中）。我们用相应的解释器作为确定性求解器来执行 $C_{\mathrm{SL}}$ 并得到 $A$。

在图 3 的例子中，LM 首先生成子问题“1. 梨的密度是多少？”与“2. 水的密度是多少？”，二者分别在 NL 中得到回答

<!-- 原 PDF 第 4 页 -->

**图 3：** 来自各任务（数学应用题、多跳 QA、关系推理与规划）的例子，展示我们的两阶段翻译与问题求解流水线。左侧为查询，中间为推理链，右侧为答案。翻译器为 LM，求解器为确定性求解器。

**数学应用题。** 查询：如果停车场里有 3 辆车，又来了 2 辆车，停车场里一共有多少辆车？

推理链：

```text
# 1. 一开始有多少辆车？（独立，依据：["停车场里有 3 辆车"]）
n_cars_begin = 3
# 2. 来了多少辆车？（独立，依据：["又来了 2 辆车"]）
n_cars_arrive = 2
# 3. 最终答案：停车场里有多少辆车？（依赖于 1、2）
n_cars_total = n_cars_begin + n_cars_arrive
```

答案：5。

**多跳 QA。** 查询：一只苹果会沉入水中吗？

推理链：

```text
// 1. 一只苹果的密度是多少？
// 一只苹果的密度大约是 0.75 g/cm^3。
// 2. 水的密度是多少？
// 水的密度是 1 g/cm^3。
// 然后，我们用 Datalog 表示这些答案：
// 1. 一只苹果的密度大约是 0.75 g/cm^3。
.decl Has_density(Object:symbol, Density:float)
Has_density("apple", 0.75).
// 2. 水的密度是 1 g/cm^3。
Has_density("water", 1).
// 现在，我们导出最终答案：一只苹果会沉入水中吗？
// 仅当苹果比水更密时，答案才为是。
.decl Answer()
Answer() :- Has_density("apple", density1), Has_density("water", density2), density1 > density2.
.output Answer
```

答案：否。

**关系推理。** 查询：[Gabrielle] 开车送她的女儿 [Dorothy] 去医院。[Dorothy] 的儿子 [Vincent] 不久后出现。[Vincent] 与 [Gabrielle] 是什么关系？

推理链：

```text
# 1. [Vincent] 与 [Dorothy] 是什么关系？（独立，依据："[Dorothy] 的儿子 [Vincent] 不久后出现。"）
relation(Vincent, Dorothy) = son
# 2. [Dorothy] 与 [Gabrielle] 是什么关系？（独立，依据："[Gabrielle] 开车送她的女儿 [Dorothy] 去医院。"）
relation(Dorothy, Gabrielle) = daughter
# 3. 最终答案：[Vincent] 与 [Gabrielle] 是什么关系？（依赖于 1、2）
relation(Vincent, Gabrielle) = relation(Vincent, Dorothy) @ relation(Dorothy, Gabrielle)
```

答案：grandson（孙子）。

**规划。** 查询：我把可乐洒在桌子上了，你能把它扔掉，并拿点东西来打扫吗？

PDDL 中的目标：

```text
(:goal
    ; 我需要做两件事
    (and
        ; 首先扔掉可乐
        (at coke trash)
        ; 然后给用户拿一块海绵作为清洁工具
        (at sponge user)
    )
)
```

答案：

1. find(coke)
2. pick(coke)
3. find(trash)
4. put(coke)
5. find(sponge)
6. pick(sponge)
7. find(user)
8. put(sponge)

（图中多跳 QA 的示例查询在正文第 3.2 节写作“梨”，图 3 图题区域抽取为“苹果”。正文后续密度数值与图中示例不完全一致，译文按各处原文分别保留，不自行统一。）

<!-- 原 PDF 第 5 页 -->

这些子问题分别在 NL 中得到回答。答案（“水的密度是 $1\,\mathrm{g/cm^3}$”）被转换成 Datalog 语句（`Has_density("water", 1)`），再组合起来，形式化最终答案的真值条件。最后，我们执行该 Datalog 程序，判定一只梨不会沉入水中。

### 3.3 规划

在用户与机器人交互的场景中，给定用户的一项家务任务查询 $Q$，我们希望给出机器人为完成该任务应当采取的动作计划 $A$。例如，在图 3 中，给定用户查询“我把可乐洒在桌子上了，你能把它扔掉，并拿点东西来打扫吗？”，一个可能的计划是“find(coke), pick(coke), find(trash), put(coke), …”。在翻译阶段，LM 把 $Q$ 翻译成 $C$，其中包含 $C_{\mathrm{NL}}$（把 $Q$ 分解为子任务）与 $C_{\mathrm{SL}}$（把子任务表示为 PDDL⁶ 中的符号目标——PDDL 是一种定义并求解经典规划问题的语言）。图 3 展示了这一翻译，$C_{\mathrm{SL}}$ 为蓝色，$C_{\mathrm{NL}}$ 为黑色。最后，我们调用一个 PDDL 规划器作为确定性求解器，在预定义场景下得到实现目标 $C_{\mathrm{SL}}$ 的计划 $A$。

⁶ https://en.wikipedia.org/wiki/Planning_Domain_Definition_Language 。目标（goal）是 PDDL 中的一种特殊构造。

### 3.4 关系推理

给定一个用 NL 写成的关系推理问题 $Q$，我们希望得到字符串值变量形式的答案 $A$。例如，CLUTRR（Sinha et al., 2019）数据集要求从一篇短文推断两个人之间的家庭关系（例如“grandson”，孙子）。短文例如：“[Gabrielle] 开车送她的女儿 [Dorothy] 去医院。[Dorothy] 的儿子 [Vincent] 不久后出现。[Vincent] 与 [Gabrielle] 是什么关系？”（图 3 中为黄色）。在翻译阶段，我们提示 LM 生成由 $C_{\mathrm{NL}}$ 与 $C_{\mathrm{SL}}$ 组成的 $C$。与先前任务类似，$C_{\mathrm{NL}}$ 把 $Q$ 分解为子问题（“[Vincent] 与 [Dorothy] 是什么关系”以及“[Dorothy] 与 [Gabrielle] 是什么关系”），并提供输入摘录作为支持答案的依据（“[Dorothy] 的儿子 [Vincent] 不久后出现”，等等）。$C_{\mathrm{NL}}$ 中的每个子问题在 $C_{\mathrm{SL}}$ 中用一个关系表达式回答，表示所提及实体之间的关系。例如，$\mathrm{relation}(\mathrm{Vincent}, \mathrm{Dorothy}) = \mathrm{son}$ 表示 Vincent 是 Dorothy 的儿子。在问题求解阶段，我们的求解器是一个简单的关系推理引擎，依赖 Zhang et al. (2022) 给出的一组可能家庭关系之间的传递规则，例如 $\mathrm{son}@\mathrm{daughter}=\mathrm{grandson}$（某人女儿的儿子是某人的孙子）。我们的求解器在 $C_{\mathrm{SL}}$ 上递归应用这些规则以导出 $A$，并判定 Vincent 是 Gabrielle 的孙子。

## 4 实验设置

### 4.1 数据集

这里我们概述每个领域使用的评估数据集。我们选取与 Wei et al. (2022) 相同数量（6 到 10 个，取决于任务）的示例来构成少样本提示，提示见我们的代码库。除非另有说明，我们使用官方划分：训练集用于选择示例，验证集用于调提示，测试集用于评估。⁷

⁷ 数据集统计、例子、数据清洗方法、划分、提示构造策略等见附录 E。

**数学应用题（MWP）。** 我们遵循 Wei et al. (2022)，考虑同样的五个 MWP 基准：GSM8K（Cobbe et al., 2021）、SVAMP（Patel et al., 2021）、MultiArith（Roy and Roth, 2015）、ASDiv（Miao et al., 2020）与 AQuA（Ling et al., 2017）。对所有数据集，输入问题都用 NL 表述。AQuA 的答案是一个字符串值的数学表达式，其余数据集的答案是一个或多个整数。除 AQuA 外，所有数据集使用同一套 8-shot 提示。

**多跳 QA。** 我们考虑三个数据集：StrategyQA（Geva et al., 2021），一个开放域问题数据集，回答这些问题需要隐式的多步策略，例如“亚里士多德用过笔记本电脑吗？”涉及回答“1. 亚里士多德生活在什么时候？”“2. 笔记本电脑是何时发明的？”以及“3. #2 是否早于 #1？”；来自 BIG-bench（BIG-Bench collaboration, 2021）的日期理解（Date Understanding），要求模型通过对相对时间段做计算，从上下文推断一个日期；以及来自 BIG-bench 的体育理解（Sports Understanding），要求模型判断一条人工构造的、与体育相关的陈述是合理还是不合理。由于后两个数据集没有训练集，我们遵循 Wei et al. (2022)，从测试集中选取 10 个例子构成提示，其余用于评估。

**规划。** 我们使用 SayCan 数据集（Ahn et al., 2022）。它假设机器人在这样的场景中活动：

<!-- 原 PDF 第 6 页 -->

机器人在厨房中运作，帮助用户做家务，例如“把一罐可乐拿到桌上”。有若干地点和物体可供机器人交互。机器人只能执行固定的一组动作，包括 find、pick 与 put。任务是把 NL 形式的用户查询映射为预定义动作的计划。遵循 Wei et al. (2022)，由于没有提供训练集，我们手工编写 7 个示例。

**关系推理。** 我们使用第 3.4 节所述的 CLUTRR（Sinha et al., 2019）基准。该数据集按到达答案所需的中间步数 $K$ 有多个划分。我们用 $K \in \{2, 3\}$ 的 8 个示例构造提示，并在其余 $K$ 最高到 10 的例子上测试模型。

### 4.2 评估指标

我们以最终答案准确率作为主要指标来评估模型性能。遵循先前工作（Wei et al., 2022; Wang et al., 2022; Chen et al., 2022），对所有答案包含整数的 MWP 数据集（AQuA 除外），正确答案定义为预测与真值都转换成最近整数后的精确匹配；对答案为布尔值的 StrategyQA 与 Sports Understanding，定义为预测与真值都作为布尔变量求值后的精确匹配；对 SayCan，若生成的计划属于真值计划之中，则视为正确；对其余所有数据集，我们依赖预测字符串与真值字符串的精确匹配。此外，我们在附录 D 中评估推理链经人工评定的合理性。

### 4.3 基线

我们把本方法与另外三种少样本提示基线比较，如图 4 所示：由 Brown et al. (2020) 推广的标准提示，其演示只包含问题与答案；CoT（Wei et al., 2022），额外包含一条 NL 推理链；以及从易到难（Least-to-Most，LtM）（Zhou et al., 2022），它用 NL 分解问题，但不涉及 SL。所有提示方法都在两种解码策略下比较：贪心解码，即 LM 从词表中采样最可能的下一个词元（即 temperature = 0.0）；以及自一致性解码（Wang et al., 2022），即 LM 生成多条推理链，并基于对所求答案的多数投票选择最终链条（我们对所有数据集使用 temperature 0.4 与 40 次生成）。⁸ 当某些任务没有报告基线结果，或当我们清洗了测试集时，我们自行复现基线结果。

⁸ 请注意，我们不报告标准提示配合自一致性解码的性能，因为当采样输出数量足够大时，它收敛到贪心解码下的标准提示（Wang et al., 2022）。

### 4.4 语言模型

我们在第 5 节使用 OpenAI Codex（Chen et al., 2021）（code-davinci-002），并在附录 C.3 中用另外四个代码生成 LM 做实验。

## 5 结果

我们在所有数据集上的结果见表 1。以 code-davinci-002 作为翻译器，Faithful CoT 在两种解码策略下，于绝大多数

**图 4：** 一道数学题上来自三个基线与 Faithful CoT（我们的方法）的样例输出。真值答案是 280，只有我们的方法正确算出了答案。

查询：Royce 给房子铺木瓦比 Rob 所需时间的两倍还多 40 分钟。如果 Rob 需要 2 小时，Royce 需要多少分钟？

**Faithful CoT 推理（我们的方法）**，模型输出：

```text
# 为回答这个问题，写一个 Python 程序来回答下列子问题：
# 1. Rob 给房子铺木瓦需要多少分钟？（独立，依据：["如果 Rob 需要 2 小时"]）
minutes_rob = 2 * 60
# 2. Royce 给房子铺木瓦需要多少分钟？（依赖于 1，依据：["Royce 比 Rob 的两倍还多 40 分钟"]）
minutes_royce = minutes_rob * 2 + 40
# 3. 最终答案：Royce 需要多少分钟？（依赖于 2，依据：[]）
answer = minutes_royce
```

Python 解释器：`280`。

**思维链（CoT）提示（Wei et al., 2022）**，模型输出：Royce 比 Rob 的两倍还多 40 分钟。这意味着 Royce 需要 $2 \times 2 + 40 = 80 + 40 = 120$ 分钟。答案是 120。

**标准提示**，模型输出：答案是 4 小时 20 分钟。

**从易到难提示（Zhou et al., 2023）**，模型输出：

要回答这个问题，我们需要知道：

问 1. Rob 需要多少分钟？Rob 需要 2 小时。

问 2. Royce 需要多少分钟？Royce 比 Rob 的两倍还多 40 分钟。

最终答案：Royce 需要多少分钟？Royce 需要 $2 \times 2 + 40 = 84$ 分钟。答案是 84。

（图 4 的版面为多栏示例，正文抽取完整；默认 `find_tables` 只抽出其中碎片，未另编数字。真值 280 与各方法输出 280、120、4 小时 20 分钟、84 均来自该页正文抽取。）

<!-- 原 PDF 第 7 页 -->

数据集与领域上优于所有基线。

**表 1：** 不同提示方法在来自 4 个领域的 10 个推理数据集上的准确率。我们把方法 Faithful CoT 与标准提示（Brown et al., 2020）、CoT（Wei et al., 2022）以及从易到难提示（Zhou et al., 2022）比较，LM 为 code-davinci-002。每种解码策略内的最佳结果在原文中加粗。

贪心解码：

| 方法 | GSM8K | SVAMP | MultiArith | ASDiv | AQuA | SayCan | StrategyQA | Date | Sport | CLUTRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 标准提示 | 19.6 | 69.5 | 43.8 | 72.1 | 31.5 | 82.5 | 63.9 | 51.3 | 71.9 | 42.0 |
| CoT | 63.3 | 77.3 | 96.5 | 80.0 | 42.1 | 86.4 | 72.5 | 59.9 | 98.6 | 48.5 |
| LtM | 38.3 | 80.3 | 74.0 | 76.5 | 40.6 | 77.7 | 72.2 | 76.6 | 99.5 | 47.2 |
| Faithful CoT（我们的） | 72.3 | 83.4 | 98.8 | 80.2 | 47.2 | 89.3 | 63.0 | 81.6 | 99.1 | 58.9 |

自一致性解码：

| 方法 | GSM8K | SVAMP | MultiArith | ASDiv | AQuA | SayCan | StrategyQA | Date | Sport | CLUTRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| CoT | 78.0 | 86.8 | 100.0 | 84.2 | 52.0 | 89.3 | 79.8 | 63.8 | 98.0 | 45.7 |
| LtM | 38.8 | 80.5 | 74.0 | 76.3 | 44.9 | 76.7 | 71.9 | 77.2 | 99.4 | 50.9 |
| Faithful CoT（我们的） | 80.0 | 88.8 | 99.2 | 84.4 | 61.4 | 94.2 | 65.2 | 85.5 | 99.0 | 71.9 |

（表 1 的数字来自该页 `get_text` 按列读出的单元格，并与默认 `find_tables` 的数字一致。领域表头为：数学应用题、规划、多跳 QA、关系。）

在贪心解码下，Faithful CoT 在 10 个数据集中的 8 个上优于所有基线，相对提升在 MWP 上最高达 14.2%，在规划上为 3.4%，在多跳 QA 的日期理解上为 6.5%，在关系推理上则出人意料地达到 21.4%。一般而言，我们在更难的数据集上看到更大的增益。以 MWP 为例：在较简单的数据集上，CoT 已经表现尚可（例如 MultiArith 与 ASDiv，大多数问题只需 1–2 步即可解决），增益较小（0.3% 到 2.4%）；然而，我们在最难的 GSM8K 上看到最大增益（14%），该数据集解题最多需要 8 步。在自一致性解码下，Faithful CoT 仍然在 10 个数据集中的 7 个上表现最好。与贪心解码相比，相对增益在 4 个数据集上增加（AQuA：$12.1\% \rightarrow 18.1\%$，SayCan：$3.4\% \rightarrow 5.5\%$，日期理解：$6.5\% \rightarrow 10.8\%$，CLUTRR：$21.4\% \rightarrow 41.3\%$），但在其余三个 MWP 数据集上下降或保持不变（GSM8K：$9.0\% \rightarrow 2.6\%$，SVAMP：$3.9\% \rightarrow 2.3\%$，ASDiv：$0.2\% \rightarrow 0.2\%$）。

另一方面，我们在两个多跳 QA 数据集 Sports Understanding 与 StrategyQA 上没有看到明确的经验增益。在 Sports Understanding 上，Faithful CoT 与 LtM 都有接近完美的准确率（99 以上），表明该数据集几乎已经饱和。然而在 StrategyQA 上，我们方法的性能仍然远不及基线。为理解原因，我们专门比较 CoT 预测正确而我们的方法失败的例子。如附录 F 的图 11 所示，我们发现最可能的主要原因是 Codex 预训练数据中 Datalog 的稀疏性，因为高达 29% 的错误与语法相关。此外，在提示中加入 Datalog 也会干扰 NL 生成，使 Codex 更难产生相关子问题（17%）、正确检索知识（10%），以及从知识到答案形成有效推理（10%）。另一个潜在原因是任务本身的性质：许多 StrategyQA 问题的难度不在推理，而在知识检索，这使得确定性求解器的优势不那么明显。尽管如此，若在 Datalog 上进一步预训练，我们相信仍有改进空间。

为考察本方法的可推广性，我们还用四个替代 LM 做了实验，并观察到 Faithful CoT 相对基线带来一致增益，如附录 C.3 所示。特别地，使用 GPT-4 时，我们在 7 个数据集上取得新的少样本 SOTA 结果，在五个 MWP 中的四个以及三个多跳 QA 中的两个上达到 95.0 以上的准确率。总体而言，这些结果表明，忠实性在经验上确实能提升性能。

## 6 分析

在本节中，我们对本方法的优劣作广泛分析，以便更好地理解不同组成部分的作用、对设计选择的稳健性、所生成推理链的合理性，以及它仍然容易出错的常见错误模式。这里我们只展示前两个方面；其余见附录 C。除非另有说明，我们从每个领域选择一个数据集（GSM8K、日期理解、SayCan 与 CLUTRR），并使用 code-davinci-002 在贪心解码下的输出。

### 6.1 消融研究

鉴于 Faithful CoT 的强性能，我们现在回答一个自然的问题：提示的每一部分对准确率贡献有多大？我们做消融研究，移除提示的不同部分，观察性能如何变化。除原始提示（“完整”）外，我们测试四种变体，用图 4 的例子说明：

<!-- 原 PDF 第 8 页 -->

**无依据。** 我们移除依据，即 NL 注释中括号里的一切，例如“独立，依据：['有 15 棵树']”。

**无 NL 但保留提示句。** 我们移除所有 NL 注释，只保留“提示句”（nudge）：例如“# 为回答这个问题，我们写一个 Python 程序来回答下列子问题”。

**无 NL。** 我们移除所有 NL 注释。

**无求解器。** 我们不调用外部求解器，而是在每个示例末尾加上“答案：{answer}”，让 LM 自己预测答案。

**图 5：** 消融研究结果：移除提示不同部分后的准确率。详见第 6.1 节。横轴为 GSM8K、Date、SayCan、CLUTRR，纵轴为准确率（0 到 100）。图例为：完整、无依据、无 NL 但保留提示句、无 NL、无求解器。

（图 5 为柱状图。该页正文未给出各柱精确读数；对应数值见表 4，见原 PDF 第 15 页。此处不编造图中读数。）

在 GSM8K、日期理解与 SayCan 上，NL 注释对性能贡献很小，有时甚至略有损害。然而在 CLUTRR 上，它们的作用至关重要，因为排除每一个组成部分（依据、提示句、子问题）都会导致明显的准确率下降。特别地，比较“无 NL 但保留提示句”与“无 NL”，提示句本身带来高达 31.3 个点的显著提升。

外部求解器把问题求解的负担从 LM 上卸下。没有它，准确率在 GSM8K、日期理解与 CLUTRR 上大幅下降（分别下降 50.8、22.9 与 19.4），而在 SayCan 上反而提高 2.9。一个潜在影响因素是 SayCan 可能过于同质，因为它只包含 3 个预定义动作。这会使任务相对容易，使所有模型变体都能达到约 90% 的准确率，从而使求解器变得不必要。另一个潜在原因是不同数据集上最终答案与推理链之间的对应程度：如图 3 所示，SayCan 中的答案是一串动作（例如 find(redbull)），每一步都直接对应推理链中的一步（例如 at redbull trash）。然而，另外三个数据集中的答案只是单个数字或字符串，只能在执行推理链中的全部步骤之后才能导出。因此，后一类任务更需要外部求解器的存在。

### 6.2 对示例的稳健性

我们现在回答下一个问题：示例的选择有多重要？为此，我们总共标注 20 个例子，随机抽取 $k$ 个（7–10 个，取决于数据集）来构造提示，并重复该过程五次。表 2 给出全部六次运行的性能，包括原始运行（来自表 1）。平均准确率接近原始结果（$-1.5$ 到 $+1.2$），在考虑标准差（1.3 到 2.9）之后，除了可以说是最容易的 SayCan 之外，在所有数据集上仍以很大幅度（7 到 17）高于基线。这有力地表明，Faithful CoT 的收益受示例选择的影响很小。

**表 2：** 对示例选择的稳健性。

| 示例 | GSM8K | Date | SayCan | CLUTRR |
| --- | ---: | ---: | ---: | ---: |
| 集合 0（表 1） | 72.3 | 81.6 | 89.3 | 58.9 |
| 集合 1 | 72.6 | 81.3 | 91.3 | 59.0 |
| 集合 2 | 71.1 | 85.0 | 85.4 | 57.2 |
| 集合 3 | 72.3 | 82.5 | 88.3 | 58.0 |
| 集合 4 | 71.2 | 77.4 | 88.3 | 55.5 |
| 集合 5 | 71.5 | 85.0 | 89.3 | 56.0 |
| 均值 | 71.8 | 82.1 | 88.7 | 57.4 |
| 标准差 | 0.6 | 2.8 | 1.9 | 1.5 |

### 6.3 合理性的人工评估

我们的主实验用最终答案准确率作为性能度量，但这并不必然对应推理链的有效性。技术上，模型有时会带着一条无效的推理链偶然得到正确答案。于是我们问：当答案正确时，推理链真正正确的频率有多高？换言之，我们想评估推理链的合理性。

我们在 Prolific 上进行人工评估：给定一条得到正确答案的生成推理链，众包工人选择它是 A）完全正确，或者若不正确，则用 B）NL 不正确和/或 C）SL 不正确来说明原因。他们也可以选择 D）问题有缺陷，以及 E）我感到困惑。⁹

⁹ 人工研究的更多细节见附录 D。

研究结果见图 6（数值结果见附录表 8）。

<!-- 原 PDF 第 9 页 -->

**图 6：** 推理链合理性的人工评估结果。每一列表示人类评估者在各领域/数据集中选择不同答案选项的百分比。图中领域包括多跳 QA 与关系推理等。精确百分比见表 8（原 PDF 第 17 页）。该页图本身未抽出可读的逐柱数字，此处不编造。

对大多数领域，我们看到标注者常常认为推理链完全正确——Sports、SayCan 与 MWP 的正确率在 90% 以上。为更深入了解推理链何时可能“不正确”，我们对三个表现最差的数据集上的用户标注作深入分析——StrategyQA（正确率 66.7%）、Date（正确率 87.9%）与 CLUTRR（正确率 88.0%）。经检查，我们发现标注者会以随任务而异的比率，错误地把一条正确的推理链标为不正确（StrategyQA 为 8.3% 的时间，日期理解为 41.7%，CLUTRR 为 100%）。我们发现，标注者在日期理解上不准确，是因为他们错误地认为生成的代码误用了某个 Python 库（relativedelta），或者他们抱怨存在更好的回答方式。对 CLUTRR，标注者把链条标为不正确，是因为数据集中已知的歧义。例如，某人孩子的祖母未必是其父母，也可能是姻亲父母。

至于其余真正不正确的推理链，我们发现 LM 有时会加入不必要的步骤，或偶然得到正确答案。后者在 StrategyQA 上尤其成问题——由于所有问题都是真/假答案，一条不正确的推理链得到正确答案的情况很常见。例如，LM 把问题“卡拉奇曾是亚历山大大帝成功的一部分吗？”正确地回答为“真”。然而，推理链包含有缺陷的子问题“哪些国家在巴基斯坦？巴基斯坦包括巴基斯坦、阿富汗和印度。”尽管最终答案正确，并且忠实于 LM 的生成，推理链却包含错误知识。

总体而言，当答案正确时，Faithful CoT 在绝大多数情况下确实生成有效的推理链。然而，我们仍然看到模型经由不正确的推理链得到正确答案的例外。尽管这种情况不频繁，它提出了人们何时应当信任 LM 的问题。据我们所知，我们是第一个对 CoT 式推理链的合理性进行系统性人工研究的工作，我们希望未来工作进一步研究并改进本研究所揭示的缺陷。

## 7 结论

我们提出 Faithful CoT，一个把复杂推理分解为翻译与问题求解的框架。它保证推理链是对模型如何得出答案的忠实解释。我们在 4 类复杂推理问题上展示了本方法的有效性：数学应用题、多跳 QA、规划与关系推理。我们的方法在 10 个数据集中的 7 个上取得新的 SOTA 性能，同时还为最终答案提供忠实解释。这些结果给出经验证据：通过保证解释的忠实性来改进模型可解释性，并不以整体性能为代价；事实上，我们看到二者之间存在很强的协同。通过对本方法优劣的全面分析，我们展示了它对示例选择的稳健性、求解器的关键作用，以及它仍然容易出错的常见错误模式。

## 局限性

本研究的一个关键局限是：2023 年 3 月 23 日，OpenAI 停止了 code-davinci-002 的使用。这使部分结果对任何未被授予继续访问该模型权限的团队或研究者而言无法复现。这一停用在我们的研究期间出乎意料。它提出了在学术研究中使用闭源模型的重要问题。

与此同时，本方法的一个方法论局限在于忠实性的范围。目前，我们保证问题求解阶段是忠实的。然而，翻译阶段仍然不透明，也就是说，LM 如何从问题生成推理链，其本身并不可自解释。一般而言，是否有可能改进 LM 生成过程的可解释性，仍然是一个探索不足的问题；近期若干研究已取得有希望的早期进展（Yin and Neubig, 2022; Sarti et al., 2023），或可用于改进翻译阶段的忠实性。

<!-- 原 PDF 第 10 页 -->

最后，推理链中 NL 注释的作用仍需进一步探索。从我们的消融研究来看，就性能而言，是否在推理链中包含 NL 注释，在许多数据集上差别不大，尤其是那些任务并非知识密集型的数据集。尽管如此，就可解释性而言，NL 注释可以使推理链对终端用户更加结构化、更易理解。此外，NL 注释可以成为允许没有编程背景的用户与模型交互并调试模型的界面，我们把这一点留给未来工作。

## 伦理声明

随着生成式大 LM 近期的成功，它们正被用来解决复杂推理问题。当使用 LM 的输出进行推理时，存在一种危险：如果推理看起来真实，那么最终答案或结论也会被认为可靠。正如我们在图 1 与图 7 中所强调的，情况往往并非如此，因为 LM 可能产生一条看起来合理的推理链，但最终答案仍然是错的。本工作朝着使 LM 的使用更可信迈出一步：只使用 LM 来将其推理表达为符号程序，并独立执行该程序。在本工作中，我们在多个领域中确保了推理链相对于最终答案如何产生的忠实性，但必须承认翻译阶段仍然不透明。因此，我们的流水线仍然并非完全可解释。此外，正如我们在第 1 节所强调的，忠实性并不保证正确性，所以我们的方法有时仍会产生错误答案，这可能对依赖它做决策的用户构成风险。

## 致谢

本研究部分基于以下项目的支持：DARPA KAIROS 计划（合同 FA8750-19-2-1004）、DARPA LwLL 计划（合同 FA8750-19-2-0201）、IARPA HIATUS 计划（合同 2022-22072200005）以及 NSF（奖项 1928631）。批准公开分发，分发不受限制。本文所含观点与结论属于作者，不应被解释为必然代表 DARPA、IARPA、NSF 或美国政府的官方政策，无论是明示还是暗示。

我们感谢 OpenAI 在提高 Codex API 速率限制方面的支持。我们也感谢 Jiani Huang、Ziyang Li、Litao Yan、Andrew Head、Mayur Naik 与 Lyle Ungar 的宝贵反馈。


## 参考文献

Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Daniel Ho, Jasmine Hsu, Julian Ibarz, Brian Ichter, Alex Irpan, Eric Jang, Rosario Jauregui Ruano, Kyle Jeffrey, Sally Jesmonth, Nikhil J. Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Kuang-Huei Lee, Sergey Levine, Yao Lu, Linda Luu, Carolina Parada, Peter Pastor, Jornell Quiambao, Kanishka Rao, Jarek Rettinghouse, Diego Reyes, Pierre Sermanet, Nicolas Sievers, Clayton Tan, Alexander Toshev, Vincent Vanhoucke, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Mengyuan Yan, and Andy Zeng. 2022. 按我所能，而非按我所说：将语言锚定到机器人可供性（Do As I Can, Not As I Say: Grounding Language in Robotic Affordances）. ArXiv:2204.01691 [cs].

Yoshua Bengio. 2019. 从系统 1 深度学习到系统 2 深度学习（FROM SYSTEM 1 DEEP LEARNING TO SYSTEM 2 DEEP LEARNING）.

BIG-Bench collaboration. 2021. 超越模仿游戏：测量并外推语言模型的能力（Beyond the Imitation Game: Measuring and extrapolating the capabilities of language models）.

Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel Ziegler, Jeffrey Wu, Clemens Winter, Chris Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. 2020. 语言模型是少样本学习者（Language Models are Few-Shot Learners）. In Advances in Neural Information Processing Systems, volume 33, pages 1877–1901. Curran Associates, Inc.

Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens Winter,

<!-- 原 PDF 第 11 页 -->

Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain, William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Josh Achiam, Vedant Misra, Evan Morikawa, Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder, Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba. 2021. 评估在代码上训练的大语言模型（Evaluating Large Language Models Trained on Code）. ArXiv:2107.03374 [cs].

Wenhu Chen, Xueguang Ma, Xinyi Wang, and William W. Cohen. 2022. 思维程序提示：为数值推理任务将计算与推理解耦（Program of Thoughts Prompting: Disentangling Computation from Reasoning for Numerical Reasoning Tasks）. ArXiv:2211.12588 [cs].

Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John Schulman. 2021. 训练验证器以求解数学应用题（Training Verifiers to Solve Math Word Problems）. ArXiv:2110.14168 [cs].

Luyu Gao, Aman Madaan, Shuyan Zhou, Uri Alon, Pengfei Liu, Yiming Yang, Jamie Callan, and Graham Neubig. 2022. PAL：程序辅助的语言模型（PAL: Program-aided Language Models）. ArXiv:2211.10435 [cs].

Mor Geva, Daniel Khashabi, Elad Segal, Tushar Khot, Dan Roth, and Jonathan Berant. 2021. 亚里士多德用过笔记本电脑吗？一个带有隐式推理策略的问答基准（Did Aristotle Use a Laptop? A Question Answering Benchmark with Implicit Reasoning Strategies）. Transactions of the Association for Computational Linguistics, 9:346–361.

Leilani H. Gilpin, David Bau, Ben Z. Yuan, Ayesha Bajwa, Michael Specter, and Lalana Kagal. 2018. 解释“解释”：机器学习可解释性综述（Explaining Explanations: An Overview of Interpretability of Machine Learning）. In 2018 IEEE 5th International Conference on Data Science and Advanced Analytics (DSAA), pages 80–89.

L. A. Harrington, M. D. Morley, A. Šcedrov, and S. G. Simpson. 1985. Harvey Friedman 关于数学基础的研究（Harvey Friedman’s Research on the Foundations of Mathematics）. Elsevier. Google-Books-ID: 2plPRR4LDxIC.

Bernease Herman. 2019. 模型可解释性中人工评估的希望与危险（The Promise and Peril of Human Evaluation for Model Interpretability）. arXiv:1711.07414 [cs, stat]. ArXiv: 1711.07414.

Alon Jacovi and Yoav Goldberg. 2020. 迈向忠实可解释的 NLP 系统：我们应如何定义并评估忠实性？（Towards faithfully interpretable NLP systems: How should we define and evaluate faithfulness?） In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, pages 4198–4205. Association for Computational Linguistics.

Jaehun Jung, Lianhui Qin, Sean Welleck, Faeze Brahman, Chandra Bhagavatula, Ronan Le Bras, and Yejin Choi. 2022. 产婆术式提示：带递归解释的逻辑一致推理（Maieutic Prompting: Logically Consistent Reasoning with Recursive Explanations）. ArXiv:2205.11822 [cs].

Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa. 2022. 大语言模型是零样本推理者（Large Language Models are Zero-Shot Reasoners）.

Aitor Lewkowycz, Anders Andreassen, David Dohan, Ethan Dyer, Henryk Michalewski, Vinay Ramasesh, Ambrose Slone, Cem Anil, Imanol Schlag, Theo Gutman-Solo, Yuhuai Wu, Behnam Neyshabur, Guy Gur-Ari, and Vedant Misra. 2022. 用语言模型求解定量推理问题（Solving Quantitative Reasoning Problems with Language Models）. ArXiv:2206.14858 [cs].

Yifei Li, Zeqi Lin, Shizhuo Zhang, Qiang Fu, Bei Chen, Jian-Guang Lou, and Weizhu Chen. 2022. 论让语言模型成为更好推理者的进展（On the Advance of Making Language Models Better Reasoners）. ArXiv:2206.02336 [cs].

Wang Ling, Dani Yogatama, Chris Dyer, and Phil Blunsom. 2017. 通过理由生成进行程序归纳：学习求解并解释代数应用题（Program induction by rationale generation: Learning to solve and explain algebraic word problems）. In Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 158–167. Association for Computational Linguistics. ArXiv:1705.04146 [cs].

Shen-yun Miao, Chao-Chun Liang, and Keh-Yih Su. 2020. 一个用于评估和开发英语数学应用题求解器的多样化语料库（A diverse corpus for evaluating and developing English math word problem solvers）. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, pages 975–984, Online. Association for Computational Linguistics.

Maxwell Nye, Anders Johan Andreassen, Guy Gur-Ari, Henryk Michalewski, Jacob Austin, David Bieber, David Dohan, Aitor Lewkowycz, Maarten Bosma, David Luan, Charles Sutton, and Augustus Odena. 2021. 展示你的工作：用于语言模型中间计算的草稿纸（Show Your Work: Scratchpads for Intermediate Computation with Language Models）. ArXiv:2112.00114 [cs].

OpenAI. 2023. GPT-4 技术报告（Gpt-4 technical report）.

Arkil Patel, Satwik Bhattamishra, and Navin Goyal. 2021. NLP 模型真的能求解简单数学应用题吗？（Are NLP models really able to solve simple math word problems?） In Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, pages 2080–2094, Online. Association for Computational Linguistics.

Silviu Pitis, Michael R Zhang, Andrew Wang, and Jimmy Ba. 2023. 面向大语言模型的增强提示集成（Boosted prompt ensembles for large language models）. arXiv preprint arXiv:2304.05970.

Danish Pruthi, Mansi Gupta, Bhuwan Dhingra, Graham Neubig, and Zachary C. Lipton. 2020. 学习用基于注意力的解释进行欺骗（Learning to deceive with attention-based explanations）. In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, pages 4782–4793, Online. Association for Computational Linguistics.

<!-- 原 PDF 第 12 页 -->

Jing Qian, Hong Wang, Zekun Li, Shiyang Li, and Xifeng Yan. 2022. 语言模型在算术与符号归纳上的局限（Limitations of Language Models in Arithmetic and Symbolic Induction）. ArXiv:2208.05051 [cs].

Marco Ribeiro, Sameer Singh, and Carlos Guestrin. 2016. “我为什么应该信任你？”：解释任意分类器的预测（“why should I trust you?”: Explaining the predictions of any classifier）. In Proceedings of the 2016 Conference of the North American Chapter of the Association for Computational Linguistics: Demonstrations, KDD ’16, pages 97–101, New York, NY, USA. Association for Computational Linguistics.

Subhro Roy and Dan Roth. 2015. 求解一般算术应用题（Solving general arithmetic word problems）. In Proceedings of the 2015 Conference on Empirical Methods in Natural Language Processing, pages 1743–1752, Lisbon, Portugal. Association for Computational Linguistics.

Gabriele Sarti, Nils Feldhus, Ludwig Sickert, and Oskar van der Wal. 2023. Inseq：面向序列生成模型的可解释性工具包（Inseq: An interpretability toolkit for sequence generation models）. arXiv preprint arXiv:2302.13942.

Koustuv Sinha, Shagun Sodhani, Jin Dong, Joelle Pineau, and William L. Hamilton. 2019. CLUTRR：从文本进行归纳推理的诊断基准（CLUTRR: A diagnostic benchmark for inductive reasoning from text）. In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP), pages 4506–4515, Hong Kong, China. Association for Computational Linguistics.

Dylan Slack, Sophie Hilgard, Emily Jia, Sameer Singh, and Himabindu Lakkaraju. 2020. 愚弄 LIME 与 SHAP：对事后解释方法的对抗攻击（Fooling LIME and SHAP: Adversarial Attacks on Post hoc Explanation Methods）. In Proceedings of the AAAI/ACM Conference on AI, Ethics, and Society, pages 180–186. Association for Computing Machinery, New York, NY, USA.

Miles Turpin, Julian Michael, Ethan Perez, and Samuel R. Bowman. 2023. 语言模型并不总是说出它们所想的：思维链提示中的不忠实解释（Language Models Don’t Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting）.

Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou. 2022. 自一致性改进语言模型中的思维链推理（Self-Consistency Improves Chain of Thought Reasoning in Language Models）. ArXiv:2203.11171 [cs].

Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed H. Chi, Quoc V. Le, and Denny Zhou. 2022. 思维链提示激发大语言模型中的推理（Chain of Thought Prompting Elicits Reasoning in Large Language Models）.

Kayo Yin and Graham Neubig. 2022. 用对比解释来解释语言模型（Interpreting language models with contrastive explanations）. arXiv preprint arXiv:2202.10419.

Hanlin Zhang, Ziyang Li, Jiani Huang, Mayur Naik, and Eric Xing. 2022. 通过可微符号编程改进语言模型的逻辑推理（Improved logical reasoning of language models via differentiable symbolic programming）. In First Workshop on Pre-training: Perspectives, Pitfalls, and Paths Forward at ICML 2022.

Denny Zhou, Nathanael Schärli, Le Hou, Jason Wei, Nathan Scales, Xuezhi Wang, Dale Schuurmans, Olivier Bousquet, Quoc Le, and Ed Chi. 2022. 从易到难提示使大语言模型能够进行复杂推理（Least-to-Most Prompting Enables Complex Reasoning in Large Language Models）. ArXiv:2205.10625 [cs].


<!-- 原 PDF 第 13 页 -->

## 附录 A 实现细节

在我们的全部实验中，我们通过 beta.openai.com 上提供的 Python API，使用 OpenAI GPT-3（text-davinci-001 与 text-davinci-002）以及 Codex（code-davinci-001 与 code-davinci-002）模型，时间从 2022 年 9 月到 2023 年 1 月。每个例子的推理费用对所有 Codex 模型为 0 美元，因为它们处于有限的 beta 期；对 GPT-3 模型为 0.01 到 0.03 美元，取决于数据集。在每分钟 150,000 个词元的速率限制下，用 Codex 模型对一个例子做推理需要 2–15 秒；在每分钟 250,000 个词元的限制下，用 GPT-3 模型需要 1–8 秒，同样取决于数据集。例如，在包含 1,319 个例子的 GSM8K 测试集上，用 Codex 完成推理需要 3.5 小时，用 GPT-3 需要 2.3 小时。

我们在所有实验中使用以下超参数：

- temperature：贪心解码为 0.0，自一致解码为 0.4；
- max_tokens：1000；
- n：贪心解码为 1，自一致解码为 40；
- frequency_penalty：0；
- presence_penalty：0。

任何未指定的超参数都设为 https://beta.openai.com/docs/api-reference/completions/create 上的默认值。

## 附录 B 扩展结果

在本节中，我们给出未能放入正文的更多结果。

### B.1 不忠实 CoT 输出的例子

图 7 展示 CoT 方法（Wei et al., 2022）在三个数据集上的不忠实输出：GSM8K（MWP）、StrategyQA（多跳 QA）与 SayCan（规划）。请注意，这里我们只展示明显不忠实的模型输出。在其他情形中，推理链与答案之间没有已知的不一致，但这仍然不意味着推理链是忠实解释，因为真值（模型如何预测答案）是未知的。

GSM8K 的例子已在第 1 节解释。在 StrategyQA 的例子中，尽管推理链正确指出蜂鸟的体重大大超过一颗豌豆，答案仍然是“yes”；在 SayCan 的例子中，推理链只提到“去桌子和柜台那里”，但计划中包含不必要的 “pick” 与 “put” 操作。

**图 7：** CoT 提示（Wei et al., 2022）在三个数据集上的不忠实输出例子。答案（绿色）并不能由推理链（蓝色）推出。

**数学应用题（GSM8K）。** 输入：John 打算卖掉他所有的玩具，并用这笔钱买电子游戏。他有 13 套乐高，每套卖 15 美元。最后他以每款 20 美元买了 8 款电子游戏，还剩下 5 美元。他还剩多少套乐高？

CoT 输出：他一开始有 13 套乐高。他以每套 15 美元卖掉它们。因此卖掉后他一定得到了 $13 \times \$15 = \$195$。他用这笔钱以每款 20 美元买了 8 款电子游戏。这意味着他在电子游戏上花了 $8 \times \$20 = \$160$。他还剩 5 美元，所以他总共一定曾经有 $\$195 + \$5 = \$200$。答案是 0。

**多跳 QA（StrategyQA）。** 输入：问：一只蜂鸟能否与放着一颗豌豆的天平平衡？

CoT 输出：答：蜂鸟是世界上最小的鸟。蜂鸟的平均体重约为 2 克。一颗豌豆约重 0.1 克。因此，一只蜂鸟能够与放着一颗豌豆的天平平衡。所以答案是 yes。

**规划（SayCan）。** 推理链：去桌子和柜台那里。

CoT 输出：用户要求我去桌子和柜台那里，我将按这个顺序去做。1. find(table)，2. pick(table)，3. find(counter)，4. put(counter)，5. done()。

Wei et al. (2022) 声称，CoT “为观察模型行为提供一个可解释的窗口，提示它可能如何得出某个特定答案，并提供机会来调试推理路径在何处出错”。正如我们在第 1 节所指出的，由于 CoT 不保证忠实性，模型得出答案的方式可能与推理链所展示的截然不同。此外，用户仍然很难调试模型：即便他们手工改正推理链并让模型重新生成答案，答案仍可能是错的，因为推理链与答案之间没有因果关系。

### B.2 与少样本 SOTA 的比较

我们在表 3 中把 Faithful CoT 的结果与已发表的少样本 SOTA 比较。Faithful CoT 的结果取自我们实验的五个 LM 中，在每个数据集上表现最好的那个 LM（见第 C.3 节）。SOTA 结果来自以下来源：

- GSM8K：OpenAI (2023)；
- MultiArith、ASDiv、StrategyQA：Wang et al. (2022)；
- SVAMP：Chen et al. (2022)；
- AQuA：Pitis et al. (2023)；

<!-- 原 PDF 第 14 页 -->

**表 3：** 现有少样本 SOTA 结果与最优 Faithful CoT 结果的比较（表现最好的 LM：SayCan 与 CLUTRR 为 code-davinci-002，其余数据集为 gpt-4）。SOTA 来源见附录 B.2。

| 方法 | GSM8K | SVAMP | MultiArith | ASDiv | AQuA | SayCan | StrategyQA | Date | Sport | CLUTRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 少样本 SOTA | 92.0 | 89.1 | 100.0 | 87.8 | 76.4 | 88.3 | 81.6 | 76.2 | 98.5 | 50.9 |
| Faithful CoT（我们的） | 95.0 | 95.4 | 99.2 | 95.6 | 73.6 | 93.2 | 65.2 | 95.8 | 99.3 | 71.9 |
| $\delta_{\mathrm{acc}}$ | +3.0 | +6.3 | −0.8 | +7.8 | −2.8 | +4.9 | −16.4 | +19.6 | +0.8 | +21.0 |

- SayCan、Sports Understanding：（Wei et al., 2022）；
- 日期理解：（Gao et al., 2022）；
- CLUTRR：我们对 LtM 提示的实现（Zhou et al., 2022）（尚无已有工作报告 $K$ 最高到 10 的 CLUTRR 少样本性能）。

使用 Codex 与 GPT-4，Faithful CoT 在四个领域的 10 个数据集中的 7 个上取得新的 SOTA 性能，其中 6 个准确率达到 95.0 以上。

**图 8：** 我们的方法与两项同期工作在 10 个推理数据集上的准确率：思维程序（Program of Thoughts，PoT）（Chen et al., 2022）与程序辅助语言模型（Program-Aided Language Models，PAL）（Gao et al., 2022）。横轴数据集为 GSM8K、SVAMP、MultiArith、ASDiv、AQuA、SayCan、StrategyQA、date、sports、CLUTRR；纵轴为准确率 0.0 到 100.0。图例为 PAL/PoT 与 Faithful CoT。

（图 8 为柱状图。该页正文与默认 `find_tables` 均未抽出各柱的精确读数，见原 PDF 第 14 页。此处不编造图中数字。下文只转述正文给出的定性比较。）

### B.3 与同期工作的经验比较

两项同期工作，思维程序（PoT）（Chen et al., 2022）与程序辅助语言模型（PAL）（Gao et al., 2022），在我们的工作之后三个月内于 arXiv 上公布。本质上，它们都生成 Python 程序，即仅含 SL 的推理链，来得出答案。我们的方法与它们的主要差别在于额外的结构化 NL 注释，它把原始问题分解为更简单、相互依赖的子问题。

除第 2 节强调的质性差别之外，我们在主评估所用的同一组 10 个数据集上与它们做经验性能比较。由于两篇论文都只处理了数学推理与符号推理任务，我们用第 6.1 节消融研究中的 “noNL” 提示来重新实现它们的方法。比较以 code-davinci-002 为底层 LM，并使用贪心解码。

如图 8 所示，在 10 个数据集中的 6 个上（包括大多数 MWP 数据集、SayCan 与日期理解），PAL/PoT 与 Faithful CoT 的准确率非常接近（差异小于 2.0）。在 AQuA 上，PAL/PoT 明显更好。在其余三个数据集（StrategyQA、Sports Understanding 与 CLUTRR）上，Faithful CoT 合理地优于 PAL/PoT。这可能表明，当任务需要大量外部知识（例如 StrategyQA 与 Sports Understanding），或者当 SL 在 LM 预训练数据中不常见（例如 Datalog，或我们自定义的关系表达式）时，我们的方法具有优势。

最后请注意，我们方法的关键贡献在于可解释性。尽管加入结构化 NL 注释有时并不带来性能差别，它确实使推理链对用户更易理解。此外，它甚至可能使没有编程背景的用户能够调试模型，只需与 NL 子问题交互（例如增加、删除或编辑一个子问题）。这一点值得未来进一步探索。

## 附录 C 扩展分析

### C.1 消融研究

表 4 给出第 6.1 节消融研究的完整结果。

### C.2 对提示措辞的稳健性

我们研究方法对提示设计中细微差别的敏感度。我们试验三种提示变体：1. 随机打乱独立子问题/推理步骤的顺序；2. 更改变量名；3. 更改提示句（例如，从 “# To answer this

<!-- 原 PDF 第 15 页 -->

question, write a Python program to answer the following subquestions” 改为 “# To solve this question, we answer each of the following subquestions with a Python program”）。

**表 4：** 与图 5 配套的消融研究结果。我们报告移除提示不同部分后的准确率。

| 提示 | GSM8K | Date | SayCan | CLUTRR |
| --- | ---: | ---: | ---: | ---: |
| 完整 | 72.3 | 81.6 | 89.3 | 58.9 |
| 无依据 | 75.4 | 83.0 | — | 51.8 |
| 无 NL 但保留提示句 | 73.5 | 80.2 | — | 39.6 |
| 无 NL | 72.8 | 79.7 | 90.3 | 9.3 |
| 无求解器 | 21.5 | 57.9 | 90.3 | 40.9 |

我们在第 6 节所用的 4 个数据集上（在适用时），于贪心解码下重新评估全部三种变体。表 5 给出结果。总体而言，性能相当稳定，在全部四个数据集上始终高于各基线。

**表 5：** 对提示措辞的稳健性。

| 提示 | GSM8K | Date | SayCan | CLUTRR |
| --- | ---: | ---: | ---: | ---: |
| 原始 | 72.3 | 81.6 | 89.3 | 58.9 |
| 变体 1 | 69.1 | 84.4 | 88.3 | — |
| 变体 2 | 70.3 | 81.6 | 90.3 | 56.2 |
| 变体 3 | 70.2 | 80.5 | 87.4 | 55.9 |
| 均值 | 70.5 | 82.0 | 88.8 | 57.0 |
| 标准差 | 1.3 | 1.7 | 1.3 | 1.7 |

### C.3 模型敏感性

在本节中，我们想回答这个问题：LM 的选择有多重要？第 5 节的全部结果都是用 code-davinci-002 得到的。这里，我们考察使用四个替代的代码生成模型作为翻译器的效果：code-davinci-001、text-davinci-002、text-davinci-003、gpt-4。我们在五个 MWP 数据集上，用上述每一个 LM，把我们的方法与三个基线比较，解码策略为贪心解码。

如表 6 所示，无论底层 LM 是哪一个，Faithful CoT 都在绝大多数数据集上一致地优于所有基线，并在其余数据集上与最佳方法非常接近（差异小于 2.0）。平均而言，相对各 LM 下基线中表现最好的方法，它的相对准确率增益分别为 16.1%、11.0%、9.4% 与 4.6%。这表明，尽管绝对性能随 LM 而变化，Faithful CoT 带来的准确率增益相对一致。

值得注意的是，以 GPT-4 为底层 LM 时，Faithful CoT 在 5 个 MWP 数据集中的 4 个上达到 95.0 以上的准确率，在其中三个（GSM8K、SVAMP 与 ASDiv）上大幅超过先前的少样本 SOTA。

### C.4 施加约束

由于我们生成的推理链包含结构化成分（例如依赖图），另一个自然的问题是：对生成施加某些约束是否有帮助？我们以 MWP 数据集为案例，考察三种此类约束的效果：

**图的有效性。** 依赖图必须是有向循环图（Directed Cyclic Graph，DAG）。例如，不允许一个子问题依赖它自己。

**无过度依赖。** 代码不能依赖其对应子问题未曾提到的任何变量。例如在图 4 中，既然问 5 说“依赖于 4”，那么对应代码就不应使用变量 eggs_in_dozen，因为它不是问 4 的输出。

**无不足依赖。** 代码必须依赖其对应子问题所提到的全部变量。例如在同一例子中，既然问 5 说“依赖于 4”，那么对应代码就必须使用变量 eggs_in_dozen。

我们在自一致解码下考察对生成施加约束的效果。从我们的原始结果（没有任何约束）出发，我们每次加入一组不同的约束，并在表 7 中报告准确率变化。单独来看，图有效性约束对性能几乎没有改变，但另外两个约束导致跨数据集更不稳定的变化——大多是下降。加入两个或更多约束会在几乎所有情形中进一步降低性能，MultiArith（最容易的数据集）除外，这揭示了准确率与满足约束之间的权衡。它也表明，我们现有结果中有一部分生成（1.0% 到 8.9%）并不满足全部约束。然而，为了让用户更好地控制模型并与之交互，以性能为代价来强制某些约束（例如图的有效性）可能仍然值得。

## 附录 D 人工评估细节

我们在 Prolific 上聘请众包工人，评估那些得到正确答案的、由模型生成的推理链的正确性。我们采样

<!-- 原 PDF 第 16 页 -->

每个领域 100 条由 code-davinci-002 以贪心解码策略生成的推理链，其中每组 100 条包含该领域内所有数据集的等量样本。我们进一步要求标注者具有其所标注数据集之编程语言的编码经验（MWP/CLUTRR/Sports/Date 为 Python，StrategyQA 为 Scala，因为 Prolific 上没有 Datalog 这一选项）。除多跳 QA 外，每个领域只有一份问卷（在多跳 QA 中，鉴于各数据集性质不同，我们为 StrategyQA、Date 与 Sports 分别设置问卷）。此外，在 Prolific 上无法确保标注者了解 PPDL。为确保 SayCan 的标注质量，作者们自己标注了这个数据集。

**图 9：** 我们为 CLUTRR 问卷设计的标注界面示例。（界面截图本身未能以文字抽出，见原 PDF 第 16 页。）

**标注过程。** 每个领域的 100 个问题各由至少三名标注者标注。每位标注者被分配 10 个问题。图 9 是我们问卷界面的截图。问卷开始时，向标注者给出一条正确推理链、一条 NL 不正确的推理链，以及一条 SL 不正确的推理链的例子。这些例子与每份问卷中推理链的领域相匹配。作为注意力与理解检查，我们要求标注者标注一个他们刚刚见过的例子。如果标注者未能通过这一问题，他们会被送到问卷末尾，其回答被滤除。我们还手工滤除所有垃圾标注者（以同一回答反复出现，或在 3 分钟内完成问卷的标注者）。

**表 6：** 每种底层 LM 下，不同提示方法在 5 个 MWP 推理数据集上的准确率。

LM：code-davinci-001

| 方法 | GSM8K | SVAMP | MultiArith | ASDiv | AQuA | 平均 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 标准提示 | 5.2 | 28.7 | 8.6 | 38.5 | 22.8 | 20.8 |
| CoT | 14.7 | 41.2 | 57.2 | 50.4 | 22.4 | 37.2 |
| LtM | 9.8 | 44.9 | 18.5 | 46.6 | 20.5 | 28.1 |
| Faithful CoT（我们的） | 27.4 | 50.8 | 63.3 | 53.7 | 20.9 | 43.2 |

LM：text-davinci-002

| 方法 | GSM8K | SVAMP | MultiArith | ASDiv | AQuA | 平均 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 标准提示 | 15.4 | 65.2 | 34.1 | 64.8 | 24.0 | 40.7 |
| CoT | 47.2 | 68.0 | 91.1 | 69.9 | 40.6 | 63.4 |
| LtM | 32.9 | 73.8 | 68.3 | 70.9 | 34.6 | 56.1 |
| Faithful CoT（我们的） | 62.7 | 80.0 | 92.8 | 75.4 | 41.3 | 70.4 |

LM：text-davinci-003

| 方法 | GSM8K | SVAMP | MultiArith | ASDiv | AQuA | 平均 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 标准提示 | 16.9 | 69.4 | 38.8 | 59.1 | 29.5 | 42.7 |
| CoT | 59.6 | 79.5 | 95.0 | 69.1 | 46.9 | 70.0 |
| LtM | 34.6 | 79.5 | 73.7 | 70.0 | 44.5 | 60.5 |
| Faithful CoT（我们的） | 71.7 | 85.1 | 94.5 | 80.7 | 50.8 | 76.6 |

LM：gpt-4

| 方法 | GSM8K | SVAMP | MultiArith | ASDiv | AQuA | 平均 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 标准提示 | 46.9 | 88.4 | 98.7 | 70.2 | 50.4 | 70.9 |
| CoT | 64.9 | 80.0 | 94.0 | 71.6 | 75.2 | 77.1 |
| LtM | 91.8 | 92.9 | 98.3 | 86.7 | 72.0 | 87.5 |
| Faithful CoT（我们的） | 95.0 | 95.4 | 98.5 | 95.6 | 73.6 | 91.6 |

**表 7：** 对生成施加不同约束后的准确率变化。“无”这一行给出没有任何约束时的原始性能（来自表 1）。下面每一行加入一组不同的约束：G 表示“图的有效性”，O 表示“无过度依赖”，U 表示“无不足依赖”。结果是自一致解码下的全部 MWP 数据集。

| 约束 | GSM8K | SVAMP | MultiArith | ASDiv | AQuA |
| --- | ---: | ---: | ---: | ---: | ---: |
| 无 | 80.0 | 88.8 | 99.2 | 84.4 | 61.4 |
| + G | 0.0 | 0.0 | 0.0 | −0.1 | −0.8 |
| + O | −0.9 | −0.1 | −0.1 | +0.4 | −3.9 |
| + U | −1.0 | −3.6 | 0.0 | −1.2 | +1.2 |
| + GO | −1.7 | −0.4 | −0.1 | +0.2 | −3.9 |
| + GU | −1.0 | −3.7 | 0.0 | −1.2 | +0.8 |
| + OU | −4.0 | −5.4 | −0.1 | −2.6 | −4.3 |
| + GOU | −5.0 | −5.9 | −0.1 | −3.2 | −5.5 |


<!-- 原 PDF 第 17 页 -->

问卷完成后，我们计算标注者一致性，然后取每条推理链的多数标签作为分析中的最终标签。我们的标注者群体包括 100 名标注者，平均年龄 25 岁，平均年收入 4 万美元。87.9% 的标注者为男性，56% 拥有四年制大学学位。标注者报酬为每小时 16 美元，平均每题 2 分钟。整个研究花费 280 美元。CLUTRR 问卷的样例说明见补充材料。

**表 8：** 推理链正确性人工评估的数值结果，与图 6 配套。每一行表示人类评估者在各领域/数据集中选择不同答案选项的百分比（0–100），以及标注者间一致性。

| 领域 | 正确 | NL 不正确 | SL 不正确 | 问题有缺陷 | 困惑 | 一致性 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| MWP | 92.0 | 3.0 | 2.0 | 2.0 | 1.0 | 0.790 |
| 规划 | 94.0 | 3.9 | 2.1 | 0.0 | 0.0 | 0.947 |
| StrategyQA | 66.7 | 30.3 | 3.0 | 0.0 | 0.0 | 0.455 |
| Date | 87.9 | 6.1 | 6.1 | 0.0 | 0.0 | 0.788 |
| Sports | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.899 |
| 关系 | 88.0 | 6.0 | 0.0 | 5.0 | 1.0 | 0.683 |

## 附录 E 数据集细节

### E.1 统计

我们在表 9 中给出数据集细节，包括统计量、提示中使用的少样本示例数量，以及输入与输出示例。

特别地，我们注意到在基线之一 Wei et al. (2022) 中，所报告的提示示例数量在正文（10）与附录（6）之间不一致。为确保公平比较，我们对表 1 中的结果用 10 个示例重跑了该基线，这也是我们自己的方法所使用的数量。

### E.2 网址与许可

我们沿用 Wei et al. (2022) 的数据集发行版本：

**数学应用题**

- GSM8K（Cobbe et al., 2021）：https://github.com/openai/grade-school-math ，MIT 许可：https://github.com/openai/grade-school-math/blob/master/LICENSE 。
- SVAMP（Patel et al., 2021）：https://github.com/arkilpatel/SVAMP ，MIT 许可：https://github.com/arkilpatel/SVAMP/blob/main/LICENSE 。
- MultiArith（Roy and Roth, 2015），许可：CC BY 4.0。
- ASDiv（Miao et al., 2020）：https://github.com/chaochun/nlu-asdiv-dataset 。
- AQuA（Ling et al., 2017）：https://github.com/deepmind/AQuA ，许可：https://github.com/deepmind/AQuA/blob/master/LICENSE 。

**多跳 QA**

- StrategyQA（Geva et al., 2021）：我们使用来自（BIG-Bench collaboration, 2021）的开放域设定（仅问题集合）：https://github.com/google/BIG-bench/tree/main/bigbench/benchmark_tasks/strategyqa 。
- 来自 BIG-Bench（BIG-Bench collaboration, 2021）的日期理解与体育理解：Apache License v.2：https://github.com/google/BIG-bench/blob/main/LICENSE 。

**规划**

- SayCan（Ahn et al., 2022）：SayCan 数据集可在 https://say-can.github.io/ 获取，许可为 CC BY 4.0。

**关系推理**

- CLUTRR（Sinha et al., 2019）：https://github.com/facebookresearch/clutrr ，许可：https://github.com/facebookresearch/clutrr/blob/main/

<!-- 原 PDF 第 18 页 -->

LICENSE。我们获取公开分发的版本，见 https://drive.google.com/file/d/1SEq_e1IVCDDzsBIBhoUQ5pOVH5kxRoZF/view ，具体为 data_089907f8 这一划分。

我们仅将上述全部数据集用于研究目的，与其预期用途一致。

**表 9：** 用于评估的数据集。“# Shot” 表示提示中的少样本示例数（遵循 Wei et al. (2022)），“# Test” 表示测试例子数。

| 领域 | 数据集 | # Shot | # Test | 示例 |
| --- | --- | ---: | ---: | --- |
| 数学应用题 | GSM8K | 8 | 1,319 | 问：Natalia 在四月把发夹卖给了她的 48 个朋友，然后在五月卖掉的数量是四月的一半。Natalia 在四月和五月一共卖了多少个发夹？答：72 |
| 数学应用题 | SVAMP | 8 | 1,000 | 问：每包 DVD 售价 76 美元。如果每包有 25 美元折扣，买每包要付多少钱？答：51 |
| 数学应用题 | MultiArith | 8 | 600 | 问：万圣节，Debby 和她姐姐把收到的糖果合在一起。Debby 有 32 块糖果，她姐姐有 42 块。如果第一晚他们吃了 35 块，还剩多少块？答：39 |
| 数学应用题 | ASDiv | 8 | 2,096 | 问：篮子里有七个红苹果和两个绿苹果。篮子里有多少个苹果？答：9 |
| 数学应用题 | AQuA | 8 | 254 | 问：一辆汽车以每小时 60 公里的速度用 20 小时完成一段旅程。若同一距离要在 10 小时内走完，汽车需要提高多少速度？答：“120 kmph” |
| 多跳 QA | StrategyQA | 6 | 2,290 | 问：亚里士多德用过笔记本电脑吗？答：False |
| 多跳 QA | 日期理解 | 10 | 359 | 问：昨天是 2021 年 4 月 30 日。明天的日期是什么，格式为 MM/DD/YYYY？答：“05/02/2021” |
| 多跳 QA | 体育理解 | 10 | 977 | 问：下面这句话是否合理：“Lebron James hit the turnaround jumper”？答：True |
| 规划 | SayCan | 7 | 103 | 问：能给我拿一杯含咖啡因的饮料吗？答：“1.find(redbull) 2.pick(redbull) 3.find(user) 4.put(redbull) 5.done().” |
| 关系推理 | CLUTRR | 8 | 1,042 | 问：[Carlos] 是 [Clarence] 的兄弟。[Carlos] 和他的妹妹 [Annie] 去购物。[Annie] 问她的妈妈 [Valerie] 是否想要什么，但 [Valerie] 说不用。[Valerie] 与 [Clarence] 是什么关系？答：“mother” |

### E.3 数据清洗

我们在 ASDiv、日期理解、体育理解与 SayCan 上做了手工清洗，因为我们发现若干标注问题。在实验中，我们在清洗后的测试集上重跑所有基线。这些数据放在我们的代码库中，以协助未来研究。

具体而言，我们对每个数据集的清洗如下：

**ASDiv：** 我们从 Wei et al. (2022) 使用的测试集出发，该测试集移除了所有浮点值与字符串值答案的问题。然而，在他们发布的版本中，我们注意到对答案中含有多于一个数值的问题，答案抽取步骤有误（例如“X 的宽和长是多少？”，答案由两个值组成）。在他们的实现中，只把第一个值抽取为真值答案，再与模型输出比较。这可能人为抬高最终准确率。为修正这一点，我们把答案中的全部数值抽取为一个集合，并将模型输出与之比较。

**日期理解：** 我们发现测试集中有若干错误答案。例如，对于问题“Jane 与 John 于 1958 年 1 月 2 日结婚。今天是他们的 5 周年纪念日。今天的日期是什么，格式为 MM/DD/YYYY？”，所给答案是 “01/02/1961”，而正确答案应为 “01/02/1963”。我们手工改正这些答案，所得测试集的例子数与原始测试集相同。

**体育理解：** 我们注意到体育理解数据集有几处歧义。例如，在许多运动中跑出界是违规的。短语 “Domantas Sabonis ran out of bounds” 被标为不合理，然而 Domantas Sabonis 是篮球运动员，而篮球运动员确实可以在

<!-- 原 PDF 第 19 页 -->

球场上跑出界。我们移除了 8 个带有此类基于动作之歧义的问题。此外，自该数据集发布以来，若干新运动员成名，其姓名与数据集中提到的人相同。例如，问题 “Chris Paul struck out the side” 是不合理的，因为所指的 “Chris Paul” 是一位著名篮球运动员。然而 “Chris Paul” 也是一位新的 MLB 棒球运动员的名字，在这种情况下该陈述是合理的。我们移除了 5 个带有此类基于姓名之歧义的问题。

**SayCan：** 我们发现测试集中有若干问题：（1）环境设置（例如物体列表、地点列表，以及每个物体的初始位置）并非对所有例子都相同；（2）真值答案的标注常常不完整（即对于“访问所有地点”这样的给定任务，就访问地点的顺序而言存在许多可能的计划，但标注并未全部包含）；（3）某些查询中的描述有歧义，例如在 “Could you get me something refreshing?” 中，不清楚哪些饮料算“清爽”。对这些问题，我们尽可能补全标注，并滤除其余问题。所得测试集包含原始 120 个例子中的 103 个。

### E.4 数据集划分

如第 4.1 节所述，我们尽可能使用官方划分：训练集用于选择示例，验证集用于调提示，测试集用于评估。在这些划分可用的情况下，我们对每个数据集采用如下策略：

**GSM8K：** 它只有训练集和测试集。我们从训练集中随机抽样 1,000 个例子构成验证集。

**其他 MWP 数据集：** 对 AQuA，我们使用官方的训练/验证/测试划分。对其余数据集，只使用测试集，因为它们与 GSM8K 使用同一提示。

**日期理解与体育理解：** 它们只有测试集。我们遵循 Wei et al. (2022)，从测试集中选取相同数量的例子构成少样本提示，并用剩余例子作为新的测试集。

**SayCan：** 遵循 Wei et al. (2022)，由于没有提供训练集，我们手工编写 7 个少样本示例。我们在上一小节所述的清洗后测试集上评估模型。

**CLUTRR：** 该数据集被分成多个折。有一个训练折，$K \in \{2, 3\}$（其中 $K$ 是到达答案所需的中间步数），并且对从 2 到 10 的每个 $K$ 有一个测试折。我们用来自训练折的示例构造少样本提示，并在所有测试折的拼接上测试我们的方法。

## 附录 F 错误分析

为进一步考察我们的方法仍然在何处失败，我们检查模型在四个数据集上各自预测的 100 个错误¹⁰，并手工标注错误类别。

¹⁰ 为鼓励样本多样性，我们用 text-davinci-002 嵌入全部错误，并用谱聚类对嵌入聚类。这产生约 70 个大小不同的簇，我们从中用重要性采样收集 100 个样本。

### F.1 GSM8K

**图 10：** GSM8K 的错误分析。错误类别的详细描述见附录 F.1。

（图 10 为错误类型分布图。各类型占比由下文给出，此处不另编图中读数。）

如图 10 所示，我们把 GSM8K 上的错误分为 6 类，按频率由高到低排列：

**错误子问题（49%）：** LM 产生一个错误的 NL 子问题，最终导致不正确的答案。虽然这是我们样本中的多数错误类型，但值得注意的是，在典型的人在回路协作中，这些错误很容易修正。即使用户不熟悉编程，他们也可以检查 NL 子问题，并可能仅通过删除或编辑一个错误子问题来纠正模型错误。

**错误代码（24%）：** NL 子问题是正确的，但代码未能正确回答该子问题。例如，代码使用了一个先前未曾定义的变量。

**语义理解错误（12%）：** LM 错误地解释查询中的某些语义细节。这是最复杂也最有意思的错误类别。例如，考虑下面这个问题：

如果 Martin 每天早餐都吃 Cheerios，他每周会减掉 1.25 磅。如果他每天早餐都吃甜甜圈，他每周会增重 1.75 磅。5 周结束时，两种早餐选择之间他的体重差将是多少？

<!-- 原 PDF 第 20 页 -->

**表 10：** 附录 F.1 中该问题的生成代码，作为“语义理解错误”的例子。

```text
# 1. 如果 Martin 每天早餐都吃 Cheerios，他每周会减掉多少磅？（独立，依据：["他每周会减掉 1.25 磅"]）
pounds_lost_cheerios = 1.25
# 2. 如果 Martin 每天早餐都吃甜甜圈，他每周会增重多少磅？（独立，依据：["他每周会增重 1.75 磅"]）
pounds_gained_donuts = 1.75
# 3. 5 周里有多少周？（独立，依据：["外部知识：一周有 7 天"]）
weeks_in_5_weeks = 5
# 4. 如果 Martin 每天早餐都吃 Cheerios，5 周内他会减掉多少磅？（依赖于 1 和 3，依据：[]）
pounds_lost_cheerios_5_weeks = pounds_lost_cheerios * weeks_in_5_weeks
# 5. 如果 Martin 每天早餐都吃甜甜圈，5 周内他会增重多少磅？（依赖于 2 和 3，依据：[]）
pounds_gained_donuts_5_weeks = pounds_gained_donuts * weeks_in_5_weeks
# 6. 5 周结束时，两种早餐选择之间他的体重差将是多少？（依赖于 4 和 5，依据：[]）
difference_5_weeks = pounds_gained_donuts_5_weeks - pounds_lost_cheerios_5_weeks
# 7. 最终答案：5 周结束时，两种早餐选择之间他的体重差将是多少？（依赖于 6，依据：[]）
answer = difference_5_weeks
```

如表 10 所示，生成的代码没有给“减掉的磅数”与“增加的磅数”赋予相反的极性（符号）。对该类别中的其他例子，我们注意到诸如漏掉“一对某物里面有 2 件”、当“两年前”作为虚拟语气出现时漏减 2，等等。一般而言，修正这些错误所需要的不止是在提示中提供更多例子。

**生成截断（7%）：** 生成中途停止，主要是因为 LM 一遍又一遍地产生相同的步骤。这些错误可以在后处理中轻易检测，并可能通过重新提示 LM 来修正。

**错误金标（5%）：** 我们发现 5 个（在我们的 100 个之中）例子是金标中真正的标注错误。

**缺失子问题（3%）：** LM 漏掉了推理链其余部分得以成立所需的一个相关子问题。这些错误也有可能通过人在回路交互来修正，用户可以把一个子问题插入推理链。

### F.2 StrategyQA

如第 5 节所述，图 11 展示 StrategyQA 上一个 70 个实例样本的错误类型分布。我们专门比较 CoT 的预测正确而我们的预测错误的情形。

**图 11：** StrategyQA 的错误分析。错误类别的详细描述见第 F.2 节。

（图 11 为错误类型分布图。各类型占比由下文给出，此处不另编图中读数。）

错误类型有 8 种，从最频繁到最不频繁：

**语法（29%）：** 这些是导致无效 Datalog 程序的语法相关错误。例如，LM 重新定义一个先前已经声明的关系，使用无效的字符串比较运算，在答案定义中生成一个无根据的变量，等等。若在 Datalog 上进一步预训练，我们相信 Codex 能够在合理程度上克服这些错误。

**无限循环（24%）：** LM 生成了一个
<!-- 原 PDF 第 21 页 -->

无限循环的子问题，这些子问题往往相当哲学化。例如，对于问题“土豆原产于欧洲大陆吗？”，LM 生成了一列 40 个子问题（若不被词元上限截断，可能更多）：

1. 土豆原产于哪里？土豆原产于安第斯山脉。
2. 安第斯山脉在哪个大陆？安第斯山脉在南美洲。
3. 南美洲在哪个大陆？南美洲在美洲。
4. 美洲在哪个大陆？美洲在西半球。
5. 西半球在哪个半球？西半球在地球上。
6. 地球在哪个大陆？地球在太阳系。
……
11. 宇宙在哪个大陆？宇宙在 Multiverse。
12. Multiverse 在哪个大陆？Multiverse 在 Omniverse。
13. Omniverse 在哪个大陆？Omniverse 在 Metaverse。
14. Metaverse 在哪个大陆？Metaverse 在 Hyperverse。
……
39. Quattuordecaverse 在哪个大陆？Quattuordecaverse 在 Quindeciverse。
40. Quindeciverse 在哪个大陆？

我们注意到，如果提示不包含 Datalog 代码而只有 NL 子问题，这类错误也会发生，但少得多。

**错误子问题（17%）：** LM 生成一个与原问题无关的子问题。例如，给定问题“给素食者的吐司是否会用人造黄油代替黄油？”，生成的一个子问题是“素食者与严格素食者之间有什么区别？”，这对得出最终答案没有帮助。

**错误推理（10%）：** 子问题是正确的，但从检索到的事实到最终答案的推理有问题。例如，为回答问题“独奏钢琴家需要指挥吗？”，模型正确地生成了相关子问题及其各自的答案：

1. 独奏钢琴家的定义是什么？独奏钢琴家是独自表演的钢琴家。
2. 指挥的定义是什么？指挥是领导管弦乐队的人。
3. 管弦乐队的定义是什么？管弦乐队是包含弦乐、铜管、木管和打击乐器的大型器乐合奏。

但在导出最终答案时，推理是错的：“现在，我们导出最终答案：独奏钢琴家需要指挥吗？仅当独奏钢琴家不是指挥时，答案才为是。”

**错误知识（10%）：** LM 未能检索到回答子问题的正确知识。例如，给定原问题“新墨西哥州最大的城市是否也被称为 Yootó？”，模型正确地生成子问题“新墨西哥州最大的城市是什么？”（答案：Albuquerque）以及“Albuquerque 是否也被称为 Yootó？”。然而，在回答第二个子问题时，它检索到一条错误知识（“Albuquerque 也被称为 Yootó。”，而实际上应被称为 Yootó 的是 “Santa Fe”）。

**答案定义（6%）：** 在我们的提示中，我们总是以“答案为是，仅当……”的格式导出答案，其后是一条 Datalog 规则，包含要使答案为真所应满足的条件。然而，LM 有时把它生成为“答案为否，仅当……”，从而输出相反的答案。

**知识表示（3%）：** NL 中检索到的知识是正确的，但它在 Datalog 中的表示是错的。例如，对于知识“The Lucy Show 与 JAG（电视剧）不是同一部电视剧”，模型把它表示如下：

```text
.decl Same_TV_series(TV_series1:symbol, TV_series2:symbol)
Same_TV_series("The Lucy Show", "JAG (TV series)").
```

这实际上表示相反的意思（它们是同一部）。

**未知（1%）：** 有非常小的一部分错误（70 个中的 1 个），我们不确定

<!-- 原 PDF 第 22 页 -->

其原因。具体而言，我们期望求解器输出 True，但它却输出 False。

### F.3 日期理解

**图 12：** 日期理解的错误分析。错误类别的详细描述见附录 F.3。

（图 12 为错误类型分布图。正文没有给出该图各类的百分比，见原 PDF 第 22 页。此处不编造图中数字。）

与 GSM8K 不同，在 359 个测试例子中我们只有 69 个错误，因此我们把它们全部标注，如图 12 所示。日期理解的错误类别与 GSM8K 相似，只是在样本中我们没有看到任何生成错误，但我们看到一些措辞有歧义的问题，使得金标答案与预测答案根据解释都可以是正确的。

### F.4 SayCan

**图 13：** SayCan 的错误分析。错误类别的详细描述见第 F.4 节。

（图 13 为错误类型分布图。下文给出两类占比。）

由于 SayCan 只有 120 个测试例子，而 Faithful CoT 产生 7 个错误，我们把这 7 个全部标注，如图 13 所示。这 7 个例子可以分为两类：

**额外子目标（64%）：** 模型在分解原任务时生成了不必要的子目标，使规划器走偏。请求“把墨西哥辣椒薯片从柜台上清走”说明了这一点：

```text
(:goal
(and
(not (at jalapeno-chips counter))
(not (at jalapeno-chips table))
(not (at jalapeno-chips trash))
(not (at jalapeno-chips bowl))
(not (at jalapeno-chips user))
)
)
```

**错误物体（36%）：** 这里模型在目标中生成了错误的物体或物体类型。例如，“我先前打开了一罐百事可乐。你会怎样给我拿一罐打开的？”这样的请求会失败，因为模型生成的动作用的是水而不是百事可乐。

### F.5 CLUTRR

**图 14：** CLUTRR 的错误分析。错误类别的详细描述见第 F.5 节。

（图 14 为错误类型分布图。各类占比由下文给出。）

对 CLUTRR，我们按 $K$（其金标推理链中的步数）把所有错误情形分组，作为问题复杂度的代理，并对这些组做重要性采样以选取 100 个例子。对这些例子的标注揭示出 5 个错误类别，如图 14 所示：

**关系颠倒（41%）：** 这是错误中的大多数。这些错误由问题中行为者的方向性关系被颠倒引起，即当答案分别是 “daughter” 或 “uncle” 时，预测成 “mother” 或 “nephew”。

**错误关系（30%）：** 这里模型抽取的关系不正确（甚至不是其逆关系）。例如，对于子问题“[Donald] 与 [Jason] 是什么关系？”，依据被正确识别为 “[Jason] is father of their father”，模型却产生 $\mathrm{relation}(\mathrm{Donald}, \mathrm{Jason}) = \mathrm{son}$，而正确关系应为 “grandson”。

**不存在的关系（4%）：** 模型幻觉出一个不存在的关系（例如用 “adopted” 来表示

<!-- 原 PDF 第 23 页 -->

daughter）。

**错误路径（12%）：** 这里，模型没有生成一条从问题中的目标实体 A 到目标实体 B 的正确推理路径。

**错误金标（13%）：** 这些是 CLUTRR 数据集中的标注错误。在一个例子中，对于句子 “[Gloria] asked her mother [Laura] if she could go outside and play with her friends.”，标注说 Laura 是 Gloria 的祖母。

## 附录 G 提示

由于篇幅限制，我们在这里为每个数据集展示提示中的一个示例。完整提示见我们的代码库。

在所有 MWP 数据集中，我们对 AQuA 的提示与其余数据集不同，因为答案是多项选择格式，而不是整数。为产生多项选择答案，我们采取两步方法：首先以与其他数学数据集相同的方式产生一个数值答案。然后，我们再增加一步，再次提示语言模型生成哪个答案选项最接近先前产生的数值答案，从而把数值答案转换成一个答案选项。这一两步提示的一个示例见表 11。

<!-- 原 PDF 第 24 页 -->

**表 11：** 我们为 AQuA 准备的提示中的一个示例。

AQuA 示例

第一步：答案预测

```text
# 问题：在 600 公里的飞行中，一架飞机因恶劣天气而减速。这次行程的平均速度降低了 200 公里/小时，飞行时间增加了 30 分钟。飞行时长是：
# 答案选项：['A)1 hour', 'B)2 hours', 'C)3 hours', 'D)4 hours', 'E)5 hours']
# 写 Python 代码来解决下列问题。把结果存为一个名为 'answer' 的变量。
# 1. 飞行时长是多少？（独立，依据：["飞行时长是"]）
duration = Symbol('duration', positive=True)
# 2. 飞行延误是多少？（独立，依据：["飞行时间增加了 30 分钟"]）
delay = 30 / 60
# 3. 总飞行距离是多少？（独立，依据：["在 600 公里的飞行中"]）
total_distance = 600
# 4. 原来的速度是多少？（依赖于 1 和 3，依据：["外部知识：速度是距离除以时间"]）
original_speed = total_distance / duration
# 5. 降低后的速度是多少？（依赖于 1、2 和 3，依据：[]）
reduced_speed = total_distance / (duration + delay)
# 6. 如果原来的速度比降低后的速度快 200 公里/小时，飞行时长是多少？（依赖于 4、5 和 1，依据：[]）
solution = solve_it(original_speed - reduced_speed - 200, duration)
answer = solution[duration]
```

第二步：多项选择转换

```text
# 问题：在 600 公里的飞行中，一架飞机因恶劣天气而减速。这次行程的平均速度降低了 200 公里/小时，飞行时间增加了 30 分钟。飞行时长是：
# 答案选项：['A)1 hour', 'B)2 hours', 'C)3 hours', 'D)4 hours', 'E)5 hours']
# 预测：1.00000000000000
# 最接近的选项：A
```

**表 12：** 我们为 GSM8K、SVAMP、MultiArith 与 ASDiv 准备的提示中的一个示例。

```text
# 问：小树林里有 15 棵树。树林工人今天将在小树林里种树。他们完成后，将有 21 棵树。树林工人今天种了多少棵树？
# 为回答这个问题，写一个 Python 程序来回答下列子问题：
# 1. 一开始有多少棵树？（独立，依据：["有 15 棵树"]）
trees_begin = 15
# 2. 最后有多少棵树？（独立，依据：["将有 21 棵树"]）
trees_end = 21
# 3. 树林工人今天种了多少棵树？（依赖于 1 和 2，依据：[]）
trees_today = trees_end - trees_begin
# 4. 最终答案：树林工人今天种了多少棵树？（依赖于 3，依据：[]）
answer = trees_today
```

**表 13：** 我们为 StrategyQA 准备的提示中的一个示例。

```text
// 问：一只梨会沉入水中吗？
// 为回答这个问题，我们回答下列子问题：
// 1. 一只梨的密度是多少？
// 一只梨的密度大约是 0.6g/cm3。
// 2. 水的密度是多少？
// 水的密度是 1g/cm3。
// 然后，我们用 Datalog 表示这些答案：
// 1. 一只梨的密度大约是 0.6g/cm3。
.decl Has_density(Object:symbol, Density:float)
Has_density("pear", 0.6).
// 2. 水的密度是 1g/cm3。
Has_density("water", 1).
// 现在，我们导出最终答案：一只梨会沉入水中吗？
// 仅当梨的密度大于水的密度时，答案才为是。
.decl Answer()
Answer() :- Has_density("pear", density1), Has_density("water", density2), density1 > density2.
.output Answer
```

<!-- 原 PDF 第 25 页 -->

**表 14：** 我们为日期理解准备的提示中的一个示例。

```text
# 问：昨天是 2021 年 4 月 30 日。明天的日期是什么，格式为 MM/DD/YYYY？
# 为回答这个问题，我们写一个程序来回答下列子问题：
# 导入相关包
from datetime import date, time, datetime
from dateutil.relativedelta import relativedelta
# 1. 昨天的日期是什么？（独立，依据：["昨天是 2021 年 4 月 30 日"]）
date_yesterday = date(2021,4,30)
# 2. 今天的日期是什么？（依赖于 1，依据：["昨天是 2021 年 4 月 30 日"]）
date_today = date_yesterday + relativedelta(days=1)
# 3. 明天的日期是什么？（依赖于 2，依据：[]）
date_tomorrow = date_today + relativedelta(days=1)
# 4. 最终答案：明天的日期是什么，格式为 MM/DD/YYYY？（依赖于 3，依据：[]）
answer = date_tomorrow.strftime("%m/%d/%Y")
```

**表 15：** 我们为体育理解准备的提示中的一个示例。

```text
# 问：下面这句话是否合理？Sam Darnold passed the puck
# 为回答这个问题，写一个 Python 程序来回答下列子问题：
# 1. Sam Darnold 是哪项运动的运动员？（独立，依据：["Sam Darnold 是 NFL 四分卫", "NFL 是 National Football League"]）
player_sport = "football"
# 2. 短语 "passed the puck" 意味着在进行哪项运动？（独立，依据：["运动员在冰球中传冰球"]）
playing_sport = "hockey"
# 3. 下面这句话是否合理？Sam Darnold passed the puck（依赖于 1 和 2，依据：["Sam Darnold 是 NFL 四分卫", "NFL 是 National Football League", "运动员在冰球中传冰球"]）
plausibility = (player_sport == playing_sport)
# 4. 下面这句话是否合理？Sam Darnold passed the puck（依赖于 3，依据：[]）
answer = int(plausibility)
```

**表 16：** 我们为 SayCan 准备的提示中的一个示例。

```text
用户查询：给我拿点不甜的东西吃。
PDDL 中的目标：
(:goal
; 我需要找一份零食
(exists (?s - snack)
; 它必须满足下列条件
(and
; 零食必须不甜
(not (is-sweet ?s))
; 把它带给用户
(at ?s user)
)
)
)
```

**表 17：** 我们为 CLUTRR 准备的提示中的一个示例。

```text
# 上下文：[Jason] 总是在外孙女 [Guillermina] 来访时为她计划一些很棒的冒险。因此，自然地，当 [Myrna] 告诉她的女儿 [Guillermina] 他们将去拜访 [Jason] 时，她几乎无法抑制自己。
# 问题：[Jason] 与 [Myrna] 是什么关系？
# 为回答这个问题，我们写一个程序来回答下列子问题：
# 1. [Jason] 与 [Guillermina] 是什么关系？（独立，依据："[Jason] 总是在外孙女 [Guillermina] 来访时为她计划一些很棒的冒险。"）
relation(Jason, Guillermina) = grandfather
# 2. [Guillermina] 与 [Myrna] 是什么关系？（独立，依据："因此，自然地，当 [Myrna] 告诉她的女儿 [Guillermina] 他们将去拜访 [Jason] 时，她几乎无法抑制自己。"）
relation(Guillermina, Myrna) = daughter
# 3. 最终答案：[Jason] 与 [Myrna] 是什么关系？（依赖于 1、2）
relation(Jason, Myrna) = relation(Jason, Guillermina) @ relation(Guillermina, Myrna)
```

<!-- 译完 -->
