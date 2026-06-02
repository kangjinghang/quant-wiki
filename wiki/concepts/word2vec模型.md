---
title: "Word2Vec"
title_zh: 
type: concept
summary: "由Google提出的一组相关模型，用于生成词向量，通过简化的神经网络架构（CBOW和Skip-gram）高效地将词语映射到高维向量空间。"
tags: [机器学习, 另类数据, 深度研究, 券商研报]
sources: []
  - "[[nlp综述-勾勒ai语义理解的轨迹]]"
origin: agent-compiled
status: developing
created: 2026-06-01
updated: 2026-06-02
review_by: ""
---
## 定义 / Definition

Word2Vec是2013年由Mikolov等人提出的一种轻量级神经网络模型，旨在高效地将词语转化为分布式向量表示。它包含两种主要架构：CBOW（Continuous Bag-of-Words）和Skip-gram。

## 方法与机制 / Methods

- **CBOW**：利用上下文（周围词）预测中心词。相比前代模型去掉了隐藏层，将词向量求和或平均，训练速度更快。
- **Skip-gram**：利用中心词预测上下文。在处理小语料库时表现通常优于CBOW。
- **优化算法**：为了解决输出层Softmax计算量过大的问题，引入了**Hierarchical Softmax**（利用哈夫曼树将复杂度降至O(log|V|)）和**Negative Sampling**（通过随机负采样简化计算）。

## 意义

Word2Vec不仅提供了高质量的静态词向量，更重要的是开启了NLP领域的**迁移学习**思潮：在大型语料上预训练得到的词向量可以作为下游任务的初始化输入，显著提升模型效果。

## 相关概念

- [[词向量]]
- [[自然语言处理]]
- [[机器学习]]

## 来源

- [[nlp综述-勾勒ai语义理解的轨迹]]
