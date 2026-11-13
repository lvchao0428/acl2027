# Understanding the Effects of Noise in Text-to-SQL: An Examination of the BIRD-Bench Benchmark

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`Wretblad_BIRD-noise_ACL2024-short.pdf`。

## Abstract 摘要

Text-to-SQL 是把自然语言翻译成结构化查询语言（Structured Query Language, SQL），对于让不具备专业知识的人也能广泛访问结构化数据库至关重要。然而，为这类任务设计模型很困难，原因众多，其中包括“噪声”（noise）的存在，例如有歧义的问题和句法错误（syntactical errors）。本研究深入分析了广泛使用的 BIRD-Bench 基准中噪声的分布与类型，以及噪声对模型的影响。BIRD-Bench 的创建是为了刻画脏且带噪声的数据库取值，而不是为了在问题和标准 SQL 查询（gold SQL queries）中包含噪声与错误。我们发现，问题和标准查询中的噪声在数据集中很普遍，不同领域的数量不同，噪声类型的分布也不均衡。不正确的标准 SQL 查询会进而生成不正确的标准答案（gold answers），对基准的可靠性有显著影响。出人意料的是，在修正后的 SQL 查询上评测模型时，零样本基线（zero-shot baselines）超过了最先进提示方法（state-of-the-art prompting methods）的性能。我们的结论是：有信息量的噪声标签和可靠的基准，对于开发能够处理不同类型噪声的新 Text-to-SQL 方法至关重要。全部数据集、标注与代码见 https://github.com/niklaswretblad/the-effects-of-noise-in-text-to-SQL。

## 1 Introduction 引言

借助大语言模型的 Text-to-SQL 能够在不要求专业知识的情况下，让更多人访问结构化数据库。要开发这样的模型，高质量的开放数据集和基准是必不可少的资源；多年来已经建立了若干基准和数据集。早期基准，如 WikiSQL（Zhong et al., 2017），刻画的是简单场景，常常是单表查询；随后的数据集试图更接近真实世界场景：跨多张表、带连接语句（join-statements）的复杂查询（Yu et al., 2018），未见过的领域专用数据集（Gan et al., 2021b; Lee et al., 2021），以及带噪声的问题（Gan et al., 2021a）。BIRD-Bench 是一个新近且有难度的基准，旨在进一步缩小 Text-to-SQL 研究与真实应用之间的差距，例如包含大量且脏的数据库取值，并要求外部知识（Li et al., 2023）。

尽管 BIRD-Bench 并没有明确向数据中的问题引入噪声，噪声仍可能在数据集创建过程中因人为失误而被无意加入。出于同样的原因，噪声也是真实使用场景的一个基本方面，因为人类输入常常有歧义，并含有句法错误。然而，基准若要成为判断模型性质（例如噪声处理能力）的有用工具，数据必须有效，并告诉我们模型可以在哪些方面改进。

本文延续检视开放数据集与基准之适用性和局限性的传统。我们特别关注噪声如何体现在 BIRD-Bench 的问题和查询中。我们定性分析数据中存在哪些类型的噪声，以及特定领域中的噪声分布。然后，我们使用强基线和最先进方法，研究噪声对不同模型和提示技术的影响。

我们发现，问题和标准 SQL 查询中的噪声很普遍，噪声在各领域间分布不均，各类噪声在数据中的占比也不相等。标准 SQL 查询中的错误同样常见，并降低了 BIRD-Bench 的可靠性。在带有修正后标准查询的数据集上评测模型时，零样本基线与最先进提示技术之间的性能差距被抹平，这促使我们追问应当如何解释模型在 BIRD-Bench 上的性能。

图 1：一条不正确的 SQL 查询示例，它为给定问题生成了错误的标准参考答案。JOIN 操作错误地按 district_id 匹配客户与账户。由于同一地区可能有多个客户和多个账户，账户被错误地关联到了不对应的用户。图中文字按词拆行抽出，下列 SQL 由这些词按出现顺序还原。

问题：男性借款人的平均贷款金额是多少？（What is the average loan amount by male borrowers?）

不正确的标准查询（Incorrect Gold Query）：

```sql
SELECT AVG(T3.amount)
FROM client AS T1
INNER JOIN account AS T2
ON T1.district_id = T2.district_id
INNER JOIN loan AS T3
ON T2.account_id = T3.account_id
WHERE T1.gender = 'M'
```

修正后的查询（Corrected Query）：

```sql
SELECT AVG(T1.amount)
FROM loan AS T1
INNER JOIN account AS T2
ON T1.account_id = T2.account_id
INNER JOIN disp AS T3
ON T2.account_id = T3.account_id
INNER JOIN client AS T4
ON T3.client_id = T4.client_id
WHERE T4.gender = 'M'
```

## 2 Related Work 相关工作

**数据集（Datasets）。** WikiSQL 是一个大型 Text-to-SQL 数据集，只包含简单的 SELECT 和 WHERE 操作，没有嵌套查询或 JOIN 操作（Zhong et al., 2017）。SPIDER（Yu et al., 2018）后来被开发出来，以更接近真实场景，要求模型构造复杂查询并理解数据库模式（database schema）。复杂度是真实用例的关键方面，在此之外，SPIDER 的变体被创建出来，以包含带噪声的问题（Gan et al., 2021a）和领域专用问题（Gan et al., 2021b）。BIRD-Bench 的创建是为了缩小学术研究与真实应用之间的差距，做法是引入大量且脏的数据库取值、需要外部知识的问题，并优化 SQL 执行效率（Li et al., 2023）。

**Text-to-SQL 方法（Text-to-SQL Methods）。** 自动化系统（65.45%）与人类专家（92.96%）之间显著的准确率差距，突出了 Text-to-SQL 模型仍需持续发展。脚注 1：该数字取自截至 2024-02-16 的 BIRD-Bench 基准（https://bird-bench.github.io）。人们已经采取不同途径来构建能够生成 Text-to-SQL 的模型。较传统的做法是在 Text-to-SQL 例子上微调（finetune）大语言模型（LLMs）。这些模型给出了有希望的结果，但与指令微调的大语言模型（instruction-tuned LLMs），尤其是通过提示工程（prompt engineering）适配到 Text-to-SQL 任务的 GPT-4，仍有性能差距（Li et al., 2023）。提示常常被串联起来，每个提示作用于任务的子问题，例如模式链接（schema linking）、查询分解，以及对模型生成结果的修正（Pourreza and Rafiei, 2023a; Wang et al., 2023）。

**数据集中的噪声（Noise in Datasets）。** Wang et al. (2023) 与 Sun et al. (2024) 几乎同时期的工作表明，BIRD-Bench 中存在有歧义的问题和不正确的 SQL 查询。然而，与我们的工作不同，他们没有研究噪声如何随领域变化，也没有研究所识别的噪声和错误如何影响模型性能。Pourreza and Rafiei (2023b) 对不正确的 SQL 查询做了更细粒度的分析，但也提到了我们工作所覆盖的噪声类别（例如自然语言问题与数据库模式不匹配）。与他们的工作相对，我们对自然语言问题中的噪声做了更细粒度的分析，例如句法错误、同义词（synonyms）和有歧义问题的影响。

Katsogiannis-Meimarakis and Koutrika (2023) 指出，数据库模式常常与数据实体错位，这可能造成影响 Text-to-SQL 模型的词汇歧义或句法歧义。
