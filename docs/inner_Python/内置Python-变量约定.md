# 内置Python - 变量约定

> 来源：https://dict.thinktrader.net/innerApi/variable_convention.html

## 函数命名规则

- 函数名以 `get_` 开头的，表示数据来源于客户端内存
- 函数名以 `query_` 开头的，表示数据是向服务查询

## 账号类型说明

| 值 | 说明 |
|---|---|
| 'FUTURE' | 期货账号 |
| 'STOCK' | 股票账号 |
| 'CREDIT' | 信用账号 |
| 'FUTURE_OPTION' | 期货期权 |
| 'STOCK_OPTION' | 股票期权 |
| 'HUGANGTONG' | 沪港通 |
| 'SHENGANGTONG' | 深港通 |

## symbol_code - 代码表示

格式：**交易标的代码.交易所代码**，例如 `000001.SZ`

### 交易所代码

| 交易所名称 | 迅投简称 | 显示后缀 |
|-----------|---------|---------|
| 上海证券交易所 | SH | SH |
| 深圳证券交易所 | SZ | SZ |
| 北京证券交易所 | BJ | BJ |
| 香港证券交易所 | HK | HK |
| 中国金融期货交易所 | IF | CFFEX |
| 上海期货交易所 | SF | SHFE |
| 大连商品交易所 | DF | DCE |
| 郑州商品交易所 | ZF | CZCE |
| 上海国际能源交易中心 | INE | INE |
| 广州期货交易所 | GF | GFEX |

### symbol 示例

| 市场 | 代码示例 | 说明 |
|------|---------|------|
| 上交所 | 600000.SH | 浦发银行 |
| 深交所 | 000001.SZ | 平安银行 |
| 北交所 | 830779.BJ | 武汉蓝电 |
| 中金所 | IC2311.IF | 中证500指数期货 |
| 上期所 | rb2311.SF | 螺纹钢期货 |
| 大商所 | m2311.DF | 豆粕期货 |
| 郑商所 | FG305.ZF | 玻璃期货 |
| 能源中心 | sc2311.INE | 原油期货 |
| 广期所 | lc2405.GF | 碳酸锂期货 |

> **注意**：期货合约代码严格区分大小写，`AP401.ZF` 不能写成 `ap401.ZF`

### 期货主力连续合约

仅支持回测模式下交易，如 `rb00.SF`（螺纹钢主连合约）

### 期货加权连续合约

仅支持回测模式下交易，如 `rbJQ00.SF`（加权连续合约）

## mode - 模式选择

| 模式 | 说明 |
|------|------|
| 调试运行模式 | 实时行情运算，不记录交易信号 |
| 回测模式 | 历史行情回测，记录交易结果 |
| 模拟信号模式 | 实时行情运算，不实际下单，仅记录信号 |
| 实盘交易模式 | 实时行情运算，实际下单交易 |

## ContextInfo - 上下文对象

### ContextInfo.start / ContextInfo.end

设定回测开始/结束时间，格式 `%Y-%m-%d %H:%M:%S`，仅回测模式生效。

### ContextInfo.capital

设定回测初始资金，默认 1000000。

### ContextInfo.period

获取当前周期，只读。值：`'1d'`, `'1m'`, `'3m'`, `'5m'`, `'15m'`, `'30m'`, `'1h'`, `'1w'`, `'1mon'`, `'1q'`, `'1hy'`, `'1y'`

### ContextInfo.barpos

获取当前运行到的 K 线索引号，只读，从 0 开始。

### ContextInfo.stockcode

获取当前主图代码，只读。

### ContextInfo.market

获取当前主图市场，只读。

### ContextInfo.dividend_type

获取当前主图复权处理方式。值：`'none'`, `'front'`, `'back'`, `'front_ratio'`, `'back_ratio'`

### ContextInfo.benchmark

获取回测基准标的，只读，仅回测模式可用。

### ContextInfo.do_back_test

表示当前是否为回测模式，只读，默认 False。
