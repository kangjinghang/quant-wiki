# QMT 量化策略开发指南

> 沉淀自 PEAD 01e 披露时点策略的完整开发过程（2026-07），为后续所有 QMT 策略提供可复用的环境配置、架构模式、数据采集、避坑经验。
>
> **配套文档**：
> - 流程方法：`docs/superpowers/specs/` + `docs/superpowers/plans/`
> - QMT API：`docs/inner_Python/`（内置 Python）、`docs/XtQuant/`（外部 miniQMT）
> - 首个范例：[PEAD 01e 设计](../superpowers/specs/2026-07-07-pead-01e-disclosure-qmt-design.md) + [实现计划](../superpowers/plans/2026-07-07-pead-01e-disclosure-qmt.md)
>
> **核实状态**：2026-07-07 已在服务器（152.136.15.72）实地复核全文——Python 环境、依赖、路径、MySQL 表行数、QMT 路径与版本，并据实修正了原文与服务器不符之处（QMT 路径、f-string 兼容性）。最新缺口见第十节「后续待办」。

---

## 一、环境总览（三个工作区）

策略开发跨三个位置，各司其职：

```
┌─────────────────────────────────────────────────────────────┐
│  ① 开发机（mac）                                            │
│     路径：~/workspace/temp/llm-workspace/quant-wiki         │
│           ~/workspace/github/QuantVoyager                   │
│     Python：系统 3.14（无项目依赖，只跑纯函数单测）          │
│     职责：写代码、跑单测、git commit/push                    │
│     不能做：跑 Flask app、连服务器 MySQL、抓网络数据          │
├─────────────────────────────────────────────────────────────┤
│  ② 服务器（Windows，152.136.15.72）                          │
│     路径：C:\workspace\QuantVoyager                          │
│     Python：pyenv-win 3.10.11（全局，依赖齐全）              │
│             ⚠️ .venv 是空的不能用                             │
│     MySQL：8.0.45，quant_voyager 库（localhost）             │
│     QMT：内置 Python 3.6 + miniQMT（同机）                   │
│     职责：跑数据采集、Flask 任务、QMT 回测/实盘              │
├─────────────────────────────────────────────────────────────┤
│  ③ GitHub（kangjinghang/QuantVoyager）                      │
│     职责：开发机↔服务器的代码同步通道                        │
└─────────────────────────────────────────────────────────────┘
```

**代码流转**：开发机 commit → push GitHub → 服务器 `git pull` → 服务器跑。

---

## 二、服务器环境详解

### 2.1 连接

```bash
# SSH（密码免登已配置）
ssh Administrator@152.136.15.72 "<命令>"
```

⚠️ **SSH 执行 Python 的引号陷阱**：通过 SSH 跑内联 Python（`python -c "..."`）时，引号会被 SSH 层和 cmd 层双重转义破坏。**务必把脚本写到文件再跑**：

```bash
# ✅ 正确：本地写文件 → scp 上去 → 跑
cat > /tmp/_probe.py << 'PYEOF'
# -*- coding: utf-8 -*-
print("hello")
PYEOF
scp /tmp/_probe.py Administrator@152.136.15.72:C:/workspace/QuantVoyager/_probe.py
ssh Administrator@152.136.15.72 "cd C:\workspace\QuantVoyager && <python> _probe.py"

# ❌ 错误：内联 python -c，引号必坏
ssh ... "python -c \"import ...\""   # 大概率失败
```

### 2.2 Python 环境（关键避坑）

服务器用 **pyenv-win**，装了 3.10.11 / 3.11.9 / 3.12.0。但：

| Python | 能否跑 QuantVoyager | 说明 |
|---|---|---|
| `C:\Users\Administrator\.pyenv\pyenv-win\versions\3.10.11\python.exe` | ✅ **用这个** | 全局装了 flask_sqlalchemy/pymysql/pandas/requests/curl_cffi 等全套依赖 |
| pyenv 默认（3.11.9）| ❌ | 缺 flask_sqlalchemy |
| `.venv\Scripts\python.exe` | ❌ | **venv 是空的**（可能是 Windows 创建后未装依赖），import 直接 ModuleNotFoundError |

**固定用法**——所有服务器 Python 任务都用全路径：
```bash
ssh Administrator@152.136.15.72 "cd C:\workspace\QuantVoyager && C:\Users\Administrator\.pyenv\pyenv-win\versions\3.10.11\python.exe <脚本.py>"
```

### 2.3 MySQL

```bash
# root 只绑定了 localhost，必须用 TCP 协议 + 127.0.0.1
ssh Administrator@152.136.15.72 "mysql -uroot -p123456 -h 127.0.0.1 --protocol=TCP quant_voyager -e \"<SQL>\""

# ⚠️ 不带 -h 127.0.0.1 --protocol=TCP 会报 Access denied（root@localhost 走 socket）
# ⚠️ SSH 传 SQL 时中文会乱码（终端编码），但数据库实际存的是 utf8mb4 正确中文
#    验证时用 python 查而不是 mysql 命令行，避免乱码误导
```

数据库：`quant_voyager`。已有的可复用表：

| 表 | 内容 | 来源 |
|---|---|---|
| `sec_basic_info` | 证券基本信息（5522 只 A 股 + 可转债），含上市日 | QuantVoyager 原有 |
| `stock_core_indicator` | 股票核心指标（流通市值/PE/PB/ROE 等）| QuantVoyager 原有，⚠️ 可能是快照需补抓全量 |
| `disclosure_yysj` | 预约/实际披露日（PEAD 01e 新增）| 本次新增 |
| `trade_calendar` | 交易日历 | 本次新增 |
| `sec_daily_kline` | 日线（⚠️ 仅近期快照，回测不用）| QuantVoyager 原有 |

### 2.4 QMT

QMT 装在 `C:\QMT`，内置 Python **3.6.8**（`C:\QMT\bin.x64\pythonw.exe`，⚠️ 只有 `pythonw.exe` 无控制台版、**没有 `python.exe`**），与服务器 pyenv 的 3.10/3.11 完全独立。

| 限制 | 影响 |
|---|---|
| 不能装 akshare（要求 3.8+）| 所以数据走 MySQL，不直接抓 |
| 不能装 SQLAlchemy 2.0 | 用 pymysql 直连（纯 Python，可装）|
| walrus `:=`（3.8+）等新语法不能用 | 写 QMT 策略代码必须 3.6 兼容；f-string 在 3.6.8 实测可用，但建议统一用 `%`，避免 QMT 升级换解释器翻车 |
| 自带 pandas **0.22.0**（很老）| 不用额外装，但 API 受限——避免用新 pandas 的参数/方法 |

**QMT 内置 Python 装 pymysql**（✅ 2026-07-07 已装，PyMySQL 1.0.2，3.6.8 兼容；实测可连 quant_voyager + 查 disclosure_yysj + 读中文无乱码）：
```cmd
C:\QMT\bin.x64\pythonw.exe -m pip install pymysql
```

---

## 三、推荐架构（跨策略复用）

### 3.1 三层分离

```
QuantVoyager（Python 3.10）   →  MySQL quant_voyager  →  QMT 内置 Python 3.6
   数据采集 + 落库                 数据仓库（共享）         策略逻辑 + 回测 + 下单
   requests 直连东财                                       pymysql 读 + QMT 行情 + passorder
```

**核心原则**：
1. **行情走 QMT 自带**（`get_market_data_ex`），不进 MySQL——回测实盘同源、不重复缓存
2. **非行情数据进 MySQL**（披露日、财务、龙虎榜、分析师…）——QMT 拿不到的才存
3. **策略逻辑放 QMT 内置 Python**——回测实盘完全同代码，靠 `C.is_last_bar()` 区分
4. **数据采集放 QuantVoyager**——复用成熟的 safe_request + SQLAlchemy + APScheduler 框架

### 3.2 代码组织（QuantVoyager 内）

```
QuantVoyager/
├── data/                          # 数据层（QuantVoyager 原有，复用）
│   ├── data_models.py             # ORM 模型（新策略加表在这里加类）
│   ├── data_collector.py          # 抓取函数（复用 safe_request）
│   ├── data_mapper.py             # 数据映射（原始→ORM dict）
│   ├── data_storage.py            # bulk_upsert（批量写库，已有）
│   └── data_loader.py             # 启动加载
├── tasks/static_data_scheduled_tasks.py  # 定时任务函数
├── config/scheduler.yaml          # 任务调度配置
├── migrations/versions/           # Alembic 迁移脚本
├── scripts/                       # 一次性脚本（backfill 等）
└── strategy/qmt/                  # QMT 策略（PEAD 家族）
    ├── pead_01e_disclosure.py     # 主策略（init + handlebar）
    ├── qmt_common/                # 策略共享工具
    │   ├── db_reader.py           # MySQL 读取（pymysql，as_of 防前视）
    │   ├── dreport.py             # 因子计算（纯函数）
    │   └── rebalance.py           # 调仓日计算（纯函数）
    └── README.md
```

**新策略加数据域的步骤**（零成本复用）：
1. `data_models.py` 加 ORM 模型类
2. `data_collector.py` 加抓取函数（调东财，复用 safe_request）
3. `data_mapper.py` 加映射函数
4. `tasks/` + `scheduler.yaml` 加定时任务
5. Alembic 迁移（`flask db migrate` 或手写）
6. `strategy/qmt/` 加策略文件

### 3.3 防前视偏差（PEAD 策略最重要的工程问题）

前视偏差是 PEAD/事件策略最容易翻车的地方。统一处理模式：

**在因子计算的纯函数里用 `as_of` 参数**，而不是在 SQL 层：
```python
def compute_dreport_for_rebalance(df, as_of, current_report, prev_report):
    # 选披露日：实际披露日若 <= as_of 则用之，否则用预约日（防前视）
    def _pick(row):
        actual = row.get("actual_report_date")
        if actual is not None and _to_date(actual) <= as_of:
            return _to_date(actual)
        return _to_date(row.get("latest_book_date"))  # 预约日兜底
```

SQL 层只按 `report_date` 取数（今年+去年），可见性判断交给因子函数的 `as_of`。

---

## 四、开发流程（TDD + 服务器验证）

### 4.1 任务分类：哪些在开发机，哪些在服务器

| 任务类型 | 在哪做 | 说明 |
|---|---|---|
| 写 ORM 模型/抓取函数/映射函数/策略代码 | **开发机** | git commit |
| 纯函数单测（因子计算、调仓日、SQL 构造）| **开发机** | 只依赖 pandas + 标准库，能跑 |
| 网络抓取测试、Flask 任务、DB 落库 | **服务器** | 开发机无依赖/无网络 |
| Alembic 迁移、历史数据补抓 | **服务器** | 需 Flask 环境 + MySQL |
| QMT 回测、实盘 | **服务器 GUI** | 必须人工操作 QMT 客户端 |

### 4.2 开发机单测的 import 链问题

QuantVoyager 的 `data/` 包顶部有重依赖（flask_sqlalchemy 等），开发机 import 整个 `data` 包会失败。解决方案：

1. **纯函数模块**（如 `strategy/qmt/qmt_common/dreport.py`）只依赖 pandas + 标准库，开发机能直接 import 测试
2. **data_mapper 的纯函数测试**：用文本提取 + exec 方式，避免触发 data 包 import 链：
   ```python
   import re
   with open("data/data_mapper.py") as f: src = f.read()
   match = re.search(r'(def _normalize_symbol.*?)(?=\ndef |\Z)', src, re.DOTALL)
   ns = {"pd": pd}; exec(match.group(1), ns)
   normalize = ns['_normalize_symbol']
   ```
3. **测试文件顶部的 `import data` 包进 try/except**：让测试模块本身能 import，原有网络测试降级 skip

### 4.3 服务器验证流程（新数据源必做）

**任何新接的东财接口，必须先在服务器探测真实响应**，不能相信文档/akshare 源码里的字段名（akshare 会丢字段、文档可能过时）：

```python
# 1. 先探测原始响应（不经过封装）
url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
params = {"reportName": "<接口名>", "columns": "ALL", "pageSize": "3", ...}
r = safe_request(url, params=params)
print(r.json()['success'])           # 确认接口存在
print(list(r.json()['result']['data'][0].keys()))  # 拿真实字段名
print(r.json()['result']['data'][0])                # 看真实数据样例
# 2. 字段名确认后再写 mapper
```

---

## 五、东财接口实测笔记（价值高，血泪经验）

### 5.1 通用调用模式

东财 `datacenter-web.eastmoney.com/api/data/v1/get` 是万能数据接口，不同数据靠 `reportName` 区分：

```python
params = {
    "reportName": "<报表名>",        # 如 RPT_PUBLIC_BS_APPOIN
    "columns": "ALL",                # 取全部字段
    "pageSize": "500", "pageNumber": "1",
    "sortColumns": "<排序字段>",     # 可选
    "sortTypes": "1,1",
    "filter": "<过滤条件>",          # SQL 风格，如 (REPORT_DATE='2024-12-31')
    "source": "WEB", "client": "WEB",
}
```

**分页**：响应里有 `result.pages`（总页数），循环到最后一页。
**限速**：每页 `time.sleep(random.uniform(0.5, 1.0))`，避免被封。

**域名可用性（2026-07-07 服务器实测，重要）**：

| 域名 | 状态 | 说明 |
|---|---|---|
| `datacenter-web.eastmoney.com` | ✅ 稳定 | 披露日/财务类报表，普通 requests 即可，无需 TLS 绕过 |
| `push2.eastmoney.com` / `push2his.eastmoney.com` | ⚠️ **被封** | 整个 push2 域名族对该云服务器 IP 返回 `RemoteDisconnected`（IP 级封禁），**curl_cffi + chrome120 指纹也绕不过**——不是 TLS 指纹问题，是 IP 封禁 |

⚠️ **修正原 5.1 表述**：曾认为 push2 域名是 TLS 指纹检测、可用 curl_cffi 绕过。实测发现是 **IP 级封禁**，curl_cffi 无效。push2 系列接口（实时行情 clist、K线 kline）在该服务器上**完全不可用**。需要 K 线/行情数据时走 QMT 自带行情（`get_market_data_ex`）或其他数据源（如新浪 klc）。

#### 预约披露时间（PEAD 01e 用）
- **reportName**: `RPT_PUBLIC_BS_APPOIN`（⚠️ 不是 RPT_PUBLIC_OP_PREDICTDATE）
- **filter**: `(SECURITY_TYPE_CODE in ("058001001","058001008"))(TRADE_MARKET_CODE!="069001017")(REPORT_DATE='2024-12-31')`
  - 日期**必须带横线** `2024-12-31`（不是 `20241231`）
- **关键字段**：
  - `SECUCODE`：已含交易所后缀（如 `300708.SZ`），**直接用作 symbol，不用拼接**
  - `FIRST_APPOINT_DATE`：首次预约时间
  - `FIRST_CHANGE_DATE` / `SECOND_CHANGE_DATE` / `THIRD_CHANGE_DATE`：变更日期（取末次非空作 latest）
  - `ACTUAL_PUBLISH_DATE`：实际披露时间（null=未披露）
  - `SECURITY_NAME_ABBR`：股票简称
- **数据量**：单报告期约 3000-5200 条（随 A 股扩容）

### 5.3 akshare 字段丢失问题（重要）

akshare 对部分东财接口会**裁剪字段**。例如 `stock_yjyg_em`（业绩预告）只暴露单一"预测数值"，丢了上下限字段。**对策**：绕过 akshare，直接调东财 API（用 `columns: "ALL"` 拿全字段）。QuantVoyager 的 `safe_request` 模式就是为此设计。

---

## 六、Git 工作流

### 6.1 分支策略

```bash
# 开发机：每个策略一个 feature 分支
cd ~/workspace/github/QuantVoyager
git checkout -b feature/<策略名>     # 如 feature/pead-01e-disclosure

# ... 开发、commit ...

# 同步到服务器
git push -u origin feature/<策略名>
ssh Administrator@152.136.15.72 "cd C:\workspace\QuantVoyager && git fetch origin && git checkout feature/<策略名>"
```

⚠️ **scp 创建的文件会阻碍 git pull**（git 视为未跟踪文件，担心覆盖）。服务器上不要用 scp 放代码——用 git pull。临时探测脚本用完即删。

### 6.2 服务器有未跟踪文件导致 pull 失败

```bash
# 现象：git pull 报 "Aborting" / "untracked working tree files would be overwritten"
# 解决：删掉冲突的未跟踪文件再 pull
ssh Administrator@152.136.15.72 "cd C:\workspace\QuantVoyager && del <文件> && git pull"
```

---

## 七、PEAD 家族策略落地优先级（已验证可行性）

经核实原文 + akshare/东财接口后，PEAD 5 个策略的落地排序：

| 策略 | 数据降级 | 难度 | 状态 | 数据缺口 |
|---|---|---|---|---|
| **01e 披露时点** | 最小（8-9 折）| ⭐ | ✅ **已完成**（待回测）| 无 |
| **01d AOG 量价** | 最小（8-9 折）| ⭐ | 待做 | 仅需开盘价（QMT 自带）|
| **01a SUE 单因子** | 中（6-7 折）| ⭐⭐ | 待做 | 需新增分析师预期 + 财务表 |
| **01b Plus 五因子** | 大（5-6 折）| ⭐⭐⭐ | 待做 | 需微观结构因子（理想反转/小单残差，走日线代理版）|
| **01c Plus 2.0** | 大（5-6 折）| ⭐⭐⭐⭐ | 待做 | 01b + 4 道过滤 + 改进 FYR |

**下一个推荐做 01d**：数据需求最小（仅开盘价）、与 01e 正交、复用本套数据层，几乎零额外数据建设。

---

## 八、避坑清单（按踩坑顺序）

### 8.1 东财接口名/字段名不能信文档，必须实测
- **坑**：plan 里写的 `RPT_PUBLIC_OP_PREDICTDATE` 是错的，开发机 TDD 全绿但服务器抓到空数据
- **教训**：新接口先在服务器探测 `success:True` + 真实字段名，再写 mapper
- **修正 commit**：`1732d80`

### 8.2 dReport 跨年相减会得到常数（因子失效）
- **坑**：`今年披露日(2025-04-20) − 去年披露日(2024-04-28) = 357 天`，每只股票都~365，因子无区分度
- **教训**：同比类因子要把去年日期平移到今年同一年再相减
- **修正**：`dreport.py` 的 `_shift_to_this_year` 函数

### 8.3 MySQL root 只认 localhost socket
- **坑**：`mysql -uroot -p123456` 在 SSH 非交互环境报 Access denied
- **原因**：root 只有 `root@localhost`（socket），没有 `root@127.0.0.1`（TCP）
- **解决**：`CREATE USER 'root'@'127.0.0.1' ...` 或强制 `--protocol=TCP -h 127.0.0.1`

### 8.4 服务器 .venv 是空的
- **坑**：`.venv\Scripts\python.exe -c "import flask_sqlalchemy"` 报 ModuleNotFoundError
- **教训**：服务器用全局 pyenv 3.10.11（`C:\Users\Administrator\.pyenv\pyenv-win\versions\3.10.11\python.exe`），不要用 .venv

### 8.5 SSH 跑内联 Python 的引号地狱
- **坑**：`ssh ... "python -c \"...\""` 引号被双重转义破坏
- **解决**：写文件 → scp → 跑（永远这样，别内联）

### 8.6 中文乱码误导判断
- **坑**：SSH 终端看 MySQL 中文显示乱码，误以为数据损坏
- **教训**：用 Python + `ensure_ascii=False` 查，别信 cmd 终端的中文显示

### 8.7 QMT 策略代码必须 Python 3.6 兼容
- **坑**：用了 walrus `:=`（3.8+）等新语法在 QMT 里跑不了
- **教训**：写 `strategy/qmt/` 下的代码全程用 `%` 格式化，不用 3.7+ 语法
- **补充**：f-string 在 QMT 的 3.6.8 实测**可用**（3.6.0 起引入），但建议仍统一用 `%`——QMT 客户端升级可能换解释器，统一风格最稳

### 8.8 Alembic create_all 与 migrate 的关系
- **坑**：`db.create_all()` 建表后，`flask db migrate` 报 "No changes in schema detected"（因为表已存在）
- **解决**：手写迁移脚本 + `flask db stamp <revision>` 登记版本（不重复建表）

### 8.9 交易日历数据源连环失效
- **坑**：`trade_calendar` 表建了但一直 0 行，因为采集函数依赖的新浪 `klc_kd.js` 早已 404；改用东财 push2his 指数日线反推，结果整个 push2 域名族对服务器 IP 被封
- **教训**：数据源会随时间失效，**不能相信代码里写死的旧 URL，必须实测当前可用性**
- **解决**：用 akshare 最新版的稳定源——新浪 `klc_td_sh.txt`（私有编码，需 `py_mini_racer` + `sina_klc_decode.js` 解码，覆盖 1990-至今含未来到年底）
- **脚本**：`scripts/backfill_trade_calendar.py`（已落库 8797 行）

---

## 九、快速命令速查

### 开发机
```bash
# 跑纯函数单测
cd ~/workspace/github/QuantVoyager
PYTHONPATH=. python3 -m unittest tests.test_dreport tests.test_rebalance tests.test_db_reader

# 语法验证（开发机无法 import 含重依赖的模块）
python3 -c "import ast; ast.parse(open('<文件>').read()); print('OK')"

# push 到 GitHub
git push origin feature/<分支名>
```

### 服务器
```bash
PYTHON='C:\Users\Administrator\.pyenv\pyenv-win\versions\3.10.11\python.exe'

# 拉最新代码
ssh Administrator@152.136.15.72 "cd C:\workspace\QuantVoyager && git pull"

# 跑 Flask 任务（如抓数据）
ssh Administrator@152.136.15.72 "cd C:\workspace\QuantVoyager && $PYTHON scripts/<脚本>.py"

# 查 MySQL 数据
ssh Administrator@152.136.15.72 "mysql -uroot -p123456 -h 127.0.0.1 --protocol=TCP quant_voyager -e \"<SQL>\""

# Alembic 迁移
ssh Administrator@152.136.15.72 "cd C:\workspace\QuantVoyager && set FLASK_APP=app.py && $PYTHON -m flask db <命令>"
```

---

## 十、后续待办

> 2026-07-07 服务器核实后的实际状态。

- [ ] **PEAD 01e：QMT 回测验证**（对标招商原文绩效，预期 8-9 折）——回测前需先完成下面一项环境准备
- [x] **QMT 装 pymysql**（✅ 2026-07-07 已装 PyMySQL 1.0.2，实测连通 quant_voyager）
- [x] **`trade_calendar` 补数据**（✅ 2026-07-07 已补 8797 行，1990-12-19 ~ 2026-12-31，无周末，用新浪 klc_td_sh.txt）
- [ ] **`stock_core_indicator` 全量补抓**（实测仅 342 行，远小于 A 股规模；01e 小中盘划分需要全量）
- [ ] **`stock_core_indicator` 全量补抓**（实测仅 342 行，远小于 A 股规模；01e 小中盘划分需要全量）
- [ ] PEAD 01d AOG 量价策略：复用本套数据层，仅新增开盘价处理
- [ ] 考虑把 `strategy/qmt/qmt_common/` 沉淀成更通用的策略工具包（因子基类、回测净值计算、过滤器）
