---
title: "SUE因子"
title_zh: "SUE因子（标准化超预期）"
type: concept
summary: "Standardized Unexpected Earnings，在 ESP 基础上除以分析师预测的标准差进行标准化，考虑分析师分歧度。表现优于 ESP 因子。"
tags: [量化, 因子, 基本面, a股]
sources:
  - "[[季度超预期再构建及业绩超预期因子分析]]"
origin: agent-compiled
status: developing
created: 2026-05-20
updated: 2026-05-20
review_by: ""
---

# SUE因子 / Standardized Unexpected Earnings

## Definition / 定义

SUE（Standardized Unexpected Earnings，标准化超预期）因子在[[esp因子|ESP]]的基础上，除以分析师预测的标准差（分歧度）进行标准化处理。其核心思想是：当分析师分歧度较大时，[[业绩超预期]]的"含金量"应被打折扣。

## How It Works / 工作原理

### 年报 SUE

$$SUE_{i,q} = \frac{E_{i,q} - \hat{E}_{i,q}}{\sigma_{i,q}}$$

其中 $\sigma_{i,q}$ 为分析师预测值的标准差（分歧度）。

### 季报 SUE

$$SUE_{i,q} = \frac{\hat{AE}_{i,q} - \hat{BE}_{i,q}}{\sigma_{i,q}}$$

其中分子为季报前后分析师预测变化，$\sigma_{i,q}$ 为预测的标准差。

### 与 ESP 的区别

| 维度 | ESP | SUE |
|------|-----|-----|
| 分母 | 一致预期绝对值 | 分析师预测标准差 |
| 含义 | 超预期幅度百分比 | 标准化后的超预期程度 |
| 分歧度 | 不考虑 | 考虑 |
| 覆盖度 | 相同 | 相同 |

## Why It Matters / 为什么重要

- SUE 因子表现优于 ESP 因子：
  - 沪深 300：超额 20.0%，IR 1.87（ESP 为 17.25%/1.44）
  - 中证 500：超额 19.18%，IR 1.28（ESP 为 18.90%/1.33）
- 考虑分析师分歧度后，因子的区分度有所提升
- 在 IC 和最优组收益上均有小幅改善

## Examples / 示例

- SUE 因子 5 分组测试同样体现良好的单调性
- 最优组要求超预期幅度在 10% 以上
- 信号衰减同样快，需及时调仓

## Related Pages / 关联页面

- [[esp因子]] — SUE 的基础版本
- [[业绩超预期]] — 核心概念
- [[一致预期]] — 因子计算输入
- [[盈余惯性]] — SUE 发现的市场现象
- [[业绩超预期因子体系]] — 综合分析

## Sources / 来源

- [[季度超预期再构建及业绩超预期因子分析]]

## Notes / 笔记

<!-- human:start -->
<!-- human:end -->
