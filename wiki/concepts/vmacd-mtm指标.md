---
title: "VMACD_MTM指标"
title_zh: 
type: concept
summary: "一种基于成交量变动趋势的动量择时指标，通过对VMACD指标进行Z-score标准化并计算其N日累计变动值来生成交易信号。"
tags: [技术面, 量价关系, 择时, 东北金工, 券商研报]
sources:
  - "[[成交量择时指标-vmacd-mtm]]"
origin: agent-compiled
status: seed
created: 2026-06-04
updated: 2026-06-04
review_by: ""
---
## 定义 / Definition

VMACD_MTM（Vol Moving Average Convergence Divergence Momentum）是一种基于成交量数据的动量择时指标。它通过计算VMACD指标在一定时间窗口内的累计变化量（即动量），来刻画近期成交量放量或缩量势头的变化，从而捕捉价格变动的择时信号。

## 方法/机制 / Methodology

1. **基础指标计算**：将传统[[macd指标]]计算过程中的每日收盘价替换为每日成交量，得到[[vmacd指标]]。
2. **标准化处理**：对VMACD指标进行Z-score标准化，以消除绝对数值过大的影响并统一阈值标准。
3. **动量计算**：计算标准化后VMACD的每日差值（VMACD_diff），并对其取N日累加，得到VMACD_MTM。
4. **信号生成**：设定阈值T（默认T=1）。若VMACD_MTM > T，则持仓；若VMACD_MTM < -T，则空仓；若介于-T与T之间，则维持当前状态不变。

该策略在参数组合（N=60, T=1）下表现最为出色，其本质是捕捉了成交量在季度级别上的趋势性变动。

## 相关概念 / Related Concepts

- [[vmacd指标]]：VMACD_MTM的基础计算底座。
- [[macd指标]]：经典的价格趋势指标，VMACD的构造原型。
- [[量价关系]]：该指标的理论基础，利用成交量的放量预期来推断价格走势。
- [[择时]]：该指标的核心应用场景。
- [[技术面]]：属于技术分析与趋势跟踪的范畴。

## 来源 / Sources

- [[成交量择时指标-vmacd-mtm]]
