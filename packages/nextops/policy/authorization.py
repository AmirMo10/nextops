"""Deny-by-default Stage 1A authorization without operational side effects."""

from collections.abc import Iterable, Mapping
from enum import StrEnum
from types import MappingProxyType
from typing import Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from nextops.contracts.models import (
    ActionName,
    ActorContext,
    InvestigationRequest,
    ScopeName,
    TargetKind,
)
from nextops.domain.types import RiskClass


class FrozenPolicyModel(BaseModel):
    """Strict immutable base for trusted rules and their decisions."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)


class DecisionReason(StrEnum):
    """Stable reasons suitable for audit and localized presentation."""

    ALLOWED = "allowed"
    ORGANIZATION_DENIED = "organization_denied"
    ENVIRONMENT_DENIED = "environment_denied"
    TARGET_DENIED = "target_denied"
    UNKNOWN_ACTION = "unknown_action"
    MUTATION_DISABLED = "mutation_disabled"
    SCOPE_DENIED = "scope_denied"


class PolicyRule(FrozenPolicyModel):
    """Trusted policy metadata for one named action."""

    action: ActionName
    risk_class: RiskClass
    allowed_target_kinds: frozenset[TargetKind] = Field(min_length=1, max_length=64)
    required_scopes: frozenset[ScopeName] = Field(min_length=1, max_length=64)


class PolicyDecision(FrozenPolicyModel):
    """Complete deterministic decision returned for every request."""

    request_id: UUID
    allowed: bool
    reason: DecisionReason
    policy_version: str = Field(min_length=1, max_length=64)
    risk_class: RiskClass | None = None

    @model_validator(mode="after")
    def validate_consistency(self) -> Self:
        """Prevent contradictory decisions from reaching audit or callers."""

        if self.allowed != (self.reason is DecisionReason.ALLOWED):
            raise ValueError("allowed must match the decision reason")
        if self.allowed and self.risk_class is not RiskClass.READ_ONLY:
            raise ValueError("an allowed Stage 1A decision must be READ_ONLY")
        return self


class AuthorizationPolicy:
    """Evaluate an investigation against one explicit local organization scope."""

    def __init__(
        self,
        *,
        organization_id: UUID,
        environment_id: UUID,
        known_target_ids: frozenset[UUID],
        rules: Iterable[PolicyRule],
        version: str,
    ) -> None:
        rule_map: dict[str, PolicyRule] = {}
        for rule in rules:
            if rule.action in rule_map:
                raise ValueError(f"duplicate policy action: {rule.action}")
            rule_map[rule.action] = rule

        if not version:
            raise ValueError("policy version must not be empty")

        self._organization_id = organization_id
        self._environment_id = environment_id
        self._known_target_ids = known_target_ids
        self._rules: Mapping[str, PolicyRule] = MappingProxyType(rule_map)
        self._version = version

    def evaluate(
        self,
        request: InvestigationRequest,
        actor: ActorContext,
    ) -> PolicyDecision:
        """Return a side-effect-free decision; any unmet condition is a denial."""

        if (
            actor.organization_id != self._organization_id
            or request.target.organization_id != self._organization_id
            or actor.organization_id != request.target.organization_id
        ):
            return self._deny(request, DecisionReason.ORGANIZATION_DENIED)

        if (
            actor.environment_id != self._environment_id
            or request.target.environment_id != self._environment_id
            or actor.environment_id != request.target.environment_id
        ):
            return self._deny(request, DecisionReason.ENVIRONMENT_DENIED)

        if request.target.target_id not in self._known_target_ids:
            return self._deny(request, DecisionReason.TARGET_DENIED)

        rule = self._rules.get(request.action)
        if rule is None:
            return self._deny(request, DecisionReason.UNKNOWN_ACTION)

        if rule.risk_class is not RiskClass.READ_ONLY:
            return self._deny(
                request,
                DecisionReason.MUTATION_DISABLED,
                risk_class=rule.risk_class,
            )

        if request.target.kind not in rule.allowed_target_kinds:
            return self._deny(
                request,
                DecisionReason.TARGET_DENIED,
                risk_class=rule.risk_class,
            )

        if not rule.required_scopes.issubset(actor.scopes):
            return self._deny(
                request,
                DecisionReason.SCOPE_DENIED,
                risk_class=rule.risk_class,
            )

        return PolicyDecision(
            request_id=request.request_id,
            allowed=True,
            reason=DecisionReason.ALLOWED,
            policy_version=self._version,
            risk_class=rule.risk_class,
        )

    def _deny(
        self,
        request: InvestigationRequest,
        reason: DecisionReason,
        *,
        risk_class: RiskClass | None = None,
    ) -> PolicyDecision:
        return PolicyDecision(
            request_id=request.request_id,
            allowed=False,
            reason=reason,
            policy_version=self._version,
            risk_class=risk_class,
        )
