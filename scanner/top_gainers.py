from __future__ import annotations

from typing import List
from data_layer.binance_client import BinanceClient


class TopGainersScanner:
    def __init__(self, client: BinanceClient | None = None):
        self.client = client or BinanceClient()

    def scan(self, top_n: int = 20):
        return self.client.get_top_gainers(top_n=top_n)
