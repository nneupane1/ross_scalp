from __future__ import annotations

from scanner.top_gainers import TopGainersScanner
from scanner.momentum_filter import momentum_filter
from data_layer.candle_store import CandleStore
from typing import List
import yaml
from pathlib import Path


class WatchlistManager:
    def __init__(self, top_n: int | None = None):
        cfg = yaml.safe_load(Path("config/system.yaml").read_text())
        default_top = cfg.get("scanner", {}).get("top_n_symbols", 10)
        self.top_n = top_n or int(default_top)
        self.scanner = TopGainersScanner()
        self.candle_store = CandleStore()

    def build_watchlist(self) -> List[str]:
        """Build a watchlist by taking top gainers and filtering for recent activity."""
        gainers = self.scanner.scan(top_n=self.top_n * 2)
        symbols = [g["symbol"] for g in gainers]
        in_play: List[str] = []
        for s in symbols:
            try:
                df = self.candle_store.refresh(s)
                if df is None or df.empty:
                    continue
                # require recent momentum within last few candles
                if momentum_filter(df):
                    in_play.append(s)
                if len(in_play) >= self.top_n:
                    break
            except Exception:
                continue
        return in_play
