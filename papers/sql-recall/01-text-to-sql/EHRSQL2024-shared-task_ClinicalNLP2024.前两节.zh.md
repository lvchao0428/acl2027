> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名：** `EHRSQL2024-shared-task_ClinicalNLP2024.pdf`

**原文标题：** Overview of the EHRSQL 2024 Shared Task on Reliable Text-to-SQL Modeling on Electronic Health Records

**作者：** Gyubok Lee、Sunjun Kweon、Seongsu Bae、Edward Choi（KAIST AI）。

**场合：** Proceedings of the 6th Clinical Natural Language Processing Workshop，页 644–654，2024 年 6 月 21 日。

## 摘要

电子健康记录是医院里的关系数据库，从入院、诊断一直记到治疗和出院。要超出预设查询去翻这些数据，就得会 SQL。一种做法是做问答系统，用 text-to-SQL 把自然语言问题翻成 SQL 再取答案。EHRSQL 2024 共享任务要推进的是：给各类医护人员做一个可靠的 EHR 问答，既改善临床流程，也满足他们的实际需求。

报名超过 100 人，有 8 支队伍走完整个流程，方法差异很大。本文说明可靠 text-to-SQL 的任务定义、数据，以及参赛方法与结果。摘要只给出“8 支队伍、方法多样”这一句，没有印出分数，也没有指向表号。作者希望由此推动可靠的 EHR 问答。

## 1 Introduction

第 1 节先把 EHR 的价值和使用障碍放在一起。记录覆盖入院、诊断、操作、处方和出院，替代纸质病历，并被引用的工作认为有助于护理、效率和医护协作（Upadhyay and Hu, 2022; Mullins et al., 2020; Uslu et al., 2021）。障碍是结构复杂，抽取分析又要会 SQL，医护人员因此用不满（Wang et al., 2020; Lee et al., 2022）。问答系统让他们用自然语言提问、直接拿答案，不必懂查询语言或库结构。因为 EHR 通常是关系数据库，text-to-SQL 是合适的做法：先生成 SQL，再在库上执行。LLM 之后，高性能模型要么靠微调（Scholak et al., 2021），要么靠带示例的提示（Pourreza and Rafiei, 2024; Gao et al., 2023; Chang and Fosler-Lussier, 2023）。若可靠，医护就可以更自由地用自然语言探病人数据。

已有 EHR 问答数据包括 MIMICSQL（Wang et al., 2020）、emrKBQA（Raghavan et al., 2021）和 EHRSQL（Lee et al., 2022）。作者把 EHRSQL 的独特之处写成：第一次把医生、护士和医院行政人员的不同需求收成问题集；时间表达多；SQL 更复杂，更接近医院真实需求。查询连到两个开源库 MIMIC-III（Johnson et al., 2016）和 eICU（Pollard et al., 2018），对不上库的问题被留成 unanswerable，用来测模型会不会放弃回答。脚注强调 SQL 依赖具体库：同样是列出全部药物，MIMIC-III 是 `SELECT drug FROM prescriptions`，eICU 是 `SELECT drugname FROM medication`。这次共享任务相对 EHRSQL 的更新是：改用 MIMIC-IV，问题有新的改写；设定更难，包括新的数据划分和更多不可回答问题。数据在 `https://github.com/glee4810/ehrsql-2024`，平台是 Codabench 竞赛 1889。

图 1 把“可靠”画成三条路。能答的要写出可执行 SQL：病人 10027602 最后一次处方，答案是 Readi-cat 2（barium sulfate 2% suspension）；同一病人上次住院多久，用入院、出院时间差再取最近一次，答案是 21.1 天。不能答的要弃权，例如长期使用胰岛素的副作用，系统应表明无法根据 EHR 回答。图注的定义是：能答的准确预测 SQL，不能答的放弃，包括本质上不可回答的问题，以及模型很可能写错的问题。第 1 节末尾说明后文安排：第 2、3 节分别是任务和数据，第 4 节是指标与基线，第 5 节是参赛方法与官方结果。成绩表不在前两节，这里不展开。

## 2 Task - Reliable Text-to-SQL Modeling

第 2 节很短，只定义任务，不讲数据怎么造。目标是用 text-to-SQL 做可靠的 EHR 问答。可靠性被放在医院这个高风险场景里：预测错了后果严重。问答里的 reliability 沿用已有说法，指系统宁可放弃，也不要给错误答案（Whitehead et al., 2022; Chen et al., 2023; Lee et al., 2024）。

本任务采用 TrustSQL（Lee et al., 2024）里 reliable text-to-SQL 的定义，并指出该工作第一次把可靠性扩到不可回答的问题。因此模型要同时做到两件事：对能答的问题正确生成 SQL，这是效用；对很可能答错或根本不可回答的问题放弃，这是把伤害压到最小。这和其他大多数 text-to-SQL 任务相反，那些任务只追求在可回答问题上把 SQL 生成做高。如何在具体情形里度量这种可靠性，正文指到第 4.1 节，第 2 节没有公式、表或数字。数据构建从第 3 节 Dataset Construction 起。
