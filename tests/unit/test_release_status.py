"""Release/status manifest invariants."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


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
