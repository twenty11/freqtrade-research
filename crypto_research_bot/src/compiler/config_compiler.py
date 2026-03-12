from __future__ import annotations

from domain.models.strategy_spec import StrategySpec


def compile_runtime_config(spec: StrategySpec) -> dict:
    return {
        "exchange": {"name": spec.market.exchange},
        "trading_mode": spec.market.trading_mode,
        "margin_mode": spec.market.margin_mode,
        "pair_whitelist": spec.market.universe.pairs,
        "pair_blacklist": spec.market.universe.blacklist,
        "max_open_trades": spec.risk.max_open_trades,
        "dry_run": True,
        "db_url": "sqlite:///data/cache/research.sqlite",
        "dataformat_ohlcv": "feather",
    }
