---
title: "WOE指标"
title_zh: 
type: concept
summary: "Weight of Evidence，对数财务危机风险概率，衡量特定分箱内正常样本与异常样本比例的差异，作为财务指标的打分标准。"
tags: []
sources: []
origin: agent-compiled
status: seed
created: 2026-05-28
updated: 2026-05-28
review_by: ""
---
## 定义 / Definition

[[WOE指标]]（Weight of Evidence，证据权重）即对数财务危机风险概率，用于衡量特定分箱内正常样本与异常样本比例的差异，作为财务指标的打分标准。

## 计算公式

130WOE_i = \ln\left(\frac{Good_i / Good_{total}}{Bad_i / Bad_{total}}\right)130

其中 $ 为第 $ 个分箱中正常样本数，$ 为异常样本数。

## 作用

- 将[[分箱法]]处理后的财务指标转化为统一量纲的风险得分
- 正值表示该分箱中正常样本比例更高，负值表示异常样本比例更高
- 作为[[财务质量打分模型]]的打分标准

## 与IV指标的关系

130IV = \sum_{i=1}^{n} (Good_i - Bad_i) \times WOE_i130

[[IV指标]]是[[WOE指标]]的加权求和，IV值越大说明该变量的区分能力越强。

## 来源

- [[高质量股票池构造体系Ⅱ事件型风险研究]]（[[光大金工]]，2022年5月）
