"""Fail-closed runtime configuration loaded from the deployment boundary."""

from __future__ import annotations

import os
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, SecretStr, model_validator


class AppSettings(BaseModel):
    """Validated secrets and bounded timing configuration for the local app."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    database_url: SecretStr
    bootstrap_secret: SecretStr = Field(min_length=32, max_length=512)
    recovery_secret: SecretStr = Field(min_length=32, max_length=512)
    session_ttl_seconds: int = Field(default=3_600, ge=900, le=86_400)
    lease_ttl_seconds: int = Field(default=30, ge=5, le=300)

    @model_validator(mode="after")
    def validate_security_boundaries(self) -> Self:
        """Reject non-PostgreSQL state and shared bootstrap/recovery secrets."""

        database_url = self.database_url.get_secret_value()
        if not database_url.startswith("postgresql+psycopg://"):
            raise ValueError("database_url must use postgresql+psycopg")
        if self.bootstrap_secret.get_secret_value() == self.recovery_secret.get_secret_value():
            raise ValueError("bootstrap_secret and recovery_secret must differ")
        return self

    @classmethod
    def from_environment(cls) -> AppSettings:
        """Load required values without a secret-bearing default."""

        return cls(
            database_url=os.environ.get("NEXTOPS_DATABASE_URL", ""),
            bootstrap_secret=os.environ.get("NEXTOPS_BOOTSTRAP_SECRET", ""),
            recovery_secret=os.environ.get("NEXTOPS_RECOVERY_SECRET", ""),
            session_ttl_seconds=int(os.environ.get("NEXTOPS_SESSION_TTL_SECONDS", "3600")),
            lease_ttl_seconds=int(os.environ.get("NEXTOPS_LEASE_TTL_SECONDS", "30")),
        )
