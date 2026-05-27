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

    def refresh(self, symbol: str) -> Optional[pd.DataFrame]:
        """Fetch latest candles and update in-memory store (rolling up to limit)."""
        df = self.client.get_klines(symbol, limit=self.limit)
        if df is None or df.empty:
            return self.store.get(symbol)
        self.store[symbol] = df
        return df

    def update_latest(self, symbol: str) -> Optional[pd.DataFrame]:
        """Fetch only recent few candles and merge with store to avoid refetching full history."""
        df_new = self.client.get_klines(symbol, limit=5)
        if df_new is None or df_new.empty:
            return self.store.get(symbol)
        existing = self.store.get(symbol)
        if existing is None:
            self.store[symbol] = df_new
            return df_new
        # join on close_time
        combined = pd.concat([existing, df_new]).drop_duplicates(subset=["close_time"]).sort_values("close_time")
        # keep last self.limit rows
        self.store[symbol] = combined.iloc[-self.limit :].reset_index(drop=True)
        return self.store[symbol]
