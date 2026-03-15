"""
pricing.py
Quote pricing rule: computes bid/ask quotes around mid price.
Inspired by Avellaneda-Stoikov framework (simplified).
"""

import numpy as np


def compute_spread(realized_vol: float, spread_base: float = 0.0002,
                   vol_multiplier: float = 5.0) -> float:
    """Spread widens with realized volatility."""
    return spread_base + vol_multiplier * realized_vol


def skew_mid(mid: float, inventory: float, inventory_limit: float,
             skew_factor: float = 0.5, realized_vol: float = 0.0) -> float:
    """
    Shift the quoted mid away from inventory direction.
    Long inventory → lower the quoted mid (want to sell more).
    Short inventory → raise the quoted mid (want to buy more).
    """
    inventory_ratio = inventory / (inventory_limit + 1e-9)
    skew = -skew_factor * inventory_ratio * mid * realized_vol
    return mid + skew


def compute_quotes(mid: float, inventory: float, realized_vol: float,
                   spread_base: float = 0.0002, vol_multiplier: float = 5.0,
                   inventory_limit: float = 0.05, skew_factor: float = 0.5):
    """
    Returns (bid, ask) prices given market conditions and current inventory.
    """
    spread = compute_spread(realized_vol, spread_base, vol_multiplier)
    adjusted_mid = skew_mid(mid, inventory, inventory_limit,
                            skew_factor, realized_vol)
    bid = adjusted_mid * (1 - spread / 2)
    ask = adjusted_mid * (1 + spread / 2)
    return round(bid, 2), round(ask, 2)
