from __future__ import annotations

from utils.subprocess import CommandResult, run_command


def run_hyperopt(config: str, strategy: str, epochs: int = 20) -> CommandResult:
    cmd = ["freqtrade", "hyperopt", "-c", config, "--strategy-path", strategy.rsplit('/', 1)[0], "-s", "CompiledStrategy", "--epochs", str(epochs), "--enable-protections"]
    return run_command(cmd)
