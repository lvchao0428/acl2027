> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名：** OmniSQL_arXiv2503.02240.pdf

**原文标题：** OmniSQL: Synthesizing High-quality Text-to-SQL Data at Scale

**作者：** Haoyang Li、Shang Wu、Xiaokang Zhang、Xinmei Huang、Jing Zhang（通讯作者）、Hong Chen、Cuiping Li（Renmin University of China）；Fuxin Jiang、Shuai Wang、Tieying Zhang（通讯作者）、Jianjun Chen、Rui Shi（ByteDance Inc）。脚注说明 Haoyang Li 的工作完成于在 ByteDance 实习期间。

**场合 / arXiv：** arXiv:2503.02240v2 [cs.CL]，2025 年 7 月 13 日。PDF 同时带有 PVLDB 参考文献格式：*Proceedings of the VLDB Endowment*，Vol. 18, No. 11，2025，ISSN 2150-8097；页码与 DOI 在文内仍是占位符 XXX-XXX 与 XX.XX/XXX.XX。许可为 CC BY-NC-ND 4.0。代码、数据与模型：https://github.com/RUCKBReasoning/OmniSQL 。

## 摘要 Abstract

Text-to-SQL 让非专家用自然语言查数据库。大语言模型把这项任务的成绩拉高了，但落到真实应用上仍有两处限制：靠提示调用闭源模型又贵又有隐私问题，也难以按需改；微调则受公开训练数据覆盖面限制，泛化差。本文提出一个可扩展的数据合成框架，在很少人工介入的情况下自动做出大规模、高质量、多样的 text-to-SQL 数据。由此得到 SynSQL-2.5M，作者称之为第一个百万级 text-to-SQL 数据集：约 250 万条样本，覆盖超过 16,000 个合成数据库；每条样本含数据库、SQL、自然语言问题和 chain-of-thought（CoT）解答。在这批数据上训练出开源模型 OmniSQL，有 7B、14B、32B 三档。

摘要所报的后文主结果是一句：在九个数据集上，OmniSQL 达到当时的最优，尽管参数更少，仍与包括 GPT-4o 和 DeepSeek-V3 在内的领先闭源、开源模型持平或超过它们。摘要未标表号。

## 1 INTRODUCTION

Text-to-SQL 把自然语言问题变成可执行 SQL，服务以数据为中心的应用，NLP 和数据库两边都在做。当时的领先方案常把任务拆给多个智能体，分别做 schema linking、生成、SQL 修正和 SQL 选择，其中生成仍是核心。生成有两条路：用精心提示调用闭源 API，或者在 Spider、BIRD 等已有数据上微调。前者费用高、有隐私顾虑，调用方也控制不了模型行为；后者难以泛化到复杂问题或特定领域的库，因为公开数据覆盖的真实场景有限。文中举例：在 Spider 和 BIRD 训练集上微调的 Qwen2.5-Coder-7B-Instruct，在分布相近的开发集上表现好，但在域外的 ScienceBenchmark 和 EHRSQL 上执行准确率只有 43.8% 和 31.4%；零样本提示 GPT-4-Turbo 则达到 59.2% 和 43.1%。作者认为，用大规模、多样、高质量的数据去加强开源模型，既能提高成绩和泛化，又能本地部署，从而更便宜、更利于数据安全、也更好改。人工标注做不到这个规模。早期数据增强大多让新样本贴近已有数据集的分布，多样性、质量和可扩展性都有限，而且常常要人去写复杂模板或语法。

本文的合成框架强调三点：全过程几乎不用人、能大规模覆盖很多领域、并且贴近真实用户。做法是把合成拆成几步，每步用大语言模型自动完成。第一步用网页表格合成数据库：给定一张表，模型推断一个说得通的业务场景，再生成带主外键的多张关系表；每张表包含表名、描述、列名、类型、列描述和两行示例。网上有数百万张网页表，所以领域可以铺开。第二步根据库信息生成有意义的 SQL。第三步用 back-translation 把 SQL 译回语义等价的自然语言问题；作者认为 SQL 到自然语言比反方向更准、歧义更少，因此合成的问题–SQL 对质量更有保证。第四步为每条样本写逐步的 CoT，说明从问题和库怎样推到这条 SQL，既便于解释，也给训练提供信号。为了贴近真实需求，SQL 复杂度分成 simple、moderate、complex、highly complex 四级，生成时先选定一级再让模型按该级来写。问题风格归纳出九种：formal、colloquial、imperative、interrogative、descriptive、concise、vague、metaphorical、conversational，翻译时指定一种风格。

用该框架得到的 SynSQL-2.5M 含 2,544,390 条样本、16,583 个不同的合成数据库，每条是 <database, question, SQL query, CoT solution>。作者称其多样性和复杂度高于已有 text-to-SQL 数据，并在数据库、问题、SQL 和整条样本四个维度上与人工标注的 BIRD 比较，几乎所有标准都更好。OmniSQL 在此基础上微调，规模为 7B、14B、32B，评测覆盖九个数据集：标准集为 Spider 的开发集与测试集、BIRD 开发集；领域集为 Spider2.0-SQLite、ScienceBenchmark、EHRSQL；鲁棒性集为 Spider-DK、Spider-Syn、Spider-Realistic。引言给出的结论是，OmniSQL 在这些数据集上的平均成绩达到当时最优，参数更少，仍与 DeepSeek-V3、Qwen2.5-72B-Instruct、GPT-4-Turbo、GPT-4o 持平或更好。贡献对应三块：自动且可扩展的合成框架；SynSQL-2.5M 与三个规模的 OmniSQL；以及用更少参数超过领先开源和闭源模型的 text-to-SQL 成绩。具体分数表在后文，引言未给表号。

## 2 RELATED WORK

2.1 把 text-to-SQL 的模型形态分成三段。早期工作用显式的编码器–解码器：编码器读入数据库 schema 和问题，解码器生成 SQL。有的工作给编码器加图关系信息，或借助预训练；有的给解码器加语法约束，以减少 SQL 语法错误。序列到序列模型兴起后，任务被转成 seq2seq，不少工作微调 T5。GPT-4、Gemini 这类大语言模型出现后，复杂任务又被拆成 schema linking、text-to-SQL 生成、SQL 修正和 SQL 选择，每个子任务由一个基于语言模型的智能体用提示或微调来做。本文不设计这种复杂的多智能体框架，而是用大规模合成数据加强其中的核心能力，也就是 text-to-SQL 生成。

2.2 数据增强用来补公开数据集覆盖不足，目标通常是多造一些符合原分布的 <question, SQL> 对。一条常见管道是 SQL-to-question：用 SQL 模板或语法先生成查询，再用神经网络译成自然语言。SQL 到自然语言较容易，合成对的质量较高。模板多从已有数据里抽，抽象语法树语法则要专家设计；前者限制多样性，后者费人工，都难以扩大规模。另一条是 question-to-SQL：先造问题，再用现成 text-to-SQL 模型译成 SQL，模型本身的错误会把噪声带进数据。还有工作用手工编写或从数据中抽出的问题–SQL 模板对，靠填槽生成新样本，多样性有限，问题也不自然。最接近的是 Sense：用精心设计的提示让 GPT-4 先生成数据库，再根据库写问题，最后写 SQL。依赖昂贵的 GPT-4，规模和成本都受限制。本文把合成拆成更简单、更可控的步骤，因此可以用较弱的开源模型，做到百万级仍然便宜；并且采用 SQL-to-question，避免 Sense 那种先有问题再补 SQL 时写错查询的风险。本文还会额外合成 CoT 解答。
