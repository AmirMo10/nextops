"""Validate the human-readable server deployment dossiers."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from yaml.constructor import ConstructorError
from yaml.nodes import MappingNode

EXPECTED_DOSSIERS = {
    "nextops-ai.yaml",
    "nextops-app.yaml",
    "nextops-connectors-ro.yaml",
    "zabbix-server.yaml",
}
EXPECTED_SERVER_IDS = {
    "nextops-ai",
    "nextops-app",
    "nextops-connectors-ro",
    "zabbix-server",
}
EXPECTED_TOTALS = (40, 184, 980)


class DossierValidationError(RuntimeError):
    """Raised when the public deployment dossier contract is invalid."""


class UniqueKeySafeLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects ambiguous duplicate mapping keys."""

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


@dataclass(frozen=True)
class ValidationSummary:
    """Cross-file values reported after successful validation."""

    dossier_count: int
    total_vcpu: int
    total_ram_gib: int
    total_disk_gib: int


def _load_yaml_mapping(path: Path) -> dict[str, Any]:
    try:
        document = yaml.load(
            path.read_text(encoding="utf-8"),
            Loader=UniqueKeySafeLoader,
        )
    except (OSError, yaml.YAMLError) as error:
        raise DossierValidationError(f"{path.name}: cannot parse YAML: {error}") from error

    if not isinstance(document, dict):
        raise DossierValidationError(f"{path.name}: top-level YAML value must be a mapping")
    return document


def _format_error_path(parts: Any) -> str:
    rendered = ".".join(str(part) for part in parts)
    return rendered or "<root>"


def validate_repository(repository_root: Path) -> ValidationSummary:
    """Validate filenames, schema conformance, server identity, and resource totals."""

    dossier_directory = repository_root / "deploy" / "server-dependencies"
    schema_path = dossier_directory / "server-dependency.schema.json"

    actual_dossiers = {path.name for path in dossier_directory.glob("*.yaml")}
    if actual_dossiers != EXPECTED_DOSSIERS:
        missing = sorted(EXPECTED_DOSSIERS - actual_dossiers)
        unexpected = sorted(actual_dossiers - EXPECTED_DOSSIERS)
        raise DossierValidationError(
            f"YAML dossier set mismatch; missing={missing}, unexpected={unexpected}"
        )

    legacy_json = sorted(
        path.name for path in dossier_directory.glob("*.json") if path.name != schema_path.name
    )
    if legacy_json:
        raise DossierValidationError(f"legacy JSON dossiers remain: {legacy_json}")

    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    except (OSError, json.JSONDecodeError) as error:
        raise DossierValidationError(f"cannot load shared JSON Schema: {error}") from error

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    documents: list[dict[str, Any]] = []
    for dossier_name in sorted(EXPECTED_DOSSIERS):
        document = _load_yaml_mapping(dossier_directory / dossier_name)
        errors = sorted(validator.iter_errors(document), key=lambda error: list(error.path))
        if errors:
            details = "; ".join(
                f"{_format_error_path(error.path)}: {error.message}" for error in errors
            )
            raise DossierValidationError(f"{dossier_name}: schema validation failed: {details}")
        documents.append(document)

    server_ids = {str(document["server_id"]) for document in documents}
    if server_ids != EXPECTED_SERVER_IDS:
        raise DossierValidationError(
            f"server IDs do not match the approved set: {sorted(server_ids)}"
        )

    total_vcpu = sum(int(document["vm"]["vcpu"]) for document in documents)
    total_ram_gib = sum(int(document["vm"]["ram_gib"]) for document in documents)
    total_disk_gib = sum(int(document["vm"]["disk_gib"]) for document in documents)
    actual_totals = (total_vcpu, total_ram_gib, total_disk_gib)
    if actual_totals != EXPECTED_TOTALS:
        raise DossierValidationError(
            "resource totals differ from the accepted initial profile: "
            f"expected={EXPECTED_TOTALS}, actual={actual_totals}"
        )

    return ValidationSummary(
        dossier_count=len(documents),
        total_vcpu=total_vcpu,
        total_ram_gib=total_ram_gib,
        total_disk_gib=total_disk_gib,
    )


def main() -> int:
    repository_root = Path(__file__).resolve().parents[1]
    try:
        summary = validate_repository(repository_root)
    except DossierValidationError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print(
        f"PASS: {summary.dossier_count} YAML dossiers match schema 1.0.0; "
        f"{summary.total_vcpu} vCPU / {summary.total_ram_gib} GiB RAM / "
        f"{summary.total_disk_gib} GiB disk."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
