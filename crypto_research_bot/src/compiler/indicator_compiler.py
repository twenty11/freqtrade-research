from __future__ import annotations

from domain.models.strategy_spec import Indicator


def compile_indicators(indicators: list[Indicator]) -> list[str]:
    lines: list[str] = []
    for ind in indicators:
        src = ind.source or "close"
        if ind.type == "ema":
            lines.append(f"dataframe['{ind.id}'] = dataframe['{src}'].ewm(span={ind.params.get('period', 14)}).mean()")
        elif ind.type == "rsi":
            lines.append("delta = dataframe['close'].diff()")
            lines.append("up = delta.clip(lower=0).rolling(14).mean()")
            lines.append("down = (-delta.clip(upper=0)).rolling(14).mean()")
            lines.append(f"dataframe['{ind.id}'] = 100 - (100 / (1 + (up / down)))")
        else:
            lines.append(f"# TODO unsupported indicator type: {ind.type}")
    return lines
