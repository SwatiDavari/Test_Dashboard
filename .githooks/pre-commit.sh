#!/usr/bin/env bash
# qik pre-commit gate — cargo build (Rust changes only), axon needs-graph
# staleness check, algorithmic cortex check, and axon traceability check.
# Called by .githooks/pre-commit (extensionless dispatcher).
# This file carries @needs markers and is scanned by sphinx-codelinks (comment_type: bash).
set -euo pipefail

QIK="${QIK_BIN:-qik}"
if ! command -v "$QIK" &>/dev/null; then
    printf '[qik] pre-commit: "%s" not found — install qik or set QIK_BIN\n' "$QIK" >&2
    exit 1
fi

# @needs Cargo build gate in pre-commit hook, prd_unit_imp__main__precommit_cargo_build, prd_unit_imp, [prd_unit_des__main__precommit_cargo_build], released
if git diff --cached --name-only --diff-filter=ACM | grep -q '\.rs$'; then
    if ! cargo build --workspace; then
        printf '[qik] pre-commit: cargo build failed — fix compile errors before committing\n' >&2
        exit 1
    fi
fi

# @needs Needs-graph staleness gate in pre-commit hook, prd_unit_imp__main__precommit_needs_verify, prd_unit_imp, [prd_unit_des__main__precommit_needs_verify], released
# Runs before cortex/axon check: both read needs.json, a build artifact — if it
# is stale relative to the authored sources, their results describe the old
# graph, not the one actually being committed. Verifying freshness first makes
# every check after it trustworthy instead of silently checking stale data.
if ! "$QIK" axon verify; then
    printf '[qik] pre-commit: needs.json is stale relative to its authored sources — run bash scripts/needs-build.sh before committing\n' >&2
    exit 1
fi

"$QIK" cortex check --kind algo
"$QIK" axon check
