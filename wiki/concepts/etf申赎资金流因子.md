---
title: "ETF申赎资金流因子"
title_zh: 
type: concept
summary: "基于ETF一级市场申购赎回数据构建的量化因子，涵盖ETF产品、跟踪指数和明细成分股三个维度，总体呈现反转特征。"
tags: [etf, 资金面, 回测, 广发金工, 券商研报, 量化投资, 反转因子]
sources:
  - "[[基于etf申赎的etf轮动策略]]"
origin: agent-compiled
status: seed
created: 2026-06-04
updated: 2026-06-04
review_by: ""
---
## 定义 / Definition

ETF申赎资金流因子（ETF Creation/Redemption Flow Factor）是基于ETF一级市场申赎行为所产生的资金流数据构建的量化因子。该因子利用了ETF独特的双层交易机制，通过追踪份额变动来刻画资金的流入与流出。

## 方法/机制 / Methodology

因子的构建主要基于以下三个数据层级：
1. **ETF维度**：单独统计每只ETF的申赎资金流情况。
2. **指数维度**：将跟踪同一指数的多只ETF资金流数据进行汇总计算。
3. **个股维度**：基于PCF（Portfolio Composition File）清单中的成分股名单及权重，将ETF资金流下沉至具体股票，再进行汇总计算。

在数据类型上，主要分为原始申赎资金流（flow）、资金流相对ETF规模占比（flow2ast）以及资金流相对成交额占比（flow2amt）。数据处理上可采用固定百分位、滚动百分位及周度/月度平滑（ma5/ma21）等加工方式。

## 核心特征 / Characteristics

实证表明，ETF资金流相关因子总体呈现显著的[[反转效应]]，即IC为负。这意味着相对较高资金流入的ETF后续预期有相对较差的市场表现。其中，下沉至个股维度的因子表现最优。此外，由于“救市资金”常通过宽基ETF流入市场，剔除宽基ETF数据后构建的因子（如`stock_flow2amt_ma5`）表现会有显著提升。

## 相关概念

- [[etf交易所交易基金]]
- [[etf轮动策略]]
- [[资金流因子]]
- [[反转效应]]
- [[均值回归]]

## 来源

- [[基于etf申赎的etf轮动策略]]
