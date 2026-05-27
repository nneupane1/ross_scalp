from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Rules:
    account_size: float = 25000
    risk_per_trade_pct: float = 0.3
    daily_max_loss_pct: float = 1.5
    daily_max_trades: int = 20
