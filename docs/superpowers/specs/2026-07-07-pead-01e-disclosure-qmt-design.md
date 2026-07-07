# PEAD 01e 披露时点策略 · QMT 落地设计

> **状态**：已实现 ✅（数据层 + 采集层 + 策略层完成，服务器数据已落库；QMT 回测待人工执行）
> **日期**：2026-07-07
> **策略**：PEAD 家族 01e（披露时点 / dReport 因子）
> **落地形态**：QMT 内置 Python 3.6 回测 + 实盘（同代码）
> **设计依据**：[01e 策略详细实现](../../../strategy-directions/strategy-designs/01-pead/01e-pead-disclosure-timing.md) + [01-pead playbook](../../../strategy-directions/strategy-playbooks/01-pead-earnings-surprise.md)

---

## 一、背景与目标

### 1.1 为什么先做 01e

PEAD 家族 5 个策略（01a SUE / 01b Plus 五因子 / 01c Plus 2.0 / 01d AOG / 01e 披露时点）经核实原文与 akshare 接口后，按"数据可得性 + 落地难度"排序，01e 最适合作为第一个落地项目：

| 策略 | 数据降级幅度 | 落地难度 | 优先级 |
|---|---|---|---|
| **01e 披露时点** | 最小（8-9 折，仅需披露日）| ⭐ 最低 | ⭐⭐⭐ |
| 01d AOG 量价 | 最小（8-9 折，仅需开盘价）| ⭐ 低 | 后续 |
| 01a SUE 单因子 | 中（6-7 折，依赖分析师覆盖）| ⭐⭐ 中 | 后续 |
| 01b/01c Plus | 大（5-6 折，含微观因子降级）| ⭐⭐⭐⭐ 高 | 后续 |

**目标**：跑通 01e，验证整条"数据采集 → MySQL → QMT 信号 → 下单"链路，为后续策略打地基。

### 1.2 赚什么钱

公司发布财报的**披露时点本身**蕴含基本面信息：好公司对业绩有信心倾向于尽早披露，差公司倾向拖延。dReport = 今年披露日 − 去年同期披露日（负值=提前=好），这个因子与各大类因子相关性 <3%（招商 2021 §三.4），是独立 alpha。

### 1.3 原文绩效（招商定量 2021）

| 股票池 | 多头年化 | 多头超额 | 对冲年化 |
|---|---|---|---|
| 小盘股 | 19.29% | +12.26% | 11.71% |
| 全 A | 15.51% | +8.48% | 8.49% |
| 沪深300 | 7.83% | +1.3% | — （无效）|

**主战场是中小盘**，沪深300 不用此策略。预期实战绩效为原文 8-9 折。

---

## 二、核心决策（经 brainstorming 确认）

| 决策项 | 选定方案 | 理由 |
|---|---|---|
| **首个策略** | 01e 披露时点 | 数据需求最小、逻辑独立、验证整条链路 |
| **运行模式** | QMT 内置 Python（handlebar 回测 + 实盘）| 回测实盘同源，最直接 |
| **数据仓库** | 复用已有 MySQL quant_voyager 库 | 服务器已装 MySQL 8.0.45，QMT 同机 |
| **数据采集** | 扩展 QuantVoyager 项目（requests 直连东财）| 已有成熟采集框架，不重新造轮子 |
| **策略逻辑位置** | QMT 内置 Python | 回测实盘完全同代码 |
| **下单方式** | QMT 内置 passorder | 与回测同源，不需 miniQMT |
| **存储形式** | MySQL（不用文件仓库）| 多策略共享、增量更新干净、SQL 查询灵活 |

---

## 三、整体架构

```
服务器 152.136.15.72（单机：QMT + MySQL + QuantVoyager 同机）
═══════════════════════════════════════════════════════════

┌─ MySQL quant_voyager 库（localhost:3306）─────────────────┐
│  已有表（直接复用）：                                     │
│    sec_basic_info        股票池 + 上市日（5522 只 A 股）  │
│    stock_core_indicator  流通市值 / PE / 总市值           │
│  【本次新增】：                                           │
│    disclosure_yysj       预约/实际披露日（01e 核心）      │
│    trade_calendar        交易日历（算调仓日）             │
└───────────────────────────────────────────────────────────┘
        ▲ safe_request 写                    ▲ pymysql 读 (as_of 切片)
        │                                     │
┌───────┴──────────────────────┐   ┌──────────┴──────────────────────┐
│  QuantVoyager/ (Python 3.10) │   │  QMT 内置 Python 3.6            │
│  职责：数据采集 + 落库        │   │  职责：策略逻辑 + 回测 + 下单   │
│  复用：                       │   │                                  │
│   data_collector.py safe_req │   │  strategy/qmt/                   │
│   data_models.py  BaseModel  │   │   └─ pead_01e_disclosure.py      │
│   data_storage.py bulk 写库  │   │      ├─ init(C)   连 MySQL+加载  │
│   scheduler.yaml  APScheduler│   │      ├─ handlebar(C) 主循环      │
│  新增：                       │   │      │   ├─ 调仓日判断          │
│   +DisclosureYysj 模型       │   │      │   ├─ dReport 因子(as_of) │
│   +TradeCalendar 模型        │   │      │   ├─ 过滤(ST/上市/停牌)  │
│   +scrape_disclosure_yysj()  │   │      │   ├─ 选股(等权 top N)    │
│   +scrape_trade_calendar()   │   │      │   └─ 下单/记录净值       │
│   +scheduler 季度任务         │   │      └─ 辅助函数               │
└──────────────────────────────┘   │                                  │
                                    │  数据来源：                     │
                                    │  ├─ MySQL(localhost) 披露日等  │
                                    │  └─ get_market_data_ex 行情    │
                                    │      + passorder 下单          │
                                    └─────────────────────────────────┘
```

**三层职责清晰分离**：
1. **QuantVoyager**（外部 Python 3.10）= 数据采集与落库，与策略逻辑解耦
2. **MySQL** = 数据仓库，所有策略共享
3. **QMT 内置 Python 3.6** = 策略逻辑、回测、实盘下单

**关键设计原则**：
- 行情走 QMT 自带（`get_market_data_ex`），不进 MySQL——回测实盘同源、不重复缓存
- 非行情数据进 MySQL（披露日、市值等）——QMT 拿不到的才存
- 防前视偏差在 SQL 层用 `as_of` 切片统一处理
- 回测实盘同代码——同一份 `pead_01e_disclosure.py`，靠 `C.is_last_bar()` 区分

---

## 四、数据层设计

### 4.1 新增表 1：`disclosure_yysj`（预约/实际披露日，01e 核心）

```sql
CREATE TABLE disclosure_yysj (
    seq                 BIGINT AUTO_INCREMENT PRIMARY KEY,
    symbol              VARCHAR(160)  NOT NULL COMMENT '唯一代码 如 600519.SH',
    stock_code          VARCHAR(200)  NOT NULL COMMENT '股票代码 如 600519',
    stock_name          VARCHAR(840)  COMMENT '股票简称',
    report_date         DATE          NOT NULL COMMENT '报告期 如 2024-12-31',
    first_book_date     DATE          COMMENT '首次预约时间',
    latest_book_date    DATE          COMMENT '最新预约时间(取末次变更)',
    actual_report_date  DATE          COMMENT '实际披露时间(NULL=未披露)',
    ctime               DATETIME DEFAULT CURRENT_TIMESTAMP,
    utime               DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uniq_symbol_reportdate (symbol, report_date),
    INDEX idx_reportdate (report_date),
    INDEX idx_actual (actual_report_date)
) COMMENT '预约/实际披露日（01e dReport 因子核心数据）';
```

**字段设计依据**：东财 `stock_yysj_em` 输出"首次预约时间 / 变更日期 / 实际披露时间"，正好覆盖 dReport 所需。

**dReport 计算规则**（在 QMT 策略里实现）：
```
披露日取值（按可见性优先）：
  若 actual_report_date <= as_of：用 actual_report_date
  否则（未披露）：用 latest_book_date（预约日，重合度≥98%）

dReport = 今年披露日 − 去年同期披露日
  负值 = 提前披露（好）
  正值 = 延迟披露（差）
```

**历史数据需求**：回测 5 年（2020-2024）需抓 6 年披露日（2019-2024，多 1 年用于算同比）。东财 `stock_yysj_em` 的 `date` 参数从 20081231 起可用，历史可补抓。

### 4.2 新增表 2：`trade_calendar`（交易日历）

```sql
CREATE TABLE trade_calendar (
    seq         BIGINT AUTO_INCREMENT PRIMARY KEY,
    trade_date  DATE NOT NULL COMMENT '交易日',
    is_open     TINYINT DEFAULT 1 COMMENT '是否交易日(1是/0否)',
    UNIQUE KEY uniq_date (trade_date)
) COMMENT '交易日历（算调仓日）';
```

**用途**：01e 调仓日是"每季度结束后第 5 个交易日"，必须有交易日历来推算。

### 4.3 复用已有表（不改动）

| 表 | 01e 用法 | 字段 |
|---|---|---|
| `sec_basic_info` | 股票池 + 上市天数过滤 | `sec_type='A股'` / `listed_date` |
| `stock_core_indicator` | 大中小盘划分 | `floating_market_cap` |

### 4.4 数据现状与处理

经实测（2026-07-07）：
- `sec_basic_info`：✅ A 股 5522 只，完整可用
- `stock_core_indicator`：⚠️ 当前快照仅 342 只（项目近期未全量跑）。**本次需补抓全量 A 股**（约 5500 只），复用 QuantVoyager 已有的采集函数模式。01e 的中小盘划分依赖此表的 `floating_market_cap`
- `sec_daily_kline`：❌ 仅近期 20 天 659 只，**回测不用它**——行情走 QMT 自带
- `special_treatment_stock`：❌ 空表（0 条），ST 序列需另行处理（见 §5.3③）

---

## 五、QMT 策略实现

### 5.1 文件位置

```
QuantVoyager/strategy/qmt/pead_01e_disclosure.py
```

放在 QuantVoyager 仓库内统一管理，但与可转债逻辑隔离（`strategy/qmt/` 子目录）。QMT 加载策略时指向此路径。

### 5.2 执行流程（handlebar 驱动）

```
init(C)：初始化（仅启动时一次）
  ├─ 连 MySQL（pymysql，localhost，root/123456）
  ├─ 读全部 disclosure_yysj 到内存 DataFrame（数据量小，几千行）
  ├─ 读交易日历 → 预计算所有"季度末后第5交易日"作为调仓日集合
  └─ 读股票池（sec_basic_info A股 + stock_core_indicator 市值）

handlebar(C)：每根 K 线触发一次
  │
  ├─ ① 当前日期是否调仓日？否 → return
  │     （调仓日 = 季度末后第 5 交易日，init 里预计算）
  │
  ├─ ② 计算 dReport 因子（as_of = 当前调仓日）
  │     对每只股票：
  │     ├─ 今年披露日：actual_report_date 若 <= as_of 则用之，否则用 latest_book_date
  │     ├─ 去年同期披露日：去年的 actual_report_date（去年此时已披露，可见）
  │     └─ dReport = 今年披露日 − 去年同期披露日（天数差，负值=提前=好）
  │     ⚠️ 防前视：SQL 查询加 WHERE actual_report_date <= as_of OR actual_report_date IS NULL
  │
  ├─ ③ 过滤
  │     ├─ 只保留 A 股（sec_basic_info.sec_type）
  │     ├─ 上市 >250 天（listed_date 计算）
  │     ├─ 剔除 ST（stock_zh_a_st_em 或当日名称含 ST/PT）
  │     ├─ 剔除当日停牌/一字涨跌停（get_market_data_ex 当日数据）
  │     └─ 可选：中小盘（floating_market_cap 过滤，01e 主战场）
  │
  ├─ ④ 选股
  │     按 dReport 升序排（越提前越靠前）→ 取前 50-80 只 → 等权
  │
  ├─ ⑤ 回测 vs 实盘分支
  │     ├─ 回测（C.is_last_bar()==False）：
  │     │   记录目标持仓，用 QMT 撮合规则算收益，累积净值
  │     └─ 实盘（C.is_last_bar()==True 且在交易时段）：
  │       passorder 批量下单（先卖不在新持仓的、再买新进的）
  │
  └─ ⑥ 记录净值（回测用）
       等权组合收益 → 输出净值曲线，供与原文绩效对比
```

### 5.3 关键设计点

#### ① 防前视偏差（最重要）

前视偏差是 PEAD 策略最容易翻车的地方（开源 2021 专文强调）。本策略的防护在 SQL 层：

```sql
-- 算 dReport 时，今年披露日只能用 <= 调仓日 as_of 的
SELECT symbol, report_date, actual_report_date, latest_book_date
FROM disclosure_yysj
WHERE report_date IN ('今年报告期', '去年报告期')
  AND (actual_report_date <= :as_of OR actual_report_date IS NULL)
```

- 去年同期披露日：去年的事，调仓日一定可见 ✅
- 今年披露日：若 actual > as_of 视为"未披露"，改用预约日 `latest_book_date`（重合度≥98%）

#### ② 调仓日的确定

01e 是季度调仓，"每季度结束后第 5 个交易日"：
- Q1（3/31）结束 → 约 4 月初第 5 个交易日
- Q2（6/30）结束 → 约 7 月第 5 个交易日
- Q3（9/30）结束 → 约 10 月第 5 个交易日
- Q4（12/31）结束 → 次年 1 月第 5 个交易日

`init` 里根据 `trade_calendar` 预计算所有调仓日，`handlebar` 里判断当前 K 线日期是否命中。

#### ③ ST 序列问题

现有 `special_treatment_stock` 表是空的。ST 状态是历史时变的（某股 2021 年是 ST、2023 年摘帽），回测需要历史 ST 序列。两个方案（实现时择一）：
- **方案 A**：回测时用"股票名称是否含 ST/PT/*ST"近似判断（从历史日线名称拿）
- **方案 B**：补抓历史 ST 序列进 MySQL（更准但工作量大）

起步建议方案 A（近似），因为 01e 的 ST 过滤不是核心，且原文 ST 剔除对绩效影响有限。

#### ④ 回测撮合与费用

- **撮合**：QMT 自带规则（指定价在当根 K 线高低点间按指定价，否则按收盘价）
- **成交价**：次日收盘价（招商原文口径：复权收盘价）
- **费用**：单边 0.3%（双边千六，原文 §四.1 口径）

#### ⑤ 回测 vs 实盘的切换

同一份代码，靠 `C.is_last_bar()` 区分：
- 回测：遍历历史 K 线，`is_last_bar()` 为 False，记录持仓与净值
- 实盘：运行到最新 K 线，`is_last_bar()` 为 True，在交易时段调用 `passorder`

### 5.4 参数表（与原文对齐）

| 参数 | 值 | 出处 |
|---|---|---|
| 主因子 | dReport（今年披露日 − 去年同期，天数）| 招商 2021 §三.2 |
| 因子方向 | 升序（dReport 越小=越提前=越好）| 负值=提前 |
| 披露日取值 | 实际披露日优先；未披露用最新预约日 | 招商 2021 §一.2（重合度≥98%）|
| 选股域 | 全 A 或中小盘 | 沪深300 无效（原文验证）|
| 持仓数 | 50-80 只（等权）| 招商 2021 §四.2 |
| 调仓频率 | 季度（每季度末后第 5 交易日）| 招商 2021 §四.1 |
| 持仓周期 | 1 季度 | 招商 2021 §四.1 |
| 费用 | 单边 0.3%（双边千六）| 招商 2021 §四.1 |
| 池内过滤 | 剔除停牌 / ST / 涨跌停 | 招商 2021 §四.1 |
| 上市天数 | >250 天 | 通用过滤 |

### 5.5 验证标准

回测跑通后，与招商原文绩效对比：

| 指标 | 原文 | 预期实战（8-9 折）|
|---|---|---|
| 全 A 多头年化 | 15.51% | 12-14% |
| 全 A 对冲年化 | 8.49% | 6.8-7.6% |
| 小盘多头年化 | 19.29% | 15-17% |

**若跑出明显低于此**：优先检查数据链路（披露日是否完整、前视偏差防护、调仓日计算）。

---

## 六、实施范围（本次）

### 6.1 QuantVoyager 侧（数据采集）

| 工作项 | 说明 |
|---|---|
| `DisclosureYysj` ORM 模型 | `data/data_models.py` 新增 |
| `TradeCalendar` ORM 模型 | `data/data_models.py` 新增 |
| `scrape_disclosure_yysj()` | `data/data_collector.py` 新增，调东财预约披露接口 |
| `scrape_trade_calendar()` | `data/data_collector.py` 新增，拉交易日历 |
| Alembic 迁移 | 生成两张新表的建表脚本 |
| `scheduler.yaml` 任务 | 披露日季度抓取 + 交易日历年度更新 |
| 历史数据补抓 | 抓 2019-2024 共 6 年披露日（用于回测+同比）|
| `stock_core_indicator` 全量补抓 | 当前仅 342 只快照，补抓全量 A 股（约 5500 只）供中小盘划分 |

### 6.2 QMT 策略侧

| 工作项 | 说明 |
|---|---|
| `strategy/qmt/pead_01e_disclosure.py` | 主策略文件（init + handlebar）|
| MySQL 连接封装 | pymysql 连 localhost |
| dReport 因子计算 | 含防前视偏差的 as_of 切片 |
| 过滤逻辑 | ST / 上市天数 / 停牌 / 涨跌停 |
| 选股与等权 | dReport 升序取前 N |
| 回测净值记录 | 输出净值曲线 |
| 实盘下单分支 | passorder 批量下单 |

---

## 七、后续扩展（不在本次范围）

- **01d AOG 量价**：同样数据需求小，可作为第二个落地策略，复用本套数据层
- **01a/b/c SUE 路线**：需新增财务/分析师数据表，复用本套采集框架模式
- **多策略组合**：01e 与 01d 正交叠加（时机 + 量价），框架已支持
- **数据源升级**：东财 requests → Wind/Choice，只改采集层

---

## 附录：原文核实结论

本次设计前已核实：
1. **5 份策略设计文档引用的 8 篇原始研报全部存在**（`raw/articles/` 逐篇核对）
2. **关键结论可溯源**：dReport IC 0.027/IR 1.09、与大类因子相关性<3%、小盘多头 19.29% 等均能在原文找到
3. **akshare 接口实测**：`stock_yysj_em` 字段齐全（首次预约/变更/实际披露）；`stock_a_lg_indicator` 不存在（设计文档笔误，改用 `stock_value_em`）
4. **本项目改用 requests 直连东财**（复用 QuantVoyager 的 safe_request），绕开 akshare，更可控且能拿到完整字段
