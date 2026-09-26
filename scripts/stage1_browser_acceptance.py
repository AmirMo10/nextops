"""Qualify a fresh browser against a private NextOps endpoint with WAN denied."""

from __future__ import annotations

import argparse
import json
import socketserver
import threading
from contextlib import ExitStack
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import Browser, BrowserContext, Page, Response, sync_playwright


class DenyProxyHandler(socketserver.StreamRequestHandler):
    def handle(self) -> None:
        request_line = self.rfile.readline(4096).decode("latin-1", errors="replace").strip()
        if request_line:
            self.server.attempts.append(request_line)  # type: ignore[attr-defined]
        while True:
            line = self.rfile.readline(4096)
            if not line or line in {b"\r\n", b"\n"}:
                break
        self.wfile.write(
            b"HTTP/1.1 502 WAN Blocked\r\nConnection: close\r\nContent-Length: 0\r\n\r\n"
        )


class ThreadingDenyProxy(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self) -> None:
        self.attempts: list[str] = []
        super().__init__(("127.0.0.1", 0), DenyProxyHandler)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--username", required=True)
    parser.add_argument("--password-file", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def revoke_test_session(context: BrowserContext, base_url: str, token: str) -> str:
    """Attempt server-side revocation without adding the token to the evidence report."""

    response = context.request.post(
        f"{base_url.rstrip('/')}/api/v1/logout",
        headers={"Authorization": f"Bearer {token}"},
        timeout=10_000,
    )
    return "revoked" if response.status == 204 else "revocation_failed"


def main() -> int:
    args = parse_args()
    password = args.password_file.read_text(encoding="utf-8-sig").strip()
    check(len(password) >= 32, "protected password file is invalid")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    host = urlparse(args.base_url).hostname
    check(bool(host), "base URL must contain a hostname")

    result: dict[str, object] = {
        "started_at": datetime.now(UTC).isoformat(),
        "base_url": args.base_url,
        "browser": "Microsoft Edge",
        "fresh_context": True,
        "tls_verification": "enabled",
        "wan_policy": "deny proxy with private application host bypass only",
        "checks": {},
        "api_statuses": [],
        "page_request_hosts": [],
        "deny_proxy_attempts": [],
        "status": "FAIL",
    }
    checks: dict[str, object] = result["checks"]  # type: ignore[assignment]
    api_statuses: list[dict[str, object]] = result["api_statuses"]  # type: ignore[assignment]
    request_hosts: set[str] = set()
    browser: Browser | None = None
    context: BrowserContext | None = None
    page: Page | None = None
    session_token: str | None = None

    def cleanup_browser() -> None:
        if result["status"] != "PASS" and context is not None:
            try:
                token = session_token
                if not token and page is not None:
                    token = page.evaluate("sessionStorage.getItem('nextops-session')")
                if isinstance(token, str) and token:
                    result["failure_session_cleanup"] = revoke_test_session(
                        context, args.base_url, token
                    )
                else:
                    result["failure_session_cleanup"] = "no_tab_session"
            except Exception as cleanup_error:
                result["failure_session_cleanup"] = "revocation_unverified"
                result["cleanup_error_type"] = type(cleanup_error).__name__
        for resource in (context, browser):
            if resource is not None:
                try:
                    resource.close()
                except Exception as close_error:
                    result["status"] = "FAIL"
                    result["resource_close_error_type"] = type(close_error).__name__

    proxy = ThreadingDenyProxy()
    proxy_thread = threading.Thread(target=proxy.serve_forever, daemon=True)
    proxy_thread.start()
    try:
        with sync_playwright() as playwright, ExitStack() as cleanup_stack:
            cleanup_stack.callback(cleanup_browser)
            browser = playwright.chromium.launch(
                channel="msedge",
                headless=True,
                proxy={
                    "server": f"http://127.0.0.1:{proxy.server_address[1]}",
                    "bypass": host,
                },
                args=[
                    "--disable-background-networking",
                    "--disable-component-update",
                    "--disable-default-apps",
                    "--disable-domain-reliability",
                    "--no-first-run",
                ],
            )
            context = browser.new_context(
                locale="en-GB",
                service_workers="block",
                viewport={"width": 1440, "height": 1000},
            )
            page = context.new_page()
            page.set_default_timeout(180_000)
            page.on(
                "request",
                lambda request: request_hosts.add(urlparse(request.url).hostname or ""),
            )

            def record_response(response: Response) -> None:
                path = urlparse(response.url).path
                if path.startswith("/api/"):
                    api_statuses.append({"path": path, "status": response.status})

            page.on("response", record_response)

            page.goto(args.base_url, wait_until="networkidle")
            check(page.locator("#loginForm").is_visible(), "fresh login form is not visible")
            check(page.evaluate("document.documentElement.lang") == "en", "English lang missing")
            check(page.evaluate("document.documentElement.dir") == "ltr", "LTR direction missing")
            checks["fresh_login_page"] = "PASS"
            checks["english_ltr"] = "PASS"

            page.locator("#username").fill(args.username)
            page.locator("#password").fill(password)
            page.locator("#loginForm button[type=submit]").click()
            page.locator("#workspaceView:not(.hidden)").wait_for()
            session_token = page.evaluate("sessionStorage.getItem('nextops-session')")
            check(bool(session_token), "authenticated tab session is missing")
            page.locator("#aiStatus.ready").wait_for()
            page.locator("#monitoringStatus.ready").wait_for()
            checks["authenticated_workspace"] = "PASS"
            checks["ai_readiness"] = "PASS"
            checks["monitoring_readiness"] = "PASS"

            page.locator("#question").fill("Hi. Reply with one short friendly greeting.")
            page.locator("#assistantForm").evaluate("form => form.requestSubmit()")
            page.locator("#resultCard:not(.hidden)").wait_for(timeout=180_000)
            general_answer = page.locator("#answer").inner_text().strip()
            check(bool(general_answer), "general answer is empty")
            check(
                "hidden" in (page.locator("#evidencePanel").get_attribute("class") or ""),
                "general answer exposed monitoring evidence",
            )
            check(
                "no live evidence" in page.locator("#evidenceBadge").inner_text().lower(),
                "general answer badge is incorrect",
            )
            checks["general_mode_direct_answer"] = "PASS"
            checks["general_answer_length"] = len(general_answer)

            page.locator("#languageButton").click()
            check(page.evaluate("document.documentElement.lang") == "fa", "Persian lang missing")
            check(page.evaluate("document.documentElement.dir") == "rtl", "RTL direction missing")
            check(
                "از دستیار داخلی بپرسید" in page.locator("#workspaceView h1").inner_text(),
                "Persian workspace text missing",
            )
            checks["persian_rtl"] = "PASS"

            page.locator('.mode-choice[data-mode="monitoring"]').click()
            page.locator('.locale-choice[data-locale="fa"]').click()
            page.locator("#question").fill(
                "وضعیت فعلی سامانهٔ پایش چیست؟ پاسخ را کوتاه و فقط بر پایهٔ شواهد زنده ارائه کن."
            )
            page.locator("#assistantForm").evaluate("form => form.requestSubmit()")
            page.locator("#resultCard:not(.hidden)").wait_for(timeout=240_000)
            page.locator("#evidencePanel:not(.hidden)").wait_for(timeout=240_000)
            monitoring_answer = page.locator("#answer").inner_text().strip()
            check(bool(monitoring_answer), "monitoring answer is empty")
            check(
                page.locator("#answer").get_attribute("dir") == "rtl", "Persian answer is not RTL"
            )
            check(
                page.locator("#evidenceSource").inner_text().startswith("Zabbix"),
                "Zabbix provenance is missing",
            )
            check(
                page.locator("#runId").inner_text().strip() not in {"", "—"},
                "durable run id is missing",
            )
            check(
                page.locator("#evidenceReference").inner_text().strip() not in {"", "—"},
                "evidence reference is missing",
            )
            check(
                page.locator("#auditEventId").inner_text().strip() not in {"", "—"},
                "audit event id is missing",
            )
            checks["persian_monitoring_answer"] = "PASS"
            checks["zabbix_provenance"] = "PASS"
            checks["durable_audit_identifiers"] = "PASS"
            checks["monitoring_answer_length"] = len(monitoring_answer)

            page.screenshot(path=args.output_dir / "fresh-browser-qualified.png", full_page=True)

            page.locator("#logoutButton").click()
            page.locator("#loginView:not(.hidden)").wait_for()
            check(page.locator("#loginView").is_visible(), "logout did not return to login")
            check(
                page.evaluate("sessionStorage.getItem('nextops-session')") is None,
                "logout did not clear tab session",
            )
            check(
                {"path": "/api/v1/logout", "status": 204} in api_statuses,
                "logout did not receive the expected server revocation response",
            )
            session_token = None
            checks["client_logout"] = "PASS"
            checks["server_session_revocation"] = "PASS"

            clean_page = context.new_page()
            clean_page.goto(args.base_url, wait_until="networkidle")
            check(clean_page.locator("#loginForm").is_visible(), "new tab did not require login")
            checks["new_tab_requires_login"] = "PASS"

            result["page_request_hosts"] = sorted(request_hosts)
            external_hosts = sorted(item for item in request_hosts if item and item != host)
            check(not external_hosts, f"page attempted external hosts: {external_hosts}")
            checks["no_page_wan_requests"] = "PASS"
            checks["browser_background_wan_blocked"] = "PASS"
            checks["deny_proxy_observed_attempts"] = len(proxy.attempts)
            result["status"] = "PASS"
    except Exception as exc:
        result["error_type"] = type(exc).__name__
        result["error"] = str(exc)
    finally:
        result["deny_proxy_attempts"] = list(proxy.attempts)
        result["finished_at"] = datetime.now(UTC).isoformat()
        proxy.shutdown()
        proxy.server_close()
        result_path = args.output_dir / "fresh-browser-result.json"
        result_path.write_text(
            json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

    print(f"browser_acceptance_status={result['status']}")
    print(f"evidence_file={args.output_dir / 'fresh-browser-result.json'}")
    print(f"wan_attempts={len(proxy.attempts)}")
    if result["status"] != "PASS":
        print(f"failure={result.get('error_type')}: {result.get('error')}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
