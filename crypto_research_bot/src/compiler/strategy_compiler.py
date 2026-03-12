from __future__ import annotations

import json
from pathlib import Path

from compiler.config_compiler import compile_runtime_config
from compiler.indicator_compiler import compile_indicators
from compiler.protection_compiler import compile_protections
from compiler.signal_compiler import compile_signal
from compiler.template_renderer import render_strategy, write_text
from domain.models.strategy_spec import StrategySpec
from domain.services.strategy_hasher import sha256_text


def compile_strategy(spec: StrategySpec, out_dir: str | Path) -> dict[str, str]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)

    indicator_lines = compile_indicators(spec.indicators)
    enter_lines = compile_signal(spec.signals.enter_long, "enter_long", "enter_tag")
    exit_lines = []
    if spec.signals.exit_long:
        exit_lines.extend(compile_signal(spec.signals.exit_long, "exit_long"))

    strategy_code = render_strategy(
        class_name="CompiledStrategy",
        timeframe=spec.market.timeframe,
        can_short=str(spec.market.can_short),
        startup_candle_count=spec.data.startup_candle_count,
        minimal_roi={"0": 0.02},
        stoploss=-0.1,
        protections=compile_protections(spec.protections),
        indicator_lines=indicator_lines,
        enter_lines=enter_lines,
        exit_lines=exit_lines,
    )
    strategy_path = out / "CompiledStrategy.py"
    write_text(strategy_path, strategy_code)

    runtime_config = compile_runtime_config(spec)
    runtime_path = out / "runtime_config.json"
    write_text(runtime_path, json.dumps(runtime_config, ensure_ascii=False, indent=2))

    compiled_meta = {
        "strategy_id": spec.meta.get("strategy_id", "unknown"),
        "compiled_strategy_hash": sha256_text(strategy_code),
        "runtime_config_hash": sha256_text(json.dumps(runtime_config, sort_keys=True)),
    }
    meta_path = out / "compiled_meta.json"
    write_text(meta_path, json.dumps(compiled_meta, ensure_ascii=False, indent=2))

    manifest = {"artifacts": [str(strategy_path), str(runtime_path), str(meta_path)]}
    manifest_path = out / "manifest.json"
    write_text(manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2))

    return {
        "strategy": str(strategy_path),
        "runtime": str(runtime_path),
        "meta": str(meta_path),
        "manifest": str(manifest_path),
    }
