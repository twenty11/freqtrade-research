from __future__ import annotations


def check_acceptance(metrics: dict, min_trades: int, min_profit_factor: float = 1.0) -> dict:
    return {
        "passed": metrics.get("trade_count", 0) >= min_trades and metrics.get("profit_factor", 0) >= min_profit_factor,
        "reasons": [],
    }
