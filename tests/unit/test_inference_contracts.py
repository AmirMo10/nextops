"""Stage 1B inference trust-boundary contract tests."""

from datetime import UTC, datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from nextops.inference.configuration import LlamaCppSettings
from nextops.inference.contracts import InferenceRequest, ProviderGeneration


def test_request_is_bounded_and_rejects_provider_controls() -> None:
    request = InferenceRequest(
        request_id=uuid4(),
        correlation_id=uuid4(),
        locale="fa",
        prompt="وضعیت سرویس را خلاصه کن",
        max_output_tokens=256,
        temperature=0.6,
    )

    assert request.max_output_tokens == 256
    with pytest.raises(ValidationError):
        InferenceRequest(
            request_id=uuid4(),
            correlation_id=uuid4(),
            locale="en",
            prompt="diagnose",
            max_output_tokens=2048,
            temperature=0.6,
        )
    with pytest.raises(ValidationError):
        InferenceRequest(
            request_id=uuid4(),
            correlation_id=uuid4(),
            locale="en",
            prompt="diagnose",
            max_output_tokens=128,
            temperature=0.6,
            model="attacker-controlled",  # type: ignore[call-arg]
        )


def test_provider_generation_requires_aware_ordered_timestamps() -> None:
    now = datetime.now(UTC)
    generation = ProviderGeneration(
        answer="No live infrastructure evidence was supplied.",
        model_id="nextops-qwen3-8b-q4-k-m",
        prompt_tokens=10,
        completion_tokens=8,
        finish_reason="stop",
        started_at=now,
        completed_at=now,
    )

    assert generation.completed_at >= generation.started_at
    with pytest.raises(ValidationError):
        ProviderGeneration(
            answer=generation.answer,
            model_id=generation.model_id,
            prompt_tokens=generation.prompt_tokens,
            completion_tokens=generation.completion_tokens,
            finish_reason=generation.finish_reason,
            started_at=now,
            completed_at=datetime(2026, 1, 1),
        )


def test_llama_cpp_settings_allow_only_loopback_and_distinct_secrets() -> None:
    settings = LlamaCppSettings(
        base_url="http://127.0.0.1:8080",
        provider_api_key="p" * 32,
        service_auth_secret="s" * 32,
    )

    assert settings.base_url == "http://127.0.0.1:8080"
    for unsafe_url in (
        "http://10.0.0.20:8080",
        "https://127.0.0.1:8080",
        "http://127.0.0.1:8080/v1",
    ):
        with pytest.raises(ValidationError):
            LlamaCppSettings(
                base_url=unsafe_url,
                provider_api_key="p" * 32,
                service_auth_secret="s" * 32,
            )

    with pytest.raises(ValidationError):
        LlamaCppSettings(
            base_url="http://127.0.0.1:8080",
            provider_api_key="x" * 32,
            service_auth_secret="x" * 32,
        )
