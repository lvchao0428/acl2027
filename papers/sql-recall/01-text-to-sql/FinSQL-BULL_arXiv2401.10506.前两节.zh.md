> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名：** FinSQL-BULL_arXiv2401.10506.pdf

**原文标题：** FinSQL: Model-Agnostic LLMs-based Text-to-SQL Framework for Financial Analysis

**作者：** Chao Zhang、Yuren Mao、Yijiang Fan、Yu Mi、Yunjun Gao、Lu Chen（Zhejiang University）；Dongfang Lou、Jinshu Lin（Hundsun Technologies INC.）。

**arXiv：** arXiv:2401.10506v1 [cs.CL]，2024 年 1 月 19 日。PDF 使用 ACM 模板，页眉仍为占位信息 Conference’17, July 2017, Washington, DC, USA；文内参考文献格式写 2018 年、13 页。

## 摘要 Abstract

金融分析需要 Text-to-SQL 这种不必手写 SQL 的关系数据库接口，因为从业人员往往不熟 SQL。此前没有面向金融分析的实用基准，已有方法也没处理金融库的特点，例如常见的宽表。作者从 Hundsun Technologies Inc. 的实际金融分析业务收集基准 BULL，库覆盖基金、股票和宏观经济；并提出与底座模型无关的大语言模型框架 FinSQL，从提示构造、参数高效微调和输出校准三方面处理金融 Text-to-SQL。摘要所报的后文主结果是：在 BULL 上以较小代价达到当时的最优表现，少样本跨库迁移场景最高提升 36.64%。

## 1 INTRODUCTION

这一节先把任务和缺口钉住。Text-to-SQL 把自然语言问题变成可执行 SQL，方便不熟 SQL 的人查库。投资顾问等金融人员要频繁查库，所以该任务对金融分析很重要。作者认为缺两样东西：金融分析用的 Text-to-SQL 基准，以及对金融库特点的处理。

BULL 取自 Hundsun Technologies Inc. 的智能投顾产品，该产品服务超过 50 家金融机构（文中点名 Alipay、China Merchants Bank 等）和数百万个人用户。其中三个库分别对应基金、股票和宏观经济，由该公司的金融专业人员、数据科学家和软件工程师标注 4,966 对问题–SQL，并有英文和中文两个版本。相对 Spider、BIRD，BULL 每个库的表更多、列更多，表名和列名还常用缩写或含糊写法，模型因此要能吃下很长的上下文。Table 1（Differences Between Datasets）列出样本数、每库表数和每库列数：WikiSQL 为 80654 / 1 / 6.3，Spider 为 10181 / 5.1 / 27.1，BIRD 为 12751 / 7.3 / 54.2，BULL 为 4966 / 26 / 390。基于大语言模型的 Text-to-SQL 能满足长上下文和语境理解，但当时的领先方法依赖 OpenAI API，例如 GPT-3.5-turbo 或 GPT-4，费用高，还有信息泄露风险，不适合把隐私放在首位的金融应用。

改在私有域里训练开源模型（文中举 LLaMA 和 Baichuan）会遇到三件事。金融库表多列多，问题很难和 schema 项对齐；标注贵，问题–SQL 对的数量和多样性有限，简洁又多样的提示就难构造。下游微调往往要多块 GPU 算数日，迭代和换库迁移的成本都高。采样解码带来的随机性还会让输出不一致，SQL 出现语法错误或无效查询。FinSQL 可套在任意开源大语言模型上。Figure 1 把训练和推理分开：训练时先做混合数据增强，再训出面向不同 Text-to-SQL 任务的 LoRA 插件，由 LoRA plugin hub 管理；推理时先做 schema linking 得到精简提示，把合并后的 LoRA 接到基座上生成 SQL，再做输出校准。图例用冰与火分别表示冻结和更新权重。三个部件与上述困难对应：提示构造含并行 schema linking 和混合数据增强；参数高效微调用 LoRA 只更新很少一部分参数（<1%），做成可切换的权重插件，以支持少样本跨库迁移；输出校准对生成 SQL 做后处理。贡献概括为提出 BULL、提出 FinSQL，以及在 BULL 上表明该框架与底座无关、能达到最优，并且少样本跨库迁移最高提升 36.64%。

## 2 RELATED WORKS

数据集一条线用来说明学术基准和金融现场之间的距离。早期 GeoQuery、Scholar 查询量有限，只覆盖单库，SQL 也相对简单。WikiSQL 和 Spider 各自提供超过 10,000 条 SQL，能做跨库迁移，并包含复杂的多表查询。真实库往往更大，还会提供帮助理解 schema 的外部知识。KaggleDBQA 在八个库上构造了 272 条 SQL，用外部知识解释列的含义；BIRD 样本更多、库更大，并加入问题与库内容之间的外部知识。作者认为这些仍满足不了更复杂的工业需求。Table 1 显示，真实工业场景里的表数和列数远多于现有开源数据集，已有方法很难把 schema 信息纳入输入，因此难以在这种场景工作。

模型一条线从规则走到大语言模型。早期规则方法靠手写模板生成 SQL，换场景、扩展和泛化都弱。Seq2Seq 路线中，IRNet 用编码器表示问题和 schema；RAT-SQL、LGESQL 和 S²SQL 用图神经网络捕捉问题与 schema 的对齐，再由解码器生成 SQL。T5、mT5、LLaMA 等预训练模型加强了语言理解和泛化，微调方法随之变好：Graphix 让 T5 具备多跳推理，Picard 用约束解码提高 SQL 质量，RESDSQL 先检索与问题相关的 schema 元素再生成 SQL，论文称其为当时 Spider 排行榜上基于微调的最优方法。更近的大语言模型借 in-context learning 不必重训就能按指令做任务；Spider 榜上领先的是调用 GPT 的 C3、DIN-SQL 和 DAIL-SQL。这些方法要调用 OpenAI API，有成本和隐私风险，换场景时指令模板也要重做。
