from __future__ import annotations

from pathlib import Path


def run_dir(run_id: str) -> Path:
    return Path("data/reports") / run_id
