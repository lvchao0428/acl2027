# 面向文本与关系检索的知识感知大语言模型查询扩展

- 原文件名：KAR_arXiv2410.13765.pdf
- 原标题：Knowledge-Aware Query Expansion with Large Language Models for Textual and Relational Retrieval
- 中文标题：面向文本与关系检索的知识感知大语言模型查询扩展
- 作者：Yu Xia¹，Junda Wu¹，Sungchul Kim²，Tong Yu²，Ryan A. Rossi²，Haoliang Wang²，Julian McAuley¹
- 来源：arXiv:2410.13765v2 [cs.CL] 5 Feb 2025

<!-- 原 PDF 第 1 页 -->

¹University of California San Diego  
²Adobe Research  
{yux078, juw069, jmcauley}@ucsd.edu  
{sukim, tyu, ryrossi, hawang}@adobe.com

## 摘要

大语言模型（LLM）已被用来生成查询扩展，以扩充原始查询、改进信息搜索。近期研究还探索向 LLM 提供初始检索结果，使生成的查询扩展更贴合文档语料。然而，这些方法大多着重增强搜索查询与目标文档之间的文本相似度，而忽略了文档关系。对于诸如「帮我找一款评分很高、适合野生动物摄影、且兼容我的 Nikon F-Mount 镜头的相机」这类查询，现有方法可能生成语义相近、但在结构上与用户意图无关的扩展。为处理同时带有文本要求与关系要求的半结构化查询，本文提出一种知识感知查询扩展框架，用知识图谱（KG）中的结构化文档关系来增强 LLM。针对现有基于 KG 的方法在实体打分上的局限，我们把文档文本用作丰富的 KG 节点表示，并采用基于文档的关系过滤，得到知识感知检索（Knowledge-Aware Retrieval，KAR）。在三个不同领域数据集上的大量实验表明，相对最先进基线，本方法在文本与关系半结构化检索上具有优势。

## 1 引言

大语言模型已被用来为原始查询补充额外上下文，以捕捉目标文档的相似语义，从而提升检索性能（Gao et al., 2023; Wang et al., 2023）。直接生成会带来幻觉、信息过时以及缺乏领域知识等问题，因此近期方法（Jagerman et al., 2023; Lei et al., 2024; Shen et al., 2024）探索用初始检索结果作为上下文来增强 LLM，例如伪相关反馈（pseudo relevance feedback，PRF）（Lv and Zhai, 2010; Li et al., 2022），从而使扩展更扎根于特定领域的文档语料。

这些方法虽然有效，但现有工作大多关注提升扩展查询与目标文档文本之间的语义相似度。然而在真实搜索场景中，文档除文本描述外，往往还以特定类型的关系相互连接（Talmor and Berant, 2018; Cao et al., 2022）。用户经常以半结构化方式同时查询文本细节与关系细节（Wu et al., 2024b; Patel et al., 2024; Wu et al., 2024a; Boer et al., 2024），以便更准确地描述搜索意图，而这一点被现有查询扩展方法所忽视。例如，

**图 1**：给定一条同时包含文本要求与关系要求的半结构化商品搜索查询（Wu et al., 2024b），HyDE（Gao et al., 2023）、RAR（Shen et al., 2024）与 KAR（本文）生成的查询扩展示例。HyDE 与 RAR 丰富了文本信息，例如「野生动物」和「高评分」，但编造了不正确的文档关系，例如「Nikon Coolpix P1000」与「F-Mount 镜头」的兼容性。相比之下，KAR 利用知识图谱中的文档关系，例如顾客同时购买了「Nikon Z7 II」和「F-Mount 镜头」，从而生成语义相近且结构相关的查询扩展。

图中查询为：Find me a highly rated camera for wildlife photography compatible with my Nikon F-Mount lenses.（帮我找一款评分很高、适合野生动物摄影、且兼容我的 Nikon F-Mount 镜头的相机。）

图中三路扩展的可见文本如下。

HyDE 一侧：

- Title：Nikon camera
- Feature：the camera is designed for wildlife photography…
- Description：compatible with Nikon F-Mount lenses
- Reviews："This is a great camera for shooting wildlife animals!"

RAR 一侧：

- Title：Nikon Coolpix P1000
- Feature：impressive 125x zoom for wildlife photography…
- Description：built-in lens options inc. Nikon F-Mount lenses…
- Reviews：5 stars "captured wildlife birds without a hitch!"

KAR 一侧：

- Title：Nikon Z7 II
- Feature：45.7 megapixels; autofocus…
- Description：wildlife flexible lens adapter…
- Reviews：4.5/5 "autofocus fast animals…"
- Relations：
  - products also bought：Nikon F-Mount lenses, …
  - products also viewed：FTZ adapter, …

图 1 的版式是示意图，find_tables 抽到的是破碎单元格，上列文字来自按页正文抽取。

<!-- 原 PDF 第 2 页 -->

图 1 中的用户查询同时指定了商品的文本要求「高评分」和「野生动物摄影」，以及关系要求「兼容 Nikon F-Mount 镜头」。现有方法或许能就该商品生成语义相近的扩展，但往往编造不正确的商品关系，即相机与镜头之间的兼容性，从而导致次优的检索结果。

为处理这类半结构化查询，我们提出知识感知查询扩展框架，用来自知识图谱（KG）的结构化文档关系增强 LLM。我们首先用 LLM 解析原始查询中显式提及的实体，然后检索这些实体的文本文档，以及它们在 KG 上的关联节点与关系。现有基于 KG 的问答方法（Yasunaga et al., 2021; Zhang et al., 2022; Taunk et al., 2023）根据查询与实体名称（例如「Nikon camera」）之间的语义相似度对节点相关性打分，从而滤除无关关系；但它们忽略了用户所查询实体的丰富文本细节，例如「高评分」和「野生动物」。

为此，我们把文档文本用作丰富的 KG 节点表示，并用基于文档的关系过滤来抽取聚焦于查询的关系。随后，把收集到的文本知识与关系知识作为输入，LLM 生成既扎根于文档语料、又保留用户指定文档关系的查询扩展。扩展后的查询再用于最终检索，即我们的知识感知检索（KAR）。我们在 STaRK 基准（Wu et al., 2024b）的三个文本与关系半结构化检索数据集上做了充分实验，分别对应商品、学术论文与生物医学搜索。结果表明，本方法优于最先进的查询扩展方法，并且相对基于 LLM 的检索智能体至少达到相当的性能。

概括而言，我们的贡献如下：i）为处理同时带有文本要求与关系要求的复杂搜索查询，提出用 KG 增强 LLM 的知识感知查询扩展框架；ii）针对基于实体的打分的局限，把文档文本用作 KG 节点表示，并为知识感知检索（KAR）采用基于文档的关系过滤；iii）在三个半结构化检索数据集上的实验展示了本方法的优势及其实际适用性。

## 2 相关工作

### 2.1 基于 LLM 的查询扩展

查询扩展是信息搜索应用中广泛采用的技术（Azad and Deepak, 2019），它用额外上下文扩展原始查询，以匹配目标文档。较早的研究把初始检索到的文档用作伪相关反馈（PRF）（Yu et al., 2003; Cao et al., 2008; Lv and Zhai, 2010; Li et al., 2022），从中抽取相关内容作为补充信息。然而，这些方法的效果受初始检索质量限制。

近来，LLM 增强的信息检索成为一个突出方向（Zhu et al., 2023），LLM 被用来凭借其内在知识生成查询扩展。HyDE（Gao et al., 2023）用 LLM 直接生成能够回答查询的假设文档，再用这些文档的嵌入去检索相似的真实文档。Query2Doc（Wang et al., 2023）进一步向 LLM 提供少样本示例，以提升扩展质量。Jagerman et al. (2023) 还探索把思维链用作扩展。针对 LLM 可能缺乏领域知识这一局限，Shen et al. (2024) 提出检索增强检索（retrieval-augmented retrieval，RAR），把初始检索结果作为上下文，供 LLM 生成查询扩展。Lei et al. (2024) 先让 LLM 从初始检索结果中抽取关键信息，再扩展查询。AGR（Chen et al., 2024）设计了分析—生成—精炼（Analyze-Generate-Refine）这一多步查询扩展框架，把 LLM 的自我精炼能力与作为参照的初始检索结果结合起来。Jia et al. (2024) 也探索了类似的验证策略。尽管已有这些进展，现有方法大多关注文本相似度，而忽略文档关系。相比之下，我们的知识感知查询扩展用来自 KG 的结构化文档关系增强 LLM，以处理半结构化检索任务。

### 2.2 知识图谱增强的 LLM

在较早的研究中，语言模型被用来提供文本嵌入，以增强图神经网络在 KG 推理任务上的表现（Feng et al., 2020; Lin et al., 2021; Yasunaga et al., 2021; Spillo et al., 2023）。随着 LLM 对多种文本结构涌现出推理能力，KG 反过来被用作结构化知识来源，为 LLM 补充事实或领域

<!-- 原 PDF 第 3 页 -->

特定信息，从而使推理与生成更加有据（Pan et al., 2024）。例如，Think-on-Graph（Sun et al., 2024）进行实体与关系探索，以检索用于问答的相关三元组。Reason-on-Graph（Luo et al., 2024）从 KG 中检索推理路径，供 LLM 进行忠实推理。HyKGE（Jiang et al., 2024）生成假设推理路径，并将其落实到 KG 上以生成答案。LPKG（Wang et al., 2024）从 KG 构造规划数据，用于复杂问答。图检索增强生成也近期涌现（Peng et al., 2024; Xu et al., 2024; He et al., 2024; Hu et al., 2024），它把 KG 等图数据作为检索来源，以生成更准确、更结构化的回答。

与这些把 LLM 与 KG 结合的研究相比，我们的工作有两个关键不同。第一，先前研究大多关注知识图谱问答，其中查询更侧重事实，答案被精确编码在 KG 中。我们的工作关注文档检索，查询往往更具描述性、也更依赖领域。第二，先前研究中 KG 是唯一的检索来源。在我们的工作中，文本文档与知识图谱共同构成半结构化知识来源，信息覆盖多个方面（Wu et al., 2024b）。检索来源的这种半结构化性质，给有效的知识抽取与检索带来了不同的挑战（Patel et al., 2024; Wu et al., 2024a; Boer et al., 2024）。

## 3 问题定义

我们将所研究的、面向文本与关系半结构化检索的查询扩展定义如下。遵循 Wu et al. (2024b)，设知识库包含文本文档集合 \(D\) 以及知识图谱 \(G = (V, R)\)，其中 \(d_i \in D\) 是描述实体 \(i\) 的文本文档，\(v_i \in V\) 是 KG 上对应的实体节点，\(R\) 是不同节点之间的关系集合。例如，在图 2 所示的论文搜索场景中，每篇论文 \(i\) 有一份文本文档 \(d_i\)，其中包含摘要、发表 venue、发表日期等；知识图谱 \(G\) 上对应的节点 \(v_i\) 编码它与其他节点的关系，例如论文引用、作者身份以及研究领域。

现给定一条查询 \(q\)，它同时对 \(D\) 中的非结构化文本和 \(G\) 中的结构化关系提出要求。半结构化检索（Wu et al., 2024b; Boer et al., 2024; Wu et al., 2024a）要输出文档集合 \(A \subseteq D\)，使得每篇文档所描述的实体同时满足查询 \(q\) 指定的文本要求与关系要求。

为弥合查询与文档之间的差距，我们旨在基于可用的文本知识与关系知识，用查询扩展 \(Q_e\) 来增强原始查询 \(q\)：

\[
Q_e = f(q, D, G), \tag{1}
\]

\[
q' = \mathrm{Concat}(q, Q_e), \tag{2}
\]

其中 \(f\) 表示查询扩展函数，扩展被追加到 \(q\) 上，形成扩展查询 \(q'\)，用于最终的文档检索。

## 4 方法

本节按图 2 描述我们的知识感知查询扩展框架。

**由 LLM 解析实体。** 作为初始步骤，我们首先利用 LLM，在给定文档结构的条件下，从原始查询 \(q\) 中抽取显式提及的实体，记为 \(E_q\)。遵循与 Gao et al. (2023) 类似的想法，我们还把原始查询 \(q\) 本身视为一个伪实体，代表待检索的目标实体文档：

\[
E_q = \{q, \mathrm{LLM}(q)\}. \tag{3}
\]

于是，一条论文搜索查询的实体可能包括作者名、论文标题以及查询本身。

**实体文档检索。** 对每个被提及的实体 \(i \in E_q\)，我们再用一个现成的文本嵌入模型，从 \(D\) 中检索其关联文本文档 \(d_i\)。如图 2 所示，作者文档包含论文数与被引次数等信息，论文文档包含摘要以及日期、venue 等发表信息。

**KG 关系传播。** 基于该半结构化知识库，我们随后把每篇文档链接到 KG 上对应的实体节点 \(v_i \in V\)。对每个节点 \(v_i\)，我们根据 \(G\) 中的 KG 关系抽取其 \(h\) 跳邻居。将这些邻居节点的集合记为 \(N_i\)，它们与 \(v_i\) 的关系集合记为 \(R_i\)，例如「作者撰写论文」「论文引用论文」。类似地，我们把每个邻居节点 \(v_j \in N_i\) 链接到其对应的文本文档 \(d_j\)。

**基于文档的关系过滤。** 对于稠密的 KG，一个节点可能拥有大量邻居，其中包括与查询无关的节点。现有基于 KG 的方法（Yasunaga et al., 2021;

<!-- 原 PDF 第 4 页 -->

Zhang et al., 2022; Taunk et al., 2023）根据实体名称对节点与查询之间的相关性打分，从而滤除无关关系。然而，这种基于实体的做法忽略了实体丰富的文本细节。例如，图 2 中论文搜索的 KG 实体名称只是论文标题，而论文的进一步细节，例如摘要内容「高分辨率图像恢复」和发表信息「2010」，尽管经常被用户查询，却往往不能直接从 KG 中获得。

为此，我们把关联的文档文本用作 KG 节点的丰富表示，并用基于文档的关系过滤得到聚焦于查询的关系。具体而言，给定邻居节点集合 \(N_i\)，我们不再只使用实体名称，而是用文本嵌入模型嵌入每个邻居节点的文本文档 \(d_j\)，得到 \(x_j = \mathrm{Embed}(d_j)\)，并用同一嵌入模型嵌入原始查询 \(q\)，得到 \(x_q = \mathrm{Embed}(q)\)。然后计算每个节点 \(v_j\) 与查询 \(q\) 的语义相似度并打分：

\[
s_{j,q} = \mathrm{Sim}(x_j, x_q). \tag{4}
\]

该分数利用实体名称之外更丰富的文本细节，更准确地反映查询与邻居节点之间的相关性。基于相似度分数，我们选出得分最高的 top-\(k\) 个节点，作为聚焦于查询的邻居：

\[
N_{i,q} = \{v_j \in N_i \mid s_{j,q} \in \mathrm{TopK}(s_q)\}, \tag{5}
\]

并由此得到对应的、聚焦于查询的关系 \(R_{i,q} \subseteq R_i\)。由于基于文档的关系过滤使用现成的文本嵌入模型，当 KG 中加入新节点时，它不像大多数图神经网络那样需要重新训练，从而体现了本方法的可扩展性。

**文档三元组构造。** 在得到过滤后的邻居节点与关系之后，我们并不像 Sun et al. (2024) 和 Luo et al. (2024) 那样构造基于实体的知识三元组，而是进一步利用丰富的文本信息，构造如图 2 所示的基于文档的知识三元组：

\[
T_{i,q} = \{(d_i, r_{i,j}, d_j) \mid v_j \in N_{i,q},\ r_{i,j} \in R_{i,q}\}, \tag{6}
\]

其中 \(r_{i,j}\) 表示 KG 上从节点 \(v_i\) 到节点 \(v_j\) 的关系，例如「论文引用论文」，而 \(d_i\) 与 \(d_j\) 是与 \(v_i\)、\(v_j\) 关联的文档文本，包含每个节点的细节，例如论文摘要、venue 和发表日期。这种文档三元组不仅提供丰富的文本细节，还保留来自 KG 的结构化关系知识，以提高信息准确性。

**知识感知扩展。** 在最后一步，我们把文档三元组 \(T_q\) 转换成文本，与原始查询 \(q\) 一起作为 LLM 的输入。借助其较强的文本推理能力，我们提示 LLM 从 \(T_q\) 中抽取有用信息，并生成有助于回答查询 \(q\) 的查询扩展：

\[
Q_e = \mathrm{LLM}(q, T_q), \tag{7}
\]

其中我们遵循 Shen et al. (2024) 和 Chen et al. (2024)，在一次 LLM 推理中采样 \(n\) 个回答，并将它们拼接为追加到原始查询上的最终扩展。按式 (2) 定义的扩展查询 \(q'\) 随后用于基于嵌入的最终文档检索。

在整个查询扩展过程中，我们协同利用文本文档与 KG 关系，实现知识感知检索（KAR）。由于本方法是零样本的，它可以与多种现成的 LLM 和文本嵌入模型一起使用。此外，由于本方法利用

**图 2**：以一条同时带有文本要求与关系要求的学术论文搜索查询为例，展示知识感知查询扩展框架的总览。

图中示例查询为：Find me a paper about high resolution image recovery written by Andrew Stokes in 2010 and citing the paper "Multi-aperture coherent imaging".（帮我找一篇关于高分辨率图像恢复的论文，由 Andrew Stokes 写于 2010 年，并引用论文 “Multi-aperture coherent imaging”。）

图中可见的流程与示例文本如下。LLM 实体解析得到：1）Andrew Stokes；2）Multi-aperture coherent imaging；3）（伪实体，即查询 \(q\) 本身）。随后进行实体文档检索、KG 关系传播（\(h\) 跳邻居；关系示例包括 author writes paper、paper cites paper）、基于文档的关系过滤（Embed 与 Sim），以及文档三元组构造，形式如 \((\ \cdot\ ,\ \text{author writes paper},\ \cdot\ )\)。知识感知扩展阶段，LLM 在查询 \(q\) 与文档三元组上生成扩展。图中可见的文档字段包括：

- title：Distributed aperture synthesis；abstract：recovering high resolution image…；publication date：2010-05-10；venue：Optic Express；relations：author writes paper：Andrew Stokes, …；paper cites paper：Multi-aperture coherent imaging, …；paper has topic：Optical field, …
- title：Multi-aperture cohere imaging；abstract：Aperture synthesis offers…；publication date：2011-05-13；venue：Proceedings of SPIE
- author name：Andrew Stokes；paper count：2；citation count：31
- title：Single shot high resolution…；abstract：We demonstrate a novel…；publication date：2013-02-11；venue：Optics Express

图 2 是流程图，find_tables 抽到的是破碎单元格，上列文字来自按页正文抽取。原文在 venue 处同时出现 “Optic Express” 与 “Optics Express”，在标题处出现 “Multi-aperture cohere imaging”，均按抽取原文保留。

<!-- 原 PDF 第 5 页 -->

文档文本作为 KG 节点表示，因此不需要额外的模型微调；当知识库加入新文档时，本方法仍然可扩展、也足够灵活。

## 5 实验设置

### 5.1 数据集与指标

我们在 STaRK 基准（Wu et al., 2024b）的三个文本与关系半结构化检索数据集上评估本方法：

- **AMAZON**：商品搜索数据集。约 100 万个实体的文本文档来自 Amazon 评论（He and McAuley, 2016）以及问答记录（McAuley et al., 2015）；940 万条 KG 关系包括一同浏览或一同购买的商品、品牌和颜色。
- **MAG**：学术论文搜索数据集，基于 obgn-papers100M（Hu et al., 2020）与 MAG（Wang et al., 2020）。190 万个实体的文本文档包括论文标题、摘要和发表细节；3980 万条 KG 关系包括引用与作者信息。
- **PRIME**：精准医学问询数据集。文本文档从多个来源收集，约 12.9 万个实体，例如疾病、药物、蛋白质和基因；810 万条 KG 关系来自 PrimeKG（Chandak et al., 2023）。

数据集统计见表 1。AMAZON 的文本信息更丰富，而 MAG 与 PRIME 的关系更稠密。我们使用 STaRK 基准中合成查询的官方测试集，以及人工编写查询的留出集，并采用以下评价指标：Hit@1、Hit@5、Recall@20（R@20）以及 Mean Reciprocal Rank（MRR）。我们还在人工编写的查询上给出进一步的消融结果，以展示本方法处理真实查询时的泛化能力。

**表 1**：STaRK 基准中文本与关系半结构化检索数据集的统计。

| 数据集 | 实体数 | 文本 token 数 | 关系数 | 平均度 |
| --- | ---: | ---: | ---: | ---: |
| AMAZON | 1,035,542 | 592,067,882 | 9,443,802 | 18.2 |
| MAG | 1,872,968 | 212,602,571 | 39,802,116 | 43.5 |
| PRIME | 129,375 | 31,844,769 | 8,100,498 | 125.2 |

### 5.2 基线与变体

我们在零样本设置下，将 KAR 与下列基线及消融变体比较：

- **Base**：基于原始查询进行检索。
- **PRF**：经典伪相关反馈（Lv and Zhai, 2010; Li et al., 2022），用排名前 \(n\) 的初始检索结果扩展查询。
- **HyDE**（Gao et al., 2023）：仅根据原始查询，直接用 LLM 生成扩展。
- **RAR**（Shen et al., 2024）：检索增强检索方法，把初始检索到的前 \(n\) 篇文档作为上下文，用 LLM 生成查询扩展。
- **AGR**（Chen et al., 2024）：近期方法，采用多步框架，基于前 \(n\) 个初始检索结果进行分析、生成再精炼，用 LLM 优化扩展。
- **KARw/o KG**：本文 KAR 的消融变体，不能访问 KG 关系，因此只根据式 (3) 中检索到的实体文本文档生成扩展。
- **KARw/o DRF**：本文 KAR 的消融变体，不使用基于文档的关系过滤（Document-based Relation Filtering，DRF）。它改为像 Yasunaga et al. (2021) 和 Zhang et al. (2022) 那样，用实体名称做基于实体的关系过滤。

为做更全面的比较，我们还报告 STaRK 基准中若干有监督基线的结果，包括作为稠密检索代表的 DPR（Karpukhin et al., 2020）、作为语言模型嵌入增强图神经网络代表的 QAGNN（Yasunaga et al., 2021），以及最先进的 LLM 检索智能体 AvaTaR（Wu et al., 2024a）。

### 5.3 实现细节

对所有基于 LLM 的查询扩展方法，主实验使用 Azure OpenAI API 的 GPT-4o（2024-02-01）作为骨干 LLM。第 6.5 节还给出以 LLaMA-3.1-8B-Instruct（Dubey et al., 2024）为骨干 LLM 的额外结果。遵循 Jia et al. (2024) 与 Shen et al. (2024)，主实验中所有查询扩展方法都使用 OpenAI text-embedding-ada-002 模型的稠密嵌入，并用点积计算相似度以及进行文档检索。第 6.5 节还给出以 BM25（Robertson et al., 2009）为检索器的稀疏检索额外结果。当输入长度超过

<!-- 原 PDF 第 6 页 -->

骨干 LLM 或嵌入模型的上下文窗口时，我们对输入进行截断。全部实验在一张 NVIDIA A100-SXM4-80G GPU 上运行。所有基于 LLM 的方法所用提示词见附录 A。

超参数方面，遵循 Chen et al. (2024) 与 Jia et al. (2024)，对 PRF 以及所有使用前 \(n\) 个初始检索结果的方法，我们设 \(n = 3\)。现有基于 LLM 的查询扩展方法（Gao et al., 2023; Shen et al., 2024; Chen et al., 2024）通常在式 (7) 的一次 LLM 推理中采样多个扩展，以增强生成多样性，从而扩大相关信息的覆盖。因此我们沿用这一做法，把默认采样的扩展生成数也设为同一个 \(n = 3\)，以便与 PRF 公平比较。采样查询扩展数量对检索精度的影响在第 6.4 节进一步讨论。对于 KAR 特有的 KG 参数，我们遵循 Zhang et al. (2022) 与 Taunk et al. (2023)，把 \(h\) 跳邻居设为 \(h = 2\)，以避免超过 2 跳后邻居节点数量指数增长。我们取 \(k = 10\)，为聚焦于查询的关系选择 top-\(k\) 邻居。不同 \(k\) 的消融结果见第 6.3 节。各查询扩展方法的相对延迟在第 6.6 节讨论。

**表 2**：合成搜索查询测试集上的检索结果。

| 设置 | 方法 | AMAZON Hit@1 | AMAZON Hit@5 | AMAZON R@20 | AMAZON MRR | MAG Hit@1 | MAG Hit@5 | MAG R@20 | MAG MRR | PRIME Hit@1 | PRIME Hit@5 | PRIME R@20 | PRIME MRR |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 有监督 | DPR | 15.29 | 47.93 | 44.49 | 30.20 | 10.51 | 35.23 | 42.11 | 21.34 | 4.46 | 21.85 | 30.13 | 12.38 |
| 有监督 | QAGNN | 26.56 | 50.01 | 52.05 | 37.75 | 12.88 | 39.01 | 46.97 | 29.12 | 8.85 | 21.35 | 29.63 | 14.73 |
| 有监督 | AvaTaR | 49.87 | 69.16 | 60.57 | 58.70 | 44.36 | 59.66 | 50.63 | 51.15 | 18.44 | 36.73 | 39.31 | 26.73 |
| 零样本 | Base | 39.16 | 62.73 | 53.29 | 50.35 | 29.08 | 49.61 | 48.36 | 38.62 | 12.63 | 31.49 | 36.00 | 21.41 |
| 零样本 | PRF | 40.07 | 60.66 | 51.24 | 49.79 | 29.04 | 47.65 | 46.69 | 37.90 | 12.46 | 28.63 | 33.04 | 20.06 |
| 零样本 | HyDE | 40.31 | 64.43 | 53.71 | 51.42 | 29.98 | 50.10 | 50.02 | 39.58 | 16.85 | 37.59 | 43.55 | 26.56 |
| 零样本 | RAR | 51.52 | 66.63 | 54.63 | 58.73 | 39.02 | 52.87 | 50.87 | 45.74 | 22.53 | 40.84 | 44.50 | 30.93 |
| 零样本 | AGR | 49.82 | 62.97 | 53.38 | 56.77 | 39.29 | 53.66 | 51.89 | 46.20 | 25.85 | 44.41 | 46.63 | 35.04 |
| 零样本 | KARw/o KG | 43.54 | 60.29 | 51.83 | 51.80 | 31.14 | 46.75 | 46.86 | 38.88 | 18.03 | 36.27 | 42.00 | 26.84 |
| 零样本 | KARw/o DRF | 47.99 | 67.54 | 56.91 | 57.14 | 45.44 | 63.83 | 58.67 | 53.85 | 25.85 | 46.52 | 48.10 | 35.52 |
| 零样本 | KAR | 54.20 | 68.70 | 57.24 | 61.29 | 50.47 | 65.37 | 60.28 | 57.51 | 30.35 | 49.30 | 50.81 | 39.22 |

## 6 结果

### 6.1 KAR 在文本与关系半结构化检索上表现如何？

表 2 给出合成查询测试集上的结果，表 3 给出人工编写查询留出集上的结果。从中可见，KAR 在所有指标上始终取得最好或次好的性能，验证了它在文本与关系检索上的有效性，以及对真实场景的泛化能力。

对于查询扩展基线，我们发现，若只把初始检索结果用作扩展，即 PRF，对最终检索精度几乎没有提升，甚至会有负面影响，因为低质量的初始检索会给最终检索引入噪声。与此同时，HyDE 用 LLM 凭借其内在知识直接生成查询扩展。然而，若没有来自文档语料的、有据可依的文本知识，HyDE 对检索性能的提升很有限。对于更先进的基于 LLM 的方法，即 RAR 与 AGR，我们观察到：在扩展之前用初始检索结果作为上下文来增强 LLM，并利用其自我精炼能力，确实能提高扩展质量，从而提升检索精度。然而，缺少关系知识仍会导致不正确的文档关系，限制它们在文本与关系半结构化检索上的表现。

对于有监督基线，根据 Wu et al. (2024b)，把文本信息与关系信息都编码成文本来训练稠密检索器存在困难，QAGNN 中的图神经网络计算开销也很大，因而造成显著的性能差距。基于 LLM 的智能体 AvaTaR 在训练数据上优化之后显示出有希望的结果，但 LLM 推理次数很多，成本与效率仍然是挑战。

此外，相对于 MAG 和 PRIME，我们观察到所有方法在 AMAZON 上的总体性能更高，KAR 与基线之间的差距也更小；例如表 2 中 AvaTaR 在 Hit@5 和 R@20 上超过 KAR。这一观察与表 1 的数据特点一致：AMAZON 的文本信息更丰富，因而能被

<!-- 原 PDF 第 7 页 -->

LLM 更好地处理；而 MAG 与 PRIME 中更稠密的关系结构，使 LLM 难以生成高质量扩展。

**表 3**：人工编写搜索查询的留出集上的检索结果。

| 方法 | AMAZON Hit@1 | AMAZON Hit@5 | AMAZON R@20 | AMAZON MRR | MAG Hit@1 | MAG Hit@5 | MAG R@20 | MAG MRR | PRIME Hit@1 | PRIME Hit@5 | PRIME R@20 | PRIME MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Base | 39.50 | 64.20 | 35.46 | 52.65 | 28.57 | 42.86 | 36.40 | 35.95 | 22.02 | 41.28 | 43.98 | 30.63 |
| PRF | 43.21 | 64.20 | 30.19 | 53.53 | 29.76 | 41.67 | 32.91 | 35.66 | 24.77 | 36.70 | 40.65 | 30.35 |
| HyDE | 45.68 | 72.84 | 39.25 | 57.56 | 29.76 | 44.05 | 37.84 | 35.51 | 24.77 | 42.20 | 47.70 | 33.65 |
| RAR | 55.56 | 71.60 | 36.15 | 62.15 | 38.10 | 45.24 | 35.19 | 42.04 | 31.19 | 43.12 | 49.01 | 37.72 |
| AGR | 55.56 | 71.60 | 37.27 | 63.54 | 33.33 | 44.05 | 37.23 | 38.95 | 32.11 | 49.54 | 49.65 | 39.27 |
| KARw/o KG | 49.38 | 67.90 | 33.94 | 57.77 | 30.95 | 40.48 | 30.95 | 35.16 | 29.36 | 47.71 | 53.52 | 37.80 |
| KARw/o DRF | 56.79 | 76.54 | 39.95 | 65.72 | 41.67 | 55.95 | 44.54 | 48.99 | 34.86 | 56.88 | 56.21 | 44.51 |
| KAR | 61.73 | 72.84 | 40.62 | 66.32 | 51.20 | 58.33 | 46.60 | 54.52 | 44.95 | 60.55 | 59.90 | 51.85 |

**图 3**：KAR 中过滤后 top-\(k\) 邻居取不同 \(k\) 时的影响。横轴 \(k\) 的可见刻度为 3、5、10、20、40。三个子图分别对应 AMAZON、MAG、PRIME，纵轴为 Hit@5 与 R@20。可见纵轴刻度约为：AMAZON 的 Hit@5 为 60、65、70，R@20 为 36、38、40、42；MAG 的 Hit@5 为 48、51、54、57，R@20 为 44、46、48、50；PRIME 的 Hit@5 为 56、57、58、59、60，R@20 为 56、58、60、62。曲线数据点抽取不完整。表抽取失败，见原 PDF 第 7 页。

### 6.2 KG 与基于文档的关系过滤（DRF）是否真正有效？

表 2 与表 3 都给出了本方法两个消融变体的结果：不能访问关系知识的 KARw/o KG，以及像 Yasunaga et al. (2021) 和 Zhang et al. (2022) 那样做基于实体的关系过滤的 KARw/o DRF。除表 3 中 AMAZON 的 Hit@5 之外，KAR 始终优于这两个变体。结果表明，文档文本与关系都是必要且有效的，尤其是在关系结构更稠密时能提高检索精度，并且二者协同贡献于 KAR。我们还发现，KARw/o DRF 总体上优于 KARw/o KG。我们将这一结果归因于：LLM 的内在知识可以在一定程度上缓解查询与文档之间的文本语义差距，但它们缺少应从 KG 中得到的、更结构化的关系知识。

### 6.3 过滤后的 top-\(k\) 邻居数量如何影响 KAR？

为进一步研究引入 KG 关系的效果，图 3 给出 KAR 在过滤后 top-\(k\) 邻居的 \(k \in [3, 5, 10, 20, 40]\) 上的检索结果。从结果可见，起初根据文本文档纳入更多聚焦于查询的邻居，确实能提高检索精度，因为覆盖了更多有用的文档关系。然而，随着 \(k\) 变大，边际改进减弱；当 \(k\) 增至 40 时，检索精度下降。这表明已经纳入了无关邻居，嘈杂的文档关系影响了 LLM 的查询扩展质量。尽管如此，KAR 在不同 \(k\) 的选择下都表现得有竞争力。

### 6.4 采样的查询扩展数量 \(n\) 是否影响检索精度？

现有基于 LLM 的方法（Gao et al., 2023; Shen et al., 2024; Chen et al., 2024）常常从一次 LLM 推理中采样多个扩展，以增强生成的多样性与覆盖面。为研究它对文本与关系检索的影响，图 4 给出基于 LLM 的方法在采样扩展数 \(n \in [1, 3, 5, 7]\) 下的检索精度。从结果可见，只有在 AMAZON 上它们呈现轻微上升趋势；在 MAG 和 PRIME 上，采样扩展的数量对检索精度没有明显影响。我们将此归因于 MAG 与 PRIME 中更稠密的关系：从 LLM 采样更多扩展无助于识别结构化的文档关系，因而不能改进检索。

### 6.5 KAR 能否与其他检索器和骨干 LLM 一起工作？

为进一步展示 KAR 的灵活性与可扩展性，我们在表 4 中给出检索结果，

<!-- 原 PDF 第 8 页 -->

其中所有参与比较的查询扩展方法都用 BM25 这一稀疏检索器替换基于稠密嵌入的检索；表 5 则给出以 LLaMA-3.1-8B-Instruct 为骨干 LLM 来生成扩展的结果。我们使用与附录 A 相同的提示词，并观察到不同方法之间相似的性能趋势，KAR 始终是最好或次好的。我们还发现，在用查询扩展增强时，基于 BM25 的稀疏检索性能低于基于稠密嵌入的检索，这表明文本与关系半结构化检索具有复杂性。

**表 4**：在人工编写查询上以 BM25 为检索器的结果。

| 方法 | AMAZON Hit@1 | AMAZON Hit@5 | AMAZON R@20 | AMAZON MRR | MAG Hit@1 | MAG Hit@5 | MAG R@20 | MAG MRR | PRIME Hit@1 | PRIME Hit@5 | PRIME R@20 | PRIME MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Base | 34.57 | 55.56 | 22.78 | 44.31 | 32.14 | 41.67 | 29.32 | 36.88 | 23.85 | 43.12 | 39.73 | 31.19 |
| PRF | 38.27 | 56.79 | 22.19 | 46.45 | 29.76 | 50.00 | 37.83 | 38.08 | 25.68 | 40.37 | 41.96 | 32.66 |
| HyDE | 36.63 | 58.44 | 23.39 | 46.29 | 32.14 | 50.40 | 39.72 | 39.84 | 28.44 | 44.65 | 44.40 | 35.79 |
| RAR | 40.74 | 59.26 | 23.39 | 49.09 | 34.23 | 50.00 | 38.41 | 40.90 | 29.82 | 45.18 | 45.05 | 37.02 |
| AGR | 43.46 | 60.25 | 24.12 | 50.90 | 34.76 | 48.57 | 36.90 | 40.59 | 30.64 | 45.50 | 44.94 | 37.50 |
| KAR | 45.06 | 61.32 | 24.10 | 52.24 | 36.51 | 50.20 | 38.69 | 42.41 | 32.26 | 47.25 | 46.06 | 39.14 |

**表 5**：在人工编写查询上以 LLaMA-3.1-8B-Instruct 为骨干 LLM 的检索结果。

| 方法 | AMAZON Hit@1 | AMAZON Hit@5 | AMAZON R@20 | AMAZON MRR | MAG Hit@1 | MAG Hit@5 | MAG R@20 | MAG MRR | PRIME Hit@1 | PRIME Hit@5 | PRIME R@20 | PRIME MRR |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Base | 39.50 | 64.20 | 35.46 | 52.65 | 28.57 | 42.86 | 36.40 | 35.95 | 22.02 | 41.28 | 43.98 | 30.63 |
| PRF | 43.21 | 64.20 | 30.19 | 53.53 | 29.76 | 41.67 | 32.91 | 35.66 | 24.77 | 36.70 | 40.65 | 30.35 |
| HyDE | 43.21 | 65.43 | 36.11 | 53.92 | 22.62 | 38.10 | 29.78 | 29.23 | 21.10 | 39.45 | 42.61 | 29.95 |
| RAR | 50.62 | 62.96 | 33.67 | 57.84 | 33.33 | 41.67 | 32.01 | 37.37 | 28.44 | 44.95 | 50.12 | 36.13 |
| AGR | 51.85 | 70.37 | 35.70 | 59.91 | 30.95 | 39.29 | 32.11 | 35.20 | 23.85 | 44.95 | 50.00 | 34.43 |
| KAR | 51.85 | 71.60 | 37.78 | 60.70 | 42.86 | 54.76 | 41.36 | 47.31 | 41.28 | 55.96 | 56.45 | 48.12 |

**图 4**：采样查询扩展数 \(n\) 的影响。横轴 \(n\) 的可见刻度为 1、3、5、7，纵轴为 Hit@1。可见纵轴刻度约为：AMAZON 为 45、50、55、60；MAG 为 30、40、50；PRIME 为 25、35、45。图例为 HyDE、RAR、AGR、KAR。曲线数据点抽取不完整。表抽取失败，见原 PDF 第 8 页。

### 6.6 在检索延迟上，KAR 与其他方法相比如何？

由于各方法的延迟会因实现和 API 版本而不同，我们按第 5.3 节的规定使它们保持一致，并在图 5 中报告结果以供相对比较。我们观察到，PRF 与 HyDE 的延迟最低，因为它们在最终检索之前只额外引入一次检索或一次 LLM 推理。RAR 把初始检索结果作为 LLM 推理的上下文，由于额外的检索以及更长的文本输入，延迟更高。

**图 5**：查询扩展的延迟比较。横轴为相对延迟，分组为 AMAZON、MAG、PRIME，方法为 PRF、HyDE、RAR、AGR、KAR。图中未抽出具体柱高数值，见原 PDF 第 8 页。

AGR 实现了多步精炼框架，涉及五次 LLM 推理，延迟大约是 RAR 的两倍；Chen et al. (2024) 也提示了这一观察。KAR 并不引入额外的 LLM 推理，而是用 KG 提供结构化关系知识，因而可以快速推理：在取得可观性能提升的同时，只增加少量额外延迟。

## 7 结论

本文提出一种面向文本与关系检索的知识感知查询扩展框架，利用文本文档之间的 KG 关系来增强 LLM 的查询扩展生成。通过协同利用文本知识与关系知识，我们以文档文本作为丰富的 KG 节点表示来过滤聚焦于查询的关系，从而实现知识感知检索。在三个不同领域的半结构化检索数据集上的实验表明，相对最先进的查询扩展方法，本方法具有优势，并展示了它处理真实世界复杂搜索查询的适用性。

<!-- 原 PDF 第 9 页 -->

## 局限性

与所有现有基于 LLM 的查询扩展方法类似，KAR 的一个局限是第 6.6 节所讨论的检索效率。虽然我们已经把框架优化为每条搜索查询只包含两次 LLM 推理，API 调用的延迟仍可能受变化的服务器负载影响。尽管第 6.5 节也展示了 KAR 配合 LLaMA-3.1-8B-Instruct 进行本地 LLM 推理时的有效性，计算约束与部署成本仍是实际应用中需要另行考虑的重要因素。因此，未来工作可以进一步探索 LLM 推理的加速与成本优化，例如并行推理，从而实现更高效的查询扩展。

## 参考文献

Hiteshwar Kumar Azad and Akshay Deepak. 2019. 信息检索中的查询扩展技术：综述. *Information Processing & Management*, 56(5):1698–1735.

Derian Boer, Fabian Koch, and Stefan Kramer. 2024. 借助基于三元组的预过滤，利用半结构化知识与大语言模型进行问答. arXiv preprint arXiv:2409.00861.

Guihong Cao, Jian-Yun Nie, Jianfeng Gao, and Stephen Robertson. 2008. 为伪相关反馈选择优质扩展词. In *Proceedings of the 31st annual international ACM SIGIR conference on Research and development in information retrieval*, pages 243–250.

Shulin Cao, Jiaxin Shi, Liangming Pan, Lunyiu Nie, Yutong Xiang, Lei Hou, Juanzi Li, Bin He, and Hanwang Zhang. 2022. KQA Pro：带有显式组合程序、面向知识库复杂问答的数据集. In *Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 6101–6119, Dublin, Ireland. Association for Computational Linguistics.

Payal Chandak, Kexin Huang, and Marinka Zitnik. 2023. 构建知识图谱以支持精准医学. *Scientific Data*, 10(1):67.

Xinran Chen, Xuanang Chen, Ben He, Tengfei Wen, and Le Sun. 2024. 分析、生成与精炼：面向零样本开放域问答的大语言模型查询扩展. In *Findings of the Association for Computational Linguistics ACL 2024*, pages 11908–11922, Bangkok, Thailand and virtual meeting. Association for Computational Linguistics.

Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan, et al. 2024. Llama 3 模型族群. arXiv preprint arXiv:2407.21783.

Yanlin Feng, Xinyue Chen, Bill Yuchen Lin, Peifeng Wang, Jun Yan, and Xiang Ren. 2020. 面向知识感知问答的可扩展多跳关系推理. In *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, pages 1295–1309, Online. Association for Computational Linguistics.

Luyu Gao, Xueguang Ma, Jimmy Lin, and Jamie Callan. 2023. 无需相关性标签的精确零样本稠密检索. In *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 1762–1777, Toronto, Canada. Association for Computational Linguistics.

Ruining He and Julian McAuley. 2016. 起落：用单类协同过滤建模时尚趋势的视觉演化. In *proceedings of the 25th international conference on world wide web*, pages 507–517.

Xiaoxin He, Yijun Tian, Yifei Sun, Nitesh V Chawla, Thomas Laurent, Yann LeCun, Xavier Bresson, and Bryan Hooi. 2024. G-Retriever：面向文本图理解与问答的检索增强生成. arXiv preprint arXiv:2402.07630.

Weihua Hu, Matthias Fey, Marinka Zitnik, Yuxiao Dong, Hongyu Ren, Bowen Liu, Michele Catasta, and Jure Leskovec. 2020. 开放图基准：图上机器学习数据集. *Advances in neural information processing systems*, 33:22118–22133.

Yuntong Hu, Zhihan Lei, Zheng Zhang, Bo Pan, Chen Ling, and Liang Zhao. 2024. GRAG：图检索增强生成. arXiv preprint arXiv:2405.16506.

Rolf Jagerman, Honglei Zhuang, Zhen Qin, Xuanhui Wang, and Michael Bendersky. 2023. 通过提示大语言模型进行查询扩展. arXiv preprint arXiv:2305.03653.

Pengyue Jia, Yiding Liu, Xiangyu Zhao, Xiaopeng Li, Changying Hao, Shuaiqiang Wang, and Dawei Yin. 2024. MILL：用大语言模型相互验证的零样本查询扩展. In *Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)*, pages 2498–2518, Mexico City, Mexico. Association for Computational Linguistics.

Xinke Jiang, Ruizhe Zhang, Yongxin Xu, Rihong Qiu, Yue Fang, Zhiyuan Wang, Jinyi Tang, Hongxin Ding, Xu Chu, Junfeng Zhao, et al. 2024. HyKGE：面向准确且可靠的医学大语言模型回答的假设知识图谱增强框架. arXiv preprint arXiv:2312.15883.

<!-- 原 PDF 第 10 页 -->

Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, and Wen-tau Yih. 2020. 面向开放域问答的稠密段落检索. In *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, pages 6769–6781, Online. Association for Computational Linguistics.

Yibin Lei, Yu Cao, Tianyi Zhou, Tao Shen, and Andrew Yates. 2024. 语料引导的大语言模型查询扩展. In *Proceedings of the 18th Conference of the European Chapter of the Association for Computational Linguistics (Volume 2: Short Papers)*, pages 393–401, St. Julian’s, Malta. Association for Computational Linguistics.

Hang Li, Shengyao Zhuang, Ahmed Mourad, Xueguang Ma, Jimmy Lin, and Guido Zuccon. 2022. 用伪相关反馈改进稠密检索的查询表示：一项可复现性研究. In *European Conference on Information Retrieval*, pages 599–612. Springer.

Yuxiao Lin, Yuxian Meng, Xiaofei Sun, Qinghong Han, Kun Kuang, Jiwei Li, and Fei Wu. 2021. BertGCN：结合 GNN 与 BERT 的直推式文本分类. In *Findings of the Association for Computational Linguistics: ACL-IJCNLP 2021*, pages 1456–1462, Online. Association for Computational Linguistics.

Linhao Luo, Yuan-Fang Li, Reza Haf, and Shirui Pan. 2024. 在图上推理：忠实且可解释的大语言模型推理. In *The Twelfth International Conference on Learning Representations*.

Yuanhua Lv and ChengXiang Zhai. 2010. 面向伪相关反馈的位置相关性模型. In *Proceedings of the 33rd international ACM SIGIR conference on Research and development in information retrieval*, pages 579–586.

Julian McAuley, Christopher Targett, Qinfeng Shi, and Anton Van Den Hengel. 2015. 基于图像的风格与替代品推荐. In *Proceedings of the 38th international ACM SIGIR conference on research and development in information retrieval*, pages 43–52.

Shirui Pan, Linhao Luo, Yufei Wang, Chen Chen, Jiapu Wang, and Xindong Wu. 2024. 统一大语言模型与知识图谱：一份路线图. *IEEE Transactions on Knowledge and Data Engineering*.

Liana Patel, Siddharth Jha, Carlos Guestrin, and Matei Zaharia. 2024. Lotus：使大语言模型能够对非结构化与结构化数据表进行语义查询. arXiv preprint arXiv:2407.11418.

Boci Peng, Yun Zhu, Yongchao Liu, Xiaohe Bo, Haizhou Shi, Chuntao Hong, Yan Zhang, and Siliang Tang. 2024. 图检索增强生成：综述. arXiv preprint arXiv:2408.08921.

Stephen Robertson, Hugo Zaragoza, et al. 2009. 概率相关性框架：BM25 及其拓展. *Foundations and Trends® in Information Retrieval*, 3(4):333–389.

Tao Shen, Guodong Long, Xiubo Geng, Chongyang Tao, Yibin Lei, Tianyi Zhou, Michael Blumenstein, and Daxin Jiang. 2024. 检索增强检索：大语言模型是强大的零样本检索器. In *Findings of the Association for Computational Linguistics ACL 2024*, pages 15933–15946, Bangkok, Thailand and virtual meeting. Association for Computational Linguistics.

Giuseppe Spillo, Cataldo Musto, Marco Polignano, Pasquale Lops, Marco de Gemmis, and Giovanni Semeraro. 2023. 结合图神经网络与句子编码器进行知识感知推荐. In *Proceedings of the 31st ACM Conference on User Modeling, Adaptation and Personalization*, pages 1–12.

Jiashuo Sun, Chengjin Xu, Lumingyuan Tang, Saizhuo Wang, Chen Lin, Yeyun Gong, Lionel Ni, Heung-Yeung Shum, and Jian Guo. 2024. Think-on-Graph：大语言模型在知识图谱上的深度且负责任推理. In *The Twelfth International Conference on Learning Representations*.

Alon Talmor and Jonathan Berant. 2018. 把万维网当作回答复杂问题的知识库. In *Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long Papers)*, pages 641–651, New Orleans, Louisiana. Association for Computational Linguistics.

Dhaval Taunk, Lakshya Khanna, Siri Venkata Pavan Kumar Kandru, Vasudeva Varma, Charu Sharma, and Makarand Tapaswi. 2023. GrapeQA：用图增强与剪枝来改进问答. In *Companion Proceedings of the ACM Web Conference 2023, WWW ’23 Companion*, page 1138–1144, New York, NY, USA. Association for Computing Machinery.

Junjie Wang, Mingyang Chen, Binbin Hu, Dan Yang, Ziqi Liu, Yue Shen, Peng Wei, Zhiqiang Zhang, Jinjie Gu, Jun Zhou, et al. 2024. 从知识图谱中学习为检索增强大语言模型做规划. arXiv preprint arXiv:2406.14282.

Kuansan Wang, Zhihong Shen, Chiyuan Huang, Chieh-Han Wu, Yuxiao Dong, and Anshul Kanakia. 2020. 微软学术图谱：当专家还不够时. *Quantitative Science Studies*, 1(1):396–413.

Liang Wang, Nan Yang, and Furu Wei. 2023. Query2Doc：用大语言模型进行查询扩展. In *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing*, pages 9414–9423, Singapore. Association for Computational Linguistics.

<!-- 原 PDF 第 11 页 -->

Shirley Wu, Shiyu Zhao, Qian Huang, Kexin Huang, Michihiro Yasunaga, Kaidi Cao, Vassilis N. Ioannidis, Karthik Subbian, Jure Leskove, and James Zou. 2024a. Avatar：为工具辅助的知识检索优化大语言模型智能体. In *NeurIPS*.

Shirley Wu, Shiyu Zhao, Michihiro Yasunaga, Kexin Huang, Kaidi Cao, Qian Huang, Vassilis N. Ioannidis, Karthik Subbian, James Zou, and Jure Leskovec. 2024b. STaRK：在文本与关系知识库上对大语言模型检索进行基准评测. In *NeurIPS Datasets and Benchmarks Track*.

Zhentao Xu, Mark Jerome Cruz, Matthew Guevara, Tie Wang, Manasi Deshpande, Xiaofeng Wang, and Zheng Li. 2024. 面向客服问答的、结合知识图谱的检索增强生成. In *Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval*, pages 2905–2909.

Michihiro Yasunaga, Hongyu Ren, Antoine Bosselut, Percy Liang, and Jure Leskovec. 2021. QA-GNN：结合语言模型与知识图谱进行问答推理. In *Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies*, pages 535–546, Online. Association for Computational Linguistics.

Shipeng Yu, Deng Cai, Ji-Rong Wen, and Wei-Ying Ma. 2003. 利用网页分割改进网络信息检索中的伪相关反馈. In *Proceedings of the 12th international conference on World Wide Web*, pages 11–18.

Xikun Zhang, Antoine Bosselut, Michihiro Yasunaga, Hongyu Ren, Percy Liang, Christopher D Manning, and Jure Leskovec. 2022. GreaseLM：图推理增强的语言模型. In *International Conference on Learning Representations*.

Yutao Zhu, Huaying Yuan, Shuting Wang, Jiongnan Liu, Wenhan Liu, Chenlong Deng, Haonan Chen, Zhicheng Dou, and Ji-Rong Wen. 2023. 面向信息检索的大语言模型：综述. arXiv preprint arXiv:2308.07107.

## 附录 A 基于 LLM 的方法所用提示词

本节给出实验中所有基于 LLM 的查询扩展方法所用的提示词。HyDE 与 RAR 的提示词见表 6，AGR 各模块的提示词见表 7。KAR 的提示词见表 8。我们总体上遵循各比较方法的原始提示词（Gao et al., 2023; Shen et al., 2024; Chen et al., 2024），并做了轻微调整，以使这些方法适于所评估的文本与关系检索任务。例如，我们遵循 Wu et al. (2024a)，向 LLM 提供 STaRK 基准中每个数据集的文档结构信息，以帮助它们生成格式更好的查询扩展。提示词中使用的各数据集文档结构见表 9。数据集的更多细节请参见 Wu et al. (2024b)。

**表 6**：HyDE 与 RAR 的提示词。

HyDE：

```text
"""给定文档结构：{doc_struct}，
撰写一份能够回答下列用户查询的文档。只返回该文档，不要任何额外文本。
查询：{query}
文档："""
```

RAR：

```text
"""给定文档结构：{doc_struct}，
以及初始检索到的文档：
{PRF_doc_1}
{PRF_doc_2}
{PRF_doc_3}
撰写一份能够回答下列用户查询的文档。只返回该文档，不要任何额外文本。
查询：{query}
文档："""
```

<!-- 原 PDF 第 12 页 -->

**表 7**：AGR 中不同模块的提示词。

Extract（抽取）：

```text
"""给定下列用户查询，写一份关键词列表。只返回关键词，不要任何额外文本。
查询：{query}
关键词："""
```

Analyze（分析）：

```text
"""给定下列用户查询以及抽取出的关键词：{extracted_keywords}，不要试图解释或回答该问题，只提供查询分析：
查询：{query}
分析："""
```

Generate1（生成 1）：

```text
"""给定文档结构：{doc_struct}，
以及查询分析：{query_analysis}，撰写一份能够回答下列用户查询的文档。只返回该文档，不要任何额外文本。
查询：{query}
文档："""
```

Generate2（生成 2）：

```text
"""给定文档结构：{doc_struct}，
以及初始检索到的文档：
{AGR_retrieved_doc_1}
{AGR_retrieved_doc_2}
...
{AGR_retrieved_doc_9}
撰写一份能够回答下列用户查询的文档。只返回该文档，不要任何额外文本。
查询：{query}
文档："""
```

Refine（精炼）：

```text
"""给定候选文档：
{AGR_generated_doc_1}
{AGR_generated_doc_2}
{AGR_generated_doc_3}
评估每份候选文档的准确性与可靠性。指出答案中的任何错误信息或不正确事实。然后撰写一份最能回答下列用户查询的正确文档。只返回该文档，不要任何额外文本。
查询：{query}
文档："""
```

**表 8**：KAR 中不同模块的提示词。

Parse（解析）：

```text
"""给定文档结构：{doc_struct}，
识别下列用户查询中的命名实体。遵循文档结构，按如下格式为每个实体写一份文档：
{document type: {document attributes}}。
查询：{query}
文档："""
```

Generate（生成）：

```text
"""给定文档结构：{doc_struct}，
以及检索到的文本与关系文档：
{KAR_document_triples}
抽取有助于回答下列用户查询的有用信息。然后撰写一份回答下列用户查询的文档。只返回该文档，不要任何额外文本。
查询：{query}
文档："""
```

**表 9**：三个数据集的文档结构。字段名按原文保留。`molecular_function` 与 `cellular_component` 的属性列表在原文中于 `name` 与 `source` 之间换行，抽取文本里没有逗号，按下式保留，未补写。

```text
AMAZON
{
"product": ["title", "brand", "description",
"features", "reviews", "Q&A"],
"brand": ["brand_name"],
"category": ["category_name"],
"color": ["color_name"]
}

MAG
{
"paper": ["title", "abstract", "publication date", "venue"],
"author": ["name"],
"institution": ["name"],
"field_of_study": ["name"]
}

PRIME
{
"disease": ["id", "type", "name", "source",
"details"],
"gene/protein": ["id", "type", "name",
"source", "details"],
"molecular_function": ["id", "type", "name"
"source"],
"drug": ["id", "type", "name", "source",
"details"],
"pathway": ["id", "type", "name", "source",
"details"],
"anatomy": ["id", "type", "name", "source"],
"biological_process": ["id", "type", "name",
"source"],
"cellular_component": ["id", "type", "name"
"source"],
"exposure": ["id", "type", "name", "source"]
}
```

<!-- 译完 -->
