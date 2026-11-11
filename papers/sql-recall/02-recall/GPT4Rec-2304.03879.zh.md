# GPT4Rec：面向个性化推荐与用户兴趣解释的生成式框架

- 原文件名：GPT4Rec-2304.03879.pdf
- 原标题：GPT4Rec: A Generative Framework for Personalized Recommendation and User Interests Interpretation
- 中文标题：GPT4Rec：面向个性化推荐与用户兴趣解释的生成式框架
- 作者：Jinming Li、Wentao Zhang、Tian Wang、Guanglei Xiong、Alan Lu、Gerard Medioni
- 会议或 arXiv：页边标注为 arXiv:2304.03879v1 [cs.IR] 8 Apr 2023。PDF 页眉为 ACM 模板占位文字 “Conference acronym ’XX, June 03–05, 2018, Woodstock, NY”，并非正式会议名称。

<!-- 原 PDF 第 1 页 -->

Jinming Li$^1$，Wentao Zhang$^2$，Tian Wang$^2$，Guanglei Xiong$^2$，Alan Lu$^2$，Gerard Medioni$^2$

lijinmin@umich.edu，{wentazha, wangtan, glx, alalu, medioni}@amazon.com

$^1$University of Michigan, Ann Arbor　　$^2$Amazon, United States

## 摘要

自然语言处理（NLP）的最新进展催生了一批基于 NLP 的推荐系统，并展现出更优的性能。然而，现有模型通常把物品仅仅当作 ID，并采用判别式建模，因而存在三方面局限：（1）不能充分运用物品的内容信息以及 NLP 模型的语言建模能力；（2）难以解释用户兴趣，从而提升相关性与多样性；（3）难以适应物品库持续增长等实际情形。为克服这些局限，我们提出 GPT4Rec，一种受搜索引擎启发的、新颖且灵活的生成式框架。它首先根据用户历史中的物品标题生成假设性的“搜索查询”，再通过检索这些查询来召回用于推荐的物品。该框架在语言空间中同时学习用户嵌入与物品嵌入，从而克服了以往的局限。为了从不同方面、不同粒度上更好地捕捉用户兴趣，以提升相关性与多样性，我们提出一种结合束搜索的多查询生成技术。生成的查询天然就是可解释的用户兴趣表示，并且可以被检索，从而推荐冷启动物品。在 GPT-2 语言模型与 BM25 搜索引擎上，我们的框架在两个公开数据集上的 Recall@K 分别超越当时最先进方法 75.7% 与 22.2%。实验进一步表明，结合束搜索的多查询生成同时提高了召回物品的多样性，以及用户多重兴趣的覆盖度。我们还通过定性案例讨论了所生成查询的适应性与可解释性。

## CCS 概念

- Information systems → Recommender systems。

## 关键词

个性化推荐，用户兴趣建模，生成式语言模型，查询生成，搜索

## ACM 参考文献格式

Jinming Li$^1$, Wentao Zhang$^2$, Tian Wang$^2$, Guanglei Xiong$^2$, Alan Lu$^2$, Gerard Medioni$^2$. 2018. GPT4Rec: A Generative Framework for Personalized Recommendation and User Interests Interpretation. In Proceedings of Make sure to enter the correct conference title from your rights confirmation email (Conference acronym ’XX). ACM, New York, NY, USA, 5 pages. https://doi.org/XXXXXXX.XXXXXXX

允许为个人或课堂使用而制作本作品全部或部分的数字或纸质副本，无须付费，前提是副本不为牟利或商业利益而制作或分发，并且副本在首页带有本声明及完整引用。本作品中由 ACM 以外主体拥有的组件，其版权必须得到尊重。允许带署名的摘要。除此之外的复制、再版、在服务器上张贴或向列表再分发，均须事先获得特定许可和/或支付费用。许可请求请寄至 permissions@acm.org。

Conference acronym ’XX, June 03–05, 2018, Woodstock, NY

© 2018 Association for Computing Machinery.

ACM ISBN 978-1-4503-XXXX-X/18/06...$15.00

https://doi.org/XXXXXXX.XXXXXXX

## 1 引言

推荐系统是一类信息过滤系统，为特定用户提供相关物品的个性化建议，已广泛用于电子商务与社交媒体等应用 [4, 11, 14, 19]。随着自然语言处理（NLP）的发展，许多基于 NLP 的模型通过建模用户—物品交互序列来做个性化推荐 [9, 27, 30]。大语言模型（LLM，[1, 5, 17, 24]）在各类 NLP 任务乃至对话（ChatGPT [16]）上取得的优异表现，推动了基于 LLM 的推荐系统研究 [6, 10, 15, 22, 23, 29]。其中，BERT4Rec [23] 采用了 BERT [5] 的双向自注意力结构，并优于其他基于 NLP 的模型以及序列模型 [9, 10, 18]。

尽管模型性能有所提升，现有基于 NLP 的模型 [6, 10, 15, 22, 23, 29] 通常仍把物品仅仅当作 ID，并采用判别式建模，因而有如下局限。首先，这些模型无法充分运用物品的内容信息以及 NLP 模型的语言建模能力。其次，它们无法适应不断变化、不断增长的物品库，而这两者都是重要的实际问题 [12, 21]。此外，判别式模型难以解释用户兴趣，而这种解释对于提升推荐的多样性与质量至关重要 [2, 3, 13, 28]。

为应对这些局限，我们提出 GPT4Rec，一种新颖、灵活的个性化推荐生成式框架，同时提供对用户兴趣的解释。我们的框架受搜索引擎启发：GPT4Rec 先用生成式语言模型生成假设性的“搜索查询”，模型输入是用户历史中的物品标题再加上一段生成提示。随后，GPT4Rec 用搜索引擎检索这些生成查询，从而得到推荐物品。GPT4Rec 的关键组件是一个强大的生成式语言模型，它在语言空间中同时学习用户嵌入与物品嵌入，使我们能够利用物品标题中的语义信息，并捕捉用户的多样兴趣。为了解码用户的多重兴趣并提升推荐多样性，我们在查询生成中采用多查询束搜索技术。这些查询是人可读的，并且本身就具有解释用户兴趣的独立价值。此外，用代表用户兴趣的查询去做推荐检索，可以自然地解决物品冷启动问题以及物品库变化问题。最后，GPT4Rec 在实践中也较为有利，因为它可以灵活地接入更先进的 LLM 或搜索引擎以提升性能。

<!-- 原 PDF 第 2 页 -->

图 1 见原 PDF。

**图 1：GPT4Rec 框架的架构。** 图中从左到右包括：输入的物品标题序列（Item Title 1 至 Item Title T）、语言模型（GPT-2）、多束生成的搜索查询（Search Queries, Multi-Beam Generation）、搜索引擎（BM25），以及输出的推荐结果（Item Title 1 至 Item Title N，标记为 Recommendation T+1）。

概括而言，我们的贡献包括：（1）提出 GPT4Rec，一种新颖且灵活的生成式框架，把推荐任务视为“查询生成 + 搜索”；（2）采用多查询束搜索策略，产生多样且可解释的用户兴趣表示；（3）在两个公开数据集上进行实验，表明相对当时最先进方法，Recall@$K$ 有大幅提升；（4）通过定量与定性分析，我们考察并表明：生成查询的数量会提高召回物品的多样性，以及用户多重兴趣的覆盖度。

## 2 方法

所提框架的架构如图 1 所示。给定用户的物品交互序列，GPT4Rec 用一段提示把物品标题格式化，并使用生成式语言模型，在语言空间中同时学习物品嵌入与用户嵌入。模型随后生成多条代表用户兴趣的查询，这些查询被送入搜索引擎以召回推荐物品。本文选用 GPT-2 语言模型与 BM25 搜索引擎，但该框架可以灵活地接入更先进的模型。

### 2.1 基于语言模型的查询生成

GPT4Rec 的第一个组件是生成式语言模型，其目标是从物品交互序列中、在语言空间里学习用户表示，再生成多条代表用户兴趣的查询。我们所选的 GPT-2 具有 1.17 亿参数、采用复杂的 Transformer 式架构，并在大规模语料上预训练；对其微调，符合我们捕捉用户兴趣与物品内容信息的目的。经实验，我们决定用如下提示来格式化模型输入：

> Previously, the customer has bought:
>
> \<ITEM TITLE 1\>. \<ITEM TITLE 2\>...
>
> In the future, the customer wants to buy

（此前，该顾客购买过：\<物品标题 1\>. \<物品标题 2\>…… 将来，该顾客想购买）

其中包含物品标题的语义信息，并对每个用户 $u$ 记为 $W^{u}$。GPT-2 从 $W^{u}$ 学习用户表示，并能够按条件分布 $P(\cdot \mid W^{u})$ 以自回归方式生成查询。

为了更好地表示用户的多样兴趣，并提高推荐结果的多样性，我们提出不只生成单条查询，而是用束搜索技术生成多条查询 [18, 25]。给定束宽 $m$、生成得分函数 $S(\cdot)$，以及长度为 $l$ 的候选查询

$$Q^{l} = (q^{l}_{1}, q^{l}_{2}, \ldots, q^{l}_{m}),$$

束搜索算法将 $Q^{l+1}$ 更新为长度为 $l+1$、且使 $S(W^{u}, q)$ 最大的前 $m$ 条查询，其中

$$q \in \{\,|q| = l+1,\ q_{[1:l]} \in Q^{l}\,\}.$$

最重要的是，这种束搜索策略生成的用户兴趣表示在不同方面和不同粒度上都是多样的。

### 2.2 基于搜索引擎的物品检索

所提框架的第二个组件是搜索引擎，它起到“判别器”的作用。它以每条生成查询为输入，用匹配得分函数在物品库中检索最相关的物品作为输出。匹配得分函数衡量语言空间上的相似度，其角色类似于向量嵌入方法中的内积相似度 [4, 19]。我们选用 BM25 匹配得分函数 [20]，因为它是使用最广的基线搜索引擎之一，并用两个相应参数 $k_1$ 与 $b$ 来考虑词频饱和以及文档长度。

设 $K$ 为推荐物品总数，$m$ 为生成查询的条数。我们提出一种基于排序的策略来合并每条查询的检索结果。它首先从生成得分最高的查询的检索结果中取出前 $K/m$ 个物品，再按其得分排序，从其余查询中依次加入 $K/m$ 个不重复的物品。该策略能够在召回物品的相关性与多样性之间取得平衡。

### 2.3 训练策略

我们提出一种灵活的两步训练流程，分别优化语言模型与搜索引擎，这在实践中有利于模型迭代。给定每个用户 $u$ 的物品交互序列 $i_1, i_2, \ldots, i_T$，我们取第 2.1 节所示提示中的前 $T-1$ 个物品标题，再将其与最后一个物品 $i_T$ 的标题拼接，构成训练语料，用以微调预训练的 GPT-2。该策略受到对比学习文献的启发 [8]，其基本想法是：最细粒度、最准确的搜索查询就是目标物品标题本身。语言模型训练完成后，我们用网格搜索优化 BM25 参数 $k_1$ 与 $b$，使检索生成查询以召回目标物品时的性能最好。

## 3 实验

### 3.1 实验设置

#### 3.1.1 数据

我们在两个公开数据集上进行实验，即 5-core Amazon Review 数据 [7] 中的 Beauty 与 Electronics 两个类目。缺失标题或标题噪声过大（超过 400 个字符）的物品被丢弃。每个用户的物品交互序列去重，并截断到最大长度 15。预处理后数据集的描述统计见表 2。按照下一物品预测任务的设定 [23]，用户序列按 0.8 / 0.1 / 0.1 的比例划分为训练集、验证集与测试集，每条测试序列的最后一个物品作为预测目标。

#### 3.1.2 评价指标

Recall@$K$ 是下一物品预测所关注的主要指标，它衡量前 $K$ 个推荐物品中是否包含目标物品，并对所有用户取平均。除 Recall@$K$ 外，我们还关注：

<!-- 原 PDF 第 3 页 -->

**表 1：基线方法与所提框架在不同生成查询条数下的总体性能。** 最佳性能以粗体标出，最佳基线结果以下划线标出。

| 数据集 | Recall@$K$ | FM-BPR | ContentRec | YouTubeDNN | BERT4Rec | GPT4Rec 5 Queries | 10 Queries | 20 Queries | 40 Queries |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Beauty | $K=5$ | 0.0356 | 0.0254 | <u>0.0376</u> | 0.0355 | **0.0653** | — | — | — |
| Beauty | $K=10$ | 0.0499 | 0.0440 | <u>0.0549</u> | 0.0513 | 0.0810 | **0.1036** | — | — |
| Beauty | $K=20$ | 0.0716 | 0.0644 | 0.0753 | <u>0.0816</u> | 0.1027 | 0.1252 | **0.1454** | — |
| Beauty | $K=40$ | 0.1040 | 0.0952 | 0.1066 | <u>0.1161</u> | 0.1297 | 0.1522 | 0.1743 | **0.2040** |
| Electronics | $K=5$ | 0.0345 | 0.0241 | 0.0352 | <u>0.0362</u> | **0.0434** | — | — | — |
| Electronics | $K=10$ | 0.0387 | 0.0307 | 0.0435 | <u>0.0451</u> | 0.0480 | **0.0545** | — | — |
| Electronics | $K=20$ | 0.0441 | 0.0391 | 0.0539 | <u>0.0573</u> | 0.0524 | 0.0607 | **0.0705** | — |
| Electronics | $K=40$ | 0.0505 | 0.0494 | 0.0684 | <u>0.0751</u> | 0.0574 | 0.0672 | 0.0788 | **0.0918** |

粗体与下划线按表题规则标出：每行最高值为粗体，基线四列中的最高值为下划线。数字与原 PDF 一致。

**表 2：数据集统计。**

| 名称 | #User | #Item | #Interaction | Ave. Length | Meta Info. |
| --- | ---: | ---: | ---: | ---: | --- |
| Beauty | 22,254 | 11,778 | 190,726 | 7.439 | Cate. |
| Electronics | 728,719 | 159,456 | 6,724,382 | 7.797 | Cate., Brand |

Diversity@$K$ [3] 衡量物品之间的不相似度：

$$\mathrm{Diversity@}K = \mathrm{Average}\left[1 - \frac{\sum_{i_1 \neq i_2}\mathrm{Sim}(i_1, i_2)}{K(K-1)}\right],$$

其中我们在物品类目或品牌上采用 Jaccard 相似度$^1$。Coverage@$K$ 衡量推荐物品集合 $R$ 在类目或品牌上对用户序列 $U$ 的覆盖程度：

$$\mathrm{Coverage@}K = \mathrm{Average}\left[\frac{\left|\left(\bigcup_{i \in R}\mathrm{Cate}_i\right) \cap \left(\bigcup_{i \in U}\mathrm{Cate}_i\right)\right|}{\left|\bigcup_{i \in U}\mathrm{Cate}_i\right|}\right],$$

它是衡量用户多重兴趣覆盖度的更合理指标，因为 Diversity@$K$ 会偏向完全随机或不相关的推荐。

#### 3.1.3 基线方法

FM-BPR [11] 是带有贝叶斯个性化排序准则的因子分解机模型，从用户—物品交互矩阵中学习协同信息。

ContentRec 是工业界广泛使用的基于内容的模型，从物品标题学习词袋嵌入，并对用户交互过的物品做均值池化以得到用户嵌入。

YouTubeDNN [4] 是工业界最流行的深度学习模型之一，用神经网络学习用户/物品嵌入。

BERT4Rec [23] 是当时最先进的基于 BERT 的模型，具有双向自注意力架构和掩码训练策略。

#### 3.1.4 实现细节

我们实现 HuggingFace [26] 发布的、具有 1.17 亿参数的 GPT-2 模型，使用带权重衰减的 Adam 优化器微调 20 个 epoch。学习率设为 0.0001，优化器以 2000 步预热进行初始化。BM25 在 $k_1 \in [0, 3]$、$b \in (0, 1)$ 上按前文所述方法优化。

ContentRec 使用 StarSpace [27] 学习物品标题嵌入，其他基线方法用公开的 Github 仓库实现$^2$。对所有基线方法，我们从 64、128、256 中在验证集上选择最优嵌入维度，其余超参数按原论文作者的建议设置。

$^1$ https://en.wikipedia.org/wiki/Jaccard_index

$^2$ LightFM: https://github.com/lyst/lightfm ；StarSpace: https://github.com/facebookresearch/StarSpace ；DeepMatch: https://github.com/shenweichen/DeepMatch ；RecBole: https://github.com/RUCAIBox/RecBole

### 3.2 定量分析

#### 3.2.1 总体性能

表 1 汇总了 GPT4Rec 在不同生成查询条数下、相对于基线方法、在两个数据集上的 Recall@$K$。我们提出的框架在两个数据集上都优于全部基线：在规模较小的 Beauty 数据集上，Recall@40 的相对提升为 75.7%；在规模较大的 Electronics 数据集上为 22.2%。与基线的比较表明，物品内容信息与现代语言建模都是取得更优性能的关键成分。一方面，BERT4Rec 借助现代语言建模技术，在基线中性能最好，但它把物品当作 ID，未能充分利用物品内容信息。另一方面，ContentRec 虽使用物品内容信息，但其词袋嵌入与均值池化建模不足以达到可比的性能。

#### 3.2.2 多查询生成的优势

观察表 1 中两个数据集的下三角数值，沿行方向、列方向和对角方向都能看到单调上升的趋势。这些趋势表明，多查询束搜索生成策略大幅提高了推荐物品的相关性。特别地，生成 $K$ 条查询、每条查询检索一个物品，能得到最好的 Recall@$K$。这一发现说明，每条查询都包含足够的细节来检索到一个相关物品。

我们进一步考察推荐物品中用户兴趣的多样性与覆盖度，以及它们与多查询生成策略的关系。如表 3 所示，对 Diversity@$K$ 与 Coverage@$K$ 而言，最佳性能都是在生成 $K$ 条查询且每条查询检索一个物品时取得的，这与表 1 中关于 Recall@$K$ 的发现一致。类似的单调上升趋势表明，多查询生成策略产生了更全面的用户兴趣表示。另一方面，从 Diversity@$K$ 的各列可以看到，若只增大 $K$ 而不增加查询条数，多样性不会提高。这说明搜索本身无助于提升多样性。

<!-- 原 PDF 第 4 页 -->

**表 3：用户兴趣的多样性与覆盖度随生成查询条数的变化。** 两个数据集上，就类目/品牌信息而言的最高值以粗体标出。

| 指标 | $K$ | Beauty (Category) 5 | 10 | 20 | 40 | Electronics (Category) 5 | 10 | 20 | 40 | Electronics (Brand) 5 | 10 | 20 | 40 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Diversity@$K$ | $K=5$ | **0.679** | — | — | — | **0.671** | — | — | — | **0.534** | — | — | — |
| Diversity@$K$ | $K=10$ | 0.654 | **0.716** | — | — | 0.617 | **0.733** | — | — | 0.529 | **0.643** | — | — |
| Diversity@$K$ | $K=20$ | 0.659 | 0.706 | **0.749** | — | 0.605 | 0.703 | **0.778** | — | 0.559 | 0.645 | **0.717** | — |
| Diversity@$K$ | $K=40$ | 0.679 | 0.715 | 0.749 | **0.783** | 0.601 | 0.696 | 0.762 | **0.811** | 0.604 | 0.669 | 0.724 | **0.767** |
| Coverage@$K$ | $K=5$ | **0.417** | — | — | — | **0.321** | — | — | — | **0.173** | — | — | — |
| Coverage@$K$ | $K=10$ | 0.472 | **0.547** | — | — | 0.340 | **0.425** | — | — | 0.177 | **0.239** | — | — |
| Coverage@$K$ | $K=20$ | 0.535 | 0.602 | **0.674** | — | 0.364 | 0.447 | **0.537** | — | 0.184 | 0.245 | **0.317** | — |
| Coverage@$K$ | $K=40$ | 0.614 | 0.669 | 0.726 | **0.787** | 0.389 | 0.474 | 0.562 | **0.653** | 0.197 | 0.255 | 0.324 | **0.403** |

每个数据集分组内，该行的最高数值标为粗体。数字与原 PDF 一致。

图 2 见原 PDF。

**图 2：一名测试用户的示例，其对 Beauty 产品具有多样兴趣，目标物品以红圈标出。**

图中文字转录如下。提示为：“Previously, the customer has bought”（此前，该顾客购买过）：

- Ben Nye Banana Luxury Face Powder 3.0 oz Makeup Kim Kardashian NEW!!!.
- Rosallini Women Stainless Steel Extension Eyelash Applicator Tool Fish Tail Clip.
- Beauty Flawless Makeup Blender Sponge Puff (size 1). Fruit Of The Earth 100% Aloe Vera 24oz Gel Pump.

“In the future, the customer wants to buy”（将来，该顾客想购买）。Fine-tuned GPT-2 生成：

- Ben Nye Luxury Powders - Banana 1.5oz.
- Beautyblender Solid Blendercleanser 1 oz.
- Professional 15 Color Concealer Camouflage Makeup Palette.
- Pro Beauty Makeup Sponge Blender Flawless Smooth Shaped Water Droplets Puff (Random Color).
- L'Oreal Paris True Match Super Blendable Makeup, Natural Buff, 1.0 Ounces.

### 3.3 定性分析

本节通过案例研究，考察生成查询在捕捉用户兴趣方面的有效性，以及它们在解释用户兴趣方面的用处。我们在图 2 与图 3 中给出两名测试用户的序列及模型输出。

在第一个例子中，测试用户对 Beauty 产品的多个类目和品牌都有兴趣。此情形下 GPT4Rec 能够生成多样的查询，不仅覆盖用户历史中的某些产品或品牌，还会生成从未在用户历史中出现、但相关的物品，例如 “makeup palette”（化妆盘）。这表明 GPT4Rec 能够基于用户—物品交互以及物品标题的语义信息，捕捉物品之间的关联。在第二个例子中，测试用户对 Logitech 无线鼠标有非常具体的兴趣。GPT4Rec 捕捉到了这一特征，所有生成查询都集中在同一品牌、同一类目，但产品细节不同。

如上两个案例所示，我们证明了 GPT4Rec 能够生成在不同方面、不同粒度上捕捉用户兴趣的查询。

图 3 见原 PDF。

**图 3：一名测试用户的示例，其对 Electronics 产品具有特定兴趣，目标物品以红圈标出。**

图中文字转录如下。提示为：“Previously, the customer has bought”（此前，该顾客购买过）：

- Logitech Wireless Mouse M325 with Designed-For-Web Scrolling – Blue. Logitech M325c Wireless Optical Mouse Marc Monkey. Logitech Play Collection M325c Mouse - Optical - Wireless – Radio Frequency - Lemon - Usb – 1000 Dpi - Tilt Wheel - 5 Button[s]. Logitech M325c Wrls Mouse Zigzag Red. Logitech Wireless Mouse M325 Dark Silver (910-002816).
- Logitech Wireless Mouse M325 with Designed-For-Web Scrolling - Light Silver.

“In the future, the customer wants to buy”（将来，该顾客想购买）。Fine-tuned GPT-2 生成：

- Logitech - M325c Wireless Optical Mouse – Red Harlequin.
- Logitech - M325c Wireless Optical Mouse – Flamingo.
- Logitech M325 Wireless Mouse with Designed-For-Web.
- Logitech Wireless Mouse m317 with Unifying Receiver Felicity Fox.
- Logitech Party Collection M325c Wireless Optical Mouse, Geo Purple.

这些查询直接服务于解释用户兴趣这一目的。此外，两个例子的对比表明，生成查询的多样性水平会适应用户序列中的多样性水平，从而进一步帮助理解其行为。

## 4 结论

本文提出 GPT4Rec，一种新颖的生成式框架，同时产生个性化推荐和可解释的用户兴趣表示。借助先进的语言模型与物品内容信息，GPT4Rec 取得了更优的性能，并自然地解决了物品冷启动等实际问题。所提出的多查询束搜索技术生成具有不同方面和粒度的用户兴趣表示，从而提升推荐结果的相关性与多样性。我们的框架可以灵活地接入更先进的生成式语言模型或搜索引擎，以及更好的生成与检索策略，这些都是值得未来探索的方向。

<!-- 原 PDF 第 5 页 -->

## 参考文献

[1] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. 2020. 语言模型是少样本学习者。Advances in neural information processing systems 33 (2020), 1877–1901.

[2] Yukuo Cen, Jianwei Zhang, Xu Zou, Chang Zhou, Hongxia Yang, and Jie Tang. 2020. 可控的多兴趣推荐框架。In Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining. 2942–2951.

[3] Minmin Chen, Yuyan Wang, Can Xu, Ya Le, Mohit Sharma, Lee Richardson, Su-Lin Wu, and Ed Chi. 2021. 推荐系统中用户探索的价值。In Fifteenth ACM Conference on Recommender Systems. 85–95.

[4] Paul Covington, Jay Adams, and Emre Sargin. 2016. 用于 YouTube 推荐的深度神经网络。In Proceedings of the 10th ACM conference on recommender systems. 191–198.

[5] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. 2018. BERT：面向语言理解的深度双向 Transformer 预训练。arXiv preprint arXiv:1810.04805 (2018).

[6] Shijie Geng, Shuchang Liu, Zuohui Fu, Yingqiang Ge, and Yongfeng Zhang. 2022. 把推荐当作语言处理（RLP）：统一的预训练、个性化提示与预测范式（P5）。arXiv preprint arXiv:2203.13366 (2022).

[7] Ruining He and Julian McAuley. 2016. 起伏：用单类协同过滤建模时尚趋势的视觉演化。In proceedings of the 25th international conference on world wide web. 507–517.

[8] Ashish Jaiswal, Ashwin Ramesh Babu, Mohammad Zaki Zadeh, Debapriya Banerjee, and Fillia Makedon. 2020. 对比式自监督学习综述。Technologies 9, 1 (2020), 2.

[9] Dietmar Jannach and Malte Ludewig. 2017. 当循环神经网络遇上邻域：会话推荐。In Proceedings of the eleventh ACM conference on recommender systems. 306–310.

[10] Wang-Cheng Kang and Julian McAuley. 2018. 自注意力序列推荐。In 2018 IEEE international conference on data mining (ICDM). IEEE, 197–206.

[11] Maciej Kula. 2015. 面向用户与物品冷启动推荐的元数据嵌入。In Proceedings of the 2nd Workshop on New Trends on Content-Based Recommender Systems co-located with 9th ACM Conference on Recommender Systems (RecSys 2015), Vienna, Austria, September 16-20, 2015. (CEUR Workshop Proceedings, Vol. 1448), Toine Bogers and Marijn Koolen (Eds.). CEUR-WS.org, 14–21. http://ceur-ws.org/Vol-1448/paper4.pdf

[12] Xuan Nhat Lam, Thuc Vu, Trong Duc Le, and Anh Duc Duong. 2008. 应对推荐系统中的冷启动问题。In Proceedings of the 2nd international conference on Ubiquitous information management and communication. 208–211.

[13] Chao Li, Zhiyuan Liu, Mengmeng Wu, Yuchi Xu, Huan Zhao, Pipei Huang, Guoliang Kang, Qiwei Chen, Wei Li, and Dik Lun Lee. 2019. 带动态路由的多兴趣网络：天猫推荐。In Proceedings of the 28th ACM International Conference on Information and Knowledge Management. 2615–2623.

[14] Aditya Pal, Chantat Eksombatchai, Yitong Zhou, Bo Zhao, Charles Rosenberg, and Jure Leskovec. 2020. PinnerSage：Pinterest 推荐的多模态用户嵌入框架。In Proceedings of the 26th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining. 2311–2320.

[15] Gustavo Penha and Claudia Hauff. 2020. BERT 对图书、电影和音乐知道多少？面向对话推荐探测 BERT。In Fourteenth ACM Conference on Recommender Systems. 388–397.

[16] Alec Radford, Karthik Narasimhan, Tim Salimans, Ilya Sutskever, et al. 2018. 通过生成式预训练改进语言理解。(2018).

[17] Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, Ilya Sutskever, et al. 2019. 语言模型是无监督的多任务学习者。OpenAI blog 1, 8 (2019), 9.

[18] Marc’Aurelio Ranzato, Sumit Chopra, Michael Auli, and Wojciech Zaremba. 2015. 用循环神经网络做序列级训练。arXiv preprint arXiv:1511.06732 (2015).

[19] Steffen Rendle. 2010. 因子分解机。In 2010 IEEE International conference on data mining. IEEE, 995–1000.

[20] Stephen Robertson, Hugo Zaragoza, et al. 2009. 概率相关框架：BM25 及其延伸。Foundations and Trends® in Information Retrieval 3, 4 (2009), 333–389.

[21] Andrew I Schein, Alexandrin Popescul, Lyle H Ungar, and David M Pennock. 2002. 冷启动推荐的方法与指标。In Proceedings of the 25th annual international ACM SIGIR conference on Research and development in information retrieval. 253–260.

[22] Damien Sileo, Wout Vossen, and Robbe Raymaekers. 2022. 把零样本推荐当作语言建模。In Advances in Information Retrieval: 44th European Conference on IR Research, ECIR 2022, Stavanger, Norway, April 10–14, 2022, Proceedings, Part II. Springer, 223–230.

[23] Fei Sun, Jun Liu, Jian Wu, Changhua Pei, Xiao Lin, Wenwu Ou, and Peng Jiang. 2019. BERT4Rec：用 Transformer 双向编码器表示做序列推荐。In Proceedings of the 28th ACM international conference on information and knowledge management. 1441–1450.

[24] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. 2017. 注意力就是你所需要的一切。Advances in neural information processing systems 30 (2017).

[25] Ashwin K Vijayakumar, Michael Cogswell, Ramprasath R Selvaraju, Qing Sun, Stefan Lee, David Crandall, and Dhruv Batra. 2016. 多样束搜索：从神经序列模型解码多样解。arXiv preprint arXiv:1610.02424 (2016).

[26] Thomas Wolf, Lysandre Debut, Victor Sanh, Julien Chaumond, Clement Delangue, Anthony Moi, Pierric Cistac, Tim Rault, Rémi Louf, Morgan Funtowicz, et al. 2019. HuggingFace 的 Transformers：最先进的自然语言处理。arXiv preprint arXiv:1910.03771 (2019).

[27] Ledell Wu, Adam Fisch, Sumit Chopra, Keith Adams, Antoine Bordes, and Jason Weston. 2018. StarSpace：把所有东西都嵌入！In Proceedings of the AAAI Conference on Artificial Intelligence, Vol. 32.

[28] Yongfeng Zhang, Xu Chen, et al. 2020. 可解释推荐：综述与新视角。Foundations and Trends® in Information Retrieval 14, 1 (2020), 1–101.

[29] Yuhui Zhang, Hao Ding, Zeren Shui, Yifei Ma, James Zou, Anoop Deoras, and Hao Wang. 2021. 把语言模型当作推荐系统：评估与局限。(2021).

[30] Kun Zhou, Hui Wang, Wayne Xin Zhao, Yutao Zhu, Sirui Wang, Fuzheng Zhang, Zhongyuan Wang, and Ji-Rong Wen. 2020. S3-Rec：用互信息最大化做序列推荐的自监督学习。In Proceedings of the 29th ACM international conference on information & knowledge management. 1893–1902.

<!-- 译完 -->
