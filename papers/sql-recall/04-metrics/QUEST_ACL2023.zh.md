# QUEST_ACL2023.pdf

- 原文件名：QUEST_ACL2023.pdf
- 原标题：QUEST: A Retrieval Dataset of Entity-Seeking Queries with Implicit Set Operations
- 中文标题：QUEST：带有隐式集合运算的实体寻求型查询检索数据集
- 作者：Chaitanya Malaviya、Peter Shaw、Ming-Wei Chang、Kenton Lee、Kristina Toutanova
- 会议：Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics（ACL 2023），Volume 1: Long Papers，pages 14032–14047，July 9-14, 2023

<!-- 原 PDF 第 1 页 -->

Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics
Volume 1: Long Papers, pages 14032–14047
July 9-14, 2023 ©2023 Association for Computational Linguistics

**QUEST：带有隐式集合运算的实体寻求型查询检索数据集**

Chaitanya Malaviya$^{1*}$、Peter Shaw$^{2}$、Ming-Wei Chang$^{2}$、Kenton Lee$^{2}$、Kristina Toutanova$^{2}$

$^{1}$University of Pennsylvania　$^{2}$Google DeepMind

cmalaviy@seas.upenn.edu

{petershaw, mingweichang, kentonl, kristout}@google.com

**摘要**

把有选择性的信息需求表述出来，会得到隐式指定集合运算的查询，例如交集、并集与差集。例如，人们可能会搜索「不是矶鹬的滨鸟」，或「在英格兰拍摄的科幻电影」。为研究检索系统满足此类信息需求的能力，我们构建了 QUEST，其中包含 3357 条带有隐式集合运算的自然语言查询，每条查询映射到一组与 Wikipedia 文档相对应的实体。该数据集要求模型把查询中提到的多项约束与文档中的相应证据匹配起来，并正确执行各种集合运算。数据集以半自动方式、利用 Wikipedia 类别名称构建。查询先由单个类别自动组合而成，再由众包人员改写，并进一步校验其自然性与流畅性。众包人员还根据实体文档评估实体的相关性，并标出查询约束在文档文本片段上的归因。我们分析了若干现代检索系统，发现它们在这类查询上常常表现吃力。涉及否定与合取的查询尤其困难，而这些运算的组合会进一步增加系统的难度。$^{1}$

$^{*}$ 工作完成于在 Google 实习期间。

$^{1}$ 数据集见 https://github.com/google-research/language/tree/master/language/quest 。

**1 引言**

人们表达信息需求时，常常带有多项偏好或约束。与这类需求对应的查询，通常会隐式表达交集、差集和并集等集合运算。例如，一位观影者可能在寻找一部 90 年代的科幻电影，而且其中不出现外星人；一位读者可能对以法国为背景的历史小说感兴趣。同样，一位植物学家若想根据记忆鉴定某个物种，可能会搜索常绿、且分布于巴拿马的灌木。此外，若满足这些约束的实体集合相对较小，读者可能希望看到并浏览一份穷尽的实体列表。另外，为了核验并信任系统的推荐，用户也能从展示来自可信来源的证据中受益（Lamm et al., 2021）。

应对这类查询的研究，主要是在基于结构化知识库（KB）的问答这一背景下进行的：查询约束被落到预定义谓词上，再以符号方式执行。然而，知识库可能不完整，而且整理与维护成本高昂。与此同时，信息检索的进展或许能促成这样的系统：不依赖结构化知识库，而是通过

**图 1：QUEST 的数据集构建流程。** 首先，（1）我们抽样 Wikipedia 类别名称，并找出其对应的相关实体集合。（2）然后，我们用集合运算组合出一条查询，并由众包人员改写该查询。（3）这些查询随后接受流畅性与自然性校验。（4）最后，众包人员通过在实体文档中高亮可归因片段，来标注实体的相关性。

图中可见文字：

- （1）Birds of Venezuelan Andes — Birds of Colombia（委内瑞拉安第斯山脉的鸟类 — 哥伦比亚的鸟类）
- （2）Paraphrasing（改写）：Birds found in the Venezuelan Andes but not in Colombia（分布于委内瑞拉安第斯山脉、但不分布于哥伦比亚的鸟类）
- （3）Fluent（流畅）、Natural（自然）
- （4）Relevance & Attribution Labeling（相关性与归因标注）
  - Rose-crowned parakeet：Partial Evidence（部分证据）、Likely Relevant（可能相关）
  - Mérida sunangel：Complete Evidence（完整证据）、Definitely Relevant（肯定相关）

第 1 页的 `find_tables` 把图 1 拆成了空单元格居多的碎片，未形成可用的数据表。上列文字来自按页 `get_text`。

<!-- 原 PDF 第 2 页 -->

把查询约束直接匹配到文本文档中的支持性证据来应对这类查询。然而，把多项约束与隐式集合运算组合在一起的查询，在现有检索基准中代表性不足，例如 MSMarco（Nguyen et al., 2016）和 Natural Questions（Kwiatkowski et al., 2019）。而且，这类数据集并不关注检索出一个穷尽的文档集合，而是把标注限制在某个基线信息检索系统的前若干条结果上。

为分析检索系统在这类查询上的表现，我们提出 QUEST。它是一个包含四个领域自然语言查询的数据集，这些查询被映射到相对完整的实体集合，实体对应于 Wikipedia 页面。我们把 Wikipedia 中的类别及其到实体的映射，用作数据集构建方法的基本构件，但在推理时不允许访问这一半结构化数据源，以模拟基于文本的检索。Wikipedia 类别涵盖了很广的一类用自然语言描述的实体属性，并且常常对应于搜索引擎用户有可能发出的、有选择性的信息需求查询。属性名称与文档文本之间的关系往往很微妙，需要精细的推理才能判定，这体现了该任务内在的自然语言推断挑战。

我们的数据集构建流程见图 1。基础查询利用 Wikipedia 类别名称半自动生成。为构造复杂查询，我们抽样类别名称，并用预定义模板把它们组合起来（例如 $A \cap B \setminus C$）。接下来，我们请众包人员改写这些自动生成的查询，同时确保改写后的查询流畅，并且清楚地描述用户可能在寻找什么。然后由另一批众包人员校验其自然性与流畅性，并按这些标准过滤。最后，对于数据中的很大一个子集，我们根据实体文档收集标量相关性标签，以及把查询约束映射到文档文本片段的细粒度文本归因。这类标注有助于开发能够从来源可信的材料中做出精确推断的系统。

要在该数据集上取得好成绩，系统必须能把查询约束与文档中的相应证据匹配起来，并处理查询所隐式指定的集合运算（见图 2），同时还要能高效扩展到大规模实体集合。我们通过在本数据集上微调预训练模型，评测了若干检索系统。系统被训练为：给定一条查询，检索出多文档集合。我们发现，当前的双编码器与交叉注意力模型，即便规模达到 T5-Large（Raffel et al., 2020），在带有集合运算的查询上做检索，大体上仍然效果不佳。带有合取与否定的查询对模型尤其困难，集合运算的组合会进一步增加系统的难度。我们的错误分析表明，不相关的假阳性实体，往往是因为模型忽略了被否定的约束，或忽略了查询中的合取约束。

**图 2：QUEST 中一条查询及其相关实体的示例。** 不同查询约束的归因可以来自文档的不同部分。

图中可见文字：

- 查询：Supernatural horror films set in Nevada（以内华达州为背景的超自然恐怖电影）
- 实体：Willy’s Wonderland
- 文档文本：Willy’s Wonderland is a 2021 American action comedy horror film directed by Kevin Lewis from a screenplay by G. O. Parsons. The film stars Nicolas Cage, who also [...] It follows a quiet drifter who is tricked into cleaning up an abandoned family entertainment center haunted by eight murderous animatronic characters. The project was announced in October 2019, [...] When his car catches a flat tire on a remote country road, a quiet drifter ends up stranded outside of Hayesville, Nevada. Mechanic Jed Love picks [...]
- 图中还标有 Large Document Corpus（大型文档语料库）、Retrieval System（检索系统）、Retrieved Set（检索得到的集合）。

第 2 页的 `find_tables` 把图 2 抽成了断词碎片（例如 “horror” 被拆开），未形成可读的表。上文文档摘录来自按页 `get_text`。

**2 相关工作**

先前关于问答与信息检索的工作，既关注知识库上的问答，也关注开放域问答，以及在一组实体或文档上的检索。下面我们说明这些工作与本文的关系。

**知识库问答。** 已有若干数据集被提出，用于知识库上的问答（Berant et al., 2013；Yih et al., 2016；Talmor and Berant, 2018；Keysers et al., 2020；Gu et al., 2021，等等）。这些基准要求检索一组作为节点而存在的实体，

<!-- 原 PDF 第 3 页 -->

或作为所附知识库中的关系而存在的实体。问题可以选择性地配有逻辑形式。Lan et al.（2021）对复杂知识库问答数据集做了全面综述。

先前的工作也同时指出，经过大量整理的大型知识库是不完整的（Watanabe et al., 2017）。值得注意的是，知识库问答系统在受限的答案模式上运行，这限制了它们所能处理的查询类型。此外，这些模式的构建与维护成本很高。因此，本文关注的设定是：我们不假设可以访问知识库。我们也注意到，知识库问答数据集已被改写到知识库不完整或不可用的设定中（Watanabe et al., 2017；Sun et al., 2019）。做法要么是从知识库中删去某一部分数据，要么是完全忽略知识库。与这些数据集的一个关键差别还在于：我们并不关注跨多篇文档的多跳推理。相反，一个实体是否相关，可以仅根据其自身文档来判定。

**开放域问答与检索。** 先前工作提出了许多开放域问答基准，它们考虑的是在非结构化文本语料上的问答。其中一些，例如 TREC（Craswell et al., 2020）、MSMarco（Nguyen et al., 2016）和 Natural Questions（Kwiatkowski et al., 2019），是用「现成数据」构建的，使用的是搜索引擎上的真实用户查询。Thakur et al.（2021）给出了一个把许多此类既有数据集放在一起考虑的基准。HotpotQA（Yang et al., 2018）和 MultiRC（Khashabi et al., 2018）等数据集关注多跳问答。另有工作探索了电子商务数据集（例如 Kong et al., 2022），但这些数据集并未公开。值得注意的是，这些数据集的侧重点与我们不同：我们关注的是在穷尽答案集合上包含隐式集合运算的查询。这类查询在现有数据集中代表性不足，因为它们出现在所考虑的查询分布的长尾中。

**多答案检索。** 相关工作（Min et al., 2021；Amouyal et al., 2022）也研究多答案检索问题，即系统需要对一条查询预测多个彼此不同的答案。Min et al.（2021）改编既有数据集（例如 WebQuestionsSP（Yih et al., 2016））来研究这一设定，并提出新指标 MRecall@K，用以评估对多个答案的穷尽 Recall。我们也考虑多答案集合检索问题，但考虑的是隐式包含集合约束的查询。

在同期工作中，RomQA（Zhong et al., 2022）提出一个开放域问答数据集，关注从 Wikidata 中抽出的约束组合。RomQA 与我们的动机相同，都是为了能够回答带有多项约束、且答案集合可能很大的查询。为了在没有人工标注的情况下使证据归因可行，RomQA 聚焦于这样一类问题：其组成约束可以从 Wikipedia 摘要中的单句、且已链接到实体的句子上加以验证；这些句子通过远程监督自动标注了关系，精确率高，但 Recall 可能较低（T-Rex 语料）。在 QUEST 中，我们放宽了查询—证据匹配操作的范围，允许通过更全局的、文档级的推断来做归因。为使归因的人工标注可行，我们限制了答案集合的大小，并把一个答案的证据限制在单篇文档之内。

**3 数据集生成**

QUEST 由 3357 条查询组成，每条查询配有至多 20 个对应实体。每个实体都有一篇由其 Wikipedia 页面派生的文档。数据集划分为 1307 条训练查询、323 条验证查询和 1727 条测试查询。系统的任务是：对给定查询返回正确的实体集合。此外，由于集合中包含 325,505 个实体，该任务要求检索系统能够高效扩展。在推理时，我们不允许系统访问实体文本描述之外的额外信息。所有实体文档中都省略了类别标签。

**3.1 原子查询**

本数据集中的基础原子查询（即未引入任何集合运算的查询）来自 Wikipedia 类别名称$^{2}$。这些是人工整理的自然语言标签，被赋予 Wikipedia 中一组相关文档$^{3}$。把类别指派给文档，使我们能够自动确定查询的答案实体集合，精确率高，Recall 也相对较高。我们计算所有相关类别的传递闭包，以确定其答案集合。

然而，把这些类别改用于构造查询会带来挑战：1）缺乏证据

$^{2}$ 我们使用 2022 年 6 月 1 日的 Wikipedia 版本。

$^{3}$ 注意，这些类别标签本身有时也可以是合取式的，从而可能增加复杂度。

<!-- 原 PDF 第 4 页 -->

在文档中：文档可能并不包含足以判断其与某个类别是否相关的证据，从而给可归因于文档文本的相关性带来噪声信号；2）Recall 低：实体可能从其本应所属的类别中缺失。对于大约一半的数据，我们基于文档文本众包了相关性标签与归因，并通过人工错误分析考察 Recall（第 5 节）。

我们选择四个领域，以体现查询上的一定多样性：电影、图书、动物和植物。聚焦于四个领域而不是所有可能的领域，有助于提高质量控制。前两个领域刻画的是一般搜索场景，后两个领域刻画的是科学搜索场景。

**3.2 引入集合运算**

为构造带有集合运算的查询，我们定义了表示原子查询之合理组合的模板。把原子查询记为 $A$、$B$ 和 $C$，我们的模板以及来自不同领域的相应示例列于表 1。模板由三种基本集合运算（交集、并集与差集）组合而成。选择这些模板时，略去了非结合的集合运算组合，以保证所得查询的解释没有歧义。

下面说明为组合复杂查询而抽样原子查询（即 $A$、$B$、$C$）时、针对不同集合运算所依据的逻辑。在所有情形中，我们都保证答案集合包含 2 到 20 个实体，以便众包相关性判断是可行的。我们对每个模板、每个领域抽样 200 条查询，最初共 4200 条查询。数据集被平均划分为训练+验证（80–20 划分）与测试。在其中每一个集合里，我们按模板抽样了数量相等的查询。

**交集。** 对模板 $A \cap B$ 而言，当 $A$ 与 $B$ 的答案集合都很大、但其交集很小时，交集运算尤其有意思，也潜在地更困难。我们要求 $A$ 与 $B$ 各自的最小答案集合规模相当大（多于 50 个实体），同时它们的交集要小（2 到 20 个实体）。

**差集。** 与交集类似，我们要求 $A$ 与 $B$ 的答案集合都相当可观（多于 50 个实体），但对 $A$（少于 200 个实体）和 $B$（少于 10000 个实体）都设置了规模上限，因为过大的类别在 Wikipedia 中往往存在 Recall 问题。我们还限制 $A$ 与 $B$ 的交集（理由见附录 B）。

**并集。** 对于并集运算，我们要求 $A$ 与 $B$ 都通过其并集 $A \cup B$ 的答案集合中的实体得到充分代表。因此，我们要求 $A$ 与 $B$ 都至少有 3 个实体。此外，我们要求它们的交集非空，但小于其并集的三分之一。这样做是为了让 $A$ 与 $B$ 在一定程度上是相关的查询。

**表 1：用于构造带集合运算查询的模板，以及所考虑的四个领域中的示例，并给出每个领域、每个模板的示例数量。**

`find_tables` 把表 1 抽成了一行，各列内容被拼接在一起；下列行列对齐来自按页 `get_text` 的阅读顺序，并与该次 `find_tables` 抽出的模板序列、示例序列和数量序列一致。数字均来自抽取结果，未另行填写。

| 领域 | 模板 | 示例 | 查询数 |
| --- | --- | --- | --- |
| 电影 | $A$ | 意大利强盗传记电影 | 125 |
| 电影 | $A \cup B$ | 荷兰犯罪喜剧或浪漫喜剧电影 | 135 |
| 电影 | $A \cap B$ | 以 20 世纪 70 年代为背景的意大利犯罪电影 | 143 |
| 电影 | $A \setminus B$ | 并非关于板球的印度体育电影 | 126 |
| 电影 | $A \cup B \cup C$ | 荷兰或瑞士战争电影，或 1945 年的战争电影 | 122 |
| 电影 | $A \cap B \cap C$ | 在 cleveland 拍摄的 21 世纪 20 年代剧情片 | 124 |
| 电影 | $A \cap B \setminus C$ | 不以以色列为背景的、关于基督教的史诗电影 | 121 |
| 图书 | $A$ | 2004 年德国小说 | 125 |
| 图书 | $A \cup B$ | 1925 年俄国小说，或 Ivan Bunin 的小说 | 125 |
| 图书 | $A \cap B$ | 以冰岛为背景的 1991 年小说 | 133 |
| 图书 | $A \setminus B$ | 以 20 世纪头十年为背景、并非基于真实事件的小说 | 123 |
| 图书 | $A \cup B \cup C$ | 以南京、河北或江苏为背景的小说 | 125 |
| 图书 | $A \cap B \cap C$ | Harper & Brothers 的英语儿童小说 | 124 |
| 图书 | $A \cap B \setminus C$ | 发生在越南、但并非关于战争的小说 | 115 |
| 植物 | $A$ | 仅产于加蓬的植物 | 115 |
| 植物 | $A \cup B$ | 曼尼托巴或亚北极美洲的树 | 125 |
| 植物 | $A \cap B$ | 用于美洲原住民传统医药的灌木 | 135 |
| 植物 | $A \setminus B$ | 产于美国西北部、在加拿大找不到的树 | 61 |
| 植物 | $A \cup B \cup C$ | 瓜德罗普的蛾、昆虫或节肢动物 | 121 |
| 植物 | $A \cap B \cap C$ | 北极、英国和高加索共有的植物 | 123 |
| 植物 | $A \cap B \setminus C$ | 印度尼西亚和马来西亚有、但泰国没有的兰花 | 122 |
| 动物 | $A$ | 柬埔寨的啮齿动物有哪些 | 115 |
| 动物 | $A \cup B$ | 来自古巴或牙买加、且已灭绝的动物 | 121 |
| 动物 | $A \cap B$ | 属于奇蹄类的非洲新近纪哺乳动物 | 111 |
| 动物 | $A \setminus B$ | 蒙古的非古北界鸟类 | 110 |
| 动物 | $A \cup B \cup C$ | 亚洲或非洲的新生代鸟类，或亚洲的古近纪鸟类 | 114 |
| 动物 | $A \cap B \cap C$ | 既是智利鸟类、也是秘鲁鸟类和圭亚那区动物区系的鸟类 | 104 |
| 动物 | $A \cap B \setminus C$ | 见于大西洋和哥伦比亚、但不见于巴西的哺乳动物 | 114 |

原文示例（便于对照专名，与上表同行）：

- Films / $A$：Biographical Italian bandits films（125）
- Films / $A \cup B$：Dutch crime comedy or romantic comedy films（135）
- Films / $A \cap B$：Italian crime films set in the 1970’s（143）
- Films / $A \setminus B$：Indian sport films that are not about cricket（126）
- Films / $A \cup B \cup C$：Dutch or Swiss war films, or war films from 1945（122）
- Films / $A \cap B \cap C$：2020’s drama films shot in cleveland（124）
- Films / $A \cap B \setminus C$：Epic films about Christianity not set in Israel（121）
- Books / $A$：2004 German novels（125）
- Books / $A \cup B$：1925 Russian novels or Novels by Ivan Bunin（125）
- Books / $A \cap B$：1991 Novels set in Iceland（133）
- Books / $A \setminus B$：Novels set in the 1900s not based on real events（123）
- Books / $A \cup B \cup C$：Novels set in Nanjing, Hebei, or Jiangsu（125）
- Books / $A \cap B \cap C$：English language Harper & Brothers Children’s fiction books（124）
- Books / $A \cap B \setminus C$：Novels that take place in Vietnam that aren’t about war（115）
- Plants / $A$：plants only from Gabon（115）
- Plants / $A \cup B$：Trees of Manitoba or Subarctic America（125）
- Plants / $A \cap B$：Shrubs used in traditional Native American medicine（135）
- Plants / $A \setminus B$：Trees from the Northwestern US that can’t be found in Canada（61）
- Plants / $A \cup B \cup C$：Moths or Insects or Arthropods of Guadeloupe（121）
- Plants / $A \cap B \cap C$：Plants the Arctic, the United Kingdom, and the Caucasus have in common（123）
- Plants / $A \cap B \setminus C$：Orchids of Indonesia and Malaysia but not Thailand（122）
- Animals / $A$：what are the Rodents of Cambodia（115）
- Animals / $A \cup B$：Animals from Cuba or Jamaica that are extinct（121）
- Animals / $A \cap B$：Neogene mammals of Africa that are Odd-toed ungulates（111）
- Animals / $A \setminus B$：Non-Palearctic birds of Mongolia（110）
- Animals / $A \cup B \cup C$：Cenozoic birds of Asia or Africa or Paleogene birds of Asia（114）
- Animals / $A \cap B \cap C$：Birds of Chile that are also Birds of Peru and Fauna of the Guianas（104）
- Animals / $A \cap B \setminus C$：mammals found in the Atlantic Ocean and Colombia, but not in Brazil（114）

<!-- 原 PDF 第 5 页 -->

**表 2：QUEST 中不同领域示例的统计。**

第 5 页默认 `find_tables` 返回 0 张表。下表按同页 `get_text` 的行序整理，数字均来自该抽取，未另行填写。

|  | 电影 | 图书 | 植物 | 动物 | 全部 |
| --- | --- | --- | --- | --- | --- |
| 查询数 | 896 | 870 | 802 | 789 | 3357 |
| 实体数 | 146368 | 50784 | 83672 | 44681 | 325505 |
| 平均查询长度 | 8.68 | 7.93 | 8.94 | 9.09 | 8.64 |
| 平均文档长度 | 532.2 | 655.3 | 258.1 | 293.1 | 452.2 |
| 平均答案集合大小 | 8.8 | 8.6 | 12.2 | 12.6 | 10.5 |

对于其余所有由上述集合运算组合而成的模板，我们递归地施加同样的约束。例如，对于 $A \cap B \setminus C$，我们先为交集运算抽样原子查询 $A$ 和 $B$，再根据 $A \cap B$ 与 $C$ 之间的关系抽样 $C$。

**3.3 标注任务**

基于模板自动生成查询，得到的查询并不总是流畅、连贯的。此外，映射到某条查询的实体未必真正相关，也并不总是拥有可用于判断其相关性的可归因证据。我们通过众包来处理这些问题。标注任务旨在确保：1）查询流畅、无歧义，并包含多样的自然语言逻辑连接词；2）实体被核实为相关或不相关；3）对每个相关实体，相关性判断都被归因到文档文本。众包分三个阶段进行，如下所述。更多标注细节和标注界面见附录 C。

**3.3.1 改写**

众包人员被要求改写一条按模板生成的查询，使改写后的查询流畅，表达原查询中的全部约束，并清楚描述用户可能在寻找什么。每条查询由一名工作人员完成此项标注。

**3.3.2 校验**

这一阶段旨在校验我们从改写阶段得到的查询。众包人员拿到第一阶段的查询，并被要求标注：该查询是否 1）流畅，2）在意义上等同于原来的模板查询，以及 3）为其自然性打分（真实用户发出该查询的可能性有多大）。每条查询由 3 名工作人员完成此项标注。根据多数表决，我们排除了那些被评为不流畅、不自然、或与原查询意义不同的查询。基于这次校验，我们从第 1 阶段去掉了大约 11% 的查询。

**3.3.3 相关性标注**

接下来，众包人员被要求为自动确定的查询答案集合提供相关性判断。具体而言，他们会拿到一条查询以及相关联的实体/文档，并被要求在 0–3 的量表上标注其相关性（肯定不相关、可能不相关、可能相关、肯定相关）。他们被要求保证：相关性应主要从文档中推断，但可以使用一些背景知识，并做最少量的查证。

我们还请他们为文档相关性提供归因。具体而言，我们先请他们标注文档是否为该实体的相关性提供了充分证据（完整 / 部分 / 无）。然后，针对查询中的不同短语（由标注者确定），我们请他们在文档中标出表明其相关性的句子。归因标注大体上受 Rashkin et al.（2021）启发。对于被否定的约束，若句子提供了反证，我们请标注者标出可归因的句子。由于这项标注很费时，我们只为两个领域（电影和图书）收集了这些标注。我们发现，植物和动物领域的相关性标注尤其困难，因为它们需要更专门的科学知识。在更大规模数据收集之前的预试验中，我们针对电影领域的 905 对查询与文档，从不同标注者处收集了 3 份相关性评分。在 61.4% 的情形中，3 名评分者都把文档判为「肯定相关」或「可能相关」，或者 3 名评分者都把文档判为「肯定不相关」或「可能不相关」。该数据上的 Fleiss’ kappa 为 $K=0.43$。我们从答案集合中排除了所有根据文档文本被标为可能不相关或肯定不相关的实体。第 2 阶段约有 23.7% 的查询—文档对被排除。

<!-- 原 PDF 第 6 页 -->

**图 3：我们比较若干系统。每个系统由两部分组成：一个检索器，用于从文档语料库中高效选出一组候选；以及一个文档相关性分类器，用于确定最终预测的文档集合。**

图中可见文字：Query（查询）；Document Corpus（文档语料库）；Retriever（BM25 or T5 Dual Encoder）（检索器，BM25 或 T5 双编码器）；Top-100 Candidate Documents（前 100 篇候选文档）；Relevance Classifier（T5）（相关性分类器，T5）；Predicted Document Set（预测文档集合）。

**3.4 数据集统计**

基本数据集统计见表 2。数据集中来自电影领域的实体更多，因为该领域在 Wikipedia 中更为充实。查询的平均长度为 8.6 个词，文档的平均长度为 452 个词。电影和图书领域的文档平均更长，因为它们常常包含情节和故事线。大约 $\sim$69% 的实体具有完整证据，大约 $\sim$30% 具有部分证据。当查询中并非所有短语都在文档中有显式证据时（也就是说，它们可能需要背景知识或推理），证据被标为部分证据。每个实体平均有 33.2 个词被归因，最长的归因文本片段长度可达 1837 个词。最后，平均答案集合大小为 10.5 个实体。

**3.5 额外的训练样本**

在已标注数据之外，我们还生成了额外的合成样本用于训练。我们发现加入这些样本能提高模型表现，并在第 4 节的实验中使用了这些样本。为生成这些样本，我们从所有领域抽样 5000 条原子查询，确保它们尚未作为子查询出现在 QUEST 的任何查询中，并使用它们在 Wikipedia 中的对应实体作为其相关实体集合。

**4 实验设置**

我们评测现代检索系统，以建立基线表现。我们还进行了广泛的错误分析，以理解模型错误的模式以及 QUEST 中标签的质量。

**4.1 任务定义**

我们考虑一个语料库 $E$，它包含数据集中所有领域的实体。每个实体都配有一篇基于其 Wikipedia 页面的文档。数据集中的一个样本由一条查询 $x$，以及一个经过标注的相关实体集合 $y \subset E$ 组成。如第 3 节所述，对所有样本都有 $|y| < 20$。我们的任务是开发一个系统：给定 $E$ 和查询 $x$，预测一个相关实体集合 $\hat{y} \subset E$。

**4.2 评测**

我们的主要评测指标是平均 F1，即对每个样本的 F1 分数取平均。我们通过比较预测的实体集合 $\hat{y}$ 与标注集合 $y$，计算每个样本的 F1。

**4.3 基线系统**

我们评测了若干检索器与分类器的组合，如图 3 所示。对于检索器部分，我们考虑稀疏的 BM25 检索器（Robertson et al., 2009）和稠密的双编码器检索器（记为 DE）。遵循 Ni et al.（2022），我们用 T5（Raffel et al., 2020）编码器初始化双编码器，并用批内采样的 softmax 损失进行训练（Henderson et al., 2017）。一旦有了候选集合，就需要确定一组相关实体。为了对给定查询判断每篇候选文档的相关性，我们考虑一个由 T5 编码器和解码器组成的交叉注意力模型。$^{4}$ 我们用二元交叉熵损失训练该交叉注意力分类器，负例来自 BM25 检索到的前 1,000 篇文档中的不相关文档，以及随机的不相关文档（类似于 Nogueira and Cho（2019））。由于对大量候选做交叉注意力分类的计算开销很大，我们把 BM25 和双编码器限制为检索 100 个候选，再由交叉注意力分类器考虑这些候选。由于我们基于 T5 的双编码器只能高效容纳至多 512 个词元，

$^{4}$ 用 softmax 损失训练的 BM25 与双编码器分数，并未被归一化，因而不能作为文档的相关性概率。我们发现，朴素地对这些分数施加一个全局阈值来产生答案集合，不如使用以二元交叉熵损失训练的分类器来预测文档相关性。

<!-- 原 PDF 第 7 页 -->

我们截断文档文本。我们在第 5 节讨论这一做法的影响以及替代方案。此外，由于 T5 在 Wikipedia 上做过预训练，我们在附录 D 中考察记忆带来的影响。更多细节和超参数设置见附录 A。

**4.4 人工错误标注**

对于总体最好的系统，我们抽样错误，并人工标注了验证集中的 1145 对查询—文档。对于检索器，我们抽样了未进入前 100 候选集合的相关文档，以及排序高于相关文档的不相关文档。对于分类器，我们抽样了在前 100 候选集合上犯下的假阳性与假阴性错误。这一标注过程包括：对文档相关性的判断（以评估与数据集中标注的一致性），以及文档（以及双编码器或分类器所考虑的截断版本）是否包含足以合理判定相关性的证据。我们还为查询内部的每一项约束标注了相关性。这些结果在第 5 节讨论。

**5 结果与分析**

我们在表 3 中报告基线系统在测试集上的表现。本节概括我们对这些结果、以及对第 4.4 节所述错误标注所做分析的主要发现。

**双编码器优于 BM25。** 如表 3 所示，总体最好的系统在检索时使用 T5-Large 双编码器，而不是 BM25。若直接比较双编码器与 BM25 的 Recall，性能差距更为显著。我们在表 4 中，针对不同的候选集合大小，报告平均 Recall（对全部相关文档集合、按样本计算 Recall 后再平均）和 MRecall（Min et al., 2021）（候选集合包含全部相关文档的样本所占百分比）。

**表 3：在测试数据集上评测的基线系统的平均精确率、Recall 与 F1。**

第 7 页默认 `find_tables` 返回 0 张表。表 3 与表 4 的数字来自同页 `get_text`，未另行填写。

| 检索器（$K=100$） | 分类器 | 平均精确率 | 平均 Recall | 平均 F1 |
| --- | --- | --- | --- | --- |
| BM25 | T5-Base | 0.168 | 0.160 | 0.141 |
| BM25 | T5-Large | 0.178 | 0.168 | 0.150 |
| T5-Large DE | T5-Base | 0.153 | 0.354 | 0.176 |
| T5-Large DE | T5-Large | 0.165 | 0.368 | 0.192 |

**表 4：各检索器的平均 Recall 与 MRecall。**

| 检索器 | 平均 Recall@20 | 平均 Recall@50 | 平均 Recall@100 | 平均 Recall@1000 | MRecall@20 | MRecall@50 | MRecall@100 | MRecall@1000 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BM25 | 0.104 | 0.153 | 0.197 | 0.395 | 0.020 | 0.030 | 0.037 | 0.087 |
| T5-Base DE | 0.255 | 0.372 | 0.455 | 0.726 | 0.045 | 0.088 | 0.127 | 0.360 |
| T5-Large DE | 0.265 | 0.386 | 0.476 | 0.757 | 0.047 | 0.100 | 0.142 | 0.408 |

**检索与分类都具有挑战性。** 由于我们只考虑检索器的前 100 个候选，检索器的 Recall@100 为整个系统的 Recall 设定了上界。T5-Large 双编码器的 Recall@100 仅为 0.476，而 T5-Large 分类器把总体 Recall 进一步降到 0.368，尽管精确率只有 0.165。这表明两个阶段都有改进空间，从而提高总体分数。由于检索和分类在更大的 T5 规模上都有所提升，进一步扩大模型规模可能是有益的。

**模型在交集与差集上表现吃力。** 我们还按不同模板和领域分析结果，如表 5 所示。不同约束会导致答案集合大小以及所使用的原子类别呈现不同的分布。因此，跨模板解释 F1 分数的差异可能很困难。尽管如此，我们发现带有集合并集的查询具有最高的平均 F1。带有集合交集的查询平均 F1 最低，带有集合差集的查询看来也具有挑战性。

为分析为什么带有合取与否定的查询具有挑战性，我们在系统错误地把一篇不相关文档判为相关的情形下，标注了单条查询约束的相关性（第 4.4 节）。结果汇总于表 6。对于涉及交集的大多数假阳性错误，至少有一项约束得到满足。这可以解释为模型在判定相关性时，错误地把

<!-- 原 PDF 第 8 页 -->

交集当作并集。类似地，对于带有集合差集的大多数样本，被否定的约束并未得到满足。这表明系统对否定不够敏感。

**表 5：我们最强基线（T5-Large DE + T5-Large 分类器）在各模板和各领域上的 F1。**

第 8 页默认 `find_tables` 把表 6 抽成了两格拼接文本，未给出表 5。表 5 的数字来自同页 `get_text`。表 6 的数字同时见于 `get_text` 与该次 `find_tables`，二者一致，未另行填写。

| 模板 | 电影 | 图书 | 植物 | 动物 | 全部 |
| --- | --- | --- | --- | --- | --- |
| $A$ | 0.231 | 0.436 | 0.209 | 0.214 | 0.274 |
| $A \cup B$ | 0.264 | 0.366 | 0.229 | 0.271 | 0.282 |
| $A \cap B$ | 0.115 | 0.138 | 0.049 | 0.063 | 0.092 |
| $A \setminus B$ | 0.177 | 0.188 | 0.216 | 0.204 | 0.193 |
| $A \cup B \cup C$ | 0.200 | 0.348 | 0.306 | 0.294 | 0.287 |
| $A \cap B \cap C$ | 0.086 | 0.121 | 0.07 | 0.065 | 0.086 |
| $A \cap B \setminus C$ | 0.119 | 0.112 | 0.121 | 0.136 | 0.122 |
| 全部 | 0.171 | 0.248 | 0.165 | 0.182 | 0.192 |

**精确率和 Recall 都有很大的提升空间。** 作为人工错误分析（第 4.4 节）的一部分，我们自行做了相关性判断，并度量其与 QUEST 中相关性标注的一致性。由于这一分析聚焦于我们最好的系统与数据集中相关性标签不一致的情形，我们预期这些情形上的一致性会显著低于数据集中随机选取的查询—文档对。因此，它提供了一种有针对性的方式，用来判断该数据集的提升空间和标注质量。

对于假阴性错误，在电影和图书领域，我们判定 91.1% 的实体是相关的；在植物和动物领域，这一比例为 81.4%。值得注意的是，我们为电影和图书领域收集了相关性标签，并如第 3 节所述根据这些标签移除了一些实体，这很可能解释了这两个领域假阴性上更高的一致性。这表明，按 QUEST 所定义的 Recall 仍有很大的提升空间，尤其是在我们收集了相关性标签的领域。

对于假阳性错误，我们判定 28.8% 的实体是相关的，这与数据集中的相关性标签存在更大的分歧。这主要是因为实体并未包含在由 Wikipedia 类别体系派生的实体集合中（97.7%），而不是因为实体在相关性标注中被移除。这是一个难以彻底解决的问题，因为不可能穷尽地为所有实体标注相关性，以修正 Wikipedia 类别体系中的 Recall 问题。未来工作可以使用汇聚（pooling）来持续扩大相关文档集合（Sparck Jones and Van Rijsbergen, 1975）。尽管如此，我们的分析表明精确率仍有很大的提升空间，因为我们判定，假阳性预测中的很大一部分是不相关的。

**表 6：对 T5-Large 分类器假阳性错误的分析，以及 T5-Large 双编码器把不相关文档排在相关文档之前的情形。** 对于带有合取的查询，我们统计预测文档未满足模板中 1、2 或 3 项约束的情形所占百分比（# Constraints，约束条数）。对于带有否定的查询，我们统计被否定约束（Neg.）未被满足的情形所占百分比。表中「—」表示抽取文本中的空缺标记。

|  | 模板 | 1 项约束未满足 | 2 项约束未满足 | 3 项约束未满足 | Neg. |
| --- | --- | --- | --- | --- | --- |
| 检索器 | $A \cap B$ | 63.5 | 36.5 | — | — |
| 检索器 | $A \cap B \cap C$ | 56.5 | 37.0 | 6.5 | — |
| 检索器 | $A \setminus B$ | 80.3 | 19.7 | — | 59.1 |
| 检索器 | $A \cap B \setminus C$ | 47.6 | 40.5 | 11.9 | 26.2 |
| 分类器 | $A \cap B$ | 83.3 | 16.7 | — | — |
| 分类器 | $A \cap B \cap C$ | 73.2 | 22.0 | 4.9 | — |
| 分类器 | $A \setminus B$ | 81.0 | 19.1 | — | 38.1 |
| 分类器 | $A \cap B \setminus C$ | 95.5 | 4.6 | 0.0 | 68.2 |

**截断文档文本通常能提供充分的上下文。** 在实验中，我们把双编码器的文档文本截断到 512 个词元，把分类器的文档文本截断到 384 个词元，以便把文档和查询拼接在一起。根据我们的错误分析（第 4.4 节），在具有充分证据、因而可以判断相关性的文档中，证据出现在这一截断上下文之内的比例，对双编码器为 93.2%，对分类器为 96.1%。这或许可以解释：对于处理长文档，这一简单基线何以相对成功。我们还评测了替代策略，但它们在初步实验中表现更差。$^{5}$ 未来工作可以评测高效的 Transformer 变体（Guo et al., 2022；Beltagy et al., 2020）。

**6 结论**

我们提出 QUEST，一个新的查询基准：这些查询包含隐式集合运算，并配有相应的相关实体文档集合。我们的实验表明，这类查询对

$^{5}$ 对于双编码器，我们把文档切成相互重叠的、长度为 512 个词元的块，并在推理时聚合分数（Dai and Callan, 2019）。对于交叉注意力模型，我们评测了用 BM25 选出长度为 128 的前 3 个段落。

<!-- 原 PDF 第 9 页 -->

现代检索系统构成挑战。未来工作可以考虑这样的方法：它们对处理自然语言表达中的集合运算具有更好的归纳偏置（例如 Vilnis et al.（2018））。QUEST 中的归因可用于构建能够在推理时提供细粒度归因的系统。也可以研究预训练生成式语言模型以及多证据聚合方法的潜力：它们在回答寻求集合的选择性查询的同时，提供对来源的归因。

**7 局限性**

**自然性。** 由于本数据集依赖 Wikipedia 类别名称以及半自动生成的组合，它并不代表真实搜索查询中、包含隐式集合运算的那部分查询之自然分布的无偏样本。此外，我们把注意力限制在无歧义的查询上，并不处理真实搜索场景中因歧义而产生的额外挑战。不过，本数据集中的查询被判定为可以合理地对应于真实用户的搜索需求；在 QUEST 上测得的系统改进，应当与至少一部分带有集合运算的自然搜索引擎查询上的改进相关。

**Recall。** 我们还指出，由于 Wikipedia 类别对所有相关实体（即其文档中包含充分证据的实体）的 Recall 并不完美，系统可能会因为预测出被评估为假阳性的相关实体而受到不正确的惩罚。我们在第 5 节对此做了量化。我们还把一个实体的可信来源限制为其 Wikipedia 文档，但文档中文本证据不足的实体仍可能是相关的。理想情况下，可以同时考虑多个可信来源，并聚合证据以做出相关性决策。RomQA（Zhong et al., 2022）在后一方向上迈出了一步，尽管其证据归因并未经过人工核验。

**答案集合大小。** 为确保相关性标签正确且可核验，我们寻求众包人员的帮助。然而，这意味着我们需要把数据集中查询的答案集合大小限制在 20，以使标注可行。一方面，这对搜索场景是现实的，因为用户可能只对有限的一组结果感兴趣。另一方面，本数据集并不刻画答案集合大得多的场景。

**致谢**

我们感谢 Isabel Kraus-Liang、Mahesh Maddinala、Andrew Smith、Daphne Domansi 以及全体标注人员的工作。我们也感谢 Mark Yatskar、Dan Roth、Zhuyun Dai、Jianmo Ni、William Cohen、Andrew McCallum、Shib Sankar Dasgupta 和 Nicholas Fitzgerald 的有益讨论。

**参考文献**

Samuel Joseph Amouyal, Ohad Rubin, Ori Yoran, Tomer Wolfson, Jonathan Herzig, and Jonathan Berant. 2022. Qampari：一个开放域问答基准，面向具有许多答案、且答案来自多个段落的问题. ArXiv, abs/2205.12665.

Iz Beltagy, Matthew E. Peters, and Arman Cohan. 2020. Longformer：长文档 Transformer. arXiv:2004.05150.

Jonathan Berant, Andrew Chou, Roy Frostig, and Percy Liang. 2013. 基于问答对在 Freebase 上进行语义解析. In Proceedings of the 2013 Conference on Empirical Methods in Natural Language Processing, pages 1533–1544, Seattle, Washington, USA. Association for Computational Linguistics.

Nick Craswell, Bhaskar Mitra, Emine Yilmaz, Daniel Campos, and Ellen M Voorhees. 2020. TREC 2019 深度学习赛道概述. arXiv preprint arXiv:2003.07820.

Zhuyun Dai and Jamie Callan. 2019. 借助上下文神经语言建模，实现面向信息检索的更深文本理解. In Proceedings of the 42nd International ACM SIGIR Conference on Research and Development in Information Retrieval, pages 985–988.

Yu Gu, Sue Kase, Michelle Vanni, Brian Sadler, Percy Liang, Xifeng Yan, and Yu Su. 2021. 超越 iid：知识库问答的三个泛化层次. In Proceedings of the Web Conference 2021, pages 3477–3488.

Mandy Guo, Joshua Ainslie, David Uthus, Santiago Ontanon, Jianmo Ni, Yun-Hsuan Sung, and Yinfei Yang. 2022. LongT5：面向长序列的高效文本到文本 Transformer. In Findings of the Association for Computational Linguistics: NAACL 2022, pages 724–736, Seattle, United States. Association for Computational Linguistics.

Matthew Henderson, Rami Al-Rfou, Brian Strope, Yun-Hsuan Sung, László Lukács, Ruiqi Guo, Sanjiv Kumar, Balint Miklos, and Ray Kurzweil. 2017. 面向智能回复的高效自然语言回复建议. arXiv preprint arXiv:1705.00652.

<!-- 原 PDF 第 10 页 -->

Daniel Keysers, Nathanael Schärli, Nathan Scales, Hylke Buisman, Daniel Furrer, Sergii Kashubin, Nikola Momchev, Danila Sinopalnikov, Lukasz Stafiniak, Tibor Tihon, Dmitry Tsarkov, Xiao Wang, Marc van Zee, and Olivier Bousquet. 2020. 衡量组合泛化：一种在真实数据上的综合方法. In 8th International Conference on Learning Representations, ICLR 2020, Addis Ababa, Ethiopia, April 26-30, 2020. OpenReview.net.

Daniel Khashabi, Snigdha Chaturvedi, Michael Roth, Shyam Upadhyay, and Dan Roth. 2018. 超越表面：面向多个句子之上阅读理解的挑战集. In Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long Papers), pages 252–262, New Orleans, Louisiana. Association for Computational Linguistics.

Weize Kong, Swaraj Khadanga, Cheng Li, Shaleen Gupta, Mingyang Zhang, Wensong Xu, and Mike Bendersky. 2022. 多方面稠密检索. In Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining.

Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh, Chris Alberti, Danielle Epstein, Illia Polosukhin, Jacob Devlin, Kenton Lee, Kristina Toutanova, Llion Jones, Matthew Kelcey, Ming-Wei Chang, Andrew M. Dai, Jakob Uszkoreit, Quoc Le, and Slav Petrov. 2019. Natural Questions：问答研究基准. Transactions of the Association for Computational Linguistics, 7:452–466.

Matthew Lamm, Jennimaria Palomaki, Chris Alberti, Daniel Andor, Eunsol Choi, Livio Baldini Soares, and Michael Collins. 2021. QED：问答中解释的框架与数据集. Transactions of the Association for Computational Linguistics, 9:790–806.

Yunshi Lan, Gaole He, Jinhao Jiang, Jing Jiang, Wayne Xin Zhao, and Ji-Rong Wen. 2021. 复杂知识库问答综述：方法、挑战与解决方案. Proceedings of the Thirtieth International Joint Conference on Artificial Intelligence (IJCAI-21).

Sewon Min, Kenton Lee, Ming-Wei Chang, Kristina Toutanova, and Hannaneh Hajishirzi. 2021. 面向多样化多答案检索的联合段落排序. In Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, pages 6997–7008, Online and Punta Cana, Dominican Republic. Association for Computational Linguistics.

Tri Nguyen, Mir Rosenberg, Xia Song, Jianfeng Gao, Saurabh Tiwary, Rangan Majumder, and Li Deng. 2016. MS MARCO：人工生成的机器阅读理解数据集. In CoCo@NIPs.

Jianmo Ni, Chen Qu, Jing Lu, Zhuyun Dai, Gustavo Hernandez Abrego, Ji Ma, Vincent Zhao, Yi Luan, Keith Hall, Ming-Wei Chang, and Yinfei Yang. 2022. 大型双编码器是可泛化的检索器. In Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing, pages 9844–9855, Abu Dhabi, United Arab Emirates. Association for Computational Linguistics.

Rodrigo Nogueira and Kyunghyun Cho. 2019. 使用 BERT 进行段落重排序. arXiv preprint arXiv:1901.04085.

Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, and Peter J Liu. 2020. 探索统一文本到文本 Transformer 迁移学习的极限. Journal of Machine Learning Research, 21:1–67.

Hannah Rashkin, Vitaly Nikolaev, Matthew Lamm, Lora Aroyo, Michael Collins, Dipanjan Das, Slav Petrov, Gaurav Singh Tomar, Iulia Turc, and David Reitter. 2021. 衡量自然语言生成模型中的归因.

Stephen Robertson, Hugo Zaragoza, et al. 2009. 概率相关性框架：BM25 及其后. Foundations and Trends® in Information Retrieval, 3(4):333–389.

K. Sparck Jones and C. J. Van Rijsbergen. 1975. 关于理想信息检索测试集之需求与提供的报告.

Haitian Sun, Tania Bedrax-Weiss, and William Cohen. 2019. PullNet：在知识库与文本上进行迭代检索的开放域问答. In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP), pages 2380–2390, Hong Kong, China. Association for Computational Linguistics.

Alon Talmor and Jonathan Berant. 2018. 把万维网当作回答复杂问题的知识库. In Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long Papers), pages 641–651, New Orleans, Louisiana. Association for Computational Linguistics.

Nandan Thakur, Nils Reimers, Andreas Rücklé, Abhishek Srivastava, and Iryna Gurevych. 2021. BEIR：用于信息检索模型零样本评测的异构基准. In Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2).

Luke Vilnis, Xiang Li, Shikhar Murty, and Andrew McCallum. 2018. 用盒格测度对知识图谱做概率嵌入. In Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 263–272, Melbourne, Australia. Association for Computational Linguistics.

<!-- 原 PDF 第 11 页 -->

Yusuke Watanabe, Bhuwan Dhingra, and Ruslan Salakhutdinov. 2017. 通过检索与理解，从未结构化文本中进行问答. arXiv preprint arXiv:1703.08885.

Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William Cohen, Ruslan Salakhutdinov, and Christopher D. Manning. 2018. HotpotQA：一个面向多样化、可解释多跳问答的数据集. In Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing, pages 2369–2380, Brussels, Belgium. Association for Computational Linguistics.

Wen-tau Yih, Matthew Richardson, Chris Meek, Ming-Wei Chang, and Jina Suh. 2016. 语义解析标注对知识库问答的价值. In Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 2: Short Papers), pages 201–206, Berlin, Germany. Association for Computational Linguistics.

Victor Zhong, Weijia Shi, Wen-tau Yih, and Luke Zettlemoyer. 2022. RoMQA：一个面向稳健、多证据、多答案问答的基准. arXiv preprint arXiv:2210.14353.

<!-- 原 PDF 第 12 页 -->

**A 实验细节与超参数**

所有模型都从 T5 1.1 检查点出发进行微调。$^{6}$ 我们在 32 个 Cloud TPU v3 核心上微调 T5 模型。$^{7}$ 所有模型的微调时间都少于 8 小时。

**双编码器。** 我们使用 t5x_retrieval 库实现双编码器模型。$^{8}$ 我们根据验证集上的结果调节了部分参数。训练双编码器的相关超参数为：

- 学习率：1e-3
- 预热步数：1500
- 微调步数：15000
- 批大小：512
- 最大查询长度：64
- 最大候选长度：512

**分类器。** 对于负例，我们抽样 250 篇随机的不相关文档，并从 BM25 检索到的前 1000 篇文档中抽样 250 篇不相关文档。我们还把每个正例复制 50 次。我们发现，正例与负例数量大致相当，比在类别严重不平衡的情况下训练效果更好。我们发现，随机负例与来自 BM25 的负例相结合，优于只使用其中任何一种负例。此外，从 BM25 中选取负例，优于从 T5-Large 双编码器中选取负例。

对于 T5 的输入，我们把查询与截断后的文档文本拼接起来。T5 的输出是字符串 “relevant” 或 “not relevant”。在推理时对文档相关性进行分类，我们对指派给 “relevant” 标签的概率施加一个阈值，该阈值在验证集上调节。对 BM25 候选进行分类时，我们使用阈值 0.9；对双编码器候选进行分类时，我们使用阈值 0.95。

训练分类器的其他相关超参数为：

$^{6}$ https://github.com/google-research/t5x/blob/main/docs/models.md

$^{7}$ https://cloud.google.com/tpu/

$^{8}$ https://github.com/google-research/t5x_retrieval

- 学习率：1e-3
- 预热步数：1000
- 微调步数：10000
- 批大小：1024
- 最大源长度：512
- 最大目标长度：16

**B 集合差与 Recall**

**记号与假设。** 假设我们有两个从 Wikipedia 类别图派生的集合 $\hat{A}$ 与 $\hat{B}$。Wikipedia 类别图可能缺失一些相关实体，因而 $\hat{A} \subset A$ 且 $\hat{B} \subset B$，其中 $A$ 与 $B$ 被解释为包含全部相关实体的假设集合。我们用 Recall $r_A$ 与 $r_B$ 来量化缺失实体的程度，使得 $|\hat{A}| = r_A \cdot |A|$，$|\hat{B}| = r_B \cdot |B|$。我们用 $r_{\cap}$ 量化 $A$ 中同时也属于 $B$ 的元素所占比例，使得 $|A \cap B| = r_{\cap} \cdot |A|$。为简单起见，我们还假设 $\hat{A}$ 与 $\hat{B}$ 的重叠满足 $|\hat{A} \cap B| = r_A \cdot |A \cap B|$，以及 $|\hat{A} \cap \hat{B}| = r_A \cdot r_B \cdot |A \cap B|$。

**推导。** 相对于 $A \setminus B$，$\hat{A} \setminus \hat{B}$ 的 Recall（$r$）和精确率（$p$）作为 $r_A$、$r_B$ 与 $r_{\cap}$ 的函数是什么？

首先，我们推导 Recall 的这一函数：$^{9}$

$$
r = \frac{|(A \setminus B) \cap (\hat{A} \setminus \hat{B})|}{|(A \setminus B)|}
$$

$$
r = \frac{|(\hat{A} \setminus B)|}{|(A \setminus B)|}
$$

$$
r = \frac{|\hat{A}| - |\hat{A} \cap B|}{|A| - |A \cap B|}
$$

$$
r = \frac{r_A \cdot |A| - r_A \cdot r_{\cap} \cdot |A|}{|A| - (r_{\cap} \cdot |A|)}
$$

$$
r = \frac{r_A \cdot (1 - r_{\cap}) \cdot |A|}{(1 - r_{\cap}) \cdot |A|}
$$

$$
r = r_A
$$

精确率则为：

$$
p = \frac{|(A \setminus B) \cap (\hat{A} \setminus \hat{B})|}{|(\hat{A} \setminus \hat{B})|}
$$

$^{9}$ 我们指出成对集合 $X$ 与 $Y$ 的若干有用性质：$X \setminus Y = X \cap Y^{c}$，$|X \setminus Y| = |X| - |X \cap Y|$；若 $X \subset Y$，则 $X \cap Y = X$；若 $X \subset Y$，则 $Y^{c} \subset X^{c}$。

<!-- 原 PDF 第 13 页 -->

$$
p = \frac{|(\hat{A} \setminus B)|}{|(\hat{A} \setminus \hat{B})|}
$$

$$
p = \frac{|\hat{A}| - |\hat{A} \cap B|}{|\hat{A}| - |\hat{A} \cap \hat{B}|}
$$

$$
p = \frac{r_A \cdot |A| - r_A \cdot r_{\cap} \cdot |A|}{r_A \cdot |A| - r_A \cdot r_B \cdot r_{\cap} \cdot |A|}
$$

$$
p = \frac{r_A \cdot (1 - r_{\cap}) \cdot |A|}{r_A \cdot (1 - r_B \cdot r_{\cap}) \cdot |A|}
$$

$$
p = \frac{(1 - r_{\cap})}{(1 - r_B \cdot r_{\cap})}
$$

**讨论。** Recall 简单地等于 $r_A$，而精确率是 $r_B$ 与 $r_{\cap}$ 的一个更复杂的函数，并且在 $r_{\cap}$ 取值很大时可以非常低。直观地说，如果从 $\hat{A}$ 中减去 $\hat{B}$ 会去掉 $\hat{A}$ 的大部分，那么所得集合的精确率将主要由 $\hat{B}$ 中缺失的相关实体所主导。这促使我们限制用于构造涉及集合交集的查询的那两个集合的交集。例如，若 $r_B = 0.95$，则在 $r_{\cap} < 0.8$ 时，可以保证 $p > 0.83$。

**C 标注细节**

QUEST 中的标注任务由受薪承包人员完成。他们位于 Austin, TX，要么拥有学士学位（55%），要么拥有同等工作经验（45%）。他们按小时获得报酬，并由一家供应商招募，该供应商筛选了他们对美国英语的掌握情况。他们被告知自己的工作将如何被使用，并且可以退出。他们获得标准的合同工资，该工资符合其受雇所在国家的最低生活工资法律。呈现给标注人员的标注界面见图 4、图 5 和图 6。

**D 预训练数据记忆的影响**

由于我们用来初始化模型的 T5 检查点是在 C4 语料上预训练的（其中包含 Wikipedia），我们考察这些模型是否记住了 Wikipedia 类别图的某些方面。我们比较基于 T5 的双编码器模型的 Recall：一类是在 T5 检查点预训练日期之前创建的 Wikipedia 文档，另一类是预训练之后新增的文档。我们在表 7 中报告这些结果，并给出同一批文档在 BM25 检索器上的 Recall，作为基线比较。

**表 7：在 T5 预训练之前与之后创建的文档子集上的平均 Recall@100。**

第 13 页默认 `find_tables` 返回 0 张表。下表数字来自同页 `get_text`，未另行填写。

| 检索器 | 之前 | 之后 |
| --- | --- | --- |
| BM25 | 0.183 | 0.050 |
| T5-Large DE | 0.466 | 0.171 |

我们注意到，预训练之前加入的文档与预训练之后加入的文档，其分数之比在两个系统上是相似的，这表明记忆之外的因素可能解释这一差异。例如，在预训练日期之前与之后创建的文档，平均长度分别为 759.7 与 441.2 个词。

<!-- 原 PDF 第 14 页 -->

**图 4：改写阶段的标注界面。**

**图 5：校验阶段的标注界面。**

**图 6：相关性标注阶段的标注界面。**

这三幅图是标注界面截图。同页 `get_text` 只抽出上述图题；默认 `find_tables` 也只得到图题，没有抽出界面内部的控件文字。界面内文字见原 PDF 第 14 页。

<!-- 原 PDF 第 15 页 -->

**ACL 2023 Responsible NLP Checklist**

ACL 2023 所使用的 Responsible NLP Checklist 采纳自 NAACL 2022，并增加了一个关于人工智能写作辅助的问题。

清单条目的方框之后，文本层中紧跟不可读控制字符（多数为 U+0013；A4 为 U+0017）。勾选字形未进入文本层，见原 PDF 第 15–16 页。下面只译题干及其后写出的答复，不根据该控制字符判断是否勾选。

**A 对每一篇投稿：**

A1. 你是否描述了本工作的局限性？

答复：7

A2. 你是否讨论了本工作的任何潜在风险？

答复：不适用。我们没有识别出任何风险。

A3. 摘要和引言是否概括了本文的主要主张？

答复：摘要与第 1 节

A4. 在撰写本文时，你是否使用了人工智能写作助手？

答复：留空。

**B**

你是否使用或创建了科学成果物？

答复：我们将公开释放代码和数据集。

B1. 你是否引用了你所使用的成果物的创建者？

答复：附录 A

B2. 你是否讨论了任何成果物的使用许可或条款，和/或分发许可或条款？

答复：是的，我们将使用 MIT 许可证发布我们的数据集。

B3. 你是否讨论了：你对既有成果物的使用是否与其预期用途一致（若该预期用途已被说明）？对于你所创建的成果物，你是否说明了预期用途，以及该用途是否与原始访问条件兼容（尤其是：为研究目的而访问的数据之派生数据，不应在研究语境之外使用）？

答复：3

B4. 你是否讨论了为检查所收集/使用的数据是否包含点名或唯一标识个人的信息、或冒犯性内容而采取的步骤，以及为保护/匿名化这些数据而采取的步骤？

答复：3

B5. 你是否提供了成果物的文档，例如领域覆盖、语言与语言现象的覆盖、所代表的人口群体等？

答复：3

B6. 对于你所使用/创建的数据，你是否报告了相关统计，例如样本数量、训练/测试/开发集划分的细节等？即便对于常用的基准数据集，也应给出训练/验证/测试划分中的样本数量，因为这些信息为读者理解实验结果提供了必要语境。例如，大测试集上准确率的微小差异可能是显著的，而在小测试集上则可能并不显著。

答复：3

**C**

你是否运行了计算实验？

答复：4

C1. 你是否报告了所用模型的参数量、总计算预算（例如 GPU 小时）以及所使用的计算基础设施？

答复：附录 A

<!-- 原 PDF 第 16 页 -->

C2. 你是否讨论了实验设置，包括超参数搜索以及找到的最佳超参数值？

答复：第 4 节与附录 A

C3. 你是否报告了关于结果的描述性统计（例如结果周围的误差线、一组实验的汇总统计），并且是否透明地说明你报告的是最大值、均值等，还是仅仅单次运行？

答复：附录 A

C4. 如果你使用了既有软件包（例如用于预处理、归一化或评测），你是否报告了所使用的实现、模型与参数设置（例如 NLTK、Spacy、ROUGE 等）？

答复：附录 A

**D**

你是否使用了人工标注者（例如众包人员），或开展了有人类参与者的研究？

答复：附录 C

D1. 你是否报告了给予参与者的说明全文，包括例如截图、对参与者或标注者的任何风险声明等？

答复：附录 C

D2. 你是否报告了你如何招募参与者（例如众包平台、学生）以及如何支付报酬，并讨论了鉴于参与者的人口特征（例如居住国），这样的报酬是否充分？

答复：附录 C

D3. 你是否讨论了是否以及如何从你正在使用/整理其数据的人那里获得同意？例如，如果你通过众包收集数据，你给众包人员的说明是否解释了数据将如何被使用？

答复：附录 C

D4. 数据收集方案是否获得了伦理审查委员会的批准（或被判定为豁免）？

答复：留空。

D5. 你是否报告了作为数据来源的标注者群体的基本人口统计与地理特征？

答复：附录 C

<!-- 译完 -->
