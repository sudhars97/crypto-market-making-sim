"""
simulator.py
Event-loop market-making simulator over OHLCV bar data.
"""

import pandas as pd
import numpy as np
from src.pricing import compute_quotes
from src.risk import check_inventory_limit, apply_stop_loss


def run_simulation(df: pd.DataFrame, spread_base: float = 0.0002,
                   vol_multiplier: float = 5.0, inventory_limit: float = 0.05,
                   skew_factor: float = 0.5, fee_rate: float = 0.0001,
                   stop_loss: float = -500.0) -> pd.DataFrame:
    """
    Simulate market-making over a bar DataFrame.
    Assumes df has columns: close, high, low, realized_vol (from features.py).
    Returns a DataFrame of per-bar simulation results.
    """
    records = []
    inventory = 0.0
    cash = 0.0

    for ts, row in df.iterrows():
        mid = row["close"]
        vol  = row.get("realized_vol", 0.001)

        bid, ask = compute_quotes(
            mid, inventory, vol,
            spread_base, vol_multiplier,
            inventory_limit, skew_factor
        )

        buy_fill  = row["low"]  <= bid
        sell_fill = row["high"] >= ask

        if buy_fill and check_inventory_limit(inventory, inventory_limit, "buy"):
            inventory += 1.0
            cash -= bid * (1 + fee_rate)

        if sell_fill and check_inventory_limit(inventory, inventory_limit, "sell"):
            inventory -= 1.0
            cash += ask * (1 - fee_rate)

        mark_to_market = cash + inventory * mid
        if apply_stop_loss(mark_to_market, stop_loss):
            print(f"  [stop-loss] triggered at {ts}, PnL={mark_to_market:.2f}")
            break

        records.append({
            "timestamp": ts,
            "mid": mid,
            "bid": bid,
            "ask": ask,
            "inventory": inventory,
            "cash": cash,
            "pnl": mark_to_market,
            "buy_fill": buy_fill,
            "sell_fill": sell_fill,
        })

    return pd.DataFrame(records).set_index("timestamp")
