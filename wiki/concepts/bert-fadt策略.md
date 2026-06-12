---
title: "BERT-FADT策略"
title_zh: 
type: concept
summary: "华泰金工前期提出的文本选股策略，利用FinBERT提取研报文本语义向量，并通过XGBoost模型学习其中的超额收益信息。"
tags: [华泰金工, 大语言模型, 文本情感分析, xgboost模型, 深度学习, 券商研报, 深度研究, ai应用, 量化投资, 指数增强策略]
sources:
  - "[[llm-fadt-大模型增强文本选股]]"
origin: agent-compiled
status: seed
created: 2026-06-04
updated: 2026-06-04
review_by: ""
---
## 定义 / Definition

[[bert-fadt策略]]是[[华泰金工]]在前期报告《人工智能63：再探文本FADT选股》中提出的选股策略。该策略以分析师研报文本的语义向量（词频向量或[[finbert模型]]隐藏层编码特征向量）为基础，以研报发布前后两日个股超额收益为标签，引导[[xgboost模型]]学习研报文本中蕴含的超额信息。

## 方法/机制 / Methodology

1. **文本编码**：使用微调的FinBERT模型对分析师研报文本进行语义编码，提取隐藏层特征向量。
2. **收益预测**：将文本特征向量输入XGBoost模型，通过滚动训练的方式（如过去6个月为样本内，未来12个月为样本外），预测个股未来的超额收益。
3. **局限性**：尽管BERT模型在文本解析领域表现出色，但其主要基于Transformer的Encoder部分，在文本生成和深层推理演绎方面存在局限，这为后续引入基于Decoder架构的[[大语言模型]]（如[[llm-fadt策略]]）提供了改进空间。

## 相关概念 / Related Concepts

- [[llm-fadt策略]]
- [[finbert模型]]
- [[xgboost模型]]
- [[文本情感分析]]
- [[分析师预期因子]]

## 来源 / Sources

- [[llm-fadt-大模型增强文本选股]]
