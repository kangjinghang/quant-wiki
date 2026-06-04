---
title: "TM模型"
type: concept
summary: "Treynor-Mazuy模型，用于分解基金经理择时能力和选股能力的经典回归模型。"
tags: [因子投资, 回测]
sources:
  - "[[划线基金-优美曲线-的正反面]]"
origin: extracted
status: seed
created: "2026-06-04"
updated: "2026-06-04"
---

## Definition / 定义

TM模型（Treynor-Mazuy Model）是 Treynor 和 Mazuy 于1966年提出的基金绩效评价模型，在 CAPM 单因子模型基础上引入市场收益率的二次项，用于分离基金经理的择时能力（gamma）和选股能力（alpha）：

$$R_p - R_f = \alpha + \beta(R_m - R_f) + \gamma(R_m - R_f)^2 + \epsilon$$

其中 $\gamma$ 为择时系数：若 $\gamma > 0$，说明基金经理具有正向市场择时能力。

## Applications / 应用

在[[划线基金]]研究中，TM模型系数被用作[[随机森林]]预测模型的特征之一，用于判断[[基金]]是否具备持续产生"优美曲线"的能力。
