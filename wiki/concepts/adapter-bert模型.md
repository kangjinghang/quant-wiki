---
title: "Adapter-BERT"
title_zh: 
type: concept
summary: "一种高效的BERT微调技术，通过在Transformer层中插入少量参数的Adapter模块，将微调参数量从上亿降至数百万，同时基本保持模型性能。"
tags: [机器学习, 另类数据, 深度研究, 券商研报, ai应用, 量化]
sources: []
origin: agent-compiled
status: seed
created: 2026-06-01
updated: 2026-06-01
review_by: ""
---
## 定义 / Definition

Adapter-BERT是一种针对大规模预训练语言模型（如BERT）的高效微调技术，发表于2019年机器学习顶级会议ICML。该技术旨在解决预训练模型全参数微调时计算资源消耗过大的问题。

## 方法/机制 / Methodology

在BERT的每个Transformer层内（通常位于全连接层之后）添加Adapter模块。该模块主要包含一个下采样全连接层和一个上采样全连接层，并配有残差连接。在微调过程中，模型原有的庞大参数（灰色模块）被冻结，仅训练新增的Adapter模块参数（绿色模块）。这种方法将可调参数量减少到预训练模型总参数量的3%左右（例如从上亿参数降至约三百万），大幅提升了训练效率。

## 相关概念

- [[finbert模型]]
- [[自然语言处理]]
- [[机器学习]]

## 来源

- [[再探文本FADT选股]]
