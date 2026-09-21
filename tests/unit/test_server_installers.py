from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT))

from deploy.installers.installer import (  # noqa: E402
    ROLE_PACKAGES,
    BundleValidationError,
    InstallerError,
    PackageSpec,
    _blocked_service_start,
    _validate_simulation,
    parse_package_lock,
    verify_bundle,
)


def _write_bundle(bundle: Path, role: str, *, extra_file: bool = False) -> str:
    files = {
        "apt/dists/stable/InRelease": b"signed repository metadata\n",
        "keyrings/nextops-archive-keyring.gpg": b"test public key\n",
        "packages.lock": "".join(
            f"{package}=1.0-1\n" for package in sorted(ROLE_PACKAGES[role])
        ).encode(),
    }
    if extra_file:
        files["unreviewed.deb"] = b"not in the manifest\n"

    for relative_path, contents in files.items():
        target = bundle / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(contents)

    manifest_lines = []
    for relative_path, contents in sorted(files.items()):
        if relative_path == "unreviewed.deb":
            continue
        manifest_lines.append(f"{hashlib.sha256(contents).hexdigest()}  {relative_path}\n")
    manifest = "".join(manifest_lines).encode()
    (bundle / "manifest.sha256").write_bytes(manifest)
    return hashlib.sha256(manifest).hexdigest()


def test_repository_exposes_one_guarded_script_per_server() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_server_installers.py"],
        cwd=REPOSITORY_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "4 guarded server installers" in result.stdout


def test_bundle_verification_accepts_a_complete_authenticated_role_bundle(
    tmp_path: Path,
) -> None:
    bundle = tmp_path / "bundle"
    manifest_digest = _write_bundle(bundle, "nextops-app")

    verified = verify_bundle(bundle, manifest_digest, "nextops-app")

    assert {package.name for package in verified.packages} == ROLE_PACKAGES["nextops-app"]
    assert verified.apt_repository == bundle / "apt"


def test_check_mode_validates_without_requesting_apply_authorization(tmp_path: Path) -> None:
    bundle = tmp_path / "bundle"
    manifest_digest = _write_bundle(bundle, "nextops-app")
    result = subprocess.run(
        [
            sys.executable,
            "deploy/installers/installer.py",
            "--server",
            "nextops-app",
            "--check",
            "--bundle-dir",
            str(bundle),
            "--bundle-manifest-sha256",
            manifest_digest,
        ],
        cwd=REPOSITORY_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "no changes made" in result.stdout


def test_apply_mode_requires_the_explicit_authorization_marker(tmp_path: Path) -> None:
    bundle = tmp_path / "bundle"
    manifest_digest = _write_bundle(bundle, "nextops-ai")
    environment = os.environ.copy()
    environment.pop("NEXTOPS_PROVISIONING_AUTHORIZED", None)
    result = subprocess.run(
        [
            sys.executable,
            "deploy/installers/installer.py",
            "--server",
            "nextops-ai",
            "--apply",
            "--bundle-dir",
            str(bundle),
            "--bundle-manifest-sha256",
            manifest_digest,
            "--change-id",
            "CHG-TEST-001",
        ],
        cwd=REPOSITORY_ROOT,
        check=False,
        capture_output=True,
        text=True,
        env=environment,
    )

    assert result.returncode == 1
    assert "NEXTOPS_PROVISIONING_AUTHORIZED=YES" in result.stderr


def test_package_lock_rejects_unpinned_versions(tmp_path: Path) -> None:
    lock = tmp_path / "packages.lock"
    lock.write_text("ca-certificates\n", encoding="utf-8")

    with pytest.raises(BundleValidationError, match="name=version"):
        parse_package_lock(lock, frozenset({"ca-certificates"}))


def test_package_lock_rejects_duplicate_packages(tmp_path: Path) -> None:
    lock = tmp_path / "packages.lock"
    lock.write_text("ca-certificates=1.0\nca-certificates=1.1\n", encoding="utf-8")

    with pytest.raises(BundleValidationError, match="duplicate package"):
        parse_package_lock(lock, frozenset({"ca-certificates"}))


def test_package_lock_requires_every_direct_role_package(tmp_path: Path) -> None:
    lock = tmp_path / "packages.lock"
    lock.write_text("ca-certificates=1.0\n", encoding="utf-8")

    with pytest.raises(BundleValidationError, match="missing required packages"):
        parse_package_lock(lock, frozenset({"ca-certificates", "python3.12"}))


def test_bundle_rejects_files_outside_the_approved_manifest(tmp_path: Path) -> None:
    bundle = tmp_path / "bundle"
    manifest_digest = _write_bundle(bundle, "nextops-ai", extra_file=True)

    with pytest.raises(BundleValidationError, match="not listed in manifest"):
        verify_bundle(bundle, manifest_digest, "nextops-ai")


def test_bundle_rejects_the_wrong_manifest_trust_anchor(tmp_path: Path) -> None:
    bundle = tmp_path / "bundle"
    _write_bundle(bundle, "nextops-connectors-ro")

    with pytest.raises(BundleValidationError, match="manifest SHA-256"):
        verify_bundle(bundle, "0" * 64, "nextops-connectors-ro")


def test_bundle_rejects_manifest_path_traversal(tmp_path: Path) -> None:
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    manifest = f"{'0' * 64}  ../outside.deb\n".encode()
    (bundle / "manifest.sha256").write_bytes(manifest)

    with pytest.raises(BundleValidationError, match="unsafe relative path"):
        verify_bundle(bundle, hashlib.sha256(manifest).hexdigest(), "nextops-app")


def test_apt_simulation_rejects_an_unlisted_dependency() -> None:
    packages = (PackageSpec("ca-certificates", "1.0-1"),)
    output = (
        "Inst ca-certificates (1.0-1 NextOps:stable [amd64])\n"
        "Inst unreviewed-helper (2.0-1 NextOps:stable [amd64])\n"
    )

    with pytest.raises(InstallerError, match="unlisted package unreviewed-helper"):
        _validate_simulation(output, packages)


def test_apt_simulation_rejects_package_removal() -> None:
    packages = (PackageSpec("ca-certificates", "1.0-1"),)

    with pytest.raises(InstallerError, match="would remove"):
        _validate_simulation("Remv existing-service [1.0-1]\n", packages)


def test_apt_simulation_rejects_a_different_version() -> None:
    packages = (PackageSpec("ca-certificates", "1.0-1"),)

    with pytest.raises(InstallerError, match=r"expected ca-certificates=1.0-1"):
        _validate_simulation(
            "Inst ca-certificates (1.1-1 NextOps:stable [amd64])\n",
            packages,
        )


def test_service_start_guard_is_created_and_removed_unchanged(tmp_path: Path) -> None:
    policy_path = tmp_path / "policy-rc.d"

    with _blocked_service_start(policy_path):
        assert policy_path.read_text(encoding="utf-8").endswith("exit 101\n")

    assert not policy_path.exists()


def test_service_start_guard_never_overwrites_an_existing_policy(tmp_path: Path) -> None:
    policy_path = tmp_path / "policy-rc.d"
    policy_path.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")

    with (
        pytest.raises(InstallerError, match="requires separate review"),
        _blocked_service_start(policy_path),
    ):
        pytest.fail("guard must fail before yielding")

    assert policy_path.read_text(encoding="utf-8") == "#!/bin/sh\nexit 0\n"
