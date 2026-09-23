"""Forced-command Linux collector safety tests (Linux CI only)."""

import json
import os
import sys
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest

if os.name != "posix":
    pytest.skip("Linux collector executes only on POSIX hosts", allow_module_level=True)

COLLECTOR_PATH = Path(__file__).resolve().parents[2] / "scripts" / "linux_readonly_collector.py"
COLLECTOR_SPEC = spec_from_file_location("nextops_linux_readonly_collector", COLLECTOR_PATH)
if COLLECTOR_SPEC is None or COLLECTOR_SPEC.loader is None:
    raise RuntimeError("unable to load the standalone Linux collector")
collector = module_from_spec(COLLECTOR_SPEC)
COLLECTOR_SPEC.loader.exec_module(collector)


def _write_config(path: Path, **changes: object) -> None:
    payload: dict[str, object] = {
        "schema_version": "1.0.0",
        "target_id": "app",
        "filesystems": ["/"],
        "services": ["nextops-app.service"],
    }
    payload.update(changes)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_collector_configuration_is_exact_and_allowlisted(tmp_path: Path) -> None:
    config = tmp_path / "collector.json"
    _write_config(config)

    loaded = collector._load_config(config)

    assert loaded["target_id"] == "app"
    assert loaded["filesystems"] == ["/"]


@pytest.mark.parametrize(
    ("change", "message"),
    [
        ({"target_id": "../../root"}, "target id"),
        ({"filesystems": ["/", "/tmp/../root"]}, "filesystem allowlist"),
        ({"services": ["ssh"]}, "service allowlist"),
        ({"services": []}, "service allowlist"),
        ({"extra": "field"}, "fields"),
    ],
)
def test_collector_rejects_unbounded_configuration(
    tmp_path: Path,
    change: dict[str, object],
    message: str,
) -> None:
    config = tmp_path / "collector.json"
    _write_config(config, **change)

    with pytest.raises(collector.CollectorError, match=message):
        collector._load_config(config)


def test_collector_redacts_secret_assignments_from_journal_text() -> None:
    value = "request failed token=abc123 authorization: Bearer bearer-value password=hunter2"

    redacted = collector._safe_text(value, 512)

    assert "abc123" not in redacted
    assert "hunter2" not in redacted
    assert "bearer-value" not in redacted
    assert "token=[REDACTED]" in redacted
    assert "password=[REDACTED]" in redacted


def test_collector_main_denies_non_forced_execution(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["linux_readonly_collector.py"])
    monkeypatch.delenv("SSH_ORIGINAL_COMMAND", raising=False)

    assert collector.main() == 64
