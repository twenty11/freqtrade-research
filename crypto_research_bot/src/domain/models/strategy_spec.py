"""Dataclass models for the Strategy JSON DSL."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Universe:
    mode: str
    pairs: list[str] = field(default_factory=list)
    blacklist: list[str] = field(default_factory=list)


@dataclass
class Market:
    exchange: str
    trading_mode: str
    timeframe: str
    can_short: bool
    universe: Universe
    margin_mode: str | None = None
    informative_timeframes: list[str] = field(default_factory=list)


@dataclass
class FeatureAlignment:
    join_on: list[str]
    allow_forward_fill: bool = False
    max_feature_lag_minutes: int = 0


@dataclass
class DataConfig:
    startup_candle_count: int
    feature_alignment: FeatureAlignment
    timerange_default: str | None = None
    price_source: str = "ohlcv"


@dataclass
class ExternalFeature:
    id: str
    source: str
    path: str
    column: str
    join_keys: list[str]
    time_lag_minutes: int = 0
    default: float | int | str | None = None
    allow_forward_fill: bool = False


@dataclass
class Features:
    external: list[ExternalFeature] = field(default_factory=list)


@dataclass
class Indicator:
    id: str
    type: str
    timeframe: str
    source: str | None = None
    params: dict[str, Any] = field(default_factory=dict)


@dataclass
class Rule:
    left: str
    op: str
    right: Any


@dataclass
class SignalBlock:
    logic: str = "all"
    rules: list[Rule] = field(default_factory=list)
    tag: str | None = None


@dataclass
class Signals:
    enter_long: SignalBlock
    enter_short: SignalBlock | None = None
    exit_long: SignalBlock | None = None
    exit_short: SignalBlock | None = None


@dataclass
class Risk:
    max_open_trades: int = 1
    stake: dict[str, Any] = field(default_factory=dict)
    leverage: dict[str, Any] | None = None
    stoploss: dict[str, Any] = field(default_factory=dict)
    take_profit: dict[str, Any] = field(default_factory=dict)


@dataclass
class Validation:
    require_lookahead_analysis: bool = True
    require_recursive_analysis: bool = True
    min_trades: int = 0


@dataclass
class Reporting:
    export_trades: bool = True
    export_signals: bool = True
    save_metrics_json: bool = True
    save_compiled_strategy: bool = True
    save_manifest: bool = True


@dataclass
class StrategySpec:
    version: str
    meta: dict[str, Any]
    market: Market
    data: DataConfig
    features: Features
    indicators: list[Indicator]
    signals: Signals
    risk: Risk
    protections: list[dict[str, Any]] = field(default_factory=list)
    optimization: dict[str, Any] = field(default_factory=dict)
    validation: Validation = field(default_factory=Validation)
    reporting: Reporting = field(default_factory=Reporting)
