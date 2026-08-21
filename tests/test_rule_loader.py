from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from conformance_platform.rule_engine.loader import load_rules

BASELINE_PATH = Path("architecture-rules/baseline.yml")


def test_loads_valid_baseline() -> None:
    rules = load_rules(BASELINE_PATH)

    assert rules.application.name == "sample-commerce"
    assert rules.application.language == "python"
    assert len(rules.services) == 3
    assert "order-service" in rules.services


def test_rejects_unknown_service_reference(tmp_path: Path) -> None:
    invalid_rules = yaml.safe_load(
        BASELINE_PATH.read_text(encoding="utf-8")
    )

    invalid_rules["services"]["order-service"]["allowed_calls"].append(
        "unknown-service"
    )

    invalid_path = tmp_path / "invalid-rules.yml"
    invalid_path.write_text(
        yaml.safe_dump(invalid_rules),
        encoding="utf-8",
    )

    with pytest.raises(
        ValidationError,
        match="references unknown services",
    ):
        load_rules(invalid_path)


def test_rejects_shared_database_ownership(tmp_path: Path) -> None:
    invalid_rules = yaml.safe_load(
        BASELINE_PATH.read_text(encoding="utf-8")
    )

    invalid_rules["services"]["payment-service"]["database"] = "order-db"

    invalid_path = tmp_path / "shared-database.yml"
    invalid_path.write_text(
        yaml.safe_dump(invalid_rules),
        encoding="utf-8",
    )

    with pytest.raises(
        ValidationError,
        match="unique database",
    ):
        load_rules(invalid_path)


def test_rejects_unknown_fields(tmp_path: Path) -> None:
    invalid_rules = yaml.safe_load(
        BASELINE_PATH.read_text(encoding="utf-8")
    )

    invalid_rules["application"]["unexpected_field"] = "invalid"

    invalid_path = tmp_path / "unknown-field.yml"
    invalid_path.write_text(
        yaml.safe_dump(invalid_rules),
        encoding="utf-8",
    )

    with pytest.raises(ValidationError):
        load_rules(invalid_path)