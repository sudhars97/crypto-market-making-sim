"""
risk.py
Position limits and stop-loss rules for the simulator.
"""


def check_inventory_limit(inventory: float, inventory_limit: float,
                           side: str) -> bool:
    """
    Returns True if the proposed trade is allowed.
    side: "buy" or "sell"
    """
    if side == "buy" and inventory >= inventory_limit:
        return False
    if side == "sell" and inventory <= -inventory_limit:
        return False
    return True


def apply_stop_loss(pnl: float, stop_loss_threshold: float = -500.0) -> bool:
    """Returns True if stop-loss has been breached (trading should halt)."""
    return pnl < stop_loss_threshold
