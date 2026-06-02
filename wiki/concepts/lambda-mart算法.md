---
title: "Lambda-MART算法"
title_zh: 
type: concept
summary: "结合LambdaRank梯度函数和MART（GBDT）的排序学习算法，通过决策树对梯度进行建模。"
tags: [华创金工, 券商研报, 排序学习, ltr, 机器学习, 集成学习, 量价关系, 回测, 深度研究]
sources: []
  - "[[基于价量数据的排序学习选股模型]]"
origin: agent-compiled
status: seed
created: 2026-06-02
updated: 2026-06-02
review_by: ""
---
## 定义 / Definition

LambdaMART是一种结合了LambdaRank中的梯度函数（$\lambda$）和MART（Multiple Additive Regression Trees，又称GBDT）算法的[[排序学习]]模型。它将LambdaRank中定义的梯度作为MART算法的拟合目标，利用决策树对梯度进行建模，从而兼具了LambdaRank优化全局排序指标的能力和GBDT强大的拟合与泛化能力。

## 方法/机制 / Methodology

LambdaMART的算法流程结合了梯度提升决策树的迭代框架：
1. 初始化决策树模型。
2. 对于每一棵新的决策树，计算每个样本的lambda梯度值。
3. 创建回归树去拟合这些梯度值，划分叶节点区域。
4. 在每个叶节点上，根据牛顿法或类似方法更新输出值，以最小化损失函数。
5. 更新整体的得分函数，累加新树的预测结果。
通过多棵树的迭代累加，模型能够不断降低排序损失，提升[[ndcg指标]]等评估标准的得分。

## 相关概念

- [[排序学习]]
- [[lgbmranker模型]]
- [[集成学习]]

## 来源

- [[基于价量数据的排序学习选股模型]]
