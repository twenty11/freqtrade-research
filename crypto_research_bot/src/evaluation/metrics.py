from __future__ import annotations


def compute_basic_metrics(trade_count: int = 0) -> dict:
    return {
        "total_return": 0.0,
        "max_drawdown": 0.0,
        "win_rate": 0.0,
        "profit_factor": 0.0,
        "trade_count": trade_count,
    }
