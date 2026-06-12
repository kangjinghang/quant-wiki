---
title: "Logsig-Alpha因子"
title_zh: 
type: concept
summary: "一种利用log-signature特征提取结合因子正交转化模块（MLP架构），将高频成交量序列端到端转化为低相关性选股因子的生成器模型。"
tags: [东北金工, 券商研报, 深度研究, 高频量价因子, 因子, 机器学习, 深度学习, 回测]
sources:
  - "[[日内成交量分布因子及logsig-alpha因子生成-因子选股系列之六]]"
origin: agent-compiled
status: seed
created: 2026-06-03
updated: 2026-06-03
review_by: ""
---
## 定义 / Definition

Logsig-Alpha是一种从序列到因子的生成器模型。它能够端到端地将高频数据序列（如成交量序列）转化为具有优异选股能力且两两相关性较低的因子。该模型在仅使用成交量信息的情况下，生成的Logsig-Alpha-v因子表现优于传统人工构造的因子。

## 方法/机制 / Methodology

Logsig-Alpha模型架构主要包含两个核心模块：

1. **Log-signature计算模块**：利用高截断阶数（如10阶）的log-signature提取原始序列的特征集。Log-signature保留了序列中的绝大部分信息，且相比signature具有更低的维度，对稀疏样本数据处理更为稳健。
2. **因子正交转化模块**：采用多层感知机（MLP）架构。在保留因子选股能力的同时，降低因子之间的相关性。该模块将标准化后的log-signature特征转化为一批独立的基础因子，随后进行标准化并等权合成输出。

## 表现 / Performance

基于成交量序列构建的Logsig-Alpha-v因子表现优异：
- **周度因子**：Rank IC为7.52%，ICIR为1.24，五分组多头年化收益20.30%，多空年化收益36.39%。
- **月度因子**：Rank IC为9.12%，ICIR为1.34，五分组多头年化收益17.43%，多空年化收益26.18%。

## 相关概念

- [[log-signature特征]]
- [[高频数据低频化]]
- [[日内成交量分布因子]]
- [[深度学习]]

## 来源

- [[日内成交量分布因子及logsig-alpha因子生成-因子选股系列之六]]
