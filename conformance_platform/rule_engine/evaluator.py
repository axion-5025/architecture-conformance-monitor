from hashlib import sha256

from conformance_platform.rule_engine.models import ArchitectureRules
from conformance_platform.rule_engine.violations import (
    ArchitectureViolation,
    EvidenceType,
    ViolationType,
)
from conformance_platform.scanner.models import ServiceScanResult


def _create_violation_id(
    service_name: str,
    source_file: str,
    line: int,
    target_module: str,
) -> str:
    identity = (
        f"{service_name}:{source_file}:{line}:{target_module}"
    )
    return sha256(identity.encode("utf-8")).hexdigest()[:16]


def evaluate_layer_conformance(
    rules: ArchitectureRules,
    scan_results: list[ServiceScanResult],
) -> list[ArchitectureViolation]:
    policy = rules.policies.layer_violation

    if not policy.enabled:
        return []

    violations: list[ArchitectureViolation] = []

    for scan_result in scan_results:
        for dependency in scan_result.dependencies:
            source_layer = dependency.source_layer
            target_layer = dependency.target_layer

            if source_layer is None or target_layer is None:
                continue

            if source_layer == target_layer:
                continue

            layer_rule = rules.layer_rules.get(source_layer)
            if layer_rule is None:
                continue

            if target_layer in layer_rule.allowed_imports:
                continue

            violations.append(
                ArchitectureViolation(
                    violation_id=_create_violation_id(
                        service_name=scan_result.service_name,
                        source_file=str(dependency.source_file),
                        line=dependency.line,
                        target_module=dependency.target_module,
                    ),
                    violation_type=ViolationType.LAYER_VIOLATION,
                    severity=policy.severity,
                    service_name=scan_result.service_name,
                    message=(
                        f"Layer '{source_layer}' cannot import "
                        f"layer '{target_layer}'"
                    ),
                    source_file=dependency.source_file,
                    line=dependency.line,
                    source_layer=source_layer,
                    target_layer=target_layer,
                    target_module=dependency.target_module,
                    evidence_type=EvidenceType.STATIC,
                )
            )

    return violations