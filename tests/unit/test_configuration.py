"""Fail-closed application configuration tests."""

from pathlib import Path

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


def test_settings_accept_only_a_loopback_inference_origin() -> None:
    with pytest.raises(ValidationError, match="inference_base_url"):
        AppSettings(
            database_url="postgresql+psycopg://nextops_app@db.internal/nextops",
            bootstrap_secret="b" * 32,
            recovery_secret="r" * 32,
            inference_base_url="http://192.0.2.10:8090",
            inference_service_secret="i" * 32,
        )


def test_runtime_settings_load_protected_systemd_credentials(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    values = {
        "database-url": "postgresql+psycopg://nextops_app@127.0.0.1/nextops",
        "bootstrap-secret": "b" * 32,
        "recovery-secret": "r" * 32,
        "inference-service-secret": "i" * 32,
    }
    for name, value in values.items():
        path = tmp_path / name
        path.write_text(f"{value}\n", encoding="utf-8")
        path.chmod(0o640)
    for variable in (
        "NEXTOPS_DATABASE_URL",
        "NEXTOPS_BOOTSTRAP_SECRET",
        "NEXTOPS_RECOVERY_SECRET",
        "NEXTOPS_INFERENCE_SERVICE_SECRET",
    ):
        monkeypatch.delenv(variable, raising=False)
    monkeypatch.setenv("CREDENTIALS_DIRECTORY", str(tmp_path))
    monkeypatch.setenv("NEXTOPS_INFERENCE_BASE_URL", "http://127.0.0.1:18090")

    settings = AppSettings.from_environment()

    assert settings.database_url.get_secret_value().endswith("/nextops")
    assert settings.inference_base_url == "http://127.0.0.1:18090"
