# OneRec-Think: 面向生成式推荐的文本内推理

**原标题**: ONEREC-THINK: In-Text Reasoning for Generative Recommendation

**作者**: Zhanyu Liu, Shiyao Wang, Xingmei Wang 等

**单位**: Kuaishou Inc.（快手）

## 摘要

大语言模型（LLMs）强大的生成能力引发了推荐领域的范式转变。然而，现有的生成式模型（如 OneRec）仅作为隐式预测器运行，严重缺乏显式且可控的推理能力——而这正是 LLM 的核心优势。为弥合这一差距，我们提出 OneRec-Think，一个无缝整合对话、推理和个性化推荐的统一框架。OneRec-Think 包含：(1) **物品语义对齐（Itemic Alignment）**：通过跨模态的物品-文本对齐实现语义锚定；(2) **推理激活（Reasoning Activation）**：利用推理脚手架在推荐语境中激活 LLM 的推理能力；(3) **推理增强（Reasoning Enhancement）**：设计推荐专用的奖励函数，充分考虑用户偏好的多正确性（multi-validity）特征。在公开基准上的实验表明本方法达到了最优性能。此外，我们提出的"预思考（Think-Ahead）"架构实现了在快手的有效工业部署，APP 停留时间提升 0.159%，验证了模型显式推理能力的实际效用。
