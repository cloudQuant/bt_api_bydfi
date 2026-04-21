"""BYDFi Ticker Data Container."""

from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base._compat import Self
from bt_api_base.containers.tickers.ticker import TickerData
from bt_api_base.functions.utils import from_dict_get_float, from_dict_get_string


class BYDFiRequestTickerData(TickerData):

    def __init__(self, ticker_info, symbol_name, asset_type, has_been_json_encoded=False) -> None:
        super().__init__(ticker_info, has_been_json_encoded)
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.exchange_name = "BYDFI"
        self.local_update_time = time.time()
        self.ticker_data = ticker_info if has_been_json_encoded else None
        self.ticker_symbol_name: str | None = None
        self.last_price: float | None = None
        self.bid_price: float | None = None
        self.ask_price: float | None = None
        self.volume_24h: float | None = None
        self.high_24h: float | None = None
        self.low_24h: float | None = None
        self.timestamp: int | None = None
        self.has_been_init_data = False

    def init_data(self) -> Self:
        if not self.has_been_json_encoded:
            self.ticker_data = json.loads(self.ticker_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        data = (self.ticker_data or {}).get("data", {})

        if data:
            self.ticker_symbol_name = data.get("symbol")
            self.last_price = from_dict_get_float(data, "price")
            self.bid_price = from_dict_get_float(data, "bidPrice")
            self.ask_price = from_dict_get_float(data, "askPrice")
            self.volume_24h = from_dict_get_float(data, "quoteVolume")
            self.high_24h = from_dict_get_float(data, "highPrice")
            self.low_24h = from_dict_get_float(data, "lowPrice")
            self.timestamp = from_dict_get_string(data, "time")

        self.has_been_init_data = True
        return self

    def get_symbol_name(self) -> str:
        return str(self.symbol_name)

    def get_exchange_name(self) -> str:
        return self.exchange_name

    def get_asset_type(self) -> str:
        return str(self.asset_type)

    def get_local_update_time(self) -> float:
        return self.local_update_time

    def get_ticker_symbol_name(self) -> str | None:
        return self.ticker_symbol_name

    def get_last_price(self) -> float | None:
        return self.last_price

    def get_bid_price(self) -> float | None:
        return self.bid_price

    def get_ask_price(self) -> float | None:
        return self.ask_price

    def get_all_data(self) -> dict[str, Any]:
        return {
            "symbol_name": self.symbol_name,
            "ticker_symbol_name": self.ticker_symbol_name,
            "exchange_name": self.exchange_name,
            "asset_type": self.asset_type,
            "last_price": self.last_price,
            "bid_price": self.bid_price,
            "ask_price": self.ask_price,
            "volume_24h": self.volume_24h,
            "high_24h": self.high_24h,
            "low_24h": self.low_24h,
            "timestamp": self.timestamp,
            "local_update_time": self.local_update_time,
        }

    def __str__(self) -> str:
        return f"BYDFiTicker(symbol={self.symbol_name}, price={self.last_price})"

    def __repr__(self) -> str:
        return self.__str__()