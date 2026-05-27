"""Engine wires scanner -> strategy -> portfolio for a single cycle."""
from __future__ import annotations

from typing import List

from scanner.watchlist_manager import WatchlistManager
from data_layer.candle_store import CandleStore
from strategy.breakout import BreakoutStrategy
from portfolio.portfolio_manager import PortfolioManager
from risk.risk_manager import RiskManager
from utils.logging_utils import append_csv
from datetime import datetime


class Engine:
    def __init__(self, config: dict | None = None) -> None:
        self.watchlist_manager = WatchlistManager()
        self.candle_store = CandleStore()
        self.strategy = BreakoutStrategy()
        self.portfolio = PortfolioManager()
        self.risk = RiskManager()

    def run_cycle(self) -> None:
        symbols = self.watchlist_manager.build_watchlist()
        candles = {s: self.candle_store.get_recent(s) for s in symbols}

        for symbol, df in candles.items():
            if df is None or df.empty:
                continue
            sig = self.strategy.check_breakout(symbol, df)
            if sig and self.risk.can_take_trade(self.portfolio, sig):
                # log signal
                append_csv("data/logs/signals.csv", [datetime.utcnow().isoformat(), sig.symbol, sig.type, sig.price, sig.meta or {}])
                self.portfolio.execute_trade(sig)


if __name__ == "__main__":
    e = Engine()
    e.run_cycle()
