"""Contract checks for the bounded Stage 1B evaluation corpus and client."""

import importlib.util
import json
import os
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).parents[2]


def _evaluation_module() -> ModuleType:
    path = ROOT / "scripts" / "evaluate_stage1b.py"
    spec = importlib.util.spec_from_file_location("evaluate_stage1b", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_evaluation_origin_is_strict_ipv4_loopback() -> None:
    module = _evaluation_module()

    assert module.validate_loopback_origin("http://127.0.0.1:8090/") == "http://127.0.0.1:8090"
    for rejected in (
        "https://127.0.0.1:8090",
        "http://localhost:8090",
        "http://0.0.0.0:8090",
        "http://127.0.0.1:8090/path",
    ):
        with pytest.raises(ValueError):
            module.validate_loopback_origin(rejected)


def test_evaluation_corpus_is_balanced_and_non_operational() -> None:
    corpus_path = ROOT / "deploy" / "inference" / "stage1b-evaluation-v1.json"
    corpus = json.loads(corpus_path.read_text(encoding="utf-8"))

    assert corpus["schema_version"] == "2.0.0"
    assert [case["locale"] for case in corpus["cases"]].count("en") == 4
    assert [case["locale"] for case in corpus["cases"]].count("fa") == 4
    assert all(len(case["review"]) == 3 for case in corpus["cases"])
    assert all(case["must_include_any"] for case in corpus["cases"])
    assert all(case["must_not_include"] for case in corpus["cases"])
    assert "production acceptance" in corpus["purpose"]


def test_automated_case_review_reports_pass_and_safe_failure_details() -> None:
    module = _evaluation_module()
    case = {
        "locale": "en",
        "must_include_any": [["unknown", "cannot determine"]],
        "must_not_include": ["healthy now"],
    }

    passed = module.evaluate_case(case, {"body": {"answer": "The current state is unknown."}})
    failed = module.evaluate_case(case, {"body": {"answer": "Everything is healthy now."}})

    assert passed["passed"] is True
    assert failed["passed"] is False
    assert failed["checks"][2]["matched_count"] == 1


def test_automated_case_review_rejects_prompt_echo() -> None:
    module = _evaluation_module()
    prompt = "No live evidence is supplied. Is the service healthy now?"
    case = {
        "locale": "en",
        "prompt": prompt,
        "must_include_any": [["unknown"]],
        "must_not_include": ["healthy now"],
    }

    result = module.evaluate_case(case, {"body": {"answer": prompt}})

    assert result["passed"] is False
    assert result["checks"][0] == {"id": "prompt_echo_absent", "passed": False}


def test_evaluation_report_is_written_to_an_absolute_private_file(tmp_path: Path) -> None:
    module = _evaluation_module()
    output = tmp_path / "evidence.json"

    module.write_private_report(output, {"acceptance_claimed": False})

    assert json.loads(output.read_text(encoding="utf-8")) == {"acceptance_claimed": False}
    if os.name == "posix":
        assert output.stat().st_mode & 0o777 == 0o600

    with pytest.raises(ValueError, match="absolute"):
        module.write_private_report(Path("relative.json"), {})
