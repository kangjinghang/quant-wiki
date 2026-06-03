---
title: MISV_TTM因子
type: concept
summary: 基于一阶段剩余收益模型和滚动12个月净利润（TTM）计算的基本面错误定价因子，用于规避分析师过度乐观偏差及小市值股票数据缺失问题。
tags:
  - 估值因子
  - 因子投资
  - 基本面量化
  - 中银量化
sources:
  - "[[中银多因子选股-八-价值掘金因子]]"
origin: llm-extract
status: seed
created: 2026-06-03
updated: 2026-06-03
---

## 定义 / Definition

[[MISV_TTM因子]]（Mispricing based on TTM earnings）是基于一阶段[[剩余收益模型]]，使用过去12个月（TTM）滚动净利润替代分析师[[一致预期]]，计算股票合理估值与当前PB差异比例的基本面因子。

## 方法/机制 / Methodology

采用TTM净利润替代FY1一致预期数据，主要解决两个问题：
1. **分析师过度乐观偏差**：分析师预测普遍偏乐观，TTM数据更为客观。
2. **小市值股票数据缺失**：部分小市值股票缺乏分析师覆盖，TTM数据覆盖面更广。

对缺失的TTM净利润，采用全A截面OLS回归（以TTM净利润和行业哑变量为解释变量）进行填充，调整后R²达95%以上。

## 相关概念 / Related Concepts

- [[基本面错误定价]]
- [[MISV_FY1因子]]
- [[剩余收益模型]]
- [[价值掘金因子]]
