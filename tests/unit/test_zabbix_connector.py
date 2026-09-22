"""Read-only Zabbix connector contract tests."""

from datetime import UTC, datetime
from typing import Any

from fastapi.testclient import TestClient

from nextops.application.errors import ApplicationError
from nextops.connectors.api import create_connector_app
from nextops.connectors.zabbix import ZabbixReadClient
from nextops.contracts.errors import ErrorCode


class FakeTransport:
    """Record methods and return bounded Zabbix-shaped fixtures."""

    def __init__(self) -> None:
        self.methods: list[str] = []

    async def call(self, method: str, params: dict[str, Any]) -> Any:
        self.methods.append(method)
        if method == "apiinfo.version":
            return "7.0.30"
        if method == "host.get":
            return [
                {
                    "hostid": "10084",
                    "host": "Zabbix server",
                    "name": "Zabbix server",
                    "status": "0",
                }
            ]
        if method == "item.get":
            return [
                {
                    "name": "CPU idle time",
                    "key_": "system.cpu.util[,idle]",
                    "lastvalue": "88.2",
                    "units": "%",
                    "lastclock": "1789999999",
                    "status": "0",
                    "state": "0",
                }
            ]
        if method == "problem.get":
            return []
        raise AssertionError(f"unexpected method: {method}")


def test_connector_calls_only_read_methods_and_marks_old_measurements_stale() -> None:
    transport = FakeTransport()
    summary = __import__("asyncio").run(ZabbixReadClient("Zabbix server", transport).summary())

    assert transport.methods == ["apiinfo.version", "host.get", "item.get", "problem.get"]
    assert summary.source == "zabbix"
    assert summary.metrics[0].stale is True
    assert summary.is_partial is False
    assert summary.partial_reasons == ()


def test_connector_marks_bounded_metric_selection_partial() -> None:
    class ManyMetricsTransport(FakeTransport):
        async def call(self, method: str, params: dict[str, Any]) -> Any:
            if method != "item.get":
                return await super().call(method, params)
            self.methods.append(method)
            return [
                {
                    "name": f"Metric {index}",
                    "key_": f"custom.metric[{index}]",
                    "lastvalue": str(index),
                    "units": "",
                    "lastclock": "1789999999",
                    "status": "0",
                    "state": "0",
                }
                for index in range(9)
            ]

    summary = __import__("asyncio").run(
        ZabbixReadClient("Zabbix server", ManyMetricsTransport()).summary()
    )

    assert len(summary.metrics) == 8
    assert summary.is_partial is True
    assert summary.partial_reasons == ("metrics_truncated",)


def test_connector_marks_missing_usable_metrics_partial() -> None:
    class EmptyMetricsTransport(FakeTransport):
        async def call(self, method: str, params: dict[str, Any]) -> Any:
            if method == "item.get":
                self.methods.append(method)
                return []
            return await super().call(method, params)

    summary = __import__("asyncio").run(
        ZabbixReadClient("Zabbix server", EmptyMetricsTransport()).summary()
    )

    assert summary.metrics == ()
    assert summary.is_partial is True
    assert summary.partial_reasons == ("no_usable_metrics",)


def test_connector_rejects_malformed_monitoring_text_with_safe_typed_error() -> None:
    class MalformedTransport(FakeTransport):
        async def call(self, method: str, params: dict[str, Any]) -> Any:
            if method == "item.get":
                self.methods.append(method)
                return [
                    {
                        "name": "X" * 257,
                        "key_": "custom.metric",
                        "lastvalue": "1",
                        "units": "",
                        "lastclock": "1789999999",
                    }
                ]
            return await super().call(method, params)

    try:
        __import__("asyncio").run(
            ZabbixReadClient("Zabbix server", MalformedTransport()).summary()
        )
    except ApplicationError as error:
        assert error.code is ErrorCode.DEPENDENCY_UNAVAILABLE
        assert error.message_key == "connector.zabbix_response_invalid"
        assert error.retryable is True
        assert "X" * 32 not in str(error)
    else:
        raise AssertionError("malformed monitoring text was accepted")


def test_connector_api_requires_service_bearer() -> None:
    transport = FakeTransport()
    client = TestClient(
        create_connector_app(
            ZabbixReadClient("Zabbix server", transport),
            "connector-service-secret-that-is-long-enough",
        )
    )

    denied = client.get("/api/v1/zabbix/summary")
    allowed = client.get(
        "/api/v1/zabbix/summary",
        headers={"Authorization": "Bearer connector-service-secret-that-is-long-enough"},
    )

    assert denied.status_code == 401
    assert allowed.status_code == 200
    assert allowed.json()["source_version"] == "7.0.30"


def test_fixture_clock_is_timezone_aware() -> None:
    value = datetime.fromtimestamp(1789999999, UTC)
    assert value.tzinfo is UTC
