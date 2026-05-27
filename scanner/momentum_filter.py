from __future__ import annotations

import pandas as pd


import yaml
from pathlib import Path


def momentum_filter(df: pd.DataFrame, min_price_move_pct: float | None = None, min_volume_multiplier: float | None = None) -> bool:
    """Return True if the last candle shows momentum relative to recent history.

    Loads defaults from `config/strategy.yaml` when parameters are not provided.
    """
    if df is None or df.empty:
        return False
    cfg = yaml.safe_load(Path("config/strategy.yaml").read_text())
    breakout_cfg = cfg.get("breakout", {})
    min_price_move_pct = min_price_move_pct if min_price_move_pct is not None else breakout_cfg.get("min_price_move_pct", 0.5)
    min_volume_multiplier = min_volume_multiplier if min_volume_multiplier is not None else breakout_cfg.get("min_volume_multiplier", 1.5)

    last = df.iloc[-1]
    prev = df.iloc[-6:-1]
    if prev.empty:
        return False
    avg_vol = prev["volume"].mean()
    vol_ok = last["volume"] >= avg_vol * float(min_volume_multiplier)
    price_move_pct = (float(last["close"]) - float(last["open"])) / float(last["open"]) * 100
    price_ok = abs(price_move_pct) >= float(min_price_move_pct)
    return vol_ok and price_ok
