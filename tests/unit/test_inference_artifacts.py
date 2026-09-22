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
    assert "controlled_service_qualified_not_production_accepted" in result.stdout
    document = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    assert document["model"]["size_bytes"] == 5_027_783_488
    assert document["model"]["sha256"] == (
        "d98cdcbd03e17ce47681435b5150e34c1417f50b5c0019dd560e4882c5745785"
    )
    assert document["runtime"]["binary_sha256"] == (
        "dbe5a5cdd4842fe2d498270c1e1df58344e9052e97214e2ba9c9845443a1b0dc"
    )
    assert document["evidence"]["runtime_binary_built"] is True
    assert document["evidence"]["model_imported"] is True
    assert document["evidence"]["cpu_only_execution_verified"] is True
    assert document["evidence"]["controlled_service_installed"] is True
    assert document["evidence"]["application_source_commit"] == (
        "62de8d61fb4a841f016732815f75d95ca6c403a9"
    )
    assert document["evidence"]["authentication_readiness_verified"] is True
    assert document["evidence"]["bilingual_quality_review_passed"] is True
    assert document["evidence"]["bounded_load_run"] is True
    assert document["evidence"]["cold_process_restart_verified"] is True
    assert document["evidence"]["application_rollback_verified"] is True
    assert document["evidence"]["benchmark_run"] is False
    assert document["evidence"]["offline_cold_start_verified"] is False
