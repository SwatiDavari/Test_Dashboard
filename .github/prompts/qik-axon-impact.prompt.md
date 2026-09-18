---
description: 'Walk the downstream effect cone of a need — what does changing this artifact trigger? Use before modifying a requirement or design to understand what else must change.'
---

<!-- @needs axon impact procedure (Copilot), prd_unit_imp__axon__impact_procedure_copilot, prd_unit_imp, [prd_unit_des__axon__impact_procedure_copilot], released -->

# qik axon impact — downstream effect

Use `mcp_qik-mcp_axon_impact` or CLI:

```bash
qik axon impact <NEED_ID>
```

Walks downward from `<NEED_ID>` through all reverse links (what links *to* this need).
Returns every artifact that must be re-examined if `<NEED_ID>` changes.

**Always run before modifying a requirement or architecture node** — the result tells
you what design, implementation, and test artefacts are in scope.

**Topology**: by default, only link kinds whose declared topology
is `default = true` are walked — a `relates_to`-style kinship link (topology
`peer`) is excluded unless you pass `--topology peer` or name it explicitly
in `--via`. See `.qik/axon/classify.toml [[topology]]`.

For the full blast radius (both directions), use `/qik-axon-blast`.
