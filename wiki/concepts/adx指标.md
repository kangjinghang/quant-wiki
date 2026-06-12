---
title: "ADX指标"
title_zh: 
type: concept
summary: "平均趋向指数，用于衡量市场趋势的强度而不体现方向，常用于判断市场是否处于明显的趋势行情中。"
tags: [华泰金工, 券商研报, 择时, 技术面, 趋势跟踪, 量价关系, 波动率, 回测]
sources:
  - "[[a股择时之技术打分体系]]"
origin: agent-compiled
status: seed
created: 2026-06-05
updated: 2026-06-05
review_by: ""
---
## 定义 / Definition

[[adx指标]]（Average Directional Movement Index，平均趋向指数）由技术分析师威尔斯·威尔德提出。该指标包含+DI（上行趋势强度）、-DI（下行趋势强度）和ADX（趋势强度均值）三条线，主要用于衡量市场趋势的强度，而不体现趋势的方向。

## 方法/机制 / Methodology

在[[技术打分体系]]中，ADX被用作趋势维度的观测指标：
- 可以进一步构建正向ADX和负向ADX，以明确当前趋势的方向。
- 策略构建上，采用跟踪20日ADX的趋势策略：趋势强度升高则买入，减缓则卖出。

## 相关概念 / Related Concepts

- [[多维度技术指标]]
- [[技术打分体系]]
- [[趋势跟踪]]
- [[择时]]

## 来源 / Sources

- [[a股择时之技术打分体系]]
