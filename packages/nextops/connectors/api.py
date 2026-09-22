"""Authenticated loopback API for read-only monitoring evidence."""

from __future__ import annotations

import secrets
from typing import Annotated, Protocol

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from nextops.application.errors import ApplicationError
from nextops.connectors.configuration import ConnectorSettings
from nextops.connectors.zabbix import HttpsZabbixTransport, ZabbixReadClient
from nextops.contracts.errors import ErrorCode
from nextops.contracts.monitoring import MonitoringSummary

BearerCredentials = Annotated[
    HTTPAuthorizationCredentials | None,
    Depends(HTTPBearer(auto_error=False)),
]


class MonitoringClient(Protocol):
    """Narrow connector boundary for API tests."""

    async def summary(self) -> MonitoringSummary: ...


def create_connector_app(client: MonitoringClient, service_secret: str) -> FastAPI:
    """Build a protected connector API that exposes no generic proxy surface."""

    app = FastAPI(title="NextOps read-only connector", version="1.0.0")

    @app.exception_handler(ApplicationError)
    async def application_error_handler(_request: object, error: ApplicationError) -> JSONResponse:
        status = 401 if error.code is ErrorCode.UNAUTHENTICATED else 503
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
    return create_connector_app(
        ZabbixReadClient(settings.zabbix_host, transport),
        settings.service_auth_secret.get_secret_value(),
    )
