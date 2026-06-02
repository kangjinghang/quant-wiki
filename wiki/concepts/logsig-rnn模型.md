---
title: "Logsig-RNN模型"
title_zh: 
type: concept
summary: "一种结合了Log-signature特征提取器与RNN的深度学习架构，专门用于处理高频时间序列数据，能有效降低时间维度并保留序列中的大部分信息。"
tags: [机器学习, 深度学习, 高频量价因子, 因子投资, 东北金工, 券商研报, 深度研究]
sources: []
  - "[[基于logsig-rnn的高频数据低频化选股因子-机器学习系列之三]]"
origin: agent-compiled
status: seed
created: 2026-06-02
updated: 2026-06-02
review_by: ""
---
## 定义 / Definition

Logsig-RNN是一种将基于Log-signature的特征提取器与循环神经网络（RNN）相结合的深度学习模型架构。该模型专门为处理高频时间序列数据而设计，能够有效解决传统RNN在处理高频数据时面临的计算成本高和信息丢失问题。

## 方法/机制 / Methodology

Logsig-RNN模型主要包含两个部分：
1. **分段特征提取部分**：对原始数据流的时间节点进行划分，对每个子区间的数据流计算截断Log-signature特征。由于Log-signature的性质，每个子区间中得到的特征维数相同，并且实现了降维。
2. **RNN部分**：将每个子区间的Log-signature特征作为一个序列输入到RNN（如LSTM）中进行输出。

**优势**：
- 相比于传统RNN通过下采样方式处理高频数据，Logsig-RNN保留了序列中的大部分信息。
- 模型架构简单高效，具有普适性，可以估计任何受控微分方程在一定条件下的解。

## 相关概念

- [[log-signature特征]]
- [[高频数据低频化]]
- [[深度学习因子挖掘]]
- [[lstm模型]]

## 来源

- [[基于logsig-rnn的高频数据低频化选股因子-机器学习系列之三]]
