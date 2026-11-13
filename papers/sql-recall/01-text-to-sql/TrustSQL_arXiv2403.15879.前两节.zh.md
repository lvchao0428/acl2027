> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

- 原文件名：TrustSQL_arXiv2403.15879.pdf
- 原文标题：TrustSQL: Benchmarking Text-to-SQL Reliability with Penalty-Based Scoring
- 作者：Gyubok Lee、Woosog Chay、Seonhee Cho、Edward Choi（KAIST AI）
- 场合：预印本，Under review；arXiv:2403.15879v6 [cs.AI]，2024 年 7 月 2 日。数据见 https://github.com/glee4810/TrustSQL

## 摘要

Text-to-SQL 让用户用自然语言检索和综合数据库里的信息。大语言模型把问题译成 SQL 已经很强，但广泛部署仍受两件事限制：用户必须事先知道模型能答对哪类问题；模型又不会弃答，错误 SQL 会悄悄产生，从而损害对输出的信任。

TrustSQL 用来评估 text-to-SQL reliability：对任何输入，可行问题要生成正确 SQL，不可行问题则弃答。不可行的原因包括与模式不兼容，或超出 SQL 的功能。评测使用一种带惩罚的新分数，并比较两类建模：一是流水线，把 SQL 生成器与不可行问题检测器、SQL 错误检测器组合起来以便弃答；二是用单一模型完成整个任务。实验结论是，在严厉惩罚下拿高分需要很大努力，这为更安全的部署提供了另一种看法。具体公式在第 3 节，这里不展开。

## 1 Introduction

Text-to-SQL 是从自然语言生成 SQL，这个问题已经存在数十年。数据库遍布医学、金融、零售和电信，用自然语言访问结构化数据，才能让领域专家从大数据里得到定量发现。要用好模型，用户得知道它能答准哪些问题、能看到什么信息、哪些运算 SQL 做得到或做不到。许多潜在用户并不了解这些能力，问题经常落在模型范围之外。真实部署里既有可行问题，也有不可行问题，例如要求数据库内容或 SQL 功能之外的知识。Figure 1(a) 把部署画成可行区域与不可行区域并存。现有模型没有弃答机制，两类问题上的错误输出都可能不被发现，甚至抵消使用模型的好处。若模型只在能给出正确 SQL 时回答、其余弃答，用户信心会提高。

Figure 1(b) 的标准 Text-to-SQL 追求尽量多生成正确 SQL。绿色是正确生成，红色是错误生成；用户必须熟悉每个模型能答对的问题类型，门槛很高。Figure 1(c) 的可靠 Text-to-SQL 要用弃答压低错误输出，同时在可行区域内尽量增加正确输出。脚注把图中五个区域定义为：（I）可行问题生成正确 SQL，可取；（II）对可行问题弃答，既非严格可取也非不可取，视为中性；（III）可行问题生成错误 SQL，不可取；（IV）不可行问题生成错误 SQL，不可取；（V）对不可行问题正确弃答，可取。缩小红色的（III）（IV），再缩小黄色的（II），用户才会信任输出。这五种情况都被放进后文的惩罚分数，例子在补充材料。

据此，text-to-SQL reliability 被定义成：靠正确生成 SQL 和弃答，正确处理任何输入，从而把 Figure 1(c) 里的红色和黄色区域缩掉、用绿色盖住整个区域。标准任务只定义在可行区域内；真实问题则跨过数据库内容和 SQL 功能的边界。TrustSQL 用三个领域数据集 ATIS、Advising、EHRSQL，以及一个跨领域数据集 Spider 构造这一设定。构造时刻意纳入破坏可靠性的常见错误，切分方式类似 red teaming，并加入多种不可行问题。他们用专为可靠性设计的惩罚分数评现有方法。引言中的实验观察是：多数先进方法在无惩罚设定下看起来不错，但在严厉惩罚下仍很难拿高分；从高惩罚的角度看，知道何时精确弃答，比贸然生成 SQL 更重要。

## 2 Dataset Construction

本节先列出部署中让答案掉进 Figure 1(c) 红色区域的常见错误，再说明如何把它们写进数据。五类是：SQL 生成的复杂度，尤其领域专家的问题太难，难在查询本身，或模型没见过库特有的说法和实体；不会弃答就会损害信任。可行数据因此纳入查询难度 [P1] 和熟悉度 [P2]。用户问句含糊，特别是指称列或取值不够精确；澄清需要多轮交互，超出本文范围。模式不兼容：不熟悉模式的用户会问现有列里不存在的信息；以往工作靠删除或扰动已有列来造这类例子，这里改成三种更细的类型 [P3]。SQL 功能范围：用户可能要求复杂数值运算、数据分析或预约安排等标准 SQL 做不到的事 [P4]。外部知识：问题可能完全超出库内容，例如 “What airport is in Wilder, KY?”，也可能只是部分超出，例如 “Find me patients born after WWII”。构造不可行问题时只收前者 [P5]，排除后者。

2.1 Feasible Data Construction 选了三个复杂的领域数据集：ATIS（航班）、Advising（教育）、EHRSQL（医疗），再加上跨领域的 Spider。领域与跨领域的差别以及各数据集复杂度放在补充材料。初步分析发现 ATIS 和 Advising 有大量重复查询、不一致和低质量自然语言，因此用 GPT-4 为全部输入问题生成新的转述，再由作者人工复查。预处理后的四个库及其问题–SQL 对，进入 Figure 1(a) 的可行区域（浅蓝色）。难度 [P1] 沿用文献中的 SQL hardness 标准，各级数量在补充材料的 Table 7。熟悉度 [P2] 留到 §2.3 的切分。

2.2 Infeasible Data Construction 针对灰色的不可行区域手工标注自然语言问题，这些请求没有对应 SQL。模式不兼容 [P3] 不随机删列，而引入 hypothetical columns：问题写得像存在 SQL，但库里并没有那些列。三类是 column-surface、column-related 和 column-unrelated，分别对应表面形式相似、语义上能自然并进模式、以及语义上不相关。surface 的例子是 dog_kennels 库里，Professionals 表上假想的 age 列，表面上像 Dogs 表已有的 age。related 的例子是 song 表上假想的 duration，被看成 ADVETA 里 ADD 扰动的手工版。unrelated 的例子是从别的库随机抽来、多半不自然的列，如 battles 库里的 product_category。超出 SQL [P4] 先列出 27 项 NLP 和数据分析任务，例如异常检测、可视化和网页搜索，用 GPT-4 判断：若允许使用任何工具，给定库内容后助手还能做什么；再按各库已有列手工写问题，模拟用户期待模型做 SQL 单独完成不了的事。外部知识 [P5] 用 GPT-4 生成需要领域专长、定性判断或因果理解的问题，直到样本量与其他不可行类型大致平衡。标注后再用 GPT-4 迭代复查，确认确实不可行。Table 1 给了 Spider 中 orchestra 库的例子，该库有 4 张表、23 列：surface 问所有演出的平均上座容量，对应假想列 show.attendance_capacity；related 问哪个乐团成员最多，对应 orchestra.number_of_member；unrelated 问 Charles Dutoit 拥有什么飞机，对应 conductor.aircraft；non-sql 要求找出影响上座率的三个最重要特征，注释为 feature importance；ext-know 问多样性给乐团带来什么好处。

2.3 Data Splitting 的原则是：可行数据要有不同的查询熟悉度 [P2]，不可行数据则要在评测时显得意外。SQL structure 在脚注中定义为：由特定 SQL 成分以及特定表和列组成的组合，不含实际数据值。seen SQL 指该 structure 出现在训练集，但验证集和测试集里是不同的转述问句；unseen SQL 指训练集里没有这种 structure。领域数据集的切分是：先按自然语言问题以 6:2:2 分成训练、验证和测试，各份的 SQL structure 相同、问句不同；再从验证集和测试集去掉 20% 互不重叠的 SQL structure；然后从训练集去掉共计 40% 的 SQL structure。结果是各划分里 60% 为 seen SQL，验证集和测试集包含 80% 的 SQL structure，其中 60% 是 seen SQL、20% 是 unseen SQL。Spider 把 development split 对半，成为新的验证集和测试集，各 10 个数据库，全部是 unseen SQL，与训练集无重叠。五种不可行问题（column-surface、column-related、column-unrelated、non-sql、ext-know）全部、并按大致均衡的比例放进测试集。

Table 2 给出规模。可行问题 \(Q\) 的三个数依次是训练、验证、测试；测试集里可回答与不可回答的问题数量相等。全部问题 \(Q \cup Q^c\)：ATIS 2555，Advising 2769，EHRSQL 7473，Spider 8561。表头把医疗数据集印成 EHRQSL，正文称 EHRSQL。可行问题：ATIS 1114 / 489 / 476，Advising 1170 / 533 / 533，EHRSQL 4674 / 931 / 934，Spider 7000 / 507 / 527。不可行问题 \(Q^c\) 为 ATIS 476、Advising 533、EHRSQL 934、Spider 527。其中 non-sql 为 99、110、191、100；surface 为 93、102、185、100；unrelated 为 94、110、187、100；related 为 98、107、189、100；ext-know 为 92、104、182、127。顺序均为 ATIS、Advising、EHRSQL、Spider。
