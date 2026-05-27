"""Small runner to validate the Binance client quickly.

Usage:
    python run/run_paper_trading.py
"""
from core.engine import Engine


def main():
    engine = Engine()
    engine.run_cycle()


if __name__ == "__main__":
    main()
