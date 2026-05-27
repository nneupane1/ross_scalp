from __future__ import annotations

import yaml
from pathlib import Path

from portfolio.portfolio_manager import PortfolioManager
from strategy.signal import Signal


class RiskManager:
    def __init__(self):
        cfg = yaml.safe_load(Path("config/risk.yaml").read_text())
        self.account_size = cfg.get("account_size", 25000)
        self.risk_per_trade = cfg.get("risk_per_trade_pct", 0.3) / 100.0

    def can_take_trade(self, portfolio: PortfolioManager, signal: Signal) -> bool:
        # Very simple check: ensure we have cash
        cash = portfolio.state.get("cash", 0)
        return cash > 100  # minimum availability
