from __future__ import annotations

from pathlib import Path
import csv


def append_csv(path: str, row: list[str]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)
