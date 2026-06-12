---
title: "Amihud非流动性因子"
title_zh: 
type: concept
summary: "Amihud非流动性因子（Amihud_illiq），衡量价格冲击成本。是唯一正Alpha收益与负Alpha收益接近的高频因子，扣除交易成本后多头年化超额收益达17.28%。"
tags: [high-frequency, factor-investing]
sources:
  - "[[青出于蓝-系列研究之六-如何对非流动性因子进行改进]]"
origin: agent-compiled
status: developing
created: 2026-05-26
updated: 2026-06-02
review_by: ""
---
## Definition / 定义

[[Amihud非流动性因子]]（Amihud\_illiq）是衡量价格冲击成本的经典流动性指标，由Amihud（2002）提出。属于[[日内价量相关因子]]类别。

## 计算方法

345\text{Amihud\_illiq} = \frac{1}{N} \sum_{i=1}^{N} \frac{|r_i|}{V_i}345

其中 $ 为分钟收益率，$ 为分钟成交金额。

## Performance / 表现

- 唯一正Alpha与负Alpha接近的高频因子
- 扣除交易成本后多头年化超额收益达17.28%
- 多头端和空头端均有显著预测能力

## Key Findings

- 在所有46个高频因子中，Amihud非流动性因子是唯一一个能直接转化为多头超额收益的因子
- 其他高频因子的空头端Alpha远强于多头端，说明流动性因子具有独特的定价逻辑
- 非流动性高的股票（流动性差的股票）预期收益更高，这与[[低波动异象]]有方法论关联
- 因子逻辑清晰：流动性溢价补偿

## Related Pages

- [[日内价量相关因子]] — 所属类别
- [[精选量化研究系列之二高频价量数据的因子化方法]] — 来源报告
- [[低波动异象]] — 低波动股票超额收益
- [[聪明钱因子]] — 开源金工S指标，高频数据低频因子范式
