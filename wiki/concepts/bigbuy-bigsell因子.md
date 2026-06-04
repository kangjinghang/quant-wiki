---
title: "bigbuy-bigsell因子"
title_zh: 
type: concept
summary: "一种基于Level2数据提取的大单买卖行为特征构建的量化选股或轮动因子。"
tags: [etf, 多因子模型, 券商研报, 广发金工, 量化投资, 量价因子, 资金面, 回测]
sources:
  - "[[基于多因子加权的etf轮动策略]]"
origin: agent-compiled
status: seed
created: 2026-06-04
updated: 2026-06-04
review_by: ""
---
## 定义 / Definition

[[bigbuy-bigsell因子]]是基于Level2行情数据中的大单买入与卖出行为提取的量化因子，用于刻画主力资金或机构资金在个股或ETF层面的交易动向，属于高频量价因子的范畴。

## 方法/机制 / Methodology

该因子通过分析逐笔成交数据中的大买单和大卖单信息，提取资金流的特征。在广发金工的测试中，该因子在股票端和ETF轮动端均表现出较好的预测能力。特别是在ETF多头Top5组合的回测中，该因子的收益表现相对较高，但在不同年度之间的特征存在差异化。

## 相关概念 / Related Concepts

- [[大单资金流]]
- [[高频量价因子]]
- [[etf轮动策略]]
- Level2行情数据（逐笔成交数据）

## 来源 / Sources

- [[基于多因子加权的etf轮动策略]]
