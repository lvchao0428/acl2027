# ACL 2026 推荐系统方向论文调研

## 📋 项目概述

本项目基于 [ACL 2026 主会议录用论文分类总结报告](https://4m0egkrxk1e0j.aiforce.cloud/app/app_17dqnauys1t) 中推荐系统（Recommendation）方向的论文，进行系统化的论文调研、下载和阅读笔记整理。

- **论文来源**：[ACL 2026 Accepted Papers](https://2026.aclweb.org/program/accepted_papers/)
- **研究方向**：推荐系统（Recommendation Systems）
- **论文数量**：20 篇

## 📂 项目结构

```
acl2027/
├── README.md                              # 本文件
├── papers/
│   └── recommendation/                    # 论文 PDF（20 篇）
│       ├── 01_OneRec-Think.pdf
│       ├── ...
│       └── 20_PreferenceHeads.pdf
├── summaries/                             # 论文阅读笔记（20 篇 + 算力总览）
│   ├── 00_算力需求总览.md
│   ├── 01_OneRec-Think.md
│   ├── ...
│   └── 20_PreferenceHeads.md
└── .cursor/
    └── skills/
        └── paper-research/
            └── SKILL.md                   # 论文调研方法技能
```

## 📑 全部 20 篇论文

### 报告推荐方向核心论文（9 篇，报告中列出）

| # | 论文 | 作者 & 单位 | 子方向 | 算力 | 关键词 |
|---|------|-------------|--------|------|--------|
| 01 | [OneRec-Think](summaries/01_OneRec-Think.md) | Zhanyu Liu 等 · **Kuaishou（快手）** | 生成式推荐 + 推理 | 🔴 | In-Text Reasoning, GRPO, 快手部署 |
| 02 | [BLaIR](summaries/02_BLaIR.md) | Yupeng Hou 等 · **UCSD**; UCLA | 推荐评测 | 🟢 | LLM Semantic Encoder, Benchmark |
| 03 | [ReRec](summaries/03_ReRec.md) | Jiani Huang 等 · **PolyU（香港理工）** | 推荐推理 | 🟡 | Reinforcement Fine-tuning, Reasoning RL |
| 04 | [HARPO](summaries/04_HARPO.md) | Subham Raj 等 · **IIT Patna**; IIIT Allahabad | 对话式推荐 | 🔴 | Agentic Reasoning, Tree Search |
| 05 | [MemRec](summaries/05_MemRec.md) | Weixin Chen 等 · **HKBU**; Rutgers; Snap | Agentic 推荐 | 🟡 | Collaborative Memory, O(1) Propagation |
| 06 | [ROS](summaries/06_ROS.md) | Dongyi Lv 等 · **XJTU**; 高德/阿里巴巴 | 地理推荐 | 🟡 | Spatial Reasoning, Mobility CoT |
| 07 | [Mirroring Users](summaries/07_MirroringUsers.md) | Tianjun Wei 等 · **NTU**; ZJU; SUTD | 用户模拟 | 🟡 | User Simulator, DPO, 3B 超越 GPT-5 |
| 08 | [RecPO](summaries/08_RecPO.md) | Zhongyu Ouyang 等 · **Dartmouth**; ByteDance; Notre Dame | 序列推荐 | 🟢 | Preference Intensity, Temporal Context |
| 09 | [AlignUSER](summaries/09_AlignUSER.md) | Nicolas Bougie 等 · **Woven by Toyota** | 推荐评测 | 🟡 | World Model, A/B Test Correlation |

### ACL 2026 推荐相关扩展论文（11 篇）

| # | 论文 | 作者 & 单位 | 子方向 | 算力 | 关键词 |
|---|------|-------------|--------|------|--------|
| 10 | [PURPLE](summaries/10_PURPLE.md) | Linfeng Du 等 · **McGill**; Mila; MBZUAI; Salesforce | 个性化推荐 | 🟢 | Contextual Bandits, RAG Personalization |
| 11 | [PtE](summaries/11_PtE.md) | Song-Li Wu 等 · **Tsinghua**; Huawei Noah's Ark; USTC | 表示学习 | 🟡 | ID vs LLM Representation, Profile-then-Embedding |
| 12 | [MHL](summaries/12_MHL.md) | Kaiwen Wei 等 · **Chongqing Univ**; CAS; CityU HK | 生成式推荐 | 🟢 | Masked History Learning, Entropy-guided |
| 13 | [SiPeR](summaries/13_SiPeR.md) | Dongding Lin 等 · **PolyU**; Sichuan Univ | 对话式推荐 | 🟡 | Situated Recommendation, Bayesian Inference |
| 14 | [Visual Inception](summaries/14_VisualInception.md) | Jiachen Qian · **CityU HK** | 推荐安全 | 🔴 | Memory Poisoning, CognitiveGuard |
| 15 | [NovelQR](summaries/15_NovelQR.md) | Powei Chang 等 · **Fudan（复旦）** | 引用推荐 | 🟢 | Novelty, Defamiliarization, Label Agent |
| 16 | [ClusterRAG](summaries/16_ClusterRAG.md) | Gibson Nkhata 等 · **Univ of Arkansas**; Walmart | 个性化 RAG | 🟢 | Collaborative Filtering + RAG, HDBSCAN |
| 17 | [ShopSimulator](summaries/17_ShopSimulator.md) | Pei Wang 等 · **Alibaba（阿里巴巴）** | 购物 Agent | 🟡 | RL Shopping Agent, Taobao, SFT+RL |
| 18 | [OPeRA](summaries/18_OPeRA.md) | Ziyi Wang 等 · **Northeastern**; USC; Columbia 等 | 行为模拟数据集 | 🟢 | Shopping Behavior, Persona, Rationale |
| 19 | [C-BPO](summaries/19_C-BPO.md) | Xilai Ma 等 · **HIT Shenzhen（哈工大深圳）**; Huawei; NTU | LLM 个性化 | 🟢 | PU Learning, Binary Feedback |
| 20 | [PreferenceHeads](summaries/20_PreferenceHeads.md) | Weixu Zhang 等 · **McGill**; Mila; MBZUAI; Salesforce | 可解释个性化 | 🟢 | Mechanistic Interpretability, Training-free |

## ⚡ 算力需求速览

详细算力分析见 [算力需求总览](summaries/00_算力需求总览.md)

| 级别 | 论文数量 | 论文编号 |
|------|---------|---------|
| 🟢 低（1-2 GPU） | 9 篇 | 02, 08, 10, 12, 15, 16, 18, 19, 20 |
| 🟡 中（4-8× A100） | 8 篇 | 03, 05, 06, 07, 09, 11, 13, 17 |
| 🔴 高（集群级） | 3 篇 | 01, 04, 14 |

## 🔍 研究趋势总结

### ACL 2026 推荐系统方向的六大趋势

1. **推理增强推荐**：OneRec-Think、ReRec、HARPO、ROS 等论文表明，将显式推理（CoT、Tree Search、Spatial Reasoning）引入推荐是主流方向。

2. **Agentic 推荐系统**：MemRec、HARPO、ShopSimulator、Visual Inception 标志着推荐系统从"静态排序"走向"自主 Agent"。

3. **LLM 偏好对齐**：RecPO、Mirroring Users、C-BPO 等将 RLHF/DPO 对齐技术引入推荐场景。

4. **领域专用评测**：BLaIR、AlignUSER、OPeRA、ShopSimulator 反映了推荐评测的专业化趋势。

5. **安全与可信推荐**：Visual Inception 揭示了 agentic 推荐的新安全威胁。

6. **可解释与 Training-free 个性化**：PreferenceHeads/DPS 和 ClusterRAG 探索无需训练的个性化方法，降低落地门槛。

## 📖 阅读建议

1. **入门路径**：BLaIR(02) → OneRec-Think(01) → RecPO(08)
2. **深入推理**：ReRec(03) → HARPO(04) → ROS(06) → MHL(12)
3. **Agentic 方向**：MemRec(05) → ShopSimulator(17) → Visual Inception(14)
4. **评测与对齐**：OPeRA(18) → AlignUSER(09) → Mirroring Users(07) → C-BPO(19)
5. **低算力优选**：ClusterRAG(16) → PreferenceHeads(20) → PURPLE(10) → NovelQR(15)
