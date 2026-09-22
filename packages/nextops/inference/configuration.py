"""Fail-closed configuration for the local llama.cpp boundary."""

from __future__ import annotations

import os
from typing import Literal, Self
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field, SecretStr, model_validator

from nextops.security.deployment_credentials import deployment_secret


class LlamaCppSettings(BaseModel):
    """Fixed local-provider identity, secrets, and bounded timeouts."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    base_url: str
    provider_api_key: SecretStr = Field(min_length=32, max_length=512)
    service_auth_secret: SecretStr = Field(min_length=32, max_length=512)
    model_id: Literal["nextops-qwen3-8b-q4-k-m"] = "nextops-qwen3-8b-q4-k-m"
    runtime_version: Literal["v0.4.1"] = "v0.4.1"
    request_timeout_seconds: float = Field(default=120.0, ge=1.0, le=600.0)
    queue_timeout_seconds: float = Field(default=5.0, ge=0.01, le=60.0)

    @model_validator(mode="after")
    def validate_security_boundary(self) -> Self:
        """Accept only a plain HTTP IPv4 loopback origin with no URL decorations."""

        parsed = urlsplit(self.base_url)
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
            raise ValueError("base_url must be an undecorated http://127.0.0.1:<port> origin")
        if self.provider_api_key.get_secret_value() == self.service_auth_secret.get_secret_value():
            raise ValueError("provider_api_key and service_auth_secret must differ")
        return self

    @classmethod
    def from_environment(cls) -> LlamaCppSettings:
        """Load deployment settings without requiring secrets in process environment values."""

        return cls(
            base_url=os.environ.get("NEXTOPS_LLAMA_BASE_URL", ""),
            provider_api_key=deployment_secret(
                value_variable="NEXTOPS_LLAMA_API_KEY",
                file_variable="NEXTOPS_LLAMA_API_KEY_FILE",
                credential_name="llama-api-key",
            ),
            service_auth_secret=deployment_secret(
                value_variable="NEXTOPS_INFERENCE_SERVICE_SECRET",
                file_variable="NEXTOPS_INFERENCE_SERVICE_SECRET_FILE",
                credential_name="inference-service-secret",
            ),
            request_timeout_seconds=float(
                os.environ.get("NEXTOPS_INFERENCE_TIMEOUT_SECONDS", "120")
            ),
            queue_timeout_seconds=float(os.environ.get("NEXTOPS_QUEUE_TIMEOUT_SECONDS", "5")),
        )
