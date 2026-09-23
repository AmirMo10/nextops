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

IncidentPartialReason = (
    MonitoringPartialReason
    | Literal[
        "history_metrics_truncated",
        "history_points_truncated",
        "events_truncated",
    ]
)


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


class MonitoringHistoryPoint(FrozenContract):
    """One bounded historical value for an explicitly selected numeric item."""

    name: str = Field(min_length=1, max_length=256)
    key: str = Field(min_length=1, max_length=256)
    value: str = Field(min_length=1, max_length=256)
    units: str = Field(default="", max_length=32)
    measured_at: AwareDatetime


class MonitoringEvent(FrozenContract):
    """One bounded trigger event in the configured incident window."""

    event_id: str = Field(pattern=r"^[0-9]+$", max_length=32)
    name: str = Field(min_length=1, max_length=512)
    severity: int = Field(ge=0, le=5)
    occurred_at: AwareDatetime
    state: Literal["problem", "recovery"]
    acknowledged: bool
    suppressed: bool


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


class MonitoringIncidentContext(FrozenContract):
    """A bounded current snapshot plus recent numeric history and trigger events."""

    source: Literal["zabbix"] = "zabbix"
    source_version: str = Field(pattern=r"^7\.0\.\d+$")
    host: str = Field(min_length=1, max_length=128)
    collected_at: AwareDatetime
    window_started_at: AwareDatetime
    window_ended_at: AwareDatetime
    summary: MonitoringSummary
    history: tuple[MonitoringHistoryPoint, ...] = Field(max_length=32)
    events: tuple[MonitoringEvent, ...] = Field(max_length=25)
    is_partial: bool = False
    partial_reasons: tuple[IncidentPartialReason, ...] = Field(
        default_factory=tuple,
        max_length=6,
    )

    @model_validator(mode="after")
    def validate_incident_context(self) -> Self:
        """Keep source identity, time bounds, and partial markers internally consistent."""

        if self.window_started_at >= self.window_ended_at:
            raise ValueError("incident window must have positive duration")
        if self.window_ended_at != self.collected_at:
            raise ValueError("incident window must end at collection time")
        if any(
            point.measured_at < self.window_started_at or point.measured_at > self.window_ended_at
            for point in self.history
        ):
            raise ValueError("history point falls outside the incident window")
        if any(
            event.occurred_at < self.window_started_at or event.occurred_at > self.window_ended_at
            for event in self.events
        ):
            raise ValueError("event falls outside the incident window")
        if (
            self.summary.source != self.source
            or self.summary.source_version != self.source_version
            or self.summary.host != self.host
            or self.summary.collected_at != self.collected_at
        ):
            raise ValueError("incident context source must match its summary")
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
