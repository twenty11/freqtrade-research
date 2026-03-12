from __future__ import annotations

import subprocess
from dataclasses import dataclass


@dataclass
class CommandResult:
    cmd: list[str]
    returncode: int
    stdout: str
    stderr: str


def run_command(cmd: list[str]) -> CommandResult:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return CommandResult(cmd=cmd, returncode=proc.returncode, stdout=proc.stdout, stderr=proc.stderr)
