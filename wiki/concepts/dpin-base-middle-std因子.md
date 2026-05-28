---
title: "DPIN_BASE_MIDDLE_STD因子"
title_zh: 
type: concept
summary: "刻画日内知情交易概率分散度的因子，在全市场测试中IC均值为0.061，多空策略年化收益率达44.3%。"
tags: []
sources: []
origin: agent-compiled
status: seed
created: 2026-05-28
updated: 2026-05-28
review_by: ""
---
## Definition / 定义

DPIN_BASE_MIDDLE_STD因子是[[DPIN因子]]体系中的标准差维度因子，用于刻画日内知情交易概率的分散度。分散度越高，说明日内知情交易活跃程度波动越大。

## 构建 methodology

1. 将日内交易数据按时间切片
2. 在每个切片中计算DPIN值
3. 在基础条件切片中计算DPIN的标准差（分散度）

## 实证表现

- 全市场测试中IC均值为0.061
- 多空策略年化收益率达44.3%
- 在[[中证1000指数]]和[[中证500指数]]等中小盘股域表现更优

## 因子特征

- 属于[[DPIN因子]]体系的标准差维度
- 与[[dpin-small-pm-mean因子]]（均值维度）和[[dpin-small-total-stable因子]]（稳定性维度）互补
- 衡量知情交易在日内不同时段的波动程度

## 相关概念

- [[DPIN因子]] — 所属因子体系
- [[信息优势交易概率]] — 理论基础
- [[高频量价因子]] — 更广泛的因子类别
