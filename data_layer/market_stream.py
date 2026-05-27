"""Market stream helpers for polling and websocket-based candle updates."""
from __future__ import annotations

import time
import json
from typing import Callable

from data_layer.binance_client import BinanceClient


class MarketStream:
    def __init__(self, client: BinanceClient | None = None):
        self.client = client or BinanceClient()

    def subscribe(self, symbol: str, callback: Callable):
        last_ts = None
        df = self.client.get_klines(symbol, limit=2)
        if not df.empty:
            last_ts = df.iloc[-1]["close_time"]
            callback(symbol, df.iloc[-1:])

        while True:
            time.sleep(1)
            df = self.client.get_klines(symbol, limit=2)
            if df.empty:
                continue
            ts = df.iloc[-1]["close_time"]
            if ts != last_ts:
                last_ts = ts
                callback(symbol, df.iloc[-1:])


class WebsocketMarketStream:
    def __init__(self, callback: Callable, symbol: str, interval: str = "1m"):
        self.callback = callback
        self.symbol = symbol.lower()
        self.interval = interval
        self.connected = False
        self.ws_url = f"wss://stream.binance.com:9443/ws/{self.symbol}@kline_{self.interval}"

    def _on_message(self, message: str) -> None:
        payload = json.loads(message)
        k = payload.get("k", {})
        if not k:
            return
        candle = {
            "open_time": int(k.get("t", 0)),
            "open": float(k.get("o", 0)),
            "high": float(k.get("h", 0)),
            "low": float(k.get("l", 0)),
            "close": float(k.get("c", 0)),
            "volume": float(k.get("v", 0)),
            "close_time": int(k.get("T", 0)),
            "is_closed": k.get("x", False),
        }
        self.callback(self.symbol.upper(), candle)

    def run(self) -> None:
        try:
            from websocket import create_connection
        except ImportError:
            raise RuntimeError("websocket-client is required for websocket streaming")

        ws = create_connection(self.ws_url)
        self.connected = True
        while True:
            message = ws.recv()
            if message:
                self._on_message(message)
