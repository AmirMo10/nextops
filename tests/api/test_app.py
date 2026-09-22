"""Minimal authenticated API contract tests."""

from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from nextops.api.app import create_app
from nextops.application.errors import ApplicationError
from nextops.contracts.assistant import AssistantRequest, AssistantResponse
from nextops.contracts.durable import (
    AuthenticatedSession,
    BootstrapRequest,
    BootstrapResult,
    EvidenceSource,
    FixtureResult,
    LeaseGrant,
    LoginRequest,
    RecoveryRequest,
    RecoveryResult,
    RunCreateRequest,
    RunRecord,
    RunStatus,
    SessionToken,
)
from nextops.contracts.errors import ErrorCode
from nextops.contracts.models import ActorContext, Role
from nextops.contracts.monitoring import MonitoringMetric, MonitoringSummary
from nextops.inference.contracts import FinishReason, InferenceReadiness, ReadinessState

NOW = datetime(2026, 9, 21, 9, 0, tzinfo=UTC)
ORG_ID = UUID("10000000-0000-4000-8000-000000000001")
ENV_ID = UUID("20000000-0000-4000-8000-000000000001")
ACTOR_ID = UUID("30000000-0000-4000-8000-000000000001")
TARGET_ID = UUID("40000000-0000-4000-8000-000000000001")
RUN_ID = UUID("50000000-0000-4000-8000-000000000001")


class FakeService:
    """Deterministic service double; database behavior has separate integration tests."""

    def __init__(self) -> None:
        self.actor = ActorContext(
            subject_id=ACTOR_ID,
            organization_id=ORG_ID,
            environment_id=ENV_ID,
            roles=frozenset({Role.ADMIN}),
            scopes=frozenset({"runs.read", "zabbix.read"}),
        )
        self.created_with_actor: ActorContext | None = None
        self.raise_on_create: ApplicationError | None = None

    def bootstrap(
        self, request: BootstrapRequest, supplied_secret: str, correlation_id: UUID
    ) -> BootstrapResult:
        del request, supplied_secret, correlation_id
        return BootstrapResult(
            organization_id=ORG_ID,
            environment_id=ENV_ID,
            admin_identity_id=ACTOR_ID,
            fixture_target_id=TARGET_ID,
            authenticated_session=self._session(),
        )

    def login(self, request: LoginRequest, correlation_id: UUID) -> AuthenticatedSession:
        del request, correlation_id
        return self._session()

    def authenticate(self, token: str) -> ActorContext:
        if token != "valid-bearer-token-that-is-long-enough":
            raise ApplicationError(ErrorCode.UNAUTHENTICATED, "auth.session_invalid")
        return self.actor

    def recover(
        self, request: RecoveryRequest, supplied_secret: str, correlation_id: UUID
    ) -> RecoveryResult:
        del request, supplied_secret, correlation_id
        return RecoveryResult(
            identity_id=ACTOR_ID,
            revoked_session_count=1,
            credential_version=2,
        )

    def create_run(
        self,
        actor: ActorContext,
        request: RunCreateRequest,
        idempotency_key: str,
        correlation_id: UUID,
    ) -> RunRecord:
        del request, idempotency_key, correlation_id
        self.created_with_actor = actor
        if self.raise_on_create is not None:
            raise self.raise_on_create
        return self._record(RunStatus.PENDING)

    def get_run(self, actor: ActorContext, run_id: UUID) -> RunRecord:
        del actor, run_id
        return self._record(RunStatus.SUCCEEDED, with_result=True)

    def claim_lease(self, run_id: UUID, owner_id: str) -> LeaseGrant:
        return LeaseGrant(
            run_id=run_id,
            owner_id=owner_id,
            lease_token="lease-token-that-is-long-enough-for-contract",
            generation=1,
            acquired_at=NOW,
            expires_at=NOW + timedelta(seconds=30),
        )

    def complete_fixture(self, grant: LeaseGrant) -> RunRecord:
        del grant
        return self._record(RunStatus.SUCCEEDED, with_result=True)

    def _session(self) -> AuthenticatedSession:
        return AuthenticatedSession(
            actor=self.actor,
            session=SessionToken(
                access_token="valid-bearer-token-that-is-long-enough",
                expires_at=NOW + timedelta(hours=1),
            ),
        )

    def _record(self, status: RunStatus, *, with_result: bool = False) -> RunRecord:
        result = None
        if with_result:
            result = FixtureResult(
                run_id=RUN_ID,
                status=RunStatus.SUCCEEDED,
                locale="fa",
                answer="این داده آزمایشی است و اتصال زنده انجام نشده است.",
                source=EvidenceSource(
                    connector="fixture",
                    method="zabbix.host.read",
                    collected_at=NOW,
                    measured_at=NOW,
                ),
                organization_id=ORG_ID,
                environment_id=ENV_ID,
                target_id=TARGET_ID,
                is_partial=False,
                is_stale=True,
                audit_event_id=uuid4(),
            )
        return RunRecord(
            run_id=RUN_ID,
            request_id=uuid4(),
            correlation_id=uuid4(),
            status=status,
            locale="fa",
            created_at=NOW,
            updated_at=NOW,
            result=result,
        )


class FakeInferenceGateway:
    """Deterministic protected-AI boundary for application route tests."""

    def __init__(self) -> None:
        self.last_request: AssistantRequest | None = None

    async def readiness(self) -> InferenceReadiness:
        return InferenceReadiness(
            state=ReadinessState.READY,
            model_id="nextops-qwen3-8b-q4-k-m",
            runtime_version="v0.4.1",
            cpu_only_required=True,
            max_active_requests=1,
            max_queued_requests=2,
            active_requests=0,
            queued_requests=0,
        )

    async def generate(self, request: AssistantRequest, correlation_id: UUID) -> AssistantResponse:
        self.last_request = request
        return AssistantResponse(
            request_id=uuid4(),
            correlation_id=correlation_id,
            locale=request.locale,
            answer="پاسخ آزمایشی مدل داخلی",
            model_id="nextops-qwen3-8b-q4-k-m",
            prompt_tokens=10,
            completion_tokens=8,
            finish_reason=FinishReason.STOP,
            started_at=NOW,
            completed_at=NOW + timedelta(seconds=1),
            queue_ms=0,
            cpu_only_required=True,
            evidence_mode="model_only",
            live_monitoring_data=False,
        )


class FakeMonitoringGateway:
    """Deterministic source-qualified monitoring boundary."""

    async def summary(self) -> MonitoringSummary:
        return MonitoringSummary(
            source_version="7.0.30",
            host="Zabbix server",
            collected_at=NOW,
            metrics=(
                MonitoringMetric(
                    name="CPU idle time",
                    key="system.cpu.util[,idle]",
                    value="91.25",
                    units="%",
                    measured_at=NOW - timedelta(seconds=15),
                    stale=False,
                ),
            ),
            active_problems=(),
        )


def test_health_is_unversioned_and_contains_no_dependency_claim() -> None:
    client = TestClient(create_app(FakeService()))

    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "nextops-app"}


def test_panel_is_local_bilingual_and_sets_browser_security_headers() -> None:
    client = TestClient(create_app(FakeService()))

    response = client.get("/")
    javascript = client.get("/assets/app.js")

    assert response.status_code == 200
    assert "NextOps" in response.text
    assert "محیط کنترل‌شده ارزیابی کاربران" in javascript.text
    assert "max_output_tokens: 128" in javascript.text
    assert "زمان پردازش مدل محلی به پایان رسید" in javascript.text
    assert "https://" not in response.text
    assert "https://" not in javascript.text
    assert response.headers["x-frame-options"] == "DENY"
    assert "default-src 'self'" in response.headers["content-security-policy"]


def test_assistant_requires_local_session_and_labels_model_only_output() -> None:
    client = TestClient(create_app(FakeService(), FakeInferenceGateway()))

    unauthenticated = client.post(
        "/api/v1/assistant/generate",
        json={"locale": "fa", "question": "یک پاسخ آزمایشی ارائه کن"},
    )
    response = client.post(
        "/api/v1/assistant/generate",
        headers={"Authorization": "Bearer valid-bearer-token-that-is-long-enough"},
        json={"locale": "fa", "question": "یک پاسخ آزمایشی ارائه کن"},
    )

    assert unauthenticated.status_code == 401
    assert response.status_code == 200
    assert response.json()["evidence_mode"] == "model_only"
    assert response.json()["live_monitoring_data"] is False
    assert response.json()["answer"] == "پاسخ آزمایشی مدل داخلی"


def test_assistant_readiness_is_authenticated() -> None:
    client = TestClient(create_app(FakeService(), FakeInferenceGateway()))

    response = client.get(
        "/api/v1/assistant/ready",
        headers={"Authorization": "Bearer valid-bearer-token-that-is-long-enough"},
    )

    assert response.status_code == 200
    assert response.json()["state"] == "ready"


def test_investigation_requires_session_and_returns_exact_live_evidence() -> None:
    inference = FakeInferenceGateway()
    client = TestClient(create_app(FakeService(), inference, FakeMonitoringGateway()))

    unauthenticated = client.post(
        "/api/v1/investigate",
        json={"locale": "en", "question": "What is the current state?"},
    )
    response = client.post(
        "/api/v1/investigate",
        headers={"Authorization": "Bearer valid-bearer-token-that-is-long-enough"},
        json={"locale": "en", "question": "What is the current state?"},
    )

    assert unauthenticated.status_code == 401
    assert response.status_code == 200
    body = response.json()
    assert body["evidence_mode"] == "live_zabbix"
    assert body["live_monitoring_data"] is True
    assert body["evidence"]["source_version"] == "7.0.30"
    assert body["evidence"]["metrics"][0]["stale"] is False
    assert inference.last_request is not None
    assert inference.last_request.max_output_tokens == 128


def test_run_actor_is_derived_from_bearer_session_and_fixture_is_explicit() -> None:
    service = FakeService()
    client = TestClient(create_app(service))

    response = client.post(
        "/api/v1/runs",
        headers={
            "Authorization": "Bearer valid-bearer-token-that-is-long-enough",
            "Idempotency-Key": "request-0001",
        },
        json={
            "target_id": str(TARGET_ID),
            "action": "zabbix.host.read",
            "question": "Fixture question using the Persian locale",
            "locale": "fa",
            "parameters": {},
        },
    )

    assert response.status_code == 201
    assert service.created_with_actor == service.actor
    body = response.json()
    assert body["result"]["source"]["connector"] == "fixture"
    assert body["result"]["is_stale"] is True
    assert body["result"]["audit_event_id"]


def test_run_payload_rejects_client_supplied_actor_context() -> None:
    client = TestClient(create_app(FakeService()))

    response = client.post(
        "/api/v1/runs",
        headers={
            "Authorization": "Bearer valid-bearer-token-that-is-long-enough",
            "Idempotency-Key": "request-0001",
        },
        json={
            "target_id": str(TARGET_ID),
            "action": "zabbix.host.read",
            "question": "Untrusted actor injection",
            "locale": "en",
            "actor": {"organization_id": str(ORG_ID)},
        },
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "invalid_request"


def test_revoked_or_unknown_bearer_gets_structured_401_with_correlation() -> None:
    client = TestClient(create_app(FakeService()))
    correlation_id = str(uuid4())

    response = client.get(
        f"/api/v1/runs/{RUN_ID}",
        headers={
            "Authorization": "Bearer revoked-token-that-is-long-enough",
            "X-Correlation-ID": correlation_id,
        },
    )

    assert response.status_code == 401
    assert response.json()["error"] == {
        "code": "unauthenticated",
        "message_key": "auth.session_invalid",
        "correlation_id": correlation_id,
        "retryable": False,
        "details": {},
    }


def test_idempotency_conflict_maps_to_structured_409() -> None:
    service = FakeService()
    service.raise_on_create = ApplicationError(ErrorCode.CONFLICT, "run.idempotency_conflict")
    client = TestClient(create_app(service))

    response = client.post(
        "/api/v1/runs",
        headers={
            "Authorization": "Bearer valid-bearer-token-that-is-long-enough",
            "Idempotency-Key": "request-0001",
        },
        json={
            "target_id": str(TARGET_ID),
            "action": "zabbix.host.read",
            "question": "Changed intent",
            "locale": "en",
        },
    )

    assert response.status_code == 409
    assert response.json()["error"]["message_key"] == "run.idempotency_conflict"
