---
title: "基于Logsig-RNN的高频数据低频化选股因子——机器学习系列之三"
title_zh: 
type: source
summary: "本报告由东北证券金融工程组发布，主要探讨了利用Logsig-RNN模型处理高频量价数据并将其转化为低频（周频）选股因子的方法。报告详细介绍了Signature与Log-signature在路径特征提取中的作用，并基于此构建了深度学习因子LogsigRNN_week。测试表明，该因子表现优异，与传统因子相关性低，能为国证2000增强策略提供显著的增量信息。"
tags: []
origin: agent-compiled
status: seed
created: 2026-06-02
updated: 2026-06-02
source_type: ""
source_language: ""
raw_path: "raw/articles/[202309081858]基于LogsigRNN的高频数据低频化选股因子机器学习系列之三.md"
review_by: ""
raw_hash: "0af2e880fdaad94ed2e50b2b6fb62f9d1fb5d40155690580f33c9bea3e3f0629"
---
## 核心内容

本报告提出了一种基于Logsig-RNN模型的高频数据低频化选股因子构建方法。传统RNN模型在处理高频序列时面临序列过长或采样点过密等问题，而Logsig-RNN通过将高密度采样的多维数据流分段转化为特征集，有效缓解了这些问题。报告首先介绍了Signature与Log-signature的数学定义及其在提取路径特征时的独特优势，随后利用处理后的高频量价数据与Logsig-RNN结合，构造了周度的深度学习因子LogsigRNN_week。

## 关键发现

- **LogsigRNN_week因子表现优异**：在中性化后，该因子的Rank IC达到0.0672，ICIR达到0.9333，多头组合年化收益达20.60%。
- **合成因子效果更佳**：将LogsigRNN_week因子与Sig_week因子等权合成得到的LogsigRNN_sig_week因子表现进一步提升，Rank IC为0.0716，ICIR为1.0628。
- **策略增强显著**：在国证2000增强策略中加入该深度学习因子后，超额年化收益达到14.67%，年化跟踪误差4.78%，Sharpe ratio提升至3.07。
- **因子特性**：该因子与常见风格因子及高频因子相关性较低，且在小市值股票池（如中证1000、国证2000）中表现更好。

## 相关概念

- [[signature特征]]
- [[log-signature特征]]
- [[logsig-rnn模型]]
- [[高频数据低频化]]
- [[深度学习因子挖掘]]

## 来源

- [[基于logsig-rnn的高频数据低频化选股因子-机器学习系列之三]]
