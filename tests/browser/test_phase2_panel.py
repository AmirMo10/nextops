"""Real-browser acceptance for the bilingual Phase 2 incident panel."""

from __future__ import annotations

import socket
import threading
import time
from collections.abc import Iterator
from pathlib import Path
from typing import Any
from urllib.request import urlopen
from uuid import uuid4

import pytest
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Page, expect, sync_playwright

pytestmark = pytest.mark.browser
STATIC = Path(__file__).resolve().parents[2] / "packages" / "nextops" / "api" / "static"
NOW = "2026-09-23T10:00:00Z"


def _assistant(locale: str) -> dict[str, Any]:
    return {
        "request_id": str(uuid4()),
        "correlation_id": str(uuid4()),
        "locale": locale,
        "answer": (
            "شواهد زنده در دسترس است و علت قطعی هنوز اثبات نشده است."
            if locale == "fa"
            else "Live evidence is available; a definitive root cause is not established."
        ),
        "model_id": "nextops-qwen3-8b-q4-k-m",
        "prompt_tokens": 120,
        "completion_tokens": 16,
        "finish_reason": "stop",
        "started_at": NOW,
        "completed_at": "2026-09-23T10:00:01Z",
        "queue_ms": 0,
        "cpu_only_required": True,
        "evidence_mode": "model_only",
        "live_monitoring_data": False,
    }


def _summary() -> dict[str, Any]:
    return {
        "source": "zabbix",
        "source_version": "7.0.30",
        "host": "NextOps App",
        "collected_at": NOW,
        "metrics": [
            {
                "name": "CPU idle time",
                "key": "system.cpu.util[,idle]",
                "value": "91.2",
                "units": "%",
                "measured_at": "2026-09-23T09:59:45Z",
                "stale": False,
            }
        ],
        "active_problems": [],
        "is_partial": False,
        "partial_reasons": [],
    }


def _incident_response(locale: str, target_id: str) -> dict[str, Any]:
    summary = _summary()
    evidence = {
        "target_id": target_id,
        "zabbix": {
            "source": "zabbix",
            "source_version": "7.0.30",
            "host": "NextOps App",
            "collected_at": NOW,
            "window_started_at": "2026-09-23T09:00:00Z",
            "window_ended_at": NOW,
            "summary": summary,
            "history": [],
            "events": [
                {
                    "event_id": "30001",
                    "name": "CPU pressure observed",
                    "severity": 3,
                    "occurred_at": "2026-09-23T09:58:00Z",
                    "state": "problem",
                    "acknowledged": False,
                    "suppressed": False,
                }
            ],
            "is_partial": False,
            "partial_reasons": [],
        },
        "linux": {
            "source": "linux",
            "collector_version": "1.0.0",
            "target_id": target_id,
            "hostname": "nextops-app",
            "operating_system": "Ubuntu 24.04.3 LTS",
            "collected_at": NOW,
            "uptime_seconds": 7200,
            "logical_cpu_count": 8,
            "load_1m": 0.1,
            "load_5m": 0.2,
            "load_15m": 0.3,
            "memory_total_bytes": 34_359_738_368,
            "memory_available_bytes": 30_064_771_072,
            "swap_total_bytes": 0,
            "swap_free_bytes": 0,
            "filesystems": [
                {
                    "path": "/",
                    "total_bytes": 100_000,
                    "available_bytes": 75_000,
                    "used_percent": 25.0,
                }
            ],
            "processes": [{"pid": 101, "name": "uvicorn", "rss_bytes": 120_000_000}],
            "services": [
                {
                    "unit": "nextops-app.service",
                    "load_state": "loaded",
                    "active_state": "active",
                    "sub_state": "running",
                }
            ],
            "journal": [],
            "local_user_count": 1,
            "logged_in_user_count": 0,
            "installed_package_count": 850,
            "listening_sockets": [],
            "routes": [],
            "nameservers": [],
            "is_partial": False,
            "partial_reasons": [],
        },
        "is_partial": False,
        "partial_reasons": [],
    }
    run_id = str(uuid4())
    return {
        "assistant": _assistant(locale),
        "evidence": evidence,
        "run_id": run_id,
        "evidence_reference": f"run-evidence:{run_id}",
        "evidence_sha256": "a" * 64,
        "audit_event_id": str(uuid4()),
        "evidence_mode": "live_zabbix_linux",
        "live_monitoring_data": True,
    }


def _fixture_app() -> FastAPI:
    app = FastAPI()
    app.mount("/assets", StaticFiles(directory=STATIC), name="assets")
    app.state.incident_requests = []

    @app.get("/")
    def panel() -> FileResponse:
        return FileResponse(STATIC / "index.html")

    @app.post("/api/v1/login")
    async def login() -> dict[str, Any]:
        return {
            "actor": {
                "subject_id": str(uuid4()),
                "organization_id": str(uuid4()),
                "environment_id": str(uuid4()),
                "roles": ["admin"],
                "scopes": ["zabbix.read", "linux.read", "runs.read"],
            },
            "session": {"access_token": "browser-test-token", "expires_at": NOW},
        }

    @app.get("/api/v1/me")
    async def me() -> dict[str, str]:
        return {"status": "authenticated"}

    @app.get("/api/v1/assistant/ready")
    async def ready() -> dict[str, Any]:
        return {
            "state": "ready",
            "model_id": "nextops-qwen3-8b-q4-k-m",
            "runtime_version": "v0.4.1",
            "cpu_only_required": True,
            "max_active_requests": 1,
            "max_queued_requests": 2,
            "active_requests": 0,
            "queued_requests": 0,
        }

    @app.get("/api/v1/monitoring/summary")
    async def summary() -> dict[str, Any]:
        return _summary()

    @app.get("/api/v1/incidents/targets")
    async def targets() -> dict[str, list[str]]:
        return {"targets": ["app", "ai", "connector", "zabbix"]}

    @app.post("/api/v1/incidents/investigate")
    async def incident(request: Request) -> dict[str, Any]:
        payload = await request.json()
        app.state.incident_requests.append(payload)
        return _incident_response(str(payload["locale"]), str(payload["target_id"]))

    return app


@pytest.fixture()
def browser_server() -> Iterator[tuple[str, FastAPI]]:
    app = _fixture_app()
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = int(probe.getsockname()[1])
    server = uvicorn.Server(
        uvicorn.Config(app, host="127.0.0.1", port=port, log_level="error", access_log=False)
    )
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{port}"
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        try:
            with urlopen(f"{base_url}/", timeout=0.25) as response:
                if response.status == 200:
                    break
        except OSError:
            time.sleep(0.05)
    else:
        server.should_exit = True
        thread.join(timeout=5)
        raise RuntimeError("browser fixture server did not start")
    try:
        yield base_url, app
    finally:
        server.should_exit = True
        thread.join(timeout=5)


def _login(page: Page, base_url: str) -> None:
    page.goto(base_url, wait_until="networkidle")
    expect(page.locator(".ocs-logo-header")).to_be_visible()
    expect(page.get_by_text("Omid System Computer Services")).to_be_visible()
    logo_background = str(
        page.locator(".ocs-logo-header").evaluate(
            "element => getComputedStyle(element).backgroundImage"
        )
    )
    assert logo_background.startswith('url("data:image/jpeg;base64,')
    icon_href = page.locator("#appIcon").get_attribute("href")
    assert icon_href is not None
    assert icon_href.startswith("data:image/jpeg;base64,")
    page.locator("#languageButton").click()
    page.set_viewport_size({"width": 375, "height": 812})
    assert page.locator("html").get_attribute("dir") == "rtl"
    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth") is True
    page.locator("#languageButton").click()
    page.set_viewport_size({"width": 1280, "height": 900})
    page.get_by_label("Username").fill("owner")
    page.get_by_label("Password").fill("test-password")
    page.get_by_role("button", name="Sign in securely").click()
    expect(page.get_by_role("heading", name="Ask the local assistant")).to_be_visible()


def _launch_browser(playwright: Any) -> Any:
    try:
        return playwright.chromium.launch()
    except PlaywrightError:
        return playwright.chromium.launch(channel="chrome")


def test_phase2_panel_supports_incident_evidence_and_persian_rtl(
    browser_server: tuple[str, FastAPI],
) -> None:
    base_url, app = browser_server
    with sync_playwright() as playwright:
        browser = _launch_browser(playwright)
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        _login(page, base_url)

        page.get_by_role("button", name="Incident investigation").click()
        target = page.get_by_label("Investigation target")
        expect(target).to_be_visible()
        target.select_option("app")
        page.get_by_label("Question").fill("Explain the current application condition.")
        page.get_by_role("button", name="Ask assistant").click()

        expect(page.get_by_text("Live Zabbix + Linux evidence")).to_be_visible()
        expect(page.get_by_text("nextops-app.service")).to_be_visible()
        expect(page.get_by_text("CPU pressure observed")).to_be_visible()
        assert app.state.incident_requests[-1]["target_id"] == "app"

        page.locator("#languageButton").click()
        expect(page.get_by_role("button", name="بررسی رخداد")).to_be_visible()
        expect(page.get_by_text("شرکت رایانه خدمات امید سیستم")).to_be_hidden()
        expect(page.locator(".brand").get_by_text("هوشمندی داخلی برای عملیات")).to_be_visible()
        assert page.locator("html").get_attribute("dir") == "rtl"

        page.set_viewport_size({"width": 375, "height": 812})
        assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth") is True
        assert page.get_by_role("button", name="بررسی رخداد").evaluate(
            "element => element.getBoundingClientRect().height >= 44"
        )

        page.emulate_media(reduced_motion="reduce")
        page.set_viewport_size({"width": 844, "height": 390})
        assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth") is True
        browser.close()
