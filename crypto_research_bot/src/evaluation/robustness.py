from __future__ import annotations


def robustness_score(metrics: dict) -> float:
    return float(metrics.get("profit_factor", 0)) - float(metrics.get("max_drawdown", 0))
