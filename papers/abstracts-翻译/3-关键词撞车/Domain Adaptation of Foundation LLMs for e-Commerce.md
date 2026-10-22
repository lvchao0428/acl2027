# Domain Adaptation of Foundation LLMs for e-Commerce
> 来源文件：Domain Adaptation of Foundation LLMs for e-Commerce.pdf

## 英文原文摘要（Original Abstract）

We present the e-Llama models: 8 billion and 70 billion parameter large language models that are adapted towards the e-commerce domain. These models are meant as foundation models with deep knowledge about e-commerce, that form a base for instruction- and fine-tuning. The e-Llama models are obtained by continuously pretraining the Llama 3.1 base models on 1 trillion tokens of domain-specific data. We discuss our approach and motivate our choice of hyperparameters with a series of ablation studies. To quantify how well the models have been adapted to the e-commerce domain, we define and implement a set of multilingual, e-commerce specific evaluation tasks. We show that, when carefully choosing the training setup, the Llama 3.1 models can be adapted towards the new domain without sacrificing significant performance on general domain tasks. We also explore the possibility of merging the adapted model and the base model for a better control of the performance trade-off between domains.

## 中文翻译（Chinese Translation）

我们发布 e-Llama 模型：分别为 80 亿和 700 亿参数、面向电商领域适配的大语言模型。这些模型作为具备深厚电商知识的基础模型，可作为后续指令微调和精调的底座。e-Llama 模型通过在 1 万亿 token 的领域专属数据上对 Llama 3.1 基座模型进行持续预训练得到。我们讨论了方法设计，并通过一系列消融实验说明超参数选择的依据。为量化模型对电商领域的适配程度，我们定义并实现了一组多语种、电商专属的评测任务。结果表明，在精心设计训练配置的前提下，Llama 3.1 模型可以较好地适配新领域，而不会在通用领域任务上损失显著性能。我们还探索了将领域适配后模型与基座模型进行模型合并（model merging）的可能性，以便更好地权衡不同领域之间的性能折中。
