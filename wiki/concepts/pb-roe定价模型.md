---
title: PB-ROE定价模型
type: concept
summary: 将估值因子（PB或M/V）与盈利能力（ROE）结合的定价模型，通过回归残差或简单rank合成寻找相对更具性价比的个股。
tags:
  - 因子投资
  - 估值
  - 多因子模型
  - 深度研究
sources:
  - "[[pb之变-精细分拆-新生华彩-量化研究系列报告之十三]]"
origin: llm-extract
status: seed
created: 2026-06-03
updated: 2026-06-03
---

## 定义 / Definition

PB-ROE定价模型是一种经典的选股框架，其本质是在截面上选出相对更具性价比的个股，即寻找"低估值、高盈利能力"的组合。该模型由Jarrod Wilcox在1984年提出，核心逻辑在于将估值与盈利能力结合，以评估公司的合理价格。

## 方法/机制 / Methodology

传统的PB-ROE模型形式为：$\ln(P/B) = ROE \times T - k \times T$，其中T为投资周期，k为期望投资回报率。在实际应用中，通常在每个时间截面将$\ln(P/B)$与$ROE$进行回归，取残差作为个股被高估或低估的程度。

[[pb之变-精细分拆-新生华彩-量化研究系列报告之十三]]将此模型扩展至[[m-v因子]]，提出"M/V-ROE"定价模型：$\ln(M/V) = ROE \times T - k \times T$。研究发现，采用简单的rank方法结合M/V与ROE（M/V_ROE_rank）的表现不亚于复杂的回归残差模型。

## 关键发现 / Key Findings

- **M/V与ROE的协同效应**：M/V_ROE_rank的表现全面超越PB_ROE_rank，Rank IC为-6.4%，ICIR为-3.34，IC胜率84.7%。
- **ln转换的贡献**：在"估值-ROE"模型中，对原始估值进行自然对数转换对超额收益的贡献显著，而ROE的主要作用在于提高因子稳定性。
- **VAL与ROE的结合**：在表现优异的[[val因子]]基础上引入ROE带来的增量有限，且在ROE失效年份会形成拖累。

## 相关概念 / Related Concepts

- [[估值因子]]
- [[价值因子]]
- [[m-v因子]]
- [[val因子]]

## 来源 / Sources

- [[pb之变-精细分拆-新生华彩-量化研究系列报告之十三]]
