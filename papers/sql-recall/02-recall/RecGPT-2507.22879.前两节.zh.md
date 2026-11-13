> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名**：RecGPT-2507.22879.pdf

**原文标题**：RecGPT Technical Report

**作者**：首页署 RecGPT Team。PDF 文档属性里另有一长串个人姓名，首页没有逐一印出。

**场合 / arXiv**：首页版权为 © 2025 Taobao。未见会议名称。arXiv:2507.22879v2 [cs.IR]，2025-07-31。

## 摘要

原文没有单独的 Abstract 标题，下面概括首页开篇。工业推荐被写成连接用户、商家和平台的基础设施，但多数系统仍按历史共现和 log-fitting 来优化，只拟合过去的交互、不显式建模用户意图，于是过拟合狭窄的历史偏好，抓不住变化中的和潜在的兴趣，并强化 filter bubbles 与长尾现象。RecGPT 把用户意图放进推荐流水线中心：在兴趣挖掘、物品检索和解释生成这几段接入 LLM，把 log-fitting 改成以意图为中心的过程。为了把通用 LLM 对齐到这些推荐任务，训练分成多阶段，包括 reasoning-enhanced pre-alignment 和 self-training evolution，并由 Human-LLM cooperative judge 系统引导。系统已全量部署在 Taobao App。在线结果按利益相关方给出：用户侧内容多样性和满意度上升，例子是 CICD +6.96%、DT +4.82%；商家和平台得到更多曝光与转化，例子是 CTR +6.33%、IPV +9.47%、DCAU +3.72%。Fig. 1 对应淘宝 App 首页 “Guess What You Like”。左图是相对基线的 CTR、IPV、DCAU、人均点击类目多样性 CICD 和停留时间 DT；右图是不同流行度商品组上的 CTR 与 Page View Rate（PVR）。图注说明 CTR、PVR 等商业指标为保密做了归一化。

## 1. Introduction

理想推荐是把用户往往说不清的意图配上最相关的物品，让用户用最小代价得到最大体验；对齐之后，用户满意、商家销量、平台流量和收入会形成正循环。难点是从又长又快变的行为轨迹里推断真实意图。过去二十年主要在特征和结构上优化：特征从手工统计到序列与交叉特征，再到超长行为建模；结构从 factorization machines、深度匹配网络、图神经网络，到生成式 Transformer。作者认为这些收益仍被历史日志里的共现绑住，本质上是 “learn clicks from clicks”。没有显式的兴趣理解，就会强化相似用户已经消费过的东西，放大 Filter Bubble，并进一步边缘化长尾，文中称为 Matthew Effects。LLM 的世界知识、细粒度语义和逐步推理，被看成能分析潜在兴趣、并说明用户为什么可能想要某件物品的一条路；但已有 LLM 推荐多停在小规模离线基准，进不了真实环境。

RecGPT 把三个推理 LLM 放进工业推荐主干，形成闭环：User Interest Mining → Item Tag Prediction → Item Retrieval → Explanation Generation，对应 Figure 2。User-Interest LLM 读用户终身行为，写成一段当前兴趣的自然语言画像。Item-Tag LLM 再据此生成细粒度物品标签，描述用户最可能在找的东西。这些标签进入检索，把原来的 user–item 双塔扩成 user–item–tag 三塔，只有对齐推断意图的物品才进入下游排序和重排；候选生成从协同过滤改成兴趣增强，下游基础设施不用改。最后 Recommendation-Explanation LLM 给最终物品附上缓存好的自然语言解释。贡献有三条。一是已全量上线淘宝 App 首页 “Guess What You Like”：用户侧 CICD +6.96%、DT +4.82%，用来说明挖到了历史交互之外的潜在、多样兴趣；商家和平台侧 CTR +6.33%、IPV +9.47%、DCAU +3.72%；并称缓解了 Matthew effect，让不同商家的曝光更均衡。二是用 LLM 的世界知识和推理，从行为里显式挖潜在兴趣，而不是只学表面共现；作者称这是首次把 reasoning-enhanced、hundred-billion-scale 的推荐基础模型部署到服务超过十亿消费者和物品的工业场景。三是一套多阶段训练：从 reasoning-enhanced pre-alignment 到 self-training evolution，用 LLM-as-a-Judge 做数据质量筛选和模型评估，再从人工专家审核过渡到 Human-LLM cooperative judge，以加快迭代并保住质量。第 3 节的评判系统不在本导读范围内。

## 2. RecGPT Workflow

Figure 2 把流水线画成三个 LLM 加一次检索。LLMUI 做兴趣挖掘，LLMIT 做物品标签预测，LLMRE 做推荐解释。LLMIT 预测的是文中所称的 item tags，再用 tag-aware 语义相关检索映回域内物品库：标签来自基于推理的意图，而不是表层特征匹配，并与传统协同信号一起，兼顾语义相关和协同模式。四段分别是：LLMUI 在终身多行为序列上做显式兴趣挖掘（Section 2.1）；LLMIT 根据兴趣预测代表潜在偏好分布的标签（Section 2.2）；标签感知检索把标签映到具体物品，并加入行为协同，平衡语义与协同（Section 2.3）；LLMRE 结合兴趣和物品，生成个性化、面向用户的解释（Section 2.4）。相对只靠隐向量和最终反馈的做法，这里各阶段都是显式文本，便于看中间过程和做过程级监督，也把端到端优化拆成输入输出清楚的子任务。

### 2.1. User Interest Mining

这一段称为 Generative User Profiling。两个障碍是：淘宝用户平均有超过 37k 条历史行为，而当时 LLM 的上下文窗口是 128k token；以及 LLM 缺少推荐域知识。对策是 Reliable Behavioral Sequence Compression，再加 LLMUI 的多阶段 Task Alignment。可靠行为只留高参与动作：favorites、purchases、add-to-cart，以及 detailed product views、reviews reading 这类刻意点击，加上 search queries；普通商品点击因噪声大被排除。压缩分物品级和序列级。序列级先用 “时间–行为类型” 做键聚合，再按物品序列反向聚合，得到信息更密的行为序列。文中给出的经验结果是：压缩后 98% 的用户行为能放进 128k token 窗口，未压缩只有 88%；兴趣推断效率提高 29%。对齐分三阶段。Stage 1 是 Curriculum Learning-based Multi-task Fine-tuning，16 个预备子任务、16.3k 训练样本。Stage 2 是 Reasoning-Enhanced Pre-alignment，人工把最初 90.0k 条生成样本筛成 19.0k 条高质量数据。Stage 3 是 Self-Training Evolution，模型自己产数据再迭代，收集到 21.1k 条高质量样本，并用 Human-LLM 协作和 LLM-as-a-Judge 做低成本筛选。Prompt 2.1.2 用用户属性和压缩后的可靠行为序列，并带上预设兴趣池。质量看 Willingness（自发还是出于外部必要）和 Reasonableness（强相关、弱相关、无相关、幻觉），标准在 Table 1。Table 2 的人工通过率：DeepSeek-R1 70.00%，Qwen3-Base 59.74%，多阶段对齐后的 Qwen3-SFT 77.28%，内部稀疏 MoE 模型 TBStars-42B-A3.5（文中称 TBStars-SFT）全参微调后 74.39%。线上用 LLMUI 离线预测，平均每位用户 16.1 个兴趣。

### 2.2. Item Tag Prediction

LLMIT 同样先做多阶段 Task Alignment，再用 Incremental Learning 跟上兴趣和商品趋势。Figure 4 标出 Reasoning-Enhanced Pre-Alignment 约 90k 样本、Self-Training Evolution 约 5k 样本。标签格式是 “Modifier + Core-Word”，例子是 “Outdoor waterproof non-slip hiking boots”，并用 CoT 推理。提示里的约束包括：与已有兴趣一致、至少 50 个标签以保证多样性、语义要具体、优先新类目并避开刚交互过的物品、结合时间戳考虑季节。输出是三元组 (Tag, Associated Interest Preference, Rationale)。式 (2) 写成 \(T_u=\mathrm{LLMIT}(A_u,I_u,S_u\mid P_{IT})\)，其中 \(A_u\)、\(I_u\)、\(S_u\) 是属性、兴趣和多行为序列（点击、购买、搜索）。拒样看 Relevance、Consistency、Specificity、Validity，Table 3 用 “全部满足才算对、任一不满足即错” 举例。Table 4 的人工通过率：Qwen3-Base 33.70%，DeepSeek-R1 80.00%，Qwen3-SFT 84.80%，TBStars-SFT 88.80%。增量学习每两周一次，用过去 14 天的线上点击、购买等记录。噪声（误点、促销痕迹）和头部兴趣标签带来的不平衡，用三步处理：QwQ-32B 按相关性和时效（当季或下一季）做 Data Purification；再用 QwQ-32B 把有效行为补成上述三元组，标签直接用商品标题，即 Interest Completion；然后两阶段重采样做 Data Balancing。Table 5 用真实线上交互验证：TBStars-SFT 不做增量学习时 HR@30 为 0.3671，做了之后为 0.3776，提升 1.05%。

### 2.3. Item Retrieval

检索称为 User-Item-Tag Retrieval Framework（TAR），Figure 5。物品塔把物品的稀疏、稠密特征送进 DNN 得到 \(\mathbf{h}_v\)。用户塔用用户 id embedding 和点击、购买等多行为序列的池化表示，得到 \(\mathbf{h}_u\)。标签塔对标签 token 的 embedding 做平均再送进 DNN，得到 \(\mathbf{h}_t\)。协同分是 \(\hat y_{\mathrm{col}}=\mathbf{h}_u^\top\mathbf{h}_v\)，语义分是 \(\hat y_{\mathrm{sem}}=\mathbf{h}_t^\top\mathbf{h}_v\)。优化把协同对比损失和语义对比损失加在一起；语义侧还有类别感知的对比，让同类物品分得更细、不同类之间边界更清楚。总损失写成 \(\mathcal{L}_{\mathrm{TAR}}=\mathcal{L}_{\mathrm{col}}+\alpha\mathcal{L}_{\mathrm{tag}}+(1-\alpha)\mathcal{L}_{\mathrm{cate}}\)，实验里 \(\alpha=0.5\)。在线推理把用户塔和标签塔融成 \(\mathbf{h}_{\mathrm{fuse}}=\beta\mathbf{h}_u+(1-\beta)\mathbf{h}_t\)，等价于 \(\hat y_{\mathrm{final}}=\beta\hat y_{\mathrm{col}}+(1-\beta)\hat y_{\mathrm{sem}}\)。\(\beta\) 控制协同和语义的比例，这两节没有给出它的具体取值。

### 2.4. Personalized Explanation Generation

LLMRE 要在低延迟下给推荐结果写个性化解释。对齐同样走 DeepSeek-R1 产生的教师数据（Reasoning-Enhanced Pre-Alignment）和 Judge 过滤（Self-Training Evolution）。Figure 6 把这两段标成约 80k 与约 120k 样本。生成分两步：先理解用户兴趣和物品特点，再在相关成立时写解释。质量四条是 Relevance、Factuality、Clarity、Safety，正反例在 Table 6。Table 7 的人工通过率：Qwen3-Base 30.0%，DeepSeek-R1 92.7%，对齐后的 Qwen3-SFT 95.8%。实时为每个用户–物品对生成解释开销过大，因此改为离线生产：从兴趣集合和已收集的标签–兴趣关联出发，用预训练的 Tag-to-Cate 模型 \(\phi\) 把标签 \(T\) 映到类目 \(C\)，只给同类目下对上的兴趣–物品对写解释，建成 Interest–Item–Explanation Lookup Table；线上按当前推荐物品和用户兴趣查表。第 3 节 Human-LLM Cooperative Judge 起不在本导读范围内。
