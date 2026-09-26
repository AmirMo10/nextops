"""Transactional identity, run, lease, fixture, and audit application services."""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import delete, func, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from nextops.application.errors import ApplicationError
from nextops.configuration import AppSettings
from nextops.contracts.assistant import AssistantRequest, AssistantResponse
from nextops.contracts.durable import (
    AuditOutcome,
    AuthenticatedSession,
    BootstrapRequest,
    BootstrapResult,
    EvidenceSource,
    FixtureResult,
    LeaseGrant,
    LiveIncidentResult,
    LiveInvestigationResult,
    LoginRequest,
    RecoveryRequest,
    RecoveryResult,
    RunCreateRequest,
    RunFailure,
    RunRecord,
    RunStatus,
    SessionToken,
)
from nextops.contracts.errors import ErrorCode
from nextops.contracts.incidents import IncidentEvidence, IncidentInvestigationRequest
from nextops.contracts.models import ActorContext, InvestigationRequest, Role, TargetReference
from nextops.contracts.monitoring import MonitoringSummary
from nextops.domain.types import RiskClass
from nextops.persistence.models import (
    AuditEvent,
    Environment,
    Identity,
    Organization,
    Run,
    RunLease,
    Target,
)
from nextops.persistence.models import (
    Session as SessionModel,
)
from nextops.policy.authorization import AuthorizationPolicy, PolicyRule
from nextops.security.secrets import (
    PasswordService,
    hash_opaque_token,
    issue_opaque_token,
    verify_deployment_secret,
)

IDEMPOTENCY_PATTERN = re.compile(r"^[A-Za-z0-9._:-]{8,128}$")
FIXTURE_ACTION = "zabbix.host.read"
FIXTURE_SCOPE = "zabbix.read"
RUN_READ_SCOPE = "runs.read"
LINUX_READ_SCOPE = "linux.read"
LIVE_INVESTIGATION_ACTION = "zabbix.summary.read"
LIVE_INVESTIGATION_TARGET_KIND = "zabbix"
LIVE_INVESTIGATION_TARGET_NAME = "zabbix-live"
INCIDENT_INVESTIGATION_ACTION = "incident.explain.read"
INCIDENT_TARGET_KIND = "linux-zabbix"
INCIDENT_TARGET_PREFIX = "incident:"


class DurableAppService:
    """Coordinate all Stage 1A durable operations through PostgreSQL transactions."""

    def __init__(
        self,
        session_factory: sessionmaker[Session],
        settings: AppSettings,
        *,
        password_service: PasswordService | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._session_factory = session_factory
        self._settings = settings
        self._passwords = password_service or PasswordService()
        self._clock = clock or (lambda: datetime.now(UTC))
        self._dummy_password_hash = self._passwords.hash(issue_opaque_token())

    def bootstrap(
        self,
        request: BootstrapRequest,
        supplied_secret: str,
        correlation_id: UUID,
    ) -> BootstrapResult:
        """Create the one organization, environment, admin, target, audit, and session."""

        if not verify_deployment_secret(
            self._settings.bootstrap_secret.get_secret_value(), supplied_secret
        ):
            raise ApplicationError(ErrorCode.UNAUTHENTICATED, "auth.bootstrap_secret_invalid")

        now = self._now()
        organization_id = uuid4()
        environment_id = uuid4()
        identity_id = uuid4()
        target_id = uuid4()
        token = issue_opaque_token()
        expires_at = now + timedelta(seconds=self._settings.session_ttl_seconds)

        try:
            with self._session_factory() as session, session.begin():
                if session.scalar(select(Organization.id).limit(1)) is not None:
                    raise ApplicationError(
                        ErrorCode.CONFLICT, "identity.bootstrap_already_complete"
                    )

                session.add(
                    Organization(
                        id=organization_id,
                        singleton_key=1,
                        slug=request.organization_slug,
                        display_name=request.organization_name,
                    )
                )
                session.flush()
                session.add(
                    Environment(
                        id=environment_id,
                        organization_id=organization_id,
                        slug=request.environment_slug,
                        display_name=request.environment_name,
                    )
                )
                session.flush()
                identity = Identity(
                    id=identity_id,
                    organization_id=organization_id,
                    environment_id=environment_id,
                    username=request.admin_username,
                    password_hash=self._passwords.hash(request.admin_password.get_secret_value()),
                    roles=[Role.ADMIN.value],
                    scopes=[FIXTURE_SCOPE, LINUX_READ_SCOPE, RUN_READ_SCOPE],
                    is_active=True,
                    credential_version=1,
                )
                session.add(identity)
                session.add(
                    Target(
                        id=target_id,
                        organization_id=organization_id,
                        environment_id=environment_id,
                        kind="fixture",
                        name="stage-1a-fixture",
                        enabled=True,
                    )
                )
                session.add(
                    Target(
                        id=uuid4(),
                        organization_id=organization_id,
                        environment_id=environment_id,
                        kind=LIVE_INVESTIGATION_TARGET_KIND,
                        name=LIVE_INVESTIGATION_TARGET_NAME,
                        enabled=True,
                    )
                )
                session.flush()
                session.add(
                    SessionModel(
                        id=uuid4(),
                        identity_id=identity_id,
                        token_sha256=hash_opaque_token(token),
                        credential_version=1,
                        created_at=now,
                        expires_at=expires_at,
                    )
                )
                # Establish every referenced row in foreign-key order before audit.
                # Every flush remains in this transaction, so any failure still rolls
                # the complete bootstrap back.
                session.flush()
                self._add_audit(
                    session,
                    organization_id=organization_id,
                    environment_id=environment_id,
                    actor_id=identity_id,
                    correlation_id=correlation_id,
                    event_type="identity.bootstrap.completed",
                    outcome=AuditOutcome.ACCEPTED,
                    details={"target_kind": "fixture"},
                    occurred_at=now,
                )
                session.flush()
        except ApplicationError:
            raise
        except IntegrityError as exc:
            if self._is_bootstrap_conflict(exc):
                raise ApplicationError(
                    ErrorCode.CONFLICT, "identity.bootstrap_already_complete"
                ) from exc
            raise self._database_error() from exc
        except SQLAlchemyError as exc:
            raise self._database_error() from exc

        actor = ActorContext(
            subject_id=identity_id,
            organization_id=organization_id,
            environment_id=environment_id,
            roles=frozenset({Role.ADMIN}),
            scopes=frozenset({FIXTURE_SCOPE, LINUX_READ_SCOPE, RUN_READ_SCOPE}),
        )
        return BootstrapResult(
            organization_id=organization_id,
            environment_id=environment_id,
            admin_identity_id=identity_id,
            fixture_target_id=target_id,
            authenticated_session=AuthenticatedSession(
                actor=actor,
                session=SessionToken(access_token=token, expires_at=expires_at),
            ),
        )

    def login(self, request: LoginRequest, correlation_id: UUID) -> AuthenticatedSession:
        """Verify a local password and issue a hashed, expiring opaque session."""

        now = self._now()
        token = issue_opaque_token()
        expires_at = now + timedelta(seconds=self._settings.session_ttl_seconds)
        pending_error: ApplicationError | None = None
        actor: ActorContext | None = None

        try:
            with self._session_factory() as session, session.begin():
                identity = session.scalar(
                    select(Identity).where(Identity.username == request.username)
                )
                if identity is None:
                    self._passwords.verify(
                        self._dummy_password_hash, request.password.get_secret_value()
                    )
                    pending_error = ApplicationError(
                        ErrorCode.UNAUTHENTICATED, "auth.credentials_invalid"
                    )
                elif not identity.is_active or not self._passwords.verify(
                    identity.password_hash, request.password.get_secret_value()
                ):
                    self._add_audit(
                        session,
                        organization_id=identity.organization_id,
                        environment_id=identity.environment_id,
                        actor_id=identity.id,
                        correlation_id=correlation_id,
                        event_type="identity.login.denied",
                        outcome=AuditOutcome.DENIED,
                        details={},
                        occurred_at=now,
                    )
                    pending_error = ApplicationError(
                        ErrorCode.UNAUTHENTICATED, "auth.credentials_invalid"
                    )
                else:
                    if self._passwords.needs_rehash(identity.password_hash):
                        identity.password_hash = self._passwords.hash(
                            request.password.get_secret_value()
                        )
                    session.add(
                        SessionModel(
                            id=uuid4(),
                            identity_id=identity.id,
                            token_sha256=hash_opaque_token(token),
                            credential_version=identity.credential_version,
                            created_at=now,
                            expires_at=expires_at,
                        )
                    )
                    self._add_audit(
                        session,
                        organization_id=identity.organization_id,
                        environment_id=identity.environment_id,
                        actor_id=identity.id,
                        correlation_id=correlation_id,
                        event_type="identity.login.accepted",
                        outcome=AuditOutcome.ACCEPTED,
                        details={},
                        occurred_at=now,
                    )
                    actor = self._actor_from_identity(identity)
                session.flush()
        except SQLAlchemyError as exc:
            raise self._database_error() from exc

        if pending_error is not None:
            raise pending_error
        if actor is None:
            raise ApplicationError(ErrorCode.INTERNAL_ERROR, "auth.actor_derivation_failed")
        return AuthenticatedSession(
            actor=actor,
            session=SessionToken(access_token=token, expires_at=expires_at),
        )

    def authenticate(self, token: str) -> ActorContext:
        """Derive actor context solely from a valid server-side session."""

        now = self._now()
        try:
            with self._session_factory() as session:
                row = session.execute(
                    select(SessionModel, Identity)
                    .join(Identity, Identity.id == SessionModel.identity_id)
                    .where(SessionModel.token_sha256 == hash_opaque_token(token))
                ).one_or_none()
                if row is None:
                    raise ApplicationError(ErrorCode.UNAUTHENTICATED, "auth.session_invalid")
                stored_session, identity = row
                if (
                    stored_session.revoked_at is not None
                    or stored_session.expires_at <= now
                    or not identity.is_active
                    or stored_session.credential_version != identity.credential_version
                ):
                    raise ApplicationError(ErrorCode.UNAUTHENTICATED, "auth.session_invalid")
                return self._actor_from_identity(identity)
        except ApplicationError:
            raise
        except SQLAlchemyError as exc:
            raise self._database_error() from exc

    def logout(self, token: str, correlation_id: UUID) -> None:
        """Revoke one presented session without revealing whether an unknown token existed."""

        now = self._now()
        try:
            with self._session_factory() as session, session.begin():
                row = session.execute(
                    select(SessionModel, Identity)
                    .join(Identity, Identity.id == SessionModel.identity_id)
                    .where(SessionModel.token_sha256 == hash_opaque_token(token))
                    .with_for_update(of=SessionModel)
                ).one_or_none()
                if row is None:
                    return
                stored_session, identity = row
                if stored_session.revoked_at is not None:
                    return
                stored_session.revoked_at = now
                self._add_audit(
                    session,
                    organization_id=identity.organization_id,
                    environment_id=identity.environment_id,
                    actor_id=identity.id,
                    correlation_id=correlation_id,
                    event_type="identity.logout.accepted",
                    outcome=AuditOutcome.ACCEPTED,
                    details={},
                    occurred_at=now,
                )
                session.flush()
        except SQLAlchemyError as exc:
            raise self._database_error() from exc

    def recover(
        self,
        request: RecoveryRequest,
        supplied_secret: str,
        correlation_id: UUID,
    ) -> RecoveryResult:
        """Rotate the admin password and revoke every prior session atomically."""

        now = self._now()
        pending_error: ApplicationError | None = None
        result: RecoveryResult | None = None

        try:
            with self._session_factory() as session, session.begin():
                identity = session.scalar(
                    select(Identity).where(Identity.username == request.admin_username)
                )
                if identity is None or Role.ADMIN.value not in identity.roles:
                    verify_deployment_secret(
                        self._settings.recovery_secret.get_secret_value(), supplied_secret
                    )
                    pending_error = ApplicationError(
                        ErrorCode.UNAUTHENTICATED, "auth.recovery_denied"
                    )
                elif not verify_deployment_secret(
                    self._settings.recovery_secret.get_secret_value(), supplied_secret
                ):
                    self._add_audit(
                        session,
                        organization_id=identity.organization_id,
                        environment_id=identity.environment_id,
                        actor_id=identity.id,
                        correlation_id=correlation_id,
                        event_type="identity.recovery.denied",
                        outcome=AuditOutcome.DENIED,
                        details={},
                        occurred_at=now,
                    )
                    pending_error = ApplicationError(
                        ErrorCode.UNAUTHENTICATED, "auth.recovery_denied"
                    )
                else:
                    identity.password_hash = self._passwords.hash(
                        request.new_password.get_secret_value()
                    )
                    identity.credential_version += 1
                    identity.updated_at = now
                    revoke_result = session.execute(
                        update(SessionModel)
                        .where(
                            SessionModel.identity_id == identity.id,
                            SessionModel.revoked_at.is_(None),
                        )
                        .values(revoked_at=now)
                    )
                    revoked_count = int(getattr(revoke_result, "rowcount", 0))
                    self._add_audit(
                        session,
                        organization_id=identity.organization_id,
                        environment_id=identity.environment_id,
                        actor_id=identity.id,
                        correlation_id=correlation_id,
                        event_type="identity.recovery.completed",
                        outcome=AuditOutcome.ACCEPTED,
                        details={"revoked_session_count": revoked_count},
                        occurred_at=now,
                    )
                    result = RecoveryResult(
                        identity_id=identity.id,
                        revoked_session_count=revoked_count,
                        credential_version=identity.credential_version,
                    )
                session.flush()
        except SQLAlchemyError as exc:
            raise self._database_error() from exc

        if pending_error is not None:
            raise pending_error
        if result is None:
            raise ApplicationError(ErrorCode.INTERNAL_ERROR, "auth.recovery_result_missing")
        return result

    def create_run(
        self,
        actor: ActorContext,
        request: RunCreateRequest,
        idempotency_key: str,
        correlation_id: UUID,
    ) -> RunRecord:
        """Persist one policy-approved run or replay its identical prior record."""

        if IDEMPOTENCY_PATTERN.fullmatch(idempotency_key) is None:
            raise ApplicationError(ErrorCode.INVALID_REQUEST, "run.idempotency_key_invalid")

        now = self._now()
        request_id = uuid4()
        request_hash = self._request_hash(request)
        pending_error: ApplicationError | None = None
        record: RunRecord | None = None

        try:
            with self._session_factory() as session, session.begin():
                target = session.scalar(select(Target).where(Target.id == request.target_id))
                if (
                    target is None
                    or not target.enabled
                    or target.organization_id != actor.organization_id
                    or target.environment_id != actor.environment_id
                ):
                    self._add_audit(
                        session,
                        organization_id=actor.organization_id,
                        environment_id=actor.environment_id,
                        actor_id=actor.subject_id,
                        correlation_id=correlation_id,
                        event_type="run.create.denied",
                        outcome=AuditOutcome.DENIED,
                        details={"reason": "target_scope"},
                        occurred_at=now,
                    )
                    pending_error = ApplicationError(ErrorCode.POLICY_DENIED, "run.target_denied")
                else:
                    investigation = InvestigationRequest(
                        request_id=request_id,
                        correlation_id=correlation_id,
                        idempotency_key=idempotency_key,
                        target=TargetReference(
                            target_id=target.id,
                            organization_id=target.organization_id,
                            environment_id=target.environment_id,
                            kind=target.kind,
                        ),
                        action=request.action,
                        question=request.question,
                        locale=request.locale,
                        parameters=request.parameters,
                    )
                    policy = AuthorizationPolicy(
                        organization_id=actor.organization_id,
                        environment_id=actor.environment_id,
                        known_target_ids=frozenset({target.id}),
                        rules=(
                            PolicyRule(
                                action=FIXTURE_ACTION,
                                risk_class=RiskClass.READ_ONLY,
                                allowed_target_kinds=frozenset({"fixture"}),
                                required_scopes=frozenset({FIXTURE_SCOPE}),
                            ),
                        ),
                        version="stage-1a.2",
                    )
                    decision = policy.evaluate(investigation, actor)
                    if not decision.allowed:
                        self._add_audit(
                            session,
                            organization_id=actor.organization_id,
                            environment_id=actor.environment_id,
                            actor_id=actor.subject_id,
                            correlation_id=correlation_id,
                            event_type="run.create.denied",
                            outcome=AuditOutcome.DENIED,
                            details={"reason": decision.reason.value},
                            occurred_at=now,
                        )
                        pending_error = ApplicationError(
                            ErrorCode.POLICY_DENIED, "run.policy_denied"
                        )
                    else:
                        statement = (
                            insert(Run)
                            .values(
                                id=uuid4(),
                                request_id=request_id,
                                correlation_id=correlation_id,
                                organization_id=actor.organization_id,
                                environment_id=actor.environment_id,
                                target_id=target.id,
                                actor_id=actor.subject_id,
                                idempotency_key=idempotency_key,
                                request_sha256=request_hash,
                                action=request.action,
                                question=request.question,
                                locale=request.locale,
                                parameters=request.parameters,
                                status=RunStatus.PENDING.value,
                                created_at=now,
                                updated_at=now,
                            )
                            .on_conflict_do_nothing(constraint="uq_runs_actor_idempotency")
                            .returning(Run)
                        )
                        run = session.scalars(statement).one_or_none()
                        event_type = "run.created"
                        if run is None:
                            run = session.scalar(
                                select(Run).where(
                                    Run.organization_id == actor.organization_id,
                                    Run.actor_id == actor.subject_id,
                                    Run.idempotency_key == idempotency_key,
                                )
                            )
                            if run is None:
                                raise ApplicationError(
                                    ErrorCode.INTERNAL_ERROR, "run.idempotency_lookup_failed"
                                )
                            if run.request_sha256 != request_hash:
                                self._add_audit(
                                    session,
                                    organization_id=actor.organization_id,
                                    environment_id=actor.environment_id,
                                    actor_id=actor.subject_id,
                                    correlation_id=correlation_id,
                                    run_id=run.id,
                                    event_type="run.idempotency_conflict",
                                    outcome=AuditOutcome.DENIED,
                                    details={},
                                    occurred_at=now,
                                )
                                pending_error = ApplicationError(
                                    ErrorCode.CONFLICT, "run.idempotency_conflict"
                                )
                            else:
                                event_type = "run.replayed"
                        if pending_error is None:
                            self._add_audit(
                                session,
                                organization_id=actor.organization_id,
                                environment_id=actor.environment_id,
                                actor_id=actor.subject_id,
                                correlation_id=correlation_id,
                                run_id=run.id,
                                event_type=event_type,
                                outcome=AuditOutcome.ACCEPTED,
                                details={},
                                occurred_at=now,
                            )
                            record = self._run_record(run)
                session.flush()
        except ApplicationError:
            raise
        except SQLAlchemyError as exc:
            raise self._database_error() from exc

        if pending_error is not None:
            raise pending_error
        if record is None:
            raise ApplicationError(ErrorCode.INTERNAL_ERROR, "run.record_missing")
        return record

    def create_live_investigation(
        self,
        actor: ActorContext,
        request: AssistantRequest,
        correlation_id: UUID,
    ) -> RunRecord:
        """Persist a scoped live investigation before calling external local services."""

        now = self._now()
        request_hash = self._assistant_request_hash(request)
        idempotency_key = f"investigate:{correlation_id}"
        pending_error: ApplicationError | None = None
        record: RunRecord | None = None

        try:
            with self._session_factory() as session, session.begin():
                if FIXTURE_SCOPE not in actor.scopes:
                    self._add_audit(
                        session,
                        organization_id=actor.organization_id,
                        environment_id=actor.environment_id,
                        actor_id=actor.subject_id,
                        correlation_id=correlation_id,
                        event_type="investigation.create.denied",
                        outcome=AuditOutcome.DENIED,
                        details={"reason": "missing_zabbix_read_scope"},
                        occurred_at=now,
                    )
                    pending_error = ApplicationError(
                        ErrorCode.POLICY_DENIED, "investigation.scope_denied"
                    )
                else:
                    target_statement = (
                        insert(Target)
                        .values(
                            id=uuid4(),
                            organization_id=actor.organization_id,
                            environment_id=actor.environment_id,
                            kind=LIVE_INVESTIGATION_TARGET_KIND,
                            name=LIVE_INVESTIGATION_TARGET_NAME,
                            enabled=True,
                            created_at=now,
                        )
                        .on_conflict_do_nothing(constraint="uq_targets_scope_name")
                        .returning(Target)
                    )
                    target = session.scalars(target_statement).one_or_none()
                    if target is None:
                        target = session.scalar(
                            select(Target).where(
                                Target.organization_id == actor.organization_id,
                                Target.environment_id == actor.environment_id,
                                Target.name == LIVE_INVESTIGATION_TARGET_NAME,
                            )
                        )
                    if (
                        target is None
                        or not target.enabled
                        or target.kind != LIVE_INVESTIGATION_TARGET_KIND
                    ):
                        raise ApplicationError(
                            ErrorCode.DEPENDENCY_UNAVAILABLE,
                            "investigation.target_unavailable",
                            retryable=True,
                        )

                    statement = (
                        insert(Run)
                        .values(
                            id=uuid4(),
                            request_id=uuid4(),
                            correlation_id=correlation_id,
                            organization_id=actor.organization_id,
                            environment_id=actor.environment_id,
                            target_id=target.id,
                            actor_id=actor.subject_id,
                            idempotency_key=idempotency_key,
                            request_sha256=request_hash,
                            action=LIVE_INVESTIGATION_ACTION,
                            question=request.question,
                            locale=request.locale,
                            parameters={
                                "max_output_tokens": request.max_output_tokens,
                                "evidence_mode": "live_zabbix",
                            },
                            status=RunStatus.RUNNING.value,
                            created_at=now,
                            updated_at=now,
                        )
                        .on_conflict_do_nothing(constraint="uq_runs_actor_idempotency")
                        .returning(Run)
                    )
                    run = session.scalars(statement).one_or_none()
                    event_type = "investigation.started"
                    if run is None:
                        run = session.scalar(
                            select(Run).where(
                                Run.organization_id == actor.organization_id,
                                Run.actor_id == actor.subject_id,
                                Run.idempotency_key == idempotency_key,
                            )
                        )
                        if run is None:
                            raise ApplicationError(
                                ErrorCode.INTERNAL_ERROR, "investigation.lookup_failed"
                            )
                        if run.request_sha256 != request_hash:
                            pending_error = ApplicationError(
                                ErrorCode.CONFLICT, "investigation.correlation_conflict"
                            )
                        elif run.status == RunStatus.SUCCEEDED.value:
                            event_type = "investigation.replayed"
                        else:
                            pending_error = ApplicationError(
                                ErrorCode.CONFLICT, "investigation.already_in_progress"
                            )

                    if pending_error is None:
                        self._add_audit(
                            session,
                            organization_id=actor.organization_id,
                            environment_id=actor.environment_id,
                            actor_id=actor.subject_id,
                            correlation_id=correlation_id,
                            run_id=run.id,
                            event_type=event_type,
                            outcome=AuditOutcome.ACCEPTED,
                            details={"target_kind": LIVE_INVESTIGATION_TARGET_KIND},
                            occurred_at=now,
                        )
                        record = self._run_record(run)
                    else:
                        self._add_audit(
                            session,
                            organization_id=actor.organization_id,
                            environment_id=actor.environment_id,
                            actor_id=actor.subject_id,
                            correlation_id=correlation_id,
                            run_id=run.id,
                            event_type="investigation.replay.denied",
                            outcome=AuditOutcome.DENIED,
                            details={"reason": pending_error.message_key},
                            occurred_at=now,
                        )
                session.flush()
        except ApplicationError:
            raise
        except SQLAlchemyError as exc:
            raise self._database_error() from exc

        if pending_error is not None:
            raise pending_error
        if record is None:
            raise ApplicationError(ErrorCode.INTERNAL_ERROR, "investigation.record_missing")
        return record

    def complete_live_investigation(
        self,
        actor: ActorContext,
        run_id: UUID,
        assistant: AssistantResponse,
        evidence: MonitoringSummary,
    ) -> LiveInvestigationResult:
        """Atomically persist the bounded evidence, model result, and completion audit."""

        evidence_payload = evidence.model_dump(mode="json")
        evidence_sha256 = self._json_hash(evidence_payload)
        evidence_reference = f"run-evidence:{run_id}"
        now = self._now()

        try:
            with self._session_factory() as session, session.begin():
                run = session.scalar(
                    select(Run)
                    .where(
                        Run.id == run_id,
                        Run.organization_id == actor.organization_id,
                        Run.environment_id == actor.environment_id,
                        Run.actor_id == actor.subject_id,
                        Run.action == LIVE_INVESTIGATION_ACTION,
                    )
                    .with_for_update()
                )
                if run is None:
                    raise ApplicationError(ErrorCode.NOT_FOUND, "investigation.not_found")
                if run.status != RunStatus.RUNNING.value:
                    raise ApplicationError(ErrorCode.CONFLICT, "investigation.not_running")
                if assistant.correlation_id != run.correlation_id or assistant.locale != run.locale:
                    raise ApplicationError(
                        ErrorCode.DEPENDENCY_UNAVAILABLE,
                        "investigation.result_identity_mismatch",
                    )

                audit_event_id = uuid4()
                result = LiveInvestigationResult(
                    run_id=run.id,
                    status=RunStatus.SUCCEEDED,
                    locale=run.locale,
                    assistant=assistant,
                    evidence=evidence,
                    evidence_reference=evidence_reference,
                    evidence_sha256=evidence_sha256,
                    organization_id=run.organization_id,
                    environment_id=run.environment_id,
                    target_id=run.target_id,
                    is_partial=evidence.is_partial,
                    is_stale=any(metric.stale for metric in evidence.metrics),
                    audit_event_id=audit_event_id,
                )
                run.result = result.model_dump(mode="json")
                run.error = None
                run.status = RunStatus.SUCCEEDED.value
                run.updated_at = now
                self._add_audit(
                    session,
                    event_id=audit_event_id,
                    organization_id=run.organization_id,
                    environment_id=run.environment_id,
                    actor_id=run.actor_id,
                    correlation_id=run.correlation_id,
                    run_id=run.id,
                    event_type="investigation.completed",
                    outcome=AuditOutcome.ACCEPTED,
                    details={
                        "evidence_reference": evidence_reference,
                        "evidence_sha256": evidence_sha256,
                        "source": evidence.source,
                        "source_version": evidence.source_version,
                        "metric_count": len(evidence.metrics),
                        "problem_count": len(evidence.active_problems),
                        "is_partial": result.is_partial,
                        "partial_reasons": list(evidence.partial_reasons),
                        "is_stale": result.is_stale,
                        "model_id": assistant.model_id,
                        "answer_integrity_status": assistant.integrity_status,
                        "answer_limitations": list(assistant.limitations),
                    },
                    occurred_at=now,
                )
                session.flush()
                return result
        except ApplicationError:
            raise
        except SQLAlchemyError as exc:
            raise self._database_error() from exc

    def fail_live_investigation(
        self,
        actor: ActorContext,
        run_id: UUID,
        error: ApplicationError,
    ) -> None:
        """Persist a safe failure outcome and mandatory audit in one transaction."""

        now = self._now()
        safe_error = {
            "code": error.code.value,
            "message_key": error.message_key,
            "retryable": error.retryable,
        }
        try:
            with self._session_factory() as session, session.begin():
                run = session.scalar(
                    select(Run)
                    .where(
                        Run.id == run_id,
                        Run.organization_id == actor.organization_id,
                        Run.environment_id == actor.environment_id,
                        Run.actor_id == actor.subject_id,
                        Run.action == LIVE_INVESTIGATION_ACTION,
                    )
                    .with_for_update()
                )
                if run is None:
                    raise ApplicationError(ErrorCode.NOT_FOUND, "investigation.not_found")
                if run.status != RunStatus.RUNNING.value:
                    raise ApplicationError(ErrorCode.CONFLICT, "investigation.not_running")
                run.status = RunStatus.FAILED.value
                run.error = safe_error
                run.updated_at = now
                self._add_audit(
                    session,
                    organization_id=run.organization_id,
                    environment_id=run.environment_id,
                    actor_id=run.actor_id,
                    correlation_id=run.correlation_id,
                    run_id=run.id,
                    event_type="investigation.failed",
                    outcome=AuditOutcome.FAILED,
                    details=safe_error,
                    occurred_at=now,
                )
                session.flush()
        except ApplicationError:
            raise
        except SQLAlchemyError as exc:
            raise self._database_error() from exc

    def create_incident_investigation(
        self,
        actor: ActorContext,
        request: IncidentInvestigationRequest,
        correlation_id: UUID,
        allowed_target_ids: tuple[str, ...],
    ) -> RunRecord:
        """Persist a target-scoped Phase 2 investigation before evidence collection."""

        now = self._now()
        request_hash = self._json_hash(request.model_dump(mode="json"))
        idempotency_key = f"incident:{correlation_id}"
        required_scopes = {FIXTURE_SCOPE, LINUX_READ_SCOPE}
        pending_error: ApplicationError | None = None
        record: RunRecord | None = None

        try:
            with self._session_factory() as session, session.begin():
                missing_scopes = sorted(required_scopes.difference(actor.scopes))
                if missing_scopes:
                    self._add_audit(
                        session,
                        organization_id=actor.organization_id,
                        environment_id=actor.environment_id,
                        actor_id=actor.subject_id,
                        correlation_id=correlation_id,
                        event_type="incident.create.denied",
                        outcome=AuditOutcome.DENIED,
                        details={"reason": "missing_scope", "missing_scopes": missing_scopes},
                        occurred_at=now,
                    )
                    pending_error = ApplicationError(
                        ErrorCode.POLICY_DENIED, "incident.scope_denied"
                    )
                elif request.target_id not in allowed_target_ids:
                    self._add_audit(
                        session,
                        organization_id=actor.organization_id,
                        environment_id=actor.environment_id,
                        actor_id=actor.subject_id,
                        correlation_id=correlation_id,
                        event_type="incident.create.denied",
                        outcome=AuditOutcome.DENIED,
                        details={"reason": "target_not_allowlisted"},
                        occurred_at=now,
                    )
                    pending_error = ApplicationError(
                        ErrorCode.POLICY_DENIED, "incident.target_denied"
                    )
                else:
                    target_name = f"{INCIDENT_TARGET_PREFIX}{request.target_id}"
                    target_statement = (
                        insert(Target)
                        .values(
                            id=uuid4(),
                            organization_id=actor.organization_id,
                            environment_id=actor.environment_id,
                            kind=INCIDENT_TARGET_KIND,
                            name=target_name,
                            enabled=True,
                            created_at=now,
                        )
                        .on_conflict_do_nothing(constraint="uq_targets_scope_name")
                        .returning(Target)
                    )
                    target = session.scalars(target_statement).one_or_none()
                    if target is None:
                        target = session.scalar(
                            select(Target).where(
                                Target.organization_id == actor.organization_id,
                                Target.environment_id == actor.environment_id,
                                Target.name == target_name,
                            )
                        )
                    if target is None or not target.enabled or target.kind != INCIDENT_TARGET_KIND:
                        raise ApplicationError(
                            ErrorCode.DEPENDENCY_UNAVAILABLE,
                            "incident.target_unavailable",
                            retryable=True,
                        )

                    statement = (
                        insert(Run)
                        .values(
                            id=uuid4(),
                            request_id=uuid4(),
                            correlation_id=correlation_id,
                            organization_id=actor.organization_id,
                            environment_id=actor.environment_id,
                            target_id=target.id,
                            actor_id=actor.subject_id,
                            idempotency_key=idempotency_key,
                            request_sha256=request_hash,
                            action=INCIDENT_INVESTIGATION_ACTION,
                            question=request.question,
                            locale=request.locale,
                            parameters={
                                "target_id": request.target_id,
                                "max_output_tokens": request.max_output_tokens,
                                "evidence_mode": "live_zabbix_linux",
                            },
                            status=RunStatus.RUNNING.value,
                            created_at=now,
                            updated_at=now,
                        )
                        .on_conflict_do_nothing(constraint="uq_runs_actor_idempotency")
                        .returning(Run)
                    )
                    run = session.scalars(statement).one_or_none()
                    event_type = "incident.started"
                    if run is None:
                        run = session.scalar(
                            select(Run).where(
                                Run.organization_id == actor.organization_id,
                                Run.actor_id == actor.subject_id,
                                Run.idempotency_key == idempotency_key,
                            )
                        )
                        if run is None:
                            raise ApplicationError(
                                ErrorCode.INTERNAL_ERROR, "incident.lookup_failed"
                            )
                        if run.request_sha256 != request_hash:
                            pending_error = ApplicationError(
                                ErrorCode.CONFLICT, "incident.correlation_conflict"
                            )
                        elif run.status == RunStatus.SUCCEEDED.value:
                            event_type = "incident.replayed"
                        else:
                            pending_error = ApplicationError(
                                ErrorCode.CONFLICT, "incident.already_in_progress"
                            )

                    if pending_error is None:
                        self._add_audit(
                            session,
                            organization_id=actor.organization_id,
                            environment_id=actor.environment_id,
                            actor_id=actor.subject_id,
                            correlation_id=correlation_id,
                            run_id=run.id,
                            event_type=event_type,
                            outcome=AuditOutcome.ACCEPTED,
                            details={
                                "target_kind": INCIDENT_TARGET_KIND,
                                "logical_target_id": request.target_id,
                            },
                            occurred_at=now,
                        )
                        record = self._run_record(run)
                    else:
                        self._add_audit(
                            session,
                            organization_id=actor.organization_id,
                            environment_id=actor.environment_id,
                            actor_id=actor.subject_id,
                            correlation_id=correlation_id,
                            run_id=run.id,
                            event_type="incident.replay.denied",
                            outcome=AuditOutcome.DENIED,
                            details={"reason": pending_error.message_key},
                            occurred_at=now,
                        )
                session.flush()
        except ApplicationError:
            raise
        except SQLAlchemyError as exc:
            raise self._database_error() from exc

        if pending_error is not None:
            raise pending_error
        if record is None:
            raise ApplicationError(ErrorCode.INTERNAL_ERROR, "incident.record_missing")
        return record

    def complete_incident_investigation(
        self,
        actor: ActorContext,
        run_id: UUID,
        assistant: AssistantResponse,
        evidence: IncidentEvidence,
    ) -> LiveIncidentResult:
        """Persist the exact composite evidence, answer, hash, and completion audit."""

        evidence_payload = evidence.model_dump(mode="json")
        evidence_sha256 = self._json_hash(evidence_payload)
        evidence_reference = f"run-evidence:{run_id}"
        now = self._now()

        try:
            with self._session_factory() as session, session.begin():
                run = session.scalar(
                    select(Run)
                    .where(
                        Run.id == run_id,
                        Run.organization_id == actor.organization_id,
                        Run.environment_id == actor.environment_id,
                        Run.actor_id == actor.subject_id,
                        Run.action == INCIDENT_INVESTIGATION_ACTION,
                    )
                    .with_for_update()
                )
                if run is None:
                    raise ApplicationError(ErrorCode.NOT_FOUND, "incident.not_found")
                if run.status != RunStatus.RUNNING.value:
                    raise ApplicationError(ErrorCode.CONFLICT, "incident.not_running")
                if assistant.correlation_id != run.correlation_id or assistant.locale != run.locale:
                    raise ApplicationError(
                        ErrorCode.DEPENDENCY_UNAVAILABLE,
                        "incident.result_identity_mismatch",
                    )
                if evidence.target_id != run.parameters.get("target_id"):
                    raise ApplicationError(
                        ErrorCode.DEPENDENCY_UNAVAILABLE,
                        "incident.evidence_target_mismatch",
                    )

                audit_event_id = uuid4()
                result = LiveIncidentResult(
                    run_id=run.id,
                    status=RunStatus.SUCCEEDED,
                    locale=run.locale,
                    assistant=assistant,
                    evidence=evidence,
                    evidence_reference=evidence_reference,
                    evidence_sha256=evidence_sha256,
                    organization_id=run.organization_id,
                    environment_id=run.environment_id,
                    target_id=run.target_id,
                    is_partial=evidence.is_partial,
                    is_stale=any(metric.stale for metric in evidence.zabbix.summary.metrics),
                    audit_event_id=audit_event_id,
                )
                run.result = result.model_dump(mode="json")
                run.error = None
                run.status = RunStatus.SUCCEEDED.value
                run.updated_at = now
                self._add_audit(
                    session,
                    event_id=audit_event_id,
                    organization_id=run.organization_id,
                    environment_id=run.environment_id,
                    actor_id=run.actor_id,
                    correlation_id=run.correlation_id,
                    run_id=run.id,
                    event_type="incident.completed",
                    outcome=AuditOutcome.ACCEPTED,
                    details={
                        "logical_target_id": evidence.target_id,
                        "evidence_reference": evidence_reference,
                        "evidence_sha256": evidence_sha256,
                        "zabbix_source_version": evidence.zabbix.source_version,
                        "zabbix_metric_count": len(evidence.zabbix.summary.metrics),
                        "zabbix_history_count": len(evidence.zabbix.history),
                        "zabbix_event_count": len(evidence.zabbix.events),
                        "linux_collector_version": evidence.linux.collector_version,
                        "linux_service_count": len(evidence.linux.services),
                        "linux_journal_count": len(evidence.linux.journal),
                        "is_partial": result.is_partial,
                        "partial_reasons": list(evidence.partial_reasons),
                        "is_stale": result.is_stale,
                        "model_id": assistant.model_id,
                        "answer_integrity_status": assistant.integrity_status,
                        "answer_limitations": list(assistant.limitations),
                    },
                    occurred_at=now,
                )
                session.flush()
                return result
        except ApplicationError:
            raise
        except SQLAlchemyError as exc:
            raise self._database_error() from exc

    def fail_incident_investigation(
        self,
        actor: ActorContext,
        run_id: UUID,
        error: ApplicationError,
    ) -> None:
        """Persist a safe Phase 2 failure and mandatory audit atomically."""

        now = self._now()
        safe_error = {
            "code": error.code.value,
            "message_key": error.message_key,
            "retryable": error.retryable,
        }
        try:
            with self._session_factory() as session, session.begin():
                run = session.scalar(
                    select(Run)
                    .where(
                        Run.id == run_id,
                        Run.organization_id == actor.organization_id,
                        Run.environment_id == actor.environment_id,
                        Run.actor_id == actor.subject_id,
                        Run.action == INCIDENT_INVESTIGATION_ACTION,
                    )
                    .with_for_update()
                )
                if run is None:
                    raise ApplicationError(ErrorCode.NOT_FOUND, "incident.not_found")
                if run.status != RunStatus.RUNNING.value:
                    raise ApplicationError(ErrorCode.CONFLICT, "incident.not_running")
                run.status = RunStatus.FAILED.value
                run.error = safe_error
                run.updated_at = now
                self._add_audit(
                    session,
                    organization_id=run.organization_id,
                    environment_id=run.environment_id,
                    actor_id=run.actor_id,
                    correlation_id=run.correlation_id,
                    run_id=run.id,
                    event_type="incident.failed",
                    outcome=AuditOutcome.FAILED,
                    details=safe_error,
                    occurred_at=now,
                )
                session.flush()
        except ApplicationError:
            raise
        except SQLAlchemyError as exc:
            raise self._database_error() from exc

    def get_run(self, actor: ActorContext, run_id: UUID) -> RunRecord:
        """Read a run only inside the authenticated actor's server-derived scope."""

        if RUN_READ_SCOPE not in actor.scopes:
            raise ApplicationError(ErrorCode.POLICY_DENIED, "run.read_scope_denied")
        try:
            with self._session_factory() as session:
                run = session.scalar(
                    select(Run).where(
                        Run.id == run_id,
                        Run.organization_id == actor.organization_id,
                        Run.environment_id == actor.environment_id,
                    )
                )
                if run is None:
                    raise ApplicationError(ErrorCode.NOT_FOUND, "run.not_found")
                return self._run_record(run)
        except ApplicationError:
            raise
        except SQLAlchemyError as exc:
            raise self._database_error() from exc

    def claim_lease(self, run_id: UUID, owner_id: str) -> LeaseGrant:
        """Atomically claim an unleased or expired run for one bounded worker."""

        now = self._now()
        expires_at = now + timedelta(seconds=self._settings.lease_ttl_seconds)
        lease_token = issue_opaque_token()
        pending_error: ApplicationError | None = None
        grant: LeaseGrant | None = None

        try:
            with self._session_factory() as session, session.begin():
                run = session.scalar(select(Run).where(Run.id == run_id))
                if run is None:
                    raise ApplicationError(ErrorCode.NOT_FOUND, "run.not_found")
                if run.status in {RunStatus.SUCCEEDED.value, RunStatus.FAILED.value}:
                    raise ApplicationError(ErrorCode.CONFLICT, "run.not_leaseable")

                statement = (
                    insert(RunLease)
                    .values(
                        run_id=run_id,
                        owner_id=owner_id,
                        lease_token_sha256=hash_opaque_token(lease_token),
                        generation=1,
                        acquired_at=now,
                        heartbeat_at=now,
                        expires_at=expires_at,
                    )
                    .on_conflict_do_update(
                        index_elements=[RunLease.run_id],
                        set_={
                            "owner_id": owner_id,
                            "lease_token_sha256": hash_opaque_token(lease_token),
                            "generation": RunLease.generation + 1,
                            "acquired_at": now,
                            "heartbeat_at": now,
                            "expires_at": expires_at,
                        },
                        where=RunLease.expires_at <= now,
                    )
                    .returning(RunLease.generation, RunLease.acquired_at, RunLease.expires_at)
                )
                lease_row = session.execute(statement).one_or_none()
                if lease_row is None:
                    self._add_audit(
                        session,
                        organization_id=run.organization_id,
                        environment_id=run.environment_id,
                        correlation_id=run.correlation_id,
                        run_id=run.id,
                        event_type="run.lease.denied",
                        outcome=AuditOutcome.DENIED,
                        details={"owner_id": owner_id},
                        occurred_at=now,
                    )
                    pending_error = ApplicationError(ErrorCode.CONFLICT, "run.lease_unavailable")
                else:
                    run.status = RunStatus.RUNNING.value
                    run.updated_at = now
                    self._add_audit(
                        session,
                        organization_id=run.organization_id,
                        environment_id=run.environment_id,
                        correlation_id=run.correlation_id,
                        run_id=run.id,
                        event_type="run.lease.claimed",
                        outcome=AuditOutcome.ACCEPTED,
                        details={"owner_id": owner_id, "generation": lease_row.generation},
                        occurred_at=now,
                    )
                    grant = LeaseGrant(
                        run_id=run.id,
                        owner_id=owner_id,
                        lease_token=lease_token,
                        generation=lease_row.generation,
                        acquired_at=lease_row.acquired_at,
                        expires_at=lease_row.expires_at,
                    )
                session.flush()
        except ApplicationError:
            raise
        except SQLAlchemyError as exc:
            raise self._database_error() from exc

        if pending_error is not None:
            raise pending_error
        if grant is None:
            raise ApplicationError(ErrorCode.INTERNAL_ERROR, "run.lease_result_missing")
        return grant

    def renew_lease(self, grant: LeaseGrant) -> LeaseGrant:
        """Extend a live lease only for the holder of its opaque token."""

        now = self._now()
        extended_expiry = func.greatest(RunLease.expires_at, now) + timedelta(
            seconds=self._settings.lease_ttl_seconds
        )
        try:
            with self._session_factory() as session, session.begin():
                statement = (
                    update(RunLease)
                    .where(
                        RunLease.run_id == grant.run_id,
                        RunLease.owner_id == grant.owner_id,
                        RunLease.lease_token_sha256 == hash_opaque_token(grant.lease_token),
                        RunLease.expires_at > now,
                    )
                    .values(heartbeat_at=now, expires_at=extended_expiry)
                    .returning(RunLease.generation, RunLease.acquired_at, RunLease.expires_at)
                )
                row = session.execute(statement).one_or_none()
                if row is None:
                    raise ApplicationError(ErrorCode.CONFLICT, "run.lease_invalid")
                return LeaseGrant(
                    run_id=grant.run_id,
                    owner_id=grant.owner_id,
                    lease_token=grant.lease_token,
                    generation=row.generation,
                    acquired_at=row.acquired_at,
                    expires_at=row.expires_at,
                )
        except ApplicationError:
            raise
        except SQLAlchemyError as exc:
            raise self._database_error() from exc

    def release_lease(self, grant: LeaseGrant) -> None:
        """Release a live lease and return unfinished work to pending."""

        now = self._now()
        try:
            with self._session_factory() as session, session.begin():
                released = session.scalar(
                    delete(RunLease)
                    .where(
                        RunLease.run_id == grant.run_id,
                        RunLease.owner_id == grant.owner_id,
                        RunLease.lease_token_sha256 == hash_opaque_token(grant.lease_token),
                    )
                    .returning(RunLease.run_id)
                )
                if released is None:
                    raise ApplicationError(ErrorCode.CONFLICT, "run.lease_invalid")
                run = session.get(Run, grant.run_id)
                if run is None:
                    raise ApplicationError(ErrorCode.NOT_FOUND, "run.not_found")
                run.status = RunStatus.PENDING.value
                run.updated_at = now
                self._add_audit(
                    session,
                    organization_id=run.organization_id,
                    environment_id=run.environment_id,
                    correlation_id=run.correlation_id,
                    run_id=run.id,
                    event_type="run.lease.released",
                    outcome=AuditOutcome.ACCEPTED,
                    details={"owner_id": grant.owner_id},
                    occurred_at=now,
                )
                session.flush()
        except ApplicationError:
            raise
        except SQLAlchemyError as exc:
            raise self._database_error() from exc

    def complete_fixture(self, grant: LeaseGrant) -> RunRecord:
        """Complete a leased run with deterministic, explicitly non-live fixture data."""

        now = self._now()
        try:
            with self._session_factory() as session, session.begin():
                run = session.scalar(
                    select(Run)
                    .join(RunLease, RunLease.run_id == Run.id)
                    .where(
                        Run.id == grant.run_id,
                        RunLease.owner_id == grant.owner_id,
                        RunLease.lease_token_sha256 == hash_opaque_token(grant.lease_token),
                        RunLease.expires_at > now,
                    )
                )
                if run is None:
                    raise ApplicationError(ErrorCode.CONFLICT, "run.lease_invalid")
                audit_event_id = uuid4()
                result = FixtureResult(
                    run_id=run.id,
                    status=RunStatus.SUCCEEDED,
                    locale=run.locale,
                    answer=self._fixture_answer(run.locale),
                    source=EvidenceSource(
                        connector="fixture",
                        method=FIXTURE_ACTION,
                        collected_at=now,
                        measured_at=now,
                    ),
                    organization_id=run.organization_id,
                    environment_id=run.environment_id,
                    target_id=run.target_id,
                    is_partial=False,
                    is_stale=True,
                    errors=(),
                    audit_event_id=audit_event_id,
                )
                run.result = result.model_dump(mode="json")
                run.status = RunStatus.SUCCEEDED.value
                run.updated_at = now
                session.execute(delete(RunLease).where(RunLease.run_id == run.id))
                self._add_audit(
                    session,
                    event_id=audit_event_id,
                    organization_id=run.organization_id,
                    environment_id=run.environment_id,
                    actor_id=run.actor_id,
                    correlation_id=run.correlation_id,
                    run_id=run.id,
                    event_type="run.fixture.completed",
                    outcome=AuditOutcome.ACCEPTED,
                    details={"source": "fixture", "is_stale": True},
                    occurred_at=now,
                )
                session.flush()
                record = self._run_record(run)
        except ApplicationError:
            raise
        except SQLAlchemyError as exc:
            raise self._database_error() from exc
        return record

    def _actor_from_identity(self, identity: Identity) -> ActorContext:
        return ActorContext(
            subject_id=identity.id,
            organization_id=identity.organization_id,
            environment_id=identity.environment_id,
            roles=frozenset(Role(role) for role in identity.roles),
            scopes=frozenset(identity.scopes),
        )

    def _add_audit(
        self,
        session: Session,
        *,
        organization_id: UUID,
        environment_id: UUID,
        correlation_id: UUID,
        event_type: str,
        outcome: AuditOutcome,
        details: dict[str, Any],
        occurred_at: datetime,
        event_id: UUID | None = None,
        actor_id: UUID | None = None,
        run_id: UUID | None = None,
    ) -> UUID:
        audit_event_id = event_id or uuid4()
        session.add(
            AuditEvent(
                id=audit_event_id,
                organization_id=organization_id,
                environment_id=environment_id,
                actor_id=actor_id,
                run_id=run_id,
                correlation_id=correlation_id,
                event_type=event_type,
                outcome=outcome.value,
                occurred_at=occurred_at,
                details=details,
            )
        )
        return audit_event_id

    @staticmethod
    def _request_hash(request: RunCreateRequest) -> str:
        payload = json.dumps(
            request.model_dump(mode="json"),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )
        return sha256(payload.encode("utf-8")).hexdigest()

    @staticmethod
    def _assistant_request_hash(request: AssistantRequest) -> str:
        return DurableAppService._json_hash(request.model_dump(mode="json"))

    @staticmethod
    def _json_hash(payload: Any) -> str:
        canonical = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )
        return sha256(canonical.encode("utf-8")).hexdigest()

    @staticmethod
    def _run_record(run: Run) -> RunRecord:
        result: FixtureResult | LiveInvestigationResult | LiveIncidentResult | None = None
        if run.result is not None:
            if run.result.get("result_type") == "live_monitoring":
                result = LiveInvestigationResult.model_validate(run.result)
            elif run.result.get("result_type") == "live_incident":
                result = LiveIncidentResult.model_validate(run.result)
            else:
                result = FixtureResult.model_validate(run.result)
        return RunRecord(
            run_id=run.id,
            request_id=run.request_id,
            correlation_id=run.correlation_id,
            status=RunStatus(run.status),
            locale=run.locale,
            created_at=run.created_at,
            updated_at=run.updated_at,
            result=result,
            error=RunFailure.model_validate(run.error) if run.error is not None else None,
        )

    @staticmethod
    def _fixture_answer(locale: str) -> str:
        if locale == "fa":
            return (
                "دادهٔ آزمایشی: دو میزبان پایش‌شده و یک میزبان خارج از دسترس؛ اتصال زنده انجام نشد."
            )
        return "Fixture data: 2 monitored hosts and 1 unavailable; no live connection was made."

    @staticmethod
    def _database_error() -> ApplicationError:
        return ApplicationError(
            ErrorCode.DEPENDENCY_UNAVAILABLE,
            "database.transaction_failed",
            retryable=True,
        )

    @staticmethod
    def _is_bootstrap_conflict(error: IntegrityError) -> bool:
        diagnostic = getattr(error.orig, "diag", None)
        constraint_name = getattr(diagnostic, "constraint_name", None)
        return constraint_name in {"uq_organizations_singleton", "uq_organizations_slug"}

    def _now(self) -> datetime:
        now = self._clock()
        if now.tzinfo is None or now.utcoffset() is None:
            raise ValueError("clock must return a timezone-aware datetime")
        return now
