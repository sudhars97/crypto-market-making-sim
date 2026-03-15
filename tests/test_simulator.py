"""Unit tests for simulator.py"""
import sys
import pandas as pd
import numpy as np
sys.path.insert(0, ".")
from src.simulator import run_simulation


def make_flat_df(price=50000, n=100):
    idx = pd.date_range("2024-01-01", periods=n, freq="1min")
    return pd.DataFrame({
        "close": price,
        "high":  price * 1.001,
        "low":   price * 0.999,
        "realized_vol": 0.001,
    }, index=idx)


def test_simulator_runs():
    df = make_flat_df()
    results = run_simulation(df)
    assert len(results) > 0


def test_pnl_column_exists():
    results = run_simulation(make_flat_df())
    assert "pnl" in results.columns


def test_inventory_within_limit():
    results = run_simulation(make_flat_df(), inventory_limit=0.05)
    assert results["inventory"].abs().max() <= 0.05 + 1e-9
