from __future__ import annotations

import copy
import importlib.util
import sys
from pathlib import Path

import pytest
import yaml

SCRIPT_PATH = Path(__file__).resolve().parents[2] / "scripts" / "check_recovery_profile.py"
SPEC = importlib.util.spec_from_file_location("nextops_check_recovery_profile", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
CHECK_RECOVERY = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CHECK_RECOVERY
SPEC.loader.exec_module(CHECK_RECOVERY)

DEFAULT_PROFILE = CHECK_RECOVERY.DEFAULT_PROFILE
RecoveryProfileError = CHECK_RECOVERY.RecoveryProfileError
_load_yaml = CHECK_RECOVERY._load_yaml
main = CHECK_RECOVERY.main
validate_profile = CHECK_RECOVERY.validate_profile


def _profile() -> dict[str, object]:
    return copy.deepcopy(_load_yaml(DEFAULT_PROFILE))


def _write_profile(tmp_path: Path, profile: dict[str, object]) -> Path:
    path = tmp_path / "recovery-profile.yaml"
    path.write_text(yaml.safe_dump(profile, sort_keys=False), encoding="utf-8")
    return path


def test_repository_profile_is_valid_and_intentionally_blocked() -> None:
    summary = validate_profile()

    assert summary.profile_id == "nextops-independent-recovery-v1"
    assert summary.qualified is False
    assert summary.blocker_count == 4
    assert summary.database_repository_count == 2


def test_require_qualified_rejects_blocked_profile(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--require-qualified"]) == 2
    assert "still blocked" in capsys.readouterr().err


def test_duplicate_yaml_key_is_rejected(tmp_path: Path) -> None:
    text = DEFAULT_PROFILE.read_text(encoding="utf-8")
    duplicate = text.replace(
        "schema_version: 1.0.0", "schema_version: 1.0.0\nschema_version: 1.0.0", 1
    )
    path = tmp_path / "duplicate.yaml"
    path.write_text(duplicate, encoding="utf-8")

    with pytest.raises(RecoveryProfileError, match="duplicate key"):
        validate_profile(path)


def test_database_repositories_must_be_separate(tmp_path: Path) -> None:
    profile = _profile()
    databases = profile["databases"]
    assert isinstance(databases, dict)
    application = databases["application"]
    zabbix = databases["zabbix"]
    assert isinstance(application, dict)
    assert isinstance(zabbix, dict)
    zabbix["repository_id"] = application["repository_id"]

    with pytest.raises(RecoveryProfileError, match="separate repository IDs"):
        validate_profile(_write_profile(tmp_path, profile))


def test_qualified_claim_requires_independent_destination(tmp_path: Path) -> None:
    profile = _profile()
    qualification = profile["qualification"]
    assert isinstance(qualification, dict)
    qualification.update({"qualified": True, "status": "qualified", "blockers": []})

    with pytest.raises(RecoveryProfileError, match="approved independent destination"):
        validate_profile(_write_profile(tmp_path, profile))


def test_restic_cannot_include_database_data(tmp_path: Path) -> None:
    profile = _profile()
    file_backup = profile["file_backup"]
    assert isinstance(file_backup, dict)
    included = file_backup["included_classes"]
    assert isinstance(included, list)
    included.append("database_data_directories")

    with pytest.raises(RecoveryProfileError, match="must not contain PostgreSQL"):
        validate_profile(_write_profile(tmp_path, profile))


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("repository_password", "do-not-store-this", "secret-like field"),
        ("source_url", "https://user:pass@example.invalid/tool", "URL user information"),
    ],
)
def test_public_profile_rejects_secret_material(
    tmp_path: Path, field: str, value: str, message: str
) -> None:
    profile = _profile()
    tools = profile["tools"]
    assert isinstance(tools, dict)
    pgbackrest = tools["pgbackrest"]
    assert isinstance(pgbackrest, dict)
    pgbackrest[field] = value

    with pytest.raises(RecoveryProfileError, match=message):
        validate_profile(_write_profile(tmp_path, profile))
