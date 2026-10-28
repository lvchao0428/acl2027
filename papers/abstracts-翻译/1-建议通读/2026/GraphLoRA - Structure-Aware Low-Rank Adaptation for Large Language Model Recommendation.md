# GraphLoRA: Structure-Aware Low-Rank Adaptation for Large Language Model Recommendation
> 来源文件：GraphLoRA - Structure-Aware Low-Rank Adaptation for Large Language Model Recommendation.pdf
> 发表年份：2026
> 单位：Anhui University；University of Science and Technology of China

## 英文原文摘要（Original Abstract）

Large Language Models (LLMs) have shown strong potential for recommendation (LLMRec) due to their powerful reasoning and generalization abilities. However, effectively aligning the textual semantics modeled by LLMs with the collaborative signals remains a key challenge. Existing methods either translate collaborative information into textual prompts or inject pre-trained embeddings into the LLM, both of which treat structural information as static input and fail to capture high-order relational dependencies. To bridge this gap, we propose GraphLoRA, a novel framework that generalizes low-rank adaptation from independent to structure-aware propagation. GraphLoRA embeds a trainable graph message-passing network within the low-rank adaptation pathway, enabling structural signals to propagate through the parameter space. This design allows collaborative topology to explicitly guide parameter updates, fostering deep integration between graph-structured and textual semantic information. Extensive experiments on multiple benchmarks demonstrate that GraphLoRA not only outperforms state-of-the-art LLM-based recommendation methods but also achieves superior generalization, effectively balancing structural reasoning capability with computational efficiency.

## 中文翻译（Chinese Translation）

大语言模型（LLM）凭借强大的推理与泛化能力，在推荐（LLM-based Recommendation, LLM-Rec）领域展现出巨大潜力。然而，如何有效地将 LLM 所建模的文本语义与协同信号（collaborative signals）对齐，仍是一个关键挑战。现有方法要么把协同信息翻译为文本提示（prompt），要么把预训练嵌入（embedding）注入 LLM，二者都将结构信息视为静态输入，无法捕获高阶关系依赖。为弥合这一缺口，我们提出 GraphLoRA——一个将低秩适配（LoRA）从"独立适配"推广到"结构感知传播"的新框架。GraphLoRA 在低秩适配通路中嵌入一个可训练的图消息传递网络，使结构信号能够在参数空间中传播。该设计让协同拓扑（collaborative topology）显式地引导参数更新，促进图结构信息与文本语义信息的深度融合。在多个基准上的大量实验表明，GraphLoRA 不仅优于当前最先进的 LLM 推荐方法，还具有更强的泛化能力，在结构推理能力与计算效率之间取得了良好平衡。代码见 https://github.com/wgj15965/GraphLoRA。
