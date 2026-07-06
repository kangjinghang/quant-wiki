# QMT 内置Python 快速开始

> 来源：https://dict.thinktrader.net/innerApi/start_now.html

## 一、概述

QMT 极速策略交易系统，以下简称 **QMT 系统**，内置了 **`3.6 版本`** 的 `python` 运行环境，提供**行情数据**与**交易下单**两大核心功能。通过编写 python 脚本，可以完成指标计算，策略编写，策略回测，实盘下单等需求。

## 二、场景需求

QMT 系统支持**回测模型**与**实盘模型**。

### 回测模型

指在历史 k 线上，自左向右逐根遍历 k 线，以模拟的资金账号记录每日的买卖信号，持仓盈亏，最终展示策略在历史上的净值走势结果。

**注意事项：**

1. 回测是遍历固定的历史数据，首先需要下载历史行情
2. 回测模型取本地数据遍历，不需要向服务器订阅实时行情，应使用 `get_market_data_ex` 函数，指定`subscribe`参数为`False`
3. 回测模型的撮合规则为：指定交易价格在当前k线高低点间的，按指定价格撮合；超过高低点的，按当前 k 线收盘价撮合。委托数量大于可用数量时，按可用数量撮合
4. 回测必须以`副图模式`执行，不要选择主图/主图叠加

### 实盘模型

指在盘中收取最新的动态行情，即时发送买卖信号到交易所，判断委托状态，需要实时重复报撤的模型。

**注意事项：**

1. 实盘模型提供两种交易模式：
   - **逐 k 线生效**（`passorder`函数`quicktrade`参数填`0`）：适用于需要在盘中模拟历史上逐 k 线的效果
   - **立即下单**（`passorder`函数`quicktrade`参数填`2`）：可以在运行后立刻发出委托，不对信号进行等待/丢弃
2. 实盘的撮合规则以交易所为准
3. 实盘模型需要在模型交易界面执行

## 三、运行机制对比

QMT 系统提供两大类(事件驱动与定时任务)，共三种运行机制：

| 机制 | 分类 | 特点 | 匹配需求 |
|------|------|------|----------|
| 逐 K 线运行（`handlebar`） | 事件驱动 | 同时支持历史回测和盘中可模拟逐K线效果 | 在实盘中模拟逐K线运行的效果 |
| 订阅推送（`subscribe`） | 事件驱动 | 盘中行情分笔触发函数调用 | 盘中随分笔行情判断交易 |
| 定时运行（`run_time`） | 定时任务 | 固定间隔触发调用 | 盘中固定时间间隔判断交易 |

### 逐 K 线驱动：handlebar

`handlebar`是**主图历史 k 线**+**盘中订阅推送**。运行开始时，所选周期历史 k 线从左向右每根触发一次`handlebar`函数调用。盘中时，主图品种每个新分笔数据到达，触发一次`handlebar`函数调用。

### 事件驱动：subscribe 订阅推送

盘中订阅指定品种的分笔数据，新分笔到达时，触发指定的回调函数。

### 定时任务：run_time 定时运行

指定固定的时间间隔，持续触发指定的回调函数。

## 四、逐 K 线驱动（handlebar）示例

> **注意**：编写策略时，首先需要在代码的最前一行写上：`#coding:gbk` 统一脚本的编码格式是`GBK`

### 回测示例-基于 handlebar

```python
#coding:gbk

import pandas as pd
import numpy as np
import talib

def init(C):
    C.stock = C.stockcode + '.' + C.market
    C.line1 = 10
    C.line2 = 20
    C.accountid = "testS"

def handlebar(C):
    bar_date = timetag_to_datetime(C.get_bar_timetag(C.barpos), '%Y%m%d%H%M%S')
    local_data = C.get_market_data_ex(['close'], [C.stock], end_time=bar_date, period=C.period, count=max(C.line1, C.line2), subscribe=False)
    close_list = list(local_data[C.stock].iloc[:, 0])
    if len(close_list) < 1:
        print(bar_date, '行情不足 跳过')
    line1_mean = round(np.mean(close_list[-C.line1:]), 2)
    line2_mean = round(np.mean(close_list[-C.line2:]), 2)
    print(f"{bar_date} 短均线{line1_mean} 长均线{line2_mean}")
    account = get_trade_detail_data('test', 'stock', 'account')
    account = account[0]
    available_cash = int(account.m_dAvailable)
    holdings = get_trade_detail_data('test', 'stock', 'position')
    holdings = {i.m_strInstrumentID + '.' + i.m_strExchangeID: i.m_nVolume for i in holdings}
    holding_vol = holdings[C.stock] if C.stock in holdings else 0
    if holding_vol == 0 and line1_mean > line2_mean:
        vol = int(available_cash / close_list[-1] / 100) * 100
        passorder(23, 1101, C.accountid, C.stock, 5, -1, vol, C)
        print(f"{bar_date} 开仓")
        C.draw_text(1, 1, '开')
    elif holding_vol > 0 and line1_mean < line2_mean:
        C.holding = False
        passorder(24, 1101, C.accountid, C.stock, 5, -1, holding_vol, C)
        print(f"{bar_date} 平仓")
        C.draw_text(1, 1, '平')
```

### 实盘示例-基于 handlebar

```python
#coding:gbk

import pandas as pd
import numpy as np
import datetime

class a():
    pass
A = a()

def init(C):
    A.stock = C.stockcode + '.' + C.market
    A.acct = account
    A.acct_type = accountType
    A.amount = 10000
    A.line1 = 17
    A.line2 = 27
    A.waiting_list = []
    A.buy_code = 23 if A.acct_type == 'STOCK' else 33
    A.sell_code = 24 if A.acct_type == 'STOCK' else 34

def handlebar(C):
    if not C.is_last_bar():
        return
    now = datetime.datetime.now()
    now_time = now.strftime('%H%M%S')
    if now_time < '093000' or now_time > "150000":
        return
    account = get_trade_detail_data(A.acct, A.acct_type, 'account')
    if len(account) == 0:
        print(f'账号{A.acct} 未登录 请检查')
        return
    account = account[0]
    available_cash = int(account.m_dAvailable)
    if A.waiting_list:
        found_list = []
        deals = get_trade_detail_data(A.acct, A.acct_type, 'deal')
        for deal in deals:
            if deal.m_strRemark in A.waiting_list:
                found_list.append(deal.m_strRemark)
        A.waiting_list = [i for i in A.waiting_list if i not in found_list]
    if A.waiting_list:
        print(f"当前有未查到委托 {A.waiting_list} 暂停后续报单")
        return
    holdings = get_trade_detail_data(A.acct, A.acct_type, 'position')
    holdings = {i.m_strInstrumentID + '.' + i.m_strExchangeID: i.m_nCanUseVolume for i in holdings}
    data = C.get_market_data_ex(["close"], [A.stock], period='1d', count=max(A.line1, A.line2)+1)
    close_list = data[A.stock].values
    if len(close_list) < max(A.line1, A.line2)+1:
        print('行情长度不足 跳过运行')
        return
    pre_line1 = np.mean(close_list[-A.line1-1: -1])
    pre_line2 = np.mean(close_list[-A.line2-1: -1])
    current_line1 = np.mean(close_list[-A.line1:])
    current_line2 = np.mean(close_list[-A.line2:])
    vol = int(A.amount / close_list[-1] / 100) * 100
    if A.amount < available_cash and vol >= 100 and A.stock not in holdings and pre_line1 < pre_line2 and current_line1 > current_line2:
        msg = f"双均线实盘 {A.stock} 上穿均线 买入 {vol}股"
        passorder(A.buy_code, 1101, A.acct, A.stock, 14, -1, vol, '双均线实盘', 2, msg, C)
        print(msg)
        A.waiting_list.append(msg)
    if A.stock in holdings and holdings[A.stock] > 0 and pre_line1 > pre_line2 and current_line1 < current_line2:
        msg = f"双均线实盘 {A.stock} 下穿均线 卖出 {holdings[A.stock]}股"
        passorder(A.sell_code, 1101, A.acct, A.stock, 14, -1, holdings[A.stock], '双均线实盘', 2, msg, C)
        print(msg)
        A.waiting_list.append(msg)
```

## 五、事件驱动（subscribe）示例

### 实盘示例-基于 subscribe

```python
#coding:gbk

class a(): pass
A = a()
A.bought_list = []

account = 'testaccount'

def init(C):
    def callback_func(data):
        for stock in data:
            current_price = data[stock]['close']
            pre_price = data[stock]['preClose']
            ratio = current_price / pre_price - 1
            print(stock, C.get_stock_name(stock), '当前涨幅', ratio)
            if ratio > 0 and stock not in A.bought_list:
                msg = f"当前涨幅 {ratio} 大于0 买入100股"
                print(msg)
                # passorder(23, 1101, account, stock, 5, -1, 100, '订阅下单示例', 2, msg, C)
                A.bought_list.append(stock)
    stock_list = ['600000.SH', '000001.SZ']
    for stock in stock_list:
        C.subscribe_quote(stock, period='1d', callback=callback_func)
```

## 六、定时任务（run_time）示例

### 实盘示例-基于 run_time

```python
#coding:gbk
import time, datetime

class a():
    pass
A = a()

def init(C):
    A.hsa = C.get_stock_list_in_sector('沪深A股')
    A.vol_dict = {}
    for stock in A.hsa:
        A.vol_dict[stock] = C.get_last_volume(stock)
    A.bought_list = []
    C.run_time("f", "1nSecond", "2019-10-14 13:20:00")

def f(C):
    t0 = time.time()
    now = datetime.datetime.now()
    full_tick = C.get_full_tick(A.hsa)
    total_market_value = 0
    total_ratio = 0
    count = 0
    for stock in A.hsa:
        ratio = full_tick[stock]['lastPrice'] / full_tick[stock]['lastClose'] - 1
        if ratio > 0.09 and stock not in A.bought_list:
            msg = f"{now} {stock} {C.get_stock_name(stock)} 当前涨幅 {ratio} 大于5% 买入100股"
            # passorder(23, 1101, account, stock, 5, -1, 100, '示例策略', 2, msg, C)
            A.bought_list.append(stock)
        market_value = full_tick[stock]['lastPrice'] * A.vol_dict[stock]
        total_ratio += ratio * market_value
        total_market_value += market_value
        count += 1
    total_ratio /= total_market_value
    total_ratio *= 100
    print(f'{now} 当前A股加权涨幅 {round(total_ratio, 2)}% 函数运行耗时{round(time.time()-t0, 5)}秒')
```

## 文档导航

| 页面 | 说明 |
|------|------|
| [使用须知](https://dict.thinktrader.net/innerApi/user_attention.html) | 内置API使用注意事项 |
| [界面操作](https://dict.thinktrader.net/innerApi/interface_operation.html) | 策略编辑、回测、模型交易界面操作 |
| [变量约定](https://dict.thinktrader.net/innerApi/variable_convention.html) | 变量命名和约定规则 |
| [数据结构](https://dict.thinktrader.net/innerApi/data_structure.html) | 内置数据结构说明 |
| [系统函数](https://dict.thinktrader.net/innerApi/system_function.html) | 系统级函数API |
| [行情函数](https://dict.thinktrader.net/innerApi/data_function.html) | 行情数据获取函数 |
| [交易函数](https://dict.thinktrader.net/innerApi/trading_function.html) | 交易下单函数 |
| [成交回报实时主推函数](https://dict.thinktrader.net/innerApi/callback_function.html) | 成交回报回调 |
| [引用函数](https://dict.thinktrader.net/innerApi/quote_function.html) | 引用相关函数 |
| [绘图函数](https://dict.thinktrader.net/innerApi/drawing_function.html) | 绘图函数 |
| [枚举常量](https://dict.thinktrader.net/innerApi/enum_constants.html) | 枚举常量定义 |
| [完整示例](https://dict.thinktrader.net/innerApi/code_examples.html) | 更多完整代码示例 |
| [常见问题](https://dict.thinktrader.net/innerApi/question_answer.html) | 常见问题解答 |
