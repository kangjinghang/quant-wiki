---
title: "itransformer模型"
title_zh: 
type: concept
summary: "发表于ICLR 2024的倒置Transformer模型，通过将时间序列维度反转，利用自注意力机制捕捉多变量时间序列中变量间的相关性。"
tags: [华泰金工, 深度研究, 深度学习, transformer模型, 大语言模型, 高频量价因子, 指数增强策略, 注意力机制, 市场微观结构, 量化投资]
sources:
  - "[[多角度改进高频量价选股模型]]"
origin: agent-compiled
status: seed
created: 2026-06-04
updated: 2026-06-04
review_by: ""
---
## 定义 / Definition
iTransformer（Inverted Transformer，倒置变换器）是一种创新性的时间序列预测模型，发表于2024年的ICLR会议。其核心思想是将传统Transformer应用于时间序列时的维度进行反转处理。

## 方法/机制
传统Transformer在处理多变量时间序列时，通常将每个时间步的特征作为一个token。而iTransformer则将每个变量的完整时间序列嵌入为一个独立的token。
- **变量间注意力**：通过自注意力机制（Self-Attention）捕捉不同变量之间的相关性和依赖关系。
- **非线性表示**：利用前馈网络（Feed-Forward Network）学习每个变量时间序列的非线性表示。

这种设计使得iTransformer能够更好地处理多变量时间序列中的复杂依赖关系，同时有效避免了传统Transformer在处理长序列时可能出现的性能下降和计算爆炸问题。

## 应用
在量化投资领域，iTransformer被用于[[多角度改进高频量价选股模型|高频量价选股模型]]的改进。[[华泰金工]]的研究表明，iTransformer在处理多因子时间序列数据时，能够有效捕捉因子间的交互作用，其训练得到的因子在RankICIR和多头信息比率上均优于传统[[transformer模型]]。

## 相关概念
[[transformer模型]], [[crossformer模型]], [[注意力机制]], [[深度学习]], [[高频量价因子]]

## 来源
- [[多角度改进高频量价选股模型]]
