"""Static safety checks for the native Stage 1B systemd profile."""

from pathlib import Path

ROOT = Path(__file__).parents[2]
SYSTEMD = ROOT / "deploy" / "systemd"


def _unit(name: str) -> str:
    return (SYSTEMD / name).read_text(encoding="utf-8")


def test_llama_unit_is_cpu_only_authenticated_and_loopback_only() -> None:
    unit = _unit("nextops-llama.service")

    assert "User=nextops-ai" in unit
    assert "LoadCredential=llama-api-key:" in unit
    assert "--api-key-file %d/llama-api-key" in unit
    assert "--host 127.0.0.1" in unit
    assert "--parallel 1" in unit
    assert "--gpu-layers 0" in unit
    assert "--no-webui" in unit
    assert "--no-slots" in unit
    assert "IPAddressDeny=any" in unit
    assert "IPAddressAllow=localhost" in unit
    assert "0.0.0.0" not in unit
    assert "CUDA" not in unit
    assert "ROCM" not in unit


def test_units_set_resource_and_filesystem_boundaries() -> None:
    for name in ("nextops-llama.service", "nextops-ai.service"):
        unit = _unit(name)
        assert "CPUQuota=" in unit
        assert "MemoryHigh=" in unit
        assert "MemoryMax=" in unit
        assert "TasksMax=" in unit
        assert "ProtectSystem=strict" in unit
        assert "ProtectHome=yes" in unit
        assert "CapabilityBoundingSet=\n" in unit
        assert "NoNewPrivileges=yes" in unit
        assert "PrivateDevices=yes" in unit
        assert "LimitCORE=0" in unit
        assert "Restart=on-failure" in unit


def test_api_unit_uses_distinct_file_backed_credentials() -> None:
    unit = _unit("nextops-ai.service")
    environment = (SYSTEMD / "nextops-ai.env").read_text(encoding="utf-8")

    assert "LoadCredential=llama-api-key:" in unit
    assert "LoadCredential=inference-service-secret:" in unit
    assert "--host 127.0.0.1" in unit
    assert "--workers 1" in unit
    assert "NEXTOPS_LLAMA_API_KEY=" not in environment
    assert "NEXTOPS_INFERENCE_SERVICE_SECRET=" not in environment
    assert "http://127.0.0.1:8080" in environment
