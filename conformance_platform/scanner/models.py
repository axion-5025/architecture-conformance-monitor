from pathlib import Path

from pydantic import BaseModel, ConfigDict


class DependencyEvidence(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_file: Path
    line: int
    source_module: str
    target_module: str
    source_layer: str | None
    target_layer: str | None


class ServiceScanResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    service_name: str
    source_path: Path
    files_scanned: int
    dependencies: list[DependencyEvidence]