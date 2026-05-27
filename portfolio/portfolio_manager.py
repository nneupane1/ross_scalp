from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import List

from portfolio.position import Position
from strategy.signal import Signal
from portfolio.trade import Trade
from utils.logging_utils import append_csv
from datetime import datetime


class PortfolioManager:
    def __init__(self):
        p = Path("data/state/portfolio_state.json")
        if p.exists():
            self.state = json.loads(p.read_text())
        else:
            self.state = {"equity": 25000, "cash": 25000, "positions": []}
        self.positions: List[Position] = []
        self.trades: List[Trade] = []

    def execute_trade(self, signal: Signal) -> None:
        # Simple market entry: allocate fixed cash per trade
        cash = self.state.get("cash", 0)
        alloc = min(1000, cash)
        size = alloc / signal.price
        pos = Position(symbol=signal.symbol, entry_price=signal.price, size=size)
        self.positions.append(pos)
        self.state["cash"] = cash - alloc
        t = Trade(symbol=signal.symbol, entry_time=signal.time, exit_time=None, entry_price=signal.price, exit_price=None, size=size)
        self.trades.append(t)
        # append to trades log
        append_csv("data/logs/trades.csv", [datetime.utcnow().isoformat(), signal.symbol, "BUY", signal.price, "", size, ""]) 
        self._persist_state()

    def _persist_state(self) -> None:
        p = Path("data/state/portfolio_state.json")
        p.write_text(json.dumps(self.state, indent=2, default=str))
