> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名：** `EHRSQL_NeurIPS2022.pdf`

**原文标题：** EHRSQL: A Practical Text-to-SQL Benchmark for Electronic Health Records

**作者：** Gyubok Lee、Hyeonji Hwang、Seongsu Bae、Yeonsu Kwon、Woncheol Shin、Seongjun Yang、Minjoon Seo、Jongyeup Kim、Edward Choi。Lee、Hwang、Bae、Shin、Yang、Seo、Choi 来自 KAIST；Kwon 来自 Seoul Women’s University；Kim 来自 College of Medicine, Konyang University。

**场合：** 36th Conference on Neural Information Processing Systems (NeurIPS 2022) Track on Datasets and Benchmarks。

## 摘要

EHRSQL 是面向电子健康记录的 text-to-SQL 数据集。问句来自 222 名医院人员，包括医生、护士、保险审核和病案团队等。做法是在一家大学医院做问卷调查，把回答收成种子问题模板，再人工连到两个开源库 MIMIC-III 和 eICU；问卷里的各种时间表达，以及留出的不可回答问题，也进了数据集。

作者把难度收成三条：SQL 要覆盖医院里从简单检索到计算生存率这类复杂操作；要听懂医疗场景里对时间敏感的多种说法；还要根据预测置信区分问题能不能答。他们把 EHRSQL 定位成结构化 EHR 问答的实用基准，用来缩小 text-to-SQL 研究和医院真实部署之间的距离。数据在 `https://github.com/glee4810/EHRSQL`，按 CC BY-SA 4.0 发布。摘要没有指向表号。

## 1 Introduction

第 1 节先写 EHR 是什么：医院里记录病人全部病史的关系数据库，从入院、治疗到出院，形式包括表、文本和图像。医生、护士和行政人员不断往里存、从里面取，用来做临床决定。现状是大多数人只能用预先写好的规则转换系统；想超出规则，就要专门培训才能改系统。作者把这看成充分利用 EHR 的瓶颈。替代方案是把问题直接翻成 SQL：用户打字或口头提问，系统返回答案。这样检索会快很多。

已有的结构化 EHR 问答数据是 MIMICSQL 和 emrKBQA。前者是 MIMIC-III 上第一个此类数据，问题由预定义模板自动生成；后者从临床阅读理解数据 emrQA 改到 MIMIC-III。作者说，大学医院的问卷表明这些数据离真实工作需求还差得远。EHRSQL 因此被定义成连到 MIMIC-III 和 eICU 的大规模 text-to-SQL 数据，并且据作者所知是第一个既反映医院人员多样需求、又把部署时的实际问题放进来的 EHR 问答数据。

三条挑战在第 1 节展开。问题范围：问卷收集人们经常对结构化 EHR 提的问题，有效受访者 222 人，从业年限不同，人口统计见图 1（按科室和年限，图本身没有抽出具体比例）。过滤、模板化之后，既有取生命体征、住院费用这类病人记录，也有群体操作，例如诊断后开得最多的前 N 种药，以及 N 年生存率。时间：医院问题里时间表达很多，因为时间是医疗的关键维度。他们把时间分成表达类型（绝对、相对、混合）、单位（如住院、月、日）和区间类型（since、until、in），再嵌进问题模板；细节指向第 3.1.2 节。可信问答：系统只应返回准确答案，超出能力就拒绝。不可回答的问句来自问卷里剩下的话，原因是和库 schema 不相容，或者需要外部领域知识。表 1 给出样例，SQL 会按 MIMIC-III 和 eICU 两套 schema 分别标注：

| 类型 | 样例问题 | 科室 |
| --- | --- | --- |
| 人口统计 | 病人 92721 的出生日期 | Nursing |
| 处方 | 病人 20000 第一次处方时间 | Nursing |
| 生命体征 | 病人 23042 最后一次动脉收缩压 | Physician, Nursing, Health records, Other |
| 费用 | 涉及 non-invasive mech vent 的平均总住院费用 | Insurance review |
| 生存率 | 四年生存率最低的五种诊断 | Nursing |
| 纵向统计 | 被诊断为 hypotension、no earlier since 2104、2 个月内最常开的五种药 | Physician, Nursing |
| 绝对时间 | 病人 2518 在 2105-12-31 12:00:00 的心率是否低于当天 09:00:00 | Physician |
| 绝对时间 | 病人 51177 在 10/2105 的最后一项标本检查 | Nursing |
| 相对时间 | 病人 6990 上次 ICU 住院期间胃药的日均摄入 | 表中科室为 “-” |
| 混合时间 | 病人 3929 在今年 5 月第一次被开的药 | Nursing |
| 不可回答（要外部知识） | 腿部对比动脉造影治疗期间不该用的药名 | Nursing |
| 不可回答（超出 schema） | 病人 73652 下一次最早的住院是什么时候 | Nursing |

纵向统计那一行原文在换行处粘连，读作 “hypotension no earlier since 2104 within 2 months”。

## 2 Related Works

第 2 节分三块：EHR 问答、语义解析数据、问答里的不可回答问题。落点是 EHRSQL 的问题来自真实问卷，而且同时做语义解析和可靠性，不是只在可回答问题上把 SQL 做高。

**EHR QA。** emrQA（Pampari et al.）根据医生常问的问题，做临床笔记上的问答。emrKBQA（Raghavan et al.）把它改到 MIMIC-III 的结构化病人记录上；因为原数据面向门诊，问题大多停在化验结果，而且本文写作时尚未公开。MIMICSQL（Wang et al.）第一次把 EHR 问答做成 text-to-SQL：按规则自动出题，再众包过滤。作者批评它问题范围窄，SQL 简单，而且只限制在五张表上，离医院实际用法远。对照句是：EHRSQL 来自真实问卷，覆盖经常被问到的现实问题，平均涉及 13.5 张表，并回指表 1。

**Semantic parsing datasets。** 语义解析把话转成可执行的逻辑形式，如 Python 或 SQL。WikiSQL 领域广，来自维基 HTML 表，但 SQL 简单、且是单表。Spider 要处理连接、集合运算，以及多表、多领域。更接近实用的近作里，KaggleDBQA 用 Kaggle 上的真实库，问题按领域来写，而且出题时不依赖数据库 schema；SEDE 处理 Stack Exchange 用户真实会问的复杂 SQL。作者说动机与它们一致：真实场景，这里是医疗问答，会多出学术设定里没有的困难。

**Unanswerable questions in QA。** 早期不可回答问题靠远监督、规则改写，或众包对抗来造。语义解析里多数工作假设每道题都有效、都能答，实际并非如此；为了系统可靠，也不该对所有输入都返回答案。Zhang et al. 用其他 text-to-SQL 和闲聊数据造不可回答问题，并把任务做成分类。EHRSQL 的差别是同时处理可靠性和语义解析，不可回答问题是问卷里自然收集的，不是另造的。任务型对话里同类问题叫 Out-of-Domain 检测，有些工作出于实用考虑，训练时不把 OOD 样本明示给模型。本文沿用这一设定：不可回答问题只放在验证集和测试集。第 2 节到此结束。问卷规模、模板数量和库的预处理从第 3 节 Dataset Construction 起，此处不展开。
