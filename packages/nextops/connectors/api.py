"""Authenticated loopback API for read-only monitoring evidence."""

from __future__ import annotations

import secrets
from typing import Annotated, Protocol

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from nextops.application.errors import ApplicationError
from nextops.connectors.configuration import ConnectorSettings
from nextops.connectors.linux import (
    IncidentEvidenceClient,
    LinuxReadClient,
    LinuxTargetRegistry,
    SshLinuxTransport,
)
from nextops.connectors.zabbix import HttpsZabbixTransport, ZabbixReadClient
from nextops.contracts.errors import ErrorCode
from nextops.contracts.incidents import IncidentEvidence
from nextops.contracts.linux import LinuxDiagnosticSnapshot
from nextops.contracts.monitoring import MonitoringIncidentContext, MonitoringSummary

BearerCredentials = Annotated[
    HTTPAuthorizationCredentials | None,
    Depends(HTTPBearer(auto_error=False)),
]


class MonitoringClient(Protocol):
    """Narrow connector boundary for API tests."""

    async def summary(self) -> MonitoringSummary: ...

    async def incident_context(self) -> MonitoringIncidentContext: ...


class Phase2EvidenceClient(Protocol):
    """Narrow Phase 2 connector boundary used by API tests."""

    async def linux_snapshot(self, target_id: str) -> LinuxDiagnosticSnapshot: ...

    async def evidence(self, target_id: str) -> IncidentEvidence: ...


def create_connector_app(
    client: MonitoringClient,
    service_secret: str,
    phase2_client: Phase2EvidenceClient | None = None,
) -> FastAPI:
    """Build a protected connector API that exposes no generic proxy surface."""

    app = FastAPI(title="NextOps read-only connector", version="1.0.0")

    @app.exception_handler(ApplicationError)
    async def application_error_handler(_request: object, error: ApplicationError) -> JSONResponse:
        status_by_code = {
            ErrorCode.UNAUTHENTICATED: 401,
            ErrorCode.POLICY_DENIED: 403,
            ErrorCode.TIMEOUT: 504,
        }
        status = status_by_code.get(error.code, 503)
        return JSONResponse(
            status_code=status,
            content={
                "error": {
                    "code": error.code.value,
                    "message_key": error.message_key,
                    "retryable": error.retryable,
                }
            },
        )

    def authenticate(
        credentials: BearerCredentials,
    ) -> None:
        if (
            credentials is None
            or credentials.scheme.lower() != "bearer"
            or not secrets.compare_digest(credentials.credentials, service_secret)
        ):
            raise ApplicationError(ErrorCode.UNAUTHENTICATED, "connector.auth_required")

    @app.get("/healthz")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "nextops-connectors-ro"}

    @app.get(
        "/api/v1/zabbix/summary",
        response_model=MonitoringSummary,
        dependencies=[Depends(authenticate)],
    )
    async def zabbix_summary() -> MonitoringSummary:
        return await client.summary()

    @app.get(
        "/api/v1/zabbix/incident-context",
        response_model=MonitoringIncidentContext,
        dependencies=[Depends(authenticate)],
    )
    async def zabbix_incident_context() -> MonitoringIncidentContext:
        return await client.incident_context()

    @app.get(
        "/api/v1/linux/{target_id}/snapshot",
        response_model=LinuxDiagnosticSnapshot,
        dependencies=[Depends(authenticate)],
    )
    async def linux_snapshot(target_id: str) -> LinuxDiagnosticSnapshot:
        if phase2_client is None:
            raise ApplicationError(
                ErrorCode.DEPENDENCY_UNAVAILABLE,
                "connector.linux_not_configured",
                retryable=True,
            )
        return await phase2_client.linux_snapshot(target_id)

    @app.get(
        "/api/v1/incidents/{target_id}/evidence",
        response_model=IncidentEvidence,
        dependencies=[Depends(authenticate)],
    )
    async def incident_evidence(target_id: str) -> IncidentEvidence:
        if phase2_client is None:
            raise ApplicationError(
                ErrorCode.DEPENDENCY_UNAVAILABLE,
                "connector.phase2_not_configured",
                retryable=True,
            )
        return await phase2_client.evidence(target_id)

    return app


def create_runtime_connector_app() -> FastAPI:
    """Create the production connector from protected deployment settings."""

    settings = ConnectorSettings.from_environment()
    transport = HttpsZabbixTransport(
        settings.zabbix_api_url,
        settings.zabbix_ca_file,
        settings.zabbix_api_token.get_secret_value(),
        settings.request_timeout_seconds,
    )
    phase2_client = None
    if settings.linux_targets_file is not None:
        registry = LinuxTargetRegistry.from_file(settings.linux_targets_file)
        linux_client = LinuxReadClient(
            registry,
            SshLinuxTransport(
                registry.known_hosts_file,
                timeout_seconds=settings.linux_timeout_seconds,
            ),
        )
        phase2_client = IncidentEvidenceClient(
            registry,
            transport,
            linux_client,
            incident_lookback_minutes=settings.incident_lookback_minutes,
        )
    return create_connector_app(
        ZabbixReadClient(
            settings.zabbix_host,
            transport,
            incident_lookback_minutes=settings.incident_lookback_minutes,
        ),
        settings.service_auth_secret.get_secret_value(),
        phase2_client,
    )
