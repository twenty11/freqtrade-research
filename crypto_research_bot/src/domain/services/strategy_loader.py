"""Load and parse strategy json into domain model."""

from __future__ import annotations

import json
from pathlib import Path

from domain.models.strategy_spec import (
    DataConfig,
    ExternalFeature,
    FeatureAlignment,
    Features,
    Indicator,
    Market,
    Reporting,
    Risk,
    Rule,
    SignalBlock,
    Signals,
    StrategySpec,
    Universe,
    Validation,
)


def _parse_signal_block(data: dict | None) -> SignalBlock | None:
    if data is None:
        return None
    return SignalBlock(
        logic=data.get("logic", "all"),
        rules=[Rule(**r) for r in data.get("rules", [])],
        tag=data.get("tag"),
    )


def load_strategy(path: str | Path) -> StrategySpec:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    market = Market(
        exchange=data["market"]["exchange"],
        trading_mode=data["market"]["trading_mode"],
        timeframe=data["market"]["timeframe"],
        can_short=data["market"]["can_short"],
        universe=Universe(**data["market"]["universe"]),
        margin_mode=data["market"].get("margin_mode"),
        informative_timeframes=data["market"].get("informative_timeframes", []),
    )
    dcfg = data["data"]
    cfg = DataConfig(
        startup_candle_count=dcfg["startup_candle_count"],
        timerange_default=dcfg.get("timerange_default"),
        price_source=dcfg.get("price_source", "ohlcv"),
        feature_alignment=FeatureAlignment(**dcfg["feature_alignment"]),
    )
    feats = Features(external=[ExternalFeature(**f) for f in data["features"].get("external", [])])
    indicators = [Indicator(**i) for i in data.get("indicators", [])]
    sigs = data["signals"]
    signals = Signals(
        enter_long=_parse_signal_block(sigs.get("enter_long")),
        enter_short=_parse_signal_block(sigs.get("enter_short")),
        exit_long=_parse_signal_block(sigs.get("exit_long")),
        exit_short=_parse_signal_block(sigs.get("exit_short")),
    )
    return StrategySpec(
        version=data["version"],
        meta=data["meta"],
        market=market,
        data=cfg,
        features=feats,
        indicators=indicators,
        signals=signals,
        risk=Risk(**data.get("risk", {})),
        protections=data.get("protections", []),
        optimization=data.get("optimization", {}),
        validation=Validation(**data.get("validation", {})),
        reporting=Reporting(**data.get("reporting", {})),
    )
