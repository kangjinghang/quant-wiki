---
title: "用逐笔订单数据改进分钟频因子：海量Level 2数据因子挖掘系列（六）"
title_zh: 
type: source
summary: "广发金工安宁宁团队撰写的报告，探讨了如何利用Level 2逐笔订单数据改进传统分钟频因子。报告基于成交量、涨跌幅、股价等指标对日内重点时段进行区分，构建了涨跌、价格、成交金额、量价协同共4大类、123个KeyPeriod因子，并验证了其中6个代表性因子的有效性及低相关性。"
tags: []
origin: agent-compiled
status: seed
created: 2026-06-05
updated: 2026-06-05
source_type: ""
source_language: ""
raw_path: "raw/articles/[202512051506]广发金工用逐笔订单数据改进分钟频因子海量Level2数据因子挖掘系列六.md"
review_by: ""
raw_hash: "caa7087ab00a21b0c25e880249df4e5c12fd8c7def40822a65ba6239beed7fa9"
---
## 核心内容

本文是广发金工“海量Level 2数据因子挖掘”系列报告的第六篇。核心逻辑在于利用更为精细的Level 2逐笔订单数据，对前序报告中基于分钟频数据构建的Alpha因子进行改进。研究通过设定不同阈值，提取日内重点时段，并统计这些时段内的量价特征，最终构建了123个全新的KeyPeriod因子。

## 关键发现

- **因子分类与构建**：构建了涨跌、价格、成交金额、量价协同共4大类、123个因子，并引入了主买/主卖区分。
- **选股表现**：6个代表性因子在2020年1月至2025年11月期间表现出色。例如，大成交金额时段因子KeyPeriod_amount_top30pct的20日换仓历史RankIC均值达11.23%，胜率84.8%。
- **因子独立性**：与Barra风格因子、深度学习因子及前期大小单、长短单等因子的相关性测试显示，KeyPeriod_ret_zero、KeyPeriod_ret_low5pct、KeyPeriod_price_low5pct、KeyPeriod_sync_low50pct这4个因子具有高度独立性（相关系数基本在10%以内）。

## 相关概念

- [[逐笔订单数据]]
- [[重点时段因子]]
- [[高频量价因子]]
- [[市场微观结构]]

## 来源

- [[用逐笔订单数据改进分钟频因子海量level-2数据因子挖掘系列六]]
