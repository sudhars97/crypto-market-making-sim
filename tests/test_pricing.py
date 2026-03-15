"""Unit tests for pricing.py"""
import sys
sys.path.insert(0, ".")
from src.pricing import compute_spread, compute_quotes


def test_spread_increases_with_vol():
    low_spread  = compute_spread(0.001)
    high_spread = compute_spread(0.01)
    assert high_spread > low_spread


def test_spread_minimum_is_base():
    spread = compute_spread(0.0, spread_base=0.0002)
    assert spread == 0.0002


def test_quotes_bid_below_ask():
    bid, ask = compute_quotes(mid=50000, inventory=0, realized_vol=0.001)
    assert bid < ask


def test_long_inventory_lowers_bid():
    bid_neutral, _ = compute_quotes(50000, inventory=0,    realized_vol=0.001)
    bid_long,    _ = compute_quotes(50000, inventory=0.04, realized_vol=0.001,
                                    inventory_limit=0.05)
    assert bid_long < bid_neutral
