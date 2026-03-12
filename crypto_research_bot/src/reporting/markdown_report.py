from __future__ import annotations

from pathlib import Path


def write_summary(path: str, summary: dict) -> None:
    lines = [
        "# Research Summary",
        f"- accepted: {summary.get('accepted')}",
        f"- profit_factor: {summary.get('metrics', {}).get('profit_factor')}",
        f"- max_drawdown: {summary.get('metrics', {}).get('max_drawdown')}",
        f"- lookahead_passed: {summary.get('lookahead_passed')}",
        f"- recursive_passed: {summary.get('recursive_passed')}",
    ]
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(lines), encoding="utf-8")
