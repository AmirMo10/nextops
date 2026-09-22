"""TLS-verified, read-only Zabbix JSON-RPC adapter."""

from __future__ import annotations

import asyncio
import json
import ssl
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Protocol
from urllib.error import HTTPError, URLError
from urllib.request import HTTPSHandler, ProxyHandler, Request, build_opener

from pydantic import ValidationError

from nextops.application.errors import ApplicationError
from nextops.contracts.errors import ErrorCode
from nextops.contracts.monitoring import (
    MonitoringMetric,
    MonitoringPartialReason,
    MonitoringProblem,
    MonitoringSummary,
)

MAX_ZABBIX_RESPONSE_BYTES = 1_048_576
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
    """Expose only latest values and active problems for one configured host."""

    def __init__(self, host: str, transport: ZabbixTransport) -> None:
        self._host = host
        self._transport = transport

    async def summary(self) -> MonitoringSummary:
        collected_at = datetime.now(UTC)
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
                "output": ["name", "key_", "lastvalue", "units", "lastclock", "status", "state"],
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
        try:
            metrics = self._metrics(raw_items, collected_at)
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
                source_version=str(version),
                host=str(hosts[0].get("name") or hosts[0]["host"]),
                collected_at=collected_at,
                metrics=metrics,
                active_problems=problems,
                is_partial=bool(
                    partial_reasons := self._partial_reasons(raw_items, raw_problems, metrics)
                ),
                partial_reasons=partial_reasons,
            )
        except (KeyError, TypeError, ValueError, ValidationError) as error:
            raise ApplicationError(
                ErrorCode.DEPENDENCY_UNAVAILABLE,
                "connector.zabbix_response_invalid",
                retryable=True,
            ) from error

    @staticmethod
    def _metrics(raw_items: Any, collected_at: datetime) -> tuple[MonitoringMetric, ...]:
        if not isinstance(raw_items, list):
            raise TypeError("items result is not a list")
        usable = [
            item
            for item in raw_items
            if int(item.get("lastclock", "0")) > 0 and str(item.get("lastvalue", ""))
        ]
        priority = {key: index for index, key in enumerate(PREFERRED_KEYS)}
        selected = sorted(
            usable,
            key=lambda item: (
                priority.get(str(item.get("key_")), len(priority)),
                -int(item["lastclock"]),
                str(item.get("name", "")),
            ),
        )[:8]
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
