---
title: "DPIN_SMALL_PM_MEAN因子"
title_zh: 
type: concept
summary: "在小单卖出、大单买入的非预期收益为正的切片中构建的DPIN均值因子，在全市场周度调仓下IC均值为0.044，多头相对中证800年化超额23.4%。"
tags: []
sources: []
  - "[[日内价量数据因子化研究]]"
origin: agent-compiled
status: developing
created: 2026-05-28
updated: 2026-06-02
review_by: ""
---
## Definition / 定义

DPIN_SMALL_PM_MEAN因子是[[dpin因子]]体系中的均值维度因子。其构建逻辑为：在日内交易切片中，筛选小单卖出、大单买入且非预期收益为正的切片，计算这些切片中DPIN的均值。

## 构建 methodology

1. 将日内交易数据按时间切片
2. 在每个切片中计算DPIN值
3. 筛选条件：小单卖出 + 大单买入 + 非预期收益为正
4. 对筛选后的切片取DPIN均值

## 实证表现

- 全市场周度调仓下IC均值为0.044
- 正IC占比84.4%
- 行业中性化后多头超额IR达1.65
- 多头相对[[中证800]]年化超额23.4%
- 在[[中证1000指数]]和[[中证500指数]]等中小盘股域表现更优

## 因子特征

- 属于[[dpin因子]]体系的均值维度
- 与[[dpin-base-middle-std因子]]（标准差维度）和[[dpin-small-total-stable因子]]（稳定性维度）互补
- 与Barra流动性因子（STOM）有一定相关性，需正交化处理

## 相关概念

- [[dpin因子]] — 所属因子体系
- [[信息优势交易概率]] — 理论基础
- [[高频量价因子]] — 更广泛的因子类别
