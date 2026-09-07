#!/usr/bin/env bash
# Local preview for antiAI.robbiemed.org.
# Port 3402 is claimed in /home/user/Projects/PORTS.md — do not change it here alone.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/build_site.py
echo "serving http://127.0.0.1:3402/"
exec python3 -m http.server 3402 --bind 127.0.0.1
