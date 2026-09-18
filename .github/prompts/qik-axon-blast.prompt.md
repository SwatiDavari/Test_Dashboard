---
description: 'Compute the full blast radius of a need — trace (up) + impact (down) combined. Use when assessing the total scope of a change before implementation.'
---

<!-- @needs axon blast procedure (Copilot), prd_unit_imp__axon__blast_procedure_copilot, prd_unit_imp, [prd_unit_des__axon__blast_procedure_copilot], released -->

# qik axon blast — full blast radius

Use `mcp_qik-mcp_axon_blast` or CLI:

```bash
qik axon blast <NEED_ID>
```

Combines `trace` (upward provenance) and `impact` (downward effect) into a single
connected subgraph. Each result entry carries `direction` and `distance`:
- `[up, 1]` — direct upstream parent
- `[down, 2]` — two hops downstream

**Important**: The two walks are independent one-directional walks that are merged.
Direction never switches at an intermediate node — this is NOT a bidirectional BFS.

**Topology**: every link kind carries a project-declared topology
(`.qik/axon/classify.toml [[topology]]`, e.g. `primary`/`secondary`/`peer`). By
default `blast` walks only topologies marked `default = true` — a symmetric
kinship link like `relates_to` (topology `peer`) is silently excluded unless
you ask for it: pass `--topology peer` (or `--topology primary,secondary,peer`
for everything) or name the link explicitly in `--via`.

## Workflow for change impact assessment

1. Identify the need(s) you plan to change.
2. Run `blast` on each.
3. Read the listed artefacts at their source paths.
4. Update any that drift from the proposed change — never silently; propose the edits.
5. Re-run `mcp_qik-mcp_axon_check` to verify integrity after edits.
