---
title: "NLP综述：勾勒AI语义理解的轨迹"
title_zh: 
type: source
summary: "本文是华泰金工人工智能系列文本挖掘主题下的理论介绍篇，系统回顾了自然语言处理（NLP）的发展历史，并将其划分为传统统计语言模型、Word2Vec词向量时代和以BERT为代表的预训练语言模型三个阶段。文章详细解析了各阶段的代表模型（如N-gram, NNLM, Word2Vec, ELMo, GPT, BERT, XLNet）的原理及演进逻辑，旨在帮助量化投资者更好地理解文本挖掘技术，从而充分利用金融文本数据中的Alpha。"
tags: []
origin: agent-compiled
status: seed
created: 2026-06-01
updated: 2026-06-01
source_type: ""
source_language: ""
raw_path: "raw/articles/[202212181100]华泰金工NLP综述勾勒AI语义理解的轨迹.md"
review_by: ""
raw_hash: "c5c9e28dd67441ef6180da9f47d535e885d0e3dc918e4edb0f928610c4a9a31a"
---
## 核心内容

本文将NLP发展历史划分为三个阶段，并详细介绍了各阶段的代表模型：
1. **第一阶段：传统统计语言模型**。以N-gram和NNLM为代表。N-gram基于马尔可夫假设计算文本概率，但存在无法建模长程依赖和词语相似性的缺陷；NNLM首次引入深度学习，并产生了“词向量”这一重要副产物。
2. **第二阶段：[[word2vec模型]]词向量时代**。以CBOW和Skip-gram模型为代表，简化了网络结构，引入了Hierarchical Softmax和Negative Sampling优化训练，使得大规模语料训练成为现实，开启了NLP领域的迁移学习思潮。
3. **第三阶段：预训练语言模型**。以ELMo、GPT、BERT和XLNet为代表。ELMo实现了动态词向量；GPT首次将[[transformer模型]]应用于语言模型；[[bert模型]]集大成，实现了真正的双向语义理解；XLNet则通过排列组合语言模型结合了自回归和自编码的优点。

## 关键发现

- 金融文本数据的结构化程度越来越高，曾经的“另类数据”已逐渐成为标配。
- [[word2vec模型]]不仅提供了分布式词向量，更重要的是开启了NLP中“迁移学习”的全新训练方式。
- [[bert模型]]通过Masked Language Model (MLM)和Next Sentence Prediction (NSP)任务，站在了前人模型的肩膀上，在多项NLP任务中取得了SOTA效果。
- 预训练模型在金融领域的应用（如FinBERT）前景广阔，但针对金融文本的预处理（如截断策略）仍需特别设计。

## 相关概念

- [[自然语言处理]]
- [[词向量]]
- [[word2vec模型]]
- [[transformer模型]]
- [[bert模型]]
- [[预训练语言模型]]
- [[迁移学习]]

## 来源

- 原始研报：华泰金工《人工智能62：NLP综述：勾勒AI语义理解的轨迹》
