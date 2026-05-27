"""Simple loop-based market stream that fetches latest candles periodically.

This is a lightweight alternative to a websocket stream for now.
"""
from __future__ import annotations

import time
from typing import Callable

from data_layer.binance_client import BinanceClient


class MarketStream:
    def __init__(self, client: BinanceClient | None = None):
        self.client = client or BinanceClient()

    def subscribe(self, symbol: str, callback: Callable):
        # Polling implementation: call callback with latest candle every interval
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
