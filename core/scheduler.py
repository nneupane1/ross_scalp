"""Minimal scheduler helper for timing and refresh intervals."""
import yaml
from pathlib import Path


def load_system_config() -> dict:
    p = Path("config/system.yaml")
    if not p.exists():
        return {}
    return yaml.safe_load(p.read_text())
