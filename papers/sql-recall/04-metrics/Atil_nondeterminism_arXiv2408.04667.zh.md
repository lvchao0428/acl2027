# “确定性” LLM 设定的非确定性

- 原文件名：Atil_nondeterminism_arXiv2408.04667.pdf
- 原标题：Non-Determinism of “Deterministic” LLM Settings
- 中文标题：“确定性” LLM 设定的非确定性
- 作者：Berk Atil（1Penn State University；本工作完成于在 Comcast AI Technologies 的实习期间）、Sarp Aykent（2Comcast AI Technologies）、Alexa Chittams（2）、Lisheng Fu（2）、Rebecca J. Passonneau（1）、Evan Radcliffe（2）、Guru Rajan Rajagopal（2）、Adam Sloan（2）、Tomasz Tudrej（2）、Ferhan Ture（2）、Zhe Wu（2）、Lixinyu Xu（2）、Breck Baldwin（2）
- 会议或 arXiv：页眉为 Preprint. Under review.；arXiv:2408.04667v5 [cs.CL] 2 Apr 2025
- 通信：{bka5352,rjp49}@psu.edu；breckbaldwin@gmail.com

<!-- 原 PDF 第 1 页 -->

## 摘要

大语言模型（LLM）的实践者普遍注意到：在预期为确定性的设定下，相同输入的输出仍可能变化。然而，据我们所知，这种现象有多普遍、以及对结果有何影响，尚未被系统研究。我们考察五款被配置为确定性的 LLM，把它们用于八项常见任务，在零样本和少样本设定下各跑 10 次。我们看到，在自然出现的多次运行之间，准确率变化最高达 15%；最好可能性能与最差可能性能之间的差距最高达 70%。事实上，没有一款 LLM 能在全部任务上持续给出可重复的准确率，更谈不上输出字符串完全相同。与内部人士分享初步结果后发现，非确定性或许对高效使用计算资源是必要的：输入缓冲区里的数据被混在一起处理，因此这个问题短期内不会消失。为了更好地量化我们的观察，我们引入聚焦于量化确定性的指标：TARr@N，即 N 次运行上原始输出的总一致率；以及 TARa@N，即解析出的答案的总一致率。代码与数据公开于 https://github.com/breckbaldwin/llm-stability 。

## 1 引言

大语言模型（LLM）在许多类型的 NLP 或与 NLP 相关的任务上表现良好，包括问答（Robinson & Wingate, 2023）、多种推理（Qiao et al., 2023）、代码生成（Jiang et al., 2024b）等等。鉴于它们的通用性，以及它们被广泛用于多样、高利害的社会功能——例如医学中的信息收集（Shool et al., 2025）或法律（Niklaus et al., 2024）、财务规划（de Zarz`a i Cubero et al., 2024；原 PDF 第 1 页抽取串，重音符号乱码）、制造优化（Du et al., 2025）等——人们越来越关注可靠性（例如分布外行为（Liu et al., 2024; Du et al., 2022）），以及其他可信赖性方面（Shridhar et al., 2024; Chen & Mueller, 2024）。LLM 领域整体上值得称道的一个维度是广泛使用基准数据集：你知道自己是在对照一项客观指标做购买决策。然而，如果 LLM 的结果在多次运行之间不稳定，这类基准的价值是什么？可靠性的一个方面，据我们所知在文献中尚未被充分讨论，那就是：在被假定为确定性的设定下，用户无法控制 LLM 输出在不同 LLM 和平台之间的方差。我们表明，在假定的确定性设定下，一组高性能 LLM 在等价输入的多次运行之间存在令人警惕的变化程度。我们的发现提示：在一个人们期望稳健工程的领域里，不确定性实在太多。

除训练过程和数据之外，温度、top-k、top-p 和重复惩罚等超参数会显著影响模型性能（Wang et al., 2023）。

【脚注】Berk Atil 在 Comcast AI Technologies 实习期间完成这项工作。

<!-- 原 PDF 第 2 页 -->

**图 1 见原 PDF。** 图 1：每个模型在 10 次运行中最大准确率与最小准确率的百分比差。共 5 个模型、8 项任务，含零样本与少样本设定。

Top-k 和 top-p 根据概率缩小采样空间，而温度修改词表上的概率分布（Wang et al., 2020; 2023）。温度高时，分布变平；然而当它更接近 0 时，模型应当更确定。许多 LLM 平台的用户期望：当 temperature=0 时，模型性能是确定的。虽然许多其他用户可能在这一设定下观察到一定程度的非确定性，对这一方差几乎没有量化。我们把这种尽管温度为零、输出仍然有方差的行为称为不稳定性。【脚注 1】

尽管神经网络不同训练运行之间的不确定性是已知的，在基准数据集上衡量 LLM 性能时，报告单一结果已经成为标准做法（Hendrycks et al., 2021; Suzgun et al., 2023; Wang et al., 2024; Gema et al., 2024; Rein et al., 2023），可能是由于成本和计算时间的限制。然而，如果相同训练运行之间的输出存在显著方差，这会降低基准的有效性，因为不确定性的度量（例如置信区间）往往并不包括在内。这里我们考察不确定性的另一个来源：同一个已训练模型、在相同输入上、当 temperature=0 时的性能方差。

在本工作中，我们分析不同模型家族在两个常见基准的任务上的不稳定性：大规模多任务语言理解（MMLU）（Hendrycks et al., 2021）和 BIG-Bench Hard（BBH）（Suzgun et al., 2023）。图 1 表明模型并不是确定的，并且不稳定程度随模型、设定和任务而变化。因此，性能不稳定无疑会影响模型的排名性能。我们的具体贡献包括：

- 两个指标，TARr@N（N 次运行上原始数据的总一致率）和 TARa@N（N 次运行上解析答案的总一致率），用于刻画 LLM 不稳定性，以捕捉答案准确率和输出词跨度中的变异。
- 对从两个常见基准 BBH 和 MMLU 中随机选出的 8 项任务，量化 LLM 不稳定性。
- 跨设定的比较，包括零样本和少样本（BBH 为 3，MMLU 为 5，与标准设定一致）。
- 不稳定性与准确率、输入长度和输出长度的相关分析。
- 运行数据与源代码。【脚注 2】

我们的系统研究按如下各节组织：引言、相关工作、控制 LLM 确定性、数据集、方法、实验、结果、讨论和结论。

【脚注 1】本文中，稳定性/不稳定性与确定性/非确定性互换使用。

【脚注 2】若论文被接收，将提供下载 URL。摘要中另给出公开仓库 https://github.com/breckbaldwin/llm-stability 。

<!-- 原 PDF 第 3 页 -->

## 2 相关工作

已有工作研究机器学习（ML）模型在输入发生细微变化时的稳健性（Sehwag et al., 2019; Freiesleben & Grote, 2023; Hancox-Li, 2020; Rauber et al., 2017）。然而，我们关心的是：当输入中的一切都相同时，响应的变化。Biderman 等人（2024）为 LLM 引入一套标准评估工具包，并提出可复现性的最佳实践；然而不稳定性并未被讨论。提到不稳定性的工作包括 Song 等人（2024），它分析温度、采样策略、重复惩罚和对齐算法对性能的影响。虽然该工作发现 LLM 的输出有一些方差，评估基准应当加以考虑，但他们使用的温度为 1，从而引入了我们的研究试图最小化的变异性。Ouyang 等人（2025）对单一模型 ChatGPT 做了类似的不稳定性分析，在单一类型的任务（代码生成）上变化温度。最后，Holtzman 等人（2020）提到文本生成中的自由度可能导致相同输入得到不同输出，但他们没有讨论影响这一行为的参数。据我们所知，没有工作在给定相同输入和配置（零样本与少样本）、并使用最大限度确定性的超参数时，系统研究 LLM 的不稳定性。

## 3 控制 LLM 的确定性

确定性是一个重要却常常被忽视的挑战，各平台的实践并不一致。温度是关键参数，0 是最确定的值，1 是最不确定的值。式 (1) 给出词 $i$ 的概率，其中 $T$ 是温度，$y_i$ 是 LLM 的 logit。

$$
\frac{e^{y_i / T}}{\sum_{j=1}^{N} e^{y_j / T}}
\tag{1}
$$

当 $T$ 设为 0 时，给定相同提示，LLM 在理论上应当产生相同输出。提高 $T$ 可以使输出多样化。我们确认，其他可能相关的超参数，例如 top-p（概率之和达到 $p$ 的最小词元集合），对确定性几乎没有影响。

## 4 数据集

为确保对不稳定性的考察涵盖多样的自然语言处理（NLP）任务，我们转向两个广泛使用的多项选择基准：Beyond the Imitation Game Benchmark Hard（BBH）（Suzgun et al., 2023），含来自数学、常识推理和其他领域的 27 项多样任务；Measuring Massive Multitask Language Understanding（MMLU）（Hendrycks et al., 2021），含横跨人文学科、社会科学和 STEM 领域的 57 项任务。为了在多样性与计算资源之间取得平衡，我们从每个基准中随机选择四个子任务。表 1 列出任务、样例数和多项选择选项数。

## 5 方法

为考察不稳定性，也就是零温度设定的非确定性，我们在未经微调的模型上做实验，采用零样本和少样本提示（不用思维链（CoT）（Wei et al., 2022））。关于少样本的样例数，我们使用标准设定：BBH 任务为 3-shot，MMLU 任务为 5-shot。我们把温度设为 0，top-p 设为 1，并固定种子。我们使用相同的计算基础设施、输入和配置。

<!-- 原 PDF 第 4 页 -->

**表 1：来自 BBH 和 MMLU 的八项任务，含简短描述、样例数和答案选项数。** 默认 `find_tables` 把各行挤进同一单元格；下表按 `get_text` 的逐行文本还原。描述栏中的 identical 译为“与任务名相同”。

| 任务 | 描述 | 规模 | 选项数 |
| --- | --- | --- | --- |
| BBH: navigation | 路径是否在起点结束 | 250 | 2 |
| BBH: ruin names | 对乐队名或电影名做幽默改写 | 250 | 4 |
| BBH: geometric shapes | 给定 SVG 格式下的形状 | 250 | 10 |
| BBH: logical deduct. 3 objects | 在约束下给出 3 个物体的顺序 | 250 | 3 |
| MMLU: h. s. Europ. hist. | 与任务名相同 | 165 | 4 |
| MMLU: college math | 与任务名相同 | 100 | 4 |
| MMLU: prof. accounting | 与任务名相同 | 282 | 4 |
| MMLU: public rel. | 媒介理论、危机管理等 | 110 | 4 |

**图 2 见原 PDF。** 图 2：college math 上 20 次相同运行的准确率，temperature=0，top-p=1。中位数为蓝色，均值为黑色，虚线为 5% 与 95% 分位数。

### 5.1 模型

我们从不同家族、不同规模中选择五款表现靠前的模型：GPT-3.5 Turbo（Brown et al., 2020）、GPT-4o（OpenAI et al., 2024）、Llama-3-70B-Instruct（Meta, 2024）、Llama-3-8B-Instruct（Meta, 2024）和 Mixtral-8x7B-Instruct（Jiang et al., 2024a）。

### 5.2 指标

为量化不稳定性，我们收集同一条件（模型 × 数据集）下一组运行的准确率。我们还专门定义五个指标来量化每种条件的不稳定性，它们捕捉正、负准确率的极端。此外，我们报告中位数准确率，以便看到相对中位数的偏离。注意我们不报告均值的标准差，因为给定条件下各次运行的分布不是正态分布（见下文）。

- N 次运行的总一致率（TAR@N）：在 N 次运行中，生成答案全部相同的测试集问题所占百分比，无论答案是否正确。TAR@N 有两个变体：
  - TARr@N（原始模型响应的 TAR@N）：LLM 响应在字符串上等价。
  - TARa@N（答案的 TAR@N）：解析出的答案相同，例如 “The answer is a)” 与 “a) is the answer” 相同。

<!-- 原 PDF 第 5 页 -->

**表 2：少样本条件下（BBH 为 3，MMLU 为 5，见第 5 节）的结果，单位为百分比。** 上半部分每个单元格依次为 BestAcc、中位数准确率、WorstAcc；下半部分每个单元格依次为 TARa@10、TARr@10。默认 `find_tables` 把同一列的各行挤成一个单元格；数值按 `get_text` 的逐行顺序还原。

准确率结果（BestAcc，中位数，WorstAcc）：

| 任务 | gpt3.5 | gpt4o | llama8b | llama70b | mixtral8-7b |
| --- | --- | --- | --- | --- | --- |
| navigation | 96.8, 95.6, 93.2 | 98.8, 98.8, 98.4 | 82.0, 80.2, 78.0 | 95.2, 94.6, 93.6 | 84.4, 79.0, 71.6 |
| geo. shapes | 72.4, 59.6, 46.8 | 82.4, 68.4, 53.6 | 49.2, 40.6, 32.8 | 67.2, 57.0, 47.2 | 54.4, 27.8, 08.8 |
| logical deduct. | 88.8, 81.6, 75.2 | 100., 100., 99.6 | 95.6, 90.2, 81.2 | 98.0, 96.4, 95.2 | 87.6, 75.0, 64.0 |
| public rel. | 75.5, 69.1, 65.5 | 80.0, 76.4, 73.6 | 63.6, 61.8, 61.8 | 67.3, 60.5, 53.6 | 58.2, 48.2, 36.4 |
| Europ. hist. | 83.6, 81.2, 78.2 | 89.1, 81.5, 72.1 | 74.5, 67.0, 59.4 | 61.8, 50.3, 41.2 | 65.5, 51.5, 35.8 |
| ruin names | 72.0, 58.0, 44.8 | 93.2, 90.8, 88.4 | 68.4, 66.8, 64.4 | 89.2, 87.2, 84.4 | 78.8, 67.6, 55.6 |
| prof. account | 52.5, 50.9, 48.9 | 89.0, 74.5, 57.8 | 48.2, 45.4, 44.0 | 78.0, 67.2, 55.3 | 67.0, 39.0, 13.1 |
| college math | 39.0, 38.0, 34.0 | 88.0, 69.0, 44.0 | 50.0, 22.5, 04.0 | 85.0, 54.5, 22.0 | 75.0, 31.5, 03.0 |

TAR 结果（TARa@10，TARr@10）：

| 任务 | gpt3.5 | gpt4o | llama8b | llama70b | mixtral8-7b |
| --- | --- | --- | --- | --- | --- |
| navigation | 96.4, 46.0 | 99.6, 46.0 | 96.0, 86.0 | 98.4, 64.0 | 84.8, 50.0 |
| geo. shapes | 62.8, 25.2 | 63.2, 00.0 | 58.8, 27.6 | 66.4, 18.0 | 12.0, 02.4 |
| logical deduct. | 84.4, 34.8 | 99.6, 36.8 | 85.2, 50.0 | 97.2, 49.6 | 74.8, 16.4 |
| public rel. | 87.3, 82.7 | 92.7, 37.3 | 96.4, 73.6 | 81.8, 17.3 | 62.7, 10.9 |
| Europ. hist. | 94.5, 70.9 | 81.2, 09.1 | 82.4, 07.3 | 73.3, 22.4 | 55.2, 23.6 |
| ruin names | 66.0, 05.6 | 95.2, 00.0 | 88.4, 47.6 | 94.4, 10.8 | 70.4, 24.8 |
| prof. account | 91.1, 76.6 | 66.7, 04.6 | 89.0, 52.1 | 69.5, 00.0 | 23.4, 00.7 |
| college math | 89.0, 76.0 | 50.0, 00.0 | 22.0, 00.0 | 25.0, 00.0 | 07.0, 00.0 |

- N 次运行上最好可能准确率（BestAcc）：可以从 N 次运行中提取出的最大可能准确率。对每个问题，只要有一次运行的答案正确，该问题就标为回答正确。
- N 次运行上最差可能准确率（WorstAcc）：可以从 N 次运行中提取出的最小可能准确率。对每个问题，只要有一次运行的答案不正确，该问题就标为回答不正确。
- N 次运行上的中位数准确率。
- N 次运行上最大与最小准确率之差。注意这不同于 BestAcc 和 WorstAcc，因为我们看的是每次运行的实际准确率分数，而不是最坏情形和最好情形。

TARr@N 是最严格的不稳定性指标，因为任何字符变化都会导致不一致。因此，一组运行有可能同时具有 100% 准确率和 100% TARa@N，而 TARr@N 为 0%。

为考察准确率分数的分布性质，我们对 GPT-4o 和 Llama-3-70b 在 college math 的少样本设定上做了 20 次运行，这是较不稳定的例子中的两个。图 2 所示结果清楚地呈现非正态分布，均值和中位数远离众数。Kolmogorov-Smirnov 正态性检验（Massey Jr, 1951）以 $p < 10^{-9}$ 拒绝了正态假设。

## 6 实验

我们的八个数据集、五个基座模型和两种设定（零样本/少样本）产生八十种条件。对每种条件，我们在温度为零时做十次运行，以量化一次运行内部的不稳定程度。

## 7 结果

### 7.1 不稳定性结果

图 1 汇总了五个模型在零样本和少样本设定下、我们八个数据集上观察到的极端情况。y 轴是每种条件下十次运行中最大准确率与最小准确率的百分比差。

<!-- 原 PDF 第 6 页 -->

值得注意的是，某些任务上有 5–15% 的差异。

表 2 上半部分报告五个模型在少样本条件下的 BestAcc、中位数准确率和 WorstAcc（零样本结果呈现出相似程度的非确定性，各条件之间的一致性有所不同，见附录 A.2 的表 3）。表的下半部分报告 TARa@10 和 TARr@10。当 BestAcc 与 WorstAcc 的差距大于 10 时，TARr@10 往往很低（例如 gpt3.5 在 geometric shapes、logical deduction、ruin names 上；gpt4o 在 public relations、European history、professional accounting、college math 上；等等）。值得注意的是，TARr@10 通常相当低，并且在模型和数据集之间有大量变化。毫不意外，TARa@10 可以比 TARr@10 高得多，因为答案解析具有灵活性，而原始输出没有这种灵活性。总体而言，模型在原始输出层面和准确率层面都表现出高度不稳定。

**图 3 见原 PDF。** 图 3：少样本设定下每个模型的 TARr@10。数据集颜色用来区分相对较难（红色色调越来越深）与相对较易（蓝色色调越来越深）。

**图 4 见原 PDF。** 图 4：少样本设定下每项任务的 TARa@10。模型颜色用来区分相对低性能（红色色调越来越深）与相对高性能（蓝色色调越来越深）。

GPT-3.5 Turbo 的 TARr 低于其他模型（不稳定性更小），而 Llama-3-70B 的 TARr 往往非常低。

<!-- 原 PDF 第 7 页 -->

**图 5 见原 PDF。** 图 5：少样本设定（左）与零样本设定（右）下各指标之间的 Spearman 相关矩阵。

图 4 展示少样本设定下每种条件的 TARa@10（零样本见图 11，附录 A.2）。虽然 TARa@10 的结果比 TARr@10 显示出更少的不稳定性，它们仍然远非完美，并呈现出很强的任务特异性行为。navigation 任务上的高性能表明，该任务上的排行榜可以预期更为可靠。另一方面，college math 和 professional accounting 任务上更为分散的结果表明，在这些任务上报告的结果可能没有那么稳健。

### 7.2 相关分析

我们对下列指标的所有配对做 Spearman 秩相关分析：TARa@10、TARr@10、最大最小准确率差、中位数准确率、中位数输入长度和输出长度。热图结果见图 5，分别对应少样本和零样本提示的模型。这里我们把准确率定义为：在相同模型和数据集设定下 10 次运行的中位数准确率。输入长度和输出长度是按空格切分的中位数词数，在每个 LLM 实验设定的输入和输出上计算。我们按空格切分词，而不是使用某个特定分词器，因为我们实验的模型使用不同的分词器。

结果表明，在少样本/零样本设定下，输出长度与 TARa@10 之间、以及输出长度与 TARr@10 之间存在强/中等的负相关。注意这也与输出长度和最大–最小差的正相关一致。这些相关意味着：随着 LLM 输出长度增加，输出的不稳定性增加，从而产生更多样的自然语言响应，以及实际的多项选择答案预测。LLM 输出长度与不稳定性之间的强负相关，可以促使商业使用 LLM 的人限制最大生成词元数，以控制不稳定性。我们还看到，在少样本设定下，中位数准确率与 TARa@10 之间存在强正相关。这表明当 LLM 更准确时，它对多项选择的选择变得更确定。此外，在少样本设定下，输出长度与中位数准确率之间存在中等负相关，这表明限制最大生成词元数既改善确定性也改善准确率。这与 Zhang 等人（2024）的发现平行。

除一般相关之外，我们也查看每个模型的相关图，以看一般发现如何适用于每一个模型。我们发现，所有模型在生成更短响应时都更稳定。值得注意的是，Mixtral 和 Llama-3 模型在少样本设定下更准确时更稳定，但该效应在零样本设定下有所变化。最后，GPT-3.5 在少样本设定下输入更长时更稳定，该效应在零样本设定下不那么显著。这些相关图见附录 A.1。

<!-- 原 PDF 第 8 页 -->

## 8 讨论

理论上，在零温度下，给定相同输入，LLM 应当是确定的：TARa@10 和 TAR@10 的值应为 100%，BestAcc 与 WorstAcc 的值相同，并且在全部任务上最小值与最大值之差为 0%。

TARr@10 分数表明，模型在字符串变化层面上不稳定，但在解析出的答案层面上稳定得多。字符串变化对人类读者影响不大，因为即使输出格式不同，我们仍能抽出相同答案；但需要解析 LLM 响应的下游系统，在格式或模式不同时会受到显著影响。使用 LLM 时应当考虑到这一点。TARa@10 的值比 TARr@10 一致得多，但仍然导致高达 15% 的不稳定性，如图 1 所示。一个注意点是：我们的答案抽取系统有许多硬编码部分，这降低了系统的一般性。因此，如果重复实验，我们不能保证原始输出会为我们的各种准确率指标带来完全相同的结果。

最大–最小准确率差在理论上应为 0%。所有模型在这一指标上都表现出可观的变化。Mixtral-8x7b 在 college math 上是 72%（75% − 3%），这是一个特别差的例子，提示生成过程中存在真正的随机成分，把最小值推到了 0%。这种不稳定性降低了只在 LLM 基准中报告单一数字的可靠性信心。我们鼓励报告多次运行之间的最大–最小分数，以便对模型做更稳健的比较。

### 8.1 对实际工程的含义

虽然使用多块 GPU 会引入一些随机性（Nvidia, 2024），但可以通过设置随机种子来消除，从而使 AI 模型在给定相同输入时是确定的。在那种情况下，性能错误可以归因于模型的泛化能力（例如欠拟合/过拟合）。然而，为了让 LLM 跑得更快的工程优化，例如连续批处理、分块预填充或前缀缓存，可能导致非确定性行为。由于许多模型是闭源的（GPT-3.5、GPT-4o），并且全部都托管在我们无法控制的 API 之后，我们只能推测这一行为的原因。为支持这一推理，我们在本地 GPU 上不加任何优化地运行 Llama3-8b，得到了确定性结果。这表明模型和 GPU 本身并不是非确定性的唯一来源。

此外，我们用两折交叉验证微调了 gpt-3.5。虽然结果表明微调有助于降低不稳定性，我们假设微调后的模型不能在用户之间共享，因此当时运行的只有我们的任务。

非确定的 AI 给开发者带来新挑战，在商业应用中尤其如此：

- 由于非确定性，对 AI 函数使用单元测试是受限的。一种替代可能是容忍变异的回归测试。
- 低稳定性也可能增加难以解释的错误的可能性，这些错误与人类错误非常不同，例如在任务是多项选择时回答 “none of the above”。
- 输出格式的不稳定性可能导致下游解析器失败。
- 假设由非确定性引起的错误和由系统性能引起的错误是独立同分布（IID）的，它们合在一起产生乘性的性能下降。例如，一个用非确定 LLM 分类器来管理转移的对话系统，其性能会随着对话状态序列中每增加一个状态而下降。具体而言，一个有 4 个分类器、每个稳定度为 95% 的对话系统，在甚至还没有把分类器在新输入上的准确率算进去之前，就会表现出期望性能 .954 = .814。公式抽取不完整，见原 PDF 第 8 页。
- 最重要的影响之一在于系统复杂度：系统必须优雅地处理“通常正确、但这一次错了”的结果。Zipfian 分布在

<!-- 原 PDF 第 9 页 -->

应用 AI 系统中很常见：某个输入/类别的频率与它在按计数排序后的秩成反比，$frequency \propto 1/rank$。测试倾向于集中在频繁事件上，这给人信心：所得系统对常见输入是稳定的。然而，缺乏稳定性会动摇这一信心的整个基础，尤其是当错误代价高昂时。

## 9 结论

我们对应当最大化确定性的超参数下 LLM 的确定性做了系统分析。结果表明，LLM 在标准设定下可以非常非确定。此外，给定相同输入，LLM 很少十次都产生相同响应；然而，解析出的答案往往更稳定。不稳定性结果不是正态分布这一观察，使衡量由此产生的不确定性更加困难。最后，对同一模型，不稳定性在任务之间高度可变；对同一任务，不稳定性在模型之间高度可变。

关于不稳定性的其他问题仍有待探索。例如，如何在训练或推断时降低 LLM 的不稳定性（例如增加一条元提示，表明模型只允许用单个字母作答）？第二，商业产品中如何把 LLM 的不稳定性考虑进去？第三，我们应当如何向决策者沟通不稳定性？最后，还可以做更多分析，看稳定性与特定类型的错误（例如假阳性和假阴性）之间是否存在任何相关。

## 参考文献

Stella Biderman, Hailey Schoelkopf, Lintang Sutawika, Leo Gao, Jonathan Tow, Baber Abbasi, Alham Fikri Aji, Pawan Sasanka Ammanamanchi, Sidney Black, Jordan Clive, et al. 来自一线的教训：语言模型可复现评估. arXiv preprint arXiv:2405.14782, 2024.

Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. 语言模型是少样本学习者. Advances in neural information processing systems, 33:1877–1901, 2020.

Jiuhai Chen and Jonas Mueller. 量化任意语言模型答案中的不确定性并增强其可信赖性. In Lun-Wei Ku, Andre Martins, and Vivek Srikumar (eds.), Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 5186–5200, Bangkok, Thailand, August 2024. Association for Computational Linguistics. doi: 10.18653/v1/2024.acl-long.283. URL https://aclanthology.org/2024.acl-long.283/.

Irene de Zarz`a i Cubero, Joaquim de Curt`o i D´ıaz, Gemma Roig, and Carlos T Calafate（原 PDF 第 9 页抽取串，重音符号乱码）. 优化的财务规划：把个人与合作预算模型与 LLM 建议整合起来. 2024.

Kaze Du, Bo Yang, Keqiang Xie, Nan Dong, Zhengping Zhang, Shilong Wang, and Fan Mo. llm-manuf：面向制造中智能决策的大语言模型微调集成框架. Advanced Engineering Informatics, 65:103263, 2025.

Xuefeng Du, Zhaoning Wang, Mu Cai, and Sharon Li. 走向借助虚拟离群点合成的未知感知学习. In International Conference on Learning Representations (ICLR), 2022. URL https://openreview.net/forum?id=TW7d65uYu5M.

Timo Freiesleben and Thomas Grote. 超越泛化：机器学习中稳健性的一种理论. Synthese, 202(4):109, 2023.

<!-- 原 PDF 第 10 页 -->

Aryo Pradipta Gema, Joshua Ong Jun Leang, Giwon Hong, Alessio Devoto, Alberto Carlo Maria Mancino, Rohit Saxena, Xuanli He, Yu Zhao, Xiaotang Du, Mohammad Reza Ghasemi Madani, et al. 我们做完 MMLU 了吗？ arXiv preprint arXiv:2406.04127, 2024.

Leif Hancox-Li. 机器学习解释中的稳健性：它重要吗？ In Proceedings of the 2020 Conference on Fairness, Accountability, and Transparency, FAT* ’20, pp. 640–647, New York, NY, USA, 2020. Association for Computing Machinery. ISBN 9781450369367. doi: 10.1145/3351095.3372836. URL https://doi.org/10.1145/3351095.3372836.

Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, and Jacob Steinhardt. 衡量大规模多任务语言理解. In International Conference on Learning Representations, 2021. URL https://openreview.net/forum?id=d7KBjmI3GmQ.

Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes, and Yejin Choi. 神经文本退化的奇特情形. In International Conference on Learning Representations, 2020. URL https://openreview.net/forum?id=rygGQyrFvH.

Albert Q. Jiang, Alexandre Sablayrolles, Antoine Roux, Arthur Mensch, Blanche Savary, Chris Bamford, Devendra Singh Chaplot, Diego de las Casas, Emma Bou Hanna, Florian Bressand, Gianna Lengyel, Guillaume Bour, Guillaume Lample, L´elio Renard Lavaud, Lucile Saulnier, Marie-Anne Lachaux, Pierre Stock, Sandeep Subramanian, Sophia Yang, Szymon Antoniak, Teven Le Scao, Th´eophile Gervet, Thibaut Lavril, Thomas Wang, Timoth´ee Lacroix, and William El Sayed（原 PDF 第 10 页抽取串，重音符号乱码）. 专家混合 Mixtral, 2024a. URL https://arxiv.org/abs/2401.04088.

Juyong Jiang, Fan Wang, Jiasi Shen, Sungju Kim, and Sunghun Kim. 用于代码生成的大语言模型综述. arXiv preprint arXiv:2406.00515, 2024b.

Bo Liu, Li-Ming Zhan, Zexin Lu, Yujie Feng, Lei Xue, and Xiao-Ming Wu. LLM 在分布外检测上有多好？ In Nicoletta Calzolari, Min-Yen Kan, Veronique Hoste, Alessandro Lenci, Sakriani Sakti, and Nianwen Xue (eds.), Proceedings of the 2024 Joint International Conference on Computational Linguistics, Language Resources and Evaluation (LREC-COLING 2024), pp. 8211–8222, Torino, Italia, May 2024. ELRA and ICCL. URL https://aclanthology.org/2024.lrec-main.720/.

Frank J Massey Jr. 拟合优度的 Kolmogorov-Smirnov 检验. Journal of the American statistical Association, 46(253):68–78, 1951.

Meta. 介绍 Meta Llama 3：迄今能力最强的公开可用 LLM. https://ai.meta.com/blog/meta-llama-3, 2024.

Joel Niklaus, Veton Matoshi, Matthias St¨urmer, Ilias Chalkidis, and Daniel Ho（原 PDF 第 10 页抽取串，变音符号乱码）. MultiLegalPile：一个 689GB 的多语言法律语料. In Lun-Wei Ku, Andre Martins, and Vivek Srikumar (eds.), Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 15077–15094, Bangkok, Thailand, August 2024. Association for Computational Linguistics. doi: 10.18653/v1/2024.acl-long.805. URL https://aclanthology.org/2024.acl-long.805/.

Nvidia. NVIDIA GPU 的浮点与 IEEE 754 符合性. https://docs.nvidia.com/cuda/floating-point/index.html, 2024.

OpenAI, Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, Red Avila, Igor Babuschkin, Suchir Balaji, Valerie Balcom, Paul Baltescu, Haiming Bao, Mohammad Bavarian, Jeff Belgum, Irwan Bello, Jake Berdine, Gabriel Bernadett-Shapiro, Christopher Berner, Lenny Bogdonoff, Oleg Boiko, Madelaine Boyd, Anna-Luisa Brakman, Greg Brockman, Tim Brooks, Miles Brundage, Kevin Button, Trevor Cai, Rosie Campbell, Andrew Cann, Brittany Carey, Chelsea Carlson, Rory Carmichael, Brooke Chan, Che Chang, Fotis Chantzis, Derek Chen, Sully Chen, Ruby Chen, Jason Chen, Mark Chen, Ben Chess, Chester Cho, Casey Chu, Hyung Won Chung, Dave Cummings,

<!-- 原 PDF 第 11 页 -->

Jeremiah Currier, Yunxing Dai, Cory Decareaux, Thomas Degry, Noah Deutsch, Damien Deville, Arka Dhar, David Dohan, Steve Dowling, Sheila Dunning, Adrien Ecoffet, Atty Eleti, Tyna Eloundou, David Farhi, Liam Fedus, Niko Felix, Sim´on Posada Fishman（原 PDF 第 11 页抽取串）, Juston Forte, Isabella Fulford, Leo Gao, Elie Georges, Christian Gibson, Vik Goel, Tarun Gogineni, Gabriel Goh, Rapha Gontijo-Lopes, Jonathan Gordon, Morgan Grafstein, Scott Gray, Ryan Greene, Joshua Gross, Shixiang Shane Gu, Yufei Guo, Chris Hallacy, Jesse Han, Jeff Harris, Yuchen He, Mike Heaton, Johannes Heidecke, Chris Hesse, Alan Hickey, Wade Hickey, Peter Hoeschele, Brandon Houghton, Kenny Hsu, Shengli Hu, Xin Hu, Joost Huizinga, Shantanu Jain, Shawn Jain, Joanne Jang, Angela Jiang, Roger Jiang, Haozhun Jin, Denny Jin, Shino Jomoto, Billie Jonn, Heewoo Jun, Tomer Kaftan, Łukasz Kaiser, Ali Kamali, Ingmar Kanitscheider, Nitish Shirish Keskar, Tabarak Khan, Logan Kilpatrick, Jong Wook Kim, Christina Kim, Yongjik Kim, Jan Hendrik Kirchner, Jamie Kiros, Matt Knight, Daniel Kokotajlo, Łukasz Kondraciuk, Andrew Kondrich, Aris Konstantinidis, Kyle Kosic, Gretchen Krueger, Vishal Kuo, Michael Lampe, Ikai Lan, Teddy Lee, Jan Leike, Jade Leung, Daniel Levy, Chak Ming Li, Rachel Lim, Molly Lin, Stephanie Lin, Mateusz Litwin, Theresa Lopez, Ryan Lowe, Patricia Lue, Anna Makanju, Kim Malfacini, Sam Manning, Todor Markov, Yaniv Markovski, Bianca Martin, Katie Mayer, Andrew Mayne, Bob McGrew, Scott Mayer McKinney, Christine McLeavey, Paul McMillan, Jake McNeil, David Medina, Aalok Mehta, Jacob Menick, Luke Metz, Andrey Mishchenko, Pamela Mishkin, Vinnie Monaco, Evan Morikawa, Daniel Mossing, Tong Mu, Mira Murati, Oleg Murk, David M´ely（原 PDF 第 11 页抽取串）, Ashvin Nair, Reiichiro Nakano, Rajeev Nayak, Arvind Neelakantan, Richard Ngo, Hyeonwoo Noh, Long Ouyang, Cullen O’Keefe, Jakub Pachocki, Alex Paino, Joe Palermo, Ashley Pantuliano, Giambattista Parascandolo, Joel Parish, Emy Parparita, Alex Passos, Mikhail Pavlov, Andrew Peng, Adam Perelman, Filipe de Avila Belbute Peres, Michael Petrov, Henrique Ponde de Oliveira Pinto, Michael, Pokorny, Michelle Pokrass, Vitchyr H. Pong, Tolly Powell, Alethea Power, Boris Power, Elizabeth Proehl, Raul Puri, Alec Radford, Jack Rae, Aditya Ramesh, Cameron Raymond, Francis Real, Kendra Rimbach, Carl Ross, Bob Rotsted, Henri Roussez, Nick Ryder, Mario Saltarelli, Ted Sanders, Shibani Santurkar, Girish Sastry, Heather Schmidt, David Schnurr, John Schulman, Daniel Selsam, Kyla Sheppard, Toki Sherbakov, Jessica Shieh, Sarah Shoker, Pranav Shyam, Szymon Sidor, Eric Sigler, Maddie Simens, Jordan Sitkin, Katarina Slama, Ian Sohl, Benjamin Sokolowsky, Yang Song, Natalie Staudacher, Felipe Petroski Such, Natalie Summers, Ilya Sutskever, Jie Tang, Nikolas Tezak, Madeleine B. Thompson, Phil Tillet, Amin Tootoonchian, Elizabeth Tseng, Preston Tuggle, Nick Turley, Jerry Tworek, Juan Felipe Cer´on Uribe（原 PDF 第 11 页抽取串）, Andrea Vallone, Arun Vijayvergiya, Chelsea Voss, Carroll Wainwright, Justin Jay Wang, Alvin Wang, Ben Wang, Jonathan Ward, Jason Wei, CJ Weinmann, Akila Welihinda, Peter Welinder, Jiayi Weng, Lilian Weng, Matt Wiethoff, Dave Willner, Clemens Winter, Samuel Wolrich, Hannah Wong, Lauren Workman, Sherwin Wu, Jeff Wu, Michael Wu, Kai Xiao, Tao Xu, Sarah Yoo, Kevin Yu, Qiming Yuan, Wojciech Zaremba, Rowan Zellers, Chong Zhang, Marvin Zhang, Shengjia Zhao, Tianhao Zheng, Juntang Zhuang, William Zhuk, and Barret Zoph. GPT-4 技术报告, 2024. URL https://arxiv.org/abs/2303.08774.

Shuyin Ouyang, Jie M. Zhang, Mark Harman, and Meng Wang. ChatGPT 在代码生成中的非确定性的实证研究. ACM Transactions on Software Engineering and Methodology, 34(2), January 2025. doi: 10.1145/3697010.

Shuofei Qiao, Yixin Ou, Ningyu Zhang, Xiang Chen, Yunzhi Yao, Shumin Deng, Chuanqi Tan, Fei Huang, and Huajun Chen. 用语言模型提示做推理：综述. In Anna Rogers, Jordan Boyd-Graber, and Naoaki Okazaki (eds.), Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pp. 5368–5393, Toronto, Canada, July 2023. Association for Computational Linguistics. doi: 10.18653/v1/2023.acl-long.294. URL https://aclanthology.org/2023.acl-long.294.

Jonas Rauber, Wieland Brendel, and Matthias Bethge. Foolbox：一个用于基准测试机器学习模型稳健性的 Python 工具箱. arXiv preprint arXiv:1707.04131, 2017.

David Rein, Betty Li Hou, Asa Cooper Stickland, Jackson Petty, Richard Yuanzhe Pang, Julien Dirani, Julian Michael, and Samuel R. Bowman. GPQA：一个研究生水平、抗谷歌检索的问答基准, 2023.

<!-- 原 PDF 第 12 页 -->

Joshua Robinson and David Wingate. 利用大语言模型做多项选择问答. In The Eleventh International Conference on Learning Representations, 2023. URL https://openreview.net/forum?id=yKbprarjc5B.

Vikash Sehwag, Arjun Nitin Bhagoji, Liwei Song, Chawin Sitawarin, Daniel Cullina, Mung Chiang, and Prateek Mittal. 分析开放世界机器学习的稳健性. In Proceedings of the 12th ACM Workshop on Artificial Intelligence and Security, AISec’19, pp. 105–116, New York, NY, USA, 2019. Association for Computing Machinery. ISBN 9781450368339. doi: 10.1145/3338501.3357372. URL https://doi.org/10.1145/3338501.3357372.

Sina Shool, Sara Adimi, Reza Saboori Amleshi, Ehsan Bitaraf, Reza Golpira, and Mahmood Tara. 临床医学中大语言模型（LLM）评估的系统综述. BMC Medical Informatics and Decision Making, 25(1):117, 2025.

Kumar Shridhar, Koustuv Sinha, Andrew Cohen, Tianlu Wang, Ping Yu, Ramakanth Pasunuru, Mrinmaya Sachan, Jason Weston, and Asli Celikyilmaz. LLM 精炼的 ART：询问、精炼与信任. In Kevin Duh, Helena Gomez, and Steven Bethard (eds.), Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers), pp. 5872–5883, Mexico City, Mexico, June 2024. Association for Computational Linguistics. doi: 10.18653/v1/2024.naacl-long.327. URL https://aclanthology.org/2024.naacl-long.327/.

Yifan Song, Guoyin Wang, Sujian Li, and Bill Yuchen Lin. 好的、坏的与贪心的：LLM 评估不应忽视非确定性. arXiv preprint arXiv:2407.10457, 2024.

Mirac Suzgun, Nathan Scales, Nathanael Sch¨arli（原 PDF 第 12 页抽取串，变音符号乱码）, Sebastian Gehrmann, Yi Tay, Hyung Won Chung, Aakanksha Chowdhery, Quoc Le, Ed Chi, Denny Zhou, and Jason Wei. 有挑战的 BIG-bench 任务，以及思维链能否解决它们. In Anna Rogers, Jordan Boyd-Graber, and Naoaki Okazaki (eds.), Findings of the Association for Computational Linguistics: ACL 2023, pp. 13003–13051, Toronto, Canada, July 2023. Association for Computational Linguistics. doi: 10.18653/v1/2023.findings-acl.824. URL https://aclanthology.org/2023.findings-acl.824.

Chi Wang, Xueqing Liu, and Ahmed Hassan Awadallah. 大语言模型生成推断的高性价比超参数优化. In International Conference on Automated Machine Learning, pp. 21–1. PMLR, 2023.

Pei-Hsin Wang, Sheng-Iou Hsieh, Shieh-Chieh Chang, Jia-Yu Pan, Yu-Ting Chen, Wei Wei, and Da-Cheng Juan. 语言建模的上下文温度, 2020. URL https://openreview.net/forum?id=H1x9004YPr.

Yubo Wang, Xueguang Ma, Ge Zhang, Yuansheng Ni, Abhranil Chandra, Shiguang Guo, Weiming Ren, Aaran Arulraj, Xuan He, Ziyan Jiang, et al. MMLU-Pro：一个更稳健、更有挑战的多任务语言理解基准. arXiv preprint arXiv:2406.01574, 2024.

Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al. 思维链提示激发大语言模型中的推理. Advances in neural information processing systems, 35:24824–24837, 2022.

Yusen Zhang, Sarkar Snigdha Sarathi Das, and Rui Zhang. 冗长不等于真实：揭开大语言模型冗长补偿行为的神秘面纱, 2024. URL https://arxiv.org/abs/2411.07858. 原 PDF 第 12 页符号 “̸=” 保留，题名原文为 Verbosity ̸= veracity。

## A 附录

### A.1 每个模型的相关矩阵

### A.2 零样本结果

<!-- 原 PDF 第 13 页 -->

**图 6 见原 PDF。** 图 6：GPT-4o 在少样本设定（左）与零样本设定（右）下各指标之间的 Spearman 相关矩阵。

**图 7 见原 PDF。** 图 7：GPT-3.5-turbo 在少样本设定（左）与零样本设定（右）下各指标之间的 Spearman 相关矩阵。

**图 8 见原 PDF。** 图 8：Llama-8b 在少样本设定（左）与零样本设定（右）下各指标之间的 Spearman 相关矩阵。

<!-- 原 PDF 第 14 页 -->

**图 9 见原 PDF。** 图 9：Llama-70b 在少样本设定（左）与零样本设定（右）下各指标之间的 Spearman 相关矩阵。

**图 10 见原 PDF。** 图 10：Mixtral-8x7b 在少样本设定（左）与零样本设定（右）下各指标之间的 Spearman 相关矩阵。

**图 11 见原 PDF。** 图 11：零样本设定下每项任务的 TARa@10。模型颜色用来区分相对低性能（红色色调越来越深）与相对高性能（蓝色色调越来越深）。

<!-- 原 PDF 第 15 页 -->

**表 3：零样本条件下的结果，单位为百分比。** 上半部分每个单元格依次为 BestAcc、中位数准确率、WorstAcc；下半部分每个单元格依次为 TARa@10、TARr@10。数值按 `get_text` 逐行还原。

准确率结果（BestAcc，中位数，WorstAcc）：

| 任务 | gpt3.5 | gpt4o | llama8b | llama70b | mixtral8-7b |
| --- | --- | --- | --- | --- | --- |
| navigation | 67.2, 64.8, 61.6 | 94.8, 92.0, 88.8 | 88.4, 73.0, 54.0 | 94.0, 88.0, 78.4 | 66.0, 57.6, 48.0 |
| geo. shapes | 16.8, 15.2, 13.6 | 76.0, 56.8, 30.4 | 24.4, 18.8, 12.0 | 44.4, 21.6, 6.4 | 29.6, 27.0, 24.8 |
| logical deduct. | 52.8, 50.8, 48.8 | 100.0, 98.6, 96.0 | 72.4, 62.8, 55.6 | 95.6, 92.2, 87.6 | 70.0, 59.6, 49.6 |
| public rel. | 66.4, 65.0, 61.8 | 81.8, 75.5, 66.4 | 28.2, 25.0, 19.1 | 39.1, 26.4, 13.6 | 57.3, 46.8, 35.5 |
| Europ. hist. | 75.2, 74.5, 72.7 | 76.4, 65.2, 55.2 | 38.8, 34.2, 30.3 | 41.2, 27.9, 19.4 | 66.1, 56.1, 45.5 |
| ruin names | 67.2, 65.6, 65.2 | 85.2, 83.2, 80.0 | 54.8, 50.6, 45.6 | 67.6, 60.0, 51.2 | 38.0, 34.4, 30.4 |
| prof. account | 60.3, 53.2, 47.5 | 84.0, 72.0, 58.5 | 36.2, 29.1, 25.5 | 54.6, 38.7, 24.8 | 42.9, 28.9, 20.2 |
| college math | 54.0, 32.0, 15.0 | 85.0, 59.0, 41.0 | 55.0, 34.0, 17.0 | 77.0, 58.0, 40.0 | 57.0, 31.5, 13.0 |

TAR 结果（TARa@10，TARr@10）：

| 任务 | gpt3.5 | gpt4o | llama8b | llama70b | mixtral8-7b |
| --- | --- | --- | --- | --- | --- |
| navigation | 94.4, 94.4 | 91.6, 15.2 | 65.2, 9.2 | 83.2, 4.8 | 77.6, 3.2 |
| geo. shapes | 91.6, 91.6 | 45.6, 0.8 | 60.4, 31.2 | 39.2, 5.6 | 90.4, 83.6 |
| logical deduct. | 92.8, 90.4 | 96.8, 7.6 | 80.4, 37.6 | 92.0, 16.4 | 74.4, 14.0 |
| public rel. | 92.7, 86.4 | 83.6, 38.2 | 82.7, 46.4 | 56.4, 0.9 | 61.8, 10.0 |
| Europ. hist. | 94.5, 94.5 | 74.5, 17.0 | 77.6, 41.2 | 53.9, 6.1 | 63.6, 19.4 |
| ruin names | 95.6, 97.2 | 93.6, 27.6 | 86.8, 26.8 | 79.2, 11.6 | 82.4, 20.8 |
| prof. account | 81.9, 49.3 | 71.3, 4.3 | 77.0, 44.0 | 57.8, 2.1 | 48.2, 4.3 |
| college math | 46.0, 10.0 | 50.0, 0.0 | 45.0, 3.0 | 54.0, 0.0 | 29.0, 2.0 |

**图 12 见原 PDF。** 图 12：零样本设定下每个模型的 TARr@10。数据集颜色用来区分相对较难（红色色调越来越深）与相对较易（蓝色色调越来越深）。

<!-- 译完 -->
