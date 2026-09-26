"""Release/status manifest invariants."""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Any
from unittest.mock import patch

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]


def _status_module() -> ModuleType:
    path = ROOT / "scripts" / "check_release_status.py"
    spec = importlib.util.spec_from_file_location("check_release_status", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _manifest() -> dict[str, Any]:
    result = yaml.safe_load((ROOT / "docs/status/current-release.yaml").read_text(encoding="utf-8"))
    assert isinstance(result, dict)
    return result


def test_release_status_manifest_is_valid_and_matches_ai_artifacts() -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/check_release_status.py")],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "PASS:" in result.stdout


def test_current_app_qualification_is_bound_to_serving_release() -> None:
    module = _status_module()
    status = _manifest()
    assert module.current_application_errors(status) == []

    mismatched_release = copy.deepcopy(status)
    mismatched_release["current_application_qualification"]["release"] = "nextops-0.1.0-deadbee"
    assert any(
        "release differs" in error
        for error in module.current_application_errors(mismatched_release)
    )

    mismatched_commit = copy.deepcopy(status)
    mismatched_commit["current_application_qualification"]["source_commit"] = "deadbee"
    assert any(
        "source_commit differs" in error
        for error in module.current_application_errors(mismatched_commit)
    )


def test_current_app_qualification_requires_all_revision_sensitive_gates() -> None:
    module = _status_module()
    status = _manifest()
    status["current_application_qualification"]["gates"].pop()

    assert any(
        "missing or unexpected" in error for error in module.current_application_errors(status)
    )

    duplicate = _manifest()
    gates = duplicate["current_application_qualification"]["gates"]
    gates[-1] = copy.deepcopy(gates[0])
    assert any("must be unique" in error for error in module.current_application_errors(duplicate))


def test_schema_rejects_missing_or_invalid_candidate_qualification() -> None:
    schema = json.loads(
        (ROOT / "docs/status/release-status.schema.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema)
    status = _manifest()
    assert not list(validator.iter_errors(status))

    missing_candidate = copy.deepcopy(status)
    missing_candidate.pop("current_application_qualification")
    assert list(validator.iter_errors(missing_candidate))

    invalid_status = copy.deepcopy(status)
    invalid_status["current_application_qualification"]["gates"][0]["status"] = "assumed"
    assert list(validator.iter_errors(invalid_status))


def test_production_claim_rejects_blocked_recovery_and_current_release_gates() -> None:
    module = _status_module()
    status = _manifest()
    assert module.recovery_profile_qualified() is False
    assert module.production_claim_errors(status, False) == []

    for gate in status["acceptance_gates"]:
        if gate["id"] == "production_acceptance":
            gate["status"] = "passed"
    errors = module.production_claim_errors(status, False)
    assert any("deployment status" in error for error in errors)
    assert any("current-app gate" in error for error in errors)
    assert any("release gate" in error for error in errors)
    assert any("qualified recovery" in error for error in errors)


def test_unavailable_recovery_validator_fails_closed() -> None:
    module = _status_module()
    with patch.object(module.subprocess, "run", side_effect=OSError("unavailable")):
        assert module.recovery_profile_qualified() is False
    with patch.object(
        module.subprocess,
        "run",
        side_effect=subprocess.TimeoutExpired("check_recovery_profile.py", 30),
    ):
        assert module.recovery_profile_qualified() is False


def test_production_claim_requires_all_gates_even_with_asserted_recovery() -> None:
    module = _status_module()
    status = _manifest()
    status["deployment_status"] = "production_accepted"
    for gate in status["acceptance_gates"]:
        gate["status"] = "passed"

    errors = module.production_claim_errors(status, False)
    assert any("current-app gate" in error for error in errors)
    assert any("qualified recovery" in error for error in errors)

    assert any(
        "current-app gate" in error for error in module.production_claim_errors(status, True)
    )
    assert not any(
        "qualified recovery" in error for error in module.production_claim_errors(status, True)
    )

    for gate in status["current_application_qualification"]["gates"]:
        gate["status"] = "passed"
    # This in-memory predicate fixture does not call or bypass the real recovery validator.
    assert module.production_claim_errors(status, True) == []


def test_production_acceptance_gate_cannot_be_omitted() -> None:
    module = _status_module()
    status = _manifest()
    status["acceptance_gates"] = [
        gate for gate in status["acceptance_gates"] if gate["id"] != "production_acceptance"
    ]

    assert module.production_claim_errors(status, False) == [
        "production_acceptance gate is missing"
    ]
