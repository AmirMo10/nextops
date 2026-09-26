#!/usr/bin/env python3
"""Validate the public, non-secret NextOps release/status manifest."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/status/current-release.yaml"
SCHEMA = ROOT / "docs/status/release-status.schema.json"
INFERENCE_MANIFEST = ROOT / "deploy/inference/qwen3-8b-q4-k-m.yaml"
RECOVERY_VALIDATOR = ROOT / "scripts/check_recovery_profile.py"
REQUIRED_CURRENT_APP_GATES = frozenset(
    {
        "current_app_bounded_live_functionality",
        "current_app_held_out_answer_semantics",
        "current_app_exact_release_rollback",
        "current_app_server_side_wan_isolation",
        "current_app_vm_reboot_cold_start",
    }
)


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain one mapping")
    return data


def current_application_errors(status: dict[str, Any]) -> list[str]:
    """Keep revision-sensitive results bound to the actually deployed application."""

    candidate = status.get("current_application_qualification")
    components = status.get("components")
    if not isinstance(candidate, dict) or not isinstance(components, dict):
        return ["current application qualification or components are missing"]
    application = components.get("application")
    if not isinstance(application, dict):
        return ["application component is missing"]

    errors: list[str] = []
    for field in ("release", "source_commit"):
        if candidate.get(field) != application.get(field):
            errors.append(f"current application qualification {field} differs from application")

    gates = candidate.get("gates")
    if not isinstance(gates, list):
        return [*errors, "current application qualification gates are missing"]
    ids = [str(gate.get("id")) for gate in gates if isinstance(gate, dict)]
    if len(ids) != len(set(ids)):
        errors.append("current application qualification gate IDs must be unique")
    if set(ids) != REQUIRED_CURRENT_APP_GATES:
        errors.append("current application qualification has missing or unexpected gate IDs")
    return errors


def recovery_profile_qualified() -> bool:
    """Require the existing independent recovery validator to pass without Internet."""

    try:
        result = subprocess.run(
            [sys.executable, str(RECOVERY_VALIDATOR), "--require-qualified"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return result.returncode == 0


def production_claim_errors(status: dict[str, Any], recovery_qualified: bool) -> list[str]:
    """Reject contradictory production claims; evidence review remains a separate gate."""

    gates = status.get("acceptance_gates")
    if not isinstance(gates, list):
        return ["production acceptance gates are missing"]
    gate_status = {
        str(gate.get("id")): gate.get("status") for gate in gates if isinstance(gate, dict)
    }
    if "production_acceptance" not in gate_status:
        return ["production_acceptance gate is missing"]

    deployment_status = status.get("deployment_status")
    production_passed = gate_status["production_acceptance"] == "passed"
    if not production_passed and deployment_status != "production_accepted":
        return []

    errors: list[str] = []
    if not production_passed or deployment_status != "production_accepted":
        errors.append("deployment status and production_acceptance gate must agree")

    candidate = status.get("current_application_qualification")
    candidate_gates = candidate.get("gates") if isinstance(candidate, dict) else None
    if (
        not isinstance(candidate_gates, list)
        or not candidate_gates
        or any(
            not isinstance(gate, dict) or gate.get("status") != "passed" for gate in candidate_gates
        )
    ):
        errors.append("production acceptance requires every current-app gate to pass")

    if any(
        state != "passed"
        for gate_id, state in gate_status.items()
        if gate_id != "production_acceptance"
    ):
        errors.append("production acceptance requires every release gate to pass")

    if not recovery_qualified:
        errors.append(
            "production acceptance requires a qualified recovery profile and restore gates"
        )
    return errors


def main() -> int:
    errors: list[str] = []
    status = _load_yaml(MANIFEST)
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors.extend(error.message for error in sorted(validator.iter_errors(status), key=str))
    errors.extend(current_application_errors(status))
    errors.extend(production_claim_errors(status, recovery_profile_qualified()))

    ids: list[str] = []
    candidate = status.get("current_application_qualification")
    candidate_gates = candidate.get("gates", []) if isinstance(candidate, dict) else []
    for entries in (
        status.get("capabilities", []),
        status.get("acceptance_gates", []),
        candidate_gates,
    ):
        if isinstance(entries, list):
            ids.extend(str(entry.get("id")) for entry in entries if isinstance(entry, dict))
            for entry in entries:
                if not isinstance(entry, dict):
                    continue
                for evidence in entry.get("evidence", []):
                    if not (ROOT / evidence).is_file():
                        errors.append(f"missing evidence path: {evidence}")
    if len(ids) != len(set(ids)):
        errors.append("capability and acceptance-gate IDs must be globally unique")

    inference = _load_yaml(INFERENCE_MANIFEST)
    components = status.get("components", {})
    if isinstance(components, dict):
        runtime = components.get("inference_runtime", {})
        model = components.get("model", {})
        if runtime.get("source_commit") != inference.get("runtime", {}).get("source_commit"):
            errors.append("runtime source commit differs from the inference artifact manifest")
        if runtime.get("binary_sha256") != inference.get("runtime", {}).get("binary_sha256"):
            errors.append("runtime SHA-256 differs from the inference artifact manifest")
        if model.get("sha256") != inference.get("model", {}).get("sha256"):
            errors.append("model SHA-256 differs from the inference artifact manifest")

    if errors:
        print("Release status validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "PASS: release status schema, evidence paths, unique IDs, and AI artifact identity match."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
