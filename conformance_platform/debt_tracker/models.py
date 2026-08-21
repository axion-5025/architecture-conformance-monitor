from datetime import UTC, datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from conformance_platform.debt_tracker.database import Base


class ScanRecord(Base):
    __tablename__ = "scan_records"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    application: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )
    rules_version: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )
    services_scanned: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    files_scanned: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    dependencies_found: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    violations_found: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    blocking: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    violations: Mapped[list["ViolationRecord"]] = relationship(
        back_populates="scan",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="selectin",
        order_by="ViolationRecord.id",
    )


class ViolationRecord(Base):
    __tablename__ = "violation_records"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    scan_id: Mapped[int] = mapped_column(
        ForeignKey(
            "scan_records.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )
    violation_id: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,
    )
    violation_type: Mapped[str] = mapped_column(
        String(60),
        nullable=False,
    )
    severity: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    service_name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )
    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    source_file: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    line: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    source_layer: Mapped[str] = mapped_column(
        String(60),
        nullable=False,
    )
    target_layer: Mapped[str] = mapped_column(
        String(60),
        nullable=False,
    )
    target_module: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    evidence_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    scan: Mapped[ScanRecord] = relationship(
        back_populates="violations",
    )