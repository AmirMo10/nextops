"""Shared, fail-closed engine for NextOps server package installers."""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import os
import re
import stat
import subprocess
import sys
import tempfile
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from itertools import chain
from pathlib import Path, PurePosixPath

ROLE_PACKAGES: dict[str, frozenset[str]] = {
    "nextops-app": frozenset(
        {
            "ca-certificates",
            "libpq5",
            "nginx",
            "postgresql-16",
            "postgresql-client-16",
            "python3.12",
            "python3.12-venv",
        }
    ),
    "nextops-ai": frozenset(
        {
            "build-essential",
            "ca-certificates",
            "cmake",
            "libgomp1",
            "libopenblas-dev",
            "libopenblas0-pthread",
            "ninja-build",
            "pkg-config",
        }
    ),
    "nextops-connectors-ro": frozenset(
        {
            "ca-certificates",
            "python3.12",
            "python3.12-venv",
        }
    ),
    "zabbix-server": frozenset(
        {
            "ca-certificates",
            "nginx",
            "php8.3-fpm",
            "php8.3-pgsql",
            "postgresql-16",
            "postgresql-client-16",
            "zabbix-agent2",
            "zabbix-frontend-php",
            "zabbix-nginx-conf",
            "zabbix-server-pgsql",
            "zabbix-sql-scripts",
        }
    ),
}

_PACKAGE_LINE = re.compile(r"^(?P<name>[a-z0-9][a-z0-9+.-]*)=(?P<version>[0-9][A-Za-z0-9.+:~_-]*)$")
_SHA256 = re.compile(r"^[a-f0-9]{64}$")
_CHANGE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]{2,127}$")
_INSTALL_LINE = re.compile(r"^Inst (?P<name>\S+)(?: \[[^]]+\])? \((?P<version>\S+)(?:\s|\))")
_REQUIRED_BUNDLE_FILES = frozenset(
    {
        "apt/dists/stable/InRelease",
        "keyrings/nextops-archive-keyring.gpg",
        "packages.lock",
    }
)
_COMMAND_ENV = {
    "DEBIAN_FRONTEND": "noninteractive",
    "LC_ALL": "C",
    "PATH": "/usr/sbin:/usr/bin:/sbin:/bin",
}


class InstallerError(RuntimeError):
    """Raised when an installer precondition or package operation fails."""


class BundleValidationError(InstallerError):
    """Raised when an offline bundle does not match its trust anchor or contract."""


@dataclass(frozen=True, order=True)
class PackageSpec:
    """An exact Debian package request."""

    name: str
    version: str

    @property
    def apt_argument(self) -> str:
        return f"{self.name}={self.version}"


@dataclass(frozen=True)
class VerifiedBundle:
    """Paths and package requests from an authenticated offline bundle."""

    root: Path
    apt_repository: Path
    signing_key: Path
    packages: tuple[PackageSpec, ...]


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_package_lock(
    lock_path: Path, required_packages: frozenset[str]
) -> tuple[PackageSpec, ...]:
    """Parse exact package specs and require the role's direct package set."""

    try:
        lines = lock_path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        raise BundleValidationError(f"cannot read package lock: {error}") from error

    packages: dict[str, PackageSpec] = {}
    for line_number, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        match = _PACKAGE_LINE.fullmatch(line)
        if match is None:
            raise BundleValidationError(
                f"packages.lock:{line_number} must use exact name=version syntax"
            )
        package = PackageSpec(match.group("name"), match.group("version"))
        if package.name in packages:
            raise BundleValidationError(
                f"packages.lock:{line_number} has duplicate package {package.name}"
            )
        packages[package.name] = package

    if not packages:
        raise BundleValidationError("packages.lock has no package entries")
    missing = sorted(required_packages - packages.keys())
    if missing:
        raise BundleValidationError(f"packages.lock is missing required packages: {missing}")
    return tuple(sorted(packages.values()))


def _parse_manifest(manifest_path: Path) -> dict[str, str]:
    try:
        lines = manifest_path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        raise BundleValidationError(f"cannot read manifest.sha256: {error}") from error

    entries: dict[str, str] = {}
    for line_number, line in enumerate(lines, start=1):
        digest, separator, relative_name = line.partition("  ")
        if not separator or not _SHA256.fullmatch(digest):
            raise BundleValidationError(
                f"manifest.sha256:{line_number} must use '<sha256>  <relative-path>'"
            )
        path = PurePosixPath(relative_name)
        if (
            not relative_name
            or relative_name.strip() != relative_name
            or path.is_absolute()
            or "\\" in relative_name
            or any(ord(character) < 32 for character in relative_name)
            or any(part in {"", ".", ".."} for part in path.parts)
        ):
            raise BundleValidationError(
                f"manifest.sha256:{line_number} contains an unsafe relative path"
            )
        normalized = path.as_posix()
        if normalized in entries:
            raise BundleValidationError(
                f"manifest.sha256:{line_number} has duplicate path {normalized}"
            )
        entries[normalized] = digest
    if not entries:
        raise BundleValidationError("manifest.sha256 has no file entries")
    return entries


def verify_bundle(
    bundle_directory: Path, expected_manifest_sha256: str, server_id: str
) -> VerifiedBundle:
    """Authenticate every bundle file and parse the role's exact package lock."""

    if server_id not in ROLE_PACKAGES:
        raise BundleValidationError(f"unknown server role: {server_id}")
    expected_digest = expected_manifest_sha256.lower()
    if not _SHA256.fullmatch(expected_digest):
        raise BundleValidationError("expected manifest SHA-256 must be 64 hexadecimal characters")

    try:
        root = bundle_directory.resolve(strict=True)
    except OSError as error:
        raise BundleValidationError(f"offline bundle does not exist: {error}") from error
    if not root.is_dir() or root.is_symlink():
        raise BundleValidationError("offline bundle must be a real directory, not a symlink")

    manifest_path = root / "manifest.sha256"
    if not manifest_path.is_file() or manifest_path.is_symlink():
        raise BundleValidationError("offline bundle is missing a regular manifest.sha256")
    actual_manifest_digest = _sha256_file(manifest_path)
    if actual_manifest_digest != expected_digest:
        raise BundleValidationError(
            "manifest SHA-256 does not match the separately approved trust anchor"
        )

    entries = _parse_manifest(manifest_path)
    missing_records = sorted(_REQUIRED_BUNDLE_FILES - entries.keys())
    if missing_records:
        raise BundleValidationError(f"manifest is missing required records: {missing_records}")

    actual_files: set[str] = set()
    for candidate in root.rglob("*"):
        if candidate.is_symlink():
            raise BundleValidationError(
                f"offline bundle may not contain symlinks: {candidate.relative_to(root)}"
            )
        if not candidate.is_dir() and not candidate.is_file():
            raise BundleValidationError(
                f"offline bundle contains a non-file entry: {candidate.relative_to(root)}"
            )
        if candidate.is_file() and candidate != manifest_path:
            actual_files.add(candidate.relative_to(root).as_posix())

    unlisted = sorted(actual_files - entries.keys())
    missing = sorted(entries.keys() - actual_files)
    if unlisted:
        raise BundleValidationError(f"bundle files not listed in manifest: {unlisted}")
    if missing:
        raise BundleValidationError(f"manifest lists missing bundle files: {missing}")

    for relative_name, approved_digest in entries.items():
        candidate = root.joinpath(*PurePosixPath(relative_name).parts)
        if not candidate.is_file() or candidate.is_symlink():
            raise BundleValidationError(f"manifest target is not a regular file: {relative_name}")
        if _sha256_file(candidate) != approved_digest:
            raise BundleValidationError(f"bundle file checksum mismatch: {relative_name}")

    packages = parse_package_lock(root / "packages.lock", ROLE_PACKAGES[server_id])
    return VerifiedBundle(
        root=root,
        apt_repository=root / "apt",
        signing_key=root / "keyrings" / "nextops-archive-keyring.gpg",
        packages=packages,
    )


def _read_os_release(path: Path = Path("/etc/os-release")) -> dict[str, str]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise InstallerError(f"cannot read {path}: {error}") from error
    values: dict[str, str] = {}
    for line in lines:
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key] = value.strip().strip('"')
    return values


def _validate_apply_authorization(change_id: str | None) -> None:
    if os.environ.get("NEXTOPS_PROVISIONING_AUTHORIZED") != "YES":
        raise InstallerError(
            "apply requires NEXTOPS_PROVISIONING_AUTHORIZED=YES from the approved change window"
        )
    if change_id is None or _CHANGE_ID.fullmatch(change_id) is None:
        raise InstallerError("apply requires a non-secret --change-id with 3-128 safe characters")
    if not hasattr(os, "geteuid") or os.geteuid() != 0:
        raise InstallerError("apply must run as root")

    os_release = _read_os_release()
    if os_release.get("ID") != "ubuntu" or os_release.get("VERSION_ID") != "24.04":
        raise InstallerError("apply is restricted to the approved Ubuntu 24.04 guest baseline")

    detector = Path("/usr/bin/systemd-detect-virt")
    if not detector.is_file():
        raise InstallerError("systemd-detect-virt is required to verify the VM boundary")
    detected = subprocess.run(
        [detector],
        check=False,
        capture_output=True,
        text=True,
        env=_COMMAND_ENV,
    )
    if detected.returncode != 0 or detected.stdout.strip() != "vmware":
        raise InstallerError("apply is restricted to an approved VMware guest")


def _validate_secure_bundle_permissions(root: Path) -> None:
    """Prevent a less-privileged user from swapping files after verification."""

    candidates = chain(reversed(root.parents), (root,), root.rglob("*"))
    for candidate in candidates:
        try:
            metadata = candidate.lstat()
        except OSError as error:
            raise InstallerError(f"cannot inspect offline bundle permissions: {error}") from error
        try:
            relative_name = "." if candidate == root else str(candidate.relative_to(root))
        except ValueError:
            relative_name = str(candidate)
        if stat.S_ISLNK(metadata.st_mode):
            raise InstallerError(f"offline bundle contains symlink: {relative_name}")
        if metadata.st_uid != 0:
            raise InstallerError(f"offline bundle path is not owned by root: {relative_name}")
        if metadata.st_mode & (stat.S_IWGRP | stat.S_IWOTH):
            raise InstallerError(f"offline bundle path is group/world writable: {relative_name}")


def _ensure_postgresql_creation_guard(packages: Sequence[PackageSpec]) -> None:
    if "postgresql-16" not in {package.name for package in packages}:
        return
    config_directory = Path("/etc/postgresql-common")
    config_path = config_directory / "createcluster.conf"
    required_setting = re.compile(r"^\s*create_main_cluster\s*=\s*false\s*(?:#.*)?$", re.MULTILINE)
    if config_path.exists():
        if config_path.is_symlink() or not config_path.is_file():
            raise InstallerError(f"refusing unsafe PostgreSQL cluster guard path: {config_path}")
        try:
            current = config_path.read_text(encoding="utf-8")
        except OSError as error:
            raise InstallerError(f"cannot read PostgreSQL cluster guard: {error}") from error
        if required_setting.search(current) is None:
            raise InstallerError(
                f"{config_path} must set create_main_cluster = false before package installation"
            )
        return

    config_directory.mkdir(mode=0o755, parents=True, exist_ok=True)
    try:
        descriptor = os.open(config_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        with os.fdopen(descriptor, "w", encoding="utf-8") as target:
            target.write(
                "# NextOps package-install guard: database initialization is a separate change.\n"
                "create_main_cluster = false\n"
            )
    except OSError as error:
        raise InstallerError(f"cannot create PostgreSQL cluster guard: {error}") from error


@contextlib.contextmanager
def _blocked_service_start(
    policy_path: Path = Path("/usr/sbin/policy-rc.d"),
) -> Iterator[None]:
    created_inode: int | None = None
    guard_contents = (
        b"#!/bin/sh\n# NextOps: package installation must not start services.\nexit 101\n"
    )

    if policy_path.exists():
        raise InstallerError(
            f"pre-existing {policy_path} requires separate review; it was not modified"
        )
    try:
        descriptor = os.open(policy_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o755)
        with os.fdopen(descriptor, "wb") as target:
            target.write(guard_contents)
        created_inode = policy_path.stat().st_ino
    except OSError as error:
        raise InstallerError(f"cannot create temporary service-start policy: {error}") from error

    try:
        yield
    finally:
        if created_inode is not None:
            try:
                current = policy_path.stat()
                if (
                    current.st_ino == created_inode
                    and stat.S_ISREG(current.st_mode)
                    and policy_path.read_bytes() == guard_contents
                ):
                    policy_path.unlink()
                else:
                    raise InstallerError(
                        f"{policy_path} changed during installation and requires manual review"
                    )
            except OSError as error:
                raise InstallerError(f"could not remove {policy_path}: {error}") from error


def _apt_options(source_path: Path, work_directory: Path) -> list[str]:
    lists = work_directory / "lists"
    archives = work_directory / "archives"
    source_parts = work_directory / "sourceparts"
    (lists / "partial").mkdir(parents=True)
    (archives / "partial").mkdir(parents=True)
    source_parts.mkdir()
    return [
        "-o",
        f"Dir::Etc::sourcelist={source_path}",
        "-o",
        f"Dir::Etc::sourceparts={source_parts}",
        "-o",
        f"Dir::State::lists={lists}",
        "-o",
        f"Dir::Cache::archives={archives}",
        "-o",
        "Acquire::Languages=none",
        "-o",
        "Acquire::Retries=0",
        "-o",
        "Acquire::http::Proxy=false",
        "-o",
        "Acquire::https::Proxy=false",
        "-o",
        "Acquire::AllowInsecureRepositories=false",
        "-o",
        "Acquire::AllowDowngradeToInsecureRepositories=false",
        "-o",
        "APT::Get::List-Cleanup=0",
    ]


def _run_checked(
    command: Sequence[str], *, capture_output: bool = False
) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            check=True,
            capture_output=capture_output,
            text=True,
            env=_COMMAND_ENV,
        )
    except subprocess.CalledProcessError as error:
        detail = (error.stderr or error.stdout or "").strip().splitlines()
        suffix = f": {detail[-1]}" if detail else ""
        raise InstallerError(f"package command failed ({command[0]}){suffix}") from error
    except OSError as error:
        raise InstallerError(f"cannot execute package command {command[0]}: {error}") from error


def _validate_simulation(output: str, packages: Sequence[PackageSpec]) -> None:
    approved = {package.name: package.version for package in packages}
    for line in output.splitlines():
        if line.startswith("Remv "):
            raise InstallerError(f"APT simulation would remove a package: {line}")
        match = _INSTALL_LINE.match(line)
        if match is None:
            continue
        name = match.group("name").split(":", 1)[0]
        version = match.group("version")
        if name not in approved:
            raise InstallerError(f"APT simulation includes unlisted package {name}")
        if approved[name] != version:
            raise InstallerError(
                f"APT simulation selected {name}={version}, expected {name}={approved[name]}"
            )


def install_packages(bundle: VerifiedBundle) -> None:
    """Install only exact packages from the authenticated local repository."""

    if any(character.isspace() for character in str(bundle.root)):
        raise InstallerError("offline bundle path may not contain whitespace")
    apt_get = Path("/usr/bin/apt-get")
    dpkg_query = Path("/usr/bin/dpkg-query")
    if not apt_get.is_file() or not dpkg_query.is_file():
        raise InstallerError("apt-get and dpkg-query are required")

    _ensure_postgresql_creation_guard(bundle.packages)
    with tempfile.TemporaryDirectory(prefix="nextops-apt-") as temporary:
        work_directory = Path(temporary)
        source_path = work_directory / "nextops.sources"
        source_path.write_text(
            "Types: deb\n"
            f"URIs: file:{bundle.apt_repository}\n"
            "Suites: stable\n"
            "Components: main\n"
            f"Signed-By: {bundle.signing_key}\n",
            encoding="utf-8",
        )
        options = _apt_options(source_path, work_directory)
        requested = [package.apt_argument for package in bundle.packages]

        with _blocked_service_start():
            _run_checked([str(apt_get), *options, "update"])
            simulation = _run_checked(
                [
                    str(apt_get),
                    *options,
                    "--simulate",
                    "--no-install-recommends",
                    "--no-remove",
                    "install",
                    *requested,
                ],
                capture_output=True,
            )
            _validate_simulation(simulation.stdout, bundle.packages)
            _run_checked(
                [
                    str(apt_get),
                    *options,
                    "--yes",
                    "--download-only",
                    "--reinstall",
                    "--no-install-recommends",
                    "--no-remove",
                    "install",
                    *requested,
                ]
            )
            _run_checked(
                [
                    str(apt_get),
                    *options,
                    "--yes",
                    "--no-install-recommends",
                    "--no-remove",
                    "-o",
                    "Dpkg::Options::=--force-confold",
                    "install",
                    *requested,
                ]
            )

    for package in bundle.packages:
        installed = _run_checked(
            [str(dpkg_query), "-W", "-f=${Version}", package.name], capture_output=True
        ).stdout.strip()
        if installed != package.version:
            raise InstallerError(f"installed version mismatch for {package.name}: {installed!r}")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Validate or install an authenticated offline Ubuntu package bundle "
            "for one NextOps server."
        )
    )
    parser.add_argument("--server", choices=sorted(ROLE_PACKAGES), required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check", action="store_const", const="check", dest="mode", help="validate only (default)"
    )
    mode.add_argument(
        "--apply", action="store_const", const="apply", dest="mode", help="install exact packages"
    )
    parser.set_defaults(mode="check")
    parser.add_argument(
        "--bundle-dir", type=Path, required=True, help="offline role bundle directory"
    )
    parser.add_argument(
        "--bundle-manifest-sha256",
        required=True,
        help="separately approved SHA-256 of manifest.sha256",
    )
    parser.add_argument(
        "--change-id", help="approved non-secret change record identifier; required with --apply"
    )
    return parser


def main(arguments: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    options = parser.parse_args(arguments)
    try:
        bundle = verify_bundle(
            options.bundle_dir,
            options.bundle_manifest_sha256,
            options.server,
        )
        if options.mode == "check":
            print(
                f"PASS: authenticated {options.server} bundle with "
                f"{len(bundle.packages)} exact packages; no changes made."
            )
            return 0

        _validate_apply_authorization(options.change_id)
        _validate_secure_bundle_permissions(bundle.root)
        install_packages(bundle)
        print(
            f"PASS: installed and verified {len(bundle.packages)} exact packages for "
            f"{options.server}; services remain stopped."
        )
        return 0
    except InstallerError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
