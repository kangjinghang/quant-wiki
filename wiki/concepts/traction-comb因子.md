---
title: "Traction_comb因子"
title_zh: 
type: concept
summary: "将基金、北向资金、小单资金流和隔夜价格四个维度构建的牵引因子等权合成的复合因子，多空表现稳健。"
tags: [开源金工, 量价关系, 因子, 回测, 深度研究]
sources: []
  - "[[从隔夜价格行为到股票关联网络]]"
origin: agent-compiled
status: seed
created: 2026-06-03
updated: 2026-06-03
review_by: ""
---
## 定义 / Definition

Traction_comb因子是开源金工股票关联网络系列研究中的合成因子。该因子将基于基金持仓（Traction_F）、北向托管券商持仓（Traction_NS）、小单资金流（Traction_SI）和隔夜价格行为（Traction_ORE）四个不同维度构建的牵引因子进行等权合成，旨在将多方向的股价牵引力形成合力。

## 方法/机制 / Methodology

由于不同维度构建的Traction系列因子之间截面相关性较低，尤其是价格视角的Traction_ORE与资金流视角的因子之间IC序列低相关，等权合成能够有效分散风险并增强收益。其中，资金流视角的三个因子之间IC序列存在一定相关性（如Traction_F与Traction_NS相关性达50%）。

从绩效来看，Traction_comb因子表现显著优于各单因子：
- RankIC均值为5.6%，RankICIR为3.6。
- 多空组合年化收益率达19.29%，年化IR为3.99，最大回撤仅为3.47%，月度胜率77%。

## 相关概念

- [[traction-ore因子]]
- [[股票关联网络]]
- [[多因子模型]]
- [[集成学习]]

## 来源

- [[从隔夜价格行为到股票关联网络]]
