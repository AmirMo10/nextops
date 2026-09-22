"""Contracts for source-qualified monitoring evidence."""

from typing import Literal, Self
from uuid import UUID

from pydantic import AwareDatetime, Field, model_validator

from nextops.contracts.assistant import AssistantResponse
from nextops.contracts.models import FrozenContract

MonitoringPartialReason = Literal[
    "metrics_truncated",
    "problems_truncated",
    "no_usable_metrics",
]


class MonitoringMetric(FrozenContract):
    """One bounded latest-value observation returned by the read-only connector."""

    name: str = Field(min_length=1, max_length=256)
    key: str = Field(min_length=1, max_length=256)
    value: str = Field(min_length=1, max_length=256)
    units: str = Field(default="", max_length=32)
    measured_at: AwareDatetime
    stale: bool


class MonitoringProblem(FrozenContract):
    """One active Zabbix problem visible to the scoped API identity."""

    name: str = Field(min_length=1, max_length=512)
    severity: int = Field(ge=0, le=5)
    started_at: AwareDatetime


class MonitoringSummary(FrozenContract):
    """A current, attributable snapshot from the connector boundary."""

    source: Literal["zabbix"] = "zabbix"
    source_version: str = Field(pattern=r"^7\.0\.\d+$")
    host: str = Field(min_length=1, max_length=128)
    collected_at: AwareDatetime
    metrics: tuple[MonitoringMetric, ...] = Field(max_length=8)
    active_problems: tuple[MonitoringProblem, ...] = Field(max_length=25)
    is_partial: bool = False
    partial_reasons: tuple[MonitoringPartialReason, ...] = Field(
        default_factory=tuple,
        max_length=3,
    )

    @model_validator(mode="after")
    def validate_partial_marker(self) -> Self:
        """Require the public marker and its machine-readable reasons to agree."""

        if self.is_partial != bool(self.partial_reasons):
            raise ValueError("is_partial must match partial_reasons")
        return self


class InvestigationResponse(FrozenContract):
    """Model synthesis paired with the exact monitoring evidence supplied to it."""

    assistant: AssistantResponse
    evidence: MonitoringSummary
    run_id: UUID
    evidence_reference: str = Field(pattern=r"^run-evidence:[0-9a-f-]{36}$")
    evidence_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    audit_event_id: UUID
    evidence_mode: Literal["live_zabbix"] = "live_zabbix"
    live_monitoring_data: Literal[True] = True
