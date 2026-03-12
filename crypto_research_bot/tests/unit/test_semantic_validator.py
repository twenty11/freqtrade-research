from domain.services.strategy_loader import load_strategy
from dsl.semantic_validator import validate_semantics


def test_spot_semantic_rules():
    spec = load_strategy("templates/trend_spot.json")
    errors = validate_semantics(spec)
    assert errors == []
