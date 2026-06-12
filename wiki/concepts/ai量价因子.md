---
title: "AI量价因子"
type: concept
summary: "利用人工智能技术从量价数据中提取的选股因子，通常基于深度学习模型（如GRU）从多频段K线数据中挖掘非线性特征。"
tags: [华泰金工, 量价因子, 机器学习, 深度学习, esg, ai应用, 指数增强, 券商研报, 另类数据, 多因子模型]
sources:
  - "[[esg分歧度因子和ai量价增强策略]]"
origin: agent-compiled
status: seed
created: 2026-06-03
updated: 2026-06-03
---
## 定义 / Definition

利用人工智能技术从量价数据中提取的选股因子，通常基于深度学习模型（如GRU）从多频段K线数据中挖掘非线性特征。

## 相关页面 / Related

> Seed page — content to be expanded from future source ingests.

## Related Pages / 关联页面

- [[esg分歧度因子]] — 衡量不同评级机构对同一上市公司ESG评分差异程度的因子，通常取评级分位数两两配对标准差的均值。
- [[esg综合因子]] — 将ESG评级因子与ESG分歧度因子等权结合构建的复合因子，旨在同时捕捉企业的ESG水平及评级一致性。
## 补充发现 / Additional Findings

### 来自 [[esg分歧度因子和ai量价增强策略]]

## 应用场景 / Application

在本文中，AI量价因子被用于构建沪深300指数增强策略的收益预测端。为了结合基本面的ESG信息，策略首先筛选出高ESG综合因子的个股作为底仓，然后在该底仓范围内应用AI量价因子进行增强。这种“高ESG底仓 + AI量价增强”的组合在回测期内实现了10.55%的年化超额收益，信息比率达到2.79，优于纯AI量价模型。

## 相关概念

- [[深度学习]]
- [[量价因子]]
- [[高频数据]]
- [[指数增强策略]]
