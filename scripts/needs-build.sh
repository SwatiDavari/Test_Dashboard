#!/usr/bin/env bash
# Build this project's qik traceability needs and emit needs.json (the bridge
# format consumed by qik axon). Idempotently provisions a dedicated docs venv.
#
# Usage: scripts/needs-build.sh
# Output: needs/_build/needs/needs.json
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="$ROOT/.venv"
REQ="$ROOT/requirements-docs.txt"

if [[ ! -x "$VENV/bin/sphinx-build" ]]; then
    echo "[needs-build] provisioning docs venv at $VENV"
    python3 -m venv "$VENV"
    "$VENV/bin/pip" install --quiet --upgrade pip
    "$VENV/bin/pip" install --quiet -r "$REQ"
fi

# needs_flow_engine = "graphviz" (needs/conf.py) shells out to the `dot`
# binary for every needflow diagram; a missing binary fails mid-build with a
# generic Sphinx traceback instead of a diagnosable message.
if ! command -v dot &>/dev/null; then
    echo "[needs-build] ERROR: graphviz's 'dot' binary not found on PATH." >&2
    echo "[needs-build] Install it (e.g. apt install graphviz / brew install graphviz), then re-run." >&2
    exit 1
fi

echo "[needs-build] sphinx-build -b needs"
"$VENV/bin/sphinx-build" -b needs -q "$ROOT/needs" "$ROOT/needs/_build/needs"

echo "[needs-build] done: $ROOT/needs/_build/needs/needs.json"
