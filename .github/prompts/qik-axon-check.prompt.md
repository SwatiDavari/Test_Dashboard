---
description: 'Verify traceability integrity — orphans, dangling links, coverage gaps. Use after any change to needs or code, or before a release.'
---

<!-- @needs axon quality-gate procedure (Copilot), prd_unit_imp__axon__quality_gate_procedure_copilot, prd_unit_imp, [prd_unit_des__axon__quality_gate_procedure_copilot], released -->

# qik axon check — traceability integrity

Use `mcp_qik-mcp_axon_check` or CLI:

```bash
qik axon check                        # colored output (TTY)
qik axon check --no-color             # parse-safe: no ANSI codes
qik axon check --root /path/to/project
```

> Pass `--no-color` whenever you parse the output (grep, string match, exit-code
> check in a script). The MCP tool is always uncolored JSON — prefer it for
> programmatic use.

Returns a `Report` with statements:
- **error** — hard violations: orphan needs (no upstream link), dangling links
  (target does not exist), rule violations
- **warning** — coverage gaps, incomplete chains

## Workflow

1. Run the check.
2. For each `error`: find the offending need in `needs/`, repair the link or
   upstream reference, re-run.
3. For each `warning`: evaluate whether the gap is acceptable; if not, add the
   missing artefact.
4. Re-run until clean — a commit with open axon errors is a traceability gap.

Also use `mcp_qik-mcp_axon_coverage` for a targeted coverage report on a specific need.
