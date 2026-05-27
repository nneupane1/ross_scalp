from __future__ import annotations

import pandas as pd
from portfolio.position import Position


class ExecutionLogic:
    def should_enter(self, signal) -> bool:
        return True

    def should_exit(self, position: Position, df: pd.DataFrame) -> bool:
        if df is None or df.empty:
            return False

        last = df.iloc[-1]
        if position.stop is not None and last["close"] <= position.stop:
            return True

        if last["close"] < last["open"]:
            if len(df) >= 3:
                prev = df.iloc[-2]
                if prev["close"] < prev["open"]:
                    return True

        if position.entry_price > 0:
            profit_pct = (last["close"] - position.entry_price) / position.entry_price * 100
            if profit_pct >= 1.5 and last["close"] < df.iloc[-2]["close"]:
                return True

        return False
