# WebReco: A Comprehensive Overview of an Industrial-Scale Webpage Recommendation System at Bing

> 版权声明：本文档为同目录英文论文「摘要与正文前两节」的中文译文，仅供论文快速阅读与选题使用。译文不替代原文，不用于发表、再分发或商业用途。版权归原作者及出版方所有。原文件：`WebReco-IRS2024-not-archival.pdf`。

## Abstract 摘要

本文介绍 WebReco，即 Bing 中的一个网页规模的网页推荐系统。该产品以 Explore Further 的形式出现在 Bing 搜索结果的首页，用于在搜索结果旁边提供有趣、吸引人且互补的网页推荐。我们首先概述产品的北极星目标，界定对本产品而言何谓一条好的网页推荐。我们描述评估方法，并全面概述生产推荐系统，从候选生成到排序逐一说明每个组件。我们深入特征工程与在线服务、模型开发与演进的具体细节，以及如何把各组件扩展到处理数十亿网页。我们还分享构建推荐触发模型的方法：在给定约束下动态决定推荐条数。本文详细展示如何构建并优化一个网页规模的推荐系统，并突出我们所做的设计选择。

## 1 Introduction and Product Overview 引言与产品概览

我们的产品在 Bing 搜索结果首页直接提供与查询无关的网页推荐。我们的目标是增强 Bing 用户的搜索体验，提供吸引人、互补且具有探索性的网页推荐，这些推荐并不必然绑定于查询的狭窄意图。据我们所知，我们构建了业界最大的推荐系统之一，索引总量超过 200 billion 个网页。我们每月在两个主要推荐场景上提供数十亿次曝光：

1. Inline Scenario：显示在前三条搜索结果下方，当用户查看初始搜索结果页时出现这些推荐。
2. Clickback Scenario：当用户点击某条搜索结果后返回 Bing 搜索标签页时展示，提供与被点击 URL 相关联的额外网页建议。

我们在图 1 中勾勒产品的北极星，即我们希望为 Bing 用户带来的价值。本文中，我们用 URL1 表示触发网页（搜索结果），用 URL2 表示一条网页推荐。一条好的网页推荐既值得信任，又能提供超出 URL1 内容的额外价值。最好的推荐体验，来自这样的网页：它们要么鼓励探索相关主题，要么提供可靠的另一种视角，要么能够预判用户的下一个信息需求。明确表述什么构成好的、什么构成坏的网页推荐，很难达成共识，但这至关重要。有了明确的产品北极星，我们才能构建 RecoDCG，这是一种由 LLM 驱动的推荐质量指标，其提示把产品目标写入了打分指令。LLM 使我们能够构建一个捕捉产品北极星的指标，从而推动团队把使产品朝正确方向移动的技术投入生产。

在图 2 中，关于 “The Jain Diet” 的 jainar.net 网页是 URL1，Explore Further 下方的网页推荐称为 URL2。作为背景，耆那教（Jainism）是起源于古印度的一种宗教。在这个例子中，系统生成一组多样的推荐：“Jain Food Habits” 网页作为替代资源；“Jain Recipes” 网页预判了那些有兴趣按饮食约束准备餐食的用户很可能随后产生的意图；“Jain Dietary Practices: Unveiling Their Health Benefits” 网页则为用户提供探索另一侧面的机会，具体是该饮食的健康益处。

图 1：网页推荐的产品北极星（Product North Star）。

在本工作中，我们全面概述网页规模推荐系统的开发与演进，如图 3 所示。我们对端到端系统做深入介绍，包括指标、设计选择背后的动机、所部署的模型、特征工程，以及用于在线特征服务的数据流水线与机制。

图 2：Inline Scenario。

## 2 Evaluation: Offline and Online Metrics 评估：离线与在线指标

### 2.1 Offline: RecoDCG 离线：RecoDCG

来自人工评测员的相关性与质量标签既昂贵又缓慢。已有工作表明，LLM 是强且一致的相关性评判者，常常优于人工标注者 [15]。为了提高实验敏捷性并形成质量信号，我们开发了一种由 LLM 驱动的推荐质量指标，称为 RecoDCG，用于评估生产系统与新技术。该指标的核心是一个逐点打分提示，回答“URL2 作为 URL1 的推荐有多好”这一问题：它先对各个推荐侧面（topicality、location、authority 和 spam）进行推理，再确定一个从 0 到 4 的推荐质量分数。该提示对照一个由人工评判的 URL1–URL2 质量评估集进行调优和评估，以确保提示准确衡量推荐质量。

RecoDCG 基于标准的折扣累计增益（Discounted Cumulative Gain, DCG）公式，关键区别在于用大语言模型（Large Language Model, LLM）生成的逐点推荐质量分数作为相关性标签。作为 RecoDCG 的测量集，我们使用从 Bing 用户历史查询中得到的、由数千个 URL1 组成的多样集合。该集合的构造足以充分代表广泛的市场和语言。我们对评估集中的每个 URL1 抓取生产服务排序最高的 5 个网页，并计算 RecoDCG@1、RecoDCG@3 和 RecoDCG@5。

### 2.2 Offline: ClickNDCG 离线：ClickNDCG

为便于在排序阶段快速离线评估点击预测模型，我们使用一个称为 ClickNDCG 的离线指标。该指标充当在线点击率（click-through rate, CTR）的离线代理，因此我们把它称为内环指标（inner-loop metric）。

为收集不受位置偏差或选择偏差影响的日志，我们运行一个低流量的在线实验：从排序阶段的候选中随机选择前 5 个 URL2 展示给用户，顺序也随机。我们保留至少有一次满意点击（satisfied click, SAT click）的日志；满意点击定义为用户的信息需求得到满足的点击。作为启发式，我们把停留时间超过 30 秒的点击视为 SAT 点击。我们计算 NDCG，对满意点击赋予相关性分数 100（以便指标易于解释），否则为 0。实验表明，ClickNDCG 与生产系统的在线 CTR 高度一致，能够准确反映提升或回退。

图 3：生产系统概览。

### 2.3 Offline: Recall@k 离线：Recall@k

为评估图 3 所示的协同过滤（Collaborative Filtering, CF）召回通路，我们报告 Recall@k。我们抽样一组固定的、能代表 WebReco 流量的 URL1，并通过收集训练数据窗口之后 1 周时间范围内、来自 Bing 会话日志的共现点击（co-occurrence clicks，详见 Section 3.1）来构造评估集。一个强的 CF 实现应当能够泛化，并得到明显优于同一 CoClick 图上 CoClick 记忆通路的 Recall@k。我们用 \(k \in \{30, 100\}\) 报告消融。

### 2.4 Online: Page Click Through Rate (PTR) 在线：页面点击率（PTR）

\[
PTR = \frac{\text{Impressions with at least 1 click on Explore Further}}{\text{Total Bing Impressions}}
\]

### 2.5 Online: Conditional Click Through Rate (CTR) 在线：条件点击率（CTR）

\[
CTR = \frac{\text{Impressions with at least 1 click on Explore Further}}{\text{Total Explore Further Impressions}}
\]
