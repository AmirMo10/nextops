"""Stable domain enumerations shared by contracts and policy."""

from enum import StrEnum


class RiskClass(StrEnum):
    """Risk assigned by trusted, versioned policy rather than request text."""

    READ_ONLY = "READ_ONLY"
    LOW_RISK = "LOW_RISK"
    MEDIUM_RISK = "MEDIUM_RISK"
    HIGH_RISK = "HIGH_RISK"
    CRITICAL = "CRITICAL"
