from __future__ import annotations


def backtest_cmd(config: str, strategy: str, timerange: str | None = None) -> list[str]:
    cmd = ["freqtrade", "backtesting", "-c", config, "--strategy-path", strategy.rsplit('/', 1)[0], "-s", "CompiledStrategy", "--enable-protections", "--export", "trades"]
    if timerange:
        cmd.extend(["--timerange", timerange])
    return cmd


def lookahead_cmd(config: str, strategy: str) -> list[str]:
    return ["freqtrade", "lookahead-analysis", "-c", config, "--strategy-path", strategy.rsplit('/', 1)[0], "-s", "CompiledStrategy"]


def recursive_cmd(config: str, strategy: str) -> list[str]:
    return ["freqtrade", "recursive-analysis", "-c", config, "--strategy-path", strategy.rsplit('/', 1)[0], "-s", "CompiledStrategy"]
