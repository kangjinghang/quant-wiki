---
title: "Delta对冲"
title_zh: 
type: concept
summary: "一种通过买入或卖出标的资产来对冲期权头寸中性化风险的交易策略，使投资组合免受标的资产价格小幅变动的影响。"
tags: [广发金工, 券商研报, 套利, etf, 回测, 深度研究]
sources: []
  - "[[基于etf的自动赎回型期权产品收益复制策略]]"
origin: agent-compiled
status: seed
created: 2026-06-02
updated: 2026-06-02
review_by: ""
---
## 定义 / Definition

[[delta对冲]]（Delta Hedging）是一种期权对冲策略。记期权（或自动赎回型产品）价值为 $V$，标的资产价格为 $S$，Delta即为 $V$ 相对 $S$ 的导数 $\frac{\partial V}{\partial S}$。

## 机制与原理 / Mechanism

发行方在发行产品后，其头寸为 $-V$。为了对冲风险，发行方需买入 Delta 份标的资产，使得整个组合不受标的资产价格微小变化的影响。对冲后的头寸价值变为 $-V + \text{Delta} \times S$。

在动态对冲过程中：
- 标的资产价格下跌时，|Delta| 上升，发行方需买入更多标的资产。
- 标的资产价格上升时，|Delta| 下降，发行方会卖出部分标的资产。

## 收益复制策略 / Replication Strategy

利用该原理，假设未实际发行产品，直接对标的ETF进行对应Delta的动态买卖，即可构建一个理论上价值与产品相近的头寸。通过蒙特卡洛模拟法计算每日Delta，并据此调整ETF仓位，可以复制出类似自动赎回型产品的收益特征。

## 相关概念

- [[自动赎回型期权产品]]
- [[回测]]
- [[算法交易]]

## 来源

- [[基于etf的自动赎回型期权产品收益复制策略]]
