---
title: "标准化预期外盈利（SUE）"
title_zh:
type: concept
summary: "标准化预期外盈利（Standardized Unexpected Earnings），将实际盈利与预期盈利的差值进行标准化处理得到的因子，是PEAD效应最直接的量化度量。单季度净利润计算效果最优。"
tags: [因子, 量化, a股]
sources:
  - "[[基于pead效应的超预期因子选股效果如何-权益配置因子研究系列01]]"
origin: agent-compiled
status: developing
created: 2026-05-28
updated: 2026-06-02
review_by: ""
---
## 定义

标准化预期外盈利（Standardized Unexpected Earnings, SUE）是[[pead效应|PEAD效应]]最直接的量化度量指标。其核心思想是将公司实际公布的盈利与市场预期盈利之间的偏差进行标准化处理，以消除不同公司间波动性的差异。

## 计算方法

$$SUE = \frac{EPS_{actual} - EPS_{expected}}{\sigma(EPS_{actual} - EPS_{expected})}$$

其中：
- $EPS_{actual}$ 为实际每股收益
- $EPS_{expected}$ 为预期每股收益（通常取历史均值作为代理）
- $\sigma$ 为盈利意外的标准差

根据[[基于pead效应的超预期因子选股效果如何-权益配置因子研究系列01|国君配置权益配置因子研究系列01]]的测试，**单季度净利润**计算效果最优。

## 在超预期因子体系中的地位

SUE因子是超预期因子族的核心，相关因子均在其基础上衍生：

- [[sue衍生因子|SUE衍生因子]]：将净利润替换为营业收入、ROE、ROA等财务指标
- [[盈余公告前后异常收益因子]]：从价格反应角度捕捉PEAD
- [[分析师上下调比例因子]]：从分析师行为角度间接度量
- [[分析师预测调整幅度因子]]：从分析师调整幅度角度度量
- [[超预期复合因子]]：综合SUE及其衍生因子的多维度信息

## 理论基础

SUE的理论基础来自[[pead效应]]，最早由[[ball和brown|Ball和Brown]]（1968）发现。高SUE值的公司在盈余公告后倾向于持续产生正超额收益，低SUE值的公司则持续产生负超额收益。

## Related Pages / 关联页面

- [[pead效应]] — SUE的理论基石
- [[sue衍生因子]] — 基于SUE的衍生因子
- [[超预期复合因子]] — 综合超预期信息的复合因子
- [[ball和brown]] — PEAD效应的发现者
