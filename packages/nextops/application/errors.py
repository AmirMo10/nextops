"""Typed application failures mapped consistently by outer interfaces."""

from typing import Any

from nextops.contracts.errors import ErrorCode


class ApplicationError(Exception):
    """Expected failure safe to translate without exposing raw exceptions."""

    def __init__(
        self,
        code: ErrorCode,
        message_key: str,
        *,
        retryable: bool = False,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message_key)
        self.code = code
        self.message_key = message_key
        self.retryable = retryable
        self.details = details or {}
