# What Makes an Ideal Quote? Recommending "Unexpected yet Rational" Quotations via Novelty

| 项目 | 内容 |
|------|------|
| **Paper** | What Makes an Ideal Quote? Recommending "Unexpected yet Rational" Quotations via Novelty |
| **Authors** | Powei Chang, Jin Xiao, Guanglei Yue, Qianyu He, Yanghua Xiao, Deqing Yang, Jiaqing Liang |
| **Affiliation** | Fudan University（复旦大学） |
| **Theme** | 引用推荐 / 新奇性建模 / 检索增强推荐 |
| **Problem** | 现有引用推荐系统主要关注主题相关性，忽略了使引用令人难忘的关键因素——新奇性（novelty） |
| **Method** | NovelQR 框架：(1) 生成式标签 Agent 将引用和上下文解析为多维深层语义标签，增强检索；(2) Token 级新奇性估计器对候选进行重排序，同时缓解自回归延续偏差。受陌生化理论（defamiliarization theory）启发 |
| **Benchmark** | 中英双语数据集，覆盖多个领域 |
| **Result** | 人类评委评价 NovelQR 的推荐更恰当、更新颖、更引人入胜 |
| **Question** | 新奇性和相关性之间的最优平衡点如何确定？不同文化背景下"出人意料"的定义是否一致？ |

## 详细笔记

### 研究背景与动机

引用推荐旨在为写作建议合适的引文。现有系统大多优化表面主题相关性，忽略了引用的深层语义和美学属性。用户研究表明，人们系统性地偏好那些"出乎意料却又合理"的引用——读者初见时可能短暂困惑，但随即感受到顿悟。这一发现受到文学理论中"陌生化"（defamiliarization）概念的启发。

### 核心方法详解

**生成式标签 Agent**：使用 LLM 将每条引用及其上下文解析为多维深层语义标签（如修辞手法、情感基调、隐含主题等），这些标签用于增强检索阶段的语义匹配。

**Token 级新奇性估计器**：在重排序阶段，为每个候选引用计算 token 级别的新奇性得分。特别地，该估计器缓解了"自回归延续偏差"——即模型倾向于推荐与上下文最自然衔接（但可能平淡无奇）的引用。

### 实验设置与结果

- **数据集**：中英双语数据集，涵盖文学、演讲、学术等多个领域
- **关键结果**：人类评委在恰当性、新奇性和引人入胜程度三个维度上一致偏好 NovelQR 的推荐

### 个人思考

NovelQR 将文学理论引入推荐系统设计，是跨学科研究的好例子。"出乎意料却合理"这一目标不仅适用于引用推荐，对新闻推荐、内容发现等场景也有启发。自回归延续偏差的发现和缓解也为 LLM-based 推荐提供了新视角。
