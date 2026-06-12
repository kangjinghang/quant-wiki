---
title: "Video Vision Transformer选股模型"
title_zh: 
type: concept
summary: "应用ViViT模型对多日Level-2数据图像序列进行时空特征学习，以更低换手率预测个股超额收益的深度学习选股方法。"
tags: [华泰金工, 深度学习, transformer模型, 注意力机制, 高频数据, 市场微观结构, 量价关系, 指数增强, 券商研报, 深度研究, ai应用, 量化投资]
sources:
  - "[[基于level2数据图像的选股模型]]"
origin: agent-compiled
status: seed
created: 2026-06-05
updated: 2026-06-05
review_by: ""
---
## 定义 / Definition

Video Vision Transformer（ViViT）选股模型是一种基于视频识别技术的量化选股模型。该模型将过去20个交易日的[[level-2数据图像化]]数据构造为图像序列，视为四维视频数据进行处理，以捕捉时序维度的微观结构演变模式。

## 方法/机制 / Methodology

模型采用Arnab等人于2021年提出的[[vivit模型]]架构，关键设计包括：
1. **嵌入阶段**：使用Tubelet Embedding方法，将视频直接切分成固定尺寸的三维立方体，保留局部时空特征。
2. **编码器阶段**：采用Factorised Encoder方法，先以Transformer编码器学习空间注意力，再以另一个编码器学习时间注意力，降低计算复杂度。

在2017年初至2025年11月底的回测期内，ViViT模型周度RankIC为9.64%，多头年化超额收益为18.26%，双边换手率降至97.18%，显著低于ViT模型的144.93%。

## 相关概念

- [[vivit模型]]
- [[vision-transformer选股模型]]
- [[level-2数据图像化]]
- [[深度学习选股]]
- [[transformer模型]]

## 来源

- [[基于level2数据图像的选股模型]]
