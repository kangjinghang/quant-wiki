---
title: "LLM-FADT策略"
title_zh: 
type: concept
summary: "一种利用大语言模型（如Qwen3-8b）对分析师文本进行多角度重构，并结合FinBERT与XGBoost构建的增强型文本选股策略。"
tags: [华泰金工, 大语言模型, 文本情感分析, xgboost模型, 深度学习, 券商研报, 深度研究, ai应用, 量化投资, 指数增强策略]
sources: []
  - "[[llm-fadt-大模型增强文本选股]]"
origin: agent-compiled
status: seed
created: 2026-06-04
updated: 2026-06-04
review_by: ""
---
## 定义 / Definition

[[llm-fadt策略]]（Large Language Model - Financial Analysis of Document Text）是[[华泰金工]]提出的一种基于大语言模型增强的文本选股策略。该策略在前期[[bert-fadt策略]]的基础上，利用LLM对原始分析师研报文本进行多角度的推理演绎重构，以提取更深层的增量信息。

## 方法/机制 / Methodology

1. **文本重构（LLM博观视角）**：使用[[qwen3-8b模型]]等大模型，模拟人类阅读时的推理演绎过程，从5个角度重构原始文本：标题新解、行情催化剂、“言外之意”、潜在风险、收益指引。
2. **特征提取**：使用微调版的[[finbert模型]]对原始文本及5类重构文本分别进行语义编码，提取CLS层768维向量作为特征。
3. **模型训练与合成**：采用“先训练后合成”方案。即对6类文本分别训练[[xgboost模型]]，然后将模型预测结果取均值，得到最终的因子值。研究表明该方案优于将特征向量取均值后再训练的“先合成后训练”方案。
4. **组合构建**：可直接构建多头等权组合，或结合基本面、技术面因子构建因子增强Top25组合。针对特定场景（如沪深300指增、行业增强），可通过修改模型训练标签进行定制化优化。

## 相关概念 / Related Concepts

- [[大语言模型]]
- [[bert-fadt策略]]
- [[文本情感分析]]
- [[finbert模型]]
- [[xgboost模型]]
- [[指数增强策略]]

## 来源 / Sources

- [[llm-fadt-大模型增强文本选股]]
