#!/usr/bin/env python3
"""Validate the public, non-secret recovery profile and qualification gates."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from yaml.constructor import ConstructorError
from yaml.nodes import MappingNode

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROFILE = ROOT / "deploy" / "recovery" / "recovery-profile.yaml"
SCHEMA = ROOT / "deploy" / "recovery" / "recovery-profile.schema.json"

EXPECTED_DATABASES = {
    "application": {
        "service_unit": "postgresql@16-nextops.service",
        "data_directory": "/var/lib/postgresql/16/nextops",
    },
    "zabbix": {
        "service_unit": "postgresql@16-zabbix.service",
        "data_directory": "/var/lib/postgresql/16/zabbix",
    },
}
REQUIRED_FILE_EXCLUSIONS = {
    "database_data_directories",
    "live_database_snapshots",
    "postgresql_wal",
}
SENSITIVE_KEY = re.compile(
    r"(^|_)(password|secret|token|credential|private_key|encryption_key)($|_)", re.IGNORECASE
)


class RecoveryProfileError(RuntimeError):
    """Raised when the public recovery contract is invalid or overclaims readiness."""


class UniqueKeySafeLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects duplicate mapping keys."""

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
    """Sanitized recovery qualification state."""

    profile_id: str
    qualified: bool
    blocker_count: int
    database_repository_count: int


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        document = yaml.load(path.read_text(encoding="utf-8"), Loader=UniqueKeySafeLoader)
    except (OSError, yaml.YAMLError) as error:
        raise RecoveryProfileError(f"cannot parse profile: {error}") from error
    if not isinstance(document, dict):
        raise RecoveryProfileError("profile top-level YAML value must be a mapping")
    return document


def _format_error_path(parts: Any) -> str:
    rendered = ".".join(str(part) for part in parts)
    return rendered or "<root>"


def _walk_public_values(value: Any, path: tuple[str, ...] = ()) -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for raw_key, child in value.items():
            key = str(raw_key)
            child_path = (*path, key)
            if SENSITIVE_KEY.search(key):
                errors.append(f"secret-like field is forbidden: {'.'.join(child_path)}")
            errors.extend(_walk_public_values(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(_walk_public_values(child, (*path, str(index))))
    elif isinstance(value, str):
        parsed = urlsplit(value)
        if parsed.scheme and (parsed.username is not None or parsed.password is not None):
            errors.append(f"URL user information is forbidden: {'.'.join(path)}")
    return errors


def validate_profile(profile_path: Path = DEFAULT_PROFILE) -> ValidationSummary:
    """Validate schema, topology invariants, secret hygiene, and readiness claims."""

    profile = _load_yaml(profile_path)
    try:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    except (OSError, json.JSONDecodeError) as error:
        raise RecoveryProfileError(f"cannot load recovery schema: {error}") from error

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    schema_errors = sorted(validator.iter_errors(profile), key=lambda error: list(error.path))
    errors = [f"{_format_error_path(error.path)}: {error.message}" for error in schema_errors]
    errors.extend(_walk_public_values(profile))

    databases = profile.get("databases", {})
    repository_ids: list[str] = []
    if isinstance(databases, dict):
        for name, expected in EXPECTED_DATABASES.items():
            database = databases.get(name, {})
            if not isinstance(database, dict):
                continue
            repository_ids.append(str(database.get("repository_id", "")))
            for field, expected_value in expected.items():
                if database.get(field) != expected_value:
                    errors.append(
                        f"databases.{name}.{field} must be {expected_value!r} "
                        "for the deployed cluster"
                    )
        if len(repository_ids) == 2 and len(set(repository_ids)) != 2:
            errors.append("application and Zabbix databases require separate repository IDs")

    file_backup = profile.get("file_backup", {})
    if isinstance(file_backup, dict):
        included = {str(item) for item in file_backup.get("included_classes", [])}
        forbidden = {str(item) for item in file_backup.get("forbidden_classes", [])}
        database_classes = REQUIRED_FILE_EXCLUSIONS & included
        if database_classes:
            errors.append(
                "restic included_classes must not contain PostgreSQL data/WAL classes: "
                + ", ".join(sorted(database_classes))
            )
        missing_exclusions = REQUIRED_FILE_EXCLUSIONS - forbidden
        if missing_exclusions:
            errors.append(
                "restic forbidden_classes is missing: " + ", ".join(sorted(missing_exclusions))
            )

    qualification = profile.get("qualification", {})
    qualified = bool(qualification.get("qualified")) if isinstance(qualification, dict) else False
    blockers = qualification.get("blockers", []) if isinstance(qualification, dict) else []
    status = qualification.get("status") if isinstance(qualification, dict) else None
    if qualified:
        if status != "qualified":
            errors.append("a qualified profile must use qualification.status=qualified")
        if blockers:
            errors.append("a qualified profile cannot retain blockers")

        destination = profile.get("destination", {})
        destination_ready = isinstance(destination, dict) and all(
            destination.get(field) is True
            for field in (
                "approved",
                "independent_from_serving_guest",
                "independent_from_serving_datastore",
                "independent_from_serving_hypervisor",
            )
        )
        if not destination_ready or not destination.get("identifier"):
            errors.append("qualified recovery requires an approved independent destination")

        objectives = profile.get("objectives", {})
        if not isinstance(objectives, dict) or any(
            objectives.get(field) is None for field in ("rpo_minutes", "rto_minutes")
        ):
            errors.append("qualified recovery requires approved RPO and RTO")

        retention = profile.get("retention", {})
        if not isinstance(retention, dict) or any(value is None for value in retention.values()):
            errors.append("qualified recovery requires a complete retention policy")

        tools = profile.get("tools", {})
        if not isinstance(tools, dict) or any(
            not isinstance(tool, dict)
            or tool.get("offline_bundle_verified") is not True
            or not tool.get("artifact_sha256")
            for tool in tools.values()
        ):
            errors.append("qualified recovery requires checksummed, verified offline tool bundles")

        gates = profile.get("acceptance_gates", {})
        if (
            not isinstance(gates, dict)
            or not gates
            or any(value is not True for value in gates.values())
        ):
            errors.append("qualified recovery requires every acceptance gate to pass")

        key_custody = profile.get("key_custody", {})
        if not isinstance(key_custody, dict) or key_custody.get("recovery_tested") is not True:
            errors.append("qualified recovery requires a passed key-recovery test")
    else:
        if status != "blocked":
            errors.append("an unqualified profile must use qualification.status=blocked")
        if not blockers:
            errors.append("an unqualified profile must identify at least one blocker")

    if errors:
        raise RecoveryProfileError("; ".join(errors))

    return ValidationSummary(
        profile_id=str(profile["profile_id"]),
        qualified=qualified,
        blocker_count=len(blockers),
        database_repository_count=len(set(repository_ids)),
    )


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    parser.add_argument(
        "--require-qualified",
        action="store_true",
        help="fail unless every production recovery gate is explicitly satisfied",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        summary = validate_profile(args.profile)
    except RecoveryProfileError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1

    state = "QUALIFIED" if summary.qualified else "BLOCKED"
    print(
        f"VALID: profile={summary.profile_id}; qualification={state}; "
        f"database_repositories={summary.database_repository_count}; "
        f"blockers={summary.blocker_count}."
    )
    if args.require_qualified and not summary.qualified:
        print("FAIL: production recovery qualification is still blocked.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
