> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文标题：** REGEN: A Dataset and Benchmarks with Natural Language Critiques and Narratives

**作者：** Kun Su、Krishna Sayana、Hubert Pham、James Pine、Yuri Vasilevski、Raghavendra Vasudeva、Marialena Kyriakidi、Ambarish Jash、Anushya Subbiah、Sukhdeep Sodhi（Google Research），Liam Hebert（University of Waterloo）。前五位同等贡献。

**场合：** 预印本，arXiv:2503.11924。页眉是 ACM 模板占位 “Conference acronym ’XX”，没有可引用的会议名。

**PDF：** `regen-2503.11924.pdf`

## Abstract

摘要认为对话推荐既要给出下一个物品，也要给出自然的解释，并允许用户用话把推荐拧向另一个方向。Amazon 评论只有一条条交互，没有这种对话。REGEN 用语言模型把缺的话语补上：用户短评表示「把当前推荐导向另一件物品」，叙事则是较长的推荐说明。数据落在 Office 和 Clothing 两类评论序列上。摘要的主张是，联合做生成式推荐和语言任务时，表现可以接近当时的推荐器和语言模型；模型能学会写跟上下文贴合的叙事，并用短评动态引导推荐，还能生成连贯的对话轨迹。

## 1 Introduction

第 1 节把缺口写成：序列推荐预测下一件物品，但解释和用户修正通常不在同一条数据里。评论能提供偏好文本，却不是对话，也没有「用户听到推荐后要求改一改」这种回合。作者因此不收集新的真人对话，而是在已有评论序列上补写短评和叙事，使同一条序列既能做下一物品，也能做语言生成。

贡献在节末收成数据、任务和模型三块。数据是带短评和叙事的开放序列。任务同时包含下一物品、带短评的下一物品，以及物品加叙事的联合生成。模型侧提出 LUMEN，用 LLM 同时吃历史、短评并生成推荐与叙事。这一节没有给出 Office 或 Clothing 的用户数、物品数，也没有 Recall 表。具体生成规则留在第 3 节：短评只加在类目层级足够接近的相邻物品上，而且生成时第二件被指定为目标。

## 2 Related Work

第 2 节按数据形态和任务形态各写一组，用来说明 REGEN 补的是「叙事和历史序列绑在一起」，不是再收一套电影对话。

**2.1.1 Conversational。** DuRecDial、E-ConvRec、ReDial、TG-ReDial、E-Redial 收集或构造对话，但对话和用户历史偏好往往没有绑紧。LLM-Redial 用真实用户画像和模板造对话，和 REGEN 一样关心画像与文本一致。差别有两条：REGEN 保留按时间排的物品序列，短评和叙事以过去行为为条件；REGEN 要的是较长的个性化叙事，不是短对话回合。

**2.1.2 Narratives。** Ni 等和 Chen 等从评论生成购买解释。作者把 Amazon-C4 写成用评论构造复杂查询、再关联到物品的检索数据。REGEN 的延伸是：叙事更开放，以整段用户历史为条件，用途不限于解释一次购买。

**2.1.3 Critiquing。** 经典批判式推荐允许用户在特征层修改推荐，后来的工作把关键短语放进隐空间，用来推动推荐改变。这些工作被当成「用自然语言短评当用户反馈」的前身。

**2.2 Recommendation Tasks。** 序列推荐一节把 LLM 与推荐的结合收成一大组文献，差别在于物品用 ID 还是文本嵌入。作者把自己的位置放在：既保留序列推荐的下一物品标签，又让短评和叙事进入同一条训练。实验数字不在第 2 节。
