"""Security primitive tests for local identity and opaque sessions."""

from nextops.security.secrets import (
    PasswordService,
    hash_opaque_token,
    issue_opaque_token,
    verify_deployment_secret,
)


def test_password_hash_is_memory_hard_salted_and_verifiable() -> None:
    passwords = PasswordService()

    first = passwords.hash("correct horse battery staple")
    second = passwords.hash("correct horse battery staple")

    assert first.startswith("$argon2id$")
    assert first != second
    assert passwords.verify(first, "correct horse battery staple") is True
    assert passwords.verify(first, "wrong horse battery staple") is False


def test_opaque_session_token_is_returned_separately_from_its_storage_hash() -> None:
    token = issue_opaque_token()
    digest = hash_opaque_token(token)

    assert len(token) >= 32
    assert len(digest) == 64
    assert token not in digest
    assert hash_opaque_token(token) == digest


def test_deployment_secret_comparison_accepts_only_exact_value() -> None:
    assert verify_deployment_secret("configured-secret", "configured-secret") is True
    assert verify_deployment_secret("configured-secret", "configured-secreu") is False
    assert verify_deployment_secret("configured-secret", "") is False
