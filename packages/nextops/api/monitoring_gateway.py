"""Server-side client for the protected connector tunnel."""

from __future__ import annotations

from typing import Protocol

from pydantic import ValidationError

from nextops.application.errors import ApplicationError
from nextops.contracts.errors import ErrorCode
from nextops.contracts.incidents import IncidentEvidence
from nextops.contracts.monitoring import MonitoringIncidentContext, MonitoringSummary
from nextops.inference.llama_cpp import JsonTransport, UrllibJsonTransport


class MonitoringGateway(Protocol):
    """Narrow monitoring boundary used by the application API."""

    async def summary(self) -> MonitoringSummary: ...

    async def incident_context(self) -> MonitoringIncidentContext: ...

    async def incident_evidence(self, target_id: str) -> IncidentEvidence: ...


class LoopbackMonitoringGateway:
    """Retrieve source-qualified evidence through a loopback-only tunnel."""

    def __init__(
        self,
        base_url: str,
        service_auth_secret: str,
        timeout_seconds: float,
        transport: JsonTransport | None = None,
    ) -> None:
        self._transport = transport or UrllibJsonTransport(base_url)
        self._timeout_seconds = timeout_seconds
        self._headers = {
            "Authorization": f"Bearer {service_auth_secret}",
            "Accept": "application/json",
        }

    async def summary(self) -> MonitoringSummary:
        try:
            raw = await self._transport.get_json(
                "/api/v1/zabbix/summary", self._headers, self._timeout_seconds
            )
        except ApplicationError as error:
            raise ApplicationError(
                error.code,
                "connector.summary_unavailable",
                retryable=error.retryable,
            ) from error
        try:
            return MonitoringSummary.model_validate(raw)
        except ValidationError as error:
            raise ApplicationError(
                ErrorCode.DEPENDENCY_UNAVAILABLE,
                "connector.summary_invalid",
                retryable=True,
            ) from error

    async def incident_context(self) -> MonitoringIncidentContext:
        try:
            raw = await self._transport.get_json(
                "/api/v1/zabbix/incident-context", self._headers, self._timeout_seconds
            )
        except ApplicationError as error:
            raise ApplicationError(
                error.code,
                "connector.incident_context_unavailable",
                retryable=error.retryable,
            ) from error
        try:
            return MonitoringIncidentContext.model_validate(raw)
        except ValidationError as error:
            raise ApplicationError(
                ErrorCode.DEPENDENCY_UNAVAILABLE,
                "connector.incident_context_invalid",
                retryable=True,
            ) from error

    async def incident_evidence(self, target_id: str) -> IncidentEvidence:
        try:
            raw = await self._transport.get_json(
                f"/api/v1/incidents/{target_id}/evidence",
                self._headers,
                self._timeout_seconds,
            )
        except ApplicationError as error:
            raise ApplicationError(
                error.code,
                "connector.incident_evidence_unavailable",
                retryable=error.retryable,
            ) from error
        try:
            return IncidentEvidence.model_validate(raw)
        except ValidationError as error:
            raise ApplicationError(
                ErrorCode.DEPENDENCY_UNAVAILABLE,
                "connector.incident_evidence_invalid",
                retryable=True,
            ) from error
