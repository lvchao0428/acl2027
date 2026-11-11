# Overview of the EHRSQL 2024 Shared Task on Reliable Text-to-SQL Modeling on Electronic Health Records

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`EHRSQL2024-shared-task_ClinicalNLP2024.pdf`。

## Abstract 摘要

电子健康记录（Electronic Health Records, EHRs）是关系数据库，存储医院内患者的全部病史。它们记录患者医疗照护的诸多方面，从入院和诊断到治疗与出院。尽管 EHR 是临床数据的重要来源，但要超出预定义查询集合去探索它们，需要 SQL 等查询语言的技能。为了让信息检索更容易获得，一种策略是构建问答系统，并可能借助 text-to-SQL 模型：这些模型能自动把自然语言问题翻译成相应的 SQL 查询，并用这些查询检索答案。EHRSQL 2024 共享任务旨在推进并促进如下研究：用 text-to-SQL 建模为 EHR 开发问答系统，使其能够可靠地向各类医疗专业人员提供所请求的答案，以改进其临床工作流程并满足其需求。在申请该共享任务的 100 余名参与者中，有八支队伍完成了全部流程，并展示了有效求解该任务的多种方法。本文描述可靠 text-to-SQL 建模这一任务、数据集，以及参与者的方法与结果。我们希望这一共享任务能激发进一步研究，并为开发面向 EHR 的可靠问答系统带来认识。

## 1 Introduction 引言

电子健康记录（EHRs）存储医院中发生的各类医疗事件，包括入院、诊断、操作、处方和出院。它们取代传统的纸质记录，并为患者数据提供集中式存储库。多年来，医院广泛采用 EHR 已被证明可以改善患者照护、提高效率，并增强医疗专业人员之间的协调（Upadhyay and Hu, 2022; Mullins et al., 2020; Uslu et al., 2021）。尽管 EHR 是有价值的患者数据来源，其数据结构的复杂性，以及抽取和分析信息所需的专门技能（例如 SQL 等查询语言），常常阻碍医疗专业人员有效利用它们（Wang et al., 2020; Lee et al., 2022）。这些障碍导致 EHR 在临床实践和研究中的全部潜力利用不足。

利用 EHR 中所存数据的另一种方式，是开发问答（question-answering, QA）系统。QA 系统提供用户友好的界面，使医疗专业人员可以用自然语言提问，并从 EHR 数据中获得相关答案，而无需了解查询语言或 EHR 数据库结构。具体而言，text-to-SQL 建模是为 EHR 构建 QA 系统的有效途径，因为 EHR 通常是关系数据库。这些模型自动把自然语言问题转换成相应的 SQL 查询，然后在数据库上执行这些查询以得到最终答案。随着大语言模型（large language models, LLMs）的显著进展，已提出多种高性能 text-to-SQL 模型，它们通过模型微调（Scholak et al., 2021）或带演示的 LLM 提示（Pourreza and Rafiei, 2024; Gao et al., 2023; Chang and Fosler-Lussier, 2023）来实现。如果以可靠的性能部署，这些模型可以让医疗专业人员通过自然语言交互更自由地探索 EHR 中的患者数据，从而显著受益。

已提出若干面向 EHR 问答的数据集，包括 MIMICSQL（Wang et al., 2020）、emrKBQA（Raghavan et al., 2021）和 EHRSQL（Lee et al., 2022）。EHRSQL 尤其提出了独特挑战。它是第一个汇编问题集合、以反映医疗专业人员多样需求的数据集，这些专业人员包括医生、护士和医院行政人员。它大量使用时间表达式，并包含复杂度更高的 SQL 查询，从而更好地反映医院场景的真实需求。这些 SQL 查询链接到两个开源 EHR 数据库，即 MIMIC-III（Johnson et al., 2016）和 eICU（Pollard et al., 2018），并把不兼容的问题作为数据集中的不可回答问题保留下来（用于测试模型弃答的能力）。SQL 查询依赖于数据库：即使一个问题试图检索相同的信息，该信息在不同数据库中的位置也可能不同。例如，要列出 MIMIC-III 中的全部药物，会使用 `SELECT drug FROM prescriptions`；而在 eICU 中则是 `SELECT drugname FROM medication`。

从他们收集的真实世界问题出发，本共享任务对 text-to-SQL 建模给出了更新的变化（使用 MIMIC-IV，并为问题提供新的改写），以及更具挑战性的问题设定（新的数据划分，以及额外的不可回答问题）。本共享任务的数据集公开于 https://github.com/glee4810/ehrsql-2024 。共享任务平台托管在 Codabench：https://www.codabench.org/competitions/1889/ 。本文在第 2 节和第 3 节分别介绍 EHRSQL 2024 共享任务及其数据集。第 4 节介绍该任务的评测指标和基线模型。第 5 节描述参赛队伍提出的方法，并讨论官方结果中的有趣发现。

图 1 的版面在抽取中有粘连。可辨认的问答与 SQL 如下；第二条 SQL 的两个 `strftime` 之间缺少运算符，标为【抽取不清】。

- 问题：What medication was last prescribed to patient 10027602? SQL：`SELECT drug FROM prescriptions WHERE subject_id = 10027602 AND starttime = (SELECT MAX(starttime) FROM prescriptions WHERE subject_id = 10027602);` 答案：Readi-cat 2 (barium sulfate 2% suspension)。
- 问题：Tell me the length of the last hospital stay of patient 10027602? SQL：`SELECT strftime('%J', admissions.dischtime) 【抽取不清】 strftime('%J', admissions.admittime) FROM admissions WHERE admissions.subject_id = 10027602 AND admissions.dischtime IS NOT NULL ORDER BY admissions.admittime DESC LIMIT 1;` 答案：21.1 days。
- 问题：What are the side effects of long term insulin administration? 标注为不可回答（Not answerable）。回答：I am not able to answer based on the EHR。

图注：图 1：EHR 上可靠 text-to-SQL 建模概览。对于任何输入问题，可靠的 text-to-SQL 模型应对自己能够回答的问题准确预测 SQL 查询，并对自己不能回答的问题弃答，例如本质上不可回答的问题，或模型很可能答错的问题。成功开发这样的模型，可以作为医院中医疗专业人员的有用工具，以更好地获取患者数据并辅助临床决策。

## 2 Task - Reliable Text-to-SQL Modeling 任务：可靠的 Text-to-SQL 建模

EHRSQL 2024 共享任务的目标，是为 EHR 开发可靠的 QA 系统，具体途径是 text-to-SQL 建模。可靠性对 AI 系统的部署至关重要，尤其是在医院这类关键领域，错误预测可能带来严重后果。问答中的可靠性一词，指系统宁可弃答，也不提供错误答案（Whitehead et al., 2022; Chen et al., 2023; Lee et al., 2024）。在本共享任务中，我们采用 TrustSQL（Lee et al., 2024）对可靠 text-to-SQL 的定义，它首先把可靠性的范围扩展到包括不可回答的问题。一个可靠的 text-to-SQL 模型不仅应正确生成 SQL 查询以提供效用，还应拒答那些很可能不正确或不可回答的问题，从而把伤害降到最低。这一目标与大多数其他 text-to-SQL 任务形成对照：那些任务的首要焦点只是最大化可回答问题上的 SQL 生成性能。关于衡量 text-to-SQL 可靠性的具体情形，进一步讨论见第 4.1 节。

图 2 为数据构建流程图，抽取到的节点包括：来自调查的问题语句（Question Utterances from the Poll），超过 200 名医院工作人员（>200 Hospital Staff）；EHRSQL（Lee et al., 2022）问题模板（Question Templates）；MIMIC-IV Demo；（面向 MIMIC-IV Demo 的问题, SQL）对；不可回答问题 + 取值抽样（Unanswerable Questions + Value Sampling）；使用 ChatGPT 的问题改写（Question Paraphrases Using ChatGPT）；SQL 标注（MIMIC-IV Schema）。图中箭头连接【抽取不清】。图注：图 2：EHRSQL 共享任务的数据构建过程。
