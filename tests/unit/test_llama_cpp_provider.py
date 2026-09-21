"""llama.cpp adapter tests over a deterministic JSON transport."""

import asyncio
from typing import Any

import pytest

from nextops.application.errors import ApplicationError
from nextops.contracts.errors import ErrorCode
from nextops.inference.configuration import LlamaCppSettings
from nextops.inference.contracts import InferenceRequest, ReadinessState
from nextops.inference.llama_cpp import LlamaCppProvider


class StubTransport:
    def __init__(self) -> None:
        self.health: dict[str, Any] = {"status": "ok"}
        self.generation: dict[str, Any] = {
            "model": "nextops-qwen3-8b-q4-k-m",
            "choices": [
                {
                    "message": {"role": "assistant", "content": "Verified summary"},
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": 12, "completion_tokens": 4, "total_tokens": 16},
        }
        self.last_path = ""
        self.last_payload: dict[str, Any] = {}
        self.last_headers: dict[str, str] = {}

    async def get_json(
        self, path: str, headers: dict[str, str], timeout_seconds: float
    ) -> dict[str, Any]:
        del timeout_seconds
        self.last_path = path
        self.last_headers = headers
        return self.health

    async def post_json(
        self,
        path: str,
        payload: dict[str, Any],
        headers: dict[str, str],
        timeout_seconds: float,
    ) -> dict[str, Any]:
        del timeout_seconds
        self.last_path = path
        self.last_payload = payload
        self.last_headers = headers
        return self.generation


def _settings() -> LlamaCppSettings:
    return LlamaCppSettings(
        base_url="http://127.0.0.1:8080",
        provider_api_key="provider-secret-00000000000000000",
        service_auth_secret="service-secret-000000000000000000",
    )


def _request() -> InferenceRequest:
    from uuid import uuid4

    return InferenceRequest(
        request_id=uuid4(),
        correlation_id=uuid4(),
        locale="en",
        prompt="Summarize only this evidence.",
        max_output_tokens=128,
        temperature=0.4,
    )


def test_provider_uses_fixed_route_identity_auth_and_non_thinking_mode() -> None:
    async def scenario() -> None:
        transport = StubTransport()
        generation = await LlamaCppProvider(_settings(), transport).generate(_request())

        assert generation.answer == "Verified summary"
        assert transport.last_path == "/v1/chat/completions"
        assert transport.last_headers["Authorization"].startswith("Bearer ")
        assert transport.last_payload["model"] == "nextops-qwen3-8b-q4-k-m"
        assert transport.last_payload["stream"] is False
        assert transport.last_payload["messages"][-1]["content"].endswith("/no_think")
        assert "tools" not in transport.last_payload

    asyncio.run(scenario())


def test_provider_rejects_wrong_model_and_reports_safe_readiness() -> None:
    async def scenario() -> None:
        transport = StubTransport()
        transport.generation["model"] = "unexpected-model"
        provider = LlamaCppProvider(_settings(), transport)

        with pytest.raises(ApplicationError) as captured:
            await provider.generate(_request())
        assert captured.value.code is ErrorCode.DEPENDENCY_UNAVAILABLE
        assert captured.value.details == {}

        readiness = await provider.readiness()
        assert readiness.state is ReadinessState.READY
        assert readiness.cpu_only_required is True

    asyncio.run(scenario())


def test_provider_rejects_malformed_completion_without_raw_details() -> None:
    async def scenario() -> None:
        transport = StubTransport()
        transport.generation["choices"] = []

        with pytest.raises(ApplicationError) as captured:
            await LlamaCppProvider(_settings(), transport).generate(_request())
        assert captured.value.message_key == "inference.provider_response_invalid"
        assert captured.value.details == {}

    asyncio.run(scenario())


def test_provider_rejects_usage_above_the_request_limit() -> None:
    async def scenario() -> None:
        transport = StubTransport()
        transport.generation["usage"]["completion_tokens"] = 129

        with pytest.raises(ApplicationError) as captured:
            await LlamaCppProvider(_settings(), transport).generate(_request())
        assert captured.value.message_key == "inference.provider_response_invalid"

    asyncio.run(scenario())
