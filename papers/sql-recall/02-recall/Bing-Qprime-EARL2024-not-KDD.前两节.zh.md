> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名：** `Bing-Qprime-EARL2024-not-KDD.pdf`

**原文标题：** Leveraging LLMs to Enhance a Web-Scale Webpage Recommendation System

**作者：** Iman Barjasteh、Jaidev Shah、Amey Barapatre、Rana Forsati、Gang Luo（同等贡献），以及 Fan Wu、Julie Fang、Xue Deng、Blake Shephard、Ronak Shah、Linjun Yang、Hongzhi Li、Rangan Majumder（Microsoft AI, USA）

**场合：** 本地文件名标明 EARL 2024，不是 KDD。首页场合以 PDF 为准。

## 摘要（Abstract）

Explore Further @ Bing 是网页到网页的推荐：在搜索结果 URL 旁边给出能吸引人的相关网页。文章用 LLM 改这套网络规模系统，分三块。RecoDCG 是 LLM 驱动的推荐质量指标，并做了验证。排序阶段用 LLM 变成质量感知。Q' recall 是一条新召回，让 LLM 生成互补、能吸引用户的候选。系统还要在推荐质量和点击之间做多目标平衡。工作已上线，摘要只说推荐质量明显提高，并会给出离线和在线结果，以及为了扩到网络规模做了哪些事。具体数字不在摘要里。

## 1 Introduction

Explore Further 在 Bing 搜索结果页上，推荐与查询、与用户都无关，只跟触发网页有关。索引超过 2000 亿个网页。大规模系统缺的是可靠的质量与相关性标签：人工标签贵、慢、不稳定，撑不起持续变化的索引，训练和评估都如此。

点击这类隐式反馈被很多产品拿来优化，但过拟合点击会偏向标题党和低质量页。这个系统历史上主要用交互和行为信号训练，用户不满意反馈里反复出现的也是标题党和低质推荐。索引大到无法逐页审核，有把垃圾、标题党甚至不当页面推出去的风险。作者引用近期工作，认为 LLM 能理解搜索意图和文档的语义关系，也能给相关性打出高质量标签。因此先做离线指标 RecoDCG，用来快速试新技术，再用这些质量标签改排序。正文路线是：先讲生产系统，再讲 RecoDCG 的做法；质量感知排序在第 4 节，LLM 互补候选在第 5 节。

## 2 System Overview

产品目标是：针对搜索结果前 3 个 URL，给出有趣、互补、相关的文档。好的推荐要么接住用户的下一次查询意图，要么给一个替代视角，要么引出和触发页相关的探索主题。触发页叫 URL1，候选叫 URL2。图 1 里 cheatsheet.md 是 URL1。推荐不看用户，也不看查询。召回从数千亿网页里出候选，路径包括共点击、协同过滤、双塔嵌入，以及第 5 节的 LLM 通路。候选聚合后进入两层排序（图 2）。

### 2.1 Candidate Generation Stage Overview

每条召回路从约 2000 亿网页里按配额出候选，进排序前聚合去重。共点击指多个 Bing 浏览会话里两个网页都被点过。在这个共点击图上，协同过滤在数十亿网页规模学习嵌入。另一条是 6 层 XLM-Roberta 双塔，用点击日志做标签，每塔吃 URL 和相关文本。对 URL1 推理时，协同过滤和双塔都按余弦相似度做近似最近邻。新的 Q' recall 用 LLM 为数亿个 URL1 生成更多样、更互补的候选，细节在第 5 节。

### 2.2 Ranking Stage Overview

排序按顺序四段。（1）阶段 1：特征较少、成本低的 LightGBM，主要是不同时间窗口上 URL1–URL2 的点击和曝光计数。（2）阶段 2.a：MT RecoLM，多任务交叉编码器，两个头分别做配对点击预测和推荐质量。（3）阶段 2.b：特征更多、更贵的 LightGBM，输入里包括交叉编码器各头的分数，按配对点击的 LTR 目标优化。（4）阶段 2.c：把阶段 2 的 LightGBM 分数和推荐质量头的分数线性组合。质量感知排序的展开在第 4 节。
