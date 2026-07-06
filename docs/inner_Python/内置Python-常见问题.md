# 内置Python - 常见问题

> 来源：https://dict.thinktrader.net/innerApi/question_answer.html

## Python环境相关

### 安装第三方 Python 库报错

`ImportError:Forbidden:Moduleopenpyxl not in whitelist!`

该报错是由于券商后台开启了 Python 库白名单，请联系所属券商开通对应 Python 库白名单权限。

### 启动策略时pandas库报错

**NameError: name 'pandas' is not defined**

1. 在`设置-模型设置`中检查正确设置了路径，正确路径应指向`{安装目录}\bin.x64`
2. 检查是否已经下载了python环境

**AttributeError: module 'pandas' has no attribute 'core'**

重启客户端即可。

### 系统自带的 Python 环境

集成的第三方库：NumPy、Pandas、Patsy、SciPy、Statsmodels、TA_Lib

### 第三方库导入指引

1. 本地安装Python 3.6环境
2. 安装到 `C:\Python36`
3. 新增环境变量
4. 安装命令：`pip install openpyxl -t E:\QMT交易端\bin.x64\Lib\site-packages`

## 业务规则相关

### 交易所委托数量规则

- 科创板：限价单笔最大10万股，市价5万股，200股起，1股递增
- 创业板：限价单笔最大30万股，市价15万股，100股起，100股递增
- 主板：单笔最大100万股，100股起，100股递增

## 策略回测相关

### QMT在回测时如何选择复权方式

推荐使用**等比前复权价**，避免配股、增发带来的价格异常波动。

## 交易相关

### 系统对象 ContextInfo 逐 k 线保存的机制

`ContextInfo`每次`handlebar`函数调用前会进行深拷贝。只有 k 线结束时最后一个分笔触发的`handlebar`调用，对`ContextInfo`的修改才有效。

**影响**：
1. 在`ContextInfo`中存数据每次分笔到达时会被深拷贝，拖慢策略运行
2. 不适宜立刻下单的情况，应使用普通全局变量保存状态

### 快速交易参数 quickTrade

- `0`：只在k线结束分笔时生效（默认）
- `1`：最新k线时调用即生效
- `2`：任何情况调用都生效，不会丢弃信号
- 定时器/回调函数/after_init中下单需要传`2`

### 下单与回报相关

1. 交易接口是异步的，调用后立即返回
2. 委托/成交/持仓更新在客户端后台进行，`get_trade_detail_data`从本地缓存读取
3. 实盘策略需要设计盘中保存/更新委托状态的机制

### QMT 下单失败

1. 检查是否在模型交易界面实盘模式运行
2. 检查`quickTrade`参数设置
3. 检查客户端左下角消息提示是否有报错

## 行情相关

### QMT 行情数据基础概念

三种行情数据：
1. **本地数据**：下载到本地的加密文件，适合回测，用`get_market_data_ex(subscribe=False)`
2. **全推数据**：客户端启动后自动接收的全市场最新数据快照，用`get_full_tick`或`subscribe_whole_quote`
3. **订阅数据**：向服务器订阅指定品种行情，用`subscribe_quote`或`get_market_data_ex(subscribe=True)`

### 行情调用函数对比

| 函数 | 用途 | 特点 |
|------|------|------|
| `download_history_data` | 下载历史数据到本地 | 存放硬盘 |
| `get_local_data` | 取本地数据 | 盘中不更新，速度快 |
| `get_full_tick` | 取最新全推数据 | 不含历史，无品种限制 |
| `subscribe_quote` | 订阅股票行情 | 实时更新，有数量限制 |
| `get_market_data_ex` | 取订阅/本地数据 | 综合接口 |

### openint证券状态值说明

**沪市**：9:15-9:25 盘前集合竞价(12) → 9:25-14:57 盘中连续竞价(13) → 14:57-15:00 盘后集合竞价(18) → 15:00 收盘(15)

**深市**：9:15-9:25 盘前集合竞价(12) → 9:25-9:30 休市(14) → 9:30-11:30 连续竞价(13) → 11:30-13:00 休市(14) → 13:00-14:57 连续竞价(13) → 14:57-15:00 盘后集合竞价(18) → 15:00 收盘(15)

## 软件运行日志

- 投研：`{安装目录}\userdata\log`
- QMT：`{安装目录}\userdata\log`
- 极简模式：`{安装目录}\userdata_mini\log`
