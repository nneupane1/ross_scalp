"""Helpers to compute market-level snapshots like percent change and volume ranking."""
from __future__ import annotations

from data_layer.binance_client import BinanceClient


class MarketSnapshot:
    def __init__(self, client: BinanceClient | None = None):
        self.client = client or BinanceClient()

    def top_gainers(self, top_n: int = 20):
        return self.client.get_top_gainers(top_n=top_n)
