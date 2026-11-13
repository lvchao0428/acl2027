- 原文件名：`Wretblad_BIRD-noise_ACL2024-short.pdf`
- 原标题：Understanding the Effects of Noise in Text-to-SQL: An Examination of the BIRD-Bench Benchmark
- 中文标题：理解噪声对 Text-to-SQL 的影响：对 BIRD-Bench 基准的考察
- 作者：Niklas Wretblad、Fredrik Gordh Riseby、Rahul Biswas、Amin Ahmadi、Oskar Holmström
- 会议或 arXiv：Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers), pages 356–369, August 11-16, 2024

<!-- 原 PDF 第 1 页 -->

Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers), pages 356–369。August 11-16, 2024。©2024 Association for Computational Linguistics。

# 理解噪声对 Text-to-SQL 的影响：对 BIRD-Bench 基准的考察

Niklas Wretblad<sup>1,*</sup>　Fredrik Gordh Riseby<sup>1,*</sup>　Rahul Biswas<sup>2</sup>　Amin Ahmadi<sup>2</sup>　Oskar Holmström<sup>1</sup>

<sup>1</sup>Linköping University，<sup>2</sup>Silo AI

niklas.wretblad@liu.se

\*同等贡献（Equal Contribution）

## 摘要

Text-to-SQL 要把自然语言翻译成结构化查询语言（SQL），它使人们无需专家知识即可广泛访问结构化数据库，因而至关重要。然而，为这类任务设计模型颇具挑战，原因很多，其中包括「噪声」的存在，例如含糊的问句和语法错误。本研究深入分析了广泛使用的 BIRD-Bench 基准中噪声的分布与类型，以及噪声对模型的影响。BIRD-Bench 的建立是为了刻画脏且带噪声的数据库取值，但并非为了在问句和金标准 SQL 查询中包含噪声与错误。我们发现，问句和金标准查询中的噪声在该数据集中很普遍，不同领域的数量各不相同，噪声类型之间的分布也不均衡。错误的金标准 SQL 查询会进而生成错误的金标准答案，这对基准的可靠性有显著影响。出人意料的是，在修正后的 SQL 查询上评测模型时，零样本基线超过了当时最先进提示方法的表现。我们的结论是：能提供信息的噪声标签和可靠的基准，对于开发能够处理不同类型噪声的新 Text-to-SQL 方法至关重要。全部数据集、标注和代码可在此网址获取：https://github.com/niklaswretblad/the-effects-of-noise-in-text-to-SQL 。

## 1 引言

用大语言模型做 Text-to-SQL，可以在不要求专家知识的情况下，让更多人访问结构化数据库。要开发这样的模型，高质量的公开数据集和基准是必不可少的资源。多年来已经建立了若干基准和数据集。早期基准，例如 WikiSQL（Zhong et al., 2017），刻画的是简单场景，查询常常只涉及一张表；随后的数据集试图更接近真实场景：跨多张表、带连接语句的复杂查询（Yu et al., 2018），训练时未见过的领域数据集（Gan et al., 2021b; Lee et al., 2021），以及带噪声的问句（Gan et al., 2021a）。BIRD-Bench 是一个较新且有难度的基准，旨在进一步缩小 Text-to-SQL 研究与真实应用之间的差距，例如包含又大又脏的数据库取值，并要求使用外部知识（Li et al., 2023）。

**图 1**（排在右栏顶部）：一条错误的 SQL 查询示例。该查询为给定问题生成了错误的金标准参考答案。JOIN 操作按 `district_id` 错误地匹配客户与账户。由于同一地区可能有多名客户和多个账户，账户被错误地关联到了错误的用户。

- 问句（Question）：What is the average loan amount by male borrowers?
- 中文：男性借款人的平均贷款额是多少？

错误的金标准查询（Incorrect Gold Query）：

```sql
SELECT AVG(T3.amount) FROM client AS T1
INNER JOIN account AS T2 ON T1.district_id = T2.district_id
INNER JOIN loan AS T3 ON T2.account_id = T3.account_id
WHERE T1.gender = 'M'
```

修正后的查询（Corrected Query）：

```sql
SELECT AVG(T1.amount) FROM loan AS T1
INNER JOIN account AS T2 ON T1.account_id = T2.account_id
INNER JOIN disp AS T3 ON T2.account_id = T3.account_id
INNER JOIN client AS T4 ON T3.client_id = T4.client_id
WHERE T4.gender = 'M'
```

虽然 BIRD-Bench 并没有明确往数据中的问句引入噪声，但在数据集构建过程中，人为失误仍可能无意中把噪声加进去。出于同样的原因，噪声也是真实使用中的一个基本方面，因为人的输入常常含糊，并且含有语法错误。然而，基准若要成为判断模型性质（例如噪声处理能力）的有用工具，数据必须有效，并且能告诉我们模型可以在哪些方面改进。

本文延续考察公开数据集与基准之适用性及其限度的传统。我们特别关注噪声如何体现在 BIRD-

<!-- 原 PDF 第 2 页 -->

**图 2**：BIRD-Bench 开发集不同领域上的问题难度分布，以及 DIN-SQL 模型的执行准确率。

图中数值抽取不完整，见原 PDF 第 2 页。该图为嵌入图像，文本层未抽出各领域名称、难度占比和准确率曲线的具体数值。

Bench 的问句和查询中。我们对数据中存在哪些类型的噪声，以及特定领域中的噪声分布，做定性分析。然后，我们研究噪声对不同模型和提示技术的影响，比较时同时使用较强的基线和当时的先进方法。

我们发现，问句和金标准 SQL 查询中的噪声很普遍；噪声在不同领域之间分布不均；各类噪声在数据中的占比也不均衡。金标准 SQL 查询中的错误同样常见，并降低了 BIRD-Bench 的可靠性。在一份金标准查询已经修正的数据集上评测模型时，零样本基线与当时先进提示技术之间的性能差距被抹平，这使人质疑应当如何解读模型在 BIRD-Bench 上的表现。

## 2 相关工作

### 数据集

WikiSQL 是一个大型 Text-to-SQL 数据集，只包含简单的 SELECT 和 WHERE 操作，没有嵌套查询，也没有 JOIN 操作（Zhong et al., 2017）。后来开发的 SPIDER（Yu et al., 2018）更接近真实场景，要求模型构造复杂查询并理解数据库模式。复杂度固然是真实使用中的关键方面，但人们也建立了 SPIDER 的变体，用以包含带噪声的问句（Gan et al., 2021a）和特定领域的问句（Gan et al., 2021b）。BIRD-Bench 的建立是为了缩小学术研究与真实应用之间的差距，做法是引入又大又脏的数据库取值、需要外部知识的问题，并优化 SQL 的执行效率（Li et al., 2023）。

### Text-to-SQL 方法

自动化系统（65.45%）与人类专家（92.96%）之间显著的准确率差距<sup>1</sup>，表明 Text-to-SQL 模型仍需持续发展。

人们采取了不同途径来建立能够做 Text-to-SQL 生成的模型。较传统的做法是在 Text-to-SQL 样本上微调大语言模型。这些模型已经给出有希望的结果，但与通过提示工程适配到 Text-to-SQL 任务的指令微调大语言模型之间仍有性能差距，其中尤其是 GPT-4（Li et al., 2023）。提示常常串成一条链，每一步处理任务的一个子问题，例如模式链接、查询分解，以及对模型已生成内容的修正（Pourreza and Rafiei, 2023a; Wang et al., 2023）。

### 数据集中的噪声

几乎同时发表的 Wang et al. (2023) 与 Sun et al. (2024) 表明，BIRD-Bench 中存在含糊问句和错误的 SQL 查询。然而，与本文不同，他们没有研究噪声如何随领域变化，也没有研究这些被识别出的噪声和错误如何影响

<sup>1</sup> 截至 2024-02-16 的 BIRD-Bench 基准（https://bird-bench.github.io）。

<!-- 原 PDF 第 3 页 -->

**表 1**：五个领域中，含有错误的问句与 SQL 查询对的总数，以及问句和金标准 SQL 查询各自的错误数量。

| 统计项 | Financial | California Schools | Superhero | Toxicology | Thrombosis Prediction |
| --- | --- | --- | --- | --- | --- |
| 含噪声的问句与 SQL 查询对 | 52/106 (49%) | 9/20 (45%) | 3/20 (15%) | 7/20 (35%) | 8/20 (40%) |
| 带噪声的问句 | 44/106 (41.5%) | 5/20 (25%) | 2/20 (10%) | 6/20 (30%) | 3/20 (15%) |
| 错误的金标准查询 | 22/106 (20.7%) | 8/20 (40%) | 1/20 (5%) | 2/20 (10%) | 6/20 (30%) |

**表 2**：各领域中遇到的不同类型噪声的分布。

| 噪声类型 | Financial | California Schools | Superhero | Toxicology | Thrombosis Prediction |
| --- | --- | --- | --- | --- | --- |
| 拼写/语法错误（Spelling/Syntactical Errors） | 23 | 2 | 1 | 4 | 2 |
| 含糊/歧义问句（Vague/Ambiguous Questions） | 17 | 1 | 1 | 1 | 1 |
| 错误的 SQL 查询（Incorrect SQL query） | 22 | 8 | 1 | 2 | 6 |
| 同义词（Synonyms） | 2 | 0 | 0 | 0 | 0 |
| 字符串大小写（String Capitalization） | 7 | 0 | 0 | 0 | 0 |
| 问句无法映射到数据库（Question does not map to DB） | 1 | 4 | 1 | 0 | 0 |
| 错误总数 | 72 | 15 | 4 | 7 | 9 |

模型表现。Pourreza and Rafiei (2023b) 对错误的 SQL 查询做了更细粒度的分析，同时也提到了本文所覆盖的几类噪声（例如，自然语言问句与数据库模式不匹配）。与他们的工作不同，我们对自然语言问句中的噪声做了更细粒度的分析，例如语法错误、同义词和含糊问句各自的影响。

Katsogiannis-Meimarakis and Koutrika (2023) 指出，数据库模式经常与数据实体错位，这可能造成词汇歧义或句法歧义，从而影响 Text-to-SQL 模型。

## 3 方法

### 3.1 数据

本文研究 BIRD-Bench 数据集（Li et al., 2023），因为它是较新且被广泛使用的数据集，在当前基准中最接近真实世界场景。BIRD 包含跨很多领域的 12,751 个样本。由于本文的人工标注很耗时，分析的主要重点放在金融领域<sup>2</sup>，其中包括与银行业务相关的查询。

金融领域的开发集包含 106 对问句与 SQL 查询，约占开发集数据点的 7.5%，并围绕八张不同的表来组织，这些表完整列于附录 A.1。每个问句都标有难度等级（simple、moderate 和 challenging）。具体分布见图 2。

我们另外选择了四个领域，以验证对金融领域的噪声分析，并对每个领域随机抽取的 20 个问句做了同样的分析。领域选择依据问题难度以及 DIN-SQL 的模型准确率<sup>3</sup>，如图 2 所示。我们选择了准确率低、问句简单的 California Schools，准确率高、问句简单的 Superhero，准确率与金融领域相近但问句更复杂的 Toxicology，以及准确率低、问句难度中等的 Thrombosis Prediction。

### 3.2 噪声标注

所选领域中的全部问句和 SQL 查询都经过标注，以判断它们是否含有错误。标注由本文的两位作者独立完成，两人都精通英语，并且是 SQL 专家。在第一阶段，标注者独立标出含有错误的问句和 SQL 查询。Cohen's Kappa 系数为 0.73，表明标注者之间具有实质性的一致。随后，标注者独立为错误类型命名。在第二阶段，标注者通过查看对方的理由来解决分歧，其余分歧则

<sup>2</sup> 把分析重点放在金融领域，也是因为本文是与瑞典银行 SEB 合作进行的。

<sup>3</sup> 各领域上 DIN-SQL 的结果由 DIN-SQL 的创建者提供。

<!-- 原 PDF 第 4 页 -->

**图 3**：若干模型在 BIRD-Bench 金融领域上的准确率。模型分别在原始数据（左）、修正后的 SQL 查询（中），以及修正后的 SQL 查询和修正后的带噪声问句上评测。

图中柱状数值抽取不完整，见原 PDF 第 4 页。该图为嵌入图像。三个面板的标题分别为 Original Data、Corrected SQL 和 Corrected Data；横轴模型为 Zero-Shot (GPT-3.5)、Zero-Shot (GPT-4)、DIN-SQL (GPT-3.5)、MAC-SQL (GPT-3.5)；纵轴为 Accuracy (%)。柱顶标注的具体百分数未能从文本层可靠抽出。

通过讨论解决。识别出的错误按相似性分组，并按其共同性质命名，如表 2 所示。这些标注随后被用来生成两个不同的数据集：一个修正了 SQL，另一个同时修正了 SQL 查询和带噪声的问句。

### 3.3 模型与提示技术

使用了两个模型，GPT-3.5 和 GPT-4，以及三种不同的提示方法：作为基线的零样本提示，以及更进一步的 DIN-SQL（Pourreza and Rafiei, 2023a）和 MAC-SQL（Wang et al., 2023）。零样本提示使用了 GPT-3.5 和 GPT-4；对于更进一步的提示技术，我们只用了 GPT-3.5，因为用 GPT-4 做链式提示超出了本项目的资源。我们选择这些模型和提示方法，是因为在撰写本文时，它们是 BIRD-Bench 上公开可得、表现最高的模型。

数据库模式信息对于为 BIRD-Bench 的问题生成正确查询至关重要。DIN-SQL 和 MAC-SQL 有预定义的格式来加入数据库模式。对于零样本模型，我们以上下文中的 SQL 建表语句形式提供数据库模式，因为已有工作表明，与其他格式相比，这种形式能提高准确率（Nan et al., 2023）。零样本模型的提示模板见附录 A.2。代码库在匿名期结束后发布。

## 4 噪声的定性分析

尽管 BIRD-Bench 并非有意要在问句和 SQL 查询中放入噪声，我们的分析表明，所有被研究的领域都在不同程度上存在噪声。金融领域的噪声水平最高，为 49%，California Schools 领域紧随其后，为 45%，见表 1。相比之下，Superhero 领域的噪声水平最低，只有 15% 的数据点含有错误。如第 3.1 节和图 2 所示，Superhero 领域在问题难度分布相近的同时，准确率最高。这可能表明，各任务上的模型准确率与噪声相关，因而在设计数据集时需要仔细考虑问句和 SQL 查询中的噪声。

每个数据集上噪声的类别及其绝对频次见表 2；各类噪声的例子和说明见附录 A.3。我们的分析表明，在金融领域，拼写/语法错误和错误的 SQL 查询最为普遍。问句中存在噪声不一定不可取，因为它更接近真实场景。然而，各类别上的噪声分布并不均衡。这或许可以近似真实世界的分布，但也可能不公平地使基准偏向更擅长处理语法错误的模型。由于错误分布不均，并且缺少噪声标签，该基准并不能告诉我们哪些噪声类型对当前模型构成挑战，以及它们应当在哪些方面改进。

一个更严重的问题是，所有领域都含有错误的 SQL 查询，而这些查询被用来生成金标准参考答案。错误 SQL 查询的一个例子见图 1。这类错误使人质疑该基准能否准确地判定模型表现。下一节将探讨这一点。

<!-- 原 PDF 第 5 页 -->

**表 3**：各模型在金融领域上、按不同错误类别的表现，以及对无错误问句的总体正确预测。

| 错误类别 | 合计 | DIN-SQL (3.5) | Zero-shot (3.5) | Zero-shot (4) | MAC-SQL (3.5) |
| --- | --- | --- | --- | --- | --- |
| 拼写/语法错误（Spelling/Syntactical Errors） | 23 | 2 | 6 | 4 | 6 |
| 含糊/歧义问句（Vague/Ambiguous Questions） | 17 | 1 | 2 | 3 | 4 |
| 错误的 SQL（Incorrect SQL） | 22 | 0 | 2 | 2 | 4 |
| 同义词（Synonyms） | 2 | 0 | 0 | 0 | 0 |
| 字符串大小写（String Capitalization） | 7 | 2 | 1 | 1 | 0 |
| 问句无法映射到数据库（Question does not map to DB） | 1 | 0 | 0 | 0 | 0 |

## 5 噪声对模型表现的影响

我们把模型应用到原始数据集、SQL 已经修正的数据集，以及 SQL 查询和带噪声问句都已经修正的数据集上。图 3 给出所有模型在全部这些数据集上的一次评测结果。

在问句和查询都含有噪声的原始数据集上，MAC-SQL 略优于 DIN-SQL 和零样本基线。然而，修正 SQL 查询之后，MAC-SQL 的表现下降，与 DIN-SQL 并列，成为表现最差的方法。出人意料的是，就连零样本 GPT-3.5 基线也超过了更进一步的 DIN-SQL 和 MAC-SQL。SQL 查询已经修正的数据集也可以看作是最优的：金标准标签是正确的，同时问句中的噪声仍然得到体现。鉴于模型名次发生了剧烈重排，有必要追问 BIRD-Bench 是否是可靠的模型评判者，以及它是否是帮助研究者开发新的 Text-to-SQL 方法的有用工具。

在问句和 SQL 查询都已经修正的数据集上评测时，所有模型的准确率都显著提高。零样本 GPT-4 表现最好，其余模型表现相近，其中 DIN-SQL 略为领先。与只修正 SQL 查询的理想情形相比，噪声的存在明显影响了所有模型的准确率。不过，各模型受噪声的影响并不相同，有些模型的准确率上升更为明显。表 3 给出每个模型在各错误类别上的表现。在与拼写和语法错误、含糊问句以及错误 SQL 相关的错误上，MAC-SQL 略优于其他模型。MAC-SQL 与其他方法的主要差别，在于对表和列做了大量过滤，并且增加了上下文中的相关信息，这可能使模型对噪声更稳健。然而，这一假说必须通过考察模型在生成阶段实际看到了什么来加以确认或否定，我们把这一点留给今后的研究。

## 6 结论与未来工作

本文分析了 Text-to-SQL 所用 BIRD-Bench 基准中噪声的质量与分布。我们表明，问句和 SQL 查询中的噪声都很普遍，并且噪声在噪声类型之间、也在领域之间分布不均。金标准 SQL 查询中的错误很常见，降低了 BIRD-Bench 的可靠性。出人意料的是，在修正后的金标准查询上评测模型时，零样本基线超过了更进一步的提示技术。这些发现说明，有必要开发能够引导研究者去设计更抗噪声的模型的基准。因此，一项重要改进是在整个数据集上为噪声类型打上标签。在未来工作中，我们计划研究如何把大语言模型用于噪声分类。这是一项新任务，在实际采用 Text-to-SQL 的系统中也可能很关键。

总体而言，本研究使人们更深入地理解噪声在 Text-to-SQL 任务中如何体现，以及噪声与模型如何相互作用，并指出 BIRD-Bench 数据集中可以改进的地方。

## 局限

虽然本研究就数据集噪声对 Text-to-SQL 翻译任务的影响提供了有价值的认识，它仍有若干局限。由于分析主要在 BIRD-Bench 数据集的金融领域上进行，这些发现的可推广性可能有限。我们只检查了其他领域的一个小子集，以验证我们的发现，而这也许只能代表跨领域噪声分布中的一部分。

此外，标注者在为噪声做标注时可能带入主观偏差，即使

<!-- 原 PDF 第 6 页 -->

我们试图通过两位独立标注者来尽量减小这种偏差。再者，我们把噪声分成六个具体类别，这一决定可能过分简化了这些基准中噪声类型的复杂性与多样性。

我们对模型和提示技术的选择也可能构成潜在局限。我们只用了 GPT-3.5 和 GPT-4 两个模型，以及三种不同的提示方法。若评测范围更广的模型和提示技术，也许能更全面地理解它们在噪声影响下的表现。

最后，修正数据集中的 SQL 查询和带噪声问句需要投入大量工作；尽管经过复查，仍可能引入错误。这可能会影响我们在修正后的数据集上评测模型时所报告的模型表现。

## 致谢

我们感谢 Mohammadreza Pourreza 提供 DIN-SQL 模型的结果。我们也感谢 SEBx 的慷慨支持以及所提供的资源。此外，本研究部分由瑞典国家计算机科学研究生院（National Graduate School of Computer Science in Sweden, CUGS）资助。

## 参考文献

Yujian Gan, Xinyun Chen, Qiuping Huang, Matthew Purver, John R. Woodward, Jinxia Xie, and Pengsheng Huang. 2021a. 迈向能抵御同义词替换的 Text-to-SQL 模型稳健性。In Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers), pages 2505–2515, Online. Association for Computational Linguistics.

Yujian Gan, Xinyun Chen, and Matthew Purver. 2021b. 探索跨领域 Text-to-SQL 泛化中研究不足的局限。In Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, pages 8926–8931, Online and Punta Cana, Dominican Republic. Association for Computational Linguistics.

George Katsogiannis-Meimarakis and Georgia Koutrika. 2023. 面向 Text-to-SQL 的深度学习方法综述。The VLDB Journal, 32(4):905–936.

Chia-Hsuan Lee, Oleksandr Polozov, and Matthew Richardson. 2021. KaggleDBQA：对 Text-to-SQL 解析器的现实评测。In Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers), pages 2261–2273, Online. Association for Computational Linguistics.

Jinyang Li, Binyuan Hui, Ge Qu, Binhua Li, Jiaxi Yang, Bowen Li, Bailin Wang, Bowen Qin, Rongyu Cao, Ruiying Geng, Nan Huo, Xuanhe Zhou, Chenhao Ma, Guoliang Li, Kevin C. C. Chang, Fei Huang, Reynold Cheng, and Yongbin Li. 2023. 大语言模型是否已经能够充当数据库接口？一个面向大规模、基于数据库的 Text-to-SQL 大型基准。In Advances in Neural Information Processing Systems. Spotlight Poster.

Linyong Nan, Yilun Zhao, Weijin Zou, Narutatsu Ri, Jaesung Tae, Ellen Zhang, Arman Cohan, and Dragomir Radev. 2023. 增强大语言模型的 Text-to-SQL 能力：一项关于提示设计策略的研究。In Findings of the Association for Computational Linguistics: EMNLP 2023, pages 14935–14956, Singapore. Association for Computational Linguistics.

Mohammadreza Pourreza and Davood Rafiei. 2023a. DIN-SQL：带自我修正的 Text-to-SQL 分解式上下文学习。In Advances in Neural Information Processing Systems 36. Accepted for poster presentation, full citation details to be updated.

Mohammadreza Pourreza and Davood Rafiei. 2023b. 评测跨领域 Text-to-SQL 模型与基准。In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pages 1601–1611, Singapore. Association for Computational Linguistics.

<!-- 原 PDF 第 7 页 -->

Ruoxi Sun, Sercan Ö. Arik, Alex Muzio, Lesly Miculicich, Satya Gundabathula, Pengcheng Yin, Hanjun Dai, Hootan Nakhost, Rajarishi Sinha, Zifeng Wang, and Tomas Pfister. 2024. SQL-PaLM：面向 Text-to-SQL 的改进型大语言模型适配（扩展版）。http://arxiv.org/abs/2306.00739

Bing Wang, Changyu Ren, Jian Yang, Xinnian Liang, Jiaqi Bai, Qian-Wen Zhang, Zhao Yan, and Zhoujun Li. 2023. MAC-SQL：面向 Text-to-SQL 的多智能体协作框架。http://arxiv.org/abs/2312.11242

Tao Yu, Rui Zhang, Kai Yang, Michihiro Yasunaga, Dongxu Wang, Zifan Li, James Ma, Irene Li, Qingning Yao, Shanelle Roman, Zilin Zhang, and Dragomir Radev. 2018. Spider：面向复杂且跨领域的语义解析与 Text-to-SQL 任务的大规模人工标注数据集。In Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing, pages 3911–3921, Brussels, Belgium. Association for Computational Linguistics.

Victor Zhong, Caiming Xiong, and Richard Socher. 2017. Seq2SQL：利用强化学习从自然语言生成结构化查询。arXiv e-prints, page arXiv:1709.00103.

<!-- 原 PDF 第 8 页 -->

## 附录 A

### A.1 金融领域的数据库模式

**图 4**：BIRD-Bench 金融领域中该数据库的数据库模式。

模式图为嵌入图像，列名与类型抽取不完整，见原 PDF 第 8 页。

图 4 展示金融领域的数据库模式。该模式包含多张表，例如与贷款、交易、账户、银行卡和客户有关的表，这些都反映出数据库的金融取向。这些表所含信息的说明见表 4。数据库由分布在八张不同表中的 55 个列组成。大多数列名可以凭直觉理解，但正如模式图所示，有些列在解释上存在困难。一个说明性的例子是 district 表，它纳入了 16 个互不相同的列。其中包括名为 district_ID 的一列，以及另外 15 列，从 A2 到 A16。后一类列的名称并不能直接表明它们所保存数据的性质，因此较难凭直觉理解。在实践中，数据库模式往往附有数据字典或文档，详细解释每一张表和每一列。这类文档通常会提供充分理解模式中每个元素之含义、类型未指明之字段的可能取值范围，以及关系背后的业务逻辑所需要的语境。若没有这些额外文档，就无法充分

<!-- 原 PDF 第 9 页 -->

解释并有效使用该数据库，districts 表中的列名正说明了这一点。BIRD-Bench 数据集为每个问题包含一项称为 hint 的独特特征。该特征旨在提供与此类数据库文档中具体细节相对应的见解或补充信息。在实验中，第 3.3 节所描述的全部模型在回答每个问题时都得到了这一特征。

**表 4**：BIRD-Bench 金融领域数据库中各表的说明。

| 表名（Table Name） | 说明（Description） |
| --- | --- |
| loan | 包含贷款的详细信息。 |
| order | 保存货币订单的信息。 |
| trans | 表示金融交易。 |
| account | 包含账户信息。 |
| disp | 把客户关联到账户（dispositions）。 |
| card | 包含已发行银行卡的详细信息。 |
| client | 保存客户信息。 |
| district | 包含地区或区域的详细信息。 |

此外，图 4 中表与表之间的连线表示关系，关系的性质由连线接到每张表的那一端的形状来表示。一对多关系的表示是：连线的一端以单线开始，上方标有数字 1，另一端则以鸦爪形（三条线）结束。例如，一个账户可以关联多笔订单、多笔交易、多条 disposition 和多笔贷款，但这些实体中的每一个都只关联到一个账户。一个账户可以有多笔贷款，但一笔贷款只排他地关联到一个账户，这是说得通的。再者，客户与账户通过 disposition 表构成多对多关系。一个账户可以关联许多不同的客户，例如一名客户被列为账户所有者，另有多名客户被列为该账户的使用者。这在家庭共用账户时会很实用：其中一位家长可以是账户所有者，其他多名家庭成员则被列为使用者。反过来，单个客户也可以关联到许多不同的账户。

### A.2 提示模板

**代码清单 1**：零样本提示模板（Zero-Shot Prompting Template）。原文如下：

```text
"""Database schema in the form of CREATE_TABLE statements:

{database_schema}

Using valid SQL, answer the following question based on the
tables provided above.

Hint helps you to write the correct sqlite SQL query.
Question: {question}
Hint: {evidence}
DO NOT return anything else except the SQL query."""
```

中文：

```text
"""以 CREATE_TABLE 语句形式给出的数据库模式：

{database_schema}

请使用合法的 SQL，根据上面提供的表回答下列问题。

Hint 帮助你写出正确的 sqlite SQL 查询。
问题：{question}
Hint：{evidence}
除 SQL 查询外，不要返回任何其他内容。"""
```

第 3.3 节所述零样本模型所依据的提示模板见代码清单 1。该提示把给定问题、相应的数据库模式、指示大语言模型生成合法 SQL 的指令，以及 BIRD-Bench 数据集提供的 hint 整合在一起。该 hint 旨在提供

<!-- 原 PDF 第 10 页 -->

为准确解释数据库模式、并把问题正确转换成 SQL 查询所需要的见解或补充信息。需要说明的是，本研究中实现的其他模型也同样获得了这一特征。

<!-- 原 PDF 第 11 页 -->

### A.3 错误与修正的例子

本节给出表 1 所列不同错误类别中、错误数据点及其修正的例子。

**例 1：拼写/语法错误（Spelling/Syntactical Error）**

图 5 给出一个含有语法错误的问句例子，对应 BIRD-Bench 开发集金融领域中 ID 为 125 的问题。该问句的语法结构使人类读者难以解释其含义，也难以弄清它在询问哪一项信息。因此，大语言模型也有可能误解这个问题。修正后的问句见图。

带噪声的原问句（Original Question With Noise）：

> For loans contracts which are still running where client are in debt, list the district of the and the state the percentage unemployment rate increment from year 1995 to 1996.

中文（按原文的语病直译）：对于那些仍在执行的贷款合同，其中客户处于负债状态，列出「the」的地区，并陈述从 1995 年到 1996 年失业率增量的百分比。

修正后的问句（Corrected Question）：

> For loan contracts that are still active and where clients are in debt, state the percentage increase in unemployment rate from 1995 to 1996.

中文：对于仍在有效期内、且客户处于负债状态的贷款合同，陈述从 1995 年到 1996 年失业率上升的百分比。

**图 5**：BIRD-Bench 开发集中 ID 为 125 的问句，其中含有语法错误，以及该问句的一个修正版本。

**例 2：含糊/歧义问句（Ambiguous/Vague Question）**

图 6 展示 BIRD-Bench 开发集金融领域中 ID 为 159 的数据点。它含有一处被归入含糊/歧义问句类别的错误。难点在于自然语言问句的歧义，具体是短语 “List all the withdrawals...”（「列出全部取款……」）。这一歧义围绕着执行 SQL 查询时应当返回哪些列。

含歧义的问句（Question With Ambiguity）：

> List all the withdrawals in cash transactions that the client with the id 3356 makes.

中文：列出 ID 为 3356 的客户所做的全部现金交易取款。

金标准查询（Gold Query）：

```sql
SELECT T4.trans_id
FROM client AS T1
INNER JOIN disp AS T2 ON T1.client_id = T2.client_id
INNER JOIN account AS T3 ON T2.account_id = T3.account_id
INNER JOIN trans AS T4 ON T3.account_id = T4.account_id
WHERE T1.client_id = 3356 AND T4.operation = 'VYBER'
```

修正后的问句（Corrected Question）：

> List the transaction ID of all withdrawals in cash transactions that the client with the id 3356 makes.

中文：列出 ID 为 3356 的客户所做的全部现金交易取款的交易 ID。

**图 6**：与 BIRD-Bench 开发集中 ID 为 159 的数据点相对应的问句、金标准 SQL 查询以及问句的修正版本，展示含糊/歧义类别中的一处错误。

<!-- 原 PDF 第 12 页 -->

**例 3：错误的金标准 SQL（Incorrect Gold SQL）**

图 7 展示 BIRD-Bench 开发集金融领域中 ID 为 132 的数据点里一条错误的金标准 SQL 查询。JOIN 操作按 `district_id` 错误地匹配客户与账户。由于同一地区可能有多名客户和多个账户，账户被错误地关联到了错误的用户。

问句（Question）：

> What is the average loan amount by male borrowers?

中文：男性借款人的平均贷款额是多少？

错误的金标准查询（Incorrect Gold Query）：

```sql
SELECT AVG(T3.amount) FROM client AS T1
INNER JOIN account AS T2 ON T1.district_id = T2.district_id
INNER JOIN loan AS T3 ON T2.account_id = T3.account_id
WHERE T1.gender = 'M'
```

修正后的查询（Corrected Query）：

```sql
SELECT AVG(T1.amount) FROM loan AS T1
INNER JOIN account AS T2 ON T1.account_id = T2.account_id
INNER JOIN disp AS T3 ON T2.account_id = T3.account_id
INNER JOIN client AS T4 ON T3.client_id = T4.client_id
WHERE T4.gender = 'M'
```

**图 7**：一条错误的 SQL 查询示例。该查询为给定问题生成了错误的金标准参考答案。JOIN 操作按 `district_id` 错误地匹配客户与账户。由于同一地区可能有多名客户和多个账户，账户被错误地关联到了错误的用户。

<!-- 原 PDF 第 13 页 -->

**例 4：同义词（Synonyms）**

图 8 说明，特定措辞会如何使大语言模型更难解释。sum 既是 SQL 关键字，又是一个描述用语，这导致大语言模型按字面理解，并对一笔交易做了错误的求和。实际意图是询问该交易的余额或金额。把问句换一种说法之后，大语言模型生成了正确的 SQL 查询，取出了所要的信息，如图所示。

含 SQL 关键字/同义词的原问句（Original Question With SQL Keyword/Synonym）：

> What is the sum that client number 4's account has following transaction 851? Who owns this account, a man or a woman?

中文：客户编号 4 的账户在交易 851 之后的 sum 是多少？这个账户的所有者是男性还是女性？

预测查询（不正确）（Predicted Query (Incorrect)）：

```sql
SELECT
  SUM(trans.amount)
  client.gender
FROM trans
JOIN account ON trans.account_id = account.account_id
JOIN disp ON account.account_id = disp.account_id
JOIN client ON disp.client_id = client.client_id
WHERE trans.trans_id = 851 AND client.client_id = 4;
```

修正后的问句（Corrected Question）：

> What is the balance of client number 4's account following transaction 851? Who owns this account, a man or a woman?

中文：客户编号 4 的账户在交易 851 之后的余额是多少？这个账户的所有者是男性还是女性？

预测查询（正确）（Predicted Query (Correct)）：

```sql
SELECT
  trans.balance
  client.gender
FROM
  trans
  JOIN disp ON trans.account_id = disp.account_id
  JOIN client ON disp.client_id = client.client_id
WHERE trans.trans_id = 851 AND client.client_id = 4;
```

**图 8**：BIRD-Bench 开发集中 ID 为 177 的数据点里的问句。该问句含有一个难处理的同义词；图中还有把同义词替换之后的修正问句，以及第 3.3 节所述 DIN-SQL（GPT-3.5）模型对应的预测 SQL 查询。此图展示同义词给模型预测带来的困难。

<!-- 原 PDF 第 14 页 -->

**例 5：字符串大小写（String Capitalization）**

由于 SQL 在查询中比较字符串值时区分大小写，问句在索取某个具体取值时使用大写还是小写，会影响结果。这是因为，除非大语言模型知道数据库中不同条目所使用的大小写，否则它在生成查询时很可能会原样使用问句里给出的那个写法。因此，图 9 给出一个例子：其中 “East” 和 “North” 按常见写法以大写字母开头。然而，这些列值在数据库中的条目是小写的，所以问句必须把这一点考虑进去，大语言模型才有可能生成正确的查询。修正后的问句以及由它生成的 SQL 查询也见图 9。

含脏取值的原问句（Original Question With Dirty Values）：

> What was the difference in the number of crimes committed in East and North Bohemia in 1996?

中文：1996 年，East Bohemia 与 North Bohemia 的犯罪数量之差是多少？

金标准查询（Gold Query）：

```sql
SELECT
SUM(IIF(A3 = 'East Bohemia', A16, 0)) - SUM(IIF(A3 = 'North Bohemia', A16, 0))
FROM district
```

修正后的问句（Corrected Question）：

> What was the difference in the number of crimes committed in east and north Bohemia in 1996?

中文：1996 年，east Bohemia 与 north Bohemia 的犯罪数量之差是多少？

修正后的查询（Corrected Query）：

```sql
SELECT
SUM(IIF(A3 = 'east Bohemia', A16, 0)) - SUM(IIF(A3 = 'north Bohemia', A16, 0))
FROM district
```

**图 9**：含糊示例（Example Ambiguous）。

**例 6：与数据库模式不对齐（Database Schema Non-Alignment）**

**表 5**：无法映射到数据库模式的问句示例，以及它们为何无法映射的说明。

| 错误问句（Incorrect Question） | 说明（Description） |
| --- | --- |
| What is the disposition ID of the client who made $5100 USD transaction on 1998/9/2? 中文：在 1998/9/2 做了一笔 5100 美元交易的那位客户，其 disposition ID 是什么？ | 该问句要求返回单一的 disposition ID，但这并没有反映出客户与 disposition 之间存在一对多关系，而且很可能无法返回单一的 ID。 |
| List out the account numbers of clients who are youngest and have highest average salary? 中文：列出那些最年轻、且平均薪资最高的客户的账号。 | 数据库中没有关于特定客户薪资的信息。 |

<!-- 译完 -->
