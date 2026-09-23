"""Fail-closed Phase 2 connector configuration tests."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from nextops.connectors.configuration import ConnectorSettings


def test_connector_loads_protected_credentials_and_linux_registry(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    ca_file = tmp_path / "zabbix-ca.crt"
    ca_file.write_text("test-ca", encoding="utf-8")
    targets_file = tmp_path / "linux-targets.json"
    targets_file.write_text("{}", encoding="utf-8")
    (tmp_path / "zabbix-api-token").write_text("z" * 32, encoding="utf-8")
    (tmp_path / "connector-service-secret").write_text("s" * 32, encoding="utf-8")
    monkeypatch.setenv("CREDENTIALS_DIRECTORY", str(tmp_path))
    monkeypatch.setenv("NEXTOPS_ZABBIX_API_URL", "https://zabbix.local/api_jsonrpc.php")
    monkeypatch.setenv("NEXTOPS_ZABBIX_CA_FILE", str(ca_file))
    monkeypatch.setenv("NEXTOPS_LINUX_TARGETS_FILE", str(targets_file))
    monkeypatch.setenv("NEXTOPS_LINUX_TIMEOUT_SECONDS", "12")
    for name in (
        "NEXTOPS_ZABBIX_API_TOKEN",
        "NEXTOPS_ZABBIX_API_TOKEN_FILE",
        "NEXTOPS_CONNECTOR_SERVICE_SECRET",
        "NEXTOPS_CONNECTOR_SERVICE_SECRET_FILE",
    ):
        monkeypatch.delenv(name, raising=False)

    settings = ConnectorSettings.from_environment()

    assert settings.linux_targets_file == targets_file
    assert settings.linux_timeout_seconds == 12


def test_connector_rejects_missing_linux_registry(tmp_path: Path) -> None:
    ca_file = tmp_path / "zabbix-ca.crt"
    ca_file.write_text("test-ca", encoding="utf-8")

    with pytest.raises(ValidationError, match="linux_targets_file"):
        ConnectorSettings(
            zabbix_api_url="https://zabbix.local/api_jsonrpc.php",
            zabbix_ca_file=ca_file,
            zabbix_api_token="z" * 32,
            service_auth_secret="s" * 32,
            zabbix_host="Zabbix server",
            linux_targets_file=tmp_path / "missing.json",
        )
