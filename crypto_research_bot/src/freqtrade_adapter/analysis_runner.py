from __future__ import annotations

from freqtrade_adapter.commands import lookahead_cmd, recursive_cmd
from utils.subprocess import CommandResult, run_command


def run_lookahead(config: str, strategy: str) -> CommandResult:
    return run_command(lookahead_cmd(config=config, strategy=strategy))


def run_recursive(config: str, strategy: str) -> CommandResult:
    return run_command(recursive_cmd(config=config, strategy=strategy))
