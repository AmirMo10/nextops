"""Fail-closed application configuration tests."""

import pytest
from pydantic import ValidationError

from nextops.configuration import AppSettings


def test_settings_require_postgresql_and_independent_strong_deployment_secrets() -> None:
    settings = AppSettings(
        database_url="postgresql+psycopg://nextops_app@db.internal/nextops",
        bootstrap_secret="bootstrap-secret-that-is-at-least-32-bytes",
        recovery_secret="recovery-secret-that-is-different-and-long",
    )

    assert settings.database_url.get_secret_value().startswith("postgresql+psycopg://")


@pytest.mark.parametrize(
    ("database_url", "bootstrap_secret", "recovery_secret"),
    [
        ("sqlite:///nextops.db", "b" * 32, "r" * 32),
        ("postgresql+psycopg://db/nextops", "short", "r" * 32),
        ("postgresql+psycopg://db/nextops", "same" * 8, "same" * 8),
    ],
)
def test_settings_reject_unsafe_database_or_secret_configuration(
    database_url: str, bootstrap_secret: str, recovery_secret: str
) -> None:
    with pytest.raises(ValidationError):
        AppSettings(
            database_url=database_url,
            bootstrap_secret=bootstrap_secret,
            recovery_secret=recovery_secret,
        )
