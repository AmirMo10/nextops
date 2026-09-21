"""PostgreSQL acceptance tests for identity, audit, idempotency, and leases."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from alembic import command
from alembic.config import Config
from pydantic import SecretStr
from sqlalchemy import Engine, inspect, select, text, update
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session, sessionmaker

from nextops.application.errors import ApplicationError
from nextops.application.service import DurableAppService
from nextops.configuration import AppSettings
from nextops.contracts.durable import (
    BootstrapRequest,
    LoginRequest,
    RecoveryRequest,
    RunCreateRequest,
    RunStatus,
)
from nextops.contracts.errors import ErrorCode
from nextops.persistence.models import AuditEvent, Environment, Identity

pytestmark = pytest.mark.integration

BOOTSTRAP_SECRET = "bootstrap-secret-for-postgresql-tests-only"
RECOVERY_SECRET = "recovery-secret-for-postgresql-tests-only"
ADMIN_PASSWORD = "correct horse battery staple"
NEW_ADMIN_PASSWORD = "new correct horse battery staple"


class MutableClock:
    """Deterministic aware clock used to prove lease recovery after restart."""

    def __init__(self) -> None:
        self.value = datetime(2026, 9, 21, 9, 0, tzinfo=UTC)

    def __call__(self) -> datetime:
        return self.value

    def advance(self, seconds: int) -> None:
        self.value += timedelta(seconds=seconds)


@pytest.fixture()
def settings() -> AppSettings:
    return AppSettings(
        database_url=SecretStr("postgresql+psycopg://unused-in-service"),
        bootstrap_secret=SecretStr(BOOTSTRAP_SECRET),
        recovery_secret=SecretStr(RECOVERY_SECRET),
        session_ttl_seconds=3_600,
        lease_ttl_seconds=30,
    )


def bootstrap_request() -> BootstrapRequest:
    return BootstrapRequest(
        organization_slug="omid-nextai",
        organization_name="Omid NextAI",
        environment_slug="local",
        environment_name="Local",
        admin_username="owner",
        admin_password=ADMIN_PASSWORD,
    )


def test_migration_upgrade_downgrade_and_role_grants(
    migrated_postgres: tuple[str, Engine], alembic_config: Config
) -> None:
    _, admin_engine = migrated_postgres
    expected_tables = {
        "alembic_version",
        "audit_events",
        "environments",
        "identities",
        "organizations",
        "run_leases",
        "runs",
        "sessions",
        "targets",
    }
    assert expected_tables <= set(inspect(admin_engine).get_table_names())

    with admin_engine.connect() as connection:
        assert connection.scalar(
            text("SELECT has_table_privilege('nextops_app', 'runs', 'INSERT')")
        )
        assert connection.scalar(
            text("SELECT has_table_privilege('nextops_support_ro', 'runs', 'SELECT')")
        )
        assert not connection.scalar(
            text("SELECT has_table_privilege('nextops_app', 'audit_events', 'UPDATE')")
        )

    command.downgrade(alembic_config, "base")
    assert "runs" not in set(inspect(admin_engine).get_table_names())
    command.upgrade(alembic_config, "head")
    assert expected_tables <= set(inspect(admin_engine).get_table_names())


def test_bootstrap_login_and_recovery_revoke_every_prior_session(
    app_session_factory: sessionmaker[Session], settings: AppSettings
) -> None:
    service = DurableAppService(app_session_factory, settings)
    bootstrap = service.bootstrap(bootstrap_request(), BOOTSTRAP_SECRET, uuid4())
    bootstrap_token = bootstrap.authenticated_session.session.access_token

    actor = service.authenticate(bootstrap_token)
    assert actor.subject_id == bootstrap.admin_identity_id

    login = service.login(
        LoginRequest(username="owner", password=ADMIN_PASSWORD), correlation_id=uuid4()
    )
    assert service.authenticate(login.session.access_token) == actor

    recovery = service.recover(
        RecoveryRequest(admin_username="owner", new_password=NEW_ADMIN_PASSWORD),
        RECOVERY_SECRET,
        uuid4(),
    )
    assert recovery.revoked_session_count == 2
    assert recovery.credential_version == 2

    for revoked_token in (bootstrap_token, login.session.access_token):
        with pytest.raises(ApplicationError) as failure:
            service.authenticate(revoked_token)
        assert failure.value.code is ErrorCode.UNAUTHENTICATED

    with pytest.raises(ApplicationError):
        service.login(LoginRequest(username="owner", password=ADMIN_PASSWORD), uuid4())
    new_login = service.login(LoginRequest(username="owner", password=NEW_ADMIN_PASSWORD), uuid4())
    assert service.authenticate(new_login.session.access_token).subject_id == actor.subject_id


def test_run_idempotency_fixture_result_and_expired_lease_restart_recovery(
    app_session_factory: sessionmaker[Session], settings: AppSettings
) -> None:
    clock = MutableClock()
    service = DurableAppService(app_session_factory, settings, clock=clock)
    bootstrap = service.bootstrap(bootstrap_request(), BOOTSTRAP_SECRET, uuid4())
    actor = bootstrap.authenticated_session.actor
    request = RunCreateRequest(
        target_id=bootstrap.fixture_target_id,
        action="zabbix.host.read",
        question="Which monitored hosts are unavailable?",
        locale="en",
    )

    created = service.create_run(actor, request, "request-0001", uuid4())
    replayed = service.create_run(actor, request, "request-0001", uuid4())
    assert replayed.run_id == created.run_id

    changed_request = request.model_copy(update={"question": "Changed intent"})
    with pytest.raises(ApplicationError) as conflict:
        service.create_run(actor, changed_request, "request-0001", uuid4())
    assert conflict.value.code is ErrorCode.CONFLICT

    first_lease = service.claim_lease(created.run_id, "fixture-worker-a")
    with pytest.raises(ApplicationError):
        service.claim_lease(created.run_id, "fixture-worker-b")

    clock.advance(31)
    restarted_service = DurableAppService(app_session_factory, settings, clock=clock)
    recovered_lease = restarted_service.claim_lease(created.run_id, "fixture-worker-b")
    assert recovered_lease.generation == first_lease.generation + 1

    renewed = restarted_service.renew_lease(recovered_lease)
    assert renewed.expires_at > recovered_lease.expires_at
    completed = restarted_service.complete_fixture(renewed)

    assert completed.status is RunStatus.SUCCEEDED
    assert completed.result is not None
    assert completed.result.source.connector == "fixture"
    assert completed.result.is_stale is True
    assert completed.result.audit_event_id is not None


def test_cross_environment_target_is_denied_and_audited(
    app_session_factory: sessionmaker[Session], settings: AppSettings
) -> None:
    service = DurableAppService(app_session_factory, settings)
    bootstrap = service.bootstrap(bootstrap_request(), BOOTSTRAP_SECRET, uuid4())

    with app_session_factory.begin() as session:
        second_environment = Environment(
            id=uuid4(),
            organization_id=bootstrap.organization_id,
            slug="other",
            display_name="Other",
        )
        session.add(second_environment)
        second_identity = Identity(
            id=uuid4(),
            organization_id=bootstrap.organization_id,
            environment_id=second_environment.id,
            username="other-admin",
            password_hash="not-used-in-this-scope-test",
            roles=["admin"],
            scopes=["zabbix.read", "runs.read"],
            is_active=True,
            credential_version=1,
        )
        session.add(second_identity)
        session.flush()
        other_actor = bootstrap.authenticated_session.actor.model_copy(
            update={
                "subject_id": second_identity.id,
                "environment_id": second_environment.id,
            }
        )

    request = RunCreateRequest(
        target_id=bootstrap.fixture_target_id,
        action="zabbix.host.read",
        question="Cross-scope attempt",
        locale="en",
    )
    with pytest.raises(ApplicationError) as denied:
        service.create_run(other_actor, request, "request-0002", uuid4())
    assert denied.value.code is ErrorCode.POLICY_DENIED

    with app_session_factory() as session:
        denied_events = session.scalars(
            select(AuditEvent).where(AuditEvent.event_type == "run.create.denied")
        ).all()
    assert len(denied_events) == 1
    assert denied_events[0].outcome == "denied"


def test_audit_failure_rolls_back_state_and_append_only_trigger_blocks_owner(
    app_session_factory: sessionmaker[Session],
    migrated_postgres: tuple[str, Engine],
    settings: AppSettings,
) -> None:
    _, admin_engine = migrated_postgres
    service = DurableAppService(app_session_factory, settings)

    with admin_engine.begin() as connection:
        connection.execute(text("REVOKE INSERT ON audit_events FROM nextops_app"))
    try:
        with pytest.raises(ApplicationError) as failure:
            service.bootstrap(bootstrap_request(), BOOTSTRAP_SECRET, uuid4())
        assert failure.value.code is ErrorCode.DEPENDENCY_UNAVAILABLE
        with admin_engine.connect() as connection:
            assert connection.scalar(text("SELECT count(*) FROM organizations")) == 0
    finally:
        with admin_engine.begin() as connection:
            connection.execute(text("GRANT SELECT, INSERT ON audit_events TO nextops_app"))

    service.bootstrap(bootstrap_request(), BOOTSTRAP_SECRET, uuid4())
    with admin_engine.begin() as connection, pytest.raises(DBAPIError):
        connection.execute(update(AuditEvent).values(outcome="failed"))
