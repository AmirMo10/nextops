#!/usr/bin/env python3
"""Standalone forced-command collector for bounded read-only Linux evidence."""

from __future__ import annotations

import ipaddress
import json
import os
import pwd
import re
import socket
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

COLLECTOR_VERSION = "1.0.0"
CONFIG_PATH = Path("/etc/nextops/linux-readonly.json")
EXPECTED_ORIGINAL_COMMAND = "nextops-linux-snapshot-v1"
MAX_CONFIG_BYTES = 32_768
MAX_COMMAND_TEXT_BYTES = 131_072
MAX_FILESYSTEMS = 8
MAX_PROCESSES = 10
MAX_SERVICES = 16
MAX_JOURNAL = 25
MAX_SOCKETS = 32
MAX_ROUTES = 16
MAX_NAMESERVERS = 4
UNIT_PATTERN = re.compile(r"^[A-Za-z0-9@_.:-]{1,128}\.service$")
TARGET_PATTERN = re.compile(r"^[a-z][a-z0-9-]{1,31}$")
SECRET_PATTERN = re.compile(r"(?i)(password|passwd|secret|token|api[_-]?key)\s*[:=]\s*([^\s,;]+)")
AUTHORIZATION_PATTERN = re.compile(r"(?i)authorization\s*[:=]\s*(?:bearer\s+)?[^\s,;]+")


class CollectorError(RuntimeError):
    """Safe collector failure without embedding source data."""


def _read_text(path: Path, limit: int = MAX_COMMAND_TEXT_BYTES) -> str:
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        return handle.read(limit + 1)[:limit]


def _load_config(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    if len(raw) > MAX_CONFIG_BYTES:
        raise CollectorError("collector configuration is too large")
    try:
        config = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise CollectorError("collector configuration is invalid") from error
    if not isinstance(config, dict) or set(config) != {
        "schema_version",
        "target_id",
        "filesystems",
        "services",
    }:
        raise CollectorError("collector configuration fields are invalid")
    if config["schema_version"] != "1.0.0":
        raise CollectorError("collector configuration version is unsupported")
    target_id = config["target_id"]
    if not isinstance(target_id, str) or TARGET_PATTERN.fullmatch(target_id) is None:
        raise CollectorError("collector target id is invalid")
    filesystems = config["filesystems"]
    if (
        not isinstance(filesystems, list)
        or not 1 <= len(filesystems) <= MAX_FILESYSTEMS
        or not all(
            isinstance(item, str)
            and item.startswith("/")
            and len(item) <= 256
            and ".." not in Path(item).parts
            for item in filesystems
        )
        or len(set(filesystems)) != len(filesystems)
    ):
        raise CollectorError("collector filesystem allowlist is invalid")
    services = config["services"]
    if (
        not isinstance(services, list)
        or not 1 <= len(services) <= MAX_SERVICES
        or not all(
            isinstance(item, str) and UNIT_PATTERN.fullmatch(item) is not None for item in services
        )
        or len(set(services)) != len(services)
    ):
        raise CollectorError("collector service allowlist is invalid")
    return config


def _run(arguments: list[str], timeout: float = 5.0) -> tuple[int, str]:
    try:
        completed = subprocess.run(
            arguments,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired):
        return 127, ""
    return completed.returncode, completed.stdout[:MAX_COMMAND_TEXT_BYTES]


def _meminfo() -> dict[str, int]:
    values: dict[str, int] = {}
    for line in _read_text(Path("/proc/meminfo")).splitlines():
        key, separator, raw_value = line.partition(":")
        if not separator:
            continue
        fields = raw_value.strip().split()
        if fields and fields[0].isdigit():
            values[key] = int(fields[0]) * 1024
    required = ("MemTotal", "MemAvailable", "SwapTotal", "SwapFree")
    if any(key not in values for key in required):
        raise CollectorError("required memory counters are unavailable")
    return values


def _filesystems(paths: list[str]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    statvfs = os.__dict__.get("statvfs")
    if statvfs is None:
        raise CollectorError("filesystem statistics are unavailable")
    for path in paths:
        stats = statvfs(path)
        total = stats.f_blocks * stats.f_frsize
        available = stats.f_bavail * stats.f_frsize
        used = max(0, total - (stats.f_bfree * stats.f_frsize))
        used_percent = round((used / total) * 100, 2) if total else 0.0
        result.append(
            {
                "path": path,
                "total_bytes": total,
                "available_bytes": available,
                "used_percent": used_percent,
            }
        )
    return result


def _processes(reasons: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for entry in Path("/proc").iterdir():
        if not entry.name.isdigit():
            continue
        try:
            name = _read_text(entry / "comm", 128).strip()
            status = _read_text(entry / "status", 8_192)
            rss_kib = 0
            for line in status.splitlines():
                if line.startswith("VmRSS:"):
                    fields = line.split()
                    rss_kib = int(fields[1]) if len(fields) > 1 else 0
                    break
            if name:
                rows.append(
                    {
                        "pid": int(entry.name),
                        "name": _safe_text(name, 128),
                        "rss_bytes": rss_kib * 1024,
                    }
                )
        except (FileNotFoundError, PermissionError, OSError, ValueError):
            continue
    rows.sort(key=lambda item: (-int(item["rss_bytes"]), int(item["pid"])))
    if len(rows) > MAX_PROCESSES:
        reasons.append("processes_truncated")
    return rows[:MAX_PROCESSES]


def _services(units: list[str]) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for unit in units:
        code, output = _run(
            [
                "/usr/bin/systemctl",
                "show",
                "--no-pager",
                "--property=LoadState",
                "--property=ActiveState",
                "--property=SubState",
                unit,
            ]
        )
        properties = {
            key: value
            for line in output.splitlines()
            if "=" in line
            for key, value in [line.split("=", 1)]
        }
        load_state = properties.get("LoadState", "error" if code else "not-found")
        if load_state not in {"loaded", "not-found", "masked", "error"}:
            load_state = "error"
        result.append(
            {
                "unit": unit,
                "load_state": load_state,
                "active_state": _safe_text(properties.get("ActiveState", "unknown"), 32),
                "sub_state": _safe_text(properties.get("SubState", "unknown"), 32),
            }
        )
    return result


def _journal(units: list[str], reasons: list[str]) -> list[dict[str, Any]]:
    arguments = [
        "/usr/bin/journalctl",
        "--since=-60 minutes",
        "--priority=0..3",
        f"--lines={MAX_JOURNAL + 1}",
        "--output=json",
        "--no-pager",
    ]
    for unit in units:
        arguments.extend(["--unit", unit])
    code, output = _run(arguments, timeout=8.0)
    if code != 0:
        reasons.append("journals_unavailable")
        return []
    rows: list[dict[str, Any]] = []
    for line in output.splitlines():
        try:
            item = json.loads(line)
            if not isinstance(item, dict):
                continue
            micros = int(item.get("__REALTIME_TIMESTAMP", "0"))
            if micros <= 0:
                continue
            message = _safe_text(str(item.get("MESSAGE", "")), 512)
            if not message:
                continue
            rows.append(
                {
                    "unit": _safe_text(
                        str(
                            item.get("_SYSTEMD_UNIT") or item.get("SYSLOG_IDENTIFIER") or "unknown"
                        ),
                        128,
                    ),
                    "priority": min(7, max(0, int(item.get("PRIORITY", "3")))),
                    "observed_at": datetime.fromtimestamp(micros / 1_000_000, UTC).isoformat(),
                    "message": message,
                }
            )
        except (TypeError, ValueError, json.JSONDecodeError, OSError):
            continue
    if len(rows) > MAX_JOURNAL:
        reasons.append("journals_truncated")
    return rows[:MAX_JOURNAL]


def _safe_text(value: str, limit: int) -> str:
    normalized = " ".join(value.replace("\x00", " ").split())
    redacted = AUTHORIZATION_PATTERN.sub("authorization=[REDACTED]", normalized)
    redacted = SECRET_PATTERN.sub(lambda match: f"{match.group(1)}=[REDACTED]", redacted)
    return redacted[:limit]


def _user_counts(reasons: list[str]) -> tuple[int, int]:
    local_users = 0
    getpwall = pwd.__dict__.get("getpwall")
    if getpwall is None:
        raise CollectorError("local user database is unavailable")
    for entry in getpwall():
        if entry.pw_uid >= 1_000 and entry.pw_shell not in {
            "/usr/sbin/nologin",
            "/bin/false",
        }:
            local_users += 1
    code, output = _run(["/usr/bin/who"])
    if code != 0:
        reasons.append("sessions_unavailable")
        return local_users, 0
    return local_users, sum(1 for line in output.splitlines() if line.strip())


def _package_count(reasons: list[str]) -> int:
    code, output = _run(["/usr/bin/dpkg-query", "-W", "-f", "${binary:Package}\n"])
    if code != 0:
        reasons.append("packages_unavailable")
        return 0
    return sum(1 for line in output.splitlines() if line.strip())


def _decode_proc_address(raw: str, family: str) -> str:
    if family == "ipv4":
        return str(ipaddress.IPv4Address(bytes.fromhex(raw)[::-1]))
    packed = bytes.fromhex(raw)
    reordered = b"".join(packed[index : index + 4][::-1] for index in range(0, 16, 4))
    return str(ipaddress.IPv6Address(reordered))


def _listening_sockets(reasons: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path, family in ((Path("/proc/net/tcp"), "ipv4"), (Path("/proc/net/tcp6"), "ipv6")):
        try:
            lines = _read_text(path).splitlines()[1:]
        except OSError:
            continue
        for line in lines:
            fields = line.split()
            if len(fields) < 4 or fields[3] != "0A":
                continue
            raw_address, raw_port = fields[1].split(":", 1)
            try:
                rows.append(
                    {
                        "family": family,
                        "address": _decode_proc_address(raw_address, family),
                        "port": int(raw_port, 16),
                    }
                )
            except (ValueError, ipaddress.AddressValueError):
                continue
    rows.sort(key=lambda item: (str(item["family"]), int(item["port"]), str(item["address"])))
    if len(rows) > MAX_SOCKETS:
        reasons.append("sockets_truncated")
    return rows[:MAX_SOCKETS]


def _routes(reasons: list[str]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    try:
        lines = _read_text(Path("/proc/net/route")).splitlines()[1:]
    except OSError:
        lines = []
    for line in lines:
        fields = line.split()
        if len(fields) < 3:
            continue
        try:
            rows.append(
                {
                    "interface": fields[0][:32],
                    "destination": str(ipaddress.IPv4Address(bytes.fromhex(fields[1])[::-1])),
                    "gateway": str(ipaddress.IPv4Address(bytes.fromhex(fields[2])[::-1])),
                }
            )
        except (ValueError, ipaddress.AddressValueError):
            continue
    if len(rows) > MAX_ROUTES:
        reasons.append("routes_truncated")
    return rows[:MAX_ROUTES]


def _nameservers() -> list[str]:
    result: list[str] = []
    try:
        lines = _read_text(Path("/etc/resolv.conf"), 16_384).splitlines()
    except OSError:
        return result
    for line in lines:
        fields = line.split()
        if len(fields) == 2 and fields[0] == "nameserver":
            try:
                result.append(str(ipaddress.ip_address(fields[1])))
            except ValueError:
                continue
        if len(result) >= MAX_NAMESERVERS:
            break
    return result


def _operating_system() -> str:
    values: dict[str, str] = {}
    try:
        lines = _read_text(Path("/etc/os-release"), 16_384).splitlines()
    except OSError:
        return "Linux"
    for line in lines:
        key, separator, value = line.partition("=")
        if separator:
            values[key] = value.strip().strip('"')
    return _safe_text(values.get("PRETTY_NAME", "Linux"), 256)


def collect(config_path: Path = CONFIG_PATH) -> dict[str, Any]:
    """Collect one deterministic, bounded snapshot using only local read operations."""

    config = _load_config(config_path)
    reasons: list[str] = []
    meminfo = _meminfo()
    try:
        getloadavg = os.__dict__.get("getloadavg")
        if getloadavg is None:
            raise OSError("load averages are unavailable")
        load_1m, load_5m, load_15m = getloadavg()
    except OSError as error:
        raise CollectorError("load averages are unavailable") from error
    uptime_raw = _read_text(Path("/proc/uptime"), 256).split()
    if not uptime_raw:
        raise CollectorError("uptime is unavailable")
    local_users, logged_in_users = _user_counts(reasons)
    snapshot = {
        "source": "linux",
        "collector_version": COLLECTOR_VERSION,
        "target_id": config["target_id"],
        "hostname": _safe_text(socket.gethostname(), 128),
        "operating_system": _operating_system(),
        "collected_at": datetime.now(UTC).isoformat(),
        "uptime_seconds": int(float(uptime_raw[0])),
        "logical_cpu_count": os.cpu_count() or 1,
        "load_1m": round(load_1m, 4),
        "load_5m": round(load_5m, 4),
        "load_15m": round(load_15m, 4),
        "memory_total_bytes": meminfo["MemTotal"],
        "memory_available_bytes": meminfo["MemAvailable"],
        "swap_total_bytes": meminfo["SwapTotal"],
        "swap_free_bytes": meminfo["SwapFree"],
        "filesystems": _filesystems(config["filesystems"]),
        "processes": _processes(reasons),
        "services": _services(config["services"]),
        "journal": _journal(config["services"], reasons),
        "local_user_count": local_users,
        "logged_in_user_count": logged_in_users,
        "installed_package_count": _package_count(reasons),
        "listening_sockets": _listening_sockets(reasons),
        "routes": _routes(reasons),
        "nameservers": _nameservers(),
        "is_partial": bool(reasons),
        "partial_reasons": list(dict.fromkeys(reasons)),
    }
    return snapshot


def main() -> int:
    if sys.argv[1:]:
        print("collector arguments are not accepted", file=sys.stderr)
        return 64
    if os.environ.get("SSH_ORIGINAL_COMMAND") != EXPECTED_ORIGINAL_COMMAND:
        print("collector must run through the approved forced command", file=sys.stderr)
        return 64
    try:
        payload = collect()
    except (CollectorError, OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1
    encoded = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    if len(encoded.encode("utf-8")) > MAX_COMMAND_TEXT_BYTES:
        print("collector output exceeded its bound", file=sys.stderr)
        return 1
    print(encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
