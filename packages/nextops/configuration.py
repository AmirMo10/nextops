"""Fail-closed runtime configuration loaded from the deployment boundary."""

from __future__ import annotations

import os
import re
from typing import Self
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field, SecretStr, model_validator

from nextops.security.deployment_credentials import deployment_secret


class AppSettings(BaseModel):
    """Validated secrets and bounded timing configuration for the local app."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    database_url: SecretStr
    bootstrap_secret: SecretStr = Field(min_length=32, max_length=512)
    recovery_secret: SecretStr = Field(min_length=32, max_length=512)
    session_ttl_seconds: int = Field(default=3_600, ge=900, le=86_400)
    lease_ttl_seconds: int = Field(default=30, ge=5, le=300)
    inference_base_url: str | None = None
    inference_service_secret: SecretStr | None = Field(default=None, min_length=32, max_length=512)
    inference_timeout_seconds: float = Field(default=150.0, ge=1.0, le=600.0)
    connector_base_url: str | None = None
    connector_service_secret: SecretStr | None = Field(default=None, min_length=32, max_length=512)
    connector_timeout_seconds: float = Field(default=20.0, ge=1.0, le=60.0)
    incident_target_ids: tuple[str, ...] = Field(default_factory=tuple, max_length=8)

    @model_validator(mode="after")
    def validate_security_boundaries(self) -> Self:
        """Reject non-PostgreSQL state and shared bootstrap/recovery secrets."""

        database_url = self.database_url.get_secret_value()
        if not database_url.startswith("postgresql+psycopg://"):
            raise ValueError("database_url must use postgresql+psycopg")
        if self.bootstrap_secret.get_secret_value() == self.recovery_secret.get_secret_value():
            raise ValueError("bootstrap_secret and recovery_secret must differ")
        if (self.inference_base_url is None) != (self.inference_service_secret is None):
            raise ValueError("inference_base_url and inference_service_secret must be set together")
        if self.inference_base_url is not None:
            parsed = urlsplit(self.inference_base_url)
            valid = (
                parsed.scheme == "http"
                and parsed.hostname == "127.0.0.1"
                and parsed.port is not None
                and 1 <= parsed.port <= 65_535
                and parsed.path in ("", "/")
                and not parsed.query
                and not parsed.fragment
                and parsed.username is None
                and parsed.password is None
            )
            if not valid:
                raise ValueError(
                    "inference_base_url must be an undecorated http://127.0.0.1:<port> origin"
                )
        if (self.connector_base_url is None) != (self.connector_service_secret is None):
            raise ValueError("connector_base_url and connector_service_secret must be set together")
        if self.connector_base_url is not None:
            parsed = urlsplit(self.connector_base_url)
            valid = (
                parsed.scheme == "http"
                and parsed.hostname == "127.0.0.1"
                and parsed.port is not None
                and 1 <= parsed.port <= 65_535
                and parsed.path in ("", "/")
                and not parsed.query
                and not parsed.fragment
                and parsed.username is None
                and parsed.password is None
            )
            if not valid:
                raise ValueError(
                    "connector_base_url must be an undecorated http://127.0.0.1:<port> origin"
                )
        if len(set(self.incident_target_ids)) != len(self.incident_target_ids) or any(
            re.fullmatch(r"[a-z][a-z0-9-]{1,31}", target_id) is None
            for target_id in self.incident_target_ids
        ):
            raise ValueError("incident_target_ids must be unique normalized target identifiers")
        return self

    @classmethod
    def from_environment(cls) -> AppSettings:
        """Load required values without a secret-bearing default."""

        connector_base_url = os.environ.get("NEXTOPS_CONNECTOR_BASE_URL") or None
        return cls(
            database_url=deployment_secret(
                value_variable="NEXTOPS_DATABASE_URL",
                file_variable="NEXTOPS_DATABASE_URL_FILE",
                credential_name="database-url",
            ),
            bootstrap_secret=deployment_secret(
                value_variable="NEXTOPS_BOOTSTRAP_SECRET",
                file_variable="NEXTOPS_BOOTSTRAP_SECRET_FILE",
                credential_name="bootstrap-secret",
            ),
            recovery_secret=deployment_secret(
                value_variable="NEXTOPS_RECOVERY_SECRET",
                file_variable="NEXTOPS_RECOVERY_SECRET_FILE",
                credential_name="recovery-secret",
            ),
            session_ttl_seconds=int(os.environ.get("NEXTOPS_SESSION_TTL_SECONDS", "3600")),
            lease_ttl_seconds=int(os.environ.get("NEXTOPS_LEASE_TTL_SECONDS", "30")),
            inference_base_url=os.environ.get("NEXTOPS_INFERENCE_BASE_URL") or None,
            inference_service_secret=(
                deployment_secret(
                    value_variable="NEXTOPS_INFERENCE_SERVICE_SECRET",
                    file_variable="NEXTOPS_INFERENCE_SERVICE_SECRET_FILE",
                    credential_name="inference-service-secret",
                )
                or None
            ),
            inference_timeout_seconds=float(
                os.environ.get("NEXTOPS_INFERENCE_TIMEOUT_SECONDS", "150")
            ),
            connector_base_url=connector_base_url,
            connector_service_secret=(
                deployment_secret(
                    value_variable="NEXTOPS_CONNECTOR_SERVICE_SECRET",
                    file_variable="NEXTOPS_CONNECTOR_SERVICE_SECRET_FILE",
                    credential_name="connector-service-secret",
                )
                if connector_base_url
                else None
            ),
            connector_timeout_seconds=float(
                os.environ.get("NEXTOPS_CONNECTOR_TIMEOUT_SECONDS", "20")
            ),
            incident_target_ids=tuple(
                target_id.strip()
                for target_id in os.environ.get("NEXTOPS_INCIDENT_TARGET_IDS", "").split(",")
                if target_id.strip()
            ),
        )
