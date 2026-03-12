from compiler.strategy_compiler import compile_strategy
from domain.services.strategy_loader import load_strategy
from dsl.semantic_validator import validate_semantics
from dsl.validator import validate_schema


def test_validate_compile_pipeline(tmp_path):
    assert validate_schema("templates/trend_spot.json", "src/dsl/schema/strategy.schema.json") == []
    spec = load_strategy("templates/trend_spot.json")
    assert validate_semantics(spec) == []
    artifacts = compile_strategy(spec, tmp_path)
    assert "strategy" in artifacts
