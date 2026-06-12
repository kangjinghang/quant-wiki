---
title: "Vision Transformer选股模型"
title_zh: 
type: concept
summary: "应用ViT模型对单日Level-2数据图像进行特征学习，预测个股未来超额收益的深度学习选股方法。"
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

Vision Transformer（ViT）选股模型是一种基于图像识别的量化选股模型。该模型以个股单日[[level-2数据图像化]]后的数据作为输入，通过ViT架构提取图像中的微观结构特征，预测未来10日的个股超额收益。

## 方法/机制 / Methodology

模型采用Dosovitskiy等人于2021年提出的[[vit模型]]架构：
1. 将输入图像分割为固定尺寸的图块
2. 经过嵌入和位置编码处理
3. 通过标准Transformer编码器学习图块间的注意力关系
4. 经全连接层输出收益预测

在2017年初至2025年11月底的回测期内，ViT模型周度RankIC达到10.09%，多头组合年化超额收益为18.62%，双边换手率为144.93%。

## 相关概念

- [[vit模型]]
- [[video-vision-transformer选股模型]]
- [[level-2数据图像化]]
- [[深度学习选股]]
- [[transformer模型]]
- [[注意力机制]]

## 来源

- [[基于level2数据图像的选股模型]]
