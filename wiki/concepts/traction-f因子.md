---
title: "Traction-F因子"
title_zh: 
type: concept
summary: "基于基金持仓行为构建的股票关联网络牵引因子，与Traction-SI因子相关性仅13%，两者合成后多空组合年化收益显著提升。"
tags: []
sources: []
  - "[[从小单资金流行为到股票关联网络]]"
origin: agent-compiled
status: developing
created: 2026-05-28
updated: 2026-05-28
review_by: ""

---
## Definition / 定义

Traction-F因子（Fund holdings Infra-network Traction Factor）是基于[[基金持仓行为]]构建的股票关联网络牵引因子。通过基金持仓重叠度刻画股票间的关联关系，再利用关联网络中高关联股票的涨跌牵引力，提取个股真实收益与预期收益的预期差作为因子值。

## 与Traction-SI因子的关系

Traction-F因子与[[traction-si因子]]分别基于机构行为（基金持仓）和散户行为（小单资金流）构建关联网络。两者相关性仅为13%，说明机构与散户的行为网络提供了独立的信息来源。合成后多空组合年化收益提升至18.48%，年化IR达3.26。

## 回测表现

合成策略（Traction-F + Traction-SI）：
- 多空组合年化收益：18.48%
- 年化IR：3.26
