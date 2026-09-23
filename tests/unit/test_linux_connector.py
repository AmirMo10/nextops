"""Phase 2 Linux connector boundary tests."""

import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from nextops.application.errors import ApplicationError
from nextops.connectors.api import create_connector_app
from nextops.connectors.linux import LinuxReadClient, LinuxTargetRegistry
from nextops.contracts.errors import ErrorCode
from nextops.contracts.incidents import IncidentEvidence
from nextops.contracts.linux import LinuxDiagnosticSnapshot
from nextops.contracts.monitoring import MonitoringIncidentContext, MonitoringSummary

NOW = datetime(2026, 9, 23, 10, 0, tzinfo=UTC)


def _snapshot(target_id: str = "app") -> dict[str, Any]:
    return {
        "source": "linux",
        "collector_version": "1.0.0",
        "target_id": target_id,
        "hostname": "nextops-app",
        "operating_system": "Ubuntu 24.04.3 LTS",
        "collected_at": NOW.isoformat(),
        "uptime_seconds": 3600,
        "logical_cpu_count": 8,
        "load_1m": 0.1,
        "load_5m": 0.2,
        "load_15m": 0.3,
        "memory_total_bytes": 34_359_738_368,
        "memory_available_bytes": 30_064_771_072,
        "swap_total_bytes": 0,
        "swap_free_bytes": 0,
        "filesystems": [
            {
                "path": "/",
                "total_bytes": 100_000,
                "available_bytes": 75_000,
                "used_percent": 25.0,
            }
        ],
        "processes": [{"pid": 101, "name": "uvicorn", "rss_bytes": 120_000_000}],
        "services": [
            {
                "unit": "nextops-app.service",
                "load_state": "loaded",
                "active_state": "active",
                "sub_state": "running",
            }
        ],
        "journal": [],
        "local_user_count": 1,
        "logged_in_user_count": 0,
        "installed_package_count": 850,
        "listening_sockets": [{"family": "ipv4", "address": "127.0.0.1", "port": 8080}],
        "routes": [{"interface": "ens192", "destination": "0.0.0.0/0", "gateway": "10.0.0.1"}],
        "nameservers": ["10.0.0.2"],
        "is_partial": False,
        "partial_reasons": [],
    }


def _registry(tmp_path: Path) -> LinuxTargetRegistry:
    identity = tmp_path / "linux-app-key"
    identity.write_text("test-only-private-key-placeholder", encoding="utf-8")
    known_hosts = tmp_path / "known_hosts"
    known_hosts.write_text("test-only-host-key-placeholder", encoding="utf-8")
    registry_path = tmp_path / "linux-targets.json"
    registry_path.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "known_hosts_file": str(known_hosts),
                "targets": [
                    {
                        "target_id": "app",
                        "display_name": "NextOps application",
                        "zabbix_host": "NextOps App",
                        "ssh_destination": "nextops-linux-ro@10.0.0.47",
                        "identity_file": str(identity),
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return LinuxTargetRegistry.from_file(registry_path)


class FakeLinuxTransport:
    def __init__(self, payload: dict[str, Any]) -> None:
        self.payload = payload
        self.destinations: list[str] = []

    async def collect(self, target: Any) -> dict[str, Any]:
        self.destinations.append(str(target.ssh_destination))
        return self.payload


class UnusedMonitoringClient:
    async def summary(self) -> MonitoringSummary:
        raise AssertionError("Linux route must not call Zabbix summary")

    async def incident_context(self) -> MonitoringIncidentContext:
        raise AssertionError("Linux route must not call Zabbix incident context")


class FakePhase2Client:
    def __init__(self, payload: dict[str, Any]) -> None:
        self.payload = payload

    async def linux_snapshot(self, target_id: str) -> LinuxDiagnosticSnapshot:
        if target_id != "app":
            raise ApplicationError(ErrorCode.POLICY_DENIED, "connector.linux_target_denied")
        return LinuxDiagnosticSnapshot.model_validate(self.payload)

    async def evidence(self, target_id: str) -> IncidentEvidence:
        del target_id
        raise AssertionError("Linux snapshot route must not request composite evidence")


def test_registry_resolves_only_immutable_configured_targets(tmp_path: Path) -> None:
    registry = _registry(tmp_path)

    assert registry.resolve("app").ssh_destination == "nextops-linux-ro@10.0.0.47"
    with pytest.raises(ApplicationError) as caught:
        registry.resolve("../../root")

    assert caught.value.code is ErrorCode.POLICY_DENIED
    assert caught.value.message_key == "connector.linux_target_denied"


def test_linux_client_validates_exact_target_provenance(tmp_path: Path) -> None:
    registry = _registry(tmp_path)
    transport = FakeLinuxTransport(_snapshot())

    snapshot = asyncio.run(LinuxReadClient(registry, transport).snapshot("app"))

    assert snapshot.target_id == "app"
    assert snapshot.services[0].unit == "nextops-app.service"
    assert transport.destinations == ["nextops-linux-ro@10.0.0.47"]


def test_linux_client_rejects_collector_target_mismatch(tmp_path: Path) -> None:
    registry = _registry(tmp_path)
    transport = FakeLinuxTransport(_snapshot("ai"))

    with pytest.raises(ApplicationError) as caught:
        asyncio.run(LinuxReadClient(registry, transport).snapshot("app"))

    assert caught.value.code is ErrorCode.DEPENDENCY_UNAVAILABLE
    assert caught.value.message_key == "connector.linux_target_mismatch"


def test_registry_rejects_public_ssh_destinations(tmp_path: Path) -> None:
    identity = tmp_path / "key"
    identity.write_text("test", encoding="utf-8")
    known_hosts = tmp_path / "known-hosts"
    known_hosts.write_text("test", encoding="utf-8")

    with pytest.raises(ValueError, match="private"):
        LinuxTargetRegistry.model_validate(
            {
                "schema_version": "1.0.0",
                "known_hosts_file": known_hosts,
                "targets": [
                    {
                        "target_id": "app",
                        "display_name": "Application",
                        "zabbix_host": "NextOps App",
                        "ssh_destination": "nextops-linux-ro@8.8.8.8",
                        "identity_file": identity,
                    }
                ],
            }
        )


def test_linux_connector_route_requires_service_auth_and_denies_unknown_target() -> None:
    client = TestClient(
        create_connector_app(
            UnusedMonitoringClient(),
            "connector-service-secret-that-is-long-enough",
            FakePhase2Client(_snapshot()),
        )
    )
    headers = {"Authorization": "Bearer connector-service-secret-that-is-long-enough"}

    unauthenticated = client.get("/api/v1/linux/app/snapshot")
    accepted = client.get("/api/v1/linux/app/snapshot", headers=headers)
    denied = client.get("/api/v1/linux/unknown/snapshot", headers=headers)

    assert unauthenticated.status_code == 401
    assert accepted.status_code == 200
    assert accepted.json()["target_id"] == "app"
    assert denied.status_code == 403
    assert denied.json()["error"]["message_key"] == "connector.linux_target_denied"
