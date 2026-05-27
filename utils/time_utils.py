from __future__ import annotations

import yaml
from datetime import datetime, time as dt_time
from pathlib import Path


def in_session(now: datetime | None = None) -> bool:
    cfg = yaml.safe_load(Path("config/system.yaml").read_text())
    if now is None:
        now = datetime.now()
    # Map sessions; compare only time portion for simplicity
    berlin = now
    sessions = cfg.get("sessions", {})
    for sess in sessions.values():
        start = dt_time.fromisoformat(sess["start"])
        end = dt_time.fromisoformat(sess["end"])
        if start <= berlin.time() <= end:
            return True
    return False
