---
title: "时间差Alpha"
title_zh: 
type: concept
summary: "指由日内分钟收益率在时间轴上的涨跌分布位置差异所蕴含的选股信息，其本质是收益率结构和低波效应的综合。"
tags: [high-frequency, factor-investing, a-share, quantitative]
sources: []
origin: agent-compiled
status: seed
created: 2026-06-01
updated: 2026-06-01
review_by: ""
---
## 定义 / Definition

**时间差Alpha**是指股票日内分钟收益率序列中，涨幅和跌幅在时间轴上的分布位置差异所蕴含的超额收益信息。

## 逻辑与来源 / Logic and Origin

虽然涨跌幅的时间重心相对位置具有选股能力，但本文通过详细的实证分析指出，“时间差Alpha”并非一个独立的Alpha源。其真正的收益来源主要包含以下两个方面：

1. **收益率结构**：日内尾盘阶段（如时段7和时段8）的涨跌幅能够正向解释时间差Alpha，而盘初阶段（如时段1和时段2）的涨跌幅则是干扰因素。
2. **低波效应**：日内零涨跌幅分钟数量代表了A股市场的低波效应，这与个股成交活跃度低或盘中触及涨跌停等事件有关，同样能够解释时间差Alpha的收益。

当把上述解释因子和控制变量（如盘中是否触及涨跌停）全部剔除后，“时间差Alpha”将变为近似噪音的信号。

## 相关概念 / Related Concepts

- [[跌幅时间重心偏离因子]]：用于捕捉时间差Alpha的基础因子。
- [[时间重心偏离因子]]：剥离了干扰后的时间差Alpha因子。

## 来源 / Sources

- [[日内分钟收益率的时序特征逻辑讨论与因子增强]]
