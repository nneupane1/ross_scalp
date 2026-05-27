from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Signal:
    symbol: str
    type: str
    price: float
    time: datetime
    meta: dict | None = None
