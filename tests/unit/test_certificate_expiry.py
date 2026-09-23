"""Deterministic certificate-lifecycle checker tests."""

import sys
from datetime import UTC, datetime
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT))

from scripts.check_certificate_expiry import (  # noqa: E402
    CertificateCheckError,
    parse_openssl_output,
)

NOW = datetime(2026, 9, 23, 12, 0, tzinfo=UTC)
FINGERPRINT = ":".join(["AB"] * 32)


def output(*, not_before: str, not_after: str) -> str:
    return f"notBefore={not_before}\nnotAfter={not_after}\nsha256 Fingerprint={FINGERPRINT}\n"


@pytest.mark.parametrize(
    ("not_before", "not_after", "expected"),
    [
        ("Sep 22 12:00:00 2026 GMT", "Oct 24 12:00:00 2027 GMT", "healthy"),
        ("Sep 22 12:00:00 2026 GMT", "Oct 20 12:00:00 2026 GMT", "expiring"),
        ("Sep 22 12:00:00 2025 GMT", "Sep 22 12:00:00 2026 GMT", "expired"),
        ("Sep 24 12:00:00 2026 GMT", "Oct 24 12:00:00 2027 GMT", "not_yet_valid"),
    ],
)
def test_certificate_states_are_time_bounded(
    not_before: str,
    not_after: str,
    expected: str,
) -> None:
    result = parse_openssl_output(
        output(not_before=not_before, not_after=not_after),
        label="nextops-app",
        warning_days=30,
        checked_at=NOW,
    )

    assert result.status == expected
    assert result.fingerprint_sha256 == "AB" * 32
    assert result.checked_at == "2026-09-23T12:00:00+00:00"


@pytest.mark.parametrize(
    "label",
    ["", "contains space", "../escape", "a" * 65],
)
def test_certificate_label_is_bounded(label: str) -> None:
    with pytest.raises(CertificateCheckError, match="label"):
        parse_openssl_output(
            output(
                not_before="Sep 22 12:00:00 2026 GMT",
                not_after="Oct 24 12:00:00 2027 GMT",
            ),
            label=label,
            warning_days=30,
            checked_at=NOW,
        )


@pytest.mark.parametrize("warning_days", [0, 3651])
def test_warning_window_is_bounded(warning_days: int) -> None:
    with pytest.raises(CertificateCheckError, match="warning days"):
        parse_openssl_output(
            output(
                not_before="Sep 22 12:00:00 2026 GMT",
                not_after="Oct 24 12:00:00 2027 GMT",
            ),
            label="nextops-app",
            warning_days=warning_days,
            checked_at=NOW,
        )


@pytest.mark.parametrize(
    "certificate_output",
    [
        "notBefore=Sep 22 12:00:00 2026 GMT\n",
        f"notBefore=invalid\nnotAfter=Oct 24 12:00:00 2027 GMT\nsha256 Fingerprint={FINGERPRINT}\n",
        "notBefore=Sep 22 12:00:00 2026 GMT\n"
        "notAfter=Oct 24 12:00:00 2027 GMT\nsha256 Fingerprint=invalid\n",
    ],
)
def test_invalid_metadata_fails_closed(certificate_output: str) -> None:
    with pytest.raises(CertificateCheckError):
        parse_openssl_output(
            certificate_output,
            label="nextops-app",
            warning_days=30,
            checked_at=NOW,
        )
