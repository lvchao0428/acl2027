# OPeRA: A Dataset of Observation, Persona, Rationale, and Action for Evaluating LLMs on Human Online Shopping Behavior Simulation

| 项目 | 内容 |
|------|------|
| **Paper** | OPeRA: A Dataset of Observation, Persona, Rationale, and Action for Evaluating LLMs on Human Online Shopping Behavior Simulation |
| **Authors** | Ziyi Wang, Yuxuan Lu, Wenbo Li, Amirali Amini, Bo Sun, Yakov Bart, Weimin Lyu, Jiri Gesi, Tian Wang, Jing Huang, Yu Su, Upol Ehsan, Malihe Alikhani, Toby Jia-Jun Li, Lydia Chilton, Dakuo Wang |
| **Affiliation** | Northeastern University; USC; Stony Brook University; Ohio State University; University of Notre Dame; Columbia University |
| **Theme** | 用户行为数据集 / 购物行为模拟 / LLM Digital Twin |
| **Problem** | 缺乏高质量公开数据集同时捕捉真实用户的可观察行为和内部推理过程，限制了行为模拟的评估 |
| **Method** | OPeRA 数据集：692 个购物会话、51 个参与者在 Amazon 上的真实购物行为；四维数据：Observation（浏览器状态）、Persona（人口统计/偏好/Big Five/MBTI）、Rationale（自报推理）、Action（细粒度网页操作）。通过浏览器插件 + 问卷收集 |
| **Benchmark** | OPeRA-full（692 会话, 28,904 对）；OPeRA-filtered（527 会话, 5,856 对） |
| **Result** | 首个个性化用户行为模拟评测基准；评测了 GPT-4.1、DeepSeek-R1、Claude-3.7、Llama-3.3。被 AlignUSER 论文用于评估 |
| **Question** | 51 个参与者的多样性是否足以代表广泛的用户群体？浏览器插件的存在是否影响了自然购物行为？ |

## 详细笔记

### 研究背景与动机

LLM 能否准确模拟特定用户的下一步网页操作？虽然 LLM 已展现出生成"可信"人类行为的能力，但评估其模拟真实用户行为的能力仍是一个开放挑战——主要原因是缺乏同时记录用户操作和内部思维的高质量公开数据集。

### 核心方法详解

**数据收集流程**：参与者先填写 Persona 问卷（包含人口统计、购物习惯、消费风格、Big Five 人格、MBTI 等），然后使用定制的 ShoppingFlow Chrome 插件在 Amazon 上正常购物四周，插件在后台记录操作、时间戳、目标元素、HTML、截图和商品元数据。

**四维数据对齐**：每个用户轨迹上同时对齐了 Observation（环境状态）、Persona（长期偏好）、Rationale（即时意图）和 Action（可验证输出）。

### 实验设置与结果

- **数据规模**：OPeRA-full 包含 692 个购物会话，28,904 个行为对，604 条人类标注的 rationale
- **评测模型**：GPT-4.1、DeepSeek-R1、Claude-3.7、Llama-3.3
- **被 AlignUSER 等论文采用为评测基准**

### 个人思考

OPeRA 的最大价值在于同时捕捉了"用户做了什么"和"用户为什么这样做"。此前的电商数据集大多只保留聚合结果（点击、购买），丢失了页面上下文和用户内部原因。四维信号的对齐为构建真正的 LLM Digital Twin 奠定了数据基础。与 ShopSimulator 互补：后者提供训练环境，OPeRA 提供真实用户数据。
