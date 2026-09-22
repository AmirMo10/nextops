"""Deployment-secret loading tests for the isolated inference service."""

from pathlib import Path

import pytest

from nextops.inference.configuration import LlamaCppSettings


def _base_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NEXTOPS_LLAMA_BASE_URL", "http://127.0.0.1:8080")
    for name in (
        "NEXTOPS_LLAMA_API_KEY",
        "NEXTOPS_LLAMA_API_KEY_FILE",
        "NEXTOPS_INFERENCE_SERVICE_SECRET",
        "NEXTOPS_INFERENCE_SERVICE_SECRET_FILE",
        "CREDENTIALS_DIRECTORY",
    ):
        monkeypatch.delenv(name, raising=False)


def _write_secret(path: Path, value: str) -> None:
    path.write_text(f"{value}\n", encoding="utf-8")
    path.chmod(0o640)


def test_runtime_settings_load_systemd_credentials(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    _base_environment(monkeypatch)
    _write_secret(tmp_path / "llama-api-key", "provider-secret-00000000000000000")
    _write_secret(
        tmp_path / "inference-service-secret",
        "service-secret-000000000000000000",
    )
    monkeypatch.setenv("CREDENTIALS_DIRECTORY", str(tmp_path))

    settings = LlamaCppSettings.from_environment()

    assert settings.provider_api_key.get_secret_value().startswith("provider-secret")
    assert settings.service_auth_secret.get_secret_value().startswith("service-secret")


def test_runtime_settings_reject_ambiguous_secret_sources(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    _base_environment(monkeypatch)
    _write_secret(tmp_path / "llama-api-key", "provider-secret-00000000000000000")
    _write_secret(
        tmp_path / "inference-service-secret",
        "service-secret-000000000000000000",
    )
    monkeypatch.setenv("CREDENTIALS_DIRECTORY", str(tmp_path))
    monkeypatch.setenv("NEXTOPS_LLAMA_API_KEY", "another-provider-secret-00000000000")

    with pytest.raises(ValueError, match="cannot be combined"):
        LlamaCppSettings.from_environment()


def test_runtime_settings_reject_multiline_secret(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    _base_environment(monkeypatch)
    provider_secret = tmp_path / "provider-secret"
    _write_secret(provider_secret, "provider-secret-00000000000000000")
    service_secret = tmp_path / "service-secret"
    _write_secret(service_secret, "service-secret-000000000000000000\nsecond-line")
    monkeypatch.setenv("NEXTOPS_LLAMA_API_KEY_FILE", str(provider_secret))
    monkeypatch.setenv("NEXTOPS_INFERENCE_SERVICE_SECRET_FILE", str(service_secret))

    with pytest.raises(ValueError, match="one non-empty line"):
        LlamaCppSettings.from_environment()
