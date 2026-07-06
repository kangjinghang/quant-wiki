# 内置Python - 行情函数

> 来源：https://dict.thinktrader.net/innerApi/data_function.html

## 数据下载

### download_history_data

```python
download_history_data(stockcode, period, startTime, endTime, incrementally=None)
```

下载指定合约代码指定周期对应时间范围的行情数据。

- `stockcode`: string，如 `'600000.SH'`
- `period`: `'tick'`, `'1d'`, `'1m'`, `'5m'`
- `startTime`/`endTime`: string，格式 `"20200101"` 或 `"20200101093000"`
- `incrementally`: bool，是否增量下载

合成周期说明：3m由1m合成，10m/15m/30m/60m/2h/3h/4h由5m合成，周线/月线等由日线合成。

## 获取行情数据

### ContextInfo.get_market_data_ex（推荐）

```python
ContextInfo.get_market_data_ex(
    fields=[], stock_code=[], period='follow',
    start_time='', end_time='', count=-1,
    dividend_type='follow', fill_data=True, subscribe=True)
```

获取实时行情与历史行情数据。

**period 可选**：`"tick"`, `"1m"`, `"5m"`, `"15m"`, `"30m"`, `"1h"`, `"1d"`, `"1w"`, `"1mon"`, `"1q"`, `"1hy"`, `"1y"`, `'l2quote'`, `'l2order'`, `'l2transaction'` 等

**dividend_type 可选**：`'none'`, `'front'`, `'back'`, `'front_ratio'`, `'back_ratio'`

**subscribe 参数**：True 订阅模式（有数量限制），False 本地模式（无限制但需提前下载数据）

**K线 field 可选**：`time`, `open`, `high`, `low`, `close`, `volume`, `amount`, `settle`, `openInterest`, `preClose`, `suspendFlag`

**tick field 可选**：`time`, `lastPrice`, `lastClose`, `open`, `high`, `low`, `close`, `volume`, `amount`, `settle`, `openInterest`, `stockStatus`

**返回**：dict { stock_code: pd.DataFrame }

### ContextInfo.get_full_tick

```python
ContextInfo.get_full_tick(stock_code=[])
```

获取最新分笔数据。不能用于回测，只能取最新值。

**返回**：dict { stock_code: {lastPrice, open, high, low, lastClose, amount, volume, askPrice, bidPrice, askVol, bidVol, ...} }

### ContextInfo.subscribe_quote

```python
ContextInfo.subscribe_quote(stock_code, period='follow', dividend_type='follow',
                           result_type='', callback=None)
```

订阅行情数据，返回订阅号。

- `result_type`: `'DataFrame'`(默认) / `'dict'` / `'list'`
- `callback`: 回调函数

### ContextInfo.subscribe_whole_quote

```python
ContextInfo.subscribe_whole_quote(code_list, callback=None)
```

订阅全推数据，code_list 支持市场代码（如 `['SH','SZ']`）或合约代码。

### ContextInfo.unsubscribe_quote

```python
ContextInfo.unsubscribe_quote(subId)
```

反订阅行情数据。

### subscribe_formula / unsubscribe_formula

订阅/反订阅 VBA 模型运行结果。

### call_formula / call_formula_batch

获取/批量获取 VBA 模型运行结果。

## 获取财务数据

### ContextInfo.get_financial_data

获取财务数据，支持资产负债表、利润表、现金流量表等。

### ContextInfo.get_raw_financial_data

获取原始财务数据。

### ContextInfo.get_last_volume / get_total_share

获取最新流通股本 / 总股数。

## 获取合约信息

### ContextInfo.get_instrument_detail

```python
ContextInfo.get_instrument_detail(stockcode)
```

根据代码获取合约详细信息。

### get_st_status

获取历史 ST 状态。

### ContextInfo.get_main_contract

获取期货主力合约。

### ContextInfo.get_contract_multiplier

获取合约乘数。

## 获取期权信息

### ContextInfo.get_option_detail_data

获取指定期权品种的详细信息。

### ContextInfo.get_option_list

获取指定期权列表。

### ContextInfo.bsm_price / bsm_iv

基于 BS 模型计算欧式期权理论价格 / 隐含波动率。

## 获取除复权信息

### ContextInfo.get_divid_factors

获取除权除息日和复权因子。

## 获取指数权重

### ContextInfo.get_weight_in_index

获取某只股票在某指数中的绝对权重。

## 获取成分股信息

### ContextInfo.get_stock_list_in_sector

```python
ContextInfo.get_stock_list_in_sector(sector)
```

获取板块成份股，如 `get_stock_list_in_sector('沪深A股')`。

## 获取交易日信息

### ContextInfo.get_trading_dates

获取交易日信息。
