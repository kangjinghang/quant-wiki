---
title: "black-litterman模型"
title_zh: "Black-Litterman模型"
type: concept
summary: "Black-Litterman模型（BL模型），在贝叶斯框架下融合先验收益率与投资者观点形成后验分布，解决均值方差模型对收益率输入高度敏感的问题。"
tags: [量化, 资产配置, 策略]
sources:
  - "[[资产配置风险平价与bl模型]]"
origin: agent-compiled
status: developing
created: 2026-05-21
updated: 2026-05-21
review_by: ""
---

# Black-Litterman模型

## Definition / 定义

Black-Litterman模型（BL模型）由Black和Litterman于1992年提出，是一种在贝叶斯框架下进行资产配置的方法。与传统均值方差模型直接输入预期收益率不同，BL模型从先验权重反推出先验收益率，再结合投资者的观点（views）合成后验收益率分布，最后输入均值方差模型计算最优权重。

## How It Works / 工作原理

### 第一步：计算先验收益率

假设资产收益率服从正态分布，在均值方差模型下从先验权重反推先验收益率：

$$\Pi = \delta \Sigma \omega_{prior}$$

其中 $\Pi$ 为先验收益率，$\delta$ 为风险厌恶系数，$\Sigma$ 为协方差矩阵，$\omega_{prior}$ 为先验权重。

传统BL模型使用各资产的**市值占比**作为先验权重。

### 第二步：形成观点

观点矩阵 $P \cdot Q + \epsilon$，其中 $P$ 为观点系数矩阵，$Q$ 为预测值，$\Omega$ 为观点不确定性矩阵。

### 第三步：贝叶斯合成后验

$$\mu_{BL} = [(\tau\Sigma)^{-1} + P^T\Omega^{-1}P]^{-1}[(\tau\Sigma)^{-1}\Pi + P^T\Omega^{-1}Q]$$

其中 $\tau$ 为先验的不确定性参数。

### 第四步：均值方差最优化

将后验收益率 $\mu_{BL}$ 输入均值方差模型计算各资产权重。

## Key Advantage / 核心优势

- **解决收益率难预测**：不需要直接预测收益率，而是从先验权重反推
- **解决敏感性高**：只有观点涉及的资产权重变化，不涉及的保持不变（局部调整特性）
- **贝叶斯框架**：自然融合市场均衡信息与投资者主观判断

## Improvement in A-Share Context / A股环境下的改进

传统BL模型用**市值权重**作为先验，但在A股市场：
- 总市值受市场表现波动大
- 新股频发不断扩充总市值

[[方正金工]]在[[资产配置风险平价与bl模型]]中提出用[[风险平价]]权重替代市值权重作为先验——既能有效分散风险，又利用了资产历史表现信息。

## Related Pages / 关联页面

- [[风险平价]] — 作为BL模型先验权重的改进来源
- [[资产配置风险平价与bl模型]] — RPBL融合策略
- [[方正金工]] — 提出RPBL改进的团队

## Sources / 来源

- [[资产配置风险平价与bl模型]] — 方正金工（宋家骥、严佳炜）2019.12

## Notes / 笔记

<!-- human:start -->
<!-- human:end -->
