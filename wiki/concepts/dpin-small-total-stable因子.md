---
title: "DPIN_SMALL_TOTAL_STABLE因子"
title_zh: 
type: concept
summary: "衡量日内知情交易概率稳定性的负向因子，负IC占比72.4%，多头相对中证800策略年化收益率为19.2%。"
tags: []
sources: []
origin: agent-compiled
status: seed
created: 2026-05-28
updated: 2026-05-28
review_by: ""
---
## Definition / 定义

DPIN_SMALL_TOTAL_STABLE因子是[[DPIN因子]]体系中的稳定性维度因子，用于衡量日内知情交易概率的稳定性。该因子为负向因子，即稳定性越高（波动越小），未来收益倾向于越低。

## 构建 methodology

1. 将日内交易数据按时间切片
2. 在每个切片中计算DPIN值
3. 在小单切片中计算DPIN的稳定性指标

## 实证表现

- 负IC占比72.4%（负向因子）
- 多头相对[[中证800]]策略年化收益率为19.2%
- 在[[中证1000指数]]和[[中证500指数]]等中小盘股域表现更优

## 因子特征

- 属于[[DPIN因子]]体系的稳定性维度
- 负向因子：稳定性越高预期收益越低
- 与[[dpin-small-pm-mean因子]]（均值维度）和[[dpin-base-middle-std因子]]（标准差维度）互补
- 经济学解释：知情交易概率过于稳定可能意味着信息已被充分反映

## 相关概念

- [[DPIN因子]] — 所属因子体系
- [[信息优势交易概率]] — 理论基础
- [[高频量价因子]] — 更广泛的因子类别
