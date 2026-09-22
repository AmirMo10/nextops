"""Strict loaders for secrets supplied at the deployment boundary."""

from __future__ import annotations

import os
import stat
from pathlib import Path


def deployment_secret(
    *,
    value_variable: str,
    file_variable: str,
    credential_name: str,
) -> str:
    """Load one secret from an environment value or protected credential file."""

    direct_value = os.environ.get(value_variable)
    explicit_path = os.environ.get(file_variable)
    credentials_directory = os.environ.get("CREDENTIALS_DIRECTORY")

    if direct_value is not None and (explicit_path or credentials_directory):
        raise ValueError(
            f"{value_variable} cannot be combined with file-backed deployment credentials"
        )
    if direct_value is not None:
        return direct_value
    if explicit_path:
        return _read_secret_file(Path(explicit_path), file_variable)
    if credentials_directory:
        return _read_secret_file(
            Path(credentials_directory) / credential_name,
            "CREDENTIALS_DIRECTORY",
        )
    return ""


def _read_secret_file(path: Path, source: str) -> str:
    if not path.is_absolute():
        raise ValueError(f"{source} must resolve to an absolute path")

    try:
        metadata = path.lstat()
    except OSError as error:
        raise ValueError(f"unable to read the credential referenced by {source}") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise ValueError(f"{source} must reference a regular file, not a symlink")
    if os.name == "posix" and (metadata.st_mode & stat.S_IROTH or metadata.st_mode & stat.S_IWOTH):
        raise ValueError(f"the credential referenced by {source} must not be world-accessible")
    if metadata.st_size > 4_096:
        raise ValueError(f"the credential referenced by {source} exceeds 4096 bytes")

    try:
        value = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ValueError(f"unable to read the credential referenced by {source}") from error
    normalized = value.removesuffix("\n").removesuffix("\r")
    if (
        not normalized
        or normalized != normalized.strip()
        or "\n" in normalized
        or "\r" in normalized
    ):
        raise ValueError(f"the credential referenced by {source} must contain one non-empty line")
    return normalized
