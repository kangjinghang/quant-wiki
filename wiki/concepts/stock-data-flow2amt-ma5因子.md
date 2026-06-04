---
title: "stock-data-flow2amt-ma5因子"
title_zh: 
type: concept
summary: "一种结合资金流与成交额特征，并经过5日移动平均处理的量化因子。"
tags: [etf, 多因子模型, 券商研报, 广发金工, 量化投资, 量价因子, 资金面, 回测]
sources: []
  - "[[基于多因子加权的etf轮动策略]]"
origin: agent-compiled
status: seed
created: 2026-06-04
updated: 2026-06-04
review_by: ""
---
## 定义 / Definition

[[stock-data-flow2amt-ma5因子]]是一个结合了资金流数据与成交额特征，并通过5日移动平均（MA5）进行平滑处理的量化因子。该因子旨在捕捉资金流动与市场交投活跃度共振带来的Alpha收益。

## 方法/机制 / Methodology

该因子通过计算资金流指标与成交额的比率或相关性，并进行时序平滑处理以降低噪音。在ETF轮动回测中，该因子的多头Top5组合表现出较高的年化收益率，是构建多因子ETF轮动策略的有效低频价量类因子之一。

## 相关概念 / Related Concepts

- [[资金流因子]]
- [[量价因子]]
- [[etf轮动策略]]

## 来源 / Sources

- [[基于多因子加权的etf轮动策略]]
