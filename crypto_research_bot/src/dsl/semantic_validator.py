from __future__ import annotations

from domain.models.strategy_spec import StrategySpec


def validate_semantics(spec: StrategySpec) -> list[str]:
    errors: list[str] = []
    indicator_ids = {i.id for i in spec.indicators}
    feature_ids = {f.id for f in spec.features.external}

    if spec.market.trading_mode == "spot" and spec.market.can_short:
        errors.append("spot mode cannot set can_short=true")
    if spec.market.trading_mode == "spot" and spec.risk.leverage:
        errors.append("spot mode cannot set leverage")

    allowed = indicator_ids | feature_ids
    signal_blocks = {
        "enter_long": spec.signals.enter_long,
        "enter_short": spec.signals.enter_short,
        "exit_long": spec.signals.exit_long,
        "exit_short": spec.signals.exit_short,
    }
    for name, block in signal_blocks.items():
        if block is None:
            continue
        for rule in block.rules:
            if rule.left not in allowed:
                errors.append(f"signal {name} references unknown left operand: {rule.left}")
            if isinstance(rule.right, str) and rule.right not in allowed:
                errors.append(f"signal {name} references unknown right operand: {rule.right}")

    for ext in spec.features.external:
        if "candle_close_time" not in ext.join_keys:
            errors.append(f"external feature {ext.id} must include candle_close_time in join_keys")

    return errors
