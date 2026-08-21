from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from conformance_platform.api import main as api_module

client = TestClient(api_module.app)


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "service": "conformance-platform-api",
        "version": "0.1.0",
        "status": "healthy",
    }


def test_creates_and_retrieves_scan(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    report_path = tmp_path / "latest-report.json"

    monkeypatch.setattr(
        api_module,
        "LATEST_REPORT_PATH",
        report_path,
    )

    create_response = client.post("/api/v1/scans")

    assert create_response.status_code == 200

    create_body = create_response.json()

    assert create_body["blocking"] is False
    assert create_body["report"]["summary"] == {
        "services_scanned": 3,
        "files_scanned": 21,
        "dependencies_found": 0,
        "violations_found": 0,
    }
    assert report_path.is_file()

    latest_response = client.get("/api/v1/scans/latest")

    assert latest_response.status_code == 200
    assert latest_response.json()["report"] == create_body["report"]


def test_latest_scan_returns_404_when_missing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    missing_path = tmp_path / "missing-report.json"

    monkeypatch.setattr(
        api_module,
        "LATEST_REPORT_PATH",
        missing_path,
    )

    response = client.get("/api/v1/scans/latest")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "No conformance scan report is available"
    }