原文件名：mFAR_arXiv2410.20056.pdf

原标题：MULTI-FIELD ADAPTIVE RETRIEVAL

中文标题：多字段自适应检索

作者：Millicent Li¹‡，Tongfei Chen²‡，Benjamin Van Durme³，Patrick Xia³

单位：¹Northeastern University，²Augment Code，³Microsoft

联系方式：li.mil@northeastern.edu，patrickxia@microsoft.com

会议 / arXiv：作为会议论文发表于 ICLR 2025；arXiv:2410.20056v2 [cs.IR] 16 Apr 2025

‡ 工作完成于在 Microsoft 期间。

代码：https://github.com/microsoft/multifield-adaptive-retrieval

<!-- 原 PDF 第 1 页 -->

作为会议论文发表于 ICLR 2025

# 多字段自适应检索

## 摘要

面向搜索以及检索增强生成等任务的文档检索，通常使用非结构化数据集：每篇文档都是自由文本，内部没有显式结构。然而，文档可以具有某种结构，包含文章标题、消息正文或 HTML 标题等字段。为填补这一空白，我们提出多字段自适应检索（Multi-Field Adaptive Retrieval，MFAR）。这是一个灵活框架，能够在半结构化数据上容纳任意数量、任意类型的文档索引。该框架包含两个主要步骤：（1）把已有文档分解为字段，每个字段分别用稠密方法与词法方法独立建索引；（2）学习一个模型，该模型以文档查询为条件，自适应地预测某个字段的重要性，从而对最可能相关的字段进行即时加权。我们发现，这一方法可以按字段类型优化地使用稠密表示与词法表示，在文档排序上显著优于多种现有检索器，并在多字段半结构化数据上达到最先进性能。

## 1 引言

文档检索有许多传统应用，例如网页搜索或问答；作为大语言模型工作流的一部分，例如检索增强生成（retrieval-augmented generation，RAG），它也重新受到关注。一个研究方向致力于提高查询的复杂度与自然程度（Yang et al., 2018；Qi et al., 2019；Jeong et al., 2024；Lin et al., 2023）。另一个较少被研究的方向，考虑的是文档复杂度的提高（Jiang et al., 2024；Wu et al., 2024b）。与先前的检索数据集相比，这是一项挑战。例如 MS MARCO（Nguyen et al., 2016）包含与查询高度相关的文本块。检索要么通过词法匹配在文档上搜索（Robertson et al., 1994），要么使用把文本嵌入为向量表示的稠密检索器（Karpukhin et al., 2020；Ni et al., 2022；Izacard et al., 2022）。与此相关，一些方法（Gao et al., 2021；Chen et al., 2022）探索了混合方案的好处，但这些选项并未成为主流。在本工作中，我们重新审视混合模型，以及面向更复杂文档的检索方法。

我们朝这个方向前进，动机来自两点观察：1）文档确实有结构，例如标题、时间戳、页眉、作者等字段，而且查询可以直接指向这种结构；2）这些字段各自可能适合不同的打分方法，因为并不是每个字段都是回答每一条查询所必需的。更具体地说，我们的目标是研究半结构化数据上的检索。

现有针对半结构化数据、使用稠密表示的检索工作，侧重于通过预训练把半结构化知识直接嵌入模型（Li et al., 2023；Su et al., 2024）。我们则希望有一种方法，能够更灵活地组合已有的预训练模型与打分器。类似地，多字段检索此前已受到关注，不过那些工作聚焦于仅使用词法或稀疏特征、或早期神经模型的检索（Robertson et al., 1994；Zaragoza et al., 2004；Zamani et al., 2018）。

在本工作中，我们展示如何通过成对视图、并在逐字段的基础上表示多字段文档，同时用一种学得的机制把查询映射为这些视图的加权组合。我们的方法 MFAR¹ 是一种检索方法，可以为每个字段容纳任意数量的字段，以及任意数量的打分器（例如一个词法打分器和一个

<!-- 原 PDF 第 2 页 -->

作为会议论文发表于 ICLR 2025

**图 1：** 传统检索文档（上），例如 MS MARCO（Nguyen et al., 2016）和 BioASQ（Nentidis et al., 2023）中的文档，是非结构化的：自由文本往往直接回答查询。STaRK 数据集中的文档（下）（Wu et al., 2024b）是半结构化的：每篇文档包含多个字段。查询需要其中某些字段的信息，因此既要跨多个字段汇集证据，又要忽略无关字段。

| 数据集 | 示例查询 | 示例文档 |
| --- | --- | --- |
| MS MARCO | Aleve 的最大剂量 | 应每 8 到 10 小时服用一片，直至症状减轻，…… |
| BioASQ | 什么是斑驳病（Piebaldism）？ | 斑驳病是一种罕见的常染色体显性黑素细胞发育障碍，特征为先天性白额发以及多处…… |
| STaRK-Amazon | 想找一本 The House of Staunton 出版的国际象棋战略指南，其中提供针对古印度防御和现代防御的战术。有推荐吗？ | 标题：用 5. Bd3 击败王翼印度防御与别诺尼防御。品牌：The House of Staunton。描述：……本书还告诉你如何应对古印度防御和现代防御。评论：[{reviewerID: 1234, text:…}, {reviewerID: 1235, text:…}, …] …… |
| STaRK-MAG | Indian Maritime University 有没有研究在组态相互作用（Configuration Interaction）范围内讨论 Fe II 能级跃迁？ | 标题：Fe II 禁线的辐射跃迁速率。摘要：我们报告了在大规模组态相互作用（CI）计算中，属于 3d 6 4s、3d 7 以及 3d 5 4s 2 组态的 Fe II 能级之间的电四极与磁偶极跃迁。……作者：N.C. Deb，A Hibbert（Indian Maritime University）。…… |
| STaRK-Prime | 哪些药物以 CYP3A4 酶为靶点，并用于治疗粪类圆线虫病（strongyloidiasis）？ | 名称：Ivermectin。实体类型：drug。详情：{描述：伊维菌素是一种广谱抗寄生虫药物。它最初以……的商品名上市，半衰期：16 小时}。靶点：gene/protein。适应症：用于治疗由……引起的肠道粪类圆线虫病。类别：[Cytochrome P-450 CYP3A Inducers, Lactones, …]。…… |

基于向量的打分器）。此外，我们引入一个轻量组件，以查询为条件，自适应地为最可能相关的字段赋予权重。这样就可以在推理时穷尽地包含所有字段和打分器，并让模型判断相对重要性。MFAR 相对于现有最先进基线获得了显著的性能提升。与先前工作不同，我们这一简单方法不需要预训练，并在测试时提供一定的可控性。具体贡献如下：

1. 我们提出面向文档检索的新框架 MFAR，针对具有任意数量字段的半结构化数据。值得注意的是，MFAR 能够在查询与文档字段之间混合词法打分器与基于向量的打分器。
2. 我们发现，打分器的混合组合优于单独使用稠密或词法打分器；用多字段方法编码文档，也可以比把整篇文档作为整体编码取得更好的性能。因此，MFAR 在半结构化文档检索数据集 STaRK 上达到最先进性能。
3. 我们引入以查询为条件的自适应加权技术，提高与查询最相关字段的权重，降低较不重要字段的权重。
4. 最后，我们分析由该框架训练出的模型；在消融中于测试时控制打分器是否可用，以衡量语料里各个字段的重要性。

## 2 多字段检索

半结构化文档是一个更宽泛的说法。在本工作中，我们关注可以分解为字段的文档，每个字段有名称和值。以图 1 中的 STaRK-Prime 文档为例，Entity Type 是字段名，其值为 “drug”。字段值本身还可以有进一步的嵌套结构，例如 Category 的值是一个术语列表。注意，这种半结构化多字段文档的表述范围很广：它不仅包括知识库条目这类对象，也包括自由文本（聊天消息、电子邮件）及其关联元数据（时间戳、发件人等），以及表格数据。

<!-- 原 PDF 第 3 页 -->

作为会议论文发表于 ICLR 2025

**图 2：** 文档 D 与查询 Q 是 STaRK-MAG 数据集中的例子。查询中被标出的部分对应于 D 的特定字段。传统检索器（A）会把整篇文档与查询打分（例如通过向量相似度）。在（B）中，我们的方法 MFAR 先把 D 分解为字段，再用词法打分器与基于向量的打分器分别把每个字段与查询打分。这样就得到一对字段特定的相似度分数，再用自适应的查询条件化方法把它们合成为文档级相似度分数。

图中内容（示意）：

- 文档 D 的字段示例：摘要（Abstract）：“甲醇的 CH317OH 同位素形式已被作为远红外……加以研究。”（公式抽取不完整，见原 PDF 第 3 页）机构（Institution）：{"Michael Jackson": ["Central Washington University"], "Andrew J. Nichols": ["Edmonds Community College"], "D'Artagnon R. Womack": ["Edmonds Community College"]}。研究领域（Area of Study）：[“波长”、“中心频率”、“激光抽运”、“光电子学”、“光学”、“物理学”、“光抽运”、“有限冲激响应”、“激光”，……]。原文列表为 ["Wavelength", "Center frequency", "Laser pumping", "Optoelectronics", "Optics", "Physics", "Optical pumping", "Finite impulse response", "Laser”, …]。
- 查询 Q：Edmonds Community College 有没有关于激光抽运方法、并探讨各种发射光谱的论文？
- 标准检索器：Score(Q, D) = 0.5。
- MFAR（本文）：institution 相似度 (0.8, 1.0)；area of study 相似度 (0.5, 0.5)；abstract 相似度 (0.5, 0)；document 相似度 0.5；字段权重 [(0.3, 0.2), (0.4, 0.0), (0.0, 0.1)]；Score(Q, D) = 0.57。

形式上，我们考虑文档语料 $\mathcal{C}=\{d_1,d_2,\ldots,d_n\}$，以及构成每篇文档 $d$ 的关联字段集合 $\mathcal{F}=\{f_1,f_2,\ldots,f_m\}$，即 $d=\{f:x_f\mid f\in\mathcal{F}\}$，其中 $x_f$ 是该字段的值。然后，给定自然语言查询 $q$，我们希望有一个打分函数 $s(q,d)$，用来对 $\mathcal{C}$ 中的文档排序，使与 $q$ 最相关的文档得分最高（或进入前 $k$）。$q$ 可能会询问任意字段子集中的值，方式可以是词法上的，也可以是语义上的。

### 2.1 标准检索器与对比损失

传统上，$d$ 是作为整体被索引的。检索器可以使用词法打分器（Robertson et al., 1994）或稠密（基于嵌入的）打分器（Lee et al., 2019；Karpukhin et al., 2020）。像 BM25（Robertson et al., 1994）这样的词法打分器，直接根据词项频率计算 $s(q,d)$。对于稠密打分器，用文档编码器和查询编码器嵌入 $d$ 与 $q$，再用一个简单的相似度函数计算 $s(q,d)$；在我们这里，用的是未归一化的点积。

文档编码器与查询编码器可以用对比损失进行微调（Izacard et al., 2022）。其目标是：对给定查询 $q$，把正例（相关）文档 $d_i^{+}$ 与 $k$ 个负例（不相关）文档 $\mathcal{D}_i^{-}$ 分开。在先前工作中，文档和查询共用一个编码器，并用温度 $\tau$ 训练以保持稳定：

$$
\mathcal{L}_{c}=-\log\frac{e^{s(q_i,d_i^{+})/\tau}}{e^{s(q_i,d_i^{+})/\tau}+\sum_{d_i^{-}\in\mathcal{D}_i^{-}}e^{s(q_i,d_i^{-})/\tau}}
\tag{1}
$$

$\mathcal{L}_{c}$ 是基本的对比损失，它最大化 $P(d_i^{+}\mid q_i)$。遵循 Henderson et al. (2017)、Izacard et al. (2022) 以及 Chen et al. (2020a)，我们使用批内负例，以便高效采样这些负文档：把批次中（共 $b$ 篇文档）的其他正文档 $d_j^{+}$ 当作负例，并纳入 $\mathcal{D}_i^{-}$，其中 $j\neq i$ 且 $1\leq j\leq b$。此外，遵循先前工作（Yang et al., 2019；Ni et al., 2022；Chen et al., 2025），我们可以加入针对 $P(q_i\mid d_i^{+})$ 的双向损失。此时，对给定正文档 $d_j^{+}$，$q_j$ 是正查询，其他查询 $q_i$（$i\neq j$）成为负查询：

$$
\mathcal{L}_{b}=-\log\frac{e^{s(q_i,d_i^{+})/\tau}}{e^{s(q_i,d_i^{+})/\tau}+\sum_{q_j,\,j\neq i}e^{s(q_j,d_i^{+})/\tau}}
\tag{2}
$$

<!-- 原 PDF 第 4 页 -->

作为会议论文发表于 ICLR 2025

（共享）编码器的最终损失为 $\mathcal{L}=\mathcal{L}_{c}+\mathcal{L}_{b}$。

### 2.2 MFAR：多字段自适应检索器

由于半结构化文档可以分解为单独的字段（$d=\{x_f\}_{f\in\mathcal{F}}$），我们可以把查询 $q$ 与每个字段分别打分。这个分数可以用词法方法或稠密（基于向量的）方法计算。这就促使我们对上面的标准设置做一处修改：$s(q,d)$ 可以改为字段级分数与打分方法的加权组合，

$$
s(q,d)=\sum_{f\in\mathcal{F}}\sum_{m\in\mathcal{M}}w_{f}^{m}\,s_{f}^{m}(q,x_f).
\tag{3}
$$

这里，$s_{f}^{m}(q,x_f)$ 是用打分方法 $m\in\mathcal{M}$ 得到的、$q$ 与文档 $d$ 的字段 $f$ 之间的分数，$\mathcal{M}$ 是打分方法集合。对混合模型，$\mathcal{M}=\{\text{lexical},\text{dense}\}$。$w_{f}^{m}$ 是与字段 $f$ 和打分方法 $m$ 相关联的权重，可以是学出来的。

**自适应字段选择。** 按上面的表述，我们的方法使用为每个字段和每个打分器学得的权重 $w_{f}^{m}$。这在实践中有用，因为语料里并不是每个字段都有用、甚至会被问到，例如无关的数字或内部标识符。另外，查询通常只询问少量字段中包含的信息，而且这些字段会随查询变化。

这就促使我们让 $w_{f}^{m}$ 的取值也以 $q$ 为条件，从而权重能够适应当前查询：用查询文本来决定最重要的字段。我们使用一个适配函数 $G$，并令 $w_{f}^{m}=G(q,f,m)$。于是，以查询为条件的、或者说自适应的加权和为：

$$
s(q,d)=\sum_{f\in\mathcal{F}}\sum_{m\in\mathcal{M}}G(q,f,m)\cdot s_{f}^{m}(q,x_f).
\tag{4}
$$

为实现 $G$，令 $\mathbf{q}$ 为 $q$ 的稠密嵌入，$\mathbf{a}_{f}^{m}\in\mathbb{R}^{|\mathbf{q}|}$ 为可学习参数。然后可以定义 $G(q,f,m)=\mathbf{a}_{f}^{m\top}\mathbf{q}$。我们发现，若在所有字段 $f$ 和打分器 $m$ 上加一个非线性，学习会更稳定：$G(q,f,m)=\mathrm{softmax}(\{\mathbf{a}_{f}^{m\top}\mathbf{q}\})$。MFAR 使用的就是这个形式。

**多种打分器与归一化。** 我们的一个目标，是无缝纳入使用不同方法（词法与稠密）的打分器。然而，每种打分器可能分数的分布处于不同尺度。虽然 $G$ 技术上可以学会做归一化，我们希望 $G$ 专注于查询条件化。作为替代，我们试验对每个字段使用批归一化（Ioffe & Szegedy, 2015）：它把分数白化，并为每个字段和打分器学习新的标量 $\gamma_{f}^{m}$ 与 $\beta_{f}^{m}$。因为这些分数最终用在对比损失的 softmax 中，$\gamma_{f}^{m}$ 的作用类似偏置项，调节每个分数的重要性，而 $\beta_{f}^{m}$ 没有影响。

需要注意，分数白化并不显然有益或必要，尤其是当打分器已经共享相似分布时（也就是如果我们只用稠密打分器）。我们把是否纳入归一化留作超参数，作为网格搜索的一部分。

**推理。** 测试时，目标是按 $s(q,d)$ 对文档排序，使相关（金标）文档排在最前。因为对整个语料计算 $|\mathcal{F}|\,|\mathcal{M}|\,|\mathcal{C}|$ 个分数可能很慢，我们使用一种近似。我们首先为每个字段和每个打分器确定一个前 $k$ 的候选短名单 $\mathcal{C}_{f}^{m}$，并且只对所有 $\bigcup_{f\in\mathcal{F},\,m\in\mathcal{M}}\mathcal{C}_{f}^{m}$ 计算完整分数，由此得到最终排序。注意，这种对前 $k$ 文档的不精确近似，不同于传统的后期重排序方法——那些方法会用每篇文档对查询重新打分，而这并不是本工作的重点。

## 3 实验

我们的实验由以下假设驱动：

1. 利用多字段文档结构，会比把文档整体当作单一字段来处理得到更高的准确率。
2. 混合建模（词法与稠密的组合）会比只用其中一种更好。

<!-- 原 PDF 第 5 页 -->

作为会议论文发表于 ICLR 2025

### 3.1 数据

我们使用 STaRK（Wu et al., 2024b）。它是一组检索数据集，包含三个领域：产品评论（Amazon）、学术文章（MAG）和生物医学知识（Prime），均由知识图谱派生。Amazon 包含来自 Amazon Product Reviews（He & McAuley, 2016）和 Amazon Question and Answer Data（McAuley et al., 2015）的查询与文档。MAG 包含关于学术论文的查询与文档，来源是 Microsoft Academic Graph（Wang et al., 2020）、obgn-MAG 以及 obgn-papers100M（Hu et al., 2020）。Prime 包含来自 PrimeKG（Chandak et al., 2022）的生物医学查询与文档。在 STaRK 中，这些数据集被表述为知识图谱，并配有复杂查询。

在检索基线中（Wu et al., 2024b），节点（对应于知识图谱中的一个实体）信息被线性化成文档，从而可以用稠密方法编码和检索。我们同样把每个节点当作一篇文档。在本工作中，对多字段模型，我们把每个节点属性或关系保留为单独的字段；对单字段模型，我们同样把它重排成人类可读的文档。与 Amazon 和 MAG 相比，我们注意到 Prime 的关系类型更多，也就是说，Prime 中相对更多的字段来自知识图谱关系；而在 Amazon 或 MAG 中，文档内容来自节点的属性。Prime、Amazon 和 MAG 的字段数分别为 22、8 和 5。数据集规模、预处理和具体字段的更多细节见附录 A。

我们使用 trec_eval² 进行评测，并遵循 Wu et al. (2024b)，报告 Hit@1、Recall@20 和平均倒数排名（MRR）。由于篇幅限制，Hit@5 放在附录 C.1。

² https://github.com/usnistgov/trec_eval

### 3.2 基线与先前工作

我们主要与 STaRK 上的先前工作比较，即 Wu et al. (2024b) 建立的一组基线，以及 Wu et al. (2024a) 更新的工作。具体而言，其中包含两种使用 OpenAI 的 text-embedding-ada-002 模型的向量相似度搜索方法：ada-002 和 multi-ada-002。值得注意的是，后者也是一种多向量方法，不过每篇文档只用两个向量：一个捕捉节点属性，一个表示关系信息。我们还纳入他们在 ada-002 之上的两个基于大语言模型的重排序基线（Claude3 与 GPT4 重排序器）。虽然本工作不做重排序，我们仍加入这些结果，以表明微调较小的检索器，优于用通用大语言模型做重排序。

较新的 AvaTaR（Wu et al., 2024a）是一种基于智能体的方法，它迭代地生成提示，以改进对文档的推理和打分。它与我们的工作并不可比——我们既不关注智能体，也不使用那么大的模型——但它是 STaRK 上的最先进方法。

最后，我们使用一个现成的预训练检索编码器作为稠密打分器的基线：在 MS MARCO 上微调过的 Contriever³（Izacard et al., 2022），随后我们继续在 STaRK 上微调它。早期实验表明，Contriever 优于其他稠密检索器。我们用 BM25（Robertson et al., 1994；Lù, 2024）作为词法基线。这些基线使用第 3.1 节所述的单字段格式。

³ https://huggingface.co/facebook/contriever-msmarco

### 3.3 实验设置

MFAR 允许在各实验中组合词法打分器与稠密打分器。与基线类似，我们用 BM25 作为词法打分器，用 Contriever 嵌入的点积作为稠密打分器。查询和文档共用一个嵌入模型；计算适配函数 $G$ 时构造 $\mathbf{q}$ 也用这个模型。由于各数据集可能存在差异，我们首先考虑四种配置，以利用 MFAR 容纳多个字段或多个打分器的能力：MFARDense 使用全部字段和稠密打分器；MFARLexical 使用全部字段和词法打分器；MFARAll 使用全部字段和两种打分器；MFAR2 使用两种打分器，但采用单字段（第 3.1 节）文档表示。根据最终结果与分析，我们另外构建并评测 MFARAll+2：它对词法和稠密两种打分方法，同时包含单文档表示和多字段表示。这样就得到五个 MFAR 模型，使用的打分器数量分别为 $|\mathcal{F}|$、$|\mathcal{F}|$、$2|\mathcal{F}|$、$2$ 和 $2|\mathcal{F}|+2$。对每个数据集（以及各个模型），

<!-- 原 PDF 第 6 页 -->

作为会议论文发表于 ICLR 2025

我们在学习率以及是否做归一化上进行网格搜索，并依据开发集选择最佳模型。

由于 Contriever 的上下文窗口为 512 个词元，我们优先把每个字段的这一窗口用满，这最终限制了每个数据集可选的批大小：Amazon 和 Prime 为 96，MAG 为 192。每次运行的具体超参数见附录 B。

## 4 结果

我们在表 1 中报告 MFAR 模型的结果，并与先前方法和基线比较。我们最好的模型都使用了两种打分器，它们显著优于先前工作和基线：Amazon 上是 MFAR2，其他数据集上是 MFARAll 和 MFARAll+2。这包括超过基于重排序的方法，以及最强的智能体方法 AvaTaR。MFARAll 在 Prime 上表现尤其好（Hit@1 为 +20%）。相比之下，所有基于 ada-002 的模型都有 2K 词元的扩展上下文窗口，而 MFAR 使用的编码器上下文窗口小得多（512），性能仍然显著更好。此外，这些收益不能只归因于微调，也不能只归因于完全依赖词法打分器，因为 MFAR 模型优于已经很有竞争力的 BM25 基线和微调后的 Contriever 基线。

我们发现，采用混合方法有利于 Recall。这可以归因于成功整合了 BM25 的分数。单独来看，BM25 的 Recall@20 已经高于大多数基于向量的方法。MFAR 模型保持并进一步提高了这一性能。对于 RAG 这类任务，Recall 尤其重要：把文档收集进前 $k$ 个结果，比把正确答案排到最顶部更重要。

回到第 3 节的假设，我们可以比较 MFAR 的各种配置。注意到 BM25 相当于单字段的词法基线，Contriever-FT 相当于单字段的稠密基线，我们可以观察到以下几点。

**多字段与单字段。** 把单字段模型与其多字段对应模型并排比较，结果是混合的。如果只考虑稠密打分器，MFARDense 在所有数据集上都优于 Contriever-FT。据我们所知，这是支持稠密检索中多字段方法的第一项正面证据。对于 MFARLexical，在 Amazon 和 MAG 上，BM25 基线表现特别好，我们没有看到一致的提升。Robertson et al. (2004) 此前已经指出过这一具体现象。他们描述了 BM25F，即 BM25 的一个变体，它以更有原则的方式聚合多字段信息。

**表 1：** 在 STaRK 测试集上，将我们的方法（MFAR）与基线及最先进方法比较。ada-002 和 multi-ada-002 基于向量相似度；+{Claude3, GPT4} 进一步在 ada-002 之上加入大语言模型重排序步骤。AvaTaR 是基于智能体的迭代框架。Contriever-FT 是微调后的 Contriever 模型，也是 MFAR 中被微调的那个编码器。MFAR 优于先前方法和各数据集上的结果，并且在该基准的平均指标上取得大幅优势。♦ 在 Wu et al. (2024b) 中，这些是重排序模型，只在查询的一个随机 10% 子集上运行。

| 模型 | Amazon Hit@1 | Amazon Recall@20 | Amazon MRR | MAG Hit@1 | MAG Recall@20 | MAG MRR | Prime Hit@1 | Prime Recall@20 | Prime MRR | 平均 Hit@1 | 平均 Recall@20 | 平均 MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ada-002 | 0.392 | 0.533 | 0.542 | 0.291 | 0.484 | 0.386 | 0.126 | 0.360 | 0.214 | 0.270 | 0.459 | 0.381 |
| multi-ada-002 | 0.401 | 0.551 | 0.516 | 0.259 | 0.508 | 0.369 | 0.151 | 0.381 | 0.235 | 0.270 | 0.480 | 0.373 |
| Claude3♦ | 0.455 | 0.538 | 0.559 | 0.365 | 0.484 | 0.442 | 0.178 | 0.356 | 0.263 | 0.333 | 0.459 | 0.421 |
| GPT4♦ | 0.448 | 0.554 | 0.557 | 0.409 | 0.486 | 0.490 | 0.183 | 0.341 | 0.266 | 0.347 | 0.460 | 0.465 |
| AvaTaR agent | 0.499 | 0.606 | 0.587 | 0.444 | 0.506 | 0.512 | 0.184 | 0.393 | 0.267 | 0.376 | 0.502 | 0.455 |
| BM25 | 0.483 | 0.584 | 0.589 | 0.471 | 0.689 | 0.572 | 0.167 | 0.410 | 0.255 | 0.374 | 0.561 | 0.462 |
| Contriever-FT | 0.383 | 0.530 | 0.497 | 0.371 | 0.578 | 0.475 | 0.325 | 0.600 | 0.427 | 0.360 | 0.569 | 0.467 |
| MFARLexical | 0.332 | 0.491 | 0.443 | 0.429 | 0.657 | 0.522 | 0.257 | 0.500 | 0.347 | 0.339 | 0.549 | 0.437 |
| MFARDense | 0.390 | 0.555 | 0.512 | 0.467 | 0.669 | 0.564 | 0.375 | 0.698 | 0.485 | 0.411 | 0.641 | 0.520 |
| MFAR2 | 0.574 | 0.663 | 0.681 | 0.503 | 0.721 | 0.603 | 0.227 | 0.495 | 0.327 | 0.435 | 0.626 | 0.537 |
| MFARAll | 0.412 | 0.585 | 0.542 | 0.490 | 0.717 | 0.582 | 0.409 | 0.683 | 0.512 | 0.437 | 0.662 | 0.545 |
| MFARAll+2 | 0.530 | 0.663 | 0.643 | 0.559 | 0.741 | 0.643 | 0.400 | 0.726 | 0.520 | 0.496 | 0.710 | 0.602 |

<!-- 原 PDF 第 7 页 -->

作为会议论文发表于 ICLR 2025

具体到 BM25，其分数按长度归一化。对某些字段，例如机构，重复并不意味着更强的匹配，因此把机构字段单独处理（并给它预测出很高的权重）可能导致负文档得到高分。于是，多字段稀疏表示未必总是最好的方案，这取决于数据集。我们进一步尝试改用 BM25F，但发现性能平平，原因很可能是权重欠调（附录 D）。鉴于 STaRK 数据集的字段数量，调节字段权重是一个困难且开放的问题；对 BM25F 来说，它似乎不如对 MFAR 那样可行。最后，我们注意到，把多字段与单字段结合起来可以带来进一步收益，如 MFARAll+2 所示（以及附录 C.2）。

**混合最好。** 无论是多字段模型（MFARAll 对比 MFARDense 或 MFARLexical）还是单字段模型（MFAR2 对比 BM25 或 Contriever-FT），并且在几乎每个数据集上，同时使用两种打分器都比只使用单一类型的打分器有性能提升，这验证了我们较早的假设。这也加强了先前工作的发现（Gao et al., 2021；Kuzi et al., 2020）：混合方法效果好。唯一的例外（Prime 上的单字段）对单字段模型可能较难，原因可能是该数据集的字段数量相对更多，以及这些字段的语义，我们在第 5.3 节做了更多考察。然而，在 Prime 的多字段设定下，我们再次看到混合方法最好。这为我们最初的动机提供了证据：混合模型适合某些半结构化、多字段文档，并带来正面收益。

## 5 分析

接下来，我们更深入地考察 MFAR 为何带来提升。我们首先验证模型确实对查询具有自适应性，表明查询条件化是 MFAR 的必要组成部分。因为字段权重天然可解释、也可控，我们可以手动设置权重，对模型做事后分析。这既能告诉我们，对给定查询而言数据集的哪些字段重要，也能告诉我们模型在每个字段上受益于稠密打分器、词法打分器，还是两者都有。最后，我们做定性分析，以提出 MFAR 具有优势的原因。

我们的分析与定量结果一起，促使我们在附录 C.2 中试验单字段与多字段文档表示的组合，例如 MFARAll+2。我们发现，这些组合相对于 MFARAll 提供了额外收益；甚至只把单字段词法与多字段稠密组合起来，也优于单独的 MFARAll 或 MFAR2。

### 5.1 以查询为条件的自适应是否必要？

我们为 MFAR 设计了自适应字段选择机制：对一条测试时查询，模型在各字段上做出加权预测，以决定哪些字段重要。在本节中，我们分析这种自适应是否为取得良好性能所必需。为此，我们将 MFAR 与一个消融版本对比：该版本不能预测查询特定的权重，但仍然可以通过直接学习式 (3) 中的 $w_{f}^{m}$ 来预测全局的、字段特定的权重。这样，如果某些字段在全局上被认为重要（或不重要），模型仍然可以强调（或减弱）它们。

**表 2：** 去掉查询条件化（QC）后 MFARAll 的测试分数，以及去掉之后的相对变化百分比。

|  | Amazon Hit@1 | Amazon Recall@20 | Amazon MRR | MAG Hit@1 | MAG Recall@20 | MAG MRR | Prime Hit@1 | Prime Recall@20 | Prime MRR | STaRK 平均 Hit@1 | STaRK 平均 Recall@20 | STaRK 平均 MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| MFARAll | 0.412 | 0.585 | 0.542 | 0.490 | 0.717 | 0.582 | 0.409 | 0.683 | 0.512 | 0.437 | 0.662 | 0.545 |
| 无 QC | 0.346 | 0.547 | 0.473 | 0.428 | 0.662 | 0.528 | 0.241 | 0.596 | 0.368 | 0.338 | 0.602 | 0.456 |
| 损失（%） | -16.0 | -6.5 | -12.7 | -12.7 | -7.7 | -9.3 | -41.1 | -12.7 | -28.1 | -22.6 | -9.1 | -16.3 |

在表 2 中，我们给出 MFARAll 的细节，并发现查询条件化对于所有数据集上的性能提升确实是必要的。去掉它，会在每个数据集的指标上以及 STaRK 平均值上造成大幅损失。这一点也延伸到其他模型。我们还发现，STaRK 平均值在 3 项指标（Hit@1、Recall@20、MRR）上更低：MFARDense 为 -10%、-6%、-8%，MFARLexical 为 -17%、-13%、-14%。

<!-- 原 PDF 第 8 页 -->

作为会议论文发表于 ICLR 2025

### 5.2 哪些字段和打分器是重要的？

MFAR 框架的可解释设计，使我们能够在模型训练完成之后，方便地控制所使用的字段和打分器。具体而言，我们可以把用于计算 $s(q,d)$（式 4）的权重 $w_{f}^{m}$ 的任意子集掩码（置零）。例如，对每个 $f$ 设 $w_{f}^{\mathrm{lexical}}=0$，就会迫使模型对每个字段只使用稠密分数。我们可以把性能下降直接解释为排除了某些字段或打分器的结果，从而衡量它们的贡献（或缺乏贡献）。在这一深入分析中，我们在掩掉整类打分方法（词法或稠密）、特定字段（标题、摘要等），乃至特定的字段与打分方法组合（例如标题配稠密打分器）之后，重新评测 MFARAll 在每个数据集上的性能。

**打分器。** 我们在表 3 中给出三个 STaRK 数据集上的结果。可以看到，MFARAll 在 Amazon 上的性能严重依赖稠密分数。知道表 1 的结果后，这也许并不意外，因为 MFARLexical 的表现最差。模型在 Prime 上同样偏向稠密分数；而在 MAG 上，它更多依赖词法分数。这说明每个数据集可能受益于不同的打分器。进一步说，这未必能事先预料到：我们本会预期 Prime 最受益于词法分数，因为这个生物医学数据集包含许多在语义上并不清晰的首字母缩写和 ID。这展示了 MFAR 对多种打分策略的灵活性与自适应性。

从表 1 我们观察到，MFARAll 以很小的幅度优于 MFARDense（平均 Hit@1 为 0.435 对 0.411），因此人们可能会怀疑 MFARAll 严重依赖稠密分数。然而，把 $w_{f}^{\mathrm{lexical}}$ 掩掉之后的 MFARAll，在每个数据集上都明显更差（表 3；平均 0.326），差于 MFARDense。这表明 MFARAll 的性能中有不可忽略的一部分来自词法分数。因此，与检索中的后期重排序或路由模型不同，训练期间稠密打分器与词法打分器（乃至各个字段）的共存，很可能会影响模型和编码器学到的内容。

**表 3：** 在测试时把整类打分方法掩掉之后，MFARAll 的性能。

| 掩码 | Amazon Hit@1 | Amazon Recall@20 | Amazon MRR | MAG Hit@1 | MAG Recall@20 | MAG MRR | Prime Hit@1 | Prime Recall@20 | Prime MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 无 | 0.412 | 0.586 | 0.542 | 0.490 | 0.717 | 0.582 | 0.409 | 0.683 | 0.512 |
| 仅稠密：$w_{f}^{\mathrm{lexical}}=0$ | 0.389 | 0.553 | 0.512 | 0.257 | 0.481 | 0.355 | 0.331 | 0.635 | 0.352 |
| 仅词法：$w_{f}^{\mathrm{dense}}=0$ | 0.271 | 0.452 | 0.386 | 0.352 | 0.602 | 0.446 | 0.267 | 0.500 | 0.442 |

**字段。** 在更细的字段层面做类似分析，我们可以识别文档的哪些部分被问到或有用。对每个字段 $f_i$，我们可以设 $w_{f_i}^{\mathrm{lexical}}=0$、$w_{f_i}^{\mathrm{dense}}=0$，或两者都置零。我们从每个数据集中收集若干有意思的字段放入表 4，全部字段见附录 E。

我们发现，行为随字段而变化。对某些字段（MAG 的 authors、Amazon 的 title），掩掉其中一个打分器几乎不引起变化。然而，掩掉另一个打分器会造成幅度可观的下降，其大小与把该字段的两种打分器都掩掉相近。在这种情况下，一种解释是：在 MFARAll 内部，$s_{\mathrm{author}}^{\mathrm{dense}}(q,d)$ 和 $s_{\mathrm{title}}^{\mathrm{lexical}}(q,d)$ 并不有用。

为简化模型，人们可能会建议：只要把 $w_{f}^{m}$ 设为 0 不会造成下降，就把对应的 $s_{f}^{m}(q,d)$ 去掉。然而，我们不能这样做，否则会伤害模型。换句话说，很小的差值并不表示重要性很低。对某些字段（例如 Amazon 的 qa、MAG 的 title，或 Prime 的 phenotype absent），当词法或稠密打分器被单独置零时，分数大体不受影响。然而，把两种打分器都置零、从而完全去掉该字段，会造成明显下降。在许多情况下，我们观察到掩掉整个字段带来的下降，大于单独掩掉其中任何一种打分器。这种行为可能是因为 MFAR 用不同打分器冗余地获取了相同的相似度信息。相反，字段之间也存在信息重叠，因此在某些情况下可以去掉整个字段而不造成大幅下降，尤其是在 Prime（例如 enzyme）和 Amazon 中。

<!-- 原 PDF 第 9 页 -->

作为会议论文发表于 ICLR 2025

**表 4：** 对每个数据集，从 MFARAll 中掩掉某些字段和打分器之后，Hit@1 与 Recall@20 的绝对变化（delta）。对每个字段，我们置零词法打分器、稠密打分器，或两者都置零。每个数据集中全部字段、全部指标的原始分数见附录 E。文本流中 authors 一行出现在 MAG 节标题之前；按默认 `find_tables` 的结果以及正文（MAG 的 authors），将该行归入 MAG。

| 数据集 | 字段 | $w_{f}^{\mathrm{lexical}}=0$ 的 Hit@1 | $w_{f}^{\mathrm{lexical}}=0$ 的 Recall@20 | $w_{f}^{\mathrm{dense}}=0$ 的 Hit@1 | $w_{f}^{\mathrm{dense}}=0$ 的 Recall@20 | 两者都置零的 Hit@1 | 两者都置零的 Recall@20 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Amazon | qa | 0 | 0 | 0 | 0 | -0.031 | -0.041 |
| Amazon | title | 0.002 | -0.003 | -0.022 | -0.031 | -0.023 | -0.024 |
| MAG | authors | -0.152 | -0.117 | 0 | 0 | -0.101 | -0.086 |
| MAG | title | -0.011 | -0.003 | -0.017 | -0.014 | -0.076 | 0.063 |
| Prime | phenotype absent | -0.001 | -0.002 | 0 | 0 | -0.033 | -0.030 |
| Prime | enzyme | 0 | 0 | 0 | 0 | -0.004 | -0.006 |

**图 3：** 各种 MFAR 所选出的最高分文档片段。上：单字段混合模型（MFAR2）对比 MFARAll。MFARAll 选对了，而 MFAR2 可能被查询中的否定所干扰。下：能够使用不同打分器的 MFAR 配置所给出的片段。只有 MFARAll 正确地同时利用了跨字段的词法匹配与语义匹配。

查询：哪个基因或蛋白质在雌性性腺组织中不表达？

- MFAR2：名称：NUDT19P5；类型：基因/蛋白质（gene/protein）；表达存在（expression present）：{解剖部位：雌性性腺（female gonad）}
- MFARAll：名称：HSP90AB3P；类型：基因/蛋白质（gene/protein）；表达缺失（expression absent）：{解剖部位：[小脑（cerebellum），雌性性腺（female gonad）]}

查询：Arxiv 上有没有 Eckerd College 关于中子物理中 $^6$He 中子散射的研究论文？（原文写为 6He。）

- MFARLexical：摘要：一台新的针孔小角中子散射（SANS）谱仪，安装在核物理研究所 20 MW 中国绵阳研究堆（CMRR）的冷中子源上……作者：Mei Peng（China Academy of Engineering Physics），Guanyun Yan（China Academy of Engineering Physics），Qiang Tian（China Academy of Engineering Physics），……
- MFARDense：摘要：对 54Fe 的中子弹性与非弹性散射截面进行了测量，入射中子能量在 2 到 6 MeV 之间共九个能量点……被引论文：1.5 至 4.5 MeV 的 23Na 中子散射微分截面，54Fe 上的中子非弹性散射。研究领域：[弹性散射、物理学、非弹性散射、中子、直接耦合、原子物理、散射，……]
- MFARAll：摘要：……用微观折叠光学势描述 $^6$He 在质子靶上的散射，其中 $^6$He 核被描述为带有两个额外价中子、处于价 p 壳层的 $^4$He 核心。与先前同类工作不同，价中子相互作用的全部贡献……作者：P. Weppner（Eckerd College），A. Orazbayev（Ohio University），Ch. Elster（Ohio University）。研究领域：[弹性散射、物理学、中子、……、原子物理、散射]

### 5.3 定性分析

**与单字段相比，多字段为字段的选择赋予语义。** 在图 3（上）中，查询寻找的是不表达的基因或蛋白质。使用 MFARAll 时，检索器比 MFAR2 更准确地匹配到一段更长的文本。MFARAll 和 MFAR2 都正确匹配了雌性性腺（female gonad）。然而，MFARAll 选择的是指称表达缺失的那个字段，这是模型学到的。在 MFAR2 中，由于词法打分器无法区分“存在”（present）与“缺失”（absent），MFAR2 错误地把负文档排得更高。

**当同时需要词法匹配和语义相似度时，混合方法表现突出。** 在图 3（下）中，MFARAll 相对于 MFARDense 的优势在于能够对 Eckerd College 做词法匹配。此外，MFARAll 仍然能够在语义上匹配文档摘要。MFARDense 也找到了一个很接近的结果，但无法把这个不正确但相似的例子与正确例子区分开。

我们同样观察到只用词法打分的缺点。BM25 的一个局限是，连续词项匹配的频率会导致分数升高。因为 Physics 是作者列表中的高频关键词，这篇文档会得到高分，尽管它在语义上并不是同一含义。另一方面，MFARAll 正确匹配了具体机构，因为最终分数基于词法打分器与稠密打分器的加权组合，从而可能减弱高词法分数的影响。

<!-- 原 PDF 第 10 页 -->

作为会议论文发表于 ICLR 2025

## 6 相关工作

**结构化与半结构化检索。** 结构化与半结构化检索的各种形式，已在多种任务和领域中得到探索。我们特别关注多字段检索。它是半结构化检索的一种形式（Zaragoza et al., 2004）。此前的稀疏方法包括前面提到的 BM25F（Robertson et al., 2004）、学得的稀疏表示（Zamani et al., 2018），以及贝叶斯方法（Piwowarski & Gallinari, 2003）。Lin et al. (2023) 用稠密检索器处理类似任务，主要聚焦于查询分解，以支持若干“专家”检索器的加权组合。与他们的系统不同——那些权重是手工挑选的，而且每个检索器独立训练——我们的 MFAR 模型以单个共享编码器和学得的权重端到端学习，这有助于可扩展性。

表格检索（Zhang & Balog, 2021；Bhagavatula et al., 2015；Pasupat & Liang, 2015；Herzig et al., 2021；Shraga et al., 2020；Chen et al., 2020b）是一项结构化检索任务，采用与多字段检索相似的方法（MFAR 在该任务上的评测见附录 F）。表格检索并不必然需要表格专用的模型设计，因为表格的线性化形式就足以取得有竞争力的性能（Wang et al., 2022），而且许多表格检索数据集在编码器预训练时已经被见过（例如 DPR（Karpukhin et al., 2020）曾在 Wikipedia 上训练）。除表格数据外，其他结构化检索任务包括代码搜索（Husain et al., 2020）以及购物这类知识图谱数据集（Reddy et al., 2022）。后者与 STaRK 的 Amazon 子集相似。另有 Lin et al. (2023) 使用的一个图书问答数据集是多模态的，这不是我们的重点。

除了分解——它用专门的参数对准结构的某些部分，例如字段——先前工作还研究过修改训练过程：基于 Wikipedia 的格式生成伪查询（Su et al., 2024），以及在文档与自然语言描述之间加入辅助对齐目标（Li et al., 2023）。这些方法通常假设存在语义上重复的信息（例如表格以及对该表格的描述）。我们不做这一假设，而聚焦于可以使用现成编码器的训练后方法。

**混合方法。** 词法打分器与稠密打分器这两类方法的组合，此前已被发现是互补的，并能带来性能提升（Gao et al., 2021；Kuzi et al., 2020；Lee et al., 2023）。值得注意的是，Kuzi et al. (2020) 指出长文档对基于词法的方法构成挑战，并建议把文档分块作为未来工作中的一种可能补救。我们利用文档内在的多字段结构，隐式地把文档切段；而且与那些先前工作不同，本工作首次在多字段设定下展示了基于混合的方法的优势。另一些混合检索设置把稠密特征与词法特征一起放进一个稠密编码器，并端到端训练（Lin & Lin, 2023；Shen et al., 2023），而我们显式地使用已有的词法打分器。

## 7 结论

我们提出 MFAR，一个面向多字段数据检索的新框架。它使用多个打分器，每个打分器独立地把查询与半结构化文档的一个部分（字段）打分。这些打分器可以是基于词法的，也可以是基于稠密表示的，而且每个字段都可以由两类打分器同时打分。我们引入一个可解释、可控的、以查询为条件的权重预测器，用来自适应地对这些分数求和。在三个大规模数据集上，我们发现，由于多字段优势以及纳入了打分器的混合组合，MFAR 能够相对现有方法取得显著的性能提升，并达到最先进性能。通过分析，我们发现最好的模型既受益于同时使用两种打分器，也受益于能够以查询为条件对每个字段加权，这进一步验证了我们的方法。

我们的首要目标，是研究多字段半结构化数据检索这一具有挑战性且正在出现的问题，并引入一个灵活框架来处理它。在打下这一基础之后，未来工作可以包括更专门的单个打分器，扩展到视觉或音频等其他模态中的更多打分器，以及对跨打分器的分数加权整合加入其他算法改进。届时，MFAR 将迈向任意类型内容的检索，并进一步帮助通用搜索或基于智能体的 RAG。

<!-- 原 PDF 第 11 页 -->

作为会议论文发表于 ICLR 2025

## 8 致谢

作者感谢审稿人富有成效的交流和有帮助的反馈。作者也感谢 Nick Craswell、Jason Eisner、Jenny Liang、Shirley Wu、Jay DeYoung、Somin Wadhwa 和 Byron Wallace，感谢他们为改进本文进行的有洞见的讨论。ML 在 Microsoft 的 MSAI 组担任研究实习生期间完成本工作。ML 还受到 NSF Graduate Research Fellowship 的支持。

## 参考文献

Chandra Sekhar Bhagavatula, Thanapon Noraset, and Doug Downey. Tabel：网页表格中的实体链接. In *The Semantic Web - ISWC 2015: 14th International Semantic Web Conference*, Bethlehem, PA, USA, October 11-15, 2015, Proceedings, Part I, pp. 425–441, Berlin, Heidelberg, 2015. Springer-Verlag. doi: 10.1007/978-3-319-25007-6_25. https://doi.org/10.1007/978-3-319-25007-6_25

Payal Chandak, Kexin Huang, and Marinka Zitnik. 构建知识图谱以支持精准医学. *bioRxiv*, 2022. doi: 10.1101/2022.05.01.489928. https://www.biorxiv.org/content/early/2022/05/09/2022.05.01.489928

Ting Chen, Simon Kornblith, Mohammad Norouzi, and Geoffrey Hinton. 视觉表征对比学习的一个简单框架. In Hal Daumé III and Aarti Singh (eds.), *Proceedings of the 37th International Conference on Machine Learning*, volume 119 of *Proceedings of Machine Learning Research*, pp. 1597–1607. PMLR, 13–18 Jul 2020a. https://proceedings.mlr.press/v119/chen20j.html

Tongfei Chen, Ankita Sharma, Adam Pauls, and Benjamin Van Durme. 层次化语料编码器：融合生成式检索与稠密索引, 2025. https://arxiv.org/abs/2502.18877

Xilun Chen, Kushal Lakhotia, Barlas Oguz, Anchit Gupta, Patrick Lewis, Stan Peshterliev, Yashar Mehdad, Sonal Gupta, and Wen-tau Yih. 显著短语感知的稠密检索：稠密检索器能否模仿稀疏检索器？ In Yoav Goldberg, Zornitsa Kozareva, and Yue Zhang (eds.), *Findings of the Association for Computational Linguistics: EMNLP 2022*, pp. 250–262, Abu Dhabi, United Arab Emirates, December 2022. Association for Computational Linguistics. doi: 10.18653/v1/2022.findings-emnlp.19. https://aclanthology.org/2022.findings-emnlp.19

Zhiyu Chen, Mohamed Trabelsi, Jeff Heflin, Yinan Xu, and Brian D. Davison. 使用深度上下文化语言模型进行表格搜索. In *Proceedings of the 43rd International ACM SIGIR Conference on Research and Development in Information Retrieval*, SIGIR ’20, pp. 589–598, New York, NY, USA, 2020b. Association for Computing Machinery. doi: 10.1145/3397271.3401044. https://doi.org/10.1145/3397271.3401044

Luyu Gao, Zhuyun Dai, Tongfei Chen, Zhen Fan, Benjamin Van Durme, and Jamie Callan. 用语义残差嵌入补充词法检索模型. In *Advances in Information Retrieval: 43rd European Conference on IR Research, ECIR 2021*, Virtual Event, March 28 – April 1, 2021, Proceedings, Part I, pp. 146–160, Berlin, Heidelberg, 2021. Springer-Verlag. doi: 10.1007/978-3-030-72113-8_10. https://doi.org/10.1007/978-3-030-72113-8_10

Ruining He and Julian McAuley. 起落：用单类协同过滤建模时尚趋势的视觉演化. In *Proceedings of the 25th International Conference on World Wide Web*, WWW ’16, pp. 507–517, Republic and Canton of Geneva, CHE, 2016. International World Wide Web Conferences Steering Committee. doi: 10.1145/2872427.2883037. https://doi.org/10.1145/2872427.2883037

Matthew Henderson, Rami Al-Rfou, Brian Strope, Yun hsuan Sung, Laszlo Lukacs, Ruiqi Guo, Sanjiv Kumar, Balint Miklos, and Ray Kurzweil. 面向智能回复的高效自然语言回复建议, 2017. https://arxiv.org/abs/1705.00652

<!-- 原 PDF 第 12 页 -->

作为会议论文发表于 ICLR 2025

Jonathan Herzig, Thomas Müller, Syrine Krichene, and Julian Eisenschlos. 通过稠密检索在表格上进行开放域问答. In Kristina Toutanova, Anna Rumshisky, Luke Zettlemoyer, Dilek Hakkani-Tur, Iz Beltagy, Steven Bethard, Ryan Cotterell, Tanmoy Chakraborty, and Yichao Zhou (eds.), *Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies*, pp. 512–519, Online, June 2021. Association for Computational Linguistics. doi: 10.18653/v1/2021.naacl-main.43. https://aclanthology.org/2021.naacl-main.43/

Weihua Hu, Matthias Fey, Marinka Zitnik, Yuxiao Dong, Hongyu Ren, Bowen Liu, Michele Catasta, and Jure Leskovec. 开放图基准：图上机器学习的数据集. In H. Larochelle, M. Ranzato, R. Hadsell, M.F. Balcan, and H. Lin (eds.), *Advances in Neural Information Processing Systems*, volume 33, pp. 22118–22133. Curran Associates, Inc., 2020. https://proceedings.neurips.cc/paper_files/paper/2020/file/fb60d411a5c5b72b2e7d3527cfc84fd0-Paper.pdf

Hamel Husain, Ho-Hsiang Wu, Tiferet Gazit, Miltiadis Allamanis, and Marc Brockschmidt. CodeSearchNet 挑战：评估语义代码搜索的现状, 2020. https://arxiv.org/abs/1909.09436

Sergey Ioffe and Christian Szegedy. 批归一化：通过降低内部协变量偏移加速深度网络训练. In Francis R. Bach and David M. Blei (eds.), *Proceedings of the 32nd International Conference on Machine Learning*, ICML 2015, Lille, France, 6-11 July 2015, volume 37 of *JMLR Workshop and Conference Proceedings*, pp. 448–456. JMLR.org, 2015. http://proceedings.mlr.press/v37/ioffe15.html

Gautier Izacard, Mathilde Caron, Lucas Hosseini, Sebastian Riedel, Piotr Bojanowski, Armand Joulin, and Edouard Grave. 用对比学习进行无监督稠密信息检索. *Transactions on Machine Learning Research*, 2022. https://openreview.net/forum?id=jKN1pXi7b0

Soyeong Jeong, Jinheon Baek, Sukmin Cho, Sung Ju Hwang, and Jong Park. Adaptive-RAG：通过问题复杂度学习适配检索增强大语言模型. In Kevin Duh, Helena Gomez, and Steven Bethard (eds.), *Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)*, pp. 7036–7050, Mexico City, Mexico, June 2024. Association for Computational Linguistics. doi: 10.18653/v1/2024.naacl-long.389. https://aclanthology.org/2024.naacl-long.389

Zhengbao Jiang, Zhiqing Sun, Weijia Shi, Pedro Rodriguez, Chunting Zhou, Graham Neubig, Xi Lin, Wen-tau Yih, and Srini Iyer. 指令微调的语言模型是更好的知识学习者. In Lun-Wei Ku, Andre Martins, and Vivek Srikumar (eds.), *Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pp. 5421–5434, Bangkok, Thailand, August 2024. Association for Computational Linguistics. doi: 10.18653/v1/2024.acl-long.296. https://aclanthology.org/2024.acl-long.296

John Foley. FastRank alpha 发布. https://jjfoley.me/2019/10/11/fastrank-alpha.html, 2019.

Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, and Wen-tau Yih. 面向开放域问答的稠密段落检索. In Bonnie Webber, Trevor Cohn, Yulan He, and Yang Liu (eds.), *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, pp. 6769–6781, Online, November 2020. Association for Computational Linguistics. doi: 10.18653/v1/2020.emnlp-main.550. https://aclanthology.org/2020.emnlp-main.550

Saar Kuzi, Mingyang Zhang, Cheng Li, Michael Bendersky, and Marc Najork. 利用语义匹配与词法匹配提升文档检索系统的 Recall：一种混合方法, 2020. https://arxiv.org/abs/2010.01195

Dohyeon Lee, Seung-won Hwang, Kyungjae Lee, Seungtaek Choi, and Sunghyun Park. 论混合检索的互补性目标. In Anna Rogers, Jordan Boyd-Graber, and Naoaki

<!-- 原 PDF 第 13 页 -->

作为会议论文发表于 ICLR 2025

Okazaki (eds.), *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pp. 13357–13368, Toronto, Canada, July 2023. Association for Computational Linguistics. doi: 10.18653/v1/2023.acl-long.746. https://aclanthology.org/2023.acl-long.746/

Kenton Lee, Ming-Wei Chang, and Kristina Toutanova. 面向弱监督开放域问答的潜在检索. In Anna Korhonen, David Traum, and Lluís Màrquez (eds.), *Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics*, pp. 6086–6096, Florence, Italy, July 2019. Association for Computational Linguistics. doi: 10.18653/v1/P19-1612. https://aclanthology.org/P19-1612

Xinze Li, Zhenghao Liu, Chenyan Xiong, Shi Yu, Yu Gu, Zhiyuan Liu, and Ge Yu. 结构感知的语言模型预训练提升结构化数据上的稠密检索. In Anna Rogers, Jordan Boyd-Graber, and Naoaki Okazaki (eds.), *Findings of the Association for Computational Linguistics: ACL 2023*, pp. 11560–11574, Toronto, Canada, July 2023. Association for Computational Linguistics. doi: 10.18653/v1/2023.findings-acl.734. https://aclanthology.org/2023.findings-acl.734

Kevin Lin, Kyle Lo, Joseph Gonzalez, and Dan Klein. 为话到嘴边检索分解复杂查询. In Houda Bouamor, Juan Pino, and Kalika Bali (eds.), *Findings of the Association for Computational Linguistics: EMNLP 2023*, pp. 5521–5533, Singapore, December 2023. Association for Computational Linguistics. doi: 10.18653/v1/2023.findings-emnlp.367. https://aclanthology.org/2023.findings-emnlp.367

Sheng-Chieh Lin and Jimmy Lin. 面向词法匹配与语义匹配的稠密表示框架, April 2023. https://doi.org/10.1145/3582426

Xing Han Lù. Bm25s：通过急切稀疏打分实现快上数量级的词法搜索, 2024. https://arxiv.org/abs/2407.03618

Julian McAuley, Christopher Targett, Qinfeng Shi, and Anton van den Hengel. 基于图像的风格与替代品推荐. In *Proceedings of the 38th International ACM SIGIR Conference on Research and Development in Information Retrieval*, SIGIR ’15, pp. 43–52, New York, NY, USA, 2015. Association for Computing Machinery. doi: 10.1145/2766462.2767755. https://doi.org/10.1145/2766462.2767755

Anastasios Nentidis, Georgios Katsimpras, Anastasia Krithara, Salvador Lima López, Eulália Farré-Maduell, Luis Gasco, Martin Krallinger, and Georgios Paliouras. BioASQ 2023 综述：第十一届大规模生物医学语义索引与问答 BioASQ 挑战, pp. 227–250. Springer Nature Switzerland, 2023. doi: 10.1007/978-3-031-42448-9_19. http://dx.doi.org/10.1007/978-3-031-42448-9_19

Tri Nguyen, Mir Rosenberg, Xia Song, Jianfeng Gao, Saurabh Tiwary, Rangan Majumder, and Li Deng. MS MARCO：一个由人工生成的机器阅读理解数据集. November 2016. https://www.microsoft.com/en-us/research/publication/ms-marco-human-generated-machine-reading-comprehension-dataset/

Jianmo Ni, Chen Qu, Jing Lu, Zhuyun Dai, Gustavo Hernandez Abrego, Ji Ma, Vincent Zhao, Yi Luan, Keith Hall, Ming-Wei Chang, and Yinfei Yang. 大型双编码器是可泛化的检索器. In Yoav Goldberg, Zornitsa Kozareva, and Yue Zhang (eds.), *Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing*, pp. 9844–9855, Abu Dhabi, United Arab Emirates, December 2022. Association for Computational Linguistics. doi: 10.18653/v1/2022.emnlp-main.669. https://aclanthology.org/2022.emnlp-main.669

Panupong Pasupat and Percy Liang. 半结构化表格上的组合语义解析. In Chengqing Zong and Michael Strube (eds.), *Proceedings of the 53rd Annual Meeting of the Association for Computational Linguistics and the 7th International Joint Conference on Natural Language Processing (Volume 1: Long Papers)*, pp. 1470–1480, Beijing, China, July 2015. Association for Computational Linguistics. doi: 10.3115/v1/P15-1142. https://aclanthology.org/P15-1142/

<!-- 原 PDF 第 14 页 -->

作为会议论文发表于 ICLR 2025

Benjamin Piwowarski and Patrick Gallinari. 面向结构化文档信息检索的机器学习模型. In Petra Perner and Azriel Rosenfeld (eds.), *Machine Learning and Data Mining in Pattern Recognition*, pp. 425–438, Berlin, Heidelberg, 2003. Springer Berlin Heidelberg. https://doi.org/10.1007/3-540-45065-3_37

Peng Qi, Xiaowen Lin, Leo Mehr, Zijian Wang, and Christopher D. Manning. 通过迭代查询生成回答复杂开放域问题. In Kentaro Inui, Jing Jiang, Vincent Ng, and Xiaojun Wan (eds.), *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)*, pp. 2590–2602, Hong Kong, China, November 2019. Association for Computational Linguistics. doi: 10.18653/v1/D19-1261. https://aclanthology.org/D19-1261

Chandan K. Reddy, Lluís Màrquez, Fran Valero, Nikhil Rao, Hugo Zaragoza, Sambaran Bandyopadhyay, Arnab Biswas, Anlu Xing, and Karthik Subbian. 购物查询数据集：用于改进商品搜索的大规模 ESCI 基准, 2022. https://arxiv.org/abs/2206.06588

Nils Reimers and Iryna Gurevych. Sentence-BERT：使用孪生 BERT 网络的句子嵌入. In Kentaro Inui, Jing Jiang, Vincent Ng, and Xiaojun Wan (eds.), *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)*, pp. 3982–3992, Hong Kong, China, November 2019. Association for Computational Linguistics. doi: 10.18653/v1/D19-1410. https://aclanthology.org/D19-1410/

Stephen Robertson, Hugo Zaragoza, and Michael Taylor. 把 BM25 简单扩展到多个加权字段. In *Proceedings of the Thirteenth ACM International Conference on Information and Knowledge Management*, CIKM ’04, pp. 42–49, New York, NY, USA, 2004. Association for Computing Machinery. doi: 10.1145/1031171.1031181. https://doi.org/10.1145/1031171.1031181

Stephen E. Robertson, Steve Walker, Susan Jones, Micheline Hancock-Beaulieu, and Mike Gatford. Okapi 在 TREC-3. In Donna K. Harman (ed.), *Proceedings of The Third Text REtrieval Conference, TREC 1994*, Gaithersburg, Maryland, USA, November 2-4, 1994, volume 500-225 of *NIST Special Publication*, pp. 109–126. National Institute of Standards and Technology (NIST), 1994. http://trec.nist.gov/pubs/trec3/papers/city.ps.gz

Tao Shen, Xiubo Geng, Chongyang Tao, Can Xu, Guodong Long, Kai Zhang, and Daxin Jiang. Unifier：面向大规模检索的统一检索器. In *Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining*, KDD ’23, pp. 4787–4799, New York, NY, USA, 2023. Association for Computing Machinery. doi: 10.1145/3580305.3599927. https://doi.org/10.1145/3580305.3599927

Roee Shraga, Haggai Roitman, Guy Feigenblat, and Mustafa Cannim. 使用多模态深度学习的网页表格检索. In *Proceedings of the 43rd International ACM SIGIR Conference on Research and Development in Information Retrieval*, SIGIR ’20, pp. 1399–1408, New York, NY, USA, 2020. Association for Computing Machinery. doi: 10.1145/3397271.3401120. https://doi.org/10.1145/3397271.3401120

Weihang Su, Qingyao Ai, Xiangsheng Li, Jia Chen, Yiqun Liu, Xiaolong Wu, and Shengluan Hou. Wikiformer：利用 Wikipedia 的结构化信息进行 ad-hoc 检索的预训练. In *Proceedings of the Thirty-Eighth AAAI Conference on Artificial Intelligence and Thirty-Sixth Conference on Innovative Applications of Artificial Intelligence and Fourteenth Symposium on Educational Advances in Artificial Intelligence*, AAAI’24/IAAI’24/EAAI’24. AAAI Press, 2024. doi: 10.1609/aaai.v38i17.29869. https://doi.org/10.1609/aaai.v38i17.29869

Kuansan Wang, Zhihong Shen, Chiyuan Huang, Chieh-Han Wu, Yuxiao Dong, and Anshul Kanakia. 微软学术图谱：当专家还不够的时候. *Quantitative Science Studies*, 1(1):396–413, 02 2020. doi: 10.1162/qss_a_00021. https://doi.org/10.1162/qss_a_00021

<!-- 原 PDF 第 15 页 -->

作为会议论文发表于 ICLR 2025

Zhiruo Wang, Zhengbao Jiang, Eric Nyberg, and Graham Neubig. 表格检索未必需要表格专用的模型设计. In Wenhu Chen, Xinyun Chen, Zhiyu Chen, Ziyu Yao, Michihiro Yasunaga, Tao Yu, and Rui Zhang (eds.), *Proceedings of the Workshop on Structured and Unstructured Knowledge Integration (SUKI)*, pp. 36–46, Seattle, USA, July 2022. Association for Computational Linguistics. doi: 10.18653/v1/2022.suki-1.5. https://aclanthology.org/2022.suki-1.5/

Shirley Wu, Shiyu Zhao, Qian Huang, Kexin Huang, Michihiro Yasunaga, Kaidi Cao, Vassilis Ioannidis, Karthik Subbian, Jure Leskovec, and James Y Zou. Avatar：通过对比较推理优化大语言模型智能体的工具使用. In A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang (eds.), *Advances in Neural Information Processing Systems*, volume 37, pp. 25981–26010. Curran Associates, Inc., 2024a. https://proceedings.neurips.cc/paper_files/paper/2024/file/2db8ce969b000fe0b3fb172490c33ce8-Paper-Conference.pdf

Shirley Wu, Shiyu Zhao, Michihiro Yasunaga, Kexin Huang, Kaidi Cao, Qian Huang, Vassilis Ioannidis, Karthik Subbian, James Y Zou, and Jure Leskovec. STaRK：在文本与关系知识库上对大语言模型检索进行基准评测. In A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang (eds.), *Advances in Neural Information Processing Systems*, volume 37, pp. 127129–127153. Curran Associates, Inc., 2024b. https://proceedings.neurips.cc/paper_files/paper/2024/file/e607b1419e9ae7cd5cb5b5bb60c2ad5c-Paper-Datasets_and_Benchmarks_Track.pdf

Yinfei Yang, Gustavo Hernandez Abrego, Steve Yuan, Mandy Guo, Qinlan Shen, Daniel Cer, Yun-hsuan Sung, Brian Strope, and Ray Kurzweil. 使用带加性间隔 softmax 的双向双编码器改进多语言句子嵌入. In *Proceedings of the Twenty-Eighth International Joint Conference on Artificial Intelligence*, IJCAI-19, pp. 5370–5378. International Joint Conferences on Artificial Intelligence Organization, 7 2019. doi: 10.24963/ijcai.2019/746. https://doi.org/10.24963/ijcai.2019/746

Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William Cohen, Ruslan Salakhutdinov, and Christopher D. Manning. HotpotQA：一个多样化、可解释的多跳问答数据集. In Ellen Riloff, David Chiang, Julia Hockenmaier, and Jun’ichi Tsujii (eds.), *Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing*, pp. 2369–2380, Brussels, Belgium, October-November 2018. Association for Computational Linguistics. doi: 10.18653/v1/D18-1259. https://aclanthology.org/D18-1259/

Hamed Zamani, Bhaskar Mitra, Xia Song, Nick Craswell, and Saurabh Tiwary. 带有多个文档字段的神经排序模型. In *Proceedings of the Eleventh ACM International Conference on Web Search and Data Mining*, WSDM ’18, pp. 700–708, New York, NY, USA, 2018. Association for Computing Machinery. doi: 10.1145/3159652.3159730. https://doi.org/10.1145/3159652.3159730

Hugo Zaragoza, Nick Craswell, Michael J. Taylor, Suchi Saria, and Stephen E. Robertson. Microsoft Cambridge 在 TREC 13：Web 与 Hard 赛道. In Ellen M. Voorhees and Lori P. Buckland (eds.), *Proceedings of the Thirteenth Text REtrieval Conference, TREC 2004*, Gaithersburg, Maryland, USA, November 16-19, 2004, volume 500-261 of *NIST Special Publication*. National Institute of Standards and Technology (NIST), 2004. http://trec.nist.gov/pubs/trec13/papers/microsoft-cambridge.web.hard.pdf

Shuo Zhang and Krisztian Balog. 使用关键词查询与表格查询的语义表格检索. *ACM Trans. Web*, 15(3), May 2021. doi: 10.1145/3441690. https://doi.org/10.1145/3441690

<!-- 原 PDF 第 16 页 -->

作为会议论文发表于 ICLR 2025

## 附录 A 数据集

**表 5：** 每个 STaRK 数据集的语料规模、字段数量，以及按划分统计的查询数量。字段信息见附录中的表 6。

| 数据集 | 领域 | 文档数 | 字段数 | 训练集 | 开发集 | 测试集 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Amazon | 产品、产品评论 | 950K | 8 | 6K | 1.5K | 1.5K |
| MAG | 科学论文、作者 | 700K | 5 | 8K | 2.6K | 2.6K |
| Prime | 生物医学实体 | 130K | 22 | 6.1K | 2.2K | 2.8K |

### A.1 预处理

严格来说，STaRK 是一个在知识图谱上的查询数据集。完整的数据集细节见表 5。基线（Wu et al., 2024b）为每个节点创建一篇线性化文档，这会省略知识图谱中可用的部分边信息和多跳信息。AvaTaR（Wu et al., 2024a）直接在知识图谱上操作。由于我们希望在半结构化文档上操作，需要一个预处理步骤，要么处理线性化文档，要么处理图。

因为解析文档容易出错，我们决定复现 (Wu et al., 2024b) 的文档创建过程。我们从 STaRK 的全部原始数据出发，其形式是查询以及知识图谱中关联的答案 id。每条查询都需要数据集中实体信息与关系信息的某种组合才能回答。然而，每个数据集处理实体类型的方式不同。Amazon 中每条查询的答案都是产品实体。MAG 的答案是论文实体。而 Prime 有一个包含十种可能实体的列表可以回答查询，因此我们把这十种都作为文档纳入。

我们根据他们知识图谱中所走的有向路径来创建文档集合；如果存在超过单跳的关系，则对额外的实体和关系最多取两跳。对 Amazon，由于查询最多一跳，我们不纳入额外的节点信息。而 MAG 和 Prime 可以包含超过两跳的更多查询，因此我们在数据集的每篇文档中纳入关于额外关系和节点的信息。

### A.2 字段

我们在表 6 中列出本工作使用的字段。STaRK 知识图谱（Wu et al., 2024b）中并非每一个可用字段都被使用，因为有些字段基线没有用到，所以我们尽量与基线保持一致。为了篇幅和清晰，我们在正文示例中做了一些版式上的改动，包括把字段名大写，以及用空格替换下划线。我们还缩短了 “author affiliated with institution”，把 “paper cites paper” 缩短为 “Papers Cited”，把 “paper has topic field of study” 缩短为 “Area of Study”，并把 “type” 扩展为 “Entity Type”。

表 6 还列出每个字段内容长度分布的一些信息，长度由 Contriever 分词器度量。这有助于了解有多少信息可能因为有限的窗口而丢失。此外，我们列出 MFAR 的稠密打分器在训练时和测试时对该字段使用的最大序列长度。序列长度与批大小之间的权衡，关系到 GPU 显存占用。我们的词法基线（BM25）不做任何截断。

## 附录 B 实现细节

训练时，我们对每条查询采样 $k=1$ 个负例。加上批内负例，对于批大小 $b$，这会得到 $2b-1$ 个负样本。该负文档用 Pyserini Lucene⁴ 采样：检索 100 篇最近文档，从中去掉正文档。然后在剩余集合中采样排名最高的负文档。我们采用早

⁴ https://github.com/castorini/pyserini


<!-- 原 PDF 第 17 页 -->

作为会议论文发表于 ICLR 2025

**表 6：** 本工作使用的数据集与字段列表 $\mathcal{F}$，以及这些字段内容的基本长度统计。列出的是第 $k$ 百分位最长取值的长度。例如 $k=50$ 就是中位长度。MSL 是我们为 MFAR 中该字段选择的最大序列长度阈值，依据要么是编码器的最大窗口（512），要么是覆盖语料中大多数（$>99\%$）文档。

| 数据集 | 字段 | 90 | 95 | 99 | 99.9 | Max | MSL |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Amazon | also buy | 64 | 217 | 908 | 3864 | 50176 | 512 |
| Amazon | also view | 86 | 189 | 557 | 1808 | 21888 | 512 |
| Amazon | brand | 7 | 8 | 10 | 12 | 35 | 16 |
| Amazon | description | 207 | 289 | 446 | 1020 | 5038 | 512 |
| Amazon | feature | 130 | 171 | 305 | 566 | 1587 | 512 |
| Amazon | qa | 4 | 4 | 5 | 698 | 1873 | 512 |
| Amazon | review | 1123 | 2593 | 12066 | 58946 | 630546 | 512 |
| Amazon | title | 28 | 34 | 48 | 75 | 918 | 128 |
| MAG | abstract | 354 | 410 | 546 | 775 | 2329 | 512 |
| MAG | author affiliated with institution | 90 | 121 | 341 | 18908 | 46791 | 512 |
| MAG | paper cites paper | 581 | 863 | 1785 | 4412 | 79414 | 512 |
| MAG | paper has topic field of study | 49 | 52 | 57 | 63 | 90 | 64 |
| MAG | title | 31 | 34 | 44 | 62 | 9934 | 64 |
| Prime | associated with | 10 | 35 | 173 | 706 | 4985 | 256 |
| Prime | carrier | 3 | 4 | 4 | 13 | 2140 | 8 |
| Prime | contraindication | 4 | 4 | 66 | 586 | 3481 | 128 |
| Prime | details | 329 | 823 | 2446 | 5005 | 12319 | 512 |
| Prime | enzyme | 4 | 4 | 12 | 63 | 5318 | 64 |
| Prime | expression absent | 4 | 8 | 29 | 77 | 12196 | 64 |
| Prime | expression present | 204 | 510 | 670 | 18306 | 81931 | 512 |
| Prime | indication | 4 | 4 | 25 | 146 | 1202 | 32 |
| Prime | interacts with | 93 | 169 | 446 | 1324 | 55110 | 512 |
| Prime | linked to | 3 | 4 | 4 | 57 | 544 | 8 |
| Prime | name | 17 | 21 | 38 | 74 | 133 | 64 |
| Prime | off-label use | 3 | 4 | 4 | 56 | 727 | 8 |
| Prime | parent-child | 49 | 70 | 168 | 714 | 18585 | 256 |
| Prime | phenotype absent | 3 | 4 | 4 | 33 | 1057 | 8 |
| Prime | phenotype present | 20 | 82 | 372 | 1931 | 28920 | 512 |
| Prime | ppi | 36 | 125 | 438 | 1563 | 22432 | 512 |
| Prime | side effect | 4 | 4 | 93 | 968 | 5279 | 128 |
| Prime | source | 5 | 6 | 6 | 7 | 8 | 8 |
| Prime | synergistic interaction | 4 | 4 | 4800 | 9495 | 13570 | 512 |
| Prime | target | 4 | 9 | 33 | 312 | 5852 | 64 |
| Prime | transporter | 3 | 4 | 4 | 41 | 2721 | 8 |
| Prime | type | 7 | 8 | 8 | 9 | 9 | 8 |

长度单位为 Contriever 词元（第 $k$ 百分位）。

停，在验证损失上的耐心值为 5。我们设 $\tau=0.05$，并用 DDP 在 8 张 NVIDIA A100 上训练。Contriever 是 1.1 亿参数的模型，通过 $G$ 增加的额外参数可以忽略（$768|\mathcal{F}|$），并随字段数线性增长。

我们对微调编码器和其他参数使用不同的学习率。具体而言，编码器的学习率搜索范围为 $[5\times10^{-6},\,1\times10^{-5},\,5\times10^{-5},\,1\times10^{-4}]$，而 $G(q,f,m)$ 中参数的学习率搜索范围为 $[1\times10^{-3},\,5\times10^{-3},\,1\times10^{-2},\,5\times10^{-2},\,1\times10^{-1}]$。这些参数包括 $\mathbf{a}_{f}^{m}$，以及批归一化中的 $\gamma_{f}^{m}$ 和 $\beta_{f}^{m}$。主要网格搜索在加粗的取值上进行；文本抽取未保留加粗，见原 PDF 第 17 页。不过我们发现，对 Amazon 而言，$5\times10^{-3}$ 对 $G(q,f,m)$ 是有效的。除此之外，优化器（AdamW、dropout 等）和批归一化（PyTorch 2.4.0）都遵循默认设置。如前所述，是否使用批归一化本身也是被搜索的超参数：我们发现它在混合设定下有用。

<!-- 原 PDF 第 18 页 -->

作为会议论文发表于 ICLR 2025

我们的实现使用 Pytorch Lightning⁵ 和 sentence-transformers 2.2.2（Reimers & Gurevych, 2019）。词法打分器使用一个快速的、基于 Python 的 BM25 实现（Lù, 2024）。⁶ 本工作中每个模型的最佳超参数列于表 7。在只有单一字段的情形（最后两节），不需要自适应的查询条件化。

推理时，我们为每个字段检索前 100 个结果以形成候选集，并在该候选集上计算完整分数，从而得到最终排序。

⁵ https://lightning.ai/

⁶ https://github.com/xhluca/bm25s

**表 7：** 本工作各次运行使用的超参数。同一模型后续数据集行的“主要出现位置”在文本流中为空，按多行表处理，不另填。

| 模型 | 数据集 | 主要出现位置 | 编码器学习率 | $G()$ 学习率 | 批归一化？ |
| --- | --- | --- | --- | --- | --- |
| MFARAll | Amazon | 表 1，大多数表/图 | 1e-5 | 5e-3 | 否 |
| MFARAll | MAG |  | 5e-5 | 1e-2 | 是 |
| MFARAll | Prime |  | 5e-5 | 1e-2 | 是 |
| MFARDense | Amazon | 表 1，图 3 | 1e-5 | 5e-3 | 否 |
| MFARDense | MAG |  | 5e-5 | 5e-2 | 否 |
| MFARDense | Prime |  | 1e-5 | 1e-2 | 否 |
| MFARLexical | Amazon | 表 1，图 3 | 1e-5 | 5e-3 | 是 |
| MFARLexical | MAG |  | 1e-5 | 1e-2 | 是 |
| MFARLexical | Prime |  | 5e-5 | 1e-1 | 是 |
| MFAR2 | Amazon | 表 1，图 3 | 1e-5 | 1e-2 | 否 |
| MFAR2 | MAG |  | 5e-5 | 5e-3 | 是 |
| MFAR2 | Prime |  | 5e-5 | 5e-3 | 是 |
| MFARDense&1 | Amazon | 表 10（仅附录） | 1e-5 | 1e-2 | 否 |
| MFARDense&1 | MAG |  | 5e-5 | 5e-3 | 是 |
| MFARDense&1 | Prime |  | 1e-5 | 5e-3 | 是 |
| Contriever-FT | Amazon | 表 1 | 5e-5 | 不适用 | 不适用 |
| Contriever-FT | MAG |  | 1e-5 | 不适用 | 不适用 |
| Contriever-FT | Prime |  | 5e-5 | 不适用 | 不适用 |

## 附录 C STaRK 上的详细结果

我们给出 Amazon、MAG 和 Prime 测试划分上的完整结果。

### C.1 完整测试结果与比较

这里我们报告与正文相同的结果，但另外加入 Hit@5，以便在已有指标之外把 STaRK 的指标列全。表 8 给出包含这一额外指标的测试结果。表 9 把平均值单独成表。这里我们发现，即便面对很强的词法基线 BM25，MFAR 在这些半结构化数据集上的平均表现仍然优于其他基线。

### C.2 把全文表示与逐字段表示合并

我们评测额外的模型。它们把多字段（$|\mathcal{F}|$ 个打分器）与单字段（一篇拼接起来的文档）文档表示组合起来，用于词法检索器、稠密检索器，或两者兼有。例如，可以把 BM25 理解为在一篇（单字段的）全文上的词法检索器，该全文把所有字段拼接在一起。我们在先前实验之上增加 4 组实验：MFARLexical+1 是在 MFARLexical 上再加一个打分器（字段），用单文档 BM25 分数为全文打分；MFARDense+1 是在 MFARDense 上再加一个打分器，嵌入全文并打分（使用微调后的 Contriever）；MFARAll+2 是一个混合模型，与 MFARAll 类似，它把 MFARLexical+1 和 MFARDense+1 组合起来，也就是包含最多打分器的那个模型。

<!-- 原 PDF 第 19 页 -->

作为会议论文发表于 ICLR 2025

**表 8：** 与表 1 类似，但这里加入 Hit@5，并把平均值放到单独的表中，对象是测试划分。我们纳入相同的基线，并且总体上发现 Hit@5 也遵循同样的趋势。所有数据集上的平均值见表 9。

| 模型 | Amazon Hit@1 | Amazon Hit@5 | Amazon Recall@20 | Amazon MRR | MAG Hit@1 | MAG Hit@5 | MAG Recall@20 | MAG MRR | Prime Hit@1 | Prime Hit@5 | Prime Recall@20 | Prime MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| ada-002 | 0.392 | 0.627 | 0.533 | 0.542 | 0.291 | 0.496 | 0.484 | 0.386 | 0.126 | 0.315 | 0.360 | 0.214 |
| multi-ada-002 | 0.401 | 0.650 | 0.551 | 0.516 | 0.259 | 0.504 | 0.508 | 0.369 | 0.151 | 0.336 | 0.381 | 0.235 |
| Claude3 | 0.455 | 0.711 | 0.538 | 0.559 | 0.365 | 0.532 | 0.484 | 0.442 | 0.178 | 0.369 | 0.356 | 0.263 |
| GPT4 | 0.448 | 0.712 | 0.554 | 0.557 | 0.409 | 0.582 | 0.486 | 0.490 | 0.183 | 0.373 | 0.341 | 0.266 |
| BM25 | 0.483 | 0.721 | 0.584 | 0.589 | 0.471 | 0.693 | 0.689 | 0.572 | 0.167 | 0.355 | 0.410 | 0.255 |
| Contriever-FT | 0.383 | 0.639 | 0.530 | 0.497 | 0.371 | 0.594 | 0.578 | 0.475 | 0.325 | 0.548 | 0.600 | 0.427 |
| AvaTaR (agent) | 0.499 | 0.692 | 0.606 | 0.587 | 0.444 | 0.567 | 0.506 | 0.512 | 0.184 | 0.367 | 0.393 | 0.267 |
| MFARLexical | 0.332 | 0.569 | 0.491 | 0.443 | 0.429 | 0.634 | 0.657 | 0.522 | 0.257 | 0.455 | 0.500 | 0.347 |
| MFARDense | 0.390 | 0.659 | 0.555 | 0.512 | 0.467 | 0.678 | 0.669 | 0.564 | 0.375 | 0.620 | 0.698 | 0.485 |
| MFAR2 | 0.574 | 0.814 | 0.663 | 0.681 | 0.503 | 0.717 | 0.721 | 0.603 | 0.227 | 0.439 | 0.495 | 0.327 |
| MFARAll | 0.412 | 0.700 | 0.585 | 0.542 | 0.490 | 0.696 | 0.717 | 0.582 | 0.409 | 0.628 | 0.683 | 0.512 |
| MFARAll+2 | 0.530 | 0.785 | 0.663 | 0.643 | 0.559 | 0.742 | 0.741 | 0.643 | 0.400 | 0.659 | 0.726 | 0.520 |

**表 9：** 表 8 的平均值。

| 模型 | Hit@1 | Hit@5 | Recall@20 | MRR |
| --- | ---: | ---: | ---: | ---: |
| ada-002 | 0.270 | 0.479 | 0.459 | 0.381 |
| multi-ada-002 | 0.270 | 0.497 | 0.480 | 0.373 |
| Claude3* | 0.333 | 0.537 | 0.459 | 0.421 |
| GPT4* | 0.347 | 0.556 | 0.460 | 0.465 |
| BM25 | 0.374 | 0.590 | 0.561 | 0.462 |
| Contriever-FT | 0.360 | 0.594 | 0.569 | 0.467 |
| AvaTaR (agent) | 0.376 | 0.542 | 0.502 | 0.455 |
| MFARLexical | 0.339 | 0.553 | 0.549 | 0.437 |
| MFARDense | 0.411 | 0.652 | 0.641 | 0.520 |
| MFAR2 | 0.435 | 0.656 | 0.626 | 0.537 |
| MFARAll | 0.437 | 0.675 | 0.662 | 0.545 |
| MFARAll+2 | 0.496 | 0.729 | 0.710 | 0.602 |

最后，MFARDense&1 是一个混合模型，它把 MFARDense 与一个额外的 BM25 分数组合起来，该 BM25 分数针对完整的单文档表示。我们单独试验这一组合，原因是：BM25 基线在某些数据集上的结果很有希望（相对于 MFARLexical），MFARDense 相对于 MFARAll 也相对较强，以及我们的定性分析。

这些模型各自复用了对应基础版本的超参数。唯一的例外是 MFARDense&1。由于没有明确对应的基础模型，我们像先前的模型那样对它额外做了网格搜索。

把这些分数与基础模型的分数（来自表 1）比较，我们发现，在多字段表示之外再纳入单文档表示，有相当大的好处。

### C.3 随机种子之间的方差

对表 1 中每个训练过的模型，我们另选 3 个随机种子并重新训练，以确定各次运行之间分数的变化。注意，这些种子都与主实验所用的种子不同。值得注意的是，尽管打分器更少（$|\mathcal{F}|+1$ 对 $2|\mathcal{F}|$），MFARDense&1 仍然优于 MFARAll。

## 附录 D BM25F

本工作把 BM25F 作为一个比较点，但 Python 中没有公开实现，因此我们用一个已有代码库手工实现 BM25F。⁷ 我们并不穷尽地

⁷ https://github.com/jxmorris12/bm25_pt

<!-- 原 PDF 第 20 页 -->

作为会议论文发表于 ICLR 2025

搜索要设置的权重，因为那会需要多达 $2|\mathcal{F}|+1$ 次独立的参数搜索（Zaragoza et al., 2004）。因此，若没有大量计算，就很难得到带有最优权重的穷尽 BM25F 基线；而 MFAR 不需要这种随数据集字段数增长的网格搜索。

下面，我们给出每个字段使用均匀权重的 BM25F，所有权重都设为 1，并与普通 BM25 和 MFARAll 比较。尽管可能存在更优的设置，权重选择完全取决于数据集。

**表 10：** 同时考虑单字段与多字段文档表示的模型分数。

| 模型 | Amazon Hit@1 | Amazon Hit@5 | Amazon Recall@20 | Amazon MRR | MAG Hit@1 | MAG Hit@5 | MAG Recall@20 | MAG MRR | Prime Hit@1 | Prime Hit@5 | Prime Recall@20 | Prime MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| MFARLexical | 0.332 | 0.569 | 0.491 | 0.443 | 0.429 | 0.634 | 0.657 | 0.522 | 0.257 | 0.455 | 0.500 | 0.347 |
| MFARLexical+1 | 0.471 | 0.728 | 0.605 | 0.588 | 0.470 | 0.675 | 0.690 | 0.564 | 0.271 | 0.479 | 0.541 | 0.367 |
| MFARDense | 0.390 | 0.659 | 0.555 | 0.512 | 0.467 | 0.678 | 0.669 | 0.564 | 0.375 | 0.620 | 0.698 | 0.485 |
| MFARDense+1 | 0.453 | 0.704 | 0.594 | 0.570 | 0.472 | 0.703 | 0.679 | 0.576 | 0.384 | 0.636 | 0.707 | 0.498 |
| MFARAll | 0.412 | 0.700 | 0.585 | 0.542 | 0.490 | 0.696 | 0.717 | 0.582 | 0.409 | 0.628 | 0.683 | 0.512 |
| MFARDense&1 | 0.530 | 0.785 | 0.663 | 0.643 | 0.559 | 0.742 | 0.741 | 0.643 | 0.400 | 0.659 | 0.726 | 0.520 |
| MFARAll+2 | 0.562 | 0.808 | 0.672 | 0.674 | 0.507 | 0.721 | 0.717 | 0.605 | 0.342 | 0.615 | 0.669 | 0.464 |

**表 11：** 每个数据集、每个模型、每个指标的标准差。这些值通常在 0 到 0.015 之间，可以用来感受模型之间的差异有多显著。

| 模型 | Amazon Hit@1 | Amazon Hit@5 | Amazon Recall@20 | Amazon MRR | MAG Hit@1 | MAG Hit@5 | MAG Recall@20 | MAG MRR | Prime Hit@1 | Prime Hit@5 | Prime Recall@20 | Prime MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| MFARLexical | 0.009 | 0.007 | 0.004 | 0.008 | 0.014 | 0.008 | 0.002 | 0.001 | 0.013 | 0.009 | 0.016 | 0.013 |
| MFARDense | 0.007 | 0.004 | 0.004 | 0.003 | 0.008 | 0.005 | 0.001 | 0.001 | 0.005 | 0.003 | 0.004 | 0.002 |
| MFAR2 | 0.004 | 0.003 | 0.004 | 0.003 | 0.010 | 0.007 | 0.007 | 0.001 | 0.010 | 0.014 | 0.012 | 0.002 |
| MFARAll | 0.001 | 0.002 | 0.002 | 0.001 | 0.026 | 0.020 | 0.020 | 0.007 | 0.014 | 0.011 | 0.011 | 0.012 |
| MFARDense&1 | 0.001 | 0.002 | 0.001 | 0.001 | 0.011 | 0.009 | 0.009 | 0.002 | 0.004 | 0.002 | 0.002 | 0.003 |
| MFARAll+2 | 0.012 | 0.007 | 0.007 | 0.001 | 0.005 | 0.009 | 0.009 | 0.005 | 0.006 | 0.012 | 0.012 | 0.008 |

**表 12：** 均匀加权的 BM25F，与 BM25 和 MFARAll 比较。

| 模型 | Amazon Hit@1 | Amazon Recall@20 | Amazon MRR | MAG Hit@1 | MAG Recall@20 | MAG MRR | Prime Hit@1 | Prime Recall@20 | Prime MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| BM25 | 0.483 | 0.584 | 0.589 | 0.471 | 0.689 | 0.472 | 0.167 | 0.410 | 0.255 |
| BM25F | 0.183 | 0.332 | 0.264 | 0.451 | 0.671 | 0.551 | 0.142 | 0.244 | 0.214 |
| MFARAll | 0.412 | 0.585 | 0.542 | 0.490 | 0.717 | 0.582 | 0.409 | 0.683 | 0.512 |

我们发现，使用均匀权重时，BM25F 的表现甚至比 BM25 更差。这突出了选择合适权重的重要性，而这件事并非平凡。相比之下，MFAR 中分配给每个字段的相对重要性（或权重）是学出来的。

⁸ 存在 RankLib（John Foley, 2019）这类可用于搜索权重的 learning-to-rank 算法，以及坐标上升，但我们发现，要充分实现它们仍然需要大量计算。对每一对查询和文档，都必须生成一组供 RankLib 使用的特征。这些特征随文档数量增长。因此，如果查询与文档的组合很大，生成所有可能的特征就可能变得不可行。此外，如果选择增加更多样本，再使用 RankLib 也非平凡（必须从头重新搜索）。

<!-- 原 PDF 第 21 页 -->

作为会议论文发表于 ICLR 2025

## 附录 E 字段掩码的完整结果

我们给出在测试时掩掉 MFARAll 的每个字段和每个打分器之后的完整分数：Amazon 见表 13，MAG 见表 14，Prime 见表 15。第一行“—”是没有任何掩码的 MFARAll，并重复三次作为参照。最后一行 “all” 是把所有词法分数掩掉（或把所有稠密分数掩掉）的结果。把所有分数都掩掉没有意义，因为那样就没有任何打分器了。

根据表 14 中的发现，MAG 的所有字段大体上都有用，因为将相应字段置零的每一种情形都会导致性能下降。尽管 MAG 有这一发现，其他数据集里并非所有字段都同样明显地重要。对表 15 而言，Prime 有相当数量的字段在两种打分器都被掩掉时并不贡献于最终排序。而对 Amazon，在表 13 中，我们惊讶地发现像 “description” 和 “brand” 这样的字段影响很小。这既反映了数据集本身（以及其中包含的冗余），也反映了查询的分布以及它们所询问的内容。

**表 13：** 在测试时掩掉 MFARAll 的每个字段和打分器之后，Amazon 上的测试分数。

| 被掩字段 | 词法置零 Hit@1 | 词法置零 Hit@5 | 词法置零 Recall@20 | 词法置零 MRR | 稠密置零 Hit@1 | 稠密置零 Hit@5 | 稠密置零 Recall@20 | 稠密置零 MRR | 两者都置零 Hit@1 | 两者都置零 Hit@5 | 两者都置零 Recall@20 | 两者都置零 MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| （无掩码） | 0.412 | 0.700 | 0.586 | 0.542 | 0.412 | 0.700 | 0.586 | 0.542 | 0.412 | 0.700 | 0.586 | 0.542 |
| also buy | 0.407 | 0.690 | 0.578 | 0.534 | 0.410 | 0.696 | 0.586 | 0.540 | 0.403 | 0.678 | 0.578 | 0.530 |
| also view | 0.420 | 0.695 | 0.576 | 0.542 | 0.414 | 0.696 | 0.581 | 0.542 | 0.395 | 0.677 | 0.565 | 0.522 |
| brand | 0.410 | 0.699 | 0.585 | 0.540 | 0.397 | 0.692 | 0.575 | 0.528 | 0.400 | 0.686 | 0.570 | 0.526 |
| description | 0.417 | 0.699 | 0.587 | 0.542 | 0.410 | 0.692 | 0.580 | 0.540 | 0.413 | 0.680 | 0.576 | 0.535 |
| feature | 0.412 | 0.700 | 0.581 | 0.537 | 0.398 | 0.680 | 0.570 | 0.524 | 0.410 | 0.680 | 0.562 | 0.531 |
| qa | 0.412 | 0.700 | 0.586 | 0.542 | 0.412 | 0.700 | 0.586 | 0.542 | 0.381 | 0.636 | 0.545 | 0.499 |
| review | 0.410 | 0.696 | 0.583 | 0.541 | 0.398 | 0.680 | 0.575 | 0.526 | 0.384 | 0.666 | 0.548 | 0.510 |
| title | 0.414 | 0.685 | 0.583 | 0.535 | 0.390 | 0.650 | 0.555 | 0.508 | 0.389 | 0.672 | 0.562 | 0.516 |
| all | 0.389 | 0.660 | 0.553 | 0.512 | 0.271 | 0.518 | 0.452 | 0.386 | — | — | — | — |

**表 14：** 在测试时掩掉 MFARAll 的每个字段和打分器之后，MAG 上的测试分数。由于篇幅，部分字段名被截断，全名见表 6。

| 被掩字段 | 词法置零 Hit@1 | 词法置零 Hit@5 | 词法置零 Recall@20 | 词法置零 MRR | 稠密置零 Hit@1 | 稠密置零 Hit@5 | 稠密置零 Recall@20 | 稠密置零 MRR | 两者都置零 Hit@1 | 两者都置零 Hit@5 | 两者都置零 Recall@20 | 两者都置零 MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| （无掩码） | 0.490 | 0.696 | 0.717 | 0.582 | 0.490 | 0.696 | 0.717 | 0.582 | 0.490 | 0.696 | 0.717 | 0.582 |
| abstract | 0.469 | 0.681 | 0.707 | 0.565 | 0.393 | 0.616 | 0.651 | 0.494 | 0.430 | 0.636 | 0.659 | 0.526 |
| author affil... | 0.338 | 0.555 | 0.600 | 0.439 | 0.490 | 0.696 | 0.717 | 0.582 | 0.389 | 0.595 | 0.631 | 0.485 |
| paper cites... | 0.458 | 0.660 | 0.655 | 0.551 | 0.484 | 0.685 | 0.708 | 0.576 | 0.424 | 0.650 | 0.668 | 0.526 |
| paper topic... | 0.459 | 0.671 | 0.695 | 0.554 | 0.491 | 0.695 | 0.717 | 0.582 | 0.398 | 0.617 | 0.650 | 0.499 |
| title | 0.479 | 0.686 | 0.714 | 0.573 | 0.473 | 0.676 | 0.703 | 0.565 | 0.414 | 0.633 | 0.654 | 0.513 |
| all | 0.257 | 0.462 | 0.481 | 0.355 | 0.352 | 0.561 | 0.602 | 0.446 | — | — | — | — |

## 附录 F 表格检索

在表 16 中，我们在表格检索上演示 MFAR，具体数据集是 NQ-Tables（Herzig et al., 2021），它包含 170K 张表及其标题。我们注意到，该数据集的输入总体上较短（字段分解有限，分为标题、列头和表格内容），因此微调过的全上下文模型可能优于 MFAR。该数据集来自 Wikipedia，其中包含预训练数据里见过的知识。最后，我们没有搜索超参数，而是复用了先前的超参数。我们与 DPR-table 比较。它是一个规模相近、在表格上微调过的模型（Wang et al., 2022）。DPR-table 在 Hit@1 上以很大的幅度优于 MFAR。然而我们发现，当考虑前 10 或前 20 个结果时，MFAR 相对于该表格检索模型有更高的 Recall。这表明，即便在并不匹配的任务上（字段很少，并且存在一个专门为这些字段设计的有竞争力的基线），MFAR 仍然可以表现出潜力。

<!-- 原 PDF 第 22 页 -->

作为会议论文发表于 ICLR 2025

**表 15：** 在测试时掩掉 MFARAll 的每个字段和打分器之后，Prime 上的测试分数。由于篇幅，部分字段名被缩短，全名见表 6。

| 被掩字段 | 词法置零 Hit@1 | 词法置零 Hit@5 | 词法置零 Recall@20 | 词法置零 MRR | 稠密置零 Hit@1 | 稠密置零 Hit@5 | 稠密置零 Recall@20 | 稠密置零 MRR | 两者都置零 Hit@1 | 两者都置零 Hit@5 | 两者都置零 Recall@20 | 两者都置零 MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| （无掩码） | 0.409 | 0.627 | 0.683 | 0.512 | 0.409 | 0.627 | 0.683 | 0.512 | 0.409 | 0.627 | 0.683 | 0.512 |
| associated with | 0.392 | 0.610 | 0.670 | 0.495 | 0.407 | 0.624 | 0.680 | 0.510 | 0.399 | 0.618 | 0.672 | 0.502 |
| carrier | 0.409 | 0.627 | 0.683 | 0.512 | 0.409 | 0.627 | 0.683 | 0.512 | 0.403 | 0.621 | 0.678 | 0.506 |
| contraindication | 0.409 | 0.627 | 0.683 | 0.512 | 0.409 | 0.627 | 0.683 | 0.512 | 0.380 | 0.587 | 0.652 | 0.479 |
| details | 0.386 | 0.606 | 0.670 | 0.488 | 0.363 | 0.569 | 0.619 | 0.458 | 0.388 | 0.601 | 0.661 | 0.489 |
| enzyme | 0.409 | 0.627 | 0.683 | 0.512 | 0.409 | 0.627 | 0.683 | 0.512 | 0.405 | 0.623 | 0.677 | 0.508 |
| expression abs. | 0.408 | 0.627 | 0.683 | 0.511 | 0.392 | 0.607 | 0.664 | 0.494 | 0.403 | 0.622 | 0.678 | 0.506 |
| expression pres. | 0.409 | 0.627 | 0.683 | 0.512 | 0.409 | 0.627 | 0.683 | 0.512 | 0.400 | 0.617 | 0.675 | 0.502 |
| indication | 0.407 | 0.627 | 0.682 | 0.511 | 0.398 | 0.613 | 0.663 | 0.498 | 0.392 | 0.611 | 0.665 | 0.495 |
| interacts with | 0.403 | 0.624 | 0.681 | 0.507 | 0.406 | 0.626 | 0.682 | 0.510 | 0.403 | 0.622 | 0.674 | 0.506 |
| linked to | 0.409 | 0.627 | 0.683 | 0.512 | 0.409 | 0.627 | 0.683 | 0.512 | 0.383 | 0.601 | 0.661 | 0.486 |
| name | 0.410 | 0.628 | 0.684 | 0.513 | 0.407 | 0.627 | 0.681 | 0.510 | 0.407 | 0.622 | 0.674 | 0.507 |
| off-label use | 0.409 | 0.627 | 0.683 | 0.512 | 0.409 | 0.627 | 0.683 | 0.512 | 0.379 | 0.602 | 0.662 | 0.482 |
| parent-child | 0.385 | 0.619 | 0.680 | 0.494 | 0.391 | 0.613 | 0.663 | 0.495 | 0.386 | 0.601 | 0.663 | 0.487 |
| phenotype abs. | 0.408 | 0.625 | 0.681 | 0.511 | 0.409 | 0.627 | 0.683 | 0.512 | 0.376 | 0.591 | 0.653 | 0.477 |
| phenotype pres. | 0.405 | 0.619 | 0.675 | 0.506 | 0.409 | 0.627 | 0.683 | 0.512 | 0.393 | 0.609 | 0.669 | 0.495 |
| ppi | 0.403 | 0.622 | 0.678 | 0.506 | 0.409 | 0.627 | 0.683 | 0.512 | 0.399 | 0.617 | 0.671 | 0.502 |
| side effect | 0.409 | 0.627 | 0.683 | 0.512 | 0.409 | 0.627 | 0.683 | 0.512 | 0.405 | 0.624 | 0.680 | 0.508 |
| source | 0.409 | 0.627 | 0.683 | 0.512 | 0.409 | 0.627 | 0.683 | 0.512 | 0.397 | 0.614 | 0.671 | 0.499 |
| synergistic int. | 0.408 | 0.627 | 0.682 | 0.511 | 0.409 | 0.627 | 0.683 | 0.512 | 0.381 | 0.597 | 0.659 | 0.483 |
| target | 0.407 | 0.627 | 0.683 | 0.511 | 0.394 | 0.613 | 0.662 | 0.497 | 0.397 | 0.617 | 0.671 | 0.501 |
| transporter | 0.409 | 0.627 | 0.683 | 0.512 | 0.409 | 0.627 | 0.683 | 0.512 | 0.406 | 0.624 | 0.679 | 0.509 |
| type | 0.409 | 0.627 | 0.683 | 0.512 | 0.403 | 0.625 | 0.681 | 0.507 | 0.396 | 0.615 | 0.669 | 0.498 |
| all | 0.342 | 0.554 | 0.624 | 0.442 | 0.267 | 0.450 | 0.500 | 0.352 | — | — | — | — |

**表 16：** 在 NQ-Tables（Herzig et al., 2021）上的表格检索结果。我们报告 Recall，因为每条查询只有一个金标文档。

| 模型 | Recall@1 | Recall@5 | Recall@10 | Recall@20 |
| --- | ---: | ---: | ---: | ---: |
| MFAR2 | 0.497 | 0.812 | 0.878 | 0.930 |
| MFARAll | 0.498 | 0.829 | 0.900 | 0.949 |
| DPR-table 110M | 0.679 | 0.849 | 0.889 | 0.906 |

<!-- 译完 -->
