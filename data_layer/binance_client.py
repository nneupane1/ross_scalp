"""Minimal Binance REST client for tickers and klines (candles).

Keep this small and dependency-light so it can be reused by scanners and stores.
"""
from __future__ import annotations

import time
from typing import Any, Dict, List

import pandas as pd
import requests


class BinanceClient:
    BASE_URL = "https://api.binance.com"

    def __init__(self, session: requests.Session | None = None) -> None:
        self.session = session or requests.Session()

    def _get(self, path: str, params: Dict[str, Any] | None = None) -> Any:
        url = f"{self.BASE_URL}{path}"
        for attempt in range(3):
            try:
                resp = self.session.get(url, params=params, timeout=10)
                resp.raise_for_status()
                return resp.json()
            except Exception:
                if attempt == 2:
                    raise
                time.sleep(0.5 * (attempt + 1))

    def get_tickers(self) -> List[Dict[str, Any]]:
        """Return the 24h ticker statistics for all symbols.

        See: GET /api/v3/ticker/24hr
        """
        return self._get("/api/v3/ticker/24hr")

    def get_top_gainers(self, top_n: int = 20, quote_asset: str = "USDT") -> List[Dict[str, Any]]:
        """Return top N gainers filtered by quote asset (default USDT).

        Each ticker dict will have numeric `priceChangePercent` and `quoteVolume` parsed.
        """
        tickers = self.get_tickers()
        filtered = [t for t in tickers if t.get("symbol", "").endswith(quote_asset)]
        for t in filtered:
            try:
                t["priceChangePercent"] = float(t.get("priceChangePercent", 0))
            except Exception:
                t["priceChangePercent"] = 0.0
            try:
                t["quoteVolume"] = float(t.get("quoteVolume", 0))
            except Exception:
                t["quoteVolume"] = 0.0
        filtered.sort(key=lambda x: x["priceChangePercent"], reverse=True)
        return filtered[:top_n]

    def get_klines(self, symbol: str, interval: str = "1m", limit: int = 100) -> pd.DataFrame:
        """Fetch klines and return a pandas.DataFrame with typed columns.

        Columns: open_time, open, high, low, close, volume, close_time, quote_asset_volume,
        num_trades, taker_base_vol, taker_quote_vol
        """
        params = {"symbol": symbol, "interval": interval, "limit": limit}
        data = self._get("/api/v3/klines", params=params)

        cols = [
            "open_time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "quote_asset_volume",
            "num_trades",
            "taker_base_vol",
            "taker_quote_vol",
            "ignore",
        ]
        df = pd.DataFrame(data, columns=cols)
        df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
        df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")
        num_cols = ["open", "high", "low", "close", "volume", "quote_asset_volume", "taker_base_vol", "taker_quote_vol"]
        df[num_cols] = df[num_cols].astype(float)
        df["num_trades"] = df["num_trades"].astype(int)
        return df


if __name__ == "__main__":
    # Quick manual test when executed directly
    client = BinanceClient()
    top = client.get_top_gainers(top_n=5)
    print("Top 5 USDT gainers:")
    for t in top:
        print(f"{t['symbol']:12} {t['priceChangePercent']:7.2f}% vol={t['quoteVolume']:.0f}")
