"""
features.py
Computes features used by the pricing and simulation modules.
"""

import numpy as np
import pandas as pd


def add_log_returns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["log_return"] = np.log(df["close"] / df["close"].shift(1))
    return df


def add_realized_vol(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    df = df.copy()
    df["realized_vol"] = df["log_return"].rolling(window).std()
    return df


def add_volume_imbalance(df: pd.DataFrame) -> pd.DataFrame:
    """Taker buy volume / total volume — proxy for order-flow pressure."""
    df = df.copy()
    df["vol_imbalance"] = df["taker_buy_base_vol"] / (df["volume"] + 1e-9)
    return df


def add_momentum(df: pd.DataFrame, window: int = 5) -> pd.DataFrame:
    df = df.copy()
    df["momentum"] = df["close"].pct_change(window)
    return df


def build_features(df: pd.DataFrame, vol_window: int = 20) -> pd.DataFrame:
    df = add_log_returns(df)
    df = add_realized_vol(df, window=vol_window)
    df = add_volume_imbalance(df)
    df = add_momentum(df)
    return df.dropna()
