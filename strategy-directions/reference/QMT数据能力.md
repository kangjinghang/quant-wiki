# QMT / xtquant 数据能力参考

> 本文件记录 QMT（迅投 mini_qmt）+ xtquant 接口的数据能力，是评估各方向"数据现在有没有"的依据。
> 查证日期：2026-07-01。来源：QMT 官方文档（迅投知识库 dict.thinktrader.net）+ 实操教程实测。

## 核心：免费 vs 付费的分界线

分界线划在**行情权限**上，不是软件功能：

| 类别 | 数据内容 | 开通 QMT 即自带？ |
|---|---|---|
| **基础行情（免费）** | 分钟K(1m/5m/15m/30m/1d)、Tick分笔(3秒五档快照)、分时、五档盘口、财务、合约信息、板块/行业 | ✅ 是，开通即有 |
| **Level-2 行情（付费/申请）** | 十档/千档盘口、逐笔成交、逐笔委托、买卖队列、总买总卖 | ❌ 需额外开 L2 权限 |

**关键**：QMT 通道里"有"L2 接口，但能不能取到取决于**账户是否开通了 Level-2 行情权限**，不是 xtquant 能力问题。

## xtquant 关键接口

### 行情数据（xtquant.xtdata）
| 函数 | 用途 |
|---|---|
| `get_market_data_ex(period, ...)` | 主力函数，取 K线/tick（历史+实时） |
| `download_history_data(...)` | 取历史前先下载到本地缓存 |
| `subscribe_quote(code, period, callback)` | 订阅单股实时行情，period 决定数据类型 |
| `subscribe_whole_quote(callback)` | 订阅全市场全推行情 |

### subscribe_quote 的 period 参数（决定取什么数据）
| period | 含义 | 需 L2 权限？ |
|---|---|---|
| `tick` | 3秒五档快照（Level-1） | ❌ 免费 |
| `1m`/`5m`/`15m`/`30m`/`1d` | 分钟/日线 K | ❌ 免费 |
| `l2quote` | 十档盘口快照 | ✅ 需 L2 |
| `l2order` | 逐笔委托 | ✅ 需 L2 |
| `l2transaction` | 逐笔成交 | ✅ 需 L2 |
| `l2quoteaux` | 实时行情补充（总买总卖） | ✅ 需 L2 |
| `l2orderqueue` | 委买委卖一档队列 | ✅ 需 L2 |
| `l2thousand` | 千档盘口（投研版） | ✅ 需 L2 |

## 对各方向的影响（速查）

| 方向 | 现状 | 补的路径 |
|---|---|---|
| 日线波段（所有🟢方向） | ✅ 不依赖 QMT 数据，用 DATA_SOURCES.md 已有 | — |
| 分钟级策略（微观结构量价/低波VOV/反转昼夜分离） | 🔵 项目没接，QMT 自带免费 | 接 `get_market_data_ex(period="1m")` |
| 逐笔/L2 策略（高频/DPIN/TOX/订单流/逐笔资金流） | 🔵 没开 L2 权限 | 向券商开 Level-2 行情权限（付费，部分券商资金量达赠送） |
| 高频执行（毫秒级 tick-to-order） | ⚠️ QMT 做不了 | 平台定位限制，需专线/co-location |

## 重要澄清
- `period="tick"` 取的是 **Level-1 的 3 秒五档快照**，不是真逐笔。真逐笔走 `l2transaction`。
- DATA_SOURCES.md §5 标注"逐笔资金流已移除"是**免费同花顺源的覆盖率问题**（深市~1400只/沪市几乎不收录），走 QMT L2 接口覆盖率不再是问题，但要开权限。

## 来源
- [XtQuant.XtData 行情模块 — 迅投知识库](https://dict.thinktrader.net/nativeApi/xtdata.html)
- [接口说明（l2 系列订阅类型）— 迅投知识库 VIP](http://docs.thinktrader.net/vip/pages/36f5df/)
- [行情利器-沪深Level2 — QMT投研数据服务](https://www.xuntou.net/forum.php?mod=viewthread&tid=410)
