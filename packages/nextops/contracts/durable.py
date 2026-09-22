"""Durable application and API contracts for Stage 1A Increment 2."""

from enum import StrEnum
from typing import Annotated, Literal
from uuid import UUID

from pydantic import AwareDatetime, Field, JsonValue, SecretStr

from nextops.contracts.assistant import AssistantResponse
from nextops.contracts.errors import ErrorCode, ErrorDetail
from nextops.contracts.models import (
    ActionName,
    ActorContext,
    FrozenContract,
    ParameterName,
    ScopeName,
)
from nextops.contracts.monitoring import MonitoringSummary

Slug = Annotated[str, Field(pattern=r"^[a-z][a-z0-9-]{1,62}$")]
Username = Annotated[str, Field(pattern=r"^[a-z][a-z0-9_.-]{2,63}$")]


class RunStatus(StrEnum):
    """Stable lifecycle states for durable investigations."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class AuditOutcome(StrEnum):
    """Stable outcomes for append-only security and workflow events."""

    ACCEPTED = "accepted"
    DENIED = "denied"
    FAILED = "failed"


class BootstrapRequest(FrozenContract):
    """One-time local installation input; the bootstrap secret is an HTTP header."""

    organization_slug: Slug
    organization_name: str = Field(min_length=1, max_length=128)
    environment_slug: Slug
    environment_name: str = Field(min_length=1, max_length=128)
    admin_username: Username
    admin_password: SecretStr = Field(min_length=14, max_length=256)


class LoginRequest(FrozenContract):
    """Local credential exchange for an opaque expiring bearer session."""

    username: Username
    password: SecretStr = Field(min_length=1, max_length=256)


class RecoveryRequest(FrozenContract):
    """Local recovery input; the recovery secret is supplied separately."""

    admin_username: Username
    new_password: SecretStr = Field(min_length=14, max_length=256)


class SessionToken(FrozenContract):
    """Opaque bearer token returned once and never stored in plaintext."""

    access_token: str = Field(min_length=32, max_length=256, repr=False)
    token_type: Literal["bearer"] = "bearer"
    expires_at: AwareDatetime


class AuthenticatedSession(FrozenContract):
    """Server-derived actor plus a newly issued bearer token."""

    actor: ActorContext
    session: SessionToken


class BootstrapResult(FrozenContract):
    """Identifiers created atomically by the one-time installation bootstrap."""

    organization_id: UUID
    environment_id: UUID
    admin_identity_id: UUID
    fixture_target_id: UUID
    authenticated_session: AuthenticatedSession


class RecoveryResult(FrozenContract):
    """Credential-rotation receipt; login is required after recovery."""

    identity_id: UUID
    revoked_session_count: int = Field(ge=0)
    credential_version: int = Field(ge=2)


class RunCreateRequest(FrozenContract):
    """Untrusted run intent; actor and scope are always derived server-side."""

    target_id: UUID
    action: ActionName
    question: str = Field(min_length=1, max_length=2_000)
    locale: Literal["en", "fa"]
    parameters: dict[ParameterName, JsonValue] = Field(default_factory=dict, max_length=64)


class EvidenceSource(FrozenContract):
    """Explicit source and time for a displayed answer."""

    connector: str = Field(pattern=r"^[a-z][a-z0-9_-]{2,63}$")
    method: str = Field(pattern=r"^[a-z][a-z0-9_.-]{2,127}$")
    collected_at: AwareDatetime
    measured_at: AwareDatetime | None = None


class FixtureResult(FrozenContract):
    """First deterministic bilingual result with provenance and limitations."""

    result_type: Literal["fixture"] = "fixture"
    run_id: UUID
    status: RunStatus
    locale: Literal["en", "fa"]
    answer: str = Field(min_length=1, max_length=8_000)
    source: EvidenceSource
    organization_id: UUID
    environment_id: UUID
    target_id: UUID
    is_partial: bool
    is_stale: bool
    errors: tuple[ErrorDetail, ...] = Field(default_factory=tuple, max_length=32)
    audit_event_id: UUID


class LiveInvestigationResult(FrozenContract):
    """Durable model result linked to the exact bounded monitoring snapshot."""

    result_type: Literal["live_monitoring"] = "live_monitoring"
    run_id: UUID
    status: RunStatus
    locale: Literal["en", "fa"]
    assistant: AssistantResponse
    evidence: MonitoringSummary
    evidence_reference: str = Field(pattern=r"^run-evidence:[0-9a-f-]{36}$")
    evidence_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    organization_id: UUID
    environment_id: UUID
    target_id: UUID
    is_partial: bool
    is_stale: bool
    audit_event_id: UUID


class RunFailure(FrozenContract):
    """Safe durable failure metadata without raw exceptions or dependency payloads."""

    code: ErrorCode
    message_key: str = Field(pattern=r"^[a-z][a-z0-9_.-]{2,127}$")
    retryable: bool = False


class RunRecord(FrozenContract):
    """Public durable-run representation without credential or lease secrets."""

    run_id: UUID
    request_id: UUID
    correlation_id: UUID
    status: RunStatus
    locale: Literal["en", "fa"]
    created_at: AwareDatetime
    updated_at: AwareDatetime
    result: FixtureResult | LiveInvestigationResult | None = None
    error: RunFailure | None = None


class LeaseGrant(FrozenContract):
    """Opaque, expiring worker ownership returned only to the claimant."""

    run_id: UUID
    owner_id: str = Field(pattern=r"^[a-zA-Z0-9_.:-]{3,128}$")
    lease_token: str = Field(min_length=32, max_length=256, repr=False)
    generation: int = Field(ge=1)
    acquired_at: AwareDatetime
    expires_at: AwareDatetime


class AuditRecord(FrozenContract):
    """Serializable view of an append-only audit event."""

    audit_event_id: UUID
    organization_id: UUID
    environment_id: UUID
    actor_id: UUID | None = None
    run_id: UUID | None = None
    correlation_id: UUID
    event_type: str = Field(pattern=r"^[a-z][a-z0-9_.-]{2,127}$")
    outcome: AuditOutcome
    occurred_at: AwareDatetime
    details: dict[str, JsonValue] = Field(default_factory=dict, max_length=64)
    required_scopes: frozenset[ScopeName] = Field(default_factory=frozenset, max_length=128)
