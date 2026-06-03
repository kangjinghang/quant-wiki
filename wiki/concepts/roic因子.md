---
title: "ROIC因子"
title_zh:
type: concept
summary: "投入资本回报率（Return on Invested Capital）因子，衡量企业利用全部投入资本创造收益的能力，是基本面量化投资中评估企业价值创造能力的核心指标。"
tags: [因子投资, 基本面量化, 估值, 东北金工]
sources:
  - "[[预期外roic-wacc回报因子及相关测试]]"
origin: agent-compiled
status: seed
created: 2026-06-04
updated: 2026-06-04
review_by: ""
---
## 定义 / Definition

[[roic因子]]（Return on Invested Capital，投入资本回报率）衡量企业利用全部投入资本（包括股权和债权）创造经营利润的能力。其核心公式为：

$$ \text{ROIC} = \frac{\text{NOPLAT}}{\text{投入资本}} $$

其中 NOPLAT（Net Operating Profit Less Adjusted Taxes，税后净营业利润）为扣除了调整后税金的营业利润，投入资本为股东权益与有息负债之和减去多余现金。ROIC 是评估企业价值创造能力的核心指标——当 ROIC 高于[[wacc因子]]（加权平均资本成本）时，企业在创造价值；反之则在毁损价值。

## 方法/机制 / Methodology

在量化因子构建中，ROIC 的计算需要处理多项数据细节：

1. **分子端（NOPLAT）**：从营业利润出发，扣除调整后的所得税，还原财务费用对税盾的影响。
2. **分母端（投入资本）**：股东权益加有息负债，减去非经营性资产（如超额现金、投资性房地产等），确保分子分母的匹配。
3. **极端值处理**：对投入资本为负或极小的样本进行合理的截断或剔除。

## 应用 / Applications

ROIC 因子在量化投资中的应用广泛：

- **与 WACC 配合**：ROIC-WACC 差值直接反映企业的经济利润（Economic Profit），是价值创造的核心度量。基于此构建的[[预期外roic-wacc回报因子]]在全 A 市场表现出显著的选股能力。
- **分域选股**：在[[roic-wacc成长分域模型]]中，ROIC 是划分价值创造域与价值毁损域的核心依据。
- **质量因子维度**：ROIC 是质量因子（Quality Factor）的重要组成部分，与盈利能力、盈余稳定性等维度互补。

## 相关概念

- [[wacc因子]]
- [[预期外roic-wacc回报因子]]
- [[roic-wacc成长分域模型]]
- [[基本面量化]]
- [[估值因子]]

## 来源

- [[预期外roic-wacc回报因子及相关测试]]
