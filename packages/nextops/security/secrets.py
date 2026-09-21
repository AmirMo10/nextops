"""Password and opaque-token handling with no plaintext persistence."""

from hashlib import sha256
from secrets import compare_digest, token_urlsafe

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError


class PasswordService:
    """Hash local passwords with an explicit Argon2id cost profile."""

    def __init__(self) -> None:
        self._hasher = PasswordHasher(
            time_cost=3,
            memory_cost=65_536,
            parallelism=4,
            hash_len=32,
            salt_len=16,
        )

    def hash(self, password: str) -> str:
        """Return a salted Argon2id PHC string."""

        return self._hasher.hash(password)

    def verify(self, stored_hash: str, supplied_password: str) -> bool:
        """Verify without exposing library-specific failures to callers."""

        try:
            return self._hasher.verify(stored_hash, supplied_password)
        except (InvalidHashError, VerificationError):
            return False

    def needs_rehash(self, stored_hash: str) -> bool:
        """Report whether a successful login should refresh cost parameters."""

        try:
            return self._hasher.check_needs_rehash(stored_hash)
        except InvalidHashError:
            return True


def issue_opaque_token() -> str:
    """Generate a 384-bit URL-safe bearer or lease token."""

    return token_urlsafe(48)


def hash_opaque_token(token: str) -> str:
    """Return the fixed-length storage/index representation of an opaque token."""

    return sha256(token.encode("utf-8")).hexdigest()


def verify_deployment_secret(configured: str, supplied: str) -> bool:
    """Compare deployment secrets without data-dependent early string comparison."""

    if not configured or not supplied:
        return False
    configured_digest = sha256(configured.encode("utf-8")).digest()
    supplied_digest = sha256(supplied.encode("utf-8")).digest()
    return compare_digest(configured_digest, supplied_digest)
