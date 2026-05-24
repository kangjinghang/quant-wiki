---
title: "brinson归因分析"
title_zh: "Brinson归因模型"
type: concept
summary: "Brinson归因模型（Brinson Attribution Model）是一种将投资组合超额收益拆解为行业配置贡献、个股选择贡献和交互效应贡献的经典归因方法。在沪深300指数增强基金分析中，验证了行业配置收益与超额收益呈明显正相关。"
tags: [量化, 基金, 分析]
origin: agent-compiled
status: seed
created: 2026-05-24
updated: 2026-05-24
review_by: ""
---

# Brinson归因分析

## Definition / 定义

Brinson归因模型（Brinson Attribution Model）是由Gary Brinson于1986年提出的投资组合绩效归因框架。该模型将投资组合相对于基准的超额收益（Active Return）拆解为三个来源：

- **配置效应（Allocation Effect）**：行业/资产类别权重偏离基准带来的收益贡献
- **选择效应（Selection Effect）**：行业内个股选择偏离基准权重带来的收益贡献
- **交互效应（Interaction Effect）**：行业权重偏离与个股权重偏离的联合效应

## How It Works / 工作原理

$$R_{active} = R_{allocation} + R_{selection} + R_{interaction}$$

其中：
- $R_{allocation} = \sum_i (w_{pi} - w_{bi}) \times R_{bi}$，行业权重差异 × 基准行业收益
- $R_{selection} = \sum_i w_{bi} \times (R_{pi} - R_{bi})$，基准权重 × 行业内超额收益
- $R_{interaction} = \sum_i (w_{pi} - w_{bi}) \times (R_{pi} - R_{bi})$

## Why It Matters / 为什么重要

在[[指数增强]]策略评价中，Brinson归因揭示了超额收益的真实来源。[[行业量化配置在沪深300增强上的应用]]通过Brinson归因分析发现，近年来沪深300指数增强基金的行业配置分化度越来越大，行业配置收益与超额收益呈明显正相关。这意味着**行业配置能力已成为指数增强策略的核心Alpha来源之一**，验证了将行业轮动信号纳入增强策略的合理性。

## Examples / 示例

- 2020年沪深300增强基金中，最高行业配置收益达29.8%，但也有部分基金为负
- 行业配置分化度从2017年至2020年逐年增大

## Related Pages / 关联页面

- [[指数增强]] — Brison归因常用于评价增强策略
- [[基金业绩归因]] — 基金归因分析体系
- [[行业量化配置在沪深300增强上的应用]] — 本文核心应用场景
- [[行业动量]] — 行业轮动信号

## Sources / 来源

- [[行业量化配置在沪深300增强上的应用]] — 开源金工 2021.02

## Notes / 笔记

<!-- human:start -->
<!-- human:end -->
