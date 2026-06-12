---
title: "Log-signature特征"
title_zh: 
type: concept
summary: "Signature的对数表示，含有与Signature同样的信息但更为简洁，维数更低，对缺失数据更加稳健，但缺乏普适性，需搭配非线性模型使用。"
tags: [机器学习, 深度学习, 高频量价因子, 因子投资, 东北金工, 券商研报, 深度研究]
sources:
  - "[[基于logsig-rnn的高频数据低频化选股因子-机器学习系列之三]]"
origin: agent-compiled
status: seed
created: 2026-06-02
updated: 2026-06-02
review_by: ""
---
## 定义 / Definition

Log-signature（对数签名）是Signature特征的一种简洁表示。在相同截断阶数下，Log-signature的维数更低，在一定程度上起到了降维的作用。

## 方法/机制 / Methodology

Log-signature具有以下重要性质：
1. **一一对应**：路径的Log-signature和Signature是一一对应的，两者在相同截断阶数下含有的信息一致。
2. **降维与稳健性**：相对于Signature，Log-signature维数更低，且经验上对缺失数据更加稳健。
3. **唯一性与不变性**：具有路径的唯一性和时间重参数化下的不变性。
4. **非普适性**：与Signature不同，Log-signature不具有普适性，因此必须搭配非线性模型（如RNN）才能实现较好的效果。

## 相关概念

- [[signature特征]]
- [[logsig-rnn模型]]
- [[高频数据低频化]]

## 来源

- [[基于logsig-rnn的高频数据低频化选股因子-机器学习系列之三]]
