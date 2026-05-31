---
title: "Transformer"
title_zh: 
type: concept
summary: "一种基于自注意力机制的深度学习架构，完全摒弃了RNN和CNN结构，具有极高的并行计算能力，是现代预训练语言模型的基石。"
tags: [机器学习, 另类数据, 深度研究, 券商研报]
sources: []
origin: agent-compiled
status: seed
created: 2026-06-01
updated: 2026-06-01
review_by: ""
---
## 定义 / Definition

Transformer是2017年Google在论文《Attention is All You Need》中提出的一种深度学习架构。它完全基于自注意力机制，抛弃了传统的RNN和CNN结构，解决了RNN难以并行计算和长程依赖衰减的问题。

## 核心机制 / Core Mechanisms

1. **Self-Attention（自注意力）**：允许模型在处理当前词时，直接关注输入序列中的所有其他词，提取全局依赖关系。
2. **Multi-Head Attention（多头注意力）**：将注意力机制并行多次执行，使模型能从不同子空间捕捉信息。
3. **Positional Encoding（位置编码）**：由于缺乏时序结构，通过注入位置信息来保留序列的顺序关系。
4. **Encoder-Decoder结构**：Encoder负责双向表征提取，Decoder结合Masked Attention用于自回归生成。

## 相关概念

- [[注意力机制]]
- [[深度学习]]
- [[bert模型]]

## 来源

- [[nlp综述-勾勒ai语义理解的轨迹]]
