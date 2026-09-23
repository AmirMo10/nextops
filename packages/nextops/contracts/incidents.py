"""Composite Phase 2 incident request, evidence, and response contracts."""

from __future__ import annotations

from typing import Literal, Self
from uuid import UUID

from pydantic import Field, model_validator

from nextops.contracts.assistant import AssistantResponse
from nextops.contracts.linux import LinuxDiagnosticSnapshot, LinuxTargetId
from nextops.contracts.models import FrozenContract
from nextops.contracts.monitoring import MonitoringIncidentContext


class IncidentInvestigationRequest(FrozenContract):
    """One authenticated incident question for a configured immutable target."""

    target_id: LinuxTargetId
    locale: Literal["en", "fa"]
    question: str = Field(min_length=1, max_length=4_000)
    max_output_tokens: int = Field(default=128, ge=32, le=128)


class IncidentTargetsResponse(FrozenContract):
    """Configured logical targets exposed without connection details."""

    targets: tuple[LinuxTargetId, ...] = Field(max_length=8)


class IncidentEvidence(FrozenContract):
    """Exact bounded Zabbix and direct Linux evidence supplied to the model."""

    target_id: LinuxTargetId
    zabbix: MonitoringIncidentContext
    linux: LinuxDiagnosticSnapshot
    is_partial: bool
    partial_reasons: tuple[str, ...] = Field(max_length=16)

    @model_validator(mode="after")
    def validate_evidence(self) -> Self:
        if self.linux.target_id != self.target_id:
            raise ValueError("Linux evidence target does not match incident target")
        expected_partial = self.zabbix.is_partial or self.linux.is_partial
        if self.is_partial != expected_partial:
            raise ValueError("combined partial marker does not match source evidence")
        if self.is_partial != bool(self.partial_reasons):
            raise ValueError("combined partial marker must match its reasons")
        if len(set(self.partial_reasons)) != len(self.partial_reasons):
            raise ValueError("combined partial reasons must be unique")
        return self

    @classmethod
    def combine(
        cls,
        target_id: str,
        zabbix: MonitoringIncidentContext,
        linux: LinuxDiagnosticSnapshot,
    ) -> IncidentEvidence:
        reasons = tuple(
            [f"zabbix:{reason}" for reason in zabbix.partial_reasons]
            + [f"linux:{reason}" for reason in linux.partial_reasons]
        )
        return cls(
            target_id=target_id,
            zabbix=zabbix,
            linux=linux,
            is_partial=zabbix.is_partial or linux.is_partial,
            partial_reasons=reasons,
        )


class IncidentInvestigationResponse(FrozenContract):
    """Durable locally generated answer paired with the exact Phase 2 evidence."""

    assistant: AssistantResponse
    evidence: IncidentEvidence
    run_id: UUID
    evidence_reference: str = Field(pattern=r"^run-evidence:[0-9a-f-]{36}$")
    evidence_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    audit_event_id: UUID
    evidence_mode: Literal["live_zabbix_linux"] = "live_zabbix_linux"
    live_monitoring_data: Literal[True] = True
