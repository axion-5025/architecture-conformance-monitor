from pathlib import Path

from conformance_platform.rule_engine.evaluator import (
    evaluate_layer_conformance,
)
from conformance_platform.rule_engine.loader import load_rules
from conformance_platform.scanner.python_scanner import scan_service


def test_detects_forbidden_layer_dependency(
    tmp_path: Path,
) -> None:
    service_directory = tmp_path / "order-service"
    api_file = service_directory / "app" / "api" / "orders.py"
    api_file.parent.mkdir(parents=True)

    api_file.write_text(
        (
            "from app.services.orders import create_order\n"
            "from app.repositories.orders import OrderRepository"
        ),
        encoding="utf-8",
    )

    rules = load_rules("architecture-rules/baseline.yml")
    scan_result = scan_service(
        service_name="order-service",
        source_path=service_directory,
    )

    violations = evaluate_layer_conformance(
        rules=rules,
        scan_results=[scan_result],
    )

    assert len(violations) == 1

    violation = violations[0]

    assert violation.service_name == "order-service"
    assert violation.source_layer == "api"
    assert violation.target_layer == "repositories"
    assert violation.severity.value == "high"
    assert violation.evidence_type.value == "static"
    assert violation.line == 2