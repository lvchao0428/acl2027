> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名**：NoteLLM-2403.01744.pdf

**原文标题**：NoteLLM: A Retrievable Large Language Model for Note Recommendation

**作者**：Chao Zhang、Shiwei Wu、Haoxin Zhang、Tong Xu、Yan Gao、Yao Hu、Di Wu、Enhong Chen。Chao Zhang、Shiwei Wu、Tong Xu、Enhong Chen 署 University of Science and Technology of China 与 State Key Laboratory of Cognitive Intelligence；Haoxin Zhang、Yan Gao、Yao Hu、Di Wu 署 Xiaohongshu Inc.。Tong Xu、Enhong Chen 为通讯作者。

**场合 / arXiv**：WWW ’24 Companion（Companion Proceedings of the ACM Web Conference 2024），2024 年 5 月 13–17 日，Singapore。ACM ISBN 979-8-4007-0172-6/24/05，DOI 10.1145/3589335.3648314。同时为 arXiv:2403.01744v2 [cs.IR]，2024-03-25。

## 摘要

用户在社区里分享经历，形成 “notes”，把笔记推荐得贴合兴趣是关键任务。现有线上方法把整篇笔记送进基于 BERT 的模型，用 embedding 相似度找相关笔记，但 hashtag 和类别这类能代表笔记核心概念的线索用得不充分。生成 hashtag 或类别，和生成笔记 embedding 一样，都是把关键信息压进有限内容，所以学会生成标签有可能反过来提高 embedding。LLM 在自然语言上又明显强于 BERT。NoteLLM 用 LLM 做 item-to-item（I2I）笔记推荐：Note Compression Prompt 把一条笔记压成一个特殊 token，再用对比学习去靠近可能相关的笔记 embedding；同时用指令微调让模型概括笔记并自动生成 hashtag 或类别。作者称在真实场景里相对线上基线有效，并给 Xiaohongshu 的推荐系统带来主要提升。这两节没有给出具体提升幅度。

## 1 INTRODUCTION

Xiaohongshu、Lemon8 这类以用户生成内容为主的平台，鼓励用户写产品评价、旅行博客和生活经历，这些内容被叫做 notes。按偏好提供更个性化的笔记，是提高参与度的重要环节。I2I 笔记推荐是从百万级笔记池里找回用户可能感兴趣的笔记的经典做法：给定一条目标笔记，按内容或协同信号选出相关笔记。

线上 I2I 通常把整篇笔记送进基于 BERT 的模型得到 embedding，再按相似度推荐。hashtag 和类别只被当成正文的一部分。Fig. 1 用一条新加坡旅行笔记说明：`# Singapore` 这类标签概括的是笔记的中心意思，用来判断两条笔记是否相关。图注写的是从百万级笔记池里推荐相关笔记，并认为学习生成 hashtag 有利于 I2I。作者把生成 hashtag/类别和产出笔记 embedding 看成同一类压缩：都是把关键信息收进有限内容，因此学会生成标签有望提高 embedding 质量。LLM 在语言和推荐上能力强，但用在 I2I 推荐上的研究很少。

NoteLLM 是一个统一的多任务框架，让 LLM 同时学 I2I 笔记推荐和 hashtag/类别生成，用“抽出浓缩概念”来加强 I2I。每条笔记先做成统一的 Note Compression Prompt，再由预训练 LLM（例子是 LLaMA 2）解码：一个特殊 token 压缩笔记内容，并同时生成 hashtag/类别。相关笔记对来自用户行为：统计所有笔记对的共现分，每条笔记形成自己的共现分集合，取得分最高的笔记作为相关笔记。Generative-Contrastive Learning（GCL）把压缩 token 当作笔记 embedding，训练 LLM 从 batch 内负样本里认出相关笔记。Collaborative Supervised Fine-tuning（CSFT）则训练模型为每条笔记生成 hashtag/类别。两边都在抽笔记的关键概念，所以 CSFT 可以加强笔记 embedding。贡献有三条：据作者所称，NoteLLM 是第一个用 LLM 做 I2I 推荐的框架，说明引入 LLM 对 I2I 系统是可行且有前景的；用多任务同时学推荐和标签生成来加强 embedding，并表明学习生成压缩概念有利于 I2I；Xiaohongshu 的离线实验和线上工业场景用来证明有效。本节没有表格。问题定义与具体方法从第 3、4 节开始，此处不展开。

## 2 RELATED WORK

### 2.1 I2I Recommendation

I2I 根据目标物品，从大规模物品池给出一个排序列表。实现上或者预先建好 I2I 索引，或者在线用近似 k 近邻检索。传统 I2I 只靠用户行为里的协同信号，没有用户–物品交互时处理不了冷启动，因此有一批基于内容的 I2I 工作。本文关注文本 I2I：用文本内容衡量物品相似度。早期是基于词项的稀疏向量匹配；深度学习之后，神经网络更擅长表示文本，已有工作把文本映到同一潜空间，用 embedding 相似度衡量关系。LLM 能力突出，但用在 I2I 推荐上仍是空白。另有工作只把 LLM 当编码器来出 embedding，没有用上生成能力。NoteLLM 则让 LLM 生成 hashtag/类别，并以此来加强笔记 embedding。

### 2.2 LLMs for Recommendation

把 LLM 接进推荐被分成三条。第一条用 LLM 扩充数据：LLM 的世界知识使扩充后的数据比原始数据更突出、更多样，但测试数据要持续预处理才能和扩充后的训练数据对齐，而且高度依赖 LLM 的生成质量。第二条让 LLM 直接做推荐，靠专门提示或监督微调来回答问题；上下文长度有限，所以这些方法集中在重排阶段，候选只有几十个物品。第三条把 LLM 当编码器，为特定物品生成 embedding；能抽出信息，但丢掉了 LLM 的生成能力。NoteLLM 把 LLM 用在召回阶段，并学习 hashtag 生成，以提高产出 embedding 的能力。

### 2.3 Hashtag/Category Generation from Text

Hashtag 和类别是社交媒体上的标记，用来识别特定话题、帮助用户找主题内容。从文本生成它们，可以给没有标签的笔记补标识，或按偏好给用户提供选项。这一领域有三类方法。抽取式从正文里找关键短语当标签，拿不到原文里没有的标签。分类式把任务当成文本分类，但人写的 hashtag 多样、形式自由，效果容易不够好。生成式按输入文本直接生成 hashtag/类别，却只解决生成这一件事。NoteLLM 做多任务，同时执行 I2I 推荐和 hashtag/类别生成；作者认为两个任务相似，学会生成标签也能加强 I2I 推荐。本节没有表格，也没有实验数字。
