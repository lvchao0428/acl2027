> 版权声明：本文档为对应英文论文前两节的中文导读，仅供论文快速阅读使用。不替代原文，不构成对原文的完整翻译或再发表。原文版权归作者与出版方所有。

原文标题：AgentRecBench: Benchmarking LLM Agent-based Personalized Recommender Systems

作者：Yu Shang、Peijie Liu（首页标注同等贡献）、Yuwei Yan、Zijing Wu、Leheng Sheng、Yuanqing Yu、Chumeng Jiang、An Zhang、Fengli Xu、Yu Wang、Min Zhang、Yong Li。单位脚注为 Tsinghua University、The Hong Kong University of Science and Technology (Guangzhou)、University of Science and Technology of China、National University of Singapore。

场合：Preprint，arXiv:2505.19623v2 [cs.IR]，28 May 2025。首页脚注给出 AgentSociety Challenge 页面：https://tsinghua-fib-lab.github.io/AgentSocietyChallenge/pages/overview.html

PDF：agentrecbench-2505.19623.pdf

## Abstract

摘要把 LLM 驱动的 agentic recommender system 写成个性化推荐的范式变化：系统借助推理和角色扮演做自主、可自适应的决策，并能从复杂环境里动态收集、解释用户与物品的交互，形成可跨场景泛化的策略。作者认为缺的是标准化评测协议，并给出三件东西。第一，交互式文本推荐模拟器，纳入用户与物品元数据，并设置 classic、evolving-interest、cold-start 三种任务。第二，一套用于开发和研究这类系统的统一模块化框架。第三，据称首次把 10 种 classical 与 agentic 推荐方法放在一起比较的综合基准。摘要层面的结论是 agentic 系统更优，同时给出核心组件的可操作设计准则。基准已用一场公开挑战验证，环境公开且排行榜持续维护；数据放在 Hugging Face：https://huggingface.co/datasets/SGJQovo/AgentRecBench 。

## 1 Introduction

这一节的推进顺序是：先写推荐系统已有的三类缺口，再写 LLM agent 为什么能补上，然后用四项贡献定义 AgentRecBench，最后用一场公开挑战的规模数字说明基准可用。

推荐系统被放在缓解网页信息过载的位置上，路线从基于规则走到数据驱动的深度学习，准确率和效率已经有明显进展。作者仍列出三点未解决问题：推荐是黑箱，结果难解释；方法主要依赖历史交互，用不上真实应用里的丰富上下文；特征多靠手工、策略固定，换场景时适应差。

转折来自 LLM-based agent。这类智能体可以做类人的规划、反思式推理和迭代行动，因此被说成有机会改写推荐范式。相对传统推荐，正文强调三条能力：用自然语言把推荐逻辑说出来，以提高透明度和用户信任；主动从环境里搜集个性化上下文，使用户建模超出基于 ID 的交互；把外部反馈和内部记忆纳入策略，在与环境的交互中持续自我改进，从而跨场景适应。

空白被收成一句：没有标准化基准，就难以判断这些方法是否有效、能否部署。AgentRecBench 在这里被定义为首个面向 agentic recommender 的综合基准。正文数出四项贡献，比摘要的三条更细。

第一项是统一的文本交互环境，数据来自 Yelp、GoodReads 和 Amazon。环境提供标准化函数接口，智能体可以在不同条件下检索，同时维护一个多领域数据库。第二项是三种评测场景：classic 看一般性能，evolving-interest 看动态适应，cold-start 看泛化；作者说三者合在一起对应真实推荐的核心困难。第三项是带认知组件的模块化智能体框架，用来快速搭建系统。四个模块分别是 dynamic planning（任务分解）、complex reasoning（决策）、tool utilization（与环境交互）和 memory management（保留并使用经验）。第四项是对 10 种现有推荐智能体与传统方法的评测；分析要抽出当前能力与局限，并由此给出设计准则。摘要里的 “10 classical and agentic recommendation methods” 与这里的 “10 existing recommendation agents and traditional methods”、节末的 “10 approaches” 指的是同一组比较对象，这一节没有列出具体方法名单。

实用性靠 AgentSociety Challenge 的数字支撑：竞赛 37 天，全球 295 支队伍，提交超过 1,400 份。Recommendation Track 在 Development Phase 的性能提升为 20.3%，Final Phase 再提高 15.9%。完整环境和持续维护的排行榜保持公开。

节末把贡献收成三条：跨多种场景、同时覆盖新兴 agentic 方法与传统方法的大规模基准；带多领域数据和标准智能体开发框架的文本环境模拟器，形成开发与评测的闭环，便于快速原型和系统测试；对 10 种方法的分析给出可执行的设计准则。这一节没有表。

## 2 Definition of Agentic Recommender System

这一节只做形式化定义。Agentic recommender 被写成一个 LLM-based agent 与环境交互并产出推荐。环境是三元组 \(E = (U, I, H)\)：\(U\) 和 \(I\) 分别是用户、物品特征空间；历史交互 \(H = \{(u, i, c, \tau)\}\)，\(c\) 是上下文元数据，文中举例为 ratings 和 comments，\(\tau\) 是时间戳。

每一步 \(t\)，智能体观察状态 \(s_t \in S\)。状态编码用户与物品画像、交互以及其他环境反馈。动作 \(a_t \in A\) 由策略 \(\pi_\theta\) 选出。式 (1) 写成 \(a_t \sim \pi_\theta(a \mid s_t)\)，并且 \(\pi_\theta : S \rightarrow p(A)\)。\(p(A)\) 是动作空间上的概率分布。动作空间 \(A = I \cup A_{\mathrm{seek}}\)，一部分是物品推荐，一部分是信息寻求动作。参数 \(\theta\) 对应内部功能模块，文中点名 reasoning 和 memory。

式 (1) 与后面的解释之间，版面插入 Figure 1，图题是交互式文本环境模拟器的总体框架。图中可见 User、Review、Item、推荐智能体、两个 Scenario，以及文本实验环境中的网络构建和查询。本节正文没有解释这张图的机制；图在后文被再次指向，这里只记录它已经印在第 2 节的版面里。

定义之后，作者用三点把该系统与传统方法分开。第一，它能自适应地从环境收集个性化上下文，同时在多种场景里保持可泛化、zero-shot 可适应的推荐策略。第二，它能靠积累的经验和外部反馈不断改内部表示与决策策略，从而自我改进、持续提高性能。第三，它有望策略性地主动发起有目标的交互，以增强主动参与，而不仅停留在被动响应。本节到此结束，没有表，也没有实验数字。第 3 节起进入文本环境模拟器，本导读不展开。
