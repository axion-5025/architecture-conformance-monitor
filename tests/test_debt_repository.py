from datetime import UTC, datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from conformance_platform.debt_tracker.database import Base
from conformance_platform.debt_tracker.repository import (
    get_latest_scan,
    list_scans,
    save_scan_report,
)


def _create_session() -> Session:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    return Session(engine)


def _build_report() -> dict:
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "application": "sample-commerce",
        "rules_version": "1.0",
        "summary": {
            "services_scanned": 1,
            "files_scanned": 1,
            "dependencies_found": 1,
            "violations_found": 1,
        },
        "services": [],
        "violations": [
            {
                "violation_id": "test-violation-1",
                "violation_type": "layer_violation",
                "severity": "high",
                "service_name": "order-service",
                "message": (
                    "Layer 'api' cannot import layer 'repositories'"
                ),
                "source_file": "app/api/orders.py",
                "line": 2,
                "source_layer": "api",
                "target_layer": "repositories",
                "target_module": "app.repositories.orders",
                "evidence_type": "static",
            }
        ],
    }


def test_saves_scan_and_violation() -> None:
    with _create_session() as session:
        saved_scan = save_scan_report(
            session,
            _build_report(),
            blocking=True,
        )

        assert saved_scan.id is not None
        assert saved_scan.blocking is True
        assert saved_scan.violations_found == 1
        assert len(saved_scan.violations) == 1

        violation = saved_scan.violations[0]

        assert violation.violation_id == "test-violation-1"
        assert violation.severity == "high"
        assert violation.source_layer == "api"
        assert violation.target_layer == "repositories"


def test_returns_latest_scan_first() -> None:
    with _create_session() as session:
        first_report = _build_report()
        first_report["generated_at"] = "2026-08-20T10:00:00+00:00"

        second_report = _build_report()
        second_report["generated_at"] = "2026-08-21T10:00:00+00:00"
        second_report["violations"][0]["violation_id"] = "latest"

        save_scan_report(session, first_report, blocking=True)
        save_scan_report(session, second_report, blocking=True)

        latest = get_latest_scan(session)
        scans = list_scans(session)

        assert latest is not None
        assert latest.violations[0].violation_id == "latest"
        assert len(scans) == 2
        assert scans[0].generated_at > scans[1].generated_at