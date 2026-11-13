> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

- 原文件名：ScienceBenchmark_PVLDB2024_Stockinger.pdf
- 原文标题：ScienceBenchmark: A Complex Real-World Benchmark for Evaluating Natural Language to SQL Systems
- 作者：Yi Zhang、Jan Deriu、Catherine Kosten、Kurt Stockinger（Zurich University of Applied Sciences）；George Katsogiannis-Meimarakis、Georgia Koutrika（Athena Research Center）
- 场合：Proceedings of the VLDB Endowment（PVLDB），Vol. 17, No. 4，685–698，2023；doi:10.14778/3636218.3636225

## 摘要

得益于基于 Transformer 的语言模型和 Spider 基准，NL-to-SQL 的准确率近来已超过 80%。Spider 里的库大多表少、列少、行少，并不像真实场景；复杂、领域专用的真实库又几乎没有 NL/SQL 成对训练数据，现有系统表现很差。

本文提出 ScienceBenchmark：面向三个真实、高度领域专用的数据库。每个领域由 SQL 专家和领域专家写出高质量 NL/SQL 对，再用 GPT-3 生成合成数据把少量人工数据扩开。作者认为该基准很难：在 Spider 上领先的系统到这里成绩很低。难点同时包括复杂领域、少量手工训练数据，以及用合成数据做增强。据作者所知，这是第一个以复杂真实科学数据库来设计、并由领域专家仔细校验训练与测试数据的 NL-to-SQL 基准。

## 1 INTRODUCTION

用自然语言查询结构化数据，被看作数据民主化的关键。数据库自然语言接口出现于 1970 年代。早期系统或靠模式把自然语言拼成 SQL（如 SODA、Precis），或先分析问句结构再映射到 SQL（如 ATHENA、NaLIR）。早在 1995 年就有人指出当时没有标准基准，对领域现状只能凭印象。WikiSQL 与 Spider 改变了这一点，使神经机器翻译式方法可以在大量 NL/SQL 对上训练。早期深度学习方法只处理单表，生成不了跨表的嵌套和复杂子句；较新的系统能覆盖整库，并在 Spider 上拿到高分，顶尖系统准确率最高到 85%。但 Spider 里多数库是为基准专门造的。当时开源领先系统里，带 Picard 约束解码的 T5-Large、SmBoP，以及带 NatSQL 的 RESDSQL，都已超过 70%。把在 Spider 上训练的系统拿到天体物理或癌症研究这类新领域，结果很差，离真实应用很远。

WikiSQL 的每个问题只对一张表，查询复杂度对真实应用几乎不够。Spider 有来自 138 个领域的 200 个关系数据库，以及超过 10,000 条自然语言问题和超过 5,000 条复杂 SQL，并试图用含新库的开发集处理迁移。这些库仍然偏简单、偏常识。科学领域需要专用基准，而纯手工构造在数据量和专业知识上都不可行，数据增强几乎是唯一可行的路。

ScienceBenchmark 与科研政策、天体物理、癌症研究的 SQL 专家和研究者一起做。Figure 1 是自动训练数据生成的四段流程：Seeding Phase、SQL Query Generation Phase、SQL-to-NL Translation Phase、Discriminative Phase。系统先吃入一小批人工 NL/SQL 对，抽出 SQL 模板，再按模式和库内容生成 SQL，然后用 GPT-3 回译成自然语言。作者比较过多种预训练 Transformer，GPT-3 最好，并且只需很少的种子对就能迁到新领域。生成的问句再由 critic 模型筛出与 SQL 最对应的一条。得到的增强数据可以送进任意 NL-to-SQL 系统训练；文中说这一做法是通用的，并在后文实验（Table 5）里展示能抬高准确率。

贡献有三点。其一，ScienceBenchmark 含超过 6,000 条 NL/SQL 对，针对流行基准忽略的真实复杂库。其二，这套自动生成方法针对几乎没有训练数据的库；与以往偏简单库的工作不同，这里集中在复杂科学库，也就是流行系统因缺领域知识和训练数据而容易失败的地方。其三，作者在该基准上评了三个当时领先的 NL-to-SQL 系统和两个 LLM。这些系统在 Spider 排行榜上准确率高于 82%，在 ScienceBenchmark 上按领域只有大约 25–60%，没有一个达到令人满意的分数。

## 2 THE NEED FOR A NEW BENCHMARK - MOTIVATING EXAMPLE: ASTROPHYSICS

NL-to-SQL 要同时对付含糊、指代难懂、用词和库不一致的自然语言，以及必须符合语法和模式的 SQL。科学库还多一层领域带来的困难。Spider 是第一个带复杂 SQL 的大规模数据集，但其库本身并不复杂：主题很泛，例如宠物和娱乐（音乐会、乐团、音乐剧），而且多数由学生专为 Spider 编写。本节以天体物理作动机；文中说这些困难同样适用于实验里的癌症研究。运行例子是 Sloan Digital Sky Survey（SDSS），存的是天空中特定位置的恒星和星系。库复杂度的进一步数字放在后文，本节不展开。

三条代表性问句用来说明难度，并标了 Spider 的 hardness：

- Q1（Easy）：找出所有 Starburst 星系。SQL 在 `specobj` 上过滤 `subclass = 'STARBURST'`，取出 `specobjid`。
- Q2（Medium）：要光谱观测星系的 object id、赤经、赤纬和红移，红移大于 0.5 且小于 1。SQL 在 `specobj` 上过滤 `class = 'GALAXY'` 以及 `z > 0.5 AND z < 1`，取出 `bestobjid`、`ra`、`dec`、`z`。
- Q3（Extra hard）：要测光对象及其光谱对象 id，光谱类别为 `GALAXY`，且星等 u 与 r 之差小于 2.22、大于 1。SQL 把 `photoobj` 与 `specobj` 按 `bestobjid = objid` 连接，并写 `p.u - p.r < 2.22 AND p.u - p.r > 1`。

由此归纳三类困难。未见过的领域：像天体物理这样的领域，写有意义的自然语言和 SQL 都需要专门知识，在 Spider 这类常识数据上预训练的神经机器翻译系统会因主题差距而失败。复杂且常晦涩的模式：科学库属性可以多到数百个，名字极短，例如 `ra`、`z`（赤经和红移），或只存数值测量；还需要额外本体来解释含义，其中可以包括方程和自然语言，从问句词元映射到属性并不容易。精细查询：领域查询可以比 Spider 更繁，分析要用属性和函数之间的数学运算，例如紫外 u 与红外 r 的星等差 `u - r < 2.22`。

这些观察说明需要能抓住领域语义和查询类型的专用基准。基准所需的规模又使纯手工构造不可行。大而复杂的模式连专家都难懂、难查，于是问题变成如何构造基准。作者的答案是数据增强，并随之提出三个未在本节展开的问题：如何为新库写出有代表性的 SQL，如何给出对应的自然语言描述，以及如何把人工参与压到最少。
