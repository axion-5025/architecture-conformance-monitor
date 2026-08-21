import json
import sys
from pathlib import Path

import pytest
import yaml

from conformance_platform.cli import main, run_scan


def _create_invalid_project(
    tmp_path: Path,
) -> tuple[Path, Path]:
    service_directory = tmp_path / "order-service"
    api_file = service_directory / "app" / "api" / "orders.py"
    api_file.parent.mkdir(parents=True)

    api_file.write_text(
        "from app.repositories.orders import OrderRepository",
        encoding="utf-8",
    )

    baseline_path = Path("architecture-rules/baseline.yml")
    rules = yaml.safe_load(
        baseline_path.read_text(encoding="utf-8")
    )

    order_rule = rules["services"]["order-service"]
    order_rule["source_path"] = str(service_directory)
    order_rule["allowed_calls"] = []
    rules["services"] = {"order-service": order_rule}

    rules_path = tmp_path / "rules.yml"
    rules_path.write_text(
        yaml.safe_dump(rules),
        encoding="utf-8",
    )

    output_path = tmp_path / "report.json"
    return rules_path, output_path


def test_run_scan_reports_blocking_violation(
    tmp_path: Path,
) -> None:
    rules_path, output_path = _create_invalid_project(tmp_path)

    report, has_blocking_violations = run_scan(
        rules_path=rules_path,
        output_path=output_path,
    )

    assert has_blocking_violations is True
    assert report["summary"]["services_scanned"] == 1
    assert report["summary"]["dependencies_found"] == 1
    assert report["summary"]["violations_found"] == 1
    assert output_path.is_file()

    saved_report = json.loads(
        output_path.read_text(encoding="utf-8")
    )

    violation = saved_report["violations"][0]

    assert violation["violation_type"] == "layer_violation"
    assert violation["severity"] == "high"
    assert violation["source_layer"] == "api"
    assert violation["target_layer"] == "repositories"


def test_cli_returns_one_for_blocking_violation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    rules_path, output_path = _create_invalid_project(tmp_path)

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "conformance-scan",
            "--rules",
            str(rules_path),
            "--output",
            str(output_path),
        ],
    )

    assert main() == 1