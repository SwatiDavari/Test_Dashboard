# qik axon check — traceability quality-gate procedure


<!-- @needs axon quality-gate procedure (Claude Code), prd_unit_imp__axon__quality_gate_procedure_claude, prd_unit_imp, [prd_unit_des__axon__quality_gate_procedure_claude], released -->
Executed by the **qik-axon** persona (Traceability Auditor).

## When to invoke

After any change to `needs/` files or source code with `@needs` markers. Before
staging a release. Whenever the artifact graph integrity is in question.

## Procedure

### Step 1 — Run the integrity check

```bash
qik axon check --no-color
```

Or via MCP: `axon_check()`. Returns a `Report` grouped by rule.

Every `error` is a hard blocker:
- **orphan** — a need exists with no upstream link; add the missing `links:` entry
- **dangling link** — a link points to a non-existent id; fix the typo or create the missing need
- **rule violation** — a structural graph rule is violated; inspect with `axon_rules()`

Re-run after every fix until **0 error(s)** is reported.

### Step 2 — Coverage check (before release)

For each top-level requirement in the blast radius:

```bash
qik axon coverage <REQ_ID> --no-color
```

Target: `test` or `rc` before staging. `open` and `impl` mean missing test coverage.

### Step 3 — Fingerprint verify

```bash
qik axon verify --no-color
```

Confirms `needs.json` matches the stored stamp. If it reports `change`, the
needs were edited without rebuilding — run `bash scripts/needs-build.sh` first.

### Step 4 — Report

State: errors found/fixed, coverage levels, verify outcome.

## Color / parsing rules

Pass `--no-color` whenever parsing CLI output. MCP tools are always uncolored JSON.
