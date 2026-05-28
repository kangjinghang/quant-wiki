---
title: "转债DELTA估计"
title_zh: 
type: concept
summary: "利用二叉树模型计算转债平价价值变动对转债价值变动的影响，平价130以上DELTA接近1，但在深度虚值区域因信用利差设定存在偏误可能。"
tags: [可转债, convertible-bond, 券商研报, 深度研究]
sources: []
origin: agent-compiled
status: seed
created: 2026-05-28
updated: 2026-05-28
review_by: ""
---
## 定义

[[转债DELTA估计]]是利用[[可转债CRR定价模型]]计算的转债价格对正股价格变动的敏感度指标。DELTA = Δ转债价值 / Δ平价价值，用于确定[[转债波动率套利策略]]中对冲比例。

## 特征

- **平价130以上**：DELTA接近1，转债与正股近似同步变动
- **平价100附近**：DELTA约0.5-0.7
- **深度虚值区域**（平价远低于100）：因信用利差设定，DELTA可能存在偏误

## 应用

在[[转债波动率套利策略]]中，DELTA用于计算融券卖出正股或股指期货的对冲数量，确保Beta中性。
