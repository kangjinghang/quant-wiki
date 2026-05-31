---
title: "BERT模型"
title_zh: 
type: concept
summary: "Google提出的基于Transformer的双向编码器表征模型，通过MLM和NSP任务进行预训练，在多项NLP任务中取得了突破性进展。"
tags: [机器学习, 另类数据, 深度研究, 券商研报]
sources: []
origin: agent-compiled
status: seed
created: 2026-06-01
updated: 2026-06-01
review_by: ""
---
## 定义 / Definition

BERT（Bidirectional Encoder Representations from Transformers）是Google于2018年提出的预训练语言模型。与单向的自回归模型不同，BERT是一种自编码语言模型，通过深度双向的Transformer架构，能够同时融合上下文信息进行语义理解。

## 预训练任务 / Pre-training Tasks

1. **Masked Language Model (MLM)**：随机遮盖输入中15%的Token，利用上下文预测被遮盖的词，从而实现真正的双向表征。
2. **Next Sentence Prediction (NSP)**：判断两个句子是否在原文中相邻，以捕捉句子级别的关联关系。

## 优势与应用

- **优势**：双向特征融合更完整，适用于文本理解（NLU）任务。
- **应用**：在分类、匹配、阅读理解等下游任务中，只需在预训练模型基础上添加简单的输出层进行微调即可达到SOTA效果。
- **金融应用**：广泛用于金融文本情感分析、研报挖掘等场景。

## 相关概念

- [[Transformer]]
- [[预训练语言模型]]
- [[自然语言处理]]

## 来源

- [[NLP综述：勾勒AI语义理解的轨迹]]
