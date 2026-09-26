#!/usr/bin/env python3
"""Capture bounded, authenticated app answers for private human semantic review."""

from __future__ import annotations

import argparse
import ipaddress
import json
import os
import re
import ssl
import stat
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import (
    HTTPRedirectHandler,
    HTTPSHandler,
    ProxyHandler,
    Request,
    build_opener,
)

MAX_CASES = 12
MAX_RESPONSE_BYTES = 1_048_576
ROUTES = {
    "general": "/api/v1/assistant/generate",
    "monitoring": "/api/v1/investigate",
    "incident": "/api/v1/incidents/investigate",
}
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


class NoRedirect(HTTPRedirectHandler):
    """Never forward a credential to a redirect target."""

    def redirect_request(self, *_args: Any, **_kwargs: Any) -> None:
        return None


def read_private_text(path: Path, *, max_bytes: int) -> str:
    if not path.is_absolute():
        raise ValueError("private input path must be absolute")
    metadata = path.lstat()
    if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > max_bytes:
        raise ValueError("private input must be a bounded regular file")
    if os.name == "posix" and metadata.st_mode & 0o077:
        raise ValueError("private input must be owner-readable only")
    return path.read_text(encoding="utf-8-sig")


def fields(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in text.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            normalized = key.strip().casefold()
            if normalized in values:
                raise ValueError("private input has a duplicate field")
            values[normalized] = value.strip()
    return values


def validate_private_https_origin(value: str) -> str:
    parsed = urlsplit(value)
    hostname = parsed.hostname
    if (
        parsed.scheme != "https"
        or not hostname
        or parsed.path not in ("", "/")
        or parsed.query
        or parsed.fragment
        or parsed.username
        or parsed.password
    ):
        raise ValueError("endpoint must be an undecorated HTTPS origin")
    try:
        address = ipaddress.ip_address(hostname)
        private_host = (
            address.is_private and not address.is_unspecified and not address.is_multicast
        )
    except ValueError:
        private_host = hostname.casefold().endswith((".local", ".lan", ".internal"))
    if not private_host:
        raise ValueError("endpoint must be on a private network")
    return value.rstrip("/")


def validate_cases(data: Any) -> list[dict[str, str]]:
    if not isinstance(data, dict) or not isinstance(data.get("cases"), list):
        raise ValueError("corpus must contain a cases array")
    raw_cases = data["cases"]
    if not 1 <= len(raw_cases) <= MAX_CASES:
        raise ValueError("corpus case count is outside the bounded range")
    cases: list[dict[str, str]] = []
    for item in raw_cases:
        if not isinstance(item, dict):
            raise ValueError("every case must be a mapping")
        case_id, mode, locale, question = (
            item.get("id"),
            item.get("mode"),
            item.get("locale"),
            item.get("question"),
        )
        if (
            not isinstance(case_id, str)
            or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", case_id) is None
            or not isinstance(mode, str)
            or mode not in ROUTES
            or locale not in ("en", "fa")
            or not isinstance(question, str)
            or not 1 <= len(question.strip()) <= 4_000
        ):
            raise ValueError("case has an invalid ID, mode, locale, or question")
        target_id = item.get("target_id", "")
        if not isinstance(target_id, str):
            raise ValueError("case target ID must be text")
        if mode == "incident":
            if re.fullmatch(r"[a-z][a-z0-9-]{1,31}", target_id) is None:
                raise ValueError("incident case requires a bounded target ID")
        elif target_id:
            raise ValueError("only incident cases may specify a target ID")
        cases.append(
            {
                "id": case_id,
                "mode": mode,
                "locale": locale,
                "question": question,
                "target_id": target_id,
            }
        )
    if len({case["id"] for case in cases}) != len(cases):
        raise ValueError("case IDs must be unique")
    return cases


def validate_report_location(path: Path) -> None:
    if not path.is_absolute() or not path.parent.is_dir():
        raise ValueError("report path must be absolute with an existing private parent")
    resolved_parent = path.parent.resolve()
    if resolved_parent == REPOSITORY_ROOT or REPOSITORY_ROOT in resolved_parent.parents:
        raise ValueError("report must be outside the repository")
    if os.name == "posix" and resolved_parent.stat().st_mode & 0o077:
        raise ValueError("report parent must be owner-accessible only")
    if path.exists() or path.is_symlink():
        raise FileExistsError("report path already exists")


def write_private_report(path: Path, report: dict[str, Any]) -> None:
    validate_report_location(path)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags, 0o600)
    try:
        if os.name == "posix":
            fchmod = getattr(os, "fchmod", None)
            if fchmod is None:
                raise OSError("POSIX runtime does not expose fchmod")
            fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as output:
            descriptor = -1
            json.dump(report, output, ensure_ascii=False, indent=2)
            output.write("\n")
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--endpoint-file", required=True, type=Path)
    parser.add_argument("--login-file", required=True, type=Path)
    parser.add_argument("--ca-file", required=True, type=Path)
    parser.add_argument("--corpus", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--expected-release", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    validate_report_location(args.output)
    endpoint = fields(read_private_text(args.endpoint_file, max_bytes=4_096)).get("url", "")
    origin = validate_private_https_origin(endpoint)
    login = fields(read_private_text(args.login_file, max_bytes=4_096))
    if not login.get("username") or len(login.get("password", "")) < 32:
        raise ValueError("protected login file is incomplete")
    corpus = json.loads(read_private_text(args.corpus, max_bytes=64_000))
    cases = validate_cases(corpus)
    context = ssl.create_default_context(cafile=str(args.ca_file))
    opener = build_opener(ProxyHandler({}), HTTPSHandler(context=context), NoRedirect())

    def call(path: str, payload: dict[str, str], token: str = "") -> dict[str, Any]:
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        request = Request(
            origin + path,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        started = time.monotonic()
        try:
            with opener.open(request, timeout=120) as response:
                status = response.status
                raw = response.read(MAX_RESPONSE_BYTES + 1)
        except HTTPError as error:
            status = error.code
            raw = error.read(MAX_RESPONSE_BYTES + 1)
        except (URLError, TimeoutError, OSError):
            return {"status": 0, "error": "transport_failure"}
        if len(raw) > MAX_RESPONSE_BYTES:
            return {"status": status, "error": "response_too_large"}
        try:
            body: Any = json.loads(raw) if raw else None
        except (UnicodeDecodeError, json.JSONDecodeError):
            body = None
        return {
            "status": status,
            "elapsed_ms": round((time.monotonic() - started) * 1_000),
            "body": body,
        }

    report: dict[str, Any] = {
        "started_at": datetime.now(UTC).isoformat(),
        "expected_release_owner_assertion": args.expected_release,
        "release_identity_verified_by_this_script": False,
        "manual_semantic_review_required": True,
        "acceptance_claimed": False,
        "cases": [],
        "logout_status": "not_run",
    }
    token = ""
    completed = False
    try:
        session = call(
            "/api/v1/login",
            {"username": login["username"], "password": login["password"]},
        )
        session_body = session.get("body")
        if session.get("status") != 200 or not isinstance(session_body, dict):
            report["login_status"] = session.get("status")
        else:
            session_data = session_body.get("session")
            token = (
                str(session_data.get("access_token", "")) if isinstance(session_data, dict) else ""
            )
            if len(token) < 32:
                report["login_status"] = "invalid_session"
            else:
                report["login_status"] = 200
                for case in cases:
                    payload = {"locale": case["locale"], "question": case["question"]}
                    if case["mode"] == "incident":
                        payload["target_id"] = case["target_id"]
                    result = call(ROUTES[case["mode"]], payload, token)
                    report["cases"].append({"case": case, "result": result})
                completed = all(item["result"].get("status") == 200 for item in report["cases"])
    finally:
        if token:
            report["logout_status"] = call("/api/v1/logout", {}, token).get("status")
        report["completed_at"] = datetime.now(UTC).isoformat()
        write_private_report(args.output, report)
        print(f"cases_recorded={len(report['cases'])}; review=required; report={args.output}")
    return 0 if completed and report["logout_status"] == 204 else 1


if __name__ == "__main__":
    raise SystemExit(main())
