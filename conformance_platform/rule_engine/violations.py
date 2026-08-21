from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from conformance_platform.rule_engine.models import Severity


class ViolationType(StrEnum):
    LAYER_VIOLATION = "layer_violation"


class EvidenceType(StrEnum):
    STATIC = "static"
    RUNTIME = "runtime"


class ArchitectureViolation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    violation_id: str
    violation_type: ViolationType
    severity: Severity
    service_name: str
    message: str
    source_file: Path
    line: int
    source_layer: str
    target_layer: str
    target_module: str
    evidence_type: EvidenceType