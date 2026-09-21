"""Real PostgreSQL fixtures for Stage 1A acceptance tests."""

from __future__ import annotations

import os
from collections.abc import Iterator
from typing import Any

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, create_engine, event, text
from sqlalchemy.orm import Session, sessionmaker

TABLES = (
    "audit_events",
    "run_leases",
    "runs",
    "sessions",
    "identities",
    "targets",
    "environments",
    "organizations",
)


@pytest.fixture(scope="session")
def postgres_url() -> str:
    """Require an explicit isolated PostgreSQL URL; never substitute SQLite."""

    database_url = os.environ.get("NEXTOPS_TEST_DATABASE_URL")
    if not database_url:
        pytest.skip("NEXTOPS_TEST_DATABASE_URL is required for real PostgreSQL tests")
    if not database_url.startswith("postgresql+psycopg://"):
        pytest.fail("NEXTOPS_TEST_DATABASE_URL must use postgresql+psycopg")
    return database_url


@pytest.fixture(scope="session")
def alembic_config(postgres_url: str) -> Config:
    config = Config("alembic.ini")
    config.set_main_option("sqlalchemy.url", postgres_url.replace("%", "%%"))
    return config


@pytest.fixture(scope="session")
def migrated_postgres(postgres_url: str, alembic_config: Config) -> Iterator[tuple[str, Engine]]:
    """Apply the real baseline once and remove schema objects after the suite."""

    admin_engine = create_engine(postgres_url)
    command.downgrade(alembic_config, "base")
    command.upgrade(alembic_config, "head")
    yield postgres_url, admin_engine
    admin_engine.dispose()


@pytest.fixture()
def app_session_factory(
    migrated_postgres: tuple[str, Engine],
) -> Iterator[sessionmaker[Session]]:
    """Use the restricted app role and clean application rows around each test."""

    postgres_url, admin_engine = migrated_postgres
    with admin_engine.begin() as connection:
        connection.execute(text(f"TRUNCATE {', '.join(TABLES)} CASCADE"))

    app_engine = create_engine(postgres_url)

    @event.listens_for(app_engine, "connect")
    def set_restricted_role(dbapi_connection: Any, connection_record: Any) -> None:
        del connection_record
        with dbapi_connection.cursor() as cursor:
            cursor.execute("SET ROLE nextops_app")

    yield sessionmaker(bind=app_engine, expire_on_commit=False)
    app_engine.dispose()

    with admin_engine.begin() as connection:
        connection.execute(text(f"TRUNCATE {', '.join(TABLES)} CASCADE"))
