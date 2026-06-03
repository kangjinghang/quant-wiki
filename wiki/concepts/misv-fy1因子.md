---
title: MISV_FY1因子
type: concept
summary: 基于一阶段剩余收益模型和一致预期净利润（FY1）计算的基本面错误定价因子，衡量股票当前PB偏离合理估值的程度。
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

[[MISV_FY1因子]]（Mispricing based on FY1 consensus）是基于一阶段[[剩余收益模型]]，使用[[一致预期]]归母净利润（FY1）作为未来盈利预测，计算股票合理估值与当前市净率（PB）差异比例的基本面因子。

## 方法/机制 / Methodology

通过全A截面OLS回归估算隐含的市场预期回报率和增速，进而计算合理估值与当前PB的差异比例。因子值越高，表示股票相对于基本面被低估越严重。

该因子是[[基本面错误定价]]的两个实现版本之一，另一个是使用TTM净利润的[[MISV_TTM因子]]。

## 相关概念 / Related Concepts

- [[基本面错误定价]]
- [[MISV_TTM因子]]
- [[剩余收益模型]]
- [[价值掘金因子]]
- [[一致预期]]
