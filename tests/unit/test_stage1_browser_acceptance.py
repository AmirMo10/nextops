"""Failure cleanup for the live browser acceptance harness."""

import importlib.util
import json
from argparse import Namespace
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import cast
from unittest.mock import MagicMock, patch

from playwright.sync_api import BrowserContext

ROOT = Path(__file__).parents[2]


def _acceptance_module() -> ModuleType:
    path = ROOT / "scripts" / "stage1_browser_acceptance.py"
    spec = importlib.util.spec_from_file_location("stage1_browser_acceptance", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_failure_cleanup_revokes_session_without_logging_token() -> None:
    context = MagicMock()
    context.request.post.return_value.status = 204

    outcome = _acceptance_module().revoke_test_session(
        cast(BrowserContext, context), "https://app.example/", "test-token"
    )

    assert outcome == "revoked"
    context.request.post.assert_called_once_with(
        "https://app.example/api/v1/logout",
        headers={"Authorization": "Bearer test-token"},
        timeout=10_000,
    )


def test_failure_cleanup_does_not_treat_non_204_as_revoked() -> None:
    context = MagicMock()
    context.request.post.return_value.status = 401

    outcome = _acceptance_module().revoke_test_session(
        cast(BrowserContext, context), "https://app.example", "token"
    )

    assert outcome == "revocation_failed"


def test_post_login_failure_revokes_before_playwright_shutdown(tmp_path: Path) -> None:
    module = _acceptance_module()
    password_file = tmp_path / "password.txt"
    password_file.write_text("x" * 32, encoding="utf-8")
    output_dir = tmp_path / "report"
    events: list[str] = []

    manager = MagicMock()
    browser = manager.__enter__.return_value.chromium.launch.return_value
    context = browser.new_context.return_value
    page = context.new_page.return_value
    page.evaluate.side_effect = lambda expression: {
        "document.documentElement.lang": "en",
        "document.documentElement.dir": "ltr",
        "sessionStorage.getItem('nextops-session')": "test-token",
    }[expression]

    def locator(selector: str) -> MagicMock:
        selected = MagicMock()
        if selector == "#aiStatus.ready":
            selected.wait_for.side_effect = AssertionError("forced post-login failure")
        return selected

    page.locator.side_effect = locator

    def revoke(*_args: object, **_kwargs: object) -> SimpleNamespace:
        events.append("revoke")
        return SimpleNamespace(status=204)

    context.request.post.side_effect = revoke
    manager.__exit__.side_effect = lambda *_args: events.append("playwright_shutdown")
    args = Namespace(
        base_url="https://app.example",
        username="test-user",
        password_file=password_file,
        output_dir=output_dir,
    )
    with (
        patch.object(module, "sync_playwright", return_value=manager),
        patch.object(module, "parse_args", return_value=args),
    ):
        assert module.main() == 1

    report = json.loads((output_dir / "fresh-browser-result.json").read_text(encoding="utf-8"))
    assert report["status"] == "FAIL"
    assert report["failure_session_cleanup"] == "revoked"
    assert "test-token" not in json.dumps(report)
    assert events == ["revoke", "playwright_shutdown"]
