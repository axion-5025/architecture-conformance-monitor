import json
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict

from conformance_platform.cli import run_scan

RULES_PATH = Path("architecture-rules/baseline.yml")
LATEST_REPORT_PATH = Path(
    "reports/latest-conformance-report.json"
)


class HealthResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    service: str
    version: str
    status: str


class ScanResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    blocking: bool
    report: dict[str, Any]


app = FastAPI(
    title="Architecture Conformance Platform API",
    description=(
        "Scans Python services and reports architecture violations."
    ),
    version="0.1.0",
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
        version="0.1.0",
        status="healthy",
    )


@app.post(
    "/api/v1/scans",
    response_model=ScanResponse,
    tags=["Scans"],
)
def create_scan() -> ScanResponse:
    report, has_blocking_violations = run_scan(
        rules_path=RULES_PATH,
        output_path=LATEST_REPORT_PATH,
    )

    return ScanResponse(
        blocking=has_blocking_violations,
        report=report,
    )


@app.get(
    "/api/v1/scans/latest",
    response_model=ScanResponse,
    tags=["Scans"],
)
def get_latest_scan() -> ScanResponse:
    if not LATEST_REPORT_PATH.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No conformance scan report is available",
        )

    report = json.loads(
        LATEST_REPORT_PATH.read_text(encoding="utf-8")
    )

    violations = report.get("violations", [])
    blocking = any(
        violation.get("severity") in {"high", "critical"}
        for violation in violations
    )

    return ScanResponse(
        blocking=blocking,
        report=report,
    )