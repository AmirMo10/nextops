"""Run bounded Stage 1B API checks without printing deployment credentials."""

from __future__ import annotations

import argparse
import json
import os
import stat
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import ProxyHandler, Request, build_opener
from uuid import uuid4

ROOT = Path(__file__).parents[1]
DEFAULT_CORPUS = ROOT / "deploy" / "inference" / "stage1b-evaluation-v1.json"
MAX_RESPONSE_BYTES = 1_048_576


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run synthetic bilingual/authentication checks against the loopback Stage 1B API. "
            "The JSON output belongs in the approved private evidence record, not Git."
        )
    )
    parser.add_argument("--base-url", default="http://127.0.0.1:8090")
    parser.add_argument("--secret-file", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS)
    parser.add_argument("--timeout-seconds", type=float, default=180.0)
    parser.add_argument("--skip-load", action="store_true")
    return parser.parse_args()


def validate_loopback_origin(value: str) -> str:
    parsed = urlsplit(value)
    valid = (
        parsed.scheme == "http"
        and parsed.hostname == "127.0.0.1"
        and parsed.port is not None
        and parsed.path in ("", "/")
        and not parsed.query
        and not parsed.fragment
        and parsed.username is None
        and parsed.password is None
    )
    if not valid:
        raise ValueError("base URL must be an undecorated http://127.0.0.1:<port> origin")
    return value.rstrip("/")


def read_secret(path: Path) -> str:
    if not path.is_absolute():
        raise ValueError("secret file must be an absolute regular path and not a symlink")
    metadata = path.lstat()
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise ValueError("secret file must be an absolute regular path and not a symlink")
    if os.name == "posix" and (metadata.st_mode & stat.S_IROTH or metadata.st_mode & stat.S_IWOTH):
        raise ValueError("secret file must not be world-accessible")
    if metadata.st_size > 4_096:
        raise ValueError("secret file exceeds 4096 bytes")
    value = path.read_text(encoding="utf-8").removesuffix("\n").removesuffix("\r")
    if not value or value != value.strip() or "\n" in value or "\r" in value:
        raise ValueError("secret file must contain one non-empty line")
    return value


def write_private_report(path: Path, report: dict[str, Any]) -> None:
    """Write evidence with a private mode and without following a final symlink."""

    if not path.is_absolute():
        raise ValueError("output path must be absolute")
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags, 0o600)
    try:
        if os.name == "posix":
            os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as output:
            descriptor = -1
            json.dump(report, output, ensure_ascii=False, indent=2)
            output.write("\n")
    finally:
        if descriptor >= 0:
            os.close(descriptor)


class LoopbackClient:
    def __init__(self, base_url: str, secret: str, timeout_seconds: float) -> None:
        self.base_url = validate_loopback_origin(base_url)
        self.secret = secret
        self.timeout_seconds = timeout_seconds
        self.opener = build_opener(ProxyHandler({}))

    def request(
        self,
        method: str,
        path: str,
        *,
        payload: dict[str, Any] | None = None,
        authenticated: bool = True,
    ) -> dict[str, Any]:
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if authenticated:
            headers["Authorization"] = f"Bearer {self.secret}"
        body = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
        request = Request(f"{self.base_url}{path}", data=body, headers=headers, method=method)
        started = time.monotonic()
        try:
            with self.opener.open(request, timeout=self.timeout_seconds) as response:
                status = response.status
                raw = response.read(MAX_RESPONSE_BYTES + 1)
        except HTTPError as error:
            status = error.code
            raw = error.read(MAX_RESPONSE_BYTES + 1)
        except (URLError, TimeoutError, OSError) as error:
            return {
                "status": 0,
                "elapsed_ms": round((time.monotonic() - started) * 1_000),
                "transport_error": type(error).__name__,
            }
        if len(raw) > MAX_RESPONSE_BYTES:
            raise ValueError("response exceeded the one-megabyte evaluation limit")
        try:
            decoded: Any = json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError):
            decoded = {"invalid_json": True}
        return {
            "status": status,
            "elapsed_ms": round((time.monotonic() - started) * 1_000),
            "body": decoded,
        }


def generation_payload(case: dict[str, Any]) -> dict[str, Any]:
    return {
        "request_id": str(uuid4()),
        "locale": case["locale"],
        "prompt": case["prompt"],
        "max_output_tokens": 192,
        "temperature": 0.1,
    }


def main() -> int:
    args = parse_args()
    client = LoopbackClient(args.base_url, read_secret(args.secret_file), args.timeout_seconds)
    corpus = json.loads(args.corpus.read_text(encoding="utf-8"))
    cases = corpus["cases"]

    report: dict[str, Any] = {
        "schema_version": "1.0.0",
        "corpus_id": corpus["corpus_id"],
        "started_at": datetime.now(UTC).isoformat(),
        "base_url": client.base_url,
        "authentication": {},
        "readiness": {},
        "quality_cases": [],
        "load_probe": {"status": "not_run"},
        "quality_review_status": "manual_review_required",
        "acceptance_claimed": False,
    }

    denied_case = cases[0]
    report["authentication"] = client.request(
        "POST",
        "/api/v1/generate",
        payload=generation_payload(denied_case),
        authenticated=False,
    )
    report["readiness"] = client.request("GET", "/readyz")

    for case in cases:
        result = client.request(
            "POST",
            "/api/v1/generate",
            payload=generation_payload(case),
        )
        report["quality_cases"].append(
            {
                "id": case["id"],
                "locale": case["locale"],
                "review": case["review"],
                "result": result,
            }
        )

    if not args.skip_load:
        load_cases = [cases[index % len(cases)] for index in range(4)]
        results: list[dict[str, Any]] = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(
                    client.request,
                    "POST",
                    "/api/v1/generate",
                    payload=generation_payload(case),
                )
                for case in load_cases
            ]
            for future in as_completed(futures):
                results.append(future.result())
        report["load_probe"] = {
            "status": "completed",
            "request_count": len(results),
            "http_status_counts": {
                str(status): sum(1 for item in results if item.get("status") == status)
                for status in sorted({int(item.get("status", 0)) for item in results})
            },
            "results": results,
        }

    automated = (
        report["authentication"].get("status") == 401
        and report["readiness"].get("status") == 200
        and all(item["result"].get("status") == 200 for item in report["quality_cases"])
    )
    report["automated_boundary_checks_passed"] = automated
    report["completed_at"] = datetime.now(UTC).isoformat()

    write_private_report(args.output, report)
    return 0 if automated else 1


if __name__ == "__main__":
    raise SystemExit(main())
