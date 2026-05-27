from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Position:
    symbol: str
    entry_price: float
    size: float
    side: str = "LONG"
    stop: float | None = None
