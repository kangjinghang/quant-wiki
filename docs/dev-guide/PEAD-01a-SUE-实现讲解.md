# PEAD 01a SUE 单因子策略 · 实现讲解

> **本文定位**：这是一份**面向学习者的实现讲解**，不是设计文档、不是计划文档。已有的文档各有分工：
>
> | 文档 | 回答什么问题 | 你什么时候看 |
> |---|---|---|
> | [01a 策略设计](../../strategy-directions/strategy-designs/01-pead/01a-pead-sue-single-factor.md) | 赚什么钱？SUE 公式有哪几种口径？绩效预期？ | 想理解策略原理时 |
> | [PEAD playbook](../../strategy-directions/strategy-playbooks/01-pead-earnings-surprise.md) | 各家研报的 SUE 怎么算？过滤规则是什么？ | 想横向对比研报时 |
> | [数据采集实现讲解](./PEAD-01a-SUE数据采集-实现讲解.md) | 3 张表怎么抓？单季值怎么转？ | 想懂采集层时 |
> | **本文（策略实现讲解）** | **SUE 因子为什么这么近似？7 条防失真规则各自防什么？报告期提前为什么翻了 3 次车？** | **想读懂策略代码、理解每个设计取舍时** |
>
> 本文聚焦**最精华的几块**：SUE 因子的"历史同比增速法"近似（为什么近似、近似了什么）、7 条防失真剔除规则（每条防什么坑）、报告期提前机制的演进史（3 个版本的 bug 各是什么）、handlebar 主循环。其余模块（采集层、DB 层、过滤层、实盘下单）只讲思路和关键点。
>
> **与 01e 的关系**：01a 和 01e 共享同一套工程基础设施（`qmt_common/` 里的 rebalance_guard / nav_logger / filters / _rebalance / _execute_backtest），差异在因子计算（SUE vs dReport）和调仓频率（月度 vs 季度）。工程层的讲解看 [01e 实现讲解](./PEAD-01e-实现讲解.md)，本文只讲 01a 独有的部分。
>
> **配套**：[QMT 策略开发指南](./QMT策略开发指南.md)（三工作区环境、东财接口实测笔记、避坑清单）。

---

## 一、阅读准备

### 1.1 你需要先知道的事

- **QMT**：迅投的交易终端，内置一个 Python 3.6.8 解释器，提供 `handlebar`（每根 K 线触发）、`passorder`（下单）、`get_market_data_ex`（取行情）等全局函数。策略代码跑在它内部。
- **handlebar 模型**：QMT 是**事件驱动**——你写两个固定签名的函数 `init(C)` 和 `handlebar(C)`，QMT 来调用。回测时遍历历史 K 线，每根调一次 `handlebar`；实盘时实时触发。
- **PEAD**：Post Earnings Announcement Drift，业绩超预期后的股价漂移。市场对盈利超预期的反应是迟钝的——好消息不会一步涨到位，而是在后续几周持续漂移。SUE 因子就是用来捕捉这个漂移的。
- **01a vs 01e**：同属 PEAD 家族但切入点不同。01e 押"披露早的公司是好公司"（事件驱动），01a 押"盈利超出预期的公司会继续涨"（基本面驱动）。01a 的因子更核心也更难算。

### 1.2 三个角色（与 01e 相同）

```
服务器单机：QMT + MySQL + QuantVoyager 同机
┌──────────────┐   写   ┌─────────┐   读   ┌──────────┐
│ QuantVoyager │ ─────→ │  MySQL  │ ─────→ │   QMT    │
│ (Py 3.10)    │        │ quant_  │        │ (Py 3.6) │
│ 抓数据落库   │        │ voyager │        │ 策略回测 │
└──────────────┘        └─────────┘        │  +实盘   │
                                            └────┬─────┘
                                                 │ get_market_data_ex
                                                 │ passorder
```

01a 比 01e 多了一张表：`financial_quarterly`（单季利润表），这是 SUE 因子的核心数据源。采集层的细节看[数据采集实现讲解](./PEAD-01a-SUE数据采集-实现讲解.md)。

---

## 二、代码地图

策略代码在 `QuantVoyager/strategy/qmt/` 目录下：

```
strategy/qmt/
├── pead_01a_sue.py            # 主策略文件（init + handlebar，跑在 QMT 里）
├── pead_01a_sue_gbk.py        # GBK 编码副本（QMT 编辑器强制 GBK，由 gen_gbk.py 生成）
└── qmt_common/                # 共享工具模块（纯 Python，可单测）
    ├── sue.py                 # ★ SUE 因子计算（本文重点）
    ├── rebalance.py           # ★ 调仓日计算（月度，与 01e 的季度版不同）
    ├── db_reader.py           # ★ MySQL 读取 + 报告期提前逻辑（本文重点）
    ├── filters.py             # 过滤（上市天数/ST，与 01e 共用）
    ├── nav_logger.py          # 净值记录（与 01e 共用）
    └── rebalance_guard.py     # 调仓幂等保护（与 01e 共用）
```

**为什么把工具拆出来放 `qmt_common/`**：和 01e 同理——这些是**纯函数**（只依赖 pandas + datetime），不依赖 QMT 全局函数。好处有两个：

1. 能在开发机 Python 3.10 + pytest 里跑单元测试（QMT 的 `handlebar`/`passorder` 在开发机没有，没法测）；
2. QMT 的 Python 3.6 也能 import 它（只用了标准库 + pandas）。

**与 01e 的代码共享**：`filters.py`、`nav_logger.py`、`rebalance_guard.py`、以及主策略里的 `_rebalance`/`_execute_backtest`/`_filter_universe` 函数，都是 01e 先写好、01a 直接复用的。01a 新写的是 `sue.py`（因子计算）、月度调仓函数、报告期提前逻辑、业绩预告合并。

---

## 三、数据怎么流动（先看全局再看细节）

一次调仓的完整数据流，从 MySQL 到下单：

```
              handlebar(C) 被某根 K 线触发
                       │
                       ▼
        ┌─────────────────────────────────┐
        │ ① 是调仓日吗？                  │ ← rebalance.compute_monthly_rebalance_dates
        │    if bar_date not in G.rebal:  │   月度调仓（每月第一个交易日）
        │        return                   │
        └─────────────────────────────────┘
                       │ 是调仓日
                       ▼
        ┌─────────────────────────────────┐
        │ ② 确定当期报告期                 │ ← _candidate_reports + pick_report_with_forecast
        │    纯日期映射 + 定期报告已批量    │   ★ 本文第六节重点（报告期提前）
        │    披露则提前到更晚的报告期       │
        └─────────────────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────┐
        │ ③ 读单季利润表（当期+全部历史）   │ ← db_reader.load_financial_quarterly
        │    防前视：announce_date <= as_of│   ★ 和 01e 不同：取全部历史（建模要 N 季）
        └─────────────────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────┐
        │ ③' 业绩预告补覆盖                │ ← db_reader.load_performance_forecast
        │    定期未发的股票用预告补 E_actual│   预告 YTD 转单季（减上期累计）
        └─────────────────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────┐
        │ ④ 算 SUE 因子                    │ ← sue.compute_sue_for_rebalance
        │    对每只股票：                  │   ★ 本文第四节重点
        │    g = 累计同比增速              │
        │    E_expected = 去年同期×(1+g)   │
        │    SUE = (实际-预期)/|预期|      │
        │    + 7 条防失真剔除              │
        └─────────────────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────┐
        │ ⑤ 过滤：上市>250天/非ST          │ ← _filter_universe（与 01e 同）
        │    + 剔除 SUE≤0（只做多头）      │
        └─────────────────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────┐
        │ ⑥ 选股：SUE 降序选前 60 只       │ ← _select_with_limit_check
        │    顺位剔除当日一字涨跌停/停牌   │   等权 target = {symbol: 1/60}
        └─────────────────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────┐
        │ ⑦ 回测 vs 实盘                   │ ← C.is_last_bar() 区分（与 01e 同）
        │    回测：passorder 虚拟撮合+净值 │
        │    实盘：passorder 批量调仓      │
        └─────────────────────────────────┘
```

和 01e 相比，多了两步：**③' 业绩预告补覆盖**和 **④ SUE 因子计算**。报告期选取（②）也比 01e 复杂得多——01e 用纯日期映射就够了，01a 有"报告期提前"机制。下面几节就是在拆解 ②③④。

---

## 四、SUE 因子计算（最精华的一块）

> 文件：`strategy/qmt/qmt_common/sue.py`
> 对应测试：`tests/test_sue.py`

### 4.1 SUE 想量什么（先建立直觉）

SUE 想量的不是"这家公司赚了多少钱"，而是：

> **"这家公司这个季度赚的，比市场原本以为它会赚的，超出了多少？"**

关键词是**超出**。绝对盈利多不代表好（茅台每季都赚几百亿，市场已经习惯了），市场真正在乎的是"比预期高了还是低了"。

举个例子：

| 公司 | 去年同期单季净利 | 今年单季净利 | 同比增速 | 直觉判断 |
|---|---|---|---|---|
| 茅台 | 100 亿 | 120 亿 | +20% | 不错，但这是"正常增长" |
| 某中盘股 | 1 亿 | 1.8 亿 | +80% | 大幅超预期！ |

茅台虽然赚得多，但 20% 增速在它的历史里不算意外。而那个中盘股增速 80%，远超正常水平——这就是"超预期"，SUE 要找的就是这种股票。

### 4.2 关键取舍：为什么用"历史同比增速法"而不是研报原文的"分析师法"

这是 01a 最重要的设计决策，必须先讲清楚。

**研报原文的 SUE 公式**（国君/华创）：

```
SUE = (E_actual − E_expected) / σ

E_expected = 分析师一致预测（全年预测的中位数）
σ          = 分析师预测的分歧度（各机构预测值的标准差）
```

这需要**历史时间点的分析师预测数据**——注意是"历史时间点"，不是当前快照。比如算 2022 年某季度的 SUE，你需要 2022 年那个时间点各家机构对它的预测值。但同花顺只提供当前快照（`worth.html`），历史的预测早被覆盖了。付费数据库（Wind/朝阳永续）有，但项目约束明确不用付费源。

**当前实现的替代方案**（历史同比增速法，`sue.py:8-17`）：

```
SUE = (E_actual − E_expected) / abs(E_expected)

g          = (今年累计净利 − 去年同期累计净利) / |去年同期累计净利|
E_expected = 去年同期单季净利 × (1 + g)
```

核心思路：用**公司自己今年隐含的增速**替代分析师预测的增速。如果一家公司今年累计利润同比增长 30%，那"正常情况下"它的单季利润也该同比增长 30%。去年同期单季赚 1 亿，今年"应该"赚 1.3 亿（E_expected）。如果实际赚了 1.8 亿，那多出来的 0.5 亿就是超预期。

**⚠️ 三重近似**，必须诚实标注：

| 维度 | 研报原文（分析师法） | 当前实现（同比增速法） | 偏差影响 |
|---|---|---|---|
| E_expected 来源 | 分析师一致预测中位数 | 去年同期 × (1+同比增速) | 预期值的基准不同 |
| 分母 σ | 分析师预测分歧度（标准差）| abs(E_expected) | 量纲完全不同 |
| 标准化程度 | 标准化得分（可跨股票比较） | 超预期比例（偏大市值的 SUE 天然更大） | 跨股可比性弱 |

这意味着当前算出的 SUE 和研报的 SUE **不是同一个量纲**——研报的 SUE 是"超出共识几个标准差"（类似 Z-score），当前实现是"比同比外推的预期高百分之多少"。数值分布、排序结果、选出的股票都会不同。

**为什么仍然值得做**：因为"业绩超预期"这个 alpha 的核心逻辑是"盈利超出正常水平 → 市场反应不足 → 后续漂移"。用同比增速外推的预期虽然粗糙，但捕捉到了"超出正常增长"这个信号。回测验证了这个 alpha 确实存在（年化正收益），只是绩效数字不能直接和研报对标。

> 💡 这也意味着 `calc_perf.py` 里对标的国君基准 12.10%（中证500 口径B）**不是公平对标**——因为分母口径不同。这个对标的参考价值有限，更多是"数量级参考"。

### 4.3 用真实数字走一遍 SUE 计算

以 2024 年中报（current_report = "2024-06-30"）为例。假设某公司数据如下：

```
报告期        单季归母净利
2023-03-31    1.0 亿    ← 去年 Q1
2023-06-30    1.0 亿    ← 去年 Q2（去年同期单季）
2023-09-30    1.0 亿    ← 去年 Q3
2023-12-31    1.0 亿    ← 去年 Q4
2024-03-31    1.2 亿    ← 今年 Q1
2024-06-30    1.5 亿    ← 今年 Q2（当期 E_actual）
```

**Step 1：算同比增长率 g**

```
今年截至当期（中报=Q1+Q2）累计 = 1.2 + 1.5 = 2.7 亿
去年同期截至Q2 累计             = 1.0 + 1.0 = 2.0 亿
g = (2.7 − 2.0) / |2.0| = 0.35   ← 今年累计同比增长 35%
```

**Step 2：算 E_expected**

```
去年同期单季净利 = 1.0 亿（2023-06-30 那行）
E_expected = 1.0 × (1 + 0.35) = 1.35 亿   ← "正常增长"的话今年 Q2 该赚 1.35 亿
```

**Step 3：算 SUE**

```
E_actual = 1.5 亿（今年 Q2 实际）
SUE = (1.5 − 1.35) / |1.35| = 0.1111   ← 超出预期 11%
```

SUE = 0.11，是个正值（超预期），会被选入多头端。如果另一家公司 SUE = 0.30（超预期 30%），它排在前面（SUE 降序选最大的）。

这和测试用例 `test_positive_surprise`（`tests/test_sue.py:45`）的数字完全一致：

```python
# 去年每季1亿，今年中报 [1.2亿, 1.5亿]（累计2.7亿 vs 去年同期2.0亿）
self.assertAlmostEqual(result.iloc[0]["e_expected"], 1.35*E8, places=2)
self.assertAlmostEqual(result.iloc[0]["g"], 0.35, places=4)
self.assertAlmostEqual(result.iloc[0]["sue"], 0.1111, places=3)
```

### 4.4 七条防失真剔除规则（每条防什么坑）

SUE 的分母是 E_expected。如果 E_expected 接近 0，SUE 会爆炸（分母趋零），一只微利股的 SUE 能飙到 56（服务器实测），完全淹没真正的超预期信号。所以需要多层剔除。以下是全部 7 条规则，每条都有它防的具体坑：

#### 规则 ①：防前视——`announce_date <= as_of`

```python
# sue.py:97-101
df["announce_date"] = df["announce_date"].apply(_to_date)
df = df[df["announce_date"] <= as_of]
```

**防什么**：用调仓日之后才披露的数据做决策。你是 8 月 3 日调仓，不能用到 8 月 20 日才发布的中报。和 01e 的防前视原理一样（见 01e 实现讲解 §4.4），区别是 01a 在 SQL 和 Python 两层都做了（SQL 的 WHERE 加 `announce_date <= as_of`，Python 里再 filter 一遍确保）。

#### 规则 ②：E_actual 缺失剔除

```python
# sue.py:113-119
cur_rows = grp[grp["report_date"] == current_report]
if cur_rows.empty:
    continue  # 当期没有数据
e_actual = cur_row["net_profit"]
if e_actual is None or pd.isna(e_actual):
    continue  # 净利为空
```

**防什么**：当期财报还没发（或发了但 net_profit 字段为空），算不了分子。

#### 规则 ③：去年同期单季缺失 / 微利剔除

```python
# sue.py:122-128
prev_rows = grp[grp["report_date"] == prev_report]
if prev_rows.empty:
    continue  # 去年同期数据缺失
prev_profit = prev_rows.iloc[0]["net_profit"]
if prev_profit is None or pd.isna(prev_profit) or abs(prev_profit) < MIN_ABS_EXPECTED:
    continue  # 去年同期亏损或微利
```

**防什么**：E_expected = 去年同期单季 × (1+g)。如果去年同期单季净利只有 10 万，乘以任何 g 都是微小值 → 分母爆炸。`MIN_ABS_EXPECTED = 1e8`（1 亿元）是硬阈值，低于此值的剔除。

> ⚠️ **这个阈值有代价**：它过滤掉了小盘股和微利股。1 亿元单季净利大致相当于年化 4 亿+ 的中大盘股。实测能覆盖约 1100-1500 只（全市场 5000+ 的 1/4 左右）。这是"保分布健康 vs 保覆盖广度"的取舍——服务器实测 1e7 阈值时 SUE 最高 abs=56（完全失真），1e8 后 mean≈0、std≈0.44（分布健康）。

#### 规则 ④：季度数不全剔除

```python
# sue.py:134-143
expected_n_cur = cur_month // 3  # 中报→2，三季报→3，年报→4
cur_mask = ...（当年截至当期的行）
prev_mask = ...（去年截至去年同期的行）
if len(cur_ytd_rows) < expected_n_cur or len(prev_ytd_rows) < expected_n_cur:
    continue  # 季度数不全
```

**防什么**：g 靠累计净利算。如果某只股票今年缺了 Q1 数据（只有 Q2），累计 = 只有 Q2 的值，g 会严重偏低。必须校验"截至当期应有的季度数都齐了"。

**例子**：算 2024 年中报（Q2），`expected_n_cur = 6 // 3 = 2`。今年必须有 Q1 + Q2 两行，去年也要有 Q1 + Q2 两行。缺任一个就剔除。

#### 规则 ⑤：去年同期累计 ≤ 0 剔除

```python
# sue.py:147-149
if ytd_prev <= 0:
    continue  # 去年同期累计亏损
```

**防什么**：g = (今年累计 − 去年累计) / |去年累计|。如果去年累计是负数（亏损），g 的符号和含义都乱了。比如去年累计 −1 亿、今年累计 +1 亿，g = (1−(−1))/|−1| = 2（+200%），看起来"增长 200%"其实是扭亏，和正常增长不是一回事。扭亏股的超预期逻辑不同，剔除更安全。

#### 规则 ⑥：abs(E_expected) < 阈值二次检查

```python
# sue.py:157-159
if abs(e_expected) < MIN_ABS_EXPECTED:
    continue  # E_expected 太小
```

**防什么**：即使去年同期单季够大（通过了规则③），如果 g 是很大的负值（今年累计暴跌），E_expected = 去年同期 × (1+g) 可能被压到阈值以下。这是第二道防线。

#### 规则 ⑦：Q1 不作报告期（设计规避）

```python
# sue.py:88-89 注释
# ⚠️ 当期为一季报(Q1)时 SUE 恒为 0（YTD=Q1 导致 e_expected=e_actual）
# 调用方应避免用 Q1 作 current_report（本策略 _pick_report_periods 只选 6/30/9/30/12/31）
```

**防什么**：Q1 的 YTD = Q1 本身（累计就一个季度）。算 g 时 `ytd_cur = Q1`、`ytd_prev = 去年Q1`，推出 g = (Q1 − 去年Q1) / 去年Q1。然后 E_expected = 去年Q1 × (1+g) = Q1 = E_actual → SUE 恒为 0。这是算法的结构性缺陷，只能规避（不用 Q1 作报告期），无法修复。

#### 小结：7 条规则的分工

```
                    E_actual（分子）
                   ┌── ① 防前视（数据可见性）
                   ├── ② E_actual 不为空
                   │
              E_expected（分母）
                   ├── ③ 去年同期单季 ≥ 1亿（不微利/不亏损）
                   ├── ④ 季度数齐全（g 不失真）
  SUE = ─────────  ├── ⑤ 去年同期累计 > 0（不是扭亏股）
       |E_expected|  ├── ⑥ E_expected ≥ 1亿（分母不爆炸）
                   │
                  报告期
                   └── ⑦ 不用 Q1（结构性恒 0 规避）
```

这 7 条规则在 `tests/test_sue.py` 里各有专门的用例覆盖（`test_excludes_future_announce_date` / `test_excludes_prev_year_loss` / `test_excludes_small_expected` / `test_excludes_missing_prev_year` / `test_excludes_incomplete_quarters`），不信可以跑测试。

---

## 五、调仓日计算（月度，与 01e 的季度版不同）

> 文件：`strategy/qmt/qmt_common/rebalance.py`
> 对应测试：`tests/test_rebalance.py`

### 5.1 规则：每月第一个交易日

01a 是**月度调仓**（不是 01e 的季度调仓）。为什么这么频繁？因为 SUE 信号**衰减极快**——研报实测"晚一个月买入基本无收益"。所以必须每月及时调仓，捕捉最新的财报超预期信号。

调仓日是**每月第一个交易日**（华创法）：

```python
def compute_monthly_rebalance_dates(calendar_df):
    """每月第一个交易日（华创法，与 SUE 因子原始设计一致）。"""
    df = calendar_df[calendar_df["is_open"] == 1].copy()
    df["trade_date"] = pd.to_datetime(df["trade_date"]).dt.date
    df = df.sort_values("trade_date").reset_index(drop=True)
    dates = df["trade_date"].tolist()

    rebalance = set()
    prev_month = None
    for d in dates:
        if d.month != prev_month:      # 月份变了 → 新月第一个交易日
            rebalance.add(d)
            prev_month = d.month
    return rebalance
```

逻辑很直白：遍历排序后的交易日，某天的月份和前一天不同 → 这天是新月第一个交易日。回测 5 年约 60 个调仓日（一年 12 个月 × 5 年）。

> ⚠️ **月度调仓的代价是高换手**。60 只满仓每月全部刷新，年换手率约 12 倍。如果双边交易成本千三，年费率约 3.6%，会显著吃掉收益。这是 SUE 月度策略的固有成本，研报原文（华创 20.0%）也未计交易费用。

---

## 六、报告期选取与"提前机制"（01a 最容易翻车的地方）

> 文件：`strategy/qmt/pead_01a_sue.py` 里的 `_pick_report_periods` / `_candidate_reports`
> 文件：`strategy/qmt/qmt_common/db_reader.py` 里的 `pick_report_with_forecast`

### 6.1 基础规则：纯日期映射

和 01e 一样，01a 先用纯日期映射确定"默认用哪个报告期"。规则是"最近一个已结束的报告期"：

```python
def _pick_report_periods(bar_date):
    y, m = bar_date.year, bar_date.month
    if m <= 4:      # 1-4月 → 去年三季报（年报还没披露完）
        cur = date(y - 1, 9, 30)
    elif m <= 7:    # 5-7月 → 去年年报（4月底披露完了）
        cur = date(y - 1, 12, 31)
    elif m <= 10:   # 8-10月 → 今年中报（8月底披露完了）
        cur = date(y, 6, 30)
    else:           # 11-12月 → 今年三季报（10月底披露完了）
        cur = date(y, 9, 30)
    return cur.isoformat(), ...
```

| 调仓月份 | 默认报告期 | 理由 |
|---|---|---|
| 1-4 月 | 去年三季报 (9/30) | 年报 4 月底才披露完 |
| 5-7 月 | 去年年报 (12/31) | 年报 4 月底已全披露 |
| 8-10 月 | 今年中报 (6/30) | 中报 8 月底已全披露 |
| 11-12 月 | 今年三季报 (9/30) | 三季报 10 月底已全披露 |

### 6.2 进阶：报告期提前（吃时效红利）

SUE 信号衰减快，能早用一份更新的报告期就尽量早用。比如 2 月调仓，默认用去年三季报（9/30），但如果去年年报的定期报告已经批量披露了，应该提前到年报（12/31）——年报信息更新，SUE 信号更鲜活。

`_candidate_reports` 生成候选列表（"更新优先"排序），`pick_report_with_forecast` 逐个检查"该报告期是否已可用"，选第一个可用的：

```python
# pead_01a_sue.py:215-227
if m <= 4:
    # 默认去年三季报；候选加去年年报
    candidates = ["%d-12-31" % (y - 1), "%d-09-30" % (y - 1)]
elif m <= 10:
    # 默认今年中报；候选加今年三季报
    candidates = ["%d-09-30" % y, "%d-06-30" % y]
```

### 6.3 翻了三次车的提前门槛（核心教训）

"该报告期是否已可用"的判断门槛，经历了三个版本的演进。这是 01a 回测过程中最曲折的调试经历——每个版本都有不同的 bug，值得逐个剖析。

#### v1：LIMIT 1（1 条就提前）

```python
# 第一版：有 1 条预告就提前
cur.execute("SELECT 1 FROM performance_forecast "
            "WHERE notice_date <= %s AND report_date = %s LIMIT 1", ...)
if cur.fetchone() is not None:
    return report  # 提前！
```

**Bug**：8 月初调仓时，三季报（9/30）才刚开始披露，全市场只有 1-2 只股票发了预告。但这 1 条预告触发了 `LIMIT 1`，报告期被提前到三季报。而三季报定期报告此时 0 条 → SUE 建不了模 → **候选池枯竭，持仓暴跌到 1-2 只**。

#### v2：预告数 ≥ 100

```python
# 第二版：预告数达 100 才算"批量发布"
cur.execute("SELECT COUNT(*) FROM performance_forecast ...")
if cnt >= 100:
    return report
```

**Bug**：三季报预告总量天生就少（全市场才 209 条，因为三季度报告发预告的公司不多）。10 月初时三季报预告已达 165 条（> 100），触发提前。但三季报**定期报告**此时只有 0-20 条 → **SUE 还是建不了模，候选池仍然枯竭**。

根本原因：预告数 ≠ 定期报告数。预告是"部分公司的自愿披露"，定期报告才是"全市场的强制披露"。SUE 建模需要定期报告（历史 N 季的基线），光有预告补的当期 E_actual 不够。

#### v3：定期报告 ≥ 500（当前版）

```python
# 第三版（当前）：定期报告已披露 ≥ 500 才提前
cur.execute("SELECT COUNT(*) FROM financial_quarterly "
            "WHERE announce_date <= %s AND report_date = %s", ...)
if cnt >= REPORT_DISCLOSED_THRESHOLD:  # 500
    return report
```

**为什么是 500**：全 A 股约 5000 只，500 是 1/10。定期报告披露呈"截止日前集中爆发"的特征——法定截止日前几周才批量出来：

| 报告期 | 披露窗口 | 达到 500 的大致时点 |
|---|---|---|
| 中报 (6/30) | 7/1 ~ 8/31 | 8 月中下旬 |
| 三季报 (9/30) | 10/1 ~ 10/31 | 10 月下旬 |
| 年报 (12/31) | 次年 1/1 ~ 4/30 | 4 月下旬 |

设 500 意味着：只有定期报告真的批量披露了（不是零星几条）才提前。这和 SUE 建模的硬依赖一致——没有足够的定期报告基线，提前到新报告期也没意义。

**效果**：v3 之后，持仓数全程稳定在 58-61 只（回测 60 个调仓日，43 天满仓 60 只），不再有个位数暴跌。

#### 教训总结

```
v1 的错：混淆了"存在"和"批量"      → 1 条 ≠ 批量
v2 的错：混淆了"预告"和"定期报告"   → 预告覆盖 ≠ 定期覆盖
v3 对了：直接看 SUE 的硬依赖          → 定期报告披露数
```

这个教训的通用版本是：**判断一个数据源"是否可用"，要看你的算法对它的硬依赖是什么**。SUE 建模硬依赖定期报告（历史基线），那就直接看定期报告的披露进度，而不是看辅助数据源（预告）的进度。

---

## 七、业绩预告补覆盖（01a 独有的数据合并）

> 文件：`strategy/qmt/qmt_common/db_reader.py` 里的 `load_performance_forecast`
> 文件：`strategy/qmt/pead_01a_sue.py` 里的 `_merge_financial_and_forecast`

### 7.1 为什么需要预告

定期报告有"披露窗口"——中报 7-8 月陆续发，但有些公司拖到 8 月底。如果调仓日是 8 月初，很多公司的中报还没发，它们就没有当期 E_actual。但这些公司里，有一部分提前发了**业绩预告**（预告整个报告期的利润范围），可以用来补 E_actual。

### 7.2 预告转单季的坑

业绩预告给的是**报告期累计 YTD**（如中报预告是 H1 上半年累计），不是单季值。而 SUE 需要单季值。所以要转换：

```
中报预告单季 = 预告 H1 累计均值 − 已披露的 Q1 累计
```

转换在 `load_performance_forecast`（`db_reader.py:119-211`）里做。预告取值用 `(profit_min + profit_max) / 2`（上下限均值，和研报原文一致）。

### 7.3 合并规则：定期优先，预告只补缺口

```python
# pead_01a_sue.py:248-257
# 当期在 financial_quarterly 里已有的 symbol（定期已发，不用预告）
cur_in_fin = set(df_fin[df_fin["report_date"] == cur_report]["symbol"])
# 预告只保留 financial_quarterly 当期缺失的股票
fc_to_add = df_forecast[~df_forecast["symbol"].isin(cur_in_fin)
                        & (df_forecast["report_date"] == cur_report)]
```

**为什么定期优先**：定期报告是审计过的确定值，预告是预测范围（还可能是区间）。同一只股票如果定期报告已发，用定期（更准）；预告只为"定期还没发"的股票提供 E_actual。

---

## 八、handlebar 主循环

> 文件：`strategy/qmt/pead_01a_sue.py`

把前面所有零件组装起来。整体流程就是第三节的 7 步流水线，这里把关键步骤对应到代码（省略了和 01e 相同的回测/实盘分支）：

```python
def handlebar(C):
    bar_date = ...  # 从 QMT 拿当前 K 线日期

    # ① 非调仓日跳过（月度调仓日集合在 init 里预计算）
    if bar_date not in G.rebalance_dates:
        ...  # 最后一根 bar 时 flush 净值
        return

    # 幂等保护：同一调仓日只执行一次（防 QMT 同 bar 多次触发）
    if not G.guard.should_run(bar_date):
        return

    # ② 确定当期报告期（纯日期映射 + 定期报告已批量则提前）
    report_candidates, default_report = _candidate_reports(bar_date)
    cur_report = db_reader.pick_report_with_forecast(
        G.conn, bar_date, report_candidates, default_report)

    # ③ 读单季利润表（当期+全部历史，防前视 announce_date <= as_of）
    df_fin = db_reader.load_financial_quarterly(G.conn, as_of=bar_date,
                                                current_report=cur_report)
    # ③' 业绩预告补覆盖（定期未发的用预告补）
    df_forecast = db_reader.load_performance_forecast(
        G.conn, as_of=bar_date, current_report=cur_report)
    if not df_forecast.empty:
        df_fin = _merge_financial_and_forecast(df_fin, df_forecast, cur_report)

    # ④ 算 SUE 因子（7 条防失真剔除在函数内部）
    sue_df = sue.compute_sue_for_rebalance(df_fin, as_of=bar_date,
                                           current_report=cur_report)

    # ⑤ 过滤：上市>250天 / 非ST + 剔除 SUE≤0（只做多头）
    candidates = _filter_universe(sue_df, df_fin, bar_date)
    candidates = candidates[candidates["sue"] > 0]

    # ⑥ 选股：SUE 降序选前 60 只，顺位剔除一字涨跌停
    selected = _select_with_limit_check(candidates, C, bar_date, HOLDINGS)
    target = {row["symbol"]: 1.0 / HOLDINGS for _, row in selected.iterrows()}

    # ⑦ 下单（回测用 passorder 虚拟撮合，实盘用 passorder 批量调仓）
    _execute_backtest(C, target, bar_date)
```

**和 01e 的 handlebar 对比**，差异在 ②③'④⑤ 这几步：01a 多了报告期提前（②）、预告补覆盖（③'）、SUE 计算（④）、多头过滤（⑤ 的 `sue > 0`）。01e 的因子（dReport）可以是负值（负值=提前披露=好），而 01a 的 SUE 只取正值（正值=超预期=好，负值剔除）。

---

## 九、其余模块概览

### 9.1 过滤层（`_filter_universe`，与 01e 共用）

| 过滤 | 怎么实现 | 为什么 |
|---|---|---|
| 上市 >250 天 | `(bar_date - listed_date).days > 250` | 剔除新股异常波动 |
| 非 ST | 利润表 stock_name 是否含 ST/PT（近似版）| ST 股流动性差、风险高 |

ST 过滤是**近似版**——stock_name 是抓取时的快照，不是严格的历史 ST 时序。起步阶段够用。

> ⚠️ **与研报的差距**：华创原文有 6 条硬过滤（超预期幅度 >10%、机构数 ≥5、PE_TTM ∈ (0,50)、累计同比 ∈ (20%,200%)、评级、上市天数），当前实现只有 2 条（上市天数 + ST）。6 条里有 3 条依赖分析师数据（机构数、PE、评级），当前口径下不适用。这是绩效差距的来源之一。

### 9.2 选股与下单（`_select_with_limit_check` / `_rebalance`，与 01e 共用）

选股时按 SUE 降序，逐只取头部 `holdings × 2`（120 只）备选，剔除当日一字涨跌停（`high == low` 无法成交），够 60 只就停。

下单用 `passorder` 按股数下单（不用 `order_target_percent`），先卖后买，买入按"可用资金 / 剩余只数"均分。这套逻辑从 01e 移植过来，原因见 [01e 实现讲解 §8.4](./PEAD-01e-实现讲解.md) 和开发指南的避坑清单。

### 9.3 净值记录（`nav_logger`，与 01e 共用）

只在调仓日记录净值（不在每个交易日调 `get_trade_detail_data`——实测会导致回测尾部卡死）。净值写 `backtest_nav` 表，用 `scripts/calc_perf.py` 算绩效。

---

## 十、关键设计决策回顾

| 决策 | 选了什么 | 为什么 |
|---|---|---|
| SUE 用历史同比增速法 | 不用分析师法 | 同花顺拿不到历史分析师预测（只有当前快照），改用隐含同比增速近似 |
| 分母用 abs(E_expected) | 不用标准差 σ | 标准差需要多机构预测分歧度，没有分析师数据就算不了 |
| MIN_ABS_EXPECTED = 1e8 | 不用更小阈值 | 1e7 时 SUE 爆炸（abs 最高 56），1e8 后分布健康（mean≈0, std≈0.44）|
| 月度调仓 | 不用季度 | SUE 信号衰减极快（晚一个月基本无收益），必须及时调 |
| 报告期提前看定期报告 ≥500 | 不看预告数 | SUE 建模硬依赖定期报告（历史基线），预告只是辅助补充 |
| 定期优先 + 预告补缺口 | 不混用 | 定期是审计确定值，预告是预测范围，同一只有定期的用定期 |
| Q1 不作报告期 | 不强行算 | Q1 的 YTD = Q1 导致 E_expected = E_actual → SUE 恒 0（结构性缺陷） |
| 工具函数放 `qmt_common/` 纯模块 | 不放主策略里 | 与 QMT 环境解耦，开发机能单测，QMT 能 import |
| 防前视在 SQL + Python 两层做 | 不只在一层 | 双保险，SQL 漏了 Python 兜底，且 Python 层可单测 |
| 共享 01e 的工程层 | 不重写 | rebalance_guard / nav_logger / _rebalance 已被 01e 验证，避免重复踩坑 |

---

## 十一、与研报原文的偏差（诚实清单）

本策略是研报 SUE 因子的**简化近似版**，以下是已知偏差，按影响程度排列：

### 重大偏差（影响绩效对标）

| 维度 | 研报原文 | 当前实现 | 影响 |
|---|---|---|---|
| 分母口径 | 口径A：分析师分歧度 σ（华创法） | abs(E_expected) | SUE 量纲不同，不可直接对标 |
| E_expected | 分析师一致预测中位数 | 去年同期 × (1+同比增速) | 预期基准不同 |
| 中性化 | 国君用市值行业严格中性（组合优化）| 完全未做 | 收益含市值/行业风格暴露 |
| 过滤规则 | 华创 6 条硬过滤 | 仅上市天数 + ST | 选股精度低，持仓更杂 |

### 小偏差（影响有限）

| 维度 | 研报原文 | 当前实现 | 影响 |
|---|---|---|---|
| 持仓数 | 前 10% 或前 50 | 固定 60 | 60 在合理范围内 |
| 交易成本 | 双边千三 | 定义了但未显式扣 | 需确认 QMT 引擎是否自动扣 |

### 一致的关键设计（做对了的）

- E_actual 用单季归母净利 ✅
- 单季值用累计相减 ✅
- 业绩预告取上下限均值 ✅
- 只做多头端 ✅
- 月度调仓、每月首个交易日 ✅
- 等权持仓 ✅
- 不带漂移项（选股场景） ✅

> 💡 **绩效对标的正确姿势**：当前实现的年化收益不应直接和国君 12.10% 对标（口径不同）。它验证的是"业绩超预期 alpha 在 A 股存在"这个命题。要追齐研报绩效，需补分析师历史数据（口径A）+ 中性化 + 过滤规则。

---

## 附录：相关文档导航

- **策略原理** → [01a 策略设计](../../strategy-directions/strategy-designs/01-pead/01a-pead-sue-single-factor.md)
- **各家研报横向对比** → [PEAD playbook](../../strategy-directions/strategy-playbooks/01-pead-earnings-surprise.md)
- **数据采集层** → [数据采集实现讲解](./PEAD-01a-SUE数据采集-实现讲解.md)
- **工程层（调仓/过滤/下单/净值）** → [01e 实现讲解](./PEAD-01e-实现讲解.md) §五~§八
- **环境配置与避坑** → [QMT 策略开发指南](./QMT策略开发指南.md)
- **SUE 因子概念** → [wiki/concepts/sue因子.md](../../wiki/concepts/sue因子.md)
- **SUE 综合分析（含口径分歧）** → [wiki/syntheses/sue因子-综合分析.md](../../wiki/syntheses/sue因子-综合分析.md)
