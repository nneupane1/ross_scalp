from __future__ import annotations

import yaml
from pathlib import Path

from portfolio.portfolio_manager import PortfolioManager
from strategy.signal import Signal


class RiskManager:
    def __init__(self):
        cfg = yaml.safe_load(Path("config/risk.yaml").read_text())
        self.account_size = float(cfg.get("account_size", 25000))
        self.risk_per_trade = float(cfg.get("risk_per_trade_pct", 0.3)) / 100.0
        self.daily_max_loss_pct = float(cfg.get("daily_limits", {}).get("max_loss_pct", 1.5)) / 100.0
        self.daily_max_trades = int(cfg.get("daily_limits", {}).get("max_trades", 20))
        self.min_trade_cash = 100.0

    def can_take_trade(self, portfolio: PortfolioManager, signal: Signal) -> bool:
        cash = portfolio.state.get("cash", 0)
        trades_today = len([t for t in portfolio.trades if t.entry_time.date() == signal.time.date()])
        if cash <= self.min_trade_cash:
            return False
        if trades_today >= self.daily_max_trades:
            return False
        return True

    def size_for_trade(self, portfolio: PortfolioManager, entry_price: float, stop_price: float | None) -> float:
        if stop_price is None or stop_price >= entry_price:
            return 0.0
        risk_amount = self.account_size * self.risk_per_trade
        stop_distance = entry_price - stop_price
        if stop_distance <= 0:
            return 0.0
        size = risk_amount / stop_distance
        max_affordable = portfolio.state.get("cash", 0) / entry_price
        return max(0.0, min(size, max_affordable))
