#!/usr/bin/env python3
"""Check one local X.509 certificate without reading its private key."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

LABEL_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}\Z")
FINGERPRINT_PATTERN = re.compile(r"[0-9A-F]{64}\Z")
OPENSSL_TIME_FORMAT = "%b %d %H:%M:%S %Y GMT"
MIN_WARNING_DAYS = 1
MAX_WARNING_DAYS = 3650
MAX_CERTIFICATE_BYTES = 1024 * 1024


class CertificateCheckError(RuntimeError):
    """Raised when the checker cannot establish a trustworthy certificate state."""


@dataclass(frozen=True)
class CertificateStatus:
    label: str
    status: str
    checked_at: str
    valid_from: str
    valid_until: str
    seconds_remaining: int
    warning_days: int
    fingerprint_sha256: str


def _parse_openssl_time(value: str) -> datetime:
    try:
        return datetime.strptime(value, OPENSSL_TIME_FORMAT).replace(tzinfo=UTC)
    except ValueError as exc:
        raise CertificateCheckError("OpenSSL returned an invalid certificate timestamp") from exc


def parse_openssl_output(
    output: str,
    *,
    label: str,
    warning_days: int,
    checked_at: datetime,
) -> CertificateStatus:
    """Turn bounded OpenSSL metadata into a deterministic lifecycle state."""
    if checked_at.tzinfo is None or checked_at.utcoffset() is None:
        raise CertificateCheckError("the supplied check time must be timezone-aware")
    if not LABEL_PATTERN.fullmatch(label):
        raise CertificateCheckError("certificate label is invalid")
    if not MIN_WARNING_DAYS <= warning_days <= MAX_WARNING_DAYS:
        raise CertificateCheckError("warning days are outside the supported range")

    fields: dict[str, str] = {}
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        fields[key.strip()] = value.strip()

    try:
        valid_from = _parse_openssl_time(fields["notBefore"])
        valid_until = _parse_openssl_time(fields["notAfter"])
        fingerprint = fields["sha256 Fingerprint"].replace(":", "").upper()
    except KeyError as exc:
        raise CertificateCheckError("OpenSSL certificate metadata is incomplete") from exc
    if not FINGERPRINT_PATTERN.fullmatch(fingerprint):
        raise CertificateCheckError("OpenSSL returned an invalid SHA-256 fingerprint")
    if valid_until <= valid_from:
        raise CertificateCheckError("certificate validity interval is invalid")

    checked_at = checked_at.astimezone(UTC)
    seconds_remaining = int((valid_until - checked_at).total_seconds())
    warning_seconds = warning_days * 24 * 60 * 60
    if checked_at < valid_from:
        state = "not_yet_valid"
    elif seconds_remaining <= 0:
        state = "expired"
    elif seconds_remaining <= warning_seconds:
        state = "expiring"
    else:
        state = "healthy"

    return CertificateStatus(
        label=label,
        status=state,
        checked_at=checked_at.isoformat(),
        valid_from=valid_from.isoformat(),
        valid_until=valid_until.isoformat(),
        seconds_remaining=seconds_remaining,
        warning_days=warning_days,
        fingerprint_sha256=fingerprint,
    )


def inspect_certificate(
    certificate: Path,
    *,
    label: str,
    warning_days: int,
    checked_at: datetime | None = None,
    openssl_binary: Path = Path("/usr/bin/openssl"),
) -> CertificateStatus:
    """Read public metadata from one local PEM certificate with a bounded process."""
    if not certificate.is_absolute():
        raise CertificateCheckError("certificate path must be absolute")
    try:
        if certificate.is_symlink() or not certificate.is_file():
            raise CertificateCheckError("certificate file is unavailable")
        certificate_stat = certificate.stat()
    except OSError as exc:
        raise CertificateCheckError("certificate file is unavailable") from exc
    if not 0 < certificate_stat.st_size <= MAX_CERTIFICATE_BYTES:
        raise CertificateCheckError("certificate file size is invalid")
    if certificate_stat.st_uid != 0 or certificate_stat.st_mode & 0o022:
        raise CertificateCheckError("certificate file ownership or mode is unsafe")
    try:
        if (
            not openssl_binary.is_absolute()
            or openssl_binary.is_symlink()
            or not openssl_binary.is_file()
        ):
            raise CertificateCheckError("the pinned OpenSSL binary is unavailable")
        openssl_stat = openssl_binary.stat()
    except OSError as exc:
        raise CertificateCheckError("the pinned OpenSSL binary is unavailable") from exc
    if openssl_stat.st_uid != 0 or openssl_stat.st_mode & 0o022:
        raise CertificateCheckError("the pinned OpenSSL binary is unsafe")

    try:
        process = subprocess.run(
            [
                str(openssl_binary),
                "x509",
                "-in",
                str(certificate),
                "-noout",
                "-dates",
                "-fingerprint",
                "-sha256",
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
            env={"PATH": "/usr/bin:/bin", "LC_ALL": "C", "TZ": "UTC"},
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CertificateCheckError("OpenSSL certificate inspection failed") from exc
    if process.returncode != 0 or len(process.stdout) > 4096:
        raise CertificateCheckError("OpenSSL rejected the certificate")

    return parse_openssl_output(
        process.stdout,
        label=label,
        warning_days=warning_days,
        checked_at=checked_at or datetime.now(UTC),
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", required=True, type=Path)
    parser.add_argument("--label", required=True)
    parser.add_argument("--warning-days", required=True, type=int)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = inspect_certificate(
            args.certificate,
            label=args.label,
            warning_days=args.warning_days,
        )
    except CertificateCheckError as exc:
        print(
            json.dumps(
                {"status": "error", "error": str(exc)},
                ensure_ascii=True,
                sort_keys=True,
            )
        )
        return 2

    print(json.dumps(asdict(result), ensure_ascii=True, sort_keys=True))
    return 0 if result.status == "healthy" else 1


if __name__ == "__main__":
    sys.exit(main())
