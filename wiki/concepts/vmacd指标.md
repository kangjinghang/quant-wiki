---
title: "VMACD指标"
title_zh: 
type: concept
summary: "将MACD指标计算公式中的价格数据替换为成交量数据，用于反映近期成交量变动趋势的方向和强弱的技术指标。"
tags: [技术面, 量价关系, 择时, 东北金工, 券商研报]
sources: []
  - "[[成交量择时指标-vmacd-mtm]]"
origin: agent-compiled
status: seed
created: 2026-06-04
updated: 2026-06-04
review_by: ""
---
## 定义 / Definition

VMACD指标全称为Vol Moving Average Convergence Divergence。它是一种将经典[[macd指标]]的计算基准从每日收盘价替换为每日成交量后衍生出的技术分析指标。该指标主要用于反映近期成交量变动趋势的方向和强弱情况。

## 方法/机制 / Methodology

VMACD指标的计算过程与MACD完全一致，包含DIF线、DEA线和MACD柱：
- **DIF线**：成交量的快速移动平均线与慢速移动平均线之间的距离。
- **DEA线**：DIF线自身的移动平均线。
- **MACD柱**：DIF线与DEA线的差值。

VMACD指标正向越大，说明近期成交量释放强度较大。然而，直接使用VMACD正负切换进行择时的效果并不理想，因此通常需要结合动量或边际变化进行改进，例如[[vmacd-mtm指标]]。

## 相关概念 / Related Concepts

- [[macd指标]]：VMACD的原始形态。
- [[vmacd-mtm指标]]：基于VMACD动量改进的高效择时指标。
- [[量价关系]]：成交量分析的理论支撑。

## 来源 / Sources

- [[成交量择时指标-vmacd-mtm]]
