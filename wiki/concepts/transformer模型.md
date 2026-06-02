---
title: "Transformer"
title_zh: 
type: concept
summary: "一种基于自注意力机制的深度学习架构，完全摒弃了RNN和CNN结构，具有极高的并行计算能力，是现代预训练语言模型的基石。"
tags: [机器学习, 另类数据, 深度研究, 券商研报, 深度学习, 神经网络, 大语言模型, 技术面]
sources: []
  - "[[transformer架构下的量价选股策略-chatgpt核心算法应用于量化投资]]"
origin: agent-compiled
status: developing
created: 2026-06-01
updated: 2026-06-02
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


## 补充发现 / Additional Findings

### 来自 [[transformer架构下的量价选股策略-chatgpt核心算法应用于量化投资]]

## 优势与应用 / Advantages & Applications

相较于传统的循环神经网络（RNN）或长短期记忆网络（LSTM），Transformer具有以下优势：
1. 能够处理超长期的记忆依赖；
2. 支持变长输入序列；
3. 具备极高的并行计算效率；
4. 可通过预训练模型大幅提高下游任务的泛化能力。

除了在自然语言处理（NLP）和图像生成领域的广泛应用外，Transformer近期被成功应用于量化投资中，处理量价关系数据进行选股。
## 来源

- [[nlp综述-勾勒ai语义理解的轨迹]]

## Related Pages / 关联页面

- [[自注意力机制]] — NLP中的一种数据处理方法，通过计算query与key的相关性来加权value矩阵，有效捕捉序列各位置间的关系。
- [[transformer选股策略]] — 以个股涨跌幅和换手率为输入，利用Transformer模型预测股票涨跌概率并指导月度调仓的量化选股策略。
