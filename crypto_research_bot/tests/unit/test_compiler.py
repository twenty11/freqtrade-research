from pathlib import Path

from compiler.strategy_compiler import compile_strategy
from domain.services.strategy_loader import load_strategy


def test_compile_outputs_files(tmp_path: Path):
    spec = load_strategy("templates/trend_spot.json")
    artifacts = compile_strategy(spec, tmp_path)
    assert Path(artifacts["strategy"]).exists()
    assert Path(artifacts["runtime"]).exists()
    assert Path(artifacts["meta"]).exists()
    assert Path(artifacts["manifest"]).exists()
