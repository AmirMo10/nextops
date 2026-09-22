"""Validate pinned, human-readable local-inference candidate metadata."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from yaml.constructor import ConstructorError
from yaml.nodes import MappingNode

EXPECTED_MANIFEST = "qwen3-8b-q4-k-m.yaml"


class ArtifactValidationError(RuntimeError):
    """Raised when candidate metadata is ambiguous or violates its contract."""


class UniqueKeySafeLoader(yaml.SafeLoader):
    """Reject duplicate YAML keys instead of accepting last-value-wins input."""

    def construct_mapping(self, node: MappingNode, deep: bool = False) -> dict[Any, Any]:
        mapping: dict[Any, Any] = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                duplicate = key in mapping
            except TypeError as error:
                raise ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    f"found unhashable key {key!r}",
                    key_node.start_mark,
                ) from error
            if duplicate:
                raise ConstructorError(
                    "while constructing a mapping",
                    node.start_mark,
                    f"found duplicate key {key!r}",
                    key_node.start_mark,
                )
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


def _format_path(parts: Any) -> str:
    rendered = ".".join(str(part) for part in parts)
    return rendered or "<root>"


def validate_repository(repository_root: Path) -> dict[str, Any]:
    """Validate the exact candidate set and its immutable source metadata."""

    directory = repository_root / "deploy" / "inference"
    schema_path = directory / "inference-artifact.schema.json"
    manifests = {path.name for path in directory.glob("*.yaml")}
    if manifests != {EXPECTED_MANIFEST}:
        raise ArtifactValidationError(
            "candidate manifest set mismatch: "
            f"expected={[EXPECTED_MANIFEST]}, actual={sorted(manifests)}"
        )
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        document = yaml.load(
            (directory / EXPECTED_MANIFEST).read_text(encoding="utf-8"),
            Loader=UniqueKeySafeLoader,
        )
    except (OSError, json.JSONDecodeError, yaml.YAMLError) as error:
        raise ArtifactValidationError(f"cannot parse candidate metadata: {error}") from error
    if not isinstance(document, dict):
        raise ArtifactValidationError("candidate manifest must be a mapping")
    errors = sorted(
        Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(document),
        key=lambda error: list(error.path),
    )
    if errors:
        details = "; ".join(f"{_format_path(error.path)}: {error.message}" for error in errors)
        raise ArtifactValidationError(f"candidate schema validation failed: {details}")
    return document


def main() -> int:
    repository_root = Path(__file__).resolve().parents[1]
    try:
        document = validate_repository(repository_root)
    except ArtifactValidationError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(
        "PASS: inference candidate metadata is schema-valid; "
        f"status={document['status']}; runtime_binary_built="
        f"{document['evidence']['runtime_binary_built']}; "
        f"model_imported={document['evidence']['model_imported']}; "
        f"controlled_service_installed="
        f"{document['evidence']['controlled_service_installed']}; "
        f"bilingual_quality_review_passed="
        f"{document['evidence']['bilingual_quality_review_passed']}; "
        f"benchmark_run={document['evidence']['benchmark_run']}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
