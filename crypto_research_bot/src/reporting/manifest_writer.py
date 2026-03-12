from __future__ import annotations

import json
from pathlib import Path

from domain.services.strategy_hasher import sha256_file, sha256_text


def write_manifest(path: str, strategy_json: str, compiled_strategy: str, extra: dict) -> None:
    payload = {
        "strategy_json_hash": sha256_file(strategy_json),
        "compiled_strategy_hash": sha256_file(compiled_strategy),
        "extra_hash": sha256_text(json.dumps(extra, sort_keys=True)),
        "extra": extra,
    }
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
