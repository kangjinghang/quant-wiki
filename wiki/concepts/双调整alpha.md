---
title: "双调整Alpha"
title_zh: 
type: concept
summary: "在传统Fama-French三因子Alpha基础上，进一步在横截面上对基金持仓特征（市值、账面市值比）进行回归，剥离特征驱动的业绩，获取更纯粹的双重调整后Alpha。由[[华安金工]]在FOF选基中应用。"
tags: []
sources: []
origin: agent-compiled
status: developing
created: 2026-05-28
updated: 2026-05-28
review_by: ""
---
## 定义 / Definition

[[双调整Alpha]]（Doubly-Adjusted Alpha）是一种基金业绩评估方法，由[[华安金工]]在[[FOF组合构建]]研究中应用。该方法在传统Fama-French三因子Alpha基础上，进一步在横截面上对基金持仓特征进行双重调整。

## 方法论

### 第一步：因子Alpha调整
使用Fama-French三因子模型（市场、规模、价值）回归，获取传统因子调整后Alpha。

### 第二步：持仓特征调整
在横截面上对基金持仓特征（市值、账面市值比）进行回归，剥离特征驱动的业绩：

1862\alpha_{double} = \alpha_{FF3} - \beta_1 \cdot Size - \beta_2 \cdot BM1862

### 优势
- 获取更纯粹的双重调整后Alpha
- 剔除基金持仓风格特征驱动的虚假业绩
- 提升选基因子的选基效果和稳定性

## 应用场景

在[[FOF组合构建]]中用于优选主动权益基金。特别地，[[赛道基金]]与全市场选股型基金放在一个池子中比较会降低双调整Alpha的选基效果，因此需分别考察。

## 来源

- [[FOF赋能绝对收益基金组合构建实战上量化绝对收益之路系列之二]]（华安金工，2022.05）
