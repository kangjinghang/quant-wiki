---
title: "ViViT模型"
title_zh: 
type: concept
summary: "Video Vision Transformer，一种扩展ViT以处理视频数据的模型，通过时空注意力机制捕捉视频序列中的动态模式。"
tags: [华泰金工, 深度学习, transformer模型, 注意力机制, 高频数据, 市场微观结构, 量价关系, 指数增强, 券商研报, 深度研究, ai应用, 量化投资]
sources: []
  - "[[基于level2数据图像的选股模型]]"
origin: agent-compiled
status: seed
created: 2026-06-05
updated: 2026-06-05
review_by: ""
---
## 定义 / Definition

Video Vision Transformer（ViViT）是由Arnab等人于2021年提出的视频模型，在[[vit模型]]基础上扩展以处理视频数据，能够同时捕捉空间和时间维度的特征。

## 方法/机制 / Methodology

ViViT在ViT基础上进行了两方面扩展：
1. **嵌入阶段**：采用Tubelet Embedding方法，直接将视频切分成固定尺寸的三维立方体，保留局部时空特征。
2. **编码器阶段**：采用Factorised Encoder方法，先通过空间Transformer编码器提取空间特征，再经时间Transformer编码器融合时序信息，有效降低计算复杂度。

在量化投资领域，ViViT被应用于[[video-vision-transformer选股模型]]，处理多日[[level-2数据图像化]]序列，以更低的换手率实现稳定的收益预测。

## 相关概念

- [[video-vision-transformer选股模型]]
- [[vit模型]]
- [[transformer模型]]
- [[注意力机制]]
- [[深度学习]]

## 来源

- [[基于level2数据图像的选股模型]]
