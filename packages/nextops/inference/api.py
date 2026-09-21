"""Authenticated HTTP boundary for the isolated local inference service."""

from collections.abc import Awaitable, Callable
from typing import Annotated, Literal, Protocol
from uuid import UUID, uuid4

from fastapi import Depends, FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import Field

from nextops.application.errors import ApplicationError
from nextops.contracts.errors import ErrorCode, ErrorDetail
from nextops.contracts.models import FrozenContract
from nextops.inference.configuration import LlamaCppSettings
from nextops.inference.contracts import (
    InferenceReadiness,
    InferenceRequest,
    InferenceResult,
    ReadinessState,
)
from nextops.inference.llama_cpp import LlamaCppProvider
from nextops.inference.scheduler import BoundedInferenceService, SchedulerLimits
from nextops.security.secrets import verify_deployment_secret

STATUS_BY_ERROR = {
    ErrorCode.INVALID_REQUEST: 400,
    ErrorCode.UNAUTHENTICATED: 401,
    ErrorCode.POLICY_DENIED: 403,
    ErrorCode.NOT_FOUND: 404,
    ErrorCode.CONFLICT: 409,
    ErrorCode.OVERLOADED: 429,
    ErrorCode.TIMEOUT: 504,
    ErrorCode.DEPENDENCY_UNAVAILABLE: 503,
    ErrorCode.INTERNAL_ERROR: 500,
}


class InferenceService(Protocol):
    async def generate(self, request: InferenceRequest) -> InferenceResult: ...

    async def readiness(self) -> InferenceReadiness: ...


class GenerationPayload(FrozenContract):
    """Untrusted client fields; provider controls are intentionally absent."""

    request_id: UUID
    locale: Literal["en", "fa"]
    prompt: str = Field(min_length=1, max_length=12_000)
    max_output_tokens: int = Field(default=512, ge=1, le=1_024)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


def create_inference_app(service: InferenceService, service_auth_secret: str) -> FastAPI:
    """Build the local service around an injected scheduler."""

    app = FastAPI(title="NextOps local inference API", version="1.0.0")
    bearer = HTTPBearer(auto_error=False)

    @app.middleware("http")
    async def correlation_middleware(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        raw = request.headers.get("X-Correlation-ID")
        try:
            correlation_id = UUID(raw) if raw else uuid4()
        except ValueError:
            correlation_id = uuid4()
        request.state.correlation_id = correlation_id
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = str(correlation_id)
        return response

    @app.exception_handler(ApplicationError)
    async def application_error_handler(request: Request, error: ApplicationError) -> JSONResponse:
        detail = ErrorDetail(
            code=error.code,
            message_key=error.message_key,
            correlation_id=_correlation_id(request),
            retryable=error.retryable,
            details=error.details,
        )
        return JSONResponse(
            status_code=STATUS_BY_ERROR[error.code],
            content={"error": detail.model_dump(mode="json")},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request, error: RequestValidationError
    ) -> JSONResponse:
        safe_errors = [
            {
                "location": ".".join(str(part) for part in item["loc"]),
                "type": item["type"],
            }
            for item in error.errors()
        ]
        detail = ErrorDetail(
            code=ErrorCode.INVALID_REQUEST,
            message_key="request.validation_failed",
            correlation_id=_correlation_id(request),
            details={"errors": safe_errors},
        )
        return JSONResponse(status_code=422, content={"error": detail.model_dump(mode="json")})

    def authenticate_service(
        credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
    ) -> bool:
        if (
            credentials is None
            or credentials.scheme.lower() != "bearer"
            or not verify_deployment_secret(service_auth_secret, credentials.credentials)
        ):
            raise ApplicationError(ErrorCode.UNAUTHENTICATED, "inference.service_auth_required")
        return True

    @app.get("/healthz")
    async def health() -> dict[str, str]:
        return {"status": "ok", "service": "nextops-ai"}

    @app.get("/readyz", response_model=InferenceReadiness)
    async def readiness(response: Response) -> InferenceReadiness:
        result = await service.readiness()
        if result.state is not ReadinessState.READY:
            response.status_code = 503
        return result

    @app.post(
        "/api/v1/generate",
        response_model=InferenceResult,
        dependencies=[Depends(authenticate_service)],
    )
    async def generate(
        request: Request,
        payload: GenerationPayload,
    ) -> InferenceResult:
        bounded_request = InferenceRequest(
            request_id=payload.request_id,
            correlation_id=_correlation_id(request),
            locale=payload.locale,
            prompt=payload.prompt,
            max_output_tokens=payload.max_output_tokens,
            temperature=payload.temperature,
        )
        return await service.generate(bounded_request)

    return app


def create_runtime_inference_app() -> FastAPI:
    """Load deployment configuration and construct the production ASGI app."""

    settings = LlamaCppSettings.from_environment()
    provider = LlamaCppProvider(settings)
    service = BoundedInferenceService(
        provider,
        SchedulerLimits(
            queue_timeout_seconds=settings.queue_timeout_seconds,
            provider_timeout_seconds=settings.request_timeout_seconds,
        ),
    )
    return create_inference_app(service, settings.service_auth_secret.get_secret_value())


def _correlation_id(request: Request) -> UUID:
    value = getattr(request.state, "correlation_id", None)
    return value if isinstance(value, UUID) else uuid4()
