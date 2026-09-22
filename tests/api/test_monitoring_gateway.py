"""Protected monitoring gateway error-boundary tests."""

import asyncio
from typing import Any

from nextops.api.monitoring_gateway import LoopbackMonitoringGateway
from nextops.application.errors import ApplicationError
from nextops.contracts.errors import ErrorCode


class FailingTransport:
    """Simulate the shared low-level transport's generic upstream classification."""

    async def get_json(
        self,
        path: str,
        headers: dict[str, str],
        timeout_seconds: float,
    ) -> dict[str, Any]:
        del path, headers, timeout_seconds
        raise ApplicationError(
            ErrorCode.DEPENDENCY_UNAVAILABLE,
            "inference.provider_unavailable",
            retryable=True,
        )

    async def post_json(
        self,
        path: str,
        payload: dict[str, Any],
        headers: dict[str, str],
        timeout_seconds: float,
    ) -> dict[str, Any]:
        del path, payload, headers, timeout_seconds
        raise AssertionError("monitoring gateway must not send POST requests")


def test_gateway_relabels_shared_transport_failure_as_connector_failure() -> None:
    gateway = LoopbackMonitoringGateway(
        "http://127.0.0.1:18100",
        "service-secret-that-is-long-enough",
        5.0,
        FailingTransport(),
    )

    try:
        asyncio.run(gateway.summary())
    except ApplicationError as error:
        assert error.code is ErrorCode.DEPENDENCY_UNAVAILABLE
        assert error.message_key == "connector.summary_unavailable"
        assert error.retryable is True
    else:
        raise AssertionError("connector transport failure was not propagated")
