"""SQLAlchemy mappings for the PostgreSQL-first durable application slice."""

from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import (
    ARRAY,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base for authoritative PostgreSQL mappings."""


class TimestampMixin:
    """Server-authored timezone-aware creation and update timestamps."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )


class Organization(Base):
    """Initial single organization, protected by a singleton database constraint."""

    __tablename__ = "organizations"
    __table_args__ = (
        CheckConstraint("singleton_key = 1", name="ck_organizations_singleton"),
        UniqueConstraint("singleton_key", name="uq_organizations_singleton"),
    )

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    singleton_key: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)
    slug: Mapped[str] = mapped_column(String(63), nullable=False, unique=True)
    display_name: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class Environment(Base):
    """Organization-scoped local environment."""

    __tablename__ = "environments"
    __table_args__ = (
        UniqueConstraint("organization_id", "slug", name="uq_environments_org_slug"),
        UniqueConstraint("id", "organization_id", name="uq_environments_id_org"),
    )

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("organizations.id", ondelete="RESTRICT"), nullable=False
    )
    slug: Mapped[str] = mapped_column(String(63), nullable=False)
    display_name: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class Target(Base):
    """Authorized local target identity without connection credentials."""

    __tablename__ = "targets"
    __table_args__ = (
        ForeignKeyConstraint(
            ["environment_id", "organization_id"],
            ["environments.id", "environments.organization_id"],
            name="fk_targets_environment_scope",
            ondelete="RESTRICT",
        ),
        UniqueConstraint("id", "organization_id", "environment_id", name="uq_targets_id_scope"),
        UniqueConstraint("organization_id", "environment_id", "name", name="uq_targets_scope_name"),
    )

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    environment_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    kind: Mapped[str] = mapped_column(String(63), nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class Identity(Base, TimestampMixin):
    """Local user identity and server-owned authorization attributes."""

    __tablename__ = "identities"
    __table_args__ = (
        ForeignKeyConstraint(
            ["environment_id", "organization_id"],
            ["environments.id", "environments.organization_id"],
            name="fk_identities_environment_scope",
            ondelete="RESTRICT",
        ),
        UniqueConstraint("organization_id", "username", name="uq_identities_org_username"),
        UniqueConstraint("id", "organization_id", "environment_id", name="uq_identities_id_scope"),
        CheckConstraint("credential_version > 0", name="ck_identities_credential_version"),
    )

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    environment_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    username: Mapped[str] = mapped_column(String(64), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(512), nullable=False)
    roles: Mapped[list[str]] = mapped_column(ARRAY(String(32)), nullable=False)
    scopes: Mapped[list[str]] = mapped_column(ARRAY(String(128)), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    credential_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)


class Session(Base):
    """Opaque session whose plaintext bearer token is never persisted."""

    __tablename__ = "sessions"
    __table_args__ = (
        CheckConstraint("credential_version > 0", name="ck_sessions_credential_version"),
        Index("ix_sessions_identity_active", "identity_id", "expires_at", "revoked_at"),
    )

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    identity_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("identities.id", ondelete="CASCADE"), nullable=False
    )
    token_sha256: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    credential_version: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Run(Base, TimestampMixin):
    """Durable, idempotent investigation intent and eventual result."""

    __tablename__ = "runs"
    __table_args__ = (
        ForeignKeyConstraint(
            ["target_id", "organization_id", "environment_id"],
            ["targets.id", "targets.organization_id", "targets.environment_id"],
            name="fk_runs_target_scope",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["actor_id", "organization_id", "environment_id"],
            ["identities.id", "identities.organization_id", "identities.environment_id"],
            name="fk_runs_actor_scope",
            ondelete="RESTRICT",
        ),
        UniqueConstraint(
            "organization_id", "actor_id", "idempotency_key", name="uq_runs_actor_idempotency"
        ),
        UniqueConstraint("id", "organization_id", "environment_id", name="uq_runs_id_scope"),
        CheckConstraint(
            "status IN ('pending', 'running', 'succeeded', 'failed')",
            name="ck_runs_status",
        ),
        CheckConstraint("locale IN ('en', 'fa')", name="ck_runs_locale"),
        Index(
            "ix_runs_scope_status_created",
            "organization_id",
            "environment_id",
            "status",
            "created_at",
        ),
    )

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    request_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False, unique=True)
    correlation_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    organization_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    environment_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    target_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    actor_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(128), nullable=False)
    request_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    action: Mapped[str] = mapped_column(String(128), nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    locale: Mapped[str] = mapped_column(String(2), nullable=False)
    parameters: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(16), nullable=False, default="pending")
    result: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    error: Mapped[dict[str, Any] | None] = mapped_column(JSONB)


class RunLease(Base):
    """Single atomic, expiring worker ownership record for a run."""

    __tablename__ = "run_leases"
    __table_args__ = (
        CheckConstraint("expires_at > acquired_at", name="ck_run_leases_expiry_after_acquisition"),
        CheckConstraint("generation > 0", name="ck_run_leases_generation"),
        Index("ix_run_leases_expiry", "expires_at"),
    )

    run_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("runs.id", ondelete="CASCADE"), primary_key=True
    )
    owner_id: Mapped[str] = mapped_column(String(128), nullable=False)
    lease_token_sha256: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    generation: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    acquired_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    heartbeat_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class AuditEvent(Base):
    """Append-only audit record; migration adds database mutation guards."""

    __tablename__ = "audit_events"
    __table_args__ = (
        ForeignKeyConstraint(
            ["environment_id", "organization_id"],
            ["environments.id", "environments.organization_id"],
            name="fk_audit_events_environment_scope",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["actor_id", "organization_id", "environment_id"],
            ["identities.id", "identities.organization_id", "identities.environment_id"],
            name="fk_audit_events_actor_scope",
            ondelete="RESTRICT",
        ),
        ForeignKeyConstraint(
            ["run_id", "organization_id", "environment_id"],
            ["runs.id", "runs.organization_id", "runs.environment_id"],
            name="fk_audit_events_run_scope",
            ondelete="RESTRICT",
        ),
        CheckConstraint(
            "outcome IN ('accepted', 'denied', 'failed')", name="ck_audit_events_outcome"
        ),
        Index(
            "ix_audit_events_scope_time",
            "organization_id",
            "environment_id",
            "occurred_at",
        ),
        Index("ix_audit_events_correlation", "correlation_id"),
    )

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    environment_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    actor_id: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True))
    run_id: Mapped[UUID | None] = mapped_column(PGUUID(as_uuid=True))
    correlation_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), nullable=False)
    event_type: Mapped[str] = mapped_column(String(128), nullable=False)
    outcome: Mapped[str] = mapped_column(String(16), nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    details: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
