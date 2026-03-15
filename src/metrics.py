"""
metrics.py
Performance metrics for evaluating the market-making simulation.
"""

import numpy as np
import pandas as pd


def sharpe_ratio(pnl_series: pd.Series, periods_per_year: int = 525600) -> float:
    """Annualized Sharpe ratio from per-bar PnL changes."""
    returns = pnl_series.diff().dropna()
    if returns.std() == 0:
        return 0.0
    return (returns.mean() / returns.std()) * np.sqrt(periods_per_year)


def max_drawdown(pnl_series: pd.Series) -> float:
    roll_max = pnl_series.cummax()
    drawdown = pnl_series - roll_max
    return drawdown.min()


def spread_capture(results: pd.DataFrame) -> float:
    """Estimated spread captured per round-trip."""
    buy_fills  = results[results["buy_fill"]]["bid"]
    sell_fills = results[results["sell_fill"]]["ask"]
    n = min(len(buy_fills), len(sell_fills))
    if n == 0:
        return 0.0
    return (sell_fills.values[:n] - buy_fills.values[:n]).mean()


def summary(results: pd.DataFrame) -> dict:
    return {
        "total_pnl":      round(results["pnl"].iloc[-1], 4),
        "sharpe":         round(sharpe_ratio(results["pnl"]), 4),
        "max_drawdown":   round(max_drawdown(results["pnl"]), 4),
        "spread_capture": round(spread_capture(results), 6),
        "total_buys":     int(results["buy_fill"].sum()),
        "total_sells":    int(results["sell_fill"].sum()),
        "peak_inventory": round(results["inventory"].abs().max(), 4),
    }
