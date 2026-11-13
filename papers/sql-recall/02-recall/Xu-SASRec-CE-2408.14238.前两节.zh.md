> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名：** Xu-SASRec-CE-2408.14238.pdf

**原文标题：** Are LLM-based Recommenders Already the Best? Simple Scaled Cross-entropy Unleashes the Potential of Traditional Sequential Recommenders

**作者：** Cong Xu、Zhangchi Zhu（East China Normal University；共同一作），Mo Yu（WeChat, Pattern Recognition Center），Jun Wang、Wei Zhang（East China Normal University），Jianyong Wang（Tsinghua University）

**场合：** arXiv:2408.14238v1 [cs.IR]，2024 年 8 月 26 日。首页未另印会议名称。代码：https://github.com/MTandHJ/CE-SCE-LLMRec

## 摘要

有工作用带 full softmax 的 cross-entropy（CE）微调大语言模型，并在序列推荐里报告到了 “state-of-the-art”。作者认为对比不公平：拿来比较的传统模型大多用 pointwise 或 pairwise 损失训练。这种设定会低估传统方法，也会把语言模型的排序能力看得过满。

他们给 CE 的优势一个理论说法，抓住两个性质：tightness 和 coverage。另外两条判断是：若只看推荐效果，CE 还不是最优，因为它对某些排序指标并不是很紧的界；当 full softmax 做不到时，可以把采样得到的 normalizing term 放大。按这个理解把传统模型的潜力放出来之后，它们可以超过基于大语言模型的推荐。摘要的收束是：算力代价已经很大，现有 LLM 推荐并没有所声称的那么有效，希望以后的评测更客观。摘要没有给具体指标数字。

## 1 Introduction

推荐要在电商、在线新闻、教育等场景里帮人从过多信息中找到感兴趣的物品。不同任务用不同模型：协同过滤里图神经网络很常见，序列推荐里 Transformer 越来越常用。大语言模型被看成通向通用推荐器的一条路。配上仔细设计的提示，它们在可解释推荐和跨域推荐上显得有潜力；但若不注入领域知识，和传统方法之间仍有不可忽略的差距。一些工作在微调之后看到“很强”的结果，就很快肯定语言模型的排序能力。作者认为，语言模型的计算负担很大，这类说法在被接受和应用之前必须仔细检查，以免大规模浪费资源。

检查的入口是损失函数。语言模型预训练和微调里的 next-token prediction，本身就是对整个词表做 full softmax 的 CE。传统推荐则多半是 pointwise 或 pairwise：SASRec 用的 BCE、FMLP-Rec 用的 BPR，都是每个正样本动态抽一个负样本。已有研究指出，在序列推荐里 CE 通常优于 BCE 或 BPR，所以上一次比较公不公平就成了问题。引言把它拆成三个问题。

第一，两边都用 CE 时，LLM 推荐是否仍超过传统模型。作者比较四套带独立 ID 嵌入表的 LLM 推荐器，以及分别基于 MLP、CNN、RNN、Transformer 的四个传统模型。用 BCE 或 BPR 时，传统模型远远落后；换成 CE 之后，其中一些会以很大幅度超过语言模型。第二，CE 为什么能提高排序能力。Bruch et al. 把 CE 和一些排序指标连起来，Wu et al. 又证明它有利于减轻流行度偏差。作者沿着前一条线补充：理想的推荐损失要同时顾 tightness 和 coverage。前者要求损失是排序指标的一个好的软代理，这样优化损失才会稳定地改善指标；后者要求训练时看到足够多的负样本。CE 在 coverage 上是满的，每个 mini-batch 都用上全部物品；但他们从理论上认为它在 tightness 上仍次优，动态截断可以更好。第三，物品数到数亿、full softmax 做不到时，传统模型还能不能超过 LLM。子词切分把语言模型的词表压在可计算的规模里，只要独立 ID 也能用类似方式表示，LLM 这边就有一条可行路线。若传统模型在这种实际设定下释放不出潜力，LLM 推荐就仍然很有希望。他们因此提出 Scaled Cross-Entropy（SCE）：均匀抽样来估计 CE 的归一化项，再用一个额外权重把采样项放大。普通 sampled softmax 的 tightness 很差，论证留在后文；SCE 的说法是，每步只抽很少的负样本，就足以接近 full softmax 的 CE。后文安排是：第 2 节先看性能，第 3 节讨论第二个问题的理论，第 4 节做第三个问题的实际比较，相关工作在第 5 节。

## 2 Potential of Traditional Recommenders over LLM-based Recommenders

这一节只做一件事：传统序列模型从 BCE/BPR 换成 CE 之后，成绩怎么变。序列推荐被定义成：查询 \(q = [v_1,\ldots,v_t]\) 是历史交互，要预测下一项 \(v_{t+1}\)。打分函数 \(s_{qv} = s_\theta(q, v)\) 把查询和候选映到同一隐空间，再用内积算相似度，按分数取靠前的物品。训练是在观测交互上最小化损失。文中把损失写成

\[
\ell(q, v_+;\theta) = -\log\frac{\exp(s_\theta(q, v_+))}{Z_\theta(q)} = -s_\theta(q, v_+) + \log Z_\theta(q),
\]

并单独把 normalizing term \(Z\) 拿出来，因为后面它决定损失和排序指标的关系。Table 1 列出本文要讨论的损失，以及均匀采样时 bounding probability 的下界。\(\ell_{\mathrm{CE}}\) 的 \(Z\) 是全体物品上 \(\exp(s_v)\) 之和，下界为 1。\(\ell_{\mathrm{BCE}}\) 和 \(\ell_{\mathrm{BPR}}\) 各用一个负样本，下界为 0。\(\ell_{\mathrm{SSM}}\) 是 sampled softmax，\(\ell_{\mathrm{SCE}}\) 在采样项上再乘权重 \(\alpha\)。SSM 与 SCE 的 bounding probability 下界印在该表最后一列，分式和上下标挤在一起，数字无法辨认，这里不逐符号抄写。

数据用公开的 Beauty 和 Yelp。过滤掉交互少于 5 次的用户和物品，按 leave-one-out 划分：最后一次交互做测试，倒数第二次做验证。预处理后的规模写在附录，前两节没有印出用户数或物品数。指标上，目标物品的预测名次 \(r_+\) 是分数不低于它的物品个数。单条查询的 NDCG 和 MRR 简化成 \(1/\log_2(1+r_+)\) 和 \(1/r_+\)，名次越靠前越大，\(r_+=1\) 时最大。脚注说明：实践中名次差过预先设定的 \(k\)（例如 1、5、10）就视为没有意义，所以 NDCG@\(k\) 和 MRR@\(k\) 对这些差的名次给 0。

基线只保留带独立 ID 嵌入表的 LLM 推荐器：P5 (CID+IID)、POD 以 T5 为底座，LlamaRec、E4SRec 微调 Llama2。POD 自带的预处理脚本可能导致信息泄漏，因此物品 ID 用随机整数，不用依次递增的整数。传统模型是 Caser、GRU4Rec、SASRec、FMLP-Rec，架构分别是 CNN、RNN、Transformer、MLP。Table 2 的规模是：P5 与 POD 嵌入 512、最大序列长度 512、历史交互最多 50、参数量 60M；两个 Llama2 模型嵌入 4096、最大序列长度 2048、历史同样最多 50、参数量 7B。四个传统模型嵌入都是 64，两种长度上限都是 50，参数量分别为 GRU4Rec 0.80M、Caser 3.80M、SASRec 0.83M、FMLP-Rec 0.92M。

Table 3 在 Beauty 和 Yelp 上比较 NDCG@5、NDCG@10、MRR@5、MRR@10。表中灰色表示低于该列最好的 LLM 推荐器；“▲ % over LLM” 是各块里最好结果相对最好 LLM 结果的差距。用 BPR 或 BCE 时，多数传统模型明显落后，例如落后于 LlamaRec。Beauty 上，BPR 这一块相对最好 LLM 是 −20.8%、−20.3%、−22.1%、−21.5%，BCE 是 −25.8%、−22.6%、−28.1%、−26.0%，和正文说的“至少大约 20% 的差距”一致。Yelp 上 FMLP-Rec 已经不错：BPR 相对最好 LLM 为 +1.3%、+10.3%、+5.7%、+6.5%，BCE 为 −0.1%、+6.5%、+6.1%、+5.7%。换成 CE 之后，SASRec 和 FMLP-Rec 在两个数据集上都超过全部 LLM 推荐器。Beauty 上 SASRec 的四个数是 0.0510、0.0597、0.0443、0.0479，FMLP-Rec 是 0.0507、0.0594、0.0438、0.0473；对照的 LlamaRec 是 0.0405、0.0492、0.0344、0.0380。Yelp 上 CE 的 FMLP-Rec 是 0.0364、0.0444、0.0316、0.0348。CE 这一块的 ▲ % 在 Beauty 为 +25.7%、+21.3%、+28.1%、+26.0%，在 Yelp 为 +10.3%、+21.0%、+16.9%、+18.1%。GRU4Rec 和 Caser 用 CE 也会变好，但表达能力有限，不一定超过 LLM。

作者据此认为，先前肯定 LLM 推荐效果的说法，建立在传统模型常用 BCE 或 BPR 的偏颇比较上。参数量从 P5 的 60M 涨到 LlamaRec 的 7B，在部分指标上只有有限的提升；世界知识和推理能力在这里用处有限。结论是：即便经过微调，只要能做 full softmax，LLM 推荐器并没有超过当时最好的传统序列模型。
