#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "usage: $0 --config PATH --public-key PATH [--apply]" >&2
  exit 64
}

CONFIG_PATH=''
PUBLIC_KEY_PATH=''
APPLY=0
while (($#)); do
  case "$1" in
    --config)
      (($# >= 2)) || usage
      CONFIG_PATH=$2
      shift 2
      ;;
    --public-key)
      (($# >= 2)) || usage
      PUBLIC_KEY_PATH=$2
      shift 2
      ;;
    --apply)
      APPLY=1
      shift
      ;;
    *) usage ;;
  esac
done

[[ $EUID -eq 0 ]] || { echo 'ERROR: run as root' >&2; exit 77; }
[[ -f $CONFIG_PATH && -f $PUBLIC_KEY_PATH ]] || usage

SCRIPT_DIRECTORY=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
REPOSITORY_ROOT=$(cd -- "$SCRIPT_DIRECTORY/../.." && pwd -P)
COLLECTOR_SOURCE="$REPOSITORY_ROOT/scripts/linux_readonly_collector.py"
[[ -f $COLLECTOR_SOURCE ]] || { echo 'ERROR: collector source is missing' >&2; exit 66; }

python3 - "$CONFIG_PATH" <<'PY'
import json
import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
payload = json.loads(path.read_text(encoding="utf-8"))
if set(payload) != {"schema_version", "target_id", "filesystems", "services"}:
    raise SystemExit("ERROR: unexpected collector configuration fields")
if payload["schema_version"] != "1.0.0":
    raise SystemExit("ERROR: unsupported collector configuration version")
if re.fullmatch(r"[a-z][a-z0-9-]{1,31}", payload["target_id"]) is None:
    raise SystemExit("ERROR: invalid target id")
PY

PUBLIC_KEY=$(tr -d '\r\n' < "$PUBLIC_KEY_PATH")
[[ $PUBLIC_KEY =~ ^ssh-ed25519\ [A-Za-z0-9+/=]+\ [A-Za-z0-9._@:-]{1,128}$ ]] || {
  echo 'ERROR: expected one comment-bearing Ed25519 public key' >&2
  exit 65
}

if ((APPLY == 0)); then
  echo 'validation_status=PASS'
  echo 'apply_status=NOT_RUN'
  exit 0
fi

if ! getent group nextops-linux-ro >/dev/null; then
  groupadd --system nextops-linux-ro
fi
if ! id nextops-linux-ro >/dev/null 2>&1; then
  useradd \
    --system \
    --gid nextops-linux-ro \
    --groups systemd-journal \
    --home-dir /var/lib/nextops-linux-ro \
    --create-home \
    --shell /bin/bash \
    nextops-linux-ro
else
  [[ $(id -gn nextops-linux-ro) == nextops-linux-ro ]] || {
    echo 'ERROR: existing collector identity has an unexpected primary group' >&2
    exit 78
  }
  usermod --append --groups systemd-journal nextops-linux-ro
fi
passwd --lock nextops-linux-ro >/dev/null

install -d -o root -g root -m 0755 /usr/local/libexec
install -o root -g root -m 0755 \
  "$COLLECTOR_SOURCE" /usr/local/libexec/nextops-linux-readonly
install -d -o root -g nextops-linux-ro -m 0750 /etc/nextops
install -o root -g nextops-linux-ro -m 0640 \
  "$CONFIG_PATH" /etc/nextops/linux-readonly.json
install -d -o root -g root -m 0755 /var/lib/nextops-linux-ro
install -d -o root -g root -m 0755 /var/lib/nextops-linux-ro/.ssh

AUTHORIZED_KEYS_TEMP=$(mktemp)
trap 'rm -f -- "$AUTHORIZED_KEYS_TEMP"' EXIT
printf 'restrict,command="/usr/local/libexec/nextops-linux-readonly" %s\n' \
  "$PUBLIC_KEY" > "$AUTHORIZED_KEYS_TEMP"
install -o root -g root -m 0644 \
  "$AUTHORIZED_KEYS_TEMP" /var/lib/nextops-linux-ro/.ssh/authorized_keys

SNAPSHOT_TEMP=$(mktemp)
trap 'rm -f -- "$AUTHORIZED_KEYS_TEMP" "$SNAPSHOT_TEMP"' EXIT
runuser -u nextops-linux-ro -- \
  env SSH_ORIGINAL_COMMAND=nextops-linux-snapshot-v1 \
  /usr/local/libexec/nextops-linux-readonly > "$SNAPSHOT_TEMP"
python3 - "$SNAPSHOT_TEMP" <<'PY'
import json
import sys
from pathlib import Path

snapshot = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
required = {"source", "collector_version", "target_id", "collected_at", "is_partial"}
if not required.issubset(snapshot) or snapshot["source"] != "linux":
    raise SystemExit("ERROR: collector self-test returned an invalid snapshot")
PY

echo 'validation_status=PASS'
echo 'apply_status=COMPLETE'
echo 'collector_command=nextops-linux-snapshot-v1'
