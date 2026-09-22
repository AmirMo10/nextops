"""Authenticated user-testing contracts for the local assistant panel."""

from typing import Literal
from uuid import UUID

from pydantic import AwareDatetime, Field

from nextops.contracts.models import FrozenContract
from nextops.inference.contracts import FinishReason


class AssistantRequest(FrozenContract):
    """A bounded model-only question submitted by an authenticated user."""

    locale: Literal["en", "fa"]
    question: str = Field(min_length=1, max_length=4_000)
    max_output_tokens: int = Field(default=384, ge=32, le=512)


class AssistantResponse(FrozenContract):
    """A model result whose evidence limitations are explicit and machine-readable."""

    request_id: UUID
    correlation_id: UUID
    locale: Literal["en", "fa"]
    answer: str = Field(min_length=1, max_length=16_000)
    model_id: Literal["nextops-qwen3-8b-q4-k-m"]
    prompt_tokens: int = Field(ge=0, le=65_536)
    completion_tokens: int = Field(ge=0, le=512)
    finish_reason: FinishReason
    started_at: AwareDatetime
    completed_at: AwareDatetime
    queue_ms: int = Field(ge=0)
    cpu_only_required: Literal[True]
    evidence_mode: Literal["model_only"] = "model_only"
    live_monitoring_data: Literal[False] = False
