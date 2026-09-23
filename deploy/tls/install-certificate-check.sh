#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
  printf '%s\n' \
    'Usage: install-certificate-check.sh --certificate ABSOLUTE_PATH --private-key ABSOLUTE_PATH' \
    '       --label SAFE_LABEL --warning-days DAYS --change-id SAFE_CHANGE_ID'
}

die() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 1
}

certificate=''
private_key=''
label=''
warning_days=''
change_id=''

while (($#)); do
  case "$1" in
    --certificate) certificate="${2:-}"; shift 2 ;;
    --private-key) private_key="${2:-}"; shift 2 ;;
    --label) label="${2:-}"; shift 2 ;;
    --warning-days) warning_days="${2:-}"; shift 2 ;;
    --change-id) change_id="${2:-}"; shift 2 ;;
    --help|-h) usage; exit 0 ;;
    *) usage >&2; die 'unsupported argument' ;;
  esac
done

[[ ${EUID} -eq 0 ]] || die 'run as root'
[[ "$certificate" = /* && -f "$certificate" && ! -L "$certificate" ]] \
  || die 'certificate must be an existing absolute regular file'
[[ "$private_key" = /* && -f "$private_key" && ! -L "$private_key" ]] \
  || die 'private key must be an existing absolute regular file'
[[ "$(dirname -- "$certificate")" == "$(dirname -- "$private_key")" ]] \
  || die 'certificate and private key must use the same protected directory'
[[ "$label" =~ ^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$ ]] || die 'label is invalid'
[[ "$change_id" =~ ^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$ ]] || die 'change ID is invalid'
[[ "$warning_days" =~ ^[0-9]+$ ]] || die 'warning days must be an integer'
((10#$warning_days >= 1 && 10#$warning_days <= 3650)) \
  || die 'warning days are outside the supported range'

source_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd -P)"
checker_source="$source_root/scripts/check_certificate_expiry.py"
service_source="$source_root/deploy/systemd/nextops-certificate-check.service"
timer_source="$source_root/deploy/systemd/nextops-certificate-check.timer"
documentation_source="$source_root/docs/requirements/CERTIFICATE_LIFECYCLE_SPEC.md"
[[ -f "$checker_source" && -f "$service_source" && -f "$timer_source" \
  && -f "$documentation_source" ]] \
  || die 'reviewed checker artifacts are incomplete'

command -v /usr/bin/python3.12 >/dev/null || die 'pinned Python 3.12 binary is unavailable'
command -v /usr/bin/openssl >/dev/null || die 'pinned OpenSSL binary is unavailable'
command -v systemd-analyze >/dev/null || die 'systemd-analyze is unavailable'
/usr/bin/openssl x509 -in "$certificate" -noout -dates >/dev/null 2>&1 \
  || die 'certificate validation failed'
key_public_digest="$({ /usr/bin/openssl pkey -in "$private_key" -pubout -outform DER 2>/dev/null \
  || die 'private key validation failed'; } | sha256sum | awk '{print $1}')"
certificate_public_digest="$({ /usr/bin/openssl x509 -in "$certificate" -pubkey -noout 2>/dev/null \
  || die 'certificate public-key extraction failed'; } \
  | /usr/bin/openssl pkey -pubin -outform DER 2>/dev/null \
  | sha256sum | awk '{print $1}')"
[[ "$key_public_digest" == "$certificate_public_digest" ]] \
  || die 'certificate and private key do not match'

if ! getent group nextops-certcheck >/dev/null; then
  groupadd --system nextops-certcheck
fi
if ! id -u nextops-certcheck >/dev/null 2>&1; then
  useradd --system --gid nextops-certcheck --home-dir /nonexistent \
    --shell /usr/sbin/nologin nextops-certcheck
fi

certificate_directory="$(dirname -- "$certificate")"
chown root:nextops-certcheck "$certificate_directory" "$certificate"
chmod 0710 "$certificate_directory"
chmod 0640 "$certificate"
chown root:root "$private_key"
chmod 0600 "$private_key"

install -d -o root -g root -m 0755 /usr/local/libexec/nextops
install -o root -g root -m 0755 "$checker_source" \
  /usr/local/libexec/nextops/check_certificate_expiry.py
install -d -o root -g root -m 0755 /usr/local/share/doc/nextops
install -o root -g root -m 0644 "$documentation_source" \
  /usr/local/share/doc/nextops/CERTIFICATE_LIFECYCLE.md
install -o root -g root -m 0644 "$service_source" \
  /etc/systemd/system/nextops-certificate-check.service
install -o root -g root -m 0644 "$timer_source" \
  /etc/systemd/system/nextops-certificate-check.timer
install -d -o root -g root -m 0755 /etc/nextops

environment_stage="$(mktemp /etc/nextops/.certificate-check.env.XXXXXX)"
trap 'rm -f -- "$environment_stage"' EXIT
{
  printf 'NEXTOPS_CERTIFICATE_PATH=%s\n' "$certificate"
  printf 'NEXTOPS_CERTIFICATE_LABEL=%s\n' "$label"
  printf 'NEXTOPS_CERTIFICATE_WARNING_DAYS=%s\n' "$warning_days"
} >"$environment_stage"
chown root:root "$environment_stage"
chmod 0644 "$environment_stage"
mv -f -- "$environment_stage" /etc/nextops/certificate-check.env

systemd-analyze verify \
  /etc/systemd/system/nextops-certificate-check.service \
  /etc/systemd/system/nextops-certificate-check.timer
systemctl daemon-reload
systemctl enable --now nextops-certificate-check.timer
systemctl start nextops-certificate-check.service

[[ "$(systemctl is-enabled nextops-certificate-check.timer)" == 'enabled' ]] \
  || die 'certificate timer is not enabled'
[[ "$(systemctl is-active nextops-certificate-check.timer)" == 'active' ]] \
  || die 'certificate timer is not active'
[[ "$(systemctl show nextops-certificate-check.service -p Result --value)" == 'success' ]] \
  || die 'certificate check did not succeed'
[[ "$(systemctl show nextops-certificate-check.service -p ExecMainStatus --value)" == '0' ]] \
  || die 'certificate check returned a non-zero status'

printf 'change_id=%s\n' "$change_id"
printf 'certificate_label=%s\n' "$label"
printf 'warning_days=%s\n' "$warning_days"
printf 'certificate_check_result=PASS\n'
printf 'certificate_timer_enabled=enabled\n'
printf 'certificate_timer_active=active\n'
