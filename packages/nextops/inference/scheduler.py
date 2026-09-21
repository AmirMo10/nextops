"""Atomic bounded admission and timeout handling for CPU inference."""

from __future__ import annotations

import asyncio
from time import monotonic

from pydantic import BaseModel, ConfigDict, Field

from nextops.application.errors import ApplicationError
from nextops.contracts.errors import ErrorCode
from nextops.inference.contracts import (
    MODEL_ID,
    InferenceReadiness,
    InferenceRequest,
    InferenceResult,
    LLMProvider,
    ProviderReadiness,
    ReadinessState,
    elapsed_milliseconds,
)


class SchedulerLimits(BaseModel):
    """Stage 1B fixed concurrency and bounded timeout policy."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    max_active_requests: int = Field(default=1, ge=1, le=1)
    max_queued_requests: int = Field(default=2, ge=2, le=2)
    queue_timeout_seconds: float = Field(default=5.0, ge=0.01, le=60.0)
    provider_timeout_seconds: float = Field(default=120.0, ge=0.01, le=600.0)


class BoundedInferenceService:
    """Allow one generation plus two waiters and clean up every exit path."""

    def __init__(self, provider: LLMProvider, limits: SchedulerLimits | None = None) -> None:
        self._provider = provider
        self._limits = limits or SchedulerLimits()
        self._semaphore = asyncio.Semaphore(self._limits.max_active_requests)
        self._state_lock = asyncio.Lock()
        self._active_requests = 0
        self._queued_requests = 0

    async def generate(self, request: InferenceRequest) -> InferenceResult:
        queued_at = monotonic()
        async with self._state_lock:
            if self._active_requests + self._queued_requests >= (
                self._limits.max_active_requests + self._limits.max_queued_requests
            ):
                raise ApplicationError(
                    ErrorCode.OVERLOADED,
                    "inference.capacity_exhausted",
                    retryable=True,
                )
            self._queued_requests += 1

        acquired = False
        try:
            try:
                await asyncio.wait_for(
                    self._semaphore.acquire(),
                    timeout=self._limits.queue_timeout_seconds,
                )
                acquired = True
            except TimeoutError as error:
                raise ApplicationError(
                    ErrorCode.TIMEOUT,
                    "inference.queue_timeout",
                    retryable=True,
                ) from error
            finally:
                async with self._state_lock:
                    self._queued_requests -= 1

            async with self._state_lock:
                self._active_requests += 1
            started = monotonic()
            try:
                try:
                    generation = await asyncio.wait_for(
                        self._provider.generate(request),
                        timeout=self._limits.provider_timeout_seconds,
                    )
                except TimeoutError as error:
                    raise ApplicationError(
                        ErrorCode.TIMEOUT,
                        "inference.provider_timeout",
                        retryable=True,
                    ) from error
            finally:
                async with self._state_lock:
                    self._active_requests -= 1

            return InferenceResult(
                **generation.model_dump(),
                request_id=request.request_id,
                correlation_id=request.correlation_id,
                locale=request.locale,
                queue_ms=elapsed_milliseconds(queued_at, started),
                cpu_only_required=True,
            )
        finally:
            if acquired:
                self._semaphore.release()

    async def readiness(self) -> InferenceReadiness:
        """Return provider state with an atomic snapshot of safe counters."""

        try:
            provider_readiness = await self._provider.readiness()
        except ApplicationError:
            provider_readiness = ProviderReadiness(
                state=ReadinessState.UNAVAILABLE,
                model_id=MODEL_ID,
                runtime_version="v0.4.1",
                cpu_only_required=True,
            )
        async with self._state_lock:
            active = self._active_requests
            queued = self._queued_requests
        return InferenceReadiness(
            **provider_readiness.model_dump(),
            max_active_requests=1,
            max_queued_requests=2,
            active_requests=active,
            queued_requests=queued,
        )
