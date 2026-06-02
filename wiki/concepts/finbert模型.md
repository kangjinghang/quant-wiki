---
title: "FinBERT模型"
title_zh: 
type: concept
summary: "由熵简科技开源的、在大规模金融领域语料上预训练的中文BERT模型，在金融情绪分类等下游任务中性能优于原版BERT。"
tags: [机器学习, 另类数据, 深度研究, 券商研报, ai应用, 量化]
sources: []
  - "[[再探文本fadt选股]]"
origin: agent-compiled
status: developing
created: 2026-06-01
updated: 2026-06-02
review_by: ""
---
## 定义 / Definition

FinBERT是一款专门针对金融领域训练的自然语言处理（NLP）预训练模型，由熵简科技于2020年末开源。它基于Google的BERT架构，但在大规模金融语料上进行了预训练，使其在处理金融文本（如研报、财经新闻）时比通用BERT模型具有更强的语义理解能力。

## 方法/机制 / Methodology

FinBERT的预训练语料主要包括金融财经类新闻（约100万篇）、研报及上市公司公告（约200万篇）以及金融类百科词条（约100万条），总计约30亿Tokens。其预训练任务分为两类：
1. **字词级别预训练**：包括Financial Whole Word Mask（全词掩码预测）和Next Sentence Prediction（下一句预测）。
2. **任务级别预训练**：包括研报行业分类（文档级有监督任务）和财经新闻的金融实体识别。

在量化选股应用中，通常使用带标注的舆情数据对FinBERT进行微调，以提升其对特定金融场景文本的表征能力。

## 相关概念

- [[自然语言处理]]
- [[bert模型]]
- [[文本情感分析]]
- [[机器学习]]

## 来源

- [[再探文本FADT选股]]
