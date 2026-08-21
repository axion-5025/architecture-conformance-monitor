from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated, Any

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from conformance_platform.cli import run_scan
from conformance_platform.debt_tracker.database import (
    create_tables,
    get_session,
)
from conformance_platform.debt_tracker.models import (
    ScanRecord,
    ViolationRecord,
)
from conformance_platform.debt_tracker.repository import (
    get_latest_scan as get_latest_scan_record,
)
from conformance_platform.debt_tracker.repository import (
    get_scan_by_id,
    list_scans,
    save_scan_report,
)

RULES_PATH = Path("architecture-rules/baseline.yml")
LATEST_REPORT_PATH = Path(
    "reports/latest-conformance-report.json"
)

SessionDependency = Annotated[
    Session,
    Depends(get_session),
]


class HealthResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    service: str
    version: str
    status: str


class ScanResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scan_id: int
    blocking: bool
    report: dict[str, Any]


class ScanSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    services_scanned: int
    files_scanned: int
    dependencies_found: int
    violations_found: int


class ViolationDetail(BaseModel):
    model_config = ConfigDict(extra="forbid")

    violation_id: str
    violation_type: str
    severity: str
    service_name: str
    message: str
    source_file: str
    line: int
    source_layer: str
    target_layer: str
    target_module: str
    evidence_type: str


class ScanHistoryItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scan_id: int
    generated_at: str
    application: str
    rules_version: str
    services_scanned: int
    files_scanned: int
    dependencies_found: int
    violations_found: int
    blocking: bool


class ScanDetailResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scan_id: int
    generated_at: str
    application: str
    rules_version: str
    blocking: bool
    summary: ScanSummary
    violations: list[ViolationDetail]


def _violation_to_detail(
    violation: ViolationRecord,
) -> ViolationDetail:
    return ViolationDetail(
        violation_id=violation.violation_id,
        violation_type=violation.violation_type,
        severity=violation.severity,
        service_name=violation.service_name,
        message=violation.message,
        source_file=violation.source_file,
        line=violation.line,
        source_layer=violation.source_layer,
        target_layer=violation.target_layer,
        target_module=violation.target_module,
        evidence_type=violation.evidence_type,
    )


def _scan_to_detail(
    scan: ScanRecord,
) -> ScanDetailResponse:
    return ScanDetailResponse(
        scan_id=scan.id,
        generated_at=scan.generated_at.isoformat(),
        application=scan.application,
        rules_version=scan.rules_version,
        blocking=scan.blocking,
        summary=ScanSummary(
            services_scanned=scan.services_scanned,
            files_scanned=scan.files_scanned,
            dependencies_found=scan.dependencies_found,
            violations_found=scan.violations_found,
        ),
        violations=[
            _violation_to_detail(violation)
            for violation in scan.violations
        ],
    )


def _scan_to_report(
    scan: ScanRecord,
) -> dict[str, Any]:
    detail = _scan_to_detail(scan)

    return {
        "generated_at": detail.generated_at,
        "application": detail.application,
        "rules_version": detail.rules_version,
        "summary": detail.summary.model_dump(),
        "services": [],
        "violations": [
            violation.model_dump()
            for violation in detail.violations
        ],
    }


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    create_tables()
    yield


app = FastAPI(
    title="Architecture Conformance Platform API",
    description=(
        "Scans Python services and reports architecture violations."
    ),
    version="0.3.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
)
def health_check() -> HealthResponse:
    return HealthResponse(
        service="conformance-platform-api",
        version="0.3.0",
        status="healthy",
    )


@app.post(
    "/api/v1/scans",
    response_model=ScanResponse,
    tags=["Scans"],
)
def create_scan(
    session: SessionDependency,
) -> ScanResponse:
    report, has_blocking_violations = run_scan(
        rules_path=RULES_PATH,
        output_path=LATEST_REPORT_PATH,
    )

    saved_scan = save_scan_report(
        session,
        report,
        blocking=has_blocking_violations,
    )

    return ScanResponse(
        scan_id=saved_scan.id,
        blocking=has_blocking_violations,
        report=report,
    )


@app.get(
    "/api/v1/scans/latest",
    response_model=ScanResponse,
    tags=["Scans"],
)
def get_latest_scan(
    session: SessionDependency,
) -> ScanResponse:
    latest_scan = get_latest_scan_record(session)

    if latest_scan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No conformance scan is available",
        )

    return ScanResponse(
        scan_id=latest_scan.id,
        blocking=latest_scan.blocking,
        report=_scan_to_report(latest_scan),
    )


@app.get(
    "/api/v1/scans/history",
    response_model=list[ScanHistoryItem],
    tags=["Scans"],
)
def get_scan_history(
    session: SessionDependency,
) -> list[ScanHistoryItem]:
    records = list_scans(session)

    return [
        ScanHistoryItem(
            scan_id=record.id,
            generated_at=record.generated_at.isoformat(),
            application=record.application,
            rules_version=record.rules_version,
            services_scanned=record.services_scanned,
            files_scanned=record.files_scanned,
            dependencies_found=record.dependencies_found,
            violations_found=record.violations_found,
            blocking=record.blocking,
        )
        for record in records
    ]


@app.get(
    "/api/v1/scans/{scan_id}",
    response_model=ScanDetailResponse,
    tags=["Scans"],
)
def get_scan_detail(
    scan_id: int,
    session: SessionDependency,
) -> ScanDetailResponse:
    scan = get_scan_by_id(session, scan_id)

    if scan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scan {scan_id} was not found",
        )

    return _scan_to_detail(scan)