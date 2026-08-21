from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from conformance_platform.debt_tracker.models import (
    ScanRecord,
    ViolationRecord,
)


def save_scan_report(
    session: Session,
    report: dict[str, Any],
    *,
    blocking: bool,
) -> ScanRecord:
    summary = report["summary"]

    scan_record = ScanRecord(
        generated_at=datetime.fromisoformat(report["generated_at"]),
        application=report["application"],
        rules_version=report["rules_version"],
        services_scanned=summary["services_scanned"],
        files_scanned=summary["files_scanned"],
        dependencies_found=summary["dependencies_found"],
        violations_found=summary["violations_found"],
        blocking=blocking,
    )

    for violation in report["violations"]:
        scan_record.violations.append(
            ViolationRecord(
                violation_id=violation["violation_id"],
                violation_type=violation["violation_type"],
                severity=violation["severity"],
                service_name=violation["service_name"],
                message=violation["message"],
                source_file=violation["source_file"],
                line=violation["line"],
                source_layer=violation["source_layer"],
                target_layer=violation["target_layer"],
                target_module=violation["target_module"],
                evidence_type=violation["evidence_type"],
            )
        )

    try:
        session.add(scan_record)
        session.commit()
        session.refresh(scan_record)
    except Exception:
        session.rollback()
        raise

    return scan_record


def get_scan_by_id(
    session: Session,
    scan_id: int,
) -> ScanRecord | None:
    statement = (
        select(ScanRecord)
        .options(selectinload(ScanRecord.violations))
        .where(ScanRecord.id == scan_id)
    )

    return session.scalar(statement)


def get_latest_scan(
    session: Session,
) -> ScanRecord | None:
    statement = (
        select(ScanRecord)
        .options(selectinload(ScanRecord.violations))
        .order_by(
            ScanRecord.generated_at.desc(),
            ScanRecord.id.desc(),
        )
        .limit(1)
    )

    return session.scalar(statement)


def list_scans(
    session: Session,
    *,
    limit: int = 50,
) -> list[ScanRecord]:
    statement = (
        select(ScanRecord)
        .order_by(
            ScanRecord.generated_at.desc(),
            ScanRecord.id.desc(),
        )
        .limit(limit)
    )

    return list(session.scalars(statement))