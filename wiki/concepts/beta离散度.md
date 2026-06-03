---
title: "Beta离散度"
title_zh: 
type: concept
summary: "衡量市场个股Beta值分布离散程度的指标，常用于评估市场走势的凝聚力，离散度越低市场共识越强。"
tags: [brokerage-report, deep-research, momentum, mean-reversion, regime-detection, valuation, a-share, 宏观]
sources: []
  - "[[多维度择时与风格轮动模型-市场定期跟踪体系介绍]]"
origin: agent-compiled
status: seed
created: 2026-06-04
updated: 2026-06-04
review_by: ""
---
## 定义 / Definition

Beta离散度是一个衡量市场整体结构特征的技术指标，通过计算全市场个股Beta值在横截面上的分位数差值来反映市场走势的凝聚力。该指标常被用作[[市场择时|择时]]体系中的情绪面指标。

## 方法/机制 / Methodology

计算步骤如下：
1. 每月末获取全A个股过去24个月的月度收益率，与市场收益率回归计算个股Beta值。
2. 在横截面上计算所有个股Beta值的90%分位点与10%分位点的差值。
3. 对该差值进行月度差分处理，得到最终的Beta离散度指标。

**信号逻辑**：该指标为反向指标。当Beta离散度极低时，说明个股走势高度一致，市场凝聚力强，通常预示着后续行情的爆发，给出乐观信号；反之则意味着市场分歧较大，走势可能偏弱。

## 相关概念 / Related Concepts

- [[市场情绪指标]]
- [[市场微观结构]]
- [[择时]]

## 来源 / Sources

- [[多维度择时与风格轮动模型-市场定期跟踪体系介绍]]
