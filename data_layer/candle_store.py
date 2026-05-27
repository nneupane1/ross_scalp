"""In-memory candle store with simple lazy fetch from Binance.

Stores up to `history_window` candles per symbol.
"""
from __future__ import annotations

from typing import Dict, Optional
import yaml
from pathlib import Path

import pandas as pd

from data_layer.binance_client import BinanceClient


class CandleStore:
    def __init__(self):
        self.client = BinanceClient()
        self.store: Dict[str, pd.DataFrame] = {}
        cfg = yaml.safe_load(Path("config/system.yaml").read_text())
        self.limit = int(cfg.get("data", {}).get("history_window", 100))

    def get_recent(self, symbol: str) -> Optional[pd.DataFrame]:
        df = self.store.get(symbol)
        if df is None or len(df) < 2:
            df = self.client.get_klines(symbol, limit=self.limit)
            self.store[symbol] = df
        return self.store.get(symbol)
