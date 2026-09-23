"""Strict SSH transport and target registry for read-only Linux diagnostics."""

from __future__ import annotations

import asyncio
import contextlib
import ipaddress
import json
import re
from pathlib import Path
from typing import Any, Protocol, Self

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from nextops.application.errors import ApplicationError
from nextops.connectors.zabbix import ZabbixReadClient, ZabbixTransport
from nextops.contracts.errors import ErrorCode
from nextops.contracts.incidents import IncidentEvidence
from nextops.contracts.linux import LinuxDiagnosticSnapshot, LinuxTargetId

MAX_LINUX_RESPONSE_BYTES = 131_072
MAX_TARGET_CONFIG_BYTES = 65_536
SSH_COMMAND = "nextops-linux-snapshot-v1"
SSH_DESTINATION_PATTERN = re.compile(r"^nextops-linux-ro@([A-Za-z0-9.-]{1,253})$")


class LinuxTarget(BaseModel):
    """One deployment-owned diagnostic target without a caller-controlled address."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    target_id: LinuxTargetId
    display_name: str = Field(min_length=1, max_length=128)
    zabbix_host: str = Field(min_length=1, max_length=128)
    ssh_destination: str = Field(min_length=1, max_length=320)
    identity_file: Path

    @model_validator(mode="after")
    def validate_target(self) -> Self:
        matched = SSH_DESTINATION_PATTERN.fullmatch(self.ssh_destination)
        if matched is None:
            raise ValueError("SSH destination must use the nextops-linux-ro identity")
        host = matched.group(1)
        try:
            address = ipaddress.ip_address(host)
        except ValueError:
            if host.startswith("-") or host.endswith("-") or ".." in host:
                raise ValueError("SSH destination host is invalid") from None
        else:
            if not address.is_private:
                raise ValueError("SSH destination address must be private")
        if not self.identity_file.is_absolute() or not self.identity_file.is_file():
            raise ValueError("identity_file must be an existing absolute file")
        return self


class LinuxTargetRegistry(BaseModel):
    """Immutable deployment configuration for every approved Linux target."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: str
    known_hosts_file: Path
    targets: tuple[LinuxTarget, ...] = Field(min_length=1, max_length=8)

    @model_validator(mode="after")
    def validate_registry(self) -> Self:
        if self.schema_version != "1.0.0":
            raise ValueError("unsupported Linux target registry version")
        if not self.known_hosts_file.is_absolute() or not self.known_hosts_file.is_file():
            raise ValueError("known_hosts_file must be an existing absolute file")
        target_ids = [target.target_id for target in self.targets]
        if len(set(target_ids)) != len(target_ids):
            raise ValueError("Linux target ids must be unique")
        destinations = [target.ssh_destination for target in self.targets]
        if len(set(destinations)) != len(destinations):
            raise ValueError("Linux SSH destinations must be unique")
        return self

    @classmethod
    def from_file(cls, path: Path) -> LinuxTargetRegistry:
        if not path.is_absolute() or not path.is_file():
            raise ValueError("Linux target registry must be an existing absolute file")
        raw = path.read_bytes()
        if len(raw) > MAX_TARGET_CONFIG_BYTES:
            raise ValueError("Linux target registry is too large")
        try:
            decoded = json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError("Linux target registry is invalid JSON") from error
        return cls.model_validate(decoded)

    def resolve(self, target_id: str) -> LinuxTarget:
        for target in self.targets:
            if target.target_id == target_id:
                return target
        raise ApplicationError(ErrorCode.POLICY_DENIED, "connector.linux_target_denied")


class LinuxTransport(Protocol):
    """Replaceable bounded Linux transport."""

    async def collect(self, target: LinuxTarget) -> dict[str, Any]: ...


class SshLinuxTransport:
    """Execute one fixed remote command with a dedicated key and pinned host identity."""

    def __init__(self, known_hosts_file: Path, timeout_seconds: float = 15.0) -> None:
        self._known_hosts_file = known_hosts_file
        self._timeout_seconds = timeout_seconds

    async def collect(self, target: LinuxTarget) -> dict[str, Any]:
        process: asyncio.subprocess.Process | None = None
        try:
            process = await asyncio.create_subprocess_exec(
                "/usr/bin/ssh",
                "-T",
                "-o",
                "BatchMode=yes",
                "-o",
                "IdentitiesOnly=yes",
                "-o",
                "StrictHostKeyChecking=yes",
                "-o",
                f"UserKnownHostsFile={self._known_hosts_file}",
                "-o",
                "ConnectTimeout=5",
                "-o",
                "ServerAliveInterval=5",
                "-o",
                "ServerAliveCountMax=1",
                "-o",
                "LogLevel=ERROR",
                "-i",
                str(target.identity_file),
                target.ssh_destination,
                SSH_COMMAND,
                stdin=asyncio.subprocess.DEVNULL,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.DEVNULL,
            )
            raw = await asyncio.wait_for(self._read_process(process), self._timeout_seconds)
        except TimeoutError as error:
            if process is not None:
                with contextlib.suppress(ProcessLookupError):
                    process.kill()
                await process.wait()
            raise ApplicationError(
                ErrorCode.TIMEOUT,
                "connector.linux_timeout",
                retryable=True,
            ) from error
        except OSError as error:
            raise ApplicationError(
                ErrorCode.DEPENDENCY_UNAVAILABLE,
                "connector.linux_unavailable",
                retryable=True,
            ) from error
        if len(raw) > MAX_LINUX_RESPONSE_BYTES:
            raise ApplicationError(
                ErrorCode.DEPENDENCY_UNAVAILABLE,
                "connector.linux_response_too_large",
                retryable=True,
            )
        try:
            decoded = json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ApplicationError(
                ErrorCode.DEPENDENCY_UNAVAILABLE,
                "connector.linux_response_invalid",
                retryable=True,
            ) from error
        if not isinstance(decoded, dict):
            raise ApplicationError(
                ErrorCode.DEPENDENCY_UNAVAILABLE,
                "connector.linux_response_invalid",
                retryable=True,
            )
        return decoded

    @staticmethod
    async def _read_process(process: asyncio.subprocess.Process) -> bytes:
        if process.stdout is None:
            raise OSError("SSH stdout pipe is unavailable")
        raw = await process.stdout.read(MAX_LINUX_RESPONSE_BYTES + 1)
        if len(raw) > MAX_LINUX_RESPONSE_BYTES:
            process.kill()
            await process.wait()
            return raw
        return_code = await process.wait()
        if return_code != 0:
            raise OSError("read-only Linux collector failed")
        return raw


class LinuxReadClient:
    """Validate target selection and the typed forced-command response."""

    def __init__(self, registry: LinuxTargetRegistry, transport: LinuxTransport) -> None:
        self._registry = registry
        self._transport = transport

    async def snapshot(self, target_id: str) -> LinuxDiagnosticSnapshot:
        target = self._registry.resolve(target_id)
        raw = await self._transport.collect(target)
        try:
            snapshot = LinuxDiagnosticSnapshot.model_validate(raw)
        except ValidationError as error:
            raise ApplicationError(
                ErrorCode.DEPENDENCY_UNAVAILABLE,
                "connector.linux_response_invalid",
                retryable=True,
            ) from error
        if snapshot.target_id != target.target_id:
            raise ApplicationError(
                ErrorCode.DEPENDENCY_UNAVAILABLE,
                "connector.linux_target_mismatch",
                retryable=False,
            )
        return snapshot


class IncidentEvidenceClient:
    """Collect matching bounded Zabbix and Linux evidence for one approved target."""

    def __init__(
        self,
        registry: LinuxTargetRegistry,
        zabbix_transport: ZabbixTransport,
        linux_client: LinuxReadClient,
        *,
        incident_lookback_minutes: int,
    ) -> None:
        self._registry = registry
        self._zabbix_transport = zabbix_transport
        self._linux_client = linux_client
        self._incident_lookback_minutes = incident_lookback_minutes

    async def evidence(self, target_id: str) -> IncidentEvidence:
        target = self._registry.resolve(target_id)
        zabbix_task = asyncio.create_task(
            ZabbixReadClient(
                target.zabbix_host,
                self._zabbix_transport,
                incident_lookback_minutes=self._incident_lookback_minutes,
            ).incident_context()
        )
        linux_task = asyncio.create_task(self._linux_client.snapshot(target_id))
        try:
            zabbix_context, linux_snapshot = await asyncio.gather(zabbix_task, linux_task)
        except BaseException:
            zabbix_task.cancel()
            linux_task.cancel()
            await asyncio.gather(zabbix_task, linux_task, return_exceptions=True)
            raise
        return IncidentEvidence.combine(target_id, zabbix_context, linux_snapshot)

    async def linux_snapshot(self, target_id: str) -> LinuxDiagnosticSnapshot:
        """Expose the named Linux snapshot without adding a generic transport surface."""

        return await self._linux_client.snapshot(target_id)
