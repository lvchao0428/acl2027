# 五步重析

五步之后的去重和网格见 [00_五步之后的网格.md](00_五步之后的网格.md)。

- [01 Text-to-SQL](01_Text-to-SQL.md)：按 PDF 重读 `01-text-to-sql` 的 22 篇；TAG 用 CIDR 版，SUQL 的字节相同副本不另写。
- [窗口 01 重核](window-01.md)：2026-11-11 按大纲五问从 PDF 重抄数字后的选题稿。BiomedSQL 的 40 个模板和专家 90.0 在 PDF 里还在。
- [03 候选 benchmark](03_benchmark.md)：03-benchmarks 八篇五步重析。主实验仍是 STaRK-Amazon；不得把合成集上的纯 SQL 集合召回，或 RecBench+ 历史子集 Precision，当主指标。QUEST 归指标路线，未在此重析。
- [04 指标](04_指标.md)：04-metrics 的 21 篇五步重析。主表可放检索指标、显式谓词匹配、温度 0 的字符串一致和结果集 Jaccard；必须丢掉 LIMIT 当推荐结果、一般的 30% 跌幅，以及 SQL 是忠实解释。
- [05 RelBench](05_RelBench.md)：会议版 v1（arXiv 只点名）、v2、ContextGNN、Fey、Wydmuch、RelAgent、ReFuGe。H&M 上成立的是特定成对 GNN 超过流行度与自身历史；手写共现是漏掉的经典基线，这组不能当 ACL 语言实验。
- [窗口 05](window-05.md)：按大纲重读七篇 PDF 之后的选题报告。格子与上一份一致；覆盖率上界和停点以这一份为准。
- [02 召回](02_召回.md)：`02-recall` 的 24 篇五步重析（SIEVE 两份只留 arXiv）。没有一篇已经占住「大模型写协同 SQL 自连接」；InteRecAgent 的 SQL 被提示禁止用来找相似物品。
