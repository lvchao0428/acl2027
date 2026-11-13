> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名：** WebReco-IRS2024-not-archival.pdf

**原文标题：** WebReco: A Comprehensive Overview of an Industrial-Scale Webpage Recommendation System at Bing

**作者：** Jaidev Shah、Iman Barjasteh、Amey Barapatre、Chuck Wang、Gang Luo、Rana Forsati、Jing Chu、Xugang Wang、Julie Fang、Fan Wu、Jiahui Liu、Xue Deng、Blake Shepard、Ronak Shah、Shaden Smith、Jon Soifer、Linjun Yang、Chuanjie Liu、Hongzhi Li、Rangan Majumder（Microsoft AI, USA）

**场合：** 3rd International Workshop on Industrial Recommendation Systems (at CIKM 2024)，IRS ’24，2024 年 10 月 25 日，Boise, ID, USA。ACM，11 页。首页 DOI 仍是占位符 https://doi.org/XXXXXXX.XXXXXXX 。未见 arXiv 号。

## 摘要

WebReco 是 Bing 里的网页级推荐。产品名是 Explore Further，出现在 Bing 搜索结果的第一页，目标是在搜索结果旁边给出有趣、能让人继续看、并且互补的网页。摘要先交代产品的 north star，也就是什么叫一条好的网页推荐，然后是评测方法，以及从候选生成到排序的整条线上系统。后面还会写特征工程与服务、模型怎么演进、组件如何撑住数十亿网页，以及一个 triggering 模型：在约束下动态决定这次该出几条推荐。摘要没有给具体效果数字。

## 1 Introduction and Product Overview

推荐是 query-agnostic 的：直接放在 Bing 搜索结果第一页，用来补充搜索体验，给出能让人继续浏览、互补、带探索性的网页，而不必绑在查询那一点很窄的意图上。作者称这是他们所知工业界最大的推荐系统之一，索引超过 2000 亿网页，两个主要界面每月服务数十亿次展示。Inline Scenario 放在前三条搜索结果下面，用户一打开结果页就能看到。Clickback Scenario 出现在用户点进某条结果、再回到 Bing 搜索标签之后，推荐和被点过的 URL 绑在一起。

后文用 URL1 指触发网页，也就是那条搜索结果，用 URL2 指被推荐的网页。好的 URL2 要可信，并且提供 URL1 内容之外的价值。最好的体验是三种之一：鼓励去看相关主题、给出可靠的另一种视角，或者提前碰到用户下一个信息需求。作者说，好推荐和坏推荐到底是什么，团队内部很难达成一致，但这件事很关键。Figure 1 把 north star 写成两栏。好的 URL2：与 URL1 相关、可信、提供可靠的替代信息或服务、预判下一步信息需求、在 URL1 内容之外增加价值、鼓励探索并制造 serendipity。坏的 URL2：不相关（主题不对、时间不对或地点不对）、和用户已经有的内容重复、低信任（例如有错误，或来自不可靠来源）、有害或垃圾（包括把推荐方的需求放在被推荐对象的需求之上）、以及过时内容。有了这张清单，他们才做了 RecoDCG：用大语言模型打分的推荐质量指标，提示词里写进产品目标，用来推动上线那些把产品往这个方向推的技术。

Figure 2 是 Inline 的一个例子。URL1 是 jainar.net 上关于 Jain Diet 的页面（耆那教起源于古印度）。Explore Further 里的 URL2 被用来说明多样性：“Jain Food Habits” 是另一份资料，“Jain Recipes” 预判感兴趣的人接下来可能要按饮食限制做菜，“Jain Dietary Practices: Unveiling Their Health Benefits” 则把话题引到这种饮食的健康收益。截图里还能看到 BBC 关于耆那僧侣饮食的报道，以及另一个 Jainworld 页面。本节收尾说，后文会按 Figure 3 把整条 web-scale 系统的演进讲完，包括指标、设计动机、上线模型、特征工程和在线特征服务。Figure 3 是生产系统总图；各模块的做法在第 3 节之后，这里不展开。

## 2 Evaluation: Offline and Online Metrics

### 2.1 Offline: RecoDCG

人工相关性和质量标注又贵又慢。作者引用已有结果，认为大语言模型可以当稳定的相关性评判，而且常常超过人工标注者。RecoDCG 用来评线上系统和新技术。核心是一个 pointwise 提示：URL2 作为 URL1 的推荐有多好。模型先分别看 topicality、location、authority 和 spam，再给 0 到 4 的质量分。提示在一套人工判定过的 URL1–URL2 质量集上调过、也对过。分数套进标准 DCG，差别只是相关标签来自语言模型而不是人工。测量集是从 Bing 历史查询来的几千个 URL1，覆盖多种市场和语言。对集合里每个 URL1，抓取线上服务排出的前 5 个网页，计算 RecoDCG@1、RecoDCG@3 和 RecoDCG@5。

### 2.2 Offline: ClickNDCG

ClickNDCG 是排序阶段点击预测模型的快速离线指标，被当作线上 CTR 的 inner-loop 代理。为了避开位置偏差和选择偏差，他们跑一个低流量在线实验：从排序候选里随机抽前 5 个 URL2，顺序也随机。只保留至少有一次 satisfied click（SAT）的日志。SAT 的启发式定义是停留超过 30 秒，表示信息需求被满足。算 NDCG 时，SAT 点击的相关分记为 100，其余为 0，这样指标比较好读。作者说实验表明它和线上 CTR 对齐，能反映出提升和回退。

### 2.3 Offline: Recall@k

这条指标评的是 Figure 3 里的 Collaborative Filtering（CF）召回路径。抽样一组能代表 WebReco 流量的 URL1，评测集用训练窗口之后 1 周的 Bing session 日志里的 co-occurrence clicks 来建；CoClick 的定义留在后文。作者认为，强的 CF 应当能泛化，在同一张 CoClick 图上，Recall@k 明显超过 CoClick 记忆路径。消融报告用 \(k \in \{30, 100\}\)。本节没有给出具体的 Recall 分数。

### 2.4 Online: Page Click Through Rate (PTR)

\[
PTR = \frac{\text{Impressions with at least 1 click on Explore Further}}{\text{Total Bing Impressions}}
\]

也就是：至少点过一次 Explore Further 的展示，除以全部 Bing 展示。

### 2.5 Online: Conditional Click Through Rate (CTR)

\[
CTR = \frac{\text{Impressions with at least 1 click on Explore Further}}{\text{Total Explore Further Impressions}}
\]

分母换成 Explore Further 自己的展示次数，所以这是在推荐已经出现的条件下的点击率。第 2 节到此结束。
