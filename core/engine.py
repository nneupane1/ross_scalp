"""Engine wires scanner -> strategy -> portfolio for a single cycle."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import List

from scanner.watchlist_manager import WatchlistManager
from data_layer.candle_store import CandleStore
from strategy.breakout import BreakoutStrategy
from strategy.execution_logic import ExecutionLogic
from portfolio.portfolio_manager import PortfolioManager
from risk.risk_manager import RiskManager
from utils.logging_utils import append_csv


class Engine:
    def __init__(self, config: dict | None = None) -> None:
        self.watchlist_manager = WatchlistManager()
        self.candle_store = CandleStore()
        self.strategy = BreakoutStrategy()
        self.exec_logic = ExecutionLogic()
        self.portfolio = PortfolioManager()
        self.risk = RiskManager()
        self.watchlist: List[str] = []
        self.last_watchlist_refresh = datetime.min
        self.refresh_interval = timedelta(minutes=5)

    def _refresh_watchlist_if_needed(self) -> List[str]:
        if datetime.utcnow() - self.last_watchlist_refresh > self.refresh_interval or not self.watchlist:
            self.watchlist = self.watchlist_manager.build_watchlist()
            self.last_watchlist_refresh = datetime.utcnow()
            append_csv("data/logs/performance.csv", [datetime.utcnow().isoformat(), "watchlist_refresh", len(self.watchlist), ""])
        return self.watchlist

    def run_cycle(self) -> None:
        symbols = self._refresh_watchlist_if_needed()
        for symbol in symbols:
            df = self.candle_store.update_latest(symbol)
            if df is None or df.empty:
                continue

            for position in list(self.portfolio.positions):
                if position.symbol != symbol:
                    continue
                if self.exec_logic.should_exit(position, df):
                    self.portfolio.exit_position(position, float(df.iloc[-1]["close"]))

            sig = self.strategy.check_breakout(symbol, df)
            if sig and self.risk.can_take_trade(self.portfolio, sig):
                stop_price = float(sig.meta.get("recent_low", sig.meta.get("recent_high", 0) * 0.99)) if sig.meta else None
                size = self.risk.size_for_trade(self.portfolio, sig.price, stop_price)
                if size > 0 and self.exec_logic.should_enter(sig):
                    append_csv("data/logs/signals.csv", [datetime.utcnow().isoformat(), sig.symbol, sig.type, sig.price, sig.meta or {}])
                    self.portfolio.execute_trade(sig, size, stop_price)


if __name__ == "__main__":
    e = Engine()
    e.run_cycle()
