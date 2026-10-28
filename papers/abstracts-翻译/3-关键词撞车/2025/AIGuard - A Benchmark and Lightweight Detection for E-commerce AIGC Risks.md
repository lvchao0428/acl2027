# AIGuard: A Benchmark and Lightweight Detection for E-commerce AIGC Risks
> 来源文件：AIGuard - A Benchmark and Lightweight Detection for E-commerce AIGC Risks.pdf
> 发表年份：2025
> 单位：Wuhan University；State Key Lab of Mathematical Engineering and Advanced Computing；Alibaba Group

## 英文原文摘要（Original Abstract）

Recent advancements in AI-generated content (AIGC) have heightened concerns about harmful outputs, such as misinformation and malicious misuse. Existing detection methods face two key limitations: (1) lacking real-world AIGC scenarios and corresponding risk datasets, and (2) both traditional and multimodal large language models (MLLMs) struggle to detect risks in AIGC. Towards this end, we introduce AIGUARD, the first benchmark for AIGC risk detection in real-world e-commerce. It includes 253,420 image-text pairs (i.e., the risk content and risk description) across four critical categories: abnormal body, violating physical laws, misleading or illogical context, and harmful or problematic message. To effectively detect these risks, we propose distilling text annotations into dense soft prompts and identifying risk content through image soft prompt matching during inference. Experiments on the benchmark show that this method achieves a 9.68% higher recall than leading multimodal models while using only 25% of the training resources and improving inference speed by 37.8 times. For further research, our benchmark and code are available at https://github.com/wenh-zhang/aiguard-dataset.

## 中文翻译（Chinese Translation）

AI 生成内容（AIGC）的最新进展引发了人们对虚假信息、恶意滥用等有害输出的担忧。现有检测方法存在两个关键局限：（1）缺乏真实世界的 AIGC 场景及对应的风险数据集；（2）传统方法和多模态大语言模型（MLLM）都难以检测 AIGC 中的风险。为此，我们提出 AIGUARD，这是首个面向真实电商场景的 AIGC 风险检测基准。它包含 253,420 个图文对（即风险内容与风险描述），覆盖四大关键类别：异常身体画面、违反物理规律、误导或不合逻辑的上下文、以及有害或有问题的信息。为有效检测这些风险，我们提出将文本标注蒸馏为稠密软提示（soft prompt），并在推理时通过图像软提示匹配来识别风险内容。在该基准上的实验表明，相比主流多模态模型，本方法召回率提升 9.68%，训练资源仅需 25%，推理速度提升 37.8 倍。基准与代码已开源：https://github.com/wenh-zhang/aiguard-dataset 。
