from __future__ import annotations

def calc_pnl(entry_price: float, exit_price: float, size: float) -> float:
    return (exit_price - entry_price) * size
