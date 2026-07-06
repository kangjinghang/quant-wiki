# xtquant 版本下载

> 来源：https://dict.thinktrader.net/nativeApi/download_xtquant.html

## 版本列表

| 更新日期 | 版本 | 下载 | 更新说明 |
|----------|------|------|----------|
| 20251219 | xtquant_250807 | [点击下载](/packages/xtquant_250807.rar) | token模式K线全推调整；xttrader支持智能算法；获取当前连接订阅数据信息；获取委托千档队列排名 |
| 20250516 | xtquant_250516 | [点击下载](/packages/xtquant_250516.rar) | 支持python3.13；xttrader支持银证转账、期货期权资金划转、北交所；交易数据字段调整；获取大单统计数据 |
| 20241017 | xtquant_241014 | [点击下载](/packages/xtquant_241014.rar) | 期权多空方向判断调整；get_trading_calendar自动下载节假日；tick增加现手字段；新增get_formula_result |
| 20240822 | xtquant_240812 | [点击下载](/packages/xtquant_240812.rar) | 期货夜盘真实时间；新增板块；撤单接口支持字符串市场参数；期权函数支持商品期权 |
| 20240617 | xtquant_240613 | [点击下载](/packages/xtquant_240613.rar) | 支持python3.12；get_full_kline；新闻公告/涨跌停连板/港股通持股数据；外盘行情；vba模型订阅 |
| 20240329 | xtquant_240329 | [点击下载](/packages/xtquant_240329.rar) | 郑商所4位年月代码；ETF iopv数据；新增板块；本地python回测多线程 |
| 20240205 | xtquant_240119b | [点击下载](/packages/xtquant_240119b.rar) | 修复token模式订阅异常；并行接入数量放宽至10个 |
| 20240129 | xtquant_240119a | [点击下载](/packages/xtquant_240119a.rar) | 合约信息支持全部字段；客户端连接状态监听；退市/待发可转债数据 |
| 20240119 | xtquant_240119 | [点击下载](/packages/xtquant_240119.rar) | 新增周/月/季/半年/年线；千档委买委卖队列；港股lv2；商品期权；历史主力合约 |
| 20231228 | xtquant_231209a | [点击下载](/packages/xtquant_231209a.rar) | 修复交易日历重复；快照指标数据；修复板块指数分钟线 |
| 20231209 | xtquant_231209 | [点击下载](/packages/xtquant_231209.rar) | ETF申赎清单接口；节假日下载；涨跌停数据；财务数据字段说明 |
| 20231124 | xtquant_231101c | [点击下载](/packages/xtquant_231101c.rar) | 修复内存泄漏；全推数据懒加载；期货全推补全 |
| 20231110 | xtquant_231101b | [点击下载](/packages/xtquant_231101b.rar) | 修复过期合约板块；增量下载参数 |
| 20231106 | xtquant_231101a | [点击下载](/packages/xtquant_231101a.rar) | 修复退出异常；优化初始化时序 |
| 20231101 | xtquant_231101 | [点击下载](/packages/xtquant_20231101.rar) | 添加xtdatacenter支持token方式登录；xtdata.QuoteServer；期货交易开平仓方向 |
| 20230920 | xtquant_230825b | [点击下载](/packages/xtquant_0825b_2023-09-20.rar) | 对应当前QMT券商版公版python库 |
| 20230905 | xtquant_230825a | [点击下载](/packages/xtquant_20230825a.rar) | - |
| 20230825 | xtquant_230825 | [点击下载](/packages/xtquant_20230825.rar) | - |
| 20230301 | xtquant_230301 | [点击下载](/packages/xtquant_20230301.rar) | - |
| 20220817 | xtquant_220817 | [点击下载](/packages/xtquant_20220817.rar) | - |

## 重要更新说明

### 最新版 (xtquant_250807)

- **token模式**：K线全推和全推数据加载模式调整，从xtdc.init()后立刻加载，调整为在第一次使用数据时加载
- **智能算法**：xttrader支持智能算法下单（get_smart_algo_param, smart_algo_order_async, query_smart_algo_task, cancel_smart_algo_task_async）
- **订阅信息**：get_current_connect_sub_info（投研版本）、get_all_sub_info()（投研版本）
- **千档队列排名**：get_order_rank()（投研版本）
- **token模式千档数据源**：xtdc.set_thousand_source_mode()
- **BugFix**：修复期货0点前夜盘复权不生效的问题

### Python版本支持

| 版本 | 支持的Python版本 |
|------|-----------------|
| xtquant_250516+ | 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12, 3.13 |
| xtquant_240613 | 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12 |
| 早期版本 | 3.6, 3.7, 3.8, 3.9, 3.10, 3.11 |
