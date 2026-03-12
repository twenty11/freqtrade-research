from __future__ import annotations

from freqtrade_adapter.commands import backtest_cmd
from utils.subprocess import CommandResult, run_command


def run_backtest(config: str, strategy: str, timerange: str | None = None) -> CommandResult:
    return run_command(backtest_cmd(config=config, strategy=strategy, timerange=timerange))
