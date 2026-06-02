---
title: "R_nolimit因子"
title_zh: 
type: concept
summary: "行业内非涨跌停股票在过去一段时间的平均涨跌幅，表现为弱动量效应。"
tags: [开源金工, 券商研报, 行业轮动, 反转因子, 动量, 量价关系, 回测]
sources: []
  - "[[从涨跌停效应到行业反转]]"
origin: agent-compiled
status: seed
created: 2026-06-03
updated: 2026-06-03
review_by: ""
---
## 定义 / Definition

R_nolimit因子是指在行业内剔除过去T日内曾涨停或跌停的股票后，计算剩余非涨跌停股票的T日平均涨跌幅所构成的因子。该因子总体呈现弱动量效应。

## 方法/机制 / Methodology

1. 每月底在各一级行业内回溯过去T日的成分股数据。
2. 剔除过去T日内触发过涨跌停的股票。
3. 计算剩余股票在T日内的平均涨跌幅即为R_nolimit因子。

## 表现 / Performance

- 在各回看周期下总体呈弱动量效应，回看周期较短时动量效应更强。
- 常用于对R_limit因子进行回归处理，以提取更纯粹的NL反转因子。

## 相关概念

- [[涨跌停效应]]
- [[nl因子]]
- [[r-limit因子]]

## 来源

- [[从涨跌停效应到行业反转]]
