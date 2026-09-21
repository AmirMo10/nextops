"""Create the Stage 1A durable local application schema.

Revision ID: 0001_durable_app
Revises: none
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0001_durable_app"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

ROLE_SQL = """
DO $roles$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'nextops_migrator') THEN
        CREATE ROLE nextops_migrator NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'nextops_app') THEN
        CREATE ROLE nextops_app NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'nextops_support_ro') THEN
        CREATE ROLE nextops_support_ro NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOINHERIT;
    END IF;
END
$roles$;
"""

AUDIT_GUARD_SQL = """
CREATE FUNCTION nextops_prevent_audit_mutation()
RETURNS trigger
LANGUAGE plpgsql
AS $audit_guard$
BEGIN
    RAISE EXCEPTION 'audit_events is append-only';
END
$audit_guard$;

CREATE TRIGGER trg_audit_events_append_only
BEFORE UPDATE OR DELETE ON audit_events
FOR EACH ROW EXECUTE FUNCTION nextops_prevent_audit_mutation();
"""

GRANT_SQL = """
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;

GRANT USAGE, CREATE ON SCHEMA public TO nextops_migrator;
GRANT USAGE ON SCHEMA public TO nextops_app, nextops_support_ro;

GRANT SELECT, INSERT ON organizations, environments, targets TO nextops_app;
GRANT SELECT, INSERT ON identities, sessions, runs TO nextops_app;
GRANT UPDATE (password_hash, credential_version, updated_at) ON identities TO nextops_app;
GRANT UPDATE (revoked_at, last_seen_at) ON sessions TO nextops_app;
GRANT UPDATE (status, result, error, updated_at) ON runs TO nextops_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON run_leases TO nextops_app;
GRANT SELECT, INSERT ON audit_events TO nextops_app;
GRANT SELECT ON organizations, environments, targets, identities, sessions, runs,
    run_leases, audit_events TO nextops_support_ro;

REVOKE UPDATE, DELETE, TRUNCATE ON audit_events FROM nextops_app, nextops_support_ro;
"""


def upgrade() -> None:
    """Create constrained state tables, audit guard, and restricted group roles."""

    op.execute(ROLE_SQL)

    op.create_table(
        "organizations",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("singleton_key", sa.SmallInteger(), nullable=False),
        sa.Column("slug", sa.String(length=63), nullable=False),
        sa.Column("display_name", sa.String(length=128), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.CheckConstraint("singleton_key = 1", name="ck_organizations_singleton"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("singleton_key", name="uq_organizations_singleton"),
        sa.UniqueConstraint("slug", name="uq_organizations_slug"),
    )
    op.create_table(
        "environments",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("slug", sa.String(length=63), nullable=False),
        sa.Column("display_name", sa.String(length=128), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "slug", name="uq_environments_org_slug"),
        sa.UniqueConstraint("id", "organization_id", name="uq_environments_id_org"),
    )
    op.create_table(
        "targets",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("environment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("kind", sa.String(length=63), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["environment_id", "organization_id"],
            ["environments.id", "environments.organization_id"],
            name="fk_targets_environment_scope",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id", "organization_id", "environment_id", name="uq_targets_id_scope"),
        sa.UniqueConstraint(
            "organization_id", "environment_id", "name", name="uq_targets_scope_name"
        ),
    )
    op.create_table(
        "identities",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("environment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("password_hash", sa.String(length=512), nullable=False),
        sa.Column("roles", postgresql.ARRAY(sa.String(length=32)), nullable=False),
        sa.Column("scopes", postgresql.ARRAY(sa.String(length=128)), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("credential_version", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.CheckConstraint("credential_version > 0", name="ck_identities_credential_version"),
        sa.ForeignKeyConstraint(
            ["environment_id", "organization_id"],
            ["environments.id", "environments.organization_id"],
            name="fk_identities_environment_scope",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "username", name="uq_identities_org_username"),
        sa.UniqueConstraint(
            "id", "organization_id", "environment_id", name="uq_identities_id_scope"
        ),
    )
    op.create_table(
        "sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("identity_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("token_sha256", sa.String(length=64), nullable=False),
        sa.Column("credential_version", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("credential_version > 0", name="ck_sessions_credential_version"),
        sa.ForeignKeyConstraint(["identity_id"], ["identities.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token_sha256", name="uq_sessions_token_sha256"),
    )
    op.create_index(
        "ix_sessions_identity_active",
        "sessions",
        ["identity_id", "expires_at", "revoked_at"],
        unique=False,
    )
    op.create_table(
        "runs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("request_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("correlation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("environment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("target_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("actor_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("idempotency_key", sa.String(length=128), nullable=False),
        sa.Column("request_sha256", sa.String(length=64), nullable=False),
        sa.Column("action", sa.String(length=128), nullable=False),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("locale", sa.String(length=2), nullable=False),
        sa.Column("parameters", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("result", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("error", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "status IN ('pending', 'running', 'succeeded', 'failed')", name="ck_runs_status"
        ),
        sa.CheckConstraint("locale IN ('en', 'fa')", name="ck_runs_locale"),
        sa.ForeignKeyConstraint(
            ["actor_id", "organization_id", "environment_id"],
            ["identities.id", "identities.organization_id", "identities.environment_id"],
            name="fk_runs_actor_scope",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["target_id", "organization_id", "environment_id"],
            ["targets.id", "targets.organization_id", "targets.environment_id"],
            name="fk_runs_target_scope",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("request_id", name="uq_runs_request_id"),
        sa.UniqueConstraint(
            "organization_id", "actor_id", "idempotency_key", name="uq_runs_actor_idempotency"
        ),
        sa.UniqueConstraint("id", "organization_id", "environment_id", name="uq_runs_id_scope"),
    )
    op.create_index(
        "ix_runs_scope_status_created",
        "runs",
        ["organization_id", "environment_id", "status", "created_at"],
        unique=False,
    )
    op.create_table(
        "run_leases",
        sa.Column("run_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("owner_id", sa.String(length=128), nullable=False),
        sa.Column("lease_token_sha256", sa.String(length=64), nullable=False),
        sa.Column("generation", sa.Integer(), nullable=False),
        sa.Column("acquired_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("heartbeat_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "expires_at > acquired_at", name="ck_run_leases_expiry_after_acquisition"
        ),
        sa.CheckConstraint("generation > 0", name="ck_run_leases_generation"),
        sa.ForeignKeyConstraint(["run_id"], ["runs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("run_id"),
        sa.UniqueConstraint("lease_token_sha256", name="uq_run_leases_token_sha256"),
    )
    op.create_index("ix_run_leases_expiry", "run_leases", ["expires_at"], unique=False)
    op.create_table(
        "audit_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("environment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("actor_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("run_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("correlation_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("event_type", sa.String(length=128), nullable=False),
        sa.Column("outcome", sa.String(length=16), nullable=False),
        sa.Column(
            "occurred_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("details", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.CheckConstraint(
            "outcome IN ('accepted', 'denied', 'failed')", name="ck_audit_events_outcome"
        ),
        sa.ForeignKeyConstraint(
            ["environment_id", "organization_id"],
            ["environments.id", "environments.organization_id"],
            name="fk_audit_events_environment_scope",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["actor_id", "organization_id", "environment_id"],
            ["identities.id", "identities.organization_id", "identities.environment_id"],
            name="fk_audit_events_actor_scope",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["run_id", "organization_id", "environment_id"],
            ["runs.id", "runs.organization_id", "runs.environment_id"],
            name="fk_audit_events_run_scope",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_audit_events_correlation", "audit_events", ["correlation_id"], unique=False)
    op.create_index(
        "ix_audit_events_scope_time",
        "audit_events",
        ["organization_id", "environment_id", "occurred_at"],
        unique=False,
    )

    op.execute(AUDIT_GUARD_SQL)
    op.execute(GRANT_SQL)


def downgrade() -> None:
    """Remove only this application's schema objects; shared group roles remain."""

    op.execute("DROP TRIGGER IF EXISTS trg_audit_events_append_only ON audit_events")
    op.execute("DROP FUNCTION IF EXISTS nextops_prevent_audit_mutation()")
    op.drop_index("ix_audit_events_scope_time", table_name="audit_events")
    op.drop_index("ix_audit_events_correlation", table_name="audit_events")
    op.drop_table("audit_events")
    op.drop_index("ix_run_leases_expiry", table_name="run_leases")
    op.drop_table("run_leases")
    op.drop_index("ix_runs_scope_status_created", table_name="runs")
    op.drop_table("runs")
    op.drop_index("ix_sessions_identity_active", table_name="sessions")
    op.drop_table("sessions")
    op.drop_table("identities")
    op.drop_table("targets")
    op.drop_table("environments")
    op.drop_table("organizations")
