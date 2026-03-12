from __future__ import annotations

from pathlib import Path


def render_strategy(**kwargs: object) -> str:
    indicator_lines = "\n".join(f"        {line}" for line in kwargs["indicator_lines"])
    enter_lines = "\n".join(f"        {line}" for line in kwargs["enter_lines"])
    exit_lines = "\n".join(f"        {line}" for line in kwargs["exit_lines"])
    return f'''from freqtrade.strategy.interface import IStrategy


class {kwargs["class_name"]}(IStrategy):
    timeframe = "{kwargs["timeframe"]}"
    can_short = {kwargs["can_short"]}
    startup_candle_count = {kwargs["startup_candle_count"]}
    minimal_roi = {kwargs["minimal_roi"]}
    stoploss = {kwargs["stoploss"]}
    protections = {kwargs["protections"]}

    def populate_indicators(self, dataframe, metadata):
{indicator_lines}
        return dataframe

    def populate_entry_trend(self, dataframe, metadata):
{enter_lines}
        return dataframe

    def populate_exit_trend(self, dataframe, metadata):
{exit_lines}
        return dataframe
'''


def write_text(path: str | Path, content: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(content, encoding="utf-8")
