---
title: "XGBoost模型"
title_zh:
type: concept
summary: "由陈天奇提出的极端梯度提升框架，属于集成学习中的Boosting方法，以高效、准确和可扩展著称，广泛应用于量化投资中的因子合成和分类预测任务。"
tags: [机器学习, 集成学习, 深度研究, 券商研报]
sources: []
origin: agent-compiled
status: seed
created: 2026-06-01
updated: 2026-06-01
review_by: ""
---
## 定义 / Definition

XGBoost（eXtreme Gradient Boosting）是一种基于决策树的集成学习框架，通过对多个弱学习器（CART回归树）进行梯度提升（Gradient Boosting），逐步降低训练误差，最终得到一个强学习器。它在量化投资中被广泛用于因子合成、收益预测和文本特征分类等任务。

## 方法/机制 / Methodology

XGBoost的核心思想是在每次迭代中拟合上一轮残差的负梯度方向，同时引入正则化项控制模型复杂度：

$$\mathcal{L}^{(t)} = \sum_{i=1}^{n} l(y_i, \hat{y}_i^{(t-1)} + f_t(x_i)) + \Omega(f_t)$$

其中 $\Omega(f) = \gamma T + \frac{1}{2}\lambda \|\mathbf{w}\|^2$ 为正则化项，$T$为叶节点数，$\mathbf{w}$为叶节点权重。

主要技术优势：
1. **二阶泰勒展开**：使用损失函数的二阶导数加速收敛
2. **正则化**：同时控制树的深度和叶节点权重，防止过拟合
3. **列采样**：借鉴随机森林的思想，每次分裂随机选取特征子集
4. **稀疏值处理**：自动处理缺失值，学习默认分裂方向

## 相关概念

- [[集成学习]]
- [[机器学习]]
- [[forecast-adj-txt-bert因子]]

## 来源

- [[再探文本FADT选股]]
