---
title: "forecast_adj_txt_bert因子"
title_zh: 
type: concept
summary: "华泰金工提出的基于FinBERT编码的分析师盈利预测调整文本因子，通过提取研报的CLS层向量结合XGBoost训练构建，相比词频版因子具有显著的超额收益提升。"
tags: [机器学习, 另类数据, 深度研究, 券商研报, ai应用, 量化]
sources: []
origin: agent-compiled
status: developing
created: 2026-06-01
updated: 2026-06-01
review_by: ""
---
## 定义 / Definition

`forecast_adj_txt_bert`因子是华泰金工在分析师盈利预测调整场景下构建的升级版文本选股因子。该因子使用FinBERT模型的隐藏层编码替代传统的词频向量，以更充分地捕捉研报文本中的上下文语义信息。

## 方法/机制 / Methodology

该因子的构建流程主要包括三个步骤：
1. **FinBERT微调**：使用万得新闻舆情文本对FinBERT进行微调，使其分类准确率达到95%以上。
2. **文本语义编码**：将预处理过的分析师研报文本输入微调后的FinBERT，提取[CLS]标识符对应的768维特征向量作为研报的表征。
3. **XGBoost二次训练**：将768维特征向量作为输入，以研报发布前后两天个股相对中证500的超额收益分类（上涨/震荡/下跌）为标签，训练XGBoost模型。最终通过计算上涨和下跌类别的log-odds值之差得到文本得分，并合成个股截面因子值。

## 相关概念

- [[finbert模型]]
- [[XGBoost模型]]
- [[文本情感分析]]
- [[另类数据]]

## 来源

- [[再探文本FADT选股]]
