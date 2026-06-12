---
title: "CUDA架构"
title_zh: 
type: concept
summary: "由英伟达推出的统一计算设备架构，允许开发者利用C语言或Python在GPU上编写通用并行计算程序。"
tags: [python, 机器学习, 华创金工, 券商研报, 实战]
sources:
  - "[[并行计算在金融上的应用]]"
origin: agent-compiled
status: seed
created: 2026-06-03
updated: 2026-06-03
review_by: ""
---
## 定义 / Definition

CUDA（Compute Unified Device Architecture）是由NVIDIA推出的一种集成技术，允许开发者利用GPU进行非纯图形任务的通用计算。它是目前深度学习和大规模科学计算的基础架构。

## 方法/机制 / Methods & Mechanisms

CUDA架构的核心思想是“层次”编程，将程序分解为在CPU（Host）和GPU（Device）上执行的两部分。GPU的计算核心被组织为流多处理器（SM），每个SM包含多个CUDA核心。

评估GPU性能的关键指标是“计算能力”，它标识了GPU硬件支持的特性。例如，TensorFlow 2.0要求GPU计算能力不低于3.5。目前的深度学习大模型对GPU的显存大小和带宽提出了极高的要求。

## 相关概念

- [[gpu加速]]
- [[深度学习]]
- [[机器学习]]

## 来源

- [[并行计算在金融上的应用]]
