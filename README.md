# bt_api_bydfi

[![PyPI Version](https://img.shields.io/pypi/v/bt_api_bydfi.svg)](https://pypi.org/project/bt_api_bydfi/)
[![Python Versions](https://img.shields.io/pypi/pyversions/bt_api_bydfi.svg)](https://pypi.org/project/bt_api_bydfi/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/cloudQuant/bt_api_bydfi/actions/workflows/ci.yml/badge.svg)](https://github.com/cloudQuant/bt_api_bydfi/actions)
[![Docs](https://readthedocs.org/projects/bt-api-bydfi/badge/?version=latest)](https://bt-api-bydfi.readthedocs.io/)

---

<!-- English -->
# bt_api_bydfi

> **BYDFi exchange plugin for bt_api** — Unified REST API for Spot trading with real-time WebSocket support.

`bt_api_bydfi` is a runtime plugin for [bt_api](https://github.com/cloudQuant/bt_api_py) that connects to **BYDFi** exchange. It depends on [bt_api_base](https://github.com/cloudQuant/bt_api_base) for core infrastructure.

| Resource | Link |
|----------|------|
| English Docs | https://bt-api-bydfi.readthedocs.io/ |
| Chinese Docs | https://bt-api-bydfi.readthedocs.io/zh/latest/ |
| GitHub | https://github.com/cloudQuant/bt_api_bydfi |
| PyPI | https://pypi.org/project/bt_api_bydfi/ |
| Issues | https://github.com/cloudQuant/bt_api_bydfi/issues |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| Main Project | https://github.com/cloudQuant/bt_api_py |

---

## Features

### Asset Types

| Asset Type | Code | REST | WebSocket | Description |
|---|---|---|---|---|
| Spot | `BYDFI___SPOT` | ✅ | — | Spot trading |

### Dual API Modes

- **REST API** — Synchronous polling for order management, balance queries, historical data
- **WebSocket API** — Real-time streaming for ticker, order book, k-lines, trades (planned)

### Plugin Architecture

Auto-registers at import time via `ExchangeRegistry`. Works seamlessly with `BtApi`:

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BYDFI___SPOT": {
        "api_key": "your_key",
        "secret": "your_secret",
    }
})

ticker = api.get_tick("BYDFI___SPOT", "BTCUSDT")
balance = api.get_balance("BYDFI___SPOT")
order = api.make_order(exchange_name="BYDFI___SPOT", symbol="BTCUSDT", volume=0.001, price=50000, order_type="limit")
```

### Unified Data Containers

All exchange responses normalized to bt_api_base container types:

- `TickContainer` — 24hr rolling ticker
- `OrderBookContainer` — Order book depth
- `BarContainer` — K-line/candlestick
- `TradeContainer` — Individual trades
- `OrderContainer` — Order status and fills
- `AccountBalanceContainer` — Asset balances

---

## Installation

### From PyPI (Recommended)

```bash
pip install bt_api_bydfi
```

### From Source

```bash
git clone https://github.com/cloudQuant/bt_api_bydfi
cd bt_api_bydfi
pip install -e .
```

### Requirements

- Python `3.9` – `3.14`
- `bt_api_base >= 0.15`
- `httpx` for HTTP client

---

## Quick Start

### 1. Install

```bash
pip install bt_api_bydfi
```

### 2. Get ticker (public — no API key needed)

```python
from bt_api_py import BtApi

api = BtApi()
ticker = api.get_tick("BYDFI___SPOT", "BTCUSDT")
print(f"BTCUSDT price: {ticker.last_price}")
```

### 3. Place an order (requires API key)

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BYDFI___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_secret",
    }
})

order = api.make_order(
    exchange_name="BYDFI___SPOT",
    symbol="BTCUSDT",
    volume=0.001,
    price=50000,
    order_type="limit",
)
print(f"Order placed: {order}")
```

### 4. Get balance

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BYDFI___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_secret",
    }
})

balance = api.get_balance("BYDFI___SPOT")
print(f"Balance: {balance}")
```

---

## Architecture

```
bt_api_bydfi/
├── src/bt_api_bydfi/
│   ├── __init__.py                  # Package exports
│   ├── registry_registration.py     # BYDFi feed/exchange_data registration
│   ├── containers/
│   │   ├── __init__.py
│   │   ├── exchanges/
│   │   │   ├── __init__.py
│   │   │   └── bydfi_exchange_data.py  # BYDFiExchangeData, BYDFiExchangeDataSpot
│   │   └── tickers/
│   │       ├── __init__.py
│   │       └── bydfi_ticker.py     # BYDFiRequestTickerData
│   └── feeds/
│       ├── __init__.py
│       ├── request_base.py           # BYDFiRequestData base class
│       └── spot.py                  # BYDFiRequestDataSpot
├── tests/
├── docs/
├── pyproject.toml
└── README.md
```

---

## Supported Operations

| Category | Operation | Notes |
|---|---|---|
| **Market Data** | `get_ticker` | 24hr rolling ticker |
| | `get_orderbook` | Depth up to 100 |
| | `get_bars` | Intervals: 1m/5m/15m/30m/1h/4h/1d/1w |
| | `get_trades` | Recent trade history |
| | `get_exchange_info` | Trading rules and symbol info |
| **Account** | `get_balance` | All asset balances |
| | `get_account` | Full account info |
| **Trading** | `make_order` | LIMIT/MARKET orders |
| | `cancel_order` | Cancel single order |
| | `query_order` | Query order by ID |
| | `get_open_orders` | All open orders |

---

## API Authentication

BYDFi uses HMAC-SHA256 authentication:

```
signature = HMAC-SHA256(accessKey + timestamp + queryString + body)
```

Required headers:
- `X-API-KEY` — API key
- `X-API-TIMESTAMP` — Request timestamp (milliseconds)
- `X-API-SIGNATURE` — HMAC-SHA256 signature

---

## Rate Limits

| Endpoint | Limit |
|---|---|
| Public endpoints | 60 requests/minute |
| Private endpoints | 30 requests/minute |

---

## Documentation

| Doc | Link |
|-----|------|
| **English** | https://bt-api-bydfi.readthedocs.io/ |
| **中文** | https://bt-api-bydfi.readthedocs.io/zh/latest/ |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| Main Project | https://cloudquant.github.io/bt_api_py/ |

---

## License

MIT — see [LICENSE](LICENSE).

---

## Support

- [GitHub Issues](https://github.com/cloudQuant/bt_api_bydfi/issues) — bug reports, feature requests
- Email: yunjinqi@gmail.com

---

---

## 中文

> **bt_api 的 BYDFi 交易所插件** — 为现货交易提供统一的 REST API 和实时 WebSocket 支持。

`bt_api_bydfi` 是 [bt_api](https://github.com/cloudQuant/bt_api_py) 的运行时插件，连接 **BYDFi** 交易所。依赖 [bt_api_base](https://github.com/cloudQuant/bt_api_base) 提供核心基础设施。

| 资源 | 链接 |
|------|------|
| 英文文档 | https://bt-api-bydfi.readthedocs.io/ |
| 中文文档 | https://bt-api-bydfi.readthedocs.io/zh/latest/ |
| GitHub | https://github.com/cloudQuant/bt_api_bydfi |
| PyPI | https://pypi.org/project/bt_api_bydfi/ |
| 问题反馈 | https://github.com/cloudQuant/bt_api_bydfi/issues |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| 主项目 | https://github.com/cloudQuant/bt_api_py |

---

## 功能特点

### 资产类型

| 资产类型 | 代码 | REST | WebSocket | 说明 |
|---|---|---|---|---|
| 现货 | `BYDFI___SPOT` | ✅ | — | 现货交易 |

### 双 API 模式

- **REST API** — 同步轮询：订单管理、余额查询、历史数据
- **WebSocket API** — 实时流：行情、订单簿、K线、交易（计划中）

### 插件架构

通过 `ExchangeRegistry` 在导入时自动注册，与 `BtApi` 无缝协作：

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BYDFI___SPOT": {
        "api_key": "your_key",
        "secret": "your_secret",
    }
})

ticker = api.get_tick("BYDFI___SPOT", "BTCUSDT")
balance = api.get_balance("BYDFI___SPOT")
order = api.make_order(exchange_name="BYDFI___SPOT", symbol="BTCUSDT", volume=0.001, price=50000, order_type="limit")
```

### 统一数据容器

所有交易所响应规范化为 bt_api_base 容器类型：

- `TickContainer` — 24小时滚动行情
- `OrderBookContainer` — 订单簿深度
- `BarContainer` — K线/蜡烛图
- `TradeContainer` — 逐笔成交
- `OrderContainer` — 订单状态和成交
- `AccountBalanceContainer` — 资产余额

---

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install bt_api_bydfi
```

### 从源码安装

```bash
git clone https://github.com/cloudQuant/bt_api_bydfi
cd bt_api_bydfi
pip install -e .
```

### 系统要求

- Python `3.9` – `3.14`
- `bt_api_base >= 0.15`
- `httpx` HTTP 客户端

---

## 快速开始

### 1. 安装

```bash
pip install bt_api_bydfi
```

### 2. 获取行情（公开接口，无需 API key）

```python
from bt_api_py import BtApi

api = BtApi()
ticker = api.get_tick("BYDFI___SPOT", "BTCUSDT")
print(f"BTCUSDT 价格: {ticker.last_price}")
```

### 3. 下单交易（需要 API key）

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BYDFI___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_secret",
    }
})

order = api.make_order(
    exchange_name="BYDFI___SPOT",
    symbol="BTCUSDT",
    volume=0.001,
    price=50000,
    order_type="limit",
)
print(f"订单已下单: {order}")
```

### 4. 获取余额

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BYDFI___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_secret",
    }
})

balance = api.get_balance("BYDFI___SPOT")
print(f"余额: {balance}")
```

---

## 架构

```
bt_api_bydfi/
├── src/bt_api_bydfi/
│   ├── __init__.py                  # 包导出
│   ├── registry_registration.py     # BYDFi feed/exchange_data 注册
│   ├── containers/
│   │   ├── __init__.py
│   │   ├── exchanges/
│   │   │   ├── __init__.py
│   │   │   └── bydfi_exchange_data.py  # BYDFiExchangeData, BYDFiExchangeDataSpot
│   │   └── tickers/
│   │       ├── __init__.py
│   │       └── bydfi_ticker.py     # BYDFiRequestTickerData
│   └── feeds/
│       ├── __init__.py
│       ├── request_base.py           # BYDFiRequestData 基类
│       └── spot.py                  # BYDFiRequestDataSpot
├── tests/
├── docs/
├── pyproject.toml
└── README.md
```

---

## 支持的操作

| 类别 | 操作 | 说明 |
|---|---|---|
| **行情数据** | `get_ticker` | 24小时滚动行情 |
| | `get_orderbook` | 深度最高100档 |
| | `get_bars` | 周期: 1m/5m/15m/30m/1h/4h/1d/1w |
| | `get_trades` | 近期成交历史 |
| | `get_exchange_info` | 交易规则和交易对信息 |
| **账户** | `get_balance` | 所有资产余额 |
| | `get_account` | 完整账户信息 |
| **交易** | `make_order` | 限价/市价订单 |
| | `cancel_order` | 撤销单笔订单 |
| | `query_order` | 按ID查询订单 |
| | `get_open_orders` | 所有挂单 |

---

## API 认证

BYDFi 使用 HMAC-SHA256 认证：

```
signature = HMAC-SHA256(accessKey + timestamp + queryString + body)
```

必需请求头：
- `X-API-KEY` — API 密钥
- `X-API-TIMESTAMP` — 请求时间戳（毫秒）
- `X-API-SIGNATURE` — HMAC-SHA256 签名

---

## 限流配置

| 端点 | 限制 |
|---|---|
| 公开接口 | 60 次/分钟 |
| 私有接口 | 30 次/分钟 |

---

## 文档

| 文档 | 链接 |
|-----|------|
| **英文文档** | https://bt-api-bydfi.readthedocs.io/ |
| **中文文档** | https://bt-api-bydfi.readthedocs.io/zh/latest/ |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| 主项目 | https://cloudquant.github.io/bt_api_py/ |

---

## 许可证

MIT — 详见 [LICENSE](LICENSE)。

---

## 技术支持

- [GitHub Issues](https://github.com/cloudQuant/bt_api_bydfi/issues) — bug 报告、功能请求
- 邮箱: yunjinqi@gmail.com