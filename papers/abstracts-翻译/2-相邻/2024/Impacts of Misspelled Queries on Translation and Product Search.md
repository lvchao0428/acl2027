# Impacts of Misspelled Queries on Translation and Product Search
> 来源文件：Impacts of Misspelled Queries on Translation and Product Search.pdf
> 发表年份：2024
> 单位：Amazon；Capital One and University of Illinois at Chicago
## 英文原文摘要（Original Abstract）
Machine translation is used in e-commerce to translate second-language queries into the primary language of the store, to be matched by the search system against the product cata- log. However, many queries contain spelling mistakes. We first present an analysis of the spelling-robustness of a population of MT sys- tems, quantifying how spelling variations af- fect MT output, the list of returned products, and ultimately user behavior. We then present two sets of practical experiments illustrating how spelling-robustness may be specifically improved. For MT, reducing the number of BPE operations significantly improves spelling- robustness in six language pairs. In end-to- end e-commerce, the inclusion of a dedicated spelling correction model, and the augmenta- tion of that model’s training data with language- relevant phenomena, each improve robustness and consistency of search results.

## 中文翻译（Chinese Translation）
在电商场景中，机器翻译（MT）用于将第二语言查询翻译为商店的主要语言，以便搜索系统将其与商品目录进行匹配。然而，许多查询包含拼写错误。本文首先分析了一组 MT 系统的拼写鲁棒性，量化了拼写变异如何影响 MT 输出、返回的商品列表以及最终的用户行为。随后，我们展示了两组实践实验，说明如何有针对性地提升拼写鲁棒性。对于 MT，减少 BPE 操作次数可显著提升六个语言对的拼写鲁棒性。在端到端电商系统中，引入专门的拼写纠错模型，以及用语言相关现象增强该模型的训练数据，均可提升搜索结果的鲁棒性和一致性。
