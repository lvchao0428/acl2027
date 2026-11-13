> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

- 原文件名：mFAR_arXiv2410.20056.pdf
- 原文标题：MULTI-FIELD ADAPTIVE RETRIEVAL
- 作者：Millicent Li（Northeastern University）、Tongfei Chen（Augment Code）、Benjamin Van Durme、Patrick Xia（Microsoft）。Li 与 Chen 的工作在 Microsoft 完成
- 场合：ICLR 2025 会议论文；arXiv:2410.20056v2 [cs.IR]，2025 年 4 月 16 日

## 摘要

搜索和 RAG 用的文档检索，语料通常是没有内部结构的自由文本。真实文档却常有字段：文章标题、消息正文、HTML header。MFAR（Multi-Field Adaptive Retrieval）是一套可接任意数量、任意类型文档索引的框架，面向半结构化数据。它分两步：把已有文档拆成字段，每个字段分别做 dense 和 lexical 索引；再学一个模型，按查询预测各字段的重要性，从而在查询时给最可能相关的字段加权。

作者的结论是：不同字段类型上，dense 与 lexical 表示可以按需搭配；文档排序明显好于若干现有检索器；在多字段半结构化数据上达到当时最优。代码在 https://github.com/microsoft/multifield-adaptive-retrieval 。摘要里的方法名是 MFAR，后文 Figure 2 写作 mFAR。

## 1 INTRODUCTION

第 1 节把缺口放在文档一侧，而不是查询一侧。检索既服务网页搜索和问答，也重新进入 LLM 工作流里的 RAG。已有工作更多把查询写得更复杂、更自然（Yang et al., 2018; Qi et al., 2019; Jeong et al., 2024; Lin et al., 2023）；文档变复杂这一面研究较少（Jiang et al., 2024; Wu et al., 2024b）。MS MARCO（Nguyen et al., 2016）一类数据里，文本块往往和查询直接相关，检索要么做词法匹配（Robertson et al., 1994），要么用稠密向量（Karpukhin et al., 2020; Ni et al., 2022; Izacard et al., 2022）。混合打分（Gao et al., 2021; Chen et al., 2022）有人试过，但不是主流。本文同时回到混合模型和更复杂文档的检索。

动机有两条。文档确有结构，标题、时间戳、header、作者等字段会被查询直接点名；不同字段也可能需要不同打分，而且不是每个字段都对当前查询有用。已有半结构化稠密检索偏向在预训练里把结构嵌进模型（Li et al., 2023; Su et al., 2024）。作者要的是能灵活组合现成预训练模型和打分器的方法。更早的多字段检索主要是词法、稀疏特征或早期神经网络（Robertson et al., 1994; Zaragoza et al., 2004; Zamani et al., 2018）。MFAR 为每个字段准备成对视图和多种打分器（例如一个词法、一个向量），再用轻量模块按查询给最可能的字段加权。推理时可以把全部字段和打分器都放进来，由模型决定相对重要性。它不要求为这个任务再预训练，测试时还有一定可控性。

贡献写成四条。框架面向任意字段数的半结构化文档，并混合词法与向量打分。混合打分好于只用 dense 或只用 lexical；按字段编码也好于把整篇文档当成一块来编码，并在半结构化检索数据 STaRK 上达到当时最优。自适应加权按查询抬高相关字段、压低不重要字段。最后用测试时开关打分器的消融，分析各字段的重要性。文中把半结构化收成可拆字段的文档：每个字段有名字和值。Figure 1 下半的 STaRK-Prime 里，Entity Type 的值可以是 “drug”，Category 的值可以是词列表。这个表述同时覆盖知识库条目、带时间戳和发件人等元数据的聊天或邮件，以及表格。Figure 1 上半用 MS MARCO 的 “aleve maximum dose” 和 BioASQ 的 “What is Piebaldism?” 对照：那些是直接回答查询的自由文本。下半的 STaRK-Amazon、STaRK-MAG、STaRK-Prime 则要在 Title、Brand、Reviews、Authors、Indication 等字段里聚合有用证据，并忽略无关字段。第 1 节没有给出具体评测数字。

## 2 MULTI-FIELD RETRIEVAL

第 2 节先把检索写成排序问题，再给出标准对比学习和 MFAR 的字段加权。语料 C = {d_1, …, d_n}，字段集 F = {f_1, …, f_m}，文档 d = {f: x_f | f ∈ F}。给定自然语言查询 q，要一个打分函数 s(q, d)，使相关文档排在最前或进入 top-k。查询可以词法地或语义地问到任意字段子集。Figure 2 用 STaRK-MAG 说明差别：查询里高亮的部分对应文档的特定字段。传统检索器（A）拿整篇文档和查询比，例如向量相似度，图中 Score(Q, D) = 0.5。mFAR（B）先拆字段，每个字段同时用词法和向量打分，得到一对分数，再按查询条件加权，合成文档级分数。图中的示意分数是 abstract (0.5, 0)、institution (0.8, 1.0)、area of study (0.5, 0.5)，字段权重 [(0.3, 0.2), (0.4, 0.0), (0.0, 0.1)]，合成分为 0.57。这些是图例，不是后文实验表里的结果。

2.1 回顾整篇索引。词法打分如 BM25 用词频直接算 s(q, d)；稠密打分用编码器嵌入文档和查询，本文用未归一化的点积。编码器可用对比损失微调（Izacard et al., 2022）：对查询 q_i，把正例文档 d^+_i 和 k 个负例分开，共享编码器，并用温度 τ 稳定训练。式 (1) 的 L_c 最大化 P(d^+_i | q_i)。负例按 Henderson et al. (2017)、Izacard et al. (2022) 和 Chen et al. (2020a) 在 batch 内采样：一个 batch 有 b 篇文档时，其他正例 d^+_j（j ≠ i）当作负例。再按 Yang et al. (2019)、Ni et al. (2022)、Chen et al. (2025) 加反向损失，最大化 P(q_i | d^+_i)，式 (2) 的 L_b 把同一正例文档上的其他查询当负查询。共享编码器的总损失是 L = L_c + L_b。

2.2 把 s(q, d) 改成字段与打分方法上的加权和。式 (3) 对字段 f 和方法 m 求和，项是 w^m_f · s^m_f(q, x_f)。混合模型的方法集 M = {lexical, dense}。权重可以学。因为无关数字或内部标识符不必参与，而且查询通常只问到少数、且随查询变化的字段，权重再条件于查询：w^m_f = G(q, f, m)，得到式 (4)。实现上，q 是查询的稠密向量，a^m_f 是与之同维的可学习参数；G 先做点积，再对所有字段和打分器做 softmax，MFAR 用的是这个更稳的形式。不同打分器的分数尺度不同。作者不想让 G 兼做归一化，于是试验按字段做 batch normalization（Ioffe & Szegedy, 2015），白化分数并学习标量 γ^m_f 和 β^m_f。这些分数最终进入对比损失的 softmax，因此 γ 像偏置，调节每项分数的重要性，β 没有作用。若只用 dense、分布已经接近，白化不一定有益，是否使用归一化留作网格搜索的超参数。推理时按 s(q, d) 排序。对全库计算 |F| |M| |C| 个分数太慢，所以先为每个字段和打分器取 top-k 短名单，只对它们的并集算完整分数再排序。文中强调，这是不精确的 top-k 近似，不同于对查询和每篇文档重新打分的后期重排，后者不是本文重点。
