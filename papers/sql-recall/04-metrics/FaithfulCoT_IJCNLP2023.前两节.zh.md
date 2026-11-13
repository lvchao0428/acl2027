> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

原文件名：FaithfulCoT_IJCNLP2023.pdf

原文标题：Faithful Chain-of-Thought Reasoning

作者：Qing Lyu、Shreya Havaldar、Adam Stein、Li Zhang、Delip Rao、Eric Wong、Marianna Apidianaki、Chris Callison-Burch，均属 University of Pennsylvania。Lyu、Havaldar、Stein 为共同一作。邮箱为 {lyuqing, shreyah, steinad, zharry, exwong, marapi, ccb}@seas.upenn.edu 与 deliprao@gmail.com。

场合：Proceedings of the 13th International Joint Conference on Natural Language Processing and the 3rd Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics (Volume 1: Long Papers)，页 305–329，2023 年 11 月 1–4 日。©2023 Association for Computational Linguistics。

## 摘要

Chain-of-Thought（CoT）能抬高语言模型在复杂推理上的表现，但生成的推理链未必反映模型真正如何得到答案，也就是未必 faithful。Faithful CoT 把推理拆成两段：Translation 用语言模型把自然语言查询译成符号推理链，Problem Solving 用确定性求解器从这条链算出答案。这样，推理链就是最终答案的忠实解释。

除了可解释性，经验表现也更好：在 4 个领域的 10 个基准里，有 9 个超过标准 CoT。相对准确率提升为数学应用题（MWP）6.3%、Planning 3.4%、多跳问答 5.5%、Relational Inference 21.4%。配上 GPT-4 和 Codex，在 7 个数据集上达到新的 few-shot 最好成绩，其中 6 个准确率在 95.0 以上。代码、数据和提示在 https://github.com/veronica320/Faithful-COT 。

## 1 Introduction

复杂推理长期是语言模型的弱点，直到 CoT 用少量上下文示例让模型连同答案写出推理链，成绩才明显上来。Wei 等人还声称这扇窗能看见模型行为，但这些链是否忠实反映预测背后的推理过程并不清楚。标准 CoT 不保证忠实，甚至会被系统性地破坏：最终答案不必从链里推出来，模型可以“谎报”自己的推理。Figure 1 用 GSM8K 上的一条 CoT 说明这一点。题目问 John 卖掉全部乐高之后还剩多少套：他有 13 套，每套 15 美元，后来买了 8 个电子游戏、每个 20 美元，还剩 5 美元。生成的链算出 13×15=195、8×20=160，再把 195+5 说成一共 200 美元，然后写 The answer is 0。这个 0 在链里没有出现，也不从前面的金额推出来。高风险场景里，这种不忠实的解释如果看起来还很像那么回事，会让人以为模型能自我解释，例如法律从业者因此过度信任带有隐含偏见的再犯预测器。

Faithful CoT 让答案变成对推理链的确定性执行结果。Figure 2 把任务分成 Translation 和 Problem Solving。Translation 阶段，语言模型把查询译成自然语言和符号语言交错的推理链：自然语言把原问题拆成相互依赖的更小子问题，每个子问题再用任务相关的符号语言处理，例如 Python、Datalog 或 Planning Domain Definition Language（PDDL）。Problem Solving 阶段由确定性求解器执行这条链，例如 Python 或 Datalog 解释器，或 PDDL 规划器。作者保证的是求解阶段如何从链得到答案可以被忠实解释，并在脚注里写明：生成这条链的 Translation 阶段本身并不声称可解释。可解释也不等于正确，方法会把做对和做错的过程都露出来；经验上它仍然提高了正确率。

评测覆盖 MWP、Planning、多跳问答和 Relational Inference 四个领域的 10 个数据集，相对三种已有基线、在不同语言模型和解码策略下都有稳定提升。用 Codex 时，10 个数据集里 9 个超过 vanilla CoT，相对准确率增益与摘要相同：MWP 6.3%、Planning 3.4%、多跳问答 5.5%、Relational Inference 21.4%。用 GPT-4 时，在 7 个数据集上创下新的 few-shot 最好成绩，其中 6 个准确率达到 95.0 以上。贡献分成三点：推理链把人能读的自然语言注释和可执行的符号程序交织在一起，从而忠实解释答案从何而来；符号语言和外部求解器可以更换，因此能超出算术和简单符号推理；并分析了跨模型的泛化、对示例和提示措辞的稳健性、求解器的关键作用、推理链的 plausibility，以及仍然常见的错误类型。

## 2 Related Work

可解释性里的 faithfulness（也称 fidelity 或 reliability）要求解释准确代表模型得出该预测的推理过程。与之相对的 plausibility（也称 persuasiveness 或 understandability）只问这条解释对人类有多令人信服。放到 CoT 上，忠实的链要反映模型如何走到最终答案，看起来合理、连贯的链则只是 plausible。标准 CoT 用纯自然语言生成推理链，常常看起来合理，但答案不必因果地跟随这条链，所以不保证忠实。脚注区分了另一套用法：自然语言生成里的 faithfulness 是生成文本相对于明确源文本是否忠实，地面真值是透明的；可解释性里要对照的是模型内部推理，地面真值通常未知。

CoT 风格的提示给定复杂问题 Q，让模型生成推理链 C 和答案 A，提示里放若干 (Q, C, A) 示例。这样预训练模型（文中举 GPT-3）解未见问题的准确率会明显高于不含 C 的标准提示。作者把已有方法分成三类。all-at-once 把 C 和 A 当成一段连续字符串一次生成，中间没有依赖或约束，例子是 Scratchpad、标准 CoT，以及 “Let’s think step by step”。ensemble-based 为了避开一次生成的局部最优，抽样多组 (C, A)，再用多数投票等策略选答案，例子是 Self-Consistent CoT、Minerva 和 DIVERSE，差别主要在投票粒度和底层模型。modularized 把问题拆开再逐个解决；Least-to-Most 的问题分解和本文接近，但链仍然全是自然语言，因此仍没有忠实性保证。

与本文同时的 Chen 等人和 Gao 等人用生成 Python 程序（只有符号语言的推理链）来得到答案。第 2 节标出的差别是：本文由可解释性驱动，对方由性能驱动；本文的链里有结构化的自然语言分解，没有编程背景的人也能看懂并可能与系统交互；对方只用 Python，且只做数学和简单符号推理，本文则把 Planning、多跳问答和 Relational Inference 也改写成符号表示，用同一套框架处理多种符号语言；本文的分析更全，尤其包含对推理链正确性的人工评估。经验对比放在 Appendix B.3。这一节没有另给实验数字。
