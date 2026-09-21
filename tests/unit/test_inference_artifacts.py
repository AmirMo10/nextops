"""Selected local-inference artifact metadata validation tests."""

import subprocess
import sys
from pathlib import Path

import yaml

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
MANIFEST = REPOSITORY_ROOT / "deploy" / "inference" / "qwen3-8b-q4-k-m.yaml"


def test_selected_artifact_manifest_is_human_readable_and_schema_valid() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_inference_artifacts.py"],
        cwd=REPOSITORY_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "selected_not_imported" in result.stdout
    document = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    assert document["model"]["size_bytes"] == 5_027_783_488
    assert document["model"]["sha256"] == (
        "d98cdcbd03e17ce47681435b5150e34c1417f50b5c0019dd560e4882c5745785"
    )
    assert document["runtime"]["binary_sha256"] is None
    assert document["evidence"]["benchmark_run"] is False
