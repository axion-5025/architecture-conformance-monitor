import json
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
from conformance_platform.debt_tracker.repository import (
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


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    create_tables()
    yield


app = FastAPI(
    title="Architecture Conformance Platform API",
    description=(
        "Scans Python services and reports architecture violations."
    ),
    version="0.2.0",
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
        version="0.2.0",
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
    scans = list_scans(session, limit=1)

    if not scans or not LATEST_REPORT_PATH.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No conformance scan report is available",
        )

    latest_scan = scans[0]
    report = json.loads(
        LATEST_REPORT_PATH.read_text(encoding="utf-8")
    )

    return ScanResponse(
        scan_id=latest_scan.id,
        blocking=latest_scan.blocking,
        report=report,
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