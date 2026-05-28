---
title: "B/P中性化"
title_zh: 
type: concept
summary: "在传统的市值与行业中性化基础上，引入账面市值比（B/P）作为控制变量，以剔除估值差异对基本面因子Alpha驱动力的影响。"
tags: [多因子模型, 因子, 量化, 无监督学习, 回测, 券商研报, 深度研究]
sources: []
origin: agent-compiled
status: seed
created: 2026-05-28
updated: 2026-05-28
review_by: ""
---
## 定义 / Definition

B/P中性化（Book-to-Price Neutralization）是一种因子处理方法。在传统的“市值+行业”中性化基础上，该方法引入了账面市值比（B/P，即PB的倒数）作为中性化控制变量，旨在剔除A股市场对不同公司估值定价差异所带来的影响。

中性化回归公式如下：
$$Factor_{adj} = Factor_{raw} - \beta_0 - \beta_1 \cdot Industry - \beta_2 \cdot \ln(Cap) - \beta_3 \cdot (B/P)$$

## 方法/机制 / Mechanism

传统的“市值+行业”中性化存在局限。例如，在同一行业、市值相近的两家公司中，若盈利能力（如ROE）相同，但估值（PB）不同，则低估值公司的基本面因子所蕴含的Alpha驱动力理论上更强。如果不进行B/P中性化，这种估值差异带来的Alpha会被掩盖。

借鉴PB-ROE分析框架，引入B/P因子后，大部分盈利和成长相关的财报因子在RankIC、多头超额收益以及多空超额收益上均实现了显著提升。

## 相关概念

- [[多因子模型]]
- [[估值因子]]
- [[市值行业中性化]]

## 来源

- [[财报因子构建框架初探]]
