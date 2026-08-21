import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from conformance_platform.rule_engine.evaluator import (
    evaluate_layer_conformance,
)
from conformance_platform.rule_engine.loader import load_rules
from conformance_platform.rule_engine.models import Severity
from conformance_platform.scanner.python_scanner import scan_service

BLOCKING_SEVERITIES = {
    Severity.HIGH,
    Severity.CRITICAL,
}


def run_scan(
    rules_path: Path,
    output_path: Path,
) -> tuple[dict[str, Any], bool]:
    rules = load_rules(rules_path)

    scan_results = [
        scan_service(
            service_name=service_name,
            source_path=service_rule.source_path,
        )
        for service_name, service_rule in rules.services.items()
    ]

    violations = evaluate_layer_conformance(
        rules=rules,
        scan_results=scan_results,
    )

    files_scanned = sum(
        result.files_scanned for result in scan_results
    )
    dependencies_found = sum(
        len(result.dependencies) for result in scan_results
    )

    report: dict[str, Any] = {
        "generated_at": datetime.now(UTC).isoformat(),
        "application": rules.application.name,
        "rules_version": rules.version,
        "summary": {
            "services_scanned": len(scan_results),
            "files_scanned": files_scanned,
            "dependencies_found": dependencies_found,
            "violations_found": len(violations),
        },
        "services": [
            result.model_dump(mode="json")
            for result in scan_results
        ],
        "violations": [
            violation.model_dump(mode="json")
            for violation in violations
        ],
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    has_blocking_violations = any(
        violation.severity in BLOCKING_SEVERITIES
        for violation in violations
    )

    return report, has_blocking_violations


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Scan Python services and check architecture conformance."
        )
    )
    parser.add_argument(
        "--rules",
        type=Path,
        default=Path("architecture-rules/baseline.yml"),
        help="Path to the approved architecture YAML file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/conformance-report.json"),
        help="Path where the JSON report will be written.",
    )
    return parser


def main() -> int:
    arguments = _build_parser().parse_args()

    report, has_blocking_violations = run_scan(
        rules_path=arguments.rules,
        output_path=arguments.output,
    )

    summary = report["summary"]

    sys.stdout.write(
        "\n".join(
            [
                "Architecture conformance scan completed",
                f"Services scanned: {summary['services_scanned']}",
                f"Files scanned: {summary['files_scanned']}",
                (
                    "Dependencies found: "
                    f"{summary['dependencies_found']}"
                ),
                f"Violations found: {summary['violations_found']}",
                f"Report: {arguments.output}",
                "",
            ]
        )
    )

    return 1 if has_blocking_violations else 0


if __name__ == "__main__":
    raise SystemExit(main())