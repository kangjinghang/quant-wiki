# QMT 内置Python 成交回报实时主推函数

> 来源：https://dict.thinktrader.net/innerApi/callback_function.html

## 一、实时主推函数

> **提示**：
> 1. 仅在实盘运行模式下生效。
> 2. 需要先在init里调用ContextInfo.set_account后生效。

### 1. account_callback - 资金账号状态变化主推

**用法：** `account_callback(ContextInfo, accountInfo)`

**释义：** 当资金账号状态有变化时，这个函数被客户端调用

**参数：**
- ContextInfo：特定对象
- accountInfo：[账号对象](https://dict.thinktrader.net/innerApi/data_structure.html#account-账户对象)

**返回：** 无

```python
#coding:gbk
def show_data(data):
    tdata = {}
    for ar in dir(data):
        if ar[:2] != 'm_':continue
        try:
            tdata[ar] = data.__getattribute__(ar)
        except:
            tdata[ar] = '<CanNotConvert>'
    return tdata

def init(ContextInfo):
    ContextInfo.set_account(account)
    
def after_init(ContextInfo):
    passorder(23, 1101, account, "000001.SZ", 5, 0, 100, "示例", 2, "投资备注",ContextInfo)
    pass

def account_callback(ContextInfo, accountInfo):
    print(show_data(accountInfo)) 
```

### 2. task_callback - 账号任务状态变化主推

**用法：** `task_callback(ContextInfo, taskInfo)`

**释义：** 当账号任务状态有变化时，这个函数被客户端调用

**参数：**
- ContextInfo：特定对象
- taskInfo：[任务对象](https://dict.thinktrader.net/innerApi/data_structure.html#ctaskdetail-任务对象)

**返回：** 无

```python
#coding:gbk
def show_data(data):
    tdata = {}
    for ar in dir(data):
        if ar[:2] != 'm_':continue
        try:
            tdata[ar] = data.__getattribute__(ar)
        except:
            tdata[ar] = '<CanNotConvert>'
    return tdata

def init(ContextInfo):
    ContextInfo.set_account(account)
    
def after_init(ContextInfo):
    passorder(23, 1101, account, "000001.SZ", 5, 0, 100, "示例", 2, "投资备注",ContextInfo)
    pass

def task_callback(ContextInfo, taskInfo):
    print(show_data(taskInfo))
```

### 3. order_callback - 账号委托状态变化主推

**用法：** `order_callback(ContextInfo, orderInfo)`

**释义：** 当账号委托状态有变化时，这个函数被客户端调用

**参数：**
- ContextInfo：特定对象
- orderInfo：[委托对象](https://dict.thinktrader.net/innerApi/data_structure.html#order-委托对象)

**返回：** 无

```python
#coding:gbk
def show_data(data):
    tdata = {}
    for ar in dir(data):
        if ar[:2] != 'm_':continue
        try:
            tdata[ar] = data.__getattribute__(ar)
        except:
            tdata[ar] = '<CanNotConvert>'
    return tdata

def init(ContextInfo):
    ContextInfo.set_account(account)
    
def after_init(ContextInfo):
    passorder(23, 1101, account, "000001.SZ", 5, 0, 100, "示例", 2, "投资备注",ContextInfo)
    pass

def order_callback(ContextInfo, orderInfo):
    print(show_data(orderInfo))
```

### 4. deal_callback - 账号成交状态变化主推

**用法：** `deal_callback(ContextInfo, dealInfo)`

**释义：** 当账号成交状态有变化时，这个函数被客户端调用

**参数：**
- ContextInfo：特定对象
- dealInfo：[成交对象](https://dict.thinktrader.net/innerApi/data_structure.html#deal-成交对象)

**返回：** 无

```python
#coding:gbk
def show_data(data):
    tdata = {}
    for ar in dir(data):
        if ar[:2] != 'm_':continue
        try:
            tdata[ar] = data.__getattribute__(ar)
        except:
            tdata[ar] = '<CanNotConvert>'
    return tdata

def init(ContextInfo):
    ContextInfo.set_account(account)
    
def after_init(ContextInfo):
    passorder(23, 1101, account, "000001.SZ", 5, 0, 100, "示例", 2, "投资备注",ContextInfo)
    pass

def deal_callback(ContextInfo, dealInfo):
    print(show_data(dealInfo))
```

### 5. position_callback - 账号持仓状态变化主推

**用法：** `position_callback(ContextInfo, positonInfo)`

**释义：** 当账号持仓状态有变化时，这个函数被客户端调用

**参数：**
- ContextInfo：特定对象
- positonInfo：[持仓对象](https://dict.thinktrader.net/innerApi/data_structure.html#position-持仓对象)

**返回：** 无

```python
#coding:gbk
def show_data(data):
    tdata = {}
    for ar in dir(data):
        if ar[:2] != 'm_':continue
        try:
            tdata[ar] = data.__getattribute__(ar)
        except:
            tdata[ar] = '<CanNotConvert>'
    return tdata

def init(ContextInfo):
    ContextInfo.set_account(account)
    
def after_init(ContextInfo):
    passorder(23, 1101, account, "000001.SZ", 5, 0, 100, "示例", 2, "投资备注",ContextInfo)
    pass

def position_callback(ContextInfo, positionInfo):
    print(show_data(positionInfo))
```

### 6. orderError_callback - 账号异常下单主推

**用法：** `orderError_callback(ContextInfo, orderArgs, errMsg)`

**释义：** 当账号下单异常时，这个函数被客户端调用

**参数：**
- ContextInfo：特定对象
- orderArgs：[下单参数对象](https://dict.thinktrader.net/innerApi/data_structure.html#passorderarguments-下单函数参数对象)
- errMsg：错误信息

**返回：** 无

```python
#coding:gbk
def show_data(data):
    tdata = {}
    for ar in dir(data):
        if ar[:2] != 'm_':continue
        try:
            tdata[ar] = data.__getattribute__(ar)
        except:
            tdata[ar] = '<CanNotConvert>'
    return tdata

def init(ContextInfo):
    ContextInfo.set_account(account)
    
def after_init(ContextInfo):
    passorder(23, 1101, account, "000001.SZ", 11, 0, 100, "示例", 2, "投资备注",ContextInfo)
    pass

def orderError_callback(ContextInfo,orderArgs,errMsg):
    print(show_data(orderArgs))
    print(errMsg)
```

## 二、其他主推函数

### 1. credit_account_callback - 查询信用账户明细回调

**用法：** `credit_account_callback(ContextInfo, seq, result)`

**释义：** 查询信用账户明细回调

**参数：**
- ContextInfo：策略模型全局对象
- seq：query_credit_account时输入查询seq
- result：[信用账户明细](https://dict.thinktrader.net/innerApi/data_structure.html#ccreditdetail-两融资金信息-查询台)

### 2. credit_opvolume_callback - 查询两融最大可下单量的回调

**用法：** `credit_opvolume_callback(ContextInfo, accid, seq, ret, result)`

**释义：** 查询两融最大可下单量的回调。

**参数：**
- `ContextInfo`：策略模型全局对象
- `accid`：查询的账号
- `seq`：`query_credit_opvolume`时输入查询`seq`
- `ret`：查询结果状态。正常返回:`1`,正在查询中`-1`,输入账号非法:`-2`,输入查询参数非法:`-3`,超时等服务器返回报错:`-4`
- `result`：查询到的结果
