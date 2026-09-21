import shutil
import subprocess
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DOSSIER_DIRECTORY = REPOSITORY_ROOT / "deploy" / "server-dependencies"
EXPECTED_DOSSIERS = {
    "nextops-ai.yaml",
    "nextops-app.yaml",
    "nextops-connectors-ro.yaml",
    "zabbix-server.yaml",
}


def test_server_dossiers_use_the_human_readable_yaml_format() -> None:
    yaml_files = {path.name for path in DOSSIER_DIRECTORY.glob("*.yaml")}
    legacy_json_files = {
        path.name
        for path in DOSSIER_DIRECTORY.glob("*.json")
        if path.name != "server-dependency.schema.json"
    }

    assert yaml_files == EXPECTED_DOSSIERS
    assert legacy_json_files == set()


def test_server_dossiers_validate_against_the_shared_schema() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_deployment_dossiers.py"],
        cwd=REPOSITORY_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert "4 YAML dossiers" in result.stdout
    assert "40 vCPU / 184 GiB RAM / 980 GiB disk" in result.stdout


def test_validator_rejects_duplicate_yaml_keys(tmp_path: Path) -> None:
    temporary_dossiers = tmp_path / "deploy" / "server-dependencies"
    temporary_scripts = tmp_path / "scripts"
    shutil.copytree(DOSSIER_DIRECTORY, temporary_dossiers)
    temporary_scripts.mkdir()
    shutil.copy2(
        REPOSITORY_ROOT / "scripts" / "check_deployment_dossiers.py",
        temporary_scripts,
    )

    app_dossier = temporary_dossiers / "nextops-app.yaml"
    with app_dossier.open("a", encoding="utf-8", newline="\n") as dossier_file:
        dossier_file.write("schema_version: 1.0.0\n")

    result = subprocess.run(
        [sys.executable, "scripts/check_deployment_dossiers.py"],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "duplicate key" in result.stderr
