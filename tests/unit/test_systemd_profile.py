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
    assert "Environment=LD_LIBRARY_PATH=/srv/nextops/runtime/llama.cpp/current/bin" in unit
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


def test_app_unit_is_rootless_loopback_only_and_uses_file_backed_credentials() -> None:
    unit = _unit("nextops-app.service")
    environment = (SYSTEMD / "nextops-app.env").read_text(encoding="utf-8")

    assert "User=nextops-api" in unit
    assert "--host 127.0.0.1" in unit
    assert "LoadCredential=database-url:" in unit
    assert "LoadCredential=bootstrap-secret:" in unit
    assert "LoadCredential=recovery-secret:" in unit
    assert "LoadCredential=inference-service-secret:" in unit
    assert "LoadCredential=connector-service-secret:" in unit
    assert "IPAddressDeny=any" in unit
    assert "IPAddressAllow=localhost" in unit
    assert "NEXTOPS_DATABASE_URL=" not in environment
    assert "NEXTOPS_INFERENCE_SERVICE_SECRET=" not in environment
    assert "http://127.0.0.1:18090" in environment
    assert "http://127.0.0.1:18100" in environment


def test_ai_tunnel_uses_pinned_host_restricted_key_and_one_local_forward() -> None:
    unit = _unit("nextops-ai-tunnel.service")

    assert "User=nextops-api" in unit
    assert "LoadCredential=ai-tunnel-key:" in unit
    assert "StrictHostKeyChecking=yes" in unit
    assert "UserKnownHostsFile=/etc/nextops/ssh/ai_known_hosts" in unit
    assert "-L 127.0.0.1:18090:127.0.0.1:8090" in unit
    assert "ExitOnForwardFailure=yes" in unit
    assert "${NEXTOPS_AI_SSH_DESTINATION}" in unit
    assert "192.168." not in unit


def test_connector_is_rootless_authenticated_and_connector_tunnel_is_pinned() -> None:
    connector = _unit("nextops-connector.service")
    tunnel = _unit("nextops-connector-tunnel.service")
    environment = (SYSTEMD / "nextops-connector.env").read_text(encoding="utf-8")

    assert "User=nextops-connector" in connector
    assert "LoadCredential=zabbix-api-token:" in connector
    assert "LoadCredential=connector-service-secret:" in connector
    assert "--host 127.0.0.1" in connector
    assert "NEXTOPS_ZABBIX_API_TOKEN=" not in environment
    assert "NEXTOPS_CONNECTOR_SERVICE_SECRET=" not in environment
    assert "User=nextops-api" in tunnel
    assert "LoadCredential=connector-tunnel-key:" in tunnel
    assert "StrictHostKeyChecking=yes" in tunnel
    assert "UserKnownHostsFile=/etc/nextops/ssh/connector_known_hosts" in tunnel
    assert "-L 127.0.0.1:18100:127.0.0.1:8100" in tunnel
    assert "192.168." not in tunnel
