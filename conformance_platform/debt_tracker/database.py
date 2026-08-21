import os
from collections.abc import Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DEFAULT_DATABASE_URL = "sqlite:///./architecture_monitor.db"


class Base(DeclarativeBase):
    pass


def build_engine(
    database_url: str | None = None,
) -> Engine:
    resolved_url = (
        database_url
        or os.getenv("DATABASE_URL")
        or DEFAULT_DATABASE_URL
    )

    connect_args = (
        {"check_same_thread": False}
        if resolved_url.startswith("sqlite")
        else {}
    )

    return create_engine(
        resolved_url,
        connect_args=connect_args,
        pool_pre_ping=True,
    )


engine = build_engine()

SessionFactory = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def get_session() -> Generator[Session]:
    session = SessionFactory()

    try:
        yield session
    finally:
        session.close()


def create_tables() -> None:
    from conformance_platform.debt_tracker import models  # noqa: F401

    Base.metadata.create_all(bind=engine)