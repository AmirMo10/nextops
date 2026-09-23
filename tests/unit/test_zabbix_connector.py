"""Read-only Zabbix connector contract tests."""

from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi.testclient import TestClient

from nextops.application.errors import ApplicationError
from nextops.connectors.api import create_connector_app
from nextops.connectors.zabbix import ZabbixReadClient
from nextops.contracts.errors import ErrorCode

COLLECTED_AT = datetime(2026, 9, 23, 8, 0, tzinfo=UTC)


class FakeTransport:
    """Record methods and return bounded Zabbix-shaped fixtures."""

    def __init__(self) -> None:
        self.methods: list[str] = []
        self.calls: list[tuple[str, dict[str, Any]]] = []

    async def call(self, method: str, params: dict[str, Any]) -> Any:
        self.methods.append(method)
        self.calls.append((method, params))
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
                    "itemid": "20001",
                    "name": "CPU idle time",
                    "key_": "system.cpu.util[,idle]",
                    "value_type": "0",
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


def test_connector_skips_over_limit_metric_values_and_marks_partial() -> None:
    class LongValueTransport(FakeTransport):
        async def call(self, method: str, params: dict[str, Any]) -> Any:
            if method != "item.get":
                return await super().call(method, params)
            self.methods.append(method)
            return [
                {
                    "itemid": "20001",
                    "name": "CPU idle time",
                    "key_": "system.cpu.util[,idle]",
                    "value_type": "0",
                    "lastvalue": "88.2",
                    "units": "%",
                    "lastclock": "1789999999",
                    "status": "0",
                    "state": "0",
                },
                {
                    "itemid": "20002",
                    "name": "Filesystem discovery payload",
                    "key_": "vfs.fs.get",
                    "value_type": "4",
                    "lastvalue": "{" + ("x" * 300) + "}",
                    "units": "",
                    "lastclock": "1790000000",
                    "status": "0",
                    "state": "0",
                },
            ]

    summary = __import__("asyncio").run(
        ZabbixReadClient("Zabbix server", LongValueTransport()).summary()
    )

    assert [metric.key for metric in summary.metrics] == ["system.cpu.util[,idle]"]
    assert summary.is_partial is True
    assert summary.partial_reasons == ("metrics_truncated",)


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
        __import__("asyncio").run(ZabbixReadClient("Zabbix server", MalformedTransport()).summary())
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


def test_incident_context_uses_fixed_host_window_and_bounded_read_methods() -> None:
    class IncidentTransport(FakeTransport):
        async def call(self, method: str, params: dict[str, Any]) -> Any:
            if method == "history.get":
                self.methods.append(method)
                self.calls.append((method, params))
                return [
                    {
                        "itemid": "20001",
                        "clock": str(int((COLLECTED_AT - timedelta(minutes=5)).timestamp())),
                        "value": "87.4",
                    }
                ]
            if method == "event.get":
                self.methods.append(method)
                self.calls.append((method, params))
                return [
                    {
                        "eventid": "30001",
                        "name": "CPU pressure observed",
                        "severity": "3",
                        "clock": str(int((COLLECTED_AT - timedelta(minutes=2)).timestamp())),
                        "value": "1",
                        "acknowledged": "0",
                        "suppressed": "0",
                    }
                ]
            return await super().call(method, params)

    transport = IncidentTransport()
    context = __import__("asyncio").run(
        ZabbixReadClient(
            "Zabbix server",
            transport,
            incident_lookback_minutes=60,
            clock=lambda: COLLECTED_AT,
        ).incident_context()
    )

    assert transport.methods == [
        "apiinfo.version",
        "host.get",
        "item.get",
        "problem.get",
        "history.get",
        "event.get",
    ]
    history_params = next(params for method, params in transport.calls if method == "history.get")
    event_params = next(params for method, params in transport.calls if method == "event.get")
    assert history_params["hostids"] == ["10084"]
    assert history_params["itemids"] == ["20001"]
    assert history_params["limit"] == 9
    assert event_params["hostids"] == ["10084"]
    assert event_params["limit"] == 26
    assert event_params["source"] == 0
    assert event_params["object"] == 0
    assert context.window_started_at == COLLECTED_AT - timedelta(hours=1)
    assert context.window_ended_at == COLLECTED_AT
    assert context.history[0].key == "system.cpu.util[,idle]"
    assert context.events[0].state == "problem"
    assert context.is_partial is False
    assert context.partial_reasons == ()


def test_incident_context_rejects_unbounded_lookback() -> None:
    try:
        ZabbixReadClient("Zabbix server", FakeTransport(), incident_lookback_minutes=1_441)
    except ValueError as error:
        assert "lookback" in str(error)
    else:
        raise AssertionError("unbounded incident lookback was accepted")


def test_incident_context_rejects_history_for_an_unrequested_item() -> None:
    class MismatchedHistoryTransport(FakeTransport):
        async def call(self, method: str, params: dict[str, Any]) -> Any:
            if method == "history.get":
                return [
                    {
                        "itemid": "99999",
                        "clock": str(int((COLLECTED_AT - timedelta(minutes=5)).timestamp())),
                        "value": "87.4",
                    }
                ]
            if method == "event.get":
                return []
            return await super().call(method, params)

    try:
        __import__("asyncio").run(
            ZabbixReadClient(
                "Zabbix server",
                MismatchedHistoryTransport(),
                clock=lambda: COLLECTED_AT,
            ).incident_context()
        )
    except ApplicationError as error:
        assert error.code is ErrorCode.DEPENDENCY_UNAVAILABLE
        assert error.message_key == "connector.zabbix_response_invalid"
        assert "99999" not in str(error)
    else:
        raise AssertionError("history from an unrequested item was accepted")


def test_incident_context_marks_history_and_event_limits_partial() -> None:
    class TruncatedIncidentTransport(FakeTransport):
        async def call(self, method: str, params: dict[str, Any]) -> Any:
            if method == "history.get":
                self.methods.append(method)
                self.calls.append((method, params))
                return [
                    {
                        "itemid": "20001",
                        "clock": str(int((COLLECTED_AT - timedelta(minutes=index)).timestamp())),
                        "value": str(90 - index),
                    }
                    for index in range(9)
                ]
            if method == "event.get":
                self.methods.append(method)
                self.calls.append((method, params))
                return [
                    {
                        "eventid": str(30_000 + index),
                        "name": f"Bounded event {index}",
                        "severity": "2",
                        "clock": str(int((COLLECTED_AT - timedelta(minutes=index)).timestamp())),
                        "value": "1",
                        "acknowledged": "0",
                        "suppressed": "0",
                    }
                    for index in range(26)
                ]
            return await super().call(method, params)

    context = __import__("asyncio").run(
        ZabbixReadClient(
            "Zabbix server",
            TruncatedIncidentTransport(),
            clock=lambda: COLLECTED_AT,
        ).incident_context()
    )

    assert len(context.history) == 8
    assert len(context.events) == 25
    assert context.is_partial is True
    assert context.partial_reasons == ("history_points_truncated", "events_truncated")


def test_incident_context_endpoint_requires_service_bearer() -> None:
    class EmptyIncidentTransport(FakeTransport):
        async def call(self, method: str, params: dict[str, Any]) -> Any:
            if method in {"history.get", "event.get"}:
                self.methods.append(method)
                self.calls.append((method, params))
                return []
            return await super().call(method, params)

    client = TestClient(
        create_connector_app(
            ZabbixReadClient(
                "Zabbix server",
                EmptyIncidentTransport(),
                clock=lambda: COLLECTED_AT,
            ),
            "connector-service-secret-that-is-long-enough",
        )
    )

    denied = client.get("/api/v1/zabbix/incident-context")
    allowed = client.get(
        "/api/v1/zabbix/incident-context",
        headers={"Authorization": "Bearer connector-service-secret-that-is-long-enough"},
    )

    assert denied.status_code == 401
    assert allowed.status_code == 200
    assert allowed.json()["window_ended_at"] == COLLECTED_AT.isoformat().replace("+00:00", "Z")


def test_fixture_clock_is_timezone_aware() -> None:
    value = datetime.fromtimestamp(1789999999, UTC)
    assert value.tzinfo is UTC
