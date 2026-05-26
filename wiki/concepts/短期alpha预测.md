---
title: "短期Alpha预测"
title_zh: 
type: concept
summary: "Short Alpha，用于A-VWAP算法和日内交易的短期价格方向判断，每3秒（1个Snapshot）给出方向预测，n=30时获取约14bps超额收益。"
tags: []
sources: []
origin: agent-compiled
status: seed
created: 2026-05-27
updated: 2026-05-27
review_by: ""
---
## Definition / 定义

短期Alpha预测（Short Alpha Prediction）是在极短时间尺度（秒级）上对价格方向进行判断的预测模型。每3秒（1个Snapshot）给出一个价格方向判断，应用于[[算法交易]]中的A-VWAP和[[日内程序化交易]]。

## 应用场景

### A-VWAP算法
- 融入Short Alpha方向判断的加权算法
- 在n=30时能获取约14bps的超额收益

### 日内交易
- 为日内T0策略提供微观方向信号
- 与[[多时间序列模型]]结合使用

## 算法交易演进中的位置

| 阶段 | 方法 | Short Alpha |
|------|------|------------|
| H-VWAP | 历史成交量加权 | 无 |
| D-VWAP | 动态预测加权 | 无 |
| A-VWAP | 融入方向预测 | **有** |

## 来源

[[张红庆]]在[[丽海弘金]]的实践中应用，详见[[张红庆高频交易成交数据的挖掘与基于机器学习的策略优化]]。[[TCA]]用于评估其绩效。

## Related

- [[算法交易]] — 核心应用场景
- [[TCA]] — 绩效评估框架
- [[日内程序化交易]] — 相关策略
