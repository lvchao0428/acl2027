> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

**原文件名**：KAR_arXiv2410.13765.pdf

**原文标题**：Knowledge-Aware Query Expansion with Large Language Models for Textual and Relational Retrieval

**作者**：Yu Xia、Junda Wu、Julian McAuley（University of California San Diego）；Sungchul Kim、Tong Yu、Ryan A. Rossi、Haoliang Wang（Adobe Research）。

**场合**：arXiv:2410.13765v2 [cs.CL]，2025 年 2 月 5 日。

## 摘要

大模型已被用来扩写查询，以补上和目标文档更接近的语义；也有工作先给模型看一轮初检结果，让扩写更贴着语料。这些做法主要拉近查询和文档正文的文本相似度，文档之间的关系则被放过。像“找一台评分高、适合野生动物摄影、还能配我现有 Nikon F-Mount 镜头的相机”这类查询，扩写可以在字面上很像，结构上却对不上用户要的关系。

为此，论文提出一种 knowledge-aware query expansion：把知识图谱里的文档关系提供给大模型。针对现有基于图谱的方法只用实体名打分的不足，Knowledge-Aware Retrieval（KAR）把文档正文当作图谱节点的表示，并用基于文档的关系过滤。实验覆盖三个不同领域的数据集，相对当时的文本加关系半结构化检索基线有优势。摘要没有给出具体指标数字。

## 1 Introduction

大模型扩写查询，是为了补上目标文档的相近语义（Gao et al., 2023; Wang et al., 2023）。直接生成会带来幻觉、信息过时和领域知识不足；后续工作（Jagerman et al., 2023; Lei et al., 2024; Shen et al., 2024）改用初检结果当上下文，例如 pseudo relevance feedback（PRF）（Lv and Zhai, 2010; Li et al., 2022），让扩写更贴语料。即便如此，重点仍是扩写和文档正文的语义相似。真实搜索里，文档除了文字描述，还常按特定关系连在一起（Talmor and Berant, 2018; Cao et al., 2022）。用户会以半结构化方式同时问文本和关系（Wu et al., 2024b; Patel et al., 2024; Wu et al., 2024a; Boer et al., 2024），现有扩写方法没有覆盖这一点。

图 1 用商品搜索说明缺口。查询同时要求“评分高”“适合 wildlife photography”，以及“兼容 Nikon F-Mount lenses”。HyDE（Gao et al., 2023）和 RAR（Shen et al., 2024）能补上 “wildlife”“highly rated” 这类文字，却会编出错误关系，例如把 “Nikon Coolpix P1000” 说成兼容 F-Mount 镜头。KAR 则使用图谱里真实的共购关系，例如顾客把 “Nikon Z7 II” 和 F-Mount 镜头一起买过，从而生成语义相近、关系也对得上的扩写。

做法是：先用大模型抽出查询里点名的实体，再取这些实体的文本文档，以及图谱上相连的节点和关系。已有 KG 问答（Yasunaga et al., 2021; Zhang et al., 2022; Taunk et al., 2023）按查询和实体名（如 “Nikon camera”）的语义相似度过滤关系，会漏掉用户真正在问的文本细节（如 “highly rated”“wildlife”）。KAR 改用文档正文表示节点，做 document-based relation filtering，再让大模型在收集到的文本知识和关系知识上生成扩写：既贴着语料，又保住用户指定的文档关系。扩写后的查询用于最终检索。实验在 STaRK（Wu et al., 2024b）的三个半结构化检索集上进行，分别对应商品、学术论文和生物医学搜索。结果是：KAR 超过当时的查询扩写方法，并相对基于大模型的检索 agent 至少打平。贡献有三条：用图谱增强大模型，处理同时带文本要求和关系要求的查询；用文档正文做节点表示并做基于文档的关系过滤，以克服只按实体打分；三个数据集上的实验说明方法有效、可用。引言没有印出具体检索分数。

## 2 Related Work

**2.1 LLM-based Query Expansion。** 查询扩写是信息检索里的老办法（Azad and Deepak, 2019），用额外上下文去对上目标文档。早期 pseudo-relevance feedback（Yu et al., 2003; Cao et al., 2008; Lv and Zhai, 2010; Li et al., 2022）从初检文档里抽补充内容，效果受初检质量限制。大模型进入检索之后（Zhu et al., 2023），HyDE（Gao et al., 2023）直接生成“假设文档”，再用其嵌入去找真实文档；Query2Doc（Wang et al., 2023）加上 few-shot 例子；Jagerman et al. (2023) 还试过用 chain-of-thought 当扩写。为补领域知识，RAR（Shen et al., 2024）把初检结果喂给模型再扩写；Lei et al. (2024) 先从初检里抽关键信息；AGR（Chen et al., 2024）用 Analyze-Generate-Refine 多步框架，把自我修正和初检参照结合起来，Jia et al. (2024) 也有类似核验。这一节的判断是：这些进展仍主要对准文本相似，放过了文档关系；KAR 的差别在于把图谱里的结构化文档关系交给模型，用来做半结构化检索。

**2.2 KG-Augmented LLM。** 更早的路线是用语言模型的文本嵌入去加强图神经网络，做图谱推理（Feng et al., 2020; Lin et al., 2021; Yasunaga et al., 2021; Spillo et al., 2023）。大模型具备对多种文本结构的推理能力之后，图谱反过来成为给模型补事实或领域知识的来源（Pan et al., 2024）。文中点名的例子包括：Think-on-Graph（Sun et al., 2024）沿实体和关系探索、取相关三元组；Reason-on-Graph（Luo et al., 2024）取推理路径以约束生成；HyKGE（Jiang et al., 2024）先生成假设路径再落到图谱上；LPKG（Wang et al., 2024）从图谱构造规划数据。另有一波 graph retrieval augmented generation（Peng et al., 2024; Xu et al., 2024; He et al., 2024; Hu et al., 2024），把图谱一类的图数据当作检索源。

和这些工作相比，论文标出两点不同。第一，前人多做知识图谱问答：问题偏事实，答案被精确编码在图谱里；本文做文档检索，查询更描述性、更依赖领域。第二，前人往往只把图谱当唯一检索源；本文把文本文档和知识图谱一起当作半结构化知识源，信息覆盖多个侧面（Wu et al., 2024b），这种来源本身给抽取和检索带来另一类困难（Patel et al., 2024; Wu et al., 2024a; Boer et al., 2024）。本节没有报告实验数字。第 3 节起是问题定义与方法，此处不展开。
