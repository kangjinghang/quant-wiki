---
title: "MACD指标"
title_zh: 
type: concept
summary: "一种用于判断价格趋势方向和强弱的经典技术指标，通过快速均线与慢速均线的聚合与分离来发出交易信号。"
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

MACD指标（Moving Average Convergence Divergence，指数平滑异同移动平均线）是金融市场中最经典的技术指标之一，主要用于判断价格趋势的方向和强弱。

## 方法/机制 / Methodology

MACD指标的表现形式通常为两条曲线（DIF线与DEA线）和一组MACD柱：
- **DIF线**：反映了快速移动平均线与慢速移动平均线之间的距离。DIF线上行说明快慢均线距离正向扩大，反之亦然。
- **DEA线**：DIF线自身的移动平均线，用于辅助判断DIF线的走势。
- **MACD柱**：DIF线与DEA线的差值。数值越大，说明近期DIF线的趋势越强。

传统的MACD择时逻辑为：MACD由负变正买入，由正变负卖出。但这种基于零轴交叉的策略存在明显的滞后性，容易错过最佳入场或退出时机。在量价分析中，常将其变体[[vmacd指标]]结合动量使用（如[[vmacd-mtm指标]]）以提升效果。

## 相关概念 / Related Concepts

- [[vmacd指标]]：MACD在成交量上的应用变体。
- [[vmacd-mtm指标]]：解决MACD类指标滞后性的动量改进方案。
- [[均线系统]]：MACD的底层计算基础。
- [[技术面]]：指标所属的分析维度。

## 来源 / Sources

- [[成交量择时指标-vmacd-mtm]]
