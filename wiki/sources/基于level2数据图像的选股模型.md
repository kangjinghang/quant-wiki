---
title: "基于level2数据图像的选股模型"
title_zh: 
type: source
summary: "华泰金工提出了一种基于图像识别的全新选股模型，将高频逐笔成交与逐笔委托数据转换为15×8×8的三维图像格式，并应用Vision Transformer（ViT）及Video Vision Transformer（ViViT）进行模式识别。实证表明，该图像模型能提取传统时序模型无法覆盖的差异化Alpha信号，在中证1000指数增强组合中实现了年化17.44%的超额收益。"
tags: []
origin: agent-compiled
status: seed
created: 2026-06-05
updated: 2026-06-05
source_type: ""
source_language: ""
raw_path: "raw/articles/[202512261502]华泰金工基于level2数据图像的选股模型.md"
review_by: ""
raw_hash: "63aac8027973995be3a8eaf1ce2762aa0c06e223702f884d41b8f4bf765b1de9"
---
## 核心内容

本文针对如何从海量Level-2数据中提取Alpha信号的问题，提出了一种基于图像识别的解决方案。该方法借鉴微软亚研院MarS论文的思路，将逐笔成交与逐笔委托数据转换为标准化的三维图像格式（15通道×8宽度×8高度），其中通道对应15种订单类型，宽度和高度分别对应价格区间和成交量/委托量区间。

研究采用了两种基于Transformer架构的视觉模型：
1. **ViT模型**：以单日Level-2数据图像作为输入，预测未来10日个股超额收益。
2. **ViViT模型**：将过去20个交易日的图像序列作为视频输入，采用Tubelet Embedding和Factorised Encoder方法捕捉时空特征。

## 关键发现

- **因子表现**：ViT模型周度RankIC为10.09%，多头年化超额收益18.62%；ViViT模型周度RankIC为9.64%，换手率显著降低至97.18%。
- **模型融合**：ViT与ViViT等权合成后，融合模型周度RankIC提升至10.48%，多头年化超额收益达19.66%。
- **差异化Alpha**：图像模型与传统时序Transformer模型信号相关性在0.6~0.7之间，回归残差仍具备稳定的选股能力，证明其能捕捉时序模型无法覆盖的信息。
- **指数增强**：基于融合模型的中证1000增强组合（无成分股约束）年化超额收益率达17.44%，信息比率为3.14。
- **特征重要性**：在成交数据中，大小单特征最重要；在委托数据中，非主动买卖（体现交易耐心与信心）特征信息含量最高。

## 相关概念

- [[level-2数据图像化]]
- [[vision-transformer选股模型]]
- [[video-vision-transformer选股模型]]
- [[逐笔成交数据]]
- [[逐笔委托数据]]
- [[vit模型]]
- [[vivit模型]]
- [[mars模型]]

## 来源

- [[基于level2数据图像的选股模型]]
