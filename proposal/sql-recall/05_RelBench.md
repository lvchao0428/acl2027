# RelBench

> 2026-11-11 核对。数字来自当天打开的论文、榜单或官方代码。
> 总览和先导实验在 [00_总览](00_总览.md)。

## 没人做过这件事

推荐任务是时间链接预测：给定源实体和种子时间，对目标实体排 top-K。标签用 DuckDB SQL 构造，看的是种子时间之后的一个窗口。模型输入不是自然语言。`pip install relbench`，表是 parquet，可以用 DuckDB 直接查。项目页在 [star-project.stanford.edu/relbench](https://star-project.stanford.edu/relbench/)。

论文表格里的 MAP 是百分数。评测代码和线上榜存的是 0 到 1 的小数，乘 100 才对得上表格。K 不是统一的 10：Amazon、F1、trial 是 10，H&M 和 Avito 是 12，Stack 的两个任务是 100。下面的数字是 v1 表 5 的测试集百分数，ContextGNN 一列来自它自己的表 2，同一套打印。

| 任务 | 全局流行 | 历史访问 | LightGBM | GraphSAGE | ID-GNN | ContextGNN |
|---|---:|---:|---:|---:|---:|---:|
| Amazon 购买 | 0.24 | 0.06 | 0.16 | 0.74 | 0.10 | 2.93 |
| Amazon 打 5 星 | 0.15 | 0.07 | 0.17 | 0.87 | 0.12 | 2.25 |
| H&M 购买 | 0.30 | 0.89 | 0.38 | 0.80 | 2.81 | 2.93 |
| Stack 评论 | 0.02 | 1.42 | 0.04 | 0.11 | 12.72 | 13.34 |

H&M 的标签窗口是 7 天，K=12。Amazon 购买在清单里是 91 天、K=10；论文正文写三个月，描述文字写两年，以 SQL 为准。Amazon 购买的目标实体约 1,260 万，H&M 约 1,340 万，查询必须先限制连接，不能对全表打分。四层 GraphSAGE 在 80GB A100 上会因显存退出，这一臂不跑。

历史访问和全局流行就是两条平凡的 SQL 排序。Amazon 购买上它们是 0.06 和 0.24，ContextGNN 是 2.93。H&M 上历史访问已经 0.89，ID-GNN 2.81，ContextGNN 2.93，协同模型的优势比 Amazon 小。榜上有一格对不上论文：trial 的 ID-GNN，榜是 0.00332 和 0.00137，v1 表 5 是 11.36 和 19.00。比较时用论文表格，不用那一格。

最接近的两件工作都不是「SQL 的执行结果就是推荐」。Kumo 的 Predictive Query Language 能从自然语言写成 `PREDICT LIST_DISTINCT(...) RANK TOP k`，执行器仍是关系模型。RelAgent 让模型写 DuckDB 特征 SQL，再交给树模型，而且做的是实体分类和回归，不是 top-K。RelBench 论文里的人类基线也是数据科学家写特征 SQL 再接 LightGBM，15 个分类和回归任务，每个大约 12 小时，不是一条返回排序的查询。

泄漏规则比「早于或等于」更严：每条预测只能使用时间戳严格早于该行 `time_col` 的记录。特征 SQL 不能看见标签窗口。在全表上算的全局流行，或把测试周并进共现连接，都是错的。
