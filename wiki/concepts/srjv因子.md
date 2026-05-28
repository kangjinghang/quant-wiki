---
title: "SRJV因子"
title_zh: 
type: concept
summary: "小程跳跃波动因子，衡量股价微小跳跃的波动水平，周度因子（SRJV_week）在实证中表现出极高的IC和多空收益。"
tags: [high-frequency, factor-investing, a股, 券商研报, 深度研究]
sources: []
origin: agent-compiled
status: seed
created: 2026-05-29
updated: 2026-05-29
review_by: ""
---
## 定义 / Definition

SRJV因子（Small Realized Jump Volatility）即小程跳跃波动因子，代表股价在日内高频数据中发生的幅度较小的跳跃波动总和。它是[[跳跃波动因子]]按大小维度拆分的重要子类。

## 方法/机制 / Methodology

该因子通过设定特定的阈值参数（如α=4），将日内收益率中绝对值小于阈值的跳跃部分进行平方和计算得出。在A股实证中，周度频率的SRJV_week因子表现最为优异。经过行业市值中性化后，该因子全历史IC均值达到-8.76%，年化ICIR为-8.91，扣费后多空年化收益达45.97%，夏普比率为4.40。此外，该因子与主要风格因子相关性极低，IC半衰期约为1周。

## 相关概念 / Related Concepts

- [[跳跃波动因子]]
- [[SRLJV因子]]
- [[高频量价因子]]

## 来源 / Sources

- [[基于股价跳跃模型的因子研究-高频数据因子研究系列九]]
