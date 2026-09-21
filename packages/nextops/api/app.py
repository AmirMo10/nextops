"""Minimal authenticated FastAPI surface for Stage 1A Increment 2."""

from collections.abc import Awaitable, Callable
from typing import Annotated, Protocol
from uuid import UUID, uuid4

from fastapi import Depends, FastAPI, Header, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.responses import Response

from nextops.application.errors import ApplicationError
from nextops.application.service import DurableAppService
from nextops.configuration import AppSettings
from nextops.contracts.durable import (
    AuthenticatedSession,
    BootstrapRequest,
    BootstrapResult,
    LeaseGrant,
    LoginRequest,
    RecoveryRequest,
    RecoveryResult,
    RunCreateRequest,
    RunRecord,
    RunStatus,
)
from nextops.contracts.errors import ErrorCode, ErrorDetail
from nextops.contracts.models import ActorContext
from nextops.persistence.database import create_database_engine, create_session_factory


class AppService(Protocol):
    """Interface used by HTTP routes and replaceable in boundary tests."""

    def bootstrap(
        self, request: BootstrapRequest, supplied_secret: str, correlation_id: UUID
    ) -> BootstrapResult: ...

    def login(self, request: LoginRequest, correlation_id: UUID) -> AuthenticatedSession: ...

    def authenticate(self, token: str) -> ActorContext: ...

    def recover(
        self, request: RecoveryRequest, supplied_secret: str, correlation_id: UUID
    ) -> RecoveryResult: ...

    def create_run(
        self,
        actor: ActorContext,
        request: RunCreateRequest,
        idempotency_key: str,
        correlation_id: UUID,
    ) -> RunRecord: ...

    def get_run(self, actor: ActorContext, run_id: UUID) -> RunRecord: ...

    def claim_lease(self, run_id: UUID, owner_id: str) -> LeaseGrant: ...

    def complete_fixture(self, grant: LeaseGrant) -> RunRecord: ...


STATUS_BY_ERROR = {
    ErrorCode.INVALID_REQUEST: 400,
    ErrorCode.UNAUTHENTICATED: 401,
    ErrorCode.POLICY_DENIED: 403,
    ErrorCode.NOT_FOUND: 404,
    ErrorCode.CONFLICT: 409,
    ErrorCode.DEPENDENCY_UNAVAILABLE: 503,
    ErrorCode.INTERNAL_ERROR: 500,
}


def create_app(service: AppService) -> FastAPI:
    """Build the API around an injected durable service."""

    app = FastAPI(title="NextOps local API", version="1.0.0")
    bearer = HTTPBearer(auto_error=False)

    @app.middleware("http")
    async def correlation_middleware(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        raw_correlation = request.headers.get("X-Correlation-ID")
        try:
            correlation_id = UUID(raw_correlation) if raw_correlation else uuid4()
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
        return JSONResponse(
            status_code=422,
            content={"error": detail.model_dump(mode="json")},
        )

    def current_actor(
        credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
    ) -> ActorContext:
        if credentials is None or credentials.scheme.lower() != "bearer":
            raise ApplicationError(ErrorCode.UNAUTHENTICATED, "auth.session_required")
        return service.authenticate(credentials.credentials)

    @app.get("/healthz")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "nextops-app"}

    @app.post("/api/v1/bootstrap", response_model=BootstrapResult, status_code=201)
    def bootstrap(
        request: Request,
        payload: BootstrapRequest,
        bootstrap_secret: Annotated[
            str,
            Header(
                alias="X-NextOps-Bootstrap-Token",
                min_length=32,
                max_length=512,
            ),
        ],
    ) -> BootstrapResult:
        return service.bootstrap(payload, bootstrap_secret, _correlation_id(request))

    @app.post("/api/v1/login", response_model=AuthenticatedSession)
    def login(request: Request, payload: LoginRequest) -> AuthenticatedSession:
        return service.login(payload, _correlation_id(request))

    @app.post("/api/v1/recovery", response_model=RecoveryResult)
    def recover(
        request: Request,
        payload: RecoveryRequest,
        recovery_secret: Annotated[
            str,
            Header(
                alias="X-NextOps-Recovery-Token",
                min_length=32,
                max_length=512,
            ),
        ],
    ) -> RecoveryResult:
        return service.recover(payload, recovery_secret, _correlation_id(request))

    @app.get("/api/v1/me", response_model=ActorContext)
    def me(actor: Annotated[ActorContext, Depends(current_actor)]) -> ActorContext:
        return actor

    @app.post("/api/v1/runs", response_model=RunRecord, status_code=201)
    def create_run(
        request: Request,
        payload: RunCreateRequest,
        actor: Annotated[ActorContext, Depends(current_actor)],
        idempotency_key: Annotated[
            str,
            Header(alias="Idempotency-Key", min_length=8, max_length=128),
        ],
    ) -> RunRecord:
        record = service.create_run(
            actor,
            payload,
            idempotency_key,
            _correlation_id(request),
        )
        if record.status is RunStatus.PENDING:
            lease = service.claim_lease(record.run_id, "api-fixture-worker")
            return service.complete_fixture(lease)
        return record

    @app.get("/api/v1/runs/{run_id}", response_model=RunRecord)
    def get_run(
        run_id: UUID,
        actor: Annotated[ActorContext, Depends(current_actor)],
    ) -> RunRecord:
        return service.get_run(actor, run_id)

    return app


def create_runtime_app() -> FastAPI:
    """Load deployment configuration and create the production ASGI app."""

    settings = AppSettings.from_environment()
    engine = create_database_engine(settings.database_url.get_secret_value())
    service = DurableAppService(create_session_factory(engine), settings)
    return create_app(service)


def _correlation_id(request: Request) -> UUID:
    correlation_id = getattr(request.state, "correlation_id", None)
    return correlation_id if isinstance(correlation_id, UUID) else uuid4()
