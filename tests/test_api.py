from collections.abc import Generator
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


def test_health_endpoint(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "service": "conformance-platform-api",
        "version": "0.2.0",
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
    assert latest_response.json() == create_body

    history_response = client.get("/api/v1/scans/history")

    assert history_response.status_code == 200

    history = history_response.json()

    assert len(history) == 1
    assert history[0]["scan_id"] == 1
    assert history[0]["violations_found"] == 0
    assert history[0]["blocking"] is False


def test_latest_scan_returns_404_when_missing(
    client: TestClient,
) -> None:
    response = client.get("/api/v1/scans/latest")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "No conformance scan report is available"
    }