"""Machine-stable errors for application and policy boundaries."""

from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, JsonValue


class ErrorCode(StrEnum):
    """Codes safe for programmatic handling across interfaces."""

    INVALID_REQUEST = "invalid_request"
    UNAUTHENTICATED = "unauthenticated"
    POLICY_DENIED = "policy_denied"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    OVERLOADED = "overloaded"
    TIMEOUT = "timeout"
    DEPENDENCY_UNAVAILABLE = "dependency_unavailable"
    INTERNAL_ERROR = "internal_error"


class ErrorDetail(BaseModel):
    """Localized-message reference without embedding secrets or raw exceptions."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    code: ErrorCode
    message_key: str = Field(pattern=r"^[a-z][a-z0-9_.-]{2,127}$")
    correlation_id: UUID
    retryable: bool = False
    details: dict[str, JsonValue] = Field(default_factory=dict, max_length=32)
