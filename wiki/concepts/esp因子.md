---
title: "ESP因子"
title_zh: "ESP因子（超预期幅度）"
type: concept
summary: "Earnings Surprise Percent，直接衡量业绩超预期幅度的因子。年报用公布值与一致预期之差除以一致预期；季报用公布前后分析师预测变化之差除以公布前预期。"
tags: [量化, 因子, 基本面, a股]
sources:
  - "raw/articles/[201806060856]季度超预期再构建及业绩超预期因子分析.md"
origin: agent-compiled
status: developing
created: 2026-05-20
updated: 2026-05-20
review_by: ""
---

# ESP因子 / Earnings Surprise Percent

## Definition / 定义

ESP（Earnings Surprise Percent，超预期幅度）因子直接衡量公司业绩超预期的幅度。正值为超预期，负值为低于预期。

## How It Works / 工作原理

### 年报 ESP

$$ESP_{i,q} = \frac{E_{i,q} - \hat{E}_{i,q}}{|\hat{E}_{i,q}|}$$

其中 $E_{i,q}$ 为实际利润（或业绩预告上下限均值），$\hat{E}_{i,q}$ 为分析师对全年业绩的预测中位数。要求至少 3 家机构给出预测。

### 季报 ESP

$$ESP_{i,q} = \frac{\hat{AE}_{i,q} - \hat{BE}_{i,q}}{|\hat{BE}_{i,q}|}$$

其中 $\hat{BE}_{i,q}$ 为季报公布前的机构最新预测中位数（要求 ≥2 家），$\hat{AE}_{i,q}$ 为季报公布后的机构最新预测中位数（要求 ≥2 家）。

### 计算频率

每月第一个交易日计算因子值并调仓。

## Why It Matters / 为什么重要

- ESP 因子最优组在沪深 300 取得 17.25% 年化超额收益（IR 1.44）
- 在中证 500 取得 18.90% 年化超额收益（IR 1.33）
- IC 均值较大且显著不为零，但 IC_IR 不大（波动性高）
- 高超预期幅度（>10%）才有明显的超额收益区分度

## Examples / 示例

- ESP 因子在 5 分组测试中单调性好，最优组显著优于其他组
- 信号衰减快，晚一个月基本无收益

## Related Pages / 关联页面

- [[业绩超预期]] — ESP 的概念基础
- [[SUE因子]] — 考虑分歧度的标准化版本
- [[一致预期]] — 因子计算的输入
- [[盈余惯性]] — ESP 发现的市场现象

## Sources / 来源

- [[季度超预期再构建及业绩超预期因子分析]]

## Notes / 笔记

<!-- human:start -->
<!-- human:end -->
