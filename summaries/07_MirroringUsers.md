# Mirroring Users: Towards Building Preference-aligned User Simulator with User Feedback in Recommendation

| 项目 | 内容 |
|------|------|
| **Paper** | Mirroring Users: Towards Building Preference-aligned User Simulator with User Feedback in Recommendation |
| **Authors** | Tianjun Wei, Huizhong Guo, Yingpeng Du, Zhu Sun, Huang Chen, Dongxia Wang, Jie Zhang |
| **Affiliation** | Nanyang Technological University (NTU); Zhejiang University; Singapore University of Technology and Design (SUTD) |
| **Theme** | 用户模拟 / 推荐系统评测 / LLM 偏好对齐 |
| **Problem** | LLM 作为用户模拟器缺乏推荐场景的任务对齐，且大规模模拟的效率不足；大量用户反馈数据虽可用但存在歧义性、噪声和海量体量的挑战 |
| **Method** | UserMirrorer 框架：(1) 利用 LLM 生成 EKB 决策过程作为解释性 rationale，降低歧义；(2) 基于不确定性估计和行为采样的数据蒸馏，筛选 10K 高质量样本；(3) 对 Llama-3.2-3B 进行 SFT + DPO 微调 |
| **Benchmark** | 8 个领域：MIND, Amazon, MovieLens, Steam, Goodreads, MobileRec, LastFM, KuaiRec2 |
| **Result** | 3B 微调模型在用户行为预测上超越 GPT-5 和 Gemini-3.0，覆盖 8 个领域 |
| **Question** | EKB 决策模型是否适用于所有推荐领域？10K 样本量的选择依据是什么？ |

## 详细笔记

### 研究背景与动机

用户模拟对推荐系统的开发和评估至关重要。LLM 为用户行为模拟提供了新可能性，但面临任务对齐不足和效率瓶颈两大挑战。推荐系统中积累的海量用户反馈是潜在的对齐资源，但直接利用面临歧义性、噪声和数量巨大等问题。

### 核心方法详解

**阶段一：决策过程生成**：将 8 个领域的推荐日志重写为统一模拟场景 X = Prompt(M, L)，使用 LLM 基于 EKB 消费者决策模型生成显式推理过程。

**阶段二：数据蒸馏**：使用强模型（Qwen2.5-32B）和弱模型（Llama-3.2-3B）各采样 10 个决策过程，识别"hard samples"（强模型解释好但弱模型失败），通过 rejection sampling 去噪，蒸馏出 10K 高质量 SFT/DPO 训练数据。

**模型训练**：对 Llama-3.2-3B 先 SFT 再 DPO，得到 3B 参数部署级用户模拟器。

### 实验设置与结果

- **数据集**：8 个领域（新闻、电商、电影、游戏等）
- **关键结果**：3B 微调模型全面超越 GPT-5 和 Gemini-3.0；模型和数据集已在 GitHub 和 HuggingFace 公开

### 个人思考

核心洞察是"用少量高质量数据对齐小模型，效果好于直接使用大模型"。3B 模型超越 GPT-5 的结果说明在垂直领域，精准的数据比模型规模更重要。与 AlignUSER 形成互补：后者关注"如何评估用户模拟的真实性"，本文关注"如何构建更好的用户模拟器"。
