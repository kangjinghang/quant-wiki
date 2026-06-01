---
title: "csad动量因子"
title_zh: 
type: concept
summary: "结合成分股运行一致性的动量因子，通过区间收益率除以市值加权的CSAD（个股收益与指数收益偏差绝对值和的均值）计算得出。"
tags: [momentum, 行业轮动, 量价关系, 券商研报, 深度研究]
sources: []
origin: agent-compiled
status: seed
created: 2026-06-01
updated: 2026-06-01
review_by: ""
---
## 定义 / Definition

CSAD动量因子（Market-Value Weighted CSAD Momentum Factor）是将行业指数的整体涨跌幅与行业内成分股运行的一致性相结合的复合指标。其内在逻辑是考量个股合力强度是否能支撑指数的趋势延续。当成分股走势出现较大分化时，代表投资者观点存在分歧，行业走势存在分化风险。

## 方法/机制 / Methodology

该因子是区间收益率除以一致性指标的衍生。报告测试了三种一致性指标：
1. **CSSD**：个股相对于行业指数收益率偏差的波动率均值。
2. **CSAD**：个股相对于指数日收益率偏差绝对值和的均值。
3. **Mkt_CSAD**：在计算CSAD之前，先对股票的偏差进行市值加权，然后再求和并计算区间均值。

最终选用的**市值加权CSAD动量**计算方式为：
$$ \text{Mkt\_CSAD Momentum} = \frac{\text{区间实际收益率}}{\text{市值加权的CSAD值}} $$

## 相关概念

- [[动量因子]]
- [[行业拥挤度]]
- [[个股分化度]]

## 来源

- [[行业轮动五-如何更好的描述行业趋势]]
