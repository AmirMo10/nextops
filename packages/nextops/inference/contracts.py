"""Strict runtime-neutral contracts for local inference."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Literal, Protocol
from uuid import UUID

from pydantic import AwareDatetime, Field, model_validator

from nextops.contracts.models import FrozenContract

MODEL_ID = "nextops-qwen3-8b-q4-k-m"


class FinishReason(StrEnum):
    """Accepted completion states from the selected provider route."""

    STOP = "stop"
    LENGTH = "length"


class ReadinessState(StrEnum):
    """Safe provider readiness states exposed to operators."""

    READY = "ready"
    LOADING = "loading"
    UNAVAILABLE = "unavailable"
    DEGRADED = "degraded"


class InferenceRequest(FrozenContract):
    """Trusted wrapper request after HTTP authentication and validation."""

    request_id: UUID
    correlation_id: UUID
    locale: Literal["en", "fa"]
    prompt: str = Field(min_length=1, max_length=12_000)
    max_output_tokens: int = Field(default=512, ge=1, le=1_024)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class ProviderGeneration(FrozenContract):
    """Validated provider result before request metadata is attached."""

    answer: str = Field(min_length=1, max_length=16_000)
    model_id: Literal["nextops-qwen3-8b-q4-k-m"]
    prompt_tokens: int = Field(ge=0, le=65_536)
    completion_tokens: int = Field(ge=0, le=1_024)
    finish_reason: FinishReason
    started_at: AwareDatetime
    completed_at: AwareDatetime

    @model_validator(mode="after")
    def timestamps_are_ordered(self) -> ProviderGeneration:
        if self.completed_at < self.started_at:
            raise ValueError("completed_at must not precede started_at")
        return self


class InferenceResult(ProviderGeneration):
    """Public generation result with request identity and queue evidence."""

    request_id: UUID
    correlation_id: UUID
    locale: Literal["en", "fa"]
    queue_ms: int = Field(ge=0)
    cpu_only_required: Literal[True]


class ProviderReadiness(FrozenContract):
    """Provider status without paths, secrets, prompts, or raw errors."""

    state: ReadinessState
    model_id: Literal["nextops-qwen3-8b-q4-k-m"]
    runtime_version: str = Field(pattern=r"^v[0-9]+\.[0-9]+\.[0-9]+$")
    cpu_only_required: Literal[True]


class InferenceReadiness(ProviderReadiness):
    """Provider readiness plus bounded-scheduler counters."""

    max_active_requests: Literal[1]
    max_queued_requests: Literal[2]
    active_requests: int = Field(ge=0, le=1)
    queued_requests: int = Field(ge=0, le=2)


class LLMProvider(Protocol):
    """Runtime-neutral provider interface used by the scheduler."""

    async def generate(self, request: InferenceRequest) -> ProviderGeneration: ...

    async def readiness(self) -> ProviderReadiness: ...


def elapsed_milliseconds(started: float, completed: float) -> int:
    """Convert a monotonic duration to a non-negative integer."""

    return max(0, round((completed - started) * 1_000))


def ordered_now_pair(started_at: datetime, completed_at: datetime) -> tuple[datetime, datetime]:
    """Keep a narrow helper for provider implementations that capture timestamps."""

    return started_at, max(started_at, completed_at)
