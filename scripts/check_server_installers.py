"""Validate the repository layout for guarded per-server package installers."""

from __future__ import annotations

import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT))

from deploy.installers.installer import ROLE_PACKAGES  # noqa: E402

EXPECTED_WRAPPERS = {
    "install-nextops-ai.sh": "nextops-ai",
    "install-nextops-app.sh": "nextops-app",
    "install-nextops-connectors-ro.sh": "nextops-connectors-ro",
    "install-zabbix-server.sh": "zabbix-server",
}


class LayoutError(RuntimeError):
    """Raised when installer entrypoints do not match the approved role set."""


def validate_repository(repository_root: Path) -> None:
    installer_directory = repository_root / "deploy" / "installers"
    actual_wrappers = {path.name for path in installer_directory.glob("install-*.sh")}
    if actual_wrappers != EXPECTED_WRAPPERS.keys():
        missing = sorted(EXPECTED_WRAPPERS.keys() - actual_wrappers)
        unexpected = sorted(actual_wrappers - EXPECTED_WRAPPERS.keys())
        raise LayoutError(
            f"installer wrapper set mismatch; missing={missing}, unexpected={unexpected}"
        )
    if ROLE_PACKAGES.keys() != set(EXPECTED_WRAPPERS.values()):
        raise LayoutError("installer role package sets do not match the approved server roles")

    for wrapper_name, role in EXPECTED_WRAPPERS.items():
        wrapper_path = installer_directory / wrapper_name
        try:
            contents = wrapper_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise LayoutError(f"cannot read {wrapper_name}: {error}") from error
        if "\r" in contents:
            raise LayoutError(f"{wrapper_name} must use LF line endings")
        if not contents.startswith("#!/usr/bin/env bash\nset -Eeuo pipefail\n"):
            raise LayoutError(f"{wrapper_name} must enable the guarded Bash baseline")
        expected_exec = f'exec /usr/bin/python3 "${{SCRIPT_DIR}}/installer.py" --server {role} "$@"'
        if contents.count(expected_exec) != 1:
            raise LayoutError(f"{wrapper_name} must invoke exactly the {role} installer")

    engine = (installer_directory / "installer.py").read_text(encoding="utf-8")
    for forbidden in ("shell=True", "curl ", "wget "):
        if forbidden in engine:
            raise LayoutError(f"installer engine contains forbidden operation: {forbidden!r}")


def main() -> int:
    try:
        validate_repository(REPOSITORY_ROOT)
    except (LayoutError, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    package_count = sum(len(packages) for packages in ROLE_PACKAGES.values())
    print(
        f"PASS: 4 guarded server installers declare {package_count} direct packages "
        "and share the offline exact-lock engine."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
