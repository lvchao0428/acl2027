# What Makes an Ideal Quote? Recommending “Unexpected yet Rational” Quotations via Novelty

> 来源文件：15_NovelQR.pdf

## 英文原文摘要（Original Abstract）

Quotation recommendation enriches writing by suggesting quotations that fit a given context, but prior systems largely focus on topical relevance and overlook what makes quotes memorable. Based on a user study, we find that preferred quotations are often unexpected yet rational, motivating the goal of selecting quotes that are contextually novel while semantically coherent. We propose NOVELQR, which (1) uses a generative label agent to map quotations and contexts into multi-dimensional deep-meaning labels for label-enhanced retrieval, and (2) reranks candidates with a token-level novelty estimator that mitigates auto-regressive continuation bias. Experiments on bilingual datasets across diverse domains show that NOVELQR is preferred by human judges and improves overall recommendation quality over strong baselines, while achieving competitive novelty estimation. (Code: Github link).

## 中文翻译（Chinese Translation）

名言推荐（quotation recommendation）通过为给定上下文推荐契合的引语来丰富写作，但以往系统大多聚焦主题相关性，忽略了"什么让名言令人难忘"。基于一项用户研究，我们发现受偏好的引语往往"出乎意料却又合乎情理"，这促使我们追求选择在上下文中新颖（novel）且语义连贯的引语。我们提出 NOVELQR，它（1）使用生成式标签智能体将引语与上下文映射为多维"深层含义"标签，用于标签增强的检索；（2）以 token 级新颖度估计器对候选重排，缓解自回归延续偏置（auto-regressive continuation bias）。在跨多领域的双语数据集上的实验表明，NOVELQR 更受人类评审偏好，并在新颖度估计具竞争力的同时，整体推荐质量优于强基线。（代码见 GitHub）。
