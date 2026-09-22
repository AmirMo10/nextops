"""Server-side client for the loopback endpoint of the protected AI tunnel."""

from __future__ import annotations

from typing import Protocol
from uuid import UUID, uuid4

from pydantic import ValidationError

from nextops.application.errors import ApplicationError
from nextops.contracts.assistant import AssistantRequest, AssistantResponse
from nextops.contracts.errors import ErrorCode
from nextops.inference.contracts import InferenceReadiness, InferenceResult
from nextops.inference.llama_cpp import JsonTransport, UrllibJsonTransport


class InferenceGateway(Protocol):
    """Narrow replaceable boundary used by the application API."""

    async def readiness(self) -> InferenceReadiness: ...

    async def generate(
        self, request: AssistantRequest, correlation_id: UUID
    ) -> AssistantResponse: ...


class LoopbackInferenceGateway:
    """Call only a configuration-validated loopback origin with a service credential."""

    def __init__(
        self,
        base_url: str,
        service_auth_secret: str,
        timeout_seconds: float,
        transport: JsonTransport | None = None,
    ) -> None:
        self._transport = transport or UrllibJsonTransport(base_url)
        self._timeout_seconds = timeout_seconds
        self._headers = {
            "Authorization": f"Bearer {service_auth_secret}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def readiness(self) -> InferenceReadiness:
        raw = await self._transport.get_json(
            "/readyz",
            {"Accept": "application/json"},
            min(self._timeout_seconds, 5.0),
        )
        try:
            return InferenceReadiness.model_validate(raw)
        except ValidationError as error:
            raise ApplicationError(
                ErrorCode.DEPENDENCY_UNAVAILABLE,
                "assistant.readiness_invalid",
                retryable=True,
            ) from error

    async def generate(self, request: AssistantRequest, correlation_id: UUID) -> AssistantResponse:
        request_id = uuid4()
        raw = await self._transport.post_json(
            "/api/v1/generate",
            {
                "request_id": str(request_id),
                "locale": request.locale,
                "prompt": request.question,
                "max_output_tokens": request.max_output_tokens,
                "temperature": 0.3,
            },
            {**self._headers, "X-Correlation-ID": str(correlation_id)},
            self._timeout_seconds,
        )
        try:
            result = InferenceResult.model_validate(raw)
            if result.request_id != request_id or result.correlation_id != correlation_id:
                raise ValueError("inference identity mismatch")
            if result.completion_tokens > request.max_output_tokens:
                raise ValueError("inference output exceeded request bound")
            return AssistantResponse(
                **result.model_dump(),
                evidence_mode="model_only",
                live_monitoring_data=False,
            )
        except (ValidationError, ValueError) as error:
            raise ApplicationError(
                ErrorCode.DEPENDENCY_UNAVAILABLE,
                "assistant.response_invalid",
                retryable=True,
            ) from error
