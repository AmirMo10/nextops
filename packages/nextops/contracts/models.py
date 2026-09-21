"""Validated input and evidence contracts for Stage 1A."""

from datetime import datetime
from enum import StrEnum
from typing import Annotated, Literal
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, JsonValue

ActionName = Annotated[str, Field(pattern=r"^[a-z][a-z0-9_.-]{2,127}$")]
ParameterName = Annotated[str, Field(pattern=r"^[a-z][a-z0-9_]{0,63}$")]
ScopeName = Annotated[str, Field(pattern=r"^[a-z][a-z0-9_.-]{2,127}$")]
SourceObjectId = Annotated[str, Field(min_length=1, max_length=256)]
TargetKind = Annotated[str, Field(pattern=r"^[a-z][a-z0-9_]{2,63}$")]


class FrozenContract(BaseModel):
    """Strict immutable base for values crossing a trust boundary."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)


class Role(StrEnum):
    """Initial local roles; policy still evaluates scopes for every request."""

    VIEWER = "viewer"
    OPERATOR = "operator"
    ENGINEER = "engineer"
    ADMIN = "admin"


class ActorContext(FrozenContract):
    """Authenticated identity and its server-derived authorization scope."""

    subject_id: UUID
    organization_id: UUID
    environment_id: UUID
    roles: frozenset[Role] = Field(min_length=1, max_length=4)
    scopes: frozenset[ScopeName] = Field(default_factory=frozenset, max_length=128)


class TargetReference(FrozenContract):
    """Immutable target identity; connection details stay outside this contract."""

    target_id: UUID
    organization_id: UUID
    environment_id: UUID
    kind: TargetKind


class InvestigationRequest(FrozenContract):
    """Untrusted intent; authenticated actor context is supplied separately."""

    request_id: UUID
    correlation_id: UUID
    idempotency_key: str = Field(min_length=8, max_length=128, pattern=r"^[A-Za-z0-9._:-]+$")
    target: TargetReference
    action: ActionName
    question: str = Field(min_length=1, max_length=2_000)
    locale: Literal["en", "fa"]
    parameters: dict[ParameterName, JsonValue] = Field(default_factory=dict, max_length=64)


class EvidenceMetadata(FrozenContract):
    """Provenance and freshness metadata without raw evidence content."""

    evidence_id: UUID
    request_id: UUID
    organization_id: UUID
    environment_id: UUID
    target_id: UUID
    source_connector: str = Field(pattern=r"^[a-z][a-z0-9_-]{2,63}$")
    source_method: str = Field(pattern=r"^[a-z][a-z0-9_.-]{2,127}$")
    source_object_ids: tuple[SourceObjectId, ...] = Field(default_factory=tuple, max_length=1_000)
    collected_at: AwareDatetime
    measured_at: AwareDatetime | None = None
    is_partial: bool
    is_truncated: bool
    is_stale: bool
    content_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    storage_reference: str = Field(min_length=1, max_length=512)

    @property
    def effective_time(self) -> datetime:
        """Return source measurement time when present, else collection time."""

        return self.measured_at or self.collected_at
