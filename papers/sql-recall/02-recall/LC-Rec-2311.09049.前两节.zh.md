> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名**：LC-Rec-2311.09049.pdf

**原文标题**：Adapting Large Language Models by Integrating Collaborative Semantics for Recommendation

**作者**：Bowen Zheng、Wayne Xin Zhao、Ji-Rong Wen（Gaoling School of Artificial Intelligence, Renmin University of China；姓名后标 ∗，脚注为 Corresponding author）；Yupeng Hou（University of California San Diego）；Hongyu Lu、Yu Chen、Ming Chen（WeChat, Tencent）。

**场合 / arXiv**：arXiv:2311.09049v4 [cs.IR]，2024 年 4 月 19 日。首页与前两节未印出会议或期刊名称。代码：https://github.com/RUCAIBox/LC-Rec/。

## 摘要

大语言模型要么被用来加强已有推荐模型，要么自己当推荐骨干，但和推荐系统之间有一道语义缝：待推荐物品常用离散 item ID 索引，而这些 ID 不在 LLM 的词表里。LLM 抓住的是语言语义，推荐系统隐含的是协同语义，模型容量因此用不满。LC-Rec 要在推荐里把两种语义接到一起，并且直接从整个物品集合生成推荐，不依赖事先给定的候选集。

索引一侧，用带 uniform semantic mapping 的、基于学习的向量量化，给物品分配有意义且不冲突的 ID，文中称为 item indices。对齐一侧，用一组专门设计的微调任务，迫使 LLM 把语言语义和这些索引所代表的协同语义真正合在一起，而不是只在表面上适应推荐。摘要称实验超过一批有竞争力的基线，包括传统推荐器和已有的 LLM 推荐器，但没有给出具体百分点。

## I. INTRODUCTION

引言从序列推荐的基本单位写起：用户兴趣随时间变，现有模型大多把交互日志排成序列，以 item ID 为单元，用 RNN、CNN、GNN 或 Transformer 建模。也有工作加入标题、描述、类目等内容，或用预训练语言模型抓物品文本的语义。LLM 出现后，有人用它改进排序，有人用它扩大推荐能力。根本困难被说成两套词表：语言模型用 token ID，推荐模型用 item ID，语义空间并不相同。

已有补法分成两路，作者都认为不够。一路把行为写成文本，例如拼接交互物品的标题和类目标签，再用提示让 LLM 做推荐。这只覆盖有限的物品信息，而且主要是语言语义，也不能保证生成的是领域内物品，通常还要靠候选集。另一路为物品另建索引词表，再学习生成目标物品。但在语义缝很大时，直接用原始 item ID 建词表，或只在目标任务上做较浅的微调，效果有限。作者把问题收成两件事。索引要同时满足：有意义（能反映物品相似度）、唯一（分配不冲突）、可扩展（能泛化到新物品）。对齐要让语言语义和协同语义在 LLM 内部充分结合，而不是只把目标推荐任务拟合一遍。脚注特别说明：文中的 align / alignment 指这两种语义的整合，不是让 LLM 遵循人类价值的那种 human alignment。

LC-Rec 把 Language 与 Collaborative semantics 合进推荐，并把推荐写成 token 生成，使 LLM 推荐物品像生成普通文本。索引用树结构的 vector quantization：离散 ID 从 LLM 编码的物品文本嵌入学来，从而带上物品之间的固有相似度；原始 VQ 可能把同一组 ID 分给多件物品，再用 uniform semantic mapping 减轻冲突。对齐微调除了序列物品预测，还包括显式的 index-language alignment 和隐式的、面向推荐的对齐。实验在三个真实公开数据集上进行，相对一组基线取得最好结果。实现基于 7B 参数的 LLaMA。贡献里给出的汇总数字是：在 full ranking 评价中，相对所有基线方法平均提升 25.5%。贡献本身是三条：无候选集的自回归序列推荐、能抓住相似度并避免 ID 冲突的 VQ 加上一组微调任务、以及上述 7B 实现与三个数据集上的结果。数据集名称不在本节。

## II. RELATED WORK

### A. Sequential Recommendation

序列推荐根据历史交互推断偏好并预测下一件物品。早期方法常用 Markov Chains。随后的典型做法是用 RNN、CNN、GNN、Transformer 对 item ID 序列建模。作者指出这些模型只从用户–物品交互里学协同关系，忽略标题、描述、类目等内容。后续工作把物品附带信息用于加强 ID 序列，并因标题和描述本身是自然语言，进而使用预训练语言模型。本节把本文的位置放在：用新的物品索引和对齐微调，把 LLM 和推荐任务更有效地接起来。没有指标数字。

### B. Large Language Models for Recommendation

LLM 被用于推荐，常见起点是把用户行为写成文本序列，例如拼接历史物品标题，再设计提示。作者认为语言语义和协同语义之间的缝，不能只靠提示设计补上。已有努力仍是两类。第一类用基于文本的行为序列微调 LLM，但不能保证生成领域内物品；上下文窗口有限，只能在给定候选集上排序，很难做 full ranking。第二类保留 item ID 或引入专门索引，给定纯 ID 序列后直接生成目标物品 ID。物品索引之间的协同语义可以建立，但 LLM 的语言语义和这些索引对得不齐。

同期工作也被点名，用来对照「深度、统一」的整合。TransRec 用多方面标识，把 ID、标题和属性合在一起，平衡可区分性与语义。CoLLM 把外部协同模型的表示作为输入的一部分，从而把协同语义送进 LLM。CLLM4Rec 分别从推荐任务和内容生成任务（例如评论）学习两套用户/物品嵌入，再用互正则让两边交互，最终推荐只用推荐任务那一套嵌入。本文的差别是：用仔细构造的 item indices 在 LLM 内部做统一整合。具体来说，树结构向量量化只需给 LLM 增加少量额外 token，通常约 1,000 个；再配合一系列语义对齐任务，把整合放到实际推荐设定里，例如 full ranking。第 2 节在此结束，索引学习和微调任务的公式从第 III 节才展开。
