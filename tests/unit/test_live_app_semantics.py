"""Boundaries for the private exact-release semantic-review capture tool."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[2]


def _module() -> ModuleType:
    path = ROOT / "scripts/evaluate_live_app_semantics.py"
    spec = importlib.util.spec_from_file_location("evaluate_live_app_semantics", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _case(**updates: str) -> dict[str, str]:
    case = {
        "id": "EN-FILES-01",
        "mode": "incident",
        "locale": "en",
        "question": "Only show system files.",
        "target_id": "app",
    }
    case.update(updates)
    return case


def test_semantic_review_corpus_is_bounded_and_requires_explicit_routes() -> None:
    module = _module()
    assert module.validate_cases({"cases": [_case()]})[0]["target_id"] == "app"
    assert (
        module.validate_cases({"cases": [_case(mode="general", target_id="")]})[0]["mode"]
        == "general"
    )

    invalid_cases: tuple[dict[str, Any], ...] = (
        {"cases": []},
        {"cases": [_case(), _case()]},
        {"cases": [_case(mode="shell")]},
        {"cases": [_case(target_id="../app")]},
        {"cases": [{**_case(), "target_id": None}]},
        {"cases": [_case(question=" ")]},
        {"cases": [_case()] * 13},
    )
    for invalid in invalid_cases:
        with pytest.raises(ValueError):
            module.validate_cases(invalid)


def test_semantic_review_restricts_credentials_to_private_https_origin() -> None:
    module = _module()
    assert module.validate_private_https_origin("https://192.168.1.10/") == "https://192.168.1.10"
    assert module.validate_private_https_origin("https://nextops.local") == "https://nextops.local"
    for invalid in (
        "http://192.168.1.10",
        "https://example.com",
        "https://user:secret@192.168.1.10",
        "https://192.168.1.10/path",
        "https://192.168.1.10/?key=secret",
    ):
        with pytest.raises(ValueError):
            module.validate_private_https_origin(invalid)


def test_semantic_review_private_report_is_not_overwritten(tmp_path: Path) -> None:
    module = _module()
    report = tmp_path / "semantic-review.json"
    module.write_private_report(report, {"manual_semantic_review_required": True})
    assert json.loads(report.read_text(encoding="utf-8"))["manual_semantic_review_required"]
    if os.name == "posix":
        assert report.stat().st_mode & 0o777 == 0o600
    with pytest.raises(FileExistsError):
        module.write_private_report(report, {})
    with pytest.raises(ValueError, match="absolute"):
        module.write_private_report(Path("relative.json"), {})
    with pytest.raises(ValueError, match="outside the repository"):
        module.write_private_report(ROOT / "uncommitted-review.json", {})


def test_semantic_review_redirects_are_rejected() -> None:
    module = _module()
    assert module.NoRedirect().redirect_request(None, None, None, None, None) is None


def test_semantic_review_captures_an_authenticated_case_and_logs_out(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    module = _module()
    endpoint = tmp_path / "endpoint.txt"
    login = tmp_path / "login.txt"
    corpus = tmp_path / "corpus.json"
    output = tmp_path / "report.json"
    endpoint.write_text("url: https://nextops.local\n", encoding="utf-8")
    login.write_text("username: reviewer\npassword: " + "x" * 32 + "\n", encoding="utf-8")
    corpus.write_text(json.dumps({"cases": [_case()]}), encoding="utf-8")
    if os.name == "posix":
        for path in (endpoint, login, corpus):
            path.chmod(0o600)

    requests: list[tuple[str, dict[str, str], str | None]] = []

    class FakeResponse:
        def __init__(self, status: int, body: dict[str, Any] | None) -> None:
            self.status = status
            self.body = json.dumps(body).encode() if body is not None else b""

        def __enter__(self) -> FakeResponse:
            return self

        def __exit__(self, *_args: Any) -> None:
            return None

        def read(self, _size: int) -> bytes:
            return self.body

    class FakeOpener:
        def open(self, request: Any, *, timeout: int) -> FakeResponse:
            assert timeout == 120
            payload = json.loads(request.data)
            auth = request.get_header("Authorization")
            requests.append((request.full_url, payload, auth))
            if request.full_url.endswith("/login"):
                return FakeResponse(200, {"session": {"access_token": "t" * 40}})
            if request.full_url.endswith("/logout"):
                return FakeResponse(204, None)
            return FakeResponse(200, {"answer": "Only system files.", "evidence": []})

    monkeypatch.setattr(
        module,
        "parse_args",
        lambda: argparse.Namespace(
            endpoint_file=endpoint,
            login_file=login,
            ca_file=tmp_path / "ca.pem",
            corpus=corpus,
            output=output,
            expected_release="nextops-0.1.0-01755d1",
        ),
    )
    monkeypatch.setattr(module.ssl, "create_default_context", lambda **_kwargs: object())
    monkeypatch.setattr(module, "build_opener", lambda *_args: FakeOpener())

    assert module.main() == 0
    assert [entry[0].rsplit("/", 1)[-1] for entry in requests] == [
        "login",
        "investigate",
        "logout",
    ]
    assert requests[1][2] == "Bearer " + "t" * 40
    assert requests[1][1]["question"] == "Only show system files."
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["manual_semantic_review_required"] is True
    assert report["acceptance_claimed"] is False
    assert report["cases"][0]["result"]["body"]["answer"] == "Only system files."
    assert "t" * 40 not in output.read_text(encoding="utf-8")
    assert "Only system files." not in capsys.readouterr().out
