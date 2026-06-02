---
title: "LASSO回归"
title_zh:
type: concept
summary: "一种带L1正则化的线性回归方法，通过对系数施加绝对值惩罚实现变量选择和降维，广泛用于解决共线性问题。"
tags: [回测, 量化]
sources: ["[[行业轮动逻辑的标签化应用-重构轮动框架-中观量化系列报告之四]]"]
origin: agent-compiled
status: developing
created: 2026-06-01
updated: 2026-06-01
review_by: ""
---
## 定义 / Definition

LASSO回归（Least Absolute Shrinkage and Selection Operator）是一种带L1正则化项的线性回归方法。通过在损失函数中加入系数绝对值之和的惩罚项（$\lambda \sum_{j=1}^{p} |\beta_j|$），LASSO能够将部分回归系数压缩至零，从而同时实现变量选择和模型降维。

## 在量化投资中的应用

在[[宏观事件驱动法]]中，LASSO回归被用于对筛选后的宏观事件变量进行降维。宏观指标之间往往存在较强的共线性（如经济增长与消费指标高度相关），LASSO通过自动剔除冗余变量，保留对资产收益预测最有效的事件因子，提升模型的稳定性和可解释性。

## 相关概念 / Related Concepts

- [[宏观事件驱动法]]
- [[宏观行业映射模型]]
- [[行业标签体系]]

## 来源 / Sources

- [[行业轮动逻辑的标签化应用-重构轮动框架-中观量化系列报告之四]]
