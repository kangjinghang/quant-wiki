---
title: "AOG_RANK_DEMAX因子"
title_zh: 
type: concept
summary: "改进后的盈余公告超预期因子，通过扣除公告前最大开盘跳空幅度来剔除知情交易者提前透支的影响。"
tags: [因子投资, 量价因子, 事件驱动策略, 盈余管理, 券商研报, 深度研究, 东方证券]
sources:
  - "[[盈余公告异象类因子改进与挖掘]]"
origin: agent-compiled
status: seed
created: 2026-06-04
updated: 2026-06-04
review_by: ""
---
## 定义 / Definition

AOG_RANK_DEMAX因子（如AOG_RANK_DEMAX_20d）是一种改进后的盈余公告超预期因子。它旨在解决传统AOG因子因知情交易者提前透支业绩而导致的多头失效问题，通过比较公告次日的开盘跳空与公告前的最大开盘跳空，衡量真实的超预期程度。

## 方法/机制 / Methodology

该因子的构建包含两个核心步骤：
1. **截面标准化**：将个股每日开盘涨跌幅转为全市场截面的rank分位数，解决跨日时序可比性问题。
2. **剔除知情交易者干扰**：以公告前20个交易日的最大AOG_RANK作为“真实预期”基准，用公告次日的AOG_RANK减去该基准。
$$AOG\_RANK\_DEMAX = AOG\_RANK_{t+1} - Max(AOG\_RANK_{t-20:t})$$

## 特征 / Characteristics

- **风格暴露**：微弱暴露在Value、Trend、Volatility上，偏成长超预期风格。
- **时效性**：在上半年（特别是1月、4月）表现更强。
- **相关性**：与原始AOG因子相关性高达0.95以上，但有效修复了2021年10月以来的多头走平问题。

## 相关概念

- [[aog因子]]
- [[aog-rank-quantile因子]]
- [[事件驱动因子挖掘框架]]

## 来源

- [[盈余公告异象类因子改进与挖掘]]
