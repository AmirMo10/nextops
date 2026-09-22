#!/usr/bin/env python3
"""Validate the public, non-secret NextOps release/status manifest."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/status/current-release.yaml"
SCHEMA = ROOT / "docs/status/release-status.schema.json"
INFERENCE_MANIFEST = ROOT / "deploy/inference/qwen3-8b-q4-k-m.yaml"


def _load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain one mapping")
    return data


def main() -> int:
    errors: list[str] = []
    status = _load_yaml(MANIFEST)
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors.extend(error.message for error in sorted(validator.iter_errors(status), key=str))

    ids: list[str] = []
    for section in ("capabilities", "acceptance_gates"):
        entries = status.get(section, [])
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
