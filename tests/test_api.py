from collections.abc import Generator
from datetime import UTC, datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from conformance_platform.api import main as api_module
from conformance_platform.debt_tracker.database import (
    Base,
    get_session,
)


@pytest.fixture
def client(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> Generator[TestClient]:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)

    testing_session = sessionmaker(
        bind=engine,
        expire_on_commit=False,
    )

    def override_get_session() -> Generator[Session]:
        with testing_session() as session:
            yield session

    api_module.app.dependency_overrides[get_session] = (
        override_get_session
    )

    monkeypatch.setattr(
        api_module,
        "LATEST_REPORT_PATH",
        tmp_path / "latest-report.json",
    )

    with TestClient(api_module.app) as test_client:
        yield test_client

    api_module.app.dependency_overrides.clear()


def _build_blocking_report() -> dict:
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "application": "sample-commerce",
        "rules_version": "1.0",
        "summary": {
            "services_scanned": 3,
            "files_scanned": 22,
            "dependencies_found": 1,
            "violations_found": 1,
        },
        "services": [],
        "violations": [
            {
                "violation_id": "layer-violation-1",
                "violation_type": "layer_violation",
                "severity": "high",
                "service_name": "order-service",
                "message": (
                    "Layer 'api' cannot import layer 'repositories'"
                ),
                "source_file": (
                    "apps/order-service/app/api/orders.py"
                ),
                "line": 4,
                "source_layer": "api",
                "target_layer": "repositories",
                "target_module": "app.repositories.orders",
                "evidence_type": "static",
            }
        ],
    }


def test_health_endpoint(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "service": "conformance-platform-api",
        "version": "0.3.0",
        "status": "healthy",
    }


def test_creates_retrieves_and_lists_scan(
    client: TestClient,
) -> None:
    create_response = client.post("/api/v1/scans")

    assert create_response.status_code == 200

    create_body = create_response.json()

    assert create_body["scan_id"] == 1
    assert create_body["blocking"] is False
    assert create_body["report"]["summary"]["services_scanned"] == 3

    latest_response = client.get("/api/v1/scans/latest")

    assert latest_response.status_code == 200

    latest_body = latest_response.json()

    assert latest_body["scan_id"] == 1
    assert latest_body["blocking"] is False
    assert latest_body["report"]["application"] == "sample-commerce"
    assert latest_body["report"]["rules_version"] == "1.0"
    assert latest_body["report"]["summary"] == {
        "services_scanned": 3,
        "files_scanned": 21,
        "dependencies_found": 0,
        "violations_found": 0,
    }
    assert latest_body["report"]["violations"] == []

    history_response = client.get("/api/v1/scans/history")

    assert history_response.status_code == 200

    history = history_response.json()

    assert len(history) == 1
    assert history[0]["scan_id"] == 1
    assert history[0]["services_scanned"] == 3
    assert history[0]["files_scanned"] == 21
    assert history[0]["violations_found"] == 0
    assert history[0]["blocking"] is False

    detail_response = client.get("/api/v1/scans/1")

    assert detail_response.status_code == 200

    detail = detail_response.json()

    assert detail["scan_id"] == 1
    assert detail["application"] == "sample-commerce"
    assert detail["blocking"] is False
    assert detail["summary"]["services_scanned"] == 3
    assert detail["summary"]["violations_found"] == 0
    assert detail["violations"] == []


def test_latest_scan_uses_database_when_report_file_is_missing(
    client: TestClient,
) -> None:
    create_response = client.post("/api/v1/scans")

    assert create_response.status_code == 200

    api_module.LATEST_REPORT_PATH.unlink(missing_ok=True)

    latest_response = client.get("/api/v1/scans/latest")

    assert latest_response.status_code == 200
    assert latest_response.json()["scan_id"] == 1
    assert latest_response.json()["report"]["application"] == (
        "sample-commerce"
    )


def test_returns_stored_violation_details(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    blocking_report = _build_blocking_report()

    monkeypatch.setattr(
        api_module,
        "run_scan",
        lambda **_: (blocking_report, True),
    )

    create_response = client.post("/api/v1/scans")

    assert create_response.status_code == 200
    assert create_response.json()["blocking"] is True

    detail_response = client.get("/api/v1/scans/1")

    assert detail_response.status_code == 200

    detail = detail_response.json()

    assert detail["scan_id"] == 1
    assert detail["blocking"] is True
    assert detail["summary"] == {
        "services_scanned": 3,
        "files_scanned": 22,
        "dependencies_found": 1,
        "violations_found": 1,
    }
    assert len(detail["violations"]) == 1

    violation = detail["violations"][0]

    assert violation == {
        "violation_id": "layer-violation-1",
        "violation_type": "layer_violation",
        "severity": "high",
        "service_name": "order-service",
        "message": (
            "Layer 'api' cannot import layer 'repositories'"
        ),
        "source_file": (
            "apps/order-service/app/api/orders.py"
        ),
        "line": 4,
        "source_layer": "api",
        "target_layer": "repositories",
        "target_module": "app.repositories.orders",
        "evidence_type": "static",
    }


def test_latest_scan_returns_404_when_missing(
    client: TestClient,
) -> None:
    response = client.get("/api/v1/scans/latest")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "No conformance scan is available"
    }


def test_scan_detail_returns_404_when_missing(
    client: TestClient,
) -> None:
    response = client.get("/api/v1/scans/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Scan 999 was not found"
    }