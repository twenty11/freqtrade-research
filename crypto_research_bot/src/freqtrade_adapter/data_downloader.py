from __future__ import annotations

from utils.subprocess import CommandResult, run_command


def download_data(trading_mode: str, pairs: list[str], timerange: str, timeframes: list[str], datadir: str) -> CommandResult:
    cmd = [
        "freqtrade",
        "download-data",
        "--exchange",
        "okx",
        "--trading-mode",
        trading_mode,
        "--pairs",
        *pairs,
        "--timerange",
        timerange,
        "--timeframes",
        *timeframes,
        "--datadir",
        datadir,
        "--prepend",
    ]
    return run_command(cmd)
