"""Credential-bearing transports must not follow an upstream redirect."""

from __future__ import annotations

import asyncio
import ssl
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import pytest

from nextops.application.errors import ApplicationError
from nextops.connectors.zabbix import HttpsZabbixTransport
from nextops.contracts.errors import ErrorCode
from nextops.inference.llama_cpp import UrllibJsonTransport


@contextmanager
def redirecting_server() -> Iterator[tuple[str, list[str]]]:
    seen_paths: list[str] = []

    class RedirectHandler(BaseHTTPRequestHandler):
        def do_POST(self) -> None:
            seen_paths.append(self.path)
            if self.path == "/capture":
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"result": {}}')
            else:
                self.send_response(302)
                self.send_header("Location", "/capture")
                self.end_headers()

        def do_GET(self) -> None:
            seen_paths.append(self.path)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"result": {}}')

        def log_message(self, format: str, *args: Any) -> None:
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), RedirectHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}", seen_paths
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_loopback_transport_rejects_redirect_before_forwarding_bearer() -> None:
    with redirecting_server() as (origin, seen_paths):
        transport = UrllibJsonTransport(origin)
        with pytest.raises(ApplicationError) as caught:
            asyncio.run(
                transport.post_json(
                    "/api/v1/generate",
                    {"prompt": "hello"},
                    {"Authorization": "Bearer test-only-secret"},
                    2.0,
                )
            )

    assert caught.value.code is ErrorCode.DEPENDENCY_UNAVAILABLE
    assert seen_paths == ["/api/v1/generate"]


def test_zabbix_transport_rejects_redirect_before_forwarding_bearer(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        ssl,
        "create_default_context",
        lambda **_kwargs: ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT),
    )
    with redirecting_server() as (origin, seen_paths):
        transport = HttpsZabbixTransport(
            "https://zabbix.example/api_jsonrpc.php",
            Path("unused-test-ca"),
            "test-only-secret",
            2.0,
        )
        transport._api_url = f"{origin}/api_jsonrpc.php"
        with pytest.raises(ApplicationError) as caught:
            asyncio.run(transport.call("host.get", {}))

    assert caught.value.code is ErrorCode.DEPENDENCY_UNAVAILABLE
    assert seen_paths == ["/api_jsonrpc.php"]
