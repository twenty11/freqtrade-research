from dsl.validator import validate_schema


def test_schema_validation_passes_template():
    errors = validate_schema("templates/trend_spot.json", "src/dsl/schema/strategy.schema.json")
    assert errors == []
