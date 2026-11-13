> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名：** FLEX_NAACL2025.pdf

**原文标题：** FLEX: Expert-level False-Less EXecution Metric for Reliable Text-to-SQL Benchmark

**作者：** Heegyu Kim、Taeyang Jeon、Seunghwan Choi、Seungtaek Choi、Hyunsouk Cho（通讯作者）。单位为 Ajou University（人工智能系；软件与计算机工程系），Suwon，韩国。

**场合：** NAACL 2025，*Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)*，第 4448–4475 页，2025 年 4 月 29 日–5 月 4 日。

## 摘要 Abstract

Text-to-SQL 已在多个行业里承担把自然语言写成 SQL 的工作，非技术用户靠它做复杂数据操作，系统变强之后，评测是否可信就成了瓶颈。目前最常用的 Execution Accuracy（EX）仍会把错查询判对、把对查询判错。本文提出 FLEX（False-Less EXecution）：让大语言模型按专家方式评 SQL，评测时带上更完整的上下文，并用更细的正确性标准。与人类专家的一致性从 Cohen’s kappa 62 升到 87.04。

摘要里点出的后文主结果是：在 Spider 与 BIRD 上，模型分数平均上升超过 2.6 分，排名随之改动；EX 低估模型主要来自标注质量，特别难的问题上模型又容易被高估。BIRD 前十的重排见引言 Table 1。

## 1 Introduction

这一节的主张是：人工评 SQL 既慢又贵，Spider（Yu et al., 2018）因此改用 EX，BIRD（Li et al., 2023c）沿用同一指标；EX 只比执行结果，数据库状态碰巧一致时会放过错误查询，问题含糊时又会惩罚正确查询（Pourreza and Rafiei, 2023b），评出来的能力和专家判断对不齐。已有的 LLM 评测（Kim et al., 2023; Zheng et al., 2023; Zhao et al., 2024）上下文不足，也处理不好带噪声的 ground truth，标准含糊，放到现有 text-to-SQL 基准上甚至不如 EX。

FLEX 同时看自然语言问题、数据库 schema 和外部知识，并配有判断查询是否正确的细则。它与专家的 Cohen’s kappa 为 87.04，EX 为 62.00，也高于先前的 LLM 评测。作者用它重评了 50 个公开模型在 Spider 和 BIRD 上的结果；脚注说明所用 BIRD-dev 为 20240627 版本，ground truth 有修改，因此这里的 EX 与先前研究不同。Table 1 用 FLEX 重排 BIRD 前十，Δ 定义为低估误差（FLEX − EX）。表中 SuperSQL 升 2 位居首（FLEX 64.08，EX 57.37，Δ +6.71），CHESS-GPT-4o-mini 降 1 位仍为第 2（62.71 / 59.13 / +3.59），TA-ACL 升 2 位（59.97 / 55.67 / +4.30），DAIL_SQL_9-SHOT_MP 升 3 位（59.26 / 53.52 / +5.74），DAIL_SQL_9-SHOT_QM 升 4 位与降 3 位的 DTS-SQL-BIRD-GPT4o 并列第 5（均为 58.47；EX 分别为 53.06 与 58.08，Δ 为 +5.41 与 +0.39）。其后 SFT_CodeS_15B_EK 降 3 位（56.98 / 56.52 / +0.46），SFT_CodeS_7B_EK 降 2 位（53.59 / 54.89 / −1.30），SFT_CodeS_3B_EK 降 1 位（53.26 / 53.46 / −0.20），DAIL_SQL 升 2 位（51.83 / 45.89 / +5.93）。Fig. 1 在 Spider 上把 FLEX 对 EX 画在恒等线旁，多数模型的 FLEX 更高。错误归类后，作者把低估主要归到噪声标注，并指出 BIRD 的难题上模型会被高估。代码公开于 https://github.com/HeegyuKim/FLEX 。

贡献收成三点：说清 EX 的关键缺陷；给出与专家推理更一致的 FLEX；用这 50 个模型的重评说明现有排名和基准需要更可靠的评测。

## 2 Related Work

相关工作先把传统指标的缺口说清楚。Spider 同时提出 Exact Matching（EM）和 EX。EM 比两条 SQL 在句法上是否等价，同一逻辑可以有很多写法，假阴性因此很高。BIRD 把主指标换成 EX，只比执行结果。标注质量仍会制造假阴性；错误查询若碰巧得到与 ground truth 相同的结果，又会变成假阳性。作者据此认为需要更稳的语义评测。

接着转到用 LLM 当裁判。MT-Bench（Zheng et al., 2023）和 AlpacaEval（Li et al., 2023e）用 LLM 评自然语言生成里的人类偏好，比人工更快、更便宜，但主要依赖闭源 GPT-4（OpenAI et al., 2024），模型被改掉或停用就会影响复现。Kim 等人的开源裁判 Prometheus 把复现和成本问题解决到接近 GPT-4 的水平，面向的仍是一般偏好，而不是 text-to-SQL。

专门做 text-to-SQL 的是 Zhao 等人的 LLM-SQL-Solver。它不区分假阳性与假阴性，用两种提示判断两条查询的执行是否等价：Miniature-and-Mull 评语义等价，Explain-and-Compare 比较重要的逻辑差异。作者认为它还不足以取代 EX，具体局限留到第 4.3 节再查。
