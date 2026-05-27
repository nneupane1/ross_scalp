from __future__ import annotations

import pandas as pd
from datetime import datetime
import yaml
from pathlib import Path

from .signal import Signal


class BreakoutStrategy:
    def __init__(self, lookback: int | None = None):
        cfg = yaml.safe_load(Path("config/strategy.yaml").read_text())
        lb = cfg.get("breakout", {}).get("lookback_candles", 5)
        self.lookback = lookback or int(lb)
        self.min_price_move_pct = float(cfg.get("breakout", {}).get("min_price_move_pct", 0.5))

    def check_breakout(self, symbol: str, df: pd.DataFrame) -> Signal | None:
        if df is None or df.empty or len(df) < self.lookback + 1:
            return None
        recent = df.iloc[-(self.lookback + 1):-1]
        recent_high = recent["high"].max()
        recent_low = recent["low"].min()
        last = df.iloc[-1]
        price_move_pct = (float(last["close"]) - float(last["open"])) / float(last["open"]) * 100
        if last["close"] > recent_high and price_move_pct >= self.min_price_move_pct:
            return Signal(
                symbol=symbol,
                type="BREAKOUT",
                price=float(last["close"]),
                time=datetime.utcnow(),
                meta={
                    "recent_high": float(recent_high),
                    "recent_low": float(recent_low),
                    "price_move_pct": price_move_pct,
                },
            )
        return None
