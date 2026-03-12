from __future__ import annotations

from pathlib import Path

from dsl.parser import read_json


REQUIRED_TOP_LEVEL = [
    "version",
    "meta",
    "market",
    "data",
    "features",
    "indicators",
    "signals",
    "risk",
    "validation",
    "reporting",
]


def validate_schema(strategy_path: str | Path, schema_path: str | Path | None = None) -> list[str]:
    _ = schema_path
    data = read_json(strategy_path)
    errors: list[str] = []
    for key in REQUIRED_TOP_LEVEL:
        if key not in data:
            errors.append(f"/{key}: missing required field")

    market = data.get("market", {})
    if market.get("exchange") != "okx":
        errors.append("/market/exchange: must be okx")
    if market.get("trading_mode") not in {"spot", "futures"}:
        errors.append("/market/trading_mode: must be spot or futures")

    return errors
