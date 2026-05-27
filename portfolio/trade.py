from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Trade:
    symbol: str
    entry_time: datetime
    exit_time: datetime | None
    entry_price: float
    exit_price: float | None
    size: float
    pnl: float | None = None
