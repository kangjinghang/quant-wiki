# PEAD 01a SUE 数据采集层 · 实现讲解

> **本文定位**：这是一份**面向学习者的实现讲解**，聚焦"代码为什么这么写、每个函数在抓什么数据、为什么这么映射"。
>
> | 文档 | 回答什么问题 | 你什么时候看 |
> |---|---|---|
> | [01a 策略设计](../../strategy-directions/strategy-designs/01-pead/01a-pead-sue-single-factor.md) | SUE 怎么算？赚什么钱？绩效预期？ | 想理解策略原理时 |
> | **本文（实现讲解）** | **采集代码怎么抓数据？三张表怎么对应 SUE 公式？为什么这么映射？** | **想读懂采集层代码时** |
>
> ⚠️ **本文范围**：01a 目前只实现了**数据采集层**（3 张表 + 采集函数 + 映射 + 调度 + 补历史脚本）。SUE 因子计算、选股、调仓等策略逻辑尚未实现——那是下一步的事。本文讲的是"把数据准备好"这一层。
>
> **配套**：[QMT 策略开发指南](./QMT策略开发指南.md)（三工作区环境、东财接口实测笔记、避坑清单）。

---

## 一、SUE 公式与三张表的对应关系

### 1.1 SUE 公式三要素

SUE（标准化超预期）的核心公式：

$$SUE = \frac{E_{actual} - E_{expected}}{\sigma}$$

三个要素：
- **$E_{actual}$（实际盈利）**：公司财报公布的单季利润
- **$E_{expected}$（预期盈利）**：分析师预测的利润
- **$\sigma$（标准化常数）**：让大公司和小公司可比的分母

### 1.2 三张表怎么对应

采集层的工作，就是把这三个要素所需的数据抓全、存好：

| SUE 要素 | 数据来源 | 存到哪张表 | 采集函数 |
|---|---|---|---|
| $E_{actual}$（实际盈利）| 东财 F10 单季利润表 | `financial_quarterly` | `stock_profit_quarterly_em` |
| $E_{expected}$（预期盈利）| 同花顺分析师预测 | `analyst_forecast` | `stock_analyst_forecast_ths` |
| $\sigma$（分母·补覆盖）| 东财业绩预告 | `performance_forecast` | `stock_performance_forecast_em` |

**为什么业绩预告对应的是 $\sigma$**：这里有个设计决策——01a 的 SUE 分母选了**口径 B（国君建模法）**，不依赖历史分析师预测（同花顺拿不到历史预测，只有近期快照）。业绩预告的作用是**补充分析师覆盖不足的股票**——这些股票没有分析师预测，但有业绩预告的上下限可以近似实际盈利，让建模法能算出来。

```
SUE 计算时（策略层，尚未实现）：
  E_actual  ← financial_quarterly.net_profit（单季归母净利）
  E_expected ← analyst_forecast.forecast_net_profit（分析师预测中位数）
                 或 口径B 降级：用 financial_quarterly 历史 8 季建模
  σ         ← 口径A：analyst_forecast 各机构预测标准差
              口径B：历史预测误差标准差
  覆盖不足  ← performance_forecast 补上下限均值近似 E_actual
```

### 1.3 为什么选口径 B

[策略设计 §2.4](../../strategy-directions/strategy-designs/01-pead/01a-pead-sue-single-factor.md) 里推荐口径 A（华创法，当期分析师分歧度），但采集层实现时选了口径 B。原因很实际：

> **同花顺只返回近期预测，历史预测拿不到。**

口径 A 的分母需要"当期各机构预测的标准差"，这用近期快照就能算。但口径 A 的分子（季报场景）需要"季报发布前后，分析师预测的变化"——这必须拿到**历史时间点的分析师预测**。同花顺 `worth.html` 只返回当前最新的预测，一年前的预测早就被覆盖了。

口径 B 的分母是"历史 8 季预测误差的标准差"，**只需要历史净利数据建模**，不依赖历史分析师预测。所以口径 B 能纯靠 `financial_quarterly` 一张表降级运行，应对同花顺拿不到历史的局限。

---

## 二、代码地图

采集层代码在 QuantVoyager 项目里，分工如下：

```
QuantVoyager/
├── data/
│   ├── data_models.py        # 3 个 ORM 类（表结构定义）
│   ├── data_collector.py     # ★ 4 个采集函数（抓数据）
│   ├── data_mapper.py        # ★ 4 个映射函数（转格式）
│   └── data_storage.py       # bulk_upsert（批量入库）
├── tasks/
│   └── static_data_scheduled_tasks.py  # 3 个定时任务
├── scripts/
│   ├── backfill_analyst_forecast.py    # 补历史脚本×3
│   ├── backfill_financial_quarterly.py
│   └── backfill_performance_forecast.py
├── migrations/versions/
│   └── b1c2d3e4f5g6_*.py     # Alembic 建表迁移
└── config/
    └── scheduler.yaml        # 3 条调度配置
```

**分层逻辑**（和 01e 一脉相承）：
- `collector` 只管**抓原始数据**（返回 DataFrame）
- `mapper` 只管**转格式**（DataFrame → dict 列表）
- `task` 只管**调度 + 补字段 + 入库**（调 collector → 调 mapper → 调 bulk_upsert）

这样分层的好处：collector 和 mapper 都是**纯函数**，能脱离数据库单独测试；task 是粘合层，逻辑薄。

---

## 三、数据怎么流动（先看全局再看细节）

一次完整采集的数据流，从网页到数据库：

```
    定时任务触发（或手动跑 backfill 脚本）
              │
              ▼
  ┌────────────────────────────┐
  │ ① 查 sec_basic_info 拿股票代码 │  filter_by(sec_type_code='001001')
  │    只取 A 股（排除可转债/B 股）│  5519 只，不抓 426 只非股票
  └────────────────────────────┘
              │
              ▼
  ┌────────────────────────────┐
  │ ② 逐只调采集函数              │  collector 返回原始 DataFrame
  │    → safe_request 抓网页/API  │  失败返回空 DataFrame，不中断
  └────────────────────────────┘
              │
              ▼
  ┌────────────────────────────┐
  │ ③ 调映射函数转格式            │  mapper：DataFrame → dict 列表
  │    解析中文金额/日期/字段名    │  ★ 本文重点
  └────────────────────────────┘
              │
              ▼
  ┌────────────────────────────┐
  │ ④ 补 task 层字段             │  同花顺页面不含股票代码
  │    symbol / stock_code       │  由 task 补上
  └────────────────────────────┘
              │
              ▼
  ┌────────────────────────────┐
  │ ⑤ bulk_upsert 批量入库       │  ON DUPLICATE KEY UPDATE
  │    幂等，断点续跑安全         │  重复抓不出错
  └────────────────────────────┘
```

记住这个 5 步流水线，下面三节就是在拆解其中的 ②③。

---

## 四、采集函数逐个讲

> 文件：`data/data_collector.py` 末尾 `# PEAD 01a SUE 数据采集` 段

### 4.1 `_get_company_type_em`：动态判断公司类型

东财 F10 的利润表接口需要传 `companyType` 参数，不同类型的公司（普通股/银行/保险/券商）报表结构不同。这个函数就是去 F10 页面抓一个隐藏字段。

```python
def _get_company_type_em(symbol: str) -> str:
    """
    解析东财F10页面 hidctype 隐藏字段，返回公司类型编码。
    普通股='4', 保险='2', 银行/券商='3'（实测 2026-07-08）。
    解析失败兜底返回 '4'（普通股），保证不崩。
    """
    url = "https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/Index"
    params = {"type": "web", "code": symbol.lower()}
    r = safe_request(url, params=params)
    if r is None:
        return "4"
    # 真实 HTML: hidctype" type="hidden" value="3"（属性顺序不固定，用宽松匹配）
    m = re.search(r'hidctype[^>]*value="(\d+)"', r.text)
    return m.group(1) if m else "4"
```

**为什么不能写死 `companyType=4`**：银行（如招商银行 600036）、保险（如平安 601318）、券商的报表结构和普通股不一样，传错 `companyType` 会拿不到数据或字段错位。实测茅台=4、招行=3、平安=2。

**坑：HTML 属性顺序不固定**。一开始用 `hidctype type="hidden" value="3"` 精确匹配，但东财的 HTML 里 `type` 和 `value` 的顺序不固定（有时 `value` 在前），所以改用 `hidctype[^>]*value="(\d+)"`——`[^>]*` 匹配到标签结束前的任意字符，不管属性怎么排列都能抓到 `value`。

**兜底返回 '4'**：解析失败也不崩，按普通股处理。宁可少拿几家银行的数据，也不能让全市场遍历中断。

### 4.2 `stock_profit_quarterly_em`：东财 F10 单季利润表

这是 SUE 实际盈利 $E_{actual}$ 的数据源。分三步：判断类型 → 拿报告期列表 → 分批取数据。

```python
def stock_profit_quarterly_em(symbol: str = "SH600519") -> pd.DataFrame:
    # ① 动态判断公司类型（银行/保险/券商/普通）
    company_type = _get_company_type_em(symbol)

    # ② 拿该股所有单季报告期列表
    date_url = ".../lrbDateAjaxNew"
    params = {"companyType": company_type, "reportDateType": "2", "code": symbol}
    r = safe_request(date_url, params=params)
    if r is None:
        return pd.DataFrame()
    dates = [d["REPORT_DATE"][:10] for d in r.json().get("data", [])]
    if not dates:
        return pd.DataFrame()

    # ③ 按 5 个一批取单季利润表（接口 dates 参数支持逗号分隔）
    big_df = pd.DataFrame()
    for i in range(0, len(dates), 5):
        batch = ",".join(dates[i:i + 5])
        url = ".../lrbAjaxNew"
        params = {"companyType": company_type, "reportDateType": "0",
                  "reportType": "2", "dates": batch, "code": symbol}
        r = safe_request(url, params=params)
        if r is None:
            continue
        data = r.json().get("data")
        if not data:
            break
        temp = pd.DataFrame(data)
        big_df = pd.concat([big_df, temp], ignore_index=True)
        time.sleep(0.5)
    return big_df
```

**为什么 `reportDateType="2"`**：东财 F10 利润表有两种视图——`reportDateType="2"` 是**单季度**视图（直接出单季值），`"0"` 是累计视图。01a 需要单季值（SUE 公式要求单季净利），所以用 `"2"` 拿报告期列表。但取数据时 `reportType="2"` 才是单季——两个参数含义不同，别搞混。

**为什么分 5 个一批**：东财 `lrbAjaxNew` 接口的 `dates` 参数支持逗号分隔多个报告期，但一次传太多会超时或被拒。实测 5 个一批稳定，茅台有 97 个报告期，分 20 批取完约 10 秒。

**关键字段**（实测茅台 97 报告期，204 列）：

| 东财字段 | 含义 | 映射到 |
|---|---|---|
| `REPORT_DATE` | 报告期（季度末） | `financial_quarterly.report_date` |
| `NOTICE_DATE` | **首次披露日**（见 §6.1 调查结论）| `financial_quarterly.announce_date` |
| `UPDATE_DATE` | 数据更新日（修正时刷新）| 不入库 |
| `PARENT_NETPROFIT` | 单季归母净利 | `financial_quarterly.net_profit` |
| `OPERATE_PROFIT` | 单季营业利润 | `financial_quarterly.operate_profit` |
| `DEDUCT_PARENT_NETPROFIT` | 单季扣非净利 | `financial_quarterly.deduct_profit` |
| `TOTAL_OPERATE_INCOME` | 单季营业总收入 | `financial_quarterly.total_revenue` |

**为什么只存这 4 个利润指标**：[策略设计 §2.2](../../strategy-directions/strategy-designs/01-pead/01a-pead-sue-single-factor.md) 指出不同股票池最优利润指标不同——全市场用归母净利，沪深300用营业利润/扣非净利。4 个都存下来，策略层按需取用，不用重新抓。

### 4.3 `stock_analyst_forecast_ths`：同花顺分析师预测

这是 SUE 预期盈利 $E_{expected}$ 的数据源。抓同花顺的 `worth.html` 页面。

```python
def stock_analyst_forecast_ths(stock_code: str) -> pd.DataFrame:
    url = "https://basic.10jqka.com.cn/new/%s/worth.html" % stock_code
    # ⚠️ 同花顺需要浏览器 User-Agent，否则返回 403 Forbidden
    r = safe_request(url, timeout=15,
                     headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
    if r is None:
        return pd.DataFrame()
    r.encoding = "gbk"  # ⚠️ 同花顺返回 GBK
    if "本年度暂无机构做出业绩预测" in r.text:
        return pd.DataFrame()
    try:
        tables = pd.read_html(StringIO(r.text))
    except Exception:
        return pd.DataFrame()
    if len(tables) <= 2:
        return pd.DataFrame()
    return tables[2]
```

**三个坑**：

1. **403 需要加 UA**：同花顺会检查 `User-Agent`，不传或传 Python 默认的 `python-requests/x.x` 会返回 403。必须传一个浏览器 UA。
2. **GBK 编码**：同花顺页面是 GBK 编码，`requests` 默认会猜成 UTF-8 导致乱码。必须手动 `r.encoding = "gbk"`。
3. **取第 [2] 个表**：`pd.read_html` 会把页面所有 `<table>` 都解析出来。`worth.html` 有多个表，第 0 个是页面头部信息、第 1 个是 EPS 预测、**第 2 个才是净利润预测详表**（机构明细）。

**返回的 DataFrame 是 MultiIndex 列**（实测茅台 10 机构 × 3 年）：

```
columns (MultiIndex):
  ('机构名称', '机构名称')
  ('研究员', '研究员')
  ('预测年报每股收益（元）', '2026预测')
  ('预测年报每股收益（元）', '2027预测')
  ('预测年报每股收益（元）', '2028预测')
  ('预测年报净利润（元）', '2026预测')     ← 01a 要的
  ('预测年报净利润（元）', '2027预测')     ← 01a 要的
  ('预测年报净利润（元）', '2028预测')     ← 01a 要的
  ('报告日期', '报告日期')
```

**一个表行 = 一家机构的多年预测**。第 4.2 节会讲怎么把它拆成"一行机构 → 多条记录（每年一条）"。

**同花顺页面不含股票代码**：`worth.html` 只返回机构名/研究员/预测值，不含这只股票的代码。所以采集函数无法补 `symbol`，留给 task 层补（见 §五）。

### 4.4 `stock_performance_forecast_em`：东财业绩预告

这是 SUE 补覆盖用的数据源。直连东财 datacenter API，按报告期批量抓。

```python
def stock_performance_forecast_em(date: str = "20251231") -> pd.DataFrame:
    report_date_fmt = "%s-%s-%s" % (date[:4], date[4:6], date[6:8])

    url = "https://datacenter.eastmoney.com/securities/api/data/v1/get"
    all_data = []
    page = 1
    while True:
        params = {
            "sortColumns": "NOTICE_DATE,SECURITY_CODE",
            "sortTypes": "-1,-1",
            "pageSize": "500",
            "pageNumber": str(page),
            "reportName": "RPT_PUBLIC_OP_NEWPREDICT",
            "columns": "ALL",
            "filter": '(SECURITY_TYPE_CODE in ("058001001","058001008"))'
                      '(TRADE_MARKET_CODE!="069001017")'
                      "(REPORT_DATE='%s')" % report_date_fmt,
        }
        r = safe_request(url, params=params)
        if r is None:
            return pd.DataFrame()
        data_json = r.json()
        if not data_json.get("result") or not data_json["result"].get("data"):
            break
        all_data.extend(data_json["result"]["data"])
        if page >= data_json["result"].get("pages", 1):
            break
        page += 1
        time.sleep(random.uniform(0.5, 1.0))

    if not all_data:
        return pd.DataFrame()
    return pd.DataFrame.from_dict(all_data)
```

**为什么不用 akshare**：[策略设计附录 B](../../strategy-directions/strategy-designs/01-pead/01a-pead-sue-single-factor.md) 指出 akshare 的 `stock_yjyg_em` **丢了上下限字段**——只暴露单一"预测数值"，但东财原始 API 有 `PREDICT_AMT_LOWER`/`PREDICT_AMT_UPPER`。01a 需要上下限（取均值作为近似净利润），所以直连东财 `columns=ALL` 拿全部 27 个字段。

**filter 的三个条件**：
- `SECURITY_TYPE_CODE in ("058001001","058001008")`：只要股票的业绩预告，不要债券/基金的
- `TRADE_MARKET_CODE!="069001017"`：排除某个特定市场（北交所相关，实测发现该市场数据不全）
- `REPORT_DATE='2024-12-31'`：按报告期过滤

**分页 + 限速**：每页 500 条，`while True` 翻页直到取完。每页之间 `sleep(random.uniform(0.5, 1.0))`——随机间隔避免被东财风控识别为爬虫。

**实测数据**（2024 年报，7186 条）：每条含 `PREDICT_AMT_LOWER`/`UPPER`（净利润上下限）、`ADD_AMP_LOWER`/`UPPER`（变动幅度上下限）、`PREDICT_TYPE`（预增/预减/首亏/扭亏等）。

---

## 五、映射函数逐个讲

> 文件：`data/data_mapper.py` 末尾 `# PEAD 01a SUE 数据映射` 段

映射函数的职责：把采集函数返回的原始 DataFrame，转成能直接入库的 dict 列表。这一层的核心是**字段名翻译 + 数据清洗**。

### 5.1 `_parse_chinese_amount`：中文金额解析

同花顺返回的净利润是带中文单位的字符串：`"846.86亿"`、`"1234万"`、`"5678"`。入库前要转成数字。

```python
def _parse_chinese_amount(text):
    if text is None or text == "" or (isinstance(text, float) and pd.isna(text)):
        return None
    text = str(text).strip()
    try:
        if text.endswith("亿"):
            return float(text[:-1]) * 1e8
        elif text.endswith("万"):
            return float(text[:-1]) * 1e4
        else:
            return float(text)
    except (ValueError, IndexError):
        return None
```

**逻辑很简单**：看最后一个字是"亿"还是"万"，去掉单位乘以对应倍率。但边界要处理好：

| 输入 | 输出 | 说明 |
|---|---|---|
| `"846.86亿"` | `84686000000.0` | 亿 → ×1e8 |
| `"1234万"` | `12340000.0` | 万 → ×1e4 |
| `"5678"` | `5678.0` | 无单位直接转 |
| `"-5.2亿"` | `-520000000.0` | 负数也支持（亏损）|
| `""` / `None` / `NaN` | `None` | 空值返回 None |
| `"亏损"` / `"--"` | `None` | 非数字返回 None |

> 这个函数有 9 个单测覆盖（`tests/test_unit.py::TestParseChineseAmount`），包括负数、空值、NaN、非数字文本等边界。

### 5.2 `mapping_to_analyst_forecast_list`：拆行 + 解析中文金额

同花顺返回的表是"一行机构 × 多年预测"，入库要拆成"一行 = 一机构一年"。这是映射层最复杂的一个。

```python
def mapping_to_analyst_forecast_list(df: pd.DataFrame) -> list:
    if df is None or df.empty:
        return []

    # 找出"预测年报净利润"的列（按年份展开）
    net_profit_cols = {}  # {年份字符串: 列名(tuple)}
    for col in df.columns:
        if "预测年报净利润" in col[0]:
            year_str = col[1].replace("预测", "")
            net_profit_cols[year_str] = col

    result = []
    for _, row in df.iterrows():
        org_name = row.get(("机构名称", "机构名称"))
        researcher = row.get(("研究员", "研究员"))
        announce_date = _parse_date(row.get(("报告日期", "报告日期")))
        if not org_name or not announce_date:
            continue

        for year_str, col in net_profit_cols.items():
            raw = row.get(col)
            net_profit = _parse_chinese_amount(raw)
            if net_profit is None:
                continue
            try:
                year_int = int(year_str)
            except ValueError:
                continue
            result.append({
                "org_name": org_name,
                "researcher": researcher,
                "forecast_year": year_int,
                "forecast_net_profit": net_profit,
                "announce_date": announce_date,
                "raw_text": str(raw) if raw is not None else None,
            })
    return result
```

**用茅台的例子走一遍**。输入 DataFrame：

```
     机构名称  研究员    预测年报净利润（元）
                       2026预测     2027预测    2028预测    报告日期
0   华创证券  欧阳予   846.86亿    884.71亿   923.01亿   2026-06-14
1   招商证券  陈书慧   850.42亿    901.78亿   948.69亿   2026-06-14
```

**Step 1：找"预测年报净利润"列**

遍历 MultiIndex 列，`col[0]` 是第一层（"预测年报净利润（元）"），`col[1]` 是第二层（"2026预测"）。匹配到 3 列：

```python
net_profit_cols = {
    "2026": ("预测年报净利润（元）", "2026预测"),
    "2027": ("预测年报净利润（元）", "2027预测"),
    "2028": ("预测年报净利润（元）", "2028预测"),
}
```

注意 `year_str = col[1].replace("预测", "")` —— 把 "2026预测" 变成 "2026"。

**Step 2：逐行拆分**

华创证券这一行有 3 年预测，拆成 3 条记录：

```python
# year_str="2026", raw="846.86亿"
{"org_name": "华创证券", "researcher": "欧阳予",
 "forecast_year": 2026, "forecast_net_profit": 84686000000.0,
 "announce_date": date(2026,6,14), "raw_text": "846.86亿"}

# year_str="2027", raw="884.71亿"
{"org_name": "华创证券", "researcher": "欧阳予",
 "forecast_year": 2027, "forecast_net_profit": 88471000000.0, ...}

# year_str="2028", raw="923.01亿"
{"org_name": "华创证券", "researcher": "欧阳予",
 "forecast_year": 2028, "forecast_net_profit": 92301000000.0, ...}
```

10 家机构 × 3 年 = 30 条记录（跳过空值的会更少）。

**为什么跳过 `net_profit is None` 的**：有些机构只预测了 EPS 没预测净利润（`raw` 是 None 或空），`_parse_chinese_amount` 返回 None，直接跳过——没有净利润预测的记录没有意义。

**为什么保留 `raw_text`**：调试用。万一 `_parse_chinese_amount` 解析错了，可以从 `raw_text` 看到原始值。生产环境可以删，但现在留着不影响。

### 5.3 `mapping_to_financial_quarterly_list`：字段名翻译

东财返回的列名是大写英文（`PARENT_NETPROFIT`），入库要转成下划线小写（`net_profit`）。纯翻译，逻辑简单。

```python
def mapping_to_financial_quarterly_list(df: pd.DataFrame, symbol: str) -> list:
    if df is None or df.empty:
        return []
    result = []
    for _, row in df.iterrows():
        report_date = _parse_date(row.get("REPORT_DATE"))
        if not report_date:
            continue
        result.append({
            "symbol": symbol,
            "stock_code": str(row.get("SECURITY_CODE", "")),
            "stock_name": row.get("SECURITY_NAME_ABBR"),
            "report_date": report_date,
            "net_profit": safely_parse_float(row.get("PARENT_NETPROFIT")),
            "operate_profit": safely_parse_float(row.get("OPERATE_PROFIT")),
            "deduct_profit": safely_parse_float(row.get("DEDUCT_PARENT_NETPROFIT")),
            "total_revenue": safely_parse_float(row.get("TOTAL_OPERATE_INCOME")),
            "announce_date": _parse_date(row.get("NOTICE_DATE")),
        })
    return result
```

**字段映射对照**：

| 东财字段 | 入库字段 | 说明 |
|---|---|---|
| `REPORT_DATE` | `report_date` | 报告期（如 2026-03-31）|
| `NOTICE_DATE` | `announce_date` | 首次披露日（防前视锚点）|
| `PARENT_NETPROFIT` | `net_profit` | 单季归母净利 |
| `OPERATE_PROFIT` | `operate_profit` | 单季营业利润 |
| `DEDUCT_PARENT_NETPROFIT` | `deduct_profit` | 单季扣非净利 |
| `TOTAL_OPERATE_INCOME` | `total_revenue` | 单季营业总收入 |
| `SECURITY_CODE` | `stock_code` | 股票代码 |
| `SECURITY_NAME_ABBR` | `stock_name` | 股票简称 |

**`symbol` 由调用方传入**：因为东财返回的 `SECUCODE` 格式是 `600519.SH`，和 `_normalize_symbol` 返回的一致，但 task 层已经算过一次了，传进来复用，避免重复计算。

### 5.4 `mapping_to_performance_forecast_list`：上下限取值

业绩预告返回的是净利润上下限，入库要存原始的两个值（不取均值——取均值的逻辑留给策略层）。

```python
def mapping_to_performance_forecast_list(df: pd.DataFrame, report_date_str: str) -> list:
    if df is None or df.empty:
        return []
    result = []
    for _, row in df.iterrows():
        symbol = row.get("SECUCODE") or _normalize_symbol(row.get("SECURITY_CODE"))
        if not symbol:
            continue
        result.append({
            "symbol": symbol,
            "stock_code": str(row.get("SECURITY_CODE", "")),
            "stock_name": row.get("SECURITY_NAME_ABBR"),
            "report_date": report_date_str,
            "notice_date": _parse_date(row.get("NOTICE_DATE")),
            "forecast_type": row.get("PREDICT_TYPE"),
            "profit_min": safely_parse_float(row.get("PREDICT_AMT_LOWER")),
            "profit_max": safely_parse_float(row.get("PREDICT_AMT_UPPER")),
            "change_pct_min": safely_parse_float(row.get("ADD_AMP_LOWER")),
            "change_pct_max": safely_parse_float(row.get("ADD_AMP_UPPER")),
        })
    return result
```

**`symbol` 的兜底顺序**：优先用 `SECUCODE`（东财已带 `.SH`/`.SZ` 后缀），拿不到才用 `_normalize_symbol(SECURITY_CODE)` 反推。这个降级顺序合理——能用原始的就用原始的，反推是兜底。

**为什么 `report_date` 由参数传入而不是从数据里取**：因为 `stock_performance_forecast_em` 是按报告期抓的（`date="20241231"`），调用方已经知道报告期。传入参数保证一致性，避免数据里的 `REPORT_DATE` 格式不统一。

---

## 六、关键调查结论

### 6.1 `NOTICE_DATE` 是首次披露日（不是最近更新日）

这是一个审核时专门调查过的问题，结论值得记录。

**原来的担忧**：东财 F10 单季接口返回的 `NOTICE_DATE`，可能是"最近一次财报更新日"而非"首次披露日"。如果是这样，用它做防前视锚点会出问题——回测时会以为数据比实际更早可见。

**调查方法**：用茅台（财报修正极少）、ST明诚（财报修正频繁）、航锦科技三只票实际调接口，对比 `NOTICE_DATE` 和 `UPDATE_DATE` 两个字段。

**结论**：`NOTICE_DATE` 是**首次披露日**，财报修正不会刷新它；`UPDATE_DATE` 才是数据更新日。两者不同恰恰证明了这一点：

```
茅台 2024Q1（报告期 2024-03-31）:
  NOTICE_DATE = 2024-04-27   ← 首次披露日（2024 年 4 月 27 日发的一季报）
  UPDATE_DATE = 2025-04-30   ← 一年后更新（可能有修正）

ST明诚 2024年报（报告期 2024-12-31）:
  NOTICE_DATE = 2025-03-29   ← 首次披露日
  UPDATE_DATE = 2026-04-23   ← 修正日（ST 股经常修正）

最新报告期（刚披露还没到修正周期）:
  NOTICE_DATE = UPDATE_DATE  ← 两者相同
```

茅台 97 个报告期里，72 个 `NOTICE_DATE ≠ UPDATE_DATE`——说明 `NOTICE_DATE` 确实没被刷新，稳定保持首次披露时间。

**所以**：`financial_quarterly.announce_date` 用 `NOTICE_DATE` 是正确的，没有前视风险。

**但有一个提醒**：`net_profit` 是接口返回的**最新值**（可能含修正后数据）。如果策略需要严格还原"首次披露时的数值"，需要另行处理。不过用 `announce_date` 判断"何时能看到这季利润"是准确的——这是防前视的核心。

### 6.2 全市场遍历必须过滤非股票

采集层的三个 task 启动时都查 `sec_basic_info` 拿股票代码。最初版本没有过滤，把可转债（347 只）和 B 股（79 只）也当股票抓——每只白跑 1.5 秒（同花顺返回空 + 东财 F10 返回空），合计浪费约 11 分钟。

修复后加 `.filter_by(sec_type_code='001001')`，只抓 5519 只 A 股。`sec_type_code` 的值：

| sec_type_code | sec_type | 数量 |
|---|---|---|
| 001001 | A股 | 5519 |
| 002006 | 可转债 | 347 |
| 001002 | B股 | 79 |

---

## 七、表结构设计

> 文件：`data/data_models.py` + `migrations/versions/b1c2d3e4f5g6_*.py`

三张表都继承 `BaseModel`（自带 `seq`/`ctime`/`utime`），核心字段如下：

### 7.1 `analyst_forecast`（分析师预测）

```
symbol          600519.SH          唯一代码
stock_code      600519             股票代码
org_name        华创证券            机构名称
researcher      欧阳予             研究员
forecast_year   2026              预测年份
forecast_net_profit  84686000000  预测净利润(元)
announce_date   2026-06-14        报告日期
raw_text        846.86亿          原始文本(调试用)

唯一索引: (symbol, org_name, announce_date, forecast_year)
```

**唯一索引的含义**：同一只股票、同一家机构、同一天发布的、对同一年的预测，只存一条。如果同花顺返回了重复数据，`bulk_upsert` 的 `ON DUPLICATE KEY UPDATE` 会覆盖而非报错。

**为什么不含 `stock_name`**：同花顺页面不含股票名称，只有机构名和预测值。`stock_name` 可以从 `sec_basic_info` join，没必要冗余存储。

### 7.2 `financial_quarterly`（单季利润表）

```
symbol          600519.SH          唯一代码
stock_code      600519             股票代码
stock_name      贵州茅台           股票简称
report_date     2026-03-31        报告期(季度末)
net_profit      27242512886       单季归母净利(元)
operate_profit  35000000000       单季营业利润(元)
deduct_profit   27000000000       单季扣非净利(元)
total_revenue   54702912385       单季营业总收入(元)
announce_date   2026-04-25        首次披露日(防前视用)

唯一索引: (symbol, report_date)
```

**唯一索引**：一只股票一个报告期只存一行。东财 F10 返回的同一报告期可能有多个版本（修正），以最后抓到的为准（覆盖）。

### 7.3 `performance_forecast`（业绩预告）

```
symbol          603488.SH          唯一代码
stock_code      603488             股票代码
stock_name      展鹏科技           股票简称
report_date     2024-12-31        报告期
notice_date     2025-04-30        预告公告日
forecast_type   首亏               预告类型
profit_min      -16428200         净利润下限(元)
profit_max      -16428200         净利润上限(元)
change_pct_min  -129.33           变动幅度下限(%)
change_pct_max  -129.33           变动幅度上限(%)

唯一索引: (symbol, report_date)
```

**为什么唯一索引不含 `notice_date`**：同一只股票同一报告期可能发多次预告（首次预告 + 修正预告），以最后一次为准。`notice_date` 字段记录的是这条预告的公告日，但不作为唯一性约束的一部分。

---

## 八、调度与补历史

### 8.1 定时调度（`scheduler.yaml`）

三条调度，工作日盘后执行：

| 任务 | 时间 | 说明 |
|---|---|---|
| `scrape_analyst_forecast` | 18:00 | 逐只抓同花顺，约 40 分钟 |
| `scrape_financial_quarterly` | 18:30 | 逐只抓东财 F10，约 40 分钟 |
| `scrape_performance_forecast` | 18:45 | 按报告期批量抓东财，约 10 分钟 |

**为什么时间错开**：三个任务都是全市场遍历，串行执行。18:00 开始分析师预测（~40min），18:30 开始单季利润表（~40min），18:45 开始业绩预告（~10min）。实际运行时前一个可能还没跑完，但它们操作不同的表，互不干扰。

### 8.2 补历史脚本（`scripts/backfill_*.py`）

三个一次性脚本，用于回测前补历史数据：

| 脚本 | 补什么 | 覆盖范围 |
|---|---|---|
| `backfill_financial_quarterly.py` | 全市场单季利润表 | 东财 F10 返回全部历史（2015-至今），逐只抓一次 |
| `backfill_performance_forecast.py` | 2018-2024 业绩预告 | 7 年 × 4 报告期 = 28 个报告期，按报告期批量抓 |
| `backfill_analyst_forecast.py` | 分析师预测当前快照 | ⚠️ 只能抓当前快照（同花顺拿不到历史）|

**为什么分析师预测只抓快照**：同花顺 `worth.html` 只返回当前最新的机构预测，一年前的预测已被覆盖。回测早期的分析师预期靠口径 B 降级方案（纯历史净利建模）应对。

**断点续跑安全**：三个脚本都用 `bulk_upsert`（`ON DUPLICATE KEY UPDATE`），跑到一半中断了，重跑不会出错、不会重复。已入库的会被覆盖，未入库的会新增。

### 8.3 迁移链

```
7f4260467b90 (init)
  → a1b2c3d4e5f6 (disclosure_yysj + trade_calendar，01e 用)
    → b2c3d4e5f6a7 (backtest_nav，01e 用)
      → b1c2d3e4f5g6 (01a 三张表)   ← 本文
```

⚠️ **审核时发现过迁移链分叉的 bug**：最初 `b1c2d3e4f5g6` 的 `down_revision` 指向 `a1b2c3d4e5f6`，和 `b2c3d4e5f6a7`（backtest_nav）成了兄弟节点，Alembic 会报 `Multiple head revisions`。已修正为指向 `b2c3d4e5f6a7`，变单一线性链。

---

## 九、关键设计决策回顾

| 决策 | 选了什么 | 为什么 |
|---|---|---|
| SUE 分母口径 | 口径 B（国君建模法）| 同花顺拿不到历史分析师预测，口径 B 能纯财务数据降级 |
| 单季利润表数据源 | 东财 F10 `reportDateType=2` | 直接出单季值，省去累计相减 |
| 业绩预告数据源 | 直连东财 `columns=ALL` | akshare 丢了上下限字段，直连才能拿到 |
| 分析师预测数据源 | 同花顺 `worth.html` 第 [2] 表 | akshare 的 `stock_profit_forecast_em` 无净利中位数 |
| 分析师预测只抓快照 | 不补历史 | 同花顺拿不到历史预测，用口径 B 降级 |
| 全市场遍历过滤 | `sec_type_code='001001'` | 排除可转债/B 股，省 11 分钟 |
| 分层设计 | collector/mapper/task 三层 | 纯函数可单测，task 只做粘合 |
| 入库方式 | `bulk_upsert` 幂等 | 断点续跑安全，重复抓不出错 |
| `announce_date` 用 `NOTICE_DATE` | 不 join `disclosure_yysj` | 实测 `NOTICE_DATE` 是首次披露日（见 §6.1）|
| 唯一索引设计 | 按业务语义定义 | 重复数据覆盖而非报错 |
| `companyType` 动态判断 | 不写死 | 银行/保险/券商报表结构不同 |

---

## 十、与 01e 的关系

01a 和 01e 共享同一套基础设施（`sec_basic_info`/`trade_calendar`/`bulk_upsert`/`safe_request`），但数据层各管各的：

| 维度 | 01a SUE | 01e 披露时点 |
|---|---|---|
| 数据表 | `analyst_forecast`/`financial_quarterly`/`performance_forecast` | `disclosure_yysj`/`trade_calendar` |
| 信号类型 | **内容**信号（实际 vs 预期）| **时机**信号（披露早 vs 晚）|
| 调仓频率 | 月度 | 季度 |
| 依赖分析师数据 | 是（口径 A）或可降级（口径 B）| 否 |
| 与 01e 正交性 | 两个信号维度独立，可叠加 | — |

01e 的实现讲解见 [PEAD-01e-实现讲解.md](./PEAD-01e-实现讲解.md)，重点讲 dReport 因子计算和调仓日。本文重点讲数据采集——因为 01a 目前只实现了采集层，策略计算尚未开始。

---

## 十一、下一步（策略层待实现）

采集层就绪后，SUE 因子计算需要：

1. **从 `financial_quarterly` 取单季净利**：按 `announce_date <= as_of` 过滤（防前视），取报告期的 `net_profit`
2. **从 `analyst_forecast` 取预期中位数**：按 `announce_date <= as_of` 过滤，每家机构取最新值，算中位数
3. **算 SUE**：$(E_{actual} - E_{expected}) / \sigma$，口径 B 用历史 8 季建模算 $\sigma$
4. **覆盖不足时降级**：用 `performance_forecast` 的 `(profit_min + profit_max) / 2` 近似 $E_{actual}$
5. **排序选股**：SUE 降序取前 N 只（只做多头端，SUE < 0 剔除）

这些逻辑会放在 `strategy/qmt/qmt_common/sue.py`（纯函数，可单测），和 01e 的 `dreport.py` 同级。

---

## 附录：相关文档导航

- **策略原理** → [01a SUE 单因子策略设计](../../strategy-directions/strategy-designs/01-pead/01a-pead-sue-single-factor.md)
- **SUE 因子概念** → [wiki: SUE因子](../../wiki/concepts/sue因子.md)
- **SUE 综合分析** → [wiki: SUE因子综合分析](../../wiki/syntheses/sue因子-综合分析.md)
- **01e 实现（对照参考）** → [PEAD-01e-实现讲解](./PEAD-01e-实现讲解.md)
- **环境配置与避坑** → [QMT 策略开发指南](./QMT策略开发指南.md)
