> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

原文件名：Atil_nondeterminism_arXiv2408.04667.pdf

原文标题：Non-Determinism of “Deterministic” LLM Settings

作者：Berk Atil、Sarp Aykent、Alexa Chittams、Lisheng Fu、Rebecca J. Passonneau、Evan Radcliffe、Guru Rajan Rajagopal、Adam Sloan、Tomasz Tudrej、Ferhan Ture、Zhe Wu、Lixinyu Xu、Breck Baldwin。Atil 与 Passonneau 属 Penn State University，其余属 Comcast AI Technologies。文中注明 Atil 在 Comcast AI Technologies 实习期间完成该工作。通信邮箱为 {bka5352,rjp49}@psu.edu 与 breckbaldwin@gmail.com。

场合 / arXiv：页眉为 Preprint. Under review.；arXiv:2408.04667v5 [cs.CL]，2025 年 4 月 2 日。

## 摘要

从业者经常发现：同一输入、按理应确定性的设置下，大模型输出仍会变。这种不稳定有多普遍、对结果影响多大，作者认为此前没有被系统测量。他们把五款 LLM 配成确定性设置，在八个常见任务上各跑 10 次，同时覆盖 zero-shot 和 few-shot。自然出现的各次运行之间，准确率波动最高到 15%；若把最好可能成绩和最差可能成绩拉开，差距最高到 70%。没有一款模型能在所有任务上给出可重复的准确率，更做不到输出字符串逐次相同。作者把初步结果拿给内部人员看之后得到的说法是：输入缓冲区里混放数据，可能正是高效使用算力所需要的，因此这种非确定性短期内不会消失。

为了把观察量化，他们定义两组一致性指标：TARr@N 是 N 次运行里原始输出的 total agreement rate，TARa@N 是解析出答案之后的 total agreement rate。代码和数据公开在 https://github.com/breckbaldwin/llm-stability 。

## 1 Introduction

LLM 已经用在问答、多种推理和代码生成上，也进入医疗信息获取、法律、财务规划、制造优化这类高风险场景，可靠性与可信因此受到更多关注。基准集的价值在于用客观指标说明“买到的是什么”，但如果同一次配置下多次运行结果不稳，这些数字就难以当真。作者认为文献还没充分处理的一点是：在被假定为确定性的设置下，用户无法控制输出方差。他们在多款高性能模型上观察到相当大的波动，并认为这和稳健工程的预期差得远。

温度、top-k、top-p 和 repetition penalty 都会明显影响表现。top-k 与 top-p 按概率缩小采样空间，温度则改写词表上的概率分布：温度高时分布变平，接近 0 时模型应当更确定。许多平台用户因此默认 temperature=0 就是确定性输出。作者把“温度已经是 0、输出仍然变”称为 instability，并在脚注里说明，后文把 stability / instability 与 determinism / non-determinism 互换使用。训练过程本身的不确定性已经为人知，但受成本和时间限制，基准成绩通常只报一次；若同一次训练、同一输入在 temperature=0 时仍有明显方差，而不报告置信区间，基准的有效性会被削弱。本文盯的就是这后一种来源。实验任务来自 MMLU 和 BIG-Bench Hard（BBH）。Figure 1 显示模型并不确定，而且不稳定程度随模型、设置和任务变化，因此足以影响模型排名。

贡献列了五条：用 TARr@N 和 TARa@N 同时刻画答案准确率波动和输出词跨度波动；在从 BBH 与 MMLU 随机抽出的 8 个任务上量化不稳定；比较 zero-shot 与 few-shot，few-shot 沿用标准设置，BBH 为 3-shot、MMLU 为 5-shot；分析不稳定与准确率、输入长度、输出长度的相关；并提供运行数据和源代码。贡献列表的脚注写的是，若论文被接收再公布下载地址。全文结构依次为 Introduction、Related Work、Controlling LLM Determinism、Datasets、Methods、Experiments、Results、Discussion、Conclusion。

## 2 Related Work

已有鲁棒性研究多半看输入被做了细小改动之后模型如何变。本文关心的是输入和配置都不变时，回答是否还会变。Biderman 等人（2024）给出 LLM 评测工具包和可复现性的做法，但没有处理 instability。Song 等人（2024）分析了温度、采样策略、repetition penalty 和对齐算法对表现的影响，并认为评测基准应计入输出方差；他们用的温度是 1，正好引入了本文想压到最低的那种变异。Ouyang 等人（2025）只对 ChatGPT 一个模型、代码生成一类任务、并在不同温度下做了类似分析。Holtzman 等人（2020）提到文本生成的自由度会让同一输入产生不同输出，但没有讨论哪些参数在驱动这种行为。

作者据此认为，在输入相同、配置同为 zero-shot 或 few-shot、并且超参被设到尽可能确定的条件下，还没有工作系统测量 LLM 的 instability。这一节没有给出新的实验数字。
