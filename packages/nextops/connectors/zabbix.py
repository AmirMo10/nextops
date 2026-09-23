"""TLS-verified, read-only Zabbix JSON-RPC adapter."""

from __future__ import annotations

import asyncio
import json
import ssl
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Protocol
from urllib.error import HTTPError, URLError
from urllib.request import HTTPSHandler, ProxyHandler, Request, build_opener

from pydantic import ValidationError

from nextops.application.errors import ApplicationError
from nextops.contracts.errors import ErrorCode
from nextops.contracts.monitoring import (
    IncidentPartialReason,
    MonitoringEvent,
    MonitoringHistoryPoint,
    MonitoringIncidentContext,
    MonitoringMetric,
    MonitoringPartialReason,
    MonitoringProblem,
    MonitoringSummary,
)

MAX_ZABBIX_RESPONSE_BYTES = 1_048_576
INCIDENT_LOOKBACK_MINUTES = 60
MAX_HISTORY_METRICS = 4
MAX_HISTORY_POINTS_PER_METRIC = 8
MAX_INCIDENT_EVENTS = 25
MAX_METRIC_VALUE_CHARACTERS = 256
NUMERIC_HISTORY_TYPES = frozenset({0, 3})
PREFERRED_KEYS = (
    "system.cpu.util[,idle]",
    "vm.memory.size[available]",
    "vfs.fs.size[/,pused]",
    "system.uptime",
    "agent.ping",
)


class ZabbixTransport(Protocol):
    """Replaceable JSON-RPC transport used by connector tests."""

    async def call(self, method: str, params: dict[str, Any]) -> Any: ...


class HttpsZabbixTransport:
    """Call one pinned HTTPS origin without inheriting proxy configuration."""

    def __init__(self, api_url: str, ca_file: Path, api_token: str, timeout: float) -> None:
        context = ssl.create_default_context(cafile=str(ca_file))
        self._opener = build_opener(ProxyHandler({}), HTTPSHandler(context=context))
        self._api_url = api_url
        self._api_token = api_token
        self._timeout = timeout

    async def call(self, method: str, params: dict[str, Any]) -> Any:
        return await asyncio.to_thread(self._call, method, params)

    def _call(self, method: str, params: dict[str, Any]) -> Any:
        body = json.dumps(
            {"jsonrpc": "2.0", "method": method, "params": params, "id": 1},
            separators=(",", ":"),
        ).encode()
        headers = {
            "Content-Type": "application/json-rpc",
            "Accept": "application/json",
        }
        if method != "apiinfo.version":
            headers["Authorization"] = f"Bearer {self._api_token}"
        request = Request(
            self._api_url,
            data=body,
            headers=headers,
            method="POST",
        )
        try:
            with self._opener.open(request, timeout=self._timeout) as response:
                raw = response.read(MAX_ZABBIX_RESPONSE_BYTES + 1)
        except (HTTPError, URLError, TimeoutError, OSError) as error:
            raise ApplicationError(
                ErrorCode.DEPENDENCY_UNAVAILABLE,
                "connector.zabbix_unavailable",
                retryable=True,
            ) from error
        if len(raw) > MAX_ZABBIX_RESPONSE_BYTES:
            raise ApplicationError(
                ErrorCode.DEPENDENCY_UNAVAILABLE,
                "connector.zabbix_response_too_large",
                retryable=True,
            )
        try:
            decoded = json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ApplicationError(
                ErrorCode.DEPENDENCY_UNAVAILABLE,
                "connector.zabbix_response_invalid",
                retryable=True,
            ) from error
        if not isinstance(decoded, dict) or "error" in decoded or "result" not in decoded:
            raise ApplicationError(
                ErrorCode.DEPENDENCY_UNAVAILABLE,
                "connector.zabbix_response_invalid",
                retryable=True,
            )
        return decoded["result"]


class ZabbixReadClient:
    """Expose bounded current and recent evidence for one configured host."""

    def __init__(
        self,
        host: str,
        transport: ZabbixTransport,
        *,
        incident_lookback_minutes: int = INCIDENT_LOOKBACK_MINUTES,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        if not 15 <= incident_lookback_minutes <= 1_440:
            raise ValueError("incident lookback must be between 15 and 1440 minutes")
        self._host = host
        self._transport = transport
        self._incident_lookback = timedelta(minutes=incident_lookback_minutes)
        self._clock = clock or (lambda: datetime.now(UTC))

    async def summary(self) -> MonitoringSummary:
        try:
            collected_at, version, host, _host_id, raw_items, raw_problems = await self._snapshot()
            return self._summary(version, host, collected_at, raw_items, raw_problems)
        except (AttributeError, KeyError, TypeError, ValueError, ValidationError) as error:
            raise ApplicationError(
                ErrorCode.DEPENDENCY_UNAVAILABLE,
                "connector.zabbix_response_invalid",
                retryable=True,
            ) from error

    async def incident_context(self) -> MonitoringIncidentContext:
        """Collect a fixed-window timeline without caller-selected methods or targets."""

        try:
            collected_at, version, host, host_id, raw_items, raw_problems = await self._snapshot()
            window_started_at = collected_at - self._incident_lookback
            summary = self._summary(version, host, collected_at, raw_items, raw_problems)
            history_items = self._history_items(raw_items)
            reasons: list[IncidentPartialReason] = list(summary.partial_reasons)
            numeric_item_count = self._numeric_item_count(raw_items)
            if numeric_item_count > len(history_items):
                reasons.append("history_metrics_truncated")

            history: list[MonitoringHistoryPoint] = []
            for item in history_items:
                raw_history = await self._transport.call(
                    "history.get",
                    {
                        "history": int(item["value_type"]),
                        "hostids": [host_id],
                        "itemids": [str(item["itemid"])],
                        "time_from": int(window_started_at.timestamp()),
                        "time_till": int(collected_at.timestamp()),
                        "output": ["itemid", "clock", "value"],
                        "sortfield": ["clock", "ns"],
                        "sortorder": "DESC",
                        "limit": MAX_HISTORY_POINTS_PER_METRIC + 1,
                    },
                )
                if not isinstance(raw_history, list):
                    raise TypeError("history result is not a list")
                if not all(
                    isinstance(point, dict) and str(point.get("itemid", "")) == str(item["itemid"])
                    for point in raw_history
                ):
                    raise TypeError("history result contains an unexpected item")
                if len(raw_history) > MAX_HISTORY_POINTS_PER_METRIC:
                    self._append_reason(reasons, "history_points_truncated")
                history.extend(
                    MonitoringHistoryPoint(
                        name=str(item["name"]),
                        key=str(item["key_"]),
                        value=str(point["value"]),
                        units=str(item.get("units", "")),
                        measured_at=datetime.fromtimestamp(int(point["clock"]), UTC),
                    )
                    for point in raw_history[:MAX_HISTORY_POINTS_PER_METRIC]
                )

            raw_events = await self._transport.call(
                "event.get",
                {
                    "hostids": [host_id],
                    "source": 0,
                    "object": 0,
                    "time_from": int(window_started_at.timestamp()),
                    "time_till": int(collected_at.timestamp()),
                    "output": [
                        "eventid",
                        "name",
                        "severity",
                        "clock",
                        "value",
                        "acknowledged",
                        "suppressed",
                    ],
                    "sortfield": ["clock", "eventid"],
                    "sortorder": "DESC",
                    "limit": MAX_INCIDENT_EVENTS + 1,
                },
            )
            if not isinstance(raw_events, list):
                raise TypeError("events result is not a list")
            if len(raw_events) > MAX_INCIDENT_EVENTS:
                self._append_reason(reasons, "events_truncated")
            events = tuple(self._event(event) for event in raw_events[:MAX_INCIDENT_EVENTS])

            return MonitoringIncidentContext(
                source_version=version,
                host=host,
                collected_at=collected_at,
                window_started_at=window_started_at,
                window_ended_at=collected_at,
                summary=summary,
                history=tuple(history),
                events=events,
                is_partial=bool(reasons),
                partial_reasons=tuple(reasons),
            )
        except (AttributeError, KeyError, TypeError, ValueError, ValidationError) as error:
            raise ApplicationError(
                ErrorCode.DEPENDENCY_UNAVAILABLE,
                "connector.zabbix_response_invalid",
                retryable=True,
            ) from error

    async def _snapshot(
        self,
    ) -> tuple[datetime, str, str, str, Any, Any]:
        collected_at = self._clock()
        if collected_at.tzinfo is None or collected_at.utcoffset() is None:
            raise ValueError("clock must return a timezone-aware datetime")
        version = await self._transport.call("apiinfo.version", {})
        hosts = await self._transport.call(
            "host.get",
            {
                "output": ["hostid", "host", "name", "status"],
                "filter": {"host": [self._host]},
            },
        )
        if not isinstance(hosts, list) or len(hosts) != 1 or hosts[0].get("status") != "0":
            raise ApplicationError(
                ErrorCode.DEPENDENCY_UNAVAILABLE,
                "connector.zabbix_host_unavailable",
                retryable=True,
            )
        host_id = str(hosts[0]["hostid"])
        raw_items = await self._transport.call(
            "item.get",
            {
                "hostids": [host_id],
                "output": [
                    "itemid",
                    "name",
                    "key_",
                    "value_type",
                    "lastvalue",
                    "units",
                    "lastclock",
                    "status",
                    "state",
                ],
                "filter": {"status": 0, "state": 0},
                "sortfield": "name",
                "limit": 1000,
            },
        )
        raw_problems = await self._transport.call(
            "problem.get",
            {
                "hostids": [host_id],
                "output": ["name", "severity", "clock"],
                "recent": False,
                "suppressed": False,
                "sortfield": ["eventid"],
                "sortorder": "DESC",
                "limit": 25,
            },
        )
        return (
            collected_at,
            str(version),
            str(hosts[0].get("name") or hosts[0]["host"]),
            host_id,
            raw_items,
            raw_problems,
        )

    @classmethod
    def _summary(
        cls,
        version: str,
        host: str,
        collected_at: datetime,
        raw_items: Any,
        raw_problems: Any,
    ) -> MonitoringSummary:
        metrics = cls._metrics(raw_items, collected_at)
        if not isinstance(raw_problems, list):
            raise TypeError("problems result is not a list")
        problems = tuple(
            MonitoringProblem(
                name=str(problem["name"]),
                severity=int(problem["severity"]),
                started_at=datetime.fromtimestamp(int(problem["clock"]), UTC),
            )
            for problem in raw_problems
        )
        return MonitoringSummary(
            source_version=version,
            host=host,
            collected_at=collected_at,
            metrics=metrics,
            active_problems=problems,
            is_partial=bool(
                partial_reasons := cls._partial_reasons(raw_items, raw_problems, metrics)
            ),
            partial_reasons=partial_reasons,
        )

    @staticmethod
    def _metrics(raw_items: Any, collected_at: datetime) -> tuple[MonitoringMetric, ...]:
        selected = ZabbixReadClient._sorted_usable_items(raw_items)[:8]
        stale_before = collected_at - timedelta(minutes=10)
        return tuple(
            MonitoringMetric(
                name=str(item["name"]),
                key=str(item["key_"]),
                value=str(item["lastvalue"]),
                units=str(item.get("units", "")),
                measured_at=(measured := datetime.fromtimestamp(int(item["lastclock"]), UTC)),
                stale=measured < stale_before,
            )
            for item in selected
        )

    @staticmethod
    def _partial_reasons(
        raw_items: Any,
        raw_problems: list[Any],
        metrics: tuple[MonitoringMetric, ...],
    ) -> tuple[MonitoringPartialReason, ...]:
        if not isinstance(raw_items, list):
            raise TypeError("items result is not a list")
        reasons: list[MonitoringPartialReason] = []
        usable_item_count = sum(
            1
            for item in raw_items
            if int(item.get("lastclock", "0")) > 0 and str(item.get("lastvalue", ""))
        )
        if usable_item_count > len(metrics) or len(raw_items) >= 1000:
            reasons.append("metrics_truncated")
        if len(raw_problems) >= 25:
            reasons.append("problems_truncated")
        if not metrics:
            reasons.append("no_usable_metrics")
        return tuple(reasons)

    @staticmethod
    def _sorted_usable_items(raw_items: Any) -> list[dict[str, Any]]:
        if not isinstance(raw_items, list):
            raise TypeError("items result is not a list")
        if not all(isinstance(item, dict) for item in raw_items):
            raise TypeError("item result contains a non-object")
        usable: list[dict[str, Any]] = [
            item
            for item in raw_items
            if int(item.get("lastclock", "0")) > 0
            and str(item.get("lastvalue", ""))
            and len(str(item.get("lastvalue", ""))) <= MAX_METRIC_VALUE_CHARACTERS
        ]
        priority = {key: index for index, key in enumerate(PREFERRED_KEYS)}
        return sorted(
            usable,
            key=lambda item: (
                priority.get(str(item.get("key_")), len(priority)),
                -int(item["lastclock"]),
                str(item.get("name", "")),
            ),
        )

    @classmethod
    def _history_items(cls, raw_items: Any) -> list[dict[str, Any]]:
        return [
            item
            for item in cls._sorted_usable_items(raw_items)
            if int(item.get("value_type", -1)) in NUMERIC_HISTORY_TYPES
            and str(item.get("itemid", "")).isdigit()
        ][:MAX_HISTORY_METRICS]

    @classmethod
    def _numeric_item_count(cls, raw_items: Any) -> int:
        return sum(
            1
            for item in cls._sorted_usable_items(raw_items)
            if int(item.get("value_type", -1)) in NUMERIC_HISTORY_TYPES
            and str(item.get("itemid", "")).isdigit()
        )

    @staticmethod
    def _event(raw_event: Any) -> MonitoringEvent:
        if not isinstance(raw_event, dict):
            raise TypeError("event result contains a non-object")
        value = str(raw_event["value"])
        if value not in {"0", "1"}:
            raise ValueError("event value must be a problem or recovery marker")
        return MonitoringEvent(
            event_id=str(raw_event["eventid"]),
            name=str(raw_event["name"]),
            severity=int(raw_event["severity"]),
            occurred_at=datetime.fromtimestamp(int(raw_event["clock"]), UTC),
            state="problem" if value == "1" else "recovery",
            acknowledged=str(raw_event["acknowledged"]) == "1",
            suppressed=str(raw_event["suppressed"]) == "1",
        )

    @staticmethod
    def _append_reason(reasons: list[IncidentPartialReason], reason: IncidentPartialReason) -> None:
        if reason not in reasons:
            reasons.append(reason)
