from datetime import UTC, datetime
from uuid import UUID

import pytest
from pydantic import ValidationError

from nextops.contracts.models import (
    ActorContext,
    EvidenceMetadata,
    InvestigationRequest,
    Role,
    TargetReference,
)
from nextops.domain.types import RiskClass
from nextops.policy.authorization import (
    AuthorizationPolicy,
    DecisionReason,
    PolicyDecision,
    PolicyRule,
)

ORG_ID = UUID("4c349f62-9f1e-4dd0-a2d0-9c8439772c18")
OTHER_ORG_ID = UUID("66ad09ce-665c-4054-a015-ab8066450710")
ENV_ID = UUID("1ac2b33c-084b-4aa2-9c51-9718b32da241")
OTHER_ENV_ID = UUID("6cc29f65-b929-4326-9104-4f8dbf745850")
TARGET_ID = UUID("4453f2b1-48d7-45ae-bd2e-cc88ce714204")
OTHER_TARGET_ID = UUID("1df08e5c-7f55-4bc9-9356-e86828a29d50")
USER_ID = UUID("ef848042-b144-499f-9e42-22616508b368")


def actor(
    *,
    organization_id: UUID = ORG_ID,
    environment_id: UUID = ENV_ID,
    scopes: frozenset[str] = frozenset({"zabbix.status.read"}),
) -> ActorContext:
    return ActorContext(
        subject_id=USER_ID,
        organization_id=organization_id,
        environment_id=environment_id,
        roles=frozenset({Role.ADMIN}),
        scopes=scopes,
    )


def target(
    *,
    target_id: UUID = TARGET_ID,
    organization_id: UUID = ORG_ID,
    environment_id: UUID = ENV_ID,
    kind: str = "zabbix_server",
) -> TargetReference:
    return TargetReference(
        target_id=target_id,
        organization_id=organization_id,
        environment_id=environment_id,
        kind=kind,
    )


def request(
    *,
    action: str = "zabbix.status.read",
    request_target: TargetReference | None = None,
    parameters: dict[str, object] | None = None,
) -> InvestigationRequest:
    return InvestigationRequest(
        request_id=UUID("8e3be1cb-7589-4707-9883-854a4eb1a2c6"),
        correlation_id=UUID("e662b3aa-71b8-4130-be55-38e88c2506d6"),
        idempotency_key="investigation-2026-09-21-0001",
        target=request_target or target(),
        action=action,
        question="What is the authorized Zabbix status?",
        locale="en",
        parameters=parameters or {},
    )


@pytest.fixture
def policy() -> AuthorizationPolicy:
    return AuthorizationPolicy(
        organization_id=ORG_ID,
        environment_id=ENV_ID,
        known_target_ids=frozenset({TARGET_ID}),
        rules=(
            PolicyRule(
                action="zabbix.status.read",
                risk_class=RiskClass.READ_ONLY,
                allowed_target_kinds=frozenset({"zabbix_server"}),
                required_scopes=frozenset({"zabbix.status.read"}),
            ),
            PolicyRule(
                action="zabbix.host.disable",
                risk_class=RiskClass.HIGH_RISK,
                allowed_target_kinds=frozenset({"zabbix_server"}),
                required_scopes=frozenset({"zabbix.host.write"}),
            ),
        ),
        version="stage-1a.v1",
    )


def test_named_read_only_action_with_exact_scope_is_allowed(
    policy: AuthorizationPolicy,
) -> None:
    decision = policy.evaluate(request(), actor())

    assert decision.allowed is True
    assert decision.reason is DecisionReason.ALLOWED
    assert decision.policy_version == "stage-1a.v1"
    assert decision.risk_class is RiskClass.READ_ONLY


@pytest.mark.parametrize(
    ("authenticated_actor", "candidate", "reason"),
    [
        (
            actor(),
            request(action="zabbix.unknown.read"),
            DecisionReason.UNKNOWN_ACTION,
        ),
        (
            actor(organization_id=OTHER_ORG_ID),
            request(),
            DecisionReason.ORGANIZATION_DENIED,
        ),
        (
            actor(),
            request(request_target=target(organization_id=OTHER_ORG_ID)),
            DecisionReason.ORGANIZATION_DENIED,
        ),
        (
            actor(environment_id=OTHER_ENV_ID),
            request(),
            DecisionReason.ENVIRONMENT_DENIED,
        ),
        (
            actor(),
            request(request_target=target(environment_id=OTHER_ENV_ID)),
            DecisionReason.ENVIRONMENT_DENIED,
        ),
        (
            actor(),
            request(request_target=target(target_id=OTHER_TARGET_ID)),
            DecisionReason.TARGET_DENIED,
        ),
        (
            actor(scopes=frozenset()),
            request(),
            DecisionReason.SCOPE_DENIED,
        ),
    ],
)
def test_unknown_or_out_of_scope_requests_are_denied(
    policy: AuthorizationPolicy,
    authenticated_actor: ActorContext,
    candidate: InvestigationRequest,
    reason: DecisionReason,
) -> None:
    decision = policy.evaluate(candidate, authenticated_actor)

    assert decision.allowed is False
    assert decision.reason is reason


@pytest.mark.parametrize(
    "risk_class",
    [
        RiskClass.LOW_RISK,
        RiskClass.MEDIUM_RISK,
        RiskClass.HIGH_RISK,
        RiskClass.CRITICAL,
    ],
)
def test_every_mutation_risk_class_is_denied_even_for_admin(
    risk_class: RiskClass,
) -> None:
    mutation_policy = AuthorizationPolicy(
        organization_id=ORG_ID,
        environment_id=ENV_ID,
        known_target_ids=frozenset({TARGET_ID}),
        rules=(
            PolicyRule(
                action="zabbix.host.disable",
                risk_class=risk_class,
                allowed_target_kinds=frozenset({"zabbix_server"}),
                required_scopes=frozenset({"zabbix.host.write"}),
            ),
        ),
        version="stage-1a.v1",
    )

    decision = mutation_policy.evaluate(
        request(
            action="zabbix.host.disable",
            parameters={"risk_class": "READ_ONLY", "approved": True},
        ),
        actor(scopes=frozenset({"zabbix.host.write"})),
    )

    assert decision.allowed is False
    assert decision.reason is DecisionReason.MUTATION_DISABLED
    assert decision.risk_class is risk_class


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("risk_class", "READ_ONLY"),
        ("actor", actor().model_dump(mode="json")),
    ],
)
def test_request_cannot_supply_trusted_policy_fields(field: str, value: object) -> None:
    payload = request().model_dump()
    payload[field] = value

    with pytest.raises(ValidationError):
        InvestigationRequest.model_validate(payload)


def test_actor_scope_names_are_canonical() -> None:
    with pytest.raises(ValidationError):
        actor(scopes=frozenset({"*"}))


def test_policy_decision_rejects_inconsistent_allowed_state() -> None:
    with pytest.raises(ValidationError):
        PolicyDecision(
            request_id=UUID("8e3be1cb-7589-4707-9883-854a4eb1a2c6"),
            allowed=True,
            reason=DecisionReason.SCOPE_DENIED,
            policy_version="stage-1a.v1",
            risk_class=RiskClass.READ_ONLY,
        )


def test_target_is_immutable() -> None:
    immutable_target = target()

    with pytest.raises(ValidationError):
        immutable_target.kind = "linux_host"  # type: ignore[misc]


def test_evidence_requires_aware_times_and_source_metadata() -> None:
    evidence = EvidenceMetadata(
        evidence_id=UUID("1d98d392-9dce-4284-bd85-f7267290e211"),
        request_id=UUID("8e3be1cb-7589-4707-9883-854a4eb1a2c6"),
        organization_id=ORG_ID,
        environment_id=ENV_ID,
        target_id=TARGET_ID,
        source_connector="zabbix",
        source_method="host.get",
        source_object_ids=("10105",),
        collected_at=datetime(2026, 9, 21, 8, 30, tzinfo=UTC),
        measured_at=datetime(2026, 9, 21, 8, 29, tzinfo=UTC),
        is_partial=False,
        is_truncated=False,
        is_stale=False,
        content_sha256="2c26b46b68ffc68ff99b453c1d30413413422d706483bfa0f98a5e886266e7ae",
        storage_reference="evidence://stage-1a/1d98d392",
    )

    assert evidence.collected_at.tzinfo is UTC
    assert evidence.source_method == "host.get"

    with pytest.raises(ValidationError):
        EvidenceMetadata.model_validate(
            {
                **evidence.model_dump(),
                "collected_at": datetime(2026, 9, 21, 8, 30),
            }
        )
