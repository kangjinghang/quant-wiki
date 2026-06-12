---
title: "ViT模型"
title_zh: 
type: concept
summary: "Vision Transformer，一种将Transformer架构应用于图像识别的模型，通过将图像分割为图块并学习其注意力关系进行特征提取。"
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

Vision Transformer（ViT）是由Dosovitskiy等人于2021年提出的视觉模型，首次将Transformer架构成功应用于图像识别任务。该模型将输入图像分割为固定尺寸的图块，经过嵌入和位置编码后，通过标准的Transformer编码器学习图块之间的注意力关系。

## 方法/机制 / Methodology

ViT模型的核心流程：
1. 将图像分割为固定大小的图块（如16×16）
2. 对图块进行线性嵌入
3. 添加位置编码保留空间信息
4. 使用标准Transformer编码器学习图块间关系
5. 经全连接层输出预测结果

在量化投资领域，ViT被应用于[[vision-transformer选股模型]]，对[[level-2数据图像化]]后的数据进行特征学习，预测个股未来收益。

## 相关概念

- [[vision-transformer选股模型]]
- [[vivit模型]]
- [[transformer模型]]
- [[注意力机制]]
- [[深度学习]]

## 来源

- [[基于level2数据图像的选股模型]]
