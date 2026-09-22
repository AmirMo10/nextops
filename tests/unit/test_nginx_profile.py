"""Static security checks for the user-panel reverse proxy profile."""

from pathlib import Path

ROOT = Path(__file__).parents[2]
PROFILE = ROOT / "deploy" / "nginx" / "nextops-app.conf"


def test_app_proxy_requires_tls_and_only_targets_loopback() -> None:
    profile = PROFILE.read_text(encoding="utf-8")

    assert "listen 443 ssl" in profile
    assert "ssl_protocols TLSv1.2 TLSv1.3" in profile
    assert "proxy_pass http://127.0.0.1:8000" in profile
    assert "client_max_body_size 16k" in profile
    assert "Strict-Transport-Security" in profile
    assert "limit_req zone=nextops_login" in profile
    assert "limit_req zone=nextops_assistant" in profile
    assert "assistant/generate|investigate" in profile
    assert "api/v1/(bootstrap|recovery)" in profile
    assert "docs|redoc|openapi" in profile
    assert "192.168." not in profile
