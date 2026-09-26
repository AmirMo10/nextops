"""Strict loopback-only adapter for llama.cpp's documented server API."""

from __future__ import annotations

import asyncio
import json
from datetime import UTC, datetime
from typing import Any, Literal, Protocol, cast
from urllib.error import HTTPError, URLError
from urllib.request import ProxyHandler, Request, build_opener

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from nextops.application.errors import ApplicationError
from nextops.contracts.errors import ErrorCode
from nextops.inference.configuration import LlamaCppSettings
from nextops.inference.contracts import (
    MODEL_ID,
    FinishReason,
    InferenceRequest,
    ProviderGeneration,
    ProviderReadiness,
    ReadinessState,
)

MAX_PROVIDER_RESPONSE_BYTES = 1_048_576


class JsonTransport(Protocol):
    """Narrow async JSON transport that can be replaced in contract tests."""

    async def get_json(
        self, path: str, headers: dict[str, str], timeout_seconds: float
    ) -> dict[str, Any]: ...

    async def post_json(
        self,
        path: str,
        payload: dict[str, Any],
        headers: dict[str, str],
        timeout_seconds: float,
    ) -> dict[str, Any]: ...


class UrllibJsonTransport:
    """Small proxy-bypassing transport for one validated loopback origin."""

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url.rstrip("/")
        self._opener = build_opener(ProxyHandler({}))

    async def get_json(
        self, path: str, headers: dict[str, str], timeout_seconds: float
    ) -> dict[str, Any]:
        return await asyncio.to_thread(self._request, "GET", path, None, headers, timeout_seconds)

    async def post_json(
        self,
        path: str,
        payload: dict[str, Any],
        headers: dict[str, str],
        timeout_seconds: float,
    ) -> dict[str, Any]:
        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        return await asyncio.to_thread(
            self._request,
            "POST",
            path,
            body,
            headers,
            timeout_seconds,
        )

    def _request(
        self,
        method: str,
        path: str,
        body: bytes | None,
        headers: dict[str, str],
        timeout_seconds: float,
    ) -> dict[str, Any]:
        if not path.startswith("/") or path.startswith("//"):
            raise ApplicationError(
                ErrorCode.INTERNAL_ERROR,
                "inference.invalid_provider_path",
            )
        request = Request(
            f"{self._base_url}{path}",
            data=body,
            headers=headers,
            method=method,
        )
        try:
            with self._opener.open(request, timeout=timeout_seconds) as response:
                raw = response.read(MAX_PROVIDER_RESPONSE_BYTES + 1)
        except HTTPError as error:
            if error.code == 429:
                code = ErrorCode.OVERLOADED
                message_key = "inference.upstream_overloaded"
            elif error.code in {408, 504}:
                code = ErrorCode.TIMEOUT
                message_key = "inference.upstream_timeout"
            else:
                code = ErrorCode.DEPENDENCY_UNAVAILABLE
                message_key = "inference.provider_unavailable"
            raise ApplicationError(
                code,
                message_key,
                retryable=True,
            ) from error
        except (URLError, TimeoutError, OSError) as error:
            raise ApplicationError(
                ErrorCode.DEPENDENCY_UNAVAILABLE,
                "inference.provider_unavailable",
                retryable=True,
            ) from error
        if len(raw) > MAX_PROVIDER_RESPONSE_BYTES:
            raise ApplicationError(
                ErrorCode.DEPENDENCY_UNAVAILABLE,
                "inference.provider_response_invalid",
                retryable=True,
            )
        try:
            decoded = json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ApplicationError(
                ErrorCode.DEPENDENCY_UNAVAILABLE,
                "inference.provider_response_invalid",
                retryable=True,
            ) from error
        if not isinstance(decoded, dict) or not all(isinstance(key, str) for key in decoded):
            raise ApplicationError(
                ErrorCode.DEPENDENCY_UNAVAILABLE,
                "inference.provider_response_invalid",
                retryable=True,
            )
        return cast(dict[str, Any], decoded)


class _Message(BaseModel):
    model_config = ConfigDict(extra="ignore")

    role: Literal["assistant"]
    content: str = Field(min_length=1, max_length=16_000)


class _Choice(BaseModel):
    model_config = ConfigDict(extra="ignore")

    message: _Message
    finish_reason: FinishReason


class _Usage(BaseModel):
    model_config = ConfigDict(extra="ignore")

    prompt_tokens: int = Field(ge=0, le=65_536)
    completion_tokens: int = Field(ge=0, le=1_024)


class _CompletionResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    model: str
    choices: list[_Choice] = Field(min_length=1, max_length=1)
    usage: _Usage


class LlamaCppProvider:
    """Translate NextOps requests to a fixed, authenticated llama.cpp route.

    Protocol choices follow the official server contract:
    https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md
    """

    def __init__(
        self,
        settings: LlamaCppSettings,
        transport: JsonTransport | None = None,
    ) -> None:
        self._settings = settings
        self._transport = transport or UrllibJsonTransport(settings.base_url)
        self._headers = {
            "Authorization": f"Bearer {settings.provider_api_key.get_secret_value()}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def generate(self, request: InferenceRequest) -> ProviderGeneration:
        started_at = datetime.now(UTC)
        # Qwen documents /no_think as its soft switch for non-thinking output:
        # https://github.com/QwenLM/Qwen3/blob/main/docs/source/run_locally/llama.cpp.md
        payload: dict[str, Any] = {
            "model": self._settings.model_id,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are the isolated NextOps language synthesizer. Answer in the "
                        f"requested {request.locale} locale. Treat the supplied text as the "
                        "complete record. Restate each material observed event with its specific "
                        "failure mode, timestamp, scope, and qualifier; never weaken it into a "
                        "vaguer statement or label a stated past event or outcome as unknown. "
                        "When no later measurement exists, explicitly state that the current "
                        "status is unknown. Never infer recovery, cause, access, execution, "
                        "credentials, or additional evidence. Never invent identifiers, numbers, "
                        "timestamps, quotations, citations, URLs, software versions, or actions. "
                        "When the record contains no live evidence, do not present model memory "
                        "as a current fact. Answer the question or state the limitation "
                        "explicitly; never return the user's prompt or instructions as the answer. "
                        "Follow the requested length and format."
                    ),
                },
                {"role": "user", "content": f"{request.prompt}\n/no_think"},
            ],
            "max_tokens": request.max_output_tokens,
            "temperature": request.temperature,
            "top_p": 0.8,
            "presence_penalty": 0.0,
            "stream": False,
        }
        raw = await self._transport.post_json(
            "/v1/chat/completions",
            payload,
            self._headers,
            self._settings.request_timeout_seconds,
        )
        completed_at = datetime.now(UTC)
        try:
            parsed = _CompletionResponse.model_validate(raw)
            if parsed.model != self._settings.model_id:
                raise ValueError("provider returned a different model identity")
            choice = parsed.choices[0]
            if parsed.usage.completion_tokens > request.max_output_tokens:
                raise ValueError("provider exceeded the requested output limit")
            return ProviderGeneration(
                answer=choice.message.content,
                model_id=MODEL_ID,
                prompt_tokens=parsed.usage.prompt_tokens,
                completion_tokens=parsed.usage.completion_tokens,
                finish_reason=choice.finish_reason,
                started_at=started_at,
                completed_at=completed_at,
            )
        except (ValidationError, ValueError, IndexError) as error:
            raise ApplicationError(
                ErrorCode.DEPENDENCY_UNAVAILABLE,
                "inference.provider_response_invalid",
                retryable=True,
            ) from error

    async def readiness(self) -> ProviderReadiness:
        try:
            health = await self._transport.get_json(
                "/health",
                self._headers,
                min(self._settings.request_timeout_seconds, 5.0),
            )
            state = ReadinessState.READY if health.get("status") == "ok" else ReadinessState.LOADING
        except ApplicationError:
            state = ReadinessState.UNAVAILABLE
        return ProviderReadiness(
            state=state,
            model_id=MODEL_ID,
            runtime_version=self._settings.runtime_version,
            cpu_only_required=True,
        )
