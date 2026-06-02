---
title: "MOD修正法"
title_zh: 
type: concept
summary: "一种通过截面回归剥离资金流与同期涨跌幅相关性（反转效应）以提纯资金流Alpha的因子修正方法。"
tags: [资金面, 因子, 量化, 深度研究, 券商研报]
sources: []
  - "[[大小单重定标与资金流因子改进]]"
origin: agent-compiled
status: developing
created: 2026-05-29
updated: 2026-05-29
review_by: ""

---
## 定义 / Definition
MOD修正法（Momentum-Orthogonal Decomposition）是一种处理资金流数据的方法，旨在剥离资金流与同期涨跌幅之间的正相关关系，从而剔除反转因子的负面影响，提取更为纯净的资金流Alpha信息。

## 方法/机制 / Methodology
资金流（尤其是大单净流入）通常与同期股票涨跌幅呈显著正相关，这导致原始资金流因子暴露了反转风险。MOD修正法的核心步骤如下：
1. 统计每个交易日的大单买入金额（B）和大单卖出金额（S）。
2. 计算买入卖出金额比（IMB指标）作为代理变量。
3. 逐个交易日进行截面回归：$IMB = \alpha + \beta \cdot Ret + \epsilon$，其中$Ret$为当日涨跌幅。
4. 取残差项$\epsilon$作为修正系数，反算修正后的大单买入和卖出比例关系，重新分配成交金额。

## 应用效果 / Performance
经过MOD修正法处理后，资金流因子的选股能力显著提升。例如，NIR_MOD因子相比原始NIR因子，多空信息比率（IR）由2.63大幅提升至4.76，且多空净值的回撤幅度显著减小。

## 相关概念
- [[新型因子-资金流动力学与散户羊群效应]]
- [[反转因子]]
- [[CNIR因子]]
- [[IMB指标]]

## 来源
- [[大小单重定标与资金流因子改进]]
