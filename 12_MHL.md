# From Past To Path: Masked History Learning for Next-Item Prediction in Generative Recommendation

| 项目 | 内容 |
|------|------|
| **Paper** | From Past To Path: Masked History Learning for Next-Item Prediction in Generative Recommendation |
| **Authors** | Kaiwen Wei, Kejun He, Xiaomian Kang, Jie Zhang, Yuming Yang, Li Jin, Zhenyang Li, Jiang Zhong, He Bai, Junnan Zhu |
| **Affiliation** | Chongqing University; Institute of Automation, CAS; Aerospace Information Research Institute, CAS; City University of Hong Kong |
| **Theme** | 生成式推荐 / 序列建模 / Masked Learning |
| **Problem** | 从左到右的自回归范式 inherent 偏向局部上下文，难以捕获更深层的 historical dependencies，限制 next-item prediction 性能 |
| **Method** | Masked History Learning (MHL)：在标准自回归目标上增加辅助任务——重建被 mask 的历史物品；(1) entropy-guided masking policy targeting 最具信息量的物品；(2) 三阶段 curriculum learning 从 history reconstruction 过渡到 future prediction |
| **Benchmark** | Amazon Reviews 2014 — Beauty, Toys and Games, Sports and Outdoors |
| **Result** | 相对 RPG 的 NDCG@10 提升：Beauty +13.5%、Toys +22.6%、Sports +21.1% |
| **Question** | Entropy-guided masking 的计算开销？三阶段 curriculum 各阶段比例如何设定？与 MHL 类似的 masked 目标是否适用于非生成式（判别式）推荐模型？ |

## 详细笔记

### 研究背景与动机

生成式推荐（Generative Recommendation）将 next-item prediction 建模为序列生成任务，通常采用从左到右的自回归（autoregressive）范式，类似 GPT 预测下一个 token。然而：

- 自回归模型在预测时主要依赖 **recent/local context**（最近几个交互）
- 用户行为序列中，**early history** 可能包含长期偏好、周期性模式等深层信号
- 纯自回归目标无法强制模型"理解"整个历史，导致对 distant history 的利用不足

作者来自重庆大学、中科院自动化所等机构，提出 Masked History Learning（MHL），借鉴 BERT 式 masked language modeling 思想，在生成式推荐中引入 history reconstruction 辅助任务。

### 核心方法详解

**MHL 核心组件**：

1. **Masked History Reconstruction（辅助任务）**：
   - 在训练时随机 mask 历史序列中的部分 item
   - 模型需同时完成：(a) 标准 next-item prediction（自回归）；(b) 被 mask 历史 item 的重建
   - 迫使模型关注全序列而非仅 local context

2. **Entropy-Guided Masking Policy**：
   - 非均匀随机 mask：优先 mask **信息量最大** 的历史 item
   - 用 entropy 或类似指标衡量 item 对序列的信息贡献
   - 避免 mask trivial item 导致辅助任务信号弱

3. **Three-Phase Curriculum Learning**：
   - **Phase 1**：侧重 history reconstruction，建立对全序列的理解
   - **Phase 2**：平衡 reconstruction 与 next-item prediction
   - **Phase 3**：侧重 future prediction，微调生成能力
   - 平滑过渡，避免辅助任务干扰主任务

### 实验设置与结果

- **数据集**：Amazon Reviews 2014 三个子集（Beauty、Toys and Games、Sports and Outdoors）
- **基线**：RPG（Representative generative recommendation baseline）及其他序列推荐方法
- **评估指标**：NDCG@10
- **关键结果**（相对 RPG）：
  - Beauty：+13.5%
  - Toys and Games：+22.6%
  - Sports and Outdoors：+21.1%

### 个人思考

MHL 是对生成式推荐中"自回归偏见"问题的直接回应，设计简洁且与 NLP 中 MLM+LM 联合训练的成功经验一致。Entropy-guided masking 是关键创新点——均匀 mask 可能浪费计算在 low-information item 上。三阶段 curriculum 的设定需要消融验证各阶段比例敏感性。与 OneRec-Think（01）、ReRec（03）等生成式推荐工作的关系：MHL 可视为 training objective 层面的增强，可与 reasoning-augmented 架构组合。
