"""Fail-closed configuration for the read-only connector service."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Self
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field, SecretStr, model_validator

from nextops.security.deployment_credentials import deployment_secret


class ConnectorSettings(BaseModel):
    """Validated Zabbix and service-auth settings."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    zabbix_api_url: str
    zabbix_ca_file: Path
    zabbix_api_token: SecretStr = Field(min_length=32, max_length=512)
    service_auth_secret: SecretStr = Field(min_length=32, max_length=512)
    zabbix_host: str = Field(min_length=1, max_length=128)
    request_timeout_seconds: float = Field(default=15.0, ge=1.0, le=60.0)

    @model_validator(mode="after")
    def validate_boundary(self) -> Self:
        parsed = urlsplit(self.zabbix_api_url)
        if (
            parsed.scheme != "https"
            or not parsed.hostname
            or parsed.path != "/api_jsonrpc.php"
            or parsed.query
            or parsed.fragment
            or parsed.username
            or parsed.password
        ):
            raise ValueError("zabbix_api_url must be a plain HTTPS /api_jsonrpc.php URL")
        if not self.zabbix_ca_file.is_absolute() or not self.zabbix_ca_file.is_file():
            raise ValueError("zabbix_ca_file must be an existing absolute file")
        return self

    @classmethod
    def from_environment(cls) -> ConnectorSettings:
        """Load protected credentials and non-secret deployment settings."""

        return cls(
            zabbix_api_url=os.environ["NEXTOPS_ZABBIX_API_URL"],
            zabbix_ca_file=Path(os.environ["NEXTOPS_ZABBIX_CA_FILE"]),
            zabbix_api_token=deployment_secret(
                value_variable="NEXTOPS_ZABBIX_API_TOKEN",
                file_variable="NEXTOPS_ZABBIX_API_TOKEN_FILE",
                credential_name="zabbix-api-token",
            ),
            service_auth_secret=deployment_secret(
                value_variable="NEXTOPS_CONNECTOR_SERVICE_SECRET",
                file_variable="NEXTOPS_CONNECTOR_SERVICE_SECRET_FILE",
                credential_name="connector-service-secret",
            ),
            zabbix_host=os.environ.get("NEXTOPS_ZABBIX_HOST", "Zabbix server"),
            request_timeout_seconds=float(
                os.environ.get("NEXTOPS_CONNECTOR_TIMEOUT_SECONDS", "15")
            ),
        )
