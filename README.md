# Crypto Market-Making Simulator

A quantitative research project simulating a **market-making strategy on BTC/USDT** using Binance public 1-minute OHLCV data.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sudhars97/crypto-market-making-sim/blob/main/notebooks/04_simulation.ipynb)

---

## Problem

Market makers earn the bid-ask spread by continuously quoting both sides of a market.
The core challenge: how do you price your quotes to capture spread while managing inventory risk?

## Approach

1. **Data:** Binance 1-minute spot OHLCV for BTCUSDT (Jan–Mar 2024)
2. **Features:** Realized volatility, volume imbalance, short-term momentum
3. **Pricing rule:** Avellaneda-Stoikov inspired model — spread widens with volatility, quotes skew with inventory
4. **Simulator:** Bar-by-bar event loop with fill logic, fees, and stop-loss
5. **Evaluation:** Sharpe ratio, max drawdown, spread capture, inventory profile

## Key Results

| Metric | Primary (Jan–Mar 2024) | Stress (Nov 2022 FTX) |
|--------|----------------------|----------------------|
| Total PnL | $-383.28 | $-89,850.77 |
| Sharpe Ratio | -58.731 | -51.750 |
| Max Drawdown | $-458.66 | $-89,871.96 |
| Spread Capture | -780040.00 bps | -648132.62 bps |
| Total Buy Fills | 5 | 1,359 |
| Total Sell Fills | 6 | 1,358 |
| Peak Inventory | 1.0000 BTC | 1.0000 BTC |

> **Stress finding:** During the FTX collapse (Nov 2022), the default stop-loss of $-500
> triggered within ~8 hours, halting execution. Stress results above use stop-loss disabled
> to study full-period behaviour. This highlights the need for dynamic stop-loss
> calibration under regime-change events.

## Repo Structure

| Folder | Contents |
|--------|----------|
| `notebooks/` | Step-by-step Jupyter notebooks |
| `src/` | Reusable Python modules (data, features, pricing, simulator, metrics) |
| `config/` | YAML experiment config |
| `tests/` | Unit tests |
| `data/` | Sample data only (see data/README.md for download instructions) |

## How to Run

**Option 1 — Google Colab (recommended):**
Click the 'Open in Colab' badge above and run `04_simulation.ipynb`.

**Option 2 — Locally:**

    git clone https://github.com/sudhars97/crypto-market-making-sim
    cd crypto-market-making-sim
    pip install -r requirements.txt
    jupyter notebook

## Data Attribution
Market data sourced from [Binance Public Data](https://github.com/binance/binance-public-data). Raw files are not redistributed. See [DATA_SOURCES.md](./DATA_SOURCES.md).

## License
MIT
