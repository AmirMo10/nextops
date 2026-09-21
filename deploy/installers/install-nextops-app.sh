#!/usr/bin/env bash
set -Eeuo pipefail

readonly SCRIPT_DIR="$(cd -- "$(/usr/bin/dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
exec /usr/bin/python3 "${SCRIPT_DIR}/installer.py" --server nextops-app "$@"
