# ross_momentum_system

## Project Story

This project is not simply a trading bot. It is a systematic replication of the behavior of a Ross Cameron-style momentum trader. The purpose of this system is not to predict the market or model long-term outcomes. It is to answer one practical question repeatedly:

> Where is attention and liquidity flowing right now, and can the system join that flow early enough to capture a small but reliable piece of the move?

The system translates that human trading process into a modular architecture that stays fast, focused, and disciplined.

## Table of Contents

- [Project Story](#project-story)
- [How It Works](#how-it-works)
- [Repository Structure](#repository-structure)
- [Component Details](#component-details)
- [Run Instructions](#run-instructions)
- [Logging and State](#logging-and-state)
- [Design Philosophy](#design-philosophy)
- [Next Steps](#next-steps)

## How It Works

The system follows a single continuous loop:

1. **Scan** the Binance market universe for currently active movers.
2. **Select** a small watchlist of 5–10 symbols that are still moving now.
3. **Monitor** those symbols on the 1-minute timeframe.
4. **Trade** when price breaks out of recent compression with momentum.
5. **Evaluate** exits immediately when the move stalls, reverses, or reaches a quick profit.

This flow mirrors Ross-style trading: it does not pretend to be right all the time. It trades the early phase of real momentum, accepts that false signals are part of the game, and relies on fast execution and consistent record-keeping.

## Repository Structure

```text
ross_momentum_system/

├── README.md
├── requirements.txt
├── .env
│
├── config/
│   ├── system.yaml
│   ├── strategy.yaml
│   ├── risk.yaml
│
├── data/
│   ├── cache/
│   │   ├── candles/
│   │   └── snapshots/
│   │
│   ├── logs/
│   │   ├── trades.csv
│   │   ├── signals.csv
│   │   └── performance.csv
│   │
│   └── state/
│       └── portfolio_state.json
│
├── core/
│   ├── engine.py
│   ├── event_loop.py
│   └── scheduler.py
│
├── data_layer/
│   ├── binance_client.py
│   ├── market_stream.py
│   ├── market_snapshot.py
│   └── candle_store.py
│
├── scanner/
│   ├── top_gainers.py
│   ├── momentum_filter.py
│   └── watchlist_manager.py
│
├── strategy/
│   ├── breakout.py
│   ├── signal.py
│   └── execution_logic.py
│
├── portfolio/
│   ├── portfolio_manager.py
│   ├── position.py
│   ├── trade.py
│   └── pnl_calculator.py
│
├── risk/
│   ├── risk_manager.py
│   └── rules.py
│
├── utils/
│   ├── time_utils.py
│   ├── logging_utils.py
│   └── math_utils.py
│
├── run/
│   └── run_paper_trading.py
│
├── main.py
└── notebooks/
    └── analysis.ipynb
```

## Component Details

### `config/`

| File | Purpose |
|---|---|
| `system.yaml` | Controls session windows, scanner refresh rhythm, and candle history depth. |
| `strategy.yaml` | Defines breakout lookback, momentum thresholds, and move filters. |
| `risk.yaml` | Contains account size, risk-per-trade sizing, daily limits, and discipline rules. |

### `data_layer/`

| File | Purpose |
|---|---|
| `binance_client.py` | Fetches Binance tickers and candle data via REST calls. |
| `market_stream.py` | Provides polling-based candle updates and optional websocket streaming. |
| `market_snapshot.py` | Builds snapshots such as top gainers and volume metrics. |
| `candle_store.py` | Keeps recent candle history in memory for fast access and rolling updates. |

### `scanner/`

| File | Purpose |
|---|---|
| `top_gainers.py` | Pulls the highest-momentum symbols from Binance. |
| `momentum_filter.py` | Filters symbols based on recent volume and price move, not just 24h performance. |
| `watchlist_manager.py` | Builds the active watchlist and narrows the universe to the true in-play symbols. |

### `strategy/`

| File | Purpose |
|---|---|
| `breakout.py` | Detects breakouts against recent highs and captures breakout context. |
| `signal.py` | Defines the signal object used across the engine. |
| `execution_logic.py` | Implements fast Ross-style exits and trade behavior. |

### `portfolio/`

| File | Purpose |
|---|---|
| `portfolio_manager.py` | Executes paper trades, tracks open positions, and logs all activity. |
| `position.py` | Represents an open position with entry, size, stop, and symbol. |
| `trade.py` | Stores trade history including PnL and timestamps. |
| `pnl_calculator.py` | Computes simple profit-and-loss values. |

### `risk/`

| File | Purpose |
|---|---|
| `risk_manager.py` | Decides whether a trade is valid and sizes positions based on risk. |
| `rules.py` | Holds structured risk rule objects for extension. |

### `core/`

| File | Purpose |
|---|---|
| `engine.py` | Orchestrates watchlist refresh, candle updates, breakout detection, and position management. |
| `event_loop.py` | Runs the live loop during active session windows. |
| `scheduler.py` | Loads system configuration and supports session timing. |

### `utils/`

| File | Purpose |
|---|---|
| `time_utils.py` | Determines whether the current time is within London or New York sessions. |
| `logging_utils.py` | Writes structured CSV logs for signals, trades, and performance. |
| `math_utils.py` | Provides small helper functions like percent change. |

### `run/`

| File | Purpose |
|---|---|
| `run_paper_trading.py` | Launches a single cycle run for testing and debugging. |

### `main.py`

| File | Purpose |
|---|---|
| `main.py` | The single entrypoint that starts the live trading loop. |

## Run Instructions

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the live system:

```bash
python main.py
```

3. Run a single test cycle:

```bash
python run/run_paper_trading.py
```

## Logging and State

The system persists logs and state to the `data/` folder:

- `data/logs/trades.csv`: every trade entry and exit.
- `data/logs/signals.csv`: every breakout signal generated.
- `data/logs/performance.csv`: engine and refresh activity. |
- `data/state/portfolio_state.json`: current cash, equity, and position state.

## Design Philosophy

This system is built around the idea that momentum trading is a reactive process, not a predictive model.

- **Attention over prediction**: It uses Top Gainers and recent momentum to focus on assets others are already trading.
- **Session awareness**: It only trades during high-liquidity periods aligned with London and New York windows.
- **Watchlist focus**: It narrows the market to a small set of active symbols, just like a human trader would.
- **Fast execution**: It enters on breakouts and exits quickly if momentum stalls or reverses.
- **Evidence generation**: Every trade is stored as data so the system can be improved with actual results.

## Next Steps

To evolve this system further:

- Add more granular session definitions and market awareness.
- Refine watchlist filtering with breakout volume clusters.
- Improve exit logic with trailing rules or multi-stage profit-taking.
- Add more detailed performance analytics in `notebooks/analysis.ipynb`.

---

This README now captures the full story, architecture, and why this project is designed this way.
