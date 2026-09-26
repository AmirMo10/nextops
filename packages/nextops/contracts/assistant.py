"""Authenticated user-testing contracts for the local assistant panel."""

from typing import Literal, Self
from uuid import UUID

from pydantic import AwareDatetime, Field, model_validator

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
    evidence_mode: Literal["model_only", "live_zabbix", "live_zabbix_linux"] = "model_only"
    live_monitoring_data: bool = False
    integrity_status: Literal[
        "model_unverified",
        "evidence_bounded",
        "deterministic_fallback",
        "deterministic_focus",
        "scope_redirect",
    ] = "model_unverified"
    limitations: tuple[
        Literal[
            "no_live_evidence",
            "model_output_may_be_incorrect",
            "read_only_no_action_performed",
            "stale_evidence",
            "partial_evidence",
            "file_listing_unavailable",
        ],
        ...,
    ] = Field(
        default=("no_live_evidence", "model_output_may_be_incorrect"),
        max_length=6,
    )

    @model_validator(mode="after")
    def evidence_labels_are_consistent(self) -> Self:
        """Prevent contradictory truthfulness labels at the application boundary."""

        model_only = self.evidence_mode == "model_only"
        if model_only == self.live_monitoring_data:
            raise ValueError("evidence_mode and live_monitoring_data disagree")
        if model_only and self.integrity_status == "evidence_bounded":
            raise ValueError("model-only output cannot be evidence-bounded")
        if not model_only and self.integrity_status in {"model_unverified", "scope_redirect"}:
            raise ValueError("live-evidence output requires an evidence integrity outcome")
        return self
