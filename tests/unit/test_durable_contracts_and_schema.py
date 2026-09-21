"""Stage 1A Increment 2 contract and PostgreSQL schema tests."""

from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

import pytest
from pydantic import ValidationError

from nextops.contracts.durable import (
    BootstrapRequest,
    EvidenceSource,
    FixtureResult,
    RunCreateRequest,
    RunStatus,
)
from nextops.persistence.models import Base

ORG_ID = UUID("10000000-0000-4000-8000-000000000001")
ENV_ID = UUID("20000000-0000-4000-8000-000000000001")
TARGET_ID = UUID("30000000-0000-4000-8000-000000000001")
RUN_ID = UUID("40000000-0000-4000-8000-000000000001")
AUDIT_ID = UUID("50000000-0000-4000-8000-000000000001")


def test_bootstrap_contract_rejects_weak_password_and_client_actor() -> None:
    with pytest.raises(ValidationError):
        BootstrapRequest.model_validate(
            {
                "organization_slug": "omid-nextai",
                "organization_name": "Omid NextAI",
                "environment_slug": "local",
                "environment_name": "Local",
                "admin_username": "owner",
                "admin_password": "too-short",
                "actor": {"organization_id": str(ORG_ID)},
            }
        )


def test_run_create_contract_never_accepts_client_actor_context() -> None:
    with pytest.raises(ValidationError):
        RunCreateRequest.model_validate(
            {
                "target_id": TARGET_ID,
                "action": "zabbix.host.read",
                "question": "Which monitored hosts are unavailable?",
                "locale": "en",
                "parameters": {},
                "actor": {"organization_id": str(ORG_ID)},
            }
        )


def test_fixture_result_carries_provenance_scope_and_limitations() -> None:
    measured_at = datetime(2026, 9, 21, 8, 30, tzinfo=UTC)
    collected_at = datetime(2026, 9, 21, 8, 31, tzinfo=UTC)

    result = FixtureResult(
        run_id=RUN_ID,
        status=RunStatus.SUCCEEDED,
        locale="fa",
        answer="این پاسخ آزمایشی است.",
        source=EvidenceSource(
            connector="fixture",
            method="fixture.zabbix.host.read",
            collected_at=collected_at,
            measured_at=measured_at,
        ),
        organization_id=ORG_ID,
        environment_id=ENV_ID,
        target_id=TARGET_ID,
        is_partial=False,
        is_stale=True,
        errors=(),
        audit_event_id=AUDIT_ID,
    )

    assert result.source.measured_at == measured_at
    assert result.is_stale is True
    assert result.audit_event_id == AUDIT_ID


def test_schema_contains_authoritative_state_tables() -> None:
    assert set(Base.metadata.tables) == {
        "audit_events",
        "environments",
        "identities",
        "organizations",
        "run_leases",
        "runs",
        "sessions",
        "targets",
    }


def test_database_constraints_protect_single_org_idempotency_and_lease_expiry() -> None:
    organizations = Base.metadata.tables["organizations"]
    runs = Base.metadata.tables["runs"]
    run_leases = Base.metadata.tables["run_leases"]

    organization_constraints = {constraint.name for constraint in organizations.constraints}
    run_constraints = {constraint.name for constraint in runs.constraints}
    lease_constraints = {constraint.name for constraint in run_leases.constraints}

    assert "ck_organizations_singleton" in organization_constraints
    assert "uq_organizations_singleton" in organization_constraints
    assert "uq_runs_actor_idempotency" in run_constraints
    assert "ck_run_leases_expiry_after_acquisition" in lease_constraints


def test_baseline_migration_defines_roles_and_append_only_audit_guard() -> None:
    migration = Path("migrations/versions/0001_durable_app.py").read_text(encoding="utf-8")

    assert "nextops_migrator" in migration
    assert "nextops_app" in migration
    assert "nextops_support_ro" in migration
    assert "nextops_prevent_audit_mutation" in migration
    assert "GRANT SELECT, INSERT ON audit_events TO nextops_app" in migration
    assert "GRANT UPDATE (password_hash, credential_version, updated_at)" in migration
    assert "GRANT SELECT, INSERT, UPDATE ON identities" not in migration
    assert "fk_audit_events_actor_scope" in migration
    assert "fk_audit_events_run_scope" in migration
    assert "DROP ROLE" not in migration
