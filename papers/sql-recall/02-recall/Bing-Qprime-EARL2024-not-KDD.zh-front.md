> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文标题：** Leveraging LLMs to Enhance a Web-Scale Webpage Recommendation System

**作者：** Iman Barjasteh、Jaidev Shah、Amey Barapatre、Rana Forsati、Gang Luo（首页星号标明这五人同等贡献），以及 Fan Wu、Julie Fang、Xue Deng、Blake Shephard、Ronak Shah、Linjun Yang、Hongzhi Li、Rangan Majumder。单位为 Microsoft AI, USA。

**场合：** EARL '24: Workshop on Evaluating and Applying Recommendation Systems with Large Language Models at RecSys '24（2024 年 10 月 14–18 日，Bari）。首页 ACM 引用写明收录于该 workshop proceedings，全文 10 页。

**PDF：** `Bing-Qprime-EARL2024-not-KDD.pdf`

## Abstract

摘要把一件已经上线的产品和四件要做的事绑在一起。产品是 Bing 搜索结果页上的 Explore Further：围绕搜索结果里的网页 URL，再推荐能让人继续看下去的网页。技术主张分四层。第一，做出并验证由 LLM 驱动的离线推荐质量指标 RecoDCG。第二，用 LLM 产生的质量信号，让排序阶段对质量敏感。第三，在候选生成里加一条叫 Q' recall 的召回路径，用 LLM 补出与现有候选互补、又值得点开的网页。第四，把推荐质量和点击指标放进同一个多目标优化里权衡。作者声称这套改动已经进生产，推荐质量有显著提升，后文会给离线与在线实验，以及为了 web-scale 落地做过的取舍。摘要里没有报具体涨幅、表号或线上指标数值。

## 1 Introduction

第 1 节先把产品约束和标注困难说清楚，再把 LLM 放进来当质量杠杆。Explore Further（Figure 1）挂在 Bing 搜索结果页上，给出的网页推荐既不看当前 query，也不看具体用户。系统被写成工业界规模最大的一类：总索引超过 200 billion 个网页。

论证的核心困难是标签。大规模、内容还在不断变化的推荐系统，训练和评估都需要可靠的质量与相关性标签。人工判断质量较高，但贵、慢，而且不稳定，撑不住只靠人标。工业界因此大量使用点击一类隐式反馈。作者沿用文献里的判断：过分追点击，系统会偏向 clickbait 和低质内容。网页推荐把这个问题放大了，因为全网文档质量差得很大。他们自己的系统历史上主要靠用户交互和行为信号训练；Bing 用户针对这个功能提交的不满里，反复出现 clickbait 和低质网页。索引大到无法逐页人工把关入库内容，于是存在把垃圾、标题党和不当网页推出去的风险。

转折用的是 LLM 已经表现出来的能力：理解用户意图，并抓住意图与文档内容之间的语义关系；已有工作还表明，LLM 能较准确地把握搜索者偏好，并生成高质量相关性标签。据此他们做了 RecoDCG，一种 LLM 驱动的离线推荐质量指标，用来快速比较新技术；质量标签再被送进排序，使排序阶段变成 quality-aware。

节末只交代后文分工：先概述生产中的 webpage-to-webpage 系统，并给出他们做 RecoDCG 的流程；质量感知排序放到 Section 4，用 LLM 生成互补候选放到 Section 5。这一节没有表，也没有实验数字。Figure 1 的图注只说明：触发页 URL1 下方是 Explore Further 生成的网页推荐。

## 2 System Overview

第 2 节把线上系统拆成「只看触发页的召回」和「两层排序」，并给后文要改的接口命名。产品目标是：对出现在搜索结果前 3 个位置的 URL，推荐有趣、互补、相关的文档。作者认为好的推荐应落在三种用途之一：接住用户的下一个查询意图，给出另一种视角，或引出与触发页相关的探索性话题。

两个贯穿后文的称呼在这里定义。URL1 是主触发网页，URL2 是一条推荐候选。Figure 1 里的例子是 cheatsheet.md 作为 URL1，Explore Further 下列出的网页作为 URL2。推荐只依赖 URL1，与用户身份和搜索 query 都无关。

召回阶段从 Bing 索引里取相关候选。本节开头把索引写成 several hundred billion 篇 web documents；到 2.1 又写成 200 billion webpage index。引言里的说法是 over 200 billion webpages。三条已有召回路径是 co-click、collaborative filtering，以及 two-tower embedding；第四条是本文将在 Section 5 展开的 LLM 召回。Figure 2 是系统图：候选先汇总，再送进两层排序。

### 2.1 Candidate Generation Stage Overview

生产系统有多条候选生成器，文中称为 recall paths。每条路径从约 200 billion 的网页索引里产出预定数量的候选，汇总、去重后再进入排序。

co-click（co-occurrence click）的定义是：多个 Bing 用户浏览会话里，两张网页都被点击过，因此认为它们有一定相关度。用这份共现点击建图之后，collaborative filtering 在数十亿网页的规模上学网页嵌入。

另一条是 two-tower、6-layer 的 XLM-Roberta。标签来自点击日志；每个塔输入 URL 及其配套文本特征。推理时，给定触发页 URL1，collaborative filtering 和 two-tower 两条路径都用 embedding cosine similarity 做 Approximate Nearest Neighbor（ANN）检索。

本节新引入的是 LLM 驱动的 Q' recall，目标是为数亿级 URL1 生成多样且互补的候选。具体生成方式留到 Section 5，这里只标明它和共现、协同过滤、双塔检索是并列的一条召回路径。

### 2.2 Ranking Stage Overview

排序按固定顺序分成四步，其中后三步都属于第二层内部：

1. Stage 1：LightGBM。特征少、计算便宜，主要是不同时间窗上的 URL1–URL2 点击数和曝光数。
2. Stage 2.a：MT RecoLM。多任务 cross-encoder，两个头分别训练 pairwise click prediction 和 recommendation quality。
3. Stage 2.b：另一层 LightGBM。特征更多、更贵，其中包含 cross-encoder 各头的分数；优化目标是 pairwise click prediction，文中标为 LTR。
4. Stage 2.c：把 Stage 2 的 LightGBM 分数与推荐质量头的分数做线性组合。

质量感知排序的训练、蒸馏和权重选择都放到 Section 4。第 2 节没有表。索引规模、搜索结果前 3 位、6-layer XLM-Roberta、数十亿网页上的 collaborative filtering，以及数亿级 URL1，是这两节里已经印出的关键数字。线性组合的权重和任何 RecoDCG、点击涨幅都还没出现。

本文覆盖摘要、Section 1 Introduction，以及 Section 2 System Overview（含 2.1、2.2）。Section 3 起的 RecoDCG 定义与实验不在本导读内。
