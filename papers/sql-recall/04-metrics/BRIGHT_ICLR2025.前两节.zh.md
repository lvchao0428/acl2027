> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

原文件名：BRIGHT_ICLR2025.pdf

原文标题：BRIGHT: A Realistic and Challenging Benchmark for Reasoning-Intensive Retrieval

作者：Hongjin Su、Howard Yen、Mengzhou Xia、Weijia Shi、Niklas Muennighoff、Han-yu Wang、Haisu Liu、Quan Shi、Zachary S. Siegel、Michael Tang、Ruoxi Sun、Jinsung Yoon、Sercan Ö. Arık、Danqi Chen、Tao Yu。Su、Yen、Xia 为共同一作。Su、Han-yu Wang、Haisu Liu、Tao Yu 属 The University of Hong Kong；Yen、Xia、Quan Shi、Siegel、Tang、Danqi Chen 属 Princeton University；Muennighoff 属 Stanford University；Weijia Shi 属 University of Washington；Sun、Yoon、Arık 属 Google Cloud AI Research。通信邮箱为 {hjsu,tyu}@cs.hku.hk 与 {hyen,mengzhou,danqic}@cs.princeton.edu。

场合：Published as a conference paper at ICLR 2025。

## 摘要

现有检索基准主要是信息寻求类查询，例如从搜索引擎汇集来的问题，关键词或语义匹配通常就够用。许多真实的复杂查询要先做深入推理，才能认出相关文档，而不能停在表面形式。找一段代码问题对应的文档，就得懂其中函数的逻辑和语法。BRIGHT 被提出来填这个空档：它是一个文本检索基准，找回相关文档必须做密集推理。数据有 1,384 条真实查询，覆盖经济学、心理学、数学和编程等领域，来自自然发生、并经过人工整理的数据。

即便当时最强的检索模型在 BRIGHT 上也很差。MTEB 排行榜领先的 SFR-Embedding-Mistral 在该榜上 nDCG@10 为 59.0（脚注：2024-05-28 从 MTEB leaderboard 读取），在 BRIGHT 上 nDCG@10 只有 18.3。对查询做显式推理，检索最多能提高 12.2 个点；把表现最好的检索器找回的文档接进问答，也能抬高问答表现。代码与数据在 https://github.com/xlang-ai/BRIGHT 和 https://huggingface.co/datasets/xlangai/BRIGHT 。

## 1 INTRODUCTION

信息检索要从大规模文档、网页和日志里找出与查询相关的材料。相关可以是共享关键词或语义相近，也可以是更底层的类比，例如同一条经济理论解释的另一则故事，或用报错信息去定位对应的语法文档。后一类场景里，只做词面或语义匹配找不到目标，中间还要多一步推理。BRIGHT 研究的就是这种 reasoning-intensive retrieval。BEIR 和 MTEB 主要面对从搜索引擎来的事实型查询，相关文档和查询的词面或语义重叠往往很高，例如问 “the widest highway in North America”。Figure 1 把现有基准画成两级：第 1 级靠关键词，第 2 级靠语义，例子是 NQ 和 MS MARCO；BRIGHT 被放在第 3 级，查询与文档是否相关必须靠密集推理判断。查询来自经济学、数学、地球科学等自然用户问题，语料则包括博客、语法文档和 STEM 题解等网页数据。

基准含 12 个数据集，分两块。7 个来自 StackExchange：一篇文档若被答案引用，就视为相关，再由多名标注者确认这些正例确实能支撑回答该问题；因为判断有主观性，只保留标注者一致同意的文档。另外 5 个是编程和数学题，查询和正例文档因为共用同一套算法或定理而连在一起。评测使用 13 个不同规模和结构的检索模型。表现最好的 SFR-Embedding-Mistral 在 MTEB 的检索子集 BEIR 上得 59.0，在 BRIGHT 上 nDCG@10 只有 18.3。一个有效的改进方向是让 LLM 在检索前对查询生成 chain-of-thought 推理，平均最多提高 12.2 个点。把检索器 Qwen 取回的文档交给下游模型，问答好于闭卷；若换成 oracle 文档，提升更大，说明检索器仍有明显空间。另外，即便继续在基准文档上训练，也没有看到明显涨点，作者据此认为 BRIGHT 对大规模预训练中的数据泄漏比较稳。

## 2 RELATED WORK

检索基准以往多为信息寻求任务：问答、claim verification、实体检索，后来扩展到指令跟随、多跳和长上下文。BEIR 覆盖多种领域和任务，但相关文档与查询的语义重叠仍然高。和本文最近的是 BIRCO：它借用已有数据、按多方面目标评检索，但只做 LLM 重排序，而且每个查询的候选池大约只有 100 篇文档。RAR-b 把常识、数学和代码数据改成检索，检验模型能否直接把推理题的答案检出来；BRIGHT 关心的是更真实的情形，答案不太会作为子串出现在文档里。两者都面向需要推理的检索，作者认为 BRIGHT 是第一个把真实用户查询和大型语料中的自然文档对齐、并且必须靠深度推理才能配上的基准。

稠密检索把文本编成向量，训练数据可以是无监督、有监督，或由 LLM 生成。本文要横着比较稀疏与稠密、小模型与大模型、开源与专有。检索增强生成用找回的文档帮助作答；本文主要评检索，但也做了初步分析，说明更强的检索器能提高推理密集型任务上的生成。推理能力本身已有不少问答基准：数学侧有 GSM8K 及其扩展 GSM1K、TheoremQA、MATH、LeanDojo，代码侧有 HumanEval、MBPP、LiveCodeBench，题目多来自教材、网络、竞赛或领域专家。BRIGHT 从挑选过的高质量数据集取查询，再做额外标注，做成面向真实场景的推理密集型检索基准。这一节新出现的数量级是 BIRCO 每个查询约 100 篇候选文档。
