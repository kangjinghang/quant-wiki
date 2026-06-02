---
title: "Nelson-Siegel模型"
title_zh: 
type: concept
summary: "一种经典的收益率曲线拟合模型，通过水平、斜率和曲率三个参数因子来刻画截面上的期限结构，具有参数少、解释性强的优点。"
tags: [固收量化, 资产配置, 债券, 券商研报, 开源金工, 深度研究, 回测]
sources: []
  - "[[债券预期收益框架与久期择时策略]]"
origin: agent-compiled
status: seed
created: 2026-06-03
updated: 2026-06-03
review_by: ""
---
## 定义 / Definition

Nelson-Siegel模型（N-S模型）是一种广泛应用于拟合即期收益率曲线的参数化模型。该模型通过三个具有明确经济意义的参数（水平、斜率、曲率）来刻画整个截面上的期限结构。

## 方法/机制 / Methodology

模型的核心公式为：
$$y_t(m) = \beta_{1t} + \beta_{2t}\left(\frac{1-e^{-\lambda m}}{\lambda m}\right) + \beta_{3t}\left(\frac{1-e^{-\lambda m}}{\lambda m} - e^{-\lambda m}\right)$$

其中 $y_t(m)$ 为时间 $t$ 截面上期限为 $m$ 的即期收益率，$\lambda$ 为控制收益率曲线曲率的常数（通常取0.0609）。三个参数的经济学解释如下：
- **水平因子 ($\beta_{1t}$)**：因子暴露为1，代表长债收益率，对所有期限产生同等影响。
- **负斜率因子 ($\beta_{2t}$)**：代表期限利差，与长短期利差走势高度贴合。
- **曲率因子 ($\beta_{3t}$)**：代表曲线的弯曲程度，与子弹-杠铃利差走势一致。

Diebold et al. (2006) 在此基础上进一步为每个参数构建了自回归预测模型，形成了完整的即期曲线预测框架。

## 相关概念 / Related Concepts

- [[水平因子]]
- [[负斜率因子]]
- [[曲率因子]]
- [[预期收益框架]]
- [[利率债]]

## 来源 / Sources

- [[债券预期收益框架与久期择时策略]]
