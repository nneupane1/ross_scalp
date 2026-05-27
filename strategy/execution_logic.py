from __future__ import annotations

from strategy.signal import Signal


class ExecutionLogic:
    def should_enter(self, signal: Signal) -> bool:
        return True

    def should_exit(self, position, df) -> bool:
        # Placeholder for exit logic: profit target or stall
        return False
