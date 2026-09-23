"""Bounded contracts for direct read-only Linux diagnostics."""

from __future__ import annotations

from typing import Annotated, Literal, Self

from pydantic import AwareDatetime, Field, model_validator

from nextops.contracts.models import FrozenContract

LinuxTargetId = Annotated[str, Field(pattern=r"^[a-z][a-z0-9-]{1,31}$")]
LinuxPartialReason = Literal[
    "filesystems_truncated",
    "processes_truncated",
    "services_truncated",
    "journals_truncated",
    "journals_unavailable",
    "packages_unavailable",
    "sessions_unavailable",
    "sockets_truncated",
    "routes_truncated",
]


class LinuxFilesystem(FrozenContract):
    """One configured filesystem observation."""

    path: str = Field(min_length=1, max_length=256)
    total_bytes: int = Field(ge=0)
    available_bytes: int = Field(ge=0)
    used_percent: float = Field(ge=0.0, le=100.0)


class LinuxProcess(FrozenContract):
    """One high-RSS process without command-line arguments."""

    pid: int = Field(ge=1)
    name: str = Field(min_length=1, max_length=128)
    rss_bytes: int = Field(ge=0)


class LinuxService(FrozenContract):
    """One deployment-allowlisted systemd unit state."""

    unit: str = Field(pattern=r"^[A-Za-z0-9@_.:-]{1,128}\.service$")
    load_state: Literal["loaded", "not-found", "masked", "error"]
    active_state: str = Field(min_length=1, max_length=32)
    sub_state: str = Field(min_length=1, max_length=32)


class LinuxJournalEntry(FrozenContract):
    """One bounded, redacted high-priority journal observation."""

    unit: str = Field(min_length=1, max_length=128)
    priority: int = Field(ge=0, le=7)
    observed_at: AwareDatetime
    message: str = Field(min_length=1, max_length=512)


class LinuxListeningSocket(FrozenContract):
    """One listening TCP socket from procfs."""

    family: Literal["ipv4", "ipv6"]
    address: str = Field(min_length=1, max_length=64)
    port: int = Field(ge=1, le=65_535)


class LinuxRoute(FrozenContract):
    """One kernel IPv4 route without neighbor or credential data."""

    interface: str = Field(pattern=r"^[A-Za-z0-9_.:-]{1,32}$")
    destination: str = Field(min_length=1, max_length=64)
    gateway: str = Field(min_length=1, max_length=64)


class LinuxDiagnosticSnapshot(FrozenContract):
    """A single bounded Linux snapshot produced by the forced-command collector."""

    source: Literal["linux"] = "linux"
    collector_version: Literal["1.0.0"] = "1.0.0"
    target_id: LinuxTargetId
    hostname: str = Field(min_length=1, max_length=128)
    operating_system: str = Field(min_length=1, max_length=256)
    collected_at: AwareDatetime
    uptime_seconds: int = Field(ge=0)
    logical_cpu_count: int = Field(ge=1, le=4_096)
    load_1m: float = Field(ge=0.0)
    load_5m: float = Field(ge=0.0)
    load_15m: float = Field(ge=0.0)
    memory_total_bytes: int = Field(ge=1)
    memory_available_bytes: int = Field(ge=0)
    swap_total_bytes: int = Field(ge=0)
    swap_free_bytes: int = Field(ge=0)
    filesystems: tuple[LinuxFilesystem, ...] = Field(max_length=8)
    processes: tuple[LinuxProcess, ...] = Field(max_length=10)
    services: tuple[LinuxService, ...] = Field(max_length=16)
    journal: tuple[LinuxJournalEntry, ...] = Field(max_length=25)
    local_user_count: int = Field(ge=0)
    logged_in_user_count: int = Field(ge=0)
    installed_package_count: int = Field(ge=0)
    listening_sockets: tuple[LinuxListeningSocket, ...] = Field(max_length=32)
    routes: tuple[LinuxRoute, ...] = Field(max_length=16)
    nameservers: tuple[str, ...] = Field(max_length=4)
    is_partial: bool = False
    partial_reasons: tuple[LinuxPartialReason, ...] = Field(default_factory=tuple, max_length=9)

    @model_validator(mode="after")
    def validate_snapshot(self) -> Self:
        if self.memory_available_bytes > self.memory_total_bytes:
            raise ValueError("available memory exceeds total memory")
        if self.swap_free_bytes > self.swap_total_bytes:
            raise ValueError("free swap exceeds total swap")
        if self.is_partial != bool(self.partial_reasons):
            raise ValueError("is_partial must match partial_reasons")
        if len(set(self.partial_reasons)) != len(self.partial_reasons):
            raise ValueError("partial reasons must be unique")
        return self
