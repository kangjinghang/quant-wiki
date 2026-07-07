# PEAD 01e 披露时点策略 · 实现讲解

> **本文定位**：这是一份**面向学习者的实现讲解**，不是设计文档、不是计划文档。已有的三份文档各有分工：
>
> | 文档 | 回答什么问题 | 你什么时候看 |
> |---|---|---|
> | [01e 策略设计](../../strategy-directions/strategy-designs/01-pead/01e-pead-disclosure-timing.md) | 赚什么钱？为什么有效？绩效预期？ | 想理解策略原理时 |
> | [QMT 落地 spec](../superpowers/specs/2026-07-07-pead-01e-disclosure-qmt-design.md) | 整体架构？数据流？关键决策？ | 想知道工程怎么搭时 |
> | [实现计划（12 任务）](../superpowers/plans/2026-07-07-pead-01e-disclosure-qmt.md) | 每一步具体做什么？怎么测？ | 要动手实现时 |
> | **本文（实现讲解）** | **代码为什么这么写？关键函数逐行在干嘛？** | **想读懂代码、理解每行在算什么时** |
>
> 本文聚焦**最精华的几块**（dReport 因子计算、调仓日、handlebar 主循环）逐行讲透并配数值例子；其余模块（采集层、DB 层、过滤层、实盘下单）只讲思路和关键点。
>
> **配套**：[QMT 策略开发指南](./QMT策略开发指南.md)（三工作区环境、东财接口实测笔记、避坑清单）。

---

## 一、阅读准备

### 1.1 你需要先知道的事

- **QMT**：迅投的交易终端，内置一个 Python 3.6.8 解释器，提供 `handlebar`（每根 K 线触发）、`passorder`（下单）、`get_market_data_ex`（取行情）等全局函数。策略代码跑在它内部。
- **handlebar 模型**：QMT 是**事件驱动**——你写两个固定签名的函数 `init(C)` 和 `handlebar(C)`，QMT 来调用。回测时遍历历史 K 线，每根调一次 `handlebar`；实盘时实时触发。
- **QuantVoyager**：另一个独立项目（Python 3.10），负责数据采集和落库，跟策略代码解耦。

### 1.2 三个角色

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

**为什么要分三层**，一句话总结：行情走 QMT 自带（回测实盘同源、不重复缓存），非行情数据进 MySQL（披露日、市值这些 QMT 拿不到的东西），采集用独立的 Python 3.10（能用最新库，不被 QMT 的老解释器绑住）。

---

## 二、代码地图

策略代码在 `QuantVoyager/strategy/qmt/` 目录下，分工如下：

```
strategy/qmt/
├── pead_01e_disclosure.py     # 主策略文件（init + handlebar，跑在 QMT 里）
└── qmt_common/                # 共享工具模块（纯 Python，可单测）
    ├── dreport.py             # ★ dReport 因子计算（本文重点）
    ├── rebalance.py           # ★ 调仓日计算（本文重点）
    └── db_reader.py           # MySQL 读取（pymysql 直连）
```

**为什么把工具拆出来放 `qmt_common/`**：因为这些是**纯函数**（只依赖 pandas + datetime），不依赖 QMT 的全局函数。好处有两个：
1. 能在开发机 Python 3.10 + pytest 里跑单元测试（QMT 的 `handlebar`/`passorder` 在开发机没有，没法测）；
2. QMT 的 Python 3.6 也能 import 它（只用了标准库 + pandas）。

**核心逻辑和环境解耦**——这是本策略代码最重要的工程习惯。所以下面三节（dReport、调仓日、报告期选取）讲的都是 `qmt_common/` 里的纯函数，你可以离开 QMT 直接学。

---

## 三、数据怎么流动（先看全局再看细节）

一次调仓的完整数据流，从 MySQL 到下单：

```
              handlebar(C) 被某根 K 线触发
                       │
                       ▼
        ┌─────────────────────────────────┐
        │ ① 是调仓日吗？                  │ ← rebalance.compute_rebalance_dates 预计算
        │    if bar_date not in G.rebal:  │
        │        return                   │
        └─────────────────────────────────┘
                       │ 是调仓日
                       ▼
        ┌─────────────────────────────────┐
        │ ② 确定今年/去年报告期            │ ← _pick_report_periods（按调仓月份判断）
        │    cur = 去年12/31 等            │
        │    prev = 前年12/31 等           │
        └─────────────────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────┐
        │ ③ 读披露日数据（今年+去年）      │ ← db_reader.load_disclosure
        │    SELECT … WHERE report_date   │   防前视在这里：actual/book 可见性
        │    IN (cur, prev)               │   在下一步 dreport 里用 as_of 处理
        └─────────────────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────┐
        │ ④ 算 dReport 因子               │ ← dreport.compute_dreport_for_rebalance
        │    对每只股票：                  │   ★ 本文第四节重点
        │    选今年披露日（防前视）         │
        │    dReport = 今年 − 去年对齐     │
        └─────────────────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────┐
        │ ⑤ 过滤：上市>250天/非ST/非停牌  │ ← _filter_universe
        │    用 get_market_data_ex 取行情  │
        └─────────────────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────┐
        │ ⑥ 选股：dReport 升序取前 60 只   │
        │    target = {symbol: 1/60}      │   等权
        └─────────────────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────┐
        │ ⑦ 回测 vs 实盘                   │ ← C.is_last_bar() 区分
        │    回测：记录持仓和净值           │
        │    实盘：passorder 下单          │
        └─────────────────────────────────┘
```

记住这个 7 步流水线，下面几节就是在拆解其中的 ②③④。

---

## 四、dReport 因子计算（最精华的一块）

> 文件：`strategy/qmt/qmt_common/dreport.py`
> 对应测试：`tests/test_dreport.py`

### 4.1 dReport 想量什么（先建立直觉）

dReport 想量的不是"两个日期差了多少天"，而是：

> **"今年披露的早/晚，相对去年同期，是提前了还是延后了？"**

关键词是**相对**。它问的是公司披露**行为的变化**。

举个例子，看 2024 年报（对标 2023 年报）：

| 公司 | 去年披露日（2023年报） | 今年披露日（2024年报） | 直觉判断 |
|---|---|---|---|
| 茅台 | 2024-04-03 | 2025-03-28 | 今年抢跑，提前了 |
| 暴雷公司 | 2024-03-20 | 2025-04-25 | 今年躲到 4 月底，延后了 |

注意"去年披露日"和"今年披露日"是**跨年**的（去年年报在 2024 年披露，今年年报在 2025 年披露）。这正是最容易翻车的点，下面专门讲。

### 4.2 关键坑：跨年相减必须先"年份对齐"

人脑怎么判断"茅台提前了几天"？你会这样想：

> 茅台去年是 4/3 披露的，今年 3/28 披露的，3/28 比 4/3 早 6 天。

这个"提前 6 天"背后，你**潜意识里把去年 4/3 拉到了今年**（变成 2025-04-03），再和今年的 3/28 比。这就是"年份对齐"——把两年放到同一个年份里比，才能消除那 365 天的偏移，剩下的才是"提前/延后"的纯信号。

```
茅台正确算法：
  把去年披露日 2024-04-03 的年份改成 2025 → 2025-04-03（这就是"对齐"）
  今年披露日 2025-03-28  −  对齐后的 2025-04-03  =  -6 天   ✅ 提前 6 天

如果不做对齐，直接用 Python 日期减法：
  date(2025,3,28) - date(2024,4,3)  =  359 天   ❌ 多算了一整年
```

> ⚠️ **这是策略里最容易翻车的地方**。直接相减会多出 365 天，全市场排序时方向会反掉——"提前最多"的好公司因为差值≈357 被排到最后，当成最差的。这不是理论错，是工程实现错。

### 4.3 代码逐行讲：`_align_year` 和 `_dreport`

```python
def _align_year(d, target_year):
    """
    把日期 d 拉到 target_year 的同月同日。
    用途：让"今年披露日"和"去年披露日"处在同一个年份里，才能正确相减。

    边界处理：2/29（闰日）在非闰年不存在，退化为 2/28。
    这种情况在 A 股极少见（披露日很少卡在 2/29），但写代码要稳妥。
    """
    try:
        return d.replace(year=target_year)
    except ValueError:
        # 只有 2/29 在非闰年会抛 ValueError，退到 2/28
        return d.replace(month=2, day=28, year=target_year)


def _dreport(this_year_date, prev_year_date):
    """
    算单只股票的 dReport（同比披露日变化，天数）。

    负值 = 提前披露（好），正值 = 延后披露（差）。

    参数都是 date 对象，但年份可能不同（跨年）。
    """
    # 关键一步：把去年日期对齐到今年的年份，再相减
    prev_aligned = _align_year(prev_year_date, this_year_date.year)
    return (this_year_date - prev_aligned).days
```

**代入茅台的例子验证**：

```python
this_year_date = date(2025, 3, 28)   # 茅台今年披露日
prev_year_date = date(2024, 4, 3)    # 茅台去年披露日

prev_aligned = _align_year(date(2024,4,3), 2025)  # → date(2025, 4, 3)
dreport = (date(2025,3,28) - date(2025,4,3)).days  # → -6
# 结果 -6，表示提前 6 天，是好信号 ✅
```

再验证一个"延后"的例子：

```python
this_year_date = date(2025, 4, 25)   # 暴雷公司今年披露日
prev_year_date = date(2024, 3, 20)   # 暴雷公司去年披露日

prev_aligned = _align_year(date(2024,3,20), 2025)  # → date(2025, 3, 20)
dreport = (date(2025,4,25) - date(2025,3,20)).days  # → +36
# 结果 +36，表示延后 36 天，是差信号 ❌
```

**排序选股**时，全市场按 dReport 从小到大排，最前面那批就是"提前最多"的好公司。

### 4.4 防前视偏差：`_pick_disclosure_date`

光会算减法还不够，还有个更要命的坑——**前视偏差**。这是 PEAD 策略最容易翻车的地方。

#### 什么是前视偏差（用故事讲）

你是基金经理，**今天 4 月 10 日**要调仓。你打开数据库，看到茅台 2024 年报那行：

```
symbol=600519.SH, report_date=2024-12-31,
actual_report_date=2025-04-25,    ← 实际披露日（4/25，还没到！）
latest_book_date=2025-04-20       ← 预约披露日（早就公告了）
```

陷阱来了：今天才 4/10，4/25 那天**还没发生**。如果你直接拿 `actual_report_date=4/25` 去算 dReport，相当于你 4/10 就"知道"了 4/25 公司会披露——你用了**未来才知道的信息**做决策，这就是前视偏差。

回测里这个 bug 最致命：因为回测是**事后**跑的，所有 `actual_report_date` 数据都"已经知道"，你很容易无脑拿去用，回测曲线漂亮得离谱但**全是假的**。实盘一上就崩。

#### 正确做法：用"调仓日可见的"信息

```python
def _pick_disclosure_date(row, as_of):
    """
    从一行披露数据里，选出"as_of 时点可见的"披露日。

    参数：
      row: 一只股票某个报告期的数据（dict/Series），含
            - actual_report_date: 实际披露日（可能还没到，即 None）
            - latest_book_date:   预约披露日（早就公告的）
      as_of: 调仓日（date 对象），是整个防前视的锚点

    返回：as_of 时点可见的披露日（date），无可见数据则返回 None。
    """
    actual = row.get("actual_report_date")
    book = row.get("latest_book_date")

    # 唯一的判断：actual 必须 <= 调仓日，才能用
    if actual is not None and not pd.isna(actual):
        if _to_date(actual) <= as_of:
            return _to_date(actual)   # 实际披露日可见，优先用（最准）

    # 否则退回预约日（重合度 ≥98%，足够准）
    if book is not None and not pd.isna(book):
        return _to_date(book)

    # 啥都没有（既没披露也没预约），这只股票本期没法算 dReport
    return None
```

**核心就一句**：`actual <= as_of` 才用 `actual`，否则用预约日 `book`。`as_of` 这个参数是防前视的总开关，所有数据都要过它这一关。

#### 验证：4/10 调仓的场景

```python
row = {
    "actual_report_date": date(2025, 4, 25),  # 未到
    "latest_book_date":   date(2025, 4, 20),  # 预约日
}
as_of = date(2025, 4, 10)   # 今天调仓

# 走一遍 _pick_disclosure_date：
# actual=date(2025,4,25), as_of=date(2025,4,10)
# date(2025,4,25) <= date(2025,4,10) 吗？  否（4/25 还没到）
# → 退回 book = date(2025,4,20)
# → 返回 date(2025,4,20)
```

`as_of` 是如何保证防前视的？——它强迫代码每次都问一句"这个日期在调仓日之前吗"。回测时 `as_of` 跟着每根 K 线的日期走，实盘时就是当天，逻辑完全一致。

#### 为什么不直接在 SQL 里过滤？

一个自然的想法：直接在 SQL 加 `WHERE actual_report_date <= :as_of`，省得 Python 里判断。但这样会**漏掉"未披露但有预约日"的股票**（这些股票也能算 dReport，且往往更有价值——市场还没反应过来）。

所以设计上：SQL 只按 `report_date` 取数（今年+去年），**actual/book 的可见性判断全部集中在 `_pick_disclosure_date` 这一个函数**里，由 `as_of` 统一管控。好处是单元测试能直接覆盖边界，不用连数据库就能验证防前视逻辑对不对。

### 4.5 主函数 `compute_dreport_for_rebalance`

把上面两块拼起来——这是给整个股票池算 dReport 的入口：

```python
def compute_dreport_for_rebalance(df, as_of, current_report, prev_report):
    """
    给定调仓日 as_of，计算所有股票的 dReport 因子。

    参数：
      df: 从 disclosure_yysj 表读出的 DataFrame，
          包含"今年"和"去年"两个 report_date 的所有股票记录，
          列含 symbol / report_date / actual_report_date / latest_book_date
      as_of: 调仓日（date），防前视的锚点
      current_report: 今年报告期，如 "2024-12-31"
      prev_report: 去年报告期，如 "2023-12-31"

    返回：DataFrame，列 symbol/dreport/this_year_date/prev_year_date
          dreport 升序排（越小=越提前=越好）
          缺去年数据的股票被剔除（无法算同比）
    """
    if df is None or df.empty:
        return pd.DataFrame(columns=["symbol", "dreport", "this_year_date", "prev_year_date"])

    df = df.copy()
    df["report_date"] = df["report_date"].astype(str)

    # 把 df 拆成两份：今年记录 + 去年记录
    cur = df[df["report_date"] == current_report].copy()
    prev = df[df["report_date"] == prev_report].copy()

    if cur.empty or prev.empty:
        return pd.DataFrame(columns=["symbol", "dreport", "this_year_date", "prev_year_date"])

    # 对每行选可见披露日（防前视，第 4.4 节讲的）
    cur["this_year_date"] = cur.apply(lambda r: _pick_disclosure_date(r, as_of), axis=1)
    prev["prev_year_date"] = prev.apply(lambda r: _pick_disclosure_date(r, as_of), axis=1)

    # 按股票代码合并今年+去年（inner join：两年都有才保留）
    cur_slim = cur[["symbol", "this_year_date"]].dropna(subset=["this_year_date"])
    prev_slim = prev[["symbol", "prev_year_date"]].dropna(subset=["prev_year_date"])
    merged = cur_slim.merge(prev_slim, on="symbol", how="inner")

    if merged.empty:
        return pd.DataFrame(columns=["symbol", "dreport", "this_year_date", "prev_year_date"])

    # 算 dReport（第 4.3 节讲的，含年份对齐）
    merged["dreport"] = merged.apply(
        lambda r: _dreport(r["this_year_date"], r["prev_year_date"]), axis=1
    )
    return merged[["symbol", "dreport", "this_year_date", "prev_year_date"]]
```

**几个设计决策值得记住**：

| 决策 | 为什么这么做 |
|---|---|
| `inner join` 合并今年+去年 | 缺去年数据没法算同比，直接剔除（不能瞎填）|
| `dropna` 丢掉选不出披露日的 | 既没实际也没预约的，本期无信号 |
| 返回 `this_year_date`/`prev_year_date` 两列 | 方便人眼检查结果对不对，调试用 |

### 4.6 一个完整的端到端例子

把上面所有概念串起来。假设调仓日是 **2025-05-07**，看 2024 年报 vs 2023 年报。数据库里就这么几条：

```
symbol     report_date   actual_report_date  latest_book_date
600519.SH  2024-12-31    2025-03-28          2025-03-25    ← 茅台今年
600519.SH  2023-12-31    2024-04-03          2024-04-01    ← 茅台去年
000001.SZ  2024-12-31    2025-04-25          2025-04-20    ← 平安今年
000001.SZ  2023-12-31    2024-03-20          2024-03-18    ← 平安去年
```

**Step 1：拆分今年/去年**

```
cur（2024-12-31）:  茅台、平安的两行
prev（2023-12-31）: 茅台、平安的两行
```

**Step 2：选可见披露日（`as_of = 2025-05-07`）**

```
茅台 cur:  actual=2025-03-28 <= 2025-05-07? 是 → this_year_date = 2025-03-28
茅台 prev: actual=2024-04-03 <= 2025-05-07? 是 → prev_year_date = 2024-04-03
平安 cur:  actual=2025-04-25 <= 2025-05-07? 是 → this_year_date = 2025-04-25
平安 prev: actual=2024-03-20 <= 2025-05-07? 是 → prev_year_date = 2024-03-20
```

（如果调仓日改成 2025-04-10，茅台的 actual=2025-03-28 仍可见，但平安的 actual=2025-04-25 就不可见了，会退回 book=2025-04-20）

**Step 3：合并（inner join）**

```
symbol     this_year_date   prev_year_date
600519.SH  2025-03-28       2024-04-03
000001.SZ  2025-04-25       2024-03-20
```

**Step 4：算 dReport（含年份对齐）**

```
茅台: _dreport(date(2025,3,28), date(2024,4,3))
      = 对齐 → date(2025,4,3)
      = (2025-03-28) - (2025-04-03) = -6 天   ← 提前 6 天 ✅

平安: _dreport(date(2025,4,25), date(2024,3,20))
      = 对齐 → date(2025,3,20)
      = (2025-04-25) - (2025-03-20) = +36 天  ← 延后 36 天 ❌
```

**Step 5：排序选股**

```
按 dreport 升序：
  600519.SH  -6   ← 提前最多，排第一，买入
  000001.SZ  +36  ← 延后，排后面，不买
```

这就是为什么"提前披露的公司"会浮到选股清单的最前面。

### 4.7 配套的单元测试（TDD，先写测试再写实现）

`tests/test_dreport.py` 用 5 个用例覆盖所有边界。这里挑两个最能体现设计的：

```python
def test_dreport_negative_means_early_disclosure(self):
    """dReport 负值 = 提前披露（好）。
    茅台今年 4/20 披露，去年 4/28 披露 → 提前 8 天 → dReport = -8"""
    rows = [
        {"symbol": "600519.SH", "report_date": "2024-12-31",
         "actual_report_date": date(2025, 4, 20), "latest_book_date": date(2025, 4, 20)},
        {"symbol": "600519.SH", "report_date": "2023-12-31",
         "actual_report_date": date(2024, 4, 28), "latest_book_date": date(2024, 4, 28)},
    ]
    df = pd.DataFrame(rows)
    result = compute_dreport_for_rebalance(
        df, as_of=date(2025, 5, 7), current_report="2024-12-31", prev_report="2023-12-31"
    )
    self.assertEqual(result.iloc[0]["dreport"], -8)   # 提前 8 天


def test_excludes_future_actual_date(self):
    """防前视：今年实际披露日 > as_of 时，改用预约日。
    actual=2025-05-10 但调仓日是 4/1，必须用 book=2025-04-25。"""
    rows = [
        {"symbol": "600519.SH", "report_date": "2024-12-31",
         "actual_report_date": date(2025, 5, 10), "latest_book_date": date(2025, 4, 25)},
        {"symbol": "600519.SH", "report_date": "2023-12-31",
         "actual_report_date": date(2024, 4, 28), "latest_book_date": date(2024, 4, 28)},
    ]
    df = pd.DataFrame(rows)
    result = compute_dreport_for_rebalance(
        df, as_of=date(2025, 4, 1), current_report="2024-12-31", prev_report="2023-12-31"
    )
    # 用 book=2025-04-25 算，不是 actual=2025-05-10
    # (2025-04-25) - 对齐(2024-04-28 → 2025-04-28) = -3
    self.assertEqual(result.iloc[0]["dreport"], -3)
```

**为什么要写数值断言（`-8`、`-3`）而不是只断言"是个负数"**：因为数值断言能抓出"符号反了""少了对齐"这类 bug——这些 bug 会让结果变成 +357 而不是 -8，数值断言立刻就挂。

---

## 五、调仓日计算

> 文件：`strategy/qmt/qmt_common/rebalance.py`
> 对应测试：`tests/test_rebalance.py`

### 5.1 规则：季度末后第 5 个交易日

01e 是**季度调仓**（不是月度），调仓日是**每季度结束后第 5 个交易日**。为什么是"第 5 个"而不是"第 1 个"？因为季报披露季刚开始时数据不全（很多公司还没披露），等 5 个交易日让大部分披露数据沉淀下来再用。

四个调仓日对应：

| 季度末 | 调仓日大约 |
|---|---|
| Q1（3/31）结束 | 4 月初第 5 个交易日 |
| Q2（6/30）结束 | 7 月第 5 个交易日 |
| Q3（9/30）结束 | 10 月第 5 个交易日 |
| Q4（12/31）结束 | 次年 1 月第 5 个交易日 |

### 5.2 代码逐行讲

```python
QUARTER_END_MONTHS = (3, 6, 9, 12)   # 季度末月份

def compute_rebalance_dates(calendar_df, n_days_after_quarter_end=5):
    """
    根据交易日历，计算所有调仓日（季度末后第 N 个交易日）。

    参数：
      calendar_df: trade_calendar 表读出的 DataFrame，列含 trade_date / is_open
      n_days_after_quarter_end: 季度末后第几个交易日（默认 5）

    返回：set[date]，所有调仓日（用 set 是为了 O(1) 查询）
    """
    if calendar_df is None or calendar_df.empty:
        return set()

    # 只留交易日（is_open=1），转成 date 对象，按日期排序
    df = calendar_df[calendar_df["is_open"] == 1].copy()
    df["trade_date"] = pd.to_datetime(df["trade_date"]).dt.date
    df = df.sort_values("trade_date").reset_index(drop=True)
    dates = df["trade_date"].tolist()   # 排好序的交易日列表

    rebalance = set()
    for i, d in enumerate(dates):
        # ① 只看季度末月份（3/6/9/12）
        if d.month not in QUARTER_END_MONTHS:
            continue
        # ② 粗筛：必须是月底（28 号以后），不是就跳过（性能优化）
        if d.day < 28:
            continue
        # ③ 精确确认：d 是不是当月最后一个交易日？
        #    判据：下一个交易日的月份是否还是 d.month，如果是，说明 d 不是月底
        if i + 1 < len(dates) and dates[i + 1].month == d.month:
            continue
        # 走到这里：d 就是"季度末最后一个交易日"
        # ④ 取它之后的第 N 个交易日
        if i + n_days_after_quarter_end < len(dates):
            rebalance.add(dates[i + n_days_after_quarter_end])
    return rebalance
```

### 5.3 用例子走一遍

假设交易日历（已排序，只列 3 月底和 4 月初几天）：

```
索引  trade_date
 0   2025-03-28  (周五)
 1   2025-03-31  (周一，3 月最后交易日)  ← 季度末
 2   2025-04-01  (周二)
 3   2025-04-02
 4   2025-04-03
 5   2025-04-04
 6   2025-04-07  (周一，跨周末)
 7   2025-04-08
```

代码走查（`n_days_after_quarter_end=5`）：

```
i=0, d=2025-03-28: month=3 在季度末月，但 day=28>=28 过粗筛
                   检查下一个 dates[1]=2025-03-31，month==3（同月）→ d 不是月底，跳过

i=1, d=2025-03-31: month=3，day=31>=28 过粗筛
                   下一个 dates[2]=2025-04-01，month=4 ≠ 3 → d 是月底 ✅（季度末）
                   取 dates[1+5] = dates[6] = 2025-04-07  → 加入 rebalance

i=2, d=2025-04-01: month=4 不在 (3,6,9,12) → 跳过
（后续 4 月的日子都被这条规则跳过，直到 6 月底再触发一次）
```

**结果**：`{2025-04-07, ...}`（Q1 的调仓日是 4/7）。

### 5.4 为什么要用 `set` 返回

`init` 里算一次 `G.rebalance_dates`（一个 set），`handlebar` 里每根 K 线都查 `if bar_date in G.rebalance_dates`。set 的 `in` 操作是 O(1)，跑几千根 K 线也不会慢。如果用 list，每次都是 O(n) 线性扫描。

### 5.5 为什么不直接用日历库算"第 5 个工作日"

因为 A 股的"交易日"≠"工作日"——节假日（春节、国庆）不开市。比如 10 月国庆后第 5 个交易日，可能要跳过 7 天长假。所以必须用真实交易日历表来数，不能用 `pandas.bdate_range` 这种纯工作日算法。

---

## 六、报告期选取（一个看似简单实则易错的小函数）

> 文件：`strategy/qmt/pead_01e_disclosure.py` 里的 `_pick_report_periods`

### 6.1 问题：调仓日该用哪份财报

调仓日是某个季度末后第 5 个交易日，比如 5/7（Q2 末后）。但"5/7 调仓"要用哪份财报的披露日数据？答案是**最近一个已结束的报告期**：

- 5/7 调仓 → 4 月底年报刚好披露完 → 用**去年年报**（2024-12-31）vs 前年年报（2023-12-31）
- 8/7 调仓 → 7 月底中报刚披露完 → 用**今年中报**（2025-06-30）vs 去年中报（2024-06-30）

### 6.2 代码逐行讲

```python
def _pick_report_periods(bar_date):
    """
    根据调仓日 bar_date，决定要用的今年/去年报告期。

    规则：用"最近一个已结束的报告期"。
    返回：(current_report, prev_report)，都是 "YYYY-MM-DD" 字符串。
    """
    y, m = bar_date.year, bar_date.month
    if m <= 4:
        # 1-4月：去年三季报刚披露完不久，去年年报还没披露完
        # 用去年三季报（9/30）vs 前年三季报
        cur = date(y - 1, 9, 30);  prev = date(y - 2, 9, 30)
    elif m <= 7:
        # 5-7月：4月底年报披露完毕
        # 用去年年报（12/31）vs 前年年报
        cur = date(y - 1, 12, 31); prev = date(y - 2, 12, 31)
    elif m <= 10:
        # 8-10月：8月底中报披露完毕
        # 用今年中报（6/30）vs 去年中报
        cur = date(y, 6, 30);     prev = date(y - 1, 6, 30)
    else:
        # 11-12月：10月底三季报披露完毕
        # 用今年三季报（9/30）vs 去年三季报
        cur = date(y, 9, 30);     prev = date(y - 1, 9, 30)
    return cur.isoformat(), prev.isoformat()
```

### 6.3 几个调仓日的实际输出

| 调仓日 | 月份分支 | current_report | prev_report |
|---|---|---|---|
| 2025-01-10 | m=1, `m<=4` | 2024-09-30（去年三季报）| 2023-09-30 |
| 2025-04-08 | m=4, `m<=4` | 2024-09-30（去年三季报）| 2023-09-30 |
| 2025-05-07 | m=5, `m<=7` | 2024-12-31（去年年报）| 2023-12-31 |
| 2025-08-07 | m=8, `m<=10` | 2025-06-30（今年中报）| 2024-06-30 |
| 2025-11-07 | m=11, else | 2025-09-30（今年三季报）| 2024-09-30 |

### 6.4 为什么边界是 4/7/10，不是 3/6/9/12

这里有个细节值得品味。调仓日是"季度末后第 5 个交易日"，但**报告披露有自己的节奏**：
- 年报披露窗口：次年 1/1 ~ 4/30（4 月底才披露完）
- 中报披露窗口：当年 7/1 ~ 8/31
- 一季报、三季报窗口较短

所以"季度末后第 5 个交易日"调仓时，最新能用的报告期并不是"刚结束的季度"。比如 4 月初（Q1 末后）调仓，年报还没披露完，只能用去年三季报——这就是为什么 4 月调仓对应的 cur 是 9/30 而不是 12/31。

---

## 七、handlebar 主循环

> 文件：`strategy/qmt/pead_01e_disclosure.py`

把前面所有零件组装起来，就是 `handlebar`。它在 QMT 里每根 K 线被调一次。整个流程就是第三节那个 7 步图，下面把每一步对应到代码。

```python
def handlebar(C):
    """每根 K 线触发一次。"""
    # 从 QMT 拿当前 K 线的日期
    bar_dt = timetag_to_datetime(C.get_bar_timetag(C.barpos), "%Y-%m-%d")
    bar_date = datetime.strptime(bar_dt, "%Y-%m-%d").date()

    # ① 非调仓日直接跳过（rebalance_dates 是 init 里预计算的 set）
    if bar_date not in G.rebalance_dates:
        return

    # ② 确定今年/去年报告期（第六节讲的）
    cur_report, prev_report = _pick_report_periods(bar_date)
    if cur_report is None:
        return

    # ③ 读披露日数据（今年+去年两个 report_date）
    df_disc = db_reader.load_disclosure(G.conn, cur_report, prev_report)
    if df_disc.empty:
        return

    # ④ 算 dReport（第四节讲的，as_of = 当前调仓日，防前视）
    dreport_df = dreport.compute_dreport_for_rebalance(
        df_disc, as_of=bar_date,
        current_report=cur_report, prev_report=prev_report
    )
    if dreport_df.empty:
        return

    # ⑤ 过滤：上市天数、停牌、涨跌停（第八节概览）
    candidates = _filter_universe(dreport_df, bar_date, C)
    if len(candidates) == 0:
        return

    # ⑥ 选股：dReport 升序取前 HOLDINGS 只，等权
    candidates = candidates.sort_values("dreport").head(HOLDINGS)
    target = {row["symbol"]: 1.0 / HOLDINGS for _, row in candidates.iterrows()}

    # ⑦ 回测 vs 实盘分支
    if not C.is_last_bar():
        _record_nav_backtest(C, target, bar_date)   # 回测：记录净值
        G.holding = target
    else:
        _execute_live(C, target, bar_date)          # 实盘：passorder 下单
```

**为什么不在每根 K 线都重算 dReport**：因为 ① 把非调仓日直接 `return` 了，一年只算 4 次。`init` 里预计算调仓日集合就是为了这个 O(1) 早退——几千根 K 线里，只有 4 根会真正进入策略逻辑，其余都一两行代码就返回了。

**`C.is_last_bar()` 怎么区分回测/实盘**：QMT 回测时遍历历史 K 线，每一根的 `is_last_bar()` 都是 False；只有跑到最新那根（实盘当下）才是 True。所以同一份代码天然支持两种模式，不需要"回测版/实盘版"分叉。

---

## 八、其余模块概览

这三块不是策略逻辑的核心，但实现时有各自的坑。这里只讲思路和关键点，代码细节看 [实现计划](../superpowers/plans/2026-07-07-pead-01e-disclosure-qmt.md)。

### 8.1 数据采集层（QuantVoyager 侧）

**职责**：从东财 datacenter API 抓披露日 + 交易日历，写入 MySQL 两张新表。

**关键点**：

- **直连东财而非走 akshare**：akshare 是包装层，直连能拿到全部字段（首次预约 / 一/二/三次变更 / 实际披露）。接口是 `datacenter-web.eastmoney.com/api/data/v1/get`，参数 `reportName=RPT_PUBLIC_OP_PREDICTDATE`。
- **分页 + 限速**：东财每页最多返回 200 条，全市场要分页；每页之间 `sleep(random.uniform(0.5, 1.0))` 避免被封。
- **`latest_book_date` 取末次变更**：公司可能改预约日多次（首次预约 → 一次变更 → 二次变更 → 三次变更），取最后一个非空的作为"最新预约日"。
- **`bulk_upsert` 增量更新**：按 `UNIQUE(symbol, report_date)` 去重，重复抓取不会出问题，可以随时补抓历史。

**交易日历**从新浪 `klc_kd.js` 抓，返回的是一段 JS，用正则提取 `klc_kd_data = ["2020-01-02,1", ...]` 里的日期。这个接口比东财的交易日历稳定，而且历史数据全。

### 8.2 MySQL 读取层（`db_reader.py`）

**职责**：策略侧用 pymysql 直连 MySQL，把数据读成 DataFrame。

**为什么不用 SQLAlchemy**：QMT 的 Python 3.6.8 装不上 SQLAlchemy 2.0（依赖需要更新 Python）。pymysql 是纯 Python 实现，能装上，够用。

**三个读取函数**：

```python
load_disclosure(conn, current_report, prev_report)
    # 读披露日数据（今年+去年两个 report_date）
    # 防前视不在这里做（见第四节说明），只按 report_date 取数

load_calendar(conn)
    # 读交易日历（is_open=1 的）

load_stock_universe(conn)
    # 读 A 股股票池 + 上市日 + 流通市值
    # 用于过滤（上市>250天）和市值分盘
```

### 8.3 过滤层（`_filter_universe`）

**职责**：从 dReport 候选里剔除不能买的股票。

**三类过滤**：

| 过滤 | 怎么实现 | 为什么 |
|---|---|---|
| 上市 >250 天 | `(bar_date - listed_date).days > 250` | 剔除新股，避免新股异常波动 |
| 非停牌/非一字涨跌停 | `get_market_data_ex` 取当日行情，判断 `high==low`（一字板无法成交）| 一字板买不进/卖不出 |
| 非 ST | 近似方案：用 `stock_core_indicator` 无 ST 标记；或实盘补 `stock_zh_a_st_em` 实时名单 | ST 股流动性差、风险高 |

**ST 过滤为什么用近似**：因为 ST 状态是**历史时变**的（某股 2021 年是 ST、2023 年摘帽），要精确需要历史 ST 序列。起步阶段用"当日名称是否含 ST/PT"近似即可——01e 的 ST 过滤不是核心，且原文验证 ST 剔除对绩效影响有限。

### 8.4 实盘下单（`_execute_live`）

**职责**：实盘时调 `passorder` 批量调仓。

**调仓顺序**（重要）：

```
1. 先卖出不在目标里的持仓（释放资金）
2. 再买入目标里新进的股票（用释放的资金）
```

如果顺序反了，可能因为资金不够买不进。代码用 `get_trade_detail_data` 查当前持仓，按上面的顺序下单。下单价格用市价单（`passorder` 的 `pricetype=5`），原文用收盘价口径——实盘可改限价单。

---

## 九、关键设计决策回顾

把整篇散落的决策点汇总，这些是理解策略为什么"长这样"的钥匙：

| 决策 | 选了什么 | 为什么 |
|---|---|---|
| 行情走 QMT 自带 | 不入 MySQL | 回测实盘同源、不重复缓存 |
| 非行情数据进 MySQL | 披露日、市值、日历 | QMT 拿不到的东西才存 |
| 防前视集中在因子函数 | 不在 SQL 层做 | 单一入口、可单测覆盖边界 |
| 工具函数放 `qmt_common/` 纯模块 | 与 QMT 环境解耦 | 开发机能单测，QMT 能 import |
| dReport 相减前先年份对齐 | 不直接减 | 跨年相减会多算 365 天，方向反 |
| 回测实盘同代码 | 用 `C.is_last_bar()` 区分 | 避免"回测版/实盘版"分叉 |
| 调仓日预计算成 set | 不每次现算 | O(1) 查询，handlebar 早退 |
| 用 pymysql 不用 SQLAlchemy | 纯 Python，QMT 3.6 能装 | 兼容 QMT 老解释器 |
| 历史数据补抓 2019-2024 | 6 年（回测 5 年 + 同比多 1 年）| dReport 要同比，得多 1 年数据 |

---

## 十、学习路径与练习

### 10.1 建议的学习顺序

1. **先吃透 dReport**（第四节）——这是整个策略的智识核心。在开发机跑 `tests/test_dreport.py` 的 5 个用例，自己改几个日期值看结果。
2. **再理解调仓日**（第五节）——相对简单，但"为什么用交易日历不用工作日"这个点要记牢。
3. **最后看 handlebar**（第七节）——前三步清楚了，handlebar 就是组装，逻辑透明。

### 10.2 自测题（检验理解）

**题 1**：某公司今年披露日 2025-04-25，去年披露日 2024-04-10。dReport 是多少？是提前还是延后？
> 答：对齐后 `(2025-04-25) - (2025-04-10) = +15`，延后 15 天。

**题 2**：调仓日是 2025-04-15，某公司今年 actual_report_date=2025-04-20、latest_book_date=2025-04-18。算 dReport 时今年披露日该用哪个？
> 答：actual=4/20 > as_of=4/15，不可见，退回 book=4/18。

**题 3**：为什么第四节要强调"年份对齐"？如果直接相减会怎样？
> 答：跨年相减会多算 365 天，结果从 -6 变成 359，全市场排序时方向反掉，会选出"延后最多"的公司。

**题 4**：调仓日 2025-08-07（Q2 末后）应该用哪份财报的披露日数据？
> 答：用今年中报（2025-06-30）vs 去年中报（2024-06-30），因为 8 月底中报刚披露完。

**题 5**：为什么调仓日不在 SQL 层加 `WHERE actual_report_date <= :as_of`？
> 答：会漏掉"未披露但有预约日"的股票（这些股票往往更有价值）。所以 SQL 只按 report_date 取数，可见性判断集中在 `_pick_disclosure_date` 单一函数。

---

## 附录：相关文档导航

- **策略原理** → [01e 策略设计](../../strategy-directions/strategy-designs/01-pead/01e-pead-disclosure-timing.md)
- **整体架构与决策** → [QMT 落地 spec](../superpowers/specs/2026-07-07-pead-01e-disclosure-qmt-design.md)
- **逐步实现（12 任务，含完整代码）** → [实现计划](../superpowers/plans/2026-07-07-pead-01e-disclosure-qmt.md)
- **环境配置与避坑** → [QMT 策略开发指南](./QMT策略开发指南.md)
