"""Fail-closed configuration for the local llama.cpp boundary."""

from __future__ import annotations

import os
import stat
from pathlib import Path
from typing import Literal, Self
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field, SecretStr, model_validator


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
            provider_api_key=_deployment_secret(
                value_variable="NEXTOPS_LLAMA_API_KEY",
                file_variable="NEXTOPS_LLAMA_API_KEY_FILE",
                credential_name="llama-api-key",
            ),
            service_auth_secret=_deployment_secret(
                value_variable="NEXTOPS_INFERENCE_SERVICE_SECRET",
                file_variable="NEXTOPS_INFERENCE_SERVICE_SECRET_FILE",
                credential_name="inference-service-secret",
            ),
            request_timeout_seconds=float(
                os.environ.get("NEXTOPS_INFERENCE_TIMEOUT_SECONDS", "120")
            ),
            queue_timeout_seconds=float(os.environ.get("NEXTOPS_QUEUE_TIMEOUT_SECONDS", "5")),
        )


def _deployment_secret(
    *,
    value_variable: str,
    file_variable: str,
    credential_name: str,
) -> str:
    direct_value = os.environ.get(value_variable)
    explicit_path = os.environ.get(file_variable)
    credentials_directory = os.environ.get("CREDENTIALS_DIRECTORY")

    if direct_value is not None and (explicit_path or credentials_directory):
        raise ValueError(
            f"{value_variable} cannot be combined with file-backed deployment credentials"
        )
    if direct_value is not None:
        return direct_value

    if explicit_path:
        return _read_secret_file(Path(explicit_path), file_variable)
    if credentials_directory:
        return _read_secret_file(
            Path(credentials_directory) / credential_name,
            "CREDENTIALS_DIRECTORY",
        )
    return ""


def _read_secret_file(path: Path, source: str) -> str:
    if not path.is_absolute():
        raise ValueError(f"{source} must resolve to an absolute path")

    try:
        metadata = path.lstat()
    except OSError as error:
        raise ValueError(f"unable to read the credential referenced by {source}") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise ValueError(f"{source} must reference a regular file, not a symlink")
    if os.name == "posix" and (metadata.st_mode & stat.S_IROTH or metadata.st_mode & stat.S_IWOTH):
        raise ValueError(f"the credential referenced by {source} must not be world-accessible")
    if metadata.st_size > 4_096:
        raise ValueError(f"the credential referenced by {source} exceeds 4096 bytes")

    try:
        value = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ValueError(f"unable to read the credential referenced by {source}") from error
    normalized = value.removesuffix("\n").removesuffix("\r")
    if (
        not normalized
        or normalized != normalized.strip()
        or "\n" in normalized
        or "\r" in normalized
    ):
        raise ValueError(f"the credential referenced by {source} must contain one non-empty line")
    return normalized
