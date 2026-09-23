"""Static safety checks for the native Stage 1B systemd profile."""

from pathlib import Path

ROOT = Path(__file__).parents[2]
SYSTEMD = ROOT / "deploy" / "systemd"
LINUX = ROOT / "deploy" / "linux"
TLS = ROOT / "deploy" / "tls"


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
    assert "Requires=postgresql@16-nextops.service" in unit
    assert "After=network-online.target postgresql@16-nextops.service" in unit
    assert "postgresql.service" not in unit


def test_zabbix_dropin_orders_the_server_around_the_real_database_cluster() -> None:
    dropin = _unit("zabbix-server.service.d/nextops-postgresql.conf")

    assert "Requires=postgresql@16-zabbix.service" in dropin
    assert "After=postgresql@16-zabbix.service" in dropin
    assert "TimeoutStopSec=90s" in dropin


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
    assert "LoadCredential=linux-app-key:" in connector
    assert "LoadCredential=linux-ai-key:" in connector
    assert "LoadCredential=linux-connector-key:" in connector
    assert "LoadCredential=linux-zabbix-key:" in connector
    assert "ConditionPathExists=/etc/nextops/linux-targets.json" in connector
    assert "ConditionPathExists=/etc/nextops/ssh/linux_known_hosts" in connector
    assert "NEXTOPS_LINUX_TARGETS_FILE=/etc/nextops/linux-targets.json" in environment
    assert "NEXTOPS_LINUX_TIMEOUT_SECONDS=15" in environment
    assert "--host 127.0.0.1" in connector
    assert "NEXTOPS_ZABBIX_API_TOKEN=" not in environment
    assert "NEXTOPS_CONNECTOR_SERVICE_SECRET=" not in environment
    assert "User=nextops-api" in tunnel
    assert "LoadCredential=connector-tunnel-key:" in tunnel
    assert "StrictHostKeyChecking=yes" in tunnel
    assert "UserKnownHostsFile=/etc/nextops/ssh/connector_known_hosts" in tunnel
    assert "-L 127.0.0.1:18100:127.0.0.1:8100" in tunnel
    assert "192.168." not in tunnel


def test_phase2_app_exposes_only_logical_incident_target_ids() -> None:
    environment = (SYSTEMD / "nextops-app.env").read_text(encoding="utf-8")

    assert "NEXTOPS_INCIDENT_TARGET_IDS=app,ai,connector,zabbix" in environment
    assert "192.168." not in environment


def test_linux_installer_never_reowns_the_shared_configuration_parent() -> None:
    installer = (LINUX / "install-linux-readonly.sh").read_text(encoding="utf-8")

    assert "if [[ ! -d /etc/nextops ]]" in installer
    assert "install -d -o root -g root -m 0755 /etc/nextops" in installer
    assert "install -d -o root -g nextops-linux-ro -m 0750 /etc/nextops" not in installer


def test_certificate_checker_is_local_least_privilege_and_persistent() -> None:
    service = _unit("nextops-certificate-check.service")
    timer = _unit("nextops-certificate-check.timer")
    example = (ROOT / "deploy" / "tls" / "certificate-check.env.example").read_text(
        encoding="utf-8"
    )

    assert "User=nextops-certcheck" in service
    assert "EnvironmentFile=/etc/nextops/certificate-check.env" in service
    assert "/usr/bin/python3.12" in service
    assert "/usr/local/libexec/nextops/check_certificate_expiry.py" in service
    assert "ProtectSystem=strict" in service
    assert "NoNewPrivileges=yes" in service
    assert "RestrictAddressFamilies=AF_UNIX" in service
    assert "CapabilityBoundingSet=\n" in service
    assert "NEXTOPS_CERTIFICATE_KEY" not in example
    assert "PRIVATE_KEY" not in example
    assert "NEXTOPS_CERTIFICATE_WARNING_DAYS=90" in example
    assert "OnUnitActiveSec=1d" in timer
    assert "Persistent=true" in timer


def test_certificate_installer_preserves_the_private_key_boundary() -> None:
    installer = (TLS / "install-certificate-check.sh").read_text(encoding="utf-8")

    assert "certificate and private key do not match" in installer
    assert 'chown root:nextops-certcheck "$certificate_directory" "$certificate"' in installer
    assert 'chmod 0640 "$certificate"' in installer
    assert 'chown root:root "$private_key"' in installer
    assert 'chmod 0600 "$private_key"' in installer
    assert 'chmod 0710 "$certificate_directory"' in installer
    assert "systemd-analyze verify" in installer
    assert "systemctl enable --now nextops-certificate-check.timer" in installer
    assert "curl " not in installer
    assert "wget " not in installer
    assert "apt " not in installer
    assert "192.168." not in installer
