"""Bounded inference scheduling tests with no model dependency."""

import asyncio
from datetime import UTC, datetime

import pytest

from nextops.application.errors import ApplicationError
from nextops.contracts.errors import ErrorCode
from nextops.inference.contracts import (
    InferenceRequest,
    ProviderGeneration,
    ProviderReadiness,
    ReadinessState,
)
from nextops.inference.scheduler import BoundedInferenceService, SchedulerLimits


def _request() -> InferenceRequest:
    from uuid import uuid4

    return InferenceRequest(
        request_id=uuid4(),
        correlation_id=uuid4(),
        locale="en",
        prompt="Summarize the supplied evidence.",
        max_output_tokens=64,
        temperature=0.2,
    )


class ControlledProvider:
    def __init__(self) -> None:
        self.started = asyncio.Event()
        self.release = asyncio.Event()

    async def generate(self, request: InferenceRequest) -> ProviderGeneration:
        del request
        self.started.set()
        await self.release.wait()
        now = datetime.now(UTC)
        return ProviderGeneration(
            answer="Bounded answer",
            model_id="nextops-qwen3-8b-q4-k-m",
            prompt_tokens=5,
            completion_tokens=3,
            finish_reason="stop",
            started_at=now,
            completed_at=now,
        )

    async def readiness(self) -> ProviderReadiness:
        return ProviderReadiness(
            state=ReadinessState.READY,
            model_id="nextops-qwen3-8b-q4-k-m",
            runtime_version="v0.4.1",
            cpu_only_required=True,
        )


def test_one_active_plus_two_queued_rejects_fourth_and_recovers() -> None:
    async def scenario() -> None:
        provider = ControlledProvider()
        service = BoundedInferenceService(
            provider,
            SchedulerLimits(queue_timeout_seconds=2, provider_timeout_seconds=2),
        )
        tasks = [asyncio.create_task(service.generate(_request())) for _ in range(3)]
        await provider.started.wait()
        await asyncio.sleep(0)

        with pytest.raises(ApplicationError) as captured:
            await service.generate(_request())
        assert captured.value.code is ErrorCode.OVERLOADED

        readiness = await service.readiness()
        assert readiness.active_requests == 1
        assert readiness.queued_requests == 2
        provider.release.set()
        await asyncio.gather(*tasks)
        recovered = await service.readiness()
        assert recovered.active_requests == 0
        assert recovered.queued_requests == 0

    asyncio.run(scenario())


def test_provider_timeout_releases_capacity() -> None:
    async def scenario() -> None:
        provider = ControlledProvider()
        service = BoundedInferenceService(
            provider,
            SchedulerLimits(queue_timeout_seconds=1, provider_timeout_seconds=0.01),
        )

        with pytest.raises(ApplicationError) as captured:
            await service.generate(_request())
        assert captured.value.code is ErrorCode.TIMEOUT
        readiness = await service.readiness()
        assert readiness.active_requests == 0
        assert readiness.queued_requests == 0

    asyncio.run(scenario())


def test_queue_timeout_and_cancellation_both_release_capacity() -> None:
    async def scenario() -> None:
        provider = ControlledProvider()
        service = BoundedInferenceService(
            provider,
            SchedulerLimits(queue_timeout_seconds=0.01, provider_timeout_seconds=2),
        )
        active = asyncio.create_task(service.generate(_request()))
        await provider.started.wait()

        with pytest.raises(ApplicationError) as captured:
            await service.generate(_request())
        assert captured.value.message_key == "inference.queue_timeout"

        active.cancel()
        with pytest.raises(asyncio.CancelledError):
            await active
        recovered = await service.readiness()
        assert recovered.active_requests == 0
        assert recovered.queued_requests == 0

    asyncio.run(scenario())
