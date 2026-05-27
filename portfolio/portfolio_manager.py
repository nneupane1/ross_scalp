from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import List

from portfolio.position import Position
from strategy.signal import Signal
from portfolio.trade import Trade
from portfolio.pnl_calculator import calc_pnl
from utils.logging_utils import append_csv


class PortfolioManager:
    def __init__(self):
        p = Path("data/state/portfolio_state.json")
        if p.exists():
            self.state = json.loads(p.read_text())
        else:
            self.state = {"equity": 25000, "cash": 25000, "positions": []}
        self.positions: List[Position] = []
        self.trades: List[Trade] = []

    def execute_trade(self, signal: Signal, size: float, stop_price: float | None = None) -> None:
        cash = self.state.get("cash", 0)
        if size <= 0 or cash <= 0:
            return
        cost = size * signal.price
        if cost > cash:
            size = cash / signal.price
            cost = size * signal.price
        pos = Position(symbol=signal.symbol, entry_price=signal.price, size=size, stop=stop_price)
        self.positions.append(pos)
        self.state["cash"] = cash - cost
        trade = Trade(symbol=signal.symbol, entry_time=signal.time, exit_time=None, entry_price=signal.price, exit_price=None, size=size)
        self.trades.append(trade)
        append_csv("data/logs/trades.csv", [datetime.utcnow().isoformat(), signal.symbol, "BUY", signal.price, "", size, "0"])
        self._persist_state()

    def exit_position(self, position: Position, exit_price: float) -> None:
        matching = next((t for t in self.trades if t.symbol == position.symbol and t.exit_time is None and abs(t.entry_price - position.entry_price) < 1e-9), None)
        if matching:
            matching.exit_time = datetime.utcnow()
            matching.exit_price = exit_price
            matching.pnl = calc_pnl(matching.entry_price, exit_price, matching.size)
        try:
            self.positions.remove(position)
        except ValueError:
            pass
        self.state["cash"] = self.state.get("cash", 0) + position.size * exit_price
        self.state["equity"] = self.state.get("cash", 0)
        append_csv("data/logs/trades.csv", [datetime.utcnow().isoformat(), position.symbol, "SELL", position.entry_price, exit_price, position.size, matching.pnl if matching else ""])  # type: ignore
        self._persist_state()

    def _persist_state(self) -> None:
        p = Path("data/state/portfolio_state.json")
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(self.state, indent=2, default=str))
