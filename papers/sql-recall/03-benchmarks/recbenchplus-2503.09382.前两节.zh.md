> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

原文件名：recbenchplus-2503.09382.pdf

原文标题：Towards Next-Generation Recommender Systems: a Benchmark for Personalized Recommendation Assistant with LLMs

作者：Jiani Huang、Shijie Wang、Liang-bo Ning、Wenqi Fan†、Shuaiqiang Wang、Dawei Yin、Qing Li†（前四位与 Qing Li 属香港理工大学；Shuaiqiang Wang 与 Dawei Yin 属百度。† 表示通讯作者为 Wenqi Fan 与 Qing Li，计算学系）

场合：WSDM ’26（The Nineteenth ACM International Conference on Web Search and Data Mining），2026 年 2 月 22–26 日，美国 Boise。ACM ISBN 979-8-4007-2292-9/2026/02，DOI 10.1145/3773966.3777954。同时为 arXiv:2503.09382v2 [cs.IR]，2026 年 2 月 2 日。

## 摘要

传统推荐系统多半只覆盖固定、简单的场景，很难在交互式设定里推广到没见过的推荐任务。LLM 把推荐系统推向能对话的个性化推荐助手，但现有研究常用固定的任务提示来生成和评估，常用数据集又缺少能反映真实需求的高质量文本查询，因此评不全。

RecBench+ 用来评估 LLM 处理复杂推荐需求的能力。查询同时覆盖硬条件与软偏好，并有不同难度。作者在常用 LLM 上得到两条结论：这些模型已初步能当推荐助手；明确写出条件的查询更好处理，需要推理或带有误导信息的查询更难。数据在 https://github.com/jiani-huang/RecBenchPlus。

## 正文开篇（无编号，位于第 1 节之前）

正文在编号第 1 节之前有一段没有节号的引言。Related Work 是第 3 节，不在本导读范围内。

引言用 YouTube 首页点击中 60% 来自推荐内容，说明推荐的商业价值，再把传统方法收成矩阵分解：只学用户–物品交互的隐表示，适合 “Customers Who Viewed This Also Viewed” 或 “Based on Your Browsing History” 这类固定场景。Figure 1(a) 画的就是这种范式。像 “1500 美元以内、适合平面设计的耐用笔记本” 这种带细约束的新查询，只靠用户–物品相关性接不住。GPT-o1、DeepSeek-R1、LLaMA 以及 AUTOGLM 这类能理解和规划的系统，促使人们把 LLM 做成交互式推荐助手；LLaRA 的做法是把历史交互直接写成自然语言提示。Figure 1(b) 仍是固定、简单的提示，例如判断用户会不会喜欢某部电影并回答 Yes/No，或从候选列表里选一部。Figure 1(c) 才是本文要评的复杂查询：用户用悬停滑板、时光机等描述回忆一部科幻片，助手要先认出可能是 Back to the Future Part II，再认出男主角 Michael J. Fox，然后推荐他主演的相近电影。这需要多步推理和多条件，超出属性匹配。

LastFM、Amazon Beauty、Movielens-1M 一类常用数据通常只有基本用户信息、物品元数据（如标题）和交互，适合评传统准确率，不适合评 LLM 时代的助手。RecBench+ 由此做成约 30,000 条复杂查询，覆盖多条件、多跳推理、误导信息和多样用户画像，底料包括 Movielens-1M 和 Amazon book。作者用七个常用 LLM 做评测，点名 GPT-4o、Gemini-1.5-Pro、DeepSeek-R1 等，并分析条件个数、是否加入交互历史、以及不同微调范式。引言先报四条发现：模型已能初步充当助手，但擅长点不同，GPT-4o 与 DeepSeek-R1 更擅长条件清楚的查询，Gemini-1.5-Pro 与 DeepSeek-R1 更擅长没有明确条件、但要读懂用户画像的查询；微调明显提升效果，监督微调（SFT）再加强化微调（RFT）的两阶段最好，SFT 先把模型暖起来，RFT 再细修；条件写明的查询更好做，要推理或带扰动的更难，推理能力强的模型在后者上更好；理解用户画像时，表现随兴趣和人口统计变化，流行兴趣更好做，女性用户往往比男性用户更好做。贡献分三条：把 LLM 当作交互式个性化助手这一新范式，并声称是第一个如此整合 LLM 的基准；RecBench+ 公开数据集，就他们所知是第一个能在复杂、重推理设定下评 LLM 推荐助手的公开数据；以及对前沿 LLM 和微调开源模型的实验分析。

## 1 The RecBench+ Benchmark

本节先给基准全貌，再写各类数据怎么造。用户需求被分成两种，对应助手的两种能力。一种由具体条件驱动，例如某导演或某类型的电影，考的是把约束解释并落实。另一种不给条件，只靠用户兴趣、职业、性别等画像做个性化。因此查询分成 Condition-based 与 User Profile-based。Table 1 用 Amazon-Book 和 Movielens-1M；脚注说明与 10M/20M 版本不同，MovieLens-1M 带用户人口统计。

Condition-based 再分三档。Explicit Condition Query 把约束直接写成自然语言，例如 “Can you recommend movies featuring Gwyneth Paltrow?”。Implicit Condition Query 规格不完整，要多跳才能推出条件，例如 “与 Stay Hungry 和 Beethoven 同一位摄影师的电影”，先要推出未写出的名字 David Worth。Misinformed Condition Query 故意带错误，例如把 Avatar 说成 Spielberg 导演，助手应先纠正再推荐。User Profile-based 再分 Interest-based 与 Demographics-based：兴趣是动态偏好，人口统计是性别、职业等更稳定的属性。兴趣类例子是看过 The Tree of Life 和 2046 的人可能偏好独特叙事和视觉，查询只谈语气相近、不写死条件。人口统计例子是哲学教授想看探讨道德困境的电影。

Table 1 印出的规模是：电影 / 图书两侧，查询总数 19,529 / 14,965，用户 6,036 / 48,535，物品 3,247 / 50,088，用户–物品交互 29,459 / 55,424。条件查询按显式、隐式、错误信息，再按条件个数 1、2、以及 3–4 分列。用户画像里，兴趣类为 7,365 / 2,004，人口统计类为 279 / 0，图书侧没有人口统计查询。

构造上，条件查询走知识图谱，因为物品和属性的关系太绕，直接写查询不真实。Figure 2 分三步：建 Item KG、抽共享关系、生成查询。电影 KG 来自 Wikipedia，围绕导演、演员、作曲、类型等 7 类关键属性；图书 KG 用 Amazon Book 元数据，连接作者和类别。再与 Movielens-1M、Amazon-Book 的交互接上。给定用户历史 \(H_u\)，用检索函数找出子集上共享的属性，每条共享关系是 \((r, t)\)，例如 “导演是某人”。显式条件就直接用这些共享关系。隐式条件不写出具体取值，而改成间接指称，例如不说 James Cameron，而说 “The Abyss 的导演”。错误条件则从图谱里抽并不具备该关系的物品，谎称它们有这条关系，例子是声称 Cameron 导演了 Startreck。三类条件都用 GPT-4o 按提示生成自然语言查询。每条样本是查询、去掉正确答案之后的历史，以及满足条件的物品集合作为 ground truth。

用户画像查询见 Figure 3，不要求过滤条件。兴趣类先找 Common Interest Set：在多名用户历史里出现频率不低于阈值 \(\theta\) 的物品序列，阈值是预先设定的，正文没有给出具体数值；再取这些序列之前的物品序列，交给 LLM 归纳共同兴趣并写成查询。文中例子是很多看过 The Dark Knight 的人也看了 Inception，对应动作和悬疑。人口统计类按属性组合分组，例如 18–24 岁学生，找出该组消费最多的物品，连同人口统计一起交给 LLM 写查询，这些热门物品当作 ground truth。最后一小节做过滤：条件查询用字符串匹配，丢掉没把演员、导演等信息写进查询的样本；画像查询人工检查，去掉过宽或不合理的。

## 2 Experiments

实验评的模型是 GPT-4o（2024-08-06）、GPT-4o-mini（2024-07-18）、Llama-3.1-70B-Instruct、Gemini（gemini-1.5-pro-002）、Claude（claude-3-5-sonnet-20241022）、DeepSeek-V3 和 DeepSeek-R1。GPT-o1 没测成，因为提示被判违反使用政策。另外对 Qwen-2.5-3B-Instruct 和 LLaMA-3.2-3B-Instruct 做全参数 SFT，以及基于 GRPO 的 RFT。主实验不在提示里规定推荐条数 \(K\)，固定 \(K\) 的结果放在 2.2 作参照。指标有四项：Precision 是推荐里真正相关的比例；Recall 是相关物品被推荐出来的比例；Condition Match Rate（CMR）是推荐物品里满足给定条件的百分比，用来补 Precision/Recall 看不严的条件对齐；Fail to Recommend（FTR）是模型没能给出推荐的查询比例，一般越低越好，但在错误条件查询里，更高的 FTR 表示模型认出了错误信息、避免给出错误推荐。

条件查询的结果在 Table 2，观察集中在六点。不同模型上，GPT-4o 在电影和图书两侧的平均 Precision 最高、平均 CMR 第二高，DeepSeek-R1 的 Recall 第一、Precision 第二；从显式转到隐式时，DeepSeek-R1 掉得明显更少，并在隐式条件上领先。查询越难，多数模型越差：显式最好，隐式要推断没写明的约束，错误信息最难，Recall 和 CMR 最低；错误条件下更高的 FTR 被解释为模型用常识发现了误导、从而不肯直接推荐。Figure 4 以电影数据看条件个数：条件变多时 Precision 和 Recall 上升，因为候选变窄，例如 “2010 年后 Nolan 的动作片” 比 “Nolan 的电影” 更窄；CMR 在显式查询上下降，因为要同时满足更多约束，在隐式和错误信息查询上上升，因为额外条件提供了更多上下文。Figure 5 显示加入交互历史能在各类查询上提高 Precision，用历史从大候选池里挑更合口味的物品；但 CMR 不一定升，历史会带进干扰项，例如用户历史偏奇幻时，问 Nolan 的电影却推荐 The Prestige。Table 3 是电影数据上要求输出 \(K=5\) 的补充实验，趋势与主实验一致：显式最好，隐式和错误信息依次变差；正文也指出，有些查询的合格物品本来就少于 \(K\)，硬要凑满会变差。微调方面，Table 4 显示 SFT 和 RFT 都明显提高 Recall，但只做 RFT 不如只做 SFT，作者归因于强化探索缺少暖启动。先 SFT 再 RFT 更好：电影显式条件查询上，SFT+RFT 的 Recall 为 0.410，高于只做 SFT 的 0.391 和只做 RFT 的 0.178。

用户画像结果在 2.3，Table 5 标出最优和次优。更大的模型，尤其 Gemini-1.5-Pro 和 DeepSeek-R1，Precision 和 Recall 更高；GPT-4o-mini 这类更小的模型落后。多数模型 FTR 很低，说明它们能按格式给出推荐列表。人口统计查询的 Recall 普遍低于兴趣查询，Precision 则相近：兴趣查询有较清楚的兴趣可循，人口统计要从更宽的群体趋势去推断，更含糊。Figure 6 把兴趣按流行程度分成四组。电影上，被更多用户共享的兴趣 Precision 和 Recall 更高；图书相反，因为流行书常有多个版本或出版社，模型会把版本弄混，例如 Dune 的 1965 年版和 2021 年改编，冷门书变体少，反而更容易精确匹配。Figure 7 显示人口统计上的差异：女性用户准确率更高，文中解释为偏好更稳定，例如浪漫喜剧；50–55 岁的 Recall 更好，偏好更集中、较少被快速变化的流行文化带跑；56 岁及以上不如 50–55 岁，可能因为这个年龄段在网上评分更少，LLM 训练数据里更缺。Table 6 表明，画像查询上两种微调也都有明显收益。
