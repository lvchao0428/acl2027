# MULTI-FIELD ADAPTIVE RETRIEVAL

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`mFAR_arXiv2410.20056.pdf`。

## ABSTRACT 摘要

面向搜索、检索增强生成（retrieval-augmented generation）等任务的文档检索，通常使用无结构（unstructured）数据集：每篇文档都是自由文本，内部没有显式结构。然而，文档也可以带有某种结构，包含文章标题、消息正文或 HTML 页眉（HTML header）等字段。为弥补这一缺口，我们提出多字段自适应检索（Multi-Field Adaptive Retrieval, MFAR），一个灵活框架，能在半结构化数据上容纳任意数量、任意类型的文档索引。该框架包含两个主要步骤：（1）把已有文档分解为字段，每个字段分别通过稠密方法与词法方法独立建索引；（2）学习一个模型，它以文档查询为条件，自适应地预测某个字段的重要性，从而即时为最可能的字段加权。我们发现，该方法能按字段类型优化稠密表示与词法表示的使用，在文档排序上显著优于若干现有检索器，并在多字段半结构化数据上达到最先进的性能。

## 1 INTRODUCTION 引言

文档检索有许多传统应用，例如网页搜索或问答；作为大语言模型（LLM）工作流的一部分，例如检索增强生成（retrieval-augmented generation, RAG），它也重新受到关注。一个研究方向聚焦于提高查询的复杂度与自然度（Yang et al., 2018; Qi et al., 2019; Jeong et al., 2024; Lin et al., 2023）。另一个较少被研究的方向，考虑的是文档本身复杂度的提高（Jiang et al., 2024; Wu et al., 2024b）。与先前的检索数据集相比，这是一项挑战。例如 MS MARCO（Nguyen et al., 2016）包含与查询高度相关的文本块。检索要么通过对文档做词法匹配（lexical match）（Robertson et al., 1994），要么使用把文本嵌入为向量表示的稠密检索器（dense retrievers）（Karpukhin et al., 2020; Ni et al., 2022; Izacard et al., 2022）。与此相关，一些方法（Gao et al., 2021; Chen et al., 2022）探索了混合方案的好处，但这些做法并未成为主流。本文重新考察混合模型，以及面向更复杂文档的检索方法。

我们朝这个方向做的动机来自两点观察：1）文档确实具有结构，例如标题、时间戳、页眉、作者等字段，而且查询可以直接指向这种结构；2）对不同字段而言，不同的评分方法可能各有益处，因为并非每个字段都是回答每条查询所必需的。更具体地说，我们的目标是研究半结构化数据（semi-structured data）上的检索。已有用稠密表示做半结构化数据检索的工作，侧重于通过预训练把半结构化知识直接嵌入模型（Li et al., 2023; Su et al., 2024），而我们希望有一种方法，能更灵活地组合已有的预训练模型与评分器。类似地，多字段检索此前已受到关注，不过那些工作只使用词法或稀疏特征，或早期神经模型（Robertson et al., 1994; Zaragoza et al., 2004; Zamani et al., 2018）。

本文展示如何通过成对视图（paired views）、并按字段来表示多字段文档，同时用一个学到的机制把查询映射为这些视图的加权组合。我们的方法 Multi-Field Adaptive Retrieval（MFAR）是一种检索方法，能够容纳任意数量的字段，以及每个字段上任意数量的评分器（例如每个字段一个词法评分器和一个基于向量的评分器）。1 此外，我们引入一个轻量组件，它以查询为条件，自适应地为最可能的字段加权。这使我们能在推理时穷尽地纳入全部字段与评分器，并由模型决定相对重要性。MFAR 相对现有最先进基线取得了显著的性能提升。与先前工作不同，这一简单方法不需要预训练，并且在测试时提供一定的可控性。具体而言，我们的贡献如下：

1. 我们提出一种面向文档检索的新框架 MFAR，针对具有任意数量字段的半结构化数据。值得注意的是，MFAR 能够在查询与文档各字段之间混合词法评分器与基于向量的评分器。
2. 我们发现，评分器的混合组合优于单独使用稠密评分器或词法评分器；我们还发现，用我们的多字段方式编码文档，可以比把整篇文档作为整体来编码取得更好的性能。因此，MFAR 在半结构化文档检索数据集 STaRK 上达到最先进的性能。
3. 我们提出一种自适应加权技术，它以查询为条件：对与查询最相关的字段赋予更高权重，对较不重要的字段赋予更低权重。
4. 最后，我们分析由该框架训练得到的模型；在消融研究中，我们在测试时控制评分器是否可用，以衡量语料中各个字段的重要性。

1 https://github.com/microsoft/multifield-adaptive-retrieval

## 2 MULTI-FIELD RETRIEVAL 多字段检索

半结构化文档在更一般的意义上是一个宽泛的说法。本文关注可以分解为字段（fields）的文档，每个字段有一个名称和一个值。以图 1 为例，对 STaRK-Prime 文档而言，Entity Type 是字段名，其值为 “drug”。值本身还可以有额外的嵌套结构，例如 Category 的值是一个术语列表。注意，这种半结构化多字段文档的表述是宽泛的：它不仅包括知识库条目这类对象，也包括自由文本（聊天消息、电子邮件）及其关联元数据（时间戳、发件人等）和表格数据。

图 1：传统检索文档（上方），例如 MS MARCO（Nguyen et al., 2016）与 BioASQ（Nentidis et al., 2023）中的文档，是无结构的：自由文本往往直接回答查询。STaRK 数据集中的文档（下方）（Wu et al., 2024b）是半结构化的：每篇文档包含多个字段。查询需要其中某些字段的信息，因此既要跨多个字段汇集证据，也要忽略无关字段。表中可辨认的内容如下。

| Dataset | Example Query | Example Document |
| --- | --- | --- |
| MS MARCO | aleve maximum dose | You should take one tablet every 8 to 10 hours until symptoms abate, . . . |
| BioASQ | What is Piebaldism? | Piebaldism is a rare autosomal dominant disorder of melanocyte development characterized by a congenital white forelock and multiple . . . |
| STaRK-Amazon | Looking for a chess strategy guide from The House of Staunton that offers tactics against Old Indian and Modern defenses. Any recommendations? | Title: Beating the King’s Indian and Benoni Defense with 5. Bd3. Brand: The House of Staunton. Description: ... This book also tells you how to play against the Old Indian and Modern defenses. Reviews: [{reviewerID: 1234, text:...}, {reviewerID: 1235, text:...}, ...] . . . |
| STaRK-MAG | Does any research from the Indian Maritime University touch upon Fe II energy level transitions within the scope of Configuration Interaction? | Title: Radiative transition rates for the forbidden lines in Fe II. Abstract: We report electric quadrupole and magnetic dipole transitions among the levels belonging to 3d 6 4s, 3d 7 and 3d 5 4s 2 configurations of Fe II in a large scale configuration interaction (CI) calculation. ... Authors: N.C. Deb, A Hibbert (Indian Maritime University). . . . |
| STaRK-Prime | What drugs target the CYP3A4 enzyme and are used to treat strongyloidiasis? | Name: Ivermectin. Entity Type: drug. Details: {Description: Ivermectin is a broad-spectrum anti-parasite medication. It was first marketed under..., Half Life: 16 hours}. Target: gene/protein. Indication: For the treatment of intestinal strongyloidiasis due to .... Category: [Cytochrome P-450 CYP3A Inducers, Lactones, ...] . . . |

图 2：文档 \(D\) 与查询 \(Q\) 是 STaRK-MAG 数据集中的例子。查询中被标出的部分对应于 \(D\) 的特定字段。传统检索器（A）把整篇文档与查询打分（例如通过向量相似度）。在（B）中，我们的方法 mFAR 先把 \(D\) 分解为字段，再用词法评分器与基于向量的评分器分别把每个字段与查询打分。由此得到一对字段特定的相似度分数，再用我们的自适应查询条件化方法合成为文档级相似度分数。图中可辨认的文字包括：Abstract: “The CH317OH isotopic form of methanol has been investigated as a far-infrared ...”；Institution: {"Michael Jackson": ["Central Washington University"], "Andrew J. Nichols": ["Edmonds Community College"], "D'Artagnon R. Womack": ["Edmonds Community College"]}；Area of Study: ["Wavelength", "Center frequency", "Laser pumping", "Optoelectronics", "Optics", "Physics", "Optical pumping", "Finite impulse response", "Laser"], …；查询 “Are there any publications from Edmonds Community College on laser pumping methods that explore various emission spectra?”；Standard Retriever 的 Score(Q, D) = 0.5；document sim: 0.5；institution sim: (0.8, 1.0)；area of study sim: (0.5, 0.5)；abstract sim: (0.5, 0)；Field weights: [(0.3, 0.2), (0.4, 0.0), (0.0, 0.1)]；mFAR (Ours) 的 Score(Q, D) = 0.57。分数对之间出现运算符 ⨂。各框之间的连线【抽取不清】。

形式化地，我们考虑文档语料 \(C = \{d_1, d_2, \ldots, d_n\}\)，以及构成每篇文档的一组相关字段 \(F = \{f_1, f_2, \ldots, f_m\}\)，即 \(d = \{f : x_f \mid f \in F\}\)，其中 \(x_f\) 是该字段的值。然后，给定自然语言查询 \(q\)，我们希望有一个评分函数 \(s(q, d)\)，用来对 \(C\) 中的文档排序，使与 \(q\) 最相关的文档得分最高（或位于 top-\(k\) 之内）。\(q\) 可能询问任意字段子集中的值，方式可以是词法的，也可以是语义的。

### 2.1 STANDARD RETRIEVER AND CONTRASTIVE LOSS 标准检索器与对比损失

传统上，\(d\) 被整体建索引。检索器可以使用词法评分器（Robertson et al., 1994）或稠密（基于嵌入的）评分器（Lee et al., 2019; Karpukhin et al., 2020）。像 BM25（Robertson et al., 1994）这样的词法评分器，直接根据词频计算 \(s(q, d)\)。对稠密评分器，文档编码器与查询编码器分别嵌入 \(d\) 与 \(q\)，再用一个简单的相似度函数计算 \(s(q, d)\)；本文使用未归一化的点积。

文档编码器与查询编码器可以用对比损失（contrastive loss）（Izacard et al., 2022）微调。该损失旨在对给定查询 \(q\)，把正（相关）文档 \(d^{+}_{i}\) 与 \(k\) 个负（不相关）文档 \(\mathrm{D}^{-}_{i}\) 分开。先前工作用这一损失训练文档与查询的共享编码器，并用温度 \(\tau\) 来稳定训练：

\[
\mathcal{L}_{c} = -\log \frac{e^{s(q_{i}, d^{+}_{i})/\tau}}{e^{s(q_{i}, d^{+}_{i})/\tau} + \sum_{d^{-}_{i} \in \mathrm{D}^{-}_{i}} e^{s(q_{i}, d^{-}_{i})/\tau}}
\tag{1}
\]

\(\mathcal{L}_{c}\) 是基本的对比损失，它最大化 \(P(d^{+}_{i} \mid q_{i})\)。遵循 Henderson et al. (2017)、Izacard et al. (2022) 与 Chen et al. (2020a)，我们使用批内负样本（in-batch negatives）来高效采样这些负文档：把一个批次（共 \(b\) 篇文档）中的其他正文档 \(d^{+}_{j}\) 当作负样本，并纳入 \(\mathrm{D}^{-}_{i}\)，其中 \(j \neq i\) 且 \(1 \leq j \leq b\)。此外，遵循先前工作（Yang et al., 2019; Ni et al., 2022; Chen et al., 2025），我们可以加入针对 \(P(q_{i} \mid d^{+}_{i})\) 的双向损失。这里，对给定的正文档 \(d^{+}_{j}\)，\(q_{j}\) 是正查询，其余查询 \(q_{i}\)（\(i \neq j\)）成为负查询：

\[
\mathcal{L}_{b} = -\log \frac{e^{s(q_{i}, d^{+}_{i})/\tau}}{e^{s(q_{i}, d^{+}_{i})/\tau} + \sum_{q_{j},\ j \neq i} e^{s(q_{j}, d^{+}_{i})/\tau}}
\tag{2}
\]

（共享）编码器的最终损失为 \(\mathcal{L} = \mathcal{L}_{c} + \mathcal{L}_{b}\)。

### 2.2 MFAR: A MULTI-FIELD ADAPTIVE RETRIEVER MFAR：多字段自适应检索器

因为半结构化文档可以分解为单独的字段（\(d = \{x_f\}_{f \in F}\)），我们可以把查询 \(q\) 与每个字段分别打分。该分数可以通过词法方法或稠密（基于向量的）方法计算。这促使我们修改上面的标准设定：\(s(q, d)\) 可以改为字段级分数与评分方法的加权组合，

\[
s(q, d) = \sum_{f \in F} \sum_{m \in M} w^{m}_{f}\, s^{m}_{f}(q, x_{f}).
\tag{3}
\]

其中，\(s^{m}_{f}(q, x_{f})\) 是用评分方法 \(m \in M\) 计算的、\(q\) 与文档 \(d\) 的字段 \(f\) 之间的分数，\(M\) 是评分方法的集合。对混合模型，\(M = \{\mathrm{lexical}, \mathrm{dense}\}\)。\(w^{m}_{f}\) 是与字段 \(f\) 和评分方法 \(m\) 相关联的权重，可以是学到的。

**Adaptive field selection. 自适应字段选择。** 如上所述，我们的方法使用为每个字段和每个评分器学到的权重 \(w^{m}_{f}\)。这在实践中有用，因为语料中并非每个字段都有用，甚至并非都会被问到，例如无关的数字或内部标识符。此外，查询通常只询问少数字段中的信息，而且这些字段会随查询而变化。

这促使我们把 \(w^{m}_{f}\) 的取值也条件化于 \(q\)，从而让权重适应当前查询：用查询文本决定最重要的字段。我们使用一个适配函数 \(G\)，并令 \(w^{m}_{f} = G(q, f, m)\)。于是，以查询为条件的、或者说自适应的加权和为：

\[
s(q, d) = \sum_{f \in F} \sum_{m \in M} G(q, f, m) \cdot s^{m}_{f}(q, x_{f}).
\tag{4}
\]

为了实现 \(G\)，设 \(\mathbf{q}\) 为 \(q\) 的稠密嵌入，\(a^{m}_{f} \in \mathbb{R}^{|\mathbf{q}|}\) 为可学习参数。于是可以定义 \(G(q, f, m) = {a^{m}_{f}}^{\top}\mathbf{q}\)。我们发现，对所有字段 \(f\) 与评分器 \(m\) 施加非线性会让学习更稳定：\(G(q, f, m) = \mathrm{softmax}(\{{a^{m}_{f}}^{\top}\mathbf{q}\})\)，这正是 MFAR 所使用的形式。

**Multiple scorers and normalization. 多种评分器与归一化。** 我们的一个目标是无缝纳入使用不同方法（词法与稠密）的评分器。然而，不同评分器可能分数的分布尺度并不相同。虽然 \(G\) 在技术上可以学会归一化，我们希望 \(G\) 专注于查询条件化。因此，我们试验对每个字段使用批归一化（batch normalization）（Ioffe & Szegedy, 2015）：它白化分数，并为每个字段和评分器学习新的标量 \(\gamma^{m}_{f}\) 与 \(\beta^{m}_{f}\)。由于这些分数最终用于对比损失的 softmax，\(\gamma^{m}_{f}\) 像一个偏置项，调节每个分数的重要性，而 \(\beta^{m}_{f}\) 没有作用。

请注意，分数白化并不显然有益或必要，尤其是当各评分器已经具有相似分布时（即如果我们只用稠密评分器）。我们把是否加入归一化留作网格搜索中的一个超参数。

**Inference 推理。** 在测试时，目标是按 \(s(q, d)\) 对文档排序，使相关（gold）文档排在最前。因为对整个语料计算 \(|F||M||C|\) 个分数可能很慢，我们使用一种近似。我们先为每个字段和每个评分器确定一个 top-\(k\) 短名单 \(C^{m}_{f}\)，并只对

\[
\bigcup_{f \in F,\ m \in M} C^{m}_{f}
\]

计算完整分数，从而得到最终排序。请注意，这种对 top-\(k\) 文档的不精确近似，不同于传统的后期重排序方法：后者会用查询对每篇文档重新打分，而那不是本文的重点。
