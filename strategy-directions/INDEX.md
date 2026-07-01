# INDEX — 进度追踪

> 任何新会话第一步：读本文件知全局进度。详见 [README.md](README.md) 的「如何恢复」。

## 进度总览
- L0 全景地图：✅ 完成（34 方向）
- L1 评估卡：✅ 完成（34/34）
- L2 全量目录：✅ 完成 → [`catalog.md`](catalog.md)

---

## L1 评估卡（34 张，按档位分组）

### 🟢 立即可做（22 张）

| slug | 方向 | 卡片 |
|---|---|---|
| `event-driven-pead` | 事件驱动/PEAD/超预期 | [卡片](cards/event-driven-pead.md) |
| `momentum-trend` | 动量与趋势 | [卡片](cards/momentum-trend.md) |
| `industry-rotation` | 行业轮动 | [卡片](cards/industry-rotation.md) |
| `style-rotation` | 风格轮动 | [卡片](cards/style-rotation.md) |
| `analyst-expectation` | 分析师预期因子 | [卡片](cards/analyst-expectation.md) |
| `prosperity-fundamentals` | 景气度/基本面量化 | [卡片](cards/prosperity-fundamentals.md) |
| `value-estimation` | 估值与价值因子 | [卡片](cards/value-estimation.md) |
| `quality-profitability` | 盈利质量/财务因子 | [卡片](cards/quality-profitability.md) |
| `fund-flow-northbound` | 资金流/北向资金（主线） | [卡片](cards/fund-flow-northbound.md) |
| `ipo-strategy` | 打新/抢权配售 | [卡片](cards/ipo-strategy.md) |
| `macro-timing` | 宏观择时/股债轮动 | [卡片](cards/macro-timing.md) |
| `asset-allocation-risk-parity` | 资产配置/风险平价/BL | [卡片](cards/asset-allocation-risk-parity.md) |
| `repo-cash-management` | 交易所回购/现金管理 | [卡片](cards/repo-cash-management.md) |
| `index-enhancement` | 指数增强 | [卡片](cards/index-enhancement.md) |
| `etf-rotation` | ETF轮动/主题 | [卡片](cards/etf-rotation.md) |
| `technical-channel` | 技术分析/通道/形态 | [卡片](cards/technical-channel.md) |
| `brokerage-gold-stock` | 券商金股/机构推荐 | [卡片](cards/brokerage-gold-stock.md) |
| `institutional-behavior` | 机构行为(龙虎榜/调研/大宗) | [卡片](cards/institutional-behavior.md) |
| `national-team` | 国家队资金跟踪 | [卡片](cards/national-team.md) |
| `position-risk-management` | 仓位管理/回撤控制（横切基础设施） | [卡片](cards/position-risk-management.md) |
| `dividend-red-chip` | 红利/央企/中特估 | [卡片](cards/dividend-red-chip.md) |
| `index-rebalancing` | 指数成分股调整效应 | [卡片](cards/index-rebalancing.md) |

### 🟡 需补数据/研究（7 张）

| slug | 方向 | 卡片 | 缺什么 |
|---|---|---|---|
| `reversal` | 反转 | [卡片](cards/reversal.md) | 最强变体(理想/残差反转)依赖逐笔，需日线降级或补分钟K |
| `low-vol-idiovol` | 低波/特质波动率 | [卡片](cards/low-vol-idiovol.md) | 日线版🟢可做；VOV高频增强需分钟K(🔵) |
| `microstructure-price-volume` | 微观结构/量价因子 | [卡片](cards/microstructure-price-volume.md) | 混合：日线版🟢/分钟版🟡(需补QMT分钟K)/重ML版🔴 |
| `convertible-bond` | 可转债 | [卡片](cards/convertible-bond.md) | 转债数据源(akshare集思录🔵可补，已验证可得) |
| `convertible-bond-arbitrage` | 可转债套利/定价 | [卡片](cards/convertible-bond-arbitrage.md) | 对冲端🔴(融券/期货门槛)；纯多头低估降级版🟡 |
| `sentiment-alternative-data` | 情绪/另类数据(可得部分) | [卡片](cards/sentiment-alternative-data.md) | 混合：新闻舆情/概念热度可做；招聘/卫星/股吧转🔴 |
| `fund-selection-fof` | 基金优选/FOF | [卡片](cards/fund-selection-fof.md) | 股基FOF🟡可做；债基踩雷依赖中债估值❌转🔴 |

### 🔴 暂不可做（5 张，如实记录缺什么）

| slug | 方向 | 卡片 | 现在缺什么 |
|---|---|---|---|
| `supply-chain-centrality` | 供应链/网络中心性 | [卡片](cards/supply-chain-centrality.md) | 核心依赖数库科技SAM商业数据，无等价免费替代 |
| `ml-heavy-mining` | 重ML因子挖掘 | [卡片](cards/ml-heavy-mining.md) | 触"不碰重ML"约束；**划清边界**：附哪些轻ML可接受 |
| `high-frequency-l2` | 高频/L2逐笔交易 | [卡片](cards/high-frequency-l2.md) | L2数据现在没开权限(QMT有接口，开权限可取)；执行端QMT非高频通道 |
| `options-derivatives` | 期权/衍生品 | [卡片](cards/options-derivatives.md) | 交易型需期权实盘账户(门槛高)；信号型(PCR/IV)可做辅助 |
| `futures-cta` | 期货/CTA | [卡片](cards/futures-cta.md) | 商品CTA需期货实盘账户(未开通)；股指期货信号可做辅助 |

---

## 统计
- 🟢 立即可做：22
- 🟡 需补数据/研究：7
- 🔴 暂不可做：5
- 合计：34
- 最近更新：2026-07-01（L1 全部完成）
