from __future__ import annotations

from scanner.top_gainers import TopGainersScanner
from typing import List


class WatchlistManager:
    def __init__(self, top_n: int = 10):
        self.scanner = TopGainersScanner()
        self.top_n = top_n

    def build_watchlist(self) -> List[str]:
        gainers = self.scanner.scan(top_n=self.top_n)
        symbols = [g["symbol"] for g in gainers]
        return symbols
